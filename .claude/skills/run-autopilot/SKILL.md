---
name: run-autopilot
description: Run a batch of autopilot issues end to end — pick the unblocked ones that don't share files, work each in its own worktree with /work-issue, then review and merge with the reviewer agent. Use when the person says "run the autopilot list", "run HIR-a, HIR-b, HIR-c", or invokes /run-autopilot.
---

# /run-autopilot [HIR-n …] [max N]

You are the orchestrator. You write no code yourself: you pick issues, start one worker
per issue, wait, then hand each PR to the reviewer. Default max 3 workers at once.

## 1. Pick

- If issues were named, use those. Otherwise list Linear issues with label `autopilot`,
  state Todo, no open blockers (`blockedBy` all Done).
- Drop any that would collide: two issues naming the same adapter, the same module, or
  both touching a hot spot (`app/migrations/`, `app/extract.py`, `app/pipeline.py`,
  `taxonomy/skills.json`). Of a colliding pair, keep the higher priority and queue the
  other for after it merges. Two taxonomy-bumping issues never run in the same batch
  (one re-extract per day; the reviewer enforces it too).
- Print the batch as a table: issue, title, why it's safe to run alongside the others,
  and the queue of what waits.

## 2. Work

For each issue in the batch, start a subagent with `isolation: "worktree"` and the prompt
`/work-issue HIR-n` and nothing else. Run them in parallel, up to the max. Each follows the
work-issue skill: brief posted to Linear, own branch, green commits, PR, follow-up tickets
filed with the autopilot rule.

Do not answer a worker's questions yourself. A worker that stops on a NO RULE has done the
right thing; note it and move on.

## 3. Review and merge

When a worker reports a PR, start the `reviewer` subagent (`.claude/agents/reviewer.md`)
with the PR number. It merges or labels `needs-chandler`. Start queued issues as slots
free up and their blockers merge.

## 4. Report

One message at the end, written for Chandler:

- **Merged:** PR, issue, one line of what changed on the dashboard (or "internal").
- **Needs you:** PR, issue, the failing check in plain words.
- **Stopped:** issue, the question the decider couldn't answer (already on Linear with an
  @mention).
- **Re-extract:** whether a merge today re-reads every job (~€3), yes or no.
- **Filed:** new tickets the workers created, with their labels.

Nothing else. No narration of the steps.
