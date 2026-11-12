"""repair-companies (HIR-198): fill blank companies off the stored link, merge the
duplicates that appear, leave what it cannot fix alone."""

import pytest

from app import db
from app.repair import merge_jobs, repair_companies, tables_referencing_job

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
    assert mentions == {"python"}                 # the kept row's reading only, not the union
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 1
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


def test_a_gone_job_board_posting_stays_blank_not_named_after_the_board(conn):
    """Job 95 (HIR-211): an employment-agency posting stored with no company whose page
    now answers 410. The board's name is not the employer, so the row is left blank."""
    def gone(url):
        raise OSError("HTTP Error 410: Gone")
    a = add_blank_job(conn, "https://www.arbeitsagentur.de/jobsuche/jobdetail/10001-1003490922-S",
                      "2026-11-04T10:00:00Z", title="Senior AI Engineer (w/m/d)")
    conn.execute("UPDATE job_source SET source='arbeitsagentur' WHERE job_id=?", (a,))
    lines = repair_companies(conn, fetch_page=gone)
    conn.commit()
    assert lines[0].company is None
    assert "unresolved" in lines[0].line() and "410" in lines[0].line()
    assert conn.execute("SELECT company FROM job WHERE id=?", (a,)).fetchone()["company"] is None


def test_jobs_with_a_company_are_not_touched(conn):
    add_blank_job(conn, "https://jamino.de/jobs/1", "2026-11-04T10:00:00Z", company="Already Set")
    assert repair_companies(conn, fetch_page=lambda u: PAGE) == []


def test_a_repaired_title_moves_the_job_family_and_queues_a_re_read(conn):
    a = add_blank_job(conn, "https://jamino.de/jobs/1", "2026-11-04T10:00:00Z",
                      title="Data Scientist | Jamino")
    conn.execute("UPDATE job SET family='data-scientist', extracted_version='v1' WHERE id=?", (a,))
    add_mention(conn, a, "python")
    # The page's title is an AI engineering role; the stored title said data science.
    repair_companies(conn, fetch_page=lambda u: PAGE)
    conn.commit()
    row = conn.execute("SELECT title, family, extracted_version FROM job WHERE id=?", (a,)).fetchone()
    assert row["title"] == "Senior AI Engineer"
    assert row["family"] == "ai-engineer"               # recomputed from the corrected title
    assert row["extracted_version"] is None             # so the job is read again
    # The old skills stay on the chart until that reading happens.
    assert conn.execute("SELECT count(*) FROM skill_mention WHERE job_id=?", (a,)).fetchone()[0] == 1


def test_a_company_only_repair_leaves_the_family_and_the_stamp_alone(conn):
    # The hostname supplies the company, so the title is not touched.
    a = add_blank_job(conn, "https://careers.newco.de/jobs/2", "2026-11-04T10:00:00Z",
                      title="Senior AI Engineer")
    conn.execute("UPDATE job SET family='research', extracted_version='v1' WHERE id=?", (a,))
    conn.commit()

    def dead(url):
        raise OSError("gone")

    repair_companies(conn, fetch_page=dead)
    conn.commit()
    row = conn.execute("SELECT company, title, family, extracted_version FROM job WHERE id=?", (a,)).fetchone()
    assert row["company"] == "Newco" and row["title"] == "Senior AI Engineer"
    assert row["family"] == "research" and row["extracted_version"] == "v1"


def test_merge_moves_a_table_nobody_listed_by_hand(conn):
    """A table added after merge_jobs was written must still be moved, not cascade away."""
    conn.execute("CREATE TABLE job_note ("
                 " id INTEGER PRIMARY KEY,"
                 " job_id INTEGER NOT NULL REFERENCES job (id) ON DELETE CASCADE,"
                 " note TEXT NOT NULL)")
    a = add_blank_job(conn, "https://x/1", "2026-11-04T10:00:00Z", company="Acme")
    b = add_blank_job(conn, "https://x/2", "2026-11-05T10:00:00Z", company="Acme")
    conn.execute("INSERT INTO job_note (job_id, note) VALUES (?, 'keep me')", (b,))
    conn.commit()

    assert ("job_note", "job_id") in tables_referencing_job(conn)
    merge_jobs(conn, a, b)
    conn.commit()
    rows = conn.execute("SELECT job_id, note FROM job_note").fetchall()
    assert [(r["job_id"], r["note"]) for r in rows] == [(a, "keep me")]


def test_merge_refuses_to_run_with_foreign_keys_off(conn):
    a = add_blank_job(conn, "https://x/1", "2026-11-04T10:00:00Z", company="Acme")
    b = add_blank_job(conn, "https://x/2", "2026-11-05T10:00:00Z", company="Acme")
    conn.execute("PRAGMA foreign_keys = OFF")
    with pytest.raises(RuntimeError, match="foreign keys are off"):
        merge_jobs(conn, a, b)
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 2


def test_merge_keeps_one_reading_and_the_record_of_both(conn):
    a = add_blank_job(conn, "https://x/1", "2026-11-04T10:00:00Z", company="Acme")
    b = add_blank_job(conn, "https://x/2", "2026-11-05T10:00:00Z", company="Acme")
    conn.execute("UPDATE job SET extracted_version='v1' WHERE id=?", (a,))
    conn.execute("UPDATE job SET extracted_version='v2' WHERE id=?", (b,))
    add_mention(conn, a, "python")
    add_mention(conn, b, "rag")
    for job_id, version in ((a, "v1"), (b, "v2")):
        conn.execute("INSERT INTO extraction_reject (job_id, reason, item, extractor_version)"
                     " VALUES (?,?,?,?)", (job_id, "unknown skill", "{}", version))
        conn.execute("INSERT INTO extraction_log (job_id, extractor_version, taxonomy_version,"
                     " model, raw_output, usage, input_sha256) VALUES (?,?,?,?,?,?,?)",
                     (job_id, version, 3, "m", "{}", "{}", f"sha-{version}"))
    conn.commit()

    merge_jobs(conn, a, b)
    conn.commit()

    row = conn.execute("SELECT extracted_version FROM job WHERE id=?", (a,)).fetchone()
    assert row["extracted_version"] == "v1"                           # the kept row's reading
    mentions = {r["skill_id"] for r in conn.execute("SELECT skill_id FROM skill_mention")}
    assert mentions == {"python"}                                     # the duplicate's dropped
    rejects = [r["extractor_version"] for r in conn.execute("SELECT extractor_version FROM extraction_reject")]
    assert rejects == ["v1"]
    logs = sorted(r["extractor_version"] for r in conn.execute(
        "SELECT extractor_version FROM extraction_log WHERE job_id=?", (a,)))
    assert logs == ["v1", "v2"]                   # both readings stay on the permanent record


def test_merge_jobs_widens_the_seen_window(conn):
    a = add_blank_job(conn, "https://x/1", "2026-11-04T10:00:00Z", company="Acme")
    b = add_blank_job(conn, "https://x/2", "2026-11-01T10:00:00Z", company="Acme")
    conn.execute("UPDATE job SET last_seen='2026-11-06T00:00:00Z' WHERE id=?", (b,))
    merge_jobs(conn, a, b)
    conn.commit()
    row = conn.execute("SELECT first_seen, last_seen FROM job WHERE id=?", (a,)).fetchone()
    assert row["first_seen"] == "2026-11-01T10:00:00Z" and row["last_seen"] == "2026-11-06T00:00:00Z"
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 1
