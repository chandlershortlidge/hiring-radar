"""discover-boards: harvest, exclusion, classification, approval writes, and the guards.
Every network call is injected; nothing here touches the network."""

import json
from pathlib import Path

import pytest

import app.__main__ as cli
from app import discover, ingest
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
                         posting("ML Engineer", "Remote - US"), posting("AI Engineer", "San Francisco, CA")],
    ("lever", "quietco"): [posting("Account Executive", "Berlin"), posting("AI Engineer", "Leipzig")],
}


def fetch_board(source, token):
    if (source, token) == ("lever", "deadco"):
        raise OSError("HTTP Error 404")
    return BOARDS[(source, token)]


def test_shipped_config_searches_for_every_active_city():
    """Switching a city on means discover-boards looks for its boards too (HIR-12, HIR-132).

    Reads ACTIVE_CITIES rather than a list of its own, so turning a city on without giving
    it a search query fails here instead of silently finding no boards for it.
    """
    import json

    from app.geo import ACTIVE_CITIES, REMOTE_EU

    queries = json.loads(discover.CONFIG_PATH.read_text())["queries"]
    for city in (c for c in ACTIVE_CITIES if c != REMOTE_EU):
        assert any(city in q for q in queries), city


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


def test_relevant_roles_need_the_title_filter_and_an_active_city():
    # Berlin and San Francisco count (HIR-12); "Sales Lead" fails the title filter and
    # "Remote - US" is not EU-remote.
    assert discover.relevant_roles(BOARDS[("ashby", "newco")]) == ["Senior AI Engineer (Berlin)",
                                                                   "AI Engineer (San Francisco)"]
    assert discover.relevant_roles(BOARDS[("lever", "quietco")]) == []


def test_run_classifies_and_reports_failures_without_stopping():
    seen = []
    r = discover.run(CONFIG, FEEDS_DOC, REJECTED_DOC,
                     search=lambda q: seen.append(q) or (URLS if "lever" in q else []), fetch_board=fetch_board)
    assert len(seen) == 2 and r.queries[1][1] == 0
    assert (r.urls, r.found, r.known, r.rejected, r.unparsed) == (9, 6, 2, 1, 2)
    by = {c.board: c for c in r.candidates}
    assert by[("ashby", "newco")].relevant == ["Senior AI Engineer (Berlin)",
                                               "AI Engineer (San Francisco)"] and by[("ashby", "newco")].total == 4
    assert by[("lever", "quietco")].relevant == [] and by[("lever", "quietco")].error is None
    assert by[("lever", "deadco")].error == "OSError: HTTP Error 404"
    out = "\n".join(discover.report_lines(r))
    assert 'site:jobs.ashbyhq.com "AI engineer" Berlin → 0 results' in out
    assert ("new boards with relevant roles: 1\n  ashby:newco: 4 jobs, 2 relevant: "
            "Senior AI Engineer (Berlin); AI Engineer (San Francisco)") in out
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


# --- launching a city: the written policy (HIR-132) ------------------------------------

def cand(token, relevant=0, total=20, error=None, source="ashby"):
    c = discover.Candidate((source, token))
    c.total, c.error = total, error
    c.relevant = [f"AI Engineer {i} (New York)" for i in range(relevant)]
    return c


def test_relevant_roles_counts_one_city_only_for_a_launch():
    """A board full of Berlin roles is no evidence it hires in New York."""
    postings = [posting("AI Engineer", "Berlin"), posting("ML Engineer", "New York, NY"),
                posting("AI Engineer", "San Francisco, CA")]
    assert len(discover.relevant_roles(postings)) == 3            # every active place
    assert discover.relevant_roles(postings, "New York") == ["ML Engineer (New York)"]


@pytest.mark.parametrize("token,word", [
    ("acme-recruiting", "recruit"),
    ("TopTalentPartners", "talentpartner"),
    ("hays", "hays"),
    ("jobleads", "jobleads"),
    ("bestStaffing", "staffing"),
])
def test_agency_names_are_recognized(token, word):
    assert discover.agency_word(("ashby", token)) == word


@pytest.mark.parametrize("token", ["openai", "anthropic", "asana", "distyl", "jupus"])
def test_employer_names_are_not_agencies(token):
    assert discover.agency_word(("ashby", token)) is None


def test_the_company_name_is_screened_too():
    assert discover.agency_word(("ashby", "xyz123"), "Randstad Deutschland") == "randstad"


def test_the_board_screen_and_the_ingest_screen_are_one_rule():
    """HIR-220: the word list lives in app/ingest.py and both screens read that one list,
    so adding a word changes the board policy and what gets stored together, on purpose."""
    assert discover.AGENCY_WORDS is ingest.AGENCY_WORDS
    assert discover.agency_word(("ashby", "bestStaffing")) == ingest.agency_name_word("bestStaffing")


def test_five_roles_is_the_line_and_fewer_is_left_unrecorded():
    """Chandler's SF policy: add at 5+, and never reject a small board (HIR-123)."""
    ds = {d.board[1]: d for d in discover.launch_decisions(
        [cand("big", relevant=5), cand("small", relevant=4), cand("none", relevant=0)])}
    assert ds["big"].verdict == "add"
    assert ds["small"].verdict == "too-few-roles"
    assert ds["none"].verdict == "too-few-roles"
    # "left unrecorded" is the point: nothing here is a rejection
    assert all(d.verdict != "reject" for d in ds.values())


def test_an_agency_is_skipped_even_with_plenty_of_roles():
    [d] = discover.launch_decisions([cand("globalstaffing", relevant=40)])
    assert d.verdict == "skip-agency" and "staffing" in d.why


def test_a_dead_board_is_reported_not_counted_as_too_few():
    [d] = discover.launch_decisions([cand("deadco", relevant=0, error="OSError: HTTP Error 404")])
    assert d.verdict == "failed" and "404" in d.why


def test_cost_estimate_tracks_the_postings_actually_read():
    one = discover.estimate_extraction_cost_eur(1)
    assert 0.005 < one < 0.05                      # a couple of cents a posting
    assert discover.estimate_extraction_cost_eur(10) == pytest.approx(one * 10)
    assert discover.estimate_extraction_cost_eur(0) == 0


def test_caps_pass_for_an_ordinary_launch():
    cost, daily, breach = discover.launch_caps(
        discover.launch_decisions([cand("a", relevant=8, total=40), cand("b", relevant=6, total=30)]))
    assert breach is None and daily == 70 and cost < discover.MAX_LAUNCH_COST_EUR


def test_the_cost_cap_stops_the_launch_and_adds_nothing():
    many = [cand(f"co{i}", relevant=60, total=80) for i in range(10)]   # 600 postings to read
    cost, _, breach = discover.launch_caps(discover.launch_decisions(many))
    assert cost > discover.MAX_LAUNCH_COST_EUR
    assert breach and "over the €10 cap" in breach


def test_the_daily_download_cap_stops_the_launch():
    """Few relevant roles, but enormous boards: cheap to read, expensive to poll daily."""
    huge = [cand(f"co{i}", relevant=5, total=1000) for i in range(6)]   # 6,000 postings/day
    cost, daily, breach = discover.launch_caps(discover.launch_decisions(huge))
    assert cost < discover.MAX_LAUNCH_COST_EUR and daily == 6000
    assert breach and "6000" in breach


def test_a_breached_cap_names_itself_in_the_report_and_writes_nothing():
    ds = discover.launch_decisions([cand(f"co{i}", relevant=60, total=80) for i in range(10)])
    cost, daily, breach = discover.launch_caps(ds)
    lines = "\n".join(discover.launch_report_lines("New York", ds, cost, daily, breach, applied=False))
    assert "STOPPED, nothing added" in lines and "€10 cap" in lines


def test_the_report_names_every_verdict():
    ds = discover.launch_decisions([cand("big", relevant=6), cand("small", relevant=2),
                                    cand("acmerecruiting", relevant=9),
                                    cand("deadco", error="OSError: boom")])
    cost, daily, breach = discover.launch_caps(ds)
    lines = "\n".join(discover.launch_report_lines("New York", ds, cost, daily, breach, applied=True))
    for expected in ("added: 1", "skipped (agency/aggregator): 1",
                     "left unrecorded: 1", "FAILED to fetch: 1"):
        assert expected in lines, expected


def test_run_restricts_relevance_to_the_launch_city():
    r = discover.run(CONFIG, FEEDS_DOC, REJECTED_DOC, lambda q: URLS,
                     fetch_board=fetch_board, city="San Francisco")
    newco = next(c for c in r.candidates if c.board == ("ashby", "newco"))
    assert newco.relevant == ["AI Engineer (San Francisco)"]
