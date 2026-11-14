"""lead_pick: the lead agent's hard limits (HIR-266, HIR-280).

`pick` is pure. Each "never" in the tickets is a test here: the three labels, the third
try, the spending cap, one ticket per area at a time, the pile of decisions waiting for
Chandler, one re-read a day, a red check, the usage limit, and the launch order's
ordering. There is no count of tickets per day (HIR-280).
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
        "may_add_decision": False,
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


def test_eight_tickets_that_do_not_collide_are_all_started():
    # HIR-280 "Done when": no fixed number of tickets a day.
    out = run([ticket(n) for n in range(1, 9)])
    assert ids(out["picked"]) == [f"HIR-{n}" for n in range(1, 9)]
    assert out["skipped"] == []


def test_two_tickets_in_one_area_run_one_after_the_other():
    out = run([ticket(1, area="web"), ticket(2, area="web"), ticket(3, area="feeds")])
    assert ids(out["picked"]) == ["HIR-1", "HIR-3"]
    assert out["skipped"] == [
        {"id": "HIR-2", "why": "HIR-1 is changing the same area (web); this one waits for it to merge"}]


@pytest.mark.parametrize("state", ["In Progress", "In Review"])
def test_a_ticket_under_way_holds_its_area_until_it_merges(state):
    under_way = ticket(1, area="web", state=state)
    out = run([under_way, ticket(2, area="web"), ticket(3, area="feeds")])
    assert ids(out["picked"]) == ["HIR-3"]
    assert "HIR-1 is changing the same area (web)" in out["skipped"][-1]["why"]
    # The next run, once HIR-1 has merged and left the list, starts the second.
    assert ids(run([ticket(2, area="web")])["picked"]) == ["HIR-2"]


def test_a_ticket_in_todo_that_was_not_picked_holds_no_area():
    parked = ticket(1, area="web", labels=["parked"])
    assert ids(run([parked, ticket(2, area="web")])["picked"]) == ["HIR-2"]


def test_tickets_with_no_area_do_not_crowd_each_other_out():
    out = run([ticket(n, area=None) for n in range(1, 4)])
    assert len(out["picked"]) == 3


def test_with_ten_decisions_waiting_a_ticket_likely_to_add_one_is_held_and_a_bug_fix_runs():
    # HIR-280 "Done when".
    feature = ticket(1, may_add_decision=True)
    bug_fix = ticket(2, may_add_decision=False)
    out = run([feature, bug_fix], decisions_waiting=10)
    assert ids(out["picked"]) == ["HIR-2"]
    assert out["skipped"] == [{"id": "HIR-1", "why": (
        "likely to add a decision for Chandler, and 10 are already waiting or under way "
        "(the limit is 10)")}]
    assert out["decisions_waiting"] == 10


def test_with_nine_decisions_waiting_one_likely_ticket_runs_and_the_next_is_held():
    out = run([ticket(1, may_add_decision=True), ticket(2, may_add_decision=True)], decisions_waiting=9)
    assert ids(out["picked"]) == ["HIR-1"]
    assert "likely to add a decision" in out["skipped"][0]["why"]


def test_a_ticket_that_does_not_say_counts_as_likely_to_add_a_decision():
    unsaid = ticket(1)
    del unsaid["may_add_decision"]
    assert run([unsaid], decisions_waiting=10)["picked"] == []
    assert ids(run([unsaid], decisions_waiting=9)["picked"]) == ["HIR-1"]


def test_the_decision_limit_can_be_set():
    likely = ticket(1, may_add_decision=True)
    assert run([likely], decisions_waiting=3, max_decisions=3)["picked"] == []
    assert ids(run([likely], decisions_waiting=2, max_decisions=3)["picked"]) == ["HIR-1"]


def test_one_re_read_of_the_stored_jobs_a_day():
    out = run([ticket(1, rereads=True, est_eur=0.5), ticket(2, rereads=True, est_eur=0.5), ticket(3)])
    assert ids(out["picked"]) == ["HIR-1", "HIR-3"]
    assert "re-read" in out["picked"][0]["why"]
    assert "one a day" in out["skipped"][0]["why"]


def test_a_re_read_started_by_an_earlier_run_today_counts():
    started = f"- HIR-9 | picked: milestone 1; {lp.REREAD} | result: merging | spend: €0.50"
    out = run([ticket(1, rereads=True)], [{"date": TODAY, "body": started}])
    assert out["picked"] == []
    assert ids(run([ticket(1, rereads=True)], [{"date": "2026-11-11", "body": started}])["picked"]) == ["HIR-1"]
    held = started.replace("merging", "not-started")
    assert ids(run([ticket(1, rereads=True)], [{"date": TODAY, "body": held}])["picked"]) == ["HIR-1"]


def test_while_a_check_is_red_only_its_repair_is_started():
    out = run([ticket(1), ticket(2, repair=True)], red=["the robot visitor"])
    assert ids(out["picked"]) == ["HIR-2"]
    assert out["skipped"] == [
        {"id": "HIR-1", "why": "the robot visitor must be green first; only the repair is started"}]
    both = run([ticket(1)], red=["the main branch's checks", "the robot visitor"])
    assert both["picked"] == []
    assert "the main branch's checks and the robot visitor must be green" in both["skipped"][0]["why"]


def test_a_usage_limit_hit_today_stops_the_rest_of_the_day():
    body = line("HIR-9", "not-started") + "\nUsage limit: reached, 14:30 run.\n"
    out = run([ticket(1)], [{"date": TODAY, "body": body}])
    assert out["picked"] == [] and "usage limit" in out["stop"]
    assert ids(run([ticket(1)], [{"date": "2026-11-11", "body": body}])["picked"]) == ["HIR-1"]


def test_the_days_spend_is_added_up_over_every_run_of_the_day():
    log = [{"date": TODAY, "body": line("HIR-8", "merged", "0.90")},
           {"date": TODAY, "body": line("HIR-9", "running", "0.90")}]
    out = run([ticket(1, est_eur=0.30), ticket(2)], log)
    assert out["spent_eur"] == 1.8
    assert ids(out["picked"]) == ["HIR-2"]


def test_the_queue_says_how_many_to_pull_into_todo():
    # Three can run alone; two are picked, one waits for its area: pull 4 to keep 5 waiting.
    tickets = [ticket(1, area="web"), ticket(2, area="web"), ticket(3),
               ticket(4, labels=["attended"]), ticket(5, blocked=True), ticket(6, state="Backlog")]
    assert run(tickets)["queue"] == {"run_alone_in_todo": 3, "left_after_pick": 1, "pull": 4}
    waiting = [ticket(n, area="web") for n in range(1, 8)]
    assert run(waiting)["queue"] == {"run_alone_in_todo": 7, "left_after_pick": 6, "pull": 0}
    assert run([], cap=0)["queue"]["pull"] == 5


def test_monday_gets_the_weeks_three_numbers():
    monday = "2026-11-16"
    log = [
        {"date": "2026-11-08", "body": line("HIR-1", "merged")},       # the week before
        {"date": "2026-11-09", "body": line("HIR-2", "merged") + "\n" + line("HIR-3", "failed")},
        {"date": "2026-11-10", "body": line("HIR-3", "merged") + "\n" + line("HIR-4", "not-started")},
        {"date": "2026-11-15", "body": line("HIR-5", "waiting")},      # a Sunday run
        {"date": monday, "body": line("HIR-6", "merged")},              # this week
    ]
    tickets = [ticket(n) for n in range(10, 14)] + [ticket(14, state="Backlog"),
               ticket(15, state="Backlog"), ticket(16, labels=["attended"]), ticket(17, state="In Progress")]
    out = lp.pick(tickets, log, monday, 2.0, decisions_waiting=7)
    assert out["monday"] == ("Agents ran 3 tickets last week (2026-11-09 to 2026-11-15). "
                             "6 tickets left can run without you. 7 decisions are waiting for you.")


def test_monday_says_plainly_when_the_run_alone_queue_is_nearly_empty():
    out = lp.pick([ticket(1), ticket(2, labels=["attended"])], [], "2026-11-16", 2.0, decisions_waiting=1)
    assert out["monday"] == (
        "Agents ran 0 tickets last week (2026-11-09 to 2026-11-15). "
        "1 ticket left can run without you. 1 decision is waiting for you. "
        "The queue of tickets that can run without you is nearly empty: the project is now "
        "waiting on your decisions, not on agents.")


def test_only_monday_gets_the_weeks_numbers():
    assert "monday" not in run([ticket(1)])           # TODAY is a Thursday
    assert "monday" in lp.pick([], [], "2026-11-16", 0)  # even when the cap stops the run


def test_a_weekend_day_is_a_day_like_any_other():
    out = lp.pick([ticket(1)], [], "2026-11-14", 2.0)   # a Saturday
    assert ids(out["picked"]) == ["HIR-1"]


def test_order_is_milestone_then_visitor_bug_then_priority_then_oldest():
    later_milestone = ticket(1, milestone_rank=2, priority=1, visitor_bug=True)
    plain = ticket(2, priority=1)
    visitor = ticket(3, priority=4, visitor_bug=True)
    older = ticket(4, priority=3, created="2026-10-01")
    newer = ticket(5, priority=3, created="2026-11-05")
    no_priority = ticket(6, priority=0, created="2026-01-01")
    out = run([later_milestone, no_priority, newer, older, plain, visitor])
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
    assert config["max_decisions_waiting"] == 10
    assert config["queue_min"] == 5
    # No count of tickets per day or per area (HIR-280).
    assert set(config) == {"_comment", "daily_cap_eur", "max_decisions_waiting", "queue_min"}


@pytest.mark.parametrize("left_out", ["decisions_waiting", "red"])
def test_cli_refuses_a_state_that_did_not_look(left_out, tmp_path, capsys):
    whole = {"today": TODAY, "decisions_waiting": 0, "red": [], "log": [], "tickets": [ticket(1)]}
    del whole[left_out]
    state = tmp_path / "state.json"
    state.write_text(json.dumps(whole))
    with pytest.raises(SystemExit):
        lp.main([str(state)])
    assert left_out in capsys.readouterr().err


def test_cli_passes_the_decisions_and_the_red_checks_on(tmp_path, capsys):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({
        "today": TODAY, "decisions_waiting": 10, "red": ["the robot visitor"], "log": [],
        "tickets": [ticket(1, may_add_decision=True, repair=True), ticket(2, repair=True), ticket(3)]}))
    assert lp.main([str(state)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert ids(out["picked"]) == ["HIR-2"]
    assert sorted(ids(out["skipped"])) == ["HIR-1", "HIR-3"]


def test_the_lead_agents_procedure_hands_the_script_what_it_needs():
    """The script's limits only hold if the procedure supplies their inputs (HIR-280)."""
    skill = (ROOT / ".claude" / "skills" / "lead-agent" / "SKILL.md").read_text()
    for field in ("decisions_waiting", "red", "area", "may_add_decision", "rereads", "repair",
                  "queue.pull", "monday", "Usage limit: reached", "result: running"):
        assert f"`{field}`" in skill, field
    # The once-a-weekday limits are gone.
    assert "up to 3" not in skill and "day's 3" not in skill
    assert "a run has happened today: stop" not in skill


def test_cli_reads_the_cap_from_the_config_and_zero_stops_it(tmp_path, capsys):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({"today": TODAY, "decisions_waiting": 0, "red": [], "log": [],
                                 "tickets": [ticket(1)]}))
    assert lp.main([str(state)]) == 0
    assert ids(json.loads(capsys.readouterr().out)["picked"]) == ["HIR-1"]
    assert lp.main([str(state), "--cap", "0"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["picked"] == [] and "zero" in out["stop"]
