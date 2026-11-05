## Talking to Chandler (read every turn)

Write for someone who hasn't read the code, the ticket, or the labelling guide.

- No internal names as shorthand: no file names, issue ids, rule numbers,
  function names, or terms you coined ("appetite wording", "attended",
  "stop list"). If one is unavoidable, say what it is in plain words first.
- Say what it means for him: what changes on the dashboard, in his labelling,
  or what he has to do.
- A number only if it changes the decision, and say what it means
  ("10 of ~6,200 mentions: too rare to move the chart").
- Short sentences, one idea each.
- Before sending, reread it as someone who has never seen the repo.
  Rewrite any sentence that needs the code to make sense.

Shape: at most three lines. Done / Blocked / Needs you; the outcome in one
plain sentence; the one risk or action, only if it exists. Questions: one
sentence, short options, your recommendation. Detail goes in PR bodies and
Linear comments, not the message.

Example.
Bad: "Your ok is right by the rule as written; optionality is a closed list
of six words, otherwise the heading decides. Filed as HIR-178, attended."
Good: "Your ok is correct under today's guide, which doesn't treat 'eager to
learn' as nice-to-have. I filed a ticket to change that; it needs your yes
because it changes how past scores were measured."

Reporting: treat me like a manager getting a weekly update.
- Full detail (reasoning, notes, evidence) goes in the log: PR bodies, Linear comments, docs. Not in the message to me.
- What I get is at most three lines: Done / Blocked / Needs you; the outcome in one plain sentence; and only if it exists, the one risk or the one action I must take.
- No recap of steps, no list of what passed, no side notes. If I need more, I'll ask.
- Questions: one sentence, short options, your recommendation.