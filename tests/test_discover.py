"""discover-boards: harvest, exclusion, classification, approval writes, and the guards.
Every network call is injected; nothing here touches the network."""

import json
from pathlib import Path

import pytest

import app.__main__ as cli
from app import discover
from app.sources import Posting, brave

FIXTURES = Path(__file__).parent / "fixtures" / "search"
CONFIG = {"count": 20, "domains": ["jobs.lever.co", "jobs.ashbyhq.com"], "queries": ['"AI engineer" Berlin']}
FEEDS_DOC = {"_comment": "c", "feeds": [
    {"type": "arbeitnow", "enabled": True},
    {"type": "lever", "enabled": True, "token": "vestiairecollective", "company": "Vestiaire"},
    {"type": "greenhouse", "enabled": False, "token": "bluefishai", "company": "Bluefish"},
]}
REJECTED_DOC = {"_comment": "c", "boards": [{"source": "ashby", "token": "cortea", "reason": "stale", "date": "2026-10-19"}]}

URLS = [
    "https://jobs.lever.co/vestiairecollective/0a1b2c3d-1111-2222-3333-444455556666",   # known
    "https://job-boards.greenhouse.io/BluefishAI/jobs/123",                            # known (disabled), case
    "https://jobs.ashbyhq.com/cortea/0a1b2c3d-1111-2222-3333-444455556666",            # rejected
    "https://jobs.ashbyhq.com/newco/0a1b2c3d-1111-2222-3333-444455556666",             # new
    "https://jobs.ashbyhq.com/newco/0a1b2c3d-9999-2222-3333-444455556666",             # same board again
    "https://jobs.lever.co/quietco/0a1b2c3d-1111-2222-3333-444455556666",              # new, nothing relevant
    "https://jobs.lever.co/deadco/0a1b2c3d-1111-2222-3333-444455556666",               # new, fetch fails
    "https://jobs.ashbyhq.com/newco",                                                  # board page, no job id
    "https://example.com/careers/ai-engineer",                                         # not an ATS
]


def posting(title, location):
    return Posting("ashby", "x", "u", "Co", title, location, "text")


BOARDS = {
    ("ashby", "newco"): [posting("Senior AI Engineer", "Berlin, Germany"), posting("Sales Lead", "Berlin"),
                         posting("ML Engineer", "Remote")],
    ("lever", "quietco"): [posting("Account Executive", "Berlin"), posting("AI Engineer", "Munich")],
}


def fetch_board(source, token):
    if (source, token) == ("lever", "deadco"):
        raise OSError("HTTP Error 404")
    return BOARDS[(source, token)]


def test_search_queries_cross_domains_and_queries():
    assert discover.search_queries(CONFIG) == ['site:jobs.lever.co "AI engineer" Berlin',
                                               'site:jobs.ashbyhq.com "AI engineer" Berlin']


def test_harvest_dedups_boards_and_counts_urls_that_name_no_board():
    boards, unparsed = discover.harvest(URLS)
    assert boards == [("lever", "vestiairecollective"), ("greenhouse", "bluefishai"), ("ashby", "cortea"),
                      ("ashby", "newco"), ("lever", "quietco"), ("lever", "deadco")]
    assert unparsed == 2


def test_known_includes_disabled_feeds_and_rejected_are_excluded():
    boards, _ = discover.harvest(URLS)
    new = discover.new_boards(boards, discover.known_boards(FEEDS_DOC), discover.rejected_boards(REJECTED_DOC))
    assert new == [("ashby", "newco"), ("lever", "quietco"), ("lever", "deadco")]


def test_relevant_roles_need_the_title_filter_and_a_tracked_city():
    assert discover.relevant_roles(BOARDS[("ashby", "newco")]) == ["Senior AI Engineer (Berlin)"]
    assert discover.relevant_roles(BOARDS[("lever", "quietco")]) == []


def test_run_classifies_and_reports_failures_without_stopping():
    seen = []
    r = discover.run(CONFIG, FEEDS_DOC, REJECTED_DOC,
                     search=lambda q: seen.append(q) or (URLS if "lever" in q else []), fetch_board=fetch_board)
    assert len(seen) == 2 and r.queries[1][1] == 0
    assert (r.urls, r.found, r.known, r.rejected, r.unparsed) == (9, 6, 2, 1, 2)
    by = {c.board: c for c in r.candidates}
    assert by[("ashby", "newco")].relevant == ["Senior AI Engineer (Berlin)"] and by[("ashby", "newco")].total == 3
    assert by[("lever", "quietco")].relevant == [] and by[("lever", "quietco")].error is None
    assert by[("lever", "deadco")].error == "OSError: HTTP Error 404"
    out = "\n".join(discover.report_lines(r))
    assert 'site:jobs.ashbyhq.com "AI engineer" Berlin → 0 results' in out
    assert "new boards with relevant roles: 1\n  ashby:newco: 3 jobs, 1 relevant: Senior AI Engineer (Berlin)" in out
    assert '{"type": "ashby", "enabled": true, "token": "newco", "company": "newco"}' in out
    assert "nothing relevant now: 1\n  lever:quietco: 2 jobs, 0 relevant" in out
    assert "board fetch FAILED: 1\n  lever:deadco: OSError: HTTP Error 404" in out
    assert "vestiairecollective" not in out.split("searches;")[1] and "bluefishai" not in out


def test_add_and_reject_write_their_files_once(tmp_path):
    feeds, rejected = tmp_path / "feeds.json", tmp_path / "rejected.json"
    feeds.write_text(json.dumps(FEEDS_DOC))
    rejected.write_text(json.dumps(REJECTED_DOC))
    assert discover.add_board(("ashby", "newco"), feeds) is True
    assert discover.add_board(("ashby", "newco"), feeds) is False
    assert discover.add_board(("greenhouse", "bluefishai"), feeds) is False         # disabled still counts
    assert json.loads(feeds.read_text())["feeds"][-1] == {"type": "ashby", "enabled": True, "token": "newco",
                                                          "company": "newco"}
    assert discover.reject_board(("lever", "quietco"), "no Berlin AI roles", "2026-10-19", rejected) is True
    assert discover.reject_board(("lever", "quietco"), "again", "2026-10-20", rejected) is False
    assert json.loads(rejected.read_text())["boards"][-1] == {"source": "lever", "token": "quietco",
                                                              "reason": "no Berlin AI roles", "date": "2026-10-19"}
    assert json.loads(rejected.read_text())["_comment"] == "c"


def test_parse_board_validates_source():
    assert discover.parse_board("Greenhouse:x".lower()) == ("greenhouse", "x")
    assert discover.parse_board("join:Motor-AI") == ("join", "motor-ai")
    for bad in ("intercom", "workday:acme", ":x"):
        with pytest.raises(ValueError):
            discover.parse_board(bad)


def test_cli_without_key_exits_cleanly(monkeypatch):
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)
    with pytest.raises(SystemExit) as e:
        cli.main(["discover-boards"])
    assert "BRAVE_API_KEY is not set" in str(e.value)


def test_cli_add_and_reject_write_files_and_do_not_search(tmp_path, monkeypatch, capsys):
    feeds, rejected = tmp_path / "feeds.json", tmp_path / "rejected.json"
    feeds.write_text(json.dumps(FEEDS_DOC))
    rejected.write_text(json.dumps(REJECTED_DOC))
    monkeypatch.setattr(discover.add_board, "__defaults__", (feeds, None))
    monkeypatch.setattr(discover.reject_board, "__defaults__", (rejected,))
    monkeypatch.setattr(brave, "fetch", lambda *a, **k: (_ for _ in ()).throw(AssertionError("searched")))
    cli.main(["discover-boards", "--add", "ashby:newco"])
    cli.main(["discover-boards", "--reject", "lever:quietco", "--reason", "no Berlin AI roles"])
    out = capsys.readouterr().out
    assert "ashby:newco: added to config/feeds.json" in out
    assert "lever:quietco: added to config/boards_rejected.json" in out
    assert json.loads(feeds.read_text())["feeds"][-1]["token"] == "newco"
    assert json.loads(rejected.read_text())["boards"][-1]["reason"] == "no Berlin AI roles"


def test_brave_parse_reads_the_recorded_response():
    """Fixtures recorded from live Brave calls on 2026-10-19 (see app/sources/brave.py)."""
    payload = json.loads((FIXTURES / "brave.json").read_text())
    urls = brave.parse(payload)
    assert urls == [r["url"] for r in payload["web"]["results"]] and len(urls) == 5
    assert all(u.startswith("https://jobs.ashbyhq.com/") for u in urls)   # site: was applied
    boards, unparsed = discover.harvest(urls)
    assert ("ashby", "nelly") in boards and ("ashby", "perplexity") in boards and unparsed == 0


def test_brave_parse_zero_results_is_empty_not_an_error():
    assert brave.parse(json.loads((FIXTURES / "brave_zero.json").read_text())) == []


def test_brave_parse_fails_loudly_on_any_other_shape():
    for bad in ({"type": "ErrorResponse", "error": {"code": "x"}},
                {"type": "search", "query": {}, "web": {"type": "search"}},
                {"results": []}):
        with pytest.raises(brave.ShapeError):
            brave.parse(bad)
