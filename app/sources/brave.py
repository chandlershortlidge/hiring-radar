"""Brave Search web results, used only to find company job boards (`discover-boards`).

Not a job feed: it returns URLs, never Postings.

API (checked against Brave's docs, 2026-10-19): `GET https://api.search.brave.com/res/v1/web/search`
with header `X-Subscription-Token: <key>`; `q` is the query (operators such as `site:` go
inside it), `count` is results per page (max 20). Result URLs are `web.results[].url`.
Pricing per Brave's pricing page: $5 per 1,000 requests, with $5 of credit a month. One
query = one request; we fetch one page per query.

`BRAVE_API_KEY` holds the key (.env).

Fixtures RECORDED from live calls on 2026-10-19, not hand-built:
tests/fixtures/search/brave.json (`site:jobs.ashbyhq.com "AI engineer" Berlin`, 20 results
trimmed to 5) and brave_zero.json (a nonsense term, 0 results). Shape facts from them:
`site:` is applied (`query.search_operators.sites`); a hit carries top-level
`type: "search"`, `query`, `mixed`, `web`; a zero-result response has `type`, `query`,
`mixed` and NO `web` key at all.

Does NOT: page through results, rank or filter URLs (app/discover.py does), or cache.

Invariant: `parse` returns [] only for the recorded zero-result shape (`type: "search"` and
a `query`, no `web`). Anything else without `web.results` raises ShapeError, so a changed
response shape never reads as "no results".
"""

import os
import urllib.parse

from app.sources import fetch_json

ENDPOINT = "https://api.search.brave.com/res/v1/web/search"


class MissingKey(RuntimeError):
    pass


class ShapeError(RuntimeError):
    pass


def api_key() -> str:
    key = os.environ.get("BRAVE_API_KEY", "").strip()
    if not key:
        raise MissingKey("BRAVE_API_KEY is not set: add it to .env (see .env.example)")
    return key


def parse(payload: dict) -> list[str]:
    """A web-search response → its result URLs, in rank order."""
    if isinstance(payload, dict) and "web" not in payload and payload.get("type") == "search" \
            and isinstance(payload.get("query"), dict):
        return []   # Brave's zero-result shape (brave_zero.json)
    try:
        results = payload["web"]["results"]
    except (KeyError, TypeError):
        raise ShapeError(f"no web.results in Brave response (keys: {sorted(payload or {})})") from None
    return [r["url"] for r in results if isinstance(r, dict) and r.get("url")]


def search_url(query: str, count: int = 20) -> str:
    return f"{ENDPOINT}?{urllib.parse.urlencode({'q': query, 'count': count})}"


def fetch(query: str, key: str, count: int = 20) -> list[str]:
    return parse(fetch_json(search_url(query, count), headers={"X-Subscription-Token": key,
                                                               "Accept": "application/json"}))
