"""Tests for app/site_watch_week.py (HIR-260): the robot visitor's part of the Monday
summary. Linear is never called: a fake stands in for the HTTP request."""

import importlib.util
from pathlib import Path

from app import site_watch_week as sw

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("site_watch_ticket", ROOT / "scripts" / "site_watch_ticket.py")
swt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(swt)

START, END = "2026-11-09", "2026-11-15"
PATH = 'Site watch: "compare mode" fails'


def issue(id, title=PATH, created="2026-11-10T09:00:00.000Z", completed=None, canceled=None,
          labels=("autopilot",), description=swt.WHAT_HAPPENED["morning"]):
    return {"id": id, "title": title, "description": description, "url": f"https://linear.app/x/{id}",
            "created": created, "completed": completed, "canceled": canceled, "labels": list(labels)}


# --- which tickets are the robot's ---------------------------------------------------------

def test_the_titles_the_ticket_script_writes_are_recognised():
    class Args:
        change = rolled_back_to = run_url = results_root = evidence_base = detail = None
    f = {"test": "compare mode", "projects": ["phone"], "error": "x", "screenshots": []}
    for t in (swt.robot_ticket("deploy", f, Args), swt.robot_ticket("still-failing", f, Args, [f]),
              swt.uptime_ticket(Args), swt.rollback_failed_ticket(Args, [f])):
        assert sw.is_robot_ticket(t["title"]), t["title"]


def test_other_tickets_about_the_site_watch_are_not_the_robots():
    assert not sw.is_robot_ticket("Site watch: agents pick up robot-visitor tickets, fix them")
    assert not sw.is_robot_ticket("Site map for the public launch")


def test_rolled_back_is_read_from_the_sentence_the_ticket_script_writes():
    assert sw.ROLLED_BACK in swt.WHAT_HAPPENED["deploy"]
    assert sw.ROLLED_BACK not in swt.WHAT_HAPPENED["morning"]


# --- the week's report ---------------------------------------------------------------------

def test_a_quiet_week_is_one_line():
    assert sw.report([], START, END) == "# The robot visitor\n\nNothing broke on the live site all week.\n"
    assert sw.needs_you([]) == ""


def test_what_broke_says_whether_the_change_was_rolled_back():
    text = sw.report([
        issue("HIR-1", description=swt.WHAT_HAPPENED["deploy"]),
        issue("HIR-2", title='Site watch: "the job list" fails', created="2026-11-12T08:05:00.000Z"),
        issue("HIR-3", title=sw.UPTIME_TITLE, created="2026-11-13T03:00:00.000Z"),
    ], START, END)
    broke = text.split("## What broke")[1].split("##")[0]
    assert '- 2026-11-10: "compare mode" stopped working, right after a change went live; the change was rolled back' in broke
    assert '- 2026-11-12: "the job list" stopped working, found on the morning check; nothing was rolled back' in broke
    assert "- 2026-11-13: The site did not answer" in broke
    assert "[HIR-1](https://linear.app/x/HIR-1)" in broke


def test_a_ticket_from_before_the_week_is_not_listed_as_broken_this_week():
    text = sw.report([issue("HIR-1", created="2026-11-08T23:59:00.000Z", completed="2026-11-09T10:00:00.000Z")], START, END)
    assert "## What broke" not in text
    assert ('- 2026-11-09: the fix for [HIR-1](https://linear.app/x/HIR-1) went in '
            '("compare mode" stopped working on 2026-11-08); the robot visitor has not seen it break since.') in text


def test_fixed_says_whether_it_has_broken_since():
    held = issue("HIR-1", completed="2026-11-11T10:00:00.000Z")
    text = sw.report([held], START, END)
    assert "the robot visitor has not seen it break since" in text
    again = issue("HIR-2", created="2026-11-13T09:00:00.000Z")
    text = sw.report([held, again], START, END)
    fixed = text.split("## What was fixed")[1].split("##")[0]
    assert "it broke again on 2026-11-13" in fixed
    # Another path breaking later says nothing about this fix.
    other = issue("HIR-3", title='Site watch: "the job list" fails', created="2026-11-13T09:00:00.000Z")
    assert "has not seen it break since" in sw.report([held, other], START, END)


def test_still_open_lists_every_open_ticket_however_old_and_who_has_it():
    text = sw.report([
        issue("HIR-1", created="2026-10-20T09:00:00.000Z"),
        issue("HIR-2", title=sw.UPTIME_TITLE, labels=("attended",)),
        issue("HIR-3", completed="2026-11-11T10:00:00.000Z"),
        issue("HIR-4", canceled="2026-11-11T10:00:00.000Z"),
    ], START, END)
    still = text.split("## Still open")[1]
    assert "open since 2026-10-20, for an agent to fix ([HIR-1]" in still
    assert "The site did not answer, open since 2026-11-10, waiting for you ([HIR-2]" in still
    assert "HIR-3" not in still and "HIR-4" not in still


def test_a_cancelled_ticket_is_not_reported_as_fixed():
    text = sw.report([issue("HIR-4", canceled="2026-11-11T10:00:00.000Z")], START, END)
    assert "## What broke" in text and "## What was fixed" not in text


# --- what goes above everything else -------------------------------------------------------

def test_a_break_after_two_fixes_is_the_needs_you_block():
    text = sw.needs_you([issue("HIR-9", labels=("attended",)), issue("HIR-8")])
    assert text.startswith("# The live site: needs you\n")
    assert '- "compare mode" stopped working again after two fixes in 30 days, so no agent is working on it.' in text
    assert "HIR-9" in text and "HIR-8" not in text


def test_needs_you_drops_a_ticket_once_it_is_closed_and_keeps_an_open_rollback_failure():
    done = issue("HIR-9", labels=("attended",), completed="2026-11-12T10:00:00.000Z")
    assert sw.needs_you([done]) == ""
    down = issue("HIR-7", title=sw.DOWN_TITLE, labels=())
    assert "the automatic rollback did not fix it" in sw.needs_you([down])


def test_the_ticket_scripts_third_time_ticket_lands_in_needs_you():
    # End to end across the two files: what the ticket script files after two fixes is what
    # this module lists for Chandler.
    t = swt.after_two_fixes({"title": PATH, "body": "b", "autopilot": True}, ["HIR-1", "HIR-2"])
    assert sw.needs_you([issue("HIR-9", title=t["title"], labels=(t["label"],), description=t["body"])])


# --- reading Linear ------------------------------------------------------------------------

def node(identifier, title, labels=("autopilot",), completed=None):
    return {"identifier": identifier, "title": title, "description": "d", "url": f"https://linear.app/x/{identifier}",
            "createdAt": "2026-11-10T09:00:00.000Z", "completedAt": completed, "canceledAt": None,
            "labels": {"nodes": [{"name": n} for n in labels]}}


def test_fetch_asks_once_read_only_and_keeps_only_the_robots_tickets():
    sent = []

    def post_json(url, payload, headers):
        sent.append((url, payload, headers))
        return {"data": {"issues": {"nodes": [
            node("HIR-1", PATH), node("HIR-260", "Site watch: agents pick up robot-visitor tickets"),
            node("HIR-2", sw.DOWN_TITLE, labels=())]}}}

    got = sw.fetch(START, "key", "team-1", post_json)
    assert [i["id"] for i in got] == ["HIR-1", "HIR-2"]
    assert got[0]["labels"] == ["autopilot"] and got[0]["created"] == "2026-11-10T09:00:00.000Z"
    [(url, payload, headers)] = sent
    assert url == sw.LINEAR_URL and headers["Authorization"] == "key"
    assert payload["variables"] == {"team": "team-1"}
    assert "mutation" not in payload["query"]
    assert '"2026-11-09T00:00:00.000Z"' in payload["query"]


def test_week_text_without_a_key_says_so_and_asks_nothing():
    def never(*a):
        raise AssertionError("no request without a key")
    assert sw.week_text(START, END, "", "team-1", never) == (
        "", "# The robot visitor\n\nNot read: there is no Linear key on the server.\n")


def test_week_text_survives_linear_failing_or_refusing():
    def boom(*a):
        raise OSError("timed out")
    top, rest = sw.week_text(START, END, "key", "team-1", boom)
    assert top == "" and "Linear could not be read this morning (OSError: timed out)" in rest
    top, rest = sw.week_text(START, END, "key", "team-1", lambda *a: {"errors": [{"message": "bad filter"}]})
    assert top == "" and "bad filter" in rest


def test_week_text_returns_both_pieces():
    top, rest = sw.week_text(START, END, "key", "team-1", lambda *a: {"data": {"issues": {"nodes": [
        node("HIR-9", PATH, labels=("attended",)), node("HIR-1", PATH, completed="2026-11-09T12:00:00.000Z")]}}})
    assert "HIR-9" in top and "## What was fixed" in rest and "## Still open" in rest
