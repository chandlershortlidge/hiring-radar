"""HIR-324: a job added on the dashboard from a company whose board we do not collect.

Before this, "Add a job" stored the one posting and stopped, so the company's next posting
was missed again; and a pasted or screenshotted job recorded no check even when its link
was given, so it never counted as a miss. These tests cover the board being recorded, the
screen that keeps recruiters and job boards out, the one ticket that asks for the waiting
boards, the three add paths, and what the reply tells the drawer.
"""

import json

import pytest
from fastapi.testclient import TestClient

from app import boards_to_add as bta
from app import db, misses
from app.api import create_app
from app.check import (LINKEDIN_ONLY, NOT_IN_SOURCES, AtsRef, CheckResult, board_not_added,
                       check_posting, check_url, diagnose, log_check, parse_ats_url)
from app.ingest import ingest_one
from app.sources import Posting
from tests.test_api import TAX, FakeClient

NOW = "2026-11-20T10:00:00Z"
FEEDS = [{"type": "greenhouse", "enabled": True, "token": "acme", "company": "Acme"},
         {"type": "lever", "enabled": False, "token": "paused", "company": "Paused"},
         {"type": "arbeitnow", "enabled": True}]
ON = [f for f in FEEDS if f["enabled"]]            # what a check is handed: the feeds switched on
NEW = "https://jobs.ashbyhq.com/Nordlicht/0a1b2c3d-0000-4000-8000-000000000001"
NEW_2 = "https://jobs.ashbyhq.com/nordlicht/0a1b2c3d-0000-4000-8000-000000000002"
JD = ("Nordlicht is hiring an AI Engineer in Berlin. You build LLM agents in Python, run RAG "
      "pipelines over vector databases and ship them to production every week. ") * 2


def posting(company="Nordlicht", url=NEW, text=JD, source="paste"):
    return Posting(source, "", url, company, "AI Engineer", "Berlin", text)


def missing(url=NEW, company="Nordlicht"):
    """A check that ended in "this company's board is not in our list"."""
    p = posting(company, url)
    ref = parse_ats_url(url)
    return CheckResult(url=url, verdict="not_found", how="", posting=p,
                       diagnosis=diagnose(p, ref, ON, None), missing_board=board_not_added(ref, ON))


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


# --- the structured board ----------------------------------------------------------------

@pytest.mark.parametrize("ref", [
    AtsRef("ashby", "nordlicht", "1"),      # a board we do not collect
    AtsRef("greenhouse", "acme", "1"),      # one we do
    AtsRef("greenhouse", None, "1"),        # an embed link that does not name the board
    None,                                   # not a board link at all
])
def test_the_structured_board_says_exactly_what_the_sentence_says(ref):
    """The board is stored from `board_not_added`, never read back out of the diagnosis;
    the two must not be able to disagree."""
    sentence = diagnose(posting(), ref, ON, None)
    assert (board_not_added(ref, ON) is not None) == ("is not in config/feeds.json" in sentence)
    if ref and ref.token == "nordlicht":
        assert board_not_added(ref, ON) == ("ashby", "nordlicht")


def test_a_link_check_carries_the_board_it_found_missing(conn):
    """The whole check, as "Add a job" by link runs it, with the board's answer handed in."""
    on_board = Posting("ashby", "0a1b2c3d-0000-4000-8000-000000000001", NEW, "", "AI Engineer", "Berlin", JD)
    r = check_url(conn, NEW, ON, fetch_page=lambda u: pytest.fail("fetched the page"),
                  fetch_board=lambda source, token: [on_board])
    assert r.verdict == "not_found" and r.missing_board == ("ashby", "Nordlicht")
    assert bta.standing(r, FEEDS, set()) == (bta.QUEUED, ("ashby", "Nordlicht"))
    polled = check_url(conn, "https://boards.greenhouse.io/acme/jobs/7", ON, fetch_page=lambda u: "<title>x</title>",
                       fetch_board=lambda source, token: [])
    assert polled.missing_board is None


# --- the check that fetches nothing (pasted text, screenshots) -----------------------------

def test_a_pasted_posting_on_a_board_we_do_not_collect_names_the_board(conn):
    r = check_posting(conn, NEW, posting(), ON)
    assert r.verdict == "not_found" and r.missing_board == ("ashby", "Nordlicht")
    assert r.diagnosis.startswith("board ashby:Nordlicht is not in config/feeds.json")


def test_a_pasted_posting_we_already_store_is_found_by_its_text(conn):
    stored = ingest_one(conn, Posting("arbeitnow", "a1", "https://x/1", "Nordlicht", "AI Engineer", "Berlin", JD), NOW)
    url = "https://www.linkedin.com/jobs/view/123"
    r = check_posting(conn, url, posting(url=url), ON)
    assert r.verdict == "found" and r.job_id == stored.job_id and r.sources == ["arbeitnow"]
    assert r.missing_board is None


def test_a_pasted_linkedin_posting_we_do_not_store_is_a_linkedin_miss(conn):
    url = "https://www.linkedin.com/jobs/view/123"
    r = check_posting(conn, url, posting(url=url), ON)
    log_check(conn, r, "linkedin", NOW)
    assert r.verdict == "not_found" and r.missing_board is None
    assert [(m.url, m.reason) for m in misses.records(conn)] == [(url, LINKEDIN_ONLY)]


# --- where a board stands, and the screen --------------------------------------------------

def test_a_missing_employer_board_is_queued():
    assert bta.standing(missing(), FEEDS, set()) == (bta.QUEUED, ("ashby", "Nordlicht"))


@pytest.mark.parametrize("url, company", [
    ("https://jobs.lever.co/toprecruiting/0a1b2c3d-0000-4000-8000-000000000001", "Top"),   # the board's name
    (NEW, "Nordlicht Staffing GmbH"),                                                        # the company's name
])
def test_a_recruiter_or_job_board_is_never_queued(url, company):
    """The same word list that keeps agencies out of board discovery (app/discover.py)."""
    from app.discover import agency_word
    r = missing(url, company)
    assert agency_word(r.missing_board, company)          # the shared screen matches…
    assert bta.standing(r, FEEDS, set()) == (bta.NONE, None)   # …so nothing is queued


def test_a_board_rejected_before_is_never_queued():
    assert bta.standing(missing(), FEEDS, {("ashby", "nordlicht")}) == (bta.NONE, None)


def test_a_board_switched_off_in_the_list_is_left_off():
    url = "https://jobs.lever.co/paused/0a1b2c3d-0000-4000-8000-000000000001"
    r = missing(url, "Paused")
    assert r.missing_board == ("lever", "paused")         # the check only sees feeds switched on
    assert bta.standing(r, FEEDS, set()) == (bta.NONE, None)


def test_a_posting_on_a_board_we_collect_is_collected_and_any_other_link_is_none():
    on_board = CheckResult(url="https://boards.greenhouse.io/acme/jobs/7", verdict="not_found", how="")
    own_site = CheckResult(url="https://nordlicht.example/careers/ai-engineer", verdict="not_found", how="")
    assert bta.standing(on_board, FEEDS, set()) == (bta.COLLECTED, None)
    assert bta.standing(own_site, FEEDS, set()) == (bta.NONE, None)


def test_a_board_is_recorded_once_however_its_name_is_spelled(conn):
    assert bta.note(conn, missing(NEW), FEEDS, set(), NOW) == bta.QUEUED
    assert bta.note(conn, missing(NEW_2), FEEDS, set(), NOW) == bta.QUEUED
    rows = conn.execute("SELECT source, token, company, url, ticket FROM board_to_add").fetchall()
    assert [tuple(r) for r in rows] == [("ashby", "Nordlicht", "Nordlicht", NEW, None)]


def test_a_screened_board_leaves_no_row(conn):
    assert bta.note(conn, missing(NEW, "Nordlicht Staffing GmbH"), FEEDS, set(), NOW) == bta.NONE
    assert conn.execute("SELECT count(*) FROM board_to_add").fetchone()[0] == 0


# --- the ticket ----------------------------------------------------------------------------

def other_board():
    return missing("https://boards.greenhouse.io/suedwind/jobs/42", "Südwind")


def test_one_ticket_asks_for_every_waiting_board_and_they_are_not_asked_for_twice(conn):
    bta.note(conn, missing(), FEEDS, set(), NOW)
    bta.note(conn, other_board(), FEEDS, set(), NOW)
    posts = []

    def post(title, body):
        posts.append((title, body))
        return "HIR-900"

    assert bta.file_ticket(conn, FEEDS, post, NOW, log=lambda *_: None) == "HIR-900"
    (title, body), = posts
    assert "Nordlicht, Südwind" in title
    # The exact lines for feeds.json, as the link checker would add them.
    assert json.dumps({"type": "ashby", "enabled": True, "token": "Nordlicht", "company": "Nordlicht"}) in body
    assert '{"type": "greenhouse", "enabled": true, "token": "suedwind", "company": "Südwind"}' in body
    assert "--only ashby:Nordlicht --only greenhouse:suedwind" in body
    assert NEW in body
    for heading in ("## Build", "## Done when", "## Out of scope"):
        assert heading in body
    assert [tuple(r) for r in conn.execute("SELECT ticket, filed_at FROM board_to_add")] == [("HIR-900", NOW)] * 2
    assert bta.file_ticket(conn, FEEDS, post, NOW, log=lambda *_: None) is None and len(posts) == 1


def test_a_board_that_reached_the_list_some_other_way_is_not_asked_for(conn):
    bta.note(conn, missing(), FEEDS, set(), NOW)
    added = FEEDS + [{"type": "ashby", "enabled": True, "token": "nordlicht", "company": "Nordlicht"}]
    assert bta.waiting(conn, added) == []
    assert bta.file_ticket(conn, added, lambda *a: pytest.fail("posted"), NOW) is None


def test_without_a_linear_key_or_when_linear_fails_the_board_keeps_waiting(conn):
    bta.note(conn, missing(), FEEDS, set(), NOW)
    assert bta.file_ticket(conn, FEEDS, None, NOW, log=lambda *_: None) is None

    def down(title, body):
        raise RuntimeError("Linear refused the issue")

    with pytest.raises(RuntimeError):
        bta.file_ticket(conn, FEEDS, down, NOW, log=lambda *_: None)
    assert len(bta.waiting(conn, FEEDS)) == 1            # still there for the morning retry
    assert bta.file_ticket(conn, FEEDS, lambda *a: "HIR-901", NOW, log=lambda *_: None) == "HIR-901"


# --- the three ways to add a job -------------------------------------------------------------

@pytest.fixture
def site(tmp_path, monkeypatch):
    path = tmp_path / "t.db"
    posts = []

    def post(title, body):
        posts.append(title)
        return f"HIR-9{len(posts):02d}"

    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    monkeypatch.setattr("app.api.load_feeds", lambda: ON)
    monkeypatch.setattr("app.api.boards_to_add.load_config", lambda: (FEEDS, set()))
    client = TestClient(create_app(path, TAX, client_factory=FakeClient, board_poster=post))
    return client, posts, lambda: db.connect(path)


def boards(connect):
    return [tuple(r) for r in connect().execute("SELECT source, token, ticket FROM board_to_add")]


def test_adding_by_link_from_a_board_we_do_not_collect_records_it_and_files_the_ticket(site, monkeypatch):
    client, posts, connect = site
    monkeypatch.setattr("app.api.check_url", lambda *a, **k: missing())
    r = client.post("/api/add/url", json={"url": NEW}).json()
    assert r["outcome"] == "added" and r["board"] == "queued"
    assert boards(connect) == [("ashby", "Nordlicht", "HIR-901")]
    assert len(posts) == 1 and "Nordlicht" in posts[0]
    # The check is in the missed-job count, under "company was not in our sources".
    assert [(m.url, m.reason) for m in misses.records(connect())] == [(NEW, NOT_IN_SOURCES)]


def test_a_second_job_from_the_same_company_files_no_second_ticket(site, monkeypatch):
    client, posts, connect = site
    monkeypatch.setattr("app.api.check_url", lambda *a, **k: missing())
    client.post("/api/add/url", json={"url": NEW})
    monkeypatch.setattr("app.api.check_url", lambda *a, **k: missing(NEW_2))
    r = client.post("/api/add/url", json={"url": NEW_2}).json()
    assert r["board"] == "queued" and len(posts) == 1 and len(boards(connect)) == 1


def test_adding_by_link_from_a_page_with_no_board_says_it_cannot_be_collected(site, monkeypatch):
    client, posts, connect = site
    url = "https://nordlicht.example/careers/ai-engineer"
    p = posting(url=url, source="url")
    monkeypatch.setattr("app.api.check_url", lambda *a, **k: CheckResult(
        url=url, verdict="not_found", how="", posting=p, diagnosis=diagnose(p, None, ON, None)))
    r = client.post("/api/add/url", json={"url": url}).json()
    assert r["outcome"] == "added" and r["board"] == "none"
    assert boards(connect) == [] and posts == []


def test_a_failed_ticket_never_fails_the_add(tmp_path, monkeypatch, capsys):
    def down(title, body):
        raise RuntimeError("Linear is down")

    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    monkeypatch.setattr("app.api.load_feeds", lambda: ON)
    monkeypatch.setattr("app.api.boards_to_add.load_config", lambda: (FEEDS, set()))
    monkeypatch.setattr("app.api.check_url", lambda *a, **k: missing())
    path = tmp_path / "t.db"
    client = TestClient(create_app(path, TAX, client_factory=FakeClient, board_poster=down))
    r = client.post("/api/add/url", json={"url": NEW})
    assert r.status_code == 200 and r.json()["outcome"] == "added" and r.json()["board"] == "queued"
    assert "could not file the boards-to-add ticket" in capsys.readouterr().out
    assert len(bta.waiting(db.connect(path), FEEDS)) == 1     # the morning run files it


PASTE = {"text": JD, "company": "Nordlicht", "title": "AI Engineer", "location": "Berlin", "found_via": "linkedin"}


def test_a_pasted_job_with_a_link_counts_as_a_miss_and_one_without_does_not(site):
    client, posts, connect = site
    r = client.post("/api/add/text", json=PASTE).json()
    assert r["outcome"] == "added" and r["board"] is None
    assert misses.records(connect()) == []                 # no link: nothing recorded, as before

    other = {**PASTE, "company": "Südwind", "text": JD.replace("Nordlicht", "Südwind"),
             "url": "https://www.linkedin.com/jobs/view/123"}
    r = client.post("/api/add/text", json=other).json()
    assert r["outcome"] == "added" and r["board"] == "none"
    (m,) = misses.records(connect())
    assert (m.url, m.reason, m.company) == (other["url"], LINKEDIN_ONLY, "Südwind")
    assert connect().execute("SELECT found_via, verdict FROM url_check").fetchone()[:] == ("linkedin", "not_found")


def test_a_pasted_job_whose_link_is_on_a_board_we_do_not_collect_queues_the_board(site):
    client, posts, connect = site
    r = client.post("/api/add/text", json={**PASTE, "url": NEW}).json()
    assert r["outcome"] == "added" and r["board"] == "queued"
    assert boards(connect) == [("ashby", "Nordlicht", "HIR-901")]
    assert [m.reason for m in misses.records(connect())] == [NOT_IN_SOURCES]


def test_a_link_that_is_not_a_link_records_nothing(site):
    client, posts, connect = site
    r = client.post("/api/add/text", json={**PASTE, "url": "see linkedin"}).json()
    assert r["outcome"] == "added" and r["board"] is None and misses.records(connect()) == []


def test_a_screenshot_with_a_link_counts_as_a_miss_and_one_without_does_not(site):
    client, posts, connect = site
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32
    meta = {"company": "Nordlicht", "title": "AI Engineer", "location": "Berlin"}
    r = client.post("/api/add/screenshot", params={**meta, "url": NEW},
                    files={"file": ("shot.png", png, "image/png")}).json()
    assert r["outcome"] == "added" and r["board"] == "queued"
    assert [m.reason for m in misses.records(connect())] == [NOT_IN_SOURCES]

    r = client.post("/api/add/screenshot", params={**meta, "company": "Südwind"},
                    files={"file": ("shot2.png", png + b"\x01", "image/png")}).json()
    assert r["outcome"] == "added" and r["board"] is None
    assert len(misses.records(connect())) == 1


# --- the morning retry -----------------------------------------------------------------------

def test_the_morning_run_files_a_board_the_dashboard_could_not(conn, monkeypatch):
    """Recorded on a database copy, with Linear unreachable at the time of the add: the
    caretaker's next run files the ticket, once."""
    from app import caretaker_run
    monkeypatch.setattr("app.caretaker_run.boards_to_add.load_config", lambda: (FEEDS, set()))
    bta.note(conn, missing(), FEEDS, set(), NOW)
    posted = []
    post = lambda title, body: posted.append(title) or "HIR-902"   # noqa: E731
    caretaker_run.report(conn, "2026-11-19", post, log=lambda *_: None)   # a Thursday: no weekly post
    caretaker_run.report(conn, "2026-11-19", post, log=lambda *_: None)
    assert posted == ["We miss later jobs from Nordlicht: add its job board to what we collect"]
    assert bta.waiting(conn, FEEDS) == []
