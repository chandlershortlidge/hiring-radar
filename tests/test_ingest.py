import pytest

from app import db, geo
from app.ingest import FAMILIES, family_of, in_scope_title, ingest, ingest_one
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


def test_san_francisco_postings_are_ingested_under_their_own_city(conn):
    """SF is active since 2026-11-03 (DECISIONS, HIR-12): feeds keep it, as its own city."""
    assert ingest_one(conn, posting(sid="sf1", company="Golden Gate Labs", location="San Francisco, CA")).startswith("new:")
    assert ingest_one(conn, posting(sid="sf2", company="Bay Co", title="ML Engineer",
                                    location="South San Francisco, CA")).startswith("new:")
    assert ingest_one(conn, posting(sid="b1")).startswith("new:")   # Berlin, unchanged
    cities = [r["city"] for r in conn.execute("SELECT city FROM job ORDER BY id")]
    assert cities == ["San Francisco", "San Francisco", "Berlin"]


def test_a_city_off_the_active_list_is_still_skipped_unless_added_by_hand(conn, monkeypatch):
    """The tracked-vs-active gate is unchanged; only SF's side of it moved."""
    monkeypatch.setattr(geo, "ACTIVE_CITIES", ("Berlin", geo.REMOTE_EU))
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


def test_eu_remote_postings_are_ingested_as_remote_eu(conn):
    """DECISIONS 2026-10-26: feeds keep EU-remote postings under the place "Remote (EU)"."""
    assert ingest_one(conn, posting(sid="r1", location="Remote (Germany)")).startswith("new:")
    assert conn.execute("SELECT city FROM job").fetchone()["city"] == "Remote (EU)"
    assert ingest_one(conn, posting(sid="r2", company="Other Co", location="Remote - US")) == "skipped_city"


# --- job family (HIR-186) ---------------------------------------------------------------

# One title per bucket plus the cases the rule's order exists for. Reused by the test that
# the SQL backfill in migration 017 agrees with family_of, so every title here is checked
# twice: once through Python, once through SQLite.
FAMILY_CASES = [
    ("Senior Data Scientist", "data-scientist"),
    ("Data Science Lead (m/w/d)", "data-scientist"),
    ("Datenwissenschaftler KI", "data-scientist"),
    ("MLOps Engineer", "ml-platform"),
    ("ML Platform Engineer", "ml-platform"),               # platform wins over ml-engineer
    ("ML Infra Engineer", "ml-platform"),
    ("Machine Learning Engineer", "ml-engineer"),
    ("Machine-Learning Engineer (f/m/x)", "ml-engineer"),
    ("Senior MLE (Berlin)", "ml-engineer"),                # `mle` as a whole word
    ("Research Engineer, LLMs", "research"),
    ("Applied Scientist - Generative AI", "research"),
    ("Agentic AI Engineer", "ai-engineer"),                # the remainder
    ("LLM Engineer", "ai-engineer"),
    ("Senior Data Scientist / Machine Learning Engineer", "data-scientist"),  # first match wins
    ("Samler AI Engineer", "ai-engineer"),                 # `mle` inside a word does not count
]


@pytest.mark.parametrize("title,family", FAMILY_CASES)
def test_family_of_buckets_the_title(title, family):
    assert family_of(title) == family


def test_family_of_only_returns_known_families():
    assert all(f in FAMILIES for _, f in FAMILY_CASES)
    assert family_of("") == "ai-engineer"


def test_migration_backfill_agrees_with_family_of(tmp_path):
    """The SQL CASE in 017 and family_of must label the same titles the same way."""
    import shutil
    old = tmp_path / "old"
    old.mkdir()
    for m in sorted(db.MIGRATIONS_DIR.glob("*.sql")):
        if int(m.name[:3]) < 17:
            shutil.copy(m, old / m.name)
    c = db.connect(tmp_path / "t.db")
    db.migrate(c, old)
    for title, _ in FAMILY_CASES:
        c.execute("INSERT INTO job (title, description_text, first_seen, last_seen)"
                  " VALUES (?, 'jd', '2026-10-16T00:00:00Z', '2026-10-16T00:00:00Z')", (title,))
    c.commit()
    assert 17 in db.migrate(c)
    rows = c.execute("SELECT title, family FROM job").fetchall()
    assert len(rows) == len(FAMILY_CASES)
    assert [(r["title"], r["family"]) for r in rows] == [(t, family_of(t)) for t, _ in FAMILY_CASES]


def test_new_job_gets_a_family_on_insert(conn):
    assert ingest_one(conn, posting(title="Senior Machine Learning Engineer"),
                      when="2026-10-16T00:00:00Z") == "new:1"
    assert conn.execute("SELECT family FROM job").fetchone()["family"] == "ml-engineer"


def test_a_hand_added_job_gets_a_family_too(conn):
    """Manual adds (/api/add/url, /add/text, /add/screenshot) go through ingest_one with
    trust_title, skipping the title filter — they must still be labelled."""
    assert ingest_one(conn, posting(title="Head of Analytics"), when="2026-10-16T00:00:00Z",
                      trust_title=True) == "new:1"
    assert conn.execute("SELECT family FROM job").fetchone()["family"] == "ai-engineer"
