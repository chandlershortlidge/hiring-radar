## 2026-11-20 — "Any one of" skill groups in labelling batches are marked by two models, with only the splits going to Chandler (HIR-387)

**The rule.** For a labelling batch whose answer keys are not yet written, the "any one of"
groups (the guide's `alternative_group` section) are marked per posting by the same two
models that settle other queue items: the proposer (`claude-haiku-5-5`) marks them, the
cross-family judge (`gemini-4-argon`) rules. Both are given the guide's `alternative_group`
section word for word and the whole posting. Where they give the same groups the posting's
grouping is settled with `by=model` and its answer key carries `groups_reviewed: true`;
where they split, or a model's answer cannot be used, the grouping stays `?` for Chandler.
The guard is the one every model in this process has: never the extractor, either labeler,
or the model that wrote the proposals.

**One queue item per posting.** Reason `groups`, key `alternative_group`. Its decision is a
JSON list of groups, each a list of skill ids, e.g. `[["bash", "python"]]`, or `[]` when the
posting offers no skills in place of each other. Two answers agree when they name the same
groups, whatever their order.

**Which skills are offered for grouping.** The posting's agreed skills, plus every skill a
still-open queue item could add (both labelers' versions), plus what a decided queue item
already added. A member that does not reach the answer key leaves its group when the key is
written; a group left with fewer than two members is dissolved. A group changes no
`requirement`.

**A posting with fewer than two such skills** gets no item and no model call: nothing in it
can be grouped. Its answer key carries `groups_reviewed: true` with no groups, as a recorded
fact rather than a model's ruling.

**Why.** Chandler, 20 Nov, on HIR-387: "yes" to the models marking the groups with only the
splits going to him. Without `groups_reviewed: true` none of these postings is scored on
grouping, and two models from two companies agreeing is the bar every other item in these
batches settled at (HIR-379, HIR-381).

**How to undo.** Remove the `groups` items from each batch's `items.json` and
`review_queue.md` and the `groups` record from its `adjudication.json`; the answer keys are
then written without groups and without `groups_reviewed`, as before.
