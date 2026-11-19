"""What one eval run cost, per reading, from the token counts the model reported.

    uv run python scripts/eval_cost.py <run_id|path> [<run_id|path> ...]

Why this exists: the scores say whether a cheaper model reads postings as well, and the
only honest answer to "how much cheaper" is the usage the API actually returned, not a
guess from the posting lengths (HIR-223). Each reading's `usage` is stored in a run's
`predictions.jsonl`, so the bill can be rebuilt afterwards from the committed run.

What it prints per run: the model, how many readings it holds, the mean input, cache-read,
cache-write and output tokens per reading, the cost of the whole run, the cost per reading,
and the largest prompt any reading sent. The prompt size matters on its own for Claude
Haiku 5.5: its prices step up for a request whose prompt passes 100,000 tokens, and the
prompt counts every input token including cache reads and writes, so the table says which
price band each run was billed in.

Prices are per million tokens, from the published pricing page on 2026-11-19
(platform.claude.com/docs/en/about-claude/pricing). They are the standard, non-batch,
global-routing prices. A model this file does not know is reported with no cost rather
than priced by a guess.

Does NOT: call a model, read held-out runs' text, or write anything.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Dollars per million tokens. "over" is Claude Haiku 5.5's second price band, which a
# request enters when its own prompt passes LONG_PROMPT_TOKENS input tokens.
PRICES = {
    "claude-sonnet-5-5": {
        "input": 2.00, "cache_write": 2.50, "cache_read": 0.10, "output": 10.00,
    },
    "claude-haiku-5-5": {
        "input": 0.10, "cache_write": 0.125, "cache_read": 0.01, "output": 0.50,
        "over": {"input": 0.50, "cache_write": 0.625, "cache_read": 0.05, "output": 2.50},
    },
}

# Claude Haiku 5.5's price bands meet here, counted over every input token of one request
# (base input, cache reads and cache writes together).
LONG_PROMPT_TOKENS = 100_000

MTOK = 1_000_000

FIELDS = ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens", "output_tokens")


def run_dir(arg: str, root: Path = ROOT) -> Path:
    """A run id or a path to its directory."""
    path = Path(arg)
    return path if path.is_dir() else root / "evals/results" / arg


def readings(path: Path) -> list[dict]:
    """Every reading's usage in a run, one row per Golden per repeat.

    A reading that errored has no usage and is skipped: it was never billed as a complete
    reading, and averaging it in as zero would understate the cost of the ones that worked.
    """
    out = []
    with (path / "predictions.jsonl").open() as f:
        for line in f:
            row = json.loads(line)
            usage = row.get("usage") or {}
            if not any(usage.get(k) for k in FIELDS):
                continue
            out.append({k: usage.get(k) or 0 for k in FIELDS} | {"golden_id": row["golden_id"]})
    return out


def prompt_tokens(r: dict) -> int:
    """One request's prompt length, as the pricing page counts it: every input token."""
    return r["input_tokens"] + r["cache_read_input_tokens"] + r["cache_creation_input_tokens"]


def price_for(model: str, reading: dict) -> dict | None:
    """The price band this one reading was billed in, or None for an unknown model."""
    table = PRICES.get(model)
    if table is None:
        return None
    if "over" in table and prompt_tokens(reading) > LONG_PROMPT_TOKENS:
        return table["over"]
    return {k: v for k, v in table.items() if k != "over"}


def cost_of(model: str, reading: dict) -> float | None:
    price = price_for(model, reading)
    if price is None:
        return None
    return (
        reading["input_tokens"] * price["input"]
        + reading["cache_creation_input_tokens"] * price["cache_write"]
        + reading["cache_read_input_tokens"] * price["cache_read"]
        + reading["output_tokens"] * price["output"]
    ) / MTOK


def summarize(path: Path) -> dict:
    meta = json.loads((path / "summary.json").read_text())["meta"]
    model = meta["model"]
    rows = readings(path)
    costs = [cost_of(model, r) for r in rows]
    priced = [c for c in costs if c is not None]
    prompts = [prompt_tokens(r) for r in rows]
    return {
        "run_id": meta["run_id"],
        "model": model,
        "n_readings": len(rows),
        "means": {k: (sum(r[k] for r in rows) / len(rows) if rows else 0.0) for k in FIELDS},
        "max_prompt_tokens": max(prompts) if prompts else 0,
        "over_long_band": sum(1 for p in prompts if p > LONG_PROMPT_TOKENS),
        "total_cost": sum(priced) if priced else None,
        "cost_per_reading": (sum(priced) / len(priced)) if priced else None,
    }


def fmt_cost(x: float | None) -> str:
    return "unknown price" if x is None else f"${x:.6f}".rstrip("0").rstrip(".")


def render(summaries: list[dict]) -> str:
    lines = ["| run | model | readings | in | cache read | cache write | out | $/reading | $/run |",
             "|---|---|---|---|---|---|---|---|---|"]
    for s in summaries:
        m = s["means"]
        lines.append(
            f"| {s['run_id']} | `{s['model']}` | {s['n_readings']} "
            f"| {m['input_tokens']:.0f} | {m['cache_read_input_tokens']:.0f} "
            f"| {m['cache_creation_input_tokens']:.0f} | {m['output_tokens']:.0f} "
            f"| {fmt_cost(s['cost_per_reading'])} | {fmt_cost(s['total_cost'])} |"
        )
    lines += ["", "Token columns are means per reading. Prices per million tokens as published "
                  "on 2026-11-19, standard (non-batch) rates.", ""]
    for s in summaries:
        band = (f"{s['over_long_band']} of {s['n_readings']} readings sent a prompt over "
                f"{LONG_PROMPT_TOKENS:,} tokens") if s["over_long_band"] else \
               f"every prompt stayed under {LONG_PROMPT_TOKENS:,} tokens"
        lines.append(f"- {s['run_id']}: largest prompt {s['max_prompt_tokens']:,} tokens; {band}.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", help="run ids or paths under evals/results/")
    args = ap.parse_args(argv)

    summaries = []
    for arg in args.runs:
        path = run_dir(arg)
        if not (path / "predictions.jsonl").exists():
            print(f"no predictions.jsonl in {path}", file=sys.stderr)
            return 1
        summaries.append(summarize(path))
    print(render(summaries), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
