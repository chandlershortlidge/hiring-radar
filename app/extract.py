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
  - Alternative groups (HIR-251) are numbered 1..n per job and have at least two members;
    a skill asked for on its own as well as in a group is kept on its own.
  - Every mention's raw_text is found in the job text (whitespace/case-insensitive);
    unsupported items are reported in `rejected`, not silently kept.
  - A call that does not produce exactly one record_skills tool call raises
    ExtractionError. tool_choice is "auto" (forced tool use is rejected by current
    models), so the prompt asks for the call and `strict` keeps its arguments valid.
  - A tool call that carries nothing at all — no skills, nothing proposed, nothing
    rejected, and none of the four attributes — raises EmptyExtractionError (HIR-172). A
    well-formed empty call is a failed read, not a posting without skills: the caller
    leaves the job unstamped and counts it as failed, instead of storing a blank job that
    looks processed, and drops the posting if a second read is blank too (Chandler's
    decision of 5 Nov). Zero skills *with* any attribute found stays a success.
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
   Wanting a skill is not having it: wording that asks only for appetite toward the skill
   ("eager to", "eagerness to", "interest in", "interested in", "keen to", "curious about",
   "excited by", "hungry to", "willing to learn", German "Interesse an", "Lust auf") makes
   that skill "nice_to_have" whatever the heading says. So does wording that accepts
   appetite in place of experience — "experience with X, or a strong interest in X" — since
   the candidate can qualify without X.
   Three limits. The appetite has to govern the skill itself: where one sentence asks the
   candidate to have one skill and only wants another, the first is "required" and the
   second is "nice_to_have". A clause about deepening, growing in, or continuing to learn a
   skill the sentence already asks for does not soften it: that skill stays "required".
   And the employer's own enthusiasm about candidates or applications is not the candidate's
   appetite toward a skill, so it changes no label.
   When a label rests on appetite wording, raw_text must include the appetite phrase, not
   just the bare skill name.
7. raw_text is the exact phrase from the job description that supports the skill, copied
   verbatim.
8. Report each skill id at most once. Report every skill you find.
9. alternative_group: when the posting accepts any one of several skills in place of each
   other, give each of them the same alternative_group number — 1 for the first such set
   in the posting, 2 for the next. Markers: "at least one of", "one or more of",
   "X, Y or Z", "X and/or Y", and examples offered for a single ask ("a language such as
   X, Y, or Z", "a framework like X or Y"): the posting wants the ask, and any one example
   meets it. Every member takes the requirement of the ask as a whole, by rule 6.
   Grouping never removes a skill: report every skill rules 3 and 4 call for, then mark
   the groups. A broad skill named with its examples ("B such as X, Y or Z") is still
   reported, with alternative_group null; only X, Y and Z share a group. "or other",
   "or similar" and "or comparable" add no skill of their own, but every skill the text
   does name is still reported. Skills asked for together ("X and Y", "X, Y and Z") are
   not alternatives: null. A set needs at least two skills; any skill not in one is null.

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

Also report whether the posting demands production work of the candidate:
- The question is whether the candidate is asked to build, ship, operate, deploy or run
  software that real users depend on. Test the verb against its object: one of
  build / ship / operate / deploy / run, applied to production systems, services,
  applications, pipelines or workflows, is "required". **The verb carries the demand, not the tense**:
  a past record ("you have shipped X to production"), a present ability ("able to take a
  service to production") and a stated expectation count equally.
  **Building alone is enough** — "you have built production data pipelines" is "required"
  with no shipping or operating clause beside it — and a hyphenated modifier on the
  object does not weaken it: production-grade, production-ready and production-oriented
  software is production software. Markers for "required": that demand is made of the candidate and not marked
  optional — "track record of building and running production systems", "experience
  building and operating production systems", "commercial experience in production
  environments". In German: "Du hast bereits Produkte in den produktiven Betrieb
  gebracht", "Erfahrung mit produktiven Anwendungen", "Erfahrung im produktiven Einsatz".
- "nice_to_have" when that same demand is marked optional. The marker may be explicit
  (plus, preferred, ideally, advantage, bonus) or soft phrasing that frames the demand as
  welcome rather than expected (relevant, welcome, helpful, appreciated, of interest).
- null when the posting does not ask the candidate for it. Work the job involves is not an
  ask: "you will deploy models to production", "take prototypes to production", "from idea
  to production", "von der Idee bis zum produktiven Einsatz" are responsibilities, null —
  the same rule as for technologies that appear only in responsibilities.
- A bar on the code itself, with no demand to build, ship or run it, is null:
  "write production-grade code", "strong Python skills, including writing
  production-quality code and tests". The verb decides, not the modifier — build, ship,
  operate, deploy or run production software is "required"; write, or code to, a
  production standard is null. One posting often carries both a clause apart; label the
  demanding clause, ignore the quality clause.
- What the candidate knows *about* production — MLOps, deployment, monitoring — is a
  knowledge bar, not a demand to have done it: "familiar with MLOps practice and how
  models are served once live" is null. Asking what someone knows of production is not
  asking what they have built or run.
- A demand scoped to one seniority level in a posting open to several levels is null: a
  bullet prefixed with a level heading, in a posting whose title or requirements invite
  more than one level, is not a job-wide demand, because the track open to a junior does
  not carry it. A demand that every candidate the posting invites must meet is "required".
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
                        "alternative_group": {"anyOf": [{"type": "integer"}, {"type": "null"}],
                                              "description": "Same number = any one of these meets the ask; null otherwise."},
                    },
                    "required": ["skill_id", "requirement", "raw_text", "alternative_group"],
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


class EmptyExtractionError(ExtractionError):
    """The call completed but carried nothing at all — a failed read, not a blank posting.

    Its own type because the caller treats it differently from a transport or schema
    failure: a posting that reads blank twice is dropped (HIR-172), while a connection
    error can be retried for ever.
    """


@dataclass(frozen=True)
class Mention:
    skill_id: str
    requirement: str
    raw_text: str
    # Same number on two or more mentions of one job = alternatives: any one meets the
    # requirement (HIR-251). None = the skill stands alone.
    alternative_group: int | None = None


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
    """A demand to ship or operate software real users depend on (HIR-69)."""
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
    # The model's tool call exactly as it arrived, before any validation dropped or rewrote an
    # item, and the model that produced it. Kept so a reading can be re-parsed years later by
    # something better than today's parser (HIR-170); nothing in the pipeline reads them.
    # None on an Extraction built by hand rather than from a model call (the seed and legacy
    # import scripts), which is how the log tells a real reading from a backfilled row.
    raw_output: dict | None = None
    model: str = ""


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

        group = item.get("alternative_group")
        group = group if isinstance(group, int) and not isinstance(group, bool) and group >= 1 else None
        prev = by_id.get(sid)
        if prev is None or _stronger(req, group, prev):
            by_id[sid] = Mention(sid, req, raw, group)

    mentions = sorted(_settle_groups(by_id.values()), key=lambda m: m.skill_id)
    return mentions, sorted(proposed.values(), key=lambda p: p.label.lower()), rejected


def _stronger(req: str, group: int | None, prev: Mention) -> bool:
    """Does a second mention of the same skill outrank the one kept? Required beats
    nice-to-have; at the same level, asked for on its own beats being one of a group,
    since a standalone ask is a requirement by itself (DECISIONS 2026-11-11)."""
    if req != prev.requirement:
        return req == "required"
    return group is None and prev.alternative_group is not None


def _settle_groups(mentions) -> list[Mention]:
    """Renumber groups 1..n in order of the model's numbers, and drop the number from a
    group left with one member (its partners were rejected, unknown, or kept standalone):
    an alternative to nothing is a plain mention."""
    mentions = list(mentions)
    sizes: dict[int, int] = {}
    for m in mentions:
        if m.alternative_group is not None:
            sizes[m.alternative_group] = sizes.get(m.alternative_group, 0) + 1
    renumber = {g: i for i, g in enumerate(sorted(g for g, n in sizes.items() if n > 1), start=1)}
    return [Mention(m.skill_id, m.requirement, m.raw_text, renumber.get(m.alternative_group)) for m in mentions]


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


def extraction_from_message(response, tax: Taxonomy, jd_text: str, model: str) -> Extraction:
    """Turn one model response into a validated Extraction. `response` is a `Message`,
    whichever call produced it: `client.messages.create`'s return value, or one item's
    `result.message` from the Batch API (app/pipeline.py, HIR-222) — both carry the same
    shape, so a batched reading is validated exactly like a direct one."""
    if response.stop_reason in ("max_tokens", "refusal"):
        raise ExtractionError(f"call did not complete: stop_reason={response.stop_reason!r}")
    blocks = [b for b in response.content if getattr(b, "type", None) == "tool_use" and b.name == TOOL["name"]]
    if len(blocks) != 1:
        raise ExtractionError(f"expected one {TOOL['name']} call, got {len(blocks)}")
    items = blocks[0].input.get("skills")
    if not isinstance(items, list):
        raise ExtractionError("tool input has no 'skills' list")

    mentions, proposed, rejected = parse_skills(items, tax, jd_text)
    seniority = parse_seniority(blocks[0].input, jd_text)
    german = parse_german(blocks[0].input, jd_text)
    degree = parse_degree(blocks[0].input, jd_text)
    production = parse_production(blocks[0].input, jd_text)
    if not (mentions or proposed or rejected) and (
            (seniority, german, degree, production)
            == (NO_SENIORITY, NO_GERMAN, NO_DEGREE, NO_PRODUCTION)):
        raise EmptyExtractionError(
            "tool call carried nothing: no skills and no seniority/german/degree/production")

    usage = getattr(response, "usage", None)
    return Extraction(
        seniority=seniority,
        german=german,
        degree=degree,
        production=production,
        mentions=mentions,
        proposed=proposed,
        rejected=rejected,
        extractor_version=extractor_version(tax, model),
        taxonomy_version=tax.version,
        usage={k: getattr(usage, k, None) for k in
               ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")} if usage else {},
        raw_output=dict(blocks[0].input),
        model=model,
    )


def extract(jd_text: str, tax: Taxonomy, client, model: str = DEFAULT_MODEL) -> Extraction:
    response = client.messages.create(**build_request(tax, jd_text, model))
    return extraction_from_message(response, tax, jd_text, model)
