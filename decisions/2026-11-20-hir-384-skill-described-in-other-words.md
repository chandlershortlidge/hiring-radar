## 2026-11-20 — A skill a posting describes in other words counts, as another spelling of the skill (HIR-384)

**The rule.** When a posting describes a skill in other words instead of naming it
("operating ML models in production" for MLOps, "post-training" for fine-tuning), the skill
counts. It counts by adding that phrase to the skill list as another spelling (alias) of the
skill, so the labelling guide's rule "label what the text names" still holds: once the phrase
is a spelling, the text names the skill.

Two conditions, both required:

1. **The phrase sits in a section that asks the candidate for something**: requirements,
   qualifications, nice-to-have, or a tech-stack section. The same words under
   responsibilities or in the company description still don't count, as for any skill.
2. **The phrase clearly means that skill.** A phrase only loosely related to it is left out.

Chandler, 20 Nov, while working the disputes in the eight city batches of 19 Nov (HIR-379):
"Count them. Where a posting describes a skill in other words instead of naming it, add that
phrase as another spelling of the skill, so 'label what the text names' still holds."

**What was added.** He approved 18 phrases as a group; 17 are new spellings, and
"monitoring" was already a spelling of Observability. He rejected, and the list leaves out:
"built generative AI products", "GenAI systems", "contributions to open-source LLM training
projects", "AI inference and/or training workflows", "including training", "removing manual
steps", "Google Docs automation", "intelligent automation solutions", "supporting the data
backend".

**Why.** Without it, a posting that asks for the skill in a sentence instead of a keyword
was labelled as not asking for it, and the two labellers split on every such case. Making
the phrase a spelling keeps one rule for labellers and the extractor, instead of a second,
looser rule about meaning.

**Undo.** Remove the spellings from the skill list and this rule from the guide; the open
jobs are then re-read once more.
