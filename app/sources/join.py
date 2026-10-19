"""JOIN company boards: https://join.com/companies/<slug>

No API. JOIN pages are Next.js, and each one embeds its data as JSON in
`<script id="__NEXT_DATA__">` under `props.pageProps.initialState` (robots.txt allows
crawling `/companies/`). Two kinds of page (shapes recorded from live pages, 2026-10-19):
- company page `/companies/<slug>?page=N` → `jobs.items` (title, `idParam`, `createdAt`,
  `city`, `workplaceType`, but no description) and `jobs.pagination` (`page`, `pageCount`),
  five jobs per page;
- job page `/companies/<slug>/<idParam>` → `job` with the HTML `description`.

`idParam` is `<number>-<title slug>`. Its number is the id in the public URL; the
`id` field is a different, internal number. The URL number is the source_job_id so that
`check` can look a pasted URL up directly.

Pages can overlap (the same job seen on page 1 and page 2), so listings are deduplicated by
idParam. One request per job page: a company board is small, but every job costs a fetch.

tests/fixtures/feeds/join_*.json are trimmed `initialState` objects from those pages.

Does NOT filter by title or city (ingest does), or read JOIN's site-wide job search.
"""

import json
import re

from app.html_text import html_to_text
from app.sources import Posting, fetch_text

SOURCE = "join"
BASE = "https://join.com/companies"
_NEXT_DATA = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)


def page_state(markup: str) -> dict:
    """A JOIN page's `initialState`, or {} when the page carries none."""
    m = _NEXT_DATA.search(markup)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))["props"]["pageProps"]["initialState"] or {}
    except (ValueError, KeyError, TypeError):
        return {}


def listing(state: dict) -> tuple[list[str], int]:
    """A company page's state → (idParams on this page, total page count)."""
    jobs = state.get("jobs") or {}
    ids = [i["idParam"] for i in jobs.get("items") or [] if i.get("idParam")]
    return ids, int((jobs.get("pagination") or {}).get("pageCount") or 0)


def _location(job: dict) -> str | None:
    city = (job.get("city") or (job.get("office") or {}).get("city") or {})
    place = ", ".join(p for p in (city.get("cityName"), city.get("countryName")) if p) or None
    if job.get("workplaceType") == "REMOTE":
        return f"{place} (remote)" if place else "Remote"
    return place


def parse(state: dict, slug: str, company: str | None = None) -> Posting | None:
    """A job page's state → a Posting, or None when it has no title or description."""
    job = state.get("job") or {}
    text = html_to_text(job.get("description") or "")
    title = (job.get("title") or "").strip()
    id_param = job.get("idParam") or ""
    if not text or not title or not id_param:
        return None
    return Posting(
        source=SOURCE,
        source_job_id=id_param.split("-", 1)[0],
        url=f"{BASE}/{slug}/{id_param}",
        company=company or (job.get("company") or {}).get("name"),
        title=title,
        location_raw=_location(job),
        description_text=text,
        posted_at=job.get("createdAt"),
    )


def fetch(slug: str, company: str | None = None, max_pages: int = 10) -> list[Posting]:
    ids, page, pages = [], 1, 1
    while page <= min(pages, max_pages):
        found, pages = listing(page_state(fetch_text(f"{BASE}/{slug}?page={page}")))
        ids += found
        page += 1
    out = []
    for id_param in dict.fromkeys(ids):
        p = parse(page_state(fetch_text(f"{BASE}/{slug}/{id_param}")), slug, company)
        if p:
            out.append(p)
    return out
