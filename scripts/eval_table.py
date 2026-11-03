"""Build the score table a PR needs when it changes the extractor or the skill list.

AGENTS.md "The eval gate": any diff touching `app/extract.py` or `taxonomy/skills.json`
runs the dev eval, pastes this table into the PR body, and commits its own
`evals/results/<run_id>/` as the baseline for the next such change. This script exists so
that table is the same table every time — it finds the baseline itself, compares every
aggregate metric, and marks any drop past the 0.02 stop line.

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

# AGENTS.md "Stop and ask": an eval metric down more than this against the last committed
# run stops the merge.
STOP_DROP = 0.02

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


def regressions(rows: list[dict], threshold: float = STOP_DROP) -> list[dict]:
    """Rows that fell further than the stop line."""
    return [r for r in rows
            if r["delta"] is not None and _is_regression(r["delta"], threshold)]


def _fmt(x: float | None) -> str:
    return "—" if x is None else f"{x:.3f}"


def _fmt_delta(x: float | None, threshold: float = STOP_DROP) -> str:
    if x is None:
        return "—"
    if abs(x) < 0.0005:
        return "±0.000"
    s = f"{x:+.3f}"
    return f"**{s}** ⚠" if _is_regression(x, threshold) else s


def render(rows: list[dict], current: dict, baseline: dict | None,
           threshold: float = STOP_DROP) -> str:
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
        head = "| metric | baseline | this run | Δ |\n|---|---|---|---|"
        body = [f"| {r['metric']} | {_fmt(r['baseline'])} | {_fmt(r['current'])} | "
                f"{_fmt_delta(r['delta'], threshold)} |" for r in rows]

    out += [head, *body, ""]

    bad = regressions(rows, threshold)
    if bad:
        names = ", ".join(f"{r['metric']} ({r['delta']:+.3f})" for r in bad)
        out += [f"**Down more than {threshold} — on the stop list, do not merge:** {names}. "
                "Needs Chandler.", ""]
    elif baseline is not None:
        out += [f"No metric down more than {threshold}; the rest is noise on "
                f"{cm.get('n_goldens', '?')} goldens.", ""]
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
                    help=f"the stop line for a drop (default {STOP_DROP})")
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

    baseline = load_baseline(exclude_run_id=summary.parent.name)
    rows = compare(current, baseline)
    print(render(rows, current, baseline, args.threshold))
    return 1 if regressions(rows, args.threshold) else 0


if __name__ == "__main__":
    raise SystemExit(main())
