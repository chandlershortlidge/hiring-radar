"""rules_gate: which files trip the gate, and whether the PR carries the block.

Pure functions, so none of this needs git, a network or a model. The end-to-end cases drive
`main` through two temporary files, which is exactly how CI calls it.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("rules_gate", ROOT / "scripts" / "rules_gate.py")
rg = importlib.util.module_from_spec(spec)
sys.modules["rules_gate"] = rg
spec.loader.exec_module(rg)


BLOCK = """## Rule changes

Changes were made to .claude/agents/skills:

* The reviewer now stops any PR that edits the agents' own instructions.
* A new automatic check fails such a PR when this list is missing.

Did you authorize these?
"""


# --- which paths trip the gate -------------------------------------------------------

@pytest.mark.parametrize(
    "path",
    [
        ".claude/agents/reviewer.md",
        ".claude/skills/work-issue/SKILL.md",
        ".claude/settings.json",
        "AGENTS.md",
        ".github/pull_request_template.md",
        ".github/workflows/ci.yml",
        ".github/workflows/rules-gate.yml",
        "scripts/rules_gate.py",
    ],
)
def test_the_watched_paths_trip_the_gate(path):
    assert rg.is_rule_path(path)


@pytest.mark.parametrize(
    "path",
    [
        "app/extract.py",
        "DECISIONS.md",
        "tests/test_rules_gate.py",
        "web/src/format.js",
        ".github/dependabot.yml",
        "AGENTS.md.bak",
        "docs/.claude/notes.md",
        "",
    ],
)
def test_ordinary_paths_do_not(path):
    assert not rg.is_rule_path(path)


def test_matched_paths_sorts_and_dedupes():
    paths = ["app/geo.py", "AGENTS.md", ".claude/agents/decider.md", "AGENTS.md", ""]
    assert rg.matched_paths(paths) == [".claude/agents/decider.md", "AGENTS.md"]


# --- is the block there --------------------------------------------------------------

def test_the_block_is_recognized():
    assert rg.block_problem(BLOCK) is None


def test_a_quoted_block_is_recognized_too():
    quoted = "\n".join("> " + line for line in BLOCK.splitlines())
    assert rg.block_problem(quoted) is None


def test_a_missing_headline_is_named():
    problem = rg.block_problem("## Testing\n\n695 tests pass.\n")
    assert "Changes were made to" in problem


def test_a_headline_with_no_bullets_fails():
    body = "Changes were made to .claude/agents/skills:\n\nDid you authorize these?\n"
    assert "no bullet list" in rg.block_problem(body)


def test_the_question_must_follow_the_bullets():
    body = (
        "Did you authorize these?\n\n"
        "Changes were made to .claude/agents/skills:\n\n"
        "* the reviewer's instructions\n"
    )
    assert "does not follow the bullets" in rg.block_problem(body)


def test_an_empty_body_is_a_missing_block():
    assert rg.block_problem("") is not None
    assert rg.block_problem(None) is not None


# --- the gate's verdict --------------------------------------------------------------

def test_a_pr_that_touches_no_rule_file_passes_without_a_block():
    ok, message = rg.report(["app/extract.py", "tests/test_extract.py"], "")
    assert ok
    assert "Nothing to ask" in message


def test_a_rules_pr_without_the_block_is_stopped():
    ok, message = rg.report([".claude/agents/reviewer.md", "app/geo.py"], "## Testing\n\nfine\n")
    assert not ok
    assert ".claude/agents/reviewer.md" in message
    assert "app/geo.py" not in message
    assert "Did you authorize these?" in message


def test_a_rules_pr_with_the_block_passes():
    ok, message = rg.report(["AGENTS.md"], BLOCK)
    assert ok
    assert "AGENTS.md" in message


def test_the_gate_stops_a_pr_that_edits_the_gate_itself():
    """The backstop's point: switching the reviewer off does not switch the gate off."""
    ok, _ = rg.report([".claude/agents/reviewer.md", ".github/workflows/rules-gate.yml"], "")
    assert not ok


# --- the CLI, as CI calls it ---------------------------------------------------------

def _run(tmp_path, paths, body):
    paths_file = tmp_path / "changed.txt"
    body_file = tmp_path / "body.md"
    paths_file.write_text("\n".join(paths), encoding="utf-8")
    body_file.write_text(body, encoding="utf-8")
    return rg.main(["--paths-file", str(paths_file), "--body-file", str(body_file)])


def test_cli_exits_zero_on_an_ordinary_pr(tmp_path, capsys):
    assert _run(tmp_path, ["app/geo.py"], "") == 0
    assert "Nothing to ask" in capsys.readouterr().out


def test_cli_exits_one_on_a_rules_pr_with_no_block(tmp_path, capsys):
    assert _run(tmp_path, ["AGENTS.md"], "## Testing\n\nfine\n") == 1
    assert "cannot merge on its own" in capsys.readouterr().out


def test_cli_exits_zero_once_the_block_is_there(tmp_path, capsys):
    assert _run(tmp_path, ["AGENTS.md", ".claude/skills/work-issue/SKILL.md"], BLOCK) == 0
    assert "asks whether that was authorized" in capsys.readouterr().out
