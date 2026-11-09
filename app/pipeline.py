"""Run stage 2 over stored jobs that have no skills yet, and persist the results.

Does: find jobs whose `extracted_version` is not the current one, extract, and write
skill_mention + proposed_skill rows and the job's seniority / German / degree, then stamp the job. One job per transaction.

Each run is also one LangSmith trace with a child per job, carrying that job's tokens,
cost and whether the evidence the model quoted was really in the posting (app/grounding.py,
app/langsmith_live.py, HIR-160). Tracing is off unless LANGSMITH_API_KEY is set, and a
LangSmith failure never fails a run.

Does NOT: fetch postings, dedup, or decide which taxonomy to use (passed in). The model
and the call that reaches it are passed in too, but both have a default — the real stage-2
call against the current model — because every caller outside the tests wants exactly that
(HIR-210).

Invariants: a job holds exactly one extraction (the latest; older rows are replaced on
re-extract) but every extraction also appends a permanent `extraction_log` row, which is
never replaced — the current answer is what the dashboard reads, the log is the record of
every reading we paid for (HIR-170); a job is processed once per extractor_version, including jobs with zero skills; a failed extraction leaves the job unstamped and no partial rows, and is reported,
not raised; re-running is safe. The grounding check is measured and never enforced: a
quote the extractor kept is stored whatever the check says, so the poll cannot come to a
different answer from the eval about the same posting. A read that comes back with nothing at all is counted on
the job (`blank_extractions`) and the posting is deleted on the second one — try twice,
then drop (HIR-172, Chandler's decision of 5 Nov). The two must be consecutive: storing a
successful extraction resets the count to 0 in the same transaction that stamps the job, so
a reading that worked clears the blank before it (HIR-199). Migration 015's comment says the
count is never reset and is wrong on that point; a committed migration is never edited, so
this docstring and the DECISIONS entry of 6 Nov are the current rule. Every other failure is retried for ever,
since it says nothing about the posting. Only one extraction runs per database at a time: a second
run (a poll started while an add is extracting, say) skips instead of paying for the same jobs
twice, and its jobs stay pending for the next run. A version bump re-reads only jobs that are
still open (the dashboard's open rule, queries.open_clause): closed jobs keep the skills and
version stamp of their day, and a repost seen again counts as open and re-enters the queue
(HIR-195). A job never read at all is read whatever its status — a first read is not a re-read.
"""

import contextlib
import fcntl
import hashlib
import json
import sqlite3
from dataclasses import dataclass, field

from app import langsmith_live
from app.extract import (
    DEFAULT_MODEL, EmptyExtractionError, Extraction, extract, extraction_input, extractor_version, make_client)
from app.grounding import grounding
from app.ingest import now_iso
from app.queries import open_clause
from app.taxonomy import Taxonomy

BLANK_READ_LIMIT = 2   # reads that come back with nothing at all before the posting is dropped
ALL_BLANK_MIN = 3      # a run at least this big where no job yields a single skill is an outage, not sparse postings


@dataclass
class ExtractReport:
    attempted: int = 0
    succeeded: int = 0
    failed: list[tuple[int, str]] = field(default_factory=list)
    mentions: int = 0
    proposed: int = 0
    skipped_busy: bool = False
    dropped: list[tuple[int, str]] = field(default_factory=list)
    logged: int = 0
    reread_queued: int = 0     # stale-stamped jobs in this run's queue (still open)
    skipped_closed: int = 0    # stale-stamped jobs left out because they are closed (HIR-195)
    # Grounding over this run's quotes: how many snippets the model offered as evidence,
    # and how many were really in the posting (app/grounding.py). Counted, never acted on
    # — a quote the extractor kept is stored whatever this says (HIR-160).
    quotes: int = 0
    grounded: int = 0

    @property
    def grounding_failures(self) -> int:
        """Quotes this run could not find in the posting they came from. Above zero is the
        shape of a model inventing its evidence, which the skills themselves do not show."""
        return self.quotes - self.grounded

    @property
    def all_blank(self) -> bool:
        """True when a real run of ALL_BLANK_MIN+ jobs produced not one skill mention —
        the shape of a broken prompt, schema or model, never of real postings (HIR-193).
        Callers running the whole queue should fail loudly on it."""
        return not self.skipped_busy and self.attempted >= ALL_BLANK_MIN and self.mentions == 0

    def line(self) -> str:
        if self.skipped_busy:
            return "extract: skipped, another extraction is running on this database (jobs stay pending)"
        return (f"extracted={self.succeeded}/{self.attempted} mentions={self.mentions} "
                f"proposed={self.proposed} failed={len(self.failed)} dropped={len(self.dropped)}")

    def log_line(self, unlogged: int) -> str:
        """The second line of the poll report (HIR-170 step 4): how much of the model's own
        output we kept this run, and how many stored extractions still have no record of the
        reading that produced them. `unlogged` only ever shrinks — it counts extractions made
        before this logging existed, which cannot be filled in without paying to read again."""
        return f"extraction log: logged={self.logged} missing={unlogged}"

    def grounding_line(self) -> str | None:
        """The run's grounding, or None when there is nothing to say.

        Printed only when a quote went missing, so a clean run stays quiet and a model
        inventing evidence is not something you have to open LangSmith to notice
        (AGENTS.md "Reporting a run": silence on failures is not cleanliness)."""
        if not self.grounding_failures:
            return None
        return (f"grounding: {self.grounding_failures} of {self.quotes} quoted snippets were not in "
                f"the posting they came from — the model is inventing evidence on some jobs")


@contextlib.contextmanager
def _extraction_lock(conn: sqlite3.Connection):
    """Yield True if this process holds the database's extraction lock, False if another does.

    A lock file next to the database file, held with flock, so it is released when the
    process exits even after a crash. In-memory databases have no file and are never locked."""
    path = next((r[2] for r in conn.execute("PRAGMA database_list") if r[1] == "main"), "")
    if not path:
        yield True
        return
    with open(path + ".extract.lock", "w") as fh:
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _pending_clause(version: str, now: str | None = None) -> tuple[str, list]:
    """WHERE fragment (over alias j) selecting the jobs that need an extraction at `version`.

    The one definition of the queue's membership, so a count of it and the queue itself can
    never disagree (HIR-221)."""
    open_sql, open_params = open_clause(now or now_iso())
    return (f"(j.extracted_version IS NULL OR (j.extracted_version != ? AND {open_sql}))"
            " AND j.extracted_version IS NOT 'legacy'", [version, *open_params])


def jobs_needing_extraction(conn: sqlite3.Connection, version: str, limit: int | None = None,
                            job_ids: list[int] | None = None, now: str | None = None) -> list[sqlite3.Row]:
    """Jobs without a current extraction; `job_ids` narrows to those jobs (the add endpoints).

    Jobs stamped 'legacy' are never re-extracted: they carry the old summary as text, not
    the posting, so a fresh extraction would be worse than the labels they have.

    A job never read at all is always in the queue, but a re-read (a job stamped with an
    older version) only while the job is still open: closed jobs keep the skills of their
    day, and nobody browses them, so a version bump must not pay to re-read them (HIR-195).
    A repost the poll sees again gets its last_seen bumped by ingest, counts as open, and
    re-enters the queue on its own."""
    where, params = _pending_clause(version, now)
    sql = f"SELECT id, extracted_version, title, description_text FROM job j WHERE {where}"
    if job_ids:
        sql += f" AND id IN ({','.join('?' * len(job_ids))})"
        params += list(job_ids)
    # Jobs never read at all come before re-reads, newest first in both: after a version
    # bump the queue holds the whole database, and this morning's postings must not sit
    # blank on the dashboard for hours behind thousands of re-reads (HIR-193).
    sql += " ORDER BY (extracted_version IS NOT NULL), id DESC"
    if limit:
        sql += f" LIMIT {int(limit)}"
    return conn.execute(sql, params).fetchall()


def reread_queue_size(conn: sqlite3.Connection, now: str | None = None) -> int:
    """How many jobs an extractor change merged now would read, without reading their text.

    Counted against a version stamp no job can be carrying, which is what a bump does to
    every stamp at once: the answer is the never-read jobs plus the stale-stamped open ones,
    exactly the queue `jobs_needing_extraction` would build (HIR-221)."""
    where, params = _pending_clause("(no version: every stamp is stale)", now)
    return conn.execute(f"SELECT count(*) FROM job j WHERE {where}", params).fetchone()[0]


def closed_reread_skips(conn: sqlite3.Connection, version: str,
                        job_ids: list[int] | None = None, now: str | None = None) -> int:
    """How many stale-stamped jobs the queue left out because they are closed (HIR-195)."""
    open_sql, open_params = open_clause(now or now_iso())
    sql = ("SELECT count(*) FROM job j"
           " WHERE j.extracted_version IS NOT NULL AND j.extracted_version != ?"
           f" AND j.extracted_version != 'legacy' AND NOT {open_sql}")
    params: list = [version, *open_params]
    if job_ids:
        sql += f" AND id IN ({','.join('?' * len(job_ids))})"
        params += list(job_ids)
    return conn.execute(sql, params).fetchone()[0]


def _count_blank_read(conn: sqlite3.Connection, job_id: int) -> int:
    """Record one blank read of this job and return how many it has had in a row.

    `store_extraction` sets the count back to 0, so this is a run of consecutive blank reads,
    not a lifetime tally: a posting we once read successfully starts again from one (HIR-199)."""
    with conn:
        conn.execute("UPDATE job SET blank_extractions = blank_extractions + 1 WHERE id = ?", (job_id,))
    return conn.execute("SELECT blank_extractions FROM job WHERE id = ?", (job_id,)).fetchone()[0]


def _drop_job(conn: sqlite3.Connection, job_id: int) -> None:
    """Delete a posting the model has read as blank twice in a row; its rows cascade with it."""
    if not conn.execute("PRAGMA foreign_keys").fetchone()[0]:
        raise RuntimeError("foreign keys are off: dropping a job would orphan its rows. "
                           "Open the database with app.db.connect.")
    with conn:
        conn.execute("DELETE FROM job WHERE id = ?", (job_id,))


def _reject_fields(item) -> tuple[str | None, str | None]:
    if not isinstance(item, dict):
        return None, None
    sid, raw = item.get("skill_id"), item.get("raw_text")
    return (str(sid) if sid is not None else None), (str(raw) if raw is not None else None)


def log_extraction(conn: sqlite3.Connection, job_id: int, ex: Extraction, model: str,
                   input_text: str) -> None:
    """Append the permanent record of one reading. Must run inside the caller's transaction.

    Append-only on purpose: `skill_mention` keeps only the latest answer, so without this a
    re-extract would destroy the earlier one, and the model version that produced it may be
    retired by the time anyone wants it back (HIR-170). `input_sha256` is the hash of the exact
    text that was sent, which is what ties a logged answer to the posting it answers even after
    the posting itself is edited or deleted."""
    conn.execute(
        "INSERT INTO extraction_log"
        " (job_id, extractor_version, taxonomy_version, model, raw_output, usage, input_sha256)"
        " VALUES (?,?,?,?,?,?,?)",
        (job_id, ex.extractor_version, ex.taxonomy_version, model or ex.model,
         json.dumps(ex.raw_output, ensure_ascii=False, sort_keys=True, default=str),
         json.dumps(ex.usage, ensure_ascii=False, sort_keys=True, default=str),
         hashlib.sha256(input_text.encode()).hexdigest()))


def unlogged_extractions(conn: sqlite3.Connection) -> int:
    """Stored extractions with no row recording the reading that produced them.

    Only extractions made before HIR-170 landed; it never grows during a run."""
    return conn.execute(
        "SELECT count(*) FROM job j WHERE j.extracted_version IS NOT NULL"
        " AND j.extracted_version != 'legacy'"
        " AND NOT EXISTS (SELECT 1 FROM extraction_log l WHERE l.job_id = j.id"
        "                 AND l.extractor_version = j.extracted_version)").fetchone()[0]


def store_extraction(conn: sqlite3.Connection, job_id: int, ex: Extraction, model: str = "",
                     input_text: str | None = None) -> None:
    """Write the job's current answer, and append the log row when the caller passed what it needs.

    `model` and `input_text` default to unset so the seed and legacy-import scripts, which
    build an Extraction by hand rather than from a model call, store an answer without
    claiming a reading that never happened."""
    with conn:
        conn.execute("DELETE FROM skill_mention WHERE job_id=?", (job_id,))  # one current extraction per job
        conn.executemany(
            "INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text, taxonomy_version, extractor_version)"
            " VALUES (?,?,?,?,?,?)",
            [(job_id, m.skill_id, m.requirement, m.raw_text, ex.taxonomy_version, ex.extractor_version)
             for m in ex.mentions])
        conn.execute("DELETE FROM extraction_reject WHERE job_id=?", (job_id,))
        conn.executemany(
            "INSERT INTO extraction_reject (job_id, reason, skill_id, raw_text, item, extractor_version)"
            " VALUES (?,?,?,?,?,?)",
            [(job_id, r["reason"], *_reject_fields(r["item"]), json.dumps(r["item"], ensure_ascii=False, default=str),
              ex.extractor_version) for r in ex.rejected])
        conn.execute("DELETE FROM proposed_skill WHERE job_id=? AND status='pending'", (job_id,))
        # A label rejected once stays rejected: re-extraction must not re-queue it.
        rejected = {r[0] for r in conn.execute(
            "SELECT DISTINCT lower(label) FROM proposed_skill WHERE status='rejected'")}
        conn.executemany(
            "INSERT INTO proposed_skill (job_id, label, raw_text) VALUES (?,?,?)",
            [(job_id, p.label, p.raw_text) for p in ex.proposed if p.label.lower() not in rejected])
        sen, ger, deg, prod = ex.seniority, ex.german, ex.degree, ex.production
        conn.execute(
            # blank_extractions=0: the two blank reads that drop a posting must be two in a
            # row. A reading that worked proves the posting is readable, so the earlier blank
            # stops counting against it (HIR-199); without this, blank -> success -> blank
            # deleted a job whose skills were already on the dashboard.
            "UPDATE job SET extracted_version=?, blank_extractions=0,"
            " seniority=?, seniority_basis=?, seniority_signal=?,"
            " german=?, german_basis=?, german_signal=?,"
            " degree=?, degree_requirement=?, degree_or_equivalent=?, degree_signal=?,"
            " production=?, production_basis=?, production_signal=? WHERE id=?",
            (ex.extractor_version, sen.level, sen.basis, sen.signal, ger.requirement, ger.basis, ger.signal,
             deg.level, deg.requirement, int(deg.or_equivalent), deg.signal,
             prod.requirement, prod.basis, prod.signal, job_id))
        # Same transaction as the answer itself: an extraction that is stored but not logged,
        # or logged but not stored, is the one outcome this table exists to rule out.
        if input_text is not None:
            log_extraction(conn, job_id, ex, model, input_text)


def default_extract_fn(client=None):
    """The real stage-2 call, which is what every caller outside the tests wants.

    Every caller used to build this same one-line wrapper itself (HIR-210). The client is
    created on the first job rather than up front, so a process with no credentials can
    still reach this function without a job to read — which is what lets the API boot
    without them.
    """
    # Wrapped for tracing here, where every real stage-2 call goes through, so no caller
    # has to remember to do it and none can wrap twice (HIR-160). A no-op without a
    # LANGSMITH_API_KEY, which is how the tests and anyone without a key run.
    held = {"client": langsmith_live.wrap_client(client)}

    def call(text: str, tax: Taxonomy, model: str) -> Extraction:
        if held["client"] is None:
            held["client"] = langsmith_live.wrap_client(make_client())
        return extract(text, tax, held["client"], model)

    return call


def extract_pending(conn: sqlite3.Connection, tax: Taxonomy, extract_fn=None, model: str = DEFAULT_MODEL,
                    limit: int | None = None, log=print, job_ids: list[int] | None = None,
                    client=None, run_kind: str = langsmith_live.REREAD) -> ExtractReport:
    """extract_fn(text, tax, model) -> Extraction. Injected so tests never hit the API;
    left out, the real model call is used (`default_extract_fn`), with `client` if given.

    `run_kind` only names this run in LangSmith — "poll", "add", "backfill", or the
    default, draining the queue after a version bump, which is a re-read (HIR-160). It
    changes nothing about what is read or stored, and without a LANGSMITH_API_KEY it is
    never looked at.
    """
    extract_fn = extract_fn or default_extract_fn(client)
    with _extraction_lock(conn) as held:
        if not held:
            # No trace: a run that read nothing and paid nothing is not a run.
            log("  extract: another extraction is running on this database; skipping")
            return ExtractReport(skipped_busy=True)
        with langsmith_live.run(run_kind,
                                metadata={"model": model, "taxonomy_version": tax.version,
                                          "extractor_version": extractor_version(tax, model)},
                                inputs={"limit": limit, "job_ids": job_ids}) as trace:
            report = _extract_pending(conn, tax, extract_fn, model, limit, log, job_ids, trace)
            trace.finish({
                "attempted": report.attempted, "succeeded": report.succeeded,
                "failed": len(report.failed), "dropped": len(report.dropped),
                "mentions": report.mentions, "proposed": report.proposed,
                "reread_queued": report.reread_queued, "skipped_closed": report.skipped_closed,
                "quotes": report.quotes, "grounded": report.grounded,
                "grounding_failures": report.grounding_failures,
            })
            if report.grounding_failures:
                trace.tag("grounding-failure")
        return report


def _extract_pending(conn, tax, extract_fn, model, limit, log, job_ids, trace=None) -> ExtractReport:
    trace = trace if trace is not None else langsmith_live.Run(None)
    version = extractor_version(tax, model)
    now = now_iso()
    report = ExtractReport()
    rows = jobs_needing_extraction(conn, version, limit, job_ids, now)
    report.reread_queued = sum(1 for r in rows if r["extracted_version"] is not None)
    report.skipped_closed = closed_reread_skips(conn, version, job_ids, now)
    # On the trace as well as in the log: HIR-224's targeted re-read is compared against a
    # full one, and the comparison is these two numbers.
    trace.note({"queued": len(rows), "first_reads": len(rows) - report.reread_queued,
                "reread_queued": report.reread_queued, "skipped_closed": report.skipped_closed})
    if report.reread_queued:
        trace.tag("reread")
    if report.reread_queued or report.skipped_closed:
        log(f"  re-reads: {report.reread_queued} open jobs queued;"
            f" {report.skipped_closed} closed jobs skipped (keep their old skills)")
    for row in rows:
        report.attempted += 1
        sent = extraction_input(row["title"], row["description_text"])
        with trace.job(row["id"], row["title"], sent) as span:
            try:
                ex = extract_fn(sent, tax, model)
            except EmptyExtractionError as e:
                # A blank read is the posting's own failure, not the connection's: try it twice,
                # then drop it (HIR-172, Chandler's decision of 5 Nov).
                blanks = _count_blank_read(conn, row["id"])
                report.failed.append((row["id"], f"{type(e).__name__}: {e}"))
                log(f"  job {row['id']}: FAILED {type(e).__name__}: {str(e)[:200]}"
                    f" (blank read {blanks} of {BLANK_READ_LIMIT})")
                dropped = blanks >= BLANK_READ_LIMIT
                if dropped:
                    _drop_job(conn, row["id"])
                    report.dropped.append((row["id"], f"{blanks} blank reads"))
                    log(f"  job {row['id']}: DROPPED after {blanks} blank reads")
                span.failed(f"{type(e).__name__}: {e}", dropped=dropped)
                continue
            except Exception as e:  # keep going; the job stays pending for the next run
                report.failed.append((row["id"], f"{type(e).__name__}: {e}"))
                log(f"  job {row['id']}: FAILED {type(e).__name__}: {str(e)[:200]}")
                span.failed(f"{type(e).__name__}: {e}")
                continue
            if not ex.mentions:
                log(f"  job {row['id']}: 0 skills")  # legitimate for a partial posting; recorded, not retried
            # The same check the eval scores, run on every live reading (HIR-160). It is
            # measured, not enforced: the extractor has already dropped the quotes it could
            # not find, and re-deciding that here would make the poll disagree with the eval.
            grounded, quotes = grounding(sent, ex.mentions, ex.proposed, ex.rejected)
            report.grounded += grounded
            report.quotes += quotes
            span.result(ex, grounded, quotes)
            store_extraction(conn, row["id"], ex, model, sent)
            report.logged += 1
            report.succeeded += 1
            report.mentions += len(ex.mentions)
            report.proposed += len(ex.proposed)
    return report
