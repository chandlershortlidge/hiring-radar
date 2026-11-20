"""Run the Golden eval against the live model and write results to evals/results/.

Usage:
    uv run python scripts/run_eval.py                 # dev split, 3 repeats
    uv run python scripts/run_eval.py --repeats 1     # quick look
    uv run python scripts/run_eval.py --split heldout --i-am-releasing   # release points only
    uv run python scripts/run_eval.py --model claude-haiku-5-5 --max-tokens 8192  # a trial
    uv run python scripts/run_eval.py --prompt-trial evals/experiments/trials/<name>.md  # a prompt trial

`--max-tokens` raises the output cap for one run and nothing else; the extractor the live
poll uses is untouched. It exists because a reading cut off at the cap returns nothing and
is scored as a total miss, so a model that writes more before it finishes is measured on
our cap instead of on how well it reads (HIR-223). Each run records the cap it ran under.

`--prompt-trial FILE` adds the file's text to the extractor's rules for one run, right after
them and before the skill list, so an instruction change can be measured without touching
the prompt the live poll uses (HIR-368). The run gets its own extractor version, hashed from
the prompt it was actually sent, so it can never pass for a run of the live extractor; the
trial file's name and text are recorded in the run. A trial run is an experiment: move it to
evals/experiments/ before committing (evals/experiments/README.md).

Needs ANTHROPIC_API_KEY, from the environment or a .env file at the repo root (see .env.example). Calls the model sequentially, no retries.
Writes evals/results/<run_id>/{predictions.jsonl, summary.json, summary.md}.

When LANGSMITH_API_KEY is set, the run is also reported to LangSmith as an experiment named
after the extractor_version (app/langsmith_eval.py): the dev Goldens as a dataset, one
trace per Golden per repeat, the scores attached. Pass --no-langsmith to skip that. The
committed evals/results/ directory stays the eval gate either way; LangSmith is the view.

Does NOT: change prompts, taxonomy, or Goldens; run held-out Goldens without the explicit
flag (AGENTS.md: never tune on held-out).
"""

import argparse
import hashlib
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

from app import evaluation, extras_judge, langsmith_eval  # noqa: E402
from app.extract import (  # noqa: E402
    DEFAULT_MODEL, INPUT_FORMAT, MAX_TOKENS, PRINCIPLES, TOOL, build_request, extraction_from_message,
    extractor_version, make_client, system_prompt,
)
from app.taxonomy import Taxonomy  # noqa: E402


def load_goldens(split: str) -> list[dict]:
    out = []
    # golden_*.json, not *.json: the directory also holds excluded.json (agent_label apply)
    for p in sorted((ROOT / "evals/goldens").glob("golden_*.json")):
        g = json.loads(p.read_text())
        if g["split"] == split and not g.get("draft"):  # drafts are unlabeled (scripts/new_goldens.py)
            out.append(g)
    return out


def trial_prompt(tax: Taxonomy, addition: str) -> str:
    """The live system prompt with `addition` placed after the rules, before the skill list."""
    live = system_prompt(tax)
    assert live.startswith(PRINCIPLES), "the system prompt no longer starts with the rules"
    return PRINCIPLES.rstrip("\n") + "\n\n" + addition.strip() + "\n" + live[len(PRINCIPLES):]


def trial_version(prompt: str, model: str) -> str:
    """extractor_version's hash, over the trial prompt instead of the live one."""
    h = hashlib.sha256((prompt + repr(TOOL) + model + INPUT_FORMAT).encode()).hexdigest()
    return f"x2-{h[:10]}"


def fmt(x):
    return "—" if x is None else f"{x:.3f}"


def render_md(meta, agg, runs) -> str:
    lines = [f"# Eval {meta['run_id']}", "",
             f"- split: `{meta['split']}`, goldens: {meta['n_goldens']}, repeats: {meta['repeats']}",
             f"- model: `{meta['model']}`, extractor: `{meta['extractor_version']}`, taxonomy v{meta['taxonomy_version']}"
             + (f", output cap {meta['max_tokens']}" if meta.get("max_tokens") else "")
             + (f", prompt trial `{meta['prompt_trial']['file']}`" if meta.get("prompt_trial") else ""),
             "", "| metric | mean | min | max |", "|---|---|---|---|"]
    for m, v in agg.items():
        lines.append(f"| {m} | {fmt(v['mean'])} | {fmt(v['min'])} | {fmt(v['max'])} |")
    first = runs[0]

    # Production experience (HIR-69): per-class P/R and the confusion matrix, run 1.
    pc = first.summary.get("production_per_class") or {}
    if pc:
        lines += ["", "## Production experience, run 1", "",
                  "| class | support | precision | recall |", "|---|---|---|---|"]
        for cls in ("required", "nice_to_have", "none"):
            r = pc.get(cls, {})
            lines.append(f"| {cls} | {r.get('support', 0)} | {fmt(r.get('precision'))} | {fmt(r.get('recall'))} |")
        conf = first.summary.get("production_confusion") or {}
        cols = ["required", "nice_to_have", "none"]
        lines += ["", "Confusion (rows = gold, cols = predicted):", "",
                  "| gold \\ pred | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
        for g in cols:
            lines.append(f"| {g} | " + " | ".join(str(conf.get(g, {}).get(c, 0)) for c in cols) + " |")
        lines += ["", f"Signal agreement where the class was right: "
                      f"{fmt(first.summary.get('production_signal_agreement'))} "
                      f"over {first.summary.get('production_signal_n', 0)} Goldens."]

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


def judge_extras(runs, goldens, args) -> dict:
    """Judge run 1's extras: {golden_id: [Verdict, ...]}.

    Run 1 only. The judge is there to find gold labels that are incomplete, which is a
    property of the label and not of a repeat, so judging all three repeats would pay three
    times for the same answer.

    Its own client is deliberately unwrapped, so its calls stay out of LangSmith: the issue
    asks for the trace budget to be checked before the judge is allowed to spend traces,
    and the verdicts are written to the results either way.
    """
    first = runs[0]
    by_id = {g["id"]: g for g in goldens}
    client = make_client()
    out = {}
    for gs in first.scores:
        if not gs.fp:
            continue
        g = by_id[gs.golden_id]
        mentions = first.predictions[gs.golden_id].get("mentions") or []
        quotes = {m["skill_id"]: m.get("raw_text") for m in mentions}
        extras = [{"skill_id": sid, "raw_text": quotes.get(sid)} for sid in gs.fp]
        out[gs.golden_id] = extras_judge.judge_golden(
            g["job_description"], sorted(x["skill_id"] for x in g["expected"]), extras,
            client, args.judge_model or extras_judge.DEFAULT_JUDGE_MODEL)
        print(f"  judged {len(extras)} extras on {gs.golden_id}", flush=True)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="dev", choices=["dev", "heldout"])
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-tokens", type=int, default=None,
                    help="output cap for this run only; the default is the extractor's own "
                         f"({MAX_TOKENS}). Raise it to measure a model that runs out of room "
                         "before it finishes answering: a reading cut off at the cap returns "
                         "nothing and scores as a total miss, which measures the cap rather "
                         "than the model (HIR-223). Changes nothing outside this run.")
    ap.add_argument("--prompt-trial", type=Path, default=None,
                    help="a file whose text is added to the extractor's rules for this run only "
                         "(HIR-368); the live prompt is untouched")
    ap.add_argument("--i-am-releasing", action="store_true")
    ap.add_argument("--no-langsmith", action="store_true",
                    help="do not report this run to LangSmith even if LANGSMITH_API_KEY is set")
    ap.add_argument("--extras-judge", action="store_true",
                    help="after the runs, ask a model whether each extra skill means the gold "
                         "label missed it or the model is wrong (one extra call per Golden "
                         "that has extras; off by default)")
    ap.add_argument("--judge-model", default=None,
                    help=f"model for --extras-judge (default: {extras_judge.DEFAULT_JUDGE_MODEL})")
    args = ap.parse_args(argv)

    if args.split == "heldout" and not args.i_am_releasing:
        sys.exit("Held-out Goldens are for release points only. Pass --i-am-releasing if this is one.")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.")

    tax = Taxonomy.load()
    goldens = load_goldens(args.split)
    if not goldens:
        sys.exit(f"No Goldens in split {args.split!r}.")
    trial = args.prompt_trial.read_text() if args.prompt_trial else None
    prompt = trial_prompt(tax, trial) if trial else None
    version = trial_version(prompt, args.model) if trial else extractor_version(tax, args.model)
    run_id = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{args.split}_{version}"
    # The cap is recorded because the run id and extractor_version do not encode it:
    # extractor_version hashes the prompt, the tool schema, the model and the input format,
    # so two runs of one model under different caps are indistinguishable without this.
    meta = {"run_id": run_id, "split": args.split, "n_goldens": len(goldens), "repeats": args.repeats,
            "model": args.model, "extractor_version": version, "taxonomy_version": tax.version,
            "max_tokens": args.max_tokens or MAX_TOKENS}
    if trial:
        meta["prompt_trial"] = {"file": args.prompt_trial.name, "text": trial}

    # Held-out text is never uploaded (app/langsmith_eval.py raises on a non-dev Golden),
    # and nothing is sent without a key.
    experiment = None if args.no_langsmith else langsmith_eval.start(goldens, meta)
    if experiment:
        print(f"langsmith experiment: {experiment.name} {experiment.url or ''}", flush=True)

    client = langsmith_eval.wrap_client(make_client()) if experiment else make_client()

    def extract_fn(text):
        """app.extract.extract, with this run's output cap if one was asked for.

        Built here rather than by adding an argument to the extractor, so the module the
        live poll uses is untouched: the cap is a property of this measurement only.
        """
        request = build_request(tax, text, args.model)
        if args.max_tokens:
            request["max_tokens"] = args.max_tokens
        if prompt:
            request["system"] = [{**request["system"][0], "text": prompt}]
        return extraction_from_message(client.messages.create(**request), tax, text, args.model)

    runs = []
    for i in range(args.repeats):
        print(f"run {i + 1}/{args.repeats} over {len(goldens)} goldens…", flush=True)
        runs.append(evaluation.run_once(goldens, extract_fn,
                                        trace=experiment.trace if experiment else None))
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

    verdicts = judge_extras(runs, goldens, args) if args.extras_judge else {}
    if verdicts:
        counts = extras_judge.tally([v for vs in verdicts.values() for v in vs])
        meta["extras_verdicts"] = counts
        print(f"extras judge over run 1: {counts}", flush=True)

    if experiment:
        experiment.finish(meta, agg, [r.summary for r in runs])

    out = ROOT / "evals/results" / run_id
    out.mkdir(parents=True)
    with (out / "predictions.jsonl").open("w") as f:
        for i, r in enumerate(runs):
            for gs in r.scores:
                row = {"run": i + 1, "golden_id": gs.golden_id, "tp": gs.tp, "fp": gs.fp, "fn": gs.fn,
                       "error": gs.error, **r.predictions[gs.golden_id]}
                if i == 0 and gs.golden_id in verdicts:
                    row["extras_verdicts"] = [vars(v) for v in verdicts[gs.golden_id]]
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    (out / "summary.json").write_text(json.dumps(
        {"meta": meta, "aggregate": agg, "runs": [r.summary for r in runs]}, indent=2) + "\n")
    (out / "summary.md").write_text(render_md(meta, agg, runs))
    print(f"\nwrote {out.relative_to(ROOT)}/summary.md")


if __name__ == "__main__":
    main()
