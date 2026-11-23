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
        "likely to add a decision for Chandler to think about, and 10 are already waiting "
        "or under way (the limit is 10)")}]
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
                             "6 tickets left can run without you. "
                             "7 decisions to think about are waiting for you.")


def test_monday_says_how_many_wait_to_think_about_and_how_many_to_approve():
    # HIR-297: only the first pile slows agents down, so the sentence keeps them apart.
    out = lp.pick([ticket(n) for n in range(1, 7)], [], "2026-11-16", 2.0,
                  decisions_waiting=2, approvals_waiting=9)
    assert out["monday"].endswith("2 decisions to think about are waiting for you, and 9 to approve.")


def test_recommendations_waiting_for_a_yes_hold_nothing_back():
    """The speed limit counts only the pile he has to think about (HIR-297)."""
    likely = ticket(1, may_add_decision=True)
    assert ids(run([likely], decisions_waiting=2, approvals_waiting=40)["picked"]) == ["HIR-1"]
    assert run([likely], decisions_waiting=10, approvals_waiting=0)["picked"] == []


def test_monday_says_plainly_when_the_run_alone_queue_is_nearly_empty():
    out = lp.pick([ticket(1), ticket(2, labels=["attended"])], [], "2026-11-16", 2.0, decisions_waiting=1)
    assert out["monday"] == (
        "Agents ran 0 tickets last week (2026-11-09 to 2026-11-15). "
        "1 ticket left can run without you. 1 decision to think about is waiting for you. "
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
    assert config["monday_questions_max"] == 10 and config["monday_yours_max"] == 3
    assert config["monday_think_max"] == 3  # HIR-297: at most 3 a week to think about
    assert set(config) == {"_comment", "daily_cap_eur", "max_decisions_waiting", "queue_min",
                           "monday_questions_max", "monday_yours_max", "monday_think_max",
                           "fixes_only"}  # HIR-341, tests/test_fixes_only.py


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


# --- Monday's "Decisions waiting for you" comment (HIR-277) --------------------------------

def waiting(n, **over):
    base = {"id": f"HIR-{n}", "kind": "question", "labels": ["attended"], "answered": False,
            "blocks_milestone": False, "blocks_todo": False, "since": "2026-11-01"}
    base.update(over)
    return base


def test_mondays_comment_asks_at_most_ten_and_counts_the_rest():
    out = lp.monday_decisions([waiting(n) for n in range(1, 14)])
    assert len(out["ask"]) == 10
    assert out["more"] == 3 and out["text"] == "3 more are waiting for you."
    assert lp.monday_decisions([waiting(n) for n in range(1, 12)])["text"] == "1 more is waiting for you."


def test_ten_or_fewer_are_all_asked():
    out = lp.monday_decisions([waiting(n) for n in range(1, 11)])
    assert len(out["ask"]) == 10 and out["more"] == 0
    assert out["text"] == "That is every decision waiting for you."


def test_order_is_launch_blockers_then_todo_blockers_then_oldest():
    out = lp.monday_decisions([
        waiting(1, since="2026-10-01"),
        waiting(2, since="2026-11-10", blocks_todo=True),
        waiting(3, since="2026-11-12", blocks_milestone=True),
        waiting(4, since="2026-10-20"),
        waiting(5, since="2026-11-11", blocks_milestone=True, blocks_todo=True),
    ])
    assert out["ask"] == ["HIR-5", "HIR-3", "HIR-2", "HIR-1", "HIR-4"]


def test_a_ticket_chandler_answered_is_not_asked_again():
    """Answered on Tuesday, recorded by the next run, gone from the following Monday."""
    out = lp.monday_decisions([waiting(1, answered=True), waiting(2)])
    assert out["ask"] == ["HIR-2"] and out["more"] == 0
    # An answered ticket does not use up one of the ten places either.
    many = lp.monday_decisions([waiting(n, answered=n <= 3) for n in range(1, 14)])
    assert len(many["ask"]) == 10 and many["more"] == 0


@pytest.mark.parametrize("label", ["hands-on", "parked", "Parked"])
def test_hands_on_and_parked_tickets_are_not_questions(label):
    out = lp.monday_decisions([waiting(1, labels=["attended", label]),
                               waiting(2, kind="yours", labels=[label])])
    assert out == {"think": [], "approve": [], "ask": [], "more": 0, "more_think": 0,
                   "more_approve": 0, "yours": [], "text": "No decisions waiting"}


def test_work_chandler_does_with_an_agent_goes_under_yours_at_most_three():
    out = lp.monday_decisions(
        [waiting(n, kind="yours", since=f"2026-11-0{n}") for n in range(1, 6)] + [waiting(9)])
    assert out["ask"] == ["HIR-9"]
    assert out["yours"] == ["HIR-1", "HIR-2", "HIR-3"]


def test_a_ticket_that_does_not_say_its_kind_is_a_question():
    item = waiting(1)
    del item["kind"]
    assert lp.monday_decisions([item])["ask"] == ["HIR-1"]


# --- the two headings: to think about, to approve (HIR-297) --------------------------------

def test_a_planted_launch_chore_is_to_approve_and_a_labelling_guide_question_is_to_think_about():
    # HIR-297 "Done when": choosing a domain arrives under "To approve", a question about
    # the labelling guide under "To think about".
    domain = waiting(301, kind="approve")
    guide = waiting(302, kind="think")
    out = lp.monday_decisions([domain, guide])
    assert out["approve"] == ["HIR-301"] and out["think"] == ["HIR-302"]
    assert out["ask"] == ["HIR-302", "HIR-301"]  # what he thinks about comes first


def test_at_most_three_a_week_to_think_about_and_the_rest_of_the_ten_to_approve():
    out = lp.monday_decisions([waiting(n, kind="think") for n in range(1, 6)]
                              + [waiting(n, kind="approve") for n in range(11, 21)])
    assert out["think"] == ["HIR-1", "HIR-2", "HIR-3"]
    assert len(out["approve"]) == 7 and len(out["ask"]) == 10
    assert out["more_think"] == 2 and out["more_approve"] == 3 and out["more"] == 5
    assert out["text"] == "5 more are waiting for you."


def test_with_nothing_to_think_about_all_ten_places_go_to_approvals():
    out = lp.monday_decisions([waiting(n, kind="approve") for n in range(1, 13)])
    assert out["think"] == [] and len(out["approve"]) == 10 and out["more_approve"] == 2


@pytest.mark.parametrize("kind", [None, "question", "something else"])
def test_a_ticket_whose_kind_is_not_known_is_to_approve_not_to_think_about(kind):
    """When unsure whether a call teaches a career skill, his thinking time is not spent."""
    item = waiting(1)
    if kind is None:
        del item["kind"]
    else:
        item["kind"] = kind
    out = lp.monday_decisions([item])
    assert out["approve"] == ["HIR-1"] and out["think"] == []


def test_each_heading_keeps_the_order_launch_blockers_then_todo_blockers_then_oldest():
    out = lp.monday_decisions([
        waiting(1, kind="think", since="2026-10-01"),
        waiting(2, kind="think", since="2026-11-10", blocks_milestone=True),
        waiting(3, kind="approve", since="2026-10-02"),
        waiting(4, kind="approve", since="2026-11-11", blocks_todo=True),
    ])
    assert out["think"] == ["HIR-2", "HIR-1"] and out["approve"] == ["HIR-4", "HIR-3"]


def test_the_think_limit_can_be_set_and_an_answered_ticket_takes_no_place():
    items = [waiting(n, kind="think", answered=n == 1) for n in range(1, 5)]
    assert lp.monday_decisions(items, max_think=2)["think"] == ["HIR-2", "HIR-3"]
    assert lp.monday_decisions(items, max_questions=1)["ask"] == ["HIR-2"]


def test_a_week_with_nothing_waiting_says_so():
    assert lp.monday_decisions([])["text"] == "No decisions waiting"
    # Work that is his to do is not a decision waiting.
    assert lp.monday_decisions([waiting(1, kind="yours")])["text"] == "No decisions waiting"


def test_the_monday_limits_can_be_set():
    out = lp.monday_decisions([waiting(n) for n in range(1, 6)], max_questions=2, max_yours=1)
    assert len(out["ask"]) == 2 and out["more"] == 3


def test_a_run_that_did_not_gather_the_decisions_gets_no_answer_about_them():
    """Left out is not the same as none: no `monday_decisions`, so nothing to post."""
    assert "monday_decisions" not in run([ticket(1)])
    assert run([ticket(1)], decisions=[])["monday_decisions"]["text"] == "No decisions waiting"
    # Even when the cap stops the run, Monday's comment can still be written.
    assert "monday_decisions" in lp.pick([], [], "2026-11-16", 0, decisions=[waiting(1)])


def test_cli_reads_the_decisions_and_their_limits_from_the_config(tmp_path, capsys):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({
        "today": "2026-11-16", "decisions_waiting": 12, "red": [], "log": [], "tickets": [],
        "decisions": [waiting(n, needs_him=True) for n in range(1, 13)]
                     + [waiting(20 + n, kind="yours") for n in range(4)]}))
    assert lp.main([str(state)]) == 0
    out = json.loads(capsys.readouterr().out)["monday_decisions"]
    assert len(out["ask"]) == 10 and out["more"] == 2 and len(out["yours"]) == 3


def test_cli_reads_the_think_limit_and_the_approvals_count(tmp_path, capsys):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({
        "today": "2026-11-16", "decisions_waiting": 5, "approvals_waiting": 4, "red": [],
        "log": [], "tickets": [],
        "decisions": [waiting(n, kind="think") for n in range(1, 6)]
                     + [waiting(10 + n, kind="approve", needs_him=True) for n in range(4)]}))
    assert lp.main([str(state)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert len(out["monday_decisions"]["think"]) == 3 and len(out["monday_decisions"]["approve"]) == 4
    assert out["monday_decisions"]["decide"] == []
    assert "5 decisions to think about are waiting for you, and 4 to approve." in out["monday"]


# --- decided for him, not asked (HIR-315) ---------------------------------------------------

MONDAY = "2026-11-23"


def monday(decisions):
    return lp.pick([], [], MONDAY, 2.0, decisions=decisions)["monday_decisions"]


def test_a_planted_recommendation_to_approve_is_decided_and_not_asked():
    # HIR-315 "Done when": a planted approve-style question is decided and reported.
    out = monday([waiting(301, kind="approve")])
    assert out["decide"] == ["HIR-301"]
    assert out["ask"] == [] and out["approve"] == [] and out["text"] == "No decisions waiting"


@pytest.mark.parametrize("kind", [None, "question", "something else"])
def test_a_waiting_ticket_whose_kind_is_not_known_is_decided_like_a_recommendation(kind):
    item = waiting(1)
    if kind is None:
        del item["kind"]
    else:
        item["kind"] = kind
    assert monday([item])["decide"] == ["HIR-1"]


def test_a_spend_above_his_limit_is_still_asked_and_never_decided():
    out = monday([waiting(1, kind="approve", needs_him=True), waiting(2, kind="approve")])
    assert out["approve"] == ["HIR-1"] and out["decide"] == ["HIR-2"]
    # Not even a decision to think about that has waited its week.
    late = monday([waiting(3, kind="think", asked="2026-11-02", needs_him=True)])
    assert late["think"] == ["HIR-3"] and late["decide"] == []


def test_a_decision_to_think_about_is_his_for_a_week_after_monday_listed_it():
    out = monday([waiting(1, kind="think", asked="2026-11-16"),    # listed a week ago
                  waiting(2, kind="think", asked="2026-11-17"),    # six days ago
                  waiting(3, kind="think", asked=MONDAY)])         # listed today
    assert out["decide"] == ["HIR-1"] and out["think"] == ["HIR-2", "HIR-3"]


@pytest.mark.parametrize("asked", [None, "", "last Monday"])
def test_a_decision_to_think_about_he_was_never_shown_is_never_decided(asked):
    """In doubt it is still his: no date, or one that cannot be read, is not a week."""
    item = waiting(1, kind="think", since="2026-09-01")
    if asked is not None:
        item["asked"] = asked
    out = monday([item])
    assert out["think"] == ["HIR-1"] and out["decide"] == []


def test_no_week_with_one_question_only_every_one_to_think_about_is_listed():
    # His 16 Nov comment on the ticket: no one-decision-a-week limit.
    out = monday([waiting(n, kind="think") for n in range(1, 4)])
    assert out["think"] == ["HIR-1", "HIR-2", "HIR-3"] and out["decide"] == []


def test_his_own_work_answered_and_parked_tickets_are_never_handed_to_be_decided():
    out = monday([waiting(1, kind="yours"), waiting(2, answered=True),
                  waiting(3, labels=["attended", "parked"]),
                  waiting(4, kind="think", asked="2026-11-01", labels=["hands-on"]),
                  waiting(5, kind="think", asked="2026-11-01", answered=True)])
    assert out["decide"] == [] and out["yours"] == ["HIR-1"] and out["ask"] == []


def test_what_is_decided_keeps_mondays_order_and_takes_no_place_in_the_list():
    out = monday([waiting(1, since="2026-10-01"),
                  waiting(2, since="2026-11-10", blocks_milestone=True),
                  waiting(3, kind="think", asked="2026-11-09", since="2026-11-05", blocks_todo=True)]
                 + [waiting(10 + n, needs_him=True) for n in range(10)])
    assert out["decide"] == ["HIR-2", "HIR-3", "HIR-1"]
    assert len(out["ask"]) == 10 and out["more"] == 0


def test_the_script_names_what_is_decided_on_any_day_not_only_monday():
    out = lp.pick([], [], "2026-11-18", 2.0, decisions=[waiting(1)])
    assert out["monday_decisions"]["decide"] == ["HIR-1"] and "monday" not in out


# --- telling Chandler's answer from an agent's comment (HIR-277) ---------------------------

ASKED = "2026-11-16T10:31:00.000Z"


def comment(at, body):
    return {"at": at, "body": body}


def test_a_plain_comment_after_the_question_may_be_his_answer():
    his = comment("2026-11-17T08:00:00.000Z", "Go with option A.")
    assert lp.answer_candidates(ASKED, [his]) == [his]


def test_a_comment_older_than_the_question_is_not_an_answer_to_it():
    assert lp.answer_candidates(ASKED, [comment("2026-11-12T09:00:00.000Z", "Option A.")]) == []
    assert lp.answer_candidates(ASKED, [comment(ASKED, "The question itself.")]) == []


@pytest.mark.parametrize("body", [
    "**Brief (autopilot run)**\n\n- **Doing:** a thing",
    "**Decided for you**\nRepaired 3 stored jobs.",
    "**Review: sent back**\n\n1. Add the test.",
    "Lead agent: no run is live on this; returned to Todo",
    "**Hands-on brief**\nStart with the form.",
    "**Answered**\nChandler, 17 Nov: option A.",
    "**Pace**\nAgents ran 3 tickets last week.",
    "**Decisions waiting for you**\n\n1. A question.",
    "**To approve**\n\n**Recommend:** buy the .com domain.",
    "**To think about**\n\nThe labelling guide does not say how to score a posting.",
    "Opened https://github.com/chandlershortlidge/hiring-radar/pull/177, 1600 tests pass.",
    "   ",
])
def test_an_agents_own_comment_is_never_his_answer(body):
    assert lp.answer_candidates(ASKED, [comment("2026-11-17T08:00:00.000Z", body)]) == []


def test_an_answer_an_agent_session_wrote_down_for_him_counts():
    noted = comment("2026-11-17T08:00:00.000Z", "**Decision (Chandler, 17 Nov, in the session): option A.**")
    assert lp.answer_candidates(ASKED, [noted]) == [noted]


def test_a_word_that_only_starts_like_a_heading_is_still_his():
    his = comment("2026-11-17T08:00:00.000Z", "Briefly: yes, do it. Reviewing the rest later.")
    assert lp.answer_candidates(ASKED, [his]) == [his]


def test_a_ticket_nobody_asked_him_about_has_no_answer():
    """Its `attended` label is his own off switch; a comment on it lifts nothing."""
    plain = comment("2026-11-17T08:00:00.000Z", "Go ahead.")
    assert lp.answer_candidates(None, [plain]) == []
    assert lp.answer_candidates("", [plain]) == []
    assert lp.answer_candidates(ASKED, []) == []


def test_the_run_gets_the_candidates_per_ticket_only_when_it_handed_the_comments_over():
    assert "answer_candidates" not in run([ticket(1)])
    his = comment("2026-11-17T08:00:00.000Z", "Option B.")
    out = run([], answers=[
        {"id": "HIR-5", "question_at": ASKED, "comments": [his, comment("2026-11-17T09:00:00.000Z", "**Answered**")]},
        {"id": "HIR-6", "question_at": None, "comments": [his]}])
    assert out["answer_candidates"] == [{"id": "HIR-5", "candidates": [his]},
                                        {"id": "HIR-6", "candidates": []}]


def test_cli_passes_the_answers_on(tmp_path, capsys):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({
        "today": TODAY, "decisions_waiting": 1, "red": [], "log": [], "tickets": [],
        "answers": [{"id": "HIR-5", "question_at": ASKED,
                     "comments": [comment("2026-11-17T08:00:00.000Z", "Option B.")]}]}))
    assert lp.main([str(state)]) == 0
    assert json.loads(capsys.readouterr().out)["answer_candidates"][0]["candidates"][0]["body"] == "Option B."


def test_the_lead_agents_procedure_writes_the_decisions_comment_and_applies_answers():
    """The comment's limits hold only if the procedure hands the script the tickets and
    posts what it answers; an answered ticket is only left out if a run records it."""
    skill = " ".join((ROOT / ".claude" / "skills" / "lead-agent" / "SKILL.md").read_text().split())
    for field in ("decisions", "kind", "answered", "blocks_milestone", "blocks_todo", "since",
                  "monday_decisions", "ask", "more", "yours", "text",
                  "think", "approve", "approvals_waiting", "decide", "asked", "needs_him",
                  "answers", "question_at", "answer_candidates"):
        assert f"`{field}`" in skill, field
    # The one exception to "never remove `attended`" is written where the never is.
    assert "except `attended` on a ticket that carries an agent's question" in skill
    for words in ("**Decisions waiting for you**", "**Yours this week**", "**Answered**",
                  "No decisions waiting", "**To think about**", "**To approve**",
                  "**Recommend:**", "**What it is:**", "**Why:**", "What you would learn",
                  '`"think"`', '`"approve"`', "**Decided for you**"):
        assert words in skill, words


# --- pull requests that collide with main (HIR-305) ----------------------------------------

def collided(pr=186, **over):
    base = {"pr": pr, "ticket": f"HIR-{pr}", "labels": ["autopilot"], "pr_labels": [],
            "rules": False, "live": False}
    base.update(over)
    return base


def repair_line(pr, result):
    return f"- repair #{pr} (HIR-{pr}) | collided with main | result: {result} | spend: €0.00"


def repairs(items, log=(), **kw):
    return run([], log, collided=items, **kw)["repairs"]


def test_a_collided_pull_request_gets_a_repair_and_then_a_review():
    out = repairs([collided()])
    assert out["skipped"] == []
    assert out["start"] == [{"pr": 186, "ticket": "HIR-186", "review": True, "why": "collides with main"}]


def test_a_run_that_did_not_look_for_collisions_gets_no_answer_about_them():
    assert "repairs" not in run([ticket(1)])
    assert run([ticket(1)], collided=[])["repairs"] == {"start": [], "skipped": []}


def test_one_failed_repair_is_tried_again_two_are_mondays():
    once = [{"date": "2026-11-11", "body": repair_line(186, "failed")}]
    twice = once + [{"date": "2026-11-12", "body": repair_line(186, "failed")}]
    assert [r["pr"] for r in repairs([collided()], once)["start"]] == [186]
    out = repairs([collided(), collided(190)], twice)
    assert [r["pr"] for r in out["start"]] == [190]  # another pull request's failures are its own
    assert "failed twice" in out["skipped"][0]["why"]


@pytest.mark.parametrize("result", ["merged", "merging", "repaired", "waiting", "not-started", "running"])
def test_only_failed_repairs_count(result):
    log = [{"date": "2026-11-11", "body": repair_line(186, result) + "\n" + repair_line(186, result)}]
    assert len(repairs([collided()], log)["start"]) == 1


def test_a_failed_repair_is_not_a_failed_ticket_and_a_failed_ticket_is_not_a_failed_repair():
    two_repairs = [{"date": "2026-11-11", "body": repair_line(7, "failed") + "\n" + repair_line(7, "failed")}]
    assert ids(run([ticket(7)], two_repairs)["picked"]) == ["HIR-7"]
    assert lp.ran_between(two_repairs, "2026-11-01", "2026-11-30") == 0
    two_tries = [{"date": "2026-11-11", "body": line("HIR-7", "failed") + "\n" + line("HIR-7", "failed")}]
    assert len(repairs([collided(7)], two_tries)["start"]) == 1


@pytest.mark.parametrize("label", ["hands-on", "parked", "Hands-On"])
def test_chandlers_own_tickets_are_never_repaired(label):
    out = repairs([collided(labels=[label], pr_labels=["needs-chandler"])])
    assert out["start"] == []
    assert "Chandler's" in out["skipped"][0]["why"]


def test_an_attended_ticket_he_is_working_in_is_left_alone():
    out = repairs([collided(labels=["attended"])])
    assert out["start"] == []
    assert "he is working in it" in out["skipped"][0]["why"]


@pytest.mark.parametrize("over", [{"pr_labels": ["needs-chandler"]}, {"rules": True},
                                  {"pr_labels": ["Needs-Chandler"], "labels": ["attended"]},
                                  {"rules": True, "labels": ["attended"]}])
def test_a_pull_request_waiting_for_chandler_is_repaired_but_not_reviewed(over):
    out = repairs([collided(**over)])
    assert [(r["pr"], r["review"]) for r in out["start"]] == [(186, False)]
    assert "left for him" in out["start"][0]["why"]


def test_a_pull_request_a_run_may_be_working_on_waits_for_the_next_run():
    live = collided()
    live["live"] = True
    unknown = collided(190)
    del unknown["live"]  # nobody looked: in doubt, a run may be on it
    out = repairs([live, unknown])
    assert out["start"] == []
    assert all("next run" in s["why"] for s in out["skipped"])


def test_a_pull_request_with_no_ticket_is_not_repaired():
    out = repairs([collided(ticket=None)])
    assert out["start"] == [] and "no ticket" in out["skipped"][0]["why"]


def test_nothing_is_repaired_when_the_run_is_stopped():
    assert repairs([collided()], cap=0)["start"] == []
    limit = [{"date": TODAY, "body": "Usage limit: reached"}]
    out = repairs([collided()], limit)
    assert out["start"] == [] and "usage limit" in out["skipped"][0]["why"]


def test_a_red_check_does_not_hold_a_repair_back():
    assert len(repairs([collided()], red=["the main branch's checks"])["start"]) == 1


def test_cli_passes_the_collided_pull_requests_on(tmp_path, capsys):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({"today": TODAY, "decisions_waiting": 0, "red": [], "log": [],
                                 "tickets": [], "collided": [collided()]}))
    assert lp.main([str(state)]) == 0
    assert json.loads(capsys.readouterr().out)["repairs"]["start"][0]["pr"] == 186


def test_the_rule_files_carry_the_repair_of_a_collided_pull_request():
    """The script's answer is only a limit if the lead agent hands it the collided pull
    requests and starts what it says; the repair is only safe if the worker's rules send
    anything but add-only prose to the senior agent."""
    def words(*parts):
        return " ".join(ROOT.joinpath(*parts).read_text().split())

    lead = words(".claude", "skills", "lead-agent", "SKILL.md")
    for field in ("collided", "pr_labels", "rules", "live", "repairs", "start", "review"):
        assert f"`{field}`" in lead, field
    assert "/work-issue HIR-n repair" in lead
    assert "- repair #<n> (HIR-n) |" in lead
    work = words(".claude", "skills", "work-issue", "SKILL.md")
    assert "## Repairing a collided pull request" in (ROOT / ".claude/skills/work-issue/SKILL.md").read_text()
    for phrase in ("scripts/collision.py --apply", "`for_senior`", "`senior` agent",
                   "**To approve**", "git merge --abort", "decisions/"):
        assert phrase in work, phrase
    assert "Repairing a collided pull request" in words(".claude", "agents", "reviewer.md")
    assert "Repairing a collided pull request" in words("AGENTS.md")


# --- pull requests sent back and then fixed (HIR-358) --------------------------------------

SENT = "2026-11-17T05:57:00Z"      # the reviewer sent it back
BEFORE = "2026-11-17T05:40:00Z"    # the author's last commit, older than that
AFTER = "2026-11-17T06:04:00Z"     # something the author did seven minutes later


def sent_back(pr=196, **over):
    base = {"pr": pr, "ticket": f"HIR-{pr}", "labels": ["autopilot"], "pr_labels": ["sent-back"],
            "rules": False, "live": False, "sent_back_at": SENT, "last_commit_at": BEFORE,
            "repair_at": None}
    base.update(over)
    return base


def rereviews(items, log=(), **kw):
    return run([], log, sent_back=items, **kw)["rereviews"]


def test_a_pull_request_fixed_after_it_was_sent_back_gets_a_fresh_reviewer():
    out = rereviews([sent_back(last_commit_at=AFTER)])
    assert out["skipped"] == []
    assert out["start"] == [{"pr": 196, "ticket": "HIR-196", "why": "sent back, then changed by a new commit"}]


def test_a_pull_request_sent_back_with_nothing_new_is_still_its_authors():
    out = rereviews([sent_back(), sent_back(197, last_commit_at=SENT)])
    assert out["start"] == []
    assert [s["pr"] for s in out["skipped"]] == [196, 197]
    assert all("nothing new since it was sent back" in s["why"] for s in out["skipped"])


def test_a_repair_comment_after_the_send_back_counts_as_a_fix():
    """The case that sat for two days: sent back only for a collision, repaired at once."""
    out = rereviews([sent_back(repair_at=AFTER), sent_back(197, repair_at=BEFORE)])
    assert out["start"] == [{"pr": 196, "ticket": "HIR-196",
                             "why": "sent back, then repaired after a collision with main"}]
    assert [s["pr"] for s in out["skipped"]] == [197]


def test_a_second_send_back_is_timed_from_itself_not_from_the_first_fix():
    """The label stays on, so the run hands over the newest send-back; the fix that
    answered the first one is older than it and earns no third review."""
    again = "2026-11-18T09:00:00Z"
    assert rereviews([sent_back(sent_back_at=again, last_commit_at=AFTER)])["start"] == []
    assert len(rereviews([sent_back(sent_back_at=again, last_commit_at="2026-11-18T09:30:00Z")])["start"]) == 1


def test_times_in_different_zones_are_compared_as_moments():
    # 07:10 in Berlin is 06:10 UTC, after a send-back at 05:57 UTC.
    # 06:30 in Berlin is 05:30 UTC, before it, though "06:30" sorts after "05:57" as text.
    assert len(rereviews([sent_back(last_commit_at="2026-11-17T07:10:00+01:00")])["start"]) == 1
    assert rereviews([sent_back(last_commit_at="2026-11-17T06:30:00+01:00")])["start"] == []


@pytest.mark.parametrize("when", [None, "", "yesterday"])
def test_a_send_back_whose_time_cannot_be_read_is_not_reviewed(when):
    out = rereviews([sent_back(sent_back_at=when, last_commit_at=AFTER)])
    assert out["start"] == []
    assert "cannot be read" in out["skipped"][0]["why"]


@pytest.mark.parametrize("over", [{"pr_labels": ["sent-back", "needs-chandler"]}, {"rules": True}])
def test_a_fixed_pull_request_waiting_for_chandler_is_left_for_him(over):
    out = rereviews([sent_back(last_commit_at=AFTER, **over)])
    assert out["start"] == []
    assert "waiting for Chandler" in out["skipped"][0]["why"]


@pytest.mark.parametrize("label", ["attended", "hands-on", "parked"])
def test_a_fixed_pull_request_on_chandlers_own_ticket_is_left_alone(label):
    out = rereviews([sent_back(last_commit_at=AFTER, labels=[label])])
    assert out["start"] == []
    assert label in out["skipped"][0]["why"]


def test_a_fixed_pull_request_that_already_passed_review_is_not_reviewed_again():
    out = rereviews([sent_back(last_commit_at=AFTER, pr_labels=["sent-back", "review-passed"])])
    assert out["start"] == []


def test_a_fixed_pull_request_a_run_may_be_working_on_waits_for_the_next_run():
    live = sent_back(last_commit_at=AFTER, live=True)
    unknown = sent_back(197, last_commit_at=AFTER)
    del unknown["live"]
    out = rereviews([live, unknown])
    assert out["start"] == []
    assert all("may still be working on it" in s["why"] for s in out["skipped"])


def test_a_fixed_pull_request_with_no_ticket_is_not_reviewed():
    out = rereviews([sent_back(last_commit_at=AFTER, ticket=None)])
    assert out["start"] == [] and "no ticket" in out["skipped"][0]["why"]


def test_no_second_review_when_the_run_is_stopped_but_a_red_check_does_not_hold_one_back():
    fixed = sent_back(last_commit_at=AFTER)
    assert rereviews([fixed], cap=0)["start"] == []
    assert len(rereviews([fixed], red=["the main branch's checks"])["start"]) == 1


def test_in_fixes_only_mode_only_a_fix_gets_its_second_review():
    on = {"from": "2026-11-01", "until": None}
    out = rereviews([sent_back(last_commit_at=AFTER),
                     sent_back(197, last_commit_at=AFTER, labels=["autopilot", "Bug"])], fixes_only=on)
    assert [s["pr"] for s in out["start"]] == [197]
    assert "fixes-only mode" in out["skipped"][0]["why"]


def test_a_run_that_did_not_look_for_sent_back_pull_requests_gets_no_answer_about_them():
    assert "rereviews" not in run([ticket(1)])
    assert run([ticket(1)], sent_back=[])["rereviews"] == {"start": [], "skipped": []}


def test_cli_passes_the_sent_back_pull_requests_on(tmp_path, capsys):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({"today": TODAY, "decisions_waiting": 0, "red": [], "log": [],
                                 "tickets": [], "sent_back": [sent_back(last_commit_at=AFTER)]}))
    assert lp.main([str(state)]) == 0
    assert json.loads(capsys.readouterr().out)["rereviews"]["start"][0]["pr"] == 196


def test_the_lead_agents_procedure_hands_over_the_sent_back_pull_requests_and_logs_them():
    """The script's answer changes nothing unless the lead agent gathers the three times,
    starts the reviewer, stops sending a repaired pull request back to Todo, and says so
    under "Unstuck"."""
    text = (ROOT / ".claude" / "skills" / "lead-agent" / "SKILL.md").read_text()
    lead = " ".join(text.split())
    for field in ("sent_back", "sent_back_at", "last_commit_at", "repair_at", "rereviews"):
        assert f"`{field}`" in lead, field
    assert "### A second review for a pull request fixed after it was sent back" in lead
    assert 'List each under "Unstuck" in the log' in lead
    assert "returned to Todo for the fixes" not in lead
    unstuck = [row for row in text.splitlines() if row.startswith("Unstuck:")]
    assert len(unstuck) == 1 and "fixed after it was sent back" in unstuck[0]
