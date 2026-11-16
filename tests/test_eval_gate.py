"""eval_gate: does a PR that changes the extractor or the skill list bring a dev eval result.

`decide` is pure — (changed files, version-check answer) -> pass/fail — so none of this
needs git, a network or a model. The end-to-end cases drive `main` through a temporary
file, which is how CI calls it, with the version check replaced by a fixed answer.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("eval_gate", ROOT / "scripts" / "eval_gate.py")
eg = importlib.util.module_from_spec(spec)
sys.modules["eval_gate"] = eg
spec.loader.exec_module(eg)

RESULT = "evals/results/20261112T101500Z_dev_x2-abc123/summary.json"
EXTRACTOR = ("modified", "app/extract.py")
SKILLS = ("modified", "taxonomy/skills.json")


# --- the four branches the ticket names ----------------------------------------------

@pytest.mark.parametrize("touched", [EXTRACTOR, SKILLS])
def test_gated_file_with_a_new_dev_result_passes(touched):
    ok, message = eg.decide([touched, ("added", RESULT)], version_match=False)
    assert ok
    assert RESULT in message


@pytest.mark.parametrize("touched", [EXTRACTOR, SKILLS])
def test_gated_file_with_no_result_and_a_different_extractor_fails(touched):
    ok, message = eg.decide([touched, ("modified", "README.md")], version_match=False)
    assert not ok
    assert touched[1] in message


def test_gated_file_with_no_result_passes_when_the_baseline_already_measured_it():
    ok, message = eg.decide([EXTRACTOR], version_match=True)
    assert ok
    assert "MATCH" in message


@pytest.mark.parametrize("version_match", [True, False])
def test_nothing_relevant_touched_passes_whatever_the_version_check_says(version_match):
    changes = [("modified", "app/queries.py"), ("added", "tests/test_queries.py")]
    ok, _ = eg.decide(changes, version_match=version_match)
    assert ok


# --- what counts as touching, and as a new result ------------------------------------

@pytest.mark.parametrize("status", ["added", "modified", "removed", "renamed", "renamed-from"])
def test_any_kind_of_change_to_a_gated_file_trips_the_gate(status):
    assert not eg.decide([(status, "app/extract.py")], version_match=False)[0]


@pytest.mark.parametrize(
    "path",
    ["app/extract_helpers.py", "tests/app/extract.py", "taxonomy/README.md", "skills.json"],
)
def test_lookalike_paths_do_not_trip_the_gate(path):
    assert eg.gated_paths([("modified", path)]) == []


@pytest.mark.parametrize(
    "change",
    [
        ("modified", RESULT),                                              # an old run edited
        ("renamed", RESULT),                                               # an old run moved
        ("added", "evals/results/20261112T101500Z_heldout_x2-abc123/summary.json"),
        ("added", "evals/results/20261112T101500Z_dev_x2-abc123/summary.md"),
        ("added", "evals/results/20261112T101500Z_dev_x2-abc123/predictions.jsonl"),
        ("added", "docs/evals/results/x_dev_y/summary.json"),
    ],
)
def test_only_a_newly_added_dev_summary_satisfies_the_gate(change):
    assert not eg.decide([EXTRACTOR, change], version_match=False)[0]


def test_failure_message_names_the_rule_and_the_two_commands():
    _, message = eg.decide([EXTRACTOR, SKILLS], version_match=False)
    assert "The eval gate" in message
    assert "uv run python scripts/run_eval.py" in message
    assert "uv run python scripts/eval_table.py <run_id>" in message
    assert "app/extract.py" in message and "taxonomy/skills.json" in message


# --- when the version check is consulted ---------------------------------------------

def test_version_check_is_needed_only_when_it_would_decide():
    assert eg.needs_version_check([EXTRACTOR])
    assert not eg.needs_version_check([EXTRACTOR, ("added", RESULT)])
    assert not eg.needs_version_check([("modified", "README.md")])


def test_parse_changes_reads_status_and_path_and_skips_blank_lines():
    text = "modified\tapp/extract.py\n\nadded\t" + RESULT + "\n"
    assert eg.parse_changes(text) == [EXTRACTOR, ("added", RESULT)]


# --- end to end, as CI calls it ------------------------------------------------------

def _run(tmp_path, monkeypatch, lines, match):
    calls = []

    def fake():
        calls.append(1)
        return match

    monkeypatch.setattr(eg, "baseline_measured_this_extractor", fake)
    f = tmp_path / "changes.txt"
    f.write_text("\n".join(lines) + "\n")
    return eg.main(["--changes-file", str(f)]), calls


def test_main_exits_nonzero_and_explains_when_the_eval_is_missing(tmp_path, monkeypatch, capsys):
    code, _ = _run(tmp_path, monkeypatch, ["modified\ttaxonomy/skills.json"], match=False)
    assert code == 1
    assert "scripts/run_eval.py" in capsys.readouterr().out


def test_main_passes_on_match(tmp_path, monkeypatch):
    code, calls = _run(tmp_path, monkeypatch, ["modified\tapp/extract.py"], match=True)
    assert code == 0
    assert calls == [1]


def test_main_passes_with_a_result_and_never_asks_for_the_version(tmp_path, monkeypatch):
    lines = ["modified\tapp/extract.py", f"added\t{RESULT}"]
    code, calls = _run(tmp_path, monkeypatch, lines, match=False)
    assert code == 0
    assert calls == []


def test_main_passes_an_unrelated_pr_without_the_version_check(tmp_path, monkeypatch):
    code, calls = _run(tmp_path, monkeypatch, ["modified\tweb/src/App.jsx"], match=False)
    assert code == 0
    assert calls == []


def test_the_real_version_check_is_eval_tables_own(monkeypatch):
    """The exemption is not reimplemented here: it is whatever eval_table answers."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import eval_table  # noqa: PLC0415

    monkeypatch.setattr(eval_table, "version_check", lambda: ("x2-abc", {"meta": {}}, True))
    assert eg.baseline_measured_this_extractor() is True
    monkeypatch.setattr(eval_table, "version_check", lambda: ("x2-abc", None, False))
    assert eg.baseline_measured_this_extractor() is False
