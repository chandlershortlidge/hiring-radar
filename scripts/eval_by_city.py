"""Per-city scores for one eval run, so a city's own numbers can be read off a run.

    uv run python scripts/eval_by_city.py <run_id>

Why this exists: the headline scores pool every answer key, so a city the model reads badly
is invisible while the other cities carry the average (HIR-253). This splits one run by the
city of each posting and prints the same measures per city.

How the numbers are made:

- Skill precision, recall and F1 come from each posting's true and false positives and
  negatives as `predictions.jsonl` stores them, pooled over the run's repeats.
- The attribute columns go through `app.evaluation.attribute_hits`, the helper the run and
  the eval gate both use, so the bottom row equals the run's headline figures rather than
  being a second, slightly different calculation.
- A city comes from the labelling run that picked the posting (`picks.json`). Keys written
  before that pipeline carry no city and are reported as "not recorded".

Only the keys in the run's own split appear: a `dev` run says nothing about the sealed half.
"""

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.evaluation import attribute_hits  # noqa: E402

GOLDENS = ROOT / "evals" / "goldens"
RUNS = ROOT / "evals" / "labeling"
RESULTS = ROOT / "evals" / "results"

METRICS = ("seniority_accuracy", "german_accuracy", "degree_accuracy")
NOT_RECORDED = "not recorded"


def cities() -> dict[str, str]:
    """golden_id -> the city its posting was picked from."""
    out: dict[str, str] = {}
    for picks in sorted(RUNS.glob("*/picks.json")):
        for p in json.loads(picks.read_text()):
            out[p["golden_id"]] = p.get("place") or NOT_RECORDED
    return out


def goldens() -> dict[str, dict]:
    return {g["id"]: g for g in
            (json.loads(f.read_text()) for f in GOLDENS.glob("golden_*.json"))}


def tally(rows: list[dict], city: dict[str, str], keys: dict[str, dict]):
    """(per-city counters, per-city set of golden ids)."""
    agg: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    seen: dict[str, set] = collections.defaultdict(set)
    for r in rows:
        gid = r["golden_id"]
        c = city.get(gid, NOT_RECORDED)
        a = agg[c]
        seen[c].add(gid)
        a["tp"] += len(r.get("tp") or [])
        a["fp"] += len(r.get("fp") or [])
        a["fn"] += len(r.get("fn") or [])
        g = keys.get(gid)
        if not g:
            continue
        for metric, hit in attribute_hits(g, r).items():
            if metric in METRICS and hit is not None:
                a[f"{metric}_n"] += 1
                a[f"{metric}_ok"] += hit
    return agg, seen


def prf(a: collections.Counter) -> tuple[float, float, float]:
    p = a["tp"] / (a["tp"] + a["fp"]) if a["tp"] + a["fp"] else 0.0
    r = a["tp"] / (a["tp"] + a["fn"]) if a["tp"] + a["fn"] else 0.0
    return p, r, (2 * p * r / (p + r) if p and r else 0.0)


def rate(a: collections.Counter, metric: str) -> str:
    n = a[f"{metric}_n"]
    return f"{a[f'{metric}_ok'] / n:.3f}" if n else "  -   "


def render(agg, seen) -> list[str]:
    lines = [f"{'city':<16}{'keys':>5}{'prec':>8}{'recall':>8}{'f1':>8}"
             f"{'seniority':>11}{'german':>8}{'degree':>8}"]
    total = collections.Counter()
    for c, a in sorted(agg.items(), key=lambda kv: (-len(seen[kv[0]]), kv[0])):
        p, r, f1 = prf(a)
        lines.append(f"{c:<16}{len(seen[c]):>5}{p:>8.3f}{r:>8.3f}{f1:>8.3f}"
                     f"{rate(a, 'seniority_accuracy'):>11}{rate(a, 'german_accuracy'):>8}"
                     f"{rate(a, 'degree_accuracy'):>8}")
        total.update(a)
    p, r, f1 = prf(total)
    lines.append(f"{'all of them':<16}{sum(len(v) for v in seen.values()):>5}"
                 f"{p:>8.3f}{r:>8.3f}{f1:>8.3f}"
                 f"{rate(total, 'seniority_accuracy'):>11}"
                 f"{rate(total, 'german_accuracy'):>8}{rate(total, 'degree_accuracy'):>8}")
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", help="run id or path of the eval run to split by city")
    args = ap.parse_args(argv)

    path = Path(args.run)
    if not path.is_dir():
        path = RESULTS / args.run
    preds = path / "predictions.jsonl"
    if not preds.exists():
        raise SystemExit(f"no predictions.jsonl in {path}")

    rows = [json.loads(l) for l in preds.read_text().splitlines() if l.strip()]
    agg, seen = tally(rows, cities(), goldens())
    print("\n".join(render(agg, seen)))


if __name__ == "__main__":
    main()
