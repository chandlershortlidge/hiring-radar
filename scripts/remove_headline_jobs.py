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
job, so no count was inflated by them. Does NOT decide for itself when a headline row is
the only stored copy of a posting: check that before running, and pass `--keep <id>` for
any row whose deletion would lose a posting rather than a duplicate. Such a row is repaired
instead, with `repair_headline_job.py` — that was job 363 on the live database, SumUp's
"AI / Machine Learning Engineer II" (DECISIONS 2026-11-02).

Safe to run twice: the second run finds nothing.

    uv run python scripts/remove_headline_jobs.py --dry-run
    uv run python scripts/remove_headline_jobs.py --keep 412
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db  # noqa: E402
from app.sources.jsearch import SOURCE as JSEARCH, is_headline  # noqa: E402


def classify(conn: sqlite3.Connection, keep: set[int] = frozenset()) -> tuple[list[dict], list[dict]]:
    """Pure read: (jobs to remove, headline-titled jobs this script will not remove).

    The second list is for a human to look at; this script never deletes from it. A job
    lands there when it did not come from jsearch, or when its id was passed to `keep`.
    """
    rows = conn.execute(
        "SELECT j.id, j.company, j.title, "
        "  (SELECT COUNT(*) FROM skill_mention m WHERE m.job_id = j.id) AS mentions, "
        "  (SELECT GROUP_CONCAT(DISTINCT s.source) FROM job_source s WHERE s.job_id = j.id) AS sources "
        "FROM job j ORDER BY j.id").fetchall()
    removable: list[dict] = []
    held: list[dict] = []
    for r in rows:
        if not is_headline(r["title"] or ""):
            continue
        sources = [s for s in (r["sources"] or "").split(",") if s]
        row = dict(r)
        row["held_because"] = ("asked to keep" if r["id"] in keep
                               else None if JSEARCH in sources else "not from jsearch")
        (held if row["held_because"] else removable).append(row)
    return removable, held


def remove(conn: sqlite3.Connection, commit: bool = True, keep: set[int] = frozenset()) -> dict:
    """Delete the headline rows in one transaction; with commit=False, roll back and report.

    `keep` holds ids a person decided not to delete — used when a headline row turns out to
    be the only stored copy of a real posting, so removing it would lose the posting rather
    than a duplicate.
    """
    if not conn.execute("PRAGMA foreign_keys").fetchone()[0]:
        raise RuntimeError(
            "foreign keys are off: deleting a job would orphan its skill mentions. "
            "Open the database with app.db.connect.")
    removable, held = classify(conn, keep)
    try:
        for r in removable:
            conn.execute("DELETE FROM job WHERE id = ?", (r["id"],))
    except Exception:
        conn.rollback()
        raise
    conn.commit() if commit else conn.rollback()
    return {"removed": removable, "kept": held}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep", type=int, action="append", default=[], metavar="JOB_ID",
                    help="a headline job to leave alone (repeatable), e.g. the only stored "
                         "copy of a posting we hold nowhere else")
    args = ap.parse_args()
    conn = db.connect(os.environ.get("HIRING_RADAR_DB", "data/hiring-radar.db"))
    db.migrate(conn)
    result = remove(conn, commit=not args.dry_run, keep=set(args.keep))
    verb = "would remove" if args.dry_run else "removed"
    for r in result["removed"]:
        print(f"{verb} job {r['id']}: {r['company']!r} — {r['title']!r} ({r['mentions']} mentions)")
    for r in result["kept"]:
        print(f"KEPT job {r['id']} ({r['held_because']}): {r['company']!r} — {r['title']!r}")
    print(f"{verb}: {len(result['removed'])} job(s), "
          f"{sum(r['mentions'] for r in result['removed'])} skill mention(s); "
          f"kept: {len(result['kept'])}")


if __name__ == "__main__":
    main()
