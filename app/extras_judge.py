"""Judge the extra skills an eval run produced: did the gold label miss it, or is the
model wrong?

An "extra" is a skill the extractor returned that the Golden does not list — a false
positive by the eval's arithmetic. Some of them are the extractor being wrong; others are
the label being incomplete, and those are worth finding, because every eval number is
measured against those labels. This asks a model which it is, one call per Golden covering
all of that Golden's extras, and writes the verdicts into the run's results for the human
spot-check (HIR-92) to work from.

Does NOT: change any score, change the Goldens, or decide anything. A verdict is a
pointer for a person to check, never an edit to a label — AGENTS.md puts any change to a
label's definition on the stop list. Off unless the eval is run with --extras-judge.

Invariants:
  - One model call per Golden with extras; a Golden with none is never sent.
  - A judge failure is recorded as a verdict of "error" for that Golden and never fails
    the eval run.
  - The judge sees the posting, the gold labels and the extras. It is not told which
    extractor version produced them, so it cannot favour one.
"""

from dataclasses import dataclass

DEFAULT_JUDGE_MODEL = "claude-sonnet-5-5"
MAX_TOKENS = 2048

VERDICTS = ("gold_missed_it", "model_wrong", "unclear")

PROMPT = """\
You are checking the labels of an evaluation set for a skill extractor.

A model read the job posting below and reported skills the posting asks candidates to
have. Some of the skills it reported are not in our reference labels. For each one, decide
which side is wrong:

- "gold_missed_it": the posting really does ask the candidate for this skill, with the
  quoted phrase as evidence. Our reference labels are incomplete.
- "model_wrong": the posting does not ask the candidate for this skill. The quote may be
  from the company description, from the responsibilities rather than the requirements, or
  may not support the skill at all.
- "unclear": the posting is genuinely ambiguous, or the quote is too thin to tell.

The rules our labels follow:
- Only skills the candidate is asked to have count: requirements, qualifications, "nice to
  have" lists, or a dedicated tech-stack section. A technology that appears only in the
  responsibilities or the company description does not count.
- A skill is a programming language, framework, library, tool, platform, technique or
  technical practice. Spoken languages, degrees, years of experience, domain knowledge and
  soft skills are not skills.
- A concrete technology given as an example ("e.g.", "such as", in parentheses) does count.

Give a one-sentence reason for each verdict, naming the part of the posting you relied on.
"""

TOOL = {
    "name": "record_verdicts",
    "description": "Record one verdict per extra skill.",
    "input_schema": {
        "type": "object",
        "properties": {
            "verdicts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "skill": {"type": "string",
                                  "description": "the extra skill, copied exactly as given"},
                        "verdict": {"type": "string", "enum": list(VERDICTS)},
                        "reason": {"type": "string", "description": "one sentence"},
                    },
                    "required": ["skill", "verdict", "reason"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["verdicts"],
        "additionalProperties": False,
    },
}


@dataclass(frozen=True)
class Verdict:
    skill_id: str
    verdict: str          # one of VERDICTS, or "error" when the call failed
    reason: str


def build_request(jd_text: str, gold_ids: list[str], extras: list[dict], model: str) -> dict:
    """extras: [{"skill_id": ..., "raw_text": ...}] — the quote is what the judge weighs."""
    listed = "\n".join(f"- {e['skill_id']}: quoted as \"{e.get('raw_text') or '(no quote)'}\""
                       for e in extras)
    return {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "system": [{"type": "text", "text": PROMPT, "cache_control": {"type": "ephemeral"}}],
        "tools": [TOOL],
        "tool_choice": {"type": "auto"},
        "messages": [{"role": "user", "content":
                      f"<job_posting>\n{jd_text}\n</job_posting>\n\n"
                      f"<reference_labels>\n{', '.join(gold_ids) or '(none)'}\n"
                      f"</reference_labels>\n\n"
                      f"<skills_to_judge>\n{listed}\n</skills_to_judge>\n\n"
                      f"Call record_verdicts with one verdict per skill to judge."}],
    }


def parse(response, extras: list[dict]) -> list[Verdict]:
    """Keep only verdicts that name an extra we asked about, with a verdict we know.

    A missing or malformed verdict becomes "unclear" rather than being dropped, so the
    count of verdicts always matches the count of extras and nothing goes missing quietly.
    """
    blocks = [b for b in response.content
              if getattr(b, "type", None) == "tool_use" and b.name == TOOL["name"]]
    got: dict[str, Verdict] = {}
    if len(blocks) == 1:
        for item in blocks[0].input.get("verdicts") or []:
            if not isinstance(item, dict):
                continue
            sid = str(item.get("skill", "")).strip()
            verdict = item.get("verdict")
            if sid and verdict in VERDICTS:
                got[sid] = Verdict(sid, verdict, str(item.get("reason", "")).strip())
    return [got.get(e["skill_id"], Verdict(e["skill_id"], "unclear", "no verdict returned"))
            for e in extras]


def judge_golden(jd_text: str, gold_ids: list[str], extras: list[dict], client,
                 model: str = DEFAULT_JUDGE_MODEL) -> list[Verdict]:
    """One call for one Golden's extras. Never raises: a failure comes back as "error"."""
    if not extras:
        return []
    try:
        response = client.messages.create(**build_request(jd_text, gold_ids, extras, model))
    except Exception as exc:  # noqa: BLE001 - a judge failure must not fail the eval run
        return [Verdict(x["skill_id"], "error", f"{type(exc).__name__}: {exc}") for x in extras]
    return parse(response, extras)


def tally(verdicts: list[Verdict]) -> dict[str, int]:
    """How the verdicts fell, for the run summary."""
    out = {v: 0 for v in (*VERDICTS, "error")}
    for v in verdicts:
        out[v.verdict] = out.get(v.verdict, 0) + 1
    return out
