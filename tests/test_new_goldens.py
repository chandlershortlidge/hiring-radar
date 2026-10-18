import importlib.util
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("new_goldens", ROOT / "scripts" / "new_goldens.py")
ng = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ng)
spec2 = importlib.util.spec_from_file_location("run_eval", ROOT / "scripts" / "run_eval.py")
re_ = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(re_)

DE = ("Wir suchen eine KI-Entwicklerin für unser Team in Berlin. Du arbeitest mit Python und der "
      "Cloud, bist für die Pipelines zuständig und bringst Erfahrung mit LLMs mit. ") * 4
EN = ("We are looking for an AI engineer for our team in Berlin. You work with Python and the "
      "cloud, own the pipelines and bring experience with LLMs. ") * 4


def test_is_german():
    assert ng.is_german(DE) and not ng.is_german(EN)
    assert not ng.is_german("Python, und")  # too short to call


def test_drafts_are_empty_heldout_and_skipped_by_the_eval(tmp_path, monkeypatch):
    goldens = tmp_path / "evals" / "goldens"; goldens.mkdir(parents=True)
    (goldens / "golden_007.json").write_text(json.dumps({"id": "golden_007", "split": "dev", "job_description": "x",
                                                         "source_sha256": ng.sha("x"), "expected": []}))
    db = tmp_path / "t.db"
    c = sqlite3.connect(db)
    c.executescript("CREATE TABLE job (id INTEGER PRIMARY KEY, company TEXT, title TEXT, description_text TEXT,"
                    " first_seen TEXT, extracted_version TEXT);"
                    "CREATE TABLE job_source (job_id INTEGER, source TEXT);")
    c.executemany("INSERT INTO job VALUES (?,?,?,?,?,?)", [
        (1, "A", "KI Engineer", DE, "2026-10-18", None),
        (2, "B", "AI Engineer", EN, "2026-10-18", None),
        (3, "C", "KI Engineer", DE + " alt", "2026-10-17", "legacy")])
    c.commit(); c.close()
    monkeypatch.setattr(ng, "GOLDENS", goldens); monkeypatch.setattr(ng, "DB", db)
    ng.main(["--german", "5"])
    d = json.loads((goldens / "golden_008.json").read_text())
    assert d["split"] == "heldout" and d["draft"] is True and d["expected"] == [] and d["german"] is None
    assert not (goldens / "golden_009.json").exists()  # English and legacy jobs not picked
    monkeypatch.setattr(re_, "ROOT", tmp_path)  # load_goldens reads ROOT/evals/goldens
    assert [g["id"] for g in re_.load_goldens("heldout")] == []
