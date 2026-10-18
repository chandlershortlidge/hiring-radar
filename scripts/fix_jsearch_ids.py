"""One-off: collapse duplicate jsearch rows written before source_job_id was made stable.

Before the fix, each poll stored a JSearch posting under a new source_job_id, so a job could
have several jsearch rows in job_source, and every extra row bumped job.repost_count. This
rewrites each jsearch row's source_job_id to `jsearch.stable_id(...)`, keeps one row per
(job, stable id) with the earliest first_seen and latest last_seen, and takes one off
repost_count per row removed.

Does NOT touch other sources' rows. Safe to run twice: the second run changes nothing.

    uv run python scripts/fix_jsearch_ids.py --dry-run
    uv run python scripts/fix_jsearch_ids.py
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db  # noqa: E402
from app.sources.jsearch import stable_id  # noqa: E402


def fix(conn: sqlite3.Connection, commit: bool = True) -> dict:
    """Apply the fix in one transaction; with commit=False, roll it back and only report."""
    rows = conn.execute("SELECT id, job_id, source_job_id, first_seen, last_seen FROM job_source "
                        "WHERE source='jsearch' ORDER BY id").fetchall()
    groups: dict[tuple[int, str], list] = {}
    for r in rows:
        groups.setdefault((r["job_id"], stable_id(r["source_job_id"] or "")), []).append(r)
    removed = renamed = 0
    try:
        for (job_id, sid), rs in groups.items():
            keep, extra = rs[0], rs[1:]
            for r in extra:
                conn.execute("DELETE FROM job_source WHERE id=?", (r["id"],))
            first = min(r["first_seen"] for r in rs)
            last = max(r["last_seen"] for r in rs)
            if keep["source_job_id"] != sid:
                renamed += 1
            conn.execute("UPDATE job_source SET source_job_id=?, first_seen=?, last_seen=? WHERE id=?",
                         (sid, first, last, keep["id"]))
            if extra:
                conn.execute("UPDATE job SET repost_count = max(0, repost_count - ?) WHERE id=?",
                             (len(extra), job_id))
                removed += len(extra)
    except Exception:
        conn.rollback()
        raise
    conn.commit() if commit else conn.rollback()
    return {"jsearch_rows": len(rows), "kept": len(groups), "removed": removed, "renamed": renamed}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    conn = db.connect(os.environ.get("HIRING_RADAR_DB", "data/hiring-radar.db"))
    db.migrate(conn)
    print(("dry run, nothing written: " if args.dry_run else "") + str(fix(conn, commit=not args.dry_run)))


if __name__ == "__main__":
    main()
