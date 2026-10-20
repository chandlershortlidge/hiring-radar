"""Run stage 2 over stored jobs that have no skills yet, and persist the results.

Does: find jobs whose `extracted_version` is not the current one, extract, and write
skill_mention + proposed_skill rows and the job's seniority / German / degree, then stamp the job. One job per transaction.

Does NOT: fetch postings, dedup, or decide which taxonomy/model to use (passed in).

Invariants: a job holds exactly one extraction (the latest; older rows are replaced on
re-extract); a job is processed once per extractor_version, including jobs with zero skills; a failed extraction leaves the job unstamped and no partial rows, and is reported,
not raised; re-running is safe.
"""

import sqlite3
from dataclasses import dataclass, field

from app.extract import Extraction, extractor_version
from app.taxonomy import Taxonomy


@dataclass
class ExtractReport:
    attempted: int = 0
    succeeded: int = 0
    failed: list[tuple[int, str]] = field(default_factory=list)
    mentions: int = 0
    proposed: int = 0

    def line(self) -> str:
        return (f"extracted={self.succeeded}/{self.attempted} mentions={self.mentions} "
                f"proposed={self.proposed} failed={len(self.failed)}")


def jobs_needing_extraction(conn: sqlite3.Connection, version: str, limit: int | None = None,
                            job_ids: list[int] | None = None) -> list[sqlite3.Row]:
    """Jobs without a current extraction; `job_ids` narrows to those jobs (the add endpoints).

    Jobs stamped 'legacy' are never re-extracted: they carry the old summary as text, not
    the posting, so a fresh extraction would be worse than the labels they have."""
    sql = ("SELECT id, description_text FROM job"
           " WHERE (extracted_version IS NULL OR extracted_version != ?) AND extracted_version IS NOT 'legacy'")
    params: list = [version]
    if job_ids:
        sql += f" AND id IN ({','.join('?' * len(job_ids))})"
        params += list(job_ids)
    sql += " ORDER BY id"
    if limit:
        sql += f" LIMIT {int(limit)}"
    return conn.execute(sql, params).fetchall()


def store_extraction(conn: sqlite3.Connection, job_id: int, ex: Extraction) -> None:
    with conn:
        conn.execute("DELETE FROM skill_mention WHERE job_id=?", (job_id,))  # one current extraction per job
        conn.executemany(
            "INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text, taxonomy_version, extractor_version)"
            " VALUES (?,?,?,?,?,?)",
            [(job_id, m.skill_id, m.requirement, m.raw_text, ex.taxonomy_version, ex.extractor_version)
             for m in ex.mentions])
        conn.execute("DELETE FROM proposed_skill WHERE job_id=? AND status='pending'", (job_id,))
        # A label rejected once stays rejected: re-extraction must not re-queue it.
        rejected = {r[0] for r in conn.execute(
            "SELECT DISTINCT lower(label) FROM proposed_skill WHERE status='rejected'")}
        conn.executemany(
            "INSERT INTO proposed_skill (job_id, label, raw_text) VALUES (?,?,?)",
            [(job_id, p.label, p.raw_text) for p in ex.proposed if p.label.lower() not in rejected])
        sen, ger, deg = ex.seniority, ex.german, ex.degree
        conn.execute(
            "UPDATE job SET extracted_version=?, seniority=?, seniority_basis=?, seniority_signal=?,"
            " german=?, german_basis=?, german_signal=?,"
            " degree=?, degree_requirement=?, degree_or_equivalent=?, degree_signal=? WHERE id=?",
            (ex.extractor_version, sen.level, sen.basis, sen.signal, ger.requirement, ger.basis, ger.signal,
             deg.level, deg.requirement, int(deg.or_equivalent), deg.signal, job_id))


def extract_pending(conn: sqlite3.Connection, tax: Taxonomy, extract_fn, model: str,
                    limit: int | None = None, log=print, job_ids: list[int] | None = None) -> ExtractReport:
    """extract_fn(text, tax, model) -> Extraction. Injected so tests never hit the API."""
    version = extractor_version(tax, model)
    report = ExtractReport()
    for row in jobs_needing_extraction(conn, version, limit, job_ids):
        report.attempted += 1
        try:
            ex = extract_fn(row["description_text"], tax, model)
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
