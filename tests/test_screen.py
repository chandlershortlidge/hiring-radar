"""One copy of "would we collect this posting?" (HIR-427): the collector, the link checker
and the board search all get their answer from `ingest.stops` / `ingest.screen`, with
`ingest.was_dropped` for the one check that reads the database."""

import json
from pathlib import Path

import pytest

from app import check, db, discover, ingest
from app.check import OTHER, AtsRef, check_posting, diagnose, miss_reason
from app.sources import Posting, arbeitnow, ashby, greenhouse, jsearch, lever, startup_jobs

FEEDS_DIR = Path(__file__).parent / "fixtures" / "feeds"
FEEDS = [{"type": "greenhouse", "enabled": True, "token": "acme", "company": "Acme"}]
GH = "https://boards.greenhouse.io/acme/jobs/1"
REF = AtsRef("greenhouse", "acme", "1")
JD = "Build LLM agents in Python and ship them to production."
WHEN = "2026-11-22T07:00:00Z"


def posting(source="greenhouse", sid="1", company="Acme", title="AI Engineer", location="Berlin"):
    return Posting(source, sid, GH, company, title, location, JD)


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


# One posting per check, each stopped by that check alone, and one that is kept.
STOPPED = {
    ingest.SKIPPED_TITLE: posting(title="Account Executive"),
    ingest.SKIPPED_CITY: posting(location="Lagos, Nigeria"),
    ingest.SKIPPED_COMPANY: posting(company="GmbH"),
    ingest.SKIPPED_AGENCY: posting(source="arbeitnow", company="Hays Recruiting"),
}


# --- the function itself ------------------------------------------------------------------

def test_screen_names_the_check_that_stops_a_posting_and_none_for_one_it_keeps():
    assert ingest.screen(posting()) is None
    for stop, p in STOPPED.items():
        assert ingest.screen(p) == stop


def test_stops_lists_every_failing_check_in_the_collectors_order():
    p = posting(source="arbeitnow", company="Hays Recruiting", title="Account Executive", location="Lagos")
    assert list(ingest.stops(p)) == [ingest.SKIPPED_TITLE, ingest.SKIPPED_CITY, ingest.SKIPPED_AGENCY]
    blank = posting(company=None, title="Account Executive")
    assert list(ingest.stops(blank)) == [ingest.SKIPPED_TITLE, ingest.SKIPPED_COMPANY]
    assert ingest.screen(blank) == ingest.SKIPPED_TITLE          # the first is the one counted


def test_the_hand_added_settings_switch_off_only_their_own_check():
    p = posting(title="Account Executive", location="Lagos")
    assert ingest.screen(p, trust_title=True) == ingest.SKIPPED_CITY
    assert ingest.screen(p, require_city=False) == ingest.SKIPPED_TITLE
    assert ingest.screen(p, trust_title=True, require_city=False) is None
    assert ingest.screen(posting(company=""), trust_title=True, require_city=False) == ingest.SKIPPED_COMPANY


def test_the_agency_check_leaves_board_and_hand_added_postings_alone():
    for source in ("greenhouse", "url", "paste"):
        assert ingest.screen(posting(source=source, company="Hays Recruiting")) is None


def test_was_dropped_reads_the_dropped_list_and_nothing_else(conn):
    assert ingest.was_dropped(conn, "greenhouse", "1") is False
    conn.execute("INSERT INTO dropped_posting (source, source_job_id, extractor_version, dropped_at)"
                 " VALUES ('greenhouse', '1', 'v', ?)", (WHEN,))
    assert ingest.was_dropped(conn, "greenhouse", "1") is True
    assert ingest.was_dropped(conn, "lever", "1") is False
    assert ingest.was_dropped(conn, "greenhouse", "") is False     # a posting with no id of its own
    assert ingest.was_dropped(conn, "greenhouse", None) is False


# --- the collector stores by it -----------------------------------------------------------

def test_the_collector_skips_exactly_what_screen_names(conn):
    for stop, p in STOPPED.items():
        assert ingest.ingest_one(conn, p, WHEN) == ingest.Stored(stop)
    assert ingest.ingest_one(conn, posting(), WHEN).kind == ingest.NEW
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 1


def _fixture_postings() -> list[Posting]:
    """Every recorded feed in tests/fixtures/feeds that parses to postings on its own."""
    def load(name):
        return json.loads((FEEDS_DIR / name).read_text())
    return (greenhouse.parse(load("greenhouse.json"))
            + lever.parse(load("lever.json"), "LeverCo") + lever.parse(load("lever.json"))
            + [p for name in ("ashby.json", "ashby_clera.json", "ashby_elevenlabs.json", "ashby_hir289.json",
                              "ashby_second_office.json") for p in ashby.parse(load(name), "AshbyCo")]
            + arbeitnow.parse(load("arbeitnow.json")) + arbeitnow.parse(load("arbeitnow_remote.json"))
            + [p for name in ("jsearch_learn4good.json", "jsearch_recorded.json", "jsearch_v2_recorded.json")
               for p in jsearch.parse(load(name))]
            + startup_jobs.parse(load("startup_jobs.json")))


def test_on_the_fixture_feeds_the_skip_counts_are_what_they_were_and_screen_agrees(conn):
    """The counts are the ones the collector gave on these 51 postings before its checks
    moved into `stops` (HIR-427, measured against that version); a change to them is a
    change to which jobs are collected."""
    postings = _fixture_postings()
    assert len(postings) == 51
    counts = dict.fromkeys((ingest.SKIPPED_TITLE, ingest.SKIPPED_CITY, ingest.SKIPPED_COMPANY,
                            ingest.SKIPPED_AGENCY), 0)
    for p in postings:
        kind = ingest.ingest_one(conn, p, WHEN).kind
        assert (kind if kind in counts else None) == ingest.screen(p), p
        if kind in counts:
            counts[kind] += 1
    assert counts == {ingest.SKIPPED_TITLE: 10, ingest.SKIPPED_CITY: 9, ingest.SKIPPED_COMPANY: 1,
                      ingest.SKIPPED_AGENCY: 1}


# --- the link checker explains a miss by it -----------------------------------------------

def test_the_link_checker_reports_a_blank_company_as_would_be_dropped(conn):
    p = Posting("paste", "", "https://example.com/careers/ai-engineer", "", "AI Engineer", "Berlin", JD)
    r = check_posting(conn, p.url, p, FEEDS)
    assert r.verdict == "not_found"
    assert r.diagnosis == ("not a hosted ATS page — no feed can reach it; --add stores it as source=url; "
                           "it would also be dropped: company '' is blank or not a usable name "
                           "(a posting is never stored without a company)")
    assert "would also be dropped: company ''" in miss_reason(p.url, "not_found", False, r.diagnosis)[1]
    # ...and the collector agrees, even for a posting added by hand.
    assert ingest.ingest_one(conn, p, WHEN, require_city=False, trust_title=True).kind == ingest.SKIPPED_COMPANY


def test_the_link_checker_reports_an_agency_on_a_country_wide_source_as_would_be_dropped(conn):
    p = Posting("arbeitnow", "a1", "https://www.arbeitnow.com/jobs/a1", "Hays Recruiting", "AI Engineer", "Berlin", JD)
    r = check_posting(conn, p.url, p, FEEDS)
    assert r.verdict == "not_found"
    assert r.diagnosis.endswith("it would also be dropped: company 'Hays Recruiting' reads as a recruitment "
                                "agency or job portal ('recruit'), which the country-wide sources screen out")
    assert ingest.ingest_one(conn, p, WHEN).kind == ingest.SKIPPED_AGENCY
    # The same company on a board we chose is not screened, by the collector or the checker.
    assert "passes both filters" in diagnose(posting(company="Hays Recruiting"), REF, FEEDS, True)


def test_on_a_polled_board_a_drop_that_is_neither_title_nor_place_is_no_longer_called_a_feed_bug():
    d = diagnose(posting(source="arbeitnow", company="Hays Recruiting"), REF, FEEDS, True)
    assert d.startswith("board greenhouse:acme is polled; ingest would drop it: company 'Hays Recruiting' reads as")
    reason, detail = miss_reason(GH, "not_found", False, d)
    assert reason == OTHER                      # where "passes both filters" was filed before
    assert detail.startswith("board greenhouse:acme is polled and the collector drops the job on purpose: company")


def test_a_board_link_takes_its_company_from_the_board_as_the_collector_does():
    # Lever and Ashby postings name no company; the collector gets it from the board's entry.
    assert "passes both filters" in diagnose(posting(company=None), REF, FEEDS, True)
    assert "passes both filters" in diagnose(posting(company="GmbH"), REF, FEEDS, True)


def test_the_link_checker_says_when_the_posting_was_already_dropped_as_unreadable(conn):
    conn.execute("INSERT INTO dropped_posting (source, source_job_id, extractor_version, dropped_at)"
                 " VALUES ('greenhouse', '1', 'v', ?)", (WHEN,))
    p = posting()
    r = check_posting(conn, GH, p, FEEDS)
    assert r.diagnosis == f"board greenhouse:acme is polled; ingest would drop it: {check.DROPPED_UNREADABLE}"
    reason, detail = miss_reason(GH, "not_found", False, r.diagnosis)
    assert reason == OTHER and "dropped as unreadable" in detail
    # The collector passes the feed's copy over for the same reason.
    assert ingest.ingest(conn, [p], WHEN).skipped_unreadable == 1
    # Another job on the same board is untouched by it.
    other = "https://boards.greenhouse.io/acme/jobs/2"
    assert "passes both filters" in check_posting(conn, other, posting(sid="2"), FEEDS).diagnosis


def test_title_and_place_misses_are_filed_as_before():
    from app.check import LOCATION_FILTER, TITLE_FILTER
    both = diagnose(posting(title="Account Executive", location="Lagos"), REF, FEEDS, True)
    assert miss_reason(GH, "not_found", False, both)[0] == TITLE_FILTER
    place = diagnose(posting(source="arbeitnow", company="Hays Recruiting", location="Lagos"), REF, FEEDS, True)
    assert miss_reason(GH, "not_found", False, place)[0] == LOCATION_FILTER


# --- the board search counts by it --------------------------------------------------------

def test_the_board_search_counts_what_the_collector_would_keep():
    board = [posting(sid=str(i), company=None, title=t, location=loc) for i, (t, loc) in enumerate(
        [("AI Engineer", "Berlin"), ("Account Executive", "Berlin"), ("ML Engineer", "Lagos, Nigeria")])]
    assert discover.relevant_roles(board, company="acme") == ["AI Engineer (Berlin)"]
    assert discover.relevant_roles(board) == ["AI Engineer (Berlin)"]
    # An entry whose name the collector could not use would collect nothing from the board.
    assert discover.relevant_roles(board, company="GmbH") == []


# --- a check added later reaches all three with no further edit ---------------------------

def test_a_sixth_check_added_to_the_function_changes_all_three_answers(conn, monkeypatch):
    p = posting(title="AI Engineer (night shift)")
    feed = lambda source, token: [p]
    run = lambda: discover.run({"queries": ["q"]}, {"feeds": []}, {"boards": []}, lambda q: [GH], fetch_board=feed)

    assert ingest.screen(p) is None
    assert "passes both filters" in diagnose(p, REF, FEEDS, True)
    assert run().candidates[0].relevant == ["AI Engineer (night shift) (Berlin)"]

    five = ingest.stops

    def six(p, **settings):
        yield from five(p, **settings)
        if "night shift" in p.title:
            yield "skipped_night_shift"

    monkeypatch.setattr(ingest, "stops", six)

    assert ingest.ingest_one(conn, p, WHEN) == ingest.Stored("skipped_night_shift")          # the collector
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 0
    assert diagnose(p, REF, FEEDS, True) == (                                                 # the link checker
        "board greenhouse:acme is polled; ingest would drop it: the collector's check 'skipped_night_shift' stops it")
    assert run().candidates[0].relevant == []                                                 # the board search
    # A posting the new check does not touch is answered as before by all three.
    assert ingest.ingest_one(conn, posting(sid="2"), WHEN).kind == ingest.NEW
