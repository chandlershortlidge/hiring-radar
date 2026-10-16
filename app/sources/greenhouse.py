"""Greenhouse job boards: https://boards-api.greenhouse.io/v1/boards/<token>/jobs?content=true

Public, no key. `content` is HTML-escaped HTML. Ids are numeric and stable.
"""

import html

from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "greenhouse"


def board_url(token: str) -> str:
    return f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"


def parse(payload: dict, company: str | None = None) -> list[Posting]:
    out = []
    for j in payload.get("jobs", []):
        content = html_to_text(html.unescape(j.get("content") or ""))
        if not content or not j.get("title"):
            continue
        out.append(Posting(
            source=SOURCE,
            source_job_id=str(j["id"]),
            url=j.get("absolute_url", ""),
            company=company or j.get("company_name"),
            title=j["title"].strip(),
            location_raw=(j.get("location") or {}).get("name"),
            description_text=content,
            posted_at=j.get("first_published") or j.get("updated_at"),
        ))
    return out


def fetch(token: str, company: str | None = None) -> list[Posting]:
    return parse(fetch_json(board_url(token)), company)
