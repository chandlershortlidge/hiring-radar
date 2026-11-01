"""JSearch: Google for Jobs as an API (postings from LinkedIn, Indeed, Glassdoor, StepStone,
company career pages), sold by OpenWeb Ninja and, as the same API, on RapidAPI.

Keys and hosts:
- OpenWeb Ninja: `GET https://api.openwebninja.com/jsearch/search`, header `x-api-key`.
- RapidAPI: `GET https://jsearch.p.rapidapi.com/search`, headers `X-RapidAPI-Key` and
  `X-RapidAPI-Host: jsearch.p.rapidapi.com`.
`JSEARCH_API_KEY` holds the key; `JSEARCH_HOST` (`openwebninja` default, or `rapidapi`)
says where it is from.

Budget: the free plan is 200 requests a month, hard limit. One request = one results page
(~10 postings). Keep `num_pages` at 1 per feed and poll once a day: two feeds a day is
~60 requests a month.

Query: `query` is free text ("AI engineer in Berlin"); `country` (ISO code), `date_posted`
(`all`, `today`, `3days`, `week`, `month`), `page`, `num_pages`.

Response: `{"status": "OK", "request_id": ..., "parameters": {...}, "data": [...]}`. A job
carries `job_id`, `job_title`, `employer_name`, `job_description` (plain text),
`job_apply_link`, `job_google_link`, `job_city`, `job_location`, `job_country`,
`job_posted_at_datetime_utc`, `job_publisher`, plus salary/benefit fields we do not use.

Fixtures: tests/fixtures/feeds/jsearch_recorded.json is a real response (recorded
2026-11-01, query "machine learning engineer in Berlin"). tests/fixtures/feeds/jsearch.json
stays hand-built, for the degenerate records a real response does not contain (no apply
link, no city, empty description).

Aggregator headlines are dropped. Some publishers (seen with JobLeads) hand Google their
search-result headline instead of the posting's own title — "AI / Machine Learning
Engineer II arbeitnow SumUp Berlin, Berlin, Germany · 10/28/2026" — and name themselves,
or an unrelated firm, as `employer_name` ("Primetime", website primetime.company). The
real company appears only inside that headline, so neither field can be recovered and
normalizing the company would not help: dedup would still see a different company and
store a second copy of a posting we already have. A title that ends in a date is the
signature; `parse` skips those records. Nothing is lost — the same SumUp posting came back
in the same response under its own publisher with the right title and company (HIR-96).

`job_id` is not stable: it is base64 of `<docid>:<per-request token>`, and the token changes
on every call (seen live 2026-10-18: one StepStone posting under four ids in two polls,
each counted as a repost). The `<docid>` part is stable, so that is the source_job_id.

The same posting often also arrives from arbeitnow, a board feed, or the Arbeitsagentur;
dedup at ingest merges those (same company, similar text).
"""

import base64
import binascii
import os
import re
import urllib.parse

from app.sources import Posting, fetch_json

SOURCE = "jsearch"
HOSTS = {
    "openwebninja": ("https://api.openwebninja.com/jsearch/search", "x-api-key", {}),
    "rapidapi": ("https://jsearch.p.rapidapi.com/search", "X-RapidAPI-Key",
                 {"X-RapidAPI-Host": "jsearch.p.rapidapi.com"}),
}


def stable_id(job_id: str) -> str:
    """The stable part of a JSearch job_id: the decoded text before the first ':'.
    Returns job_id unchanged when it does not decode to that shape."""
    try:
        raw = base64.b64decode(job_id + "=" * (-len(job_id) % 4), validate=True).decode("ascii")
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return job_id
    head, sep, _ = raw.partition(":")
    return head if sep and head else job_id


_TRAILING_DATE = re.compile(
    r"[\s·•|,-]*(\d{1,2}[/.]\d{1,2}[/.]\d{2,4}|\d{4}-\d{2}-\d{2})\s*$")


def is_headline(title: str) -> bool:
    """True when the "title" is an aggregator's search-result headline rather than the
    posting's own title. A headline ends with the date it was listed; a job title never
    does. Such a record's `employer_name` is the aggregator's, not the employer's, so the
    whole posting is unusable."""
    return bool(_TRAILING_DATE.search(title))


def _location(j: dict) -> str | None:
    """`job_is_remote: true` becomes "Remote (<country>)" so geo can judge the region;
    otherwise the city, then the location text."""
    loc = j.get("job_city") or j.get("job_location")
    if j.get("job_is_remote") is True:
        where = j.get("job_country")
        where = {"DE": "Germany"}.get(where, where)
        return "; ".join(x for x in (loc, f"Remote ({where})" if where else "Remote") if x)
    return loc


def parse(payload) -> list[Posting]:
    items = payload.get("data") if isinstance(payload, dict) else None
    out = []
    for j in items or []:
        title, text, job_id = j.get("job_title"), (j.get("job_description") or "").strip(), j.get("job_id")
        if not title or not text or not job_id:
            continue
        title = str(title).strip()
        if is_headline(title):
            continue
        out.append(Posting(
            source=SOURCE,
            source_job_id=stable_id(str(job_id)),
            url=j.get("job_apply_link") or j.get("job_google_link") or "",
            company=j.get("employer_name"),
            title=title,
            location_raw=_location(j),
            description_text=text,
            posted_at=j.get("job_posted_at_datetime_utc"),
        ))
    return out


def request(query: str, country: str | None, date_posted: str | None, page: int, num_pages: int,
            host: str, key: str) -> tuple[str, dict]:
    """The URL and headers for one search call. Pure."""
    if host not in HOSTS:
        raise ValueError(f"JSEARCH_HOST must be one of {sorted(HOSTS)}, not {host!r}")
    base, key_header, extra = HOSTS[host]
    params = {"query": query, "page": page, "num_pages": num_pages}
    if country:
        params["country"] = country
    if date_posted:
        params["date_posted"] = date_posted
    return f"{base}?{urllib.parse.urlencode(params)}", {key_header: key, **extra}


def fetch(query: str, country: str | None = "de", date_posted: str | None = "week",
          num_pages: int = 1, api_key: str | None = None, host: str | None = None) -> list[Posting]:
    key = api_key or os.environ.get("JSEARCH_API_KEY")
    if not key:
        raise RuntimeError("JSEARCH_API_KEY is not set")
    url, headers = request(query, country, date_posted, 1, num_pages,
                           host or os.environ.get("JSEARCH_HOST", "openwebninja"), key)
    return parse(fetch_json(url, headers=headers, timeout=60))
