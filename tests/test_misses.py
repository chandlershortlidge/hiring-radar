"""Why checked jobs were missed (HIR-290): the reason rules, the record each check writes,
the count, and the caretaker's weekly line and ticket."""

import pytest

from app import caretaker_run as run
from app import db, misses
from app.check import (ALREADY_HAD, LINKEDIN_ONLY, LOCATION_FILTER, NOT_IN_SOURCES, OTHER,
                       TITLE_FILTER, UNREADABLE_SYSTEM, AtsRef, CheckResult, careers_system,
                       diagnose, log_check, miss_reason)
from app.ingest import ingest_one
from app.sources import Posting

FEEDS = [{"type": "greenhouse", "enabled": True, "token": "acme", "company": "Acme"}]
GH = "https://boards.greenhouse.io/acme/jobs/1"
JD = "Build LLM agents in Python and ship them to production."


def posting(title="AI Engineer", location="Berlin", company="Acme", url=GH):
    return Posting("url", "", url, company, title, location, JD)


@pytest.fixture
def conn(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "pending_count", lambda c: 0)
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


# --- the reason rules: each of diagnose's sentences lands on one reason -----------------

def reason_of(p, ref, feeds=FEEDS, board_had_it=True, url=GH):
    return miss_reason(url, "not_found", False, diagnose(p, ref, feeds, board_had_it))


def test_a_board_we_do_not_poll_is_company_not_in_our_sources():
    r, detail = reason_of(posting(), AtsRef("greenhouse", "other", "1"), url="https://boards.greenhouse.io/other/jobs/1")
    assert (r, detail) == (NOT_IN_SOURCES, "board greenhouse:other")


def test_a_polled_board_dropping_the_title_names_the_title_filter_and_the_title():
    r, detail = reason_of(posting(title="Office Manager"), AtsRef("greenhouse", "acme", "1"))
    assert r == TITLE_FILTER
    assert "'Office Manager'" in detail and "title filter" in detail


def test_title_wins_over_location_when_both_drop_it_as_ingest_checks_the_title_first():
    r, detail = reason_of(posting(title="Office Manager", location="Paris, France"), AtsRef("greenhouse", "acme", "1"))
    assert r == TITLE_FILTER and "'Paris, France'" in detail


def test_a_polled_board_dropping_the_location_names_the_location_read():
    r, detail = reason_of(posting(location="Paris, France"), AtsRef("greenhouse", "acme", "1"))
    assert r == LOCATION_FILTER and "location 'Paris, France'" in detail


@pytest.mark.parametrize("url, where", [
    ("https://acme.jobs.personio.de/job/1", "personio"),
    ("https://amadeus.wd502.myworkdayjobs.com/x/job/1", "workday"),
    ("https://careers.bcg.com/global/en/job/1", "careers.bcg.com"),
])
def test_a_page_no_adapter_reads_is_a_careers_system_we_cannot_read(url, where):
    r, detail = reason_of(posting(url=url), None, url=url)
    assert r == UNREADABLE_SYSTEM and detail.startswith(where)


def test_a_linkedin_link_is_linkedin_only():
    url = "https://www.linkedin.com/jobs/view/123"
    assert reason_of(posting(url=url), None, url=url) == (LINKEDIN_ONLY, "")


def test_a_job_board_copy_is_other_with_the_site_named():
    url = "https://www.get-in-it.de/jobsuche/p1/x"
    r, detail = reason_of(posting(url=url), None, url=url)
    assert r == OTHER and "www.get-in-it.de" in detail


def test_closed_and_passes_both_filters_are_other():
    assert reason_of(posting(), AtsRef("greenhouse", "acme", "1"), board_had_it=False)[0] == OTHER
    r, detail = reason_of(posting(), AtsRef("greenhouse", "acme", "1"), board_had_it=None)
    assert r == OTHER and "feed bug" in detail


def test_found_through_a_feed_is_already_had_and_found_by_hand_is_still_a_miss():
    assert miss_reason(GH, "found", True, None) == (ALREADY_HAD, "")
    r, detail = miss_reason("https://jobs.lever.co/zeta/0a1b2c3d-0000-0000-0000-000000000000", "found", False, None)
    assert r == NOT_IN_SOURCES and "lever:zeta" in detail
    assert miss_reason("https://acme.jobs.personio.de/job/1", "found", False, None)[0] == UNREADABLE_SYSTEM


@pytest.mark.parametrize("url, system", [
    (GH, "greenhouse"),
    ("https://www.linkedin.com/jobs/view/1", "linkedin"),
    ("https://apply.workable.com/acme/j/ABC123/", "workable"),
    ("https://egroup.recruitee.com/o/ai", "recruitee"),
    ("https://www.michaelpage.de/job-detail/x", "job board"),
    ("https://bolt.eu/en/careers/positions/1", "own site"),
])
def test_careers_system(url, system):
    assert careers_system(url) == system


# --- the record each check writes -------------------------------------------------------

def test_every_check_logs_its_reason_company_city_and_system(conn):
    url = "https://boards.greenhouse.io/other/jobs/7"
    p = posting(url=url, company="Other GmbH", location="Berlin, Germany")
    r = CheckResult(url=url, verdict="not_found", how="", posting=p,
                    diagnosis=diagnose(p, AtsRef("greenhouse", "other", "7"), FEEDS, None))
    log_check(conn, r, "linkedin", "2026-11-13T10:00:00Z")
    row = conn.execute("SELECT company, city, careers_system, reason, reason_detail FROM url_check").fetchone()
    assert dict(row) == {"company": "Other GmbH", "city": "Berlin", "careers_system": "greenhouse",
                         "reason": NOT_IN_SOURCES, "reason_detail": "board greenhouse:other"}


def test_a_found_check_takes_company_and_city_from_the_stored_job(conn):
    res = ingest_one(conn, Posting("greenhouse", "1", GH, "Acme", "AI Engineer", "Berlin", JD), when="2026-11-01T00:00:00Z")
    r = CheckResult(url=GH, verdict="found", how="ats id", job_id=res.job_id, sources=["greenhouse"])
    log_check(conn, r, None, "2026-11-13T10:00:00Z")
    row = conn.execute("SELECT company, city, reason FROM url_check").fetchone()
    assert dict(row) == {"company": "Acme", "city": "Berlin", "reason": ALREADY_HAD}


def test_the_reason_column_refuses_a_reason_off_the_list(conn):
    import sqlite3
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO url_check (url, checked_at, verdict, feed_had_it, reason)"
                     " VALUES ('u', 't', 'not_found', 0, 'made up')")


# --- reading and counting ---------------------------------------------------------------

def logged(conn, url, at, verdict="not_found", diagnosis=None, had=0, job_id=None, **new):
    """One url_check row as the log holds it: `new` fields only for a row written since
    migration 023; without them it is an old row."""
    cols = {"url": url, "checked_at": at, "verdict": verdict, "feed_had_it": had,
            "diagnosis": diagnosis, "job_id": job_id, **new}
    conn.execute(f"INSERT INTO url_check ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
                 list(cols.values()))


NOT_POLLED = ('board ashby:zeta is not in config/feeds.json — add {"type": "ashby", "enabled": true, '
              '"token": "zeta", "company": "Zeta AI"}')


def test_old_checks_are_recovered_from_what_they_stored(conn):
    url = "https://jobs.ashbyhq.com/zeta/0a1b2c3d-0000-0000-0000-000000000000"
    logged(conn, url, "2026-10-20T08:00:00Z", diagnosis=NOT_POLLED)
    res = ingest_one(conn, Posting("ashby", "z1", url, "Zeta AI", "AI Engineer", "Berlin", JD), when="2026-10-20T09:00:00Z")
    logged(conn, url, "2026-10-20T09:05:00Z", verdict="found", had=1, job_id=res.job_id)   # the re-check
    [m] = misses.records(conn)
    assert (m.reason, m.detail, m.company, m.city, m.careers_system, m.recovered) == (
        NOT_IN_SOURCES, "board ashby:zeta", "Zeta AI", "Berlin", "ashby", True)


def test_only_the_first_check_of_a_url_counts_and_dates_bound_it(conn):
    logged(conn, "u1", "2026-11-01T08:00:00Z", reason=NOT_IN_SOURCES, careers_system="ashby")
    logged(conn, "u1", "2026-11-05T08:00:00Z", verdict="found", had=1, reason=ALREADY_HAD, careers_system="ashby")
    logged(conn, "u2", "2026-11-05T08:00:00Z", reason=UNREADABLE_SYSTEM, careers_system="personio", city="Berlin")
    assert [m.url for m in misses.records(conn)] == ["u1", "u2"]
    assert [m.url for m in misses.records(conn, since="2026-11-02")] == ["u2"]
    assert [m.url for m in misses.records(conn, until="2026-11-04")] == ["u1"]
    c = misses.count(misses.records(conn))
    assert c["reason"][NOT_IN_SOURCES] == 1 and c["reason"][ALREADY_HAD] == 0
    assert c["city"] == {"Berlin": 1, misses.UNKNOWN: 1}
    assert c["careers_system"] == {"ashby": 1, "personio": 1}


def test_the_command_lists_every_reason_even_at_zero(conn):
    logged(conn, "u1", "2026-11-01T08:00:00Z", reason=UNREADABLE_SYSTEM, careers_system="personio")
    text = "\n".join(misses.report_lines(misses.records(conn), None, None))
    assert "1 missed, 0 already in the poll" in text
    assert "0  the job only exists on LinkedIn" in text
    assert "by city:" in text and "by careers system:" in text


def miss(reason, day="2026-11-12"):
    return misses.Miss(f"https://x/{reason}/{day}", f"{day}T08:00:00Z", None, None, "own site", reason, "", False)


def test_threshold_is_reached_at_five_and_already_had_never_counts():
    assert misses.over_threshold([miss(UNREADABLE_SYSTEM)] * 4 + [miss(ALREADY_HAD)] * 9) == []
    assert misses.over_threshold([miss(UNREADABLE_SYSTEM)] * 5) == [(UNREADABLE_SYSTEM, 5)]


def test_biggest_reason_skips_already_had():
    assert misses.biggest([miss(ALREADY_HAD)] * 3 + [miss(NOT_IN_SOURCES)]) == (NOT_IN_SOURCES, 1)
    assert misses.biggest([miss(ALREADY_HAD)]) is None


# --- the caretaker ----------------------------------------------------------------------

DAY = "2026-11-16"      # a Monday


def five_unreadable(conn, day="2026-11-12"):
    for i in range(5):
        logged(conn, f"https://acme{i}.jobs.personio.de/job/{i}", f"{day}T08:0{i}:00Z",
               reason=UNREADABLE_SYSTEM, reason_detail="personio", careers_system="personio")


def test_the_monday_summary_counts_the_week_and_names_the_biggest_reason(conn):
    five_unreadable(conn)
    logged(conn, "u-had", "2026-11-13T08:00:00Z", verdict="found", had=1, reason=ALREADY_HAD, careers_system="ashby")
    posted = []
    run.report(conn, DAY, lambda t, b: posted.append((t, b)) or "HIR-900", log=lambda *_: None)
    summary = dict(posted)["Monday summary: 2026-11-09 to 2026-11-15"]
    assert "6 job links checked: 5 we had missed, 1 we already had." in summary
    assert "Biggest reason: the careers system is one we cannot read yet (5 of 5)." in summary


def test_a_reason_at_the_threshold_gets_one_ticket_listing_every_record(conn):
    five_unreadable(conn)
    posted = []
    post = lambda t, b: posted.append((t, b)) or "HIR-901"  # noqa: E731
    assert run.miss_tickets(conn, "2026-11-13", post, log=lambda *_: None) == [UNREADABLE_SYSTEM]
    [(title, body)] = posted
    assert title == "Missed jobs: 5 in a week because the careers system is one we cannot read yet"
    assert body.count("personio.de/job/") == 5
    # The next morning, and within four weeks, the same reason is not filed again.
    assert run.miss_tickets(conn, "2026-11-14", post, log=lambda *_: None) == []
    assert run.miss_tickets(conn, "2026-12-10", post, log=lambda *_: None) == []
    assert len(posted) == 1


def test_four_misses_file_nothing(conn):
    for i in range(4):
        logged(conn, f"u{i}", "2026-11-12T08:00:00Z", reason=NOT_IN_SOURCES, careers_system="ashby")
    assert run.miss_tickets(conn, "2026-11-13", lambda t, b: pytest.fail("filed"), log=lambda *_: None) == []


def test_misses_older_than_seven_days_do_not_count_toward_a_ticket(conn):
    five_unreadable(conn, day="2026-11-05")
    assert run.miss_tickets(conn, "2026-11-12", lambda t, b: pytest.fail("filed"), log=lambda *_: None) == []
