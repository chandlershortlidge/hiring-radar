import importlib.util
from pathlib import Path

import pytest

from app import db

_spec = importlib.util.spec_from_file_location(
    "refresh_workable_jobs", Path(__file__).parent.parent / "scripts" / "refresh_workable_jobs.py")
refresh_workable_jobs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(refresh_workable_jobs)

PAGES = Path(__file__).parent / "fixtures" / "pages"
WORKABLE_URL = "https://apply.workable.com/control-risks-6/j/7E5B35DAF9/"
WORKABLE_API = "https://apply.workable.com/api/v2/accounts/control-risks-6/jobs/7E5B35DAF9"
STUB = "As AI Engineer you will own the AI and data layer of the platform. You will design and t..."


def api(url):
    """Serves the saved API answer for the Control Risks posting, and nothing else."""
    assert url == WORKABLE_API, url
    return (PAGES / "workable_api.json").read_text(encoding="utf-8")


def _add_job(conn, *, url=WORKABLE_URL, source="url", text=STUB, version=None, blank=1):
    """A stored job; by default job 742's shape: a stub text, read blank once, pending."""
    job = conn.execute(
        "INSERT INTO job (company, title, title_key, city, location_raw, description_text,"
        " first_seen, last_seen, extracted_version, blank_extractions)"
        " VALUES ('Control Risks', 'AI Engineer', 'ai engineer', 'Berlin', 'Berlin, Germany', ?,"
        " 't1', 't2', ?, ?)", (text, version, blank)).lastrowid
    conn.execute("INSERT INTO job_source (job_id, source, source_job_id, url, first_seen, last_seen)"
                 " VALUES (?, ?, ?, ?, 't1', 't2')",
                 (job, source, None if source == "url" else f"id-{job}", url))
    conn.commit()
    return job


def _job(conn, job):
    return conn.execute("SELECT * FROM job WHERE id=?", (job,)).fetchone()


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def test_the_stub_is_replaced_by_the_full_posting_and_the_job_is_read_again(conn):
    job = _add_job(conn, version="x2-abc")
    result = refresh_workable_jobs.refresh(conn, fetch=api)
    assert [r["id"] for r in result["refreshed"]] == [job]
    row = _job(conn, job)
    assert len(row["description_text"]) > 5000
    assert row["description_text"].startswith("As AI Engineer you will own the AI and data layer")
    assert "\nRequirements\n" in row["description_text"]
    assert row["extracted_version"] is None          # pending: the next poll or extract reads it


def test_the_blank_read_of_the_stub_does_not_count_against_the_full_text(conn):
    # Two blank reads in a row delete a posting; the one already counted was of the stub.
    job = _add_job(conn, blank=1)
    refresh_workable_jobs.refresh(conn, fetch=api)
    assert _job(conn, job)["blank_extractions"] == 0


def test_what_a_person_set_when_adding_the_job_is_left_alone(conn):
    job = _add_job(conn)
    refresh_workable_jobs.refresh(conn, fetch=api)
    row = _job(conn, job)
    assert (row["company"], row["title"], row["city"], row["location_raw"]) == (
        "Control Risks", "AI Engineer", "Berlin", "Berlin, Germany")
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 1


def test_dry_run_changes_nothing_but_reports_the_same(conn):
    job = _add_job(conn)
    result = refresh_workable_jobs.refresh(conn, fetch=api, commit=False)
    assert [r["id"] for r in result["refreshed"]] == [job]
    assert _job(conn, job)["description_text"] == STUB
    assert _job(conn, job)["blank_extractions"] == 1


def test_second_run_finds_nothing_to_do(conn):
    job = _add_job(conn)
    refresh_workable_jobs.refresh(conn, fetch=api)
    conn.execute("UPDATE job SET extracted_version='x2-abc' WHERE id=?", (job,))   # read since
    conn.commit()
    result = refresh_workable_jobs.refresh(conn, fetch=api)
    assert result["refreshed"] == [] and [r["id"] for r in result["unchanged"]] == [job]
    assert _job(conn, job)["extracted_version"] == "x2-abc"


def test_a_longer_stored_text_is_never_replaced_by_a_shorter_one(conn):
    job = _add_job(conn, text="x" * 20000, version="x2-abc")
    result = refresh_workable_jobs.refresh(conn, fetch=api)
    assert result["refreshed"] == []
    assert _job(conn, job)["description_text"] == "x" * 20000


def no_fetch(url):
    raise AssertionError(f"should not fetch {url}")


def test_only_jobs_added_from_a_workable_link_are_touched(conn):
    other_page = _add_job(conn, url="https://jobs.bayer.com/job/Berlin-AI/1447659333/")
    board = _add_job(conn, url="https://jobs.ashbyhq.com/acme/0a1b2c3d", source="ashby")
    # A feed sighting is never refreshed, even if its link happens to be a Workable one.
    feed = _add_job(conn, source="arbeitnow")
    result = refresh_workable_jobs.refresh(conn, fetch=no_fetch)
    assert result == {"refreshed": [], "unchanged": [], "failed": []}
    for job in (other_page, board, feed):
        assert _job(conn, job)["description_text"] == STUB


def test_a_posting_workable_no_longer_serves_is_reported_and_left_alone(conn):
    def gone(url):
        raise OSError("HTTP Error 404: Not Found")
    job = _add_job(conn)
    result = refresh_workable_jobs.refresh(conn, fetch=gone)
    assert result["refreshed"] == []
    assert [(r["id"], r["error"]) for r in result["failed"]] == [(job, "OSError: HTTP Error 404: Not Found")]
    assert _job(conn, job)["description_text"] == STUB and _job(conn, job)["blank_extractions"] == 1
