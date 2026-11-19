## 2026-11-19 — The model records the lowest degree level a posting names, matching the answer keys (HIR-335)

The extractor's instructions said "degree is the highest level named". The labelling guide
changed to the lowest level on 2026-11-19 (HIR-245), so the model and the answer keys
disagreed on every posting naming two levels ("Bachelor's or Master's", "MS or PhD"). The
prompt now carries the guide's rule in the same words: the lowest level named, the least a
candidate must hold; "(or above)" names one level; an optional mention keeps the lowest
level with `nice_to_have`.

**Why the same words.** The prompt mirrors the guide so that the model and the answer keys
are judged by one standard; a paraphrase would reopen the gap this closes.

**What it changes.** Every open job is re-read once on merge (the prompt is part of the
extractor version). On the dashboard, a job asking for "bachelor's or master's" now counts
as wanting a bachelor's in the degree filter, instead of a master's.

**How to undo.** Revert the prompt line; the next poll re-reads the open jobs again.
