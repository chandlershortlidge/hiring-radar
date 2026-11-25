"""The reason a missed link is filed under is worked out as data, never read back out of
the sentence a person reads (HIR-428)."""

import pytest

from app import check, db, ingest, misses
from app.check import (ALREADY_HAD, LINKEDIN_ONLY, LOCATION_FILTER, NOT_IN_SOURCES, OTHER,
                       TITLE_FILTER, UNREADABLE_SYSTEM, check_posting, check_url, log_check)
from app.sources import Posting

FEEDS = [{"type": "greenhouse", "enabled": True, "token": "acme", "company": "Acme"}]
JD = "Build LLM agents in Python and ship them to production."
PAGE = f"<html><head><title>AI Engineer - Acme</title></head><body><p>{JD}</p><p>Berlin</p></body></html>"


def gh(n, board="acme"):
    return f"https://boards.greenhouse.io/{board}/jobs/{n}"


def posting(url, title="AI Engineer", location="Berlin", company="Acme", source="url"):
    return Posting(source, "", url, company, title, location, JD)


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    conn_dropped = "INSERT INTO dropped_posting (source, source_job_id, extractor_version, dropped_at)"
    c.execute(conn_dropped + " VALUES ('greenhouse', '13', 'v', '2026-11-20T07:00:00Z')")
    return c


def no_fetch(*a, **k):
    raise AssertionError("no fetch expected")


# One check per outcome the link checker can reach, by name: (link, how it is checked,
# the reason it is stored under, the detail stored with it).
def _pasted(url, **kw):
    return lambda conn: check_posting(conn, url, posting(url, **kw), FEEDS)


def _fetched(url, board):
    return lambda conn: check_url(conn, url, FEEDS, fetch_page=lambda u: PAGE, fetch_board=lambda s, t: board)


LINKEDIN = "https://www.linkedin.com/jobs/view/123"
PERSONIO = "https://acme.jobs.personio.de/job/1"
OWN_SITE = "https://careers.bcg.com/global/en/job/1"
JOB_BOARD = "https://www.get-in-it.de/jobsuche/p1/x"
EMBED = "https://acme.com/careers?gh_jid=77"
SUPPORTED_UNREAD = "https://jobs.lever.co/zeta"

CASES = {
    "board not collected": (_pasted(gh(1, "other")), NOT_IN_SOURCES, "board greenhouse:other"),
    "board not collected, and the job would be dropped anyway": (
        _pasted(gh(2, "other"), location="United Kingdom; France; Germany"), NOT_IN_SOURCES,
        "board greenhouse:other; would also be dropped: location 'United Kingdom; France; Germany' is neither "
        "a tracked city nor EU-remote (remote tied to a non-EU country, or no remote signal)"),
    "board no longer lists the job": (
        _fetched(gh(3), []), OTHER, "closed or re-posted under a new id on board greenhouse:acme"),
    "title filter": (
        _pasted(gh(4), title="Office Manager"), TITLE_FILTER,
        "title 'Office Manager' fails the title filter (needs an AI/ML term and a role term)"),
    "location filter": (
        _pasted(gh(5), location="Paris, France"), LOCATION_FILTER,
        "location 'Paris, France' is neither a tracked city nor EU-remote "
        "(remote tied to a non-EU country, or no remote signal)"),
    "title and location filters": (
        _pasted(gh(6), title="Office Manager", location="Paris, France"), TITLE_FILTER,
        "title 'Office Manager' fails the title filter (needs an AI/ML term and a role term); "
        "location 'Paris, France' is neither a tracked city nor EU-remote "
        "(remote tied to a non-EU country, or no remote signal)"),
    "location and agency": (
        _pasted(gh(7), location="Paris, France", company="Hays Recruiting", source="arbeitnow"), LOCATION_FILTER,
        "location 'Paris, France' is neither a tracked city nor EU-remote "
        "(remote tied to a non-EU country, or no remote signal); company 'Hays Recruiting' reads as a "
        "recruitment agency or job portal ('recruit'), which the country-wide sources screen out"),
    "dropped on purpose, by neither filter": (
        _pasted(gh(8), company="Hays Recruiting", source="arbeitnow"), OTHER,
        "board greenhouse:acme is polled and the collector drops the job on purpose: company 'Hays Recruiting' "
        "reads as a recruitment agency or job portal ('recruit'), which the country-wide sources screen out"),
    "already dropped as unreadable": (
        _pasted(gh(13)), OTHER,
        f"board greenhouse:acme is polled and the collector drops the job on purpose: {check.DROPPED_UNREADABLE}"),
    "nothing stops it": (
        _pasted(gh(9)), OTHER,
        "board greenhouse:acme is polled and the job passes both filters: posted since the last poll, or a feed bug"),
    "embedded link that names no board": (
        _fetched(EMBED, []), OTHER, "a Greenhouse link embedded on a company page that does not name the board"),
    "linkedin": (_pasted(LINKEDIN), LINKEDIN_ONLY, None),
    "a careers system we cannot read": (_pasted(PERSONIO), UNREADABLE_SYSTEM, "personio"),
    "a company's own site": (_pasted(OWN_SITE), UNREADABLE_SYSTEM, "careers.bcg.com"),
    "own site, and the job would be dropped anyway": (
        _pasted(OWN_SITE + "2", title="Office Manager"), UNREADABLE_SYSTEM,
        "careers.bcg.com; would also be dropped: title 'Office Manager' fails the title filter "
        "(needs an AI/ML term and a role term)"),
    "job board copy": (_pasted(JOB_BOARD), OTHER, "posted on a job board or recruiter site (www.get-in-it.de)"),
    "a link on a system we read, not to one job": (
        _pasted(SUPPORTED_UNREAD), UNREADABLE_SYSTEM, "a lever link the checker could not read as one job (jobs.lever.co)"),
}


def stored(conn, case):
    result = CASES[case][0](conn)
    log_check(conn, result, None, "2026-11-20T08:00:00Z")
    row = conn.execute("SELECT reason, reason_detail FROM url_check ORDER BY id DESC LIMIT 1").fetchone()
    return result, (row["reason"], row["reason_detail"])


@pytest.mark.parametrize("case", CASES)
def test_each_outcome_is_stored_under_its_reason_with_its_detail(conn, case):
    result, got = stored(conn, case)
    assert result.verdict == "not_found"
    assert got == CASES[case][1:]
    assert "unrecognised" not in (got[1] or "")


# What `miss-reasons` prints for the checks above plus three from the old log, which hold
# only their sentence. Taken on main before reasons were stored as data: the counts must
# not move.
OLD_LOG = [
    ("https://jobs.ashbyhq.com/zeta/0a1b2c3d-0000-0000-0000-000000000000", "not_found", 0,
     'board ashby:zeta is not in config/feeds.json — add {"type": "ashby", "enabled": true, '
     '"token": "zeta", "company": "Zeta AI"}'),
    ("https://boards.greenhouse.io/acme/jobs/90", "not_found", 0,
     "board greenhouse:acme is polled; ingest would drop it: location 'Lagos' is neither a tracked city "
     "nor EU-remote (remote tied to a non-EU country, or no remote signal)"),
    ("https://boards.greenhouse.io/acme/jobs/91", "found", 1, None),
]
REPORT = """\
20 checked URLs from the first check to today (first check of each): 19 missed, 1 already in the poll.
3 of them were checked before reasons were recorded; their reason was recovered from what the check printed.

by reason:
     3  company was not in our sources
     2  company was in our sources, but the title filter dropped the job
     3  company was in our sources, but the location was read wrong or not at all
     4  the careers system is one we cannot read yet
     1  the job only exists on LinkedIn
     1  the job was already in the poll (not a miss)
     6  other

by city:
    11  Berlin
     9  (unknown)

by careers system:
    13  greenhouse
     2  own site
     1  ashby
     1  linkedin
     1  personio
     1  job board
     1  lever"""


def test_the_report_over_a_fixed_log_prints_the_same_counts(conn):
    for url, verdict, had, sentence in OLD_LOG:
        conn.execute("INSERT INTO url_check (url, checked_at, verdict, feed_had_it, diagnosis)"
                     " VALUES (?, '2026-10-20T08:00:00Z', ?, ?, ?)", (url, verdict, had, sentence))
    for case in CASES:
        stored(conn, case)
    assert "\n".join(misses.report_lines(misses.records(conn), None, None)) == REPORT


# --- the sentence is for a person: rewording it moves no reason --------------------------

@pytest.mark.parametrize("case", CASES)
def test_rewording_the_sentence_leaves_the_stored_reason_and_detail_as_they_were(conn, case, monkeypatch):
    monkeypatch.setattr(check, "_sentence", lambda *a, **k: "worded some other way entirely")
    result, got = stored(conn, case)
    assert result.diagnosis == "worded some other way entirely"
    assert got == CASES[case][1:]


@pytest.mark.parametrize("case", CASES)
def test_rewording_what_stopped_the_posting_leaves_the_stored_reason_as_it_was(conn, case, monkeypatch):
    monkeypatch.setattr(check, "_why_stopped", lambda stop, posting: "the collector said no")
    assert stored(conn, case)[1][0] == CASES[case][1]


def test_the_cases_above_reach_every_outcome_and_every_check_carries_one(conn):
    seen = set()
    for run, _, _ in CASES.values():
        result = run(conn)
        assert result.miss is not None and result.diagnosis == result.miss.sentence
        seen.add(result.miss.outcome)
    assert seen == set(check.OUTCOMES)


STOP_NAMES = (ingest.SKIPPED_TITLE, ingest.SKIPPED_CITY, ingest.SKIPPED_COMPANY, ingest.SKIPPED_AGENCY,
              ingest.SKIPPED_UNREADABLE, ingest.SKIPPED_BLOCKED, "a_check_added_to_the_collector_later")


@pytest.mark.parametrize("outcome", check.OUTCOMES)
@pytest.mark.parametrize("stop", (None, *STOP_NAMES))
@pytest.mark.parametrize("url", (gh(1), EMBED, LINKEDIN, PERSONIO, OWN_SITE, JOB_BOARD, SUPPORTED_UNREAD))
def test_no_outcome_is_ever_filed_as_unrecognised(outcome, stop, url):
    stops = (check.Stop(stop, "in words"),) if stop else ()
    reason, detail = check.filed(url, check.Diagnosis(outcome, "greenhouse:acme", stops))
    assert reason in check.MISS_REASONS and reason != ALREADY_HAD
    assert "unrecognised" not in detail


def test_only_a_sentence_the_checker_never_wrote_is_unrecognised():
    assert check.miss_reason(gh(1), "not_found", False, "worded some other way entirely") == (
        OTHER, "unrecognised check result: worded some other way entirely")
