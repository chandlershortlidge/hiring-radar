"""Run the Golden eval against the live model and write results to evals/results/.

Usage:
    uv run python scripts/run_eval.py                 # dev split, 3 repeats
    uv run python scripts/run_eval.py --repeats 1     # quick look
    uv run python scripts/run_eval.py --split heldout --i-am-releasing   # release points only

Needs ANTHROPIC_API_KEY, from the environment or a .env file at the repo root (see .env.example). Calls the model sequentially, no retries.
Writes evals/results/<run_id>/{predictions.jsonl, summary.json, summary.md}.

Does NOT: change prompts, taxonomy, or Goldens; run held-out Goldens without the explicit
flag (AGENTS.md: never tune on held-out).
"""

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")  # existing environment variables win over .env

from app import evaluation  # noqa: E402
from app.extract import DEFAULT_MODEL, extract, extractor_version, make_client  # noqa: E402
from app.taxonomy import Taxonomy  # noqa: E402


def load_goldens(split: str) -> list[dict]:
    out = []
    for p in sorted((ROOT / "evals/goldens").glob("*.json")):
        g = json.loads(p.read_text())
        if g["split"] == split:
            out.append(g)
    return out


def fmt(x):
    return "—" if x is None else f"{x:.3f}"


def render_md(meta, agg, runs) -> str:
    lines = [f"# Eval {meta['run_id']}", "",
             f"- split: `{meta['split']}`, goldens: {meta['n_goldens']}, repeats: {meta['repeats']}",
             f"- model: `{meta['model']}`, extractor: `{meta['extractor_version']}`, taxonomy v{meta['taxonomy_version']}",
             "", "| metric | mean | min | max |", "|---|---|---|---|"]
    for m, v in agg.items():
        lines.append(f"| {m} | {fmt(v['mean'])} | {fmt(v['min'])} | {fmt(v['max'])} |")
    first = runs[0]
    lines += ["", f"Errors in run 1: {first.summary['n_errors']}", "",
              "## Top 10 skills, run 1", "", "| # | gold | predicted |", "|---|---|---|"]
    for i, (g, p) in enumerate(zip(first.summary["gold_top"], first.summary["pred_top"]), 1):
        lines.append(f"| {i} | {g} | {p} |")

    misses = Counter(s for r in runs for gs in r.scores for s in gs.fn)
    extras = Counter(s for r in runs for gs in r.scores for s in gs.fp)
    proposed = Counter(p["label"] for r in runs for pr in r.predictions.values() for p in pr.get("proposed", []))
    for title, c in (("Most-missed skills (all runs)", misses), ("Most-frequent extras (all runs)", extras),
                     ("Proposed new skills (all runs)", proposed)):
        lines += ["", f"## {title}", ""] + [f"- {k}: {v}" for k, v in c.most_common(15)]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="dev", choices=["dev", "heldout"])
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--i-am-releasing", action="store_true")
    args = ap.parse_args(argv)

    if args.split == "heldout" and not args.i_am_releasing:
        sys.exit("Held-out Goldens are for release points only. Pass --i-am-releasing if this is one.")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.")

    tax = Taxonomy.load()
    goldens = load_goldens(args.split)
    if not goldens:
        sys.exit(f"No Goldens in split {args.split!r}.")
    client = make_client()
    extract_fn = lambda text: extract(text, tax, client, args.model)

    runs = []
    for i in range(args.repeats):
        print(f"run {i + 1}/{args.repeats} over {len(goldens)} goldens…", flush=True)
        runs.append(evaluation.run_once(goldens, extract_fn))
        s = runs[-1].summary
        print(f"  P={fmt(s['precision'])} R={fmt(s['recall'])} F1={fmt(s['f1'])} "
              f"req={fmt(s['requirement_accuracy'])} sen={fmt(s['seniority_accuracy'])}/{s['seniority_n']} "
              f"de={fmt(s['german_accuracy'])}/{s['german_n']} deg={fmt(s['degree_accuracy'])}/{s['degree_n']} "
              f"rho={fmt(s['rank_spearman'])} errors={s['n_errors']}")
        errors = [(gid, p["error"]) for gid, p in runs[-1].predictions.items() if "error" in p]
        if errors:
            gid, msg = errors[0]
            print(f"  first error ({gid}): {msg[:500]}")
        if len(errors) == len(goldens):
            sys.exit("Every Golden failed — no results written. Fix the error above and re-run.")

    agg = evaluation.across_runs(runs)
    version = extractor_version(tax, args.model)
    run_id = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{args.split}_{version}"
    meta = {"run_id": run_id, "split": args.split, "n_goldens": len(goldens), "repeats": args.repeats,
            "model": args.model, "extractor_version": version, "taxonomy_version": tax.version}

    out = ROOT / "evals/results" / run_id
    out.mkdir(parents=True)
    with (out / "predictions.jsonl").open("w") as f:
        for i, r in enumerate(runs):
            for gs in r.scores:
                f.write(json.dumps({"run": i + 1, "golden_id": gs.golden_id, "tp": gs.tp, "fp": gs.fp, "fn": gs.fn,
                                    "error": gs.error, **r.predictions[gs.golden_id]}, ensure_ascii=False) + "\n")
    (out / "summary.json").write_text(json.dumps(
        {"meta": meta, "aggregate": agg, "runs": [r.summary for r in runs]}, indent=2) + "\n")
    (out / "summary.md").write_text(render_md(meta, agg, runs))
    print(f"\nwrote {out.relative_to(ROOT)}/summary.md")


if __name__ == "__main__":
    main()
