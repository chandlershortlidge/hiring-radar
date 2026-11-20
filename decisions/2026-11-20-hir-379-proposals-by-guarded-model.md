## 2026-11-20 — The proposed answer the judge rules on is written by a model with no stake in the run (HIR-379)

**The rule.** In a labelling batch, the proposed answer to each disagreement (the line the
judge model then accepts or rejects) is written by a model that is neither of the two
labelers, nor the extractor, nor the judge. The labelling tool now has a step that does
this with a fixed model (`claude-haiku-5-5` by default), refuses a model with a stake, and
the judge refuses to rule on proposals its own model wrote. An item counts as settled only
when two different models, from two different families, agree on it.

**Why.** On 27 Oct the proposals were written by hand by the assistant session doing the
review, then a Gemini judge ruled on them. For the eight city batches of 19 Nov that would
be about 520 proposals, and the worker session runs on the same model as labeler A: labeler
A would be proposing the answer to its own disagreements, and the judge would only be
confirming it. The rule that keeps the extractor and the labelers out of the judge's and the
third labeler's seat (HIR-70) applies to the proposer for the same reason.

**Why the small model.** A larger Claude model (Fable 5.1) was measured on four real items at
about 4 cents each, about €17 for the ~520 items: over the €10 line for a one-off spend. The
small model costs about 20 cents in total. A weaker proposer can only lengthen Chandler's
queue, not settle a wrong answer, because nothing settles unless the cross-family judge
agrees. If the judge agrees with fewer than about half the proposals, the stronger
proposer is worth asking for.

**What else.** The proposer and labeler A are both Claude models; that was also true on
27 Oct. The judge is the cross-family reader. If the judge agrees with the proposer far more
often than it did on 27 Oct (50 of 70 then; above roughly 95% now), it is likely anchoring
on the proposal rather than reading, and the settled count should not be taken at face
value.

Degree items in batches labelled before the 19 Nov degree rule (record the lowest level
named) are left for a person: neither the proposer nor the third labeler settles them
(`--skip-key degree`), as the HIR-245 decision says.

**How to undo.** Write the PROPOSED lines by hand again and stop using `propose`; the judge
still reads them the same way.
