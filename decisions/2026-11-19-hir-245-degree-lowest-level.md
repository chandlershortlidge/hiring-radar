## 2026-11-19 — An answer key records the lowest degree level a posting names, not the highest (HIR-245)

**The rule.** When a posting names several degree levels as alternatives ("Bachelor's or
Master's", "MS or PhD", "PhD / Master"), the answer key's `degree` is the **lowest** of them:
the least a candidate must hold to get in. `degree_requirement` is unchanged: `required`
unless the mention is marked optional. When the whole mention is optional ("ein Master oder
Ph.D. ist von Vorteil"), the level is still the lowest named, and the requirement is
`nice_to_have`. "Master's degree (or above)" names one level, master.

**Why.** Chandler ruled on 2026-11-10, on a "Bachelor's or master's degree" posting: "no
masters is not required, it's nice to have. bachelor's is required, but you can also have a
masters". He applied it again on 2026-11-19 ("only a degree is required, not a PhD"). The
question a visitor's degree filter asks is "what is the least that gets me in"; the highest
level named answers a different question and makes "Bachelor's or Master's" look like a
master's-only job.

**One slot, not two.** Chandler chose option 1 on HIR-245 ("go", 2026-11-19): the answer
key keeps one degree per posting. "Bachelor required, master's welcome" loses its second
half. A second "preferred higher level" field was rejected for now: 7 of the 74 answer keys
counted on 2026-11-14 name two levels, too few to carry a new field through the answer
keys, the extractor, the database and the dashboard.

**This replaces** the guide's "the highest level named" (in force since the guide was
written) and the 2026-11-02 hand check that confirmed "MS or PhD" as PhD (golden_040).

**What it changes.**

- Two held-back answer keys move: golden_036 ("ein Master oder Ph.D. ist von Vorteil")
  PhD → master, still nice-to-have; golden_040 ("MS or PhD … or equivalent practical
  experience") PhD → master, still required. The stored held-back score was measured
  against the old keys and is stale until the next release run.
- The practice (dev) keys already follow this rule: they were written with Chandler's
  2026-11-10 ruling (HIR-167 and after), so no dev key moves and the stored dev baseline
  stands.
- The extractor is still told "the highest level named", so the model disagrees with these
  keys on every multi-level posting until HIR-335 changes its instructions. Degree misses
  of that shape are expected, not a regression.
- Labelling batches already in the review queue were labelled under the old guide; their
  degree items are corrected by the person reviewing them, under this rule.

**How to undo.** Revert the guide's degree line and the two keys; this file then records a
rule no longer in force and should be superseded by a new entry, not deleted.
