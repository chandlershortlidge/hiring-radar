"""One-off repair for jobs stored without a company (HIR-198).

Does: for every job whose company is NULL or blank, re-fetch its stored link and read the
company off the page with the same rules the add-by-link path now uses (site name, title
tail, hostname); a dead link falls back to those same rules on the stored title and URL.
When the title tail supplied the company, the tail is stripped from the stored title too, the
job family is recomputed from the shorter title, and the job's extraction stamp is cleared so
it is read again under that title.
A repaired job is then matched against same-company rows with the normal dedup rules, and
a duplicate is folded into the older row (sources, skills, logs moved; the newer job row
deleted). Rows nothing could fix are reported and left untouched.

Does NOT: call a model, touch jobs that already have a company, or commit — the caller
decides (the CLI's default is a dry run that rolls everything back).

Invariants: `merge_jobs` keeps the row with the earlier first_seen (ties: the smaller id);
every table that references job.id is moved before the duplicate row is deleted, and the
list of those tables is read from the schema rather than written here, so a table added
later is moved too; the surviving row carries exactly one reading's skills, never two
unioned; running the repair twice is a no-op, because a fixed row no longer has a blank
company.
"""

import sqlite3
from dataclasses import dataclass

from app import dedup, ingest
from app.check import _PageParser, company_from_page, split_title_tail
from app.sources import fetch_text

# The tables holding one job's current reading. store_extraction replaces them wholesale, so
# a merge must drop the duplicate's rows rather than union two readings into them.
_READING_TABLES = ("skill_mention", "extraction_reject")


@dataclass
class RepairLine:
    job_id: int
    old_company: str | None
    company: str | None = None
    rule: str | None = None
    merged_into: int | None = None   # this row was folded into that older row
    absorbed: int | None = None      # that newer duplicate was folded into this row
    note: str = ""                   # why unresolved, or where the fallback came from

    def line(self) -> str:
        if self.company is None:
            return f"{self.job_id} · unresolved — {self.note}"
        s = f"{self.job_id} · {self.old_company!r} → {self.company!r} ({self.rule})"
        if self.note:
            s += f" [{self.note}]"
        if self.merged_into is not None:
            s += f" · merged into #{self.merged_into}"
        if self.absorbed is not None:
            s += f" · absorbed duplicate #{self.absorbed}"
        return s


def tables_referencing_job(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    """(table, column) for every table with a foreign key to job.id, read from the schema.

    Discovered rather than listed by hand, so a table added later is moved by merge_jobs
    without anyone remembering this function exists (HIR-208). A table a hand-written list
    missed lost its rows silently: they cascade away with the duplicate job row, or are
    orphaned from their job where the key is ON DELETE SET NULL."""
    rows = conn.execute(
        'SELECT m.name AS tbl, f."from" AS col FROM sqlite_master m'
        ' JOIN pragma_foreign_key_list(m.name) f'
        " WHERE m.type = 'table' AND lower(f.\"table\") = 'job'").fetchall()
    return sorted({(r["tbl"], r["col"]) for r in rows})


def merge_jobs(conn: sqlite3.Connection, keep: int, drop: int) -> None:
    """Fold the duplicate row `drop` into `keep`: drop the duplicate's reading, move every
    other reference, widen the seen window, delete the duplicate row.

    The kept row keeps its own reading whole and the duplicate's is dropped. Unioning the
    two left the job carrying skills from both while stamped as read once, so the chart
    counted skills neither reading alone found (HIR-208). Nothing paid for is lost: the
    reading itself stays on the record in extraction_log, which is moved, not deleted. A
    kept row with no reading of its own stays unstamped and is read again on the next run."""
    if not conn.execute("PRAGMA foreign_keys").fetchone()[0]:
        raise RuntimeError("foreign keys are off: merging a job would orphan the duplicate's "
                           "rows instead of moving them. Open the database with app.db.connect.")
    for table in _READING_TABLES:
        conn.execute(f"DELETE FROM {table} WHERE job_id=?", (drop,))
    for table, col in tables_referencing_job(conn):
        # OR IGNORE, then delete what could not move: a row the kept job already has (one
        # screenshot per job) is dropped rather than moved, as it was before.
        conn.execute(f"UPDATE OR IGNORE {table} SET {col}=? WHERE {col}=?", (keep, drop))
        conn.execute(f"DELETE FROM {table} WHERE {col}=?", (drop,))
    conn.execute(
        "UPDATE job SET first_seen = min(first_seen, (SELECT first_seen FROM job WHERE id=:drop)),"
        "               last_seen  = max(last_seen,  (SELECT last_seen  FROM job WHERE id=:drop))"
        " WHERE id=:keep", {"keep": keep, "drop": drop})
    conn.execute("DELETE FROM job WHERE id=?", (drop,))


def _resolve(url: str | None, stored_title: str, fetch_page) -> tuple[str | None, str | None, str | None, str]:
    """(company, rule, new_title, note) for one blank-company job. The live page is the
    primary source; the stored title and URL answer when the page is dead or says nothing.
    new_title is set only when a title tail was used as the company."""
    note = ""
    if url:
        try:
            parser = _PageParser()
            parser.feed(fetch_page(url))
            parser.close()
            company, rule = company_from_page(url, parser)
            if company:
                new_title = None
                if rule == "title tail":
                    new_title, _ = split_title_tail(parser.title.strip())
                return company, rule, new_title, note
        except Exception as e:
            note = f"fetch failed: {type(e).__name__}: {str(e)[:80]}"
    # Dead or unhelpful page: the same rules over what is already stored.
    fallback = _PageParser()
    fallback.title = stored_title or ""
    company, rule = company_from_page(url or "", fallback)
    if company:
        new_title = split_title_tail(stored_title.strip())[0] if rule == "title tail" else None
        return company, f"stored {rule}", new_title, note
    return None, None, None, note or "no company on the page, in the stored title, or in the hostname"


def _merge_if_duplicate(conn: sqlite3.Connection, job_id: int, company: str,
                        title: str, text: str) -> tuple[int | None, int | None]:
    """(merged_into, absorbed) after folding this job with its duplicate, if it has one."""
    cands = [dedup.Candidate(r["id"], r["company"], r["title"], r["description_text"])
             for r in conn.execute("SELECT id, company, title, description_text FROM job"
                                   " WHERE id != ? AND company IS NOT NULL", (job_id,))]
    m = dedup.find_match(company, title, text, cands)
    if m is None:
        return None, None
    rows = conn.execute("SELECT id FROM job WHERE id IN (?,?) ORDER BY first_seen, id",
                        (job_id, m.job_id)).fetchall()
    keep, drop = rows[0]["id"], rows[1]["id"]
    merge_jobs(conn, keep, drop)
    return (keep, None) if drop == job_id else (None, drop)


def repair_companies(conn: sqlite3.Connection, fetch_page=fetch_text) -> list[RepairLine]:
    """Repair every blank-company job. Writes but never commits; the caller commits
    (--apply) or rolls back (the default dry run shows the same lines either way)."""
    rows = conn.execute("SELECT id, company, title, description_text FROM job"
                        " WHERE company IS NULL OR trim(company) = ''").fetchall()
    out: list[RepairLine] = []
    for r in rows:
        src = conn.execute("SELECT url FROM job_source WHERE job_id=? AND url IS NOT NULL"
                           " AND url != '' ORDER BY first_seen LIMIT 1", (r["id"],)).fetchone()
        url = src["url"] if src else None
        company, rule, new_title, note = _resolve(url, r["title"] or "", fetch_page)
        if company is None:
            out.append(RepairLine(r["id"], r["company"], note=note))
            continue
        title = new_title or r["title"] or ""
        sets = "company=?, title=?, title_key=?"
        params: list[object] = [company, title, dedup.title_key(title)]
        if title != (r["title"] or ""):
            # The job family is a title rule, and the skills were read under the old title:
            # recompute the family and clear the stamp so the job is read again (HIR-208).
            # The old skills stay on the chart until that reading happens.
            sets += ", family=?, extracted_version=NULL"
            params.append(ingest.family_of(title))
        params.append(r["id"])
        conn.execute(f"UPDATE job SET {sets} WHERE id=?", params)
        merged_into, absorbed = _merge_if_duplicate(conn, r["id"], company, title, r["description_text"])
        out.append(RepairLine(r["id"], r["company"], company, rule, merged_into, absorbed, note))
    return out
