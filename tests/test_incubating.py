"""Incubating places and career tracks (HIR-395): collected like any other, shown nowhere
public, and shown with their whole history the moment their state says live.

One database, filled through the same ingest a daily collection uses, then read three ways:
the public API, every MCP tool, and the queries a tool behind the site calls with
`include_incubating`. The states are app/scope.py's; each test changes one line of them,
which is all a real switch is.
"""

import asyncio
import dataclasses

import pytest
from fastapi.testclient import TestClient
from mcp.server.mcpserver.exceptions import ToolError

from app import db, geo, ingest, mcp_server, queries as q, scope
from app.api import create_app
from app.extract import Extraction, Mention, Proposed, Seniority
from app.pipeline import store_extraction
from app.sources import Posting
from tests.test_api import TAX
from tests.test_queries import NOW, ts

FIRST_SEEN = ts(40)          # the day the collector first saw every job below
BODY = " The team ships models to production and writes about it at length." * 12


def collect(conn, company, title, location, skills=("python",), proposed=(), sid=None):
    """One posting through the feed path (title and city filters on), seen on FIRST_SEEN
    and again today, then read. Returns what ingest said about the first sighting."""
    p = Posting("greenhouse", sid or f"{company}-{title}", f"https://example.com/{company}", company, title,
                location, f"{company} is hiring a {title}." + BODY)
    first = ingest.ingest_one(conn, p, FIRST_SEEN)
    if first.job_id is not None:
        ingest.ingest_one(conn, p, ts(0))
        store_extraction(conn, first.job_id, Extraction(
            seniority=Seniority(None, None, None), mentions=[Mention(s, "required", s) for s in skills],
            proposed=[Proposed(label, "required", label) for label in proposed],
            extractor_version="t", taxonomy_version=3))
    return first


@pytest.fixture
def path(tmp_path, monkeypatch):
    path = tmp_path / "t.db"
    conn = db.connect(path)
    db.migrate(conn)
    collect(conn, "Acme", "AI Engineer", "Berlin", ("python", "rag"))
    collect(conn, "Windy", "AI Engineer", "Chicago, IL", ("python", "aws"), proposed=["Zig"])
    collect(conn, "Both", "ML Engineer", "Berlin; Chicago, IL", ("python",))
    collect(conn, "Lab", "Research Engineer, LLMs", "Berlin", ("python", "docker"), proposed=["Mojo"])
    conn.close()
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    return path


@pytest.fixture
def api(path):
    return TestClient(create_app(path, TAX, skill_added={}))


@pytest.fixture
def conn(path):
    c = db.connect(path)
    yield c
    c.close()


def job_id(conn, company) -> int:
    return conn.execute("SELECT id FROM job WHERE company = ?", (company,)).fetchone()[0]


def companies(api, **params) -> set[str]:
    r = api.get("/api/jobs", params={"window": "all", **params})
    assert r.status_code == 200, r.text
    return {j["company"] for j in r.json()["jobs"]}


def incubate_city(monkeypatch, city="Chicago"):
    monkeypatch.setitem(scope.PLACE_STATE, city, scope.INCUBATING)


def incubate_track(monkeypatch, track="research"):
    monkeypatch.setitem(scope.TRACKS, track, scope.Track(scope.INCUBATING))


# --- collection treats both states alike ---------------------------------------------------

def test_an_incubating_city_is_collected_exactly_like_a_live_one(conn, monkeypatch):
    incubate_city(monkeypatch)
    stored = collect(conn, "Lake", "AI Engineer", "Chicago, IL")
    assert stored.kind == ingest.NEW
    # Still listed, a second source merged in, and every place recorded: nothing differs.
    again = Posting("greenhouse", "Lake-AI Engineer", "", "Lake", "AI Engineer", "Chicago, IL",
                    "Lake is hiring a AI Engineer." + BODY)
    assert ingest.ingest_one(conn, again, ts(0)).kind == ingest.STILL_LISTED
    other = Posting("lever", "x1", "", "Lake", "AI Engineer", "Chicago, IL", "Lake is hiring a AI Engineer." + BODY)
    assert ingest.ingest_one(conn, other, ts(0)).kind == ingest.MERGED
    assert [r[0] for r in conn.execute("SELECT place FROM job_place WHERE job_id = ?", (stored.job_id,))] == ["Chicago"]


def test_an_incubating_track_is_collected_exactly_like_a_live_one(conn, monkeypatch):
    incubate_track(monkeypatch)
    stored = collect(conn, "Deep", "Research Engineer", "Berlin")
    assert stored.kind == ingest.NEW
    assert conn.execute("SELECT family FROM job WHERE id = ?", (stored.job_id,)).fetchone()[0] == "research"


# --- an incubating city: nothing public shows it -------------------------------------------

def test_an_incubating_citys_jobs_are_stored_but_absent_from_the_public_api(api, conn, monkeypatch):
    assert companies(api) == {"Acme", "Windy", "Both", "Lab"}          # all live: all shown
    incubate_city(monkeypatch)
    windy, both = job_id(conn, "Windy"), job_id(conn, "Both")
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 4   # still stored

    # The job list: gone, and not found by asking for the city, the company or its text.
    assert companies(api) == {"Acme", "Both", "Lab"}
    assert companies(api, city="Chicago") == set()
    assert companies(api, city=["Chicago", "Berlin"]) == {"Acme", "Both", "Lab"}
    assert companies(api, q="windy") == set() and companies(api, text="Windy") == set()
    # The job's own page, and flagging it: no such job.
    assert api.get(f"/api/jobs/{windy}").status_code == 404
    assert api.post(f"/api/jobs/{windy}/flag", json={"view": {}}).status_code == 404

    # The header's counts and the picker's per-city numbers.
    stats = api.get("/api/stats").json()
    assert stats["jobs"] == 3 and stats["open"] == 3 and stats["companies"] == 3
    assert stats["open_by_city"] == {"Berlin": 3}

    # The chart, compare mode's per-city numbers, the tree, the related panel.
    skills = api.get("/api/skills", params={"window": "all"}).json()
    assert skills["total"] == 3 and skills["city_totals"] == {"Berlin": 3}
    assert "aws" not in {s["skill_id"] for s in skills["skills"]}        # only Windy asked for it
    assert all(set(s["by_city"]) <= {"Berlin"} for s in skills["skills"])
    assert api.get("/api/skills", params={"window": "all", "city": "Chicago"}).json()["total"] == 0
    assert api.get("/api/skills/tree", params={"window": "all"}).json()["total"] == 3
    related = api.get("/api/skills/related", params={"window": "all", "skill": "python"}).json()
    assert related["total"] == 3 and related["selected_count"] == 3

    # The review queue names each job's company: Windy's proposal is not in it.
    groups = api.get("/api/proposed").json()["groups"]
    assert {g["label"] for g in groups} == {"Mojo"}

    # A job posted for a live city too is shown, as a job in its live city only.
    job = api.get(f"/api/jobs/{both}").json()
    assert job["places"] == ["Berlin"] and job["city"] == "Berlin"
    listed = next(j for j in api.get("/api/jobs", params={"window": "all"}).json()["jobs"] if j["id"] == both)
    assert listed["places"] == ["Berlin"] and listed["city"] == "Berlin"


def test_whats_rising_never_reads_an_incubating_city(api, conn, monkeypatch):
    """Asked for by name it answers like a place we do not collect; and its start date,
    however recent, does not hold back the answer for "every city"."""
    incubate_city(monkeypatch)
    r = api.get("/api/skills/rising", params={"city": "Chicago"}).json()
    assert (r["status"], r["reason"], r["ready_from"]) == ("not_enough_data", "new_city", None)

    old = {place: "2020-01-01" for place in scope.places()}
    everywhere = q.rising_skills(conn, q.Filters(), NOW, {}, collecting_since={**old, "Chicago": NOW[:10]})
    assert everywhere["reason"] != "new_city"
    assert everywhere["current"]["open_jobs"] == 3                       # Windy is not counted
    monkeypatch.setitem(scope.PLACE_STATE, "Chicago", scope.LIVE)
    held_back = q.rising_skills(conn, q.Filters(), NOW, {}, collecting_since={**old, "Chicago": NOW[:10]})
    assert held_back["reason"] == "new_city"                             # a live new city still does


def test_switching_a_city_to_live_shows_its_jobs_with_their_original_first_seen(api, conn, monkeypatch):
    incubate_city(monkeypatch)
    windy = job_id(conn, "Windy")
    assert api.get(f"/api/jobs/{windy}").status_code == 404

    monkeypatch.setitem(scope.PLACE_STATE, "Chicago", scope.LIVE)       # the one-line switch
    job = api.get(f"/api/jobs/{windy}").json()
    assert job["first_seen"] == FIRST_SEEN and job["places"] == ["Chicago"] and job["status"] == "open"
    assert companies(api, city="Chicago") == {"Windy", "Both"}
    assert api.get("/api/stats").json()["open_by_city"] == {"Berlin": 3, "Chicago": 2}
    assert api.get("/api/skills", params={"window": "all"}).json()["city_totals"] == {"Berlin": 3, "Chicago": 2}
    # Nothing was collected again: the same four rows, each seen first on the first day.
    assert [r[0] for r in conn.execute("SELECT DISTINCT first_seen FROM job")] == [FIRST_SEEN]


# --- an incubating track -------------------------------------------------------------------

def test_an_incubating_tracks_jobs_are_stored_but_absent_from_the_public_api(api, conn, monkeypatch):
    incubate_track(monkeypatch)
    lab = job_id(conn, "Lab")
    assert companies(api) == {"Acme", "Windy", "Both"}
    assert api.get(f"/api/jobs/{lab}").status_code == 404
    # Asking for the track by name is refused like a name nobody defined.
    assert api.get("/api/jobs", params={"family": "research"}).status_code == 422
    assert api.get("/api/skills", params={"family": "research"}).status_code == 422
    stats = api.get("/api/stats").json()
    assert stats["jobs"] == 3 and "research" not in stats["open_by_family"]
    assert stats["open_by_city"] == {"Berlin": 2, "Chicago": 2}
    skills = api.get("/api/skills", params={"window": "all"}).json()
    assert skills["total"] == 3 and "docker" not in {s["skill_id"] for s in skills["skills"]}
    assert {g["label"] for g in api.get("/api/proposed").json()["groups"]} == {"Zig"}


def test_switching_a_track_to_live_shows_its_jobs_with_their_original_first_seen(api, conn, monkeypatch):
    incubate_track(monkeypatch)
    lab = job_id(conn, "Lab")
    monkeypatch.setitem(scope.TRACKS, "research", scope.Track(scope.LIVE))
    assert api.get(f"/api/jobs/{lab}").json()["first_seen"] == FIRST_SEEN
    assert companies(api, family="research") == {"Lab"}


# --- a track added with its own title pattern ---------------------------------------------

SOFTWARE = scope.Track(scope.INCUBATING, r"\bsoftware (engineer|developer)\b")


def allow_track_in_database(conn, name: str) -> None:
    """What the migration that adds a track does: rebuild the list of values the database
    accepts in job.family, keeping every stored value. Only supported ALTER statements."""
    allowed = ", ".join(f"'{t}'" for t in (*ingest.FAMILIES, name))
    conn.executescript(f"""
        BEGIN;
        DROP INDEX job_family;
        ALTER TABLE job ADD COLUMN family_next TEXT CHECK (family_next IN ({allowed}));
        UPDATE job SET family_next = family;
        ALTER TABLE job DROP COLUMN family;
        ALTER TABLE job RENAME COLUMN family_next TO family;
        CREATE INDEX job_family ON job (family);
        COMMIT;""")


def test_a_new_tracks_pattern_widens_collection_without_touching_the_live_tracks(monkeypatch):
    live_titles = ["Senior AI Engineer", "Machine Learning Engineer", "Software Engineer, AI Platform",
                   "Data Scientist", "MLOps Engineer", "Research Engineer, LLMs"]
    before = [(ingest.in_scope_title(t), ingest.family_of(t)) for t in live_titles]
    assert not ingest.in_scope_title("Senior Software Engineer")

    monkeypatch.setitem(scope.TRACKS, "software-engineer", SOFTWARE)
    assert ingest.in_scope_title("Senior Software Engineer")
    assert ingest.family_of("Senior Software Engineer (Backend)") == "software-engineer"
    # Every title the five tracks held is still theirs, including one the new pattern matches.
    assert [(ingest.in_scope_title(t), ingest.family_of(t)) for t in live_titles] == before
    assert ingest.family_of("Software Engineer, AI Platform") == "ai-engineer"
    # A sales title stays out whatever the track; a title no rule knows keeps the old default.
    assert not ingest.in_scope_title("Software Sales Engineer")
    assert not ingest.in_scope_title("Accountant") and ingest.family_of("Accountant") == "ai-engineer"


def test_a_new_incubating_track_is_collected_hidden_and_then_switched_live(api, conn, monkeypatch):
    plain = Posting("greenhouse", "s1", "", "Stack", "Senior Software Engineer", "Berlin", "Stack hires." + BODY)
    assert ingest.ingest_one(conn, plain, FIRST_SEEN).kind == ingest.SKIPPED_TITLE   # today: not collected

    monkeypatch.setitem(scope.TRACKS, "software-engineer", SOFTWARE)
    allow_track_in_database(conn, "software-engineer")
    # The rebuild kept every stored job's track and the triggers that follow the table.
    assert dict(conn.execute("SELECT family, count(*) FROM job GROUP BY family")) == {
        "ai-engineer": 2, "ml-engineer": 1, "research": 1}
    stored = collect(conn, "Stack", "Senior Software Engineer", "Berlin", sid="s1")
    assert stored.kind == ingest.NEW
    assert conn.execute("SELECT family FROM job WHERE id = ?", (stored.job_id,)).fetchone()[0] == "software-engineer"
    assert conn.execute("SELECT place FROM job_place WHERE job_id = ?", (stored.job_id,)).fetchone()[0] == "Berlin"

    assert "Stack" not in companies(api) and companies(api, text="Stack") == set()
    assert api.get(f"/api/jobs/{stored.job_id}").status_code == 404
    assert api.get("/api/jobs", params={"family": "software-engineer"}).status_code == 422
    assert api.get("/api/stats").json()["jobs"] == 4

    monkeypatch.setitem(scope.TRACKS, "software-engineer", scope.Track(scope.LIVE, SOFTWARE.title_pattern))
    assert companies(api, family="software-engineer") == {"Stack"}
    assert api.get(f"/api/jobs/{stored.job_id}").json()["first_seen"] == FIRST_SEEN


# --- every MCP tool ------------------------------------------------------------------------

def _tool(server, name, **args):
    return asyncio.run(server.call_tool(name, args)).structured_content


def _check_search_jobs(server, hidden_id, hidden_company, hidden_place):
    found = _tool(server, "search_jobs", window="all", limit=50)
    assert hidden_company not in {j["company"] for j in found["jobs"]} and found["total"] == 3
    assert _tool(server, "search_jobs", window="all", company_or_title=hidden_company)["total"] == 0
    assert all(hidden_place not in j["places"] for j in found["jobs"])


def _check_search_postings(server, hidden_id, hidden_company, hidden_place):
    found = _tool(server, "search_postings", text="production", window="all", limit=50)   # in every posting
    assert hidden_company not in {j["company"] for j in found["jobs"]} and found["total"] == 3
    assert _tool(server, "search_postings", text=hidden_company, window="all")["total"] == 0
    assert sum(found["by_family"].values()) == 3                 # the hidden job is in no track's count
    if hidden_place:
        assert hidden_place not in found["by_city"] and all(hidden_place not in j["places"] for j in found["jobs"])
    else:
        assert "research" not in found["by_family"]


def _check_get_job(server, hidden_id, hidden_company, hidden_place):
    with pytest.raises(ToolError, match=f"no job with id {hidden_id}"):
        asyncio.run(server.call_tool("get_job", {"job_id": hidden_id}))


def _check_skill_demand(server, hidden_id, hidden_company, hidden_place):
    assert _tool(server, "skill_demand", window="all")["total"] == 3


def _check_related_skills(server, hidden_id, hidden_company, hidden_place):
    r = _tool(server, "related_skills", skills=["python"], window="all")
    assert (r["total"], r["selected_count"]) == (3, 3)   # every job lists python; the hidden one is not counted


def _check_rising_skills(server, hidden_id, hidden_company, hidden_place):
    if hidden_place:                                     # asked for by name: like a place we do not collect
        r = _tool(server, "rising_skills", city=[hidden_place])
        assert (r["status"], r["reason"], r["ready_from"]) == ("not_enough_data", "new_city", None)
    with pytest.MonkeyPatch.context() as mp:             # every place collected long enough to compare
        for place in scope.places():
            mp.setitem(geo.COLLECTING_SINCE, place, "2020-01-01")
        r = _tool(server, "rising_skills")
    assert r["current"]["open_jobs"] == r["previous"]["open_jobs"] == 3   # the hidden job is not counted


def _check_match_profile(server, hidden_id, hidden_company, hidden_place):
    with pytest.MonkeyPatch.context() as mp:             # every job counts as recent, so a leak would show
        mp.setattr(mcp_server.fit, "recent_jobs", lambda jobs, now: jobs)
        r = _tool(server, "match_profile", skills=["python"])
    assert r["ranked"] == 3 and hidden_company not in {j["company"] for j in r["jobs"]}
    assert all(hidden_place not in j["places"] for j in r["jobs"])


# One check per tool: what the tool must not give away about an incubating job.
TOOL_CHECKS = {"search_jobs": _check_search_jobs, "search_postings": _check_search_postings, "get_job": _check_get_job, "skill_demand": _check_skill_demand,
               "related_skills": _check_related_skills, "rising_skills": _check_rising_skills,
               "match_profile": _check_match_profile}


def test_every_mcp_tool_has_an_incubating_check(path):
    """A tool added later fails here until it says what it hides (and is checked below)."""
    server = mcp_server.build_server(path, TAX, lambda: NOW)
    assert {t.name for t in asyncio.run(server.list_tools())} == set(TOOL_CHECKS)


@pytest.mark.parametrize("tool", sorted(TOOL_CHECKS))
def test_no_mcp_tool_shows_an_incubating_citys_jobs(path, conn, monkeypatch, tool):
    incubate_city(monkeypatch)
    TOOL_CHECKS[tool](mcp_server.build_server(path, TAX, lambda: NOW), job_id(conn, "Windy"), "Windy", "Chicago")


@pytest.mark.parametrize("tool", sorted(TOOL_CHECKS))
def test_no_mcp_tool_shows_an_incubating_tracks_jobs(path, conn, monkeypatch, tool):
    incubate_track(monkeypatch)
    TOOL_CHECKS[tool](mcp_server.build_server(path, TAX, lambda: NOW), job_id(conn, "Lab"), "Lab", None)


def test_mcp_tools_do_not_offer_an_incubating_place_or_track(monkeypatch):
    """The lists a tool's form shows the model are built when the server starts, which is
    when a changed state takes effect on the live site (a deploy restarts it)."""
    import importlib
    incubate_city(monkeypatch)
    incubate_track(monkeypatch)
    try:
        importlib.reload(q)
        fresh = importlib.reload(mcp_server)
        assert "Chicago" not in fresh.Place.__args__ and "Berlin" in fresh.Place.__args__
        assert "research" not in fresh.Family.__args__ and "ai-engineer" in fresh.Family.__args__
    finally:
        monkeypatch.undo()
        importlib.reload(q)
        importlib.reload(mcp_server)


# --- the tools behind the site can see it --------------------------------------------------

def test_labelling_and_eval_tools_can_still_read_incubating_jobs(conn, monkeypatch):
    incubate_city(monkeypatch)
    incubate_track(monkeypatch)
    windy, lab = job_id(conn, "Windy"), job_id(conn, "Lab")
    everything = q.Filters(window="all")
    assert q.list_jobs(conn, everything, NOW)["total"] == 2
    seen = q.list_jobs(conn, everything, NOW, include_incubating=True)
    assert seen["total"] == 4
    assert next(j for j in seen["jobs"] if j["company"] == "Both")["places"] == ["Berlin", "Chicago"]
    assert q.list_jobs(conn, q.Filters(window="all", cities=("Chicago",)), NOW, include_incubating=True)["total"] == 2
    assert q.job_detail(conn, windy, NOW) is None
    assert q.job_detail(conn, windy, NOW, include_incubating=True)["places"] == ["Chicago"]
    assert q.job_detail(conn, lab, NOW, include_incubating=True)["family"] == "research"
    assert {g["label"] for g in q.proposed_skills(conn)} == set()
    assert {g["label"] for g in q.proposed_skills(conn, include_incubating=True)} == {"Zig", "Mojo"}
    # The stored rows themselves are what the sampling scripts read: untouched.
    assert conn.execute("SELECT count(*) FROM job j JOIN job_place p ON p.job_id = j.id"
                        " WHERE p.place = 'Chicago'").fetchone()[0] == 2


def test_with_nothing_incubating_the_public_rule_adds_nothing_to_a_query(monkeypatch):
    """Every place and track live: each query runs exactly as it did before this rule existed."""
    monkeypatch.setattr(scope, "PLACE_STATE", {p: scope.LIVE for p in scope.PLACE_STATE})
    monkeypatch.setattr(scope, "TRACKS", {t: dataclasses.replace(v, state=scope.LIVE) for t, v in scope.TRACKS.items()})
    # What is left is the one rule that has nothing to do with incubating: no job whose
    # link goes to a site known for fake postings (HIR-441).
    rule, params = q.public_clause()
    assert params == list(ingest.BLOCKED_SITES) and rule.startswith("NOT EXISTS (SELECT 1 FROM job_source")
    assert "job_place" not in rule and "family" not in rule
    assert q.job_set_clause(q.Filters(window="all"), NOW, include_legacy=True) == (rule, params)
