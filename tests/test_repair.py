"""repair-companies (HIR-198): fill blank companies off the stored link, merge the
duplicates that appear, leave what it cannot fix alone."""

import pytest

from app import db
from app.repair import merge_jobs, repair_companies

JD = ("Senior AI Engineer. Requirements: 5+ years Python, LLM applications, RAG pipelines "
      "and vector databases. Nice to have: Kubernetes, AWS. We build agents in Berlin and "
      "ship to production every week with a small, senior team.")

PAGE = ("<html><head><title>Senior AI Engineer | Jamino</title></head>"
        f"<body><main><p>{JD}</p></main></body></html>")


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def add_blank_job(conn, url, when, title="Senior AI Engineer | J…", text=JD, company=None):
    cur = conn.execute(
        "INSERT INTO job (company, title, title_key, city, description_text, first_seen, last_seen)"
        " VALUES (?,?,?,?,?,?,?)", (company, title, "senior ai engineer j", "Berlin", text, when, when))
    job_id = cur.lastrowid
    conn.execute("INSERT INTO job_source (job_id, source, url, first_seen, last_seen)"
                 " VALUES (?,?,?,?,?)", (job_id, "url", url, when, when))
    conn.commit()
    return job_id


def add_mention(conn, job_id, skill):
    conn.execute("INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text,"
                 " taxonomy_version, extractor_version) VALUES (?,?,?,?,3,'v1')",
                 (job_id, skill, "required", skill))
    conn.commit()


def test_two_blank_copies_become_one_row_with_a_company(conn):
    a = add_blank_job(conn, "https://jamino.de/jobs/1?utm=x", "2026-11-04T10:00:00Z")
    b = add_blank_job(conn, "https://jamino.de/jobs/1?utm=y", "2026-11-04T11:00:00Z")
    add_mention(conn, a, "python")
    add_mention(conn, b, "python")
    add_mention(conn, b, "rag")
    conn.execute("INSERT INTO extraction_log (job_id, extractor_version, taxonomy_version,"
                 " model, raw_output, usage, input_sha256) VALUES (?,?,?,?,?,?,?)",
                 (b, "v1", 3, "m", "{}", "{}", "x"))
    conn.commit()

    lines = repair_companies(conn, fetch_page=lambda u: PAGE)
    conn.commit()

    jobs = conn.execute("SELECT * FROM job").fetchall()
    assert len(jobs) == 1 and jobs[0]["id"] == a                     # the older row survives
    assert jobs[0]["company"] == "Jamino"
    assert jobs[0]["title"] == "Senior AI Engineer"                  # tail stripped, truncation gone
    assert jobs[0]["title_key"] == "senior ai engineer"
    sources = conn.execute("SELECT url FROM job_source WHERE job_id=? ORDER BY first_seen", (a,)).fetchall()
    assert [s["url"] for s in sources] == ["https://jamino.de/jobs/1?utm=x", "https://jamino.de/jobs/1?utm=y"]
    mentions = {r["skill_id"] for r in conn.execute("SELECT skill_id FROM skill_mention WHERE job_id=?", (a,))}
    assert mentions == {"python", "rag"}                             # moved, duplicate dropped
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 2
    assert conn.execute("SELECT job_id FROM extraction_log").fetchone()["job_id"] == a

    assert lines[0].company == "Jamino" and lines[0].merged_into is None and lines[0].absorbed is None
    assert lines[1].company == "Jamino" and lines[1].merged_into == a
    assert "merged into #%d" % a in lines[1].line()


def test_dry_run_rolls_back_cleanly(conn):
    add_blank_job(conn, "https://jamino.de/jobs/1", "2026-11-04T10:00:00Z")
    add_blank_job(conn, "https://jamino.de/jobs/1?utm=y", "2026-11-04T11:00:00Z")
    lines = repair_companies(conn, fetch_page=lambda u: PAGE)
    conn.rollback()
    assert len(lines) == 2 and lines[1].merged_into is not None       # the dry run saw the merge
    jobs = conn.execute("SELECT company FROM job").fetchall()
    assert len(jobs) == 2 and all(j["company"] is None for j in jobs)  # and wrote nothing


def test_dead_link_falls_back_to_the_stored_title_then_hostname(conn):
    def dead(url):
        raise OSError("gone")
    # A usable stored title tail:
    a = add_blank_job(conn, "https://jamino.de/jobs/1", "2026-11-04T10:00:00Z",
                      title="ML Engineer | Jamino")
    lines = repair_companies(conn, fetch_page=dead)
    conn.commit()
    row = conn.execute("SELECT company, title FROM job WHERE id=?", (a,)).fetchone()
    assert row["company"] == "Jamino" and row["title"] == "ML Engineer"
    assert lines[0].rule == "stored title tail" and "fetch failed" in lines[0].note

    # A truncated stored tail ("J…") is rejected; the hostname answers instead.
    b = add_blank_job(conn, "https://careers.newco.de/jobs/2", "2026-11-04T10:00:00Z")
    lines = repair_companies(conn, fetch_page=dead)
    conn.commit()
    row = conn.execute("SELECT company, title FROM job WHERE id=?", (b,)).fetchone()
    assert row["company"] == "Newco"
    assert row["title"] == "Senior AI Engineer | J…"                 # only a used tail trims the title
    assert lines[0].rule == "stored domain"


def test_unresolved_rows_are_listed_and_left_alone(conn):
    def dead(url):
        raise OSError("gone")
    a = add_blank_job(conn, "https://acto.jobs.personio.com/job/1", "2026-11-04T10:00:00Z",
                      title="Senior AI Engineer")   # no tail, and the host is an ATS
    lines = repair_companies(conn, fetch_page=dead)
    conn.commit()
    assert lines[0].company is None and "unresolved" in lines[0].line()
    assert conn.execute("SELECT company FROM job WHERE id=?", (a,)).fetchone()["company"] is None


def test_jobs_with_a_company_are_not_touched(conn):
    add_blank_job(conn, "https://jamino.de/jobs/1", "2026-11-04T10:00:00Z", company="Already Set")
    assert repair_companies(conn, fetch_page=lambda u: PAGE) == []


def test_merge_jobs_widens_the_seen_window(conn):
    a = add_blank_job(conn, "https://x/1", "2026-11-04T10:00:00Z", company="Acme")
    b = add_blank_job(conn, "https://x/2", "2026-11-01T10:00:00Z", company="Acme")
    conn.execute("UPDATE job SET last_seen='2026-11-06T00:00:00Z' WHERE id=?", (b,))
    merge_jobs(conn, a, b)
    conn.commit()
    row = conn.execute("SELECT first_seen, last_seen FROM job WHERE id=?", (a,)).fetchone()
    assert row["first_seen"] == "2026-11-01T10:00:00Z" and row["last_seen"] == "2026-11-06T00:00:00Z"
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 1
