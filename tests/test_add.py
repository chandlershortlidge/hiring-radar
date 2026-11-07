"""The add-by-link rules (app/add.py), which the CLI's `check --add` and /api/add/url share.

These rules were written out twice and drifted twice (HIR-198, HIR-204). They are tested
here, once, against the pure `decide`; the two entry points' own tests
(tests/test_cli_check.py, tests/test_api.py) cover only how each one reports an outcome.
"""

from app import add
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
