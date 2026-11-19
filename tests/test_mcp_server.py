"""The MCP server (HIR-338). The pattern for the next tool: a test that calls the tool
directly, a parity test against the dashboard's own endpoint, and a schema test that the
tool accepts exactly the API's values. The end-to-end test at the bottom goes through a
real MCP client over HTTP and covers every tool at once."""

import asyncio
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


def test_skill_demand_is_empty_when_nothing_matches(server):
    r = demand(server, city=["Berlin"], seniority=["junior"], family=["ai-engineer"])
    assert r["total"] == 0 and r["skills"] == []





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
                return names, result

    names, result = asyncio.run(run())
    assert names == ["search_jobs", "get_job", "skill_demand"]
    assert not result.is_error
    assert [j["company"] for j in result.structured_content["jobs"]] == ["Acme"]


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
