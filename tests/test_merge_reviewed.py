"""merge_reviewed: GitHub merges a reviewed PR only when every condition holds (HIR-262).

`decide` is pure. `run` is driven with a fake `gh`, so nothing here touches GitHub.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("merge_reviewed", ROOT / "scripts" / "merge_reviewed.py")
mr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mr)

CODE = ["app/ingest.py", "tests/test_ingest.py"]


def pr(labels=("review-passed",), state="open", draft=False, mergeable_state="clean"):
    return {
        "number": 7,
        "state": state,
        "draft": draft,
        "mergeable_state": mergeable_state,
        "labels": [{"name": n} for n in labels],
        "head": {"sha": "abc123"},
    }


def test_a_reviewed_clean_pr_merges():
    assert mr.decide(pr(), CODE)[0] is True


@pytest.mark.parametrize(
    "kwargs, files, why",
    [
        ({"labels": ()}, CODE, "review-passed"),
        ({"labels": ("review-passed", "needs-chandler")}, CODE, "needs-chandler"),
        ({}, CODE + ["AGENTS.md"], "own rules"),
        ({}, CODE + [".claude/agents/reviewer.md"], "own rules"),
        ({}, ["scripts/merge_reviewed.py"], "own rules"),
        ({"mergeable_state": "behind"}, CODE, "behind"),
        ({"mergeable_state": "blocked"}, CODE, "blocked"),
        ({"mergeable_state": "unstable"}, CODE, "unstable"),
        ({"mergeable_state": "dirty"}, CODE, "dirty"),
        ({"state": "closed"}, CODE, "not open"),
        ({"draft": True}, CODE, "draft"),
    ],
)
def test_any_failed_condition_stops_the_merge(kwargs, files, why):
    merge, reason = mr.decide(pr(**kwargs), files)
    assert merge is False
    assert why in reason


def test_a_labelling_guide_pr_never_merges_here_even_when_passed():
    # Backstop for the reviewer: the guide decides every score, so it is Chandler's.
    merge, reason = mr.decide(pr(), ["evals/LABELING.md"])
    assert merge is False
    assert "labelling guide" in reason


class FakeGh:
    """Answers `gh` calls from a script of PR states; records the commands that act."""

    def __init__(self, states, files=CODE, running=((),), finished=(), status=None):
        self.states = list(states)
        self.files = files
        self.running = list(running)  # per look: names of the checks not finished yet
        self.finished = finished  # every look: (name, conclusion) of the finished checks
        self.status = status or {"state": "pending", "total_count": 0}  # no commit statuses
        self.acts = []

    def __call__(self, *args):
        if args[0] == "api" and args[1].endswith("/files"):
            return "\n".join(self.files)
        if args[0] == "api" and "/check-runs" in args[1]:
            names = self.running.pop(0) if len(self.running) > 1 else self.running[0]
            rows = [f"{name}\tin_progress\t" for name in names]
            rows += [f"{name}\tcompleted\t{conclusion}" for name, conclusion in self.finished]
            return "\n".join(rows)
        if args[0] == "api" and args[1].endswith("/status"):
            return json.dumps(self.status)
        if args[0] == "api":
            state = self.states.pop(0) if len(self.states) > 1 else self.states[0]
            return json.dumps(state)
        self.acts.append(args)
        return ""


def test_run_merges_the_head_it_saw_then_starts_the_deploy(monkeypatch):
    gh = FakeGh([pr()])
    monkeypatch.setattr(mr, "_gh", gh)
    assert mr.run("o/r", 7, sleep=lambda s: None) is True
    merge, deploy = gh.acts
    assert merge[:2] == ("pr", "merge") and "--match-head-commit" in merge and "abc123" in merge
    assert "--auto" not in merge
    assert deploy[:2] == ("workflow", "run") and "ci.yml" in deploy and "main" in deploy


def test_run_asks_again_while_github_is_still_computing(monkeypatch):
    gh = FakeGh([pr(mergeable_state="unknown"), pr(mergeable_state="unknown"), pr()])
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is True
    assert len(waits) == 2


def test_run_does_nothing_when_a_condition_fails(monkeypatch):
    gh = FakeGh([pr(labels=("review-passed", "needs-chandler"))])
    monkeypatch.setattr(mr, "_gh", gh)
    assert mr.run("o/r", 7, sleep=lambda s: None) is False
    assert gh.acts == []


SHOTS = ("Before/after screenshots",)


def test_run_waits_for_a_check_still_running_then_merges(monkeypatch):
    # HIR-275: the tests finished, the screenshots check had not. The merger looked once,
    # read 'unstable', declined, and nothing made it look again (PR #158, 12 Nov).
    gh = FakeGh(
        [pr(mergeable_state="unstable"), pr(mergeable_state="unstable"), pr()],
        running=[SHOTS, SHOTS],
    )
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is True
    assert waits == [mr.PENDING_WAIT_S, mr.PENDING_WAIT_S]
    assert gh.acts[0][:2] == ("pr", "merge")


def test_run_gives_github_a_moment_after_the_last_check_finishes(monkeypatch):
    # The check is done but the PR still reads 'unstable' for one more look.
    gh = FakeGh(
        [pr(mergeable_state="unstable"), pr(mergeable_state="unstable"), pr()],
        running=[SHOTS, ()],
    )
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is True
    assert waits == [mr.PENDING_WAIT_S, mr.UNKNOWN_WAIT_S]


def test_run_does_not_merge_when_the_check_it_waited_for_fails(monkeypatch):
    # A failed check leaves the PR 'unstable' with nothing running: still a no.
    gh = FakeGh([pr(mergeable_state="unstable")], running=[SHOTS, ()])
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is False
    assert gh.acts == []
    assert waits == [mr.PENDING_WAIT_S] + [mr.UNKNOWN_WAIT_S] * mr.SETTLE_RETRIES


def test_run_stops_waiting_for_a_check_that_never_finishes(monkeypatch):
    gh = FakeGh([pr(mergeable_state="unstable")], running=[SHOTS])
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is False
    assert gh.acts == []
    assert sum(waits) == mr.PENDING_MAX_WAIT_S


@pytest.mark.parametrize(
    "kwargs, files",
    [
        ({"mergeable_state": "blocked"}, CODE),  # a required check failed or is running
        ({"mergeable_state": "behind"}, CODE),
        ({"mergeable_state": "unstable", "labels": ()}, CODE),  # not reviewed
        ({"mergeable_state": "unstable", "labels": ("review-passed", "needs-chandler")}, CODE),
        ({"mergeable_state": "unstable"}, CODE + ["AGENTS.md"]),  # a rule file
    ],
)
def test_run_waits_only_when_a_running_check_is_all_that_is_missing(monkeypatch, kwargs, files):
    gh = FakeGh([pr(**kwargs)], files=files, running=[SHOTS])
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is False
    assert waits == [] and gh.acts == []


def test_run_stops_waiting_when_the_pr_is_stopped_meanwhile(monkeypatch):
    # Adding 'needs-chandler' while the merger waits is still how a person stops it.
    gh = FakeGh(
        [pr(mergeable_state="unstable"), pr(labels=("review-passed", "needs-chandler"))],
        running=[SHOTS],
    )
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is False
    assert waits == [mr.PENDING_WAIT_S] and gh.acts == []


OWN = (mr.OWN_CHECK,)
TESTS_GREEN = (("Python tests", "success"), ("Rules gate", "success"), ("Deploy and watch", "skipped"))


def test_the_own_check_name_is_the_job_name_in_the_workflow():
    workflow = (ROOT / ".github" / "workflows" / "merge-reviewed.yml").read_text()
    assert f"name: {mr.OWN_CHECK}\n" in workflow


def test_run_merges_when_its_own_check_is_the_only_one_still_running(monkeypatch):
    # HIR-293: the label started the merger, so its own run was a check on the PR. It
    # waited on itself for the full 15 minutes, GitHub said 'unstable' throughout, and a
    # reviewed, green PR stayed open (PR #170, 13 Nov).
    gh = FakeGh([pr(mergeable_state="unstable")], running=[OWN], finished=TESTS_GREEN)
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is True
    assert waits == []
    merge = gh.acts[0]
    assert merge[:2] == ("pr", "merge") and "--match-head-commit" in merge and "abc123" in merge


def test_run_waits_for_the_other_check_but_not_for_its_own(monkeypatch):
    # Screenshots still running next to the merger's own check: wait for the screenshots,
    # then merge although the PR still reads 'unstable' (its own check is why).
    gh = FakeGh(
        [pr(mergeable_state="unstable")],
        running=[OWN + SHOTS, OWN],
        finished=TESTS_GREEN,
    )
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is True
    assert waits == [mr.PENDING_WAIT_S]


def test_run_does_not_merge_past_a_failed_check_because_its_own_is_running(monkeypatch):
    gh = FakeGh(
        [pr(mergeable_state="unstable")],
        running=[OWN],
        finished=TESTS_GREEN + (("Before/after screenshots", "failure"),),
    )
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is False
    assert gh.acts == []
    assert waits == [mr.UNKNOWN_WAIT_S] * mr.SETTLE_RETRIES  # never the 15 minutes


@pytest.mark.parametrize("state", ["pending", "failure"])
def test_run_does_not_merge_past_a_commit_status_that_is_not_green(monkeypatch, state):
    # The older kind of check, which the check list does not show.
    gh = FakeGh(
        [pr(mergeable_state="unstable")],
        running=[OWN],
        finished=TESTS_GREEN,
        status={"state": state, "total_count": 1},
    )
    monkeypatch.setattr(mr, "_gh", gh)
    assert mr.run("o/r", 7, sleep=lambda s: None) is False
    assert gh.acts == []


def test_run_merges_with_its_own_check_running_when_the_commit_statuses_are_green(monkeypatch):
    gh = FakeGh(
        [pr(mergeable_state="unstable")],
        running=[OWN],
        finished=TESTS_GREEN,
        status={"state": "success", "total_count": 1},
    )
    monkeypatch.setattr(mr, "_gh", gh)
    assert mr.run("o/r", 7, sleep=lambda s: None) is True


def test_run_ignores_an_earlier_merger_run_that_failed(monkeypatch):
    # A merger run that hit a GitHub error leaves a red check of its own name behind. That
    # is not a verdict on the PR, and must not keep the next run from merging it.
    gh = FakeGh(
        [pr(mergeable_state="unstable")],
        finished=TESTS_GREEN + ((mr.OWN_CHECK, "failure"),),
    )
    monkeypatch.setattr(mr, "_gh", gh)
    assert mr.run("o/r", 7, sleep=lambda s: None) is True


@pytest.mark.parametrize(
    "kwargs, files",
    [
        ({"mergeable_state": "blocked"}, CODE),  # a required check failed or is running
        ({"mergeable_state": "behind"}, CODE),
        ({"mergeable_state": "dirty"}, CODE),
        ({"mergeable_state": "unstable", "labels": ()}, CODE),
        ({"mergeable_state": "unstable", "labels": ("review-passed", "needs-chandler")}, CODE),
        ({"mergeable_state": "unstable"}, CODE + ["AGENTS.md"]),
        ({"mergeable_state": "unstable"}, ["evals/LABELING.md"]),
    ],
)
def test_its_own_check_running_excuses_nothing_else(monkeypatch, kwargs, files):
    gh = FakeGh([pr(**kwargs)], files=files, running=[OWN], finished=TESTS_GREEN)
    monkeypatch.setattr(mr, "_gh", gh)
    waits = []
    assert mr.run("o/r", 7, sleep=waits.append) is False
    assert waits == [] and gh.acts == []


def test_decide_reads_unstable_as_clean_only_when_told_its_own_check_is_why():
    assert mr.decide(pr(mergeable_state="unstable"), CODE)[0] is False
    assert mr.decide(pr(mergeable_state="unstable"), CODE, own_check_only=True)[0] is True
    assert mr.decide(pr(mergeable_state="blocked"), CODE, own_check_only=True)[0] is False
    assert mr.decide(pr(mergeable_state="behind"), CODE, own_check_only=True)[0] is False


def test_main_with_no_pr_for_the_branch_is_a_quiet_no(monkeypatch, capsys):
    monkeypatch.setattr(mr, "_gh", lambda *a: "")
    assert mr.main(["--repo", "o/r", "--branch", "some-branch"]) == 0
    assert "Nothing to do" in capsys.readouterr().out
