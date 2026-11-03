"""Arbeitnow: https://www.arbeitnow.com/api/job-board-api

Free, no key, Germany-focused. Paginated via `links.next`; descriptions are HTML.
Their page says nothing about reuse terms, so poll politely (once a day) and link back.
"""

import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from app.geo import city_of, names_eu_region
from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "arbeitnow"
FIRST_PAGE = "https://www.arbeitnow.com/api/job-board-api"

# The feed's own placeholder for "this posting names no place", which it sends in English
# on every one of its localized hosts. It is not employer text: a posting that says
# "Remote" or "Homeoffice" wrote that itself and keeps passing through untouched.
_NO_PLACE = "remote job"

# Arbeitnow serves one country per host, and the posting's `url` says which (HIR-111).
# Only a country the board itself runs a site for appears here; an unknown host names none.
_HOST_COUNTRY = {
    "www.arbeitnow.com": "Germany",
    "www.arbeitnow.ch": "Switzerland",
    "www.arbeitnow.nl": "Netherlands",
    "www.arbeitnow.co.uk": "United Kingdom",
    "www.arbeitnow.fr": "France",
}

_SLUG_TAIL = re.compile(r"-([a-z0-9]+-[a-z0-9]+)-\d+$", re.I)


def _slug_place(slug: str | None) -> str | None:
    """A slug ends in the posting's place and its id ("...-senior-zurich-312397"). The last
    two words before the id are the only window read, so a city named in the *title* part of
    a slug can't stand in for the place; two words, because tracked cities have two-word
    names ("san-francisco")."""
    m = _SLUG_TAIL.search(slug or "")
    return m.group(1).replace("-", " ") if m else None


def _location(j: dict) -> str | None:
    """`remote: true` becomes part of the location so geo can see it — but the country is
    never invented. Arbeitnow is German-facing, not German-only: its `location` is a bare
    place name with no country, and the pool holds Swiss, Dutch and UK postings ("Zürich",
    "Amsterdam", "Bromley") alongside German ones. So "Germany" is added only where the feed
    itself says so: an empty location (the posting is remote and nothing more is known, and
    arbeitnow's own jurisdiction is the only region on offer), or a location that already
    names Germany or an EU-wide region, which only needs the word "remote" to read as remote
    there. Every other location passes through untouched and `app/geo.py` judges it; a bare
    non-tracked city then matches nothing and ingest drops it on the city filter (HIR-98).

    The one location that cannot pass through is the feed's own placeholder, "Remote job":
    every word of it is filler to geo, so it reads as a remote posting naming no region at
    all and becomes EU-remote wherever the job really is (HIR-111). For those the place
    comes out of the posting's own URL, which is the only other thing that carries it — the
    host names the country and the slug ends in the city. A tracked city wins (geo's rule:
    "Berlin or remote" is Berlin); otherwise the host's country goes in, and geo judges it
    exactly as it judges a feed that says "Remote, UK" itself. The placeholder is read that
    way whatever the `remote` flag says, because the string itself is the feed's statement
    that no place is named — passing it through is the one thing that is never right."""
    loc = j.get("location")
    if loc and loc.strip().casefold() == _NO_PLACE:
        city = city_of(_slug_place(str(j.get("slug") or "")))
        if city:
            return f"{city} (remote)"
        country = _HOST_COUNTRY.get(urlparse(j.get("url") or "").netloc)
        return f"Remote ({country})" if country else "Remote (Germany)"
    if j.get("remote") is not True:
        return loc
    if not loc:
        return "Remote (Germany)"
    if names_eu_region(loc):
        return f"{loc} (remote)"
    return loc


def parse(payload: dict) -> list[Posting]:
    out = []
    for j in payload.get("data", []):
        text = html_to_text(j.get("description") or "")
        if not text or not j.get("title"):
            continue
        created = j.get("created_at")
        out.append(Posting(
            source=SOURCE,
            source_job_id=str(j["slug"]),
            url=j.get("url", ""),
            company=j.get("company_name"),
            title=j["title"].strip(),
            location_raw=_location(j),
            description_text=text,
            posted_at=datetime.fromtimestamp(created, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if isinstance(created, (int, float)) else None,
        ))
    return out


def next_url(payload: dict) -> str | None:
    return (payload.get("links") or {}).get("next")


def fetch(max_pages: int = 5) -> list[Posting]:
    out, url, pages = [], FIRST_PAGE, 0
    while url and pages < max_pages:
        payload = fetch_json(url)
        out.extend(parse(payload))
        url, pages = next_url(payload), pages + 1
    return out
