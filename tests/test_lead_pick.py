"""lead_pick: the lead agent's hard limits (HIR-266).

`pick` is pure. Each "never" in the ticket is a test here: the three labels, the third
try, the spending cap, the daily and per-area counts, and the launch order's ordering.
"""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("lead_pick", ROOT / "scripts" / "lead_pick.py")
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)

TODAY = "2026-11-12"


def ticket(n, **over):
    base = {
        "id": f"HIR-{n}",
        "state": "Todo",
        "labels": ["autopilot"],
        "blocked": False,
        "milestone_rank": 1,
        "visitor_bug": False,
        "priority": 3,
        "created": "2026-11-01",
        "area": f"area-{n}",
        "est_eur": 0,
    }
    base.update(over)
    return base


def line(ticket_id, result, spend="0.00"):
    return f"- {ticket_id} | picked: milestone 1 | result: {result} | spend: €{spend}"


def ids(entries):
    return [e["id"] for e in entries]


def run(tickets, log=(), cap=2.0, **kw):
    return lp.pick(tickets, list(log), TODAY, cap, **kw)


def test_an_ordinary_todo_ticket_is_picked_with_a_reason():
    out = run([ticket(1)])
    assert out["stop"] is None
    assert ids(out["picked"]) == ["HIR-1"]
    assert "milestone 1" in out["picked"][0]["why"]


@pytest.mark.parametrize("label", ["attended", "hands-on", "parked", "Attended", "Hands-On"])
def test_a_ticket_with_a_never_label_is_not_picked(label):
    out = run([ticket(1, labels=["autopilot", label])])
    assert out["picked"] == []
    assert out["skipped"][0]["why"] == f"labelled {label.lower()}"


def test_never_labels_lose_to_nothing_else_about_the_ticket():
    # Urgent, visitor-facing, first milestone: still not picked.
    hot = ticket(1, labels=["Bug", "parked"], priority=1, visitor_bug=True, milestone_rank=0)
    assert ids(run([hot, ticket(2)])["picked"]) == ["HIR-2"]


@pytest.mark.parametrize("state", ["Backlog", "In Progress", "Done", "Canceled"])
def test_only_todo_is_picked(state):
    out = run([ticket(1, state=state)])
    assert out["picked"] == []
    assert state in out["skipped"][0]["why"]


def test_a_blocked_ticket_is_not_picked():
    out = run([ticket(1, blocked=True)])
    assert out["picked"] == []
    assert "blocked" in out["skipped"][0]["why"]


def test_one_failure_is_retried_two_are_not():
    once = [{"date": "2026-11-10", "body": line("HIR-1", "failed")}]
    twice = once + [{"date": "2026-11-11", "body": line("HIR-1", "failed")}]
    assert ids(run([ticket(1)], once)["picked"]) == ["HIR-1"]
    out = run([ticket(1)], twice)
    assert out["picked"] == []
    assert "Monday" in out["skipped"][0]["why"]


def test_only_failed_results_count_as_failures():
    log = [{"date": "2026-11-10", "body": "\n".join([
        line("HIR-1", "merged"), line("HIR-1", "merging"), line("HIR-1", "sent-back"),
        line("HIR-1", "waiting"), line("HIR-2", "failed"), line("HIR-2", "failed"),
    ])}]
    assert lp.failures(log) == {"HIR-2": 2}
    assert ids(run([ticket(1), ticket(2)], log)["picked"]) == ["HIR-1"]


def test_a_cap_of_zero_stops_the_run():
    out = run([ticket(1)], cap=0)
    assert out["picked"] == [] and out["skipped"] == []
    assert "zero" in out["stop"]


def test_a_spent_cap_stops_the_run():
    log = [{"date": TODAY, "body": line("HIR-9", "merged", "2.00")}]
    out = run([ticket(1)], log)
    assert out["picked"] == []
    assert "reached" in out["stop"]
    assert out["spent_eur"] == 2.0


def test_yesterdays_spend_does_not_count_today():
    log = [{"date": "2026-11-11", "body": line("HIR-9", "merged", "2.00")}]
    out = run([ticket(1)], log)
    assert out["stop"] is None and ids(out["picked"]) == ["HIR-1"]
    assert out["spent_eur"] == 0


def test_a_ticket_that_would_pass_the_cap_is_skipped_and_a_cheaper_one_still_runs():
    log = [{"date": TODAY, "body": line("HIR-9", "merged", "1.50")}]
    out = run([ticket(1, est_eur=0.60), ticket(2, est_eur=0.40)], log)
    assert ids(out["picked"]) == ["HIR-2"]
    assert "€0.60" in out["skipped"][0]["why"]


def test_the_picked_tickets_together_stay_under_the_cap():
    out = run([ticket(1, est_eur=1.2), ticket(2, est_eur=1.2), ticket(3, est_eur=0.8)])
    assert ids(out["picked"]) == ["HIR-1", "HIR-3"]


def test_unknown_spend_is_never_started():
    out = run([ticket(1, est_eur=None)])
    assert out["picked"] == []
    assert "Chandler" in out["skipped"][0]["why"]


def test_at_most_three_a_day():
    out = run([ticket(n) for n in range(1, 6)])
    assert len(out["picked"]) == 3
    assert all("3 tickets already picked" in s["why"] for s in out["skipped"])


def test_at_most_two_in_one_area():
    out = run([ticket(1, area="web"), ticket(2, area="web"), ticket(3, area="web"), ticket(4, area="feeds")])
    assert ids(out["picked"]) == ["HIR-1", "HIR-2", "HIR-4"]
    assert "same area (web)" in out["skipped"][0]["why"]


def test_tickets_with_no_area_do_not_crowd_each_other_out():
    out = run([ticket(n, area=None) for n in range(1, 4)])
    assert len(out["picked"]) == 3


def test_order_is_milestone_then_visitor_bug_then_priority_then_oldest():
    later_milestone = ticket(1, milestone_rank=2, priority=1, visitor_bug=True)
    plain = ticket(2, priority=1)
    visitor = ticket(3, priority=4, visitor_bug=True)
    older = ticket(4, priority=3, created="2026-10-01")
    newer = ticket(5, priority=3, created="2026-11-05")
    no_priority = ticket(6, priority=0, created="2026-01-01")
    out = run([later_milestone, no_priority, newer, older, plain, visitor], max_tickets=6)
    assert ids(out["picked"]) == ["HIR-3", "HIR-2", "HIR-4", "HIR-5", "HIR-6", "HIR-1"]


def test_always_on_work_comes_before_the_first_milestone():
    out = run([ticket(1, milestone_rank=1), ticket(2, milestone_rank=0)])
    assert ids(out["picked"]) == ["HIR-2", "HIR-1"]
    assert out["picked"][0]["why"].startswith("always on")


def test_log_lines_are_read_from_a_real_looking_comment():
    body = (
        "**Lead agent log, Thu 12 Nov**\n\n"
        "- HIR-197 | picked: always on; a bug a visitor would notice | result: merged | spend: €0.00\n"
        "* HIR-131 | picked: always on | result: failed | spend: €0.35\n"
        "Needs you: nothing.\n"
        "- not a ticket line | result: failed | spend: €9.00\n"
    )
    log = [{"date": TODAY, "body": body}]
    assert lp.read_log(log) == [(TODAY, "HIR-197", "merged", 0.0), (TODAY, "HIR-131", "failed", 0.35)]
    assert lp.spent_on(log, TODAY) == 0.35


def test_the_config_holds_the_starting_limits():
    config = json.loads((ROOT / "config" / "lead_agent.json").read_text())
    assert config["daily_cap_eur"] == 2.0
    assert config["max_tickets"] == 3
    assert config["max_per_area"] == 2


def test_cli_reads_the_cap_from_the_config_and_zero_stops_it(tmp_path, capsys):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({"today": TODAY, "log": [], "tickets": [ticket(1)]}))
    assert lp.main([str(state)]) == 0
    assert ids(json.loads(capsys.readouterr().out)["picked"]) == ["HIR-1"]
    assert lp.main([str(state), "--cap", "0"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["picked"] == [] and "zero" in out["stop"]
