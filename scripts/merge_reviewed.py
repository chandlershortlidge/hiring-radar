"""Merge a PR the reviewer passed, when the reviewer's own session could not.

AGENTS.md "Who merges" (HIR-262). The reviewer agent merges a PR it passed with
`gh pr merge`. That command runs inside a Claude Code session, and the session's own
safety check has refused it before it ever reached GitHub — six reviewed, clean PRs in a
row went to Chandler only to press merge. So the reviewer also adds the label
`review-passed`, and this script, run by GitHub (.github/workflows/merge-reviewed.yml),
does the merge instead. No session setting can block it.

It merges only when all of these hold at the moment it looks:

- the PR is open and not a draft;
- it carries `review-passed` and does not carry `needs-chandler`;
- it touches none of the agents' own rule files (the rules gate, `rules_gate.py`) and
  not the labelling guide — those always wait for Chandler, whatever their labels say;
- GitHub reports it `clean`: every required check green and the branch up to date.

"At the moment it looks" has one exception (HIR-275). A check that is not required — the
before/after screenshots on a frontend PR — finishes a couple of minutes after the tests,
and no event tells this script when it does. A PR that passes every other condition and is
held back only by checks still running reports `unstable`; the script then waits for them,
up to PENDING_MAX_WAIT_S, and looks again, rather than declining once and leaving a green,
reviewed PR open forever. It waits for nothing else: a failed check, a branch behind main
or a missing label is still an immediate no, and what may merge is unchanged — only
`clean` does.

Removing `review-passed` or adding `needs-chandler` before then is how a person or an
agent stops it. It never arms GitHub's auto-merge and never updates the branch: a merge
or push made with the workflow's token starts no further workflows, so the checks on an
updated branch would never run and the deploy after an auto-merge would never fire. It
merges directly, then starts the CI workflow on main itself, which is what deploys.

Usage (from the workflow): python3 scripts/merge_reviewed.py --repo OWNER/REPO --pr N
                     or:   python3 scripts/merge_reviewed.py --repo OWNER/REPO --branch B

Exit 0 whether or not it merged (not merging is the normal answer to most events); exit 1
only when a GitHub call failed. Standard library only.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rules_gate import matched_paths  # noqa: E402

PASSED = "review-passed"
STOP = "needs-chandler"
# GitHub computes mergeability lazily; right after a check finishes it can say "unknown"
# for a few seconds. Ask again rather than read that as "no".
# Files that are Chandler's whatever the review said. The reviewer is what normally stops
# them (AGENTS.md "What Chandler is asked"); this is the backstop that does not depend on
# the reviewer having read its instructions. Only the unambiguous one: every other item on
# that list needs the ticket or the diff's content to judge.
CHANDLER_FILES = ("evals/LABELING.md",)
UNKNOWN_RETRIES = 6
UNKNOWN_WAIT_S = 10
# 'unstable' with checks still running: wait for them (HIR-275). The screenshots check runs
# about two minutes past the tests; 15 minutes covers a slow runner without holding a job
# open for a check that hangs.
PENDING_WAIT_S = 20
PENDING_MAX_WAIT_S = 15 * 60
# After the last check finishes GitHub can go on saying 'unstable' for a few seconds.
SETTLE_RETRIES = 3


def decide(pr, files):
    """(merge, reason) for a PR as the REST API returns it and its changed-file list."""
    labels = {lbl["name"] for lbl in pr.get("labels", [])}
    if pr.get("state") != "open":
        return False, "the PR is not open"
    if pr.get("draft"):
        return False, "the PR is a draft"
    if PASSED not in labels:
        return False, f"no '{PASSED}' label: the reviewer has not passed it"
    if STOP in labels:
        return False, f"labelled '{STOP}': it waits for Chandler"
    rules = matched_paths(files)
    if rules:
        return False, "it changes the agents' own rules, which always wait for Chandler: " + ", ".join(rules)
    guide = sorted({f.strip() for f in files if f.strip() in CHANDLER_FILES})
    if guide:
        return False, "it changes the labelling guide, which always waits for Chandler: " + ", ".join(guide)
    state = pr.get("mergeable_state")
    if state != "clean":
        return False, f"GitHub says '{state}', not 'clean' (checks still running or failed, or the branch is behind)"
    return True, "reviewed, checks green, branch up to date, no rule files"


def _gh(*args):
    out = subprocess.run(["gh", *args], check=True, capture_output=True, text=True)
    return out.stdout


def _api(path):
    return json.loads(_gh("api", path))


def _files(repo, n):
    out = _gh("api", f"repos/{repo}/pulls/{n}/files", "--paginate", "--jq", ".[].filename")
    return out.splitlines()


def _pr_for_branch(repo, branch):
    out = _gh("pr", "list", "--repo", repo, "--head", branch, "--state", "open",
              "--json", "number", "--jq", ".[].number")
    nums = out.split()
    return int(nums[0]) if nums else None


def _running_checks(repo, sha):
    """Names of the checks on a commit that have not finished yet."""
    out = _gh("api", f"repos/{repo}/commits/{sha}/check-runs?per_page=100", "--paginate",
              "--jq", '.check_runs[] | select(.status != "completed") | .name')
    return [line for line in out.splitlines() if line.strip()]


def _pr(repo, n, sleep):
    pr = _api(f"repos/{repo}/pulls/{n}")
    for _ in range(UNKNOWN_RETRIES):
        if pr.get("mergeable_state") not in (None, "unknown"):
            break
        sleep(UNKNOWN_WAIT_S)
        pr = _api(f"repos/{repo}/pulls/{n}")
    return pr


def _only_waiting_on_checks(pr, files):
    """True when the PR is 'unstable' and would merge if GitHub said 'clean' instead."""
    return pr.get("mergeable_state") == "unstable" and decide({**pr, "mergeable_state": "clean"}, files)[0]


def run(repo, n, sleep=time.sleep):
    pr = _pr(repo, n, sleep)
    files = _files(repo, n)

    waited = quiet = 0
    while _only_waiting_on_checks(pr, files) and waited < PENDING_MAX_WAIT_S:
        running = _running_checks(repo, pr["head"]["sha"])
        if running:
            quiet = 0
            wait = PENDING_WAIT_S
            print(f"PR #{n} waits on checks still running: {', '.join(running)}.")
        else:
            # Nothing running: either a check failed (it stays 'unstable', and that is a
            # no), or GitHub has not caught up yet. A few short looks tell them apart.
            quiet += 1
            if quiet > SETTLE_RETRIES:
                break
            wait = UNKNOWN_WAIT_S
        sleep(wait)
        waited += wait
        pr = _pr(repo, n, sleep)
        files = _files(repo, n)  # a push while we waited changes what the PR touches

    merge, reason = decide(pr, files)
    if not merge:
        print(f"PR #{n} not merged: {reason}.")
        return False

    sha = pr["head"]["sha"]
    # --match-head-commit: if someone pushed after we looked, GitHub refuses rather than
    # merging a commit the reviewer never saw.
    _gh("pr", "merge", str(n), "--repo", repo, "--merge", "--match-head-commit", sha)
    print(f"PR #{n} merged: {reason}.")
    # A merge made with the workflow's token does not fire `push`, so the deploy would not
    # run. Starting the CI workflow on main by hand is the one event that token may cause.
    _gh("workflow", "run", "ci.yml", "--repo", repo, "--ref", "main")
    print("Started CI on main, which deploys.")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", required=True)
    ap.add_argument("--pr", type=int)
    ap.add_argument("--branch", help="head branch, when the event carries no PR number")
    args = ap.parse_args(argv)

    n = args.pr
    if n is None and args.branch:
        n = _pr_for_branch(args.repo, args.branch)
    if n is None:
        print("No open PR for this event. Nothing to do.")
        return 0
    try:
        run(args.repo, n)
    except subprocess.CalledProcessError as e:
        print(f"GitHub call failed: {' '.join(e.cmd)}\n{e.stderr}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
