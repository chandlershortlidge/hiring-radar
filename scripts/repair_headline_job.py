"""One-off: give an aggregator-headline job row its real company and title back.

The counterpart to `remove_headline_jobs.py`. Most headline rows duplicate a posting we
already hold, so deleting them loses nothing. Job 363 on the live database is the
exception: SumUp's "AI / Machine Learning Engineer II" is held nowhere else and cannot
return (HIR-96 now drops the record at parse time, and SumUp's polled Greenhouse board does
not carry it), so deleting it would lose a real posting. Its description text is genuine —
only the company and title are the aggregator's, and both read out of the headline
unambiguously. Chandler chose repair over deletion, 2026-11-03 (DECISIONS 2026-11-02).

Rewrites company, title and the dedup `title_key`, then clears `extracted_version` so the
next extraction re-reads the job. Re-reading is the point, not bookkeeping: `extract` puts
the title on top of the posting text it sends the model, so every attribute on this row was
judged with the headline in front of it. Job 363 came out "senior / stated" on the quote
"Senior Machine Learning Engineer" for a posting titled "Engineer II".

Does NOT run dedup again, so it cannot merge the repaired row into another job. Check first
that the corrected company and title are not already stored under another id; for job 363
they were not (SumUp's other three rows carry different titles). Does NOT delete the row's
existing skill mentions — re-extraction replaces them. Does NOT invent the new values: pass
them, having read them off the headline yourself.

    uv run python scripts/repair_headline_job.py --job-id 363 \
      --company SumUp --title "AI / Machine Learning Engineer II" --dry-run
    uv run python scripts/repair_headline_job.py --job-id 363 \
      --company SumUp --title "AI / Machine Learning Engineer II"      # one model call
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db  # noqa: E402
from app.dedup import company_key, title_key  # noqa: E402

FIELDS = "id, company, title, title_key, extracted_version, seniority, seniority_basis, seniority_signal"


def collisions(conn: sqlite3.Connection, job_id: int, company: str, title: str) -> list[dict]:
    """Other jobs the repaired row would duplicate, by the keys dedup matches on.

    Reported, never acted on: merging two stored jobs is a separate decision.
    """
    rows = conn.execute(f"SELECT {FIELDS} FROM job WHERE id != ?", (job_id,)).fetchall()
    want = (company_key(company), title_key(title))
    return [dict(r) for r in rows
            if (company_key(r["company"]), title_key(r["title"] or "")) == want]


def repair(conn: sqlite3.Connection, job_id: int, company: str, title: str,
           commit: bool = True) -> dict:
    """Set the row's company and title, and mark it for re-extraction.

    Returns the row before and after, and any collisions, so a dry run shows the whole
    effect. Raises if the job does not exist.
    """
    before = conn.execute(f"SELECT {FIELDS} FROM job WHERE id = ?", (job_id,)).fetchone()
    if before is None:
        raise RuntimeError(f"no job {job_id}")
    found = collisions(conn, job_id, company, title)
    try:
        conn.execute(
            "UPDATE job SET company = ?, title = ?, title_key = ?, extracted_version = NULL "
            "WHERE id = ?", (company, title, title_key(title), job_id))
    except Exception:
        conn.rollback()
        raise
    after = conn.execute(f"SELECT {FIELDS} FROM job WHERE id = ?", (job_id,)).fetchone()
    result = {"before": dict(before), "after": dict(after), "collisions": found}
    conn.commit() if commit else conn.rollback()
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job-id", type=int, required=True)
    ap.add_argument("--company", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-extract", action="store_true",
                    help="rewrite the row but leave the re-read to a later `app extract`")
    args = ap.parse_args()

    conn = db.connect(os.environ.get("HIRING_RADAR_DB", "data/hiring-radar.db"))
    db.migrate(conn)
    result = repair(conn, args.job_id, args.company, args.title, commit=not args.dry_run)

    verb = "would set" if args.dry_run else "set"
    b, a = result["before"], result["after"]
    print(f"job {b['id']}")
    print(f"  company:   {b['company']!r} -> {a['company']!r}")
    print(f"  title:     {b['title']!r} -> {a['title']!r}")
    print(f"  title_key: {b['title_key']!r} -> {a['title_key']!r}")
    print(f"  attributes judged on the old title, to be re-read: "
          f"seniority={b['seniority']}/{b['seniority_basis']} on {b['seniority_signal']!r}")
    for c in result["collisions"]:
        print(f"  COLLISION with job {c['id']} ({c['company']!r} — {c['title']!r}): the repaired "
              f"row duplicates it by dedup's keys. Not merged; that is a separate decision.")
    print(f"{verb}: company, title, title_key; extracted_version cleared "
          f"({'nothing written' if args.dry_run else 'committed'})")

    if args.dry_run or args.no_extract:
        print("no model call made; run `python -m app extract` to re-read the job")
        return
    from app.__main__ import run_extraction  # noqa: PLC0415 — only needed on the live path
    run_extraction(conn, job_ids=[args.job_id])


if __name__ == "__main__":
    main()
