"""Put postings into the database: still-listed, repost, new-source sighting, or new job.

Does: for each posting decide, in order —
  1. same (source, source_job_id) already stored → still listed: bump last_seen, nothing else;
  2. same company + near-identical text as an existing job → merge: add a job_source row;
     if that source already had a *different* id for this job, it's a repost (repost_count+1);
  3. otherwise insert a new job.
Also applies the title/city filters so feeds' unrelated postings never become rows.

Does NOT: call the model (see app/pipeline.py), fetch anything, or delete rows.

Invariants: one DB transaction per posting; `job.first_seen` never moves later;
`job.last_seen` never moves earlier; a posting that fails the filters is counted, not stored.
"""

import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app import dedup
from app.geo import city_of
from app.sources import Posting

# Titles we treat as in-scope. Deliberately broad; the taxonomy decides what counts later.
TITLE_PATTERN = re.compile(
    r"\b(ai|ml|machine learning|llm|genai|generative ai|nlp|data scien|deep learning|"
    r"agentic|agent|applied scientist|research engineer|prompt)\b", re.I)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def in_scope_title(title: str) -> bool:
    return bool(TITLE_PATTERN.search(title))


@dataclass
class Report:
    seen: int = 0
    still_listed: int = 0
    merged: int = 0
    reposts: int = 0
    new: int = 0
    skipped_title: int = 0
    skipped_city: int = 0
    new_job_ids: list[int] = field(default_factory=list)

    def line(self) -> str:
        return (f"seen={self.seen} new={self.new} still_listed={self.still_listed} merged={self.merged} "
                f"reposts={self.reposts} skipped_title={self.skipped_title} skipped_city={self.skipped_city}")


def _candidates(conn: sqlite3.Connection, company: str | None) -> list[dedup.Candidate]:
    # Pull same-company rows only; company_key is applied again in dedup for safety.
    rows = conn.execute(
        "SELECT id, company, title, description_text FROM job WHERE company IS NOT NULL").fetchall()
    ck = dedup.company_key(company)
    return [dedup.Candidate(r["id"], r["company"], r["title"], r["description_text"])
            for r in rows if dedup.company_key(r["company"]) == ck]


def ingest_one(conn: sqlite3.Connection, p: Posting, when: str | None = None,
               require_city: bool = True, found_via: str | None = None) -> str:
    """Returns one of: still_listed, merged, repost, new, skipped_title, skipped_city."""
    when = when or now_iso()
    if not in_scope_title(p.title):
        return "skipped_title"
    city = city_of(p.location_raw)
    if require_city and city is None:
        return "skipped_city"

    with conn:
        if p.source_job_id:
            row = conn.execute("SELECT id, job_id FROM job_source WHERE source=? AND source_job_id=?",
                               (p.source, p.source_job_id)).fetchone()
            if row:
                conn.execute("UPDATE job_source SET last_seen=? WHERE id=?", (when, row["id"]))
                conn.execute("UPDATE job SET last_seen=max(last_seen, ?) WHERE id=?", (when, row["job_id"]))
                return "still_listed"

        match = dedup.find_match(p.company, p.description_text, _candidates(conn, p.company))
        if match:
            job_id = match.job_id
            same_source_other_id = conn.execute(
                "SELECT 1 FROM job_source WHERE job_id=? AND source=? AND source_job_id IS NOT ?",
                (job_id, p.source, p.source_job_id)).fetchone() is not None
            conn.execute(
                "INSERT INTO job_source (job_id, source, source_job_id, url, found_via, first_seen, last_seen, posted_at)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (job_id, p.source, p.source_job_id or None, p.url or None, found_via, when, when, p.posted_at))
            conn.execute("UPDATE job SET last_seen=max(last_seen, ?) WHERE id=?", (when, job_id))
            if same_source_other_id:
                conn.execute("UPDATE job SET repost_count = repost_count + 1 WHERE id=?", (job_id,))
                return "repost"
            return "merged"

        cur = conn.execute(
            "INSERT INTO job (company, title, title_key, city, location_raw, description_text, first_seen, last_seen)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (p.company, p.title, dedup.title_key(p.title), city, p.location_raw, p.description_text, when, when))
        job_id = cur.lastrowid
        conn.execute(
            "INSERT INTO job_source (job_id, source, source_job_id, url, found_via, first_seen, last_seen, posted_at)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (job_id, p.source, p.source_job_id or None, p.url or None, found_via, when, when, p.posted_at))
        return f"new:{job_id}"


def ingest(conn: sqlite3.Connection, postings: list[Posting], when: str | None = None,
           require_city: bool = True) -> Report:
    r = Report()
    for p in postings:
        r.seen += 1
        outcome = ingest_one(conn, p, when, require_city)
        if outcome.startswith("new:"):
            r.new += 1
            r.new_job_ids.append(int(outcome[4:]))
        elif outcome == "repost":
            r.reposts += 1
            r.merged += 1
        else:
            setattr(r, outcome, getattr(r, outcome) + 1)
    return r
