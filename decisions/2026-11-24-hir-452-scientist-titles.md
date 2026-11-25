## 2026-11-24 — A "scientist" title is sorted by the kind of scientist (HIR-452)

Chandler found five jobs under AI Engineer that are not AI engineering: Intercom's "Senior
Machine Learning Scientist", Zalando's "Senior Machine Learning Scientist / Data Engineer",
and three "AI Scientist" roles at mistral.ai.

**Why they were there.** The job family is decided from the title alone, by a short list of
phrases per family, tried in a fixed order; a title that matches no phrase is `ai-engineer`
(the rule of 5 Nov, "Job family is a title rule (v1)", HIR-186). The ticket guessed that
"AI" or "Machine Learning" was matched before "Scientist". It is not so: no family has
"AI" or "machine learning" as a phrase on its own. The `ml-engineer` row wants "machine
learning **engineer**", the `research` row wanted "research" or "**applied** scientist",
and the `data-scientist` row wants "data scien…". None of the five titles contains any of
those, so all five fell through every row to the remainder. The fault was missing phrases,
not their order.

**Decision** (Chandler, 24 Nov, on the ticket: "use the proposed defaults", titles only):

| title says | family |
| -- | -- |
| data scientist (`data scien`, `datenwissenschaft`) | `data-scientist`, unchanged |
| machine-learning scientist (`machine learning scientist`, `machine-learning scientist`, `ml scientist`, `ml-scientist`) | `ml-engineer` |
| any other `scientist` ("AI Scientist", "Research Scientist", "Applied Scientist") | `research` |

The row order is unchanged: data scientist, ML platform, ML engineer, research, then AI
engineer as the remainder. The rule does not read the posting, so it cannot tell a
machine-learning scientist who ships models from one who publishes; Chandler chose
`ml-engineer` for all of them.

**A title naming two roles.** The ticket says such a title "goes by its first role". The
rule of 5 Nov says it takes the earlier row of the list, wherever the role stands in the
title, and that rule is kept: "Senior Machine Learning Scientist / Data Engineer" is
`ml-engineer` either way, and changing how two-role titles are read would move titles this
ticket is not about ("ML Engineer / Data Scientist" is `data-scientist` today).

**Known limits.**

- The phrase reversed, "Research Scientist, Machine Learning" or "Scientist, Machine
  Learning", is `research`: the title does not say "machine learning scientist". If
  stored titles show that form in numbers, it becomes a phrase on the `ml-engineer` row.
- A German title with "Wissenschaftler" that is not "Datenwissenschaftler" still matches
  no row and stays `ai-engineer`.
- A scientist title is matched on the word alone, so "Scientist" in a title that is
  really engineering ("AI Engineer, Scientist Tools") is `research`.

**Stored jobs.** A migration re-labels every stored job with the full rule, so stored jobs
and new ones agree. The only jobs it can move are scientist titles that sat in
`ai-engineer`; a test holds it to that.

**To undo:** revert the change to the rule and add a migration that runs the 5 Nov rule
over every job again. Titles are untouched, so every job goes back where it was.
