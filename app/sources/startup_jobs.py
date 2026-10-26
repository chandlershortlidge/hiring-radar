"""startup.jobs API: https://api.startup.jobs/v1/jobs  (Bearer key, 20 req/min)

Terms (their API page): credit Startup Jobs as the source and link titles back to the
job page wherever jobs are shown. Returns jobs from the last 14 days with full descriptions.

Response shape, recorded from a real call (tests/fixtures/feeds/startup_jobs.json):
`{"data": [...], "total_count": int, "has_more": bool, "next_cursor": int}`. A job carries
`id`, `title`, `url`, `description_html`, `published_at`, nested `company` (`name`, `slug`,
`url`) and nested `location` (`city`, `state`, `country`, `country_code`), plus
`employment_type`, `workplace_type`, `roles` and `salary`, which we do not use.

Pagination is keyed on the id of the last job in the page: `next_cursor` repeats that id,
and the next page is the same query with `starting_after=<next_cursor>`. There is no `links`
or `meta` object and no `page`/`offset`/`cursor` parameter — unknown query parameters are
ignored and silently return page 1 again, so a wrong parameter name looks like a one-page
feed rather than an error. `has_more` says whether another page exists.

Ordering is not stable between calls, so pages collected minutes apart can repeat or miss
jobs; dedup at ingest is what makes that harmless.
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
        loc = _get(j, "location")
        location = _get(loc, "name", "city") if isinstance(loc, dict) else loc
        if str(_get(j, "workplace_type", default="")).lower() == "remote":
            # Name the country so geo can judge the region: "Remote (Germany)" counts.
            country = _get(loc, "country") if isinstance(loc, dict) else None
            remote = f"remote, {country}" if country else "remote"
            location = f"{location} ({remote})" if location else f"Remote ({country})" if country else "Remote"
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


def next_url(payload, url: str) -> str | None:
    """The same query advanced one page, or None at the end of the feed."""
    if not isinstance(payload, dict) or not payload.get("has_more"):
        return None
    cursor = payload.get("next_cursor")
    if cursor in (None, ""):
        return None
    parts = urllib.parse.urlsplit(url)
    params = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query) if k != "starting_after"]
    params.append(("starting_after", str(cursor)))
    return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(params)))


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
        url, pages = next_url(payload, url), pages + 1
    return out
