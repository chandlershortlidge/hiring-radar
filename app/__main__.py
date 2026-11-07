"""Command line: `uv run python -m app <command>`.

  poll              fetch all enabled feeds, ingest, extract skills for new jobs; --only ashby:jupus polls one feed
  extract           extract skills for any job still missing them (e.g. after a taxonomy bump)
  add-text          add one job from pasted text (reads stdin): --company --title --location --found-via
  add-screenshot    add one job from an image file (stage 1 vision → stage 2): same flags + path
  check             is this careers-page URL already in the DB? If not, why no feed stored it. --add ingests it;
                    every check is logged for the coverage line in `stats`. Takes many URLs, or --file urls.txt
  stats             counts by city and source; share of jobs a feed has seen (legacy imports excluded);
                    checked URLs split by whether a feed can reach them now
  discover-boards   web-search for Greenhouse/Lever/Ashby/JOIN boards we don't poll, check each live, report;
                    --add source:token appends to feeds.json, --reject source:token --reason R remembers a no;
                    --launch CITY applies the written board policy itself and adds what passes
  repair-companies  fill in companies on jobs stored without one and merge the duplicates
                    that appear; a dry run by default, --apply writes (HIR-198)
  migrate           apply pending migrations and exit

Database path: $HIRING_RADAR_DB, default ./data/hiring-radar.db.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

from app import add, db  # noqa: E402
from app.check import check_url, checked_coverage, job_coverage, log_check, reach_breakdown  # noqa: E402
from app.extract import DEFAULT_MODEL, extract, make_client  # noqa: E402
from app.ingest import ingest_one, job_id_for_screenshot, now_iso, store_screenshot  # noqa: E402
from app.labels import import_answers  # noqa: E402
from app.pipeline import extract_pending, unlogged_extractions  # noqa: E402
from app.poll import FEEDS_PATH, load_feeds, poll_feeds, select_feeds  # noqa: E402
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


def run_extraction(conn, limit=None, job_ids=None):
    """Extract pending jobs; `job_ids` narrows to those jobs. The add commands pass the one job
    they added, so adding a posting never triggers a full re-extract after a version bump."""
    tax = Taxonomy.load()
    client = make_client()
    report = extract_pending(conn, tax, lambda text, t, m: extract(text, t, client, m), DEFAULT_MODEL, limit,
                             job_ids=job_ids)
    print(report.line())
    print(report.log_line(unlogged_extractions(conn)))
    if job_ids is None and report.all_blank:
        sys.exit(f"ERROR: extraction produced zero skills across all {report.attempted} jobs"
                 " — the extractor is broken (prompt, schema, key or model), not the postings."
                 " Nothing was dropped; the stored answers carry the current version and WILL NOT"
                 " be retried until the extractor changes (HIR-193).")
    return report


def cmd_import_labels(args):
    """Load each labeller's own answer from the run folders, so the panel's disagreement is
    data in the database and not only files on someone's disk (HIR-170)."""
    print(import_answers(open_db()).line())


def cmd_poll(args):
    try:
        feeds = select_feeds(load_feeds(), args.only)
    except ValueError as e:
        sys.exit(str(e))
    conn = open_db()
    r = poll_feeds(conn, feeds)
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
        run_extraction(conn, job_ids=[int(outcome[4:])])


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
            run_extraction(conn, job_ids=[job_id])


def check_urls_from(args) -> list[str]:
    """URLs from the arguments plus --file (one per line, `-` = stdin; blanks and # lines skipped), deduplicated in order."""
    urls = list(args.url)
    if args.file:
        lines = (sys.stdin if args.file == "-" else open(args.file)).read().splitlines()
        urls += [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    return list(dict.fromkeys(urls))


def cmd_check(args):
    urls = check_urls_from(args)
    if not urls:
        sys.exit("no URLs given")
    if len(urls) > 1 and (args.title or args.location):   # --company is fine: one company's board
        sys.exit("--title/--location describe one posting; check that URL on its own")
    conn = open_db()
    feeds = load_feeds()
    for url in urls:
        if len(urls) > 1:
            print(f"== {url}")
        try:
            check_one(conn, url, feeds, args)
        except Exception as e:  # one dead page must not stop a batch
            print(f"error: {type(e).__name__}: {str(e)[:200]}")


def check_one(conn, url, feeds, args):
    r = check_url(conn, url, feeds, args.company, args.title, args.location)
    log_check(conn, r, args.found_via, now_iso())
    print(r.line())
    for n in r.notes:
        print(f"  note: {n}")
    if not args.add or r.posting is None:
        return
    # Every add-by-link rule lives in app/add.py, so the CLI and /api/add/url cannot drift.
    d = add.decide(r)
    if d.action == add.EXISTS:
        print(f"add: skipped — already job {d.job_id}")
        return
    if d.action == add.NEEDS_COMPANY:
        print("add: refused — no company found on the page; pass --company")
        return
    if d.action == add.TOO_SHORT:
        print(f"add: refused — only {d.characters} characters of posting text; "
              f"paste it with add-text instead")
        return
    outcome = ingest_one(conn, r.posting, now_iso(), require_city=d.require_city,
                         found_via=args.found_via, trust_title=True)
    print(f"add: {outcome}")
    if outcome.startswith("new:") and not args.no_extract:
        run_extraction(conn, job_ids=[int(outcome[4:])])


def cmd_stats(args):
    conn = open_db()
    print("jobs by city:")
    for r in conn.execute("SELECT coalesce(city,'(none)') c, count(*) n FROM job GROUP BY c ORDER BY n DESC"):
        print(f"  {r['c']:<16}{r['n']}")
    print("sightings by source:")
    for r in conn.execute("SELECT source, count(*) n FROM job_source GROUP BY source ORDER BY n DESC"):
        print(f"  {r['source']:<16}{r['n']}")
    seen, counted, legacy = job_coverage(conn)
    if counted:
        print(f"jobs a feed has seen: {seen}/{counted} ({seen / counted:.0%}); "
              f"{counted - seen} added by hand only (excludes {legacy} legacy imports)")
    covered, checked = checked_coverage(conn)
    if checked:
        print(f"checked URLs (first check each): {checked}, feed already had {covered} ({covered / checked:.0%})")
        for kind, n in reach_breakdown(conn, load_feeds()).items():
            print(f"  {kind:<22}{n}")
    pending = conn.execute("SELECT count(*) FROM proposed_skill WHERE status='pending'").fetchone()[0]
    print(f"proposed skills pending review: {pending}")


def cmd_discover_boards(args):
    from datetime import date

    from app import discover
    from app.sources import brave
    if args.reject and not args.reason:
        sys.exit("--reject needs --reason")
    if args.add or args.reject:   # approval only: no search
        try:
            for b in args.add:
                added = discover.add_board(discover.parse_board(b))
                print(f"{b}: {'added to' if added else 'already in'} config/feeds.json")
            for b in args.reject:
                done = discover.reject_board(discover.parse_board(b), args.reason, date.today().isoformat())
                print(f"{b}: {'added to' if done else 'already in'} config/boards_rejected.json")
        except ValueError as e:
            sys.exit(str(e))
        return
    try:
        key = brave.api_key()
    except brave.MissingKey as e:
        sys.exit(str(e))
    config = json.loads(discover.CONFIG_PATH.read_text())
    r = discover.run(config, json.loads(FEEDS_PATH.read_text()), json.loads(discover.REJECTED_PATH.read_text()),
                     lambda q: brave.fetch(q, key, config.get("count", 20)), city=args.launch)
    for line in discover.report_lines(r):
        print(line)
    if not args.launch:
        return
    from app.geo import ACTIVE_CITIES
    if args.launch not in ACTIVE_CITIES:
        sys.exit(f"{args.launch!r} is not collected; add it to geo.ACTIVE_CITIES first")
    decisions = discover.launch_decisions(r.candidates)
    cost, daily, breach = discover.launch_caps(decisions)
    applied = not breach and not args.dry_run
    if applied:
        for d in decisions:
            if d.verdict == "add":
                discover.add_board(d.board)
    print()
    for line in discover.launch_report_lines(args.launch, decisions, cost, daily, breach, applied):
        print(line)
    if breach:
        sys.exit(2)


def cmd_repair_companies(args):
    from app.repair import repair_companies
    conn = open_db()
    lines = repair_companies(conn)
    if not lines:
        print("no jobs with a blank company — nothing to repair")
        return
    unresolved = [l for l in lines if l.company is None]
    for l in lines:
        if l.company is not None:
            print(l.line())
    if unresolved:
        print(f"\n{len(unresolved)} unresolved (left as they are; fix by hand):")
        for l in unresolved:
            print(f"  {l.line()}")
    if args.apply:
        conn.commit()
        merges = sum(1 for l in lines if l.merged_into is not None or l.absorbed is not None)
        print(f"\napplied: {len(lines) - len(unresolved)} repaired, {merges} duplicate(s) merged")
    else:
        conn.rollback()
        print("\ndry run — nothing written; re-run with --apply")


def cmd_migrate(args):
    open_db()
    print("ok")


def cmd_serve(args):
    import uvicorn
    open_db().close()  # apply migrations before the first request
    print(f"hiring-radar on http://{args.host}:{args.port}  (db: {DB_PATH})")
    uvicorn.run("app.api:factory", factory=True, host=args.host, port=args.port, reload=args.reload)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m app", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("poll"); p.add_argument("--no-extract", action="store_true")
    p.add_argument("--only", action="append", default=[], metavar="LABEL",
                   help="poll just this feed, by its log label (e.g. ashby:jupus); repeatable")
    p.set_defaults(fn=cmd_poll)
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
    p.add_argument("url", nargs="*")
    p.add_argument("--file", default=None, help="more URLs, one per line; - reads stdin")
    p.add_argument("--company", default=None); p.add_argument("--title", default=None)
    p.add_argument("--location", default=None)
    p.add_argument("--add", action="store_true", help="ingest the posting if not already stored (and extract)")
    p.add_argument("--found-via", default="company_site", choices=["linkedin", "indeed", "company_site", "referral", "other"])
    p.add_argument("--no-extract", action="store_true"); p.set_defaults(fn=cmd_check)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    p = sub.add_parser("discover-boards", help="find company job boards we don't poll yet (Brave search)")
    p.add_argument("--add", action="append", default=[], metavar="SOURCE:TOKEN")
    p.add_argument("--reject", action="append", default=[], metavar="SOURCE:TOKEN")
    p.add_argument("--reason", default=None)
    p.add_argument("--launch", metavar="CITY", default=None,
                   help="judge boards for this one city and add what the written policy allows "
                        "(5+ roles there, employers only), then report; stops on a spending cap")
    p.add_argument("--dry-run", action="store_true", help="with --launch: decide and report, write nothing")
    p.set_defaults(fn=cmd_discover_boards)
    p = sub.add_parser("repair-companies", help="fill blank companies off each job's stored link, merge duplicates")
    p.add_argument("--apply", action="store_true", help="write the repairs; without it, a dry run that changes nothing")
    p.set_defaults(fn=cmd_repair_companies)
    sub.add_parser("migrate").set_defaults(fn=cmd_migrate)
    sub.add_parser("import-labels",
                   help="load each labeller's own answer from evals/labeling/<run>/raw into the database"
                   ).set_defaults(fn=cmd_import_labels)
    p = sub.add_parser("serve", help="run the dashboard API (and web/dist if built)")
    p.add_argument("--host", default="127.0.0.1"); p.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8000)))
    p.add_argument("--reload", action="store_true"); p.set_defaults(fn=cmd_serve)
    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
