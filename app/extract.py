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
  - German, degree and production experience follow the same rule: a value needs its quoted
    signal from the text ("inferred" German — a posting written in German — is the one
    exception, and carries no signal; production has no inferred case at all). Anything
    inconsistent collapses to "not mentioned", never to a guess.
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
# What the model is sent, beyond the prompt. Part of extractor_version, so changing how the
# input is built re-extracts every job, the same as a prompt or taxonomy change.
INPUT_FORMAT = "title-on-top"

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
- seniority_basis is "stated" when the title or text names the level outright. Otherwise
  "inferred", and only from: years of experience (0-2 junior, 3-5 mid, 5+ senior), "proven
  experience" (mid), or lead or mentoring responsibility (senior). Words like experienced,
  expert, advanced, autonomous, or production experience are not level signals on their own.
- A posting open to several levels ("all levels", or separate requirements per level) has
  no single level: null. If the posting gives no usable signal, set seniority to null and
  basis to null.
- seniority_signal is the verbatim phrase you based it on, or null.

Also report whether the posting asks for German:
- german is "required" when German is asked for and not marked optional, "nice_to_have"
  when it is marked optional (plus, preferred, ideally, advantage), or null when the
  posting does not mention German at all. English or other languages do not count.
- german_basis is "stated" when the text asks for German outright; "inferred" when the
  posting itself is written in German and says nothing about language (treat that as
  "required"). Otherwise null.
- german_signal is the verbatim phrase, or null when inferred or not mentioned.

Also report the degree the posting asks for:
- degree is the highest level named: "bachelor", "master", or "phd" (an unspecified
  "degree in computer science" is "bachelor"). null when no degree is mentioned.
- degree_requirement is "nice_to_have" only when the degree is marked optional; otherwise
  "required", including a bare mention in a requirements list. null when degree is null.
- degree_or_equivalent is true when the posting accepts equivalent or comparable
  experience in place of the degree ("or equivalent experience", "or comparable
  qualification"). false otherwise, and false when degree is null.
- degree_signal is the verbatim phrase naming the degree (include the "or equivalent"
  wording if present), or null.

Also report whether the posting asks the candidate for prior production experience:
- The question is whether the candidate is asked for a record of having shipped or operated
  software that real users depended on. Markers for "required": that experience is asked of
  the candidate and not marked optional — "you have shipped X to production", "track record
  of building production-grade services", "experience building and operating production
  systems", "experience deploying production-quality software", "commercial experience in
  production environments". In German: "Du hast bereits Produkte in den produktiven Betrieb
  gebracht", "Erfahrung mit produktiven Anwendungen", "Erfahrung im produktiven Einsatz".
- "nice_to_have" when that same ask is marked optional (plus, preferred, ideally, advantage,
  bonus).
- null when the posting does not ask the candidate for it. Work the job involves is not an
  ask: "you will deploy models to production", "take prototypes to production", "from idea
  to production", "von der Idee bis zum produktiven Einsatz" are responsibilities, null —
  the same rule as for technologies that appear only in responsibilities. A standard for the
  code rather than a record of shipping it is also null: "write production-grade code",
  "strong Python skills, including writing production-quality code and tests".
- production_basis is "stated" whenever a value is set; there is nothing to infer.
- production_signal is the verbatim phrase, or null when not mentioned.

Always respond by calling the record_skills tool exactly once. Do not reply with text."""

SENIORITY_LEVELS = ("junior", "mid", "senior")
REQUIREMENT_LEVELS = ("required", "nice_to_have")
DEGREE_LEVELS = ("bachelor", "master", "phd")

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
            # A nullable enum must be anyOf: the API rejects an enum whose values do not all
            # match a union `type` (400 "Enum value 'junior' does not match declared type").
            "seniority": {"anyOf": [{"type": "string", "enum": list(SENIORITY_LEVELS)}, {"type": "null"}]},
            "seniority_basis": {"anyOf": [{"type": "string", "enum": ["stated", "inferred"]}, {"type": "null"}]},
            "seniority_signal": {"type": ["string", "null"]},
            "german": {"anyOf": [{"type": "string", "enum": list(REQUIREMENT_LEVELS)}, {"type": "null"}]},
            "german_basis": {"anyOf": [{"type": "string", "enum": ["stated", "inferred"]}, {"type": "null"}]},
            "german_signal": {"type": ["string", "null"]},
            "degree": {"anyOf": [{"type": "string", "enum": list(DEGREE_LEVELS)}, {"type": "null"}]},
            "degree_requirement": {"anyOf": [{"type": "string", "enum": list(REQUIREMENT_LEVELS)}, {"type": "null"}]},
            "degree_or_equivalent": {"type": "boolean"},
            "degree_signal": {"type": ["string", "null"]},
            "production": {"anyOf": [{"type": "string", "enum": list(REQUIREMENT_LEVELS)}, {"type": "null"}]},
            "production_basis": {"anyOf": [{"type": "string", "enum": ["stated"]}, {"type": "null"}]},
            "production_signal": {"type": ["string", "null"]},
        },
        "required": ["skills", "seniority", "seniority_basis", "seniority_signal",
                     "german", "german_basis", "german_signal",
                     "degree", "degree_requirement", "degree_or_equivalent", "degree_signal",
                     "production", "production_basis", "production_signal"],
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


@dataclass(frozen=True)
class German:
    requirement: str | None   # required | nice_to_have | None (not mentioned)
    basis: str | None         # stated | inferred (posting written in German) | None
    signal: str | None        # verbatim phrase when stated, else None


NO_GERMAN = German(None, None, None)


@dataclass(frozen=True)
class Degree:
    level: str | None         # bachelor | master | phd | None (not mentioned)
    requirement: str | None   # required | nice_to_have | None
    or_equivalent: bool       # posting accepts equivalent experience instead
    signal: str | None        # verbatim phrase; always present when level is set


NO_DEGREE = Degree(None, None, False, None)


@dataclass(frozen=True)
class Production:
    """Prior experience shipping or operating software real users depended on (HIR-69)."""
    requirement: str | None   # required | nice_to_have | None (not asked for)
    basis: str | None         # 'stated' or None: there is no inferred case, unlike German
    signal: str | None        # verbatim phrase; always present when requirement is set


NO_PRODUCTION = Production(None, None, None)


@dataclass
class Extraction:
    seniority: Seniority = NO_SENIORITY
    german: German = NO_GERMAN
    degree: Degree = NO_DEGREE
    production: Production = NO_PRODUCTION
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
    h = hashlib.sha256((system_prompt(tax) + repr(TOOL) + model + INPUT_FORMAT).encode()).hexdigest()
    return f"x2-{h[:10]}"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def extraction_input(title: str | None, text: str) -> str:
    """The text the model sees: the job title on top, then the posting.

    Feed sources keep the title in its own column, so without this the model never sees
    "Senior …" or "Werkstudent …", the main stated-seniority signal. Text that already opens
    with the title (screenshots, pasted postings) is left as is."""
    t = (title or "").strip()
    if not t or _norm(t) in _norm(text[:300]):
        return text
    return f"{t}\n\n{text}"


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


def _quoted(signal, jd_text: str) -> str | None:
    """The signal if it is a non-empty string found in the text, else None."""
    if not isinstance(signal, str):
        return None
    signal = signal.strip()
    return signal if signal and _norm(signal) in _norm(jd_text) else None


def parse_german(data: dict, jd_text: str) -> German:
    """Validate the German fields. "stated" needs a quoted signal; "inferred" means the
    posting is written in German and carries no signal. Anything else is NO_GERMAN."""
    req = data.get("german")
    basis = data.get("german_basis")
    if req not in REQUIREMENT_LEVELS or basis not in ("stated", "inferred"):
        return NO_GERMAN
    if basis == "inferred":
        return German(req, basis, None)
    signal = _quoted(data.get("german_signal"), jd_text)
    return German(req, basis, signal) if signal else NO_GERMAN


def parse_degree(data: dict, jd_text: str) -> Degree:
    """Validate the degree fields. A degree is always stated, so a level without a quoted
    signal is dropped. or_equivalent is only kept alongside a level."""
    level = data.get("degree")
    req = data.get("degree_requirement")
    if level not in DEGREE_LEVELS or req not in REQUIREMENT_LEVELS:
        return NO_DEGREE
    signal = _quoted(data.get("degree_signal"), jd_text)
    if not signal:
        return NO_DEGREE
    return Degree(level, req, bool(data.get("degree_or_equivalent")), signal)


def parse_production(data: dict, jd_text: str) -> Production:
    """Validate the production-experience fields. The demand is always visible in the text,
    so a requirement without a quoted signal is dropped; there is no inferred basis."""
    req = data.get("production")
    if req not in REQUIREMENT_LEVELS or data.get("production_basis") != "stated":
        return NO_PRODUCTION
    signal = _quoted(data.get("production_signal"), jd_text)
    return Production(req, "stated", signal) if signal else NO_PRODUCTION


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
        german=parse_german(blocks[0].input, jd_text),
        degree=parse_degree(blocks[0].input, jd_text),
        production=parse_production(blocks[0].input, jd_text),
        mentions=mentions,
        proposed=proposed,
        rejected=rejected,
        extractor_version=extractor_version(tax, model),
        taxonomy_version=tax.version,
        usage={k: getattr(usage, k, None) for k in
               ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")} if usage else {},
    )
