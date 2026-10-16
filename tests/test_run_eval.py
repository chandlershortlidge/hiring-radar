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


def test_full_run_writes_results_with_mocked_model(monkeypatch, tmp_path):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(run_eval, "ROOT", tmp_path)
    (tmp_path / "evals/goldens").mkdir(parents=True)
    (tmp_path / "evals/goldens/g1.json").write_text(json.dumps({
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
