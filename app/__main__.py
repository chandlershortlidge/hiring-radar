"""Command line: `uv run python -m app <command>`.

  poll              fetch all enabled feeds, ingest, extract skills for new jobs; --only ashby:jupus polls one feed;
                    --launch CITY (a launch's first collection) reads only CITY's new jobs, after pricing them;
                    --region europe|us polls only that region's feeds (the VM's two daily runs, HIR-369).
                    Readings run as one Anthropic Message Batch — half price, waits for it to finish (HIR-222)
  extract           extract skills for any job still missing them (e.g. after a taxonomy bump); batches, as poll does
  read-pending      the one bulk read of a place or career track whose postings were stored unread
                    (read: later in app/scope.py): --city X and/or --family Y. Prints the job count and
                    the cost first; --dry-run stops there, a real run needs --cap EUR and stops above it.
                    Jobs keep the day they were first collected (HIR-396)
  sample            draw unread postings to build a skill list from: --family Y and/or --city X, --n 50,
                    spread across places and employers; --out FILE (default: prints JSON). No model call
  add-text          add one job from pasted text (reads stdin): --company --title --location --found-via
  add-screenshot    add one job from an image file (stage 1 vision → stage 2): same flags + path
  check             is this careers-page URL already in the DB? If not, why no feed stored it. --add ingests it;
                    every check is logged for the coverage line in `stats`. Takes many URLs, or --file urls.txt.
                    --city is the city the links were collected for (default Berlin): logged for a link
                    whose page gives no location (HIR-322).
                    Ends by copying the check log to the server, where misses are counted (HIR-294)
  receive-checks    the server's end of that copy: reads check records on stdin, stores the new ones
  stats             counts by city and source; share of jobs a feed has seen (legacy imports excluded);
                    checked URLs split by whether a feed can reach them now
  miss-reasons      why checked jobs were missed: count per reason, per city, per careers system;
                    --since/--until YYYY-MM-DD pick the range (HIR-290)
  discover-boards   web-search for Greenhouse/Lever/Ashby/JOIN boards we don't poll, check each live, report;
                    --add source:token appends to feeds.json, --reject source:token --reason R remembers a no;
                    --launch CITY applies the written board policy itself and adds what passes,
                    then runs backfill-places for that city
  backfill-places   credit stored jobs, open and closed, with every tracked city their location names
                    (a "Berlin, London" job stored before London was a city gains London). Only adds;
                    --city CITY limits it to one, --dry-run writes nothing. No model call (HIR-331)
  repair-companies  fill in companies on jobs stored without one and merge the duplicates
                    that appear; a dry run by default, --apply writes (HIR-198)
  reread-cost       what a change to the extractor or the skill list would cost to merge:
                    the jobs it would re-read x what a reading has actually cost. Makes no
                    model call. Put its figure in the PR body (HIR-221). Opens the database
                    read-only and never applies migrations (HIR-265)
  caretaker         the morning check of every job source after the poll: logs what is broken, files
                    the day's fixes to the list of job sources as one Linear ticket (never edits
                    feeds.json itself) and re-runs a collection that failed, once (HIR-261);
                    `caretaker apply-fixes FILE|-` makes a filed ticket's fixes in feeds.json, for
                    the pull request that carries the ticket out; Mondays, posts the Monday summary to Linear
                    when LINEAR_API_KEY is set: what needs Chandler, what merged, what was
                    sent back and fixed, what broke on the live site (read from the robot
                    visitor's Linear tickets), then the job sources (HIR-257, HIR-264, HIR-260)
                    Also files the ticket for company boards "Add a job" found missing (HIR-324)
  flags             why each job flagged "doesn't belong here" showed: every filter that was on
                    screen against what was stored and what the posting says, grouped by cause.
                    Makes no model call. --fixed ID [ID ...] closes flags whose cause is fixed,
                    which takes the "flagged" mark off their jobs (HIR-226)
  migrate           apply pending migrations and exit

Database path: $HIRING_RADAR_DB, default ./data/hiring-radar.db.
"""

import argparse
import json
import os
import sys
import urllib.parse
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent


def main_checkout_env(root: Path) -> Path | None:
    """The main checkout's `.env` when `root` is a git worktree, else None. `.env` is
    gitignored, so a worktree made for a ticket starts without one and the key was simply
    missing there (HIR-127). In a worktree `.git` is a file naming its git directory, and
    that directory's `commondir` points at the main checkout's `.git`."""
    try:
        gitdir = root / (root / ".git").read_text().split("gitdir:", 1)[1].strip()
        common = (gitdir / (gitdir / "commondir").read_text().strip()).resolve()
    except (OSError, IndexError):
        return None                      # a normal checkout (`.git` is a directory), or no git at all
    return common.parent / ".env"


# Earlier wins: the real environment, then this checkout's .env, then the main checkout's.
load_dotenv(ROOT / ".env")
if (_shared_env := main_checkout_env(ROOT)):
    load_dotenv(_shared_env)

from app import add, db, geo, langsmith_live, send_checks  # noqa: E402
from app.check import (assumed_city, check_url, checked_coverage, job_coverage, log_check,  # noqa: E402
                       reach_breakdown)
from app.extract import make_client  # noqa: E402
from app.ingest import Screenshot, job_id_for_screenshot, now_iso  # noqa: E402
from app.labels import import_answers  # noqa: E402
from app.pipeline import extract_pending, held_line, unlogged_extractions  # noqa: E402
from app.poll import FEEDS_PATH, load_feeds, poll_feeds, region_line, select_feeds, select_region  # noqa: E402
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


def require_anthropic_key():
    """Stop with one clear line when the key is missing. Without this the SDK looks for a
    credentials file instead and every job fails on its own with an error that never
    names the key: 510 identical lines on one poll (HIR-127)."""
    if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        sys.exit("ANTHROPIC_API_KEY is not set: add it to .env (see .env.example)")


def run_extraction(conn, limit=None, job_ids=None, run_kind=langsmith_live.REREAD, batch=False):
    """Extract pending jobs; `job_ids` narrows to those jobs. The add commands pass the one job
    they added, so adding a posting never triggers a full re-extract after a version bump.

    `run_kind` only names the run in LangSmith (HIR-160). `batch=True` submits the queue
    as one Anthropic Message Batch instead of one call per job (HIR-222) — the poll and a
    full re-read pass it; the add commands never do, since a person is waiting for that job."""
    require_anthropic_key()
    tax = Taxonomy.load()
    report = extract_pending(conn, tax, limit=limit, job_ids=job_ids, run_kind=run_kind, batch=batch)
    print(report.line())
    print(report.log_line(unlogged_extractions(conn)))
    if (line := report.cost_line()):
        print(line)
    if (line := report.grounding_line()):
        print(line)
    # The size of the run decides, not whether its jobs were named: a launch's first read
    # and read-pending name hundreds of jobs, and a hand-add's one job can never reach the
    # all-blank threshold (HIR-425).
    if report.all_blank:
        sys.exit(f"ERROR: extraction produced zero skills across all {report.attempted} jobs"
                 " — the extractor is broken (prompt, schema, key or model), not the postings."
                 " Nothing was dropped; the stored answers carry the current version and WILL NOT"
                 " be retried until the extractor changes (HIR-193).")
    return report


def current_version() -> str:
    from app.extract import DEFAULT_MODEL, extractor_version
    return extractor_version(Taxonomy.load(), DEFAULT_MODEL)


def print_held(conn):
    """One line for the jobs stored unread on purpose, kept apart from anything that
    failed to read; nothing when no place or track is set to read later (HIR-396)."""
    if (line := held_line(conn, current_version())):
        print(line)


def cmd_import_labels(args):
    """Load each labeller's own answer from the run folders, so the panel's disagreement is
    data in the database and not only files on someone's disk (HIR-170)."""
    print(import_answers(open_db()).line())


def cmd_poll(args):
    if not args.no_extract:
        require_anthropic_key()  # before the fetch, so no job is stored that cannot then be read
    try:
        feeds = select_feeds(select_region(load_feeds(), args.region), args.only)
    except ValueError as e:
        sys.exit(str(e))
    if args.region:
        print(region_line(args.region, feeds))
    if args.launch and args.launch not in geo.ACTIVE_CITIES:
        sys.exit(f"{args.launch!r} is not collected; add it to geo.ACTIVE_CITIES first")
    conn = open_db()
    r = poll_feeds(conn, feeds)
    print(f"TOTAL {r.line()}")
    print_held(conn)
    if args.no_extract:
        return
    if args.launch:   # a launch's first collection reads only the city's new jobs (HIR-380)
        launch_first_reading(conn, r.new_job_ids, args.launch)
        return
    run_extraction(conn, run_kind=langsmith_live.POLL, batch=True)


def launch_first_reading(conn, new_job_ids, city):
    from app import launch_read
    from app.extract import DEFAULT_MODEL, extractor_version
    plan = launch_read.plan(conn, new_job_ids, city, extractor_version(Taxonomy.load(), DEFAULT_MODEL))
    print()
    for line in plan.lines():
        print(line)
    if plan.over_cap:
        sys.exit(2)
    if plan.to_read:
        run_extraction(conn, job_ids=plan.to_read, run_kind=langsmith_live.POLL, batch=True)


def cmd_extract(args):
    conn = open_db()
    print_held(conn)
    run_extraction(conn, args.limit, run_kind=langsmith_live.REREAD, batch=True)


def cmd_read_pending(args):
    """The one bulk read of a place's or track's waiting jobs (HIR-396). The plan, its
    count and its cost come from app/read_pending.py; this prints it, stops on --dry-run or
    above the cap, and otherwise reads exactly those jobs as one batch."""
    from app import read_pending
    if not args.dry_run:
        if args.cap is None:
            sys.exit("read-pending: a real run needs --cap EUR, the most it may spend; "
                     "--dry-run prints the job count and the cost and reads nothing")
        require_anthropic_key()
    conn = open_db()
    try:
        plan = read_pending.plan(conn, current_version(), args.city, args.family, args.cap)
    except ValueError as e:
        sys.exit(str(e))
    for line in plan.lines():
        print(line)
    if args.dry_run:
        print("dry run: nothing read")
        return
    if plan.over_cap:
        sys.exit(2)
    if not plan.to_read:   # never an empty list to the pipeline: it reads the whole queue when given none
        return
    run_extraction(conn, job_ids=plan.to_read, run_kind=langsmith_live.BACKFILL, batch=True)
    print("While this place or track is still set to read later in app/scope.py, postings "
          "collected from now on wait again; set it to read now so the daily collection reads them.")


def cmd_sample(args):
    """Unread postings for building a skill list (HIR-396). No model call, nothing written
    to the database."""
    from app import sample
    try:
        pool = sample.unread(open_db(), args.family, args.city)
    except ValueError as e:
        sys.exit(str(e))
    picked = sample.spread(pool, args.n, args.seed)
    out = json.dumps({"family": args.family, "city": args.city, "seed": args.seed, "asked": args.n,
                      "available": len(pool), "postings": picked}, indent=2, ensure_ascii=False)
    summary = (f"sample: {len(picked)} of {len(pool)} unread postings, from "
               f"{len({p['company'] for p in picked})} employers")
    if args.out:
        Path(args.out).write_text(out + "\n")
        print(f"{summary}, written to {args.out}")
    else:
        print(out)
        print(summary, file=sys.stderr)


def cmd_add_text(args):
    text = sys.stdin.read().strip()
    if not text:
        sys.exit("no text on stdin")
    conn = open_db()
    p = Posting(source="paste", source_job_id="", url=args.url or "", company=args.company,
                title=args.title, location_raw=args.location, description_text=text)
    res = add.add_by_hand(conn, p, args.found_via)
    print(res.line())
    if res.is_new and not args.no_extract:
        run_extraction(conn, job_ids=[res.job_id], run_kind=langsmith_live.ADD)


def cmd_add_screenshot(args):
    data = Path(args.path).read_bytes()
    require_anthropic_key()  # the transcription below is a model call too
    conn = open_db()
    import hashlib
    existing = job_id_for_screenshot(conn, hashlib.sha256(data).hexdigest())
    if existing:
        print(f"already added as job {existing}")
        return
    t = transcribe(data, make_client(), VISION_MODEL)
    p = Posting(source="screenshot", source_job_id="", url=args.url or "", company=args.company,
                title=args.title, location_raw=args.location, description_text=t.text)
    # The image rides the same transaction as the job, so the two cannot come apart and
    # leave a job the next upload of this file would not recognise (HIR-210).
    res = add.add_by_hand(conn, p, args.found_via, screenshot=Screenshot(data, t.sha256, t.media_type))
    print(res.line())
    if res.is_new and not args.no_extract:
        run_extraction(conn, job_ids=[res.job_id], run_kind=langsmith_live.ADD)


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
    send_checks.after_check(conn, DB_PATH)


def cmd_receive_checks(args):
    try:
        records = json.loads(sys.stdin.read())["checks"]
        added, held = send_checks.receive(open_db(), records)
    except (ValueError, KeyError, TypeError) as e:
        sys.exit(f"receive-checks: {type(e).__name__}: {str(e)[:200]}")
    print(json.dumps({"added": added, "already_held": held}))


def check_one(conn, url, feeds, args):
    r = check_url(conn, url, feeds, args.company, args.title, args.location)
    log_check(conn, r, args.found_via, now_iso(), run_for=args.city)
    print(r.line())
    for n in r.notes:
        print(f"  note: {n}")
    if assumed_city(r, args.city):
        print(f"  note: no location on the page; city recorded as {args.city}, "
              f"the city this check is run for (--city)")
    if not args.add or r.posting is None:
        return
    # Every add-by-link rule lives in app/add.py, so no caller can drift from another.
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
    res = add.add_by_hand(conn, r.posting, args.found_via, require_city=d.require_city)
    print(f"add: {res.line()}")
    if res.is_new and not args.no_extract:
        run_extraction(conn, job_ids=[res.job_id], run_kind=langsmith_live.ADD)


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


def cmd_miss_reasons(args):
    from app import misses
    for line in misses.report_lines(misses.records(open_db(), args.since, args.until), args.since, args.until):
        print(line)


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
    if args.launch not in geo.REGION_OF:
        sys.exit(f"{args.launch!r} has no region, so neither daily poll covers it; add it to geo.REGION_OF first")
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
    from app.geo import CITIES
    if args.launch in CITIES:   # the stored jobs whose posting already named it (HIR-331)
        from app.backfill_places import backfill, report_lines
        print()
        for line in report_lines(backfill(open_db(), city=args.launch, apply=applied), args.launch):
            print(line)


def cmd_backfill_places(args):
    from app.backfill_places import backfill, report_lines
    try:
        b = backfill(open_db(), city=args.city, apply=not args.dry_run)
    except ValueError as e:
        sys.exit(str(e))
    for line in report_lines(b, args.city):
        print(line)


def cmd_markup_postings(args):
    """Count the stored postings whose text is web-page markup, by where they came from
    (HIR-420). Reads only. The job page shows them as text already; the model read the
    markup, which is what the list is for."""
    from app.html_text import looks_like_markup
    conn = open_db()
    ids = [r["id"] for r in conn.execute("SELECT id, description_text FROM job ORDER BY id")
           if looks_like_markup(r["description_text"] or "")]
    print(f"stored postings whose text is markup: {len(ids)}")
    by_source: dict[str, list[int]] = {}
    for job_id in ids:
        first = conn.execute("SELECT source, url FROM job_source WHERE job_id = ? ORDER BY first_seen, id"
                             " LIMIT 1", (job_id,)).fetchone()
        name = "(no source)" if first is None else " ".join(
            x for x in (first["source"], urllib.parse.urlsplit(first["url"] or "").hostname) if x)
        by_source.setdefault(name, []).append(job_id)
    for name, jobs in sorted(by_source.items(), key=lambda kv: -len(kv[1])):
        print(f"  {name:<44}{len(jobs):>5}   job ids: {', '.join(map(str, jobs[:10]))}{' ...' if len(jobs) > 10 else ''}")


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


def cmd_reread_cost(args):
    """The figure that goes in a PR body when the diff touches the extractor or skill list.

    Reads the database only; it never calls the model, so asking the question is free.

    Opened read-only and never migrated (HIR-265). Every other command opens the database
    with `open_db`, which applies this checkout's pending migrations; this one is run from
    ticket branches against the live database, where that recorded a branch's unmerged
    migration as applied."""
    import sqlite3

    from app.reread_cost import report_lines, reread_cost
    from app.taxonomy import Taxonomy
    if not DB_PATH.exists():
        sys.exit(f"reread-cost: no database at {DB_PATH}. Nothing was created; point "
                 "HIRING_RADAR_DB at the database to estimate for.")
    conn = db.connect_readonly(DB_PATH)
    try:
        # This checkout's own skill list: on a branch that only adds skills, the figure
        # counts only the jobs that would really be re-read (HIR-224).
        cost = reread_cost(conn, tax=Taxonomy.load())
    except sqlite3.OperationalError as e:
        if "no such table" not in str(e) and "no such column" not in str(e):
            raise
        sys.exit(f"reread-cost: the database at {DB_PATH} is older than this code and lacks "
                 f"something the estimate reads ({e}). Nothing was changed: reread-cost never "
                 "updates a database. Bring it up to date with `python -m app migrate` from "
                 "main, then ask again.")
    finally:
        conn.close()
    for line in report_lines(cost):
        print(line)


def cmd_caretaker_apply_fixes(args):
    """Make the fixes a caretaker ticket carries, in config/feeds.json (HIR-261). Run in
    the pull request that carries the ticket out, never on the server. All or nothing."""
    from app import caretaker
    if not args.file:
        sys.exit("caretaker apply-fixes: name the file holding the ticket's text, or - for standard input")
    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text()
    try:
        fixes = caretaker.fixes_from_text(text)
        doc = caretaker.apply_fixes(json.loads(FEEDS_PATH.read_text()), text)
        caretaker.write_feeds(doc, FEEDS_PATH)
    except caretaker.Refused as e:
        sys.exit(f"caretaker apply-fixes: refused, nothing was written: {e}")
    for f in fixes:
        print(f"{f.action:>16}  {f.subject}: {f.detail}")
    print(f"{len(fixes)} fix{'es' if len(fixes) != 1 else ''} written to {FEEDS_PATH.name}; commit that one file")


def cmd_caretaker(args):
    """The morning run (HIR-257), acting since HIR-261. Reads feeds.json and never writes
    it: the day's fixes are filed as a ticket, and `caretaker apply-fixes` makes them in
    the pull request that follows. A failed collection is re-run here, once."""
    if getattr(args, "action", None) == "apply-fixes":
        return cmd_caretaker_apply_fixes(args)
    import subprocess
    from datetime import datetime, timezone

    from app import caretaker_run
    from app.discover import REJECTED_PATH, rejected_boards
    from app.sources import brave
    conn = open_db()
    today = datetime.now(timezone.utc).date().isoformat()
    day = args.day or today
    # The same command, user, virtualenv and settings as the 07:00 collection
    # (deploy/hiring-radar-poll.service), so it needs no extra rights on the server. Only
    # for today: looking back at an earlier day, or a look that posts nothing, re-runs nothing.
    rerun = None
    if day == today and not args.no_post:
        rerun = lambda: subprocess.run([sys.executable, "-m", "app", "poll", "--region", "europe"],  # noqa: E731
                                       check=False)
    try:
        key = brave.api_key()
        search = lambda q: brave.fetch(q, key)  # noqa: E731
    except brave.MissingKey:
        search = None
    rejected = rejected_boards(json.loads(REJECTED_PATH.read_text())) if REJECTED_PATH.exists() else set()
    found = caretaker_run.morning(conn, day, json.loads(FEEDS_PATH.read_text()), rejected, search)
    for f in found:
        print(f"{f.action:>16}  {f.subject}: {f.detail}")
    if not found:
        print("every source worked")
    print_held(conn)   # not a finding: these are unread because their place or track says so (HIR-396)
    linear_key = os.environ.get("LINEAR_API_KEY", "").strip()
    post = None if (args.no_post or not linear_key) else caretaker_run.linear_poster(
        linear_key, os.environ.get("LINEAR_TEAM_ID", caretaker_run.LINEAR_TEAM_ID))
    from app import merged_work, site_watch_week
    team = os.environ.get("LINEAR_TEAM_ID", caretaker_run.LINEAR_TEAM_ID)
    caretaker_run.report(
        conn, day, post, changes=merged_work.week_text, rerun=rerun,
        site_watch=lambda start, end: site_watch_week.week_text(start, end, linear_key, team, caretaker_run.post_json))


def cmd_flags(args):
    from app import flags
    conn = open_db()
    if args.fixed:
        print(f"closed {flags.mark_fixed(conn, args.fixed, now_iso())} of {len(args.fixed)} flags as fixed")
        return
    print("\n".join(flags.report_lines(flags.open_flags(conn))))


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
    p.add_argument("--region", choices=geo.REGIONS, default=None,
                   help="poll only this region's feeds (the VM's two daily runs); default all feeds")
    p.add_argument("--launch", metavar="CITY", default=None,
                   help="a city launch's first collection: read only the new jobs placed in CITY, "
                        "priced first and stopped above the launch cap; older jobs are left unread")
    p.set_defaults(fn=cmd_poll)
    p = sub.add_parser("extract"); p.add_argument("--limit", type=int); p.set_defaults(fn=cmd_extract)
    p = sub.add_parser("read-pending", help="read every waiting job of a place or career track in one batch")
    p.add_argument("--city", default=None, help="a collected place, e.g. \"New York\"")
    p.add_argument("--family", default=None, help="a career track, e.g. ai-engineer")
    p.add_argument("--cap", type=float, default=None, metavar="EUR",
                   help="the most this read may cost; above it nothing is read. Required unless --dry-run")
    p.add_argument("--dry-run", action="store_true", help="print the job count and the cost, read nothing")
    p.set_defaults(fn=cmd_read_pending)
    p = sub.add_parser("sample", help="draw unread postings to build a skill list from; no model call")
    p.add_argument("--family", default=None, help="a career track")
    p.add_argument("--city", default=None, help="a collected place")
    p.add_argument("--n", type=int, default=50, help="how many postings (default 50)")
    p.add_argument("--seed", type=int, default=0, help="same seed, same sample (default 0)")
    p.add_argument("--out", default=None, metavar="FILE", help="write the JSON here instead of printing it")
    p.set_defaults(fn=cmd_sample)
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
    p.add_argument("--city", default="Berlin", choices=geo.ACTIVE_CITIES,
                   help="the city these links were collected for: recorded for a link whose page "
                        "gives no location (default: Berlin). Unlike --location it describes the "
                        "whole batch and never changes the verdict")
    p.add_argument("--add", action="store_true", help="ingest the posting if not already stored (and extract)")
    p.add_argument("--found-via", default="company_site", choices=["linkedin", "indeed", "company_site", "referral", "other"])
    p.add_argument("--no-extract", action="store_true"); p.set_defaults(fn=cmd_check)
    sub.add_parser("receive-checks", help="store check records sent from another machine (stdin, JSON)"
                   ).set_defaults(fn=cmd_receive_checks)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    p = sub.add_parser("miss-reasons", help="why checked jobs were missed: count per reason, city, careers system")
    p.add_argument("--since", default=None, metavar="YYYY-MM-DD", help="first day counted (default: the first check)")
    p.add_argument("--until", default=None, metavar="YYYY-MM-DD", help="last day counted (default: today)")
    p.set_defaults(fn=cmd_miss_reasons)
    p = sub.add_parser("discover-boards", help="find company job boards we don't poll yet (Brave search)")
    p.add_argument("--add", action="append", default=[], metavar="SOURCE:TOKEN")
    p.add_argument("--reject", action="append", default=[], metavar="SOURCE:TOKEN")
    p.add_argument("--reason", default=None)
    p.add_argument("--launch", metavar="CITY", default=None,
                   help="judge boards for this one city and add what the written policy allows "
                        "(5+ roles there, employers only), then report; stops on a spending cap")
    p.add_argument("--dry-run", action="store_true", help="with --launch: decide and report, write nothing")
    p.set_defaults(fn=cmd_discover_boards)
    p = sub.add_parser("backfill-places",
                       help="credit stored jobs, open and closed, with every tracked city their location names")
    p.add_argument("--city", default=None, help="only this tracked city (default: all of them)")
    p.add_argument("--dry-run", action="store_true", help="count and show, write nothing")
    p.set_defaults(fn=cmd_backfill_places)
    sub.add_parser("markup-postings", help="count stored postings whose text is web-page markup, by source; reads only"
                   ).set_defaults(fn=cmd_markup_postings)
    p = sub.add_parser("repair-companies", help="fill blank companies off each job's stored link, merge duplicates")
    p.add_argument("--apply", action="store_true", help="write the repairs; without it, a dry run that changes nothing")
    p.set_defaults(fn=cmd_repair_companies)
    sub.add_parser("reread-cost",
                   help="what merging an extractor or skill-list change would spend on re-reading"
                   ).set_defaults(fn=cmd_reread_cost)
    p = sub.add_parser("caretaker", help="morning check of every job source; files its fixes as a ticket, "
                                         "re-runs a failed collection once (HIR-257, HIR-261). "
                                         "`caretaker apply-fixes FILE` makes a filed ticket's fixes in feeds.json")
    p.add_argument("action", nargs="?", choices=["apply-fixes"], default=None,
                   help="apply-fixes: make the fixes in a caretaker ticket's text; without it, the morning check")
    p.add_argument("file", nargs="?", default=None, help="for apply-fixes: the file holding the ticket's text, or -")
    p.add_argument("--day", default=None, help="judge this day's poll (YYYY-MM-DD, UTC); default today")
    p.add_argument("--no-post", action="store_true",
                   help="print the summaries, post nothing to Linear and re-run nothing")
    p.set_defaults(fn=cmd_caretaker)
    p = sub.add_parser("flags", help="why each job flagged \"doesn't belong here\" showed, grouped by cause")
    p.add_argument("--fixed", nargs="+", type=int, metavar="ID", default=[],
                   help="close these flags: their cause is fixed (removes the mark from the job)")
    p.set_defaults(fn=cmd_flags)
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
