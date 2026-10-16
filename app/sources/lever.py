"""Lever postings: https://api.lever.co/v0/postings/<token>?mode=json

Public, no key. Ships `descriptionPlain` plus `lists` (bulleted sections with HTML content);
we join both so requirement bullets are not lost. Ids are UUIDs.
"""

from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "lever"


def board_url(token: str) -> str:
    return f"https://api.lever.co/v0/postings/{token}?mode=json"


def _text(j: dict) -> str:
    parts = [j.get("descriptionPlain") or html_to_text(j.get("description") or "")]
    for section in j.get("lists") or []:
        parts.append(section.get("text", ""))
        parts.append(html_to_text(section.get("content") or ""))
    if j.get("additionalPlain"):
        parts.append(j["additionalPlain"])
    return "\n".join(p for p in parts if p).strip()


def parse(payload: list, company: str | None = None) -> list[Posting]:
    out = []
    for j in payload:
        text = _text(j)
        if not text or not j.get("text"):
            continue
        created = j.get("createdAt")
        out.append(Posting(
            source=SOURCE,
            source_job_id=str(j["id"]),
            url=j.get("hostedUrl", ""),
            company=company,
            title=j["text"].strip(),
            location_raw=(j.get("categories") or {}).get("location"),
            description_text=text,
            posted_at=_ms_to_iso(created) if created else None,
        ))
    return out


def _ms_to_iso(ms: int) -> str:
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(token: str, company: str | None = None) -> list[Posting]:
    return parse(fetch_json(board_url(token)), company)
