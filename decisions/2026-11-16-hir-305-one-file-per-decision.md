## 2026-11-16 — Each decision is its own file, and a pull request that collides with main is repaired by the next lead agent run (HIR-305)

**What happened.** Chandler, 15 Nov: "I have two PRs that didn't merge because of
conflicts that needed to be resolved. What can we do about that?" Since the lead agent
began running every four hours, several tickets are built at once, and most of them add
an entry at the top of `DECISIONS.md`. Two pull requests that add text at the same place
in one file collide: the one that merges second can no longer merge. A test merge of the
"what's rising" pull request (#186) into main on 15 Nov showed the decisions log was its
only collision. And nothing picked such a pull request up again: the lead agent restarted
work a reviewer had sent back, but a pull request GitHub reports as conflicted just sat.

**How often.** Of the last 40 merged pull requests (counted 16 Nov), 13 changed
`DECISIONS.md`. No other file comes close to that for *added* text at one place: the
agents' manual was changed by 8, the lead agent's instructions by 7, `app/check.py` by 7,
the command-line entry point by 6, the work-issue and orchestrator instructions by 5
each. Those are edits spread through a file, which collide only when two tickets change
the same paragraph; the lead agent's one-ticket-per-area rule already keeps two tickets
on the agents' rules from running together. Only the decisions log is fixed here.

**Decision 1: one file per decision.** A new decision is a new file in `decisions/`,
named `YYYY-MM-DD-hir-N-short-title.md` (the date it was decided, the ticket, a few
words), and starting with the same heading an entry has always had:
`## YYYY-MM-DD — what was decided (HIR-N)`. Two pull requests that each record a decision
now add two different files and cannot collide. A second decision in the same ticket on
the same day gets its own file with a different short title.

- `DECISIONS.md` keeps every entry up to 16 Nov 2026 where it is, unchanged and not
  reordered. Its opening lines now say that newer entries are in the folder.
- **To read the log:** the files in `decisions/` (the names sort by date, newest last),
  then `DECISIONS.md`. A reference such as "DECISIONS 2026-11-20" means the entry with
  that date, in whichever of the two it is.
- `tests/test_decisions.py` checks every file in the folder has that name and that
  heading, with the same date in both. It runs with the ordinary tests.

*Not done, on purpose:* the ticket offered two shapes for `DECISIONS.md`, a short index
of the entries, or a file built from the folder by a script and checked in CI. Both are
one checked-in file that every pull request recording a decision would have to change at
the same place, which is the collision this ticket removes. So there is no per-entry
list anywhere; the folder listing is the index. To undo: add the list, and accept that
it collides.

*Not done, on purpose:* a check that fails when a new entry is added to `DECISIONS.md`.
Pull requests already open when this merges carry such entries, and some are waiting for
Chandler's own merge; a check that turns them red the moment they are brought up to date
would put a new obstacle exactly where this ticket removes one. An entry that still
lands in the old file does no harm beyond the old risk of a collision.

*Tried and ruled out:* a `.gitattributes` line telling git to keep both sides of
`DECISIONS.md` (`merge=union`). GitHub's own merge and its "update branch" button do not
run it, so it would help only merges made on a laptop.

**Decision 2: a collided pull request is repaired without Chandler.** Each lead agent run
lists the open pull requests GitHub reports as conflicted (`mergeable_state` `dirty`).
`scripts/lead_pick.py` says which may be repaired in this run; for each the lead agent
starts a worker with `/work-issue HIR-n repair`, which brings the latest main into the
pull request's branch, and then a fresh reviewer, as after any change. (A pull request a
reviewer had already sent back gets no reviewer yet: once repaired, its ticket goes back
to Todo so a worker does the fixes that are still open.)

The repair worker's rules, in `/work-issue` "Repairing a collided pull request":

- **Where both sides only added text to a prose file (a log, a list in a `.md` file):
  keep both.** `scripts/collision.py` does this, not the worker's judgment: it reads
  git's three versions of each collided file and keeps both additions only when neither
  side changed or removed a line the other also touched.
- **Everything else is not guessed at.** The same lines changed on both sides, a file one
  side deleted, and *any* collision in a code or data file, even one where both sides
  only added lines: the script lists the file, and the worker hands it to the senior
  agent with both versions. Two functions added at the same place can both be right or
  can break each other, and telling which is a judgment.
- **If the senior agent cannot settle it,** because the answer would decide something on
  Chandler's list, it writes the three lines of a recommendation, the worker posts them
  on the ticket under **To approve**, undoes the merge and stops.
- The worker changes nothing else: no fixes, no labels, no new work.

**What the lead agent may not repair** is code (`repairs` in `scripts/lead_pick.py`):

- a pull request whose repair has **failed twice**: it is listed under "Needs you" and
  waits for Monday, like a ticket that failed twice;
- a ticket labelled `hands-on` or `parked`: those are Chandler's;
- a ticket labelled `attended` whose pull request is **not** labelled `needs-chandler`:
  he is working in it. A pull request that is only waiting for his answer or his merge
  (labelled `needs-chandler`, which includes every change to the agents' own rules) *is*
  repaired, because he cannot merge a conflicted pull request and bringing main in
  decides nothing for him. Its labels are not touched and no reviewer is started on it;
- a pull request a run may still be working on (a push in the last hour, or a log line
  still `running`);
- anything, when the day's spending cap is zero or spent or the usage limit was hit.

A repair is written in the lead agent's log as its own line, `- repair #186 (HIR-232) |
… | result: … | spend: €0.00`, so it is counted apart from the ticket's own tries: a
failed repair is not a failed ticket, and the other way round.

**What cannot be shown before this merges.** "A deliberately collided test pull request
is repaired, reviewed and merged by the next lead agent run" needs the new instructions
to be the ones the lead agent loads, which happens only after the merge (AGENTS.md "A
change to an agent's instructions takes effect in the next session"). What was checked
instead is in the pull request.

**To undo.** Revert the pull request. Entries already written to `decisions/` stay
readable as files; move them to the top of `DECISIONS.md` if the folder is to go.
