"""Source adapters: turn a job board's feed into a list of Postings.

Does: define the Posting shape every adapter produces, and the tiny HTTP helper they
share. Each adapter module exposes `parse(payload) -> list[Posting]` (pure, tested on
fixtures) and `fetch(...) -> list[Posting]` (thin I/O wrapper).

Does NOT: touch the database, dedup, filter by title or city, or call a model. Adapters
return everything the feed returns; filtering is ingest's job.

Invariants: `source_job_id` is the source's own stable id for the posting; `description_text`
is plain text (HTML stripped); every Posting has a non-empty description_text and title.
"""

import json
import urllib.request
from dataclasses import dataclass

USER_AGENT = "hiring-radar/0.1 (personal job-market research)"


@dataclass(frozen=True)
class Posting:
    source: str
    source_job_id: str
    url: str
    company: str | None
    title: str
    location_raw: str | None
    description_text: str
    posted_at: str | None = None  # ISO 8601 as the source gave it, if at all


def fetch_json(url: str, headers: dict | None = None, timeout: int = 30):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def fetch_text(url: str, headers: dict | None = None, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace")
