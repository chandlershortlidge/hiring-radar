import pytest

from app import db, geo
from app.ingest import (FAMILIES, Stored, check_timestamp, family_of, in_scope_title,
                        ingest, ingest_one, now_iso)
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
    assert out == Stored("new", 1)
    job = conn.execute("SELECT * FROM job").fetchone()
    assert job["city"] == "Berlin" and job["title_key"] == "ai engineer" and job["repost_count"] == 0
    src = conn.execute("SELECT * FROM job_source").fetchone()
    assert (src["source"], src["source_job_id"], src["url"]) == ("arbeitnow", "a1", "https://x/a1")


def test_same_source_id_again_is_still_listed_and_bumps_last_seen(conn):
    ingest_one(conn, posting(), when="2026-10-16T00:00:00Z")
    assert ingest_one(conn, posting(text="completely different now"), when="2026-10-17T00:00:00Z").kind == "still_listed"
    job = conn.execute("SELECT first_seen, last_seen FROM job").fetchone()
    assert (job["first_seen"], job["last_seen"]) == ("2026-10-16T00:00:00Z", "2026-10-17T00:00:00Z")
    assert count(conn, "job") == 1 and count(conn, "job_source") == 1


def test_same_posting_from_another_source_merges(conn):
    ingest_one(conn, posting(), when="2026-10-16T00:00:00Z")
    out = ingest_one(conn, posting(source="startup_jobs", sid="s9", company="Acme", text=JD.replace("3+", "3+ ")),
                     when="2026-10-16T00:00:00Z")
    assert out.kind == "merged"
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
    assert ingest_one(conn, posting(source="greenhouse", sid="a2"), when="2026-11-20T00:00:00Z").kind == "merged"
    assert ingest_one(conn, Posting("paste", "", "", "Acme GmbH", "AI Engineer", None, JD),
                      require_city=False).kind == "merged"
    assert conn.execute("SELECT repost_count FROM job").fetchone()[0] == 0


def test_different_role_at_same_company_is_a_new_job(conn):
    ingest_one(conn, posting(sid="a1"))
    out = ingest_one(conn, posting(sid="a2", title="ML Platform Engineer", text="SQL, Airflow, dbt, Snowflake. Pipelines."))
    assert out == Stored("new", 2)


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
    assert ingest_one(conn, posting(title=title)).kind == "skipped_title"
    assert count(conn, "job") == 0


def test_filters_skip_out_of_scope_titles_and_cities(conn):
    assert ingest_one(conn, posting(title="Account Executive")).kind == "skipped_title"
    assert ingest_one(conn, posting(location="Tokyo, Japan")).kind == "skipped_city"
    assert ingest_one(conn, posting(location="Remote"), require_city=False).is_new
    assert count(conn, "job") == 1


# --- a job is never stored without a company (HIR-207) ---------------------------------

# Everything a feed has handed us, or could, where dedup's company_key comes out empty: the
# field missing, whitespace, punctuation used as a placeholder, and a bare legal suffix.
# Each of these can never be matched as a duplicate, so each must be refused at ingest.
BLANK_COMPANIES = [None, "", "   ", "-", "—", "/", "GmbH"]


@pytest.mark.parametrize("company", BLANK_COMPANIES)
def test_a_feed_posting_with_no_company_is_refused_and_counted(conn, company):
    assert ingest_one(conn, posting(company=company)).kind == "skipped_company"
    assert count(conn, "job") == 0
    assert count(conn, "job_source") == 0


@pytest.mark.parametrize("company", BLANK_COMPANIES)
def test_a_hand_picked_posting_with_no_company_is_refused_too(conn, company):
    """trust_title waives the title filter for a posting a person chose; it never waives
    this one — a blank-company row plants a duplicate however it got in."""
    p = Posting("paste", "", "", company, "AI Engineer", None, JD)
    assert ingest_one(conn, p, require_city=False, trust_title=True).kind == "skipped_company"
    assert count(conn, "job") == 0


def test_no_ingested_job_row_ever_has_a_blank_company(conn):
    """The invariant itself, over a fetch mixing good and blank-company postings."""
    ps = [posting(sid="a1"), posting(sid="a2", company=None, title="ML Engineer"),
          posting(sid="a3", company="  ", title="Data Scientist"),
          posting(sid="a4", company="Other Co", title="MLOps Engineer")]
    r = ingest(conn, ps)
    assert (r.seen, r.new, r.skipped_company) == (4, 2, 2)
    assert conn.execute("SELECT count(*) FROM job WHERE company IS NULL OR trim(company)=''").fetchone()[0] == 0


def test_the_blank_company_count_is_in_the_report_line(conn):
    """The poll's per-feed line is where this shows up for a person."""
    r = ingest(conn, [posting(sid="a1", company=""), posting(sid="a2")])
    assert "skipped_company=1" in r.line() and "new=1" in r.line()


def test_san_francisco_postings_are_ingested_under_their_own_city(conn):
    """SF is active since 2026-11-03 (DECISIONS, HIR-12): feeds keep it, as its own city."""
    assert ingest_one(conn, posting(sid="sf1", company="Golden Gate Labs", location="San Francisco, CA")).is_new
    assert ingest_one(conn, posting(sid="sf2", company="Bay Co", title="ML Engineer",
                                    location="South San Francisco, CA")).is_new
    assert ingest_one(conn, posting(sid="b1")).is_new   # Berlin, unchanged
    cities = [r["city"] for r in conn.execute("SELECT city FROM job ORDER BY id")]
    assert cities == ["San Francisco", "San Francisco", "Berlin"]


def test_a_city_off_the_active_list_is_still_skipped_unless_added_by_hand(conn, monkeypatch):
    """The tracked-vs-active gate is unchanged; only SF's side of it moved."""
    monkeypatch.setattr(geo, "ACTIVE_CITIES", ("Berlin", geo.REMOTE_EU))
    assert ingest_one(conn, posting(location="San Francisco, CA")).kind == "skipped_city"
    assert ingest_one(conn, posting(location="San Francisco, CA"), require_city=False).is_new
    assert conn.execute("SELECT city FROM job").fetchone()["city"] == "San Francisco"


def test_manual_add_records_found_via_and_has_no_source_id(conn):
    p = Posting("paste", "", "", "Acme", "AI Engineer", None, JD)
    out = ingest_one(conn, p, require_city=False, found_via="linkedin")
    assert out == Stored("new", 1)
    src = conn.execute("SELECT source, source_job_id, found_via FROM job_source").fetchone()
    assert (src["source"], src["source_job_id"], src["found_via"]) == ("paste", None, "linkedin")
    # Later, a feed finds the same posting: it merges and the manual job gains feed coverage.
    assert ingest_one(conn, posting(sid="f1")).kind == "merged"


def test_ingest_report_counts(conn):
    ps = [posting(sid="a1"), posting(sid="a1"), posting(sid="a2"), posting(title="Sales"),
          posting(sid="a3", location="Paris")]
    r = ingest(conn, ps)
    # a1 and a2 in the same fetch are concurrent duplicates: merged, not a repost.
    assert (r.seen, r.new, r.still_listed, r.reposts, r.merged, r.skipped_title, r.skipped_city) == (5, 1, 1, 0, 1, 1, 1)
    assert r.new_job_ids == [1]


def test_eu_remote_postings_are_ingested_as_remote_eu(conn):
    """DECISIONS 2026-10-26: feeds keep EU-remote postings under the place "Remote (EU)"."""
    assert ingest_one(conn, posting(sid="r1", location="Remote (Germany)")).is_new
    assert conn.execute("SELECT city FROM job").fetchone()["city"] == "Remote (EU)"
    assert ingest_one(conn, posting(sid="r2", company="Other Co", location="Remote - US")).kind == "skipped_city"


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
                      when="2026-10-16T00:00:00Z") == Stored("new", 1)
    assert conn.execute("SELECT family FROM job").fetchone()["family"] == "ml-engineer"


def test_a_hand_added_job_gets_a_family_too(conn):
    """Manual adds (/api/add/url, /add/text, /add/screenshot) go through ingest_one with
    trust_title, skipping the title filter — they must still be labelled."""
    assert ingest_one(conn, posting(title="Head of Analytics"), when="2026-10-16T00:00:00Z",
                      trust_title=True) == Stored("new", 1)
    assert conn.execute("SELECT family FROM job").fetchone()["family"] == "ai-engineer"


# --- every stored timestamp has the one exact form (HIR-209) --------------------------

@pytest.mark.parametrize("when", [
    "2026-11-07T15:42:00Z",
    "2026-01-01T00:00:00Z",
    "2026-12-31T23:59:59Z",
])
def test_the_exact_form_is_accepted(when):
    assert check_timestamp(when) == when


@pytest.mark.parametrize("when", [
    "2026-11-07T15:42:00+00:00",   # an offset sorts after "Z"
    "2026-11-07T15:42:00.123Z",    # milliseconds make a longer string, so a later one
    "2026-11-07 15:42:00Z",        # a space instead of T
    "2026-11-07T15:42:00",         # no zone marker at all
    "2026-11-07",                  # a bare date looks older than every full timestamp
    "2026-11-07T15:42Z",           # no seconds
    "2026-1-7T15:42:00Z",          # one-digit month and day
    "",
    None,
])
def test_anything_else_is_refused(when):
    with pytest.raises(ValueError, match="2026-11-07T15:42:00Z"):
        check_timestamp(when)


@pytest.mark.parametrize("when", ["2026-13-07T15:42:00Z", "2026-11-31T15:42:00Z", "2026-11-07T25:42:00Z"])
def test_the_right_shape_with_an_impossible_date_is_refused(when):
    with pytest.raises(ValueError, match="not a real date"):
        check_timestamp(when)


def test_ingest_refuses_a_badly_formatted_timestamp_and_stores_nothing(conn):
    """Scripts pass their own `when`; one in another format would sort wrong for ever."""
    with pytest.raises(ValueError, match="2026-11-07T15:42:00Z"):
        ingest_one(conn, posting(), when="2026-10-16T00:00:00+00:00")
    assert count(conn, "job") == 0
    assert count(conn, "job_source") == 0


def test_ingest_checks_before_the_title_and_city_filters(conn):
    """A bad timestamp is a caller's bug, so it is raised even for a posting that would
    have been skipped — otherwise the filters would hide it."""
    with pytest.raises(ValueError):
        ingest_one(conn, posting(title="Sales Manager"), when="2026-10-16")


def test_the_default_timestamp_passes_its_own_check(conn):
    assert check_timestamp(now_iso())
    assert ingest_one(conn, posting()) == Stored("new", 1)
