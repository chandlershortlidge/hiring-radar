import pytest

from app import db
from app.ingest import in_scope_title, ingest, ingest_one
from app.sources import Posting

JD = ("AI Engineer. Requirements: 3+ years Python, experience with LLM applications, RAG "
      "pipelines and vector databases. Nice to have: Kubernetes, AWS. We build agents in Berlin.")


def posting(source="arbeitnow", sid="a1", company="Acme GmbH", title="AI Engineer (m/w/d)",
            location="Berlin", text=JD, url="https://x/a1"):
    return Posting(source, sid, url, company, title, location, text)


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def count(conn, table):
    return conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]


def test_new_job_is_inserted_with_city_and_source(conn):
    out = ingest_one(conn, posting(), when="2026-10-16T00:00:00Z")
    assert out == "new:1"
    job = conn.execute("SELECT * FROM job").fetchone()
    assert job["city"] == "Berlin" and job["title_key"] == "ai engineer" and job["repost_count"] == 0
    src = conn.execute("SELECT * FROM job_source").fetchone()
    assert (src["source"], src["source_job_id"], src["url"]) == ("arbeitnow", "a1", "https://x/a1")


def test_same_source_id_again_is_still_listed_and_bumps_last_seen(conn):
    ingest_one(conn, posting(), when="2026-10-16T00:00:00Z")
    assert ingest_one(conn, posting(text="completely different now"), when="2026-10-17T00:00:00Z") == "still_listed"
    job = conn.execute("SELECT first_seen, last_seen FROM job").fetchone()
    assert (job["first_seen"], job["last_seen"]) == ("2026-10-16T00:00:00Z", "2026-10-17T00:00:00Z")
    assert count(conn, "job") == 1 and count(conn, "job_source") == 1


def test_same_posting_from_another_source_merges(conn):
    ingest_one(conn, posting(), when="2026-10-16T00:00:00Z")
    out = ingest_one(conn, posting(source="startup_jobs", sid="s9", company="Acme", text=JD.replace("3+", "3+ ")),
                     when="2026-10-16T00:00:00Z")
    assert out == "merged"
    assert count(conn, "job") == 1 and count(conn, "job_source") == 2
    assert conn.execute("SELECT repost_count FROM job").fetchone()[0] == 0


def test_old_id_gone_from_a_board_feed_and_new_id_appears_is_a_repost(conn):
    ingest(conn, [posting(source="greenhouse", sid="a1")], when="2026-10-16T00:00:00Z")
    r = ingest(conn, [posting(source="greenhouse", sid="a2")], when="2026-11-20T00:00:00Z")
    assert (r.reposts, r.merged) == (1, 1)
    job = conn.execute("SELECT repost_count, first_seen, last_seen FROM job").fetchone()
    assert job["repost_count"] == 1
    assert job["first_seen"] == "2026-10-16T00:00:00Z" and job["last_seen"] == "2026-11-20T00:00:00Z"
    assert count(conn, "job_source") == 2


@pytest.mark.parametrize("order", [("a1", "a2"), ("a2", "a1")])
def test_concurrent_duplicate_in_one_fetch_merges_without_a_repost(conn, order):
    """Nebius, 2026-10-19: one board listed the same job under two ids at once (job 169)."""
    ingest(conn, [posting(source="greenhouse", sid="a1")], when="2026-10-16T00:00:00Z")
    r = ingest(conn, [posting(source="greenhouse", sid=s) for s in order], when="2026-10-17T00:00:00Z")
    assert (r.reposts, r.merged, r.still_listed) == (0, 1, 1)
    assert conn.execute("SELECT repost_count FROM job").fetchone()[0] == 0
    assert count(conn, "job") == 1 and count(conn, "job_source") == 2


def test_two_ids_new_in_the_same_fetch_are_not_a_repost(conn):
    r = ingest(conn, [posting(source="greenhouse", sid="a1"), posting(source="greenhouse", sid="a2")])
    assert (r.new, r.merged, r.reposts) == (1, 1, 0)


def test_new_id_while_one_earlier_id_is_still_listed_is_not_a_repost(conn):
    ingest(conn, [posting(source="greenhouse", sid="a1")], when="2026-09-01T00:00:00Z")
    ingest(conn, [posting(source="greenhouse", sid="a2")], when="2026-10-16T00:00:00Z")   # a real repost
    r = ingest(conn, [posting(source="greenhouse", sid=s) for s in ("a2", "a3")], when="2026-10-17T00:00:00Z")
    assert r.reposts == 0  # a1 is gone, but a2 is still up: a3 is a concurrent duplicate of a2
    assert conn.execute("SELECT repost_count FROM job").fetchone()[0] == 1


@pytest.mark.parametrize("source", ["jsearch", "arbeitsagentur", "startup_jobs", "arbeitnow"])
def test_old_id_gone_from_a_sample_source_is_not_a_repost(conn, source):
    ingest(conn, [posting(source=source, sid="a1")], when="2026-10-16T00:00:00Z")
    r = ingest(conn, [posting(source=source, sid="a2")], when="2026-11-20T00:00:00Z")
    assert (r.reposts, r.merged) == (0, 1)
    assert conn.execute("SELECT repost_count FROM job").fetchone()[0] == 0


def test_single_posting_added_by_hand_is_never_a_repost(conn):
    """check --add / the url endpoint hand ingest_one one board posting, with no fetch around it."""
    ingest(conn, [posting(source="greenhouse", sid="a1")], when="2026-10-16T00:00:00Z")
    assert ingest_one(conn, posting(source="greenhouse", sid="a2"), when="2026-11-20T00:00:00Z") == "merged"
    assert ingest_one(conn, Posting("paste", "", "", "Acme GmbH", "AI Engineer", None, JD),
                      require_city=False) == "merged"
    assert conn.execute("SELECT repost_count FROM job").fetchone()[0] == 0


def test_different_role_at_same_company_is_a_new_job(conn):
    ingest_one(conn, posting(sid="a1"))
    out = ingest_one(conn, posting(sid="a2", title="ML Platform Engineer", text="SQL, Airflow, dbt, Snowflake. Pipelines."))
    assert out == "new:2"


# Titles a feed actually served that the domain-only filter let through: "AI" in a sales
# title, "Agent" as a job-title agent rather than the agent pattern.
LEAKED_TITLES = [
    "Account Executive / Sales Manager (m/w/d) \u2013 Industrial AI & SaaS",
    "Call Center Agent - Kreditabsicherung im Homeoffice (w/m/d)",
    "Brand Agent (m/w/d) - Makaro Store Berlin - Minijob - 8h/Woche",
]


@pytest.mark.parametrize("title", LEAKED_TITLES + [
    "Account Executive",
    "Sales",
    "Software Engineer",      # role, no domain
    "Backend Developer",
    "Senior KI Consultant (m/w/d)",   # German domain word, but no technical role
    "Kirchenmusiker (m/w/d)",         # "ki" only as a whole word
])
def test_in_scope_title_rejects_without_both_halves(title):
    assert in_scope_title(title) is False


@pytest.mark.parametrize("title", [
    "AI Agent Architect (m/w/d)",
    "Applied Scientist, GenAI",
    "AI Engineer (m/w/d)",
    "ML Platform Engineer",
    "MLOps Engineer",
    "Data Scientist",
    "NLP Researcher",
    # Role names that carry the domain themselves, in scope before this rule and still in it.
    "Applied Scientist",
    "Research Engineer",
    # German domain words (Arbeitsagentur titles, 2026-10-18).
    "Software Engineer / Softwareentwickler (w/m/d) Schwerpunkt Künstliche Intelligenz",
    "KI-Engineer (m/w/d)",
    # AI spelled out (a recruiter posting, 2026-10-19).
    "Artificial Intelligence Engineer",
])
def test_in_scope_title_accepts_domain_plus_role(title):
    assert in_scope_title(title) is True


@pytest.mark.parametrize("title", LEAKED_TITLES)
def test_leaked_titles_are_not_ingested(conn, title):
    assert ingest_one(conn, posting(title=title)) == "skipped_title"
    assert count(conn, "job") == 0


def test_filters_skip_out_of_scope_titles_and_cities(conn):
    assert ingest_one(conn, posting(title="Account Executive")) == "skipped_title"
    assert ingest_one(conn, posting(location="Tokyo, Japan")) == "skipped_city"
    assert ingest_one(conn, posting(location="Remote"), require_city=False).startswith("new:")
    assert count(conn, "job") == 1


def test_tracked_but_inactive_city_is_skipped_unless_added_by_hand(conn):
    """San Francisco is tracked (geo.CITIES) but not in ACTIVE_CITIES: feeds drop it."""
    assert ingest_one(conn, posting(location="San Francisco, CA")) == "skipped_city"
    assert ingest_one(conn, posting(location="San Francisco, CA"), require_city=False).startswith("new:")
    assert conn.execute("SELECT city FROM job").fetchone()["city"] == "San Francisco"


def test_manual_add_records_found_via_and_has_no_source_id(conn):
    p = Posting("paste", "", "", "Acme", "AI Engineer", None, JD)
    out = ingest_one(conn, p, require_city=False, found_via="linkedin")
    assert out == "new:1"
    src = conn.execute("SELECT source, source_job_id, found_via FROM job_source").fetchone()
    assert (src["source"], src["source_job_id"], src["found_via"]) == ("paste", None, "linkedin")
    # Later, a feed finds the same posting: it merges and the manual job gains feed coverage.
    assert ingest_one(conn, posting(sid="f1")) == "merged"


def test_ingest_report_counts(conn):
    ps = [posting(sid="a1"), posting(sid="a1"), posting(sid="a2"), posting(title="Sales"),
          posting(sid="a3", location="Paris")]
    r = ingest(conn, ps)
    # a1 and a2 in the same fetch are concurrent duplicates: merged, not a repost.
    assert (r.seen, r.new, r.still_listed, r.reposts, r.merged, r.skipped_title, r.skipped_city) == (5, 1, 1, 0, 1, 1, 1)
    assert r.new_job_ids == [1]
