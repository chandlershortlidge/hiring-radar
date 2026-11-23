"""The MCP server (HIR-338). The pattern for the next tool: a test that calls the tool
directly, a parity test against the dashboard's own endpoint, and a schema test that the
tool accepts exactly the API's values. The end-to-end test at the bottom goes through a
real MCP client over HTTP and covers every tool at once."""

import asyncio
import json
import types
import typing

import httpx2
import pytest
from fastapi.testclient import TestClient
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.server.mcpserver.exceptions import ToolError

from app import db, mcp_server, queries as q
from app.api import create_app
from app.geo import CITIES, REMOTE_EU
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


# --- the skill list (a resource) -----------------------------------------------------

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


def test_rate_limit_answers_429_once_a_visitor_runs_out():
    t = [0.0]

    async def app(scope, receive, send):
        pass

    limit = mcp_server.RateLimit(app, burst=2, rate=1.0, clock=lambda: t[0])
    sent = []

    async def send(m):
        sent.append(m)

    async def hit(ip):
        sent.clear()
        await limit({"type": "http", "client": (ip, 1)}, None, send)
        return sent[0]["status"] if sent else 200

    async def run():
        out = [await hit("1.1.1.1") for _ in range(3)]
        out.append(await hit("2.2.2.2"))     # another visitor has their own bucket
        t[0] += 1.0                          # one second refills one request
        out.append(await hit("1.1.1.1"))
        return out

    assert asyncio.run(run()) == [200, 200, 429, 200, 200]


def test_the_app_serves_mcp_behind_the_rate_limit(db_path):
    """/mcp on the dashboard's app goes through the rate limit, and a visitor over it gets 429."""
    app = create_app(db_path, TAX)
    (route,) = [r for r in app.router.routes if getattr(r, "path", None) == "/mcp"]
    assert isinstance(route.app, mcp_server.RateLimit)
    route.app.burst = 1
    ping = {"jsonrpc": "2.0", "id": 1, "method": "ping", "params": {}}
    headers = {"accept": "application/json, text/event-stream", "mcp-protocol-version": "2025-06-18"}
    with TestClient(app) as c:
        first, second = (c.post("/mcp", json=ping, headers=headers) for _ in range(2))
    assert first.status_code == 200 and second.status_code == 429 and second.headers["retry-after"] == "1"
