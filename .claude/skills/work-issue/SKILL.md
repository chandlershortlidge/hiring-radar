---
name: work-issue
description: Take one Linear issue (HIR-n) from ticket to pull request — read the issue, get on its branch, follow its build steps, test, open the PR, update Linear. Runs unattended (autopilot) by default; add "attended" to be asked for a go. Use when the person says "work HIR-n", "do HIR-n", "pick up HIR-n", or invokes /work-issue.
---

# /work-issue HIR-n [attended]

One procedure for every issue, so the person never has to spell it out. The issue is the
plan; this skill only sequences the steps. AGENTS.md rules apply throughout (smallest
change, mock model calls, regression tests, report only what you ran).

## 0. Am I running the current rules?

Skills load from the folder the session was launched in. If that folder is on an old
branch, this file is old too. First thing: `git -C <launch folder> fetch origin main` and
compare `git rev-parse HEAD` with `origin/main`. If they differ and the folder is the main
checkout (not a worktree), say so and run `git switch main && git pull` there before
continuing, then re-read this file. If the folder is a worktree on a ticket branch, leave
it — but read `.claude/skills/work-issue/SKILL.md` and `AGENTS.md` from `origin/main`
(`git show origin/main:<path>`) and follow those.

## 1. Read the issue

- `get_issue` on the Linear MCP for HIR-n with `includeRelations`. If the MCP isn't
  available, stop and ask the person to paste the issue text; don't guess the scope.
- If it is **blocked by** an open issue, say so and stop. If it is **In Progress** with a
  status note at the top, continue from where the note says it stopped.
- Read its comments too (`list_comments`). A comment headed **Answered** is Chandler's
  answer to the ticket's question, as the lead agent recorded it (HIR-277): follow it,
  write it into DECISIONS.md in this PR where it is a rule, and if the ticket's open PR
  holds that question under "Needs Chandler", move it to "Decisions taken" with his
  answer quoted.
- Its "Build" / "Steps" section is the plan. Its "Tests" section is the test list. Its
  "Out of scope" section is binding. Anything you'd add beyond those: ask first.

## 1a. Claim it, before anything else (HIR-124)

**Set the issue to In Progress now** (`save_issue`, `state: "In Progress"`), before the
brief and before the worktree. This is the claim, and it is the only signal another
session gets: orchestrators skip In Progress issues when picking, so an issue you have
read but not claimed is an issue a second orchestrator will hand to a second worker.
Claim it the moment you have decided to work it — reading the issue is not claiming it.

If it is already In Progress and no status note says where a previous run stopped, a
session you cannot see may be on it: say so and stop.

## 1b. The brief (before any code)

Post one comment on the Linear issue (`save_comment`), written for someone who hasn't read
the code. Five lines, plain words, no file names:

- **Doing:** what will exist when this is done, in one sentence.
- **You'll see:** what changes for the person using the dashboard, and any cost. When the
  work will have the model re-read the stored jobs, run `uv run python -m app reread-cost`
  and give its figure; never a remembered number.
- **Deciding alone:** the judgment calls you expect to make (AGENTS.md "Deciding alone vs.
  stopping").
- **Will ask about:** anything on the big side of Chandler's list (AGENTS.md "What
  Chandler is asked" — the one source; don't copy it). A small call on that list is not
  asked: the senior agent decides it ("A small call on Chandler's list", below). If this line isn't "nothing", @mention
  Chandler in the comment and wait for the answer before step 3.
- **Not doing:** what the issue's out-of-scope says, in plain words.

**Autopilot is the default** (HIR-120). The run is *attended* only when the person wrote
`attended` after the issue id, or the issue carries the Linear label `attended`. Everything
else runs autopilot — including an issue with no label at all. First, before the brief,
add the label `autopilot` to the issue (`save_issue` with `addLabels: ["autopilot"]`):
that label is what the reviewer reads before merging, so without it the PR would sit. If the Linear MCP can't write the label, say so once in the
session and continue — the PR body's first line then says "autopilot run, label not set".

Autopilot means: post the brief on Linear for the record but do **not** wait for a "go";
start at once. Every question goes to the decider; if it returns ANSWER, apply it and
continue; if it returns SMALL CALL, the senior agent decides it. Only a NO RULE — which
the decider gives only for the big side of Chandler's list — reaches Chandler (Linear comment, @mention), and then stop. The
person sees nothing until the PR exists. You still never merge your own PR — at the end of
the run a fresh `reviewer` agent does it (step 5c).

What makes this safe is not the label but Chandler's list (AGENTS.md "What Chandler is
asked"), the reviewer's checks and the rules gate: those apply to every run, whatever the
default.

**Show the brief in the session as well as on Linear.** Posting the comment is not
briefing the person. In an attended run, print the five lines and wait for an OK
before step 2; "go" is enough. Autopilot: post it, print it, and continue unless "will
ask about" has something in it.

The final PR reports the difference from this brief, not the work itself.

## How to write anything Chandler reads (brief, questions, Decisions taken)

He has not read the code and does not remember rule dates. Every sentence passes this
test: *could someone who has never opened the repo say "fine" or "no" to it?*

- Say what changes on the dashboard, not what changes in the code. "61 new skills appear
  on the chart, most at 1–2%" — not "61 entries land in taxonomy v5".
- Never assume a rule is known. If a rule matters, restate it in one clause: "the rule
  that a skill needs 3 job postings before it goes on the chart".
- No file names, function names, ids or dates as shorthand. `proposed_skill` is "the
  queue of skills the model has suggested"; `extractor_version` bump is "every job still
  open gets re-read by the model once, about €X" — with €X from
  `uv run python -m app reread-cost`, not from memory.
- A question is: the situation in two sentences, then one line per option with its
  consequence, then your recommendation and why. Three options at most.
- Reread it as him before sending. If it needs the repo to make sense, rewrite it.

## 2. Session start (AGENTS.md "Starting a session", HIR-88 / HIR-94)

**Every issue gets its own worktree, and this step creates it.** A folder has one current
branch and one `TICKET`; two sessions in one folder put commits on each other's branches
no matter what the hooks check. So never `git switch` in the folder the session was
launched in.

1. `git branch --show-current`. If this folder is already a worktree on HIR-n's branch,
   go to step 4.
2. Call **EnterWorktree** with `name` = the Linear `gitBranchName` without the
   `chandlershortlidge/` prefix (e.g. `hir-14-cv-upload-pre-fill-profile-skills`). It
   creates `.claude/worktrees/<name>` from `origin/main` and moves this session into it.
   If the tool isn't available: `git worktree add ../<repo>-hir-n -b <gitBranchName>
   origin/main` and `cd` there.
3. `git branch --show-current` again. If the branch name doesn't contain `hir-n`, rename
   it: `git branch -m <linear gitBranchName>`. The pre-commit hook needs the id in the name.
4. In the worktree:
   ```bash
   echo HIR-n > TICKET
   git config core.hooksPath .githooks
   uv sync
   ```

Leave the worktree in place when done; Chandler removes it after the merge
(`git worktree remove`, or the prompt on session exit).

Uncommitted changes on the tree: stop and ask whose they are. Never stash or discard.

## 3. Build

- Follow the issue's steps in order. Hot spots (`app/migrations/`, `app/extract.py`,
  `app/pipeline.py`, `app/dedup.py`, `taxonomy/skills.json`) are one branch at a time: if
  another open branch touches one, say so before editing it. The open PRs are what you
  check, not what the session remembers: `gh api "repos/:owner/:repo/pulls?state=open"`
  then `gh api repos/:owner/:repo/pulls/<n>/files` for each.
- A new migration takes the next free number — check `ls app/migrations/` first, don't
  trust the number in the issue.
- If the issue asks for a **DECISIONS.md** entry, write it before the code it describes,
  newest-first with the date. If a step changes `app/extract.py`, the prompt or the taxonomy,
  run `uv run python -m app reread-cost` and say in the PR body that merging re-reads the
  open jobs, with that command's figure (HIR-221); the merge is the approval, so don't stop
  for it. Those same changes trigger the eval gate — step 3a.
- Any step the issue says to show the person before continuing (an eval table, a dry run,
  a confusion matrix): show it and **stop** until they answer.
- **A commit is a green checkpoint.** One commit per build step of the issue, made when
  that step is done and the tests pass. Never commit a red suite; never commit half a
  step — if a step can't be green in one go, it is two steps. Subject line names the
  step: `HIR-72 step 3: aliases for 15 phrases; 391 tests pass`. Push after every commit,
  so a killed session loses nothing. Any single commit is then a safe place to go back to.

## 3a. The eval gate (only if the diff touches the extractor or the skill list)

**Check this on every run, before step 4:** `git diff --name-only origin/main...HEAD`. If
it names `app/extract.py` or `taxonomy/skills.json`, AGENTS.md "The eval gate" applies and
the PR cannot merge without a score table. The trigger is that file list, not your
judgment about whether the change could move a score.

```bash
uv run python scripts/eval_table.py --version-check     # may this PR skip the eval?
```

**MATCH** — the committed baseline already scored this exact extractor, so a run would
re-measure something unchanged. Paste those two version lines into the PR body under a
`## Eval (dev)` heading, say the run was skipped and why, and go to step 4.

**DIFFERENT** — run it:

```bash
uv run python scripts/run_eval.py                       # dev split, 3 repeats, ~60 model calls
uv run python scripts/eval_table.py <run_id>            # the table for the PR body
```

Then, in one commit of its own:

- the whole `evals/results/<run_id>/` directory — **this is not optional.** The run a PR
  commits is the baseline the next extractor change is measured against; not committing it
  is what left skill-list v8 comparable only with v5.
- the table, pasted verbatim into the PR body under `## Eval (dev)`.

`eval_table.py` exits non-zero when a metric fell more than 0.02 against the baseline.
That is on Chandler's list (item 2), not a judgment call: commit the result directory anyway so the
number is on the record, put the table in the PR body with the flagged metric, label the
PR `needs-chandler`, @mention Chandler on the issue in plain words ("the model got worse at
X by Y against the last measured run"), and stop. Do not re-run the eval hoping for a
kinder number — three repeats is already the average, and picking the best of several runs
is tuning.

The eval needs an API key from `.env` at the repo root, and **a worktree has no `.env`** —
symlink it in before the run or the first call fails (see the session's memory on this).

## 4. Verify

```bash
uv run pytest -q                 # all green, or say exactly what fails and why
cd web && npm run build          # when web/ changed
```

Report numbers you saw, not numbers you expect.

## 5. Pull request

```bash
git push -u origin HEAD
gh api -X POST repos/:owner/:repo/pulls -f base=main -f head="$(git branch --show-current)" \
  -f title="<HIR-n: what changed>" -F body=@<file with the PR body>
```

Every GitHub command in this skill is `gh api` (HIR-151): `gh pr create`, `gh pr list`,
`gh pr edit`, `gh pr checks` and `gh pr merge` fail in a cloud run, where `gh auth status`
wrongly reports a bad token, and `gh api` works there and on the Mac. To change the body
later: `gh api -X PATCH repos/:owner/:repo/pulls/<n> -F body=@<file>`. To add a label:
`gh api -X POST repos/:owner/:repo/issues/<n>/labels -f 'labels[]=<label>'`.

**Do not merge `origin/main` into your branch first** (HIR-124, HIR-136). The reviewer
brings the branch up to date at the end, once, just before the merge — a branch that is
behind main is not something to fix before review. Merging main in by hand while other
sessions were merging is what produced the duplicate edits of 3 Nov. What *is* still yours
is a real conflict: the reviewer cannot update a branch that conflicts, so it hands the PR
back to you. Resolve it then, keeping both sides newest-first in DECISIONS.md.

PR body, in the template's sections: Testing, Risk, How to revert, **Decisions taken**,
**Decided for you** (the senior agent's small calls, or "None"), plus **`## Eval (dev)`** whenever step 3a applied — the reviewer refuses a PR that touches
the extractor or the skill list and has no such section, so an absent table reads as an
eval nobody ran, not as a clean one.
**Needs Chandler** and **Follow-ups** per AGENTS.md "Deciding alone vs. stopping". "Needs
Chandler" holds only what blocks the merge. A known limit, a later ticket or a suggestion
is a Follow-up, stated as a fact, never as a question — if it doesn't need an answer,
don't ask for one. Follow-ups come in two lists, **"Changes what you'd see"** first
(chart, job list, counts, which jobs get in or out — these are decisions in disguise and
Chandler reads them) and **"Internal"** second (refactors, tests, docs, tooling — he
doesn't). Same split in the Linear comment and the final reply: lead with the first list,
and if it's empty say so in four words. Write both for a reader
who hasn't seen the code: one sentence per decision — what, why, how to undo. Then a
one-paragraph delta from the brief: what differs from what you said you'd do. Any step from
the issue that was **not** done, named. If the issue is only partly done (e.g. the eval is still
to run), say which steps remain in the PR body and in a status line at the top of the
Linear issue; don't mark it Done.

**Writing that status line, and anything else on a Linear issue: append, never replace**
(HIR-124). Use `save_issue` with `patch` — `{"op": "prepend", "text": "..."}` for a status
line at the top, `insert_after` or `append` elsewhere — or just post a comment. Never send
a whole `description`: Chandler wrote it, and on 3 Nov two agents each sent a full
description and erased the other's edit. The only description you may replace outright is
one this session wrote.

## 5b. Follow-up tickets

Any ticket you file (a Follow-up that deserves one, a bug found on the way) gets the
`autopilot` label when it is one bounded change with nothing on the big side of
Chandler's list, per AGENTS.md; `attended` only when its work is on that big side.
Decide it at filing time; Chandler does not sort issues by hand.

## 5c. Review and merge, before the run ends (autopilot only, HIR-124)

**Skip this whole step if a `/work-issue-orchestrator` started you** — the orchestrator
reviews and merges your PR itself, and two reviewers on one PR is worse than none. Skip
it for an `attended` issue too: those always wait for Chandler.

Otherwise, an autopilot run finishes the job rather than leaving a PR for something else
to notice. There is no timer and no scheduled cloud reviewer; if you don't do this, nobody
does.

1. Wait for CI on the PR's head commit: poll
   `gh api repos/:owner/:repo/commits/<head sha>/check-runs --jq '.check_runs[] | [.name, .status, .conclusion] | @tsv'`
   until every check is `completed`.
2. Start the **`reviewer`** subagent (`.claude/agents/reviewer.md`) with the PR number and
   nothing else. It has fresh context and has not seen your work — that is the point, and
   it is why this does not count as merging your own PR. It fetches the ticket itself from
   the issue id in the branch name and checks the PR against the ticket's "Done when" list
   (HIR-137), so it needs nothing from you: do not summarise your work to it, do not paste
   the issue's labels or its "Done when" list, do not tell it what you concluded, and do
   not argue with its verdict.
3. Its reply starts with the verdict:
   - **`MERGED` / `MERGING`** — done. It labels the PR `review-passed`, merges it when the
     checks are already green, and otherwise brings the branch up to date so GitHub merges
     it when the checks on the updated branch pass (HIR-157, HIR-262). "Merging" is a
     normal end state to report. If it says "merge refused by the session's safety check;
     setup step missing", the PR still merges through GitHub; pass that sentence on
     verbatim in your reply, once.
   - **`SENT BACK`** — the fixes are in its PR comment headed `**Review: sent back**`. The
     first time, do them now ("Fixing a sent-back PR" below), wait for CI, and start a
     **fresh** reviewer — never the same one, and never with your account of the fixes.
     The second time, the fix is not yours: start a fresh subagent on the strongest model
     (`model: "fable"`, the ladder in AGENTS.md if it is unavailable) with the prompt
     `/work-issue HIR-n` and nothing else; it finds the sent-back PR and fixes it on the
     same branch. Then the fresh reviewer. The reviewer counts
     the rounds; after the second send-back a third failure comes back as `NEEDS
     CHANDLER` with no @mention.
   - **`NEEDS CHANDLER`** — leave the label alone and say so in your final reply.

If you cannot get this far — CI never goes green after your fixes, the reviewer can't be
started, the run is stopping for a NO RULE — **label the PR `needs-chandler` yourself and
say in your final reply that the PR is unmerged and why**. @mention Chandler only for a NO
RULE; the rest reach him in the Monday summary. A PR left with no label and no reviewer is
the one outcome this step exists to prevent.

## Fixing a sent-back PR

You are here because a reviewer sent your PR back, or because you were started as a fresh
worker with `/work-issue HIR-n` on an issue whose open PR carries the label `sent-back`
and no `review-passed` (the orchestrator does that when the original worker is gone).

1. Work on the PR's existing branch, in its own worktree (step 2, with the branch that
   exists rather than a new one). Never open a second PR.
2. Read the latest comment headed `**Review: sent back**`. Do exactly the fixes it lists,
   nothing more; a fix you think is wrong is a question for the decider, not a skip.
3. One commit per fix or one for all, each green, pushed. Add a line per fix to the PR
   body's "Decisions taken" only when the fix involved a judgment call.
4. Leave the `sent-back` label on: it is the record of what was sent back and fixed, for
   the Monday summary. Then step 5c from 1, unless an orchestrator started you: then stop
   and report, and it starts the reviewer.

## 6. Finish

- Linear: a comment with the PR link and the same "Needs Chandler" lines as the PR, with
  an @mention if there are any. Status
  stays In Progress until the PR merges (the GitHub integration closes it).
- Reply to the person with: the PR link, the test count, whether the PR is set to merge on
  its own or is waiting and why, and open questions — nothing else. No recap of the steps.

## Before any question reaches Chandler: the decider

Hand the question to the `decider` subagent (`.claude/agents/decider.md`). It reads only
the rule files and replies ANSWER + RULE, SMALL CALL ("A small call on Chandler's list",
below), or NO RULE + the question rewritten for Chandler.

If the spawn fails because the model is unavailable, use the model ladder in AGENTS.md
"Escalate to a stronger agent before a person" — written there and nowhere else. A
question the decider can't settle is a NO RULE, not a model problem.

ANSWER → apply it, one line under "Decisions taken" naming the rule (or the closest rule,
for a judgment the decider made where none fit exactly). NO RULE → post the
rewritten question on the Linear issue with an @mention of Chandler, do what doesn't
depend on it, stop. When his answer arrives, add it to DECISIONS.md in the same PR.

## A hard technical question: the senior agent

A design choice inside the ticket's scope, a bug you cannot find, or a test you cannot make
pass after two tries is not a question for Chandler and not one for the decider. Hand it to
the `senior` subagent (`.claude/agents/senior.md`) with the ticket id, the question, and
your notes: what you tried, what happened, the files involved. It answers DECISION +
REASON — carry it out and add a line under "Decisions taken" — or ON CHANDLER'S LIST with
the question already rewritten for him: post that on the Linear issue with an @mention, do
what doesn't depend on it, and stop.

## A small call on Chandler's list: the senior agent decides (HIR-278)

Chandler's list has a small side (AGENTS.md "What Chandler is asked", "Small calls"):
repairing a few stored jobs, a small recurring cost, a wording choice, the order of bugs.
He is not asked those. When the decider replies SMALL CALL:

1. Gather the proof it named, before asking anyone. For stored data: run the change on a
   **copy** of the database (never the live one), keep what you ran and what it changed,
   and list the backup bucket to show last night's backup is there (`rtk proxy` in front
   of the command: the hook clips cloud listings). For money: the figure and where the
   cost is switched off.
2. Hand the question, the decider's reply and that proof to the `senior` agent. You never
   decide it yourself, and you do not argue with its answer.
3. **DECISION + DECIDED FOR YOU** → carry it out. Copy its "Decided for you" line,
   unchanged, into the PR body under **Decided for you**, put the proof in the PR body
   under Testing, and add the usual line under Escalations. With no PR (a one-off run, a
   ticket that is only a question), post the line as a comment on the ticket headed
   **Decided for you**. No @mention: he reads it on Monday.
4. **ON CHANDLER'S LIST** → it was big after all. Post the rewritten question on the
   Linear issue with an @mention, do what doesn't depend on it, and stop.

Every call to the senior agent or the decider goes in the PR body under **Escalations**,
one line each: who asked, what, what was answered. "None" if there were none.

## When to break off and ask

The big side of Chandler's list in AGENTS.md "What Chandler is asked", plus: the work has grown past
the issue (propose the split). An issue that contradicts a standing rule is **not** a
reason to ask: the rule wins, note it under "Decisions taken". Asking
is a Linear comment with an @mention, one sentence and the options; then do whatever
doesn't depend on the answer, and stop.
