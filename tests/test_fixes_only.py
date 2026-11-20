"""Fixes-only mode (HIR-341): over the Christmas break agents repair and ship nothing new.

One setting, three readers. Each claim in the ticket is a test here: the window's two
ends, feature tickets skipped and bug tickets picked, the merger refusing a pull request
that is not a fix, and the one line that turns it off. The Monday summary's first line
is in tests/test_caretaker_run.py.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from app import fixes_only as fx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lp = _load("lead_pick")
mr = _load("merge_reviewed")

BREAK = {"from": "2026-12-16", "until": None}
DURING = "2026-12-21"  # a Monday inside the break
BEFORE = "2026-12-15"


def ticket(n, labels=("autopilot",), **over):
    base = {"id": f"HIR-{n}", "state": "Todo", "labels": list(labels), "blocked": False,
            "milestone_rank": 1, "priority": 3, "created": "2026-12-01", "area": f"area-{n}",
            "est_eur": 0, "may_add_decision": False}
    base.update(over)
    return base


def pick(tickets, today=DURING, setting=BREAK, **over):
    return lp.pick(tickets, [], today, 2.0, fixes_only=setting, **over)


# ---- the setting

@pytest.mark.parametrize("setting, today, on", [
    (BREAK, "2026-12-15", False),          # the day before
    (BREAK, "2026-12-16", True),           # the first day
    (BREAK, "2027-03-01", True),           # no end: on until he turns it off
    ({"from": "2026-12-16", "until": "2027-01-10"}, "2027-01-10", True),   # the last day
    ({"from": "2026-12-16", "until": "2027-01-10"}, "2027-01-11", False),  # the day after
    (None, DURING, False),                 # "fixes_only": null, the off switch
    ({}, DURING, False),
])
def test_the_mode_is_on_from_its_first_day_to_its_last_or_until_turned_off(setting, today, on):
    assert fx.is_on(setting, today) is on
    assert (fx.sentence(setting, today) is not None) is on


def test_a_date_that_cannot_be_read_is_an_error_not_an_early_end():
    with pytest.raises(ValueError):
        fx.is_on({"from": "16 Dec"}, DURING)
    with pytest.raises(ValueError):
        fx.is_on({"from": "2026-12-16", "until": "January"}, DURING)


def test_the_sentence_says_when_it_began_and_how_it_ends():
    assert fx.sentence(BREAK, DURING) == (
        "The site is in fixes-only mode: since 16 December 2026 agents only repair what breaks "
        "and ship nothing new, until Chandler turns it off.")
    assert "up to and including 10 January 2027" in fx.sentence(
        {"from": "2026-12-16", "until": "2027-01-10"}, DURING)


def test_the_committed_setting_starts_on_16_december_with_no_end():
    assert fx.load() == {"from": "2026-12-16", "until": None}
    # One line in the file, so turning it off is a one-line change.
    lines = [line for line in fx.CONFIG.read_text().splitlines() if line.lstrip().startswith('"fixes_only"')]
    assert len(lines) == 1 and "2026-12-16" in lines[0]


def test_the_command_says_on_or_off(tmp_path, capsys):
    config = tmp_path / "c.json"
    config.write_text(json.dumps({"fixes_only": BREAK}))
    fx.main(["--config", str(config), "--today", DURING])
    assert capsys.readouterr().out.startswith("on: The site is in fixes-only mode")
    config.write_text(json.dumps({"fixes_only": None}))
    fx.main(["--config", str(config), "--today", DURING])
    assert capsys.readouterr().out.strip() == "off"


# ---- the lead agent's pick

def test_while_the_mode_is_on_feature_tickets_are_skipped_and_bug_tickets_are_picked():
    answer = pick([ticket(1, ["autopilot", "Feature"]), ticket(2, ["autopilot", "Bug"]),
                   ticket(3, ["autopilot", "Improvement"]), ticket(4)])
    assert [p["id"] for p in answer["picked"]] == ["HIR-2"]
    skipped = {s["id"]: s["why"] for s in answer["skipped"]}
    assert set(skipped) == {"HIR-1", "HIR-3", "HIR-4"}
    assert all("fixes-only mode is on" in why for why in skipped.values())
    assert answer["fixes_only"].startswith("The site is in fixes-only mode")


def test_the_same_tickets_all_run_the_day_before_and_once_it_is_turned_off():
    tickets = [ticket(1, ["autopilot", "Feature"]), ticket(2, ["autopilot", "Bug"])]
    for answer in (pick(tickets, today=BEFORE), pick(tickets, setting=None)):
        assert {p["id"] for p in answer["picked"]} == {"HIR-1", "HIR-2"}
        assert answer["fixes_only"] is None


def test_the_repair_for_a_red_check_is_a_fix_whatever_its_label():
    answer = pick([ticket(1, repair=True), ticket(2, ["autopilot", "Bug"])], red=["the robot visitor"])
    assert [p["id"] for p in answer["picked"]] == ["HIR-1"]


def test_a_bug_ticket_still_obeys_every_other_limit():
    answer = pick([ticket(1, ["Bug", "attended"]), ticket(2, ["Bug"], blocked=True),
                   ticket(3, ["bug"], est_eur=None)])
    assert answer["picked"] == []
    assert not any("fixes-only" in s["why"] for s in answer["skipped"])


def test_mondays_pace_opens_with_the_mode_only_while_it_is_on():
    assert pick([])["monday"].startswith("The site is in fixes-only mode")
    assert pick([], setting=None)["monday"].startswith("Agents ran")


def test_a_collided_feature_pull_request_is_repaired_but_not_reviewed_while_the_mode_is_on():
    collided = [{"pr": 1, "ticket": "HIR-1", "labels": ["autopilot"], "pr_labels": [], "live": False},
                {"pr": 2, "ticket": "HIR-2", "labels": ["autopilot", "Bug"], "pr_labels": [], "live": False}]
    start = {r["pr"]: r for r in pick([], collided=collided)["repairs"]["start"]}
    assert start[1]["review"] is False and "fixes-only mode" in start[1]["why"]
    assert start[2]["review"] is True
    assert all(r["review"] for r in pick([], setting=None, collided=collided)["repairs"]["start"])


def test_main_reads_the_setting_from_the_config(tmp_path, capsys):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({"today": DURING, "decisions_waiting": 0, "red": [],
                                 "tickets": [ticket(1), ticket(2, ["Bug"])]}))
    assert lp.main([str(state)]) == 0
    assert [p["id"] for p in json.loads(capsys.readouterr().out)["picked"]] == ["HIR-2"]


# ---- GitHub's merger

def pr(labels, mergeable_state="clean"):
    return {"number": 7, "state": "open", "draft": False, "mergeable_state": mergeable_state,
            "labels": [{"name": n} for n in labels], "head": {"sha": "abc123"}}


def test_the_merger_refuses_a_reviewed_pull_request_that_is_not_a_fix_while_the_mode_is_on():
    merge, reason = mr.decide(pr(["review-passed"]), ["app/x.py"], fixes_only=True)
    assert merge is False and "fixes-only mode" in reason
    assert mr.decide(pr(["review-passed", "fix"]), ["app/x.py"], fixes_only=True)[0] is True
    assert mr.decide(pr(["review-passed"]), ["app/x.py"], fixes_only=False)[0] is True


def test_the_fix_label_alone_merges_nothing():
    assert mr.decide(pr(["fix"]), ["app/x.py"], fixes_only=True)[0] is False
    assert mr.decide(pr(["review-passed", "fix", "needs-chandler"]), ["app/x.py"], fixes_only=True)[0] is False
    assert mr.decide(pr(["review-passed", "fix"]), ["AGENTS.md"], fixes_only=True)[0] is False


def test_the_merger_run_leaves_a_feature_open_and_does_not_wait_on_its_checks(monkeypatch):
    acts, slept = [], []

    def gh(*args):
        if args[0] == "api" and args[1].endswith("/files"):
            return "app/x.py"
        if args[0] == "api":
            return json.dumps(pr(["review-passed"], mergeable_state="unstable"))
        acts.append(args)
        return ""

    monkeypatch.setattr(mr, "_gh", gh)
    monkeypatch.setattr(mr, "_fixes_only_now", lambda: True)
    assert mr.run("o/r", 7, sleep=slept.append) is False
    assert acts == [] and slept == []
