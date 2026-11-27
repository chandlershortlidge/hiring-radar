## 2026-11-27 — A change to how postings are read also re-reads the closed jobs of the last 8 weeks (HIR-303)

**What was decided.** Chandler, 16 Nov, in the ticket: after an extractor change (the
instructions, the model, or the skill list and its spellings), also re-read the closed jobs
inside the "What's rising" panel's two 4-week periods, so both periods are read the same
way. The cost stays small and bounded however long the site runs. The long-term question,
re-reading every stored posting with each better extractor so rising and falling can be
measured over all time, stays open: he wants the cost of a full re-read estimated and
reported, and will decide once he has tested how extraction is done.

**Why.** Since HIR-195 a version bump re-read only open jobs. The panel compares the last
28 days with the 28 before, and the earlier period is mostly jobs that have since closed.
Those kept their old reading, so a skill that gained spellings, or every skill after a
prompt change, could rise or fall on the panel because of our change and not the market
(the "Known limit" in the 2026-11-14 HIR-232 entry).

**What that means in practice.**

- The re-read queue takes every stale-stamped job that was open at any moment in the last
  `2 × RISING_DAYS` days, by the panel's own rule for "open during a period"
  (`queries.open_clause` asked as of the earlier period's start). That is the same set of
  jobs the panel counts, so the two cannot drift: change `RISING_DAYS` and the re-read
  window moves with it.
- Jobs that closed before that stay as HIR-195 left them: their old skills and old stamp.
  A job never read at all is still read whatever its status.
- The targeted re-read for added skills (HIR-224) uses the same queue, so a skill that
  gains spellings re-reads the in-window closed jobs naming it, and carries the rest over.
- `python -m app reread-cost` counts the wider queue, and adds a line for re-reading every
  stored posting (legacy imports excepted: they hold a summary, not the posting). That line
  is the estimate Chandler asked for; it is a figure, not a decision.
- The 2026-11-14 HIR-232 "Known limit" is fixed by this. The rule in that entry that a
  brand-new skill is left off the panel until it has been on the list for both periods is
  unchanged.

**Undo.** In `app/pipeline.py`, have `reread_window_clause` return `open_clause(now)` again.
