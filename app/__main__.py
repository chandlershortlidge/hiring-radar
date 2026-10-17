"""Command line: `uv run python -m app <command>`.

  poll              fetch all enabled feeds, ingest, extract skills for new jobs
  extract           extract skills for any job still missing them (e.g. after a taxonomy bump)
  add-text          add one job from pasted text (reads stdin): --company --title --location --found-via
  add-screenshot    add one job from an image file (stage 1 vision → stage 2): same flags + path
  check             is this careers-page URL already in the DB? If not, why no feed stored it. --add ingests it
  stats             counts by city and source; feed coverage of manually added jobs
  migrate           apply pending migrations and exit

Database path: $HIRING_RADAR_DB, default ./data/hiring-radar.db.
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

from app import db  # noqa: E402
from app.check import check_url  # noqa: E402
from app.extract import DEFAULT_MODEL, extract, make_client  # noqa: E402
from app.ingest import ingest_one, job_id_for_screenshot, now_iso, store_screenshot  # noqa: E402
from app.pipeline import extract_pending  # noqa: E402
from app.poll import load_feeds, poll_feeds  # noqa: E402
from app.sources import Posting  # noqa: E402
from app.taxonomy import Taxonomy  # noqa: E402
from app.transcribe import DEFAULT_MODEL as VISION_MODEL, transcribe  # noqa: E402

DB_PATH = Path(os.environ.get("HIRING_RADAR_DB", ROOT / "data" / "hiring-radar.db"))


def open_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = db.connect(DB_PATH)
    applied = db.migrate(conn)
    if applied:
        print(f"applied migrations: {applied}")
    return conn


def run_extraction(conn, limit=None):
    tax = Taxonomy.load()
    client = make_client()
    report = extract_pending(conn, tax, lambda text, t, m: extract(text, t, client, m), DEFAULT_MODEL, limit)
    print(report.line())
    return report


def cmd_poll(args):
    conn = open_db()
    r = poll_feeds(conn, load_feeds())
    print(f"TOTAL {r.line()}")
    if args.no_extract:
        return
    run_extraction(conn)


def cmd_extract(args):
    run_extraction(open_db(), args.limit)


def cmd_add_text(args):
    text = sys.stdin.read().strip()
    if not text:
        sys.exit("no text on stdin")
    conn = open_db()
    p = Posting(source="paste", source_job_id="", url=args.url or "", company=args.company,
                title=args.title, location_raw=args.location, description_text=text)
    outcome = ingest_one(conn, p, now_iso(), require_city=False, found_via=args.found_via, trust_title=True)
    print(outcome)
    if outcome.startswith("new:") and not args.no_extract:
        run_extraction(conn)


def cmd_add_screenshot(args):
    data = Path(args.path).read_bytes()
    conn = open_db()
    import hashlib
    existing = job_id_for_screenshot(conn, hashlib.sha256(data).hexdigest())
    if existing:
        print(f"already added as job {existing}")
        return
    t = transcribe(data, make_client(), VISION_MODEL)
    p = Posting(source="screenshot", source_job_id="", url=args.url or "", company=args.company,
                title=args.title, location_raw=args.location, description_text=t.text)
    outcome = ingest_one(conn, p, now_iso(), require_city=False, found_via=args.found_via, trust_title=True)
    print(outcome)
    job_id = int(outcome[4:]) if outcome.startswith("new:") else None
    if job_id:
        store_screenshot(conn, job_id, data, t.sha256, t.media_type)
        if not args.no_extract:
            run_extraction(conn)


def cmd_check(args):
    conn = open_db()
    r = check_url(conn, args.url, load_feeds(), args.company, args.title, args.location)
    print(r.line())
    for n in r.notes:
        print(f"  note: {n}")
    if not args.add or r.posting is None:
        return
    # Board postings keep their feed source and id, so a later poll sees them as still-listed;
    # page postings are source=url. Either way found_via records that a person found it.
    is_board = r.posting.source in ("greenhouse", "lever", "ashby")
    outcome = ingest_one(conn, r.posting, now_iso(), require_city=not is_board,
                         found_via=args.found_via, trust_title=True)
    print(f"add: {outcome}")
    if outcome.startswith("new:") and not args.no_extract:
        run_extraction(conn)


def cmd_stats(args):
    conn = open_db()
    print("jobs by city:")
    for r in conn.execute("SELECT coalesce(city,'(none)') c, count(*) n FROM job GROUP BY c ORDER BY n DESC"):
        print(f"  {r['c']:<16}{r['n']}")
    print("sightings by source:")
    for r in conn.execute("SELECT source, count(*) n FROM job_source GROUP BY source ORDER BY n DESC"):
        print(f"  {r['source']:<16}{r['n']}")
    manual = conn.execute("""
        SELECT count(DISTINCT j.id) total,
               count(DISTINCT CASE WHEN f.job_id IS NOT NULL THEN j.id END) covered
        FROM job j
        JOIN job_source m ON m.job_id = j.id AND m.source IN ('url','paste','screenshot')
        LEFT JOIN job_source f ON f.job_id = j.id AND f.source NOT IN ('url','paste','screenshot')
    """).fetchone()
    if manual["total"]:
        print(f"feed coverage of manually added jobs: {manual['covered']}/{manual['total']}")
    pending = conn.execute("SELECT count(*) FROM proposed_skill WHERE status='pending'").fetchone()[0]
    print(f"proposed skills pending review: {pending}")


def cmd_migrate(args):
    open_db()
    print("ok")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m app", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("poll"); p.add_argument("--no-extract", action="store_true"); p.set_defaults(fn=cmd_poll)
    p = sub.add_parser("extract"); p.add_argument("--limit", type=int); p.set_defaults(fn=cmd_extract)
    p = sub.add_parser("add-text")
    p.add_argument("--company", required=True); p.add_argument("--title", required=True)
    p.add_argument("--location", default=None); p.add_argument("--url", default=None)
    p.add_argument("--found-via", default="linkedin", choices=["linkedin", "indeed", "company_site", "referral", "other"])
    p.add_argument("--no-extract", action="store_true"); p.set_defaults(fn=cmd_add_text)
    p = sub.add_parser("add-screenshot")
    p.add_argument("path")
    p.add_argument("--company", required=True); p.add_argument("--title", required=True)
    p.add_argument("--location", default=None); p.add_argument("--url", default=None)
    p.add_argument("--found-via", default="linkedin", choices=["linkedin", "indeed", "company_site", "referral", "other"])
    p.add_argument("--no-extract", action="store_true"); p.set_defaults(fn=cmd_add_screenshot)
    p = sub.add_parser("check")
    p.add_argument("url")
    p.add_argument("--company", default=None); p.add_argument("--title", default=None)
    p.add_argument("--location", default=None)
    p.add_argument("--add", action="store_true", help="ingest the posting if not already stored (and extract)")
    p.add_argument("--found-via", default="company_site", choices=["linkedin", "indeed", "company_site", "referral", "other"])
    p.add_argument("--no-extract", action="store_true"); p.set_defaults(fn=cmd_check)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    sub.add_parser("migrate").set_defaults(fn=cmd_migrate)
    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
