## 2026-11-19 — The caretaker acts through a filed ticket and the normal pull-request path; the server gets no GitHub credential (HIR-261)

The caretaker is the program on the server that checks every job source each morning.
For its first week it only wrote down what it would fix. From this change it acts.

**Decision 1: a fix to the list of job sources is filed as a ticket, not written on the
server.** Each morning's fixes (pause a dead company board, switch a moved one, switch a
recovered one back on) go into one Linear ticket, "Caretaker: job-source fixes for
<day>". The ticket holds the exact edits and the one command that makes them
(`python -m app caretaker apply-fixes`). The agents' ordinary path picks the ticket up,
runs the command, and opens a pull request that changes only `config/feeds.json`. That
pull request gets the same checks, review and revert as any other change. The server
never edits the file and never talks to GitHub.

**Decision 2: a failed morning is re-run on the server, once, with no pull request.**
When the day's collection did not run, or every source failed, the caretaker starts the
Europe collection again as the same user, with the same settings as the 07:00 run. It
does this once per day and records that it did. This is the day's normal model spend
made late, not new spend; the caretaker itself still calls no model.

**Decision 3: a fix already filed is not filed again for 7 days.** A dead board is found
again every morning until the pull request that pauses it is merged and deployed.
Without this, each of those mornings would file the same fix. After 7 days a fix still
not applied is filed again, as a reminder.

**Not chosen: a GitHub credential on the server**, which is what the ticket first
assumed. It would be a long-lived write credential on a server that faces the internet,
only Chandler could create it, and he would have to rotate it. The 1 Nov deploy decision
(HIR-74) already rejected long-lived credentials where another path exists.

**Not chosen: a scheduled GitHub Actions workflow that opens the pull request.** A pull
request opened with the workflow's own token starts no checks, so it could never merge;
it would need a stored token anyway.

**The cost** is latency: a fix lands at the lead agent's next run that day, not at 10:00.
If filed tickets sit unpicked for days, the answer is a higher sort priority for
caretaker tickets, as a separate ticket.

**Undo:** set `MODE = "report"` in `app/caretaker_run.py`. The caretaker then files no
fix ticket and re-runs nothing, and the Monday summary says "would have" again.
