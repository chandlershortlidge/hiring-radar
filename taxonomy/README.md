# Skill taxonomy

`skills.json` is the single source of truth for what counts as a skill and what it's called.

```jsonc
{
  "id": "vertex-ai",          // stable; never rename once rows reference it
  "display": "Vertex AI",     // shown on the chart
  "aliases": ["google vertex ai"],  // other spellings, lowercase
  "parents": ["gcp"],         // broader skills this one implies
  "reviewed": true            // a human has checked this entry
}
```

## Rules

- **A skill is something a candidate can have and a job can ask for**: a language,
  framework, tool, platform, technique, or technical practice. Spoken languages, degrees,
  years of experience, domain knowledge, and soft skills are not skills here.
- **Aliases are the same thing spelled differently.** "LLM APIs" → LLMs is an alias.
  "LangChain" → LLM orchestration is not; that's a parent.
- **Parents point from specific to broad**, one way only. Vertex AI → GCP → Cloud.
- **Keep specializations separate.** Agents and Multi-Agent Systems are both entries;
  the second has the first as a parent.
- **Bump `version`** when an edit changes what any existing label resolves to.
- **An id is never removed or renamed.** Stored rows point at it, so the jobs that mention
  it would lose that skill from the chart with no error. `tests/test_taxonomy.py` fails if
  an id that was ever committed is gone, against the list in
  `tests/fixtures/skill_ids.json`; a new id is added to that list with
  `uv run python scripts/record_skill_ids.py`. Rename the display name instead, and keep
  the old spelling as an alias.

## Skill boundaries

Most entries need no explanation beyond their display name and aliases. A few sit next to
something that uses the same word, and the display name alone has let the wrong phrases
collect on them. Those are written down here, and this is the list a labeller checks when a
phrase could go two ways.

Add an entry here only when two skills share a word, not to define a skill in general.

### Software Testing (`testing`) vs. A/B Testing, Statistics, Evaluation

`testing` is **software testing**: checking that code behaves as intended. Unit,
integration, regression and end-to-end tests, test automation and test infrastructure, and
the German `automatisierte Tests` / `Testautomatisierung`. Its display name is "Software
Testing" for this reason; the id stays `testing` because stored rows point at it (the id
rule above).

The three neighbours that share the word "test":

- **`a-b-testing`** — comparing two live variants to decide between them: "A/B test",
  "split test". The word is "test" but the thing is an experiment, not a check on code.
- **`statistics`** — "statistical testing", "hypothesis testing", "significance testing".
  A statistical procedure, not a check on code.
- **`evaluation`** — judging the quality of a model's or an agent's output: "model
  evaluation", "LLM evaluation", eval sets and evaluation frameworks.

A phrase that names both gets both, like any other bullet naming two skills: "tests and
evaluations" is `testing` **and** `evaluation`, and "simulation-based testing and
evaluation of agents" is the same two. The boundary decides which skill a phrase belongs
to, never how many skills one phrase may carry.

## Review pass (to do)

All 175 seed entries are `reviewed: false`. Go through them once: delete non-skills,
merge true duplicates, fix parents, set `reviewed: true`. The tests will tell you if a
Golden references something you deleted.
