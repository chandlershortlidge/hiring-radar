import importlib.util

from pathlib import Path

import pytest

from app import db

_spec = importlib.util.spec_from_file_location(
    "remove_headline_jobs", Path(__file__).parent.parent / "scripts" / "remove_headline_jobs.py")
remove_headline_jobs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(remove_headline_jobs)

# The shapes seen live: the aggregator's headline as title, an unrelated firm as company.
# A real title never ends in a date (HIR-96, JobLeads); learn4good wedges the board's name
# into the title instead, with no date in the title at all (HIR-107).
HEADLINE = "AI Engineer (m/f/x) arbeitnow commercetools Berlin · 10/16/2026"
REAL_TITLE = "AI Engineer (m/f/x)"
WEDGED_HEADLINE = "AI/ML Engineer arbeitnow Melotech"


def _add_job(conn, company, title, source="jsearch", source_job_id="sid", mentions=0):
    job = conn.execute(
        "INSERT INTO job (company, title, title_key, city, description_text, first_seen, last_seen) "
        "VALUES (?, ?, ?, 'Berlin', 'jd', 't1', 't2')",
        (company, title, (title or "").lower())).lastrowid
    if source:
        conn.execute("INSERT INTO job_source (job_id, source, source_job_id, first_seen, last_seen) "
                     "VALUES (?, ?, ?, 't1', 't2')", (job, source, f"{source_job_id}-{job}"))
    for i in range(mentions):
        conn.execute("INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text, "
                     "taxonomy_version, extractor_version) VALUES (?, ?, 'required', 'quote', 1, 'v1')",
                     (job, f"skill-{i}"))
    conn.commit()
    return job


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def test_removes_the_headline_job_and_cascades_its_mentions(conn):
    headline = _add_job(conn, "Primetime", HEADLINE, mentions=3)
    real = _add_job(conn, "commercetools", REAL_TITLE, source="greenhouse", mentions=5)

    result = remove_headline_jobs.remove(conn)

    assert [r["id"] for r in result["removed"]] == [headline]
    assert result["removed"][0]["mentions"] == 3
    assert [r[0] for r in conn.execute("SELECT id FROM job ORDER BY id")] == [real]
    # The cascade took the headline row's mentions and feed-source row with it, and left
    # the real posting's untouched.
    assert conn.execute("SELECT COUNT(*) FROM skill_mention").fetchone()[0] == 5
    assert conn.execute("SELECT COUNT(*) FROM job_source").fetchone()[0] == 1


def test_leaves_real_titles_alone_even_from_jsearch(conn):
    _add_job(conn, "NAIRON", "Voice AI Engineer", mentions=2)

    assert remove_headline_jobs.remove(conn) == {"removed": [], "kept": []}
    assert conn.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 1


def test_removes_the_learn4good_wedged_headline_too(conn):
    """HIR-107: no trailing date, but the board's name is wedged in and the company is the
    same known-aggregator identity as the JobLeads shape."""
    headline = _add_job(conn, "Primetime", WEDGED_HEADLINE, mentions=2)
    real = _add_job(conn, "Melotech", "AI/ML Engineer", source="arbeitnow", mentions=1)

    result = remove_headline_jobs.remove(conn)

    assert [r["id"] for r in result["removed"]] == [headline]
    assert [r[0] for r in conn.execute("SELECT id FROM job ORDER BY id")] == [real]


def test_leaves_a_wedged_title_alone_under_a_real_employer(conn):
    """The word "arbeitnow" wedged in a title is not itself the signature — only paired
    with the known-aggregator company name — so a real posting that happens to mention the
    board is never removed."""
    _add_job(conn, "RealCo GmbH", "Backend Engineer who has worked with the arbeitnow board",
             mentions=4)

    assert remove_headline_jobs.remove(conn) == {"removed": [], "kept": []}
    assert conn.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 1


def test_reports_but_keeps_a_headline_title_from_another_source(conn):
    pasted = _add_job(conn, "Primetime", HEADLINE, source="arbeitnow")

    result = remove_headline_jobs.remove(conn)

    assert result["removed"] == []
    assert [r["id"] for r in result["kept"]] == [pasted]
    assert conn.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 1


def test_dry_run_writes_nothing(conn):
    _add_job(conn, "Primetime", HEADLINE, mentions=3)

    assert len(remove_headline_jobs.remove(conn, commit=False)["removed"]) == 1

    assert conn.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM skill_mention").fetchone()[0] == 3


def test_second_run_finds_nothing(conn):
    _add_job(conn, "Primetime", HEADLINE, mentions=3)

    assert len(remove_headline_jobs.remove(conn)["removed"]) == 1
    assert remove_headline_jobs.remove(conn) == {"removed": [], "kept": []}


def test_refuses_to_run_with_foreign_keys_off(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    _add_job(c, "Primetime", HEADLINE, mentions=3)
    c.execute("PRAGMA foreign_keys = OFF")

    with pytest.raises(RuntimeError, match="foreign keys are off"):
        remove_headline_jobs.remove(c)

    assert c.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 1
    assert c.execute("SELECT COUNT(*) FROM skill_mention").fetchone()[0] == 3


def test_a_job_with_no_source_row_is_never_deleted(conn):
    """A pasted or screenshot job has no job_source row; it is not jsearch's to remove."""
    pasted = _add_job(conn, "Primetime", HEADLINE, source=None)

    result = remove_headline_jobs.remove(conn)

    assert result["removed"] == []
    assert [r["id"] for r in result["kept"]] == [pasted]


def test_classify_reads_without_writing(conn):
    _add_job(conn, "Primetime", HEADLINE, mentions=3)

    removable, other = remove_headline_jobs.classify(conn)

    assert len(removable) == 1 and other == []
    assert conn.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 1


def test_keep_holds_back_a_row_a_person_decided_to_spare(conn):
    """A headline row that is the only stored copy of a posting is not a duplicate; the
    person decides, and --keep is how that decision is expressed (HIR-104, job 363)."""
    doomed = _add_job(conn, "Primetime", HEADLINE, mentions=3)
    spared = _add_job(conn, "Primetime", "AI / ML Engineer II arbeitnow SumUp Berlin · 10/28/2026",
                      mentions=4)

    result = remove_headline_jobs.remove(conn, keep={spared})

    assert [r["id"] for r in result["removed"]] == [doomed]
    assert [r["id"] for r in result["kept"]] == [spared]
    assert result["kept"][0]["held_because"] == "asked to keep"
    assert [r[0] for r in conn.execute("SELECT id FROM job ORDER BY id")] == [spared]
    assert conn.execute("SELECT COUNT(*) FROM skill_mention").fetchone()[0] == 4


def test_held_because_says_which_reason(conn):
    other_source = _add_job(conn, "Primetime", HEADLINE, source="arbeitnow")

    _, held = remove_headline_jobs.classify(conn)

    assert [(r["id"], r["held_because"]) for r in held] == [(other_source, "not from jsearch")]
