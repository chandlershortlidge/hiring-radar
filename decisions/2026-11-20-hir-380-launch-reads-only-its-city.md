## 2026-11-20 — A city launch's first collection reads only that city's new jobs (HIR-380)

A launch's first collection runs on the Mac's copy of the database. A plain poll there
read every job waiting for a reading, not only the new city's: after a prompt change that
was hundreds of older jobs. Those readings stay on the Mac, because the server keeps its
own database and re-reads it itself. Twice the launch paid three to four times its
estimate for nothing: Hamburg, Frankfurt and Munich (8 Nov) about €10.50 against €3; San
Jose (20 Nov) €6.90 against €1.73, 822 older jobs read again.

**Decision.** The first collection is `uv run python -m app poll --launch "<city>" --only
<board> …`, and `discover-boards --launch` prints that command, with the added boards,
at the end of its report. With `--launch`, the poll:

- reads only the jobs that poll newly stored **and** placed in the launched city;
- prints that count and its price before reading, priced the same way as
  `python -m app reread-cost` (the average of recent readings, at the batch rate);
- stops, reading nothing, if that price is over the launch's €10 cap (unchanged);
- says how many jobs it left unread (new jobs placed in other cities, older jobs waiting
  in this copy) and why.

A poll without `--launch` is unchanged: the server's daily polls still read everything
waiting, which is how the server re-reads after a prompt change.

**Not chosen:** running the launch's collection on the server. It would make the readings
useful, but a launch is run from a ticket session on the Mac, and moving it means a remote
command path the launch does not have today. Reading less locally fixes the waste with
one option.

**Brave spend per launch** (each launch's board search runs every city's searches) is
its own ticket, HIR-363, and is not changed here.

**Undo:** drop `--launch` from the command; the poll then reads everything waiting, as
before.
