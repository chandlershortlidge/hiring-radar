from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app import db
from app.api import create_app
from app.taxonomy import Taxonomy
from tests.test_queries import NOW, add, ts

TAX = Taxonomy({"version": 3, "skills": [
    {"id": "python", "display": "Python"}, {"id": "rag", "display": "RAG", "parents": ["llms"]},
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


def test_jobs_and_detail(api):
    client, _ = api
    r = client.get("/api/jobs", params={"skill": "rag"}).json()
    assert r["total"] == 1 and r["jobs"][0]["company"] == "Acme" and r["jobs"][0]["status"] == "open"
    d = client.get(f"/api/jobs/{r['jobs'][0]['id']}").json()
    assert d["skills"][0]["display"] == "Python" and d["sources"][0]["source"] == "arbeitnow"
    assert client.get("/api/jobs/999").status_code == 404


def test_taxonomy_endpoint(api):
    client, _ = api
    t = client.get("/api/taxonomy").json()
    assert t["version"] == 3 and {"id": "rag", "display": "RAG", "parents": ["llms"]} in t["skills"]


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
