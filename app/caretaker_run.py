"""The caretaker's morning run: read what the poll recorded, judge it, log it, report.

Does:
  - read today's and recent `feed_run` rows (written by the poll), each board's history in
    job_source, the city totals and the reading queue;
  - hand them to the rules in app/caretaker.py and write every finding to `caretaker_log`;
  - on Mondays, build last week's summary from that log and post it as one Linear issue,
    the Monday summary; the pull-request half of that post (what needs Chandler, what
    merged, what was sent back and fixed: app/merged_work.py, HIR-264) is handed in as
    text and goes first, so the week is one message, not two; the robot visitor's week
    (app/site_watch_week.py, HIR-260) is handed in the same way and goes after it, except
    a break that came back after two fixes, which goes above everything;
  - on Mondays, add one line per place or career track that is collected in the background
    and not shown yet, from the admin page's own rows (app/admin.py, HIR-398);
  - post at once only what cannot wait a week (collection down two days running, spend cap);
  - count the job links checked by hand that we had missed, by reason (app/misses.py,
    HIR-290): the last 7 days go into the Monday summary, and a reason that reaches
    misses.WEEKLY_TICKET_THRESHOLD in 7 days gets a Linear ticket of its own, at most once
    per misses.TICKET_QUIET_DAYS per reason. Below it, the 8-week trend (HIR-321): whether
    the share of checked links a feed already had is rising, overall and per city;
  - file the ticket for company boards "Add a job" found we do not collect and no ticket
    names yet (app/boards_to_add.py, HIR-324). The dashboard recorded those boards until
    "Add a job" left the site (HIR-346); this files whatever is still waiting.

Acts (HIR-261, `MODE = "act"`), in the two ways it has:
  - the day's fixes to the list of job sources (pause a dead board, switch a moved one,
    switch a recovered one back on) are filed as one Linear ticket, "Caretaker:
    job-source fixes for <day>", holding the exact edits and the command that makes them
    (`python -m app caretaker apply-fixes`). The agents' ordinary path turns that ticket
    into a reviewed pull request. A fix already filed is not filed again for
    FIX_QUIET_DAYS days;
  - a collection that did not run, or in which every source failed, is re-run once that
    day, on the server, through the injected `rerun()`.

Does NOT: change config/feeds.json on the server, open a pull request, or talk to GitHub
with a credential; the server has none. The edit of the file happens in the pull request.
The log is append-only, so "filed" and "re-run" are rows of their own (`fix_ticket`,
`rerun_done`), as the Monday summary and the urgent note already are; `done` stays 0.
It never calls a model; the only paid call is the Brave search for a moved board, capped
per day by app/caretaker.py. The re-run is the day's ordinary collection made late.
`MODE = "report"` puts it back to writing down what it would do and doing nothing.

Rules and thresholds: DECISIONS 2026-11-12 (HIR-257); acting:
decisions/2026-11-19-hir-261-caretaker-acts-through-a-ticket-no-server-credential.md.
"""

import json
import sqlite3
import urllib.request
from datetime import date, datetime, timedelta, timezone

from app import caretaker as ct
from app import boards_to_add, fixes_only, geo, misses, poll
from app.caretaker import Budget, FeedRun, Finding
from app.sources import jsearch, registry

# "act": fixes are filed as a ticket and a failed collection is re-run (HIR-261).
# "report": nothing is filed or re-run; the summary says what it would have done.
MODE = "act"
# A fix filed in a ticket is not filed again for this many days: a dead board is found
# again every morning until the pull request that pauses it is merged and deployed.
FIX_QUIET_DAYS = 7
# The Hiring-radar team on Linear; LINEAR_TEAM_ID overrides it.
LINEAR_TEAM_ID = "536d7e60-8726-44aa-9e3a-b273910d72d5"
# Log rows that are bookkeeping, not findings; the weekly summary leaves them out.
BOOKKEEPING = ("spend", "weekly_summary", "urgent_sent", "miss_ticket", "fix_ticket", "rerun_done")


def _day(d: str, n: int) -> str:
    return (date.fromisoformat(d) - timedelta(days=n)).isoformat()


# --- reading -----------------------------------------------------------------------------

def load_runs(conn: sqlite3.Connection, since: str, until: str) -> list[FeedRun]:
    """Every recorded feed run from `since` to `until`, oldest first."""
    rows = conn.execute("SELECT day, label, kind, ok, seen, error, fields FROM feed_run "
                        "WHERE day >= ? AND day <= ? ORDER BY day, id", (since, until)).fetchall()
    return [FeedRun(r["label"], r["kind"], bool(r["ok"]), r["seen"], r["error"],
                    frozenset(json.loads(r["fields"])), r["day"]) for r in rows]


def latest_today(runs: list[FeedRun], day: str) -> dict[str, FeedRun]:
    """One run per feed for `day`: the last one, if the poll ran more than once."""
    out = {}
    for r in runs:
        if r.day == day:
            out[r.label] = r
    return out


def city_counts(conn: sqlite3.Connection, at: str) -> dict[str, int]:
    """Open jobs per city as of `at` (the dashboard's open rule), counting only jobs we
    already knew then, so yesterday's figure can be asked of today's database."""
    from app.queries import open_clause
    oc, params = open_clause(at)
    # Every place a job is posted for, as the dashboard counts them (HIR-289).
    rows = conn.execute(f"SELECT jpl.place, count(*) n FROM job j JOIN job_place jpl ON jpl.job_id = j.id"
                        f" WHERE {oc} AND j.first_seen <= ? GROUP BY jpl.place", [*params, at]).fetchall()
    return {r["place"]: r["n"] for r in rows}


def pending_count(conn: sqlite3.Connection) -> int:
    """Jobs the model still has to read at today's extractor: a count, no model call."""
    from app.extract import DEFAULT_MODEL, extractor_version
    from app.pipeline import jobs_needing_extraction
    from app.taxonomy import Taxonomy
    return len(jobs_needing_extraction(conn, extractor_version(Taxonomy.load(), DEFAULT_MODEL)))


def log_rows(conn: sqlite3.Connection, since: str, until: str) -> list[dict]:
    rows = conn.execute("SELECT day, mode, subject, finding, action, detail, data, done FROM caretaker_log "
                        "WHERE day >= ? AND day <= ? ORDER BY id", (since, until)).fetchall()
    return [{**dict(r), "data": json.loads(r["data"]), "done": bool(r["done"])} for r in rows]


def spent_on(conn: sqlite3.Connection, day: str) -> float:
    return sum(r["data"].get("eur", 0) for r in log_rows(conn, day, day) if r["finding"] == "spend")


def write_log(conn: sqlite3.Connection, findings: list[Finding], day: str) -> None:
    conn.executemany(
        "INSERT INTO caretaker_log (day, mode, subject, finding, action, detail, data, done) "
        "VALUES (?,?,?,?,?,?,?,0)",
        [(day, MODE, f.subject, f.finding, f.action, f.detail, json.dumps(f.data)) for f in findings])
    conn.commit()


# --- the morning judgement ---------------------------------------------------------------

def morning(conn: sqlite3.Connection, day: str, feeds_doc: dict, rejected: set, search=None,
            fetch_board=None, now: datetime | None = None) -> list[Finding]:
    """Judge `day`'s collection and log the findings. `search(query) -> [url]` is the Brave
    search, None when there is no key; `fetch_board(source, token)` fetches a board. Both are
    injected so tests never reach the network. Returns what was logged."""
    fetch_board = fetch_board or ct.default_fetch_board
    now = now or datetime.now(timezone.utc)
    runs = load_runs(conn, _day(day, ct.FEED_HISTORY_DAYS), day)
    today = latest_today(runs, day)
    # The US collection runs at 07:00 New York, after this check (HIR-369): a feed only that
    # run fetches is judged on its run from yesterday, so US searches are checked a day late.
    yesterday = latest_today(runs, _day(day, 1))
    budget = Budget(spent=spent_on(conn, day))
    start_spent = budget.spent
    known = {(f["type"], f["token"].lower()) for f in feeds_doc["feeds"] if f.get("token")}

    found = ct.judge_collection(day, list(today.values()))
    if search is None:
        found.append(Finding("caretaker", "no_search_key", "report",
                             "There is no Brave key on the server, so moved boards were not searched for."))
    for feed in feeds_doc["feeds"]:
        label = poll.feed_label(feed)
        if not feed.get("enabled", True):
            if "paused" in feed and ct.is_recheck_day(day, feed["paused"]["since"]):
                try:
                    found += ct.recheck_paused(feed, fetch_board(feed["type"], feed["token"]), None)
                except Exception as e:
                    found += ct.recheck_paused(feed, None, f"{type(e).__name__}: {str(e)[:120]}")
            continue
        run = yesterday.get(label) if poll.feed_regions(feed) == (geo.US,) else today.get(label)
        if run is None:
            continue
        history = [r for r in runs if r.label == label and r.day < run.day]
        source = registry.BY_NAME.get(feed["type"])
        if source and source.kind == "board":
            n, last_seen = poll.board_history(conn, feed)
            find_move = (lambda f=feed: ct.find_moved_board(f, search, budget, known, rejected, fetch_board)
                         ) if search else (lambda: None)
            found += ct.judge_board(feed, run, history, n, last_seen, find_move)
        else:
            found += ct.judge_feed(run, history)
    found += ct.judge_pending(pending_count(conn))
    stamp = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")  # noqa: E731
    found += ct.judge_cities(city_counts(conn, stamp(now)), city_counts(conn, stamp(now - timedelta(days=1))))
    found += ct.spend_findings(budget)
    if budget.spent > start_spent:
        found.append(Finding("caretaker", "spend", "none",
                             f"Spent €{budget.spent - start_spent:.3f} on board searches.",
                             {"eur": round(budget.spent - start_spent, 4)}))
    write_log(conn, found, day)
    return found


# --- reporting ---------------------------------------------------------------------------

def _as_findings(rows: list[dict]) -> list[Finding]:
    return [Finding(r["subject"], r["finding"], r["action"], r["detail"], r["data"]) for r in rows]


def urgent_now(conn: sqlite3.Connection, day: str) -> list[str]:
    """What cannot wait for Monday, unless it was already sent today."""
    rows = log_rows(conn, day, day)
    if any(r["finding"] == "urgent_sent" for r in rows):
        return []
    return ct.urgent(_as_findings(rows), _as_findings(log_rows(conn, _day(day, 1), _day(day, 1))))


def weekly_due(conn: sqlite3.Connection, day: str) -> tuple[str, str] | None:
    """On a Monday: last Monday..Sunday, unless that week's summary was already made."""
    if date.fromisoformat(day).weekday() != 0:
        return None
    start, end = _day(day, 7), _day(day, 1)
    if any(r["finding"] == "weekly_summary" and r["data"].get("week_start") == start
           for r in log_rows(conn, day, day)):
        return None
    return start, end


def weekly_text(conn: sqlite3.Connection, start: str, end: str) -> str:
    rows = [r for r in log_rows(conn, start, end) if r["finding"] not in BOOKKEEPING]
    # A week logged entirely before acting was switched on is still reported as
    # "would have": nothing in it was filed or re-run.
    acting = MODE == "act" and (not rows or any(r["mode"] == "act" for r in rows))
    return ct.weekly_summary(rows, start, end, acting=acting)


def jsearch_usage_text(conn: sqlite3.Connection, end: str) -> str:
    """One Monday line: Google for Jobs (JSearch) requests so far in the month of `end`,
    against our own cap (HIR-352). Past the cap the searches stop until the month turns."""
    used, cap = poll.jsearch_requests(conn, end[:7]), jsearch.MONTHLY_CAP
    line = f"Google for Jobs searches in {end[:7]}: {used:,} of our cap of {cap:,}."
    if used >= cap:
        line += " The cap is reached: those searches are stopped until the month turns."
    return line + "\n"


def incubating_text(conn: sqlite3.Connection, now: str | None = None) -> str:
    """The Monday lines for the places and career tracks collected in the background and
    not shown yet (HIR-398): one each, from the rows the admin page shows (app/admin.py),
    so the two print the same numbers. "" when nothing is incubating."""
    from app import admin
    from app.extract import DEFAULT_MODEL, extractor_version
    from app.ingest import now_iso
    from app.taxonomy import Taxonomy
    rows = admin.overview(conn, now or now_iso(), extractor_version(Taxonomy.load(), DEFAULT_MODEL))
    return admin.incubating_section(rows)


def post_json(url: str, payload: dict, headers: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def report(conn: sqlite3.Connection, day: str, post=None, log=print, changes=None, site_watch=None,
           feeds: list[dict] | None = None, mode: dict | None | bool = False, rerun=None) -> None:
    """Send the urgent note and, on Mondays, the weekly summary; then file the day's
    job-source fixes as one ticket and, last, re-run a failed collection once (`rerun()`,
    injected; None re-runs nothing) (HIR-261). `post(title, body)` returns
    the Linear identifier; None when there is no Linear key, and then the text goes to the
    journal only. Each send is logged so a second run the same day does not repeat it.
    `changes(start, end)` returns the pull-request half of the Monday summary as Markdown
    (app/merged_work.week_text); it is injected so tests never reach GitHub, and None
    leaves the post as the job-source report alone. `feeds` is what the missed-jobs trend
    judges "would a feed catch it today" against (HIR-321); None reads config/feeds.json.
    `site_watch(start, end)` returns the
    robot visitor's two pieces (app/site_watch_week.week_text, HIR-260): what waits for
    Chandler, which goes above everything else, and the week's report, which goes after the
    pull requests; injected so tests never reach Linear, and None leaves both out.
    `mode` is the fixes-only setting (app/fixes_only.py, HIR-341): while it is on, the
    summary's first line says so. False reads config/lead_agent.json; None is "no mode"."""
    if (items := urgent_now(conn, day)):
        body = "The caretaker found something that cannot wait for Monday:\n\n" + \
               "\n".join(f"- {i}" for i in items) + "\n"
        posted = post(f"Caretaker: needs you now ({day})", body) if post else None
        log(body + (f"posted as {posted}" if posted else "(not posted: no Linear key)"))
        write_log(conn, [Finding("caretaker", "urgent_sent", "none", "Urgent note sent.",
                                 {"posted": posted, "items": items})], day)
    if (week := weekly_due(conn, day)):
        start, end = week
        robot_first, robot_week = site_watch(start, end) if site_watch else ("", "")
        frozen = fixes_only.sentence(fixes_only.load() if mode is False else mode, day)
        body = ((frozen + "\n\n" if frozen else "")
                + (robot_first + "\n" if robot_first else "")
                + (changes(start, end) + "\n" if changes else "")
                + (robot_week + "\n" if robot_week else "")
                + weekly_text(conn, start, end)
                + "\n" + jsearch_usage_text(conn, end)
                + (("\n" + background) if (background := incubating_text(conn)) else "")
                + "\n" + misses.week_section(misses.records(conn, start, end), start, end)
                + "\n" + misses.trend_section(misses.records(conn), end,
                                               poll.load_feeds() if feeds is None else feeds))
        posted = post(f"Monday summary: {start} to {end}", body) if post else None
        log(body + (f"\nposted as {posted}" if posted else "\n(not posted: no Linear key)"))
        write_log(conn, [Finding("caretaker", "weekly_summary", "none", "Weekly summary made.",
                                 {"posted": posted, "week_start": start})], day)
    fix_ticket(conn, day, post, log)
    miss_tickets(conn, day, post, log)
    boards_to_add.file_ticket(conn, boards_to_add.load_config()[0], post,
                              datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), log)
    rerun_once(conn, day, rerun, log)   # last: a collection takes minutes, the posts do not wait for it


def _fix_key(r: dict) -> list:
    """What makes two logged fixes the same fix: the board, what to do, and where to."""
    return [r["subject"], r["action"], r["data"].get("to")]


def fix_ticket(conn: sqlite3.Connection, day: str, post=None, log=print) -> str | None:
    """File `day`'s fixes to the list of job sources as one Linear ticket (HIR-261); the
    pull request that makes them is opened from that ticket, never from the server. Leaves
    out a fix a ticket of the last FIX_QUIET_DAYS days already carries, and files nothing
    when none is left, in report mode, or when today's ticket was already filed. Returns
    the title filed. Without a Linear key the text goes to the journal only."""
    if MODE != "act":
        return None
    today = log_rows(conn, day, day)
    if any(r["finding"] == "fix_ticket" for r in today):
        return None
    # Only a ticket that reached Linear counts: a morning without the key filed nothing.
    filed = [k for r in log_rows(conn, _day(day, FIX_QUIET_DAYS - 1), day)
             if r["finding"] == "fix_ticket" and r["data"].get("posted")
             for k in r["data"].get("fixes", [])]
    fixes: dict[str, dict] = {}
    for r in today:   # one fix per board: the latest, if the check ran twice today
        if r["action"] in ct.FEED_FIXES and _fix_key(r) not in filed:
            fixes[r["subject"]] = r
    if not fixes:
        return None
    title, body = ct.fix_ticket_text(list(fixes.values()), day)
    posted = post(title, body) if post else None
    log(f"{title}\n{body}" + (f"posted as {posted}" if posted else "(not posted: no Linear key)"))
    write_log(conn, [Finding("caretaker", "fix_ticket", "none", title,
                             {"posted": posted, "fixes": [_fix_key(r) for r in fixes.values()]})], day)
    return title


def rerun_once(conn: sqlite3.Connection, day: str, rerun=None, log=print) -> bool:
    """Re-run the collection when `day`'s did not run or failed everywhere, once per day
    (HIR-261). `rerun()` starts it and is injected: the command line hands in the same
    `poll --region europe` the 07:00 service runs; None (a test, a dry look, report mode)
    re-runs nothing. Logged before it starts, so a re-run that dies is not tried again
    the same day. True when it was started."""
    if MODE != "act" or rerun is None:
        return False
    rows = log_rows(conn, day, day)
    if not any(r["action"] == "rerun_collection" for r in rows) or any(r["finding"] == "rerun_done" for r in rows):
        return False
    write_log(conn, [Finding("caretaker", "rerun_done", "none", f"Re-ran the {day} collection once.")], day)
    log(f"Re-running the {day} collection once.")
    rerun()
    return True


def miss_tickets(conn: sqlite3.Connection, day: str, post=None, log=print) -> list[str]:
    """File one Linear ticket for each miss reason that reached the weekly threshold in the
    7 days up to `day`, unless that reason was ticketed in the last TICKET_QUIET_DAYS days.
    Returns the reasons ticketed. Each is logged, so a second run the same day, or the
    next morning with the same misses, does not file it again."""
    start = _day(day, 6)
    week = misses.records(conn, start, day)
    recent = {r["data"].get("reason") for r in log_rows(conn, _day(day, misses.TICKET_QUIET_DAYS - 1), day)
              if r["finding"] == "miss_ticket"}
    filed = []
    for reason, n in misses.over_threshold(week):
        if reason in recent:
            continue
        title, body = misses.ticket_text(reason, n, week, start, day)
        posted = post(title, body) if post else None
        log(f"{title}\n" + (f"posted as {posted}" if posted else "(not posted: no Linear key)"))
        write_log(conn, [Finding("misses", "miss_ticket", "none", title,
                                 {"posted": posted, "reason": reason, "count": n})], day)
        filed.append(reason)
    return filed


def linear_poster(key: str, team_id: str):
    return lambda title, body: ct.post_to_linear(title, body, key, team_id, post_json)
