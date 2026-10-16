"""Ashby job boards: https://api.ashbyhq.com/posting-api/job-board/<name>

Public, no key. Provides `descriptionPlain` and `descriptionHtml`. Ids are UUIDs.
"""

from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "ashby"


def board_url(name: str) -> str:
    return f"https://api.ashbyhq.com/posting-api/job-board/{name}"


def parse(payload: dict, company: str | None = None) -> list[Posting]:
    out = []
    for j in payload.get("jobs", []):
        text = j.get("descriptionPlain") or html_to_text(j.get("descriptionHtml") or "")
        if not text or not j.get("title"):
            continue
        out.append(Posting(
            source=SOURCE,
            source_job_id=str(j["id"]),
            url=j.get("jobUrl", ""),
            company=company,
            title=j["title"].strip(),
            location_raw=j.get("location"),
            description_text=text.strip(),
            posted_at=j.get("publishedAt"),
        ))
    return out


def fetch(name: str, company: str | None = None) -> list[Posting]:
    return parse(fetch_json(board_url(name)), company)
