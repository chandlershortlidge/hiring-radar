"""Ashby job boards: https://api.ashbyhq.com/posting-api/job-board/<name>

Public, no key. Provides `descriptionPlain` and `descriptionHtml`. Ids are UUIDs.

A posting has one primary office (`location`) and any number of others
(`secondaryLocations`). All of them are kept, "; "-joined as Greenhouse does, so a posting
whose first office is untracked still maps to a tracked city (HIR-268: Qonto lists Paris
first and Berlin second).
"""

from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "ashby"


def board_url(name: str) -> str:
    return f"https://api.ashbyhq.com/posting-api/job-board/{name}"


def _locations(j: dict) -> str | None:
    """Every office the posting lists, primary first, "; "-joined, each once."""
    places = [j.get("location")] + [s.get("location") for s in j.get("secondaryLocations") or []
                                    if isinstance(s, dict)]
    return "; ".join(dict.fromkeys(p.strip() for p in places if isinstance(p, str) and p.strip())) or None


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
            location_raw=_locations(j),
            description_text=text.strip(),
            posted_at=j.get("publishedAt"),
        ))
    return out


def fetch(name: str, company: str | None = None) -> list[Posting]:
    return parse(fetch_json(board_url(name)), company)
