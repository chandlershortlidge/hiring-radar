import importlib.util
from pathlib import Path

import pytest

from app import db

_spec = importlib.util.spec_from_file_location(
    "reextract_blank_jobs", Path(__file__).parent.parent / "scripts" / "reextract_blank_jobs.py")
reextract_blank_jobs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reextract_blank_jobs)


def _add_job(conn, *, version="x2-abc", chars=2000, seniority=None, german=None,
             degree=None, production=None, mentions=0, rejects=0, proposed=0):
    """A stored job; by default the blank shape HIR-172 is about (job 569's)."""
    job = conn.execute(
        "INSERT INTO job (company, title, title_key, city, description_text, first_seen, last_seen,"
        " extracted_version, seniority, german, degree, production)"
        " VALUES ('Acme', 'AI Engineer', 'ai engineer', 'Berlin', ?, 't1', 't2', ?, ?, ?, ?, ?)",
        ("x" * chars, version, seniority, german, degree, production)).lastrowid
    for i in range(mentions):
        conn.execute("INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text,"
                     " taxonomy_version, extractor_version) VALUES (?, ?, 'required', 'quote', 1, 'v1')",
                     (job, f"skill-{i}"))
    for _ in range(rejects):
        conn.execute("INSERT INTO extraction_reject (job_id, reason, skill_id, raw_text, item,"
                     " extractor_version) VALUES (?, 'unknown skill_id', 'cobol', 'q', '{}', 'v1')", (job,))
    for i in range(proposed):
        conn.execute("INSERT INTO proposed_skill (job_id, label, raw_text) VALUES (?, ?, 'q')",
                     (job, f"Rust{i}"))
    conn.commit()
    return job


def _version(conn, job):
    return conn.execute("SELECT extracted_version FROM job WHERE id=?", (job,)).fetchone()[0]


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def test_unstamps_the_blank_job_so_it_is_read_again(conn):
    job = _add_job(conn)
    result = reextract_blank_jobs.unstamp(conn)
    assert [r["id"] for r in result["unstamped"]] == [job]
    assert _version(conn, job) is None


def test_the_blank_reading_already_stored_counts_as_the_first_attempt(conn):
    # So an already-stored blank job gets one more try, like a new one, not two.
    job = _add_job(conn)
    reextract_blank_jobs.unstamp(conn)
    assert conn.execute("SELECT blank_extractions FROM job WHERE id=?", (job,)).fetchone()[0] == 1


def test_dry_run_changes_nothing(conn):
    job = _add_job(conn)
    result = reextract_blank_jobs.unstamp(conn, commit=False)
    assert [r["id"] for r in result["unstamped"]] == [job]
    assert _version(conn, job) == "x2-abc"


@pytest.mark.parametrize("kwargs", [
    {"seniority": "senior"},            # zero skills but a stated seniority: a real extraction
    {"german": "required"},
    {"degree": "master"},
    {"production": "required"},
    {"mentions": 1},
    {"rejects": 1},
    {"proposed": 1},
    {"version": "legacy"},              # carries the old summary, never re-extracted
    {"version": None},                  # already pending
])
def test_leaves_every_other_shape_alone(conn, kwargs):
    job = _add_job(conn, **kwargs)
    result = reextract_blank_jobs.unstamp(conn)
    assert result["unstamped"] == []
    assert _version(conn, job) == kwargs.get("version", "x2-abc")


def test_a_short_blank_posting_is_reported_but_not_un_stamped(conn):
    # Un-stamping it would make every future poll pay for the same empty read.
    job = _add_job(conn, chars=200)
    result = reextract_blank_jobs.unstamp(conn)
    assert result["unstamped"] == [] and [r["id"] for r in result["skipped"]] == [job]
    assert _version(conn, job) == "x2-abc"


def test_running_twice_finds_nothing_the_second_time(conn):
    _add_job(conn)
    reextract_blank_jobs.unstamp(conn)
    assert reextract_blank_jobs.unstamp(conn)["unstamped"] == []
