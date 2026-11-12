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
    assert all(r["mode"] == "report" and not r["done"] for r in logged)


def test_both_fixes_appear_in_the_next_weekly_summary(conn):
    poll_today(conn, feeds_doc()["feeds"], day="2026-11-12")
    run.morning(conn, "2026-11-12", feeds_doc(), set(), moved_board_search, fetch_board,
                now=datetime(2026, 11, 12, 9, tzinfo=timezone.utc))
    text = run.weekly_text(conn, "2026-11-09", "2026-11-15")
    assert "report-only" in text
    assert "## What it would have fixed" in text and "ashby:doctolib" in text
    assert "## What it would have paused" in text and "lever:pipedrive" in text
    assert "Spent" not in text                                 # bookkeeping is not a finding


def test_report_only_never_writes_the_feeds_file(conn, tmp_path, monkeypatch):
    from app import caretaker
    monkeypatch.setattr(caretaker, "write_feeds", lambda *a, **k: pytest.fail("wrote feeds.json"))
    doc = feeds_doc()
    before = json.dumps(doc)
    poll_today(conn, doc["feeds"])
    morning(conn, doc=doc)
    assert json.dumps(doc) == before


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


# --- reporting ---------------------------------------------------------------------------

def test_monday_summary_posts_once(conn):
    poll_today(conn, feeds_doc()["feeds"])
    morning(conn)
    posted = []
    run.report(conn, DAY, lambda t, b: posted.append((t, b)) or "HIR-900", log=lambda *_: None)
    run.report(conn, DAY, lambda t, b: posted.append((t, b)) or "HIR-901", log=lambda *_: None)
    assert [t for t, _ in posted] == ["Caretaker weekly summary: 2026-11-09 to 2026-11-15"]


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
