"""Map a source's free-text location to one of the places we track: a city, or EU-remote.

Does: recognize the tracked cities (and their common spellings) inside a location string;
recognize remote postings a Berlin resident can take ("Remote (EU)"); say which places
are active. A posting can name several tracked cities ("Berlin; Munich"): `places_of`
returns all of them, `place_of` the first, which is what `job.city` holds (HIR-289).

A city can be tracked without being active. `city_of` recognizes every tracked city (manual
adds keep their real city). Only ACTIVE_CITIES pass the ingest and discover-boards filters
(`active_place`). Active means collected: the list is app/scope.py's, and it holds the
live places and the incubating ones alike (HIR-395). Nothing in this module tells the two
apart, because collection does not; what the public may see is app/queries.py's business.
The scope is Germany, EU-remote, and the cities Chandler has turned on:
San Francisco became active on 2026-11-03 once the held-out eval passed (DECISIONS
2026-11-03, HIR-12), and New York on 2026-11-03 as the first city launched end to end
without a human step (DECISIONS 2026-11-03, HIR-132). Hamburg, Frankfurt and Munich became
active on 2026-11-08, the three cities Chandler named in HIR-165, each launched by that same
automated path. Austin, Boston, London and Amsterdam became active on 2026-11-19, the four
Chandler named in HIR-252; Seattle, Los Angeles, Chicago and San Jose on 2026-11-19 too,
the four named in HIR-302. Turning on a city Chandler has not named is still on the AGENTS.md stop list.

EU-remote (DECISIONS 2026-10-26): a remote posting counts when its location names an
EU-wide region or Germany ("Remote (EMEA)", "Leipzig, Germany (remote)"), or names no
region at all ("Remote", "Anywhere") and the description does not restrict it to a non-EU
country. Both phrasings of that restriction count — imperative ("candidates must be
located in the US") and declarative, the shape a LOCATION section writes ("Remote within
the United States.") — always anchored on a named non-EU country (HIR-109).
A remote posting tied to one other country ("Remote – Spain", "Remote, US") does
not count: it usually needs residence or an employer entity there. A city match wins:
"Berlin or remote" is Berlin. When the location is empty (a careers page without
JSON-LD), the title and strong phrases in the description ("fully remote", "remote-first")
stand in for it.

Does NOT: geocode, handle cities we don't track (returns None), or read time-zone overlap
requirements ("5h overlap with PST" still counts as remote).

Invariant: pure; matching is case-insensitive on whole words.
"""

import re

from app import scope

# "new york" already covers "New York City" and "New York, NY" (whole-word match inside a
# longer string), so only the spellings it does not cover are listed. Bare "ny" is
# deliberately absent: it would tag the whole state, so "Rochester, NY" would read as NYC.
CITIES: dict[str, tuple[str, ...]] = {
    "Berlin": ("berlin",),
    "San Francisco": ("san francisco", "sf bay area", "bay area", "south san francisco"),
    "New York": ("new york", "nyc", "manhattan", "brooklyn"),
    "Hamburg": ("hamburg",),
    "Frankfurt": ("frankfurt",),
    "Munich": ("munich", "münchen", "muenchen"),
    "Austin": ("austin",),
    "Boston": ("boston", "cambridge, ma", "cambridge, massachusetts"),
    "London": ("london",),
    "Amsterdam": ("amsterdam",),
    # HIR-302. Bellevue and Redmond only with their state: both names exist elsewhere in
    # the US. Never a bare "LA": "LA" alone is also Louisiana's code and a word in Spanish
    # and French. San Jose holds the South Bay towns; "Bay Area" alone stays San Francisco.
    "Seattle": ("seattle", "bellevue, wa", "bellevue, washington", "redmond, wa", "redmond, washington"),
    "Los Angeles": ("los angeles", "la, ca", "santa monica"),
    "Chicago": ("chicago",),
    "San Jose": ("san jose", "santa clara", "sunnyvale", "mountain view", "palo alto", "cupertino"),
}

REMOTE_EU = "Remote (EU)"

# Every collected place, live or incubating (HIR-395). The list and each place's state are
# app/scope.py's; a city is switched on, in either state, there.
ACTIVE_CITIES: tuple[str, ...] = scope.places()

# The day each active place started being collected (HIR-232). A place's first weeks hold
# every posting that was already open on that day, all "first seen" at once, so nothing
# that compares two periods may use a period that starts before this date. A newly launched
# city gets its launch day here; tests/test_geo.py fails while an active place has none.
COLLECTING_SINCE: dict[str, str] = {
    "Berlin": "2026-10-18",          # the first live polls
    REMOTE_EU: "2026-10-26",         # DECISIONS 2026-10-26
    "San Francisco": "2026-11-03",   # HIR-12
    "New York": "2026-11-03",        # HIR-132
    "Hamburg": "2026-11-08",         # HIR-165
    "Frankfurt": "2026-11-08",
    "Munich": "2026-11-08",
    "Austin": "2026-11-19",          # HIR-252
    "Boston": "2026-11-19",
    "London": "2026-11-19",
    "Amsterdam": "2026-11-19",
    "Seattle": "2026-11-19",         # HIR-302
    "Los Angeles": "2026-11-19",
    "Chicago": "2026-11-19",
    "San Jose": "2026-11-19",
}

# The region whose daily collection covers each active place (HIR-369): Europe's runs at
# 07:00 Berlin, the US's at 07:00 New York. A newly launched city gets its region here;
# tests/test_geo.py fails while an active place has none.
EUROPE, US = "europe", "us"
REGIONS: tuple[str, ...] = (EUROPE, US)
REGION_OF: dict[str, str] = {
    "Berlin": EUROPE, REMOTE_EU: EUROPE, "Hamburg": EUROPE, "Frankfurt": EUROPE,
    "Munich": EUROPE, "London": EUROPE, "Amsterdam": EUROPE,
    "San Francisco": US, "New York": US, "Austin": US, "Boston": US,
    "Seattle": US, "Los Angeles": US, "Chicago": US, "San Jose": US,
}


def region_places(region: str) -> list[str]:
    """The active places a region's collection covers, in ACTIVE_CITIES order."""
    return [p for p in ACTIVE_CITIES if REGION_OF.get(p) == region]

# Places that share a tracked city's name (HIR-252). Each is a lookbehind and lookahead
# wrapped around the city's match: "London, Ontario", "London, ON" and "New London, CT" are
# not London. The province code is matched in capitals only, so "London, on-site" stays
# London. A bare "London, Canada" is excluded too; listing offices as "London, Canada, US"
# would lose London, which is rarer than the Ontario city.
_NOT_THIS_CITY: dict[str, tuple[str, str]] = {
    "London": (r"(?<!new )", r"(?!,?\s*(?:(?-i:ON)\b|ontario\b|canada\b))"),
    # HIR-302: San José in Costa Rica (a tech hub of its own) and in the Philippines, the
    # towns called "San Jose del ...", and Santa Clara in Cuba are not San Jose; Costa
    # Rica's code is matched in capitals only. Los Ángeles in Chile is not Los Angeles.
    "San Jose": ("", r"(?!\s+del\b)(?!,?\s*(?:(?-i:CR)\b|costa rica\b|philippines\b|cuba\b))"),
    "Los Angeles": ("", r"(?!,?\s*chile\b)"),
}

# "San Jose, CA (Bay Area)" is San Jose, not San Francisco too (HIR-302): when a posting
# names San Jose, San Francisco counts only if the posting still names it once its Bay
# Area wording ("Bay Area", "SF Bay Area", "San Francisco Bay Area") is set aside.
_BAY_AREA = re.compile(r"\b(?:san francisco |sf )?bay area\b", re.I)

_PATTERNS = {city: re.compile(_NOT_THIS_CITY.get(city, ("", ""))[0]
                              + r"\b(" + "|".join(re.escape(a) for a in aliases) + r")\b"
                              + _NOT_THIS_CITY.get(city, ("", ""))[1], re.I)
             for city, aliases in CITIES.items()}

_REMOTE = re.compile(r"\b(remote|remotely|home ?office|work from home|wfh|telecommute|anywhere|worldwide)\b", re.I)

# Regions a Berlin resident can work remotely from. DACH and Germany are subsets of that.
_EU_WIDE = re.compile(
    r"\b(europe|european|eu|eea|emea|dach|cet|cest|germany|deutschland|deutschlandweit|bundesweit)\b", re.I)

# Words that carry no region: what is left of "Fully remote / work from anywhere" after
# removing them is nothing, so that is a no-region remote posting.
_FILLER = frozenset("""
remote remotely fully full 100 first friendly only based position role job work working from home office
homeoffice wfh telecommute anywhere worldwide global globally international distributed or and in
within the any location locations ok possible hybrid flexible timezone timezones time zone zones
""".split())

# Countries a residence sentence can name to put a posting out of reach. No EU region is
# on this list: matching it only ever makes a posting drop out.
_NON_EU_COUNTRY = (r"(?:US|U\.S\.|USA|U\.S\.A\.|United States|Canada|North America"
                   r"|Latin America|LATAM|India|UK|United Kingdom)(?!\w)")

# A description restricting a no-region remote posting to a non-EU country, in either of
# the shapes postings write it (HIR-109): imperative ("candidates must be located in the
# US") and declarative, which is what a LOCATION section uses ("Remote within the United
# States.", "This role is based in Canada"). Every branch is anchored on a named country,
# so "remote within your timezone" never trips it.
# Kept narrow, because none of these says where you live: "US-based company"; a bare
# company fact ("Acme is based in the United States" — the declarative branches need a
# remote/job/person subject, or a LOCATION line of its own); a USD salary band; "visa
# sponsorship is not available"; "overlap with PST".
_NON_EU_ONLY = re.compile(
    r"\b(?:must|need to|needs to|required to|should)\s+(?:be\s+)?"
    r"(?:located|based|resid\w*|living|live)\s+in\s+(?:the\s+)?" + _NON_EU_COUNTRY
    + r"|\bremote\s+(?:with)?in\s+(?:the\s+)?" + _NON_EU_COUNTRY
    + r"|\bremote\s+from\s+(?:the\s+)?" + _NON_EU_COUNTRY
    + r"|(?:^|(?<=[.\n]))\s*(?:based|located)\s+in\s+(?:the\s+)?" + _NON_EU_COUNTRY
    + r"|\b(?:roles?|position|job|candidates?|applicants?|hires?|you)\b[^.;\n]{0,30}?"
      r"\b(?:based|located|residing)\s+in\s+(?:the\s+)?" + _NON_EU_COUNTRY
    + r"|\bauthori[sz]ed to work in the (?:US|U\.S\.|United States)\b"
    + r"|\b(?:US|U\.S\.|USA)[- ]only\b"
    + r"|\b(?:US|U\.S\.) (?:citizens?|residents?|persons?)\b",
    re.I)

# Description phrases strong enough to stand in for an empty location. Plain "remote" is
# not: hybrid postings say "remote days".
_STRONG_REMOTE_TEXT = re.compile(
    r"\b(fully remote|100\s?% remote|remote[- ]first|remote[- ]only|work from anywhere|fully distributed)\b", re.I)


def names_eu_region(location_raw: str | None) -> bool:
    """Does this location string name Germany or an EU-wide region? Source adapters ask
    before adding a remote marker of their own, so they never invent a region."""
    return bool(location_raw and _EU_WIDE.search(location_raw))


def remote_location(location_raw: str | None) -> str:
    """The location to store for a posting its board marks remote in a field of its own
    (Ashby's `workplaceType`, Lever's), so the rules below see a remote posting whatever the
    location text says (HIR-325: ElevenLabs lists ten countries and never writes "remote").

    A location that names a tracked city, or already says remote, is returned unchanged:
    a city match wins anyway, and its own wording is judged as before. Anything else
    becomes one segment, "Remote (United Kingdom, France, Germany)", so `is_remote_eu`
    decides it by the existing rule: Germany or an EU-wide region among the names counts,
    "Remote (United States)" or "Remote (France, Spain)" does not. No location at all is
    plain "Remote", a remote posting naming no region."""
    if not location_raw or not location_raw.strip():
        return "Remote"
    if _cities_in(location_raw) or _REMOTE.search(location_raw):
        return location_raw
    return "Remote (" + re.sub(r"\s*[;|/]\s*", ", ", location_raw.strip()) + ")"


def _cities_in(location_raw: str | None) -> list[str]:
    """Every tracked city the location names, in CITIES order (the San Jose rule applied)."""
    if not location_raw:
        return []
    cities = [c for c, pat in _PATTERNS.items() if pat.search(location_raw)]
    if "San Jose" in cities and "San Francisco" in cities \
            and not _PATTERNS["San Francisco"].search(_BAY_AREA.sub(" ", location_raw)):
        cities.remove("San Francisco")
    return cities


def city_of(location_raw: str | None) -> str | None:
    return (_cities_in(location_raw) or [None])[0]


def _segment_remote(segment: str) -> str | None:
    """One location segment → 'eu' (remote, EU region named), 'open' (remote, no region),
    or None (not remote, or remote tied to another country)."""
    if not _REMOTE.search(segment):
        return None
    if _EU_WIDE.search(segment):
        return "eu"
    rest = [w for w in re.findall(r"[a-zäöüß0-9]+", segment.lower()) if w not in _FILLER]
    return "open" if not rest else None


def _remote_kind(location_raw: str | None, title: str | None, text: str | None) -> str | None:
    if location_raw and location_raw.strip():
        kinds = [_segment_remote(s) for s in re.split(r"[;|/]", location_raw)]
        if "eu" in kinds:
            return "eu"
        return "open" if "open" in kinds else None
    # No location: the title's remote part ("AI Engineer - Remote", "(Remote, EU)"), then
    # the description's strong phrases.
    for piece in re.split(r"[()\[\]|–—]|\s-\s", title or ""):
        kind = _segment_remote(piece)
        if kind:
            return kind
    if text and _STRONG_REMOTE_TEXT.search(text):
        return "open"
    return None


def is_remote_eu(location_raw: str | None, title: str | None = None, text: str | None = None) -> bool:
    kind = _remote_kind(location_raw, title, text)
    if kind == "eu":
        return True
    return kind == "open" and not (text and _NON_EU_ONLY.search(text))


def place_of(location_raw: str | None, title: str | None = None, text: str | None = None) -> str | None:
    """A tracked city, else REMOTE_EU, else None: the first of `places_of`."""
    return (places_of(location_raw, title, text) or [None])[0]


def places_of(location_raw: str | None, title: str | None = None, text: str | None = None) -> list[str]:
    """Every place the posting names, in CITIES order: each tracked city its location
    mentions, or [REMOTE_EU] when it names none and is EU-remote, or []. The first is
    `place_of`; a city match still wins over remote, so "Berlin or remote" is ["Berlin"]
    (HIR-289: a Berlin + Munich posting counts under both)."""
    cities = _cities_in(location_raw)
    if cities:
        return cities
    return [REMOTE_EU] if is_remote_eu(location_raw, title, text) else []


def active_places(location_raw: str | None, title: str | None = None, text: str | None = None) -> list[str]:
    """places_of, keeping only ACTIVE_CITIES."""
    return [p for p in places_of(location_raw, title, text) if p in ACTIVE_CITIES]


def active_place(location_raw: str | None, title: str | None = None, text: str | None = None) -> str | None:
    """The place if it is tracked AND active, else None. This is the filter ingest uses."""
    place = place_of(location_raw, title, text)
    return place if place in ACTIVE_CITIES else None


def active_city(location_raw: str | None) -> str | None:
    """active_place on the location string alone."""
    return active_place(location_raw)
