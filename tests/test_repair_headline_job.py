import importlib.util
from pathlib import Path

import pytest

from app import db

_spec = importlib.util.spec_from_file_location(
    "repair_headline_job", Path(__file__).parent.parent / "scripts" / "repair_headline_job.py")
repair_headline_job = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(repair_headline_job)

# Job 363 as it was stored (HIR-104): the aggregator's headline as title, an unrelated firm
# as company, and attributes judged with that headline on top of the posting.
HEADLINE = "AI / Machine Learning Engineer II arbeitnow SumUp Berlin, Berlin, Germany · 10/28/2026"
REAL_COMPANY = "SumUp"
REAL_TITLE = "AI / Machine Learning Engineer II"


def _add_job(conn, company, title, extracted="x2-abc", mentions=0):
    job = conn.execute(
        "INSERT INTO job (company, title, title_key, city, description_text, first_seen, last_seen, "
        "extracted_version, seniority, seniority_basis, seniority_signal) "
        "VALUES (?, ?, ?, 'Berlin', 'jd text', 't1', 't2', ?, 'senior', 'stated', "
        "'Senior Machine Learning Engineer')",
        (company, title, title.lower(), extracted)).lastrowid
    for i in range(mentions):
        conn.execute("INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text, "
                     "taxonomy_version, extractor_version) VALUES (?, ?, 'required', 'quote', 1, 'x2-abc')",
                     (job, f"skill-{i}"))
    conn.commit()
    return job


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def test_sets_company_title_and_dedup_key(conn):
    job = _add_job(conn, "Primetime", HEADLINE)

    result = repair_headline_job.repair(conn, job, REAL_COMPANY, REAL_TITLE)

    row = conn.execute("SELECT company, title, title_key FROM job WHERE id=?", (job,)).fetchone()
    assert (row["company"], row["title"]) == (REAL_COMPANY, REAL_TITLE)
    # title_key is recomputed, not left as the headline's — dedup matches on it.
    assert row["title_key"] == "ai machine learning engineer ii"
    assert result["before"]["company"] == "Primetime"
    assert result["after"]["title"] == REAL_TITLE


def test_clears_extracted_version_so_the_job_is_re_read(conn):
    """The title goes on top of the text the model sees, so the old attributes were judged
    against the headline and have to be thrown away."""
    job = _add_job(conn, "Primetime", HEADLINE, extracted="x2-abc")

    repair_headline_job.repair(conn, job, REAL_COMPANY, REAL_TITLE)

    assert conn.execute("SELECT extracted_version FROM job WHERE id=?", (job,)).fetchone()[0] is None


def test_leaves_existing_mentions_for_re_extraction_to_replace(conn):
    job = _add_job(conn, "Primetime", HEADLINE, mentions=24)

    repair_headline_job.repair(conn, job, REAL_COMPANY, REAL_TITLE)

    assert conn.execute("SELECT COUNT(*) FROM skill_mention WHERE job_id=?", (job,)).fetchone()[0] == 24


def test_dry_run_writes_nothing_but_reports_the_change(conn):
    job = _add_job(conn, "Primetime", HEADLINE)

    result = repair_headline_job.repair(conn, job, REAL_COMPANY, REAL_TITLE, commit=False)

    assert result["after"]["company"] == REAL_COMPANY
    row = conn.execute("SELECT company, title, extracted_version FROM job WHERE id=?", (job,)).fetchone()
    assert (row["company"], row["title"]) == ("Primetime", HEADLINE)
    assert row["extracted_version"] == "x2-abc"


def test_reports_a_collision_without_merging(conn):
    """If the corrected company and title are already stored, say so and change nothing
    about the other row: merging two stored jobs is a separate decision."""
    twin = _add_job(conn, REAL_COMPANY, REAL_TITLE)
    job = _add_job(conn, "Primetime", HEADLINE)

    result = repair_headline_job.repair(conn, job, REAL_COMPANY, REAL_TITLE)

    assert [c["id"] for c in result["collisions"]] == [twin]
    assert conn.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 2


def test_no_collision_when_the_company_has_other_titles(conn):
    """SumUp's real case: three other SumUp rows, none with this title."""
    _add_job(conn, REAL_COMPANY, "Senior Machine Learning Engineer")
    _add_job(conn, REAL_COMPANY, "Senior Machine Learning Engineer - Platform Team")
    job = _add_job(conn, "Primetime", HEADLINE)

    assert repair_headline_job.repair(conn, job, REAL_COMPANY, REAL_TITLE)["collisions"] == []


def test_unknown_job_id_is_an_error_not_a_silent_no_op(conn):
    with pytest.raises(RuntimeError, match="no job 999"):
        repair_headline_job.repair(conn, 999, REAL_COMPANY, REAL_TITLE)
