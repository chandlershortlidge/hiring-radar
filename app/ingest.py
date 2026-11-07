"""Put postings into the database: still-listed, repost, new-source sighting, or new job.

Does: for each posting decide, in order —
  1. same (source, source_job_id) already stored → still listed: bump last_seen, nothing else;
  2. same company + near-identical text as an existing job → merge: add a job_source row;
     it's a repost (repost_count+1) only when that source had a *different* id for this job
     and none of those ids is in the current fetch — the earlier listing went away. Only
     board feeds (REPOST_SOURCES) can say that; a second id listed at the same time is a
     concurrent duplicate and just merges;
  3. otherwise insert a new job.
Also applies the title/city filters so feeds' unrelated postings never become rows:
a title needs both an AI/ML domain term and a technical role term. A posting with no
company is dropped here too (HIR-207): dedup matches on company first, so a blank-company
row can never be recognised as a duplicate and every repost of it from another source
becomes a second row. A new job is labelled with its job family (family_of, from the title
alone) as it is inserted.

Does NOT: call the model (see app/pipeline.py), fetch anything, or delete rows.

Invariants: one DB transaction per posting; `job.first_seen` never moves later (a
backdated sighting may move it earlier); `job.last_seen` never moves earlier; a posting that fails the filters is counted, not stored; no row in `job` is ever written with a blank company; every timestamp written is of the form 2026-11-07T15:42:00Z (check_timestamp).
"""

import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app import dedup
from app.geo import active_place, place_of
from app.sources import Posting, registry

# A title is in scope only when it names an AI/ML domain AND a technical role. Either half
# alone is noise: feeds carry "Industrial AI" in sales titles and "Agent" in call-centre and
# retail ones, and plain "Software Engineer" is not what this project measures. Still broad
# within that rule; the taxonomy decides what the skills are later. German domain words
# (KI, Künstliche Intelligenz) are in because the Arbeitsagentur feed carries German titles;
# "Artificial Intelligence" because titles spell AI out too.
DOMAIN_PATTERN = re.compile(
    r"\b(ai|ki|künstliche intelligenz|artificial intelligence|ml|mlops|llmops|llm|genai|generative ai|nlp|deep learning|"
    r"agentic|agent|prompt|machine learning|data scien\w*|applied scientist|research engineer)\b", re.I)

# `applied scientist` and `research engineer` sit in DOMAIN_PATTERN as well: they carry the
# domain in the role name, so they satisfy both halves on their own, as they did before.
ROLE_PATTERN = re.compile(
    r"\b(engineer\w*|developer|scientist|researcher|architect|mlops)\b", re.I)


# Board feeds return a company's whole board on every fetch, so an id missing from the
# fetch was taken down. Everything else returns a sample (search sources, capped or
# windowed aggregators) or isn't a feed (manual adds), so absence there proves nothing
# and never makes a repost. DECISIONS 2026-10-19 "Reposts".
REPOST_SOURCES = registry.BOARD_SOURCES


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# Every timestamp this project stores has exactly this shape: UTC, to the second, ending in
# Z — 2026-11-07T15:42:00Z. SQLite has no date type, so first_seen and last_seen are plain
# text and everything that reads them compares them as text: the open/closed rule in
# app/queries.py (open_clause) and the min()/max() below that move a job's seen window. A
# value in any other format sorts wrong, and silently — an offset ("+00:00") sorts after
# "Z", milliseconds make a longer string that compares as later, and a bare date is shorter
# than every full timestamp, so it looks older than everything. Callers may pass their own
# `when` (scripts/import_legacy.py, scripts/seed_demo.py), so the check sits here, where
# every stored timestamp goes through. HIR-209.
#
# Not applied to job_source.posted_at: that is kept as the feed gave it, in whatever format
# that is (app/sources/__init__.py), and nothing compares it as text.
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def check_timestamp(when: str) -> str:
    """Returns `when` unchanged, or raises ValueError naming what is wrong with it."""
    if not isinstance(when, str) or not _TIMESTAMP.match(when):
        raise ValueError(
            f"timestamp {when!r} is not of the form 2026-11-07T15:42:00Z (UTC, to the second,"
            f" ending in Z). Stored timestamps are compared as text, so another format sorts"
            f" wrong without any error.")
    try:
        datetime.strptime(when, TIMESTAMP_FORMAT)
    except ValueError as e:
        raise ValueError(f"timestamp {when!r} is not a real date or time: {e}") from None
    return when


def in_scope_title(title: str) -> bool:
    return bool(DOMAIN_PATTERN.search(title) and ROLE_PATTERN.search(title))


# Which of five job families a posting belongs to, from the title alone (HIR-186). Every
# stored job already passed in_scope_title, so the title is enough to bucket the pool at no
# model cost; a model-assigned family can replace this later without the column changing.
# First match wins, in list order: `ml-platform` before `ml-engineer` so "ML Platform
# Engineer" is platform, and a title naming two families takes the earlier entry. The same
# rule, in the same order, backfills existing rows in app/migrations/017_job_family.sql;
# tests/test_ingest.py asserts the two agree. See DECISIONS.md "Job family is a title rule
# (v1)" for the accepted misfiles.
FAMILIES = ("ai-engineer", "ml-engineer", "data-scientist", "ml-platform", "research")

# Punctuation becomes a space before the whole-word `mle` test, so "(MLE)" and "MLE, Berlin"
# count. The SQL backfill normalises exactly this set of characters.
_FAMILY_PUNCT = "-/(),."

_FAMILY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("data-scientist", ("data scien", "datenwissenschaft")),
    ("ml-platform", ("mlops", "ml platform", "ml-platform", "ml infra", "platform engineer")),
    ("ml-engineer", ("machine learning engineer", "machine-learning engineer", "ml engineer", "ml-engineer")),
    ("research", ("research", "applied scientist")),
)


def family_of(title: str) -> str:
    low = (title or "").lower()
    padded = low
    for ch in _FAMILY_PUNCT:
        padded = padded.replace(ch, " ")
    padded = f" {padded} "
    for family, needles in _FAMILY_RULES:
        if any(n in low for n in needles):
            return family
        if family == "ml-engineer" and " mle " in padded:
            return family
    return "ai-engineer"


@dataclass
class Report:
    seen: int = 0
    still_listed: int = 0
    merged: int = 0
    reposts: int = 0
    new: int = 0
    skipped_title: int = 0
    skipped_city: int = 0
    skipped_company: int = 0
    new_job_ids: list[int] = field(default_factory=list)

    def line(self) -> str:
        return (f"seen={self.seen} new={self.new} still_listed={self.still_listed} merged={self.merged} "
                f"reposts={self.reposts} skipped_title={self.skipped_title} skipped_city={self.skipped_city} "
                f"skipped_company={self.skipped_company}")


def _candidates(conn: sqlite3.Connection, company: str | None) -> list[dedup.Candidate]:
    # Pull same-company rows only; company_key is applied again in dedup for safety.
    rows = conn.execute(
        "SELECT id, company, title, description_text FROM job WHERE company IS NOT NULL").fetchall()
    ck = dedup.company_key(company)
    return [dedup.Candidate(r["id"], r["company"], r["title"], r["description_text"])
            for r in rows if dedup.company_key(r["company"]) == ck]


def ingest_one(conn: sqlite3.Connection, p: Posting, when: str | None = None,
               require_city: bool = True, found_via: str | None = None,
               trust_title: bool = False, fetched_ids: frozenset[str] | None = None) -> str:
    """Returns one of: still_listed, merged, repost, new, skipped_title, skipped_city,
    skipped_company.

    trust_title skips the title filter — for postings a person chose by hand.
    fetched_ids is every source_job_id in the fetch this posting came from; without it
    (a single posting added by hand) nothing counts as a repost.

    Raises ValueError if `when` is not of the form 2026-11-07T15:42:00Z — a caller's bug,
    not a posting this function can report on (check_timestamp).
    """
    when = check_timestamp(when or now_iso())
    if not trust_title and not in_scope_title(p.title):
        return "skipped_title"
    city = place_of(p.location_raw, p.title, p.description_text)
    if require_city and active_place(p.location_raw, p.title, p.description_text) is None:
        return "skipped_city"
    # Last, so the title and city counts keep meaning what they did. No trust_title-style
    # escape: this is the invariant of DECISIONS 2026-11-06 "A job is never stored without
    # a company". Blank means blank *to dedup* — the same company_key that would have to
    # match it — so punctuation alone ("-", "—") and a bare legal suffix ("GmbH") are
    # refused too: they key to the empty string and so could never match anything either.
    if not dedup.company_key(p.company):
        return "skipped_company"

    with conn:
        if p.source_job_id:
            row = conn.execute("SELECT id, job_id FROM job_source WHERE source=? AND source_job_id=?",
                               (p.source, p.source_job_id)).fetchone()
            if row:
                conn.execute("UPDATE job_source SET last_seen=? WHERE id=?", (when, row["id"]))
                conn.execute("UPDATE job SET last_seen=max(last_seen, ?) WHERE id=?", (when, row["job_id"]))
                return "still_listed"

        match = dedup.find_match(p.company, p.title, p.description_text, _candidates(conn, p.company))
        if match:
            job_id = match.job_id
            other_ids = {r[0] for r in conn.execute(
                "SELECT source_job_id FROM job_source WHERE job_id=? AND source=? AND source_job_id IS NOT ?",
                (job_id, p.source, p.source_job_id))}
            is_repost = (p.source in REPOST_SOURCES and fetched_ids is not None
                         and bool(other_ids) and not other_ids & fetched_ids)
            conn.execute(
                "INSERT INTO job_source (job_id, source, source_job_id, url, found_via, first_seen, last_seen, posted_at)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (job_id, p.source, p.source_job_id or None, p.url or None, found_via, when, when, p.posted_at))
            conn.execute("UPDATE job SET last_seen=max(last_seen, ?), first_seen=min(first_seen, ?) WHERE id=?",
                         (when, when, job_id))
            if is_repost:
                conn.execute("UPDATE job SET repost_count = repost_count + 1 WHERE id=?", (job_id,))
                return "repost"
            return "merged"

        cur = conn.execute(
            "INSERT INTO job (company, title, title_key, city, location_raw, description_text, family, first_seen, last_seen)"
            " VALUES (?,?,?,?,?,?,?,?,?)",
            (p.company, p.title, dedup.title_key(p.title), city, p.location_raw, p.description_text,
             family_of(p.title), when, when))
        job_id = cur.lastrowid
        conn.execute(
            "INSERT INTO job_source (job_id, source, source_job_id, url, found_via, first_seen, last_seen, posted_at)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (job_id, p.source, p.source_job_id or None, p.url or None, found_via, when, when, p.posted_at))
        return f"new:{job_id}"


def ingest(conn: sqlite3.Connection, postings: list[Posting], when: str | None = None,
           require_city: bool = True) -> Report:
    """Ingest one feed's fetch. `postings` must be the whole fetch: repost detection reads
    which ids it contains, in any order."""
    r = Report()
    fetched_ids = frozenset(p.source_job_id for p in postings if p.source_job_id)
    for p in postings:
        r.seen += 1
        outcome = ingest_one(conn, p, when, require_city, fetched_ids=fetched_ids)
        if outcome.startswith("new:"):
            r.new += 1
            r.new_job_ids.append(int(outcome[4:]))
        elif outcome == "repost":
            r.reposts += 1
            r.merged += 1
        else:
            setattr(r, outcome, getattr(r, outcome) + 1)
    return r


def store_screenshot(conn: sqlite3.Connection, job_id: int, data: bytes, sha256: str, media_type: str) -> None:
    """Keep the image so stage 1 can be re-run; one per job, replaced if re-added."""
    with conn:
        conn.execute("INSERT OR REPLACE INTO screenshot (job_id, sha256, media_type, bytes) VALUES (?,?,?,?)",
                     (job_id, sha256, media_type, data))


def job_id_for_screenshot(conn: sqlite3.Connection, sha256: str) -> int | None:
    row = conn.execute("SELECT job_id FROM screenshot WHERE sha256=?", (sha256,)).fetchone()
    return row["job_id"] if row else None
