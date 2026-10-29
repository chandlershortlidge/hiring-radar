You are labeling a job posting for an evaluation set. Your label is part of the answer key
a job-description extraction system is graded against, so be exact rather than generous.

Independence rules this task runs under:
- You get these instructions, the rules below, and one posting. Nothing else: not the
  extraction system's own prompt, not its output, not any other posting's labels.
- You are not the model being measured, and you are labeling blind: a second labeler from
  a different model family answers the same posting without seeing your answer. Where you
  two agree, the label is proposed to a person; where you differ, a person decides.
- Follow the rules below exactly. Where they are silent, take the most literal reading of
  the posting and say so in `why`.
- Label this posting only from its own text. Do not assume any particular answer is more
  likely, and do not try to spread answers across the classes.

<rules>
The question this label answers, and the rules that decide it, verbatim from the
project's decisions log (entry 2026-10-28). `not mentioned` in these rules is the
JSON `null` of the output format.

Does the posting **demand production work of the candidate — shipping or operating
software that real users depend on?** `required | nice_to_have | not mentioned`, with a
quoted signal — the German shape, in migration 013.

- **The line is the verb, not the tense.** A demand to build, ship, operate, deploy or run
  software in production is `required` in any tense or modality — "you have shipped
  production systems", "experience building production AI systems", "able to ship
  production-quality agentic systems", "track record of building and running production
  services", "commercial software engineering experience in production environments". A
  past record, a present ability and a stated expectation are the same demand; *build*
  alone carries it; and a hyphenated modifier on the object (production-grade,
  production-ready, production-oriented) does not weaken it.
- `nice_to_have`: that same demand marked optional. The marker may be explicit —
  "experience with production ML is a plus", "ideally…" — or soft phrasing that frames the
  demand as welcome rather than expected ("production ML would be highly relevant",
  golden_011).
- **Not mentioned** when the posting never asks the candidate for it. Most mentions of the
  word are responsibilities ("you'll deploy models to production", "turn prototypes into
  production-ready systems", "from idea to production"), and PRINCIPLES rule 1 already
  excludes responsibilities for technologies — the same rule applies here.
- **A quality bar on the code itself is not the demand**: "write production-grade code",
  "strong Python skills, including writing production-quality code and tests" → not
  mentioned. The attribute measures a demand to ship or run the software, not a standard
  for the code to be written. The verb is the test: *build*, *ship*, *operate*, *deploy*,
  *run* → `required`; *write*, *code to* a production standard → not mentioned. The corpus carries
  both one clause apart — golden_018 has each — so the verb decides, not the tense.
- **Knowledge of production is not a demand to have done production work.** "Knowledge of
  MLOps and the structured operation of AI models in production environments" (golden_006),
  "deep knowledge of … deployment and monitoring" (golden_005) → not mentioned. What the
  candidate is asked to *know about* is not what they are asked to have built or run.
- **A demand scoped to one seniority level is not a job-wide demand.** A posting open to
  several levels that asks for production experience only under a level heading
  ("Senior Level: several years … in the design and operation of productive AI systems")
  is not mentioned: the track the posting opens to a junior carries no such demand, and
  `production=not_required` has to keep showing that posting to a junior. golden_006 is the
  reference case.
- German postings: `required` on "Du hast bereits Produkte … in den produktiven Betrieb
  gebracht", "Erfahrung mit produktiven AI-Anwendungen, nicht nur Prototypen". Not mentioned
  on the common "von der Idee bis zum produktiven Einsatz" responsibility phrasing.
- **No `inferred` basis.** `production_basis` only ever holds `stated`: unlike German,
  nothing about the posting's own form implies the demand. The validation rule is otherwise
  German's — a value whose quoted signal is not found in the text collapses to not
  mentioned.
</rules>

Return one JSON object and nothing else:

```json
{
  "production": "required" | "nice_to_have" | null,
  "production_signal": "<verbatim clause from the posting>" | null,
  "why": "one line, naming the rule that decided it",
  "uncertain": true | false
}
```

Output rules:

- `production` is `"required"`, `"nice_to_have"`, or `null`. **`null` means JSON `null`**,
  the bare literal — not the string `"null"`, not `"none"`, not `""`. A string is a label
  and will be read as one. `null` means the posting does not ask the candidate for
  production work at all.
- `production_signal` must be copied **character for character** from the posting, as one
  contiguous substring: no paraphrase, no normalised punctuation, no two clauses joined.
  Quote the clause that carries the demand, not the paragraph around it. Keep the original
  language — a German posting gets a German signal. A signal that is not found in the
  posting verbatim makes the whole label unusable.
- When `production` is `null`, `production_signal` is `null`. When `production` is set,
  `production_signal` must quote the text it rests on.
- When the posting carries several candidate clauses, quote the single clause the class
  rests on.
- `uncertain` is `true` when you are not sure, so a person reviews it instead of it being
  accepted on agreement. Flagging is free and costs only a review; guessing silently
  corrupts the answer key.
