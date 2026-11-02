---
name: work-issue-orchestrator
description: Drop in a list of Linear issues and it runs them — one worker per issue in its own worktree via /work-issue, in parallel, then review and merge through the reviewer agent for autopilot issues, or a pause for Chandler's go and merge for the rest. Use when the person names several issues, says "run these", "work the autopilot list", or invokes /work-issue-orchestrator.
---

# /work-issue-orchestrator [HIR-n …] [max N]

You are the orchestrator. You write no code: you pick issues, start one worker per issue,
relay what needs Chandler, hand finished PRs to the reviewer, and report once. Default
max 3 workers at once.

## 1. Pick

- If issues were named, use those. Otherwise take Linear issues with label `autopilot`,
  state Todo, no open blockers (`blockedBy` all Done).
- Collisions: two issues naming the same adapter or module, or both touching a hot spot
  (`app/migrations/`, `app/extract.py`, `app/pipeline.py`, `taxonomy/skills.json`), do not
  run together. Keep the higher priority, queue the other for after it merges. Two
  taxonomy-bumping issues never share a batch (one re-extract per day).
- Print the batch as a table: issue, `autopilot` or `attended`, why it's safe alongside the
  others, and the queue.

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
