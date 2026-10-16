import csv
import sys
from pathlib import Path

import pytest

from app.taxonomy import Taxonomy

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import import_legacy as il  # noqa: E402


def test_legacy_csvs_are_consistent():
    jobs = il.read_csv(ROOT / "legacy/job_rows.csv")
    skills = il.read_csv(ROOT / "legacy/skill_rows.csv")
    ids = {j["id"] for j in jobs}
    assert len(jobs) == 48 and {s["job_id"] for s in skills} <= ids
    assert all(s["requirement"] in ("required", "nice_to_have") for s in skills)


def test_goldens_match_corpus_hashes():
    jobs = {j["id"]: j for j in il.read_csv(ROOT / "legacy/job_rows.csv")}
    g = il.goldens_by_sha()
    corpus = [j for j in jobs.values() if j["id"].startswith("job-")]
    assert len(corpus) == 19 and all(j["screenshot_hash"] in g for j in corpus)
    # golden_001 is the Artefact posting, which was deleted as job-1 and re-added live.
    assert g[jobs["live-1784279615833"]["screenshot_hash"]]["id"] == "golden_001"


def test_legacy_mentions_map_through_taxonomy_and_dedup():
    tax = Taxonomy({"version": 1, "skills": [
        {"id": "python", "display": "Python"}, {"id": "llms", "display": "LLMs", "aliases": ["llm apis"]}]})
    rows = [
        {"canonical": "Python", "raw_text": "Python", "requirement": "nice_to_have"},
        {"canonical": "python", "raw_text": "Strong Python", "requirement": "required"},
        {"canonical": "LLM APIs", "raw_text": "LLM APIs", "requirement": "required"},
        {"canonical": "Synthetic Media", "raw_text": "synthetic media", "requirement": "required"},
    ]
    mentions, unmapped = il.legacy_mentions(rows, tax)
    assert [(m.skill_id, m.requirement) for m in mentions] == [("llms", "required"), ("python", "required")]
    assert unmapped == ["Synthetic Media"]


def test_iso_timestamp():
    assert il.iso("2026-06-11 13:19:29.952+00") == "2026-06-11T13:19:29Z"


def test_dry_run_classifies_without_network(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("HIRING_RADAR_DB", str(tmp_path / "t.db"))
    monkeypatch.setattr(il, "DB_PATH", tmp_path / "t.db")
    monkeypatch.setattr(il, "make_client", lambda: pytest.fail("no network in dry run"))
    shots = tmp_path / "shots"
    shots.mkdir()
    # One live job with an image present; everything else has none.
    (shots / "live-1783670008409.png").write_bytes(b"\x89PNG" + b"\x00" * 8)
    il.main(["--screenshots", str(shots), "--dry-run"])
    out = capsys.readouterr().out
    assert "live-1783670008409: group B" in out
    assert "job-10: group A" in out
    assert "live-1783077244868: group C" in out
    assert "imported: A(golden text)=20 B(transcribed)=1 C(legacy skills)=27" in out
