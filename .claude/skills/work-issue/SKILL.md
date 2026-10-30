---
name: work-issue
description: Take one Linear issue (HIR-n) from ticket to pull request — read the issue, get on its branch, follow its build steps, test, open the PR, update Linear. Use when the person says "work HIR-n", "do HIR-n", "pick up HIR-n", or invokes /work-issue.
---

# /work-issue HIR-n

One procedure for every issue, so the person never has to spell it out. The issue is the
plan; this skill only sequences the steps. AGENTS.md rules apply throughout (smallest
change, mock model calls, regression tests, report only what you ran).

## 1. Read the issue

- `get_issue` on the Linear MCP for HIR-n with `includeRelations`. If the MCP isn't
  available, stop and ask the person to paste the issue text; don't guess the scope.
- If it is **blocked by** an open issue, say so and stop. If it is **In Progress** with a
  status note at the top, continue from where the note says it stopped.
- Its "Build" / "Steps" section is the plan. Its "Tests" section is the test list. Its
  "Out of scope" section is binding. Anything you'd add beyond those: ask first.

## 2. Session start (AGENTS.md "Starting a session", HIR-88)

```bash
git switch main && git pull
git switch -c <linear gitBranchName>          # or git switch it if it exists
echo HIR-n > TICKET
git config core.hooksPath .githooks            # once per clone
```

Uncommitted changes on the tree: stop and ask whose they are. Never stash or discard.

Set the issue to **In Progress** in Linear (`save_issue`, `state: "In Progress"`).

## 3. Build

- Follow the issue's steps in order. Hot spots (`app/migrations/`, `app/extract.py`,
  `app/pipeline.py`, `taxonomy/skills.json`) are one branch at a time: if another open
  branch touches one, say so before editing it.
- A new migration takes the next free number — check `ls app/migrations/` first, don't
  trust the number in the issue.
- If the issue asks for a **DECISIONS.md** entry, write it before the code it describes,
  newest-first with the date. If a step changes `app/extract.py`, the prompt or the taxonomy,
  say in the PR that every job re-extracts on the next poll.
- Any step the issue says to show the person before continuing (an eval table, a dry run,
  a confusion matrix): show it and **stop** until they answer.
- Commit at working checkpoints. Commit messages: what changed and why, one paragraph,
  no step-by-step narration.

## 4. Verify

```bash
uv run pytest -q                 # all green, or say exactly what fails and why
cd web && npm run build          # when web/ changed
```

Report numbers you saw, not numbers you expect.

## 5. Pull request

```bash
git fetch origin main && git merge origin/main      # resolve, keep both sides in DECISIONS.md
git push -u origin HEAD
gh pr create --base main --fill
```

PR body: what and why in two or three sentences, the test count, and any step from the
issue that was **not** done, named. If the issue is only partly done (e.g. the eval is still
to run), say which steps remain in the PR body and in a status line at the top of the
Linear issue; don't mark it Done.

## 6. Finish

- Linear: `save_issue` with a one-line comment of what shipped and the PR link. Status
  stays In Progress until the PR merges (the GitHub integration closes it).
- Reply to the person with: the PR link, the test count, and open questions — nothing
  else. No recap of the steps.

## When to break off and ask

The issue contradicts DECISIONS.md or AGENTS.md; the branch and `TICKET` disagree; a
hot-spot file is already changed on another open branch; the fix needs a full re-extract
and one is already running; the work has grown past the issue (propose the split).
