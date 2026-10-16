"""startup.jobs API: https://api.startup.jobs/v1/jobs  (Bearer key, 20 req/min)

Terms (their API page): credit Startup Jobs as the source and link titles back to the
job page wherever jobs are shown. Returns jobs from the last 14 days with full descriptions.
The exact response shape is taken from their OpenAPI spec at first use; `parse` is written
defensively and the fixture in tests/ records what we have actually seen.
"""

import os
import urllib.parse

from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "startup_jobs"
BASE = "https://api.startup.jobs/v1/jobs"


def _get(j: dict, *keys, default=None):
    for k in keys:
        if isinstance(j, dict) and k in j and j[k] not in (None, ""):
            return j[k]
    return default


def parse(payload) -> list[Posting]:
    items = payload.get("data", payload.get("jobs", [])) if isinstance(payload, dict) else payload
    out = []
    for j in items:
        title = _get(j, "title", "name")
        desc = _get(j, "description_html", "description", "content", default="")
        text = html_to_text(desc)
        if not title or not text:
            continue
        company = _get(j, "company_name")
        if company is None:
            company = _get(_get(j, "company", default={}), "name")
        location = _get(j, "location")
        if isinstance(location, dict):
            location = _get(location, "name", "city")
        out.append(Posting(
            source=SOURCE,
            source_job_id=str(_get(j, "id", "slug")),
            url=_get(j, "url", "apply_url", default=""),
            company=company,
            title=str(title).strip(),
            location_raw=location,
            description_text=text,
            posted_at=_get(j, "published_at", "created_at", "posted_at"),
        ))
    return out


def next_url(payload) -> str | None:
    if isinstance(payload, dict):
        links = payload.get("links") or {}
        return links.get("next") or (payload.get("meta") or {}).get("next")
    return None


def fetch(search: str, country: str | None = None, max_pages: int = 3, api_key: str | None = None) -> list[Posting]:
    key = api_key or os.environ.get("STARTUP_JOBS_API_KEY")
    if not key:
        raise RuntimeError("STARTUP_JOBS_API_KEY is not set")
    params = {"search": search}
    if country:
        params["country"] = country
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    out, pages = [], 0
    while url and pages < max_pages:
        payload = fetch_json(url, headers={"Authorization": f"Bearer {key}"})
        out.extend(parse(payload))
        url, pages = next_url(payload), pages + 1
    return out
