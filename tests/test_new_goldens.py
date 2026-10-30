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
    c.executescript("CREATE TABLE job (id INTEGER PRIMARY KEY, company TEXT, title TEXT, city TEXT,"
                    " seniority TEXT, description_text TEXT, first_seen TEXT, extracted_version TEXT);"
                    "CREATE TABLE job_source (job_id INTEGER, source TEXT);")
    c.executemany("INSERT INTO job VALUES (?,?,?,?,?,?,?,?)", [
        (1, "A", "KI Engineer", "Berlin", "mid", DE, "2026-10-18", None),
        (2, "B", "AI Engineer", "Berlin", None, EN, "2026-10-18", None),
        (3, "C", "KI Engineer", "Berlin", None, DE + " alt", "2026-10-17", "legacy")])
    c.commit(); c.close()
    monkeypatch.setattr(ng, "GOLDENS", goldens); monkeypatch.setattr(ng, "DB", db)
    ng.main(["--german", "5"])
    d = json.loads((goldens / "golden_008.json").read_text())
    assert d["split"] == "heldout" and d["draft"] is True and d["expected"] == [] and d["german"] is None
    assert not (goldens / "golden_009.json").exists()  # English and legacy jobs not picked
    monkeypatch.setattr(re_, "ROOT", tmp_path)  # load_goldens reads ROOT/evals/goldens
    assert [g["id"] for g in re_.load_goldens("heldout")] == []


def test_draft_puts_the_title_on_top_but_hashes_the_stored_text():
    d = ng.draft("golden_099", "Python and RAG", "Senior AI Engineer")
    assert d["job_description"] == "Senior AI Engineer\n\nPython and RAG"
    assert d["source_sha256"] == ng.sha("Python and RAG")


def test_a_non_golden_file_in_the_goldens_directory_is_not_read_as_a_golden(tmp_path, monkeypatch):
    """evals/goldens also holds excluded.json, which agent_label's apply writes. Globbing
    *.json there read it as a Golden and broke every eval run, dev split included."""
    goldens = tmp_path / "evals" / "goldens"
    goldens.mkdir(parents=True)
    (goldens / "golden_001.json").write_text(json.dumps(
        {"id": "golden_001", "split": "heldout", "job_description": "x",
         "source_sha256": ng.sha("x"), "expected": []}))
    (goldens / "excluded.json").write_text(json.dumps(
        {"excluded": [{"golden_id": "golden_002", "source_sha256": "abc"}]}))
    monkeypatch.setattr(re_, "ROOT", tmp_path)
    assert [g["id"] for g in re_.load_goldens("heldout")] == ["golden_001"]
    # and the excluded list still keeps its posting and its spent number out of the next pick
    monkeypatch.setattr(ng, "GOLDENS", goldens)
    hashes, top = ng.existing()
    assert "abc" in hashes and top == 2
