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

## Review pass (to do)

All 175 seed entries are `reviewed: false`. Go through them once: delete non-skills,
merge true duplicates, fix parents, set `reviewed: true`. The tests will tell you if a
Golden references something you deleted.
