"""One-off: give jobs added from a Workable link their full posting text, so they are read again.

HIR-268: a Workable job page is built in the browser, so before the fix in `app/check.py`
a job added from an `apply.workable.com` link was stored with the page's meta description
as its whole text — a summary Workable cuts off at about 250 characters. One such job is in
the database (742, Control Risks, "AI Engineer"). The model read that stub as blank, which
counts as the first of the two blank reads that delete a posting, so the next poll would
have read the same stub again and dropped the job.

For every job stored from a Workable link, this fetches the posting from Workable's public
job API (the same reading `check` now does) and, when that text is longer than what is
stored, replaces the stored text, clears `extracted_version` so `app.pipeline` reads the
job on the next `poll` or `extract` (one model call, cents), and sets `blank_extractions`
back to 0: the blank read was of the stub, not of this text.

Does NOT delete anything, and does NOT touch the job's title, company, city or stored
location — a person set those when adding the job. Does NOT re-read anything itself: it
makes no model call. A job whose stored text is already at least as long as the API's is
left alone, and so is one whose posting Workable no longer serves (reported, not changed).

Safe to run twice: the second run finds the stored text already as long as the API's.

    uv run python scripts/refresh_workable_jobs.py --dry-run
    uv run python scripts/refresh_workable_jobs.py
"""

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db  # noqa: E402
from app.check import posting_from_workable, workable_api_url  # noqa: E402
from app.sources import fetch_text  # noqa: E402

URL_JOBS_SQL = """
SELECT j.id, j.company, j.title, j.description_text, s.url
FROM job j JOIN job_source s ON s.job_id = j.id
WHERE s.source = 'url' AND s.url IS NOT NULL
ORDER BY j.id, s.id
"""


def refresh(conn: sqlite3.Connection, fetch=fetch_text, commit: bool = True) -> dict:
    """Replace the stored text of Workable-link jobs with the API's, in one transaction.

    Returns {"refreshed": [...], "unchanged": [...], "failed": [...]}, one dict per job with
    its id, company, title, the stored length (`chars`) and, where the API answered, the
    new length (`new_chars`); a failed one carries `error`. commit=False rolls back.
    """
    out: dict[str, list[dict]] = {"refreshed": [], "unchanged": [], "failed": []}
    seen: set[int] = set()
    try:
        for r in conn.execute(URL_JOBS_SQL).fetchall():
            api_url = workable_api_url(r["url"])
            if api_url is None or r["id"] in seen:
                continue
            seen.add(r["id"])
            row = {"id": r["id"], "company": r["company"], "title": r["title"],
                   "chars": len(r["description_text"] or "")}
            try:
                text = posting_from_workable(r["url"], json.loads(fetch(api_url))).description_text
            except Exception as e:  # posting taken down, API unreachable: report it, change nothing
                out["failed"].append({**row, "error": f"{type(e).__name__}: {str(e)[:120]}"})
                continue
            row["new_chars"] = len(text)
            if len(text) <= row["chars"]:
                out["unchanged"].append(row)
                continue
            conn.execute("UPDATE job SET description_text = ?, extracted_version = NULL,"
                         " blank_extractions = 0 WHERE id = ?", (text, r["id"]))
            out["refreshed"].append(row)
    except Exception:
        conn.rollback()
        raise
    conn.commit() if commit else conn.rollback()
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    conn = db.connect(os.environ.get("HIRING_RADAR_DB", "data/hiring-radar.db"))
    db.migrate(conn)
    result = refresh(conn, commit=not args.dry_run)
    verb = "would refresh" if args.dry_run else "refreshed"
    for r in result["refreshed"]:
        print(f"{verb} job {r['id']}: {r['company']!r} — {r['title']!r} "
              f"({r['chars']} → {r['new_chars']} chars)")
    for r in result["unchanged"]:
        print(f"left job {r['id']} alone (stored {r['chars']} chars, API {r['new_chars']}): "
              f"{r['company']!r} — {r['title']!r}")
    for r in result["failed"]:
        print(f"FAILED job {r['id']}: {r['company']!r} — {r['title']!r}: {r['error']}")
    print(f"{verb}: {len(result['refreshed'])} job(s); left alone: {len(result['unchanged'])}; "
          f"failed: {len(result['failed'])}. Refreshed jobs are read on the next poll or extract.")


if __name__ == "__main__":
    main()
