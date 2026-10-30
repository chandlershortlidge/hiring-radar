"""Tests for scripts/agent_label.py. Every model call is mocked (AGENTS.md)."""

import importlib.util
import json
import re
import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("agent_label", ROOT / "scripts" / "agent_label.py")
al = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(al)

from app.taxonomy import Taxonomy  # noqa: E402

TAX = Taxonomy({"version": 9, "skills": [
    {"id": "python", "display": "Python"},
    {"id": "rag", "display": "RAG", "aliases": ["Retrieval-Augmented Generation"]},
    {"id": "llms", "display": "LLMs"},
    {"id": "docker", "display": "Docker"},
]})

POSTING = """Senior AI Engineer (m/f/d)

Requirements:
- Strong Python and experience with RAG pipelines
- 6+ years of professional experience building LLM applications
- Master's degree in computer science or equivalent experience
- Fluent German (C1)

Nice to have:
- Docker
"""


def ok_answer(**over):
    answer = {
        "expected": [
            {"skill_id": "python", "requirement": "required", "raw_text": "Strong Python"},
            {"skill_id": "rag", "requirement": "required", "raw_text": "experience with RAG pipelines"},
            {"skill_id": "docker", "requirement": "nice_to_have", "raw_text": "Docker"},
        ],
        "unmapped": [],
        "seniority": "senior", "seniority_basis": "inferred",
        "seniority_signal": "6+ years of professional experience",
        "german": "required", "german_basis": "stated", "german_signal": "Fluent German (C1)",
        "degree": "master", "degree_requirement": "required", "degree_or_equivalent": True,
        "degree_signal": "Master's degree in computer science or equivalent experience",
        "notes": "",
    }
    answer.update(over)
    return answer


# --- auto-check -------------------------------------------------------------------

def test_auto_check_passes_a_clean_answer():
    assert al.auto_check(ok_answer(), POSTING, TAX) == []


@pytest.mark.parametrize("over, scope, needle", [
    # raw_text must be in the posting
    ({"expected": [{"skill_id": "python", "requirement": "required", "raw_text": "deep Python mastery"}]},
     "skill:python", "raw_text does not appear"),
    ({"expected": [{"skill_id": "python", "requirement": "required", "raw_text": ""}]},
     "skill:python", "raw_text does not appear"),
    # unknown ids, bad requirement, duplicate ids
    ({"expected": [{"skill_id": "kubernetes", "requirement": "required", "raw_text": "Docker"}]},
     "skill:kubernetes", "not in the taxonomy"),
    ({"expected": [{"skill_id": "Python", "requirement": "required", "raw_text": "Strong Python"}]},
     "skill:Python", "did it mean 'python'?"),
    ({"expected": [{"skill_id": "python", "requirement": "must have", "raw_text": "Strong Python"}]},
     "skill:python", "requirement is 'must have'"),
    ({"expected": [{"skill_id": "python", "requirement": "required", "raw_text": "Strong Python"},
                   {"skill_id": "python", "requirement": "nice_to_have", "raw_text": "Strong Python"}]},
     "skill:python", "2 criteria for one skill_id"),
    # signals must be verbatim
    ({"seniority_signal": "very senior role"}, "field:seniority", "seniority_signal does not appear"),
    ({"german_signal": "speaks German natively"}, "field:german", "german_signal does not appear"),
    # the string "null" is called out by name, because the prompt forbids it
    ({"seniority": "null", "seniority_basis": None, "seniority_signal": None},
     "field:seniority", 'the string "null"'),
    # field consistency
    ({"german": "required", "german_basis": None, "german_signal": None},
     "field:german", "a value needs a basis"),
    ({"seniority": "senior", "seniority_basis": "stated", "seniority_signal": None},
     "field:seniority", "a stated label quotes the text"),
    ({"german": "required", "german_basis": "inferred", "german_signal": "Fluent German (C1)"},
     "field:german", "german_signal must be null"),
    ({"degree": None, "degree_requirement": "required", "degree_or_equivalent": False,
      "degree_signal": None}, "field:degree", "degree is null but degree_requirement"),
    ({"degree": None, "degree_requirement": None, "degree_or_equivalent": True, "degree_signal": None},
     "field:degree", "degree_or_equivalent is true"),
    ({"degree": "master", "degree_requirement": None, "degree_or_equivalent": False,
      "degree_signal": "Master's degree in computer science or equivalent experience"},
     "field:degree", "degree_requirement is None"),
    ({"degree": "master", "degree_requirement": "required", "degree_or_equivalent": "yes",
      "degree_signal": "Master's degree in computer science or equivalent experience"},
     "field:degree", "not a boolean"),
])
def test_auto_check_catches(over, scope, needle):
    problems = al.auto_check(ok_answer(**over), POSTING, TAX)
    assert any(p["scope"] == scope and needle in p["problem"] for p in problems), problems


def test_auto_check_rejects_a_non_list_expected():
    problems = al.auto_check(ok_answer(expected="python, rag"), POSTING, TAX)
    assert problems[0]["scope"] == "run"


# --- merge ------------------------------------------------------------------------

def merged_for(a, b):
    return al.merge("golden_030", POSTING, a, b,
                    al.auto_check(a, POSTING, TAX), al.auto_check(b, POSTING, TAX))


def test_merge_accepts_what_both_labelers_said():
    m = merged_for(ok_answer(), ok_answer())
    assert [s["skill_id"] for s in m.accepted_skills] == ["docker", "python", "rag"]
    assert sorted(m.accepted_attrs) == ["degree", "german", "seniority"]
    assert m.review == []


def test_merge_queues_a_requirement_disagreement_and_keeps_the_rest():
    b = ok_answer(expected=[
        {"skill_id": "python", "requirement": "required", "raw_text": "Strong Python"},
        {"skill_id": "rag", "requirement": "nice_to_have", "raw_text": "experience with RAG pipelines"},
        {"skill_id": "docker", "requirement": "nice_to_have", "raw_text": "Docker"}])
    m = merged_for(ok_answer(), b)
    assert [s["skill_id"] for s in m.accepted_skills] == ["docker", "python"]
    item, = m.review
    assert (item["kind"], item["key"], item["reason"]) == ("skill", "rag", "disagreement")
    assert item["a"]["requirement"] == "required" and item["b"]["requirement"] == "nice_to_have"
    assert item["decision"] == "?"


def test_merge_queues_a_skill_only_one_labeler_gave():
    b = ok_answer(expected=ok_answer()["expected"][:2])
    m = merged_for(ok_answer(), b)
    item, = m.review
    assert item["key"] == "docker" and item["reason"] == "disagreement"
    assert item["a"]["skill_id"] == "docker" and item["b"] is None


def test_merge_pairs_the_same_evidence_mapped_to_different_ids():
    a = ok_answer(expected=[{"skill_id": "rag", "requirement": "required",
                             "raw_text": "experience with RAG pipelines"}])
    b = ok_answer(expected=[{"skill_id": "llms", "requirement": "required",
                             "raw_text": "experience with RAG   pipelines"}])
    m = merged_for(a, b)
    item, = [i for i in m.review if i["kind"] == "skill"]
    assert item["reason"] == "mapping" and item["key"] == "rag|llms"
    assert item["a"]["skill_id"] == "rag" and item["b"]["skill_id"] == "llms"


def test_merge_queues_an_uncertain_flag_even_when_both_agree():
    a = ok_answer()
    a["expected"] = [dict(a["expected"][0], uncertain=True), *a["expected"][1:]]
    a["uncertain"] = ["german"]
    m = merged_for(a, ok_answer())
    reasons = {(i["kind"], i["key"]): i["reason"] for i in m.review}
    assert reasons == {("skill", "python"): "uncertain", ("attribute", "german"): "uncertain"}
    assert "german" not in m.accepted_attrs and "seniority" in m.accepted_attrs


def test_merge_queues_an_attribute_disagreement_per_field():
    b = ok_answer(seniority="mid", seniority_basis="inferred",
                  seniority_signal="6+ years of professional experience")
    m = merged_for(ok_answer(), b)
    item, = m.review
    assert (item["kind"], item["key"], item["reason"]) == ("attribute", "seniority", "disagreement")
    assert item["a"]["seniority"] == "senior" and item["b"]["seniority"] == "mid"
    assert sorted(m.accepted_attrs) == ["degree", "german"]


def test_merge_sends_a_check_failure_to_review_rather_than_dropping_it():
    b = ok_answer(expected=[
        {"skill_id": "python", "requirement": "required", "raw_text": "unbeatable Python skills"},
        *ok_answer()["expected"][1:]])
    m = merged_for(ok_answer(), b)
    item, = m.review
    assert item["key"] == "python" and item["reason"] == "check-failed"
    assert any("B: raw_text does not appear" in p for p in item["problems"])
    assert "python" not in {s["skill_id"] for s in m.accepted_skills}


def test_merge_keeps_as_agreed_when_only_the_quoted_signal_differs():
    b = ok_answer(seniority_signal="6+ years of professional experience building LLM applications")
    m = merged_for(ok_answer(), b)
    assert m.review == [] and m.accepted_attrs["seniority"]["seniority"] == "senior"
    assert m.signal_mismatches and "golden_030 seniority" in m.signal_mismatches[0]


# --- the same-model refusal -------------------------------------------------------

def test_refuses_a_labeler_on_the_extractors_model():
    with pytest.raises(SystemExit, match="the extractor's model"):
        al.check_models("claude-sonnet-5-5", "gpt-5.6", extractor="claude-sonnet-5-5")
    with pytest.raises(SystemExit, match="labeler B is"):
        al.check_models("claude-opus-5-5", "claude-sonnet-5-5", extractor="claude-sonnet-5-5")


def test_refuses_two_copies_of_one_model():
    with pytest.raises(SystemExit, match="not two labelers"):
        al.check_models("claude-opus-5-5", "claude-opus-5-5", extractor="claude-sonnet-5-5")


def test_allows_two_different_non_extractor_models():
    assert al.check_models("claude-opus-5-5", "gpt-5.6", extractor="claude-sonnet-5-5") is None


# --- spot-check sampling ----------------------------------------------------------

def many_merged(n_postings=6, n_skills=10):
    out = []
    for p in range(n_postings):
        m = al.Merged(golden_id=f"golden_{p:03d}")
        m.accepted_skills = [{"skill_id": f"s{i}", "requirement": "required", "raw_text": "x"}
                             for i in range(n_skills)]
        m.accepted_attrs = {a: {} for a in ("seniority", "german", "degree")}
        out.append(m)
    return out


def test_spot_check_is_seeded_and_reproducible():
    pool = many_merged()
    first = al.spot_check_sample(pool, 20, seed=7)
    assert first == al.spot_check_sample(pool, 20, seed=7)
    assert first != al.spot_check_sample(pool, 20, seed=8)


def test_spot_check_samples_labels_not_postings():
    sample = al.spot_check_sample(many_merged(), 20, seed=3)
    assert len(sample) == 20
    assert all(kind in ("skill", "attribute") and key for _, kind, key in sample)
    # 20 labels drawn from 6 postings must repeat postings and must not be whole postings
    by_posting = {}
    for gid, kind, key in sample:
        by_posting.setdefault(gid, []).append(key)
    assert max(len(v) for v in by_posting.values()) < 13  # a whole posting is 13 labels
    assert len(sample) == len(set(sample))


def test_spot_check_takes_everything_when_the_pool_is_smaller_than_asked():
    pool = many_merged(n_postings=1, n_skills=2)
    assert len(al.spot_check_sample(pool, 80, seed=0)) == 5  # 2 skills + 3 attributes


def test_spot_check_pool_excludes_queued_labels():
    b = ok_answer(expected=ok_answer()["expected"][:2])  # docker is one-sided -> queued
    m = merged_for(ok_answer(), b)
    keys = {key for _, kind, key in al.spot_check_sample([m], 80, seed=0) if kind == "skill"}
    assert keys == {"python", "rag"}


# --- applying decisions -----------------------------------------------------------

def test_apply_decision_skill_words():
    item = {"kind": "skill", "key": "rag", "reason": "disagreement",
            "a": {"skill_id": "rag", "requirement": "required", "raw_text": "RAG"},
            "b": {"skill_id": "rag", "requirement": "nice_to_have", "raw_text": "RAG"}}
    assert al.apply_decision(item, "A") == ([item["a"]], None)
    assert al.apply_decision(item, "`b`") == ([item["b"]], None)
    assert al.apply_decision(item, "drop") == ([], None)
    assert al.apply_decision(dict(item, key="rag|llms", reason="mapping"), "both")[0] == [item["a"], item["b"]]


def test_apply_decision_rejects_a_word_the_item_does_not_allow():
    item = {"kind": "skill", "key": "docker", "reason": "disagreement",
            "a": {"skill_id": "docker", "requirement": "required", "raw_text": "Docker"}, "b": None}
    with pytest.raises(ValueError, match="labeler B did not label"):
        al.apply_decision(item, "B")
    with pytest.raises(ValueError, match="needs an agreed value"):
        al.apply_decision(item, "ok")
    with pytest.raises(ValueError, match="not one of"):
        al.apply_decision(item, "maybe")
    with pytest.raises(ValueError, match="no decision"):
        al.apply_decision(item, "?")


def test_apply_decision_json_override():
    item = {"kind": "skill", "key": "rag", "reason": "disagreement",
            "a": {"skill_id": "rag", "requirement": "required", "raw_text": "RAG"}, "b": None}
    add, group = al.apply_decision(item, '{"requirement": "nice_to_have", "raw_text": "RAG pipelines"}')
    assert add == [{"skill_id": "rag", "requirement": "nice_to_have", "raw_text": "RAG pipelines"}]
    assert group is None

    attr = {"kind": "attribute", "key": "degree", "reason": "disagreement", "a": {}, "b": {}}
    _, group = al.apply_decision(attr, '{"degree": "bachelor", "degree_requirement": "required",'
                                       ' "degree_signal": "Degree in CS"}')
    assert group == {"degree": "bachelor", "degree_requirement": "required",
                     "degree_or_equivalent": False, "degree_signal": "Degree in CS"}
    with pytest.raises(ValueError, match="not part of degree"):
        al.apply_decision(attr, '{"seniority": "senior"}')


def test_apply_decision_drop_nulls_a_whole_attribute_group():
    item = {"kind": "attribute", "key": "german", "reason": "disagreement", "a": {}, "b": {}}
    assert al.apply_decision(item, "drop") == (
        [], {"german": None, "german_basis": None, "german_signal": None})


def test_parse_queue_reads_one_decision_per_item_in_order():
    text = al.render_queue("r1", {
        "seed": 0, "provider_a": "anthropic", "model_a": "m-a", "provider_b": "openai",
        "model_b": "m-b", "extractor": "m-x", "spot_n": 1, "spot_pool": 9}, [
        {"golden_id": "golden_030", "kind": "skill", "key": "rag", "reason": "disagreement",
         "a": {"skill_id": "rag", "requirement": "required", "raw_text": "RAG"},
         "b": {"skill_id": "rag", "requirement": "nice_to_have", "raw_text": "RAG"},
         "excerpt": "…RAG…", "problems": [], "decision": "?"},
        {"golden_id": "golden_030", "kind": "attribute", "key": "german", "reason": "spot-check",
         "a": {"german": "required"}, "b": {"german": "required"},
         "excerpt": "…German…", "problems": [], "decision": "?"}])
    assert al.parse_queue(text) == [(1, "?"), (2, "?")]
    assert al.parse_queue(text.replace("DECISION: ?", "DECISION: A", 1)) == [(1, "A"), (2, "?")]


# --- the final Golden -------------------------------------------------------------

def test_final_golden_matches_the_attribute_registry_plus_provenance():
    # The shape is the attribute registry plus the fields the eval reads plus HIR-70
    # provenance - not whatever one committed Golden happens to carry. Asserting against a
    # single file coupled this test to Goldens labeled under other rules: a fourth attribute
    # added on another branch broke it while final_golden was still correct for its own three.
    attr_fields = {f for fields in al.ATTR_FIELDS.values() for f in fields}
    eval_fields = {"id", "split", "source_sha256", "job_description", "expected",
                   "seniority_reviewed", "attrs_reviewed"}
    provenance = {"labeled_by", "adjudicated", "spot_checked"}
    base = {"id": "golden_030", "source_sha256": "abc", "job_description": POSTING}
    golden = al.final_golden(
        base,
        [{"skill_id": "rag", "requirement": "required", "raw_text": "RAG pipelines"},
         {"skill_id": "python", "requirement": "required", "raw_text": "Strong Python"}],
        {"seniority": {"seniority": "senior", "seniority_basis": "inferred",
                       "seniority_signal": "6+ years of professional experience"},
         "german": {"german": "required", "german_basis": "stated",
                    "german_signal": "Fluent German (C1)"}},
        labeled_by=["claude-opus-5-5", "gpt-5.6"], adjudicated=["german", "skill:rag"],
        spot_checked=True)

    assert set(golden) == attr_fields | eval_fields | provenance, (
        "a Golden lost a key the eval reads, or gained one nothing reads")
    assert list(golden)[:2] == ["id", "split"] and golden["split"] == "heldout"
    assert golden["labeled_by"] == ["claude-opus-5-5", "gpt-5.6"]
    assert golden["adjudicated"] == ["german", "skill:rag"] and golden["spot_checked"] is True
    # a person decided german but not seniority, so only attrs_reviewed is true
    assert golden["attrs_reviewed"] is True and golden["seniority_reviewed"] is False
    # an attribute nobody labeled is null, not missing; expected is sorted by skill_id
    assert golden["degree"] is None and golden["degree_or_equivalent"] is False
    assert [e["skill_id"] for e in golden["expected"]] == ["python", "rag"]
    assert all(set(e) == {"skill_id", "requirement", "raw_text"} for e in golden["expected"])
    assert "draft" not in golden


# --- agreement and the Wilson interval --------------------------------------------

def test_agreement_scores_b_against_a():
    a = ok_answer()
    b = ok_answer(expected=[
        {"skill_id": "python", "requirement": "required", "raw_text": "Strong Python"},
        {"skill_id": "rag", "requirement": "nice_to_have", "raw_text": "RAG pipelines"},
        {"skill_id": "llms", "requirement": "required", "raw_text": "LLM applications"}],
        german=None, german_basis=None, german_signal=None)
    report = al.agreement([al.Merged(golden_id="golden_030")], {"golden_030": {"A": a, "B": b}})
    assert report["skills"] == {"tp": 2, "fp": 1, "fn": 1, "precision": 2 / 3, "recall": 2 / 3,
                                "f1": pytest.approx(2 / 3)}
    assert report["requirement_agreement"] == 0.5  # python agrees, rag does not
    assert report["attributes"]["seniority"]["rate"] == 1.0
    assert report["attributes"]["german"]["rate"] == 0.0


def test_wilson_interval():
    assert al.wilson(0, 0) == (None, None)
    lo, hi = al.wilson(0, 80)
    assert lo == 0.0 and 0.0 < hi < 0.06          # zero errors still leaves an upper bound
    lo, hi = al.wilson(4, 80)
    assert lo < 0.05 < hi and 0 < lo and hi < 0.13
    lo, hi = al.wilson(1, 1)
    assert hi == 1.0 and lo > 0.0                  # never outside [0, 1], unlike the normal approx


# --- prompt assembly and response parsing -----------------------------------------

def test_labeler_prompt_inlines_the_guide_and_the_taxonomy_without_parents():
    prompt = al.labeler_prompt(
        (ROOT / "evals" / "LABELER_PROMPT.md").read_text(),
        (ROOT / "evals" / "LABELING.md").read_text(), TAX)
    assert "TAXONOMY (version 9)" in prompt and "rag: RAG [Retrieval-Augmented Generation]" in prompt
    assert "## requirement: `required` or `nice_to_have`" in prompt   # the guide, verbatim
    assert "{LABELING.md" not in prompt and "{TAXONOMY" not in prompt
    # the taxonomy block carries ids, display names and aliases, and nothing else
    assert "rag: RAG [Retrieval-Augmented Generation]\n" in prompt + "\n"
    assert "parents]" not in prompt and "- parents" not in prompt
    assert "<posting>" not in prompt                                   # the posting is the user turn
    assert "System prompt for the independent labeler agents" not in prompt  # file docs dropped


def test_labeler_prompt_never_carries_the_extractors_prompt():
    from app.extract import PRINCIPLES
    prompt = al.labeler_prompt((ROOT / "evals" / "LABELER_PROMPT.md").read_text(),
                               (ROOT / "evals" / "LABELING.md").read_text(), TAX)
    assert PRINCIPLES.splitlines()[0] not in prompt


@pytest.mark.parametrize("text", [
    '{"expected": []}',
    'Here you go:\n```json\n{"expected": []}\n```\n',
    'I labeled it.\n{"expected": []}\nLet me know.',
    '{"expected": [], "notes": "the brace } is inside a string"}',
])
def test_parse_response_finds_the_one_object(text):
    assert "expected" in al.parse_response(text)


def test_parse_response_rejects_prose():
    with pytest.raises(ValueError, match="no JSON object"):
        al.parse_response("I cannot label this posting.")


# --- picking ----------------------------------------------------------------------

DE = ("Wir suchen eine KI-Entwicklerin für unser Team in Berlin. Du arbeitest mit Python und der "
      "Cloud, bist für die Pipelines zuständig und bringst Erfahrung mit LLMs mit. ") * 4
EN = ("We are looking for an AI engineer for our team in Berlin. You work with Python and the "
      "cloud, own the pipelines and bring experience with LLMs. ") * 4


def db_rows(tmp_path):
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    conn.executescript(
        "CREATE TABLE job (id INTEGER PRIMARY KEY, company TEXT, title TEXT, city TEXT, seniority TEXT,"
        " description_text TEXT, first_seen TEXT, extracted_version TEXT);"
        "CREATE TABLE job_source (job_id INTEGER, source TEXT);")
    jobs, sources = [], []
    for i in range(1, 21):
        german = i % 3 == 0
        jobs.append((i, f"Co{i}", ["Senior AI Engineer", "Data Engineer", "ML Engineer",
                                   "Werkstudent KI"][i % 4],
                     "Remote (EU)" if i in (4, 9, 14) else "Berlin",
                     [None, "junior", "mid", "senior"][i % 4],
                     (DE if german else EN) + f" #{i}", "2026-10-20", None))
        sources.append((i, ["greenhouse", "arbeitsagentur", "ashby", "jsearch"][i % 4]))
    conn.executemany("INSERT INTO job VALUES (?,?,?,?,?,?,?,?)", jobs)
    conn.executemany("INSERT INTO job_source VALUES (?,?)", sources)
    conn.commit()
    return al.ng.candidates(conn, set())  # the query agent_label shares with new_goldens


def test_pick_honours_quotas_and_is_seeded(tmp_path):
    rows = db_rows(tmp_path)
    picks = al.pick(rows, count=8, seed=5, quotas={"remote_eu": 2, "german": 3})
    assert len(picks) == 8
    assert [r["id"] for r in picks] == [r["id"] for r in al.pick(rows, 8, 5, {"remote_eu": 2, "german": 3})]
    described = [al.describe(r) for r in picks]
    assert sum(1 for d in described if d["place"] == "Remote (EU)") >= 2
    assert sum(1 for d in described if d["language"] == "de") >= 3


def test_pick_spreads_across_strata_when_it_can(tmp_path):
    rows = db_rows(tmp_path)
    described = [al.describe(r) for r in al.pick(rows, count=8, seed=1, quotas={})]
    assert len({d["seniority"] for d in described}) >= 3
    assert len({d["source"] for d in described}) >= 3
    assert len({d["role"] for d in described}) >= 3


def test_pick_takes_a_named_source_and_seniority_quota(tmp_path):
    rows = db_rows(tmp_path)
    picks = al.pick(rows, count=6, seed=2,
                    quotas={"source:jsearch": 2, "seniority:junior": 2})
    described = [al.describe(r) for r in picks]
    assert sum(1 for d in described if "jsearch" in d["sources"]) >= 2
    assert sum(1 for d in described if d["seniority"] == "junior") >= 2


def test_pick_reports_a_quota_the_corpus_cannot_meet(tmp_path):
    rows = db_rows(tmp_path)          # the fixture has exactly 3 Remote (EU) postings
    unmet = []
    picks = al.pick(rows, count=8, seed=0, quotas={"remote_eu": 5}, unmet=unmet)
    assert unmet == ["remote_eu: asked for 5, the corpus has 3"]
    assert sum(1 for r in picks if al.describe(r)["place"] == "Remote (EU)") == 3
    met = []
    al.pick(rows, 8, 0, {"remote_eu": 3}, unmet=met)
    assert met == []                  # a quota the corpus can meet stays silent


def test_pick_rejects_an_unknown_quota(tmp_path):
    with pytest.raises(ValueError, match="unknown quota"):
        al.pick(db_rows(tmp_path), 4, 0, {"city:Paris": 1})


def test_excerpt_shows_the_quote_in_context_on_word_boundaries():
    e = al.excerpt(POSTING, "RAG pipelines")
    assert "RAG pipelines" in e and e.startswith("...") and e.endswith("...")
    assert not e.startswith("...trong")                 # no half words at the edges
    assert "\n" not in e
    # the window reaches the start of the posting, so there is nothing elided before it
    assert al.excerpt(POSTING, "Strong Python").startswith("Senior AI Engineer")
    assert al.excerpt(POSTING, "a phrase that is not there").startswith("(not found")
    assert al.excerpt(POSTING, None) == "Senior AI Engineer (m/f/d)"         # falls back to the title


def test_role_family():
    assert al.role_family("Senior Data Engineer (m/f/d)") == "data-engineer"
    assert al.role_family("Machine Learning Engineer") == "ml-engineer"
    assert al.role_family("Werkstudent KI") == "ai-engineer"
    assert al.role_family("Office Manager") == "other"
    assert al.role_family(None) == "other"


# --- the pipeline, end to end with a fake client ----------------------------------

class FakeAnthropic:
    """Returns one canned answer per call, in order."""

    def __init__(self, answers):
        self.answers = list(answers)
        self.calls = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        body = json.dumps(self.answers.pop(0))
        return type("R", (), {"content": [type("B", (), {"type": "text", "text": body})()]})()


def test_label_posting_sends_only_the_prompt_and_the_posting():
    client = FakeAnthropic([ok_answer()])
    record = al.label_posting(POSTING, "SYSTEM", "anthropic", "claude-opus-5-5", client)
    assert record["parsed"]["expected"][0]["skill_id"] == "python"
    assert record["error"] is None
    call, = client.calls
    assert call["model"] == "claude-opus-5-5"
    assert call["system"][0]["text"] == "SYSTEM"
    assert call["messages"] == [{"role": "user", "content": f"<posting>\n{POSTING}\n</posting>"}]


def test_label_posting_records_a_bad_response_instead_of_raising():
    record = al.label_posting(POSTING, "S", "anthropic", "m", FakeAnthropic(["not json at all"]))
    assert record["parsed"] is None and "no JSON object" in record["error"]


def test_label_then_apply_writes_a_golden_and_reuses_the_cached_calls(tmp_path, monkeypatch, capsys):
    goldens = tmp_path / "goldens"
    goldens.mkdir()
    runs = tmp_path / "labeling"
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        "CREATE TABLE job (id INTEGER PRIMARY KEY, company TEXT, title TEXT, city TEXT, seniority TEXT,"
        " description_text TEXT, first_seen TEXT, extracted_version TEXT);"
        "CREATE TABLE job_source (job_id INTEGER, source TEXT);")
    conn.execute("INSERT INTO job VALUES (1,'Acme','Senior AI Engineer','Berlin','senior',?,'2026-10-20',NULL)",
                 (POSTING,))
    conn.execute("INSERT INTO job_source VALUES (1, 'greenhouse')")
    conn.commit()
    conn.close()

    monkeypatch.setattr(al, "GOLDENS", goldens)
    monkeypatch.setattr(al, "RUNS", runs)
    monkeypatch.setattr(al.ng, "DB", db)
    monkeypatch.setattr(al.ng, "GOLDENS", goldens)
    # Labeler B disagrees on docker's requirement, so one item needs a decision.
    b = ok_answer(expected=[
        *ok_answer()["expected"][:2],
        {"skill_id": "docker", "requirement": "required", "raw_text": "Docker"}])
    made = {}

    def fake_client(provider):
        made[provider] = FakeAnthropic([ok_answer() if provider == "anthropic" else b])
        return made[provider]

    monkeypatch.setattr(al, "make_client", fake_client)
    monkeypatch.setitem(al.PROVIDERS, "openai", al.call_anthropic)  # the fake speaks one API

    al.main(["label", "--count", "1", "--spot-check", "2", "--seed", "0",
             "--remote-eu", "0", "--german", "0"])
    run_dir, = list(runs.iterdir())
    queue = run_dir / "review_queue.md"
    items = json.loads((run_dir / "items.json").read_text())
    assert [i["reason"] for i in items].count("disagreement") == 1
    assert [i["reason"] for i in items].count("spot-check") == 2
    assert "DECISION: ?" in queue.read_text()

    # re-merge: the cached raw answers are reused, no client is made
    made.clear()
    al.main(["label", "--run", run_dir.name, "--spot-check", "2", "--seed", "0"])
    assert made == {}

    with pytest.raises(SystemExit, match="still say `?`"):
        al.main(["apply", "--run", run_dir.name])

    # once decisions exist, a re-merge would throw them away, so it refuses
    queue.write_text(queue.read_text().replace("DECISION: ?", "DECISION: A", 1))
    with pytest.raises(SystemExit, match="already has 1 decisions"):
        al.main(["label", "--run", run_dir.name, "--spot-check", "2"])

    queue.write_text(queue.read_text().replace("DECISION: ?", "DECISION: A").replace(
        "DECISION: A", "DECISION: ok", 0))
    text = queue.read_text()
    # answer the disagreement with A and the two spot-checks with ok
    out = []
    for block in text.split("\n## "):
        if "(spot-check)" in block.split("\n")[0]:
            block = block.replace("DECISION: A", "DECISION: ok")
        out.append(block)
    queue.write_text("\n## ".join(out))

    al.main(["apply", "--run", run_dir.name])
    golden = json.loads((goldens / "golden_001.json").read_text())
    assert golden["split"] == "heldout" and "draft" not in golden
    assert {e["skill_id"] for e in golden["expected"]} == {"python", "rag", "docker"}
    assert next(e for e in golden["expected"] if e["skill_id"] == "docker")["requirement"] == "nice_to_have"
    assert golden["labeled_by"] == [al.DEFAULT_MODEL_A, al.DEFAULT_MODEL_B]
    assert golden["adjudicated"] == ["skill:docker"] and golden["spot_checked"] is True
    assert golden["job_description"].startswith("Senior AI Engineer")
    summary = json.loads((run_dir / "summary.json").read_text())
    assert summary["spot_check"]["errors"] == 0 and summary["spot_check"]["n"] == 2
    assert summary["spot_check"]["wilson_95"][0] == 0.0
    assert "Spot-check error rate" in (run_dir / "summary.md").read_text()


def test_dry_run_makes_no_calls_and_writes_nothing(tmp_path, monkeypatch, capsys):
    goldens = tmp_path / "goldens"
    goldens.mkdir()
    runs = tmp_path / "labeling"
    rows_db = tmp_path / "t.db"
    conn = sqlite3.connect(rows_db)
    conn.executescript(
        "CREATE TABLE job (id INTEGER PRIMARY KEY, company TEXT, title TEXT, city TEXT, seniority TEXT,"
        " description_text TEXT, first_seen TEXT, extracted_version TEXT);"
        "CREATE TABLE job_source (job_id INTEGER, source TEXT);")
    conn.execute("INSERT INTO job VALUES (1,'Acme','Senior AI Engineer','Berlin','senior',?,'2026-10-20',NULL)",
                 (POSTING,))
    conn.execute("INSERT INTO job_source VALUES (1, 'greenhouse')")
    conn.commit()
    conn.close()
    monkeypatch.setattr(al, "GOLDENS", goldens)
    monkeypatch.setattr(al, "RUNS", runs)
    monkeypatch.setattr(al.ng, "DB", rows_db)
    monkeypatch.setattr(al.ng, "GOLDENS", goldens)

    def boom(provider):
        raise AssertionError("a dry run must not make a client")

    monkeypatch.setattr(al, "make_client", boom)
    al.main(["label", "--dry-run", "--count", "1", "--remote-eu", "0", "--german", "0"])
    out = capsys.readouterr().out
    assert "golden_001" in out and "Senior AI Engineer" in out
    assert "seniority: senior=1" in out and "place: Berlin=1" in out
    assert not runs.exists()


def test_a_guide_edit_invalidates_the_cached_labels(tmp_path, monkeypatch):
    """LABELING.md is inlined into the prompt, so editing it must re-call the labelers.

    Without the prompt in the cache key, a --run re-merge after a guide change silently
    reuses labels made under the old rules and scores them as if they followed the new ones.
    """
    goldens = tmp_path / "goldens"
    goldens.mkdir()
    runs = tmp_path / "labeling"
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        "CREATE TABLE job (id INTEGER PRIMARY KEY, company TEXT, title TEXT, city TEXT, seniority TEXT,"
        " description_text TEXT, first_seen TEXT, extracted_version TEXT);"
        "CREATE TABLE job_source (job_id INTEGER, source TEXT);")
    conn.execute("INSERT INTO job VALUES (1,'Acme','Senior AI Engineer','Berlin','senior',?,'2026-10-20',NULL)",
                 (POSTING,))
    conn.execute("INSERT INTO job_source VALUES (1, 'greenhouse')")
    conn.commit()
    conn.close()

    monkeypatch.setattr(al, "GOLDENS", goldens)
    monkeypatch.setattr(al, "RUNS", runs)
    monkeypatch.setattr(al.ng, "DB", db)
    monkeypatch.setattr(al.ng, "GOLDENS", goldens)
    monkeypatch.setitem(al.PROVIDERS, "openai", al.call_anthropic)

    made = {}

    def fake_client(provider):
        made[provider] = FakeAnthropic([ok_answer()])
        return made[provider]

    monkeypatch.setattr(al, "make_client", fake_client)
    monkeypatch.setattr(al, "labeler_prompt", lambda *a, **k: "GUIDE VERSION ONE")

    al.main(["label", "--count", "1", "--spot-check", "1", "--seed", "0",
             "--remote-eu", "0", "--german", "0"])
    run_dir, = list(runs.iterdir())
    raw = json.loads((run_dir / "raw" / "golden_001.A.json").read_text())
    assert raw["prompt_sha256"] == al.ng.sha("GUIDE VERSION ONE")

    # same prompt -> cache hit, no client made
    made.clear()
    al.main(["label", "--run", run_dir.name, "--spot-check", "1", "--seed", "0"])
    assert made == {}

    # edited guide -> cache miss, labelers called again and the new hash stored
    monkeypatch.setattr(al, "labeler_prompt", lambda *a, **k: "GUIDE VERSION TWO")
    made.clear()
    al.main(["label", "--run", run_dir.name, "--spot-check", "1", "--seed", "0"])
    assert set(made) == {"anthropic", "openai"}
    raw = json.loads((run_dir / "raw" / "golden_001.A.json").read_text())
    assert raw["prompt_sha256"] == al.ng.sha("GUIDE VERSION TWO")


@pytest.mark.parametrize("decision, keep, why", [
    ("yes", True, ""),
    ("`yes`", True, ""),
    ("YES", True, ""),
    ("no", False, ""),
    ("no marketing role, not AI engineering", False, "marketing role, not AI engineering"),
    ("no: wrong field", False, "wrong field"),
    ("no — a sales listing", False, "a sales listing"),
])
def test_parse_scope_vocabulary(decision, keep, why):
    assert al.parse_scope(decision) == (keep, why)


@pytest.mark.parametrize("bad", ["", "?", "maybe", "drop", "A", "nope"])
def test_parse_scope_rejects_anything_else(bad):
    with pytest.raises(ValueError):
        al.parse_scope(bad)


def _scope_run(tmp_path, monkeypatch, postings, answers=None):
    """A run over `postings` [(company, title, text)], with the scope item in the queue.

    `answers` maps a provider to the one answer its labeler returns, so the two labelers
    can be made to disagree; by default both return `ok_answer()` and agree on everything.
    """
    goldens = tmp_path / "goldens"
    goldens.mkdir()
    runs = tmp_path / "labeling"
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        "CREATE TABLE job (id INTEGER PRIMARY KEY, company TEXT, title TEXT, city TEXT, seniority TEXT,"
        " description_text TEXT, first_seen TEXT, extracted_version TEXT);"
        "CREATE TABLE job_source (job_id INTEGER, source TEXT);")
    for i, (company, title, text) in enumerate(postings, 1):
        conn.execute("INSERT INTO job VALUES (?,?,?,'Berlin','senior',?,'2026-10-20',NULL)",
                     (i, company, title, text))
        conn.execute("INSERT INTO job_source VALUES (?, 'greenhouse')", (i,))
    conn.commit()
    conn.close()

    monkeypatch.setattr(al, "GOLDENS", goldens)
    monkeypatch.setattr(al, "RUNS", runs)
    monkeypatch.setattr(al.ng, "DB", db)
    monkeypatch.setattr(al.ng, "GOLDENS", goldens)
    monkeypatch.setattr(al.ng, "EXCLUDED", goldens / "excluded.json")
    answers = answers or {}
    monkeypatch.setattr(al, "make_client", lambda provider: FakeAnthropic(
        [answers.get(provider, ok_answer())] * len(postings)))
    monkeypatch.setitem(al.PROVIDERS, "openai", al.call_anthropic)
    al.main(["label", "--count", str(len(postings)), "--spot-check", "1", "--seed", "0",
             "--remote-eu", "0", "--german", "0"])
    run_dir, = list(runs.iterdir())
    return goldens, run_dir


def test_scope_items_come_first_and_pre_answered_yes(tmp_path, monkeypatch):
    goldens, run_dir = _scope_run(tmp_path, monkeypatch, [("Acme", "Senior AI Engineer", POSTING)])
    items = json.loads((run_dir / "items.json").read_text())
    assert items[0]["kind"] == "scope" and items[0]["key"] == "in_scope"
    assert items[0]["reason"] == "in-scope" and items[0]["decision"] == "yes"
    assert all(i["kind"] != "scope" for i in items[1:])

    text = (run_dir / "review_queue.md").read_text()
    assert "## 1. golden_001 - scope `in_scope` (in-scope)" in text
    assert "DECISION: yes" in text
    # the default is not a decision, so a re-merge is still allowed
    al.main(["label", "--run", run_dir.name, "--spot-check", "1", "--seed", "0"])


def test_scope_yes_still_writes_the_golden(tmp_path, monkeypatch):
    goldens, run_dir = _scope_run(tmp_path, monkeypatch, [("Acme", "Senior AI Engineer", POSTING)])
    queue = run_dir / "review_queue.md"
    queue.write_text(queue.read_text().replace("DECISION: ?", "DECISION: ok"))
    al.main(["apply", "--run", run_dir.name])
    assert (goldens / "golden_001.json").exists()
    assert not (goldens / "excluded.json").exists()


def test_scope_no_writes_excluded_json_instead_of_a_golden(tmp_path, monkeypatch, capsys):
    goldens, run_dir = _scope_run(tmp_path, monkeypatch, [("benuta", "Marketing Manager", POSTING)])
    queue = run_dir / "review_queue.md"
    text = queue.read_text().replace("DECISION: ?", "DECISION: ok")
    # the other items stay answered; a `no` makes them irrelevant
    queue.write_text(text.replace("DECISION: yes", "DECISION: no marketing role, not AI engineering"))

    al.main(["apply", "--run", run_dir.name])
    assert not (goldens / "golden_001.json").exists()

    record = json.loads((goldens / "excluded.json").read_text())["excluded"]
    assert len(record) == 1
    e = record[0]
    assert e["golden_id"] == "golden_001"
    assert e["reason"] == "marketing role, not AI engineering"
    assert e["company"] == "benuta" and e["title"] == "Marketing Manager"
    assert e["source_sha256"] == al.ng.sha(POSTING)
    assert e["run"] == run_dir.name and e["labeled_by"] == [al.DEFAULT_MODEL_A, al.DEFAULT_MODEL_B]
    assert "ruled out of scope" in capsys.readouterr().out

    # an excluded posting's spot-checks must not count toward the error rate
    summary = json.loads((run_dir / "summary.json").read_text())
    assert summary["spot_check"]["n"] == 0


def test_an_excluded_posting_is_never_picked_again(tmp_path, monkeypatch):
    goldens = tmp_path / "goldens"
    goldens.mkdir()
    monkeypatch.setattr(al.ng, "GOLDENS", goldens)
    monkeypatch.setattr(al.ng, "EXCLUDED", goldens / "excluded.json")

    assert al.ng.existing() == (set(), 0)

    (goldens / "excluded.json").write_text(json.dumps({"excluded": [
        {"golden_id": "golden_048", "source_sha256": al.ng.sha(POSTING),
         "company": "benuta", "title": "Marketing Manager", "reason": "marketing role"}]}))
    used, top = al.ng.existing()
    assert al.ng.sha(POSTING) in used
    # the number stays spent, so the next Golden does not reuse golden_048
    assert top == 48

    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        "CREATE TABLE job (id INTEGER PRIMARY KEY, company TEXT, title TEXT, city TEXT, seniority TEXT,"
        " description_text TEXT, first_seen TEXT, extracted_version TEXT);"
        "CREATE TABLE job_source (job_id INTEGER, source TEXT);")
    conn.execute("INSERT INTO job VALUES (1,'benuta','Marketing Manager','Berlin','senior',?,'2026-10-20',NULL)",
                 (POSTING,))
    conn.execute("INSERT INTO job VALUES (2,'Acme','AI Engineer','Berlin','senior','Other posting entirely','2026-10-20',NULL)")
    conn.execute("INSERT INTO job_source VALUES (1, 'greenhouse'), (2, 'greenhouse')")
    conn.commit()
    conn.row_factory = sqlite3.Row
    rows = al.ng.candidates(conn, used)
    assert [r["id"] for r in rows] == [2]


# --- queue order and blind spot-checks --------------------------------------------

def _b_drops_docker():
    """Labeler B's answer: the same as A's minus `docker`, so `docker` is one-sided."""
    return {"openai": ok_answer(expected=[s for s in ok_answer()["expected"]
                                          if s["skill_id"] != "docker"])}


def test_queue_is_grouped_by_what_it_asks_of_the_reviewer(tmp_path, monkeypatch):
    _, run_dir = _scope_run(tmp_path, monkeypatch, [("Acme", "Senior AI Engineer", POSTING)],
                            answers=_b_drops_docker())
    items = json.loads((run_dir / "items.json").read_text())
    reasons = [i["reason"] for i in items]
    assert reasons[0] == "in-scope"
    assert "disagreement" in reasons and "spot-check" in reasons
    # every group is contiguous and in the documented order
    assert reasons == sorted(reasons, key=al.REASON_ORDER.__getitem__)
    assert reasons.index("disagreement") < reasons.index("spot-check")


def test_a_spot_check_item_hides_both_labelers(tmp_path, monkeypatch):
    _, run_dir = _scope_run(tmp_path, monkeypatch, [("Acme", "Senior AI Engineer", POSTING)],
                            answers=_b_drops_docker())
    items = json.loads((run_dir / "items.json").read_text())
    spot = [(n, i) for n, i in enumerate(items, 1) if i["reason"] == "spot-check"]
    assert spot
    for n, item in spot:
        block = al.render_item(n, item)
        assert "- agreed label: " in block
        assert "- A: " not in block and "- B: " not in block
        # the posting excerpt and the label itself are still there to judge it by
        assert block.split("\n")[2].startswith(">")
        assert f"`{item['key']}`" in block
    # a disagreement still names who said what
    dis = [(n, i) for n, i in enumerate(items, 1) if i["reason"] == "disagreement"]
    n, item = dis[0]
    assert "- A: " in al.render_item(n, item) and "- B: " in al.render_item(n, item)


def _answer(queue, by_item):
    """Rewrite the queue, setting item n's DECISION to by_item(n, block) for every item."""
    out, text = [], queue.read_text()
    head, *blocks = re.split(r"(?m)^(?=## \d+\. )", text)
    out.append(head)
    for b in blocks:
        n = int(re.match(r"## (\d+)\.", b).group(1))
        want = by_item(n, b)
        out.append(re.sub(r"(?m)^DECISION: .*$", f"DECISION: {want}", b) if want else b)
    queue.write_text("".join(out))


def test_apply_ignores_undecided_items_of_an_out_of_scope_posting(tmp_path, monkeypatch, capsys):
    goldens, run_dir = _scope_run(tmp_path, monkeypatch,
                                  [("Acme", "Senior AI Engineer", POSTING),
                                   ("benuta", "Marketing Manager", POSTING)])
    items = json.loads((run_dir / "items.json").read_text())
    gid = {n: i["golden_id"] for n, i in enumerate(items, 1)}
    scope = {n: i["golden_id"] for n, i in enumerate(items, 1) if i["kind"] == "scope"}
    out, keep = "golden_002", "golden_001"
    assert set(scope.values()) == {keep, out}

    queue = run_dir / "review_queue.md"
    # the out-of-scope posting is answered `no`; none of its other items are answered at all
    _answer(queue, lambda n, b: ("no marketing role" if scope.get(n) == out else
                                 "yes" if n in scope else
                                 "ok" if gid[n] == keep else "?"))
    # only the excluded posting's own items are left undecided -- otherwise this proves nothing
    undecided = [n for n, d in al.parse_queue(queue.read_text()) if d == "?"]
    assert undecided and all(gid[n] == out for n in undecided)

    al.main(["apply", "--run", run_dir.name])
    assert (goldens / f"{keep}.json").exists()
    assert not (goldens / f"{out}.json").exists()
    assert json.loads((goldens / "excluded.json").read_text())["excluded"][0]["golden_id"] == out


def test_apply_still_refuses_an_undecided_item_on_a_posting_that_stays(tmp_path, monkeypatch):
    goldens, run_dir = _scope_run(tmp_path, monkeypatch,
                                  [("Acme", "Senior AI Engineer", POSTING),
                                   ("benuta", "Marketing Manager", POSTING)])
    items = json.loads((run_dir / "items.json").read_text())
    gid = {n: i["golden_id"] for n, i in enumerate(items, 1)}
    scope = {n: i["golden_id"] for n, i in enumerate(items, 1) if i["kind"] == "scope"}
    queue = run_dir / "review_queue.md"
    # the posting that stays is one with items of its own; the other is ruled out
    keep = next(gid[n] for n in sorted(gid) if n not in scope)
    out, = set(scope.values()) - {keep}
    first_kept = min(n for n in gid if gid[n] == keep and n not in scope)
    _answer(queue, lambda n, b: (f"no marketing role" if scope.get(n) == out else
                                 "yes" if n in scope else
                                 "?" if n == first_kept else "ok"))
    with pytest.raises(SystemExit) as e:
        al.main(["apply", "--run", run_dir.name])
    assert "still say `?`" in str(e.value)
    assert not (goldens / f"{keep}.json").exists()


def test_apply_refuses_an_undecided_scope_item(tmp_path, monkeypatch):
    goldens, run_dir = _scope_run(tmp_path, monkeypatch, [("Acme", "Senior AI Engineer", POSTING)])
    queue = run_dir / "review_queue.md"
    _answer(queue, lambda n, b: "?" if n == 1 else "ok")
    with pytest.raises(SystemExit) as e:
        al.main(["apply", "--run", run_dir.name])
    assert "in-scope answer" in str(e.value)
    assert not (goldens / "golden_001.json").exists()


# --- judge: a third model rules on the items a proposal was written for -----------

def test_parse_proposal_reads_a_word_and_a_json_verdict():
    assert al.parse_proposal("`B` - qualification bullet names it") == (
        "B", "qualification bullet names it")
    assert al.parse_proposal("drop") == ("drop", "")
    verdict, why = al.parse_proposal('{"requirement": "nice_to_have"} - "is useful" is optional')
    assert json.loads(verdict) == {"requirement": "nice_to_have"}
    assert why.startswith('"is useful"')


def test_parse_proposals_scopes_each_proposal_to_its_own_item():
    """A proposal belongs to the item it is written under. Most items have none - every scope
    item, every spot-check - and scanning forward would hand item 1 item 2's proposal."""
    queue = (
        "## 1. golden_001 - scope `in_scope` (in-scope)\n\nDECISION: yes\n\n"
        "## 2. golden_001 - skill `docker` (disagreement)\n\nPROPOSED: `A` - first\n\nDECISION: ?\n\n"
        "## 3. golden_001 - skill `rag` (uncertain)\n\nDECISION: ?\n\n"
        "## 4. golden_001 - skill `llms` (disagreement)\n\nPROPOSED: `drop` - second\n\nDECISION: ?\n")
    assert al.parse_proposals(queue) == {2: ("A", "first"), 4: ("drop", "second")}


@pytest.mark.parametrize("proposed, verdict, same", [
    ("B", "B", True), ("B", "`b`", True), ("B", " B ", True), ("B", "A", False),
    ("drop", "ok", False), ("B", {"requirement": "required"}, False),
    ('{"requirement": "required", "raw_text": "x"}', {"raw_text": "x", "requirement": "required"}, True),
    ('{"requirement": "required"}', {"requirement": "nice_to_have"}, False),
])
def test_verdict_matches(proposed, verdict, same):
    assert al.verdict_matches(proposed, verdict) is same


def test_write_decisions_fills_only_the_items_asked_for():
    queue = ("## 1. g - skill `a` (disagreement)\n\nDECISION: ?\n\n"
             "## 2. g - skill `b` (disagreement)\n\nDECISION: ?\n")
    out = al.write_decisions(queue, {2: "drop"})
    assert "## 1. g - skill `a` (disagreement)\n\nDECISION: ?" in out
    assert out.endswith("DECISION: drop\n")


def test_write_decisions_refuses_to_overwrite_a_decision_already_made():
    queue = "## 1. g - skill `a` (disagreement)\n\nDECISION: B\n"
    with pytest.raises(ValueError, match="already says 'B'"):
        al.write_decisions(queue, {1: "drop"})
    with pytest.raises(ValueError, match="not found in the queue"):
        al.write_decisions(queue, {9: "drop"})


def test_check_extra_model_refuses_the_extractor_and_either_labeler():
    with pytest.raises(SystemExit, match="the extractor's model"):
        al.check_extra_model("judge", "m-extractor", ["a", "b"], extractor="m-extractor")
    with pytest.raises(SystemExit, match="which labeled this run"):
        al.check_extra_model("judge", "b", ["a", "b"], extractor="m-extractor")
    al.check_extra_model("judge", "c", ["a", "b"], extractor="m-extractor")


def test_heading_above_finds_the_section_and_skips_bullets():
    posting = "Role\n\nCore Requirements\n\n- Strong Python\n- Docker in production\n"
    assert al.heading_above(posting, posting.index("Docker")) == "Core Requirements"


def test_wide_excerpt_carries_the_heading_and_marks_the_truncation():
    posting = "Role\n\nNice-to-haves\n\n- " + ("filler " * 200) + "Docker in production\n"
    out = al.wide_excerpt(posting, "Docker in production", width=60)
    assert "section heading above the quote: Nice-to-haves" in out
    assert out.startswith("section heading") and "..." in out
    assert "Docker in production" in out


def test_judge_question_shows_both_labelers_the_proposal_and_the_options():
    item = {"golden_id": "golden_001", "kind": "skill", "key": "docker", "reason": "disagreement",
            "a": {"skill_id": "docker", "requirement": "nice_to_have", "raw_text": "Docker"},
            "b": None, "problems": []}
    q = al.judge_question(item, POSTING, "A", "nice-to-have heading")
    assert "- A: `docker` · nice_to_have" in q and "- B: (did not label this)" in q
    assert "proposed decision: A" in q and "proposer's reason: nice-to-have heading" in q
    assert al.DECISIONS["disagreement"] in q
    # the judge rules on one item; it is never handed the other labels or the taxonomy
    assert "python" not in q.lower().split("posting-excerpt")[0]


def judge_run(tmp_path, monkeypatch, proposal="`B` - the heading says required"):
    """A one-posting run whose single disagreement carries a proposal, ready to judge."""
    goldens = tmp_path / "goldens"
    goldens.mkdir()
    runs = tmp_path / "labeling"
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        "CREATE TABLE job (id INTEGER PRIMARY KEY, company TEXT, title TEXT, city TEXT, seniority TEXT,"
        " description_text TEXT, first_seen TEXT, extracted_version TEXT);"
        "CREATE TABLE job_source (job_id INTEGER, source TEXT);")
    conn.execute("INSERT INTO job VALUES (1,'Acme','Senior AI Engineer','Berlin','senior',?,'2026-10-20',NULL)",
                 (POSTING,))
    conn.execute("INSERT INTO job_source VALUES (1, 'greenhouse')")
    conn.commit()
    conn.close()
    monkeypatch.setattr(al, "GOLDENS", goldens)
    monkeypatch.setattr(al, "RUNS", runs)
    monkeypatch.setattr(al.ng, "DB", db)
    monkeypatch.setattr(al.ng, "GOLDENS", goldens)
    b = ok_answer(expected=[
        *ok_answer()["expected"][:2],
        {"skill_id": "docker", "requirement": "required", "raw_text": "Docker"}])
    monkeypatch.setattr(al, "make_client", lambda provider: FakeAnthropic(
        [ok_answer() if provider == "anthropic" else b]))
    monkeypatch.setitem(al.PROVIDERS, "openai", al.call_anthropic)
    al.main(["label", "--count", "1", "--spot-check", "2", "--seed", "0",
             "--remote-eu", "0", "--german", "0"])
    run_dir, = list(runs.iterdir())
    queue = run_dir / "review_queue.md"
    text = queue.read_text()
    # the proposal a reviewer wrote by hand, on the one disagreement
    n = next(i for i, item in enumerate(json.loads((run_dir / "items.json").read_text()), 1)
             if item["reason"] == "disagreement")
    blocks = re.split(r"(?=^## \d+\.)", text, flags=re.M)
    for i, block in enumerate(blocks):
        if block.startswith(f"## {n}."):
            blocks[i] = block.replace("DECISION: ?", f"PROPOSED: {proposal}\n\nDECISION: ?")
    queue.write_text("".join(blocks))
    return run_dir, queue, n


def judge_client(monkeypatch, *answers):
    """A fake judge. Speaks the one API the FakeAnthropic double implements."""
    client = FakeAnthropic(list(answers))
    monkeypatch.setattr(al, "make_client", lambda provider: client)
    monkeypatch.setitem(al.PROVIDERS, "google", al.call_anthropic)
    return client


def test_judge_records_its_agreement_with_the_proposal_as_a_model_decision(tmp_path, monkeypatch, capsys):
    run_dir, queue, n = judge_run(tmp_path, monkeypatch)
    client = judge_client(monkeypatch, {"decision": "B", "why": "rule 3: the required mention wins"})
    al.main(["judge", "--run", run_dir.name, "--model", "judge-model"])

    assert f"## {n}." in queue.read_text()
    decisions = dict(al.parse_queue(queue.read_text()))
    assert decisions[n] == "B"
    # the spot-checks and the scope item are not the judge's business
    assert len(client.calls) == 1
    adj = json.loads((run_dir / "adjudication.json").read_text())
    assert adj["items"][str(n)]["by"] == "model"
    assert adj["items"][str(n)]["model"] == "judge-model"
    assert adj["items"][str(n)]["decision"] == "B"
    assert adj["judge"]["agreed"] == 1 and adj["judge"]["disagreed"] == 0
    assert "rules" in adj["judge"]
    assert "agreed with the proposal on 1/1" in capsys.readouterr().out


def test_judge_leaves_a_disagreement_undecided_and_prints_it(tmp_path, monkeypatch, capsys):
    run_dir, queue, n = judge_run(tmp_path, monkeypatch)
    judge_client(monkeypatch, {"decision": "A", "why": "rule 1: the bullet is nice-to-have"})
    al.main(["judge", "--run", run_dir.name, "--model", "judge-model"])

    assert dict(al.parse_queue(queue.read_text()))[n] == "?"
    assert not (run_dir / "adjudication.json").exists()
    out = capsys.readouterr().out
    assert "1 left at `?` for you" in out
    assert "proposed: B   judge: A" in out
    assert "rule 1" in out


def test_judge_refuses_a_verdict_the_item_does_not_allow(tmp_path, monkeypatch, capsys):
    run_dir, queue, n = judge_run(tmp_path, monkeypatch)
    judge_client(monkeypatch, {"decision": "maybe", "why": "unsure"})
    al.main(["judge", "--run", run_dir.name, "--model", "judge-model"])
    assert dict(al.parse_queue(queue.read_text()))[n] == "?"
    out = capsys.readouterr().out
    assert "could not be used" in out and "does not allow" in out


def test_judge_reuses_its_cached_ruling(tmp_path, monkeypatch):
    run_dir, queue, n = judge_run(tmp_path, monkeypatch)
    judge_client(monkeypatch, {"decision": "A", "why": "no"})
    al.main(["judge", "--run", run_dir.name, "--model", "judge-model"])
    assert (run_dir / "judge" / f"{n:03d}.json").exists()
    second = judge_client(monkeypatch)   # no answers left: a second call would raise
    al.main(["judge", "--run", run_dir.name, "--model", "judge-model"])
    assert second.calls == []


def test_judge_skips_an_item_on_a_posting_ruled_out_of_scope(tmp_path, monkeypatch, capsys):
    run_dir, queue, n = judge_run(tmp_path, monkeypatch)
    queue.write_text(queue.read_text().replace("DECISION: yes", "DECISION: no marketing role"))
    client = judge_client(monkeypatch)
    al.main(["judge", "--run", run_dir.name, "--model", "judge-model"])
    assert client.calls == []
    assert "0 undecided items with a proposal" in capsys.readouterr().out


def test_judge_dry_run_makes_no_calls(tmp_path, monkeypatch, capsys):
    run_dir, queue, n = judge_run(tmp_path, monkeypatch)
    client = judge_client(monkeypatch)
    al.main(["judge", "--run", run_dir.name, "--model", "judge-model", "--dry-run"])
    assert client.calls == [] and dict(al.parse_queue(queue.read_text()))[n] == "?"
    assert "1 undecided items with a proposal" in capsys.readouterr().out


def test_judge_refuses_a_model_that_labeled_the_run(tmp_path, monkeypatch):
    run_dir, queue, n = judge_run(tmp_path, monkeypatch)
    judge_client(monkeypatch)
    with pytest.raises(SystemExit, match="which labeled this run"):
        al.main(["judge", "--run", run_dir.name, "--model", al.DEFAULT_MODEL_B])


def test_item_range():
    assert al.item_range("30-33") == {30, 31, 32, 33}
    assert al.item_range("30,41") == {30, 41}
    assert al.item_range("5") == {5}
    with pytest.raises(Exception):
        al.item_range("30-")
