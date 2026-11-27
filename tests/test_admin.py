"""The admin page (HIR-398): every place and career track with its state and its numbers,
the month's spending, and the Monday summary's lines from the same rows.

One database with an incubating city (Chicago) and an incubating track (research), filled
through the collector's own path. The page shows both; the public API and every MCP tool
show neither. The page is private because the web server asks for the password in front
of it, so that is tested where it is decided: deploy/Caddyfile.
"""

import asyncio
import fnmatch
import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from mcp.server.mcpserver.exceptions import ToolError

from app import admin, caretaker, db, ingest, mcp_server, poll, scope
from app import caretaker_run as run
from app.api import create_app
from app.extract import DEFAULT_MODEL, Extraction, Seniority, extractor_version
from app.pipeline import store_extraction
from app.sources import Posting, jsearch
from tests.test_api import TAX
from tests.test_incubating import BODY, TOOL_CHECKS, collect, companies, incubate_city, incubate_track, job_id
from tests.test_queries import NOW, ts

ROOT = Path(__file__).resolve().parent.parent
MONDAY = "2026-11-16"
VERSION = extractor_version(TAX, DEFAULT_MODEL)


@pytest.fixture
def path(tmp_path, monkeypatch):
    """Berlin is live. Chicago holds four postings: one open and read (Windy), one shared
    with Berlin (Both), one that closed weeks ago (Gone) and one never read (Fresh, from a
    second kind of source). Research holds one, in Berlin (Lab)."""
    path = tmp_path / "t.db"
    conn = db.connect(path)
    db.migrate(conn)
    collect(conn, "Acme", "AI Engineer", "Berlin", ("python", "rag"))
    collect(conn, "Windy", "AI Engineer", "Chicago, IL", ("python", "aws"))
    collect(conn, "Both", "ML Engineer", "Berlin; Chicago, IL", ("python",))
    collect(conn, "Lab", "Research Engineer, LLMs", "Berlin", ("python", "docker"))
    gone = Posting("greenhouse", "gone-1", "https://example.com/gone", "Gone", "AI Engineer", "Chicago, IL",
                   "Gone is hiring a AI Engineer." + BODY)
    closed = ingest.ingest_one(conn, gone, ts(30))
    store_extraction(conn, closed.job_id, Extraction(seniority=Seniority(None, None, None), mentions=[],
                                                     extractor_version="t", taxonomy_version=3))
    fresh = Posting("lever", "fresh-1", "https://example.com/fresh", "Fresh", "AI Engineer", "Chicago, IL",
                    "Fresh is hiring a AI Engineer." + BODY)
    ingest.ingest_one(conn, fresh, ts(2))
    ingest.ingest_one(conn, fresh, ts(0))
    conn.close()
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    monkeypatch.setattr("app.ingest.now_iso", lambda: NOW)
    incubate_city(monkeypatch)
    incubate_track(monkeypatch)
    return path


@pytest.fixture
def api(path):
    return TestClient(create_app(path, TAX, skill_added={}))


@pytest.fixture
def conn(path):
    c = db.connect(path)
    yield c
    c.close()


def page_rows(html_text: str) -> dict[str, list[str]]:
    """The page's table rows by their first cell: what a person reads off the page."""
    rows = {}
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html_text, re.S):
        cells = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if cells:
            rows[cells[0]] = cells
    return rows


def by_name(rows: list[admin.Row]) -> dict[str, admin.Row]:
    return {r.name: r for r in rows}


# --- the rows -----------------------------------------------------------------------------

def test_there_is_one_row_per_collected_place_and_per_career_track_in_the_lists_order(conn):
    rows = admin.overview(conn, NOW, VERSION)
    assert [r.name for r in rows if r.kind == admin.PLACE] == list(scope.PLACE_STATE)
    assert [r.name for r in rows if r.kind == admin.TRACK] == list(scope.TRACKS)


def test_an_incubating_citys_row_counts_what_is_stored_open_and_waiting(conn):
    chicago = by_name(admin.overview(conn, NOW, VERSION))["Chicago"]
    assert (chicago.state, chicago.read) == (scope.INCUBATING, scope.READ_NOW)
    assert chicago.stored == 4                       # Windy, Both, Gone, Fresh
    assert chicago.open_now == 3                     # Gone was last seen 30 days ago
    # Fresh was never read; Windy and Both are open and were read by an older extractor.
    # Gone was read and has closed, so nothing will read it again.
    assert chicago.waiting == 3
    assert (chicago.first_day, chicago.last_day) == (ts(40)[:10], ts(0)[:10])
    assert chicago.days == 41                        # both ends counted
    assert chicago.sources == 2                      # greenhouse and lever
    assert chicago.ready is not None


def test_a_job_read_at_the_current_extractor_is_not_waiting(conn):
    before = by_name(admin.overview(conn, NOW, VERSION))["Chicago"].waiting
    conn.execute("UPDATE job SET extracted_version = ? WHERE company = 'Windy'", (VERSION,))
    assert by_name(admin.overview(conn, NOW, VERSION))["Chicago"].waiting == before - 1


def test_a_job_posted_for_two_places_counts_in_both_rows_and_a_tracks_row_counts_its_jobs(conn):
    rows = by_name(admin.overview(conn, NOW, VERSION))
    assert rows["Berlin"].stored == 3 and rows["Berlin"].state == scope.LIVE      # Acme, Both, Lab
    assert rows["Berlin"].ready is None                                            # live: no hint
    assert rows["research"].stored == 1 and rows["research"].state == scope.INCUBATING
    assert rows["ai-engineer"].stored == 4                                         # Acme, Windy, Gone, Fresh


def test_a_place_with_nothing_stored_has_no_days_and_no_dates(conn):
    austin = by_name(admin.overview(conn, NOW, VERSION))["Austin"]
    assert (austin.stored, austin.open_now, austin.waiting, austin.days, austin.sources) == (0, 0, 0, 0, 0)
    assert austin.first_day is None and austin.last_day is None


def test_the_read_mode_is_the_lists_own(conn, monkeypatch):
    monkeypatch.setitem(scope.PLACE_READ, "Chicago", scope.READ_LATER)
    monkeypatch.setitem(scope.TRACKS, "research", scope.Track(scope.INCUBATING, read=scope.READ_LATER))
    rows = by_name(admin.overview(conn, NOW, VERSION))
    assert rows["Chicago"].read == scope.READ_LATER and rows["research"].read == scope.READ_LATER
    assert rows["Berlin"].read == scope.READ_NOW
    # A job held back on purpose is still counted as waiting: the page has one number.
    conn.execute("UPDATE job SET extracted_version = NULL WHERE company = 'Lab'")
    assert by_name(admin.overview(conn, NOW, VERSION))["research"].waiting == 1


# --- the ready hint -------------------------------------------------------------------------

def _evals(tmp_path, runs: dict[str, list[dict]], goldens: dict[str, dict]) -> Path:
    for run_id, picks in runs.items():
        (tmp_path / "labeling" / run_id).mkdir(parents=True)
        (tmp_path / "labeling" / run_id / "picks.json").write_text(json.dumps(picks))
    (tmp_path / "goldens").mkdir()
    for golden_id, extra in goldens.items():
        (tmp_path / "goldens" / f"{golden_id}.json").write_text(json.dumps({"id": golden_id, **extra}))
    return tmp_path


def _pick(golden_id, place, title="AI Engineer"):
    return {"golden_id": golden_id, "place": place, "title": title, "job_id": 1}


def test_the_ready_hint_counts_reviewed_goldens_and_names_the_latest_sample_drawn_only_from_the_place(tmp_path, monkeypatch):
    incubate_city(monkeypatch)
    evals = _evals(tmp_path, {
        "20261101T100000Z_label": [_pick("golden_201", "Chicago"), _pick("golden_202", "Berlin")],   # mixed
        "20261105T100000Z_label": [_pick("golden_203", "Chicago"), _pick("golden_204", "Chicago")],  # Chicago only
        "20261109T100000Z_label": [_pick("golden_205", "Berlin")],
    }, {"golden_201": {}, "golden_203": {}, "golden_204": {"draft": True}, "golden_205": {}})
    ready = admin.readiness(admin.PLACE, "Chicago", admin.labelling_picks(evals), admin.reviewed_goldens(evals))
    # 201 and 203 are reviewed Goldens from Chicago; 204 is a draft; 202 and 205 are Berlin's.
    assert ready == admin.Ready(skill_list=None, goldens=2, launch_sample="2026-11-05")
    assert ready.text() == "skill list: the shared one; Goldens: 2; launch check sample: 2026-11-05"


def test_a_tracks_ready_hint_reads_the_track_off_the_title_and_the_skill_list_off_the_read_mode(tmp_path, monkeypatch):
    evals = _evals(tmp_path, {"20261105T100000Z_label": [
        _pick("golden_301", "Berlin", "Research Engineer, LLMs"), _pick("golden_302", "Berlin", "AI Engineer")]},
        {"golden_301": {}, "golden_302": {}})
    runs, goldens = admin.labelling_picks(evals), admin.reviewed_goldens(evals)
    monkeypatch.setitem(scope.TRACKS, "research", scope.Track(scope.INCUBATING, read=scope.READ_LATER))
    waiting = admin.readiness(admin.TRACK, "research", runs, goldens)
    assert waiting == admin.Ready(skill_list=False, goldens=1, launch_sample=None)
    assert waiting.text() == "skill list: not yet; Goldens: 1; launch check sample: none"
    monkeypatch.setitem(scope.TRACKS, "research", scope.Track(scope.INCUBATING))
    assert admin.readiness(admin.TRACK, "research", runs, goldens).skill_list is True


def test_a_labelling_record_that_cannot_be_read_does_not_stop_the_page(tmp_path):
    evals = _evals(tmp_path, {"20261105T100000Z_label": [_pick("golden_201", "Chicago")]}, {"golden_201": {}})
    (evals / "labeling" / "20261106T100000Z_label").mkdir()
    (evals / "labeling" / "20261106T100000Z_label" / "picks.json").write_text("{not json")
    (evals / "goldens" / "golden_999.json").write_text("{not json")
    assert [run_id for run_id, _ in admin.labelling_picks(evals)] == ["20261105T100000Z_label"]
    assert admin.reviewed_goldens(evals) == {"golden_201"}


def test_the_committed_labelling_records_and_goldens_are_readable():
    """The real files, so a change to their shape is noticed here and not on the page."""
    runs, goldens = admin.labelling_picks(), admin.reviewed_goldens()
    assert runs and goldens
    assert all("place" in p and "golden_id" in p and "title" in p for _, picks in runs for p in picks)
    assert admin.readiness(admin.PLACE, "Berlin", runs, goldens).goldens > 0


# --- the month's spending -----------------------------------------------------------------

def test_spending_reads_the_three_counters_for_the_month_and_names_each_limit(conn):
    usage = {"input_tokens": 1_000_000, "output_tokens": 100_000}
    for created, use in (("2026-10-05T08:00:00Z", usage), ("2026-10-06T08:00:00Z", {}),
                         ("2026-09-30T08:00:00Z", usage)):                  # last one: another month
        conn.execute("INSERT INTO extraction_log (job_id, extractor_version, taxonomy_version, model, created_at,"
                     " raw_output, usage, input_sha256) VALUES (NULL, 'v', 3, 'claude-sonnet-5-5', ?, '{}', ?, 'x')",
                     (created, json.dumps(use)))
    for day in ("2026-10-03", "2026-10-04", "2026-09-29"):
        poll.record_run(conn, {"type": "jsearch", "search": "AI engineer in Boston"}, [], day=day)
    conn.execute("INSERT INTO caretaker_log (day, mode, subject, finding, action, detail, data)"
                 " VALUES ('2026-10-07', 'report', 'caretaker', 'spend', 'none', 'Spent.', ?)",
                 (json.dumps({"eur": 0.05}),))
    conn.commit()
    model, searches, boards = admin.spend(conn, "2026-10")
    # 1M input at $2 and 100k output at $10 per million is $3.00, €2.79.
    assert model.used == "at most €2.79 (1 reading)"
    assert "no monthly limit" in model.limit and "€10" in model.limit
    assert "1 reading came with no token counts" in model.note
    assert (searches.used, searches.limit) == ("2 requests", f"{jsearch.MONTHLY_CAP:,} requests a month")
    assert boards.used == "€0.05 (about 10 searches)"
    assert boards.limit == f"€{caretaker.DAILY_CAP_EUR:.2f} a day"


def test_spending_with_nothing_recorded_is_all_zeros(conn):
    model, searches, boards = admin.spend(conn, "2026-10")
    assert model.used == "at most €0.00 (0 readings)" and "no token counts" not in model.note
    assert searches.used == "0 requests" and boards.used == "€0.00 (about 0 searches)"


# --- the page -----------------------------------------------------------------------------

def test_the_page_shows_the_incubating_city_and_track_and_the_public_site_and_mcp_show_neither(api, conn, path):
    r = api.get("/admin")
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/html")
    rows = page_rows(r.text)
    assert rows["Chicago"][1:6] == ["incubating", "now", "4", "3", "3"]
    assert rows["research"][1:4] == ["incubating", "now", "1"]
    assert rows["Berlin"][1] == "live" and rows["Berlin"][-1] == ""
    assert rows["Chicago"][-1].startswith("skill list: the shared one; Goldens: ")
    assert {"Model reading", "Google for Jobs searches (JSearch)", "Board searches (Brave)"} <= set(rows)

    # The public site: neither the city's own jobs nor the track's.
    assert companies(api) == {"Acme", "Both"}
    assert companies(api, city="Chicago") == set()
    assert api.get("/api/jobs", params={"family": "research"}).status_code == 422
    assert api.get("/api/stats").json()["jobs"] == 2
    # Every MCP tool: the jobs cannot be fetched, found or counted.
    server = mcp_server.build_server(path, TAX, lambda: NOW)
    assert {t.name for t in asyncio.run(server.list_tools())} == set(TOOL_CHECKS)
    for company in ("Lab", "Windy"):
        hidden = job_id(conn, company)
        with pytest.raises(ToolError, match=f"no job with id {hidden}"):
            asyncio.run(server.call_tool("get_job", {"job_id": hidden}))
    found = asyncio.run(server.call_tool("search_jobs", {"window": "all", "limit": 50})).structured_content
    assert {j["company"] for j in found["jobs"]} == {"Acme", "Both"}
    assert all("Chicago" not in j["places"] for j in found["jobs"])
    assert asyncio.run(server.call_tool("skill_demand", {"window": "all"})).structured_content["total"] == 2


def test_the_page_is_read_only_and_tells_search_engines_to_stay_away(api, conn):
    before = conn.execute("SELECT count(*), max(last_seen) FROM job").fetchone()[:]
    r = api.get("/admin")
    assert not re.search(r"<(form|button|input|script|a)\b", r.text)
    assert r.headers["x-robots-tag"] == "noindex, nofollow" and r.headers["cache-control"] == "no-store"
    assert 'name="robots" content="noindex, nofollow"' in r.text
    for method in ("post", "put", "patch", "delete"):
        assert getattr(api, method)("/admin").status_code == 405
    assert conn.execute("SELECT count(*), max(last_seen) FROM job").fetchone()[:] == before


def test_the_page_escapes_what_it_prints():
    row = admin.Row(admin.PLACE, "<b>x</b>", scope.LIVE, scope.READ_NOW, 1, 1, 0, "2026-10-01", "2026-10-02", 2, 1, None)
    out = admin.page([row], [admin.Spend("a&b", "<i>", "c", "d")], NOW)
    assert "<b>x</b>" not in out and "&lt;b&gt;x&lt;/b&gt;" in out and "a&amp;b" in out and "<i>" not in out


def test_nothing_a_visitor_can_reach_leads_to_the_page(api):
    """Not linked from the dashboard, not visited by the robot visitor, not in the API's
    own description, and not under /api."""
    web = ROOT / "web"
    public = [p for folder in (web / "src", web / "e2e", ROOT / ".github") for p in folder.rglob("*") if p.is_file()]
    public += [web / "index.html", *web.glob("public/*")]
    assert public
    for p in public:
        assert "/admin" not in p.read_text(errors="ignore"), f"{p} names the admin page"
    assert "admin" not in json.dumps(api.get("/openapi.json").json())
    assert api.get("/api/admin").status_code == 404


# --- the password -------------------------------------------------------------------------

def _site_directives(caddyfile: str) -> list[tuple[list[str], list[str]]]:
    """The directives directly inside the site block, as (the words of its first line,
    the lines of its block). Enough of the format for this file: one site, one directive
    a line, blocks opened by a trailing `{`."""
    out, depth, current = [], 0, None
    for raw in caddyfile.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if depth == 1 and line != "}":
            current = (line.rstrip("{").split(), [])
            out.append(current)
        elif depth >= 2 and current is not None:
            current[1].append(line)
        depth += line.endswith("{") - (line == "}")
    return out


def asks_for_password(caddyfile: str, path: str) -> bool:
    """Would the web server ask for the password before answering `path`? True when the
    `handle` block that takes the path holds a basic-auth directive, or the site asks for
    it everywhere. Blocks with a matcher are tried in order, the plain `handle` last."""
    directives = _site_directives(caddyfile)
    paths = {words[0]: words[2:] for words, _ in directives if words[0].startswith("@") and words[1:2] == ["path"]}
    for words, body in directives:
        if words[0].startswith("@") and not words[1:]:          # a matcher written as a block
            paths[words[0]] = [w for line in body if line.startswith("path ") for w in line.split()[1:]]
    auth = ("basicauth", "basic_auth")
    if any(words == [name] for words, _ in directives for name in auth):
        return True
    handles = [(words[1:], body) for words, body in directives if words[0] == "handle"]
    for matcher, body in sorted(handles, key=lambda h: not h[0]):
        patterns = paths.get(matcher[0], []) if matcher and matcher[0].startswith("@") else matcher
        if not matcher or any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns):
            return any(line.split()[0] in auth for line in body)
    return False


OPENED = """
example.org {
	@mcp path /mcp
	handle @mcp {
		reverse_proxy 127.0.0.1:8000
	}
	%s
	handle {
		reverse_proxy 127.0.0.1:8000
	}
}
"""
ADMIN_BLOCK = """@admin path /admin /admin/*
	handle @admin {
		basic_auth {
			chandler HASH
		}
		reverse_proxy 127.0.0.1:8000
	}"""


@pytest.mark.parametrize("address", ["/admin", "/admin/"])
def test_the_page_needs_the_admin_login(address):
    """The login is the web server's (decisions/2026-11-23-hir-398-…). When the dashboard
    is opened to the public (HIR-82) this fails until /admin keeps a password block."""
    caddyfile = (ROOT / "deploy" / "Caddyfile").read_text()
    assert asks_for_password(caddyfile, address), (
        f"deploy/Caddyfile would answer {address} without the password: give the admin page "
        "its own `handle` block with basic auth before opening the rest of the site")
    assert not asks_for_password(caddyfile, "/mcp")      # the check can tell an open path


def test_the_login_check_fails_on_a_site_opened_without_a_block_for_the_admin_page():
    assert not asks_for_password(OPENED % "", "/admin")
    assert asks_for_password(OPENED % ADMIN_BLOCK, "/admin")
    assert asks_for_password(OPENED % ADMIN_BLOCK, "/admin/x")
    assert not asks_for_password(OPENED % ADMIN_BLOCK, "/")
    assert not asks_for_password(OPENED % ADMIN_BLOCK, "/administrator")


# --- the Monday summary ---------------------------------------------------------------------

def test_the_monday_summary_has_one_line_per_incubating_place_or_track_with_the_pages_numbers(api, conn):
    posted = []
    run.report(conn, MONDAY, lambda title, body: posted.append(body) or "HIR-900", log=lambda *_: None, mode=None)
    [body] = posted
    section = body[body.index("# Collected in the background, not shown yet"):].split("\n#")[0]
    lines = [line for line in section.splitlines() if line.startswith("- ")]
    assert [line.split(" (")[0] for line in lines] == ["- Chicago", "- research", "- software-engineer"]

    page = page_rows(api.get("/admin").text)
    for line, name in zip(lines, ("Chicago", "research")):
        stored, open_now, waiting, first, last, days = page[name][3:9]
        said = re.search(r": ([\d,]+) postings? stored, ([\d,]+) open now, ([\d,]+) waiting to be read, "
                         r"([\d,]+) days? collected \((\S+) to (\S+)\)\. Ready\? (.*)\.$", line)
        assert said, line
        assert said.groups() == (stored, open_now, waiting, days, first, last, page[name][-1])
    assert "- Chicago (city): 4 postings stored, 3 open now, 3 waiting to be read, 41 days collected" in section
    assert "- research (career track): 1 posting stored, 1 open now, 1 waiting to be read, 41 days collected" in section


def test_with_nothing_incubating_the_monday_summary_says_nothing_about_it(conn, monkeypatch):
    monkeypatch.setitem(scope.PLACE_STATE, "Chicago", scope.LIVE)
    monkeypatch.setitem(scope.TRACKS, "research", scope.Track(scope.LIVE))
    monkeypatch.setitem(scope.TRACKS, "software-engineer", scope.Track(scope.LIVE, scope.SWE_PATTERN))
    assert run.incubating_text(conn, NOW) == ""
    posted = []
    run.report(conn, MONDAY, lambda title, body: posted.append(body) or "HIR-900", log=lambda *_: None, mode=None)
    assert "Collected in the background" not in posted[0]


def test_an_incubating_place_with_nothing_stored_yet_still_gets_its_line(conn, monkeypatch):
    monkeypatch.setitem(scope.PLACE_STATE, "Austin", scope.INCUBATING)
    assert "- Austin (city): nothing stored yet. Ready? skill list: the shared one" in run.incubating_text(conn, NOW)
