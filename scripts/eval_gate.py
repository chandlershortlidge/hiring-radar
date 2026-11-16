"""The eval gate's CI half: an extractor or skill-list change must bring a dev eval result.

AGENTS.md "The eval gate" (HIR-133): a PR whose diff touches `app/extract.py` or
`taxonomy/skills.json` runs the dev eval and commits `evals/results/<run_id>/` as the next
baseline. Until HIR-134 only the reviewer agent enforced that, by reading the PR body — so a
PR opened by hand, or by any path that skips the agent, passed CI with no eval at all. This
script is the cheap half CI can check with no key and no model call: did the PR add a dev
result, or does the committed baseline already cover this exact extractor?

Usage (from CI, see the `eval-gate` job in .github/workflows/ci.yml):

    uv run python scripts/eval_gate.py --changes-file changes.txt

`changes.txt` holds one `<status><TAB><path>` line per changed file, the status being
GitHub's (`added`, `modified`, `removed`, `renamed`, ...). Exit 0: the PR touches neither
file, or adds a new `evals/results/*_dev_*/summary.json`, or the version check says MATCH.
Exit 1 otherwise, with the rule and the two commands to run.

The exemption is `scripts/eval_table.py`'s own `version_check`, called only when it would
decide the outcome, so there is one definition of MATCH and no phrase or label to fake.

Does NOT: run the eval, call a model, read a result's contents or judge its scores (the
stop lines are `eval_table.py`'s, applied when the table is built), look at the PR body, or
read held-out runs. `decide` is pure; `main` is the thin file reader around it.
"""

import argparse
import fnmatch
import sys
from pathlib import Path

# The two inputs to `extractor_version` — the same trigger AGENTS.md names.
GATED_FILES = ("app/extract.py", "taxonomy/skills.json")

# A dev run's summary. Held-out runs (`*_heldout_*`) never satisfy the gate.
RESULT_PATTERN = "evals/results/*_dev_*/summary.json"

RULE = (
    'The rule (AGENTS.md "The eval gate"): a pull request that changes how postings are '
    "read\nor changes the skill list is measured on the dev set before it merges, and "
    "commits\nthat measurement so the next change has something to be compared with."
)

COMMANDS = (
    "    uv run python scripts/run_eval.py --repeats 1\n"
    "    uv run python scripts/eval_table.py <run_id>"
)


def _norm(path):
    return path.strip().removeprefix("./")


def gated_paths(changes):
    """The gated files among the changes, whatever happened to them, sorted."""
    return sorted({_norm(p) for _, p in changes if _norm(p) in GATED_FILES})


def added_results(changes):
    """Dev summaries this PR adds. A modified or renamed one is not a new measurement."""
    return sorted(
        _norm(p) for status, p in changes
        if status.strip() == "added" and fnmatch.fnmatchcase(_norm(p), RESULT_PATTERN)
    )


def needs_version_check(changes):
    """Whether the version check would decide the outcome — so CI can skip it otherwise."""
    return bool(gated_paths(changes)) and not added_results(changes)


def decide(changes, version_match):
    """(ok, message) for a list of (status, path) changes and the version-check answer.

    `version_match` is True when the committed baseline already measured this extractor,
    False when it did not; it is only read when `needs_version_check(changes)`.
    """
    gated = gated_paths(changes)
    if not gated:
        return True, "This PR changes neither the extractor nor the skill list. No eval needed."

    listed = "\n".join(f"  {p}" for p in gated)
    results = added_results(changes)
    if results:
        return True, (
            f"This PR changes:\n{listed}\nand adds a dev eval result:\n"
            + "\n".join(f"  {p}" for p in results)
        )
    if version_match:
        return True, (
            f"This PR changes:\n{listed}\nbut the last committed dev eval already measured "
            "this exact extractor\n(scripts/eval_table.py --version-check says MATCH), so "
            "no new run is needed."
        )
    return False, (
        f"This PR changes:\n{listed}\nand adds no dev eval result, and the last committed "
        "one measured a different\nextractor (scripts/eval_table.py --version-check says "
        f"DIFFERENT).\n\n{RULE}\n\nRun these on the branch, paste the second one's table "
        f"into the PR description under\n\"## Eval (dev)\", and commit the whole "
        f"evals/results/<run_id>/ directory:\n\n{COMMANDS}"
    )


def parse_changes(text):
    """`<status><TAB><path>` lines -> [(status, path)]. Blank lines are skipped."""
    out = []
    for line in text.splitlines():
        if not line.strip():
            continue
        status, _, path = line.partition("\t")
        out.append((status, path))
    return out


def baseline_measured_this_extractor():
    """`eval_table.version_check`'s answer. Needs the project's dependencies, not a key."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from eval_table import version_check  # noqa: PLC0415

    return version_check()[2]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--changes-file", required=True,
                    help="file holding one '<status><TAB><path>' line per changed file")
    args = ap.parse_args(argv)

    with open(args.changes_file, encoding="utf-8") as fh:
        changes = parse_changes(fh.read())

    match = baseline_measured_this_extractor() if needs_version_check(changes) else False
    ok, message = decide(changes, match)
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
