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

## 1b. The brief (before any code)

Post one comment on the Linear issue (`save_comment`), written for someone who hasn't read
the code. Five lines, plain words, no file names:

- **Doing:** what will exist when this is done, in one sentence.
- **You'll see:** what changes for the person using the dashboard, and any cost (a full
  re-extract is about €3).
- **Deciding alone:** the judgment calls you expect to make (AGENTS.md "Deciding alone vs.
  stopping").
- **Will ask about:** anything on the stop list. If this line isn't "nothing", @mention
  Chandler in the comment and wait for the answer before step 3.
- **Not doing:** what the issue's out-of-scope says, in plain words.

**Show the brief in the session as well as on Linear.** Posting the comment is not
briefing the person. In an attended session, print the five lines and wait for an OK
before step 2; "go" is enough. Unattended, post it and continue unless "will ask about"
has something in it.

The final PR reports the difference from this brief, not the work itself.

## How to write anything Chandler reads (brief, questions, Decisions taken)

He has not read the code and does not remember rule dates. Every sentence passes this
test: *could someone who has never opened the repo say "fine" or "no" to it?*

- Say what changes on the dashboard, not what changes in the code. "61 new skills appear
  on the chart, most at 1–2%" — not "61 entries land in taxonomy v5".
- Never assume a rule is known. If a rule matters, restate it in one clause: "the rule
  that a skill needs 3 job postings before it goes on the chart".
- No file names, function names, ids or dates as shorthand. `proposed_skill` is "the
  queue of skills the model has suggested"; `extractor_version` bump is "every job gets
  re-read by the model once, about €3".
- A question is: the situation in two sentences, then one line per option with its
  consequence, then your recommendation and why. Three options at most.
- Reread it as him before sending. If it needs the repo to make sense, rewrite it.

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
- **A commit is a green checkpoint.** One commit per build step of the issue, made when
  that step is done and the tests pass. Never commit a red suite; never commit half a
  step — if a step can't be green in one go, it is two steps. Subject line names the
  step: `HIR-72 step 3: aliases for 15 phrases; 391 tests pass`. Push after every commit,
  so a killed session loses nothing. Any single commit is then a safe place to go back to.

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

PR body, in the template's sections: Testing, Risk, How to revert, and **Decisions taken**
and **Needs Chandler** per AGENTS.md "Deciding alone vs. stopping". Write both for a reader
who hasn't seen the code: one sentence per decision — what, why, how to undo. Then a
one-paragraph delta from the brief: what differs from what you said you'd do. Any step from
the issue that was **not** done, named. If the issue is only partly done (e.g. the eval is still
to run), say which steps remain in the PR body and in a status line at the top of the
Linear issue; don't mark it Done.

## 6. Finish

- Linear: a comment with the PR link and the same "Needs Chandler" lines as the PR, with
  an @mention if there are any. Status
  stays In Progress until the PR merges (the GitHub integration closes it).
- Reply to the person with: the PR link, the test count, and open questions — nothing
  else. No recap of the steps.

## When to break off and ask

The stop list in AGENTS.md "Deciding alone vs. stopping", plus: the issue contradicts
DECISIONS.md or AGENTS.md; the work has grown past the issue (propose the split). Asking
is a Linear comment with an @mention, one sentence and the options; then do whatever
doesn't depend on the answer, and stop.
