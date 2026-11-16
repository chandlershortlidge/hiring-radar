"""Alternative groups: "any one of these tools" is stored as a group (HIR-251, DECISIONS 2026-11-11).

Storage keeps the group number per mention, the job list and job detail return it, and the
chart is unchanged: every member of a required group still counts as required for its own bar.
"""

import pytest

from app import db, queries as q
from app.extract import Extraction, Mention
from app.ingest import ingest_one
from app.pipeline import store_extraction
from app.sources import Posting

NOW = "2026-11-11T12:00:00Z"
TEXT = ("Expertise in Python, Rust, Go, Java or other programming language. Docker required. "
        + "A long posting body. " * 40)


def add(conn, company, mentions):
    p = Posting("arbeitnow", f"a-{company}", "", company, "AI Engineer", "Berlin", TEXT)
    job_id = ingest_one(conn, p, q._days_ago(NOW, 1), require_city=False, trust_title=True).job_id
    store_extraction(conn, job_id, Extraction(mentions=mentions, extractor_version="t", taxonomy_version=3))
    return job_id


GROUPED = [Mention("python", "required", "Python", 1), Mention("rust", "required", "Rust", 1),
           Mention("go", "required", "Go", 1), Mention("java", "required", "Java", 1),
           Mention("docker", "required", "Docker")]
FLAT = [Mention(m.skill_id, m.requirement, m.raw_text) for m in GROUPED]


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def test_group_number_is_stored_and_a_standalone_skill_has_none(conn):
    job = add(conn, "Acme", GROUPED)
    rows = dict(conn.execute("SELECT skill_id, alternative_group FROM skill_mention WHERE job_id=?", (job,)).fetchall())
    assert rows == {"python": 1, "rust": 1, "go": 1, "java": 1, "docker": None}


def test_the_database_refuses_a_group_number_below_one(conn):
    job = add(conn, "Acme", FLAT)
    with pytest.raises(Exception):
        conn.execute("UPDATE skill_mention SET alternative_group = 0 WHERE job_id = ?", (job,))


def test_job_list_and_detail_return_the_group(conn):
    job = add(conn, "Acme", GROUPED)
    row = q.list_jobs(conn, q.Filters(window="all"), NOW)["jobs"][0]
    assert row["required_skills"] == ["docker", "go", "java", "python", "rust"]
    assert row["required_groups"] == [["go", "java", "python", "rust"]]
    detail = {s["skill_id"]: s["alternative_group"] for s in q.job_detail(conn, job, NOW)["skills"]}
    assert detail == {"python": 1, "rust": 1, "go": 1, "java": 1, "docker": None}


def test_a_job_without_groups_lists_none(conn):
    add(conn, "Acme", FLAT)
    assert q.list_jobs(conn, q.Filters(window="all"), NOW)["jobs"][0]["required_groups"] == []


def test_a_nice_to_have_group_is_not_a_required_group(conn):
    add(conn, "Acme", [Mention("python", "nice_to_have", "Python", 1), Mention("go", "nice_to_have", "Go", 1)])
    assert q.list_jobs(conn, q.Filters(window="all"), NOW)["jobs"][0]["required_groups"] == []


def test_the_chart_counts_a_grouped_job_exactly_like_an_ungrouped_one(tmp_path):
    """Chandler's decision: every member stays required, so the chart does not change."""
    def chart(mentions, name):
        c = db.connect(tmp_path / f"{name}.db")
        db.migrate(c)
        add(c, "Acme", mentions)
        return q.skill_frequency(c, q.Filters(window="all"), NOW)

    grouped, flat = chart(GROUPED, "grouped"), chart(FLAT, "flat")
    assert grouped == flat
    assert {s["skill_id"] for s in grouped["skills"]} == {"python", "rust", "go", "java", "docker"}
