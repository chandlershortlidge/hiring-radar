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
    for phrase in ("Agentic Coding Patterns", "Golden", "full-stack competence", "Elasticsearch, pgvector"):
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
    assert ex.TOOL["input_schema"]["properties"]["seniority"]["enum"] == ["junior", "mid", "senior", None]
