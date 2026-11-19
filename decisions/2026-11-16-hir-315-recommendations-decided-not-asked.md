## 2026-11-16 — A recommendation Chandler would only approve is decided for him; a question to think about is his for one week (HIR-315)

**What happened.** Chandler, 16 Nov, morning: "For now I can only handle one major
decision per week. The rest just go with whatever you think best or we'll never get this
done." His week's order: Python practice, design reviews, the internship, then this
project. The ticket was written from that: one question a week, everything else decided.

The same day, after talking that Monday's three questions through with Claude by voice
(about five minutes each), he changed it in a comment on the ticket: remove the
one-decision-a-week limit; decisions to think about get talked through by voice instead;
"recommendations stay the default when he hasn't talked a decision through".

**Decision 1: a recommendation to approve is decided, not asked.** Since 14 Nov a big
call reached him in one of two forms: a full question to think about, or three lines to
say yes or no to. The second kind is no longer put to him. The senior agent takes its
own written recommendation the moment the call comes up, and Monday's summary reports it
under "Decided for you", one line each, with how to undo it. He reverses any of them by
replying on the ticket.

**Decision 2: a question to think about is still his, for one week.** It is listed on
Monday as before, with no limit of one a week (the earlier limit of three per Monday
list stays; the rest are listed the Monday after). He talks it through with Claude by
voice, or answers on the ticket. When a Monday list has shown it and seven days have
passed with no answer, the senior agent takes the written recommendation and it is
reported under "Decided for you" like the others. A question no Monday list has shown
him is never decided this way.

The week is this entry's reading of "recommendations stay the default when he hasn't
talked a decision through". The comment does not say how long a question waits. Two
readings were possible: decide every such question at once and let him talk any of them
through afterwards, or let each wait for him first. The second was taken because it
hands agents less: what he wants to work out himself is not settled before he has seen
it. To change the wait, change `THINK_DAYS` in `scripts/lead_pick.py`; `0` is the first
reading.

**Decision 3: what still waits for him.** Three things are never decided this way.

- **Money.** A spend above €10 at once, or a new recurring cost above €10 a week, waits
  for his yes however long that takes.
- **Stored data.** Deleting stored jobs, or repairing more than 5, is decided only with
  a trial on a copy of the database and last night's backup in hand. Without them the
  worker gets them; nobody is asked, and nothing is deleted.
- **How quality is measured.** It is always a question to think about, so it always gets
  its week. If the recommendation is then taken, the reason is written into this log in
  the same pull request.

**Decision 4: actions only he can take are not decisions.** A merge that the rules gate
or the labelling guide requires from him; a credential, account, payment or setting only
he can change; work that has to be run by hand on his Mac or on the server. These go
under "Yours this week" on Monday, one line each, at most three; the rest wait.

**Decision 5: the lead agent's speed limit is unchanged.** It already counted only the
decisions waiting for him to think about (14 Nov). With recommendations decided at once
and questions decided after a week, that pile stays short, so it rarely holds work back.

**What was not done.** The tickets waiting on him on 16 Nov were not re-sorted in this
pull request: a change to the agents' rules takes effect only after he merges it. The
first lead agent run after the merge hands every waiting recommendation to the senior
agent. That Monday's seven recommendations and two of its three questions were already
answered on their tickets with the recommendation.

**How to undo.** Revert the pull request. Every call decided this way has its own undo
in its "Decided for you" line.
