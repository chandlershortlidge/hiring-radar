import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app import db
from app.api import create_app
from app.taxonomy import Taxonomy
from tests.test_queries import NOW, RELATED_JOBS, add, ts

TAX = Taxonomy({"version": 3, "skills": [
    {"id": "python", "display": "Python"},
    {"id": "rag", "display": "RAG", "aliases": ["Retrieval Augmented Generation"], "parents": ["llms"]},
    {"id": "llms", "display": "LLMs"}, {"id": "aws", "display": "AWS"}, {"id": "docker", "display": "Docker"},
    {"id": "rust-lang", "display": "Rust"}]})


class FakeClient:
    """Answers every extraction with python+rag required; never touches the network."""
    def __init__(self):
        self.messages = self
        self.calls = 0

    def create(self, **kw):
        self.calls += 1
        text = kw["messages"][0]["content"] if isinstance(kw["messages"][0]["content"], str) else ""
        if "<job_description>" in text:
            tool = SimpleNamespace(type="tool_use", name="record_skills", input={
                "skills": [{"skill_id": "python", "requirement": "required", "raw_text": "Python"},
                           {"skill_id": "new:DSPy", "requirement": "nice_to_have", "raw_text": "DSPy"}],
                "seniority": "mid", "seniority_basis": "inferred", "seniority_signal": None})
            return SimpleNamespace(stop_reason="tool_use", content=[tool], usage=None)
        # vision transcription
        return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text="Acme AI Engineer. Python and DSPy required.")],
                               usage=SimpleNamespace(input_tokens=1, output_tokens=1))


@pytest.fixture
def api(tmp_path, monkeypatch):
    path = tmp_path / "t.db"
    c = db.connect(path)
    db.migrate(c)
    add(c, "Acme", "AI Engineer", "Berlin", "arbeitnow", ts(1), [("python", "required"), ("rag", "required"), ("aws", "nice_to_have")], "mid")
    add(c, "Gamma", "AI Engineer", "San Francisco", "greenhouse", ts(0), [("python", "required"), ("aws", "required")], "junior",
        proposed=["Rust"])
    c.close()
    fake = FakeClient()
    monkeypatch.setattr("app.queries.now_iso", lambda: NOW)
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    app = create_app(path, TAX, client_factory=lambda: fake)
    return TestClient(app), fake


def test_stats_and_skills(api):
    client, _ = api
    s = client.get("/api/stats").json()
    assert s["jobs"] == 2 and s["open"] == 2 and s["skills_tracked"] == 6 and s["proposed_pending"] == 1
    r = client.get("/api/skills").json()
    assert r["total"] == 2 and r["skills"][0] == {"skill_id": "python", "count": 2, "by_city": {"Berlin": 1, "San Francisco": 1},
                                                   "pct": 100.0, "display": "Python"}
    assert r["city_totals"] == {"Berlin": 1, "San Francisco": 1}
    r = client.get("/api/skills", params={"city": "Berlin", "requirement": "all"}).json()
    assert {s["skill_id"] for s in r["skills"]} == {"python", "rag", "aws"} and r["total"] == 1


def test_filter_validation(api):
    client, _ = api
    assert client.get("/api/skills", params={"window": "yesterday"}).status_code == 422
    assert client.get("/api/skills", params={"skill": "cobol"}).status_code == 422
    assert client.get("/api/jobs", params={"sort": "random"}).status_code == 422
    assert client.get("/api/jobs", params={"seniority": "intern"}).status_code == 422
    assert client.get("/api/jobs", params={"german": "fluent"}).status_code == 422
    assert client.get("/api/jobs", params={"production": "shipped"}).status_code == 422
    assert client.get("/api/jobs", params={"production": "nice_to_have"}).status_code == 422  # not one of the four keys
    assert client.get("/api/skills", params={"degree": "masters"}).status_code == 422
    assert client.get("/api/skills", params={"degree": "open", "german": "not_required"}).status_code == 200
    assert client.get("/api/skills", params={"production": "not_required"}).status_code == 200
    assert client.get("/api/jobs", params={"production": "required"}).status_code == 200


def test_jobs_and_detail(api):
    client, _ = api
    r = client.get("/api/jobs", params={"skill": "rag"}).json()
    assert r["total"] == 1 and r["jobs"][0]["company"] == "Acme" and r["jobs"][0]["status"] == "open"
    d = client.get(f"/api/jobs/{r['jobs'][0]['id']}").json()
    assert d["skills"][0]["display"] == "Python" and d["sources"][0]["source"] == "arbeitnow"
    # the stored posting text is served on detail (the job page shows it), never on the list
    assert d["description_text"].startswith("Acme AI Engineer wants python, rag, aws")
    assert "description_text" not in r["jobs"][0]
    assert client.get("/api/jobs/999").status_code == 404


def test_taxonomy_endpoint(api):
    client, _ = api
    t = client.get("/api/taxonomy").json()
    # aliases ride along: the chart's filter box matches on them (HIR-67A).
    assert t["version"] == 3 and {"id": "rag", "display": "RAG",
                                  "aliases": ["Retrieval Augmented Generation"],
                                  "parents": ["llms"]} in t["skills"]
    assert {"id": "python", "display": "Python", "aliases": [], "parents": []} in t["skills"]


def test_proposed_resolve(api):
    client, _ = api
    g = client.get("/api/proposed").json()["groups"]
    assert g[0]["label"] == "Rust" and g[0]["count"] == 1
    assert client.post("/api/proposed/resolve", json={"ids": g[0]["ids"], "status": "accepted"}).status_code == 422
    assert client.post("/api/proposed/resolve", json={"ids": g[0]["ids"], "status": "accepted", "resolved_skill_id": "nope"}).status_code == 422
    r = client.post("/api/proposed/resolve", json={"ids": g[0]["ids"], "status": "accepted", "resolved_skill_id": "rust-lang"})
    assert r.json() == {"resolved": 1}
    assert client.get("/api/proposed").json()["groups"] == []
    assert "rust-lang" in {s["skill_id"] for s in client.get("/api/skills").json()["skills"]}


def test_add_text_runs_extraction_and_dedups(api):
    client, fake = api
    body = {"text": "Zeta GmbH is hiring an AI Engineer in Berlin. Requirements: Python and DSPy. " * 2,
            "company": "Zeta GmbH", "title": "AI Engineer", "location": "Berlin", "found_via": "linkedin"}
    r = client.post("/api/add/text", json=body).json()
    assert r["outcome"] == "added" and r["skills_found"] == 1 and r["proposed"] == 1 and fake.calls == 1
    d = client.get(f"/api/jobs/{r['job_id']}").json()
    assert d["seniority"] == "mid" and d["sources"][0]["found_via"] == "linkedin"
    r2 = client.post("/api/add/text", json=body).json()
    assert r2["outcome"] in ("merged", "repost") and r2["job_id"] is None and fake.calls == 1  # no second model call
    assert client.post("/api/add/text", json={**body, "text": "too short"}).status_code == 422


def test_add_screenshot_transcribes_then_extracts(api):
    client, fake = api
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32
    r = client.post("/api/add/screenshot", params={"company": "Acme", "title": "AI Engineer", "location": "Berlin"},
                    files={"file": ("shot.png", png, "image/png")}).json()
    assert r["outcome"] == "added" and r["skills_found"] == 1 and fake.calls == 2
    r2 = client.post("/api/add/screenshot", params={"company": "Acme", "title": "AI Engineer"},
                     files={"file": ("shot.png", png, "image/png")}).json()
    assert r2["outcome"] == "exists" and r2["job_id"] == r["job_id"] and fake.calls == 2


def test_add_url_exists_path(api, monkeypatch):
    client, _ = api
    from app.check import CheckResult
    found = CheckResult(url="https://x", verdict="found", how="ats id", job_id=1, job_title="AI Engineer", sources=["arbeitnow"])
    monkeypatch.setattr("app.api.check_url", lambda *a, **k: found)
    monkeypatch.setattr("app.api.log_check", lambda *a, **k: None)
    r = client.post("/api/add/url", json={"url": "https://x"}).json()
    assert r["outcome"] == "exists" and r["job_id"] == 1


# --- several skills at once (HIR-75) -----------------------------------------------------

# The 15-job set from tests/test_queries.py, with a taxonomy of its own so the snapshot
# below answers for the code and not for taxonomy/skills.json.
WIDE_TAX = Taxonomy({"version": 3, "skills": [
    {"id": "python", "display": "Python"}, {"id": "docker", "display": "Docker"},
    {"id": "pytorch", "display": "PyTorch"}, {"id": "aws", "display": "AWS"},
    {"id": "rag", "display": "RAG"}, {"id": "kubernetes", "display": "Kubernetes"}]})


@pytest.fixture
def wide_api(tmp_path, monkeypatch):
    path = tmp_path / "wide.db"
    c = db.connect(path)
    db.migrate(c)
    for company, city, skills in RELATED_JOBS:
        add(c, company, "AI Engineer", city, "arbeitnow", ts(1), [(s, "required") for s in skills])
    c.close()
    monkeypatch.setattr("app.queries.now_iso", lambda: NOW)
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    return TestClient(create_app(path, WIDE_TAX, client_factory=lambda: FakeClient()))


def test_repeated_skill_params_are_anded(wide_api):
    companies = lambda **p: {j["company"] for j in wide_api.get(
        "/api/jobs", params={"window": "all", "limit": 50, **p}).json()["jobs"]}
    assert companies(skill="python") == {f"Co{n:02d}" for n in range(1, 7)}
    assert companies(skill=["python", "docker"]) == {f"Co{n:02d}" for n in range(1, 6)}
    assert companies(skill=["python", "docker", "kubernetes"]) == {f"Co{n:02d}" for n in range(1, 5)}
    assert companies(skill=["docker", "rag"]) == {"Co01", "Co02", "Co05"}
    # A skill sent twice is the same query as once: the dedup keeps the clause list clean.
    assert companies(skill=["python", "python"]) == companies(skill="python")


def test_skill_tree_carries_both_shares_and_display_names(wide_api):
    r = wide_api.get("/api/skills/tree", params={"window": "all"}).json()
    assert r["total"] == len(RELATED_JOBS) and r["size"] > 0
    by = {n["skill_id"]: n for n in r["nodes"]}
    assert by["rag"]["display"] == "RAG"                 # the id resolved through the taxonomy
    assert (by["rag"]["mentioned"], by["rag"]["mentioned_pct"]) == (13, 86.7)
    assert by["rag"]["required_pct"] == 86.7             # every mention in the fixture is required
    assert {e["child"] for e in r["edges"]} == set(by)   # one edge per node, parent or spoke


def test_skill_tree_rejects_a_bad_filter_like_every_other_read(wide_api):
    assert wide_api.get("/api/skills/tree", params={"window": "yesterday"}).status_code == 422
    assert wide_api.get("/api/skills/tree", params={"seniority": "staff"}).status_code == 422


def test_related_skills_over_a_skill_set(wide_api):
    r = wide_api.get("/api/skills/related", params={"window": "all", "skill": ["python", "docker"]}).json()
    assert (r["selected_count"], r["total"]) == (5, 15)
    assert "python" not in {s["skill_id"] for s in r["skills"]}
    assert "docker" not in {s["skill_id"] for s in r["skills"]}
    # Five jobs require both; pytorch is in four of them, under MIN_CO_JOBS, so the list is
    # pruned to nothing. selected_count is what tells the panel to say that rather than
    # "no jobs require these".
    assert r["skills"] == [] and r["selected_count"] > 0


def test_skill_validation_over_a_list(api):
    client, _ = api
    assert client.get("/api/jobs", params={"skill": ["python", "rag"]}).status_code == 200
    r = client.get("/api/jobs", params={"skill": ["python", "cobol"]})
    assert r.status_code == 422 and r.json()["detail"] == "unknown skill 'cobol'"
    assert client.get("/api/skills/related", params={"skill": ["rag", "cobol"]}).status_code == 422
    # The related panel still needs at least one skill.
    r = client.get("/api/skills/related", params={"window": "all"})
    assert r.status_code == 422 and r.json()["detail"] == "skill is required"


# Captured by replaying these URLs against the tree as it stood just before HIR-75 (that is,
# with HIR-69's production field already on the job rows): with one `skill=` the responses
# must be identical, field for field, to what the single-skill `Filters.skill_id` produced.
# Regenerate it the same way — against the last commit before the change under test — rather
# than from the current code, or it stops being a before/after.
SNAPSHOT = json.loads((Path(__file__).parent / "fixtures" / "single_skill_api_snapshot.json").read_text())


def test_single_skill_responses_are_unchanged(api, wide_api):
    clients = {"small": api[0], "wide": wide_api}
    assert len(SNAPSHOT) == 9
    for key, case in SNAPSHOT.items():
        dataset, _ = key.split(":", 1)
        r = clients[dataset].get(case["url"])
        assert r.status_code == case["status"], key
        assert r.json() == case["body"], key
