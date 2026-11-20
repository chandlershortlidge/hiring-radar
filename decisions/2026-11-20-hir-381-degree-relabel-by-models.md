## 2026-11-20 — Degree labels from batches labelled under the old degree rule are re-read by two models, not by the person reviewing (HIR-381)

**The rule.** In a labelling batch labelled before the 19 Nov degree rule (record the
**lowest** level a posting names), every degree label is read again under that rule by the
same two models that settle other queue items: the proposer (`claude-haiku-5-5`) proposes,
the cross-family judge (`gemini-4-argon`) rules. Where they agree the item is settled with
`by=model`; where they split, or a model's answer cannot be used, the item stays `?` for
Chandler. Both models are given the labelling guide's own Degree section, word for word,
in place of the skill rules they get for other items.

**This replaces one line** of the 2026-11-19 degree decision (HIR-245): "Labelling batches
already in the review queue were labelled under the old guide; their degree items are
corrected by the person reviewing them, under this rule." The rest of that decision stands.
It also replaces the last paragraph of the 2026-11-20 proposer decision (HIR-379), which
left degree items for a person (`--skip-key degree`).

**Which labels.** Every degree item already in a batch's review queue (disagreements,
uncertain, and spot-check items A and B agreed on). Plus every degree label A and B agreed
on that never reached the queue, when the posting names more than one degree level, a
plain "degree" with no level counting as bachelor's, as the guide reads it. Those get a
queue item of their own (reason `rule-change`: `ok` / `drop` / a corrected value) so that
`apply` reads the correction like any other decision. An agreed label in a posting that
names one level or none reads the same under both rules and is not re-read.

**What counts as agreeing.** Two answers on an attribute agree when they give the same
value, requirement and "or equivalent" flag, whatever words each quotes: the same test
`label` already uses between labelers A and B. Where both wrote their own quote, the
shorter one is kept.

**Why.** Chandler, 20 Nov, on HIR-381: "yes" to models settling degree labels under the
lowest-level rule, with only the splits going to him. Two models from two companies
agreeing is the bar every other item in these batches settled at (HIR-379).

**How to undo.** Reset the `by=model` degree items in each batch's `adjudication.json` to
`?` in its `review_queue.md`, and remove the `rule-change` items; a person then answers
them as the 19 Nov decision first said.
