# Labeling guide

How a Golden is labeled. **Frozen**: changing a rule here changes what the Goldens mean,
so it invalidates every stored eval result. Treat an edit as a release decision, record it
in DECISIONS.md, and relabel the affected Goldens in the same change.

A Golden is a job description plus a list of expected criteria, one per skill:
`{skill_id, requirement, raw_text}`.

## What counts as a skill

From `taxonomy/README.md`, which is the source of truth:

> A skill is something a candidate can have and a job can ask for: a language, framework,
> tool, platform, technique, or technical practice. Spoken languages, degrees, years of
> experience, domain knowledge, and soft skills are not skills here.

Label only skills the candidate is asked to have — requirements, qualifications, "nice to
have" lists, or a dedicated tech-stack section. A technology that appears only in the
responsibilities or the company description is not labeled unless the candidate is also
asked for it. Concrete technologies given as examples ("e.g.", "such as", in parentheses)
are skills in their own right.

`skill_id` must exist in `taxonomy/skills.json`. If no entry fits, the skill belongs in
the taxonomy first — the Golden never invents an id.

## requirement: `required` or `nice_to_have`

Three rules, in order of precedence:

1. **The section heading sets the default.** A heading that marks its section optional —
   "Nice to have", "Bonus", "Strongly Preferred", "Preferred qualifications" — makes every
   item under it `nice_to_have`, until the next heading. A heading that marks its section
   as requirements, or no heading at all, defaults to `required`.
2. **An inline marker on the item overrides the heading**, in either direction. The markers
   are: preferred, plus, bonus, nice to have, ideally, is an advantage.
3. **An unmarked item in a tech-stack list is `required`.** A "tech stack you will work
   with" section describes the job, not a wish list, so an entry in it with no marker of
   its own is a requirement.

## raw_text

The **shortest verbatim phrase from the job description that supports the skill**, copied
exactly. Not a summary, not a synthesized phrase, not the whole bullet when a fragment
carries it. `raw_text` has to appear in the JD — the extractor rejects a mention whose
`raw_text` it cannot find, and so should a reviewer.

Where a bullet names several skills, each one gets the fragment that names it, not the
shared bullet.

## One criterion per skill per JD

A skill id appears **at most once** in a Golden. If the JD asks for it in more than one
place, the mentions collapse into one criterion:

- **Any `required` mention wins.** A skill named once in an optional section and once as a
  requirement is `required`.
- **`raw_text` quotes the mention that determined the label** — the `required` one where
  they disagree. Where the skill's bare name appears in several mentions, quote enough of
  the determining one to identify it.
