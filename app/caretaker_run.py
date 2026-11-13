"""The caretaker's morning run: read what the poll recorded, judge it, log it, report.

Does:
  - read today's and recent `feed_run` rows (written by the poll), each board's history in
    job_source, the city totals and the reading queue;
  - hand them to the rules in app/caretaker.py and write every finding to `caretaker_log`;
  - on Mondays, build last week's summary from that log and post it as one Linear issue,
    the Monday summary; the pull-request half of that post (what needs Chandler, what
    merged, what was sent back and fixed: app/merged_work.py, HIR-264) is handed in as
    text and goes first, so the week is one message, not two;
  - post at once only what cannot wait a week (collection down two days running, spend cap).

Does NOT: change config/feeds.json, re-run the collection, or open a pull request. It runs
report-only: every finding is logged with what it *would* do (`mode='report'`, `done=0`).
Acting is a separate change (HIR-261), switched on after a week of report-only summaries.
It never calls a model; the only paid call is the Brave search for a moved board, capped
per day by app/caretaker.py.

Rules and thresholds: DECISIONS 2026-11-12 (HIR-257).
"""

import json
import sqlite3
import urllib.request
from datetime import date, datetime, timedelta, timezone

from app import caretaker as ct
from app import poll
from app.caretaker import Budget, FeedRun, Finding
from app.sources import registry

MODE = "report"
# The Hiring-radar team on Linear; LINEAR_TEAM_ID overrides it.
LINEAR_TEAM_ID = "536d7e60-8726-44aa-9e3a-b273910d72d5"
# Log rows that are bookkeeping, not findings; the weekly summary leaves them out.
BOOKKEEPING = ("spend", "weekly_summary", "urgent_sent")


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
        run = today.get(label)
        if run is None:
            continue
        history = [r for r in runs if r.label == label and r.day < day]
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
    return ct.weekly_summary(rows, start, end, acting=MODE == "act")


def post_json(url: str, payload: dict, headers: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def report(conn: sqlite3.Connection, day: str, post=None, log=print, changes=None) -> None:
    """Send the urgent note and, on Mondays, the weekly summary. `post(title, body)` returns
    the Linear identifier; None when there is no Linear key, and then the text goes to the
    journal only. Each send is logged so a second run the same day does not repeat it.
    `changes(start, end)` returns the pull-request half of the Monday summary as Markdown
    (app/merged_work.week_text); it is injected so tests never reach GitHub, and None
    leaves the post as the job-source report alone."""
    if (items := urgent_now(conn, day)):
        body = "The caretaker found something that cannot wait for Monday:\n\n" + \
               "\n".join(f"- {i}" for i in items) + "\n"
        posted = post(f"Caretaker: needs you now ({day})", body) if post else None
        log(body + (f"posted as {posted}" if posted else "(not posted: no Linear key)"))
        write_log(conn, [Finding("caretaker", "urgent_sent", "none", "Urgent note sent.",
                                 {"posted": posted, "items": items})], day)
    if (week := weekly_due(conn, day)):
        start, end = week
        body = (changes(start, end) + "\n" if changes else "") + weekly_text(conn, start, end)
        posted = post(f"Monday summary: {start} to {end}", body) if post else None
        log(body + (f"\nposted as {posted}" if posted else "\n(not posted: no Linear key)"))
        write_log(conn, [Finding("caretaker", "weekly_summary", "none", "Weekly summary made.",
                                 {"posted": posted, "week_start": start})], day)


def linear_poster(key: str, team_id: str):
    return lambda title, body: ct.post_to_linear(title, body, key, team_id, post_json)
