"""One-off: take `Remote (EU)` off stored jobs whose title or location names a non-EU country (HIR-455).

Job 1826, FullStack's "Senior Forward Deployed AI Engineer - LLMs & RAG - Remote - USA",
was stored under Remote (EU): an aggregator filed it under a German town and flagged it
remote, and the location rule read that as "remote, Germany". `geo.is_remote_eu` now lets
such a title outrank the location, so new postings like it are not collected. This script
finds the ones stored before the fix.

Does: list every stored job that has a `Remote (EU)` place which today's rule
(`geo.places_of` on the stored location, title and text) would not give it, and whose
title ties it to a non-EU country (`geo.title_restricts_to_non_eu`) or whose stored
location names one. With `--apply` it removes the `Remote (EU)` place from those jobs:
the `job_place` row goes, and `job.city` becomes the job's next place, or empty.

Does NOT delete a job, touch its skills, or call a model. A job left with no place is out
of every city and out of the remote view, but still counts when no place is chosen, as a
hand-added job with no place does; taking it out altogether means deleting it, which is
Chandler's call (AGENTS.md "What Chandler is asked", item 4).

Does NOT change a job found by its location alone when more than one posting was merged
into it: only the first posting's location is stored, so the `Remote (EU)` place may have
come from another sighting that really said so. Those are listed as "look" and left.

Does NOT decide whether it may run. Changing more than 5 stored jobs is on Chandler's
list; up to 5 is the senior agent's, after a trial on a copy and with last night's backup
in the bucket. The default is a dry run that writes nothing, which gives the count.

Safe to run twice: the second run finds nothing. To undo one job:
`INSERT INTO job_place (job_id, place) VALUES (<id>, 'Remote (EU)')`, and set `job.city`
back to 'Remote (EU)' where the dry run showed it.

    uv run python scripts/untag_non_eu_remote.py            # dry run: the list and the count
    uv run python scripts/untag_non_eu_remote.py --apply
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db, geo  # noqa: E402

TITLE, LOCATION = "title", "location"


def candidates(conn: sqlite3.Connection) -> list[dict]:
    """Pure read. Each dict carries `why` (TITLE or LOCATION), `fix` (False for a "look"
    row this script leaves alone) and `city_after` (what `job.city` becomes)."""
    rows = conn.execute(
        "SELECT j.id, j.company, j.title, j.city, j.location_raw, j.description_text, "
        "  (SELECT COUNT(*) FROM job_source s WHERE s.job_id = j.id) AS sightings "
        "FROM job j JOIN job_place p ON p.job_id = j.id AND p.place = ? ORDER BY j.id",
        (geo.REMOTE_EU,)).fetchall()
    out: list[dict] = []
    for r in rows:
        if geo.REMOTE_EU in geo.places_of(r["location_raw"], r["title"], r["description_text"]):
            continue
        if geo.title_restricts_to_non_eu(r["title"]):
            why = TITLE
        elif r["location_raw"] and geo._TITLE_NON_EU_COUNTRY.search(r["location_raw"]):
            why = LOCATION
        else:
            continue        # placed differently today for some other reason: not this cleanup
        others = [x[0] for x in conn.execute(
            "SELECT place FROM job_place WHERE job_id = ? AND place != ?", (r["id"], geo.REMOTE_EU))]
        others.sort(key=lambda place: list(geo.CITIES).index(place) if place in geo.CITIES else len(geo.CITIES))
        city_after = r["city"] if r["city"] != geo.REMOTE_EU else (others[0] if others else None)
        out.append({"id": r["id"], "company": r["company"], "title": r["title"], "city": r["city"],
                    "location_raw": r["location_raw"], "why": why, "city_after": city_after,
                    "fix": why == TITLE or r["sightings"] <= 1})
    return out


def untag(conn: sqlite3.Connection, commit: bool = False) -> dict:
    """Remove the Remote (EU) place from every fixable candidate, in one transaction; with
    commit=False, roll back. Returns {"fixed": [...], "look": [...]}."""
    found = candidates(conn)
    fixed = [c for c in found if c["fix"]]
    try:
        for c in fixed:
            conn.execute("DELETE FROM job_place WHERE job_id = ? AND place = ?", (c["id"], geo.REMOTE_EU))
            if c["city"] == geo.REMOTE_EU:
                conn.execute("UPDATE job SET city = ? WHERE id = ?", (c["city_after"], c["id"]))
    except Exception:
        conn.rollback()
        raise
    conn.commit() if commit else conn.rollback()
    return {"fixed": fixed, "look": [c for c in found if not c["fix"]]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the change (default: dry run)")
    args = ap.parse_args()
    conn = db.connect(os.environ.get("HIRING_RADAR_DB", "data/hiring-radar.db"))
    db.migrate(conn)
    result = untag(conn, commit=args.apply)
    verb = "untagged" if args.apply else "would untag"
    for c in result["fixed"]:
        print(f"{verb} job {c['id']} (by {c['why']}): {c['company']!r} — {c['title']!r} "
              f"[{c['location_raw']!r}; city {c['city']!r} -> {c['city_after']!r}]")
    for c in result["look"]:
        print(f"LOOK job {c['id']} (left alone, merged from several postings): {c['company']!r} — "
              f"{c['title']!r} [{c['location_raw']!r}]")
    print(f"{verb}: {len(result['fixed'])} job(s); left for a look: {len(result['look'])}")


if __name__ == "__main__":
    main()
