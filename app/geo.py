"""Map a source's free-text location to one of the places we track: a city, or EU-remote.

Does: recognize the tracked cities (and their common spellings) inside a location string;
recognize remote postings a Berlin resident can take ("Remote (EU)"); say which places
are active.

A city can be tracked without being active. `city_of` recognizes every tracked city (manual
adds keep their real city). Only ACTIVE_CITIES pass the ingest and discover-boards filters
(`active_place`). Making a tracked city active is a deliberate one-line change: San
Francisco waits until Berlin extraction passes the held-out eval (DECISIONS 2026-10-19).

EU-remote (DECISIONS 2026-10-26): a remote posting counts when its location names an
EU-wide region or Germany ("Remote (EMEA)", "Hamburg, Germany (remote)"), or names no
region at all ("Remote", "Anywhere") and the description does not restrict it to a non-EU
country. A remote posting tied to one other country ("Remote – Spain", "Remote, US") does
not count: it usually needs residence or an employer entity there. A city match wins:
"Berlin or remote" is Berlin. When the location is empty (a careers page without
JSON-LD), the title and strong phrases in the description ("fully remote", "remote-first")
stand in for it.

Does NOT: geocode, handle cities we don't track (returns None), or read time-zone overlap
requirements ("5h overlap with PST" still counts as remote).

Invariant: pure; matching is case-insensitive on whole words.
"""

import re

CITIES: dict[str, tuple[str, ...]] = {
    "Berlin": ("berlin",),
    "San Francisco": ("san francisco", "sf bay area", "bay area", "south san francisco"),
}

REMOTE_EU = "Remote (EU)"

ACTIVE_CITIES: tuple[str, ...] = ("Berlin", REMOTE_EU)

_PATTERNS = {city: re.compile(r"\b(" + "|".join(re.escape(a) for a in aliases) + r")\b", re.I)
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

# A description restricting a no-region remote posting to a non-EU country. Kept narrow:
# "US-based company" or "overlap with PST" do not restrict where you live.
_NON_EU_ONLY = re.compile(
    r"\b(?:must|need to|needs to|required to|should)\s+(?:be\s+)?(?:located|based|resid\w*|living|live)\s+in\s+"
    r"(?:the\s+)?(?:US|U\.S\.|USA|United States|Canada|North America|Latin America|LATAM|India|UK|United Kingdom)\b"
    r"|\bauthori[sz]ed to work in the (?:US|U\.S\.|United States)\b"
    r"|\b(?:US|U\.S\.|USA)[- ]only\b"
    r"|\b(?:US|U\.S\.) (?:citizens?|residents?|persons?)\b",
    re.I)

# Description phrases strong enough to stand in for an empty location. Plain "remote" is
# not: hybrid postings say "remote days".
_STRONG_REMOTE_TEXT = re.compile(
    r"\b(fully remote|100\s?% remote|remote[- ]first|remote[- ]only|work from anywhere|fully distributed)\b", re.I)


def city_of(location_raw: str | None) -> str | None:
    if not location_raw:
        return None
    for city, pat in _PATTERNS.items():
        if pat.search(location_raw):
            return city
    return None


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
    """A tracked city, else REMOTE_EU, else None."""
    return city_of(location_raw) or (REMOTE_EU if is_remote_eu(location_raw, title, text) else None)


def active_place(location_raw: str | None, title: str | None = None, text: str | None = None) -> str | None:
    """The place if it is tracked AND active, else None. This is the filter ingest uses."""
    place = place_of(location_raw, title, text)
    return place if place in ACTIVE_CITIES else None


def active_city(location_raw: str | None) -> str | None:
    """active_place on the location string alone."""
    return active_place(location_raw)
