"""Arbeitnow: https://www.arbeitnow.com/api/job-board-api

Free, no key, Germany-focused. Paginated via `links.next`; descriptions are HTML.
Their page says nothing about reuse terms, so poll politely (once a day) and link back.
"""

from datetime import datetime, timezone

from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "arbeitnow"
FIRST_PAGE = "https://www.arbeitnow.com/api/job-board-api"


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
            location_raw=j.get("location"),
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
