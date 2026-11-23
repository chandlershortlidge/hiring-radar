import json
from pathlib import Path

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


@pytest.fixture
def api(tmp_path, monkeypatch):
    path = tmp_path / "t.db"
    c = db.connect(path)
    db.migrate(c)
    add(c, "Acme", "AI Engineer", "Berlin", "arbeitnow", ts(1), [("python", "required"), ("rag", "required"), ("aws", "nice_to_have")], "mid")
    add(c, "Gamma", "AI Engineer", "San Francisco", "greenhouse", ts(0), [("python", "required"), ("aws", "required")], "junior",
        proposed=["Rust"])
    c.close()
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    app = create_app(path, TAX)
    return TestClient(app)


def test_stats_and_skills(api):
    client = api
    s = client.get("/api/stats").json()
    assert s["jobs"] == 2 and s["open"] == 2 and s["skills_tracked"] == 6
    r = client.get("/api/skills").json()
    assert r["total"] == 2 and r["skills"][0] == {"skill_id": "python", "count": 2, "by_city": {"Berlin": 1, "San Francisco": 1},
                                                   "pct": 100.0, "display": "Python"}
    assert r["city_totals"] == {"Berlin": 1, "San Francisco": 1}
    r = client.get("/api/skills", params={"city": "Berlin", "requirement": "all"}).json()
    assert {s["skill_id"] for s in r["skills"]} == {"python", "rag", "aws"} and r["total"] == 1


def test_filter_validation(api):
    client = api
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
    # The largest page the route serves. "Best fit" ranks in the browser and so asks for
    # exactly this many rows in one request (web/src/JobList.jsx FIT_MAX) — raising that
    # constant past this bound silently empties the job list, so the bound is pinned here.
    assert client.get("/api/jobs", params={"limit": 200}).status_code == 200
    assert client.get("/api/jobs", params={"limit": 201}).status_code == 422


def test_jobs_and_detail(api):
    client = api
    r = client.get("/api/jobs", params={"skill": "rag"}).json()
    assert r["total"] == 1 and r["jobs"][0]["company"] == "Acme" and r["jobs"][0]["status"] == "open"
    d = client.get(f"/api/jobs/{r['jobs'][0]['id']}").json()
    assert d["skills"][0]["display"] == "Python" and d["sources"][0]["source"] == "arbeitnow"
    # the stored posting text is served on detail (the job page shows it), never on the list
    assert d["description_text"].startswith("Acme AI Engineer wants python, rag, aws")
    assert "description_text" not in r["jobs"][0]
    assert client.get("/api/jobs/999").status_code == 404


def test_jobs_text_search(api):
    """`text` searches the posting text, `q` the company and title; neither touches the other."""
    client = api
    r = client.get("/api/jobs", params={"text": "rag aws"}).json()
    assert r["total"] == 1 and r["jobs"][0]["company"] == "Acme"
    assert client.get("/api/jobs", params={"text": "kubernetes"}).json()["total"] == 0
    # No syntax error from FTS5's own operators, and nothing matches the literal word.
    assert client.get("/api/jobs", params={"text": 'OR "('}).json()["total"] == 0
    assert client.get("/api/jobs", params={"text": "  "}).json()["total"] == 2
    # Sent together they narrow together: no job is Gamma's and mentions Acme.
    assert client.get("/api/jobs", params={"q": "gamma", "text": "acme"}).json()["total"] == 0
    assert client.get("/api/jobs", params={"q": "acme", "text": "acme"}).json()["total"] == 1


def test_taxonomy_endpoint(api):
    client = api
    t = client.get("/api/taxonomy").json()
    # aliases ride along: the chart's filter box matches on them (HIR-67A).
    assert t["version"] == 3 and {"id": "rag", "display": "RAG",
                                  "aliases": ["Retrieval Augmented Generation"],
                                  "parents": ["llms"]} in t["skills"]
    assert {"id": "python", "display": "Python", "aliases": [], "parents": []} in t["skills"]


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
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    return TestClient(create_app(path, WIDE_TAX))


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
    client = api
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
# than from the current code, or it stops being a before/after. A later migration that puts a
# new field on every job row is the one allowed edit: HIR-186 added `family` to the stored
# rows (derived from each row's title), leaving every other field as captured; HIR-251 added
# `required_groups` (always [] here: no fixture job has alternatives) the same way, and HIR-289
# added `places` (here always the job's one city), and HIR-226 added `flagged` (always false: no
# fixture job carries a flag).
SNAPSHOT = json.loads((Path(__file__).parent / "fixtures" / "single_skill_api_snapshot.json").read_text())


def test_single_skill_responses_are_unchanged(api, wide_api):
    clients = {"small": api, "wide": wide_api}
    assert len(SNAPSHOT) == 9
    for key, case in SNAPSHOT.items():
        dataset, _ = key.split(":", 1)
        r = clients[dataset].get(case["url"])
        assert r.status_code == case["status"], key
        assert r.json() == case["body"], key


def test_family_filter_and_per_family_counts(api):
    """Both fixture jobs are AI Engineer, so the family filter either keeps or drops them."""
    client = api
    assert client.get("/api/stats").json()["open_by_family"] == {"ai-engineer": 2}
    # The related panel needs a skill of its own; the other three take the filter alone.
    extra = {"/api/skills/related": {"skill": "python"}}
    for path in ("/api/skills", "/api/skills/related", "/api/skills/tree", "/api/jobs"):
        base = extra.get(path, {})
        assert client.get(path, params={**base, "family": "ai-engineer"}).status_code == 200
        assert client.get(path, params={**base, "family": "bogus"}).status_code == 422
    assert client.get("/api/skills", params={"family": "ai-engineer"}).json()["total"] == 2
    assert client.get("/api/skills", params={"family": "data-scientist"}).json()["total"] == 0
    jobs = client.get("/api/jobs", params={"family": "ai-engineer"}).json()
    assert jobs["total"] == 2 and {j["family"] for j in jobs["jobs"]} == {"ai-engineer"}
    assert client.get("/api/jobs", params={"family": "data-scientist"}).json()["total"] == 0
    # Repeated params are an OR, the same shape as seniority.
    assert client.get("/api/jobs", params=[("family", "ai-engineer"), ("family", "research")]).json()["total"] == 2


# --- adding a job and settling a proposed skill are not on the site (HIR-346) -----------------

@pytest.mark.parametrize("path", ["/api/add/url", "/api/add/text", "/api/add/screenshot", "/api/proposed/resolve"])
def test_the_removed_write_routes_answer_404(api, path):
    assert api.post(path, json={"url": "https://x", "ids": [1], "status": "rejected"}).status_code == 404


def test_the_removed_write_routes_answer_404_when_the_built_site_is_served(tmp_path, monkeypatch):
    """The live site serves the built pages from a catch-all GET route, which would answer a
    POST to any unknown path with 405 and a GET with the home page; under /api it is 404."""
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<html>home</html>")
    monkeypatch.setattr("app.api.WEB_DIST", dist)
    client = TestClient(create_app(tmp_path / "t.db", TAX))
    for path in ("/api/add/url", "/api/add/text", "/api/add/screenshot", "/api/proposed/resolve"):
        assert client.post(path, json={}).status_code == 404
    assert client.get("/api/nothing-here").status_code == 404
    assert client.get("/api/stats").status_code == 200          # the real routes are untouched
    assert client.get("/berlin").text == "<html>home</html>"    # and so are the pages


def test_stats_no_longer_carries_the_proposed_count(api):
    assert "proposed_pending" not in api.get("/api/stats").json()
