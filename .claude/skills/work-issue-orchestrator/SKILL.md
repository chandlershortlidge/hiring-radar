---
name: work-issue-orchestrator
description: Drop in a list of Linear issues and it runs them — one worker per issue in its own worktree via /work-issue, in parallel, then review and merge through the reviewer agent — autopilot by default, or a pause for Chandler's go and merge for issues labelled attended. Use when the person names several issues, says "run these", "work the todo list", or invokes /work-issue-orchestrator.
---

# /work-issue-orchestrator [HIR-n …] [max N]

You are the orchestrator. You write no code: you pick issues, start one worker per issue,
relay what needs Chandler, hand finished PRs to the reviewer, and report once. Default
max 3 workers at once.

## 1. Pick

**You are probably not the only orchestrator running** (HIR-124). Another session on
another ticket list sees none of your workers, and you see none of its. Everything in this
step reads shared state — Linear's issue status and the open pull requests — because that
is the only state both of you can see. Your own batch table is not shared state: never
decide a collision from it alone.

- If issues were named, use those. Otherwise take Linear issues in the roadmap project,
  state Todo, no open blockers (`blockedBy` all Done), not labelled `attended`.
- **Skip anything already In Progress.** A worker claims its issue by setting it In
  Progress before it does anything else, so In Progress means "another session has this"
  — drop it from the batch and say so in the table, even when it was named on the command
  line. An In Progress issue with a status note saying where a run stopped is the one
  exception: it may be picked up, and only if no other session is live on it.
- Every issue runs autopilot unless it carries the `attended` label (HIR-120). The worker
  sets the `autopilot` label itself; you don't label anything.
- **Check the open PRs before starting each worker, not once per batch.** List them
  (`gh pr list --state open --json number,title,headRefName`) and the files each one
  changes (`gh api repos/:owner/:repo/pulls/<n>/files`). Hold back any issue that would
  touch a file an open PR already changes, or a hot spot (`app/migrations/`,
  `app/extract.py`, `app/pipeline.py`, `app/dedup.py`, `taxonomy/skills.json`) an open PR
  touches — whoever opened that PR, this run or another session. Re-run the check as each
  slot frees up: the PR list has moved on.
- Collisions inside your own batch: two issues naming the same adapter or module, or both
  touching a hot spot, do not run together. Keep the higher priority, queue the other for
  after it merges. Two taxonomy-bumping issues never share a batch (one re-extract per
  day).
- Print the batch as a table: issue, `autopilot` or `attended`, why it's safe alongside the
  others and alongside every open PR, and the queue — with what each held-back issue is
  waiting for.

## 2. Work

For each issue, start a subagent with `isolation: "worktree"` and the prompt
`/work-issue HIR-n` and nothing else. Run them in parallel up to the max. Each follows the
work-issue skill: brief, own branch, green commits, PR, follow-up tickets.

**Autopilot issue:** the worker needs nothing from anyone. Do not answer its questions;
a worker that stops on a NO RULE has done the right thing — note it and move on.

**Attended issue:** the worker posts its brief and waits for a "go". Relay the brief to
Chandler in this session, verbatim, and pass his answer back to that worker (SendMessage).
Do the same for any Needs-Chandler question. You never answer for him.

**An issue that touches the extractor or the skill list takes longer, and that is the
gate working.** Its worker runs the dev eval before opening its PR (its skill's step 3a,
AGENTS.md "The eval gate"): about 60 model calls, a few minutes, cents. Let it finish —
a worker that looks stalled on an extractor issue is usually mid-eval. Two such workers
running at once is fine; they measure independently. What you must not do is wave a
missing score table through because the batch is slow.

**Never replace a ticket description** (HIR-124). Anything you put on a Linear issue is a
comment, or an append through `save_issue`'s `patch`. Two agents overwrote one ticket's
description on 3 Nov by each sending a whole new `description`; with several orchestrators
running, the one you overwrite may belong to a session you cannot see.

## 3. Review and merge

**Autopilot PR:** start the `reviewer` subagent (`.claude/agents/reviewer.md`) with the
PR number **and nothing else** (HIR-137). It reads the ticket itself, from the issue id in
the branch name — do not paste the issue's labels, its "Done when" list, or your own
account of what the worker did into its prompt. Your framing between the ticket and the
reviewer is exactly what it is meant to be reading around. The worker inside an
orchestrator does *not* review its own PR at the end of its run (its skill's step 5c tells
it to skip that when you started it) — reviewing is yours, so every autopilot PR gets
exactly one reviewer at a time.

The reviewer's reply starts with the verdict:

- **`MERGED` / `MERGING`** — done. A safety-check refusal of its merge command is not a
  failure: its `review-passed` label hands the merge to GitHub (AGENTS.md "Who merges").
- **`SENT BACK`** — the fixes are in its PR comment headed `**Review: sent back**`. The
  first time, send the worker one message (SendMessage): "PR #n was sent back; do the
  fixes in the latest `Review: sent back` comment per your skill's 'Fixing a sent-back
  PR', then report." If that worker has finished or is gone, start a fresh one the same
  way as in step 2 with `/work-issue HIR-n` — it finds the open, sent-back PR and fixes it
  on the same branch. **The second time, always a fresh worker on the strongest model**
  (`model: "fable"`; the ladder in AGENTS.md if it is unavailable), never the original
  one.
  When it reports, start a **fresh** reviewer with the PR number and nothing else. The
  reviewer counts the rounds: a third failure comes back as `NEEDS CHANDLER`, with no
  @mention.
- **`NEEDS CHANDLER`** — an item on his list (AGENTS.md "What Chandler is asked"), or a
  third failed review. Report it; never relabel it.

**Attended PR:** do not review, do not merge. List it under "Ready for you" with the PR
link and the worker's one-line summary.

**A PR touching `app/extract.py` or `taxonomy/skills.json` needs its `## Eval (dev)`
section before it can merge** (AGENTS.md "The eval gate"). The reviewer checks this
and you do not overrule it. When a batch produces two or more of them, note in your report
that each committed its own baseline run, and that the reviewer merges at most one
re-reads-every-job PR per calendar day — the rest wait, which is not a failure to report
as one. A flagged metric (down more than 0.02) goes under "Needs you" in Chandler's words,
with the metric named and the two runs compared.

**There is no merge queue** — GitHub offers one only on organization-owned repositories
and this one is personal (HIR-136). The reviewer merges a PR whose checks are already green
outright; on any other PR it arms GitHub's auto-merge and brings the branch up to date, and
that one is not merged the moment the reviewer passes it — it merges when the checks on the
updated branch go green (HIR-157). Treat both "merged" and "set to merge" as done for
reporting, and check back once on the second. A PR with a real conflict comes back `SENT
BACK`, like any other finding: the author resolves it.

Start queued issues as slots free up and their blockers merge. Before each one, re-read
the open PRs (step 1): other sessions have been merging while you worked.

## 4. Report

One message at the end, written for Chandler:

- **Merged or merging:** PR, issue, one line of what changed on the dashboard (or
  "internal"), and whether it is merged or still waiting on its checks.
- **Ready for you:** attended PRs waiting for your merge, one line each.
- **Sent back and fixed:** PR, issue, one line of what the reviewer asked for.
- **Needs you:** only items on Chandler's list, and PRs that failed review three times —
  PR, issue, the item or what is still wrong, in plain words.
- **Stopped:** issue, the question the decider couldn't answer (already on Linear with an
  @mention).
- **Re-extract:** whether a merge today has the model re-read the open jobs, yes or no —
  and if yes, what it costs, from `uv run python -m app reread-cost` (HIR-221).
- **Filed:** new tickets the workers created, with their labels.

Nothing else. No narration of the steps.
