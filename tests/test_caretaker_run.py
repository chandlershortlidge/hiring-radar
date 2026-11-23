"""The caretaker's morning run on a real (temporary) database (HIR-257): the poll records
each feed, the morning run judges it, the log keeps it, the weekly summary reads it back.
No network, no model: board fetches, the search and Linear are fakes."""

import json
import sqlite3
from datetime import datetime, timezone

import pytest

from app import caretaker_run as run
from app import db, poll
from app.ingest import ingest_one
from app.sources import Posting

DAY = "2026-11-16"          # a Monday
NOW = datetime(2026, 11, 16, 9, 0, tzinfo=timezone.utc)


def posting(source, token, n, company, city="Berlin", title="AI Engineer"):
    return Posting(source, f"{token}-{n}", f"https://x.example/{token}/{n}", company, title, city,
                   "Build ML systems in Berlin with Python.")


def feeds_doc():
    return {"feeds": [
        {"type": "greenhouse", "enabled": True, "token": "doctolib", "company": "Doctolib"},
        {"type": "lever", "enabled": True, "token": "pipedrive", "company": "Pipedrive"},
        {"type": "ashby", "enabled": True, "token": "healthy", "company": "Healthy"},
        {"type": "arbeitnow", "enabled": True},
    ]}


@pytest.fixture
def conn(tmp_path, monkeypatch):
    """A database copy where Doctolib and Pipedrive gave us postings last month and then
    stopped, and one healthy board is fine. The reading queue is counted as empty."""
    monkeypatch.setattr(run, "pending_count", lambda c: 0)
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    for token, company in (("doctolib", "Doctolib"), ("pipedrive", "Pipedrive")):
        src = "greenhouse" if token == "doctolib" else "lever"
        ingest_one(c, posting(src, token, 1, company), when="2026-10-23T08:00:00Z")
    ingest_one(c, posting("ashby", "healthy", 1, "Healthy"), when="2026-11-16T06:00:00Z")
    return c


def poll_today(conn, feeds, day=DAY):
    """The poll's per-feed record, for the four feeds: Doctolib's old board is gone,
    Pipedrive's answers empty, the others work."""
    def fetch(feed):
        if feed["token" if "token" in feed else "type"] == "doctolib":
            raise RuntimeError("HTTPError: HTTP Error 404: Not Found")
        if feed.get("token") == "pipedrive":
            return []
        if feed.get("token") == "healthy":
            return [posting("ashby", "healthy", 1, "Healthy")]
        return [posting("arbeitnow", "an", i, f"Co{i}") for i in range(3)]
    for feed in feeds:
        try:
            poll.record_run(conn, feed, fetch(feed), day=day)
        except RuntimeError as e:
            poll.record_run(conn, feed, None, str(e), day=day)


def moved_board_search(q):
    return ["https://jobs.ashbyhq.com/doctolib/0b8f6f8e-3a1c-4d5e-9f00-1a2b3c4d5e6f"] if "ashby" in q else []


def fetch_board(source, token):
    if (source, token) == ("ashby", "doctolib"):
        return [posting("ashby", "doctolib", 9, "Doctolib")]
    raise RuntimeError("no such board")


def morning(conn, search=moved_board_search, doc=None):
    return run.morning(conn, DAY, doc or feeds_doc(), set(), search, fetch_board, now=NOW)


# --- the poll's record -------------------------------------------------------------------

def test_poll_records_every_feed_including_failures(conn):
    feeds = [{"type": "ashby", "token": "healthy"}, {"type": "greenhouse", "token": "gone"}]

    def fetch(feed):
        if feed["token"] == "gone":
            raise RuntimeError("HTTP Error 404")
        return [posting("ashby", "healthy", 2, "Healthy")]
    poll.poll_feeds(conn, feeds, fetch=fetch, log=lambda *_: None)
    rows = conn.execute("SELECT label, kind, ok, seen, error, fields FROM feed_run ORDER BY id").fetchall()
    assert [(r["label"], r["kind"], r["ok"], r["seen"]) for r in rows] == [
        ("ashby:healthy", "board", 1, 1), ("greenhouse:gone", "board", 0, 0)]
    assert "404" in rows[1]["error"]
    assert json.loads(rows[0]["fields"]) == ["company", "location_raw", "url"]


@pytest.mark.parametrize("table", ["feed_run", "caretaker_log"])
def test_the_record_and_the_log_are_append_only(conn, table):
    poll_today(conn, feeds_doc()["feeds"])
    morning(conn)
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        conn.execute(f"DELETE FROM {table}")
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        conn.execute(f"UPDATE {table} SET day = 'x'")


# --- the morning run (the issue's "done when") -------------------------------------------

def test_broken_board_is_paused_and_moved_board_is_switched_in_the_log(conn):
    poll_today(conn, feeds_doc()["feeds"])
    found = morning(conn)
    got = {(f.subject, f.finding, f.action) for f in found}
    assert ("lever:pipedrive", "board_dead", "pause") in got
    assert ("greenhouse:doctolib", "board_moved", "switch") in got
    assert not any(f.subject == "ashby:healthy" for f in found)
    logged = run.log_rows(conn, DAY, DAY)
    assert {(r["subject"], r["action"]) for r in logged} >= {("lever:pipedrive", "pause"),
                                                             ("greenhouse:doctolib", "switch")}
    # Acting (HIR-261): logged as act; `done` stays 0 because the log is append-only and
    # "filed" is a row of its own.
    assert all(r["mode"] == "act" and not r["done"] for r in logged)


def test_both_fixes_appear_in_the_next_weekly_summary(conn):
    poll_today(conn, feeds_doc()["feeds"], day="2026-11-12")
    run.morning(conn, "2026-11-12", feeds_doc(), set(), moved_board_search, fetch_board,
                now=datetime(2026, 11, 12, 9, tzinfo=timezone.utc))
    text = run.weekly_text(conn, "2026-11-09", "2026-11-15")
    assert "report-only" not in text and "would have" not in text      # acting (HIR-261)
    assert "## What it fixed or filed to fix" in text and "ashby:doctolib" in text
    assert "## What it filed to pause" in text and "lever:pipedrive" in text
    assert "Spent" not in text                                 # bookkeeping is not a finding
    run.report(conn, "2026-11-12", lambda t, b: "HIR-900", log=lambda *_: None)
    assert run.weekly_text(conn, "2026-11-09", "2026-11-15") == text   # nor is "ticket filed"


def test_a_week_logged_before_acting_was_switched_on_still_says_would_have(conn, monkeypatch):
    # The first Monday after HIR-261 merges looks back at a week in which nothing was filed.
    monkeypatch.setattr(run, "MODE", "report")
    poll_today(conn, feeds_doc()["feeds"], day="2026-11-12")
    run.morning(conn, "2026-11-12", feeds_doc(), set(), moved_board_search, fetch_board,
                now=datetime(2026, 11, 12, 9, tzinfo=timezone.utc))
    monkeypatch.setattr(run, "MODE", "act")
    text = run.weekly_text(conn, "2026-11-09", "2026-11-15")
    assert "report-only" in text and "## What it would have fixed" in text


def test_a_us_search_is_judged_on_yesterdays_run_and_a_europe_one_on_todays(conn):
    """The US collection runs at 07:00 New York, after this check (HIR-369): a feed only the
    US run fetches is judged on yesterday's record; a Europe feed's yesterday is not re-judged."""
    us = {"type": "jsearch", "enabled": True, "search": "AI engineer in Seattle", "country": "us"}
    eu = {"type": "jsearch", "enabled": True, "search": "AI engineer in Berlin", "country": "de"}
    poll.record_run(conn, us, None, "HTTPError: 500", day="2026-11-15")
    poll.record_run(conn, eu, None, "HTTPError: 500", day="2026-11-15")
    poll_today(conn, feeds_doc()["feeds"])
    found = morning(conn, doc={"feeds": feeds_doc()["feeds"] + [us, eu]})
    errors = {f.subject for f in found if f.finding == "feed_error"}
    assert "jsearch:AI engineer in Seattle" in errors
    assert "jsearch:AI engineer in Berlin" not in errors


def test_the_morning_run_never_writes_the_feeds_file_even_in_acting_mode(conn, tmp_path, monkeypatch):
    # HIR-261: the write happens in a pull request (`caretaker apply-fixes`), never on the server.
    from app import caretaker
    assert run.MODE == "act"
    monkeypatch.setattr(caretaker, "write_feeds", lambda *a, **k: pytest.fail("wrote feeds.json"))
    doc = feeds_doc()
    before = json.dumps(doc)
    poll_today(conn, doc["feeds"])
    morning(conn, doc=doc)
    run.report(conn, DAY, lambda t, b: "HIR-900", log=lambda *_: None, rerun=lambda: None)
    assert json.dumps(doc) == before


# --- acting (HIR-261) --------------------------------------------------------------------

def only_the_dead_board(q):
    return []          # no new home is found for anyone: Pipedrive's dead board is paused


def test_fixes_are_filed_as_one_ticket_a_day_with_the_exact_edits(conn):
    """The ticket's first "Done when": a fix decided on a database copy becomes a ticket
    whose text, fed to the applier, edits only that one entry of the list of job sources."""
    doc = feeds_doc()
    poll_today(conn, doc["feeds"])
    morning(conn, search=only_the_dead_board)
    posted = []
    post = lambda t, b: posted.append((t, b)) or "HIR-900"  # noqa: E731
    run.report(conn, "2026-11-17", post, log=lambda *_: None)          # a Tuesday: no Monday summary
    assert posted == []                                                # nothing was found that day
    run.report(conn, DAY, post, log=lambda *_: None)
    fix_posts = [(t, b) for t, b in posted if t.startswith("Caretaker: job-source fixes")]
    [(title, body)] = fix_posts
    assert title == f"Caretaker: job-source fixes for {DAY}"
    assert "- lever:pipedrive has returned nothing we keep since 2026-10-23" in body
    assert "Model-call spend: none. Changes only the list of job sources (config/feeds.json)." in body
    assert "+++ Agent notes" in body and "uv run python -m app caretaker apply-fixes" in body

    # Both dead boards (Doctolib's answers 404, Pipedrive's is empty) and nothing else.
    fixes = run.ct.fixes_from_text(body)
    assert [(f.subject, f.action) for f in fixes] == [("greenhouse:doctolib", "pause"), ("lever:pipedrive", "pause")]
    after = run.ct.apply_fixes(doc, body)
    changed = [(a, b) for a, b in zip(doc["feeds"], after["feeds"]) if a != b]
    assert [was["token"] for was, _ in changed] == ["doctolib", "pipedrive"]     # nothing else changed
    for was, now in changed:
        assert now == {**was, "enabled": False, "paused": now["paused"]} and now["paused"]["since"] == DAY
    assert len(after["feeds"]) == len(doc["feeds"])

    run.report(conn, DAY, post, log=lambda *_: None)                   # a second run the same day
    assert [t for t, _ in posted if t.startswith("Caretaker: job-source fixes")] == [title]
    [row] = [r for r in run.log_rows(conn, DAY, DAY) if r["finding"] == "fix_ticket"]
    assert row["data"] == {"posted": "HIR-900", "fixes": [["greenhouse:doctolib", "pause", None],
                                                          ["lever:pipedrive", "pause", None]]}


def test_a_moved_board_and_a_dead_one_travel_in_the_same_ticket(conn):
    doc = feeds_doc()
    poll_today(conn, doc["feeds"])
    morning(conn)
    posted = []
    run.fix_ticket(conn, DAY, lambda t, b: posted.append(b) or "HIR-900", log=lambda *_: None)
    after = run.ct.apply_fixes(doc, posted[0])
    by_company = {f.get("company"): f for f in after["feeds"]}
    assert (by_company["Doctolib"]["type"], by_company["Doctolib"]["token"]) == ("ashby", "doctolib")
    assert by_company["Doctolib"]["moved_from"] == "greenhouse:doctolib"
    assert by_company["Pipedrive"]["enabled"] is False
    assert by_company["Healthy"] == doc["feeds"][2] and after["feeds"][3] == doc["feeds"][3]


def test_a_fix_already_filed_is_not_filed_again_until_a_week_has_passed(conn):
    # The board stays dead every morning until the pull request is merged and deployed.
    posted = []
    post = lambda t, b: posted.append(t) or "HIR-900"  # noqa: E731
    for day in ("2026-11-16", "2026-11-17", "2026-11-22", "2026-11-23"):
        poll_today(conn, feeds_doc()["feeds"], day=day)
        run.morning(conn, day, feeds_doc(), set(), only_the_dead_board, fetch_board,
                    now=datetime.fromisoformat(day + "T09:00:00+00:00"))
        run.fix_ticket(conn, day, post, log=lambda *_: None)
    assert posted == ["Caretaker: job-source fixes for 2026-11-16", "Caretaker: job-source fixes for 2026-11-23"]


def test_without_a_linear_key_the_fix_goes_to_the_journal_and_is_filed_once_the_key_is_there(conn):
    poll_today(conn, feeds_doc()["feeds"])
    morning(conn, search=only_the_dead_board)
    out = []
    assert run.fix_ticket(conn, DAY, None, log=out.append) == f"Caretaker: job-source fixes for {DAY}"
    assert "lever:pipedrive" in out[-1] and "not posted" in out[-1]
    poll_today(conn, feeds_doc()["feeds"], day="2026-11-17")
    run.morning(conn, "2026-11-17", feeds_doc(), set(), only_the_dead_board, fetch_board,
                now=datetime(2026, 11, 17, 9, tzinfo=timezone.utc))
    posted = []
    run.fix_ticket(conn, "2026-11-17", lambda t, b: posted.append(t) or "HIR-900", log=lambda *_: None)
    assert posted == ["Caretaker: job-source fixes for 2026-11-17"]


def test_report_mode_files_nothing_and_reruns_nothing(conn, monkeypatch):
    # The undo: one line puts the caretaker back to writing down what it would do.
    monkeypatch.setattr(run, "MODE", "report")
    morning(conn, search=only_the_dead_board)                          # no poll today
    posted, reruns = [], []
    run.report(conn, DAY, lambda t, b: posted.append(t) or "HIR-900", log=lambda *_: None,
               rerun=lambda: reruns.append(1))
    assert reruns == [] and not any(t.startswith("Caretaker: job-source fixes") for t in posted)


def test_failed_collection_is_rerun_once(conn):
    """The ticket's second "Done when": the re-run happens on the server, with no pull
    request and no ticket, once per day."""
    reruns, posted = [], []
    rerun = lambda: reruns.append(1)  # noqa: E731
    post = lambda t, b: posted.append(t) or "HIR-900"  # noqa: E731
    morning(conn)                                                      # no poll today
    run.report(conn, DAY, post, log=lambda *_: None, rerun=rerun)
    assert reruns == [1]
    morning(conn)                                                      # a second run the same day
    run.report(conn, DAY, post, log=lambda *_: None, rerun=rerun)
    assert reruns == [1]
    assert not any(t.startswith("Caretaker: job-source fixes") for t in posted)
    assert [r["finding"] for r in run.log_rows(conn, DAY, DAY)].count("rerun_done") == 1

    poll_today(conn, feeds_doc()["feeds"], day="2026-11-17")           # a day whose poll ran
    run.morning(conn, "2026-11-17", feeds_doc(), set(), only_the_dead_board, fetch_board,
                now=datetime(2026, 11, 17, 9, tzinfo=timezone.utc))
    run.report(conn, "2026-11-17", post, log=lambda *_: None, rerun=rerun)
    assert reruns == [1]


def test_the_command_line_reruns_with_the_morning_collections_own_command_and_only_for_today(tmp_path, monkeypatch):
    import argparse
    import subprocess
    import sys

    import app.__main__ as cli
    seen, ran = {}, []
    monkeypatch.setattr(cli, "open_db", lambda: db.connect(tmp_path / "t.db"))
    monkeypatch.setattr(run, "morning", lambda *a, **k: [])
    monkeypatch.setattr(run, "report", lambda conn, day, post, **kw: seen.update(kw))
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kw: ran.append((cmd, kw)))
    monkeypatch.delenv("LINEAR_API_KEY", raising=False)
    cli.cmd_caretaker(argparse.Namespace(day=None, no_post=False))
    seen["rerun"]()
    assert ran == [([sys.executable, "-m", "app", "poll", "--region", "europe"], {"check": False})]
    cli.cmd_caretaker(argparse.Namespace(day="2026-11-10", no_post=False))   # looking back at an earlier day
    assert seen["rerun"] is None
    cli.cmd_caretaker(argparse.Namespace(day=None, no_post=True))            # a look that posts nothing
    assert seen["rerun"] is None


def test_a_collection_in_which_every_source_failed_is_rerun_too(conn):
    for feed in feeds_doc()["feeds"]:
        poll.record_run(conn, feed, None, "URLError: timed out", day=DAY)
    morning(conn, search=only_the_dead_board)
    reruns = []
    assert run.rerun_once(conn, DAY, lambda: reruns.append(1), log=lambda *_: None) is True
    assert run.rerun_once(conn, DAY, lambda: reruns.append(1), log=lambda *_: None) is False
    assert reruns == [1]


def test_no_poll_today_means_rerun_the_collection(conn):
    found = morning(conn)
    assert [(f.finding, f.action) for f in found if f.subject == "collection"] == [
        ("collection_missing", "rerun_collection")]


def test_without_a_search_key_it_says_so_and_does_not_search(conn):
    poll_today(conn, feeds_doc()["feeds"])
    found = morning(conn, search=None)
    assert "no_search_key" in {f.finding for f in found}
    assert not any(f.action == "switch" for f in found)


def test_spend_is_counted_across_runs_on_the_same_day(conn):
    poll_today(conn, feeds_doc()["feeds"])
    morning(conn)
    first = run.spent_on(conn, DAY)
    assert first > 0
    morning(conn)
    assert run.spent_on(conn, DAY) == pytest.approx(2 * first)


def test_sharp_city_drop_overnight_is_reported(conn):
    for i in range(25):
        ingest_one(conn, posting("arbeitnow", "drop", i, f"Drop{i}", city="Hamburg"), when="2026-11-12T10:00:00Z")
    found = morning(conn)
    assert ("city:Hamburg", "city_drop") in {(f.subject, f.finding) for f in found}


def test_city_counts_count_a_two_city_job_in_both(conn):
    # HIR-289: the caretaker counts places the way the dashboard does.
    ingest_one(conn, posting("ashby", "two", 1, "Two", city="Berlin; Munich"), when="2026-11-16T06:00:00Z")
    counts = run.city_counts(conn, "2026-11-16T09:00:00Z")
    assert counts["Munich"] == 1 and counts["Berlin"] == 2     # Healthy and Two


# --- reporting ---------------------------------------------------------------------------

def test_monday_summary_posts_once(conn):
    poll_today(conn, feeds_doc()["feeds"])
    morning(conn)
    posted = []
    run.report(conn, DAY, lambda t, b: posted.append((t, b)) or "HIR-900", log=lambda *_: None)
    run.report(conn, DAY, lambda t, b: posted.append((t, b)) or "HIR-901", log=lambda *_: None)
    assert [t for t, _ in posted] == ["Monday summary: 2026-11-09 to 2026-11-15",
                                      f"Caretaker: job-source fixes for {DAY}"]   # each once


def test_monday_summary_puts_the_robot_visitors_needs_you_first_and_its_week_after_the_pull_requests(conn):
    # HIR-260: a break that came back after two fixes is the one robot line Chandler must
    # act on, so it goes above the pull requests; the week's report goes after them.
    poll_today(conn, feeds_doc()["feeds"])
    morning(conn)
    posted, asked = [], []

    def site_watch(start, end):
        asked.append((start, end))
        return "# The live site: needs you\n\n- x\n", "# The robot visitor\n\n## What broke\n"

    run.report(conn, DAY, lambda t, b: posted.append(b) or "HIR-900", log=lambda *_: None,
               changes=lambda s, e: "# Needs you\n\nNothing.\n", site_watch=site_watch)
    body = posted[0]                      # the summary; the day's fix ticket follows it
    assert asked == [("2026-11-09", "2026-11-15")]
    order = [body.index(h) for h in ("# The live site: needs you", "# Needs you", "# The robot visitor", "# Caretaker")]
    assert order == sorted(order) and order[0] == 0


def test_monday_summary_with_nothing_waiting_from_the_robot_starts_with_the_pull_requests(conn):
    poll_today(conn, feeds_doc()["feeds"])
    morning(conn)
    posted = []
    run.report(conn, DAY, lambda t, b: posted.append(b) or "HIR-900", log=lambda *_: None,
               changes=lambda s, e: "# Needs you\n\nNothing.\n",
               site_watch=lambda s, e: ("", "# The robot visitor\n\nNothing broke on the live site all week.\n"))
    assert posted[0].startswith("# Needs you") and "Nothing broke on the live site all week." in posted[0]


def test_monday_summary_starts_with_fixes_only_mode_while_it_is_on_and_only_then(conn):
    # HIR-341: over the Christmas break the summary's first line says agents only repair.
    changes = lambda s, e: "# Needs you\n\nNothing.\n"  # noqa: E731
    for day, mode, first in (
        ("2026-12-21", {"from": "2026-12-16", "until": None}, "The site is in fixes-only mode: since 16 December 2026"),
        ("2026-12-28", None, "# Needs you"),                                    # turned off
        ("2026-12-14", {"from": "2026-12-16", "until": None}, "# Needs you"),   # not begun
    ):
        posted = []
        run.report(conn, day, lambda t, b: posted.append(b) or "HIR-900", log=lambda *_: None,
                   changes=changes, mode=mode)
        assert posted[0].startswith(first) and "# Needs you" in posted[0]


def test_no_summary_on_other_days_and_no_post_without_a_key(conn):
    assert run.weekly_due(conn, "2026-11-17") is None
    out = []
    run.report(conn, DAY, None, log=out.append)
    assert "not posted" in out[-1]
    assert run.weekly_due(conn, DAY) is None                   # logged, so not made twice


def test_collection_down_two_days_is_sent_at_once_and_only_once(conn):
    run.morning(conn, "2026-11-15", feeds_doc(), set(), None, fetch_board, now=NOW)
    morning(conn)
    posted = []
    post = lambda t, b: posted.append(t) or "HIR-902"  # noqa: E731
    run.report(conn, DAY, post, log=lambda *_: None)
    run.report(conn, DAY, post, log=lambda *_: None)
    assert posted.count(f"Caretaker: needs you now ({DAY})") == 1


def test_never_calls_a_model_in_the_morning_run():
    src = (run.ct.ROOT / "app" / "caretaker_run.py").read_text()
    assert "anthropic" not in src.lower() and "extract_pending" not in src and "make_client" not in src


def test_monday_summary_reports_jsearch_use_against_the_cap(conn):
    """HIR-352: the plan bills past its limit, so Chandler sees the month's use weekly."""
    for d in ("2026-11-03", "2026-11-04"):
        poll.record_run(conn, {"type": "jsearch", "search": "AI engineer in Boston"}, [], day=d)
    posted = []
    run.report(conn, DAY, lambda t, b: posted.append(b) or "HIR-900", log=lambda *_: None)
    assert "Google for Jobs searches in 2026-11: 2 of our cap of 5,000." in posted[0]
    assert "cap is reached" not in posted[0]


def test_jsearch_usage_line_says_when_the_cap_is_reached(conn, monkeypatch):
    from app.sources import jsearch
    monkeypatch.setattr(jsearch, "MONTHLY_CAP", 1)
    poll.record_run(conn, {"type": "jsearch", "search": "x"}, [], day="2026-11-03")
    assert "stopped until the month turns" in run.jsearch_usage_text(conn, "2026-11-15")
