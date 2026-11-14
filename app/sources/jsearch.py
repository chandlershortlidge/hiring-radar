"""JSearch: Google for Jobs as an API (postings from LinkedIn, Indeed, Glassdoor, StepStone,
company career pages), sold by OpenWeb Ninja and, as the same API, on RapidAPI.

Keys and hosts:
- OpenWeb Ninja: `GET https://api.openwebninja.com/jsearch/search`, header `x-api-key`.
- RapidAPI: `GET https://jsearch.p.rapidapi.com/search`, headers `X-RapidAPI-Key` and
  `X-RapidAPI-Host: jsearch.p.rapidapi.com`.
`JSEARCH_API_KEY` holds the key; `JSEARCH_HOST` (`openwebninja` default, or `rapidapi`)
says where it is from.

Budget: the free plan is 200 requests a month, hard limit. One request = one results page
(~10 postings). Keep `num_pages` at 1 per feed and poll once a day: each feed is ~30
requests a month, so five feeds (three German, two New York since HIR-255) is ~150.

Query: `query` is free text ("AI engineer in Berlin"); `country` (ISO code), `date_posted`
(`all`, `today`, `3days`, `week`, `month`), `page`, `num_pages`.

Response: `{"status": "OK", "request_id": ..., "parameters": {...}, "data": [...]}`. A job
carries `job_id`, `job_title`, `employer_name`, `job_description` (plain text),
`job_apply_link`, `job_google_link`, `job_city`, `job_location`, `job_country`,
`job_posted_at_datetime_utc`, `job_publisher`, plus salary/benefit fields we do not use.

What a real response has that the docs' sample did not show (HIR-41, from the recorded
response below):
- `job_city` and `job_country` are null on most postings (8 of 10), so the location
  usually comes from `job_location`.
- `job_location` is not "Berlin, Germany" but the text Google shows, in the search's
  language, with the publisher appended: "Berlin     •  über LinkedIn"; a region-less
  remote posting is "Beliebiger Ort   •  über XING" ("Anywhere" only on English searches).
  Geo still reads the city out of it; the suffix is stored as it comes.
- `job_uid` is the stable part of `job_id` as a field of its own (see `stable_id` below;
  equal on all 10 recorded postings). `stable_id` stays the source of the id, because the
  field is undocumented and stored ids must not change if it disappears.
- `job_posted_at_datetime_utc` is a date at midnight, never a time of day.
- `parameters` echoes a `language: "de"` we did not send.
- Also present, and unused by us: `apply_options`, `job_highlights`,
  `job_employment_type(s)`, `job_posted_at`, `job_posted_at_timestamp`,
  `job_latitude`/`job_longitude`, `employer_logo`, `employer_website`.
Not checked: the docs name both `/jsearch/search` and `/jsearch/search-v2`. We call
`/jsearch/search` and the daily polls return postings from it; whether v2 differs is
unknown, and finding out costs a request nobody has asked to spend.

Fixtures: tests/fixtures/feeds/jsearch_recorded.json is a real response (recorded
2026-11-01, query "machine learning engineer in Berlin", `request_id` blanked). The
hand-built jsearch.json is gone (HIR-41): the degenerate records a real response does not
contain (no apply link, no city, empty description) are made in the test from a real
recorded posting with that field removed. tests/fixtures/feeds/jsearch_learn4good.json
stays hand-built because no recorded learn4good response exists yet (HIR-107) and
fetching a live one would spend part of the 200-request/month budget.

Aggregator headlines are dropped, in either of two shapes seen live. JobLeads hands Google
its search-result headline instead of the posting's own title, with the listing date
appended — "AI / Machine Learning Engineer II arbeitnow SumUp Berlin, Berlin, Germany ·
10/28/2026" (HIR-96). learn4good wedges its own board name between the real title and the
real company with no date in the title at all — "AI/ML Engineer arbeitnow Melotech"; its
date is in the description body instead (HIR-107). Both name themselves, or an unrelated
firm, as `employer_name` ("Primetime", website primetime.company). The real company
appears only inside the title, so neither field can be recovered and normalizing the
company would not help: dedup would still see a different company and store a second copy
of a posting we already have — and even the simpler-looking learn4good shape is not always
a clean split (one real example carries a leftover fragment past the company name), so a
parsed-out title risks being subtly wrong rather than merely absent. A title that ends in a
date is on its own a reliable signature; a title with "arbeitnow" wedged in the middle only
counts alongside a known-aggregator `employer_name`, since the word alone can appear in a
real title. `parse` skips both. Nothing is lost — the same posting always comes back
elsewhere under its own publisher with the right title and company.

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

# A title with the board's own name wedged in the middle, i.e. text on both sides of the
# word. Not reliable alone — a real title could mention the board — so it is only trusted
# together with a known-aggregator `employer_name` below.
_WEDGED_PUBLISHER = re.compile(r".+\barbeitnow\b.+", re.IGNORECASE | re.DOTALL)

# employer_name values seen standing in for the real employer on a headline row (HIR-96
# JobLeads, HIR-107 learn4good). Both used the same one; add to this set only from a row
# actually seen live, not a guess at who else might do this.
_AGGREGATOR_EMPLOYER_NAMES = {"primetime"}


def is_headline(title: str, employer_name: str | None = None) -> bool:
    """True when the "title" is an aggregator's search-result headline rather than the
    posting's own title, in either shape seen live. A title ending in the date it was
    listed (JobLeads) is a signature on its own — a real job title never ends in a date.
    A title with the board's name wedged between other text on both sides (learn4good)
    only counts when `employer_name` is also a known aggregator identity, since the wedge
    alone is not reliable. Either shape's `employer_name` is the aggregator's, not the
    employer's, so the whole posting is unusable."""
    if _TRAILING_DATE.search(title):
        return True
    return bool(
        employer_name
        and employer_name.strip().lower() in _AGGREGATOR_EMPLOYER_NAMES
        and _WEDGED_PUBLISHER.search(title))


def _location(j: dict, country: str | None = None) -> str | None:
    """`job_is_remote: true` becomes "Remote (<country>)" so geo can judge the region;
    otherwise the city, then the location text.

    The country is the posting's own `job_country`, else the country the search was run
    in. For a US posting only a real `job_city` is kept beside it: JSearch fills
    `job_location` with "Anywhere" for region-less remote postings, and geo reads a bare
    "Anywhere" as remote-from-the-EU — so a US search's remote jobs landed in Remote (EU)
    (seen live on the first New York search, HIR-255)."""
    loc = j.get("job_city") or j.get("job_location")
    if j.get("job_is_remote") is True:
        where = j.get("job_country") or (country.upper() if country else None)
        if where == "US":
            return "; ".join(x for x in (j.get("job_city"), f"Remote ({where})") if x)
        where = {"DE": "Germany"}.get(where, where)
        return "; ".join(x for x in (loc, f"Remote ({where})" if where else "Remote") if x)
    return loc


def parse(payload, country: str | None = None) -> list[Posting]:
    items = payload.get("data") if isinstance(payload, dict) else None
    out = []
    for j in items or []:
        title, text, job_id = j.get("job_title"), (j.get("job_description") or "").strip(), j.get("job_id")
        if not title or not text or not job_id:
            continue
        title = str(title).strip()
        if is_headline(title, j.get("employer_name")):
            continue
        out.append(Posting(
            source=SOURCE,
            source_job_id=stable_id(str(job_id)),
            url=j.get("job_apply_link") or j.get("job_google_link") or "",
            company=j.get("employer_name"),
            title=title,
            location_raw=_location(j, country),
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
    return parse(fetch_json(url, headers=headers, timeout=60), country)
