"""Mocked: no model call leaves the process. The schema itself was checked with one live
call before any batch ran (CLAUDE.md: mocked tests do not prove a provider accepts a
request) — see the PR's "Testing" section."""

import json
from types import SimpleNamespace

from app import extras_judge as ej

JD = "Requirements: Python, SQL. We run our platform on Kubernetes."
GOLD = ["python", "sql"]
EXTRAS = [{"skill_id": "kubernetes", "raw_text": "Kubernetes"},
          {"skill_id": "dbt", "raw_text": "dbt"}]


def reply(verdicts):
    tool = SimpleNamespace(type="tool_use", name="record_verdicts", input={"verdicts": verdicts})
    return SimpleNamespace(stop_reason="tool_use", content=[tool])


def client_returning(verdicts, seen=None):
    def create(**kw):
        if seen is not None:
            seen.append(kw)
        return reply(verdicts)
    return SimpleNamespace(messages=SimpleNamespace(create=create))


def test_a_golden_with_no_extras_is_never_sent():
    def boom(**kw):
        raise AssertionError("no call should be made")

    assert ej.judge_golden(JD, GOLD, [], SimpleNamespace(messages=SimpleNamespace(create=boom))) == []


def test_verdicts_come_back_in_the_order_asked():
    client = client_returning([
        {"skill": "dbt", "verdict": "model_wrong", "reason": "not in the posting"},
        {"skill": "kubernetes", "verdict": "gold_missed_it", "reason": "named in requirements"}])
    out = ej.judge_golden(JD, GOLD, EXTRAS, client)
    assert [v.skill_id for v in out] == ["kubernetes", "dbt"]
    assert out[0].verdict == "gold_missed_it"
    assert out[1].verdict == "model_wrong"


def test_a_missing_verdict_becomes_unclear_rather_than_vanishing():
    out = ej.judge_golden(JD, GOLD, EXTRAS, client_returning(
        [{"skill": "kubernetes", "verdict": "gold_missed_it", "reason": "r"}]))
    assert [(v.skill_id, v.verdict) for v in out] == [
        ("kubernetes", "gold_missed_it"), ("dbt", "unclear")]
    assert out[1].reason == "no verdict returned"


def test_an_unknown_verdict_string_is_not_trusted():
    out = ej.judge_golden(JD, GOLD, [EXTRAS[0]], client_returning(
        [{"skill": "kubernetes", "verdict": "probably_fine", "reason": "r"}]))
    assert out[0].verdict == "unclear"


def test_a_judge_failure_is_recorded_and_never_raises():
    def boom(**kw):
        raise RuntimeError("529 overloaded")

    out = ej.judge_golden(JD, GOLD, EXTRAS, SimpleNamespace(messages=SimpleNamespace(create=boom)))
    assert [v.verdict for v in out] == ["error", "error"]
    assert "529 overloaded" in out[0].reason


def test_a_reply_without_the_tool_call_is_all_unclear():
    text = SimpleNamespace(type="text", text="I think they are all fine")
    resp = SimpleNamespace(stop_reason="end_turn", content=[text])
    out = ej.parse(resp, EXTRAS)
    assert [v.verdict for v in out] == ["unclear", "unclear"]


def test_the_request_shows_the_posting_the_labels_and_the_quotes():
    seen = []
    ej.judge_golden(JD, GOLD, EXTRAS, client_returning([], seen), model="m")
    [kw] = seen
    content = kw["messages"][0]["content"]
    assert JD in content
    assert "python, sql" in content
    assert 'kubernetes: quoted as "Kubernetes"' in content
    assert kw["model"] == "m"
    assert kw["tools"][0]["name"] == "record_verdicts"


def test_an_extra_with_no_quote_still_goes_to_the_judge():
    seen = []
    ej.judge_golden(JD, GOLD, [{"skill_id": "dbt", "raw_text": None}], client_returning([], seen))
    assert "(no quote)" in seen[0]["messages"][0]["content"]


def test_tally_counts_every_verdict_kind():
    out = ej.tally([ej.Verdict("a", "gold_missed_it", ""), ej.Verdict("b", "gold_missed_it", ""),
                    ej.Verdict("c", "model_wrong", ""), ej.Verdict("d", "error", "")])
    assert out == {"gold_missed_it": 2, "model_wrong": 1, "unclear": 0, "error": 1}


def test_the_tool_schema_keeps_enums_off_nullable_fields():
    # CLAUDE.md: the API rejects a type list combined with enum. Every enum here sits on a
    # single-typed, required field.
    props = ej.TOOL["input_schema"]["properties"]["verdicts"]["items"]["properties"]
    assert props["verdict"] == {"type": "string", "enum": list(ej.VERDICTS)}
    assert json.dumps(ej.TOOL)  # serialisable as sent
