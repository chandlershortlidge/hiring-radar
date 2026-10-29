#!/usr/bin/env python3
"""Label golden_021-024 for production experience with two independent models (HIR-69).

A one-off, not a pipeline. HIR-70's `scripts/agent_label.py` is the general tool; it cannot
scope to one attribute and carries no production field, and extending it is HIR-70's work.
This script borrows that pipeline's independence rules and nothing else.

Does: send one prompt (independence framing + the DECISIONS 2026-10-28 rule bullets +
output format + the posting) to two models from different families, cache every raw
response, auto-check each answer deterministically, and print a side-by-side of agreed
items, disagreements and auto-check failures.

Does NOT: read or write any Golden's labels, read `app/extract.py` (no PRINCIPLES, no
extractor output, no import), read predictions, or decide anything. Agreement here is a
proposal for a person; nothing reaches `evals/goldens/`.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLDENS = ROOT / "evals" / "goldens"
RUNS = ROOT / "evals" / "labeling"
DECISIONS = ROOT / "DECISIONS.md"

GOLDEN_IDS = ("golden_021", "golden_022", "golden_023", "golden_024")
ENTRY_HEADING = "## 2026-10-28 — Production experience is a fourth per-job attribute"

DEFAULT_MODEL_A = "claude-opus-5-5"
DEFAULT_MODEL_B = "gpt-6.1-sol"
MAX_TOKENS = 4096

# Deliberately not imported from app.extract: this script stays free of that module. Keep
# in step with its DEFAULT_MODEL, which reads the same variable.
EXTRACTOR_MODEL = os.environ.get("HIRING_RADAR_MODEL", "claude-sonnet-5-5")

CLASSES = (None, "required", "nice_to_have")


# --- the prompt -------------------------------------------------------------------

# Adapted from evals/LABELER_PROMPT.md on
# chandlershortlidge/hir-70-held-out-goldens-via-independent-agent-labeling-2-blind.
# That file is not on this branch, so its rules are restated here rather than read.
INDEPENDENCE = """\
You are labeling a job posting for an evaluation set. Your label is part of the answer key
a job-description extraction system is graded against, so be exact rather than generous.

Independence rules this task runs under:
- You get these instructions, the rules below, and one posting. Nothing else: not the
  extraction system's own prompt, not its output, not any other posting's labels.
- You are not the model being measured, and you are labeling blind: a second labeler from
  a different model family answers the same posting without seeing your answer. Where you
  two agree, the label is proposed to a person; where you differ, a person decides.
- Follow the rules below exactly. Where they are silent, take the most literal reading of
  the posting and say so in `why`.
- Label this posting only from its own text. Do not assume any particular answer is more
  likely, and do not try to spread answers across the classes.
"""

OUTPUT_FORMAT = """\
Return one JSON object and nothing else:

```json
{
  "production": "required" | "nice_to_have" | null,
  "production_signal": "<verbatim clause from the posting>" | null,
  "why": "one line, naming the rule that decided it",
  "uncertain": true | false
}
```

Output rules:

- `production` is `"required"`, `"nice_to_have"`, or `null`. **`null` means JSON `null`**,
  the bare literal — not the string `"null"`, not `"none"`, not `""`. A string is a label
  and will be read as one. `null` means the posting does not ask the candidate for
  production work at all.
- `production_signal` must be copied **character for character** from the posting, as one
  contiguous substring: no paraphrase, no normalised punctuation, no two clauses joined.
  Quote the clause that carries the demand, not the paragraph around it. Keep the original
  language — a German posting gets a German signal. A signal that is not found in the
  posting verbatim makes the whole label unusable.
- When `production` is `null`, `production_signal` is `null`. When `production` is set,
  `production_signal` must quote the text it rests on.
- When the posting carries several candidate clauses, quote the single clause the class
  rests on.
- `uncertain` is `true` when you are not sure, so a person reviews it instead of it being
  accepted on agreement. Flagging is free and costs only a review; guessing silently
  corrupts the answer key.
"""


def rule_bullets(decisions_md: str) -> str:
    """The 2026-10-28 entry's definition and rule bullets, verbatim.

    The entry's other paragraphs are about the schema, the migration, the dashboard filters
    and why the attribute matters - none of them decide a label, so they are left out.
    """
    i = decisions_md.index(ENTRY_HEADING)
    entry = decisions_md[i:decisions_md.index("\n## ", i + 10)]
    lines = entry.splitlines()
    # the definition: the paragraph under the heading, up to the first blank line
    head, n = [], 1
    while n < len(lines) and not lines[n].strip():
        n += 1
    while n < len(lines) and lines[n].strip():
        head.append(lines[n])
        n += 1
    # the rule bullets: the first "- " list and its continuation lines
    bullets, started = [], False
    for line in lines[n:]:
        if line.startswith("- "):
            started, _ = True, bullets.append(line)
        elif started and line.startswith("  "):
            bullets.append(line)
        elif started and not line.strip():
            bullets.append("")
        elif started:
            break
    while bullets and not bullets[-1].strip():
        bullets.pop()
    if not head or not bullets:
        raise SystemExit("could not find the 2026-10-28 definition and rule bullets in DECISIONS.md")
    return "\n".join(head) + "\n\n" + "\n".join(bullets)


def build_prompt(bullets: str) -> str:
    return (f"{INDEPENDENCE}\n"
            f"<rules>\n"
            f"The question this label answers, and the rules that decide it, verbatim from the\n"
            f"project's decisions log (entry 2026-10-28). `not mentioned` in these rules is the\n"
            f"JSON `null` of the output format.\n\n"
            f"{bullets}\n"
            f"</rules>\n\n"
            f"{OUTPUT_FORMAT}")


# --- deterministic checks ----------------------------------------------------------

def norm_ws(text: str) -> str:
    """Whitespace-normalised, for the verbatim check. Local on purpose: app.extract is out
    of bounds for this script, so this does not share its _norm."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


FOLD = {"‘": "'", "’": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "−": "-", " ": " "}


def fold(text: str) -> str:
    """Punctuation folded as well as whitespace. A quote that matches only after folding is
    reported separately: it is the labeler's transcription, not the posting's wording."""
    return norm_ws("".join(FOLD.get(c, c) for c in text))


def quoted(signal, posting: str) -> str:
    """"verbatim" | "folded" | "absent"."""
    if not isinstance(signal, str) or not signal.strip():
        return "absent"
    if norm_ws(signal) in norm_ws(posting):
        return "verbatim"
    return "folded" if fold(signal) in fold(posting) else "absent"


def parse_response(text: str) -> dict:
    """The JSON object out of a reply that may be fenced or have prose around it."""
    s = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", s, re.S)
    if fence:
        s = fence.group(1).strip()
    start = s.find("{")
    if start < 0:
        raise ValueError("no JSON object in the reply")
    depth, in_str, esc = 0, False, False
    for i, c in enumerate(s[start:], start):
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                obj = json.loads(s[start:i + 1])
                if not isinstance(obj, dict):
                    raise ValueError("top-level JSON is not an object")
                return obj
    raise ValueError("unterminated JSON object in the reply")


def auto_check(parsed: dict, posting: str) -> list[str]:
    """Deterministic problems with one labeler's answer. Empty means clean."""
    problems = []
    cls = parsed.get("production")
    if cls not in CLASSES:
        extra = (' - the string "null"/"none", not JSON null'
                 if isinstance(cls, str) and cls.strip().lower() in ("null", "none", "")
                 else f", not one of {('null', 'required', 'nice_to_have')}")
        problems.append(f"production is {cls!r}{extra}")
    signal = parsed.get("production_signal")
    if isinstance(signal, str) and signal.strip().lower() in ("null", "none"):
        problems.append(f'production_signal is the string {signal!r}, not JSON null')
        signal = None
    state = quoted(signal, posting)
    if cls is None:
        if signal is not None:
            problems.append(f"production is null but production_signal is {signal!r}")
    elif cls in ("required", "nice_to_have"):
        if signal is None:
            problems.append("production is set but production_signal is null; "
                            "a stated label quotes the posting")
        elif state == "absent":
            problems.append(f"production_signal is not in the posting verbatim: {signal!r}")
        elif state == "folded":
            problems.append(f"production_signal matches only after folding quotes/dashes "
                            f"(transcribed, not copied): {signal!r}")
    if not isinstance(parsed.get("uncertain", False), bool):
        problems.append(f"uncertain is {parsed.get('uncertain')!r}, not a boolean")
    if not str(parsed.get("why", "")).strip():
        problems.append("why is empty")
    return problems


# --- providers ---------------------------------------------------------------------

def call_anthropic(model: str, system: str, user: str) -> str:
    import anthropic
    r = anthropic.Anthropic().messages.create(
        model=model, max_tokens=MAX_TOKENS, system=system,
        messages=[{"role": "user", "content": user}])
    if r.stop_reason == "max_tokens":
        raise RuntimeError(f"{model} hit the {MAX_TOKENS}-token cap; the label is truncated")
    return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")


def call_openai(model: str, system: str, user: str) -> str:
    import openai
    r = openai.OpenAI().chat.completions.create(
        model=model, response_format={"type": "json_object"},
        max_completion_tokens=MAX_TOKENS,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    choice = r.choices[0]
    if choice.finish_reason == "length":
        raise RuntimeError(f"{model} hit the {MAX_TOKENS}-token cap; the label is truncated")
    return choice.message.content or ""


PROVIDERS = {"anthropic": call_anthropic, "openai": call_openai}


def check_models(a: str, b: str):
    """A labeler must not be the model being measured, and two copies of one model are not
    two labelers. HIR-70's rule, and the reason this process exists."""
    for name, model in (("A", a), ("B", b)):
        if model == EXTRACTOR_MODEL:
            raise SystemExit(f"labeler {name} is {model!r}, the extractor's model. A labeler "
                             f"must not be the thing being measured (HIR-70).")
    if a == b:
        raise SystemExit(f"both labelers are {a!r}; two copies of one model are not two labelers.")


# --- reporting ---------------------------------------------------------------------

def fmt(cls, signal, width: int = 64) -> str:
    label = "null (not mentioned)" if cls is None else str(cls)
    if signal is None:
        return label
    s = norm_ws(str(signal))
    return f'{label} — "{s if len(s) <= width else s[:width - 1] + "…"}"'


def render(rows: list[dict], meta: dict) -> str:
    out = [f"# Held-out production labels, two blind labelers — {meta['run_id']}", "",
           f"- labeler A: `{meta['model_a']}` ({meta['provider_a']})",
           f"- labeler B: `{meta['model_b']}` ({meta['provider_b']})",
           f"- extractor (excluded from labeling): `{meta['extractor_model']}`",
           f"- rules: DECISIONS.md 2026-10-28 rule bullets, sha256 `{meta['rules_sha'][:12]}`",
           f"- prompt sha256: `{meta['prompt_sha'][:12]}`",
           "", "Nothing here is applied. Agreement is a proposal; a person decides.", "",
           "## Side by side", "",
           "| posting | labeler A | labeler B | state |", "|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['golden_id']} | {fmt(r['a_class'], r['a_signal'], 40)} | "
                   f"{fmt(r['b_class'], r['b_signal'], 40)} | {r['state']} |")

    for title, key in (("Agreed", "agree"), ("Disagreement — needs a decision", "disagree"),
                       ("Auto-check failures", "failed"), ("Flagged uncertain", "uncertain")):
        sel = [r for r in rows if key in r["buckets"]]
        out += ["", f"## {title} ({len(sel)})"]
        if not sel:
            out.append("\nNone.")
            continue
        for r in sel:
            out += ["", f"### {r['golden_id']}"]
            for name in ("a", "b"):
                out.append(f"- **labeler {name.upper()}** — {fmt(r[f'{name}_class'], r[f'{name}_signal'], 200)}")
                out.append(f"  - why: {r[f'{name}_why'] or '(none given)'}")
                if r[f"{name}_uncertain"]:
                    out.append("  - **flagged uncertain by the labeler**")
                for p in r[f"{name}_problems"]:
                    out.append(f"  - **auto-check**: {p}")
                if r[f"{name}_error"]:
                    out.append(f"  - **error**: {r[f'{name}_error']}")
    return "\n".join(out) + "\n"


# --- main --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model-a", default=DEFAULT_MODEL_A)
    ap.add_argument("--provider-a", default="anthropic", choices=sorted(PROVIDERS))
    ap.add_argument("--model-b", default=DEFAULT_MODEL_B)
    ap.add_argument("--provider-b", default="openai", choices=sorted(PROVIDERS))
    ap.add_argument("--run", help="reuse an existing run directory's cached raw replies")
    ap.add_argument("--dry-run", action="store_true",
                    help="build and print the prompt, call nothing")
    args = ap.parse_args(argv)

    check_models(args.model_a, args.model_b)
    bullets = rule_bullets(DECISIONS.read_text())
    system = build_prompt(bullets)
    rules_sha = sha256(bullets.encode()).hexdigest()
    prompt_sha = sha256(system.encode()).hexdigest()

    if args.dry_run:
        print(system)
        print(f"\n--- rules sha256 {rules_sha}\n--- prompt sha256 {prompt_sha}", file=sys.stderr)
        return 0

    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass

    run_dir = RUNS / (args.run or
                      datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_heldout_production")
    (run_dir / "raw").mkdir(parents=True, exist_ok=True)
    (run_dir / "prompt.md").write_text(system)

    labelers = {"A": (args.provider_a, args.model_a), "B": (args.provider_b, args.model_b)}
    rows = []
    for gid in GOLDEN_IDS:
        # the posting only: no label of any kind is read from the Golden
        posting = json.loads((GOLDENS / f"{gid}.json").read_text())["job_description"]
        row = {"golden_id": gid}
        for name, (provider, model) in labelers.items():
            path = run_dir / "raw" / f"{gid}.{name}.json"
            rec = None
            if path.exists():
                cached = json.loads(path.read_text())
                if cached.get("prompt_sha") == prompt_sha and cached.get("model") == model:
                    rec = cached
                    print(f"  {gid} {name}  cached")
            if rec is None:
                print(f"  {gid} {name}  {model} …", flush=True)
                rec = {"golden_id": gid, "labeler": name, "provider": provider, "model": model,
                       "prompt_sha": prompt_sha, "rules_sha": rules_sha,
                       "raw": None, "parsed": None, "error": None}
                try:
                    rec["raw"] = PROVIDERS[provider](model, system, f"<posting>\n{posting}\n</posting>")
                except Exception as e:
                    rec["error"] = f"{type(e).__name__}: {e}"
                if rec["raw"] is not None:
                    try:
                        rec["parsed"] = parse_response(rec["raw"])
                    except (ValueError, json.JSONDecodeError) as e:
                        rec["error"] = f"{type(e).__name__}: {e}"
                path.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
            p = rec.get("parsed") or {}
            k = name.lower()
            row[f"{k}_class"] = p.get("production")
            row[f"{k}_signal"] = p.get("production_signal")
            row[f"{k}_why"] = str(p.get("why", "")).strip()
            row[f"{k}_uncertain"] = p.get("uncertain") is True
            row[f"{k}_error"] = rec.get("error")
            row[f"{k}_problems"] = auto_check(p, posting) if rec.get("parsed") else []

        buckets = []
        if row["a_error"] or row["b_error"]:
            buckets.append("failed")
        if row["a_problems"] or row["b_problems"]:
            buckets.append("failed")
        if row["a_uncertain"] or row["b_uncertain"]:
            buckets.append("uncertain")
        same = (row["a_class"] == row["b_class"]) and not row["a_error"] and not row["b_error"]
        buckets.append("agree" if same else "disagree")
        row["buckets"] = sorted(set(buckets))
        row["state"] = ("agree" if same else "DISAGREE") + (
            " · auto-check" if "failed" in buckets else "") + (
            " · uncertain" if "uncertain" in buckets else "")
        rows.append(row)

    meta = {"run_id": run_dir.name, "provider_a": args.provider_a, "model_a": args.model_a,
            "provider_b": args.provider_b, "model_b": args.model_b,
            "extractor_model": EXTRACTOR_MODEL, "rules_sha": rules_sha, "prompt_sha": prompt_sha,
            "golden_ids": list(GOLDEN_IDS),
            "agreed": sum(1 for r in rows if "agree" in r["buckets"]),
            "disagreed": sum(1 for r in rows if "disagree" in r["buckets"]),
            "auto_check_failures": sum(1 for r in rows if "failed" in r["buckets"]),
            "uncertain": sum(1 for r in rows if "uncertain" in r["buckets"])}
    (run_dir / "summary.json").write_text(
        json.dumps({"meta": meta, "rows": rows}, indent=2, ensure_ascii=False) + "\n")
    report = render(rows, meta)
    (run_dir / "summary.md").write_text(report)
    print("\n" + report)
    print(f"wrote {run_dir.relative_to(ROOT)}/  (no Golden was written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
