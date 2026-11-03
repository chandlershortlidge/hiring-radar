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

## 3. Review and merge

**Autopilot PR:** start the `reviewer` subagent (`.claude/agents/reviewer.md`) with the
PR number. It merges or labels `needs-chandler`.

**Attended PR:** do not review, do not merge. List it under "Ready for you" with the PR
link and the worker's one-line summary.

Start queued issues as slots free up and their blockers merge.

## 4. Report

One message at the end, written for Chandler:

- **Merged:** PR, issue, one line of what changed on the dashboard (or "internal").
- **Ready for you:** attended PRs waiting for your merge, one line each.
- **Needs you:** PR, issue, the failing check or open question in plain words.
- **Stopped:** issue, the question the decider couldn't answer (already on Linear with an
  @mention).
- **Re-extract:** whether a merge today re-reads every job (~€3), yes or no.
- **Filed:** new tickets the workers created, with their labels.

Nothing else. No narration of the steps.
