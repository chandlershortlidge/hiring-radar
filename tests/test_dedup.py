from app import dedup
from app.geo import active_city, city_of

JD = """AI Engineer. Requirements: 3+ years Python, experience with LLM applications,
RAG pipelines and vector databases. Nice to have: Kubernetes, AWS. We are a Berlin startup
building agents for customer service teams across Europe."""
JD_REPOST = JD.replace("3+ years", "3+ years of")  # one-word edit
JD_OTHER = """Senior Data Engineer. Requirements: 5+ years SQL, Airflow, dbt, Snowflake.
Build pipelines for analytics. Berlin, hybrid."""


def test_company_key_strips_legal_suffixes_and_punctuation():
    assert dedup.company_key("logen.ai GmbH") == dedup.company_key("Logen AI")
    assert dedup.company_key("Acme, Inc.") == "acme"
    assert dedup.company_key(None) == ""


def test_title_key_strips_gender_tags():
    assert dedup.title_key("AI Engineer (m/w/d)") == "ai engineer"
    assert dedup.title_key("AI Engineer (f/m/x)") == dedup.title_key("AI Engineer (all genders)")
    assert dedup.title_key("Senior AI Engineer") != dedup.title_key("AI Engineer")


def test_similarity_is_high_for_reposts_and_low_for_other_roles():
    assert dedup.similarity(JD, JD) == 1.0
    assert dedup.similarity(JD, JD_REPOST) > 0.85
    assert dedup.similarity(JD, JD_OTHER) < 0.1
    assert dedup.similarity("", JD) == 0.0


def test_find_match_requires_same_company():
    cands = [dedup.Candidate(1, "Acme GmbH", "AI Engineer", JD), dedup.Candidate(2, "Other", "AI Engineer", JD)]
    m = dedup.find_match("Acme", JD_REPOST, cands)
    assert m and m.job_id == 1 and m.similarity > 0.85
    assert dedup.find_match("Nobody", JD, cands) is None
    assert dedup.find_match(None, JD, cands) is None


def test_find_match_does_not_merge_different_roles_at_same_company():
    cands = [dedup.Candidate(1, "Acme", "Data Engineer", JD_OTHER)]
    assert dedup.find_match("Acme", JD, cands) is None


def test_find_match_picks_the_closest():
    cands = [dedup.Candidate(1, "Acme", "AI Engineer", JD_REPOST), dedup.Candidate(2, "Acme", "AI Engineer", JD)]
    assert dedup.find_match("Acme", JD, cands).job_id == 2


def test_city_of():
    assert city_of("Berlin, Berlin, Germany (Hybrid)") == "Berlin"
    assert city_of("San Francisco, CA | New York City, NY") == "San Francisco"
    assert city_of("Remote (Germany)") is None
    assert city_of("Berlinton") is None
    assert city_of(None) is None


def test_active_places_are_berlin_and_eu_remote():
    assert active_city("Berlin, Germany") == "Berlin"
    assert active_city("San Francisco, CA") is None and city_of("San Francisco, CA") == "San Francisco"
    assert active_city("Remote") == "Remote (EU)"
    assert active_city("Remote - US") is None
