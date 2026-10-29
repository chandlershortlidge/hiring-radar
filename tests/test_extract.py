from types import SimpleNamespace

import pytest

from app import extract as ex
from app.taxonomy import Taxonomy

JD = """Requirements:
- 3+ years with Python and Large Language Models
- Experience with LangChain
Nice to have: Kubernetes, Rust
We use Snowflake internally."""


@pytest.fixture
def tax():
    return Taxonomy({"version": 7, "skills": [
        {"id": "python", "display": "Python"},
        {"id": "llms", "display": "LLMs", "aliases": ["large language models"]},
        {"id": "langchain", "display": "LangChain"},
        {"id": "kubernetes", "display": "Kubernetes"},
        {"id": "react", "display": "React"},
        {"id": "react-agent-pattern", "display": "ReAct"},
    ]})


def item(sid, raw, req="required"):
    return {"skill_id": sid, "requirement": req, "raw_text": raw}


# --- parse_skills -------------------------------------------------------------

def test_known_ids_pass_through_sorted(tax):
    m, p, r = ex.parse_skills([item("python", "Python"), item("langchain", "LangChain")], tax, JD)
    assert [x.skill_id for x in m] == ["langchain", "python"]
    assert p == [] and r == []


def test_display_name_or_alias_is_resolved_to_id(tax):
    m, _, _ = ex.parse_skills([item("LLMs", "Large Language Models")], tax, JD)
    assert m[0].skill_id == "llms"


def test_new_label_goes_to_proposed_not_mentions(tax):
    m, p, _ = ex.parse_skills([item("new:Rust", "Rust", "nice_to_have")], tax, JD)
    assert m == []
    assert p == [ex.Proposed("Rust", "nice_to_have", "Rust")]


def test_new_label_that_already_exists_becomes_a_mention(tax):
    m, p, _ = ex.parse_skills([item("new:Large Language Models", "Large Language Models")], tax, JD)
    assert [x.skill_id for x in m] == ["llms"] and p == []


def test_unknown_id_is_rejected(tax):
    m, _, r = ex.parse_skills([item("cobol", "Python")], tax, JD)
    assert m == [] and r[0]["reason"] == "unknown skill_id"


def test_raw_text_must_appear_in_jd(tax):
    m, _, r = ex.parse_skills([item("python", "Python 3.12 expertise")], tax, JD)
    assert m == [] and r[0]["reason"] == "raw_text not found in job text"


def test_raw_text_match_ignores_whitespace_and_case(tax):
    m, _, _ = ex.parse_skills([item("python", "3+   YEARS with python")], tax, JD)
    assert len(m) == 1


def test_bad_requirement_is_rejected(tax):
    _, _, r = ex.parse_skills([item("python", "Python", "mandatory")], tax, JD)
    assert r[0]["reason"] == "bad requirement"


def test_duplicate_skill_keeps_one_and_required_wins(tax):
    m, _, _ = ex.parse_skills([item("kubernetes", "Kubernetes", "nice_to_have"),
                               item("kubernetes", "Kubernetes", "required")], tax, JD)
    assert m == [ex.Mention("kubernetes", "required", "Kubernetes")]


def test_react_case_is_respected(tax):
    jd = "Know ReAct prompting and React."
    m, _, _ = ex.parse_skills([item("ReAct", "ReAct"), item("React", "React")], tax, jd)
    assert {x.skill_id for x in m} == {"react-agent-pattern", "react"}


def test_non_object_items_are_rejected(tax):
    _, _, r = ex.parse_skills(["python"], tax, JD)
    assert r[0]["reason"] == "not an object"


# --- request + version -----------------------------------------------------------

def test_request_uses_auto_tool_choice_and_caches_system_prompt(tax):
    # Forced tool_choice ("tool"/"any") is rejected by current models, so the call asks
    # for the tool in the prompt and relies on `strict` for valid arguments instead.
    req = ex.build_request(tax, JD, "m")
    assert req["tool_choice"] == {"type": "auto"}
    assert req["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert "llms: LLMs [large language models]" in req["system"][0]["text"]
    assert JD in req["messages"][0]["content"]


def test_tool_is_strict_with_closed_schemas(tax):
    # `strict` requires additionalProperties: false plus `required` on every object.
    assert ex.TOOL["strict"] is True
    schema = ex.TOOL["input_schema"]
    assert schema["additionalProperties"] is False
    item = schema["properties"]["skills"]["items"]
    assert item["additionalProperties"] is False
    assert item["required"] == ["skill_id", "requirement", "raw_text"]


def test_prompt_asks_for_the_tool_call(tax):
    # With tool_choice "auto" the model chooses, so the instruction has to be explicit.
    assert "record_skills" in ex.system_prompt(tax)


def test_extractor_version_changes_with_taxonomy_and_model(tax):
    v1 = ex.extractor_version(tax, "m1")
    assert v1 == ex.extractor_version(tax, "m1")
    assert v1 != ex.extractor_version(tax, "m2")
    bigger = Taxonomy({"version": 8, "skills": [{"id": "python", "display": "Python"}]})
    assert v1 != ex.extractor_version(bigger, "m1")


# --- extract() with a fake client -------------------------------------------------

class FakeClient:
    def __init__(self, response):
        self.response = response
        self.requests = []
        self.messages = self

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return self.response


def response(items=None, stop="tool_use", name="record_skills", n_blocks=1):
    blocks = [SimpleNamespace(type="tool_use", name=name, input={"skills": items or []}) for _ in range(n_blocks)]
    usage = SimpleNamespace(input_tokens=100, output_tokens=20, cache_read_input_tokens=80, cache_creation_input_tokens=0)
    return SimpleNamespace(stop_reason=stop, content=blocks, usage=usage)


def test_extract_end_to_end_with_fake_client(tax):
    client = FakeClient(response([item("python", "Python"), item("new:Rust", "Rust", "nice_to_have")]))
    out = ex.extract(JD, tax, client, model="m")
    assert [m.skill_id for m in out.mentions] == ["python"]
    assert [p.label for p in out.proposed] == ["Rust"]
    assert out.taxonomy_version == 7
    assert out.extractor_version == ex.extractor_version(tax, "m")
    assert out.usage["cache_read_input_tokens"] == 80
    assert len(client.requests) == 1  # no retries


@pytest.mark.parametrize("resp", [response(stop="max_tokens"), response(stop="refusal"),
                                  response(n_blocks=0), response(n_blocks=2), response(name="other")])
def test_extract_raises_on_anything_but_one_tool_call(tax, resp):
    with pytest.raises(ex.ExtractionError):
        ex.extract(JD, tax, FakeClient(resp), model="m")


def test_extract_raises_when_the_model_answers_with_text_instead_of_calling_the_tool(tax):
    # The failure path "auto" introduces that forced tool_choice could not produce.
    text_only = SimpleNamespace(
        stop_reason="end_turn",
        content=[SimpleNamespace(type="text", text="Here are the skills: Python, LLMs.")],
        usage=None,
    )
    with pytest.raises(ex.ExtractionError):
        ex.extract(JD, tax, FakeClient(text_only), model="m")


def test_prompt_contains_no_golden_specific_text(tax):
    # Guard for the AGENTS.md rule: no JD wording copied into the prompt.
    # The production phrases below are dev-Golden wording we deliberately did not copy
    # when the rules they illustrate went into the prompt (DECISIONS 2026-10-29).
    for phrase in ("Agentic Coding Patterns", "Golden", "full-stack competence", "Elasticsearch, pgvector",
                   "structured operation", "production-quality agentic systems", "highly relevant",
                   "production-oriented LLM workflows", "production-grade applications"):
        assert phrase not in ex.PRINCIPLES


# --- seniority -------------------------------------------------------------------

SEN_JD = "Senior AI Engineer (m/w/d). Requirements: 5+ years building production ML systems. Python."


def test_seniority_stated_with_quoted_signal():
    s = ex.parse_seniority({"seniority": "senior", "seniority_basis": "stated", "seniority_signal": "Senior AI Engineer"}, SEN_JD)
    assert s == ex.Seniority("senior", "stated", "Senior AI Engineer")


def test_seniority_inferred_keeps_level_even_if_signal_is_not_verbatim():
    s = ex.parse_seniority({"seniority": "senior", "seniority_basis": "inferred", "seniority_signal": "five years experience"}, SEN_JD)
    assert s == ex.Seniority("senior", "inferred", None)


def test_seniority_stated_without_signal_is_dropped():
    s = ex.parse_seniority({"seniority": "senior", "seniority_basis": "stated", "seniority_signal": None}, SEN_JD)
    assert s == ex.NO_SENIORITY


@pytest.mark.parametrize("data", [
    {"seniority": None, "seniority_basis": None, "seniority_signal": None},
    {"seniority": "lead", "seniority_basis": "stated", "seniority_signal": "Senior AI Engineer"},
    {"seniority": "mid", "seniority_basis": None, "seniority_signal": None},
    {},
])
def test_seniority_invalid_or_absent_is_no_seniority(data):
    assert ex.parse_seniority(data, SEN_JD) == ex.NO_SENIORITY


def test_extract_carries_seniority(tax):
    tool = SimpleNamespace(type="tool_use", name="record_skills", input={
        "skills": [item("python", "Python")], "seniority": "senior", "seniority_basis": "stated",
        "seniority_signal": "Senior AI Engineer"})
    resp = SimpleNamespace(stop_reason="tool_use", content=[tool], usage=None)
    out = ex.extract(SEN_JD, tax, FakeClient(resp), model="m")
    assert out.seniority.level == "senior" and [m.skill_id for m in out.mentions] == ["python"]


def test_tool_schema_requires_seniority_fields():
    assert {"seniority", "seniority_basis", "seniority_signal"} <= set(ex.TOOL["input_schema"]["required"])
    levels = ex.TOOL["input_schema"]["properties"]["seniority"]["anyOf"]
    assert levels == [{"type": "string", "enum": ["junior", "mid", "senior"]}, {"type": "null"}]


def _schema_nodes(node):
    """Every dict in the schema tree, so a shape rule can be asserted over all of them."""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _schema_nodes(v)
    elif isinstance(node, list):
        for v in node:
            yield from _schema_nodes(v)


def test_no_enum_sits_on_a_union_type():
    """The API 400s on an enum whose values do not all match a union `type`.

    A nullable enum has to be expressed as anyOf, so no node may carry both an `enum`
    and a list-valued `type`.
    """
    for node in _schema_nodes(ex.TOOL["input_schema"]):
        if "enum" in node:
            assert not isinstance(node.get("type"), list), node


# --- German and degree -------------------------------------------------------------

ATTR_JD = ("Requirements: M.Sc. in Computer Science or a related field, or equivalent practical experience. "
           "Fluent English; German is a plus. Python.")


def test_german_stated_with_quote():
    g = ex.parse_german({"german": "nice_to_have", "german_basis": "stated", "german_signal": "German is a plus"}, ATTR_JD)
    assert g == ex.German("nice_to_have", "stated", "German is a plus")


def test_german_stated_without_a_found_quote_is_not_mentioned():
    assert ex.parse_german({"german": "required", "german_basis": "stated", "german_signal": "fluent German"}, ATTR_JD) == ex.NO_GERMAN
    assert ex.parse_german({"german": "required", "german_basis": "stated", "german_signal": None}, ATTR_JD) == ex.NO_GERMAN


def test_german_inferred_carries_no_signal():
    g = ex.parse_german({"german": "required", "german_basis": "inferred", "german_signal": "Deutschkenntnisse"}, "Wir suchen...")
    assert g == ex.German("required", "inferred", None)


@pytest.mark.parametrize("data", [{}, {"german": None, "german_basis": None, "german_signal": None},
                                  {"german": "mandatory", "german_basis": "stated", "german_signal": "German is a plus"},
                                  {"german": "required", "german_basis": None, "german_signal": "German is a plus"}])
def test_german_invalid_or_absent(data):
    assert ex.parse_german(data, ATTR_JD) == ex.NO_GERMAN


def test_degree_with_or_equivalent():
    d = ex.parse_degree({"degree": "master", "degree_requirement": "required", "degree_or_equivalent": True,
                         "degree_signal": "M.Sc. in Computer Science or a related field, or equivalent practical experience"}, ATTR_JD)
    assert d == ex.Degree("master", "required", True, "M.Sc. in Computer Science or a related field, or equivalent practical experience")


def test_degree_needs_a_quoted_signal():
    assert ex.parse_degree({"degree": "master", "degree_requirement": "required", "degree_or_equivalent": False, "degree_signal": None}, ATTR_JD) == ex.NO_DEGREE
    assert ex.parse_degree({"degree": "master", "degree_requirement": "required", "degree_or_equivalent": False, "degree_signal": "PhD"}, ATTR_JD) == ex.NO_DEGREE


@pytest.mark.parametrize("data", [{}, {"degree": None, "degree_requirement": None, "degree_or_equivalent": True, "degree_signal": "M.Sc."},
                                  {"degree": "diploma", "degree_requirement": "required", "degree_or_equivalent": False, "degree_signal": "M.Sc."},
                                  {"degree": "master", "degree_requirement": None, "degree_or_equivalent": False, "degree_signal": "M.Sc."}])
def test_degree_invalid_or_absent(data):
    assert ex.parse_degree(data, ATTR_JD) == ex.NO_DEGREE


def test_extract_carries_german_and_degree(tax):
    tool = SimpleNamespace(type="tool_use", name="record_skills", input={
        "skills": [item("python", "Python")], "seniority": None, "seniority_basis": None, "seniority_signal": None,
        "german": "nice_to_have", "german_basis": "stated", "german_signal": "German is a plus",
        "degree": "master", "degree_requirement": "required", "degree_or_equivalent": True, "degree_signal": "M.Sc. in Computer Science"})
    out = ex.extract(ATTR_JD, tax, FakeClient(SimpleNamespace(stop_reason="tool_use", content=[tool], usage=None)), model="m")
    assert out.german.requirement == "nice_to_have" and out.degree == ex.Degree("master", "required", True, "M.Sc. in Computer Science")


def test_tool_schema_requires_german_and_degree_fields():
    req = set(ex.TOOL["input_schema"]["required"])
    assert {"german", "german_basis", "german_signal", "degree", "degree_requirement", "degree_or_equivalent", "degree_signal"} <= req
    assert ex.TOOL["input_schema"]["properties"]["degree_or_equivalent"] == {"type": "boolean"}


# A requirement sentence and a responsibility sentence, so the fixture can show that only
# the first grounds a value. The quality-expectation phrasing is here for the same reason.
PROD_JD = ("You have shipped production systems and owned them end-to-end. "
           "You will deploy models to production and write production-grade code. "
           "Experience with production ML is a plus.")


def test_production_required_with_quote():
    pr = ex.parse_production({"production": "required", "production_basis": "stated",
                              "production_signal": "You have shipped production systems"}, PROD_JD)
    assert pr == ex.Production("required", "stated", "You have shipped production systems")


def test_production_nice_to_have_with_quote():
    pr = ex.parse_production({"production": "nice_to_have", "production_basis": "stated",
                              "production_signal": "Experience with production ML is a plus"}, PROD_JD)
    assert pr == ex.Production("nice_to_have", "stated", "Experience with production ML is a plus")


def test_production_without_a_found_quote_is_not_mentioned():
    assert ex.parse_production({"production": "required", "production_basis": "stated",
                                "production_signal": "five years in production"}, PROD_JD) == ex.NO_PRODUCTION
    assert ex.parse_production({"production": "required", "production_basis": "stated",
                                "production_signal": None}, PROD_JD) == ex.NO_PRODUCTION


def test_production_has_no_inferred_basis():
    """Unlike German, nothing about the posting's form implies the demand: 'inferred' is invalid."""
    assert ex.parse_production({"production": "required", "production_basis": "inferred",
                                "production_signal": None}, PROD_JD) == ex.NO_PRODUCTION


@pytest.mark.parametrize("data", [
    {},
    {"production": None, "production_basis": None, "production_signal": None},
    {"production": "mandatory", "production_basis": "stated", "production_signal": "You have shipped production systems"},
    {"production": "required", "production_basis": None, "production_signal": "You have shipped production systems"},
])
def test_production_invalid_or_absent(data):
    assert ex.parse_production(data, PROD_JD) == ex.NO_PRODUCTION


def test_extract_carries_production(tax):
    tool = SimpleNamespace(type="tool_use", name="record_skills", input={
        "skills": [item("python", "Python")], "seniority": None, "seniority_basis": None, "seniority_signal": None,
        "german": None, "german_basis": None, "german_signal": None,
        "degree": None, "degree_requirement": None, "degree_or_equivalent": False, "degree_signal": None,
        "production": "required", "production_basis": "stated",
        "production_signal": "You have shipped production systems"})
    out = ex.extract(PROD_JD, tax, FakeClient(SimpleNamespace(stop_reason="tool_use", content=[tool], usage=None)), model="m")
    assert out.production == ex.Production("required", "stated", "You have shipped production systems")


def test_extraction_defaults_to_no_production(tax):
    """A tool call with no production keys at all must not invent a value."""
    tool = SimpleNamespace(type="tool_use", name="record_skills", input={
        "skills": [item("python", "Python")], "seniority": None, "seniority_basis": None, "seniority_signal": None,
        "german": None, "german_basis": None, "german_signal": None,
        "degree": None, "degree_requirement": None, "degree_or_equivalent": False, "degree_signal": None})
    out = ex.extract(PROD_JD, tax, FakeClient(SimpleNamespace(stop_reason="tool_use", content=[tool], usage=None)), model="m")
    assert out.production == ex.NO_PRODUCTION


def test_tool_schema_requires_production_fields():
    req = set(ex.TOOL["input_schema"]["required"])
    assert {"production", "production_basis", "production_signal"} <= req
    # A nullable enum must be anyOf, and 'stated' is the only basis there is.
    assert ex.TOOL["input_schema"]["properties"]["production_basis"] == {
        "anyOf": [{"type": "string", "enum": ["stated"]}, {"type": "null"}]}


def test_prompt_describes_production_markers_and_excludes_responsibilities():
    """Per DECISIONS: describe the positive class, and keep responsibilities out of it."""
    block = ex.PRINCIPLES.split("demands production work of the candidate")[1]
    assert 'Markers for "required"' in block
    assert "are responsibilities, null" in block
    assert "write production-grade code" in block


def test_prompt_makes_the_verb_not_the_tense_the_production_test():
    """DECISIONS 2026-10-29: a present ability is the same demand as a past record."""
    block = ex.PRINCIPLES.split("demands production work of the candidate")[1]
    assert "The verb carries the demand, not the tense" in block
    assert "a present ability" in block
    # the quality-bar class is still excluded, and the verb is what separates them
    assert "Test the verb" in block


def test_prompt_excludes_a_demand_scoped_to_one_seniority_level():
    """DECISIONS 2026-10-29: golden_006 - a level-scoped demand is not job-wide."""
    block = ex.PRINCIPLES.split("demands production work of the candidate")[1]
    assert "scoped to one seniority level" in block
    assert "not a job-wide demand" in block


def test_prompt_counts_building_alone_as_a_production_demand():
    """DECISIONS 2026-10-29: build is a demand verb, and a hyphenated object is still
    production (golden_004, golden_012 were missed when the list stopped at ship/run)."""
    block = ex.PRINCIPLES.split("demands production work of the candidate")[1]
    assert "build / ship / operate / deploy / run" in block
    assert "Building alone is enough" in block
    assert "does not weaken" in block


def test_prompt_treats_knowing_about_production_as_a_knowledge_bar():
    """DECISIONS 2026-10-29: golden_006's unscoped MLOps-knowledge bullet is not a demand."""
    block = ex.PRINCIPLES.split("demands production work of the candidate")[1]
    assert "knowledge bar, not a demand to have done it" in block


def test_prompt_allows_soft_optional_phrasing_for_nice_to_have():
    """DECISIONS 2026-10-29: the category, not golden_011's wording."""
    block = ex.PRINCIPLES.split("demands production work of the candidate")[1]
    assert "soft phrasing" in block
    assert "relevant, welcome, helpful" in block


def test_prompt_keeps_degrees_and_languages_out_of_skills():
    # Rule 2 still excludes them from skills; the attribute blocks are additive.
    assert "degrees, years of experience" in ex.PRINCIPLES and "Also report the degree" in ex.PRINCIPLES


def test_extraction_input_puts_the_title_on_top():
    assert ex.extraction_input("Senior AI Engineer", "We build agents.") == "Senior AI Engineer\n\nWe build agents."


def test_extraction_input_leaves_text_that_already_opens_with_the_title():
    text = "AI Engineering - Workingstudent\ncognee · Berlin\n\nWe're looking for builders."
    assert ex.extraction_input("AI Engineering - Workingstudent", text) == text


def test_extraction_input_without_a_title_is_the_text():
    assert ex.extraction_input(None, "Python") == "Python"
    assert ex.extraction_input("  ", "Python") == "Python"
