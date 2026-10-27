"""Draft held-out Goldens with two blind labeler agents, then a human review queue (HIR-70).

Pipeline, in two commands:

    label:  pick postings -> labeler A and labeler B, blind -> deterministic auto-check
            -> merge (agreement accepted, disagreement queued) -> spot-check sample
            -> evals/labeling/<run>/{review_queue.md, summary.md, summary.json}
    apply:  read the decisions a person wrote into review_queue.md -> write final Goldens
            to evals/goldens/ with split "heldout" and provenance, and report the
            spot-check error rate with a 95% Wilson interval.

Does: build each labeler's prompt from evals/LABELER_PROMPT.md with evals/LABELING.md and
the taxonomy inlined; send each labeler nothing but that plus the posting; cache every raw
labeler response under the run directory so re-merging never re-calls a model; check every
quote verbatim and every field for internal consistency; report labeler agreement.

Does NOT: run the held-out eval (that is scripts/run_eval.py --split heldout
--i-am-releasing, at a release point, and never from here); share anything with
app/extract.py beyond the taxonomy loader, the whitespace rule and the input format;
show either labeler the extractor's prompt, the extractor's output, or the other
labeler's answer; accept a label a person has not either agreed-twice or decided.

Invariants:
  - Neither labeler may run on the extractor's model. The script refuses, it does not warn:
    a labeler sharing the extractor's blind spots makes the eval look better than it is.
  - The posting a labeler sees is byte-identical to what the extractor receives in
    production (extract.extraction_input: title on top), so the Golden measures extraction
    and not a difference in input.
  - "Agreed" means A and B produced the same skill_id with the same requirement, or the same
    attribute value and basis. Everything else - disagreement, anything either labeler
    flagged uncertain, and every auto-check failure - goes to the review queue. Nothing is
    dropped silently.
  - The spot-check samples accepted labels at the label level (one skill, one attribute),
    not whole postings, with a recorded seed, so the error rate it measures is per label.
  - apply writes only Goldens whose every queued item carries a decision.

    uv run python scripts/agent_label.py label --dry-run
    uv run python scripts/agent_label.py label --count 24 --remote-eu 3 --german 6
    uv run python scripts/agent_label.py label --run <run_id>      # re-merge from cache
    uv run python scripts/agent_label.py apply --run <run_id>
"""

import argparse
import importlib.util
import json
import os
import random
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# DEFAULT_MODEL to enforce the refusal, extraction_input so the labeler sees exactly what
# the extractor sees, _norm so "appears verbatim" means the same thing here as in
# parse_skills. Deliberately nothing else from extract: no PRINCIPLES, no extract().
from app.extract import DEFAULT_MODEL as EXTRACTOR_MODEL  # noqa: E402
from app.extract import _norm as norm_text  # noqa: E402
from app.extract import extraction_input  # noqa: E402
from app.taxonomy import Taxonomy  # noqa: E402

_spec = importlib.util.spec_from_file_location("new_goldens", ROOT / "scripts" / "new_goldens.py")
ng = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ng)

GOLDENS = ROOT / "evals" / "goldens"
RUNS = ROOT / "evals" / "labeling"
PROMPT_FILE = ROOT / "evals" / "LABELER_PROMPT.md"
GUIDE_FILE = ROOT / "evals" / "LABELING.md"

DEFAULT_MODEL_A = "claude-opus-5-5"
DEFAULT_MODEL_B = "gpt-6.1-sol"   # verified against OpenAI /v1/models, 2026-10-27
MAX_TOKENS = 8192
SPOT_CHECK_N = 80
SEED = 0

REQUIREMENTS = ("required", "nice_to_have")
SENIORITIES = ("junior", "mid", "senior")
DEGREES = ("bachelor", "master", "phd")
BASES = ("stated", "inferred")
ATTRS = ("seniority", "german", "degree")
# The fields that travel together when a person decides one attribute.
ATTR_FIELDS = {
    "seniority": ("seniority", "seniority_basis", "seniority_signal"),
    "german": ("german", "german_basis", "german_signal"),
    "degree": ("degree", "degree_requirement", "degree_or_equivalent", "degree_signal"),
}
# What agreement is judged on. Signals are checked verbatim but not compared: two correct
# quotes of the same requirement often differ in length. A signal mismatch alongside an
# agreed value is recorded in summary.json, not queued.
ATTR_KEYS = {
    "seniority": ("seniority", "seniority_basis"),
    "german": ("german", "german_basis"),
    "degree": ("degree", "degree_requirement", "degree_or_equivalent"),
}

ROLE_FAMILIES = (
    ("data-engineer", r"data\s*engineer|dateningenieur|etl"),
    ("ml-engineer", r"\b(ml|machine[\s-]*learning|mlops)\b"),
    ("data-scientist", r"data\s*scientist|datenanalyst|analytics"),
    ("research", r"research|scientist|wissenschaft"),
    ("ai-engineer", r"\b(ai|ki|llm|genai|gen[\s-]*ai)\b"),
    ("backend", r"backend|platform|software\s*engineer|entwickler"),
)


# --- pure parts -------------------------------------------------------------------

def role_family(title: str | None) -> str:
    """A coarse role bucket, for spreading the picks across job kinds."""
    t = (title or "").lower()
    for name, pattern in ROLE_FAMILIES:
        if re.search(pattern, t):
            return name
    return "other"


def taxonomy_lines(tax: Taxonomy) -> str:
    """The taxonomy as the labeler sees it: extract.taxonomy_block's format, no parents."""
    lines = [f"TAXONOMY (version {tax.version}) - id: Display [aliases]"]
    for s in sorted(tax.skills.values(), key=lambda s: s.id):
        alias = f" [{', '.join(s.aliases)}]" if s.aliases else ""
        lines.append(f"{s.id}: {s.display}{alias}")
    return "\n".join(lines)


def labeler_prompt(prompt_md: str, guide_md: str, tax: Taxonomy) -> str:
    """LABELER_PROMPT.md with its three placeholders filled.

    Everything above the `---` separator is file-level documentation for people, not
    instructions for the labeler, so it is dropped."""
    body = prompt_md.split("\n---\n", 1)[-1].strip()
    body = body.replace("{LABELING.md, verbatim}", guide_md.strip())
    body = body.replace("{TAXONOMY (version N) - id: Display [aliases], one skill per line}",
                        taxonomy_lines(tax))
    body = body.replace("{TAXONOMY (version N) — id: Display [aliases], one skill per line}",
                        taxonomy_lines(tax))
    # The posting arrives as the user turn; drop its placeholder block from the system text.
    return re.sub(r"<posting>.*?</posting>\n*", "", body, flags=re.S)


def parse_response(text: str) -> dict:
    """The one JSON object the labeler was asked for, fences and stray prose tolerated."""
    s = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", s, flags=re.S)
    if fence:
        s = fence.group(1).strip()
    start = s.find("{")
    if start == -1:
        raise ValueError("no JSON object in response")
    depth, in_str, esc = 0, False, False
    for i, ch in enumerate(s[start:], start):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(s[start:i + 1])
    raise ValueError("unterminated JSON object in response")


def _quoted(value, posting: str) -> bool:
    return isinstance(value, str) and bool(value.strip()) and norm_text(value) in norm_text(posting)


def auto_check(parsed: dict, posting: str, tax: Taxonomy) -> list[dict]:
    """Deterministic checks on one labeler's answer. Returns problems; empty means clean.

    Each problem names the scope a person would have to decide: `skill:<id>` (or
    `skill:#<n>` when the id itself is the problem), `field:<attr>`, or `run`.
    """
    problems: list[dict] = []

    def add(scope, problem):
        problems.append({"scope": scope, "problem": problem})

    items = parsed.get("expected")
    if not isinstance(items, list):
        add("run", "`expected` is not a list")
        items = []

    seen = Counter()
    for n, item in enumerate(items):
        if not isinstance(item, dict):
            add(f"skill:#{n}", "item is not an object")
            continue
        sid = str(item.get("skill_id", "")).strip()
        scope = f"skill:{sid}" if sid else f"skill:#{n}"
        if not sid:
            add(scope, "missing skill_id")
        elif sid not in tax.skills:
            resolved = tax.resolve(sid)
            add(scope, f"skill_id not in the taxonomy (did it mean {resolved!r}?)"
                if resolved else "skill_id not in the taxonomy")
        else:
            seen[sid] += 1
        req = item.get("requirement")
        if req not in REQUIREMENTS:
            add(scope, f"requirement is {req!r}, not one of {REQUIREMENTS}")
        if not _quoted(item.get("raw_text"), posting):
            add(scope, f"raw_text does not appear in the posting: {item.get('raw_text')!r}")
    for sid, n in seen.items():
        if n > 1:
            add(f"skill:{sid}", f"{n} criteria for one skill_id; the guide allows one")

    def enum_ok(field_name, allowed, scope):
        v = parsed.get(field_name)
        if v is None or v in allowed:
            return True
        add(scope, f'{field_name} is {v!r}' + (' - the string "null", not JSON null'
                                               if isinstance(v, str) and v.lower() in ("null", "none", "")
                                               else f", not one of {allowed}"))
        return False

    for attr, allowed in (("seniority", SENIORITIES), ("german", REQUIREMENTS), ("degree", DEGREES)):
        scope = f"field:{attr}"
        enum_ok(attr, allowed, scope)
        if attr != "degree":
            enum_ok(f"{attr}_basis", BASES, scope)
        signal = parsed.get(f"{attr}_signal")
        if signal is not None and not _quoted(signal, posting):
            add(scope, f"{attr}_signal does not appear in the posting: {signal!r}")

    for attr in ("seniority", "german"):
        scope, value, basis = f"field:{attr}", parsed.get(attr), parsed.get(f"{attr}_basis")
        signal = parsed.get(f"{attr}_signal")
        if (value is None) != (basis is None):
            add(scope, f"{attr}={value!r} but {attr}_basis={basis!r}; a value needs a basis and vice versa")
        if basis == "stated" and signal is None:
            add(scope, f'{attr}_basis is "stated" but {attr}_signal is null; a stated label quotes the text')
    if parsed.get("german_basis") == "inferred" and parsed.get("german_signal") is not None:
        add("field:german", 'german_basis is "inferred" (the posting is written in German), '
                            "so german_signal must be null")
    if parsed.get("seniority_basis") == "inferred" and parsed.get("seniority_signal") is None:
        add("field:seniority", 'seniority_basis is "inferred" but seniority_signal is null; '
                               "an inferred level still quotes what it was read from")

    degree, dreq = parsed.get("degree"), parsed.get("degree_requirement")
    or_eq, dsig = parsed.get("degree_or_equivalent"), parsed.get("degree_signal")
    if degree is None:
        if dreq is not None:
            add("field:degree", f"degree is null but degree_requirement is {dreq!r}")
        if or_eq:
            add("field:degree", "degree is null but degree_or_equivalent is true")
        if dsig is not None:
            add("field:degree", f"degree is null but degree_signal is {dsig!r}")
    else:
        if dreq not in REQUIREMENTS:
            add("field:degree", f"degree is {degree!r} but degree_requirement is {dreq!r}")
        if dsig is None:
            add("field:degree", "degree is set but degree_signal is null; a degree is always stated")
    if not isinstance(or_eq, bool):
        add("field:degree", f"degree_or_equivalent is {or_eq!r}, not a boolean")

    return problems


def uncertain_skills(parsed: dict) -> set[str]:
    out = set()
    for item in parsed.get("expected") or []:
        if isinstance(item, dict) and item.get("uncertain") is True:
            out.add(str(item.get("skill_id", "")).strip())
    return out


def uncertain_attrs(parsed: dict) -> set[str]:
    flagged = parsed.get("uncertain")
    if isinstance(flagged, list):
        return {str(f).strip() for f in flagged} & set(ATTRS)
    return set()


def skills_by_id(parsed: dict) -> dict[str, dict]:
    """The labeler's skill items keyed by id. A repeated id keeps the first; auto_check
    has already flagged the repeat, so the item is going to review either way."""
    out: dict[str, dict] = {}
    for item in parsed.get("expected") or []:
        if not isinstance(item, dict):
            continue
        sid = str(item.get("skill_id", "")).strip()
        if sid and sid not in out:
            out[sid] = {"skill_id": sid, "requirement": item.get("requirement"),
                        "raw_text": item.get("raw_text")}
    return out


def attr_group(parsed: dict, attr: str) -> dict:
    return {f: parsed.get(f) for f in ATTR_FIELDS[attr]}


def excerpt(posting: str, quote, width: int = 140) -> str:
    """The posting around a quote, for the review queue. Falls back to the opening line."""
    if isinstance(quote, str) and quote.strip():
        i = norm_text(posting).find(norm_text(quote))
        if i != -1:
            # norm_text collapses whitespace, so map back by searching the raw text loosely.
            pattern = r"\s+".join(re.escape(w) for w in quote.split())
            m = re.search(pattern, posting, flags=re.I)
            if m:
                a, b = max(0, m.start() - 60), min(len(posting), m.end() + 60)
                before, after = posting[a:m.start()], posting[m.end():b]
                # snap to word boundaries, so the quote is not buried in a half word
                before = before.split(" ", 1)[-1] if a > 0 and " " in before else before
                after = after.rsplit(" ", 1)[0] if b < len(posting) and " " in after else after
                return (("..." if a > 0 else "") + " ".join((before + m.group(0) + after).split())
                        + ("..." if b < len(posting) else ""))
        return f"(not found in the posting) {' '.join(str(quote).split())[:width]}"
    return " ".join(posting.splitlines()[0:1])[:width]


@dataclass
class Merged:
    """One posting after merge: what was accepted, and what a person has to decide."""
    golden_id: str
    accepted_skills: list[dict] = field(default_factory=list)
    accepted_attrs: dict = field(default_factory=dict)
    review: list[dict] = field(default_factory=list)
    unmapped: list[dict] = field(default_factory=list)
    signal_mismatches: list[str] = field(default_factory=list)


def merge(golden_id: str, posting: str, a: dict, b: dict,
          a_problems: list[dict], b_problems: list[dict]) -> Merged:
    """Accept what both labelers said; queue everything else.

    Queued, per skill and per field: a disagreement (an id only one labeler gave, a
    requirement they differ on), the same quoted evidence mapped to different ids, anything
    either labeler marked uncertain, and anything auto_check rejected on either side.
    """
    out = Merged(golden_id=golden_id)
    by_scope: dict[str, list[str]] = {}
    for side, problems in (("A", a_problems), ("B", b_problems)):
        for p in problems:
            by_scope.setdefault(p["scope"], []).append(f"{side}: {p['problem']}")

    sa, sb = skills_by_id(a), skills_by_id(b)
    unsure = uncertain_skills(a) | uncertain_skills(b)
    bad_ids = {s.split(":", 1)[1] for s in by_scope if s.startswith("skill:")}

    def queue(kind, key, reason, a_side, b_side, quote, problems=()):
        out.review.append({
            "kind": kind, "key": key, "reason": reason,
            "a": a_side, "b": b_side,
            "excerpt": excerpt(posting, quote),
            "problems": list(problems), "decision": "?",
        })

    for sid in sorted(sa.keys() & sb.keys()):
        ia, ib = sa[sid], sb[sid]
        problems = by_scope.get(f"skill:{sid}", [])
        if problems:
            queue("skill", sid, "check-failed", ia, ib, ia["raw_text"], problems)
        elif ia["requirement"] != ib["requirement"]:
            queue("skill", sid, "disagreement", ia, ib, ia["raw_text"])
        elif sid in unsure:
            queue("skill", sid, "uncertain", ia, ib, ia["raw_text"])
        else:
            out.accepted_skills.append(ia)

    # One-sided ids. Where A and B quoted the same evidence for different ids, show them
    # together: that is a mapping disagreement, not two independent misses.
    one_sided: dict[str, dict] = {}
    for side, mine, theirs in (("a", sa, sb), ("b", sb, sa)):
        for sid in sorted(set(mine) - set(theirs)):
            key = norm_text(mine[sid].get("raw_text") or "") or f"__{side}:{sid}"
            one_sided.setdefault(key, {})[side] = mine[sid]
    for key, sides in one_sided.items():
        ia, ib = sides.get("a"), sides.get("b")
        ids = "|".join(i["skill_id"] for i in (ia, ib) if i)
        problems = [p for i in (ia, ib) if i for p in by_scope.get(f"skill:{i['skill_id']}", [])]
        reason = "check-failed" if problems else ("mapping" if ia and ib else "disagreement")
        queue("skill", ids, reason, ia, ib, (ia or ib)["raw_text"], problems)

    for n, problems in sorted((s, p) for s, p in by_scope.items() if s.startswith("skill:#")):
        queue("skill", n.split(":", 1)[1], "check-failed", None, None, None, problems)
    for problems in [by_scope[s] for s in sorted(by_scope) if s == "run"]:
        queue("run", "response", "check-failed", None, None, None, problems)

    for attr in ATTRS:
        ga, gb = attr_group(a, attr), attr_group(b, attr)
        problems = by_scope.get(f"field:{attr}", [])
        key_a = tuple(ga[f] for f in ATTR_KEYS[attr])
        key_b = tuple(gb[f] for f in ATTR_KEYS[attr])
        quote = ga.get(f"{attr}_signal") or gb.get(f"{attr}_signal")
        if problems:
            queue("attribute", attr, "check-failed", ga, gb, quote, problems)
        elif key_a != key_b:
            queue("attribute", attr, "disagreement", ga, gb, quote)
        elif attr in uncertain_attrs(a) | uncertain_attrs(b):
            queue("attribute", attr, "uncertain", ga, gb, quote)
        else:
            out.accepted_attrs[attr] = ga
            if ga.get(f"{attr}_signal") != gb.get(f"{attr}_signal"):
                out.signal_mismatches.append(
                    f"{golden_id} {attr}: A {ga.get(f'{attr}_signal')!r} vs B {gb.get(f'{attr}_signal')!r}")

    for side, parsed in (("A", a), ("B", b)):
        for item in parsed.get("unmapped") or []:
            if isinstance(item, dict):
                out.unmapped.append({"labeler": side, **item})
    return out


def spot_check_sample(merged: list[Merged], n: int, seed: int) -> list[tuple[str, str, str]]:
    """A seeded sample of accepted labels, at the label level: (golden_id, kind, key).

    The pool is every accepted skill and accepted attribute across the run. Queued items
    are already going to a person, so they are not in it.
    """
    pool = [(m.golden_id, "skill", s["skill_id"]) for m in merged for s in m.accepted_skills]
    pool += [(m.golden_id, "attribute", attr) for m in merged for attr in sorted(m.accepted_attrs)]
    pool.sort()
    return sorted(random.Random(seed).sample(pool, min(n, len(pool))))


def agreement(merged: list[Merged], raw: dict) -> dict:
    """How far labeler B agrees with labeler A, A as the reference.

    Skill precision/recall/F1 on skill_id sets, micro-averaged over postings the same way
    app/evaluation.py averages the eval; requirement agreement on the ids both gave;
    per-attribute agreement on ATTR_KEYS.
    """
    tp = fp = fn = req_same = 0
    attrs = {attr: [0, 0] for attr in ATTRS}
    for m in merged:
        a, b = raw[m.golden_id]["A"], raw[m.golden_id]["B"]
        sa, sb = skills_by_id(a), skills_by_id(b)
        both = sa.keys() & sb.keys()
        tp += len(both)
        fp += len(sb.keys() - sa.keys())
        fn += len(sa.keys() - sb.keys())
        req_same += sum(1 for s in both if sa[s]["requirement"] == sb[s]["requirement"])
        for attr in ATTRS:
            attrs[attr][1] += 1
            if tuple(a.get(f) for f in ATTR_KEYS[attr]) == tuple(b.get(f) for f in ATTR_KEYS[attr]):
                attrs[attr][0] += 1
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = 2 * precision * recall / (precision + recall) if precision and recall else None
    return {
        "n_postings": len(merged),
        "skills": {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1},
        "requirement_agreement": req_same / tp if tp else None,
        "attributes": {attr: {"agreed": k, "n": n, "rate": k / n if n else None}
                       for attr, (k, n) in attrs.items()},
    }


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float] | tuple[None, None]:
    """95% Wilson score interval for k successes in n trials. Honest at small n, where the
    normal approximation puts the bound outside [0, 1]."""
    if n <= 0:
        return (None, None)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


# --- review queue: render and parse -----------------------------------------------

DECISIONS = {
    "disagreement": "`A` / `B` / `both` / `drop`",
    "mapping": "`A` / `B` / `both` / `drop`",
    "uncertain": "`ok` (keep as agreed) / `A` / `B` / `drop`",
    "check-failed": "`A` / `B` / `drop`",
    "spot-check": "`ok` (correct) / `drop` (not a real label) / JSON (what it should be)",
}
QUEUE_HEADER = """# Review queue - {run_id}

{n_items} items from {n_postings} postings. Labeler A: `{model_a}` ({provider_a}).
Labeler B: `{model_b}` ({provider_b}). Extractor (not a labeler): `{extractor}`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run {run_id}` refuses while any `?` is left, then writes the Goldens.

What the words mean:

- `A` / `B` - take that labeler's version of this skill or attribute, as printed below.
- `both` - both skills belong in the answer key (only for two ids on one phrase).
- `drop` - this skill is not in the answer key / this attribute is null for this posting.
- `ok` - the agreed value printed below is right; keep it.
- A JSON object writes the value yourself, e.g.
  `DECISION: {{"requirement": "nice_to_have", "raw_text": "ideally Kubernetes"}}` for a skill,
  or `DECISION: {{"seniority": "senior", "seniority_basis": "stated", "seniority_signal": "Lead AI Engineer"}}`
  for an attribute. A skill override keeps the printed `skill_id` unless you give one.

Spot-check items are a seeded random sample ({spot_n} of {spot_pool} accepted labels,
seed {seed}) of labels A and B already agreed on. They measure the error rate that
agreement alone cannot: two labelers can agree and both be wrong.
"""


def render_item(n: int, item: dict) -> str:
    lines = [f"## {n}. {item['golden_id']} - {item['kind']} `{item['key']}` ({item['reason']})", ""]
    lines += [f"> {item['excerpt']}", ""]
    for side in ("a", "b"):
        value = item.get(side)
        label = "A" if side == "a" else "B"
        if value is None:
            lines.append(f"- {label}: (did not label this)")
        elif item["kind"] == "skill":
            lines.append(f"- {label}: `{value['skill_id']}` · {value['requirement']} · "
                         f"raw_text: {json.dumps(value.get('raw_text'), ensure_ascii=False)}")
        else:
            lines.append(f"- {label}: " + " · ".join(
                f"{k.split('_', 1)[-1] if '_' in k else 'value'}={json.dumps(v, ensure_ascii=False)}"
                for k, v in value.items()))
    if item["problems"]:
        lines += ["", "Auto-check:"] + [f"- {p}" for p in item["problems"]]
    lines += ["", f"Options: {DECISIONS[item['reason']]}", "", "DECISION: ?", ""]
    return "\n".join(lines)


def render_queue(run_id: str, meta: dict, items: list[dict]) -> str:
    head = QUEUE_HEADER.format(**{**meta, "run_id": run_id, "n_items": len(items),
                                  "n_postings": len({i["golden_id"] for i in items})})
    return head + "\n" + "\n".join(render_item(n, i) for n, i in enumerate(items, 1))


def parse_queue(text: str) -> list[tuple[int, str]]:
    """The decision after each numbered item, in order: (item number, decision as written)."""
    out = []
    for m in re.finditer(r"^##\s+(\d+)\..*?^DECISION:[ \t]*(.*?)[ \t]*$",
                         text, flags=re.M | re.S):
        out.append((int(m.group(1)), m.group(2).strip()))
    return out


def apply_decision(item: dict, decision: str):
    """What one decision means. Returns (skills to add, attribute group or None).

    Raises ValueError on a decision the item does not allow, so a typo stops apply rather
    than quietly writing the wrong answer key.
    """
    word = decision.strip()
    if word.startswith("{"):
        override = json.loads(word)
        if item["kind"] == "skill":
            base = dict(item.get("a") or item.get("b") or {})
            base.update(override)
            base.setdefault("skill_id", item["key"].split("|")[0])
            missing = {"skill_id", "requirement", "raw_text"} - {k for k, v in base.items() if v is not None}
            if missing:
                raise ValueError(f"override is missing {sorted(missing)}")
            return [{k: base[k] for k in ("skill_id", "requirement", "raw_text")}], None
        attr = item["key"]
        group = {f: None for f in ATTR_FIELDS[attr]}
        if attr == "degree":
            group["degree_or_equivalent"] = False
        unknown = set(override) - set(ATTR_FIELDS[attr])
        if unknown:
            raise ValueError(f"override has fields that are not part of {attr}: {sorted(unknown)}")
        group.update(override)
        return [], group

    word = word.strip("`").lower()
    if word in ("", "?"):
        raise ValueError("no decision")
    if item["kind"] == "run":
        if word != "drop":
            raise ValueError("a `run` item can only be `drop` (fix the posting and re-run)")
        return [], None
    if word == "drop":
        if item["kind"] == "skill":
            return [], None
        group = {f: None for f in ATTR_FIELDS[item["key"]]}
        if item["key"] == "degree":
            group["degree_or_equivalent"] = False
        return [], group
    if word == "ok":
        if item["reason"] not in ("uncertain", "spot-check"):
            raise ValueError(f"`ok` needs an agreed value; this item is a {item['reason']}")
        side = item.get("a") or item.get("b")
        return ([side], None) if item["kind"] == "skill" else ([], side)
    if word in ("a", "b"):
        side = item.get(word)
        if side is None:
            raise ValueError(f"labeler {word.upper()} did not label this item")
        return ([side], None) if item["kind"] == "skill" else ([], side)
    if word == "both":
        if item["kind"] != "skill":
            raise ValueError("`both` only applies to a skill")
        sides = [s for s in (item.get("a"), item.get("b")) if s]
        if len(sides) != 2:
            raise ValueError("`both` needs a label from each labeler")
        return sides, None
    raise ValueError(f"{decision!r} is not one of A / B / both / drop / ok / a JSON object")


def final_golden(base: dict, skills: list[dict], attrs: dict,
                 labeled_by: list[str], adjudicated: list[str], spot_checked: bool) -> dict:
    """A Golden in the shape evals/goldens/ already uses, plus HIR-70 provenance.

    `*_reviewed` keeps its existing meaning - a person looked at this label - so it is true
    only for a field a person decided or spot-checked, not for one accepted on agreement.
    """
    out = {"id": base["id"], "split": "heldout"}
    for attr in ATTRS:
        group = attrs.get(attr) or {f: None for f in ATTR_FIELDS[attr]}
        for f in ATTR_FIELDS[attr]:
            out[f] = group.get(f) if f != "degree_or_equivalent" else bool(group.get(f))
        if attr == "seniority":
            out["seniority_reviewed"] = "seniority" in adjudicated
    out["attrs_reviewed"] = bool({"german", "degree"} & set(adjudicated))
    out["source_sha256"] = base["source_sha256"]
    out["labeled_by"] = labeled_by
    out["adjudicated"] = sorted(adjudicated)
    out["spot_checked"] = spot_checked
    out["job_description"] = base["job_description"]
    out["expected"] = [{"skill_id": s["skill_id"], "requirement": s["requirement"],
                        "raw_text": s["raw_text"]}
                       for s in sorted(skills, key=lambda s: s["skill_id"])]
    return out


# --- picking ----------------------------------------------------------------------

def describe(row) -> dict:
    sources = sorted(set((row["sources"] or "").split(","))) if row["sources"] else []
    return {
        "job_id": row["id"], "company": row["company"], "title": row["title"],
        "place": row["city"] or "?", "seniority": row["seniority"] or "none",
        "language": "de" if ng.is_german(row["description_text"]) else "en",
        "source": sources[0] if sources else "?", "sources": sources,
        "role": role_family(row["title"]),
    }


def pick(rows, count: int, seed: int, quotas: dict, unmet: list | None = None) -> list:
    """Pick `count` postings spread across seniority, language, source, role and place.

    Quotas first (`remote_eu`, `german`, `source:<name>`, `seniority:<level>`), then fill the
    rest by taking one posting at a time from each stratum in turn, so the picks spread
    instead of clumping on whatever the newest feed happened to return. Seeded, so the same
    database and seed pick the same postings.

    A quota the corpus cannot meet is appended to `unmet` rather than silently under-filled:
    a picks list that quietly misses its spread is the kind of thing that only shows up as a
    surprising eval number weeks later.
    """
    rng = random.Random(seed)
    info = {r["id"]: describe(r) for r in rows}
    pool = sorted(rows, key=lambda r: r["id"])
    rng.shuffle(pool)
    picked, taken = [], set()

    def take(key, matching, n):
        wanted = n
        for r in matching:
            if len(picked) >= count or n <= 0:
                break
            if r["id"] in taken:
                continue
            picked.append(r)
            taken.add(r["id"])
            n -= 1
        if n > 0 and unmet is not None:
            unmet.append(f"{key}: asked for {wanted}, the corpus has {wanted - n}")

    for key, n in sorted(quotas.items()):
        if n <= 0:
            continue
        if key == "remote_eu":
            take(key, [r for r in pool if (r["city"] or "").lower().startswith("remote")], n)
        elif key == "german":
            take(key, [r for r in pool if info[r["id"]]["language"] == "de"], n)
        elif key.startswith("source:"):
            take(key, [r for r in pool if key.split(":", 1)[1] in info[r["id"]]["sources"]], n)
        elif key.startswith("seniority:"):
            take(key, [r for r in pool if info[r["id"]]["seniority"] == key.split(":", 1)[1]], n)
        else:
            raise ValueError(f"unknown quota {key!r}")

    strata: dict[tuple, list] = {}
    for r in pool:
        if r["id"] in taken:
            continue
        d = info[r["id"]]
        strata.setdefault((d["seniority"], d["language"], d["source"], d["role"], d["place"]), []).append(r)
    order = sorted(strata, key=lambda k: (-len(strata[k]), k))
    while len(picked) < count and any(strata[k] for k in order):
        for k in order:
            if len(picked) >= count:
                break
            if strata[k]:
                r = strata[k].pop(0)
                picked.append(r)
                taken.add(r["id"])
    return picked


# --- model calls ------------------------------------------------------------------

def call_anthropic(client, model: str, system: str, user: str) -> str:
    response = client.messages.create(
        model=model, max_tokens=MAX_TOKENS,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user}])
    return "".join(b.text for b in response.content if getattr(b, "type", None) == "text")


def call_openai(client, model: str, system: str, user: str) -> str:
    response = client.chat.completions.create(
        model=model, response_format={"type": "json_object"},
        max_completion_tokens=MAX_TOKENS,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    choice = response.choices[0]
    # A label cut off mid-JSON must fail loudly: truncated JSON sometimes still parses
    # (a closed array with the tail missing), and a short label would silently become a
    # Golden that is missing skills.
    if choice.finish_reason == "length":
        raise RuntimeError(f"{model} hit the {MAX_TOKENS}-token output cap; label is truncated")
    return choice.message.content or ""


PROVIDERS = {"anthropic": call_anthropic, "openai": call_openai}


def make_client(provider: str):
    if provider == "anthropic":
        import anthropic  # imported here so tests never need credentials
        return anthropic.Anthropic()
    if provider == "openai":
        import openai
        return openai.OpenAI()
    raise ValueError(f"unknown provider {provider!r}; use one of {sorted(PROVIDERS)}")


def check_models(model_a: str, model_b: str, extractor: str = EXTRACTOR_MODEL):
    """Refuse to label with the extractor's own model. A labeler that shares the extractor's
    blind spots scores its mistakes as correct, which is the one failure this whole process
    exists to prevent."""
    for name, model in (("A", model_a), ("B", model_b)):
        if model == extractor:
            raise SystemExit(
                f"labeler {name} is {model!r}, the extractor's model. A labeler must not be the "
                f"thing being measured (HIR-70). Pass --model-{name.lower()} with another model, "
                f"or change HIRING_RADAR_MODEL.")
    if model_a == model_b:
        raise SystemExit(f"both labelers are {model_a!r}; two copies of one model are not two labelers.")


def label_posting(posting: str, system: str, provider: str, model: str, client) -> dict:
    """One labeler, one posting. Returns the raw text and the parsed object (or the error)."""
    text = PROVIDERS[provider](client, model, system, f"<posting>\n{posting}\n</posting>")
    record = {"provider": provider, "model": model, "raw": text, "parsed": None, "error": None}
    try:
        record["parsed"] = parse_response(text)
    except (ValueError, json.JSONDecodeError) as e:
        record["error"] = f"{type(e).__name__}: {e}"
    return record


# --- commands ---------------------------------------------------------------------

def run_id_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_label"


def cmd_label(args):
    tax = Taxonomy.load()
    prompt = labeler_prompt(PROMPT_FILE.read_text(), GUIDE_FILE.read_text(), tax)
    labelers = {"A": (args.provider_a, args.model_a), "B": (args.provider_b, args.model_b)}

    if args.run:
        run_dir = RUNS / args.run
        if not run_dir.exists():
            raise SystemExit(f"no such run: {run_dir}")
        queue = run_dir / "review_queue.md"
        if queue.exists() and not args.force:
            decided = [n for n, d in parse_queue(queue.read_text()) if d not in ("?", "")]
            if decided:
                raise SystemExit(
                    f"{queue} already has {len(decided)} decisions, and a re-merge rewrites it. "
                    f"Run `apply --run {args.run}` first, or pass --force to throw them away.")
        picks = json.loads((run_dir / "picks.json").read_text())
    else:
        import sqlite3
        conn = sqlite3.connect(ng.DB)
        conn.row_factory = sqlite3.Row
        used, top = ng.existing()
        rows = ng.candidates(conn, used)
        if not rows:
            raise SystemExit("no candidate jobs (all are already Goldens or legacy imports)")
        quotas = {"remote_eu": args.remote_eu, "german": args.german}
        quotas |= {f"source:{s}": n for s, n in args.source}
        quotas |= {f"seniority:{s}": n for s, n in args.seniority}
        unmet: list[str] = []
        chosen = pick(rows, args.count, args.seed, quotas, unmet)
        picks = []
        for i, r in enumerate(chosen, start=top + 1):
            base = ng.draft(f"golden_{i:03d}", r["description_text"], r["title"])
            picks.append({**describe(r), "golden_id": base["id"],
                          "source_sha256": base["source_sha256"],
                          "job_description": base["job_description"]})
        print(f"{len(picks)} picks (seed {args.seed}):")
        for p in picks:
            print(f"  {p['golden_id']}  job {p['job_id']:>4}  {p['seniority']:<6} {p['language']} "
                  f"{p['source']:<14} {p['role']:<14} {p['place']:<12} {p['company']} · {p['title']}")
        counts = {k: Counter(p[k] for p in picks) for k in ("seniority", "language", "source", "role", "place")}
        for k, c in counts.items():
            print(f"  {k}: " + ", ".join(f"{v}={n}" for v, n in sorted(c.items())))
        for u in unmet:
            print(f"  QUOTA NOT MET  {u}")
        if args.dry_run:
            return
        run_dir = RUNS / run_id_now()
        run_dir.mkdir(parents=True)
        (run_dir / "picks.json").write_text(json.dumps(picks, indent=2, ensure_ascii=False) + "\n")

    check_models(args.model_a, args.model_b)
    prompt_sha = ng.sha(prompt)
    raw_dir = run_dir / "raw"
    raw_dir.mkdir(exist_ok=True)
    clients: dict[str, object] = {}
    raw: dict[str, dict] = {}
    failed: list[str] = []

    for p in picks:
        raw[p["golden_id"]] = {}
        for name, (provider, model) in labelers.items():
            path = raw_dir / f"{p['golden_id']}.{name}.json"
            record = None
            if path.exists():
                cached = json.loads(path.read_text())
                # The prompt is part of the key: LABELING.md and the taxonomy are inlined
                # into it, so a guide edit changes what the labeler was asked. Without this,
                # a --run re-merge silently reuses labels made under the old rules.
                if (cached.get("model") == model
                        and cached.get("posting_sha256") == ng.sha(p["job_description"])
                        and cached.get("prompt_sha256") == prompt_sha):
                    record = cached
            if record is None:
                if provider not in clients:
                    clients[provider] = make_client(provider)
                print(f"  labeling {p['golden_id']} with {name} ({model})", flush=True)
                record = label_posting(p["job_description"], prompt, provider, model, clients[provider])
                record |= {"labeler": name, "posting_sha256": ng.sha(p["job_description"]),
                           "prompt_sha256": prompt_sha}
                path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
            raw[p["golden_id"]][name] = record

    merged: list[Merged] = []
    usable: dict[str, dict] = {}
    for p in picks:
        gid = p["golden_id"]
        bad = [n for n in ("A", "B") if raw[gid][n].get("error")]
        if bad:
            failed.append(f"{gid}: labeler {'/'.join(bad)} returned no usable JSON "
                          f"({raw[gid][bad[0]]['error']})")
            continue
        a, b = raw[gid]["A"]["parsed"], raw[gid]["B"]["parsed"]
        usable[gid] = {"A": a, "B": b}
        merged.append(merge(gid, p["job_description"], a, b,
                            auto_check(a, p["job_description"], tax),
                            auto_check(b, p["job_description"], tax)))

    items = [{"golden_id": m.golden_id, **i} for m in merged for i in m.review]
    sample = spot_check_sample(merged, args.spot_check, args.seed)
    by_gid = {m.golden_id: m for m in merged}
    posting_by_gid = {p["golden_id"]: p["job_description"] for p in picks}
    pool_n = sum(len(m.accepted_skills) + len(m.accepted_attrs) for m in merged)
    for gid, kind, key in sample:
        m = by_gid[gid]
        if kind == "skill":
            value = next(s for s in m.accepted_skills if s["skill_id"] == key)
            quote = value["raw_text"]
        else:
            value = m.accepted_attrs[key]
            quote = value.get(f"{key}_signal")
        items.append({"golden_id": gid, "kind": kind, "key": key, "reason": "spot-check",
                      "a": value, "b": value, "excerpt": excerpt(posting_by_gid[gid], quote),
                      "problems": [], "decision": "?"})

    meta = {
        "run_id": run_dir.name, "seed": args.seed,
        "provider_a": args.provider_a, "model_a": args.model_a,
        "provider_b": args.provider_b, "model_b": args.model_b,
        "extractor": EXTRACTOR_MODEL, "spot_n": len(sample), "spot_pool": pool_n,
    }
    (run_dir / "items.json").write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n")
    (run_dir / "review_queue.md").write_text(render_queue(run_dir.name, meta, items))
    (run_dir / "merged.json").write_text(json.dumps(
        {m.golden_id: {"accepted_skills": m.accepted_skills, "accepted_attrs": m.accepted_attrs,
                       "unmapped": m.unmapped} for m in merged}, indent=2, ensure_ascii=False) + "\n")

    summary = {
        **meta,
        "taxonomy_version": tax.version,
        "n_picked": len(picks), "n_labeled": len(merged), "failed": failed,
        "agreement": agreement(merged, usable),
        "accepted_skills": sum(len(m.accepted_skills) for m in merged),
        "accepted_attributes": sum(len(m.accepted_attrs) for m in merged),
        "review_items": Counter(i["reason"] for i in items),
        "spot_check": {"n": len(sample), "pool": pool_n, "seed": args.seed,
                       "sample": [list(s) for s in sample]},
        "signal_mismatches": [s for m in merged for s in m.signal_mismatches],
        "unmapped": sorted({u.get("label", "") for m in merged for u in m.unmapped}),
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=dict) + "\n")
    (run_dir / "summary.md").write_text(render_summary(summary))
    print(render_summary(summary))
    if failed:
        print("\nFAILED:\n" + "\n".join("  " + f for f in failed))
    print(f"\nReview queue: {run_dir / 'review_queue.md'} ({len(items)} items)")


def render_summary(s: dict, spot: dict | None = None) -> str:
    sk, ag = s["agreement"]["skills"], s["agreement"]
    def f(x):
        return "—" if x is None else f"{x:.3f}"
    lines = [
        f"# Labeling run {s['run_id']}", "",
        f"- labeler A: `{s['model_a']}` ({s['provider_a']}); labeler B: `{s['model_b']}` ({s['provider_b']})",
        f"- extractor (excluded as a labeler): `{s['extractor']}`; taxonomy v{s['taxonomy_version']}",
        f"- postings picked {s['n_picked']}, labeled by both {s['n_labeled']}, failed {len(s['failed'])}",
        "",
        "## Labeler agreement (A as reference)", "",
        f"- skills: precision {f(sk['precision'])}, recall {f(sk['recall'])}, F1 {f(sk['f1'])} "
        f"(tp {sk['tp']}, B-only {sk['fp']}, A-only {sk['fn']})",
        f"- requirement, on ids both gave: {f(ag['requirement_agreement'])}",
    ]
    for attr, v in ag["attributes"].items():
        lines.append(f"- {attr}: {f(v['rate'])} ({v['agreed']}/{v['n']})")
    lines += ["", "## Merge", "",
              f"- accepted on agreement: {s['accepted_skills']} skills, {s['accepted_attributes']} attributes",
              "- review queue: " + (", ".join(f"{n} {r}" for r, n in sorted(s["review_items"].items())) or "empty"),
              f"- spot-check: {s['spot_check']['n']} of {s['spot_check']['pool']} accepted labels, "
              f"seed {s['spot_check']['seed']}"]
    if s["signal_mismatches"]:
        lines += ["", "Agreed value, different quoted signal (A's kept):"] + \
                 [f"- {m}" for m in s["signal_mismatches"]]
    if s["unmapped"]:
        lines += ["", "No taxonomy entry fits (a taxonomy gap, never a Golden label):",
                  "- " + ", ".join(s["unmapped"])]
    if spot:
        lo, hi = spot["wilson_95"]
        lines += ["", "## Spot-check error rate (after review)", "",
                  f"- {spot['errors']} errors in {spot['n']} reviewed labels = {f(spot['rate'])}",
                  f"- 95% Wilson interval: {f(lo)} to {f(hi)}"]
        if spot["wrong"]:
            lines += ["", "Wrong labels found:"] + [f"- {w}" for w in spot["wrong"]]
    return "\n".join(lines) + "\n"


def cmd_apply(args):
    run_dir = RUNS / args.run
    items = json.loads((run_dir / "items.json").read_text())
    merged = json.loads((run_dir / "merged.json").read_text())
    picks = {p["golden_id"]: p for p in json.loads((run_dir / "picks.json").read_text())}
    summary = json.loads((run_dir / "summary.json").read_text())
    decisions = dict(parse_queue((run_dir / "review_queue.md").read_text()))

    missing = [n for n in range(1, len(items) + 1) if decisions.get(n, "?") in ("?", "")]
    if missing:
        raise SystemExit(f"{len(missing)} of {len(items)} items still say `?` "
                         f"(first: {missing[:8]}). Decide them, then run apply again.")

    skills = {gid: {s["skill_id"]: s for s in m["accepted_skills"]} for gid, m in merged.items()}
    attrs = {gid: dict(m["accepted_attrs"]) for gid, m in merged.items()}
    adjudicated: dict[str, set] = {gid: set() for gid in merged}
    spot_errors, spot_wrong, spot_n = 0, [], 0

    for n, item in enumerate(items, 1):
        gid, decision = item["golden_id"], decisions[n]
        try:
            add, group = apply_decision(item, decision)
        except (ValueError, json.JSONDecodeError) as e:
            raise SystemExit(f"item {n} ({gid} {item['kind']} {item['key']}): {e}")
        if item["kind"] == "run":
            skills.pop(gid, None)
            attrs.pop(gid, None)
            continue
        # A spot-check answered `ok` confirms a label; it does not adjudicate one. Only a
        # spot-check that changed something counts as both an error and an adjudication.
        confirmed = False
        if item["reason"] == "spot-check":
            spot_n += 1
            if decision.strip().strip("`").lower() == "ok":
                confirmed = True
            else:
                spot_errors += 1
                spot_wrong.append(f"{gid} {item['kind']} `{item['key']}` -> {decision}")
        if item["kind"] == "skill":
            for sid in item["key"].split("|"):
                skills[gid].pop(sid, None)
            for s in add:
                skills[gid][s["skill_id"]] = s
            if not confirmed:
                adjudicated[gid].add(f"skill:{item['key']}")
        else:
            attrs[gid][item["key"]] = group
            if not confirmed:
                adjudicated[gid].add(item["key"])

    labeled_by = [summary["model_a"], summary["model_b"]]
    spot_by_gid: dict[str, bool] = {}
    for gid, _, _ in (tuple(s) for s in summary["spot_check"]["sample"]):
        spot_by_gid[gid] = True

    written = []
    for gid in sorted(skills):
        golden = final_golden({**picks[gid], "id": gid}, list(skills[gid].values()),
                              attrs.get(gid, {}), labeled_by, sorted(adjudicated[gid]),
                              spot_by_gid.get(gid, False))
        path = GOLDENS / f"{gid}.json"
        if not args.dry_run:
            path.write_text(json.dumps(golden, indent=2, ensure_ascii=False) + "\n")
        written.append(f"{gid}  {len(golden['expected'])} skills  "
                       f"{len(golden['adjudicated'])} adjudicated"
                       f"{'  spot-checked' if golden['spot_checked'] else ''}")

    lo, hi = wilson(spot_errors, spot_n)
    spot = {"n": spot_n, "errors": spot_errors, "rate": spot_errors / spot_n if spot_n else None,
            "wilson_95": [lo, hi], "wrong": spot_wrong}
    summary["spot_check"] |= spot
    if not args.dry_run:
        (run_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
        (run_dir / "summary.md").write_text(render_summary(summary, spot))
    print(("(dry run) " if args.dry_run else "") + f"{len(written)} Goldens:")
    print("\n".join("  " + w for w in written))
    print()
    print(render_summary(summary, spot).split("## Spot-check")[-1].strip())
    if not args.dry_run:
        print(f"\nWritten to {GOLDENS}. The held-out eval is a separate, release-point step: "
              f"uv run python scripts/run_eval.py --split heldout --i-am-releasing")


def kv(text: str) -> tuple[str, int]:
    key, _, n = text.partition("=")
    if not n.isdigit():
        raise argparse.ArgumentTypeError(f"expected NAME=N, got {text!r}")
    return key, int(n)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    lab = sub.add_parser("label", help="pick, label with A and B, check, merge, write the review queue")
    lab.add_argument("--count", type=int, default=24, help="postings to label (default 24)")
    lab.add_argument("--seed", type=int, default=SEED, help="seeds the picks and the spot-check sample")
    lab.add_argument("--remote-eu", type=int, default=2,
                     help="at least N 'Remote (EU)' postings; their extraction is unmeasured (default 2)")
    lab.add_argument("--german", type=int, default=6, help="at least N German-language postings (default 6)")
    lab.add_argument("--source", type=kv, action="append", default=[], metavar="NAME=N",
                     help="at least N postings from that feed, repeatable")
    lab.add_argument("--seniority", type=kv, action="append", default=[], metavar="LEVEL=N",
                     help="at least N at that stored level (junior/mid/senior/none), repeatable")
    lab.add_argument("--provider-a", default="anthropic", choices=sorted(PROVIDERS))
    lab.add_argument("--model-a", default=DEFAULT_MODEL_A, help=f"labeler A (default {DEFAULT_MODEL_A})")
    lab.add_argument("--provider-b", default="openai", choices=sorted(PROVIDERS))
    lab.add_argument("--model-b", default=DEFAULT_MODEL_B, help=f"labeler B (default {DEFAULT_MODEL_B})")
    lab.add_argument("--spot-check", type=int, default=SPOT_CHECK_N,
                     help=f"accepted labels to sample for review (default {SPOT_CHECK_N})")
    lab.add_argument("--run", help="re-merge an existing run from its cached labeler outputs")
    lab.add_argument("--force", action="store_true",
                     help="with --run: rewrite review_queue.md even though it holds decisions")
    lab.add_argument("--dry-run", action="store_true", help="list the picks and stop")
    lab.set_defaults(fn=cmd_label)

    app = sub.add_parser("apply", help="apply the decisions in review_queue.md and write the Goldens")
    app.add_argument("--run", required=True)
    app.add_argument("--dry-run", action="store_true")
    app.set_defaults(fn=cmd_apply)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")  # existing environment variables win over .env
    if os.environ.get("HIRING_RADAR_DB"):
        ng.DB = Path(os.environ["HIRING_RADAR_DB"])
    main()
