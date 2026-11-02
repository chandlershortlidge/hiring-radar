"""One-off: delete stored jobs whose title is an aggregator's search-result headline.

HIR-96 taught the JSearch adapter to skip these records at parse time, but rows stored
before that fix are still in the database (jobs 208 and 230 in the dev copy). Such a row
carries the aggregator's headline as its title ("AI Engineer (m/f/x) arbeitnow
commercetools Berlin · 10/16/2026") and an unrelated firm as its company ("Primetime"),
so it shows on the chart and in the job list as a separate employer and double-counts the
skills of a posting we already hold under its real company.

Selects with `app.sources.jsearch.is_headline` — the same test the adapter now applies —
so this script can never remove a row the adapter would have kept. Deleting a job cascades
to its skill mentions, extraction rejects, feed-source rows and screenshot; it refuses to
run with foreign keys off, which would orphan them instead.

Does NOT touch a headline-titled job that has no jsearch source row: that would be a
different bug from the one HIR-104 approved removing, so it is reported and left alone.
Does NOT adjust any other job's repost_count — these rows were never merged into another
job, so no count was inflated by them.

Safe to run twice: the second run finds nothing.

    uv run python scripts/remove_headline_jobs.py --dry-run
    uv run python scripts/remove_headline_jobs.py
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db  # noqa: E402
from app.sources.jsearch import SOURCE as JSEARCH, is_headline  # noqa: E402


def classify(conn: sqlite3.Connection) -> tuple[list[dict], list[dict]]:
    """Pure read: (jobs to remove, headline-titled jobs from some other source).

    The second list is for a human to look at; this script never deletes from it.
    """
    rows = conn.execute(
        "SELECT j.id, j.company, j.title, "
        "  (SELECT COUNT(*) FROM skill_mention m WHERE m.job_id = j.id) AS mentions, "
        "  (SELECT GROUP_CONCAT(DISTINCT s.source) FROM job_source s WHERE s.job_id = j.id) AS sources "
        "FROM job j ORDER BY j.id").fetchall()
    removable: list[dict] = []
    other: list[dict] = []
    for r in rows:
        if not is_headline(r["title"] or ""):
            continue
        sources = [s for s in (r["sources"] or "").split(",") if s]
        (removable if JSEARCH in sources else other).append(dict(r))
    return removable, other


def remove(conn: sqlite3.Connection, commit: bool = True) -> dict:
    """Delete the headline rows in one transaction; with commit=False, roll back and report."""
    if not conn.execute("PRAGMA foreign_keys").fetchone()[0]:
        raise RuntimeError(
            "foreign keys are off: deleting a job would orphan its skill mentions. "
            "Open the database with app.db.connect.")
    removable, other = classify(conn)
    try:
        for r in removable:
            conn.execute("DELETE FROM job WHERE id = ?", (r["id"],))
    except Exception:
        conn.rollback()
        raise
    conn.commit() if commit else conn.rollback()
    return {"removed": removable, "skipped_other_source": other}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    conn = db.connect(os.environ.get("HIRING_RADAR_DB", "data/hiring-radar.db"))
    db.migrate(conn)
    result = remove(conn, commit=not args.dry_run)
    verb = "would remove" if args.dry_run else "removed"
    for r in result["removed"]:
        print(f"{verb} job {r['id']}: {r['company']!r} — {r['title']!r} ({r['mentions']} mentions)")
    for r in result["skipped_other_source"]:
        print(f"SKIPPED job {r['id']} ({r['sources']}, not jsearch): {r['company']!r} — {r['title']!r} "
              f"— headline title from another source; your call")
    print(f"{verb}: {len(result['removed'])} job(s), "
          f"{sum(r['mentions'] for r in result['removed'])} skill mention(s); "
          f"skipped: {len(result['skipped_other_source'])}")


if __name__ == "__main__":
    main()
