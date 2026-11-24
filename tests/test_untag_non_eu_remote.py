"""Stored jobs wrongly under Remote (EU) lose that place, and nothing else (HIR-455)."""

import importlib.util
from pathlib import Path

import pytest

from app import db, queries

_spec = importlib.util.spec_from_file_location(
    "untag_non_eu_remote", Path(__file__).parent.parent / "scripts" / "untag_non_eu_remote.py")
script = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(script)

NOW = "2026-11-24T00:00:00Z"
FULLSTACK = "Senior Forward Deployed AI Engineer - LLMs & RAG - Remote - USA"   # job 1826


def _add_job(conn, title, location_raw, city="Remote (EU)", sightings=1):
    job = conn.execute(
        "INSERT INTO job (company, title, title_key, city, location_raw, description_text, "
        "first_seen, last_seen) VALUES ('Acme', ?, ?, ?, ?, 'jd', ?, ?)",
        (title, title.lower(), city, location_raw, NOW, NOW)).lastrowid
    for i in range(sightings):
        conn.execute("INSERT INTO job_source (job_id, source, source_job_id, first_seen, last_seen) "
                     "VALUES (?, 'jsearch', ?, ?, ?)", (job, f"sid-{job}-{i}", NOW, NOW))
    conn.commit()
    return job


def _places(conn, job):
    return {r[0] for r in conn.execute("SELECT place FROM job_place WHERE job_id = ?", (job,))}


def _city(conn, job):
    return conn.execute("SELECT city FROM job WHERE id = ?", (job,)).fetchone()[0]


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def test_only_jobs_naming_a_non_eu_country_are_candidates(conn):
    fullstack = _add_job(conn, FULLSTACK, "Geldern; Remote (Germany)")
    us_location = _add_job(conn, "AI Engineer", "Remote (US)")
    _add_job(conn, "AI Engineer", "Remote (Germany)")                       # a real Remote (EU) job
    _add_job(conn, "AI Engineer - Remote (US or Europe)", "Remote")         # names both: kept
    _add_job(conn, "AI Engineer", "Remote, Spain")     # placed differently today, but not this cleanup
    _add_job(conn, FULLSTACK, "Berlin", city="Berlin")                      # never under Remote (EU)

    found = {c["id"]: c["why"] for c in script.candidates(conn)}

    assert found == {fullstack: script.TITLE, us_location: script.LOCATION}


def test_untag_removes_the_remote_place_and_nothing_else(conn):
    fullstack = _add_job(conn, FULLSTACK, "Geldern; Remote (Germany)")
    real = _add_job(conn, "AI Engineer", "Remote (Germany)")
    jobs_before = conn.execute("SELECT count(*) FROM job").fetchone()[0]

    result = script.untag(conn, commit=True)

    assert [c["id"] for c in result["fixed"]] == [fullstack]
    assert _places(conn, fullstack) == set() and _city(conn, fullstack) is None
    assert _places(conn, real) == {"Remote (EU)"} and _city(conn, real) == "Remote (EU)"
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == jobs_before
    # Out of the remote view, which is what the ticket asks for.
    clause, params = queries.job_set_clause(queries.Filters(cities=("Remote (EU)",)), NOW, include_legacy=True)
    assert [r[0] for r in conn.execute(f"SELECT j.id FROM job j WHERE {clause}", params)] == [real]
    # Safe to run twice.
    assert script.untag(conn, commit=True) == {"fixed": [], "look": []}


def test_a_dry_run_writes_nothing(conn):
    fullstack = _add_job(conn, FULLSTACK, "Geldern; Remote (Germany)")

    result = script.untag(conn)

    assert [c["id"] for c in result["fixed"]] == [fullstack]
    assert _places(conn, fullstack) == {"Remote (EU)"} and _city(conn, fullstack) == "Remote (EU)"


def test_a_job_with_another_place_keeps_it(conn):
    job = _add_job(conn, FULLSTACK, "Geldern; Remote (Germany)")
    conn.execute("INSERT INTO job_place (job_id, place) VALUES (?, 'New York')", (job,))
    conn.commit()

    script.untag(conn, commit=True)

    assert _places(conn, job) == {"New York"} and _city(conn, job) == "New York"


def test_a_merged_job_found_by_location_alone_is_left_for_a_look(conn):
    """Only the first posting's location is stored, so another sighting may really have
    said Remote (EU). A title that names the country is the same on every sighting."""
    by_location = _add_job(conn, "AI Engineer", "Remote (US)", sightings=2)
    by_title = _add_job(conn, FULLSTACK, "Remote (Germany)", sightings=2)

    result = script.untag(conn, commit=True)

    assert [c["id"] for c in result["look"]] == [by_location]
    assert [c["id"] for c in result["fixed"]] == [by_title]
    assert _places(conn, by_location) == {"Remote (EU)"}
