import json
import pathlib

from app import dedup
from app.geo import active_city, city_of

# Real stored postings, exported verbatim from the production DB. Four are from HIR-113: two
# are the same Cloover posting stored twice (one source kept a shorter extract); two are
# different pplwise roles that share a recruiter's boilerplate. Two more are from HIR-108:
# the same BWI posting stored twice, once as Arbeitsagentur's own short auto-generated
# summary and once as the full scraped text — the case that forced the exact-title path.
# They are the cases that set the thresholds, so they are the cases that have to keep
# holding.
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


def test_find_match_does_not_stop_scanning_after_a_company_mismatch():
    # A continue -> break mutation on the company check would make this the same
    # regression as a stopped loop: a true duplicate further down the candidate list
    # would be missed entirely because the scan never reaches it.
    cands = [dedup.Candidate(1, "Other Co", "AI Engineer", JD), dedup.Candidate(2, "Acme", "AI Engineer", JD_REPOST)]
    m = dedup.find_match("Acme", "AI Engineer", JD, cands)
    assert m and m.job_id == 2


def test_find_match_does_not_stop_scanning_after_a_same_company_non_match():
    # Same regression, on the other `continue`: a same-company posting that is a
    # different role must not stop the scan before it reaches the real duplicate.
    cands = [dedup.Candidate(1, "Acme", "Data Engineer", JD_OTHER), dedup.Candidate(2, "Acme", "AI Engineer", JD_REPOST)]
    m = dedup.find_match("Acme", "AI Engineer", JD, cands)
    assert m and m.job_id == 2


def test_find_match_honors_a_custom_similarity_threshold():
    # The default threshold (0.7) must not match these two different roles; a custom
    # threshold set at their measured similarity must -- proving the argument actually
    # reaches the comparison instead of being ignored in favor of the module default.
    sim = dedup.similarity(JD, JD_OTHER)
    cands = [dedup.Candidate(1, "Acme", "Senior Data Engineer", JD_OTHER)]
    assert dedup.find_match("Acme", "AI Engineer", JD, cands) is None
    assert dedup.find_match("Acme", "AI Engineer", JD, cands, threshold=sim) is not None


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


def test_identical_title_without_company_match_never_merges():
    # Title parity alone, without the same company, still never merges — the exact-title
    # path (HIR-108, below) only fires once company_key already matches.
    cands = [dedup.Candidate(1, "Other Co", "AI Engineer", JD)]
    assert dedup.find_match("Acme", "AI Engineer", JD, cands) is None


# --- the exact-title path (HIR-108) -------------------------------------------------------

def test_identical_company_and_title_merges_even_with_unrelated_text():
    # HIR-108: same company, byte-identical normalized title, text that shares nothing.
    # Unlike a merely *similar* title, an exact title_key match needs no text corroboration
    # — see is_same_posting's docstring for why (a feed can rewrite the stored text almost
    # completely without it being a different posting).
    cands = [dedup.Candidate(1, "Acme", "AI Engineer", JD_OTHER)]
    m = dedup.find_match("Acme", "AI Engineer", JD, cands)
    assert m and m.job_id == 1


def test_the_real_bwi_duplicate_now_merges_despite_near_zero_similarity():
    # The real pair that forced this rule: Arbeitsagentur stored its own short auto-generated
    # summary for job 106 and the full scraped posting for job 109, under the identical
    # title. The two texts share almost no wording, so neither Jaccard nor containment comes
    # anywhere close — only the exact title match catches it.
    company, summary_title, summary = _case("bwi_auto_summary")
    _, full_title, full = _case("bwi_full")
    assert summary_title == full_title
    assert dedup.similarity(summary, full) < 0.05
    assert dedup.containment(summary, full) < 0.2
    assert dedup.is_same_posting(summary_title, summary, full_title, full)
    cands = [dedup.Candidate(109, company, full_title, full)]
    m = dedup.find_match(company, summary_title, summary, cands)
    assert m and m.job_id == 109


def test_too_little_text_cannot_establish_identity():
    # A contained fragment shorter than MIN_CONTAINED shingles is not evidence, however
    # perfectly it sits inside the longer posting — otherwise a scrap of boilerplate would
    # pull unrelated roles together. The fragment's title is corroborating but deliberately
    # *not* byte-identical to the full posting's, so this isolates the containment path's own
    # guard from the exact-title path (HIR-108), which would otherwise short-circuit it.
    _, full_title, full = _case("cloover_full")
    fragment = " ".join(full.split()[:30])
    fragment_title = full_title + " (contract)"
    assert dedup.containment(fragment, full) == 1.0
    assert len(dedup.shingles(fragment)) < dedup.MIN_CONTAINED
    assert dedup.title_key(fragment_title) != dedup.title_key(full_title)
    assert not dedup.is_same_posting(fragment_title, fragment, full_title, full)


def test_a_blank_posting_is_never_treated_as_contained_in_another():
    assert dedup.containment("", JD) == 0.0
    assert dedup.containment(JD, "") == 0.0
    # A different title, so the result rests on the containment path rather than the
    # exact-title path (HIR-108), which would merge on title alone.
    cands = [dedup.Candidate(1, "Acme", "Senior Data Engineer", JD)]
    assert dedup.find_match("Acme", "AI Engineer", "", cands) is None


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


def test_active_places_are_berlin_eu_remote_and_san_francisco():
    assert active_city("Berlin, Germany") == "Berlin"
    # SF is active since 2026-11-03 (DECISIONS, HIR-12), the only non-German exception.
    assert active_city("San Francisco, CA") == "San Francisco" and city_of("San Francisco, CA") == "San Francisco"
    assert active_city("Remote") == "Remote (EU)"
    assert active_city("Remote - US") is None
    assert active_city("Tokyo, Japan") is None
