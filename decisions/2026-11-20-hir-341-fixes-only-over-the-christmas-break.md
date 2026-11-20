## 2026-11-20 — Over the Christmas break agents only fix what breaks (HIR-341)

Chandler, 17 Nov: the site is finished and live on 16 Dec, then he leaves it alone for
about two weeks; the public push comes in early January. Over the break agents keep
repairing what breaks and ship nothing new.

**Decision.** One line in `config/lead_agent.json` is the whole mode:

    "fixes_only": {"from": "2026-12-16", "until": null},

`from` is the first day in the mode; `until` is the last day in it, or `null` for "until
Chandler turns it off". While it is on:

- the scheduled run starts only a ticket labelled `Bug`, or the repair for a check that
  is red right now. Every other ticket stays in Todo;
- the reviewer still reviews, but a pull request whose ticket is not labelled `Bug` is
  left open with no label, and one whose ticket is gets the pull-request label `fix`;
- GitHub's own merger merges nothing without that `fix` label, so a feature that was
  already passed before the break began cannot slip through;
- the Monday summary, Monday's pace and each run's log open with one sentence saying so.

The caretaker, the robot visitor and the automatic rollback are not touched.

**A fix is the `Bug` label, not a reading of the ticket's text.** A label is something
code can check and Chandler can see; the lead agent gives it to a ticket that reports
something broken on the live site or in the daily collection, and to nothing else.

**The end date is the last day in the mode**, because "until 10 January" read aloud
means the 10th is still quiet.

**A date that cannot be read stops the run with an error**; it is never taken as "off".
A typo in the one line must not quietly end the break.

**Not chosen:** pausing the scheduled task. That is the off switch for everything, and it
would stop the repairs too.

**Undo:** make the line `"fixes_only": null`. Chandler merges that change himself: while
the mode is on, it is not a fix, so nothing merges it for him.
