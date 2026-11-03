import json
import pathlib

from app import dedup
from app.geo import active_city, city_of

# Four real stored postings, exported verbatim from the production DB for HIR-113. Two are
# the same Cloover posting stored twice (one source kept a shorter extract); two are
# different pplwise roles that share a recruiter's boilerplate. They are the cases that set
# the containment thresholds, so they are the cases that have to keep holding.
REAL = json.loads((pathlib.Path(__file__).parent / "fixtures" / "dedup" / "real_cases.json")
                  .read_text(encoding="utf-8"))


def _case(name):
    c = REAL[name]
    return c["company"], c["title"], c["description_text"]

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
    m = dedup.find_match("Acme", "AI Engineer", JD_REPOST, cands)
    assert m and m.job_id == 1 and m.similarity > 0.85
    assert dedup.find_match("Nobody", "AI Engineer", JD, cands) is None
    assert dedup.find_match(None, "AI Engineer", JD, cands) is None


def test_find_match_does_not_merge_different_roles_at_same_company():
    cands = [dedup.Candidate(1, "Acme", "Data Engineer", JD_OTHER)]
    assert dedup.find_match("Acme", "AI Engineer", JD, cands) is None


def test_find_match_picks_the_closest():
    cands = [dedup.Candidate(1, "Acme", "AI Engineer", JD_REPOST), dedup.Candidate(2, "Acme", "AI Engineer", JD)]
    assert dedup.find_match("Acme", "AI Engineer", JD, cands).job_id == 2


# --- the containment path (HIR-113) -------------------------------------------------------

def test_containment_sees_a_snippet_inside_a_full_posting_where_jaccard_cannot():
    _, _, snippet = _case("cloover_snippet")
    _, _, full = _case("cloover_full")
    # The real numbers that made this a bug: Jaccard sat just under the 0.7 threshold
    # because the union grows with the longer text, while the snippet is wholly contained.
    assert 0.6 < dedup.similarity(snippet, full) < dedup.THRESHOLD
    assert dedup.containment(snippet, full) == 1.0
    assert dedup.containment(full, snippet) == 1.0   # symmetric


def test_the_real_cloover_duplicate_now_merges():
    company, snippet_title, snippet = _case("cloover_snippet")
    _, full_title, full = _case("cloover_full")
    assert dedup.is_same_posting(snippet_title, snippet, full_title, full)
    cands = [dedup.Candidate(231, company, full_title, full)]
    m = dedup.find_match(company, snippet_title, snippet, cands)
    assert m and m.job_id == 231


def test_shared_boilerplate_does_not_merge_two_different_roles():
    # pplwise, a recruiter: these two postings reach containment 0.93 on boilerplate alone.
    # The title guard is the only thing keeping them apart, so this is the invariant's test.
    company, title_a, text_a = _case("pplwise_manufacturing")
    _, title_b, text_b = _case("pplwise_senior_ml")
    assert dedup.containment(text_a, text_b) > dedup.CONTAINED
    assert not dedup.is_same_posting(title_a, text_a, title_b, text_b)
    cands = [dedup.Candidate(88, company, title_b, text_b)]
    assert dedup.find_match(company, title_a, text_a, cands) is None


def test_a_matching_title_alone_never_merges():
    # The title is only ever a supporting signal: identical titles, unrelated text.
    cands = [dedup.Candidate(1, "Acme", "AI Engineer", JD_OTHER)]
    assert dedup.find_match("Acme", "AI Engineer", JD, cands) is None


def test_too_little_text_cannot_establish_identity():
    # A contained fragment shorter than MIN_CONTAINED shingles is not evidence, however
    # perfectly it sits inside the longer posting — otherwise a scrap of boilerplate would
    # pull unrelated roles together.
    _, full_title, full = _case("cloover_full")
    fragment = " ".join(full.split()[:30])
    assert dedup.containment(fragment, full) == 1.0
    assert len(dedup.shingles(fragment)) < dedup.MIN_CONTAINED
    assert not dedup.is_same_posting(full_title, fragment, full_title, full)


def test_a_translated_posting_is_still_a_duplicate_no_text_measure_can_see():
    # Cloover's third row is the same posting in German. Both measures read near zero; this
    # is recorded as a known limit, not something the containment path fixes. See HIR-117.
    _, _, english = _case("cloover_full")
    german = "Ihre Rolle Jedes interne Team bei Cloover hat Aufgaben, die KI-Agenten schneller erledigen"
    assert dedup.similarity(english, german) < 0.05
    assert dedup.containment(english, german) < 0.1


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
