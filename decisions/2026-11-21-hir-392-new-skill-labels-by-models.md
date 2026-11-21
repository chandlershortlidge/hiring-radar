## 2026-11-21 — A new skill's labels in an unwritten labelling batch are queued from the labelers' "no such skill" flags and settled by two models (HIR-392)

**The rule.** When a skill is added to the skill list while a labelling batch's answer keys
are not yet written, every place a labeler flagged that skill as missing from the list (the
batch's `unmapped` labels) becomes a queue item with the label drafted by the guide's
section rule (required section → `required`, preferred / nice-to-have → `nice_to_have`;
duties and the company description get no label). Both labelers flagged it → a
`rule-change` item showing the draft as the agreed label (`ok` / `drop` / JSON). One
labeler flagged it → a `disagreement` item with only that side. The proposer and the
cross-family judge then settle them like any other item; a split stays `?` for Chandler.
A label the judge already decided under a broader skill moves with a JSON override,
`{"skill_id": "<new id>"}`, which keeps the judge's requirement and quote; the item's key
moves with it, and labeler A's line stays as A wrote it.

**The "any one of" question is re-read.** Each such posting's `groups` item now offers the
new skill, so a settled grouping is re-opened (decision back to `?`, its proposal and its
model record removed) and the same two models answer it again. One still open for Chandler
just gets the new id in its list.

**The worker never writes a decision.** `apply` records any decision the models did not
make as a person's, so a worker-written line would be false provenance in the answer key.

**Why.** Chandler, 20 Nov: "yes, agent harnesses, add it", and the ticket says the hits are
relabelled. Once the skill list merges the extractor starts tagging these phrases, so an
answer key without the label would count it wrong. Two models from two companies agreeing
is the bar every other label in these batches settled at
(`2026-11-20-hir-381-degree-relabel-by-models.md`, `2026-11-20-hir-387-any-one-of-groups-by-models.md`);
and the 2026-10-20 rule holds that a label the skill list could not express before is a
missing answer-key label, so adding it is driven by the skill list, not tuning.

**How to undo.** Remove the appended items (the `rule_change` record with key
`agent-harnesses` in each batch's `adjudication.json` lists them) from `items.json` and
`review_queue.md`, and set golden_103's item 33 back to `A` under `agent-architecture`.
