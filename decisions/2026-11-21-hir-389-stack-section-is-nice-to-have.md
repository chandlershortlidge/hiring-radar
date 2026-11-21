## 2026-11-21 — A tool named only in the company's own tech-stack section or opening paragraph is nice-to-have, not required (HIR-389)

**The rule.** It replaces the labelling guide's old rule 4 ("an unmarked item in a
tech-stack list is required").

- A tool that appears **only** in a section describing the company's own tools or stack
  ("Our stack", "Tech stack", "We work with…", "Our tools", "In unseren Projekten verwenden
  wir…") counts as **nice-to-have**.
- If the same tool is also asked for in a requirements section, the requirement decides:
  the stack mention adds nothing. (A requirement marked optional — "preferably", "bonus" —
  stays nice-to-have; the stack does not upgrade it.)
- An explicit word in the stack section still decides: "you'll need", "must", "required"
  → required.
- A stack line inside a requirements list ("Experience with our stack: Python, Postgres")
  is a requirement, not a stack section.
- A tool named only in the company's opening paragraph, describing what the company runs
  ("we work … primarily on AWS"), is nice-to-have by the same rule. A sentence in the
  opening that describes the candidate sought ("we are looking for engineers skilled in
  X") is an ask, not the company's tools, and is labelled as any other ask.

Chandler, 20 Nov 17:46, on random check batch 10 (a posting whose separate "Our Stack"
section listed MySQL, PostgreSQL, Snowflake, AWS, all labelled required): "we need it for
sure".

**Why.** A stack section describes what the company runs, not what it asks a candidate to
bring. Counting every listed tool as required made jobs look more demanding than they are
and pushed down every visitor's fit score.

**What it changes in the answer keys.** Every key whose required skill rested only on a
stack section or a company-tools opening was relabelled in the same change; the pull
request lists each one. This moves the "required vs nice-to-have" score's meaning, so
results before this change are not comparable on that metric.

**Order with other work (Chandler, 21 Nov).** The eight city batches of 19 Nov get their
answer keys written after this change, under this rule. The switch to the cheaper model
(HIR-409) stays its own change but shares this change's re-read of the stored jobs: merge
this, merge the switch, then one re-read on the cheaper model.
