"""Arbeitnow: https://www.arbeitnow.com/api/job-board-api

Free, no key, Germany-focused. Paginated via `links.next`; descriptions are HTML.
Their page says nothing about reuse terms, so poll politely (once a day) and link back.
"""

from datetime import datetime, timezone

from app.geo import names_eu_region
from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "arbeitnow"
FIRST_PAGE = "https://www.arbeitnow.com/api/job-board-api"


def _location(j: dict) -> str | None:
    """`remote: true` becomes part of the location so geo can see it — but the country is
    never invented. Arbeitnow is German-facing, not German-only: its `location` is a bare
    place name with no country, and the pool holds Swiss, Dutch and UK postings ("Zürich",
    "Amsterdam", "Bromley") alongside German ones. So "Germany" is added only where the feed
    itself says so: an empty location (the posting is remote and nothing more is known, and
    arbeitnow's own jurisdiction is the only region on offer), or a location that already
    names Germany or an EU-wide region, which only needs the word "remote" to read as remote
    there. Every other location passes through untouched and `app/geo.py` judges it; a bare
    non-tracked city then matches nothing and ingest drops it on the city filter (HIR-98)."""
    loc = j.get("location")
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
