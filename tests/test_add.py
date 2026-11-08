"""Adding one job by hand (app/add.py): the add-by-link rules, and storing the result.

Both halves were written out once per caller and drifted (HIR-198, HIR-204, HIR-210). They
are tested here, once — the pure `decide` and the one `add_by_hand` that stores; the entry
points' own tests (tests/test_cli_check.py, tests/test_api.py) cover only how each one
reports an outcome.
"""

import sqlite3

import pytest

from app import add, db, ingest
from app.check import CheckResult
from app.sources import Posting

LONG = "Python and RAG. " * 40   # over any minimum


def result(posting=None, verdict="not_found", job_id=None):
    return CheckResult(url="https://acme.com/j/1", verdict=verdict, how="", job_id=job_id, posting=posting)


def posting(company="Acme", source="url", text=LONG):
    return Posting(source, "", "https://acme.com/j/1", company, "AI Engineer", "Berlin", text)


def test_a_posting_the_check_already_found_is_not_added_again():
    d = add.decide(result(posting(), verdict="found", job_id=51))
    assert d.action == add.EXISTS and d.job_id == 51 and not d.stores


def test_a_page_nothing_could_be_read_off_is_unreadable():
    d = add.decide(result(posting=None))
    assert d.action == add.UNREADABLE and not d.stores


def test_a_posting_with_no_company_is_refused():
    # HIR-198: a blank company can never be matched by dedup, so storing it plants a duplicate.
    for blank in (None, "", "   "):
        d = add.decide(result(posting(company=blank)))
        assert d.action == add.NEEDS_COMPANY and not d.stores


def test_a_page_with_almost_no_text_is_refused_and_says_how_little_there_was():
    d = add.decide(result(posting(text="Python.")))
    assert d.action == add.TOO_SHORT and d.characters == 7 and not d.stores


def test_the_minimum_text_is_the_callers_to_set():
    """The CLI refuses a near-empty page; the dashboard stores it and the chart leaves it out
    as "short" (DECISIONS 2026-10-21). Which is right is a separate question (HIR-205), so
    the two callers pass different minimums through one rule set rather than two."""
    short = result(posting(text="Python."))
    assert add.decide(short, min_text=add.MIN_ADD_TEXT).action == add.TOO_SHORT
    assert add.decide(short, min_text=0).stores


def test_a_page_posting_must_have_a_known_city_but_a_board_posting_need_not():
    # A board posting keeps its feed source and id, so a later poll sees it as still-listed.
    assert add.decide(result(posting(source="url"))).require_city is True
    for board in add.registry.BOARD_SOURCES:
        assert add.decide(result(posting(source=board))).require_city is False


def test_the_rules_apply_in_order_so_a_found_job_is_never_refused_first():
    """A stored posting is reported as the job it is, whatever else is wrong with the page."""
    d = add.decide(result(posting(company=None, text=""), verdict="found", job_id=7))
    assert d.action == add.EXISTS and d.job_id == 7


# --- storing a hand-added posting (HIR-210) ---------------------------------------------
#
# `add_by_hand` is the one place the "added by hand" storage settings live. Before HIR-210
# every caller passed them itself, so a new way of adding a job could store jobs under feed
# rules by forgetting one, and a screenshot's image was saved after the job in a second
# transaction — if that save failed the job stayed, with no image, and because the "have I
# added this screenshot already?" check reads the image, the same file added again made a
# second job.

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32
SHA = "a" * 64


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def hand_posting(source="paste", title="Head of Analytics", company="Acme GmbH", text=LONG):
    """A posting a person added: no source id, and a title a feed's filter would drop."""
    return Posting(source, "", "", company, title, None, text)


def rows(conn, table):
    return conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]


def test_a_hand_added_posting_is_stored_under_the_hand_added_settings(conn):
    """One call carries all three: the title is taken as read, no city is insisted on, and
    where the person found it is recorded."""
    res = add.add_by_hand(conn, hand_posting(), "linkedin")
    assert res == ingest.Stored("new", 1)
    src = conn.execute("SELECT source, source_job_id, found_via FROM job_source").fetchone()
    assert (src["source"], src["source_job_id"], src["found_via"]) == ("paste", None, "linkedin")
    assert conn.execute("SELECT city FROM job").fetchone()["city"] is None


def test_a_page_posting_can_still_be_made_to_need_a_known_city(conn):
    """`decide` asks for a known city on a company's own careers page; that is the one
    setting a caller passes, and it still reaches ingest."""
    page = Posting("url", "", "https://acme.com/j/1", "Acme GmbH", "AI Engineer", "Tokyo, Japan", LONG)
    assert add.add_by_hand(conn, page, "company_site", require_city=True).kind == "skipped_city"
    assert rows(conn, "job") == 0
    assert add.add_by_hand(conn, page, "company_site").is_new


def test_a_screenshot_is_stored_with_the_job_it_belongs_to(conn):
    res = add.add_by_hand(conn, hand_posting(source="screenshot"), "linkedin",
                          screenshot=ingest.Screenshot(PNG, SHA, "image/png"))
    assert res.is_new
    assert ingest.job_id_for_screenshot(conn, SHA) == res.job_id


def test_a_screenshot_that_cannot_be_stored_leaves_no_job_behind(conn):
    """The hole HIR-210 closes. The image's write fails here the way a real one can — the
    stored type is not one the database accepts — and the job must not survive it, because
    a job with no image is a job the same file would be added as a second time."""
    bad = ingest.Screenshot(PNG, SHA, "image/gif")   # not one of png / jpeg / webp
    with pytest.raises(sqlite3.IntegrityError):
        add.add_by_hand(conn, hand_posting(source="screenshot"), "linkedin", screenshot=bad)
    assert rows(conn, "job") == 0 and rows(conn, "job_source") == 0 and rows(conn, "screenshot") == 0
    # ...so the next upload of the same file is a first add, not a duplicate.
    assert ingest.job_id_for_screenshot(conn, SHA) is None
    good = add.add_by_hand(conn, hand_posting(source="screenshot"), "linkedin",
                           screenshot=ingest.Screenshot(PNG, SHA, "image/png"))
    assert good.is_new and rows(conn, "job") == 1


def test_a_screenshot_posting_that_merges_leaves_the_stored_job_alone(conn):
    """Unchanged behaviour: only a *new* job takes the image. A posting that dedups into a
    job already stored adds a sighting, and that job keeps whatever image it had."""
    first = add.add_by_hand(conn, hand_posting(), "linkedin")
    again = add.add_by_hand(conn, hand_posting(source="screenshot"), "referral",
                            screenshot=ingest.Screenshot(PNG, SHA, "image/png"))
    assert again.kind == "merged" and again.job_id == first.job_id
    assert rows(conn, "screenshot") == 0
