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

    def __init__(self, states, files=CODE):
        self.states = list(states)
        self.files = files
        self.acts = []

    def __call__(self, *args):
        if args[0] == "api" and args[1].endswith("/files"):
            return "\n".join(self.files)
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


def test_main_with_no_pr_for_the_branch_is_a_quiet_no(monkeypatch, capsys):
    monkeypatch.setattr(mr, "_gh", lambda *a: "")
    assert mr.main(["--repo", "o/r", "--branch", "some-branch"]) == 0
    assert "Nothing to do" in capsys.readouterr().out
