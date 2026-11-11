from pathlib import Path
from types import SimpleNamespace

import pytest

from app import extract as ex
from app.taxonomy import Taxonomy

ROOT = Path(__file__).resolve().parent.parent

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


def test_required_already_set_is_never_downgraded_by_a_later_nice_to_have(tax):
    # The reverse of test_duplicate_skill_keeps_one_and_required_wins: once required is
    # recorded for a skill, a later nice_to_have report of the same skill must not
    # overwrite it.
    m, _, _ = ex.parse_skills([item("kubernetes", "Kubernetes", "required"),
                               item("kubernetes", "Kubernetes", "nice_to_have")], tax, JD)
    assert m == [ex.Mention("kubernetes", "required", "Kubernetes")]


def test_duplicate_proposed_skill_keeps_the_required_one(tax):
    # The same "required wins" rule, on the proposed (unmapped) side rather than mentions.
    m, p, _ = ex.parse_skills([item("new:Rust", "Rust", "nice_to_have"),
                               item("new:Rust", "Rust", "required")], tax, JD)
    assert m == []
    assert p == [ex.Proposed("Rust", "required", "Rust")]


@pytest.mark.parametrize("bad_item,reason", [
    ("not a dict", "not an object"),
    (item("python", "Python", "mandatory"), "bad requirement"),
    (item("python", "text nobody wrote"), "raw_text not found in job text"),
    (item("cobol", "Python"), "unknown skill_id"),  # not new:-prefixed and not resolvable
    (item("new:Unmapped Thing", "LangChain"), None),  # accepted into proposed, not rejected
])
def test_a_bad_or_unresolved_skill_does_not_stop_the_rest_of_the_list(tax, bad_item, reason):
    # Each `continue` in parse_skills must never become a `break`: one malformed or
    # unmapped item must not silently drop every skill listed after it -- the "job stored
    # with too few skills" class of bug.
    m, _, r = ex.parse_skills([bad_item, item("langchain", "LangChain")], tax, JD)
    assert "langchain" in [x.skill_id for x in m]
    if reason is not None:
        assert r[0]["reason"] == reason


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
    assert item["required"] == ["skill_id", "requirement", "raw_text", "alternative_group"]


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


def test_extract_sends_the_actual_job_text_to_the_model(tax):
    # The request the fake client received must carry the real posting, not a stand-in --
    # a silent jd_text -> None on the way into build_request would still produce a
    # well-formed request and a well-formed (empty) response.
    client = FakeClient(response([item("python", "Python")]))
    ex.extract(JD, tax, client, model="m")
    assert JD in client.requests[0]["messages"][0]["content"]


def test_extract_carries_the_models_whole_tool_call_and_the_model_name(tax):
    """What HIR-170 logs: the tool call as it arrived, including the item validation threw away.

    'new:Rust' becomes a proposal and is not a mention, so raw_output is the only place the
    model's own wording survives — which is the point of keeping it."""
    items = [item("python", "Python"), item("new:Rust", "Rust", "nice_to_have")]
    out = ex.extract(JD, tax, FakeClient(response(items)), model="claude-test-1")
    assert out.model == "claude-test-1"
    assert out.raw_output == {"skills": items}
    assert len(out.raw_output["skills"]) == 2 and len(out.mentions) == 1


@pytest.mark.parametrize("resp", [response(stop="max_tokens"), response(stop="refusal"),
                                  response(n_blocks=0), response(n_blocks=2), response(name="other")])
def test_extract_raises_on_anything_but_one_tool_call(tax, resp):
    with pytest.raises(ex.ExtractionError):
        ex.extract(JD, tax, FakeClient(resp), model="m")


def test_extract_raises_on_cutoff_even_with_a_real_partial_tool_call(tax):
    # The parametrized cases above all carry an empty tool call, which would still raise
    # EmptyExtractionError if the stop_reason check were removed entirely -- masking
    # whether that check does anything on its own. A partial call that already carries a
    # real skill only fails because of the stop_reason check, so this is the one that
    # actually proves that this specific rule is doing the work.
    resp = response(items=[item("python", "Python")], stop="max_tokens")
    with pytest.raises(ex.ExtractionError, match="stop_reason"):
        ex.extract(JD, tax, FakeClient(resp), model="m")


def test_extract_raises_on_partial_refusal(tax):
    # The refusal case in the parameterized test has an empty skill list
    # which the empty answer rule rejects it anyway, 
    # so only this test depends on the refusal rule.
    resp = response(items=[item("python", "Python")], stop="refusal")
    with pytest.raises(ex.ExtractionError, match="stop_reason"):
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


def test_extract_raises_when_the_tool_call_carries_nothing(tax):
    # HIR-172: a well-formed but entirely empty call is a failed read, not a posting
    # without skills. Raising leaves the job unstamped and puts it in the failed= tally,
    # instead of storing a blank job that nothing downstream ever looks at again.
    with pytest.raises(ex.ExtractionError, match="carried nothing"):
        ex.extract(JD, tax, FakeClient(response([])), model="m")


def test_extract_keeps_zero_skills_when_an_attribute_was_found(tax):
    # The other half of HIR-172: zero skills is legitimate for a posting that still
    # states a seniority, so that stays a success and the job gets stamped.
    tool = SimpleNamespace(type="tool_use", name="record_skills", input={
        "skills": [], "seniority": "senior", "seniority_basis": "stated",
        "seniority_signal": "Senior AI Engineer"})
    out = ex.extract(SEN_JD, tax, FakeClient(
        SimpleNamespace(stop_reason="tool_use", content=[tool], usage=None)), model="m")
    assert out.mentions == [] and out.seniority.level == "senior"


@pytest.mark.parametrize("items,attr", [
    ([item("new:Rust", "Rust", "nice_to_have")], "proposed"),
    ([item("cobol", "Python")], "rejected"),
])
def test_extract_keeps_a_call_that_found_only_proposed_or_rejected_skills(tax, items, attr):
    # Those are reads that produced something, so they are not the empty shape.
    out = ex.extract(JD, tax, FakeClient(response(items)), model="m")
    assert getattr(out, attr) and out.mentions == []


def test_prompt_contains_no_golden_specific_text(tax):
    # Guard for the AGENTS.md rule: no JD wording copied into the prompt.
    # The production phrases below are dev-Golden wording we deliberately did not copy
    # when the rules they illustrate went into the prompt (DECISIONS 2026-10-29).
    for phrase in ("Agentic Coding Patterns", "Golden", "full-stack competence", "Elasticsearch, pgvector",
                   "structured operation", "production-quality agentic systems", "highly relevant",
                   "production-oriented LLM workflows", "production-grade applications",
                   # HIR-178: the appetite rule is illustrated in LABELING.md with the Goldens
                   # that motivated it, but the prompt states it generically. These are the
                   # dev/held-out JD phrases a first draft of rule 6 copied in by mistake.
                   "dive deep into", "scikit-learn) and", "agentic ecosystems",
                   "deepen this expertise", "love to hear from you"):
        assert phrase not in ex.PRINCIPLES


# --- the appetite rule (HIR-178) -------------------------------------------------

APPETITE_WORDS = ("eager to", "eagerness to", "interest in", "interested in", "keen to",
                  "curious about", "excited by", "hungry to", "willing to learn",
                  "Interesse an", "Lust auf")


def test_appetite_words_are_named_in_the_prompt_and_the_guide():
    """The rule has to be the same in both places, or the Goldens and the extractor are
    judged by two rules (HIR-178, DECISIONS 2026-11-05)."""
    # Both files wrap prose, so a phrase can straddle a newline: compare on one line.
    flat = lambda s: " ".join(s.split())
    guide = flat((ROOT / "evals" / "LABELING.md").read_text())
    prompt = flat(ex.PRINCIPLES)
    for word in APPETITE_WORDS:
        assert word in prompt, f"{word!r} missing from the extractor prompt"
        assert word in guide, f"{word!r} missing from the labeling guide"


def test_appetite_rule_states_the_nice_to_have_direction():
    # Guards against the rule surviving as prose that no longer says which label it gives.
    assert "Wanting a skill is not having it" in ex.PRINCIPLES
    block = ex.PRINCIPLES.split("Wanting a skill is not having it")[1]
    assert '"nice_to_have" whatever the heading says' in block
    assert "raw_text must include the appetite phrase" in block


def test_guide_lists_the_appetite_rule_in_the_precedence_list():
    guide = (ROOT / "evals" / "LABELING.md").read_text()
    section = guide.split("## requirement:")[1].split("\n## ")[0]
    assert "Four rules, in order of precedence" in section
    assert "3. **Wanting a skill is not having it.**" in section
    assert "4. **An unmarked item in a tech-stack list is `required`.**" in section


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


# --- alternative groups (HIR-251) ------------------------------------------------

GROUP_JD = """Requirements:
- Expertise in Python, Rust or Kubernetes, or a similar tool
- Experience with LangChain
Nice to have: React or ReAct"""


def grouped(sid, raw, group, req="required"):
    return {**item(sid, raw, req), "alternative_group": group}


def test_members_of_a_group_keep_its_number_and_a_lone_skill_has_none(tax):
    m, _, _ = ex.parse_skills([grouped("python", "Python", 1), grouped("kubernetes", "Kubernetes", 1),
                               grouped("langchain", "LangChain", None)], tax, GROUP_JD)
    assert {x.skill_id: x.alternative_group for x in m} == {"python": 1, "kubernetes": 1, "langchain": None}


def test_an_item_without_the_field_is_a_lone_skill(tax):
    """Readings stored before groups existed carry no field; they re-parse unchanged."""
    m, _, _ = ex.parse_skills([item("python", "Python")], tax, GROUP_JD)
    assert m == [ex.Mention("python", "required", "Python", None)]


def test_groups_are_renumbered_from_one_in_the_models_order(tax):
    m, _, _ = ex.parse_skills([grouped("python", "Python", 7), grouped("kubernetes", "Kubernetes", 7),
                               grouped("react", "React", 3, "nice_to_have"),
                               grouped("react-agent-pattern", "ReAct", 3, "nice_to_have")], tax, GROUP_JD)
    assert {x.skill_id: x.alternative_group for x in m} == {
        "react": 1, "react-agent-pattern": 1, "python": 2, "kubernetes": 2}


def test_a_group_left_with_one_member_loses_its_number(tax):
    """Rust is not in this taxonomy: it goes to the queue, and Python is an alternative to nothing."""
    m, p, _ = ex.parse_skills([grouped("python", "Python", 1), grouped("new:Rust", "Rust", 1)], tax, GROUP_JD)
    assert m == [ex.Mention("python", "required", "Python", None)]
    assert [x.label for x in p] == ["Rust"]


def test_a_rejected_partner_also_leaves_a_lone_member(tax):
    m, _, r = ex.parse_skills([grouped("python", "Python", 1), grouped("kubernetes", "not in the text", 1)],
                              tax, GROUP_JD)
    assert m == [ex.Mention("python", "required", "Python", None)] and len(r) == 1


@pytest.mark.parametrize("bad", [0, -1, True, "1", 1.5])
def test_a_malformed_group_number_counts_as_none(tax, bad):
    m, _, _ = ex.parse_skills([grouped("python", "Python", bad), grouped("kubernetes", "Kubernetes", bad)],
                              tax, GROUP_JD)
    assert {x.alternative_group for x in m} == {None}


def test_a_standalone_ask_beats_the_same_skill_as_an_option(tax):
    """Asked for on its own and again as one option: it is a requirement by itself."""
    m, _, _ = ex.parse_skills([grouped("python", "Python", 1), grouped("kubernetes", "Kubernetes", 1),
                               grouped("python", "Python", None)], tax, GROUP_JD)
    assert {x.skill_id: x.alternative_group for x in m} == {"python": None, "kubernetes": None}


def test_required_still_beats_nice_to_have_whatever_the_group(tax):
    m, _, _ = ex.parse_skills([grouped("python", "Python", None, "nice_to_have"),
                               grouped("python", "Python", 1), grouped("kubernetes", "Kubernetes", 1)],
                              tax, GROUP_JD)
    assert {x.skill_id: (x.requirement, x.alternative_group) for x in m} == {
        "python": ("required", 1), "kubernetes": ("required", 1)}


def test_the_group_field_is_nullable_without_a_type_list():
    """Strict tool schemas reject a type list combined with other keywords; anyOf is the safe shape."""
    field = ex.TOOL["input_schema"]["properties"]["skills"]["items"]["properties"]["alternative_group"]
    assert field["anyOf"] == [{"type": "integer"}, {"type": "null"}]


def test_prompt_states_that_or_similar_adds_no_skill(tax):
    assert '"or similar"' in ex.PRINCIPLES and "add no skill" in ex.PRINCIPLES


def test_prompt_says_grouping_never_drops_the_broad_skill(tax):
    """HIR-251 eval: "a broad skill ... null" read as "omit it" and cost 0.024 recall
    (cloud beside its provider examples). The rule must say the broad skill is still reported."""
    assert "Grouping never removes a skill" in ex.PRINCIPLES
    assert "is still\n   reported, with alternative_group null" in ex.PRINCIPLES
