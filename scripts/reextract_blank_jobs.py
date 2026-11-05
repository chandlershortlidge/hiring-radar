"""One-off: un-stamp jobs whose stored extraction came back entirely blank, so they are read again.

HIR-172: before the fix in `app/extract.py`, a well-formed but entirely empty tool call
counted as a success. The job was stamped with the extractor version and stored with no
skills, no seniority, no German requirement, no degree and no production signal — so
nothing downstream ever looked at it again, and the poll line reported it as extracted.
Two such jobs are in the database (84 pplwise, 569 Accenture, both with a few thousand
characters of real job description).

Clearing `extracted_version` is all that is needed to have them read again: `app.pipeline`
picks up any job whose stamp is not the current extractor version, so the next `poll` or
`extract` reads these jobs again — one model call each, cents. With the fix in place, a
repeat of the empty call now fails loudly instead of being stored as a blank success.

It also counts the blank reading already stored as the posting's first (`blank_extractions`
= 1), so the handling is the same whether a job is new or already stored: one more attempt,
and a second blank reading drops the posting (Chandler's decision of 5 Nov). Without that,
these two jobs would silently get three attempts where a new one gets two.

Selects only the shape the fix now rejects: no skill mentions, no extraction rejects, no
proposed skills, and none of the four attributes. A job with zero skills that still states
a seniority (57, 88, 253, 440, 518) is a legitimate extraction and is left alone.

Does NOT delete anything — no job, no mention, no row. Does NOT touch jobs stamped
'legacy' (they carry the old summary, not the posting) or jobs already pending. Does NOT
re-read anything itself: it makes no model call, it only clears the stamp.

Short postings are skipped (`--min-chars`, default 1000): a job with almost no description
legitimately has nothing to find, and un-stamping it would make every poll pay for the
same empty read and report it as a failure for ever.

Safe to run twice: the second run finds nothing (the jobs are pending, not blank-stamped).

    uv run python scripts/reextract_blank_jobs.py --dry-run
    uv run python scripts/reextract_blank_jobs.py
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db  # noqa: E402

BLANK_SQL = """
SELECT j.id, j.company, j.title, j.extracted_version, length(j.description_text) AS chars
FROM job j
WHERE j.extracted_version IS NOT NULL
  AND j.extracted_version != 'legacy'
  AND j.seniority IS NULL AND j.german IS NULL AND j.degree IS NULL AND j.production IS NULL
  AND NOT EXISTS (SELECT 1 FROM skill_mention m WHERE m.job_id = j.id)
  AND NOT EXISTS (SELECT 1 FROM extraction_reject r WHERE r.job_id = j.id)
  AND NOT EXISTS (SELECT 1 FROM proposed_skill p WHERE p.job_id = j.id)
ORDER BY j.id
"""


def classify(conn: sqlite3.Connection, min_chars: int = 1000) -> tuple[list[dict], list[dict]]:
    """Pure read: (blank jobs to un-stamp, blank jobs left alone because they are too short).

    The second list is for a human to look at; a posting that short has nothing to find,
    so reading it again would only buy a failure on every future poll.
    """
    blank, short = [], []
    for r in conn.execute(BLANK_SQL).fetchall():
        (blank if (r["chars"] or 0) >= min_chars else short).append(dict(r))
    return blank, short


def unstamp(conn: sqlite3.Connection, commit: bool = True, min_chars: int = 1000) -> dict:
    """Clear `extracted_version` on the blank jobs in one transaction; commit=False rolls back."""
    blank, short = classify(conn, min_chars)
    try:
        for r in blank:
            conn.execute(
                "UPDATE job SET extracted_version = NULL,"
                " blank_extractions = max(blank_extractions, 1) WHERE id = ?", (r["id"],))
    except Exception:
        conn.rollback()
        raise
    conn.commit() if commit else conn.rollback()
    return {"unstamped": blank, "skipped": short}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--min-chars", type=int, default=1000,
                    help="leave a blank job alone when its description is shorter than this")
    args = ap.parse_args()
    conn = db.connect(os.environ.get("HIRING_RADAR_DB", "data/hiring-radar.db"))
    db.migrate(conn)
    result = unstamp(conn, commit=not args.dry_run, min_chars=args.min_chars)
    verb = "would un-stamp" if args.dry_run else "un-stamped"
    for r in result["unstamped"]:
        print(f"{verb} job {r['id']}: {r['company']!r} — {r['title']!r} ({r['chars']} chars)")
    for r in result["skipped"]:
        print(f"SKIPPED job {r['id']} (only {r['chars']} chars): {r['company']!r} — {r['title']!r}")
    print(f"{verb}: {len(result['unstamped'])} job(s); skipped: {len(result['skipped'])}. "
          "They are read again on the next poll or extract.")


if __name__ == "__main__":
    main()
