import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import run_eval  # noqa: E402


def test_heldout_requires_explicit_flag(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    with pytest.raises(SystemExit, match="release points"):
        run_eval.main(["--split", "heldout"])


def test_missing_api_key_exits_before_any_call(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(run_eval, "make_client", lambda: pytest.fail("client should not be created"))
    with pytest.raises(SystemExit, match="ANTHROPIC_API_KEY"):
        run_eval.main([])


def _one_golden(tmp_path):
    (tmp_path / "evals/goldens").mkdir(parents=True)
    (tmp_path / "evals/goldens/golden_001.json").write_text(json.dumps({
        "id": "g1", "split": "dev", "source_sha256": "x", "job_description": "Python",
        "expected": [{"skill_id": "python", "requirement": "required", "raw_text": "Python"}]}))


def test_all_errors_prints_cause_and_writes_nothing(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(run_eval, "ROOT", tmp_path)
    _one_golden(tmp_path)

    def boom(**kw):
        raise RuntimeError("401 invalid x-api-key")

    monkeypatch.setattr(run_eval, "make_client", lambda: SimpleNamespace(messages=SimpleNamespace(create=boom)))
    with pytest.raises(SystemExit, match="Every Golden failed"):
        run_eval.main(["--repeats", "1", "--model", "m"])
    assert "401 invalid x-api-key" in capsys.readouterr().out
    assert not (tmp_path / "evals/results").exists()


def test_full_run_writes_results_with_mocked_model(monkeypatch, tmp_path):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(run_eval, "ROOT", tmp_path)
    (tmp_path / "evals/goldens").mkdir(parents=True)
    (tmp_path / "evals/goldens/golden_001.json").write_text(json.dumps({
        "id": "g1", "split": "dev", "source_sha256": "x", "job_description": "Python and LangChain",
        "expected": [{"skill_id": "python", "requirement": "required", "raw_text": "Python"},
                     {"skill_id": "langchain", "requirement": "required", "raw_text": "LangChain"}]}))

    tool = SimpleNamespace(type="tool_use", name="record_skills",
                           input={"skills": [{"skill_id": "python", "requirement": "required", "raw_text": "Python"}]})
    resp = SimpleNamespace(stop_reason="tool_use", content=[tool], usage=None)
    client = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: resp))
    monkeypatch.setattr(run_eval, "make_client", lambda: client)

    run_eval.main(["--repeats", "2", "--model", "m"])

    [out] = list((tmp_path / "evals/results").iterdir())
    summary = json.loads((out / "summary.json").read_text())
    assert summary["aggregate"]["recall"]["mean"] == pytest.approx(0.5)
    assert summary["aggregate"]["recall"]["n"] == 2
    assert len((out / "predictions.jsonl").read_text().splitlines()) == 2
    assert "Most-missed skills" in (out / "summary.md").read_text()


def _goldens_and_client(tmp_path):
    """One Golden whose extraction returns a skill the Golden does not list (an extra).

    Writes the Golden straight away: run_eval loads the Goldens before it builds a client,
    so creating them inside the make_client lambda would be too late.
    """
    (tmp_path / "evals/goldens").mkdir(parents=True)
    (tmp_path / "evals/goldens/golden_001.json").write_text(json.dumps({
        "id": "g1", "split": "dev", "source_sha256": "x",
        "job_description": "Requirements: Python. We run on Kubernetes.",
        "expected": [{"skill_id": "python", "requirement": "required", "raw_text": "Python"}]}))

    skills = SimpleNamespace(type="tool_use", name="record_skills", input={"skills": [
        {"skill_id": "python", "requirement": "required", "raw_text": "Python"},
        {"skill_id": "kubernetes", "requirement": "required", "raw_text": "Kubernetes"}]})
    verdicts = SimpleNamespace(type="tool_use", name="record_verdicts", input={"verdicts": [
        {"skill": "kubernetes", "verdict": "model_wrong", "reason": "only in the stack blurb"}]})

    def create(**kw):
        name = kw["tools"][0]["name"]
        block = verdicts if name == "record_verdicts" else skills
        return SimpleNamespace(stop_reason="tool_use", content=[block], usage=None)

    return SimpleNamespace(messages=SimpleNamespace(create=create))


def test_the_extras_judge_is_off_unless_asked_for(monkeypatch, tmp_path):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(run_eval, "ROOT", tmp_path)
    client = _goldens_and_client(tmp_path)
    monkeypatch.setattr(run_eval, "make_client", lambda: client)
    monkeypatch.setattr(run_eval.extras_judge, "judge_golden",
                        lambda *a, **kw: pytest.fail("the judge should not run"))

    run_eval.main(["--repeats", "1", "--model", "m"])

    [out] = list((tmp_path / "evals/results").iterdir())
    row = json.loads((out / "predictions.jsonl").read_text().splitlines()[0])
    assert "extras_verdicts" not in row


def test_the_extras_judge_writes_a_verdict_per_extra_on_run_1(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(run_eval, "ROOT", tmp_path)
    client = _goldens_and_client(tmp_path)
    monkeypatch.setattr(run_eval, "make_client", lambda: client)

    run_eval.main(["--repeats", "2", "--model", "m", "--extras-judge"])

    [out] = list((tmp_path / "evals/results").iterdir())
    rows = [json.loads(line) for line in (out / "predictions.jsonl").read_text().splitlines()]
    assert rows[0]["extras_verdicts"] == [
        {"skill_id": "kubernetes", "verdict": "model_wrong", "reason": "only in the stack blurb"}]
    assert "extras_verdicts" not in rows[1]          # run 2 is not judged twice
    summary = json.loads((out / "summary.json").read_text())
    assert summary["meta"]["extras_verdicts"]["model_wrong"] == 1
    assert "extras judge over run 1" in capsys.readouterr().out


def test_grounding_lands_in_the_committed_summary(monkeypatch, tmp_path):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(run_eval, "ROOT", tmp_path)
    client = _goldens_and_client(tmp_path)
    monkeypatch.setattr(run_eval, "make_client", lambda: client)

    run_eval.main(["--repeats", "1", "--model", "m"])

    [out] = list((tmp_path / "evals/results").iterdir())
    summary = json.loads((out / "summary.json").read_text())
    # Both quotes are in the posting, so nothing was invented.
    assert summary["aggregate"]["grounding_accuracy"]["mean"] == 1.0
    assert "grounding_accuracy" in (out / "summary.md").read_text()


def test_langsmith_is_not_touched_without_a_key(monkeypatch, tmp_path):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(run_eval, "ROOT", tmp_path)
    client = _goldens_and_client(tmp_path)
    monkeypatch.setattr(run_eval, "make_client", lambda: client)
    monkeypatch.setattr(run_eval.langsmith_eval, "start",
                        lambda *a, **kw: pytest.fail("start() must not be reached"))
    # conftest already unsets the key; this asserts run_eval asks before it connects.
    monkeypatch.setattr(run_eval.langsmith_eval, "enabled", lambda: False)
    run_eval.main(["--repeats", "1", "--model", "m", "--no-langsmith"])
    assert list((tmp_path / "evals/results").iterdir())
