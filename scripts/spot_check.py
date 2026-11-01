"""The human spot-check of a model-labelled Golden batch (HIR-92).

Does: draw a seeded, stratified, label-level sample from the Goldens no person has read
yet; render each sampled label with the posting context a person needs to judge it in
under 30 seconds; parse the compact per-batch reply; report the error rate with a 95%
Wilson interval; and stamp `spot_checked_by_human` provenance on the labels a person
actually answered.

Does NOT: call a model (every input is already on disk), label anything itself, show the
reviewer which model said what or how an item was adjudicated, touch the dev split, or run
an eval. The reasons and the "watch for" line on a rendered item are written by the agent
preparing the packet, not by this script: it supplies the mechanical context (the located
quote, its bullets, its heading and that heading's kind) and leaves the judgment lines for
a reader to fill.

Invariants:
- The pool is every label in the batch that no person has read: a skill not in
  `adjudicated`, an attribute neither in `adjudicated` nor covered by a true
  `seniority_reviewed` / `attrs_reviewed`. A label a model "spot-checked" is unread and
  stays eligible, which is the whole point of this ticket.
- The draw depends only on (pool, counts, seed), and the pool is sorted before sampling,
  so the same seed draws the same sample on any machine.
- `apply` refuses a sample with an unanswered item, and only ever adds provenance: it
  never rewrites a label's value. A `wrong` verdict is recorded as a correction to decide
  on, not applied.
"""

import argparse
import importlib.util
import json
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.taxonomy import Taxonomy  # noqa: E402

# agent_label.py owns the labeling workflow this is the human step of; its Wilson interval
# is the one the run reported with, and the two must not fork.
_spec = importlib.util.spec_from_file_location("agent_label", ROOT / "scripts" / "agent_label.py")
agent_label = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agent_label)
wilson = agent_label.wilson

GOLDENS = ROOT / "evals" / "goldens"
ATTRS = ("seniority", "german", "degree")

# The fields that make up one attribute label, so a rendered item shows the whole thing.
ATTR_FIELDS = {
    "seniority": ("seniority", "seniority_basis", "seniority_signal"),
    "german": ("german", "german_basis", "german_signal"),
    "degree": ("degree", "degree_requirement", "degree_or_equivalent", "degree_signal"),
}
# A true flag means a person already read that attribute, so it is not in the pool.
REVIEWED_FLAG = {"seniority": "seniority_reviewed", "german": "attrs_reviewed",
                 "degree": "attrs_reviewed"}

# What a reviewer may answer for each kind of item. Free text after `wrong:` is kept
# verbatim for an attribute, where the correction can be a value, a basis or both.
SKILL_CORRECTIONS = ("required", "nice_to_have", "drop")

# Enough aliases to recognise the skill, not the taxonomy's whole synonym list.
ALIASES_SHOWN = 4

# Words that would carry each attribute if the posting mentioned it at all. Shown for a
# null label, where the question is "did the models miss it", and there is no quote to bold.
TRIGGERS = {
    "seniority": ("junior", "senior", "lead", "principal", "staff", "head of", "intern",
                  "working student", "graduate", "entry-level", "years of experience",
                  "years' experience", "jahre", "berufserfahrung"),
    "german": ("german", "deutsch", "sprache", "muttersprache", "c1", "c2", "b2"),
    "degree": ("degree", "bachelor", "master", "phd", "msc", "bsc", "doctorate",
               "abschluss", "studium", "studiert", "hochschul", "universit"),
}

HEADING_KINDS = (
    # (kind, substrings that identify it) - checked in order, so "nice to have" beats the
    # generic requirements words when a heading carries both.
    ("optional", ("nice to have", "nice-to-have", "nice to haves", "bonus", "preferred",
                  "plus", "advantage", "wünschenswert", "von vorteil", "optional",
                  "desirable", "ideally")),
    ("tech stack", ("tech stack", "our stack", "technologies", "toolchain", "tooling",
                    "technologien", "you will work with")),
    ("responsibilities", ("responsibilit", "what you will do", "what you'll do", "your role",
                          "your tasks", "deine aufgaben", "aufgaben", "the role", "day to day",
                          "day-to-day", "deine rolle")),
    ("requirements", ("requirement", "qualification", "what we are looking for",
                      "what we're looking for", "you bring", "your profile", "about you",
                      "dein profil", "das bringst du", "must have", "must-have", "skills",
                      "experience", "we expect", "who you are")),
)


def classify_heading(heading: str) -> str:
    """Which kind of section a heading names: the thing requirement rule 1 turns on.

    "intro prose" is the honest answer for no heading and for one that names none of these,
    because that is also where a technology mentioned in the company blurb sits.
    """
    h = (heading or "").strip().lower()
    if not h:
        return "intro prose"
    for kind, needles in HEADING_KINDS:
        if any(n in h for n in needles):
            return kind
    return "intro prose"


# --- the pool ---------------------------------------------------------------------

def batch_goldens(goldens_dir: Path = GOLDENS) -> list[dict]:
    """The model-labelled held-out Goldens, by what the files say rather than a list of ids.

    `split == "heldout"` and a non-empty `labeled_by`: that is HIR-70's output and excludes
    both the dev split and golden_021-024, which predate the process and were hand-labeled.
    """
    out = []
    for path in sorted(goldens_dir.glob("golden_*.json")):
        d = json.loads(path.read_text())
        if d.get("split") == "heldout" and d.get("labeled_by") and not d.get("draft"):
            out.append(d)
    return out


def read_by_person(golden: dict) -> set[str]:
    """The keys in this Golden a person has already read, in `adjudicated`'s own format."""
    done = set(golden.get("adjudicated", []))
    for attr in ATTRS:
        if golden.get(REVIEWED_FLAG[attr]):
            done.add(attr)
    return done


def pool(goldens: list[dict]) -> list[tuple[str, str, str]]:
    """Every unread label as (golden_id, kind, key), sorted.

    A null attribute is in the pool: "the models saw no German requirement here" is a label
    with the same standing as any other, and the expensive kind to get wrong.
    """
    items = []
    for g in goldens:
        done = read_by_person(g)
        for e in g["expected"]:
            if f"skill:{e['skill_id']}" not in done:
                items.append((g["id"], "skill", e["skill_id"]))
        for attr in ATTRS:
            if attr not in done:
                items.append((g["id"], "attribute", attr))
    return sorted(items)


def draw(items: list[tuple[str, str, str]], n_skills: int, n_per_attr: int,
         seed: int) -> list[tuple[str, str, str]]:
    """A seeded sample: `n_skills` skills, plus `n_per_attr` of each attribute.

    Stratified rather than drawn flat, because attributes are ~1 label in 6 and a flat draw
    of 30 can miss a whole attribute. Each stratum is sampled from a sorted list with its
    own `Random(seed)`, so adding a stratum cannot shift the ones beside it.
    """
    out = list(random.Random(seed).sample(
        sorted(i for i in items if i[1] == "skill"),
        min(n_skills, sum(1 for i in items if i[1] == "skill"))))
    for attr in ATTRS:
        stratum = sorted(i for i in items if i[1] == "attribute" and i[2] == attr)
        out += random.Random(seed).sample(stratum, min(n_per_attr, len(stratum)))
    return sorted(out)


# --- locating a label in its posting ----------------------------------------------

def locate(posting: str, quote: str | None) -> re.Match | None:
    """The quote in the posting, matched across whatever whitespace wrapping introduced."""
    if not quote:
        return None
    pattern = r"\s+".join(re.escape(w) for w in str(quote).split())
    return re.search(pattern, posting, flags=re.I)


BULLET_CHARS = ("-", "*", "•", "·", "–", "", "‣", "")
MAX_SEGMENT = 300      # longer than this and a "bullet" is really a flattened paragraph
WINDOW = 200           # characters each side of the quote when that happens


def is_bullet(line: str) -> bool:
    """Whether a line is a list item rather than a heading.

    Tested on the raw line, before any `*` stripping: a markdown bold heading
    (`**Deine Benefits**`) and a `* bullet` both start with `*`, and only the second is a
    list item. What tells them apart is whether a space follows the marker.
    """
    s = line.strip()
    if not s:
        return False
    if s in BULLET_CHARS:
        return True
    return any(s.startswith(c + " ") for c in BULLET_CHARS)


def looks_like_heading(line: str) -> bool:
    """A short, non-bullet line that introduces a section.

    A line ending in a full stop is prose, not a heading. Headings in these postings end in
    a colon or nothing at all, and the exclusion earns its keep: golden_038's "These are
    meant to be indicative, not hard requirements." would otherwise be read as a heading
    and - on the word "requirements" - classified as the opposite of what it says.
    """
    s = line.strip().strip("*#").strip()
    return bool(s) and not is_bullet(line) and len(s) <= 80 and not s.endswith((".", "!", "?"))


# A colon-terminated phrase inside running text ("Das bringst Du mit:", "Your profile:").
# The only heading a flattened posting has, where the whole description is one line.
INLINE_HEADING = re.compile(r"([A-Z\u00c4\u00d6\u00dc][^.!?:\n]{2,60}):\s")


def trim_heading(text: str, width: int = 40) -> str:
    """A heading found inside running text, shortened from the left.

    A flattened posting has no boundary before its heading - "...arbeitest eng mit
    Anwendungs- und Datenteams zusammen Das bringst Du mit:" is one unpunctuated run - so
    the phrase picked up carries the tail of the sentence before it. The leading ellipsis
    says the heading is a fragment instead of pretending it is the whole line.
    """
    words = text.split()
    out = text
    while len(out) > width and len(words) > 2:
        words = words[1:]
        out = "..." + " ".join(words)
    return out


def section_heading(posting: str, at: int) -> str:
    """The heading governing the character at `at`, or "".

    Takes whichever candidate starts nearest above the quote: a heading-shaped line, or a
    colon-terminated phrase inside running text. One rule for both posting shapes in this
    batch - line-per-bullet, and the flattened HTML list that arrives as a single 4000-
    character line, where a line scan finds no heading at all and would report the section
    as intro prose.

    Deliberately not `agent_label.heading_above`: that one strips `*` before testing for a
    bullet, so a `* ...` list item reads as a heading. Its callers are a model's excerpt;
    this one's is a person deciding whether a requirement is a requirement.
    """
    before = posting[:at]
    lines = before.splitlines()
    # The slice cuts mid-line, and that partial line is the start of the quote's own bullet,
    # not a heading - it is short enough to pass for one, which is how a requirements bullet
    # came to be reported as its own section.
    if lines and not before.endswith(("\n", "\r")):
        lines = lines[:-1]
    best, text, pos = -1, "", 0
    for line in lines:
        if looks_like_heading(line):
            best, text = pos, line.strip().strip("*#").strip()
        pos += len(line) + 1
    for m in INLINE_HEADING.finditer(before):
        if m.start() > best:
            best, text = m.start(), trim_heading(m.group(1).strip())
    return text


def segments(posting: str) -> list[tuple[int, int]]:
    """The posting as (start, end) spans, one per bullet or paragraph.

    A marker on its own line is joined to the text under it, because two of these postings
    put every `-` on its own line and a reviewer shown three lines would be shown two
    dashes and one bullet.
    """
    lines, spans, pos = posting.splitlines(), [], 0
    raw = []
    for line in lines:
        raw.append((pos, pos + len(line), line))
        pos += len(line) + 1
    out: list[tuple[int, int]] = []
    pending: tuple[int, int] | None = None
    for s, e, line in raw:
        if not line.strip():
            continue
        if line.strip() in BULLET_CHARS:
            pending = (s, e) if pending is None else pending
            continue
        if pending:
            out.append((pending[0], e))
            pending = None
        else:
            out.append((s, e))
    return out or [(0, len(posting))]


def context_block(posting: str, match: re.Match, around: int = 1) -> list[str]:
    """The quote in its neighbourhood, as lines to print, the quote in `**bold**`.

    Two shapes. When the bullet holding the quote is a normal length, show it with a
    neighbour either side, so the section reads. When it is a flattened paragraph, show a
    character window instead - a 4000-character "bullet" is not context, it is the posting.
    """
    spans = segments(posting)
    here = next((i for i, (s, e) in enumerate(spans) if s <= match.start() < e), None)
    if here is not None and spans[here][1] - spans[here][0] <= MAX_SEGMENT:
        lo, hi = max(0, here - around), min(len(spans), here + around + 1)
        out = []
        for i in range(lo, hi):
            s, e = spans[i]
            out.append(_bold_in(posting, s, e, match) if i == here
                       else " ".join(posting[s:e].split()))
        return out
    a = max(0, match.start() - WINDOW)
    b = min(len(posting), match.end() + WINDOW)
    body = _bold_in(posting, a, b, match)
    return [("..." if a > 0 else "") + body + ("..." if b < len(posting) else "")]


def _bold_in(posting: str, start: int, end: int, match: re.Match) -> str:
    """The span `start:end`, whitespace-collapsed, with the match wrapped in `**`."""
    pre = " ".join(posting[start:match.start()].split())
    hit = " ".join(posting[match.start():match.end()].split())
    post = " ".join(posting[match.end():end].split())
    out = f"**{hit}**"
    if pre:
        out = pre + ("" if pre.endswith(("(", "[", "/")) else " ") + out
    if post:
        out += ("" if post[0] in ",.;:)]/%" else " ") + post
    return out


def other_headings(posting: str, skill: object, determining: re.Match | None,
                   limit: int = 3) -> list[str]:
    """Headings of the posting's *other* mentions of this skill, nearest name first.

    Rule: one criterion per skill, and `raw_text` quotes the mention that determined the
    label. A reviewer who cannot see the other mentions cannot tell a correct collapse from
    a missed `required`.
    """
    here = section_heading(posting, determining.start()) if determining else ""
    seen, out = {here}, []
    for name in [skill.display, *skill.aliases]:
        for m in re.finditer(r"\b" + re.escape(name) + r"\b", posting, flags=re.I):
            if determining and determining.start() <= m.start() < determining.end():
                continue
            h = section_heading(posting, m.start())
            if h and h not in seen:
                seen.add(h)
                out.append(h)
    return out[:limit]


def trigger_hits(posting: str, attr: str, width: int = 90, limit: int = 8) -> list[str]:
    """Each place one of the attribute's trigger words appears, as a short window.

    This is what stands in for a quote on a null label: there is nothing to bold, so the
    item has to show the reviewer the places the models decided *against*. A window rather
    than the whole bullet, because the flattened postings have no bullets to speak of.
    """
    hits, seen = [], set()
    for word in TRIGGERS[attr]:
        for m in re.finditer(re.escape(word), posting, flags=re.I):
            a = max(0, m.start() - width // 2)
            b = min(len(posting), m.end() + width)
            s = " ".join(posting[a:b].split())
            key = s[:40].lower()
            if key in seen:
                continue
            seen.add(key)
            hits.append(("..." if a > 0 else "") + s + ("..." if b < len(posting) else ""))
    return hits[:limit]


# --- rendering ---------------------------------------------------------------------

TODO = "<<fill in>>"


def skill_item(golden: dict, skill_id: str, tax: Taxonomy) -> dict:
    """Everything mechanical about one sampled skill label."""
    e = next(x for x in golden["expected"] if x["skill_id"] == skill_id)
    posting = golden["job_description"]
    m = locate(posting, e["raw_text"])
    skill = tax.skills.get(skill_id)
    if skill:
        shown_aliases = list(skill.aliases)[:ALIASES_SHOWN]
        names = "; ".join([skill.display, *shown_aliases])
        if len(skill.aliases) > ALIASES_SHOWN:
            names += f"; +{len(skill.aliases) - ALIASES_SHOWN} more"
    else:
        names = "(not in the taxonomy)"
    ctx = {"heading": "", "kind": "intro prose", "lines": [], "located": m is not None}
    if m:
        ctx["lines"] = context_block(posting, m)
        ctx["heading"] = section_heading(posting, m.start())
        ctx["kind"] = classify_heading(ctx["heading"])
    return {"golden_id": golden["id"], "kind": "skill", "key": skill_id,
            "label": f"{skill_id} ({names}) · {e['requirement']}",
            "value": {k: e[k] for k in ("skill_id", "requirement", "raw_text")},
            "context": ctx,
            "also_under": other_headings(posting, skill, m) if skill else [],
            "corrections": list(SKILL_CORRECTIONS)}


def attribute_item(golden: dict, attr: str) -> dict:
    """Everything mechanical about one sampled attribute label, null included."""
    posting = golden["job_description"]
    value = {f: golden.get(f) for f in ATTR_FIELDS[attr]}
    signal = golden.get(f"{attr}_signal")
    m = locate(posting, signal)
    ctx = {"heading": "", "kind": "intro prose", "lines": [], "located": m is not None,
           "triggers": []}
    if m:
        ctx["lines"] = context_block(posting, m)
        ctx["heading"] = section_heading(posting, m.start())
        ctx["kind"] = classify_heading(ctx["heading"])
    if golden.get(attr) is None:
        ctx["triggers"] = trigger_hits(posting, attr)
    shown = ", ".join(f"{k}={json.dumps(v)}" for k, v in value.items() if k != f"{attr}_signal")
    return {"golden_id": golden["id"], "kind": "attribute", "key": attr,
            "label": f"{attr}: {shown}", "value": value, "context": ctx,
            "also_under": [], "corrections": []}


def render_item(n: int, total: int, item: dict) -> str:
    """One item in the format HIR-92 specifies, with the judgment lines left to fill."""
    out = [f"## {n} of {total} — {item['golden_id']} · {item['kind']}",
           f"LABEL: {item['label']}", ""]
    ctx = item["context"]
    if ctx["lines"]:
        for line in ctx["lines"]:
            out.append("  " + line.strip())
        head = f'"{ctx["heading"]}"' if ctx["heading"] else "no heading above it"
        out.append(f'  (section: {head} — {ctx["kind"]})')
    elif ctx["triggers"]:
        out.append(f"  the label is null. Every line mentioning {item['key']}'s trigger words:")
        out += [f"  • {t}" for t in ctx["triggers"]]
    elif item["kind"] == "attribute" and item["value"].get(item["key"]) is None:
        out.append(f"  the label is null, and the posting never mentions "
                   f"{item['key']}'s trigger words.")
    else:
        out.append("  (the quoted phrase was not found in the posting — check it by hand)")
    if item["also_under"]:
        out.append(f"  also under: {', '.join(item['also_under'])}")
    out.append("")
    for question in (("asked of the candidate?", "required or nice-to-have?")
                     if item["kind"] == "skill"
                     else ("value right?", "basis right?", "signal supports it?")):
        out.append(f"  ✓ {question:<26} {TODO}")
    out += ["", f"  watch for: {TODO}", "",
            f"→ ok, or: wrong: <{' | '.join(item['corrections'])}>" if item["corrections"]
            else "→ ok, or: wrong: <the value it should be>", ""]
    return "\n".join(out)


def render_packet(meta: dict, items: list[dict], per_batch: int = 10) -> str:
    """The whole packet: batches of ten, numbered across the sample."""
    out = [f"# Human spot-check — {meta['run_id']}", "",
           f"{meta['n']} labels from {meta['n_goldens']} Goldens, seed {meta['seed']}, "
           f"drawn from a pool of {meta['pool']} labels no person had read.",
           "",
           "Answer per batch: `all ok`, or name the ones that are wrong "
           "(`3 wrong: nice_to_have`).", ""]
    total = len(items)
    for start in range(0, total, per_batch):
        out.append(f"---\n\n# Batch {start // per_batch + 1} "
                   f"(items {start + 1}–{min(start + per_batch, total)})\n")
        for i, item in enumerate(items[start:start + per_batch], start=start + 1):
            out.append(render_item(i, total, item))
    return "\n".join(out)


# --- the reply ---------------------------------------------------------------------

def parse_batch_reply(text: str, numbers: list[int]) -> dict[int, str]:
    """A compact reply over one batch as {item number: verdict}.

    `all ok` answers every item in the batch; otherwise every item named is wrong with the
    given correction and the rest are ok. Written as the one parser in this file with a
    test per shape, because a misread reply silently moves the error rate.
    """
    s = text.strip()
    if not s:
        raise ValueError("empty reply")
    if re.fullmatch(r"all\s+ok\.?", s, flags=re.I):
        return {n: "ok" for n in numbers}
    wrong: dict[int, str] = {}
    for part in re.split(r"[;\n]+", s):
        part = part.strip().strip(".")
        if not part:
            continue
        m = re.match(r"^(\d+(?:\s*(?:,|and|&)\s*\d+)*)\s+wrong\s*:?\s*(.*)$", part, flags=re.I)
        if not m:
            raise ValueError(f"cannot read {part!r}: expected `all ok` or `<n> wrong: <value>`")
        correction = m.group(2).strip() or "unspecified"
        for num in re.findall(r"\d+", m.group(1)):
            n = int(num)
            if n not in numbers:
                raise ValueError(f"item {n} is not in this batch ({numbers[0]}-{numbers[-1]})")
            wrong[n] = f"wrong: {correction}"
    return {n: wrong.get(n, "ok") for n in numbers}


def tally(items: list[dict], verdicts: dict[str, str]) -> dict:
    """The error rate with its 95% Wilson interval, overall and per kind."""
    def rate(subset):
        n = len(subset)
        k = sum(1 for it in subset if not verdicts[key_of(it)].startswith("ok"))
        low, high = wilson(k, n)
        return {"errors": k, "n": n, "rate": (k / n) if n else None,
                "wilson95": [low, high]}
    out = {"overall": rate(items)}
    for kind in ("skill", "attribute"):
        subset = [it for it in items if it["kind"] == kind]
        if subset:
            out[kind] = rate(subset)
    return out


def key_of(item: dict) -> str:
    """How an item is addressed in `verdicts` and in a Golden's provenance list."""
    return (f"{item['golden_id']}:skill:{item['key']}" if item["kind"] == "skill"
            else f"{item['golden_id']}:{item['key']}")


def provenance_key(item: dict) -> str:
    """The key inside its own Golden, in `adjudicated`'s format."""
    return f"skill:{item['key']}" if item["kind"] == "skill" else item["key"]


def stamp(golden: dict, keys: list[str]) -> dict:
    """Add `spot_checked_by_human` to a Golden, without touching any label's value.

    A list of item keys beside `adjudicated`, not a field inside each criterion: DECISIONS
    2026-10-29 settled that provenance in this repo is a whole-Golden list of keys, and an
    extra key inside an `expected` entry would be the first exception.
    """
    out = dict(golden)
    have = list(out.get("spot_checked_by_human", []))
    out["spot_checked_by_human"] = sorted(set(have) | set(keys))
    return out


# --- commands ----------------------------------------------------------------------

def cmd_sample(args):
    tax = Taxonomy.load()
    goldens = batch_goldens()
    by_id = {g["id"]: g for g in goldens}
    items_pool = pool(goldens)
    drawn = draw(items_pool, args.skills, args.per_attr, args.seed)
    items = [skill_item(by_id[gid], key, tax) if kind == "skill"
             else attribute_item(by_id[gid], key)
             for gid, kind, key in drawn]
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_spotcheck")
    out_dir = ROOT / "evals" / "labeling" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {"run_id": run_id, "seed": args.seed, "n": len(items),
            "n_goldens": len(goldens), "pool": len(items_pool),
            "pool_skills": sum(1 for i in items_pool if i[1] == "skill"),
            "pool_attributes": sum(1 for i in items_pool if i[1] == "attribute"),
            "goldens": [g["id"] for g in goldens],
            "drawn_from": "held-out Goldens with a model `labeled_by`, "
                          "minus every label a person had already read"}
    (out_dir / "sample.json").write_text(
        json.dumps({"meta": meta, "items": items}, indent=1, ensure_ascii=False) + "\n")
    (out_dir / "packet.md").write_text(render_packet(meta, items) + "\n")
    print(f"{len(items)} items of {len(items_pool)} eligible labels "
          f"({meta['pool_skills']} skills, {meta['pool_attributes']} attributes), seed {args.seed}")
    print(f"  {out_dir / 'sample.json'}")
    print(f"  {out_dir / 'packet.md'}")


def cmd_apply(args):
    run_dir = Path(args.run_dir)
    sample = json.loads((run_dir / "sample.json").read_text())
    items = sample["items"]
    verdicts = json.loads((run_dir / "answers.json").read_text())
    missing = [key_of(it) for it in items if key_of(it) not in verdicts]
    if missing:
        sys.exit(f"{len(missing)} item(s) unanswered, e.g. {missing[0]}")
    stats = tally(items, verdicts)
    by_golden: dict[str, list[str]] = {}
    for it in items:
        if verdicts[key_of(it)].startswith("ok"):
            by_golden.setdefault(it["golden_id"], []).append(provenance_key(it))
    if not args.dry_run:
        for gid, keys in by_golden.items():
            path = GOLDENS / f"{gid}.json"
            path.write_text(json.dumps(stamp(json.loads(path.read_text()), keys),
                                       indent=1, ensure_ascii=False) + "\n")
    wrong = {key_of(it): verdicts[key_of(it)] for it in items
             if not verdicts[key_of(it)].startswith("ok")}
    summary = {"meta": sample["meta"], "stats": stats, "verdicts": verdicts,
               "corrections_to_decide": wrong,
               "stamped": {g: sorted(k) for g, k in sorted(by_golden.items())}}
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n")
    o = stats["overall"]
    print(f"{o['errors']} errors of {o['n']}, "
          f"Wilson 95% [{o['wilson95'][0]:.3f}, {o['wilson95'][1]:.3f}]"
          + ("  (dry run: no Golden written)" if args.dry_run else ""))
    for kind in ("skill", "attribute"):
        if kind in stats:
            s = stats[kind]
            print(f"  {kind}: {s['errors']} of {s['n']}")
    for k, v in wrong.items():
        print(f"  to decide: {k} — {v}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample", help="draw the seeded sample and render the packet")
    s.add_argument("--skills", type=int, default=24)
    s.add_argument("--per-attr", type=int, default=2,
                   help="per attribute (seniority, German, degree)")
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--run-id")
    s.set_defaults(func=cmd_sample)
    a = sub.add_parser("apply", help="score answers.json, stamp provenance, write summary")
    a.add_argument("run_dir")
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_apply)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
