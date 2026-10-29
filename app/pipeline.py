"""Run stage 2 over stored jobs that have no skills yet, and persist the results.

Does: find jobs whose `extracted_version` is not the current one, extract, and write
skill_mention + proposed_skill rows and the job's seniority / German / degree, then stamp the job. One job per transaction.

Does NOT: fetch postings, dedup, or decide which taxonomy/model to use (passed in).

Invariants: a job holds exactly one extraction (the latest; older rows are replaced on
re-extract); a job is processed once per extractor_version, including jobs with zero skills; a failed extraction leaves the job unstamped and no partial rows, and is reported,
not raised; re-running is safe. Only one extraction runs per database at a time: a second
run (a poll started while an add is extracting, say) skips instead of paying for the same jobs
twice, and its jobs stay pending for the next run.
"""

import contextlib
import fcntl
import json
import sqlite3
from dataclasses import dataclass, field

from app.extract import Extraction, extraction_input, extractor_version
from app.taxonomy import Taxonomy


@dataclass
class ExtractReport:
    attempted: int = 0
    succeeded: int = 0
    failed: list[tuple[int, str]] = field(default_factory=list)
    mentions: int = 0
    proposed: int = 0
    skipped_busy: bool = False

    def line(self) -> str:
        if self.skipped_busy:
            return "extract: skipped, another extraction is running on this database (jobs stay pending)"
        return (f"extracted={self.succeeded}/{self.attempted} mentions={self.mentions} "
                f"proposed={self.proposed} failed={len(self.failed)}")


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


def jobs_needing_extraction(conn: sqlite3.Connection, version: str, limit: int | None = None,
                            job_ids: list[int] | None = None) -> list[sqlite3.Row]:
    """Jobs without a current extraction; `job_ids` narrows to those jobs (the add endpoints).

    Jobs stamped 'legacy' are never re-extracted: they carry the old summary as text, not
    the posting, so a fresh extraction would be worse than the labels they have."""
    sql = ("SELECT id, title, description_text FROM job"
           " WHERE (extracted_version IS NULL OR extracted_version != ?) AND extracted_version IS NOT 'legacy'")
    params: list = [version]
    if job_ids:
        sql += f" AND id IN ({','.join('?' * len(job_ids))})"
        params += list(job_ids)
    sql += " ORDER BY id"
    if limit:
        sql += f" LIMIT {int(limit)}"
    return conn.execute(sql, params).fetchall()


def _reject_fields(item) -> tuple[str | None, str | None]:
    if not isinstance(item, dict):
        return None, None
    sid, raw = item.get("skill_id"), item.get("raw_text")
    return (str(sid) if sid is not None else None), (str(raw) if raw is not None else None)


def store_extraction(conn: sqlite3.Connection, job_id: int, ex: Extraction) -> None:
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
            "UPDATE job SET extracted_version=?, seniority=?, seniority_basis=?, seniority_signal=?,"
            " german=?, german_basis=?, german_signal=?,"
            " degree=?, degree_requirement=?, degree_or_equivalent=?, degree_signal=?,"
            " production=?, production_basis=?, production_signal=? WHERE id=?",
            (ex.extractor_version, sen.level, sen.basis, sen.signal, ger.requirement, ger.basis, ger.signal,
             deg.level, deg.requirement, int(deg.or_equivalent), deg.signal,
             prod.requirement, prod.basis, prod.signal, job_id))


def extract_pending(conn: sqlite3.Connection, tax: Taxonomy, extract_fn, model: str,
                    limit: int | None = None, log=print, job_ids: list[int] | None = None) -> ExtractReport:
    """extract_fn(text, tax, model) -> Extraction. Injected so tests never hit the API."""
    with _extraction_lock(conn) as held:
        if not held:
            log("  extract: another extraction is running on this database; skipping")
            return ExtractReport(skipped_busy=True)
        return _extract_pending(conn, tax, extract_fn, model, limit, log, job_ids)


def _extract_pending(conn, tax, extract_fn, model, limit, log, job_ids) -> ExtractReport:
    version = extractor_version(tax, model)
    report = ExtractReport()
    for row in jobs_needing_extraction(conn, version, limit, job_ids):
        report.attempted += 1
        try:
            ex = extract_fn(extraction_input(row["title"], row["description_text"]), tax, model)
        except Exception as e:  # keep going; the job stays pending for the next run
            report.failed.append((row["id"], f"{type(e).__name__}: {e}"))
            log(f"  job {row['id']}: FAILED {type(e).__name__}: {str(e)[:200]}")
            continue
        if not ex.mentions:
            log(f"  job {row['id']}: 0 skills")  # legitimate for a partial posting; recorded, not retried
        store_extraction(conn, row["id"], ex)
        report.succeeded += 1
        report.mentions += len(ex.mentions)
        report.proposed += len(ex.proposed)
    return report
