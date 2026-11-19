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
        "scripts/merge_reviewed.py",
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


# --- tests removed or switched off (HIR-332) -------------------------------------------
# Skip markers are built by concatenation so that editing this file never trips the
# gate's own skip detector.

SKIP_PY = "@pytest.mark." + "skip"
XFAIL_PY = "@pytest.mark." + "xfail"
SKIP_JS = "it." + "skip"


def f(filename, patch=None, status="modified", previous=None):
    d = {"filename": filename, "status": status}
    if patch is not None:
        d["patch"] = patch
    if previous:
        d["previous_filename"] = previous
    return d


@pytest.mark.parametrize("path", ["tests/test_dedup.py", "tests/sub/helpers.py", "web/src/profile.test.js",
                                  "web/e2e/before-after.spec.js", "app/x_test.py"])
def test_test_paths_are_recognized(path):
    assert rg.is_test_path(path)


@pytest.mark.parametrize("path", ["app/dedup.py", "web/src/profile.js", "scripts/rules_gate.py", "README.md"])
def test_non_test_paths_are_not(path):
    assert not rg.is_test_path(path)


def test_a_deleted_python_test_is_found():
    patch = "@@ -1,4 +1,1 @@\n-def test_blank_is_not_a_duplicate():\n-    assert x\n context"
    assert rg.removed_tests([f("tests/test_dedup.py", patch)]) == [
        "test removed: test_blank_is_not_a_duplicate (tests/test_dedup.py)"]


def test_a_deleted_js_test_is_found():
    patch = "-  it(\"keeps original order on a tie\", () => {\n-  });"
    out = rg.removed_tests([f("web/src/profile.test.js", patch)])
    assert out == ["test removed: keeps original order on a tie (web/src/profile.test.js)"]


def test_a_moved_test_is_not_a_removal():
    files = [f("tests/test_a.py", "-def test_moves():\n-    pass"),
             f("tests/test_b.py", "+def test_moves():\n+    pass")]
    assert rg.removed_tests(files) == []


def test_an_edited_test_body_is_not_a_removal():
    patch = " def test_kept():\n-    assert a == 1\n+    assert a == 2"
    assert rg.removed_tests([f("tests/test_x.py", patch)]) == []


def test_a_deleted_test_file_is_found():
    assert rg.removed_tests([f("tests/test_old.py", status="removed")]) == ["test file deleted: tests/test_old.py"]


def test_a_renamed_test_file_with_no_patch_is_fine():
    assert rg.removed_tests([f("tests/test_new.py", status="renamed", previous="tests/test_old.py")]) == []


@pytest.mark.parametrize("line", [SKIP_PY, XFAIL_PY + "(reason='flaky')", f"    {SKIP_JS}(\"x\", () => {{"])
def test_an_added_skip_is_found(line):
    out = rg.removed_tests([f("tests/test_x.py" if "pytest" in line else "web/src/a.test.js", "+" + line)])
    assert len(out) == 1 and "switched off" in out[0]


def test_a_removed_skip_is_fine():
    assert rg.removed_tests([f("tests/test_x.py", "-" + SKIP_PY)]) == []


def test_a_test_file_too_large_to_read_is_flagged():
    out = rg.removed_tests([f("tests/test_big.py", patch=None)])
    assert out and "too large" in out[0]


def test_non_test_files_are_ignored():
    assert rg.removed_tests([f("app/dedup.py", "-def test_like_name():")]) == []


def test_a_pr_that_removes_a_test_needs_the_block():
    files = [f("tests/test_dedup.py", "-def test_gone():\n-    pass")]
    ok, msg = rg.report(["tests/test_dedup.py"], "Just a fix.", files)
    assert not ok and "test removed: test_gone" in msg
    ok, _ = rg.report(["tests/test_dedup.py"], BLOCK, files)
    assert ok


def test_an_ordinary_pr_with_patches_still_passes():
    files = [f("app/dedup.py", "-x = 1\n+x = 2"), f("tests/test_dedup.py", "+def test_new():\n+    pass")]
    assert rg.report(["app/dedup.py", "tests/test_dedup.py"], "Fix.", files)[0]


def test_cli_reads_the_jsonl_file_list(tmp_path):
    import json
    jl = tmp_path / "files.jsonl"
    jl.write_text(json.dumps(f("tests/test_dedup.py", "-def test_gone():")) + "\n")
    body = tmp_path / "body.md"
    body.write_text("Fix.")
    assert rg.main(["--files-jsonl", str(jl), "--body-file", str(body)]) == 1
    body.write_text(BLOCK)
    assert rg.main(["--files-jsonl", str(jl), "--body-file", str(body)]) == 0
