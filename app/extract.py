"""Stage 2: job-description text → skill mentions, as taxonomy ids.

Does: build the prompt (general principles + the taxonomy as a lookup list), call the
model once asking for a single tool call, and turn the tool output into validated mentions.
Labels the taxonomy doesn't know become `proposed` items, never mentions.

Does NOT: read images (that's stage 1), retry failed calls, write to the database,
add or change taxonomy entries, or contain rules about specific job descriptions.
Policy belongs in taxonomy/skills.json; the prompt stays general (AGENTS.md).

Invariants:
  - Seniority is one of junior/mid/senior with a basis, or absent; never a guess without a
    basis, and a "stated" level always carries its quoted signal.
  - Every returned mention has a skill_id that exists in the taxonomy it was run with.
  - Each skill_id appears at most once per job; if any mention is required, it is required.
  - Every mention's raw_text is found in the job text (whitespace/case-insensitive);
    unsupported items are reported in `rejected`, not silently kept.
  - A call that does not produce exactly one record_skills tool call raises
    ExtractionError. tool_choice is "auto" (forced tool use is rejected by current
    models), so the prompt asks for the call and `strict` keeps its arguments valid.
"""

import hashlib
import os
import re
from dataclasses import dataclass, field

from app.taxonomy import Taxonomy

DEFAULT_MODEL = os.environ.get("HIRING_RADAR_MODEL", "claude-sonnet-5-5")
MAX_TOKENS = 4096
NEW_PREFIX = "new:"

PRINCIPLES = """\
You extract the technical skills a job description asks candidates to have.

1. Only extract skills the candidate is asked to have: from requirements, qualifications,
   "nice to have" lists, or a dedicated tech-stack section. Ignore technologies that appear
   only in responsibilities or the company description unless the candidate is also asked
   for them.
2. A skill is a programming language, framework, library, tool, platform, technique, or
   technical practice. Spoken languages, degrees, years of experience, industry or domain
   knowledge, and soft skills are not skills.
3. Map each skill to an id from the taxonomy below. Use the id the text actually supports.
   If the text names both a broad skill and specific ones, include each. Do not add a broad
   skill the text does not ask for.
4. Concrete technologies given as examples ("e.g.", "such as", in parentheses) count as
   skills in their own right.
5. If no taxonomy entry fits, use "new:<Label>" with a short, conventional name for the skill.
6. requirement is "nice_to_have" only when the wording marks it optional (preferred, plus,
   bonus, nice to have, ideally, is an advantage). Otherwise "required". A section heading
   that marks its section optional sets the default for every item under it, until the next
   heading; a marker on the item itself overrides that default either way. An unmarked entry
   in a tech-stack list is "required".
7. raw_text is the exact phrase from the job description that supports the skill, copied
   verbatim.
8. Report each skill id at most once. Report every skill you find.

Also report the seniority the posting targets:
- "junior", "mid", or "senior". Intern, working student, graduate, entry-level, and "(Junior)"
  are junior. Lead, principal, staff, head, and architect are senior.
- seniority_basis is "stated" when the title or text names the level outright; "inferred"
  when you read it from years of experience, ownership or mentoring language, or the
  qualifications asked for. If the posting gives no usable signal, set seniority to null
  and basis to null.
- seniority_signal is the verbatim phrase you based it on, or null.

Always respond by calling the record_skills tool exactly once. Do not reply with text."""

SENIORITY_LEVELS = ("junior", "mid", "senior")

TOOL = {
    "name": "record_skills",
    "description": "Record the technical skills the job description asks candidates to have.",
    "strict": True,  # arguments validate against the schema; replaces forced tool_choice
    "input_schema": {
        "type": "object",
        "properties": {
            "skills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "skill_id": {"type": "string", "description": "A taxonomy id, or new:<Label>."},
                        "requirement": {"type": "string", "enum": ["required", "nice_to_have"]},
                        "raw_text": {"type": "string"},
                    },
                    "required": ["skill_id", "requirement", "raw_text"],
                    "additionalProperties": False,
                },
            },
            "seniority": {"type": ["string", "null"], "enum": ["junior", "mid", "senior", None]},
            "seniority_basis": {"type": ["string", "null"], "enum": ["stated", "inferred", None]},
            "seniority_signal": {"type": ["string", "null"]},
        },
        "required": ["skills", "seniority", "seniority_basis", "seniority_signal"],
        "additionalProperties": False,
    },
}


class ExtractionError(RuntimeError):
    pass


@dataclass(frozen=True)
class Mention:
    skill_id: str
    requirement: str
    raw_text: str


@dataclass(frozen=True)
class Proposed:
    label: str
    requirement: str
    raw_text: str


@dataclass(frozen=True)
class Seniority:
    level: str | None      # junior | mid | senior | None
    basis: str | None      # stated | inferred | None
    signal: str | None     # verbatim phrase, or None


NO_SENIORITY = Seniority(None, None, None)


@dataclass
class Extraction:
    seniority: Seniority = NO_SENIORITY
    mentions: list[Mention] = field(default_factory=list)
    proposed: list[Proposed] = field(default_factory=list)
    rejected: list[dict] = field(default_factory=list)
    extractor_version: str = ""
    taxonomy_version: int = 0
    usage: dict = field(default_factory=dict)


# --- pure parts -------------------------------------------------------------------

def taxonomy_block(tax: Taxonomy) -> str:
    lines = [f"TAXONOMY (version {tax.version}) — id: Display [aliases]"]
    for s in sorted(tax.skills.values(), key=lambda s: s.id):
        alias = f" [{', '.join(s.aliases)}]" if s.aliases else ""
        lines.append(f"{s.id}: {s.display}{alias}")
    return "\n".join(lines)


def system_prompt(tax: Taxonomy) -> str:
    return PRINCIPLES + "\n\n" + taxonomy_block(tax)


def extractor_version(tax: Taxonomy, model: str) -> str:
    """Changes whenever the prompt, tool schema, taxonomy, or model changes."""
    h = hashlib.sha256((system_prompt(tax) + repr(TOOL) + model).encode()).hexdigest()
    return f"x2-{h[:10]}"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def parse_skills(items: list, tax: Taxonomy, jd_text: str) -> tuple[list[Mention], list[Proposed], list[dict]]:
    jd = _norm(jd_text)
    by_id: dict[str, Mention] = {}
    proposed: dict[str, Proposed] = {}
    rejected: list[dict] = []

    for item in items:
        if not isinstance(item, dict):
            rejected.append({"item": item, "reason": "not an object"})
            continue
        sid = str(item.get("skill_id", "")).strip()
        req = item.get("requirement")
        raw = str(item.get("raw_text", "")).strip()
        if req not in ("required", "nice_to_have"):
            rejected.append({"item": item, "reason": "bad requirement"})
            continue
        if not raw or _norm(raw) not in jd:
            rejected.append({"item": item, "reason": "raw_text not found in job text"})
            continue

        if sid.lower().startswith(NEW_PREFIX):
            label = sid[len(NEW_PREFIX):].strip()
            known = tax.resolve(label)
            if known is None:
                key = label.lower()
                if key and (key not in proposed or req == "required"):
                    proposed[key] = Proposed(label, req, raw)
                continue
            sid = known
        elif sid not in tax.skills:
            known = tax.resolve(sid)  # model sometimes emits the display name
            if known is None:
                rejected.append({"item": item, "reason": "unknown skill_id"})
                continue
            sid = known

        prev = by_id.get(sid)
        if prev is None or (prev.requirement == "nice_to_have" and req == "required"):
            by_id[sid] = Mention(sid, req, raw)

    mentions = sorted(by_id.values(), key=lambda m: m.skill_id)
    return mentions, sorted(proposed.values(), key=lambda p: p.label.lower()), rejected


def parse_seniority(data: dict, jd_text: str) -> Seniority:
    """Validate the model's seniority fields; anything inconsistent collapses to NO_SENIORITY.

    A level needs a basis; a signal must be quoted from the text (else it is dropped, the
    level is kept); "stated" requires a signal, since a stated level is by definition visible.
    """
    level = data.get("seniority")
    basis = data.get("seniority_basis")
    signal = data.get("seniority_signal")
    if level not in SENIORITY_LEVELS or basis not in ("stated", "inferred"):
        return NO_SENIORITY
    if isinstance(signal, str):
        signal = signal.strip() or None
        if signal and _norm(signal) not in _norm(jd_text):
            signal = None
    else:
        signal = None
    if basis == "stated" and signal is None:
        return NO_SENIORITY
    return Seniority(level, basis, signal)


def build_request(tax: Taxonomy, jd_text: str, model: str) -> dict:
    return {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "system": [{"type": "text", "text": system_prompt(tax), "cache_control": {"type": "ephemeral"}}],
        "tools": [TOOL],
        "tool_choice": {"type": "auto"},
        "messages": [{"role": "user", "content": f"<job_description>\n{jd_text}\n</job_description>"}],
    }


# --- I/O wrapper ------------------------------------------------------------------

def make_client():
    import anthropic  # imported here so tests never need credentials
    return anthropic.Anthropic()


def extract(jd_text: str, tax: Taxonomy, client, model: str = DEFAULT_MODEL) -> Extraction:
    response = client.messages.create(**build_request(tax, jd_text, model))
    if response.stop_reason in ("max_tokens", "refusal"):
        raise ExtractionError(f"call did not complete: stop_reason={response.stop_reason!r}")
    blocks = [b for b in response.content if getattr(b, "type", None) == "tool_use" and b.name == TOOL["name"]]
    if len(blocks) != 1:
        raise ExtractionError(f"expected one {TOOL['name']} call, got {len(blocks)}")
    items = blocks[0].input.get("skills")
    if not isinstance(items, list):
        raise ExtractionError("tool input has no 'skills' list")

    mentions, proposed, rejected = parse_skills(items, tax, jd_text)
    usage = getattr(response, "usage", None)
    return Extraction(
        seniority=parse_seniority(blocks[0].input, jd_text),
        mentions=mentions,
        proposed=proposed,
        rejected=rejected,
        extractor_version=extractor_version(tax, model),
        taxonomy_version=tax.version,
        usage={k: getattr(usage, k, None) for k in
               ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")} if usage else {},
    )
