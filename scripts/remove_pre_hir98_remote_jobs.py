"""One-off: delete stored jobs that only reached `Remote (EU)` through the pre-HIR-98 stamp.

Until 2026-11-01 ~18:06 UTC `app/sources/arbeitnow.py` appended "(remote, Germany)" to the
location of every posting the feed marked remote, whatever its real place. `geo._EU_WIDE`
matched the injected word, so those postings were stored as `Remote (EU)` and ingest's city
filter could never drop them. HIR-98 fixed intake; the rows stored in that window are what
this script removes (HIR-110).

Selects by re-applying today's rule: it strips the fabricated suffix, runs the bare location
back through `app.sources.arbeitnow._location` and `app.geo.active_place`, and treats a row
as a candidate only when today's intake would have given it a different place. So it can
never remove a row the current code would have kept, and it does not depend on row ids
staying what they were when the database was last read.

Does NOT decide on its own which candidate to delete. `geo` has no notion of "this place is
in Germany" (HIR-102), so a remote posting at an untracked German city — Stuttgart,
Würzburg — looks identical to a remote posting at a non-EU city, while DECISIONS 2026-10-26
counts the German one as EU-remote and keeps it. That judgment is a person's, so a candidate
is deleted only when its id is passed to `--confirm`, and an id that is not a candidate is
refused rather than deleted.

Does NOT touch rows whose stamp came from a feed that supplies its own country:
`app/sources/startup_jobs.py` builds the same "(remote, <country>)" string out of the
feed's `location.country`, which was never fabricated, so only arbeitnow-sourced rows are
candidates.

Does NOT blank a place instead of deleting: a job with no city still counts on the chart,
because `queries.job_set_clause` constrains `j.city` only when a city filter is chosen.

Deleting a job cascades to its skill mentions, extraction rejects, feed-source rows and
screenshot; it refuses to run with foreign keys off, which would orphan them instead.

**Take a fresh backup first and confirm it landed** (`deploy/README.md` → "Backups"). A
delete has no other undo.

Safe to run twice: the second run finds nothing.

    uv run python scripts/remove_pre_hir98_remote_jobs.py --dry-run
    uv run python scripts/remove_pre_hir98_remote_jobs.py --confirm 278
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db, geo  # noqa: E402
from app.sources.arbeitnow import SOURCE as ARBEITNOW, _location  # noqa: E402

# What the pre-HIR-98 adapter appended to a remote posting's location.
STAMP = " (remote, Germany)"


def _place_today(bare: str, title: str | None, text: str | None) -> str | None:
    """The place today's intake would store for this posting, from its real location."""
    return geo.active_place(_location({"location": bare, "remote": True}), title, text)


def candidates(conn: sqlite3.Connection) -> list[dict]:
    """Pure read: the stamped arbeitnow rows today's intake would place differently.

    Each dict carries `bare` (the location the feed actually sent) and `place_today`
    (None when today's intake would not have stored the posting at all).
    """
    rows = conn.execute(
        "SELECT j.id, j.company, j.title, j.city, j.location_raw, j.description_text, "
        "  (SELECT COUNT(*) FROM skill_mention m WHERE m.job_id = j.id) AS mentions, "
        "  (SELECT COUNT(*) FROM extraction_reject r WHERE r.job_id = j.id) AS rejects, "
        "  (SELECT GROUP_CONCAT(DISTINCT s.source) FROM job_source s WHERE s.job_id = j.id) AS sources "
        "FROM job j WHERE j.location_raw LIKE ? ORDER BY j.id", (f"%{STAMP}",)).fetchall()
    out: list[dict] = []
    for r in rows:
        if ARBEITNOW not in [s for s in (r["sources"] or "").split(",") if s]:
            continue
        bare = (r["location_raw"] or "")[: -len(STAMP)]
        place = _place_today(bare, r["title"], r["description_text"])
        if place == r["city"]:
            continue
        out.append({"id": r["id"], "company": r["company"], "title": r["title"],
                    "city": r["city"], "location_raw": r["location_raw"], "bare": bare,
                    "place_today": place, "mentions": r["mentions"], "rejects": r["rejects"]})
    return out


def remove(conn: sqlite3.Connection, confirm: set[int], commit: bool = True) -> dict:
    """Delete the confirmed candidates in one transaction; with commit=False, roll back.

    Raises if an id in `confirm` is not a candidate — that id either never carried the
    stamp or is placed the same way by today's code, so deleting it is not this cleanup.
    """
    if not conn.execute("PRAGMA foreign_keys").fetchone()[0]:
        raise RuntimeError(
            "foreign keys are off: deleting a job would orphan its skill mentions. "
            "Open the database with app.db.connect.")
    found = candidates(conn)
    unknown = confirm - {c["id"] for c in found}
    if unknown:
        raise RuntimeError(
            f"not candidates for this cleanup: {sorted(unknown)}. Today's intake places "
            "these jobs exactly as they are stored, or they never carried the stamp; "
            "run --dry-run to see the candidate list.")
    removing = [c for c in found if c["id"] in confirm]
    try:
        for c in removing:
            conn.execute("DELETE FROM job WHERE id = ?", (c["id"],))
    except Exception:
        conn.rollback()
        raise
    conn.commit() if commit else conn.rollback()
    return {"removed": removing, "left": [c for c in found if c["id"] not in confirm]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--confirm", type=int, action="append", default=[], metavar="JOB_ID",
                    help="a candidate to delete (repeatable). Required: the script never "
                         "picks for you, because geo cannot tell an untracked German city "
                         "from a non-EU one (HIR-102) and the German ones stay.")
    args = ap.parse_args()
    conn = db.connect(os.environ.get("HIRING_RADAR_DB", "data/hiring-radar.db"))
    db.migrate(conn)
    result = remove(conn, confirm=set(args.confirm), commit=not args.dry_run)
    verb = "would remove" if args.dry_run else "removed"
    for c in result["removed"]:
        print(f"{verb} job {c['id']}: {c['company']!r} — {c['title']!r} "
              f"[{c['location_raw']!r} -> today {c['place_today']!r}] "
              f"({c['mentions']} mentions, {c['rejects']} rejects)")
    for c in result["left"]:
        print(f"CANDIDATE job {c['id']} (not confirmed): {c['company']!r} — {c['title']!r} "
              f"[{c['bare']!r} -> today {c['place_today']!r}]")
    print(f"{verb}: {len(result['removed'])} job(s), "
          f"{sum(c['mentions'] for c in result['removed'])} skill mention(s); "
          f"candidates left: {len(result['left'])}")


if __name__ == "__main__":
    main()
