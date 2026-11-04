"""Build the score table a PR needs when it changes the extractor or the skill list.

AGENTS.md "The eval gate": any diff touching `app/extract.py` or `taxonomy/skills.json`
runs the dev eval, pastes this table into the PR body, and commits its own
`evals/results/<run_id>/` as the baseline for the next such change. This script exists so
that table is the same table every time — it finds the baseline itself and compares every
aggregate metric.

Two stop lines, because the metrics carry very different amounts of evidence (HIR-164,
DECISIONS 2026-11-04):

- the four per-Golden attribute scores (seniority, German, degree, production) are gated on
  **Goldens that flipped right -> wrong**, more than 2 stopping the merge. One Golden is
  0.05 of a yes/no score on a 20-Golden set, so a fractional threshold could not tell one
  unlucky posting from a real regression.
- the skill scores pool hundreds of mentions a run and keep the **0.02** drop rule.

Flips are recomputed from each run's `predictions.jsonl` through the same
`app.evaluation.attribute_hits` the run scored with, over the Goldens both runs scored. If
rescoring no longer reproduces what a run recorded, its Goldens were relabelled since, the
runs are not comparable Golden by Golden, and the table says so and falls back to 0.02.

Usage:
    uv run python scripts/eval_table.py <run_id|path>        # the table for the PR body
    uv run python scripts/eval_table.py --version-check      # may this PR skip the eval?

The baseline is the newest **committed** dev run under `evals/results/` (run ids are
timestamp-prefixed, so newest is last in sort order). Uncommitted result directories are
ignored on purpose: the baseline has to be something the next branch will also see.

`--version-check` serves the gate's one exemption. It prints the branch's
`extractor_version` and the one the baseline run measured. When they are equal, the
committed baseline already scored this exact extractor — prompt, tool schema, model id and
taxonomy all identical — so a fresh run cannot produce new information and the PR may skip
it by quoting the output. When they differ, the eval runs.

Does NOT: call the model, run the eval, write anything, or read held-out runs (held-out is
release-only, AGENTS.md). Pure comparison plus a thin git/file reader.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# AGENTS.md "Stop and ask": a *skill* metric down more than this against the last committed
# run stops the merge. The skill scores pool hundreds of mentions a run, so a fractional
# threshold means something on them.
STOP_DROP = 0.02

# AGENTS.md "The eval gate" (HIR-164): the four per-Golden attribute scores are gated on
# Goldens that flipped right -> wrong instead, and more than this many stops the merge. On a
# 20-Golden dev set one Golden is 0.05 of a yes/no score, so STOP_DROP was smaller than the
# smallest move the measurement can make and every single flip fired it. A count says what
# happened and stays meaningful as the set grows. See DECISIONS 2026-11-04.
STOP_FLIPS = 2

# Subtracting two means gives float noise in the last bits (0.90 - 0.88 lands at
# 0.020000000000000018), which would make a drop of exactly the stop line read as "more
# than" it. The scores have three meaningful decimals; this is far below that.
_EPS = 1e-9


def _is_regression(delta: float, threshold: float) -> bool:
    """A fall further than the stop line. Strictly greater, so a drop of exactly the
    threshold passes — AGENTS.md says "down more than 0.02"."""
    return -delta > threshold + _EPS


# ---------------------------------------------------------------- pure comparison


def compare(current: dict, baseline: dict | None) -> list[dict]:
    """One row per aggregate metric: its mean now, its mean in the baseline, the delta.

    Metric order follows `current`, then any metric only the baseline had (so a metric
    dropped from the suite still shows up rather than vanishing from the gate). A metric
    missing on either side gets `None` and no delta — never a delta against zero.
    """
    cur_agg = current.get("aggregate") or {}
    base_agg = (baseline or {}).get("aggregate") or {}

    names = list(cur_agg) + [m for m in base_agg if m not in cur_agg]
    rows = []
    for name in names:
        now = (cur_agg.get(name) or {}).get("mean")
        was = (base_agg.get(name) or {}).get("mean")
        delta = None if now is None or was is None else now - was
        rows.append({"metric": name, "current": now, "baseline": was, "delta": delta})
    return rows


# ---------------------------------------------------------------- flipped Goldens


def _majority(hits: list[bool]) -> bool | None:
    """Right in most of a run's repeats. None when the repeats tie, or there are none.

    A tie is not evidence either way, so such a Golden is left out of both flip counts
    rather than guessed at.
    """
    yes = sum(1 for h in hits if h)
    no = len(hits) - yes
    return None if yes == no else yes > no


def per_golden_hits(run_dir: Path, goldens: dict[str, dict]) -> dict[str, dict[str, list[bool]]]:
    """{metric: {golden_id: [hit per repeat]}} for one run's stored predictions.

    Reads `predictions.jsonl` and scores it through `app.evaluation.attribute_hits`, the same
    function the run itself scored with, so the gate cannot grade attributes by its own rules.
    Goldens the run scored but we no longer have a label file for are skipped.
    """
    sys.path.insert(0, str(ROOT))
    from app.evaluation import ATTRIBUTE_METRICS, attribute_hits  # noqa: PLC0415

    out: dict[str, dict[str, list[bool]]] = {m: {} for m in ATTRIBUTE_METRICS}
    path = run_dir / "predictions.jsonl"
    if not path.is_file():
        return {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        g = goldens.get(row.get("golden_id"))
        if g is None:
            continue
        for metric, hit in attribute_hits(g, row).items():
            if hit is not None:
                out[metric].setdefault(row["golden_id"], []).append(hit)
    return out


def reproduces_stored(summary: dict, hits: dict[str, dict[str, list[bool]]]) -> bool:
    """Does rescoring the stored predictions give back the accuracies the run recorded?

    Goldens get relabelled — attributes were added to the set after October's runs, and
    seniority labels were revised — so rescoring an old run against today's labels can
    silently produce numbers that run never saw. When that happens the two runs are not
    comparable Golden by Golden and the flip count would be fiction, so the gate says so and
    falls back to the delta rule instead of reporting it.

    Compares each repeat's accuracy per attribute against `summary["runs"][i]`.
    """
    runs = summary.get("runs") or []
    if not runs or not hits:
        return False
    for i, stored in enumerate(runs):
        for metric, by_golden in hits.items():
            scored = [v[i] for v in by_golden.values() if len(v) > i]
            mine = (sum(1 for x in scored if x) / len(scored)) if scored else None
            theirs = stored.get(metric)
            if mine is None or theirs is None:
                if mine is not None or theirs is not None:
                    return False
            elif abs(mine - theirs) > 1e-9:
                return False
    return True


def flip_counts(current_dir: Path, baseline_dir: Path, goldens: dict[str, dict],
                current_summary: dict, baseline_summary: dict) -> dict[str, dict] | None:
    """Per attribute: how many Goldens went right -> wrong, and how many wrong -> right.

    Only Goldens *both* runs scored are counted, so growing the dev set never reads as a
    regression. Returns None when the count cannot be trusted — predictions missing, or
    either run failing `reproduces_stored` — and the caller then falls back to STOP_DROP.
    """
    cur = per_golden_hits(current_dir, goldens)
    base = per_golden_hits(baseline_dir, goldens)
    if not cur or not base:
        return None
    if not (reproduces_stored(current_summary, cur) and reproduces_stored(baseline_summary, base)):
        return None

    out = {}
    for metric, cur_by_golden in cur.items():
        base_by_golden = base.get(metric) or {}
        worse = better = 0
        shared = sorted(cur_by_golden.keys() & base_by_golden.keys())
        for gid in shared:
            now = _majority(cur_by_golden[gid])
            was = _majority(base_by_golden[gid])
            if now is None or was is None or now == was:
                continue
            if was and not now:
                worse += 1
            else:
                better += 1
        out[metric] = {"worse": worse, "better": better, "n": len(shared)}
    return out


def annotate_flips(rows: list[dict], flips: dict[str, dict] | None) -> list[dict]:
    """Attach each attribute row's flip counts. Rows without one keep the delta rule."""
    for r in rows:
        if flips and r["metric"] in flips:
            r["flips"] = flips[r["metric"]]
    return rows


def regressions(rows: list[dict], threshold: float = STOP_DROP,
                flip_limit: int = STOP_FLIPS) -> list[dict]:
    """The rows that stop the merge.

    A row carrying flip counts (the per-Golden attributes) is judged on them: more than
    `flip_limit` Goldens going right -> wrong. Every other row keeps the delta rule, and so
    does an attribute row whose flips could not be counted.
    """
    bad = []
    for r in rows:
        if r.get("flips") is not None:
            if r["flips"]["worse"] > flip_limit:
                bad.append(r)
        elif r["delta"] is not None and _is_regression(r["delta"], threshold):
            bad.append(r)
    return bad


def _fmt(x: float | None) -> str:
    return "—" if x is None else f"{x:.3f}"


def _fmt_delta(x: float | None, threshold: float = STOP_DROP) -> str:
    if x is None:
        return "—"
    if abs(x) < 0.0005:
        return "±0.000"
    s = f"{x:+.3f}"
    return f"**{s}** ⚠" if _is_regression(x, threshold) else s


def _fmt_delta_plain(x: float | None) -> str:
    """A delta with no stop-line marking — for a row judged on flips, where a 0.05 move is
    one Golden and marking it would say the opposite of what this gate decided."""
    if x is None:
        return "—"
    return "±0.000" if abs(x) < 0.0005 else f"{x:+.3f}"


def _fmt_flips(flips: dict | None, flip_limit: int = STOP_FLIPS) -> str:
    if flips is None:
        return "—"
    worse, better = flips["worse"], flips["better"]
    cell = f"{worse} / {better}"
    return f"**{cell}** ⚠" if worse > flip_limit else cell


def render(rows: list[dict], current: dict, baseline: dict | None,
           threshold: float = STOP_DROP, flip_limit: int = STOP_FLIPS) -> str:
    """The markdown block that goes in the PR body, verbatim."""
    cm = current.get("meta") or {}
    out = ["## Eval (dev)", ""]

    if baseline is None:
        out += ["No committed dev run to compare against — this run becomes the first "
                "baseline.", ""]
        head = "| metric | this run |\n|---|---|"
        body = [f"| {r['metric']} | {_fmt(r['current'])} |" for r in rows]
    else:
        bm = baseline.get("meta") or {}
        out += [
            f"- this run: `{cm.get('run_id', '?')}` — extractor `{cm.get('extractor_version', '?')}`, "
            f"skill list v{cm.get('taxonomy_version', '?')}, model `{cm.get('model', '?')}`",
            f"- baseline: `{bm.get('run_id', '?')}` — extractor `{bm.get('extractor_version', '?')}`, "
            f"skill list v{bm.get('taxonomy_version', '?')}, model `{bm.get('model', '?')}`",
            f"- {cm.get('n_goldens', '?')} goldens × {cm.get('repeats', '?')} repeats "
            f"(baseline: {bm.get('n_goldens', '?')} × {bm.get('repeats', '?')})",
            "",
        ]
        head = ("| metric | baseline | this run | Δ | Goldens worse / better |"
                "\n|---|---|---|---|---|")
        body = [f"| {r['metric']} | {_fmt(r['baseline'])} | {_fmt(r['current'])} | "
                f"{_fmt_delta(r['delta'], threshold) if r.get('flips') is None else _fmt_delta_plain(r['delta'])} | "
                f"{_fmt_flips(r.get('flips'), flip_limit)} |" for r in rows]

    out += [head, *body, ""]

    gated = [r for r in rows if r.get("flips") is not None]
    if baseline is not None:
        if gated:
            out += [f"Attribute scores are gated on flipped Goldens — more than {flip_limit} "
                    f"going right → wrong stops the merge. The skill scores keep the "
                    f"{threshold} rule. (DECISIONS 2026-11-04, HIR-164.)", ""]
        else:
            out += ["Flipped Goldens could not be counted for the attribute scores, so every "
                    f"metric here is on the {threshold} rule. Either a run is missing its "
                    "`predictions.jsonl`, or rescoring the stored predictions no longer "
                    "reproduces what a run recorded — which means the Goldens were "
                    "relabelled since, and the two runs are not comparable Golden by Golden.",
                    ""]

    bad = regressions(rows, threshold, flip_limit)
    if bad:
        names = ", ".join(
            f"{r['metric']} ({r['flips']['worse']} Goldens worse)" if r.get("flips") is not None
            else f"{r['metric']} ({r['delta']:+.3f})" for r in bad)
        out += [f"**On the stop list, do not merge:** {names}. Needs Chandler.", ""]
    elif baseline is not None:
        out += [f"Nothing over the stop line: no attribute score lost more than {flip_limit} "
                f"Goldens, and no skill score is down more than {threshold}.", ""]
    return "\n".join(out)


# ---------------------------------------------------------------- thin I/O


def committed_dev_summaries(root: Path = ROOT) -> list[Path]:
    """Committed dev `summary.json` paths, oldest run first. Git is the source of truth —
    a result directory sitting untracked in the working tree is not a baseline."""
    out = subprocess.run(
        ["git", "ls-files", "-z", "evals/results/*_dev_*/summary.json"],
        cwd=root, capture_output=True, text=True, check=True,
    ).stdout
    return sorted((root / p for p in out.split("\0") if p), key=lambda p: p.parent.name)


def load_goldens(root: Path = ROOT) -> dict[str, dict]:
    """Every Golden label file, by id. Drafts are included: `run_eval` skips them, so a run
    never scored one, and a Golden absent from a run is simply never compared."""
    out = {}
    for path in sorted((root / "evals/goldens").glob("golden_*.json")):
        g = json.loads(path.read_text())
        out[g["id"]] = g
    return out


def load_baseline_path(root: Path = ROOT, exclude_run_id: str | None = None) -> Path | None:
    """The newest committed dev run's `summary.json` path, skipping the run being reported."""
    for path in reversed(committed_dev_summaries(root)):
        if exclude_run_id and path.parent.name == exclude_run_id:
            continue
        return path
    return None


def load_baseline(root: Path = ROOT, exclude_run_id: str | None = None) -> dict | None:
    """The newest committed dev run, skipping the run being reported (it may already be
    committed by the time the table is built)."""
    for path in reversed(committed_dev_summaries(root)):
        if exclude_run_id and path.parent.name == exclude_run_id:
            continue
        return json.loads(path.read_text())
    return None


def resolve_run(arg: str, root: Path = ROOT) -> Path:
    """A run id, a run directory, or a path straight to a summary.json."""
    cand = Path(arg)
    for p in (cand, cand / "summary.json",
              root / "evals/results" / arg / "summary.json"):
        if p.is_file():
            return p
    raise SystemExit(f"no summary.json for {arg!r} — give a run id under evals/results/ "
                     "or a path to one")


def version_check(root: Path = ROOT) -> tuple[str, dict | None, bool]:
    """The branch's extractor_version, the baseline run, and whether the baseline already
    measured this exact extractor."""
    sys.path.insert(0, str(root))
    from app.extract import DEFAULT_MODEL, extractor_version  # noqa: PLC0415
    from app.taxonomy import Taxonomy  # noqa: PLC0415

    current = extractor_version(Taxonomy.load(), DEFAULT_MODEL)
    baseline = load_baseline(root)
    measured = baseline is not None and (baseline.get("meta") or {}).get(
        "extractor_version") == current
    return current, baseline, measured


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("run", nargs="?", help="run id or path of the dev run to report")
    ap.add_argument("--version-check", action="store_true",
                    help="print whether the committed baseline already measured this "
                         "extractor (the gate's one exemption)")
    ap.add_argument("--threshold", type=float, default=STOP_DROP,
                    help=f"the stop line for a skill-score drop (default {STOP_DROP})")
    ap.add_argument("--flip-limit", type=int, default=STOP_FLIPS,
                    help=f"Goldens an attribute score may lose before the gate stops the "
                         f"merge (default {STOP_FLIPS})")
    args = ap.parse_args(argv)

    if args.version_check:
        current, baseline, measured = version_check()
        bm = (baseline or {}).get("meta") or {}
        print(f"branch extractor_version:   {current}")
        print(f"baseline extractor_version: {bm.get('extractor_version', '— (no committed dev run)')}"
              f"   (run {bm.get('run_id', '—')})")
        print()
        if measured:
            print("MATCH — the committed baseline scored this exact extractor (prompt, tool "
                  "schema,\nmodel and skill list all unchanged). A fresh dev run cannot "
                  "produce new\ninformation: quote these two lines in the PR body and skip "
                  "the eval.")
        else:
            print("DIFFERENT — this branch reads postings differently from the last measured\n"
                  "extractor. The eval gate applies: run scripts/run_eval.py, paste the table,\n"
                  "commit the result directory.")
        return 0

    if not args.run:
        ap.error("give a run id (or --version-check)")

    summary = resolve_run(args.run)
    current = json.loads(summary.read_text())
    run_id = (current.get("meta") or {}).get("run_id") or summary.parent.name
    if (current.get("meta") or {}).get("split") != "dev":
        raise SystemExit(f"{run_id} is not a dev run — the gate is the dev split "
                         "(held-out is release-only, AGENTS.md)")

    baseline_path = load_baseline_path(exclude_run_id=summary.parent.name)
    baseline = json.loads(baseline_path.read_text()) if baseline_path else None
    rows = compare(current, baseline)
    if baseline is not None:
        rows = annotate_flips(rows, flip_counts(
            summary.parent, baseline_path.parent, load_goldens(), current, baseline))
    print(render(rows, current, baseline, args.threshold, args.flip_limit))
    return 1 if regressions(rows, args.threshold, args.flip_limit) else 0


if __name__ == "__main__":
    raise SystemExit(main())
