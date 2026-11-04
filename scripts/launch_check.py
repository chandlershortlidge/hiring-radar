"""Launch quality check: does the extractor read a new city's postings as well as Berlin's?

A city launched without a human step (HIR-132) still has to be checked, and the only
check available on day one is the independent labeller panel: `agent_label label --city
<city>` has two labellers from different model families label a sample blind, and the
labels they *agree* on are the yardstick here. This script compares that yardstick with
what the extractor actually stored for the same postings, and prints the same measures the
eval prints, so a city's numbers can be read against Berlin's.

Does: read a labelling run's `merged.json` (labeller-agreed skills) and `picks.json` (which
job each one is), read the stored extraction for those jobs out of the database, score one
against the other with `app.evaluation` — the same scorer the eval uses — and print micro
precision / recall / F1 plus requirement accuracy, for one run or for two side by side.

The comparison is panel-against-extractor in both cities, never panel-against-Goldens: the
committed Goldens carry no job id, so the extraction they correspond to cannot be looked up,
and a panel-labelled sample measured against a hand-labelled one would differ by method as
much as by city. The Berlin bar is therefore a second run of this same panel on Berlin
postings (`--baseline-run`), which is the only way the difference can be read as "city".

Does NOT: call a model, write Goldens, touch the labelling run, or change the database.
The labels it reads are model-written and unreviewed; they measure agreement, and they are
not Goldens until a person has checked them (DECISIONS 2026-11-03, HIR-132).

Invariants: read-only. `compare` is pure — it takes the two label sets and returns the
score — so the arithmetic is testable without a database or a run directory. A posting the
panel could not label (both labellers failed, or every label went to review) is reported as
skipped, never scored as a disagreement.

    uv run python scripts/launch_check.py --run 20261103T223629Z_label
    uv run python scripts/launch_check.py --run <new city run> --baseline-run <berlin run>
"""

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.evaluation import score_golden, summarize  # noqa: E402

LABELING_DIR = ROOT / "evals" / "labeling"
DB = Path(os.environ.get("HIRING_RADAR_DB", ROOT / "data" / "hiring-radar.db"))


def stored_extraction(conn: sqlite3.Connection, job_id: int) -> list[dict]:
    """What the extractor stored for one job: the predicted side of the comparison."""
    rows = conn.execute(
        "SELECT skill_id, requirement FROM skill_mention WHERE job_id = ? ORDER BY skill_id",
        (job_id,)).fetchall()
    return [{"skill_id": r[0], "requirement": r[1]} for r in rows]


def compare(expected_by_id: dict[str, list[dict]], predicted_by_id: dict[str, list[dict]]) -> dict:
    """Score labeller-agreed labels (expected) against stored extraction (predicted). Pure."""
    scores = [score_golden(gid, expected_by_id[gid], predicted_by_id.get(gid, []))
              for gid in sorted(expected_by_id)]
    return summarize(scores, expected_by_id, predicted_by_id)


def load_run(run_id: str) -> tuple[dict[str, list[dict]], dict[str, int], list[str]]:
    """(agreed skills per golden, job id per golden, goldens the panel could not label)."""
    run_dir = LABELING_DIR / run_id
    merged = json.loads((run_dir / "merged.json").read_text())
    picks = json.loads((run_dir / "picks.json").read_text())
    job_of = {p["golden_id"]: p["job_id"] for p in picks}
    expected, skipped = {}, []
    for gid, m in merged.items():
        skills = m.get("accepted_skills") or []
        if skills:
            expected[gid] = [{"skill_id": s["skill_id"], "requirement": s["requirement"]}
                             for s in skills]
        else:
            skipped.append(gid)
    return expected, job_of, skipped


def score_run(run_id: str) -> tuple[dict, int, list[str]]:
    """(score, postings scored, goldens the panel agreed on nothing for)."""
    expected, job_of, skipped = load_run(run_id)
    conn = sqlite3.connect(DB)
    try:
        predicted = {gid: stored_extraction(conn, job_of[gid]) for gid in expected}
    finally:
        conn.close()
    return compare(expected, predicted), len(expected), skipped


def line(name: str, s: dict) -> str:
    def pct(x):
        return "n/a" if x is None else f"{x:.3f}"
    return (f"{name}: precision {pct(s['precision'])}  recall {pct(s['recall'])}  "
            f"F1 {pct(s['f1'])}  requirement accuracy {pct(s['requirement_accuracy'])}  "
            f"(tp {s['tp']} fp {s['fp']} fn {s['fn']})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", required=True, help="a labelling run id under evals/labeling/")
    ap.add_argument("--baseline-run", default=None, metavar="RUN",
                    help="a second run, on the city that is the bar (usually Berlin)")
    ap.add_argument("--worse-by", type=float, default=0.05,
                    help="how much lower in F1 counts as clearly worse (default 0.05)")
    args = ap.parse_args()

    s, n, skipped = score_run(args.run)
    print(f"run {args.run}: {n} postings scored"
          + (f", {len(skipped)} skipped (panel agreed on nothing): {', '.join(skipped)}"
             if skipped else ""))
    print(line("new city", s))
    if args.baseline_run:
        b, bn, bskipped = score_run(args.baseline_run)
        print(f"run {args.baseline_run}: {bn} postings scored"
              + (f", {len(bskipped)} skipped" if bskipped else ""))
        print(line("baseline", b))
        if s["f1"] is not None and b["f1"] is not None:
            d = s["f1"] - b["f1"]
            worse = d < -args.worse_by
            print(f"F1 difference: {d:+.3f}  — "
                  + ("clearly worse, file a follow-up" if worse else "not clearly worse"))
    print("\nThese labels are model-written and unreviewed: they are not Goldens. "
          f"The review queue is evals/labeling/{args.run}/review_queue.md.")


if __name__ == "__main__":
    main()
