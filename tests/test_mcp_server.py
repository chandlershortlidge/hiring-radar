"""The MCP server (HIR-338). The pattern for the next tool: a test that calls the tool
directly, a parity test against the dashboard's own endpoint, and a schema test that the
tool accepts exactly the API's values. The end-to-end test at the bottom goes through a
real MCP client over HTTP and covers every tool at once."""

import asyncio
import json
import types
import typing
from pathlib import Path

import httpx2
import pytest
from fastapi.testclient import TestClient
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.server.mcpserver.exceptions import ToolError

from app import db, mcp_server, queries as q
from app.api import create_app
from app.geo import CITIES, REMOTE_EU
from app.extract import Extraction, Mention, Seniority
from app.ingest import ingest_one
from app.pipeline import store_extraction
from app.sources import Posting
from app.taxonomy import Taxonomy
from tests.test_api import TAX
from tests.test_queries import NOW, add, ts

# Jobs chosen so every filter the tests use keeps some and drops some.
JOBS = [
    ("Acme", "AI Engineer", "Berlin", ts(1), [("python", "required"), ("rag", "required")], "mid"),
    ("Beta", "AI Engineer", "Berlin", ts(2), [("python", "required"), ("rag", "nice_to_have")], "senior"),
    ("Gamma", "ML Engineer", "Berlin", ts(3), [("rag", "required"), ("aws", "required")], "junior"),
    ("Delta", "AI Engineer", "San Francisco", ts(0), [("rag", "required")], "mid"),
    ("Old", "AI Engineer", "Berlin", ts(200), [("rag", "required")], "mid"),  # long closed
]


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "t.db"
    c = db.connect(path)
    db.migrate(c)
    for company, title, city, when, skills, seniority in JOBS:
        add(c, company, title, city, "greenhouse", when, skills, seniority)
    c.close()
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    return path


@pytest.fixture
def server(db_path):
    return mcp_server.build_server(db_path, TAX, lambda: NOW)


def call(server, tool: str, **args):
    """Call a tool the way the MCP server does, minus the transport."""
    return asyncio.run(server.call_tool(tool, args))


def search(server, **args) -> dict:
    return call(server, "search_jobs", **args).structured_content


# --- search_jobs ---------------------------------------------------------------------

def test_search_jobs_filters_and_shape(server):
    r = search(server, skills=["RAG"], city=["Berlin"], family=["ai-engineer"])
    assert r["total"] == 1 and [j["company"] for j in r["jobs"]] == ["Acme"]
    job = r["jobs"][0]
    assert job["places"] == ["Berlin"] and job["status"] == "open" and job["seniority"] == "mid"
    assert job["required_skills"] == ["python", "rag"] and job["nice_to_have_skills"] == []
    assert job["first_seen"] == ts(1)[:10] and job["degree"] is None
    # "all" also counts a skill that is only nice-to-have; "30d"/"all" reach closed jobs.
    assert search(server, skills=["rag"], city=["Berlin"], requirement="all")["total"] == 3
    assert search(server, skills=["rag"], window="all")["total"] == 4
    assert {j["status"] for j in search(server, window="all")["jobs"]} == {"open", "closed"}


def test_search_jobs_accepts_skill_names_and_aliases(server):
    by_id = search(server, skills=["rag"])
    assert search(server, skills=["Retrieval Augmented Generation"]) == by_id == search(server, skills=["RAG"])


def test_search_jobs_rejects_what_the_api_rejects(server):
    with pytest.raises(ToolError, match=r"unknown skill 'ragg'; did you mean rag"):
        call(server, "search_jobs", skills=["ragg"])
    with pytest.raises(ToolError, match="limit"):
        call(server, "search_jobs", limit=51)
    with pytest.raises(ToolError):  # not one of the schema's values
        call(server, "search_jobs", seniority=["intern"])


def test_search_jobs_pages(server):
    first, second = search(server, limit=2), search(server, limit=2, offset=2)
    assert first["total"] == second["total"] == 4
    assert {j["id"] for j in first["jobs"]}.isdisjoint(j["id"] for j in second["jobs"])


@pytest.mark.parametrize("args, params", [
    ({}, {}),
    ({"skills": ["rag"], "city": ["Berlin"]}, {"skill": "rag", "city": "Berlin"}),
    ({"skills": ["rag", "python"], "requirement": "all"}, {"skill": ["rag", "python"], "requirement": "all"}),
    ({"seniority": ["mid", "senior"], "sort": "company"}, {"seniority": ["mid", "senior"], "sort": "company"}),
    ({"family": ["ml-engineer"], "window": "all"}, {"family": "ml-engineer", "window": "all"}),
    ({"german": "not_required", "degree": "open", "production": "any"},
     {"german": "not_required", "degree": "open", "production": "any"}),
    ({"company_or_title": "acm", "text": "posting"}, {"q": "acm", "text": "posting"}),
    ({"limit": 2, "offset": 1, "window": "all"}, {"limit": 2, "offset": 1, "window": "all"}),
])
def test_search_jobs_matches_the_dashboard_job_list(db_path, server, args, params):
    """Same filters → the same jobs in the same order, and the same total, as /api/jobs."""
    api = TestClient(create_app(db_path, TAX)).get("/api/jobs", params=params).json()
    tool = search(server, **args)
    assert tool["total"] == api["total"]
    assert [j["id"] for j in tool["jobs"]] == [j["id"] for j in api["jobs"]]
    for t, a in zip(tool["jobs"], api["jobs"]):
        assert (t["required_skills"], t["nice_to_have_skills"], t["status"]) == \
               (a["required_skills"], a["nice_skills"], a["status"])


# --- search_postings ------------------------------------------------------------------
# Each JOBS posting's text names its company, title and skills ("Acme AI Engineer wants
# python, rag ..."), so a skill id doubles as a word to search for.

def postings(server, **args) -> dict:
    return call(server, "search_postings", **args).structured_content


def test_search_postings_counts_matches_per_city_and_career_track(server):
    r = postings(server, text="rag")
    assert r["total"] == 4                                   # Old mentions rag too, but is closed
    assert r["by_city"] == {"Berlin": 3, "San Francisco": 1}
    assert r["by_family"] == {"ai-engineer": 3, "ml-engineer": 1}
    assert list(r["by_city"]) == ["Berlin", "San Francisco"]  # largest first
    assert {j["company"] for j in r["jobs"]} == {"Acme", "Beta", "Gamma", "Delta"}
    assert r["jobs"][0].keys() == search(server)["jobs"][0].keys()   # the same shape as search_jobs
    # Every word must appear; window "all" reaches closed jobs.
    assert postings(server, text="rag python")["total"] == 2
    assert postings(server, text="RAG", window="all")["total"] == 5


def test_search_postings_counts_only_the_chosen_places(db_path, server):
    """A job posted for several places counts in each; a city filter keeps only those."""
    c = db.connect(db_path)
    c.execute("INSERT INTO job_place (job_id, place) VALUES (?, 'Munich')", (acme_id(server),))
    c.commit()
    c.close()
    everywhere = postings(server, text="python")
    assert everywhere["total"] == 2 and everywhere["by_city"] == {"Berlin": 2, "Munich": 1}
    assert postings(server, text="python", city=["Munich"])["by_city"] == {"Munich": 1}
    assert postings(server, text="python", city=["Berlin"])["by_city"] == {"Berlin": 2}


def test_search_postings_with_limit_zero_returns_only_the_counts(server):
    r = postings(server, text="rag", limit=0)
    assert r["total"] == 4 and r["jobs"] == [] and r["by_city"]["Berlin"] == 3


def test_search_postings_finds_nothing_for_a_word_no_posting_has(server):
    assert postings(server, text="kubernetes") == {"total": 0, "by_city": {}, "by_family": {}, "offset": 0, "jobs": []}


def test_search_postings_rejects_what_search_jobs_rejects_and_an_empty_text(server):
    for text in ("", "   ", '""'):
        with pytest.raises(ToolError, match="text must name at least one word"):
            call(server, "search_postings", text=text)
    with pytest.raises(ToolError, match=r"unknown skill 'ragg'"):
        call(server, "search_postings", text="rag", skills=["ragg"])
    with pytest.raises(ToolError, match="limit"):
        call(server, "search_postings", text="rag", limit=51)
    with pytest.raises(ToolError, match="offset"):
        call(server, "search_postings", text="rag", offset=-1)
    with pytest.raises(ToolError):  # not one of the schema's values
        call(server, "search_postings", text="rag", seniority=["intern"])


@pytest.mark.parametrize("args", [
    {"text": "rag"},
    {"text": "rag", "city": ["Berlin"], "family": ["ai-engineer"]},
    {"text": "rag", "skills": ["python"], "requirement": "all", "sort": "company"},
    {"text": "posting body", "window": "all", "seniority": ["mid"], "company_or_title": "a"},
    {"text": "rag", "limit": 2, "offset": 1, "window": "all"},
])
def test_search_postings_lists_what_search_jobs_lists(server, args):
    """The same filters give the same total and the same jobs, in the same order, as
    search_jobs with the same text, so the counts and the list cannot disagree."""
    tool, jobs = postings(server, **args), search(server, **args)
    assert tool["total"] == jobs["total"] and tool["jobs"] == jobs["jobs"]
    assert sum(tool["by_family"].values()) == tool["total"]          # every JOBS posting has a track


def test_search_postings_accepts_exactly_the_search_jobs_values(server):
    hints = typing.get_type_hints(server._tool_manager.get_tool("search_postings").fn)
    jobs = typing.get_type_hints(server._tool_manager.get_tool("search_jobs").fn)
    assert hints == jobs | {"text": str}
    tool = next(t for t in asyncio.run(server.list_tools()) if t.name == "search_postings")
    assert tool.input_schema["required"] == ["text"] and tool.annotations.read_only_hint is True


# --- get_job ------------------------------------------------------------------------

def acme_id(server) -> int:
    """The id of the first job in JOBS (Acme: python and rag required, mid, Berlin)."""
    return search(server, company_or_title="Acme")["jobs"][0]["id"]


def test_get_job_returns_the_job_and_its_skills(server):
    job = call(server, "get_job", job_id=acme_id(server)).structured_content
    assert (job["company"], job["title"], job["places"]) == ("Acme", "AI Engineer", ["Berlin"])
    assert (job["status"], job["seniority"], job["first_seen"]) == ("open", "mid", ts(1)[:10])
    assert job["required_skills"] == ["python", "rag"] and job["nice_to_have_skills"] == []
    assert job["degree"] is None


def test_get_job_matches_the_dashboard_job_page(db_path, server):
    """Same job → the same details as GET /api/jobs/{id}."""
    job_id = acme_id(server)
    api = TestClient(create_app(db_path, TAX)).get(f"/api/jobs/{job_id}").json()
    tool = call(server, "get_job", job_id=job_id).structured_content
    assert (tool["company"], tool["title"], tool["status"]) == (api["company"], api["title"], api["status"])
    assert tool["required_skills"] == [s["skill_id"] for s in api["skills"] if s["requirement"] == "required"]
    assert tool["nice_to_have_skills"] == [s["skill_id"] for s in api["skills"] if s["requirement"] == "nice_to_have"]


def test_get_job_rejects_an_id_that_does_not_exist(server):
    with pytest.raises(ToolError, match="no job with id 99999"):
        call(server, "get_job", job_id=99999)


# Groups of alternatives (HIR-485). Babel asks for Python, and AWS or Docker (the posting's
# "AWS or Azure", with ids the test skill list has). Lyceum's whole ask is one group, as
# job 2063's "vLLM, SGLang, ... or GPU, cloud and Linux" was read.
GROUPED = {
    "Babel": [("python", None), ("aws", 1), ("docker", 1)],
    "Lyceum": [("rag", 1), ("llms", 1), ("aws", 1)],
}


@pytest.fixture
def grouped_server(db_path):
    c = db.connect(db_path)
    for company, mentions in GROUPED.items():
        job_id = add(c, company, "AI Engineer", "Berlin", "greenhouse", ts(1), [], "mid")
        store_extraction(c, job_id, Extraction(
            seniority=Seniority("mid", "stated", "mid"),
            mentions=[Mention(sid, "required", sid, group) for sid, group in mentions]
                     + [Mention("llms", "nice_to_have", "llms")] * (company == "Babel"),
            proposed=[], extractor_version="t", taxonomy_version=3))
    c.close()
    return mcp_server.build_server(db_path, TAX, lambda: NOW)


def job_of(server, company: str) -> dict:
    job_id = search(server, company_or_title=company)["jobs"][0]["id"]
    return call(server, "get_job", job_id=job_id).structured_content | {"id": job_id}


def test_get_job_writes_a_group_of_alternatives_as_one_requirement(grouped_server):
    babel, lyceum = job_of(grouped_server, "Babel"), job_of(grouped_server, "Lyceum")
    assert babel["required_skills"] == ["python", ["aws", "docker"]]
    assert lyceum["required_skills"] == [["aws", "llms", "rag"]]
    assert babel["nice_to_have_skills"] == ["llms"]
    # A job with no group is still a plain list of ids.
    assert job_of(grouped_server, "Acme")["required_skills"] == ["python", "rag"]
    # search_jobs writes the same job the same way.
    listed = {j["company"]: j for j in search(grouped_server, window="all")["jobs"]}
    for company in ("Babel", "Lyceum", "Acme"):
        assert listed[company]["required_skills"] == job_of(grouped_server, company)["required_skills"]


@pytest.mark.parametrize("company", ["Babel", "Lyceum", "Acme"])
def test_get_job_counts_requirements_as_match_profile_does(grouped_server, company):
    """The requirements get_job lists are match_profile's total for the job, with or
    without a group."""
    job = job_of(grouped_server, company)
    ranked = call(grouped_server, "match_profile", skills=["python"], limit=50).structured_content["jobs"]
    total = next(j["total"] for j in ranked if j["id"] == job["id"])
    assert len(job["required_skills"]) == total
    assert total == {"Babel": 2, "Lyceum": 1, "Acme": 2}[company]

# --- skill_demand ------------------------------------------------------------------------


def demand(server, **args) -> dict:
    return call(server, "skill_demand", **args).structured_content


def counts(result: dict) -> dict:
    """{skill id: number of jobs asking for it}, from a skill_demand result."""
    return {s["skill_id"]: s["count"] for s in result["skills"]}


def test_skill_demand_counts_the_skills_of_one_city(server):
    r = demand(server, city=["Berlin"])
    assert r["total"] == 3
    assert counts(r) == {"python": 2, "rag": 2, "aws": 1}


@pytest.mark.parametrize("args, params", [
    ({}, {}),
    ({"city": ["Berlin"]}, {"city": "Berlin"}),
    ({"seniority": ["mid", "senior"]}, {"seniority": ["mid", "senior"]}),
    ({"family": ["ml-engineer"], "window": "all"}, {"family": "ml-engineer", "window": "all"}),
    ({"requirement": "all"}, {"requirement": "all"}),
])
def test_skill_demand_matches_the_dashboard_skill_list(db_path, server, args, params):
    """Same filters -> the same total and the same count per skill as /api/skills."""
    api = TestClient(create_app(db_path, TAX)).get("/api/skills", params=params).json()
    tool = demand(server, **args)
    assert tool["total"] == api["total"]
    assert [(s["skill_id"], s["count"], s["pct"]) for s in tool["skills"]] == \
           [(s["skill_id"], s["count"], s["pct"]) for s in api["skills"]]


def test_skill_demand_rejects_what_the_api_rejects(server):
    with pytest.raises(ToolError):  # not one of the schema's values
        call(server, "skill_demand", seniority=["intern"])
    with pytest.raises(ToolError):
        call(server, "skill_demand", window="forever")


def test_skill_demand_accepts_exactly_the_api_values(server):
    """The schema a model sees offers the values the dashboard's API accepts, no more, no fewer."""
    tool = next(t for t in asyncio.run(server.list_tools()) if t.name == "skill_demand")
    props = tool.input_schema["properties"]
    hints = typing.get_type_hints(server._tool_manager.get_tool("skill_demand").fn)
    expected = {"city": {*CITIES, REMOTE_EU}, "seniority": set(q.SENIORITIES), "family": set(q.FAMILIES),
                "requirement": set(q.REQUIREMENTS), "window": set(q.WINDOWS), "german": set(q.GERMAN_FILTERS),
                "degree": set(q.DEGREE_FILTERS), "production": set(q.PRODUCTION_FILTERS)}
    for name, values in expected.items():
        assert _enum(hints[name]) == values, name
        assert name in props, name
    assert tool.annotations.read_only_hint is True


def test_skill_demand_counts_nice_to_have_skills_when_asked_for_all(server):
    assert counts(demand(server, city=["Berlin"], requirement="all")) == {"python": 2, "rag": 3, "aws": 1}


def test_skill_demand_includes_closed_jobs_when_the_window_is_all(server):
    assert demand(server)["total"] == 4
    assert demand(server, window="all")["total"] == 5


def test_skill_demand_returns_only_the_most_asked_for_skills_up_to_the_cap(server, monkeypatch):
    monkeypatch.setattr(mcp_server, "MAX_SKILLS_TO_RETURN", 2)
    r = demand(server, city=["Berlin"])
    assert [s["skill_id"] for s in r["skills"]] == ["python", "rag"]  # aws (1 job) is cut
    assert r["total"] == 3  # still every matching job, not just the jobs behind the two skills


def test_skill_demand_leaves_out_the_split_by_city(server):
    assert all("by_city" not in s for s in demand(server)["skills"])


def test_skill_demand_is_empty_when_nothing_matches(server):
    r = demand(server, city=["Berlin"], seniority=["junior"], family=["ai-engineer"])
    assert r["total"] == 0 and r["skills"] == []


# --- related_skills ----------------------------------------------------------------------
# The test data has too few jobs for any skill to reach queries.MIN_CO_JOBS, so the tests
# that need rows lower it to 1; the tool and the dashboard read the same constant.

def related(server, **args) -> dict:
    return call(server, "related_skills", **args).structured_content


@pytest.fixture
def every_row(monkeypatch):
    monkeypatch.setattr(q, "MIN_CO_JOBS", 1)


def test_related_skills_lists_what_the_jobs_with_a_skill_also_list(server, every_row):
    r = related(server, skills=["rag"], city=["Berlin"])
    # Berlin's three open jobs all list rag (Beta only as nice-to-have, so not by default).
    assert (r["total"], r["selected_count"]) == (3, 2)
    rows = {s["skill_id"]: s for s in r["skills"]}
    assert set(rows) == {"python", "aws"}                         # rag itself is left out
    assert (rows["python"]["count"], rows["python"]["pct"], rows["python"]["base_pct"]) == (1, 50.0, 66.7)
    assert rows["aws"]["lift"] == 1.5                             # (1/2) / (1/3)


def test_related_skills_ands_several_skills(server, every_row):
    r = related(server, skills=["rag", "python"], city=["Berlin"])
    assert r["selected_count"] == 1 and r["skills"] == []         # only Acme; it lists nothing else


@pytest.mark.parametrize("args, params", [
    ({"skills": ["rag"]}, {"skill": "rag"}),
    ({"skills": ["rag"], "city": ["Berlin"]}, {"skill": "rag", "city": "Berlin"}),
    ({"skills": ["python", "rag"], "requirement": "all"}, {"skill": ["python", "rag"], "requirement": "all"}),
    ({"skills": ["rag"], "seniority": ["mid", "junior"], "window": "all"},
     {"skill": "rag", "seniority": ["mid", "junior"], "window": "all"}),
    ({"skills": ["rag"], "family": ["ai-engineer"], "german": "none", "degree": "open", "production": "any"},
     {"skill": "rag", "family": "ai-engineer", "german": "none", "degree": "open", "production": "any"}),
])
def test_related_skills_matches_the_dashboard_related_panel(db_path, server, every_row, args, params):
    """Same skills and filters -> the same numbers as /api/skills/related."""
    api = TestClient(create_app(db_path, TAX)).get("/api/skills/related", params=params).json()
    tool = related(server, **args)
    assert (tool["total"], tool["selected_count"]) == (api["total"], api["selected_count"])
    keys = ("skill_id", "count", "pct", "base_pct", "lift")
    assert [tuple(s[k] for k in keys) for s in tool["skills"]] == [tuple(s[k] for k in keys) for s in api["skills"]]


def test_related_skills_matches_the_dashboard_with_the_real_cutoff(db_path, server):
    """Without the lowered cut-off every row here is too rare: both answer with none."""
    api = TestClient(create_app(db_path, TAX)).get("/api/skills/related", params={"skill": "rag"}).json()
    tool = related(server, skills=["rag"])
    assert tool == {"selected_count": api["selected_count"], "total": api["total"], "skills": []}
    assert tool["selected_count"] > 0


def test_related_skills_accepts_skill_names_and_aliases(server, every_row):
    by_id = related(server, skills=["rag"])
    assert related(server, skills=["Retrieval Augmented Generation"]) == by_id == related(server, skills=["RAG"])
    assert by_id["skills"]                                        # not two empty answers


def test_related_skills_suggests_ids_for_an_unknown_skill(server):
    with pytest.raises(ToolError, match=r"unknown skill 'pythn'; did you mean python"):
        call(server, "related_skills", skills=["pythn"])


def test_a_misspelled_full_name_is_matched_against_display_names_and_aliases(server):
    """HIR-442: models send the full name, so a typo in it must still find the skill."""
    with pytest.raises(ToolError, match=r"unknown skill 'retrieval augmented generaton'; did you mean rag\b"):
        call(server, "related_skills", skills=["retrieval augmented generaton"])
    with pytest.raises(ToolError, match=r"did you mean rag\b"):
        call(server, "search_jobs", skills=["Retreival-Augmented Generation"])


def test_suggestions_are_ids_and_name_a_skill_once():
    """A skill whose id, name and alias all come close is suggested once, by its id."""
    tax = Taxonomy({"version": 1, "skills": [
        {"id": "rag", "display": "RAG", "aliases": ["retrieval augmented generation", "retrieval-augmented generation"]},
        {"id": "python", "display": "Python"}]})
    with pytest.raises(ToolError) as e:
        call(mcp_server.build_server(Path("unused.db"), tax, lambda: NOW), "related_skills", skills=["retrieval augmented generatio"])
    assert str(e.value).endswith("did you mean rag?")


def test_related_skills_needs_at_least_one_skill(server):
    with pytest.raises(ToolError, match="at least one skill"):
        call(server, "related_skills", skills=[])
    with pytest.raises(ToolError):                                # missing: the schema requires it
        call(server, "related_skills", city=["Berlin"])
    tool = next(t for t in asyncio.run(server.list_tools()) if t.name == "related_skills")
    assert "skills" in tool.input_schema["required"]


def test_related_skills_rejects_what_the_api_rejects(server):
    with pytest.raises(ToolError):
        call(server, "related_skills", skills=["rag"], seniority=["intern"])
    with pytest.raises(ToolError):
        call(server, "related_skills", skills=["rag"], window="forever")


def test_related_skills_accepts_exactly_the_api_values(server):
    """The schema a model sees offers the values the dashboard's API accepts, no more, no fewer."""
    tool = next(t for t in asyncio.run(server.list_tools()) if t.name == "related_skills")
    props = tool.input_schema["properties"]
    hints = typing.get_type_hints(server._tool_manager.get_tool("related_skills").fn)
    expected = {"city": {*CITIES, REMOTE_EU}, "seniority": set(q.SENIORITIES), "family": set(q.FAMILIES),
                "requirement": set(q.REQUIREMENTS), "window": set(q.WINDOWS), "german": set(q.GERMAN_FILTERS),
                "degree": set(q.DEGREE_FILTERS), "production": set(q.PRODUCTION_FILTERS)}
    for name, values in expected.items():
        assert _enum(hints[name]) == values, name
        assert name in props, name
    assert tool.annotations.read_only_hint is True


def test_related_skills_description_states_the_real_cutoffs(server):
    """The tool's description names the top-10 and 5-job rules in words; they must stay true."""
    doc = next(t for t in asyncio.run(server.list_tools()) if t.name == "related_skills").description
    assert f"up to {q.RELATED_LIMIT} other skills" in doc
    assert f"fewer than {q.MIN_CO_JOBS} of the selected jobs" in doc




# --- rising_skills -----------------------------------------------------------------------
# The two-period market of tests/test_rising_skills.py, at its clock, so the comparison has
# enough jobs behind it to answer "ok". The calculation itself is tested there.

from tests import test_rising_skills as rs  # noqa: E402


@pytest.fixture
def rising_db(tmp_path, monkeypatch):
    path = tmp_path / "rising.db"
    c = db.connect(path)
    db.migrate(c)
    rs.market(c)
    c.close()
    monkeypatch.setattr("app.api.now_iso", lambda: rs.NOW)
    return path


@pytest.fixture
def rising_server(rising_db):
    return mcp_server.build_server(rising_db, rs.TAX, lambda: rs.NOW, rs.ADDED)


def rising(server, **args) -> dict:
    return call(server, "rising_skills", **args).structured_content


def test_rising_skills_lists_risers_and_fallers(rising_server):
    r = rising(rising_server, city=["Berlin"], family=["ai-engineer"])
    assert (r["status"], r["reason"], r["window_days"]) == ("ok", None, q.RISING_DAYS)
    assert r["current"]["open_jobs"] == r["previous"]["open_jobs"] == 30
    assert r["risers"] == [{"skill_id": "agents", "current_count": 8, "previous_count": 0,
                            "current_share": 26.7, "previous_share": 0.0, "change": 26.7}]
    assert [s["skill_id"] for s in r["fallers"]] == ["docker"]


@pytest.mark.parametrize("args, params", [
    ({}, {}),
    ({"city": ["Berlin"], "family": ["ai-engineer"]}, {"city": "Berlin", "family": "ai-engineer"}),
    ({"city": ["Berlin"], "requirement": "all"}, {"city": "Berlin", "requirement": "all"}),
    ({"city": ["San Francisco"]}, {"city": "San Francisco"}),             # no jobs there: few_jobs
    ({"city": ["Berlin", "Munich"]}, {"city": ["Berlin", "Munich"]}),     # Munich too new: new_city
])
def test_rising_skills_matches_the_dashboard_rising_panel(rising_db, rising_server, args, params):
    """Same filters -> the same answer as /api/skills/rising, less the display names it adds."""
    api = TestClient(create_app(rising_db, rs.TAX, skill_added=rs.ADDED)).get("/api/skills/rising", params=params).json()
    for row in api["risers"] + api["fallers"]:
        row.pop("display")
    assert rising(rising_server, **args) == api


def test_rising_skills_says_when_there_is_not_enough_data_yet(db_path, server):
    """At the test clock Berlin's collection has not begun: not enough data, with the day it will be."""
    r = rising(server, city=["Berlin"])
    assert (r["status"], r["reason"], r["risers"], r["fallers"]) == ("not_enough_data", "new_city", [], [])
    assert r["ready_from"] == "2026-12-13"                         # 18 Oct + 2 x 28 days
    api = TestClient(create_app(db_path, TAX, skill_added={})).get("/api/skills/rising", params={"city": "Berlin"}).json()
    assert r == api


def test_rising_skills_reads_the_api_skill_added_dates_by_default(rising_db):
    """Without injected dates the server reads the recorded ones, as create_app does."""
    tool = mcp_server.build_server(rising_db, rs.TAX, lambda: rs.NOW)
    api = TestClient(create_app(rising_db, rs.TAX)).get("/api/skills/rising", params={"city": "Berlin"}).json()
    for row in api["risers"] + api["fallers"]:
        row.pop("display")
    assert rising(tool, city=["Berlin"]) == api


def test_rising_skills_rejects_what_the_api_rejects(rising_server):
    with pytest.raises(ToolError):
        call(rising_server, "rising_skills", family=["plumber"])
    with pytest.raises(ToolError):
        call(rising_server, "rising_skills", requirement="sometimes")
    with pytest.raises(ToolError):
        call(rising_server, "rising_skills", city=["Paris"])          # a place we do not offer


def test_rising_skills_offers_only_the_three_filters_it_reads(rising_server):
    """Only city, family and requirement, with exactly the API's values: an ignored filter
    would let a model believe it had narrowed the answer."""
    tool = next(t for t in asyncio.run(rising_server.list_tools()) if t.name == "rising_skills")
    assert set(tool.input_schema["properties"]) == {"city", "family", "requirement"}
    hints = typing.get_type_hints(rising_server._tool_manager.get_tool("rising_skills").fn)
    expected = {"city": {*CITIES, REMOTE_EU}, "family": set(q.FAMILIES), "requirement": set(q.REQUIREMENTS)}
    for name, values in expected.items():
        assert _enum(hints[name]) == values, name
    assert tool.annotations.read_only_hint is True


def test_rising_skills_description_states_the_real_thresholds(rising_server):
    """The description names the period length, the row cap and the smallest move in words."""
    doc = next(t for t in asyncio.run(rising_server.list_tools()) if t.name == "rising_skills").description
    assert f"last {q.RISING_DAYS} days" in doc and f"{q.RISING_DAYS} days before" in doc
    assert f"up to {q.RISING_LIMIT} skills each" in doc
    assert f"at least {q.RISING_MIN_CHANGE:g} point" in doc


def _enum(arg) -> set:
    """The values a tool argument's type allows: Literal, list[Literal], or either | None."""
    out = set()
    for t in (typing.get_args(arg) if typing.get_origin(arg) in (typing.Union, types.UnionType) else (arg,)):
        if typing.get_origin(t) is list:
            t = typing.get_args(t)[0]
        if typing.get_origin(t) is typing.Literal:
            out |= set(typing.get_args(t))
    return out


def test_search_jobs_accepts_exactly_the_api_values(server):
    """The schema a model sees offers the values the dashboard's API accepts, no more, no fewer."""
    tool = asyncio.run(server.list_tools())[0]
    props = tool.input_schema["properties"]
    hints = typing.get_type_hints(server._tool_manager.get_tool("search_jobs").fn)
    expected = {"city": {*CITIES, REMOTE_EU}, "seniority": set(q.SENIORITIES), "family": set(q.FAMILIES),
                "requirement": set(q.REQUIREMENTS), "window": set(q.WINDOWS), "german": set(q.GERMAN_FILTERS),
                "degree": set(q.DEGREE_FILTERS), "production": set(q.PRODUCTION_FILTERS), "sort": set(q.SORTS)}
    for name, values in expected.items():
        assert _enum(hints[name]) == values, name
        assert name in props, name
    # Every place a job can be in is a city the tool offers.
    assert set(q._PLACE_ORDER) == expected["city"]
    assert tool.annotations.read_only_hint is True


# --- match_profile -----------------------------------------------------------------------
# The fit rules themselves are checked against the browser's in tests/test_fit_cases.py;
# these check the tool around them: which jobs it ranks, the order, and what it returns.

MATCH_JOBS = [  # company, title, city, when, skills, seniority
    ("Alpha", "AI Engineer", "Berlin", ts(1), [("python", "required"), ("rag", "required"),
                                               ("llms", "required"), ("docker", "required")], "mid"),
    ("German", "AI Engineer", "Berlin", ts(2), [("python", "required"), ("rag", "required")], "mid"),
    ("Senior", "Senior AI Engineer", "Berlin", ts(3), [("python", "required"), ("rag", "required"),
                                                      ("aws", "required"), ("docker", "required")], None),
    ("Nice", "AI Engineer", "Berlin", ts(4), [("python", "required"), ("rag", "required"), ("llms", "nice_to_have")], None),
    ("Plain", "AI Engineer", "Berlin", ts(5), [("python", "required"), ("rag", "required")], None),
    ("Munich", "ML Engineer", "Munich", ts(6), [("python", "required"), ("aws", "required"), ("docker", "required"),
                                                 ("rust-lang", "required"), ("rag", "required")], None),
    ("Unknown", "AI Engineer", "Berlin", ts(7), [("python", "nice_to_have")], None),
    ("Stale", "AI Engineer", "Berlin", ts(31), [("python", "required"), ("rag", "required")], None),
]
MID = {"skills": ["Python", "RAG", "llms"], "seniority": "mid"}


@pytest.fixture
def match_db(tmp_path, monkeypatch):
    path = tmp_path / "match.db"
    c = db.connect(path)
    db.migrate(c)
    for company, title, city, when, skills, seniority in MATCH_JOBS:
        add(c, company, title, city, "greenhouse", when, skills, seniority)
    c.execute("UPDATE job SET german='required', german_basis='stated', german_signal='Deutsch' WHERE company='German'")
    # Every job is still being advertised today, so the 30-day rule, not the open window,
    # is what leaves Stale out.
    c.execute("UPDATE job SET last_seen=?", (ts(0),))
    c.execute("UPDATE job_source SET last_seen=?", (ts(0),))
    c.commit()
    c.close()
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    return path


@pytest.fixture
def match_server(match_db):
    return mcp_server.build_server(match_db, TAX, lambda: NOW)


def match(server, **args) -> dict:
    return call(server, "match_profile", **args).structured_content


def companies_of(r) -> list[str]:
    return [j["company"] for j in r["jobs"]]


def test_match_profile_ranks_best_fit_first_and_gated_jobs_last(match_server):
    r = match(match_server, **MID)
    # Alpha: 3 of 4. Nice and Plain: 2 of 2, scored as 2 of 4; Nice's covered nice-to-have
    # breaks the tie. Munich: 2 of 5. Unknown lists no required skill. Then the gated jobs,
    # newest first: German (German required) and Senior (the title names another level).
    assert companies_of(r) == ["Alpha", "Nice", "Plain", "Munich", "Unknown", "German", "Senior"]
    assert r["ranked"] == 7
    # Stale is open, but first seen 31 days ago: left out, as Best fit leaves it out.
    assert "Stale" in [j["company"] for j in search(match_server)["jobs"]]
    alpha = r["jobs"][0]
    assert (alpha["covered"], alpha["total"], alpha["score"]) == (3, 4, 0.75)
    assert alpha["missing_required"] == ["docker"] and alpha["gated_by"] == []
    assert alpha["rank_score"] == pytest.approx(0.3006, abs=1e-4) and alpha["few_skills_listed"] is False
    assert alpha["places"] == ["Berlin"] and alpha["first_seen"] == ts(1)[:10] and alpha["url"] is None
    by = {j["company"]: j for j in r["jobs"]}
    assert by["Plain"]["few_skills_listed"] is True and by["Plain"]["score"] == 1
    assert by["Unknown"]["score"] is None and by["Unknown"]["total"] == 0
    assert by["German"]["gated_by"] == ["german"] and by["Senior"]["gated_by"] == ["seniority"]


def test_match_profile_profile_fields_lift_the_gates(match_server):
    r = match(match_server, skills=["python", "rag", "llms"], german=True)
    assert all(j["gated_by"] == [] for j in r["jobs"])     # no level given: no seniority gate
    assert companies_of(r)[:3] == ["Alpha", "Nice", "German"]


def test_match_profile_lists_missing_skills_most_asked_for_first(match_server):
    munich = next(j for j in match(match_server, **MID)["jobs"] if j["company"] == "Munich")
    # Of the open jobs, 3 require docker, 2 aws and 1 rust-lang: the order is that, not
    # the order the posting listed them in.
    assert munich["missing_required"] == ["docker", "aws", "rust-lang"]


def test_match_profile_since_and_filters_narrow_what_is_ranked(match_server):
    assert companies_of(match(match_server, **MID, since=ts(2)[:10])) == ["Alpha", "German"]
    assert companies_of(match(match_server, **MID, city=["Munich"])) == ["Munich"]
    assert "Munich" not in companies_of(match(match_server, **MID, family=["ai-engineer"]))
    # A date further back than 30 days changes nothing: the stale job stays out.
    assert match(match_server, **MID, since=ts(60)[:10]) == match(match_server, **MID)
    assert len(match(match_server, **MID, limit=2)["jobs"]) == 2


def test_match_profile_reads_past_one_page_of_jobs(match_server, monkeypatch):
    whole = match(match_server, **MID)
    monkeypatch.setattr(mcp_server, "FIT_PAGE", 2)
    assert match(match_server, **MID) == whole


def test_match_profile_order_matches_the_dashboard_best_fit(match_db, match_server):
    """The dashboard's Best fit: /api/jobs newest first, the last 30 days, ranked by
    web/src/profile.js. app/fit.py gives profile.js's answers (tests/test_fit_cases.py), so
    running it over /api/jobs is the dashboard's ranking."""
    from app import fit
    for city in ([], ["Berlin"], ["Munich"]):
        api = TestClient(create_app(match_db, TAX)).get(
            "/api/jobs", params={"city": city, "sort": "newest", "limit": 200}).json()
        profile = {"skills": ["python", "rag", "llms"], "seniority": "mid", "german": False,
                   "production": False, "degree": ""}
        dashboard = [j["id"] for j in fit.rank_jobs(profile, fit.recent_jobs(api["jobs"], NOW))]
        assert [j["id"] for j in match(match_server, **MID, city=city or None)["jobs"]] == dashboard


def test_match_profile_rejects_bad_input(match_server):
    for bad in ({"skills": []}, {"skills": ["telepathy"]}, {"skills": ["python"], "since": "yesterday"},
                {"skills": ["python"], "limit": 0}, {"skills": ["python"], "limit": 51},
                {"skills": ["python"], "degree": "diploma"}, {"skills": ["python"], "seniority": "lead"},
                {"skills": ["python"], "city": ["Paris"]}):
        with pytest.raises(ToolError):
            call(match_server, "match_profile", **bad)


def test_match_profile_offers_the_dashboard_profile_values(match_server):
    from app import fit
    hints = typing.get_type_hints(match_server._tool_manager.get_tool("match_profile").fn)
    assert _enum(hints["seniority"]) == set(q.SENIORITIES)
    # The profile's degrees, with "none" for the dashboard's empty string.
    assert _enum(hints["degree"]) == {"none", *(d for d in fit.DEGREE_RANK if d)}
    assert _enum(hints["city"]) == {*CITIES, REMOTE_EU} and _enum(hints["family"]) == set(q.FAMILIES)
    tool = next(t for t in asyncio.run(match_server.list_tools()) if t.name == "match_profile")
    assert tool.annotations.read_only_hint is True
    for gate in fit.GATES:
        assert f'"{gate}"' in tool.description, gate
    assert f"fewer than {fit.SKILLS_FLOOR} required skills" in tool.description


# --- a posting not read yet (HIR-484) ---------------------------------------------------
# Ingest stores a posting first and the model reads it later; in between it has no skills
# and no requirements, which must never look like a read posting that asks for nothing.

def add_unread(path, company="Fresh", city="Berlin", when=None) -> int:
    """A posting ingest stored and the model has not read: a job with no reading at all."""
    c = db.connect(path)
    p = Posting("greenhouse", f"greenhouse-{company}", "", company, "AI Engineer", city,
                f"{company} AI Engineer. Fließend Deutsch, production experience, python, rag." * 20)
    job_id = ingest_one(c, p, when or ts(0), require_city=False, trust_title=True).job_id
    c.commit()
    c.close()
    return job_id


def test_search_jobs_and_search_postings_mark_a_posting_not_read_yet(db_path, server):
    fresh = add_unread(db_path)
    jobs = {j["id"]: j for j in search(server, city=["Berlin"])["jobs"]}
    assert jobs[fresh]["read"] is False and jobs[fresh]["required_skills"] == []
    assert all(j["read"] is True for i, j in jobs.items() if i != fresh)
    # The same mark where a German filter keeps it: unknown, not "German not mentioned".
    assert {j["id"]: j["read"] for j in search(server, german="none")["jobs"]}[fresh] is False
    found = {j["id"]: j for j in postings(server, text="Fresh")["jobs"]}
    assert found[fresh]["read"] is False


def test_get_job_marks_a_posting_not_read_yet(db_path, server):
    fresh = add_unread(db_path)
    job = call(server, "get_job", job_id=fresh).structured_content
    assert job["read"] is False and job["required_skills"] == [] and job["german"] is None
    assert call(server, "get_job", job_id=acme_id(server)).structured_content["read"] is True


def test_match_profile_leaves_out_a_posting_not_read_yet_and_counts_it(match_db, match_server):
    before = match(match_server, **MID)
    fresh = add_unread(match_db)
    r = match(match_server, **MID)
    # Never ranked, so never among the jobs nothing gates; counted instead.
    assert fresh not in [j["id"] for j in r["jobs"]]
    assert (r["ranked"], r["not_read_yet"]) == (before["ranked"], 1) and before["not_read_yet"] == 0
    assert r["jobs"] == before["jobs"]
    # Counted only when the filters keep it.
    assert match(match_server, **MID, city=["Munich"])["not_read_yet"] == 0
    assert match(match_server, **MID, since=ts(0)[:10])["not_read_yet"] == 1


def test_every_tool_that_returns_jobs_says_what_happens_to_a_posting_not_read_yet(server):
    tools = {t.name: t.description for t in asyncio.run(server.list_tools())}
    for name in ("search_jobs", "search_postings", "get_job"):
        assert "read is false" in tools[name] and "has not read yet" in tools[name], name
    assert "not_read_yet" in tools["match_profile"] and "left" in tools["match_profile"]


# --- the skill list (a resource)-----------------------------------------------------

def test_the_skill_list_is_a_resource_with_every_skill(server):
    """One resource, read without arguments: every skill with its id, name, spellings and
    parents, and nothing else (no `reviewed`, which is our own bookkeeping)."""
    (res,) = asyncio.run(server.list_resources())
    assert (str(res.uri), res.name, res.mime_type) == (mcp_server.SKILLS_URI, "skills", "application/json")
    for tool in ("search_jobs", "skill_demand", "related_skills", "parents"):
        assert tool in res.description, tool
    (content,) = asyncio.run(server.read_resource(mcp_server.SKILLS_URI))
    body = json.loads(content.content)
    assert body["version"] == TAX.version
    assert [s["id"] for s in body["skills"]] == sorted(TAX.skills)
    for s in body["skills"]:
        t = TAX.skills[s["id"]]
        assert s == {"id": t.id, "display": t.display, "aliases": list(t.aliases), "parents": list(t.parents)}


def test_the_skill_list_matches_the_dashboard_taxonomy(db_path, server):
    """Same list as /api/taxonomy, which the dashboard's skill picker reads."""
    (content,) = asyncio.run(server.read_resource(mcp_server.SKILLS_URI))
    api = TestClient(create_app(db_path, TAX)).get("/api/taxonomy").json()
    assert json.loads(content.content) == api


def test_no_skill_tree_tool(server):
    """The dashboard's radial chart is not offered: its coordinates are noise to a model,
    and the hierarchy is in the skill list's parents (HIR-434)."""
    assert "skill_tree" not in {t.name for t in asyncio.run(server.list_tools())}


# --- the server over HTTP ------------------------------------------------------------

def test_an_mcp_client_calls_search_jobs_over_http(db_path):
    """End to end: a real MCP client, over Streamable HTTP, through the whole FastAPI app
    (route, rate limit, lifespan), with no network."""
    app = create_app(db_path, TAX)

    async def run():
        async with app.router.lifespan_context(app):
            http = httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://hiring-radar.test")
            url = "http://hiring-radar.test/mcp"
            async with http, Client(streamable_http_client(url, http_client=http)) as client:
                names = [t.name for t in (await client.list_tools()).tools]
                result = await client.call_tool("search_jobs", {"skills": ["rag"], "city": ["Berlin"],
                                                                 "family": ["ai-engineer"]})
                resources = [str(r.uri) for r in (await client.list_resources()).resources]
                skills = await client.read_resource(mcp_server.SKILLS_URI)
                return names, result, resources, skills

    names, result, resources, skills = asyncio.run(run())
    assert names == ["search_jobs", "search_postings", "get_job", "skill_demand", "related_skills", "rising_skills", "match_profile"]
    assert not result.is_error
    assert [j["company"] for j in result.structured_content["jobs"]] == ["Acme"]
    assert resources == [mcp_server.SKILLS_URI]
    (content,) = skills.contents
    assert [s["id"] for s in json.loads(content.text)["skills"]] == sorted(TAX.skills)


def test_an_older_mcp_client_keeps_one_connection_through_the_rate_limit(db_path):
    """A real MCP client on the handshake protocol (before 2026-07-28), through the whole app:
    it is handed a session id on `initialize`, sends it back on every later request, and so
    all its requests land in one bucket. Its listening stream is refused and it works anyway."""
    app = create_app(db_path, TAX)
    (route,) = [r for r in app.router.routes if getattr(r, "path", None) == "/mcp"]

    async def run():
        async with app.router.lifespan_context(app):
            http = httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://hiring-radar.test")
            url = "http://hiring-radar.test/mcp"
            async with http, Client(streamable_http_client(url, http_client=http), mode="legacy") as client:
                await client.list_tools()
                return await client.call_tool("search_jobs", {"skills": ["rag"], "city": ["Berlin"]})

    result = asyncio.run(run())
    assert not result.is_error
    limit = route.app
    (tokens, _), = limit.sessions.buckets.values()       # one connection, however many requests
    assert tokens <= mcp_server.BURST - 4                # initialize, initialized, list_tools, call_tool
    assert len(limit.new_sessions.buckets) == 1


# The rate limit (HIR-444): per connection (MCP session), with a ceiling per address and a
# cap on new connections per address.

def limiter(**numbers):
    """A RateLimit over an app that answers 200, a clock to move by hand, and `hit(ip, session,
    version, method)` -> (status, the response's headers as a dict)."""
    t = [0.0]

    async def app(scope, receive, send):
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"text/plain")]})
        await send({"type": "http.response.body", "body": b""})

    limit = mcp_server.RateLimit(app, clock=lambda: t[0], **numbers)

    def hit(ip, session=None, version=None, method="POST", body=b'{"jsonrpc": "2.0", "id": 7, "method": "ping"}'):
        sent = []

        async def send(m):
            sent.append(m)

        async def receive():
            return {"type": "http.request", "body": body}

        headers = [(b"mcp-session-id", session.encode())] if session else []
        headers += [(b"mcp-protocol-version", version.encode())] if version else []
        asyncio.run(limit({"type": "http", "method": method, "client": (ip, 1), "headers": headers}, receive, send))
        hit.body = b"".join(m.get("body", b"") for m in sent[1:])
        return sent[0]["status"], {k.decode(): v.decode() for k, v in sent[0]["headers"]}

    return limit, t, hit


def connect(hit, ip="1.1.1.1"):
    """Open a connection the way a client's first request does: no session id. -> the id handed out."""
    status, headers = hit(ip)
    assert status == 200
    return headers["mcp-session-id"]


def test_rate_limit_gives_each_connection_from_one_address_its_own_bucket():
    """Two users of one assistant arrive from the same address: one running out of
    requests does not slow the other."""
    _, t, hit = limiter(burst=3, rate=1.0)
    a, b = connect(hit), connect(hit)                    # opening a connection takes one of its 3
    assert a != b
    assert [hit("1.1.1.1", a)[0] for _ in range(3)] == [200, 200, 429]
    assert [hit("1.1.1.1", b)[0] for _ in range(2)] == [200, 200]
    status, headers = hit("1.1.1.1", a)
    assert status == 429 and headers["retry-after"] == "1"
    t[0] += 1.0                                          # one second refills one request
    assert hit("1.1.1.1", a)[0] == 200


def test_rate_limit_follows_a_connection_across_addresses():
    """A vendor sends one user's requests from several of its addresses: the bucket is the connection's."""
    _, _, hit = limiter(burst=2, rate=1.0)
    a = connect(hit, "1.1.1.1")
    assert [hit("2.2.2.2", a)[0], hit("3.3.3.3", a)[0]] == [200, 429]


def test_rate_limit_hands_a_session_id_to_a_request_without_one_only():
    _, _, hit = limiter()
    a = connect(hit)
    assert mcp_server._SESSION_ID.fullmatch(a)
    status, headers = hit("1.1.1.1", a)
    assert status == 200 and "mcp-session-id" not in headers


def test_rate_limit_ceiling_per_address_answers_429_whatever_the_connection():
    _, t, hit = limiter(ip_burst=4, ip_rate=1.0)
    a, b = connect(hit), connect(hit)                    # 2 of the address's 4
    assert [hit("1.1.1.1", a)[0], hit("1.1.1.1", b)[0]] == [200, 200]
    status, headers = hit("1.1.1.1", a)
    assert status == 429 and headers["retry-after"] == "1"
    assert hit("1.1.1.1")[0] == 429                      # and no new connection either
    assert hit("2.2.2.2", a)[0] == 200                   # another address has its own ceiling
    t[0] += 1.0
    assert hit("1.1.1.1", b)[0] == 200


def test_rate_limit_caps_new_connections_per_address():
    """Opening a fresh connection for every request does not step around the limit."""
    _, t, hit = limiter(new_burst=2, new_rate=1.0)
    a = connect(hit)
    connect(hit)
    status, headers = hit("1.1.1.1")
    assert status == 429 and headers["retry-after"] == "1" and "mcp-session-id" not in headers
    assert hit("1.1.1.1", a)[0] == 200                   # a connection already open carries on
    assert hit("2.2.2.2")[0] == 200                      # another address opens its own
    t[0] += 1.0
    assert hit("1.1.1.1")[0] == 200


def test_rate_limit_counts_an_unknown_session_id_as_a_new_connection():
    """After a deploy the table is empty: a client's old id is taken on, at the price of one
    new connection. A made-up id that is not in our form gets a fresh one instead."""
    limit, _, hit = limiter(burst=2, rate=1.0, new_burst=2, new_rate=1.0)
    old = "0123456789abcdef0123456789abcdef"
    status, headers = hit("1.1.1.1", old)
    assert status == 200 and "mcp-session-id" not in headers and old in limit.sessions
    assert [hit("1.1.1.1", old)[0] for _ in range(2)] == [200, 429]      # its own bucket from here on
    status, headers = hit("1.1.1.1", "x" * 5000)
    assert status == 200 and "x" * 5000 not in limit.sessions
    assert mcp_server._SESSION_ID.fullmatch(headers["mcp-session-id"])
    assert hit("1.1.1.1", "fedcba9876543210fedcba9876543210")[0] == 429  # the third new connection


def test_rate_limit_a_hammering_connection_does_not_use_up_its_address():
    """The point of HIR-444: one busy user must not throttle the others on the same address."""
    _, _, hit = limiter(burst=2, rate=1.0, ip_burst=10, ip_rate=1.0)
    a, b = connect(hit), connect(hit)
    assert [hit("1.1.1.1", a)[0] for _ in range(50)] == [200] + [429] * 49
    assert hit("1.1.1.1", b)[0] == 200


def test_rate_limit_holds_the_sessionless_protocol_version_to_the_address_ceiling():
    """A 2026-07-28 request has no handshake and no session id: nothing to key a connection on."""
    limit, _, hit = limiter(new_burst=1, ip_burst=3, ip_rate=1.0)
    results = [hit("1.1.1.1", version="2026-07-28") for _ in range(4)]
    assert [status for status, _ in results] == [200, 200, 200, 429]
    assert all("mcp-session-id" not in headers for _, headers in results)
    assert not limit.sessions.buckets and not limit.new_sessions.buckets


def test_rate_limit_answers_405_to_a_listening_stream():
    """A client holding a session id may open a GET stream; the stateless server has nothing to push."""
    _, _, hit = limiter()
    status, headers = hit("1.1.1.1", connect(hit), method="GET")
    assert status == 405 and headers["allow"] == "POST"


# The refusal (HIR-218): a JSON-RPC error the client hands its model, saying which limit,
# its numbers and how long to wait.

def refusal(hit, *args, **kwargs):
    status, headers = hit(*args, **kwargs)
    assert status == 429 and headers["content-type"] == "application/json"
    return headers, json.loads(hit.body)


def test_refusal_over_a_connections_allowance_says_which_limit_and_how_long_to_wait():
    _, t, hit = limiter(burst=2, rate=0.5)
    a = connect(hit)
    hit("1.1.1.1", a)
    t[0] += 0.5                                          # a quarter of a request back: 1.5 s to wait
    headers, msg = refusal(hit, "1.1.1.1", a)
    assert headers["retry-after"] == "2"
    assert msg["jsonrpc"] == "2.0" and msg["id"] == 7    # the refused request's own id
    assert msg["error"]["code"] == mcp_server.RATE_LIMITED
    assert msg["error"]["data"] == {"retry_after": 2, "limit": "connection"}
    assert msg["error"]["message"] == ("hiring-radar's request limit for this connection is used up: up to 2 "
                                       "requests at once, then about 30 a minute. Try again in 2 seconds.")


def test_refusal_names_the_address_ceiling_and_says_it_is_shared():
    _, _, hit = limiter(ip_burst=2, ip_rate=1.0)
    a = connect(hit)
    hit("1.1.1.1", a)
    headers, msg = refusal(hit, "1.1.1.1", a)
    assert headers["retry-after"] == "1" and msg["error"]["data"] == {"retry_after": 1, "limit": "address"}
    assert "network address is used up: up to 2 requests at once, then about 60 a minute, shared by everyone" \
        in msg["error"]["message"]
    assert msg["error"]["message"].endswith("Try again in 1 second.")
    _, msg = refusal(hit, "1.1.1.1", version="2026-07-28")   # the protocol with no connections meets it too
    assert msg["error"]["data"]["limit"] == "address"


def test_refusal_of_a_new_connection_says_to_keep_the_open_one():
    _, _, hit = limiter(new_burst=1, new_rate=1.0)
    connect(hit)
    headers, msg = refusal(hit, "1.1.1.1")
    assert "mcp-session-id" not in headers
    assert msg["error"]["data"]["limit"] == "new_connections"
    assert "Keep using the connection already open" in msg["error"]["message"]


@pytest.mark.parametrize("body", [b"not json", b'[{"jsonrpc": "2.0", "id": 1, "method": "ping"}]',
                                  b'{"jsonrpc": "2.0", "id": true}', b'{"jsonrpc": "2.0", "method": "x"}',
                                  b'{"id": 1, "pad": "' + b"x" * 70_000 + b'"}'],
                         ids=["not-json", "batch", "bool-id", "notification", "too-large"])
def test_refusal_answers_a_null_id_when_the_request_has_no_usable_one(body):
    """A batch, a body that is not JSON, a notification or a body too large to read: id null,
    which JSON-RPC allows when the id cannot be read."""
    _, _, hit = limiter(burst=1)
    a = connect(hit)
    _, msg = refusal(hit, "1.1.1.1", a, body=body)
    assert msg["id"] is None and msg["error"]["data"]["limit"] == "connection"


def test_a_real_mcp_client_over_its_limit_gets_the_message_not_a_server_error(db_path):
    """End to end, the MCP library's own client through the whole app: the tool call over
    the limit fails with our sentence, which is what the person's assistant reads."""
    app = create_app(db_path, TAX)
    (route,) = [r for r in app.router.routes if getattr(r, "path", None) == "/mcp"]
    route.app.sessions.burst = 4                         # initialize, initialized, tools/list, one tool call

    async def run():
        async with app.router.lifespan_context(app):
            http = httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://hiring-radar.test")
            url = "http://hiring-radar.test/mcp"
            async with http, Client(streamable_http_client(url, http_client=http), mode="legacy") as client:
                first = await client.call_tool("search_jobs", {"city": ["Berlin"]})
                try:
                    await client.call_tool("search_jobs", {"city": ["Berlin"]})
                except Exception as e:                   # noqa: BLE001 - whatever the library raises
                    return first, e
                return first, None

    first, refused = asyncio.run(run())
    assert not first.is_error
    assert refused is not None and "request limit for this connection is used up" in str(refused)
    assert "Try again in" in str(refused)


def test_the_app_serves_mcp_behind_the_rate_limit(db_path):
    """/mcp on the dashboard's app goes through the rate limit: `initialize`, which has no
    session id yet, is answered with one; that connection over its allowance gets 429 while a
    second connection from the same address is still served."""
    app = create_app(db_path, TAX)
    (route,) = [r for r in app.router.routes if getattr(r, "path", None) == "/mcp"]
    assert isinstance(route.app, mcp_server.RateLimit)
    route.app.sessions.burst = 2
    initialize = {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}}
    ping = {"jsonrpc": "2.0", "id": 1, "method": "ping", "params": {}}
    headers = {"accept": "application/json, text/event-stream", "mcp-protocol-version": "2025-06-18"}
    with TestClient(app) as c:
        def connect_and_ping():
            hello = c.post("/mcp", json=initialize, headers=headers)
            assert hello.status_code == 200 and hello.json()["result"]["serverInfo"]
            mine = {**headers, "mcp-session-id": hello.headers["mcp-session-id"]}
            return [c.post("/mcp", json=ping, headers=mine) for _ in range(2)]

        first, second = connect_and_ping()
        assert first.status_code == 200 and second.status_code == 429 and second.headers["retry-after"] == "1"
        assert connect_and_ping()[0].status_code == 200
