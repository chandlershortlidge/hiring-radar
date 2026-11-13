"""One-off: give every stored job all the places its stored location names (HIR-289).

Migration 022 copies each job's one city into `job_place`. A job stored before then whose
location named more of our cities ("San Francisco; New York City") still counts under the
first only. Postings still on a board get the rest on the next poll; this reaches the jobs
no longer listed, which still count in the 30-day, 90-day and all-time views.

Reads `job.location_raw` (the location as first stored) through `geo.places_of`, and only
adds rows: nothing is deleted, `job.city` is not touched. Prints, per place, how many jobs
gain it. Safe to run twice: the second run adds nothing.

It cannot recover the city of a per-city copy merged into another job before the table
existed: the copy's location was never stored. Those come back on the next poll.

    uv run python scripts/backfill_places.py --dry-run
    uv run python scripts/backfill_places.py
"""

import argparse
import os
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db  # noqa: E402
from app.geo import places_of  # noqa: E402


def backfill(conn: sqlite3.Connection, commit: bool = True) -> dict[str, int]:
    """{place: jobs that gained it}. With commit=False the additions are rolled back."""
    gained: Counter = Counter()
    try:
        for r in conn.execute("SELECT id, location_raw, title, description_text FROM job").fetchall():
            for place in places_of(r["location_raw"], r["title"], r["description_text"]):
                if conn.execute("INSERT OR IGNORE INTO job_place (job_id, place) VALUES (?, ?)",
                                (r["id"], place)).rowcount:
                    gained[place] += 1
    except Exception:
        conn.rollback()
        raise
    conn.commit() if commit else conn.rollback()
    return dict(sorted(gained.items()))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    conn = db.connect(os.environ.get("HIRING_RADAR_DB", "data/hiring-radar.db"))
    db.migrate(conn)
    print(("dry run, nothing written: " if args.dry_run else "") + str(backfill(conn, commit=not args.dry_run)))


if __name__ == "__main__":
    main()
