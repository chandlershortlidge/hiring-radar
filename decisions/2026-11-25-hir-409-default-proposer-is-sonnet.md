## 2026-11-25 — the labelling tool's default proposer is Sonnet 5.5, because Haiku is now the extractor (HIR-409)

The proposer suggests an answer for a disputed label before the cross-family judge rules.
Its rule is unchanged from HIR-379: it must have no stake, so it is not the extractor,
either labeler, or the judge. HIR-379 chose Claude Haiku 5.5 as the cheapest model that met
the rule. HIR-409 made Haiku the extractor, so the default moves to Claude Sonnet 5.5, which
no longer reads postings live.

This replaces the default named in the 2026-11-20 proposer decision (HIR-379). HIR-381 and
HIR-387 name Haiku as the proposer; for runs after this date, read Sonnet.

**Cost:** Sonnet is 20x Haiku per token in `app/reread_cost.py`, so HIR-379's €0.20 for
eight batches becomes about €4–5, roughly €0.50 a batch. `propose` runs only when someone
runs it, and `--model` picks another model on any run.

**What would show this wrong:** the judge agreeing with Sonnet's proposals above about 95%
of the time (a sign it anchors on them), or the first batch costing more than about €1.25.

**Undo:** pass `--model claude-haiku-5-5` (valid only while the extractor is not Haiku), or
set `DEFAULT_PROPOSER` back in `scripts/agent_label.py`.

Decided by the senior agent as a small call (Chandler's list, "a small recurring cost").
