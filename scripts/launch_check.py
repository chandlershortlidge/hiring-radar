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

It also prints agreed labels and unagreed extras per posting, because F1 alone cannot tell
a quality gap from an arithmetic one: precision divides the extras by the agreed labels, so
a city whose postings name fewer skills scores worse on identical behaviour. That is exactly
what New York's 0.064 F1 gap turned out to be — same 2.5 extras per posting as Berlin, half
the agreed labels to divide them by (DECISIONS 2026-11-04, HIR-139). Those 2.5 were measured
before the unsure rule below; the extras this now prints are what is left after the skills
waiting for a hand-check have been set aside, which is a smaller number.

The comparison is panel-against-extractor in both cities, never panel-against-Goldens: the
committed Goldens carry no job id, so the extraction they correspond to cannot be looked up,
and a panel-labelled sample measured against a hand-labelled one would differ by method as
much as by city. The Berlin bar is therefore a second run of this same panel on Berlin
postings (`--baseline-run`), which is the only way the difference can be read as "city".

Does NOT: call a model, write Goldens, touch the labelling run, or change the database.
The labels it reads are model-written and unreviewed; they measure agreement, and they are
not Goldens until a person has checked them (DECISIONS 2026-11-03, HIR-132).

The unsure rule (HIR-159, Chandler's decision of 2026-11-04). A skill *both* labellers
found, where one or both flagged itself unsure, used to drop out of the yardstick and so
counted as an extractor mistake — 29 of New York's 35 "mistakes" were of exactly that kind
(HIR-139). Such a skill is now **set aside** while it waits in the hand-check queue: it is
removed from the yardstick *and* from the extractor's side, so it counts neither as a
correct find nor as a mistake. Once a person answers it in `review_queue.md` the item
counts normally — `ok`/`A`/`B`/an override puts the label back in the yardstick, `drop`
leaves it out and the extractor is charged for it as before. A verdict written by the judge
model or the third labeller is not a hand-check: those items stay set aside.

The panel check (HIR-149). Two cities can only be read against each other if their labels
were produced the same way, and the first two runs this script was used on were not: New
York was labelled by three labellers (a third checker, `gemini-4-argon`, was run on it)
and Berlin by two, which made the two runs' "agreed" yardsticks differ in kind. That was
visible only to someone listing the run directories by hand. So with `--baseline-run` the
script now reads the labellers each run actually used — out of the runs' own files — and,
when the two sets differ, prints one plain line **before** the numbers saying so and
saying that the comparison should be read on the labellers both runs share. The scores
still print: the comparison is not withheld, it is just no longer presented as clean.

Invariants: read-only. `compare`, `unsure_rule` and `panel_line` are pure — they take the
label sets, the queue items and their decisions, or the two labeller sets, and return the
result — so the arithmetic and the warning are testable without a database or a run
directory. A posting the panel could not label (both labellers failed, or every label went
to review) is reported as skipped, never scored as a disagreement. Skills only one
labeller found, and skills neither found, are untouched by the unsure rule: they score as
they always did. The panel check never stops the check it annotates: a run that does not
record its labellers reads as an unknown panel, which is reported as unknown rather than
as even.

    uv run python scripts/launch_check.py --run 20261103T223629Z_label
    uv run python scripts/launch_check.py --run <new city run> --baseline-run <berlin run>
"""

import argparse
import importlib.util
import json
import os
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.evaluation import score_golden, summarize  # noqa: E402

# agent_label.py owns the review queue this reads: its decision vocabulary (`ok` / `A` / `B`
# / `drop` / a JSON override) and its queue format are reused rather than re-implemented, so
# a verdict cannot mean one thing to the person writing it and another to the score.
_spec = importlib.util.spec_from_file_location("agent_label", ROOT / "scripts" / "agent_label.py")
agent_label = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agent_label)

LABELING_DIR = ROOT / "evals" / "labeling"
DB = Path(os.environ.get("HIRING_RADAR_DB", ROOT / "data" / "hiring-radar.db"))

# A queue item with one of these in place of a verdict has not been answered.
UNANSWERED = ("", "?")


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


def unsure_rule(items: list[dict], decisions: dict[int, str],
                by_model: set[int]) -> tuple[dict[str, list[dict]], dict[str, set[str]], int]:
    """The unsure rule over one run's queue, as (confirmed, set aside, waiting). Pure.

    - `confirmed`: golden id -> skills a person has answered in favour of, to be added to
      the yardstick. A person's `drop` is an answer too, and produces nothing here: the
      skill stays out of the yardstick and the extractor is charged for it, as before.
    - `set_aside`: golden id -> the skill ids no person has answered yet. Out of both sides
      of the score.
    - `waiting`: how many queue items of any kind still carry no verdict at all — the size
      of the hand-check queue, which is the third number the report prints.

    A verdict the item does not allow stops the script: a typo in the queue must not be read
    as "still waiting", which would quietly set the skill aside instead of scoring it.
    """
    confirmed: dict[str, list[dict]] = {}
    set_aside: dict[str, set[str]] = {}
    unreadable: list[str] = []
    waiting = 0
    for n, item in enumerate(items, 1):
        verdict = (decisions.get(n) or "").strip()
        unanswered = verdict.strip("`").lower() in UNANSWERED
        if unanswered:
            waiting += 1
        if item.get("kind") != "skill" or item.get("reason") != "uncertain":
            continue
        gid = item["golden_id"]
        if unanswered or n in by_model:
            set_aside.setdefault(gid, set()).add(item["key"])
            continue
        try:
            skills, _ = agent_label.apply_decision(item, verdict)
        except (ValueError, json.JSONDecodeError) as e:
            unreadable.append(f"item {n} ({gid} skill `{item['key']}`): {verdict!r} — {e}")
            continue
        for s in skills:
            confirmed.setdefault(gid, []).append(
                {"skill_id": s["skill_id"], "requirement": s["requirement"]})
    if unreadable:
        raise SystemExit("the review queue has verdicts this script cannot read:\n  "
                         + "\n  ".join(unreadable))
    return confirmed, set_aside, waiting


def run_decisions(run_dir: Path) -> tuple[list[dict], dict[int, str], set[int]]:
    """One run's queue items, the verdicts written against them, and which were ruled by a
    model rather than by a person. A run always carries `items.json` and `review_queue.md`;
    a missing one is an error, never an empty queue, because an empty queue would silently
    turn the unsure rule off and score the run the old way."""
    items = json.loads((run_dir / "items.json").read_text())
    decisions = dict(agent_label.parse_queue((run_dir / "review_queue.md").read_text()))
    record = agent_label.load_adjudication(run_dir)
    by_model = {int(n) for n, v in (record.get("items") or {}).items()
                if v.get("by") == "model"}
    return items, decisions, by_model


@dataclass
class Run:
    """One labelling run, ready to score."""
    expected: dict[str, list[dict]] = field(default_factory=dict)
    job_of: dict[str, int] = field(default_factory=dict)
    skipped: list[str] = field(default_factory=list)
    set_aside: dict[str, set[str]] = field(default_factory=dict)
    waiting: int = 0

    @property
    def n_set_aside(self) -> int:
        """Skills set aside in the postings that were actually scored."""
        return sum(len(ids) for gid, ids in self.set_aside.items() if gid in self.expected)


def load_run(run_id: str) -> Run:
    """A run's yardstick: the labellers' agreed skills plus the unsure skills a person has
    since confirmed, the job each posting is, the postings nothing could be scored on, and
    the unsure skills that are set aside while they wait for a hand-check."""
    run_dir = LABELING_DIR / run_id
    merged = json.loads((run_dir / "merged.json").read_text())
    picks = json.loads((run_dir / "picks.json").read_text())
    confirmed, set_aside, waiting = unsure_rule(*run_decisions(run_dir))
    out = Run(job_of={p["golden_id"]: p["job_id"] for p in picks},
              set_aside=set_aside, waiting=waiting)
    for gid, m in merged.items():
        skills = [{"skill_id": s["skill_id"], "requirement": s["requirement"]}
                  for s in (m.get("accepted_skills") or [])]
        skills += confirmed.get(gid, [])
        if skills:
            out.expected[gid] = skills
        else:
            out.skipped.append(gid)
    return out


def score_run(run_id: str) -> tuple[dict, Run]:
    """(score, the run as loaded). A skill set aside is dropped from the extractor's side
    too, which is what "neither credited nor penalised" means arithmetically."""
    run = load_run(run_id)
    conn = sqlite3.connect(DB)
    try:
        predicted = {gid: [p for p in stored_extraction(conn, run.job_of[gid])
                           if p["skill_id"] not in run.set_aside.get(gid, ())]
                     for gid in run.expected}
    finally:
        conn.close()
    return compare(run.expected, predicted), run


def _recorded_model(path: Path) -> set[str]:
    """The labeller a run file says wrote it, as a one-element set, or nothing.

    Unreadable is not the same as absent, but it is treated the same here on purpose: this
    is an annotation on someone else's numbers, and it must not be able to stop them being
    printed. An unreadable file leaves the panel looking incomplete, which `panel_line`
    then reports as unknown rather than as even.
    """
    try:
        model = json.loads(path.read_text()).get("model")
    except (OSError, json.JSONDecodeError, AttributeError):
        return set()
    return {model} if model else set()


def labellers(run_dir: Path) -> list[str]:
    """The labellers actually present in one run, by model name, sorted.

    Read from the run's own files rather than from its summary: the raw per-labeller files
    (`raw/golden_NNN.A.json` and friends) are what a labeller leaves behind, and
    `third_check.json` is what a third checker leaves behind — a panel of three shows up in
    both. Model names, not the slot letters A/B/C, because the name is what tells a reader
    that two runs used different families.

    An empty list means the run does not say: its `raw/` directory is missing, or nothing
    in it records a model. Never raises.
    """
    found: set[str] = set()
    raw = run_dir / "raw"
    if raw.is_dir():
        for f in sorted(raw.glob("*.json")):
            found |= _recorded_model(f)
    found |= _recorded_model(run_dir / "third_check.json")
    return sorted(found)


def panel_line(new_id: str, new_panel: list[str], base_id: str,
               base_panel: list[str]) -> str | None:
    """The one line that goes before the numbers, or None when the panels match. Pure.

    Three cases: the two runs used the same labellers (nothing to say); one of them does
    not record its labellers (cannot be shown to be even, so say that); the sets differ
    (say how, and on what the comparison should be read).
    """
    def names(panel):
        return ", ".join(panel)

    if not new_panel or not base_panel:
        unknown = [rid for rid, panel in ((new_id, new_panel), (base_id, base_panel))
                   if not panel]
        return ("uneven panel: cannot tell — "
                + plural(len(unknown), "run", "runs") + " " + ", ".join(unknown)
                + " does not record which labellers it used, so the comparison below "
                  "cannot be shown to have been labelled the same way in both cities; "
                  "read it on the labellers both runs share.")
    if sorted(new_panel) == sorted(base_panel):
        return None
    shared = sorted(set(new_panel) & set(base_panel))
    return (f"uneven panel: this run was labelled by {names(new_panel)}; the baseline by "
            f"{names(base_panel)}. The two runs' agreed labels therefore mean different "
            "things, so the city-against-city comparison below should be read on the "
            + (f"labellers both runs share ({names(shared)})." if shared
               else "labellers both runs share — and they share none."))


def per_posting(s: dict) -> dict:
    """Agreed labels and unagreed extras per posting — the two sides of precision, unmixed.

    Precision is extras measured against the agreed labels, so it moves when either side
    moves. A city whose postings name fewer skills scores worse on identical behaviour: the
    same extras divided by a smaller yardstick (HIR-139, and HIR-12 for why US postings name
    fewer). Reporting the two counts separately is what tells those cases apart. Pure.
    """
    n = s["n_goldens"]
    if not n:
        return {"agreed": None, "extras": None, "n": 0}
    return {"agreed": (s["tp"] + s["fn"]) / n, "extras": s["fp"] / n, "n": n}


def line(name: str, s: dict) -> str:
    def pct(x):
        return "n/a" if x is None else f"{x:.3f}"
    return (f"{name}: precision {pct(s['precision'])}  recall {pct(s['recall'])}  "
            f"F1 {pct(s['f1'])}  requirement accuracy {pct(s['requirement_accuracy'])}  "
            f"(tp {s['tp']} fp {s['fp']} fn {s['fn']})")


def plural(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def counts_line(run_id: str, run: Run) -> str:
    """The three numbers the report leads with, after the score: what was scored, what was
    set aside unchecked, and how long the hand-check queue is (HIR-159)."""
    return (f"run {run_id}: {plural(len(run.expected), 'posting', 'postings')} scored, "
            f"{plural(run.n_set_aside, 'skill', 'skills')} set aside unchecked, "
            f"{plural(run.waiting, 'item', 'items')} waiting in the hand-check queue"
            + (f"; {plural(len(run.skipped), 'posting', 'postings')} skipped "
               "(panel agreed on nothing): " + ", ".join(run.skipped) if run.skipped else ""))


def per_posting_line(name: str, s: dict) -> str:
    p = per_posting(s)
    if p["n"] == 0:
        return f"{name}: no postings scored"
    return (f"{name}: {p['agreed']:.1f} agreed labels per posting, "
            f"{p['extras']:.1f} unagreed extras per posting")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", required=True, help="a labelling run id under evals/labeling/")
    ap.add_argument("--baseline-run", default=None, metavar="RUN",
                    help="a second run, on the city that is the bar (usually Berlin)")
    ap.add_argument("--worse-by", type=float, default=0.05,
                    help="how much lower in F1 counts as clearly worse (default 0.05)")
    ap.add_argument("--extras-worse-by", type=float, default=0.5,
                    help="how many more unagreed extras per posting count as a real "
                         "difference rather than an arithmetic one (default 0.5)")
    args = ap.parse_args()

    # Before any numbers: was this even a comparison between two cities, or between two
    # panels? (HIR-149.) Only with a baseline — one run alone is not a comparison.
    if args.baseline_run:
        warning = panel_line(args.run, labellers(LABELING_DIR / args.run),
                             args.baseline_run, labellers(LABELING_DIR / args.baseline_run))
        if warning:
            print(warning + "\n")

    s, run = score_run(args.run)
    print(counts_line(args.run, run))
    print(line("new city", s))
    print(per_posting_line("new city", s))
    if args.baseline_run:
        b, brun = score_run(args.baseline_run)
        print(counts_line(args.baseline_run, brun))
        print(line("baseline", b))
        print(per_posting_line("baseline", b))
        if s["f1"] is not None and b["f1"] is not None:
            d = s["f1"] - b["f1"]
            worse = d < -args.worse_by
            print(f"F1 difference: {d:+.3f}  — "
                  + ("clearly worse, file a follow-up" if worse else "not clearly worse"))
            # A lower F1 on a flat extras count is the arithmetic of a shorter yardstick,
            # not worse extraction (HIR-139). Still a follow-up — but one that should start
            # by reading the extras, not the prompt.
            pn, pb = per_posting(s), per_posting(b)
            if worse and pn["extras"] is not None and pb["extras"] is not None:
                de = pn["extras"] - pb["extras"]
                print(f"unagreed extras per posting: {de:+.1f}  — "
                      + ("the extras count held while F1 fell, so check whether this city's "
                         "postings simply name fewer skills before reading it as worse "
                         "extraction"
                         if de <= args.extras_worse_by
                         else "the extractor is adding more extras here, not just scoring "
                              "against a shorter yardstick"))
    print("\nThese labels are model-written and unreviewed: they are not Goldens. "
          f"The review queue is evals/labeling/{args.run}/review_queue.md.")


if __name__ == "__main__":
    main()
