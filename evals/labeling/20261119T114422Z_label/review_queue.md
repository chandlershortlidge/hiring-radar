# Review queue - 20261119T114422Z_label

156 items from 13 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261119T114422Z_label` refuses while any `?` is left, then writes the Goldens.

What the words mean:

- `A` / `B` - take that labeler's version of this skill or attribute, as printed below.
- `both` - both skills belong in the answer key (only for two ids on one phrase).
- `drop` - this skill is not in the answer key / this attribute is null for this posting.
- `ok` - the agreed value printed below is right; keep it.
- A JSON object writes the value yourself, e.g.
  `DECISION: {"requirement": "nice_to_have", "raw_text": "ideally Kubernetes"}` for a skill,
  or `DECISION: {"seniority": "senior", "seniority_basis": "stated", "seniority_signal": "Lead AI Engineer"}`
  for an attribute. A skill override keeps the printed `skill_id` unless you give one.

Items are grouped by what they ask of you, in the order to work them: the in-scope
questions, then disagreements, then uncertain, then mapping, then the spot-check sample.

Spot-check items are a seeded random sample (80 of 170 accepted labels,
seed 0) of labels A and B already agreed on. They measure the error rate that
agreement alone cannot: two labelers can agree and both be wrong. They print the posting
excerpt and the agreed label only - no `A:`/`B:` lines - so you check the label against the
posting rather than against the labelers, who by construction both said the same thing.

The first 13 items ask whether each posting belongs in the held-out set at all.
They come pre-answered `yes`, so leaving them alone keeps every posting. Answer `no <why>`
and that posting is written to `evals/goldens/excluded.json` with your reason instead of
becoming a Golden, and neither this script nor `new_goldens.py` will pick it again. Use it
for a posting that got past the title and city filters but is not the job market we
measure - a marketing role, a listing in the wrong field. The rest of that posting's items
are then ignored, so you can answer `no` and skip them.

## 1. golden_094 - scope `in_scope` (in-scope)

> Principal Applied AI Scientist, Commerce Foundation Models

- Prosus · Principal Applied AI Scientist, Commerce Foundation Models
- Amsterdam · en · arbeitnow · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_095 - scope `in_scope` (in-scope)

> AI Quantitative Researcher | Internship | '27

- Blocktech · AI Quantitative Researcher | Internship | '27
- Amsterdam · en · arbeitnow · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_096 - scope `in_scope` (in-scope)

> ML Engineering Intern - LLM Research & Development

- prosus · ML Engineering Intern - LLM Research & Development
- Amsterdam · en · ashby · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_097 - scope `in_scope` (in-scope)

> Developer Advocate, Toqan (Prosus AI Platform)

- prosus · Developer Advocate, Toqan (Prosus AI Platform)
- Amsterdam · en · ashby · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_098 - scope `in_scope` (in-scope)

> Machine Learning Engineer - LLMs

- prosus · Machine Learning Engineer - LLMs
- Amsterdam · en · ashby · 19 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_099 - scope `in_scope` (in-scope)

> Data Scientist, Trust & Safety

- Vinteden · Data Scientist, Trust & Safety
- Amsterdam · en · arbeitnow · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_100 - scope `in_scope` (in-scope)

> Backend Engineer, GenAI Platform

- DPG Media · Backend Engineer, GenAI Platform
- Amsterdam · en · arbeitnow · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_101 - scope `in_scope` (in-scope)

> Amsterdam or Antwerp- Combine Data Science, AI, and Media to transform the advertising market. As a Data Scientist Total Video, you will tak

- DPG Media · Data Scientist Total Video
- Amsterdam · en · arbeitnow · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_102 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer, Evals

- Prosus · Senior Machine Learning Engineer, Evals
- Amsterdam · en · arbeitnow · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_103 - scope `in_scope` (in-scope)

> Senior Backend Engineer, AI Platform (Toqan)

- prosus · Senior Backend Engineer, AI Platform (Toqan)
- Amsterdam · en · ashby · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_104 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer – LLMs

- prosus · Senior Machine Learning Engineer – LLMs
- Amsterdam · en · ashby · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_105 - scope `in_scope` (in-scope)

> Lead/Manager AI Infra Systems Engineering Team

- togetherai · Lead/Manager AI Infra Systems Engineering Team
- Amsterdam · en · greenhouse · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_106 - scope `in_scope` (in-scope)

> Senior Applied AI Scientist, Commerce Foundation Models

- Prosus · Senior Applied AI Scientist, Commerce Foundation Models
- Amsterdam · en · arbeitnow · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_095 - skill `ai-ml` (disagreement)

> ...in Amsterdam, for a minimum of 12 weeks. Nice to have - Experience using AI for quantitative research, such as working on math problems. - Python, and exposure...

- A: `ai-ml` · nice_to_have · raw_text: "Experience using AI for quantitative research"
- B: `ai-ml` · required · raw_text: "focus on AI"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 3, a required mention wins: the 'You'll need' list requires a background 'with a focus on AI (MSc or PhD)', which the quoted raw_text 'focus on AI' shows, so the nice-to-have reading in A is overridden.

DECISION: B

## 15. golden_096 - skill `model-development` (disagreement)

> ...hood. - You understand ML fundamentals because you've trained models yourself and understand the core concepts. - You can make sense...

- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "trained models yourself"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the preferred-qualifications bullet "you've trained models yourself" names a skill (training models, i.e. model development), and the labeler's nice_to_have tag and quoted raw_text match the posting word for word.

DECISION: B

## 16. golden_098 - skill `data-pipelines` (disagreement)

> ...BF16, FP8), ZeRO optimization - Track record of building synthetic data generation pipelines for instruction tuning or domain adaptation - Research...

- A: (did not label this)
- B: `data-pipelines` · nice_to_have · raw_text: "synthetic data generation pipelines"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the PREFERRED QUALIFICATIONS bullet "Track record of building synthetic data generation pipelines" names a data-pipeline skill as a qualification, so B's nice_to_have label with that raw_text is supported, and rule 5 is not triggered because the text names pipelines directly.

DECISION: B

## 17. golden_098 - skill `open-source-llms` (disagreement)

> ...benchmarks used by the community - Contributions to open-source LLM training projects or tools WHAT WE OFFER - High-impact AI projects that are...

- A: (did not label this)
- B: `open-source-llms` · nice_to_have · raw_text: "open-source LLM training projects or tools"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the preferred-qualifications bullet "Contributions to open-source LLM training projects or tools" is a qualification that names the skill, and its nice_to_have requirement matches the section heading, so B's labeling stands over A's omission.

DECISION: ?

## 18. golden_099 - skill `model-development` (disagreement)

> ...preparing training datasets, engineering features, training models and evaluating them against baselines and...

- A: (did not label this)
- B: `model-development` · required · raw_text: "training models"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'About you' bullet requires hands-on experience 'training models', which names model development as a qualification, and rule 3 makes this required mention decisive, so labeler B's required tag with that raw_text stands.

DECISION: B

## 19. golden_100 - skill `software-architecture` (disagreement)

> ...5 years of backend engineering experience, including designing systems yourself. - Proficiency in at least one backend language. We work...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "designing systems yourself"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required 'you bring' bullet asking for experience 'designing systems yourself' names a qualification skill that maps to software-architecture, and the raw_text quote appears verbatim in the posting, so labeler B's required tag stands.

DECISION: B

## 20. golden_101 - skill `ai-deployment` (disagreement)

> ...and machine learning, enabling you to design, train, and implement models in production environments • Experience transforming data models into scalable data...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "implement models in production environments"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'you bring' qualification bullet names deploying models ('implement models in production environments'), and under rule 3 that required mention supports labeler B's required ai-deployment tag.

DECISION: B

## 21. golden_101 - skill `data-modeling` (disagreement)

> ...train, and implement models in production environments • Experience transforming data models into scalable data products, preferably within a media or advertising environment •...

- A: (did not label this)
- B: `data-modeling` · required · raw_text: "Experience transforming data models into scalable data products"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'you bring' qualification bullet names data models as a required experience, and under rule 3 that required mention, quoted in raw_text, decides it, so labeler B's required data-modeling tag stands.

DECISION: B

## 22. golden_101 - skill `model-development` (disagreement)

> ...in data science and machine learning, enabling you to design, train, and implement models in production environments • Experience transforming data...

- A: (did not label this)
- B: `model-development` · required · raw_text: "design, train, and implement models"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'you bring' qualification bullet names model development ("design, train, and implement models"), and rule 3 makes that required mention count, so labeler B's required tag and quoted raw_text are supported.

DECISION: B

## 23. golden_102 - skill `a-b-testing` (disagreement)

> ...LLM-as-judge calibration, recommendation metrics or online experimentation. - Contributions to evaluation frameworks, public...

- A: `a-b-testing` · nice_to_have · raw_text: "online experimentation"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the preferred-qualifications bullet names "online experimentation", which is a close synonym for A/B testing, so labeler A's nice_to_have a-b-testing tag stands (rule 5 is not violated because this is not a broader parent skill).

DECISION: A

## 24. golden_102 - skill `fine-tuning` (disagreement)

> ...with language-model training or post-training. - Experience with agent or gaming...

- A: `fine-tuning` · nice_to_have · raw_text: "post-training"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the Preferred qualifications bullet "Experience with language-model training or post-training" names a skill, and post-training is effectively fine-tuning, so the labeler's nice_to_have fine-tuning tag with raw_text "post-training" is supported.

DECISION: ?

## 25. golden_102 - skill `model-development` (disagreement)

> ...qualifications - Experience with language-model training or post-training. - Experience with agent or gaming...

- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "language-model training"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the Preferred qualifications bullet "Experience with language-model training or post-training" names a skill that maps to model-development as a nice_to_have, and the raw_text quote supports that, while rule 5 is not violated because the skill itself is named.

DECISION: ?

## 26. golden_102 - skill `recommender-systems` (disagreement)

> ...with human evaluation, LLM-as-judge calibration, recommendation metrics or online experimentation. - Contributions to evaluation...

- A: `recommender-systems` · nice_to_have · raw_text: "recommendation metrics"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_103 - skill `ai-ml` (disagreement)

> ...still finding their shape. You're genuinely curious about the AI and LLM space — not as a trend to track, but as a domain where you've already done hands-on integration work and want to go further. AI tools aren't an afterthought in...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "the AI and LLM space — not as a trend to track, but as a domain where you've already done hands-on integration work"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'Who You Are' sentence names AI/LLM domain experience ('already done hands-on integration work') as a candidate trait, and rule 3 makes that required mention win over A's omission, so the ai-ml skill belongs in the key.

DECISION: B

## 28. golden_103 - skill `event-driven-systems` (disagreement)

> ...that use tools and execute multi-step workflows - Experience building or maintaining event-sourced systems - Python programming skills - Experience with AI or ML...

- A: `event-driven-systems` · nice_to_have · raw_text: "Experience building or maintaining event-sourced systems"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the nice-to-have bullet "Experience building or maintaining event-sourced systems" is a qualification sentence that names an event-driven skill, and rule 5 is not triggered because event-sourced systems is the named skill rather than a broader parent.

DECISION: ?

## 29. golden_103 - skill `software-architecture` (disagreement)

> ...patterns and into setting them. You're comfortable owning architectural decisions on novel infrastructure — the kind where the right answer...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "owning architectural decisions"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'Who You Are' sentence "comfortable owning architectural decisions on novel infrastructure" is a qualification that names the skill, and under rule 3 that required-style mention makes software-architecture belong in the key with B's raw_text.

DECISION: B

## 30. golden_104 - skill `model-development` (disagreement)

> ...review and architecture decisions. - Proven experience training and deploying language models to production. - Experience preparing large-scale training datasets:...

- A: (did not label this)
- B: `model-development` · required · raw_text: "training and deploying language models to production"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under Rule 1, the MINIMUM QUALIFICATIONS bullet "Proven experience training and deploying language models to production" names model development as a required skill, and Rule 3 makes that required mention decisive over labeler A's omission.

DECISION: ?

## 31. golden_105 - skill `software-engineering` (disagreement)

> ...smoothly. You are a blend of a pragmatic operator and a software engineer that applies sound engineering principles, operational discipline, and mature automation to our...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software engineer that applies sound engineering principles"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1, "a software engineer that applies sound engineering principles" is a role-descriptor in the About the Role profile, closer to a job title than a named qualification, and the posting's actual skill asks are systems and operations (rule 5 forbids adding a broader skill the text doesn't name).

DECISION: drop

## 32. golden_106 - skill `model-development` (disagreement)

> ...including doctoral research, with hands-on experience designing and running model-training experiments. For Track 1, this should include pre-training or...

- A: (did not label this)
- B: `model-development` · required · raw_text: "designing and running model-training experiments"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the minimum-qualifications sentence asks for "hands-on experience designing and running model-training experiments," a named skill, and under rule 3 that required mention is quoted verbatim, so labeler B's required model-development label stands.

DECISION: B

## 33. golden_094 - skill `a-b-testing` (uncertain)

> ...foundation models. - Familiarity with commerce data and online experimentation. - We do not expect expertise in every area. What we...

- A: `a-b-testing` · nice_to_have · raw_text: "online experimentation"
- B: `a-b-testing` · nice_to_have · raw_text: "online experimentation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, "Familiarity with commerce data and online experimentation" is a named qualification bullet in the preferred section, and online experimentation is essentially A/B testing, so the agreed nice_to_have label with that raw_text stands.

DECISION: ok

## 34. golden_094 - skill `model-development` (uncertain)

> ...that were published or reached production. - Substantial experience developing and training models, with deep expertise in pre-training, post-training or...

- A: `model-development` · required · raw_text: "experience developing and training models"
- B: `model-development` · required · raw_text: "developing and training models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the Minimum qualifications bullet "Substantial experience developing and training models" names the skill as a requirement, and the agreed raw_text appears verbatim in the posting, so the agreed required label stands (Rule 3).

DECISION: ok

## 35. golden_094 - skill `statistics` (uncertain)

> ...make better decisions. - Sound experimental and statistical judgment, including examples where the evidence changed your...

- A: `statistics` · required · raw_text: "statistical judgment"
- B: `statistics` · required · raw_text: "statistical judgment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Minimum qualifications (rule 1), the bullet names "statistical judgment" as a requirement, and rule 3 makes that required mention win, with the agreed raw_text appearing verbatim in the posting.

DECISION: ok

## 36. golden_095 - skill `evaluation` (uncertain)

> ...experience with LLMs, agents, and harnesses. - Comfort designing evaluation and feedback loops that tell you whether an agent is actually...

- A: `evaluation` · required · raw_text: "designing evaluation and feedback loops"
- B: `evaluation` · required · raw_text: "designing evaluation and feedback loops"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'You'll need' qualification 'Comfort designing evaluation and feedback loops that tell you whether an agent is actually improving' names the skill as a requirement, and the agreed raw_text quotes it word for word, so the required label stands.

DECISION: ok

## 37. golden_096 - attribute `degree` (uncertain)

> ...internship is open to candidates who are currently enrolled at a university and either hold EU citizenship or are studying in the...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="currently enrolled at a university"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="currently enrolled at a university"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - The eligibility line 'currently enrolled at a university' with no level named is the rule's 'currently studying' case, which maps to bachelor; it is a hard requirement, not optional, and no other degree level is named, so the agreed label stands.

DECISION: ok

## 38. golden_096 - skill `ai-developer-tooling` (uncertain)

> ...from research to data processing when needed. - You're friends with AI assistants and use them regularly for coding and writing. - You can commit to 6-12 months working...

- A: `ai-developer-tooling` · nice_to_have · raw_text: "You're friends with AI assistants and use them regularly for coding"
- B: `ai-developer-tooling` · nice_to_have · raw_text: "AI assistants and use them regularly for coding and writing"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the preferred-qualifications bullet "You're friends with AI assistants and use them regularly for coding" names regular use of AI coding assistants, which fits ai-developer-tooling at nice_to_have, so the agreed label stands.

DECISION: ok

## 39. golden_097 - skill `backend-development` (uncertain)

> ...code. Ideally experienced in Go, Python or TypeScript. Backend or full-stack background both fine. - Real hands-on experience with agents or...

- A: `backend-development` · required · raw_text: "Backend or full-stack background"
- B: `backend-development` · required · raw_text: "Backend"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the sentence "Backend or full-stack background both fine" sits in the WHAT YOU'LL NEED qualifications and names backend development as an accepted background, and under rule 3 that required-section mention wins, so the agreed required label stands.

DECISION: ok

## 40. golden_097 - skill `claude-code` (uncertain)

> ...setup problems. - You use AI coding tools (Cursor, Claude Code, Copilot, Codex) daily as part of how you work. - Proven...

- A: `claude-code` · required · raw_text: "Claude Code"
- B: `claude-code` · required · raw_text: "Claude Code"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'WHAT YOU'LL NEED' bullet names Claude Code as a daily tool the candidate must use, so it counts as a required skill, and the agreed raw_text 'Claude Code' appears verbatim in the posting.

DECISION: ok

## 41. golden_097 - skill `codex` (uncertain)

> ...- You use AI coding tools (Cursor, Claude Code, Copilot, Codex) daily as part of how you work. - Proven technical...

- A: `codex` · required · raw_text: "Codex"
- B: `codex` · required · raw_text: "Codex"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification bullet "You use AI coding tools (Cursor, Claude Code, Copilot, Codex) daily" names Codex as a required tool, and the agreed required label with raw_text "Codex" matches the posting word for word.

DECISION: ok

## 42. golden_097 - skill `cursor` (uncertain)

> ...common setup problems. - You use AI coding tools (Cursor, Claude Code, Copilot, Codex) daily as part of how you...

- A: `cursor` · required · raw_text: "Cursor"
- B: `cursor` · required · raw_text: "Cursor"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'WHAT YOU'LL NEED' bullet names Cursor as a daily tool the candidate must use, so it is a qualification, and rule 3 makes that required mention win; the agreed required label and raw_text 'Cursor' are accurate.

DECISION: ok

## 43. golden_097 - skill `full-stack-development` (uncertain)

> ...code. Ideally experienced in Go, Python or TypeScript. Backend or full-stack background both fine. - Real hands-on experience with agents or...

- A: `full-stack-development` · required · raw_text: "Backend or full-stack background"
- B: `full-stack-development` · required · raw_text: "full-stack background"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_097 - skill `github-copilot` (uncertain)

> ...- You use AI coding tools (Cursor, Claude Code, Copilot, Codex) daily as part of how you work. - Proven...

- A: `github-copilot` · required · raw_text: "Copilot"
- B: `github-copilot` · required · raw_text: "Copilot"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the WHAT YOU'LL NEED bullet says the candidate uses AI coding tools including Copilot daily, which is a required qualification naming the skill, and rule 3 makes that required mention control with raw_text 'Copilot' appearing verbatim.

DECISION: ok

## 45. golden_097 - skill `open-source-llms` (uncertain)

> ...working AI-powered applications. It combines frontier and open-weight models, agents, tools, sandboxes, memory, context management,...

- A: `open-source-llms` · nice_to_have · raw_text: "open-weight models"
- B: `open-source-llms` · nice_to_have · raw_text: "open-weight models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only quoted mention of open-weight models is in the "ABOUT TOQAN" company description of the platform, not in a qualification bullet asking the candidate for that skill, and the visible excerpt shows no such requirement.

DECISION: drop

## 46. golden_097 - skill `tool-calling` (uncertain)

> ...an API. You should be able to explain how an agent loop, tool call, or model router actually works. - Comfortable working...

- A: `tool-calling` · required · raw_text: "tool call"
- B: `tool-calling` · required · raw_text: "tool call"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required 'WHAT YOU'LL NEED' bullet names tool calls as something the candidate should be able to explain, and rule 3 keeps the required label with raw_text 'tool call', which appears verbatim in the posting.

DECISION: ok

## 47. golden_098 - skill `ai-deployment` (uncertain)

> ...engineering experience - Proven experience training and deploying language models to production (embedding models, encoder models, or large language...

- A: `ai-deployment` · required · raw_text: "deploying language models to production"
- B: `ai-deployment` · required · raw_text: "deploying language models to production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the MINIMUM QUALIFICATIONS bullet explicitly requires "Proven experience training and deploying language models to production," which supports the agreed required ai-deployment label with that raw_text.

DECISION: ok

## 48. golden_098 - skill `embeddings` (uncertain)

> ...training and deploying language models to production (embedding models, encoder models, or large language models) including...

- A: `embeddings` · required · raw_text: "(embedding models"
- B: `embeddings` · required · raw_text: "hands-on experience training language models at scale (from embedding models to specialized LLMs)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the MINIMUM QUALIFICATIONS bullet names embedding models as experience the candidate must have, and under rule 3 that required mention, quoted as "(embedding models", supports the agreed required label.

DECISION: ok

## 49. golden_098 - skill `inference-optimization` (uncertain)

> ...for alignment and instruction-following - Experience optimizing models for production inference: quantization, model compression, distillation, and...

- A: `inference-optimization` · nice_to_have · raw_text: "optimizing models for production inference"
- B: `inference-optimization` · nice_to_have · raw_text: "optimizing models for production inference"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the PREFERRED QUALIFICATIONS bullet names the skill directly ('Experience optimizing models for production inference'), so the agreed nice_to_have label and its verbatim raw_text are correct.

DECISION: ok

## 50. golden_098 - skill `llms` (uncertain)

> ...models to production (embedding models, encoder models, or large language models) including pre-training, continued pre-training, or...

- A: `llms` · required · raw_text: "or large language models"
- B: `llms` · required · raw_text: "hands-on experience training language models at scale (from embedding models to specialized LLMs)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the MINIMUM QUALIFICATIONS bullet names large language models as a required experience area, and rule 3 keeps a required mention even though it is one alternative among embedding and encoder models, so the agreed `llms` required label stands.

DECISION: ok

## 51. golden_098 - skill `ml-engineering` (uncertain)

> ...team engineering standards MINIMUM QUALIFICATIONS - 3+ years of ML engineering experience - Proven experience training and deploying language...

- A: `ml-engineering` · required · raw_text: "3+ years of ML engineering experience"
- B: `ml-engineering` · required · raw_text: "ML engineering experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only mention of ml-engineering is the years-of-experience line "3+ years of ML engineering experience", which does not count, and no other sentence names the skill.

DECISION: drop

## 52. golden_098 - skill `model-development` (uncertain)

> ...years of ML engineering experience - Proven experience training and deploying language models to production (embedding models, encoder models, or large...

- A: `model-development` · required · raw_text: "training and deploying language models"
- B: `model-development` · required · raw_text: "training and deploying language models to production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the MINIMUM QUALIFICATIONS bullet asking for "Proven experience training and deploying language models to production" names model development as a required skill, and the agreed raw_text appears verbatim in that bullet.

DECISION: ?

## 53. golden_098 - skill `transformers` (uncertain)

> ...with production experience using training libraries (Transformers, DeepSpeed, Accelerate) - Strong software engineering practices:...

- A: `transformers` · required · raw_text: "Transformers, DeepSpeed"
- B: `transformers` · required · raw_text: "Transformers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_099 - skill `ai-deployment` (uncertain)

> ...with the production ML lifecycle, including deployment, monitoring and retraining.</li> <li>Ability to break down...

- A: `ai-deployment` · required · raw_text: "including deployment"
- B: `ai-deployment` · required · raw_text: "deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet "Familiarity with the production ML lifecycle, including deployment, monitoring and retraining" names ML deployment, and under rule 3 the quoted phrase "including deployment" supports the required ai-deployment label as agreed.

DECISION: ok

## 55. golden_099 - skill `data-privacy-and-security` (uncertain)

> ...to apply machine learning to member safety, with care for data privacy and the consequences of incorrect...

- A: `data-privacy-and-security` · required · raw_text: "care for data privacy"
- B: `data-privacy-and-security` · required · raw_text: "care for data privacy"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet names data privacy as something the candidate must care about, and rule 3 makes that required mention count, so the agreed required label with raw_text "care for data privacy" stands.

DECISION: ?

## 56. golden_099 - skill `evaluation` (uncertain)

> ...datasets, engineering features, training models and evaluating them against baselines and metrics.</li> <li>Experience applying machine learning to at least...

- A: `evaluation` · required · raw_text: "evaluating them against baselines and metrics"
- B: `evaluation` · required · raw_text: "evaluating them against baselines and metrics"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'About you' qualification bullet 'evaluating them against baselines and metrics' names model evaluation as a required skill, and under rule 3 the required mention with its verbatim raw_text supports the agreed label.

DECISION: ok

## 57. golden_099 - skill `mlops` (uncertain)

> ...natural language processing, or computer vision.</li> <li>Familiarity with the production ML lifecycle, including deployment, monitoring and...

- A: `mlops` · required · raw_text: "Familiarity with the production ML lifecycle"
- B: `mlops` · required · raw_text: "production ML lifecycle"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'About you' bullet 'Familiarity with the production ML lifecycle, including deployment, monitoring and retraining' is a required qualification that names MLOps practice, and rule 3 makes the required mention decisive, so the agreed required label stands.

DECISION: ok

## 58. golden_099 - skill `observability` (uncertain)

> ...with the production ML lifecycle, including deployment, monitoring and retraining.</li> <li>Ability to break down problems into manageable...

- A: `observability` · required · raw_text: "monitoring and retraining"
- B: `observability` · required · raw_text: "monitoring"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 5, the posting only mentions monitoring as one step of the ML model lifecycle ("deployment, monitoring and retraining"), not observability tooling or practice, so the broader observability skill is not named and should not be added.

DECISION: drop

## 59. golden_100 - attribute `seniority` (uncertain)

> ...scalable platform solutions. In addition, you bring: - Around 5 years of backend engineering experience, including designing systems yourself. - Proficiency in...

- A: value="mid" · basis="inferred" · signal="Around 5 years of backend engineering experience"
- B: value="mid" · basis="inferred" · signal="Around 5 years of backend engineering experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - The agreed 'mid' rests on the explicit 'Around 5 years of backend engineering experience' line, which is the only seniority evidence in the excerpt and is reasonably read as mid-level; nothing names a senior or lead level, so under rules 1 and 5 I keep the agreed value.

DECISION: ok

## 60. golden_100 - skill `llms` (uncertain)

> ...systems, usage metering, FinOps data, Terraform or GenAI systems is considered an advantage. How do you work? You take ownership of your work from...

- A: `llms` · nice_to_have · raw_text: "GenAI systems is considered an advantage"
- B: `llms` · nice_to_have · raw_text: "GenAI systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the advantage sentence explicitly names "GenAI systems", which is a reasonable match for `llms` at nice_to_have, and the agreed raw_text appears word for word in the posting.

DECISION: ?

## 61. golden_100 - skill `observability` (uncertain)

> ...Kubernetes (EKS) on AWS, Terraform, Helm and ArgoCD. - Observability: Grafana, Prometheus and OpenTelemetry. - CI/CD: GitHub Actions. At DPG Media, we are open to...

- A: `observability` · required · raw_text: "Observability: Grafana, Prometheus and OpenTelemetry"
- B: `observability` · required · raw_text: "Observability"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1 the bullet naming Grafana, Prometheus and OpenTelemetry under observability is a skill-naming sentence, and rule 3 keeps the agreed required status since nothing in the excerpt marks it optional, though the 'Our stack' framing is a weak basis for 'required'.

DECISION: ?

## 62. golden_102 - skill `agents` (uncertain)

> ...training or post-training. - Experience with agent or gaming environments. - Experience with human evaluation, LLM-as-judge...

- A: `agents` · nice_to_have · raw_text: "agent or gaming environments"
- B: `agents` · nice_to_have · raw_text: "Experience with agent or gaming environments"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred qualifications bullet "Experience with agent or gaming environments" names agent work as a qualification, and the agreed nice_to_have requirement and verbatim raw_text match the posting.

DECISION: ok

## 63. golden_102 - skill `llms` (uncertain)

> ...qualifications - Experience with language-model training or post-training. - Experience with agent or gaming...

- A: `llms` · nice_to_have · raw_text: "language-model training"
- B: `llms` · nice_to_have · raw_text: "language-model training"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Preferred qualifications' bullet 'Experience with language-model training or post-training' names a skill, which supports llms as nice_to_have, and the raw_text is quoted verbatim from the posting.

DECISION: ok

## 64. golden_102 - skill `software-engineering` (uncertain)

> ...qualifications - At least five years of ML or software engineering experience, including substantial hands-on work building and...

- A: `software-engineering` · required · raw_text: "software engineering experience"
- B: `software-engineering` · required · raw_text: "reliable production software development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"requirement": "required", "raw_text": "reliable production software development"} - Rule 1 excludes the years-of-experience line "At least five years of ML or software engineering experience", but the minimum-qualifications bullet "alongside reliable production software development" names the skill directly, so I re-anchor the required mention to that quote (rules 1 and 3).

DECISION: {"raw_text": "reliable production software development", "requirement": "required"}

## 65. golden_102 - skill `transformers` (uncertain)

> ...decisions. - Strong Python and experience with PyTorch, Transformers or comparable ML libraries, alongside reliable production...

- A: `transformers` · required · raw_text: "Transformers"
- B: `transformers` · required · raw_text: "Transformers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Minimum qualifications bullet names experience with Transformers as an ML library, and under rule 3 that required mention is quoted in the posting, so the agreed required label stands.

DECISION: ok

## 66. golden_103 - skill `cloud` (uncertain)

> ...AWS experience — designing, deploying, and operating cloud-native services at scale - Experience integrating LLMs, AI models or...

- A: `cloud` · required · raw_text: "cloud-native services"
- B: `cloud` · required · raw_text: "cloud-native services"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What You Bring' bullet names cloud-native services as a requirement, and the quoted raw_text 'cloud-native services' appears verbatim, so the agreed required 'cloud' label stands (rule 3).

DECISION: ok

## 67. golden_104 - skill `ai-deployment` (uncertain)

> ...architecture decisions. - Proven experience training and deploying language models to production. - Experience preparing large-scale training datasets:...

- A: `ai-deployment` · required · raw_text: "deploying language models to production"
- B: `ai-deployment` · required · raw_text: "deploying language models to production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the MINIMUM QUALIFICATIONS bullet "Proven experience training and deploying language models to production" names the skill as a required qualification, and rule 3 confirms the required mention, so the agreed label stands.

DECISION: ok

## 68. golden_104 - skill `evaluation` (uncertain)

> ...and serving frameworks (vLLM, TensorRT-LLM). - Experience evaluating models through online experiments and A/B tests, and working with...

- A: `evaluation` · nice_to_have · raw_text: "Experience evaluating models"
- B: `evaluation` · nice_to_have · raw_text: "evaluating models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the preferred-qualifications bullet "Experience evaluating models through online experiments and A/B tests" names evaluation as a skill, the nice_to_have requirement matches the PREFERRED section, and the raw_text appears verbatim in the posting.

DECISION: ok

## 69. golden_104 - skill `fine-tuning` (uncertain)

> ...building synthetic data generation pipelines for instruction tuning or domain adaptation. - Understanding of memory and GPU...

- A: `fine-tuning` · nice_to_have · raw_text: "instruction tuning"
- B: `fine-tuning` · nice_to_have · raw_text: "instruction tuning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the preferred-qualifications bullet names instruction tuning as an experience requirement, and instruction tuning is a form of fine-tuning, so the agreed nice_to_have label with raw_text "instruction tuning" stands (rule 5 is not violated because the posting names the technique itself).

DECISION: ok

## 70. golden_104 - skill `llms` (uncertain)

> ...review and architecture decisions. - Proven experience training and deploying language models to production. - Experience preparing large-scale training datasets:...

- A: `llms` · required · raw_text: "training and deploying language models to production"
- B: `llms` · required · raw_text: "language models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the MINIMUM QUALIFICATIONS bullet "Proven experience training and deploying language models to production" names LLM work as a required qualification, and the quoted raw_text appears verbatim, so the agreed `llms` required label stands.

DECISION: ok

## 71. golden_104 - skill `transformers` (uncertain)

> ...and PyTorch skills, with production experience using training libraries (Transformers, DeepSpeed, Accelerate). PREFERRED QUALIFICATIONS -...

- A: `transformers` · required · raw_text: "training libraries (Transformers"
- B: `transformers` · required · raw_text: "Transformers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the MINIMUM QUALIFICATIONS bullet names Transformers as a library the candidate needs production experience with, and Rule 3 makes that required mention win, with the agreed raw_text appearing verbatim in the posting.

DECISION: ok

## 72. golden_105 - skill `distributed-systems` (uncertain)

> ...for availability, reliability and scalability, with varied interests in algorithms and distributed systems. Responsibilities - Be on an on-call (PagerDuty)...

- A: `distributed-systems` · nice_to_have · raw_text: "interests in algorithms and distributed systems"
- B: `distributed-systems` · nice_to_have · raw_text: "with varied interests in algorithms and distributed systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_105 - skill `networking` (uncertain)

> ...automation to our operating environments and codebase. You specialize in systems (operating systems, storage subsystems, networking), while implementing best practices for availability,...

- A: `networking` · required · raw_text: "You specialize in systems (operating systems, storage subsystems, networking)"
- B: `networking` · required · raw_text: "networking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the sentence "You specialize in systems (... networking)" describes the candidate the role is seeking rather than a responsibility, so it names a skill in a qualification-style sentence and the agreed required label stands.

DECISION: ok

## 74. golden_106 - skill `knowledge-distillation` (uncertain)

> ...data mixture research, scaling laws, tokenisation, entity representations, distillation, or tabular foundation models such as TabPFN and...

- A: `knowledge-distillation` · required · raw_text: "entity representations, distillation"
- B: `knowledge-distillation` · required · raw_text: "distillation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the sentence 'Relevant experience includes ... distillation' is a qualification line that names the skill, and 'distillation' is the knowledge-distillation technique, so the agreed label stands (rule 3 favours the required reading, and rule 5 adds nothing beyond what is named).

DECISION: ok

## 75. golden_106 - skill `llms` (uncertain)

> ...experiments. For Track 1, this should include pre-training or mid-training of language models. For Track 2, it should include language-model...

- A: `llms` · required · raw_text: "pre-training or mid-training of language models"
- B: `llms` · required · raw_text: "large language models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Minimum qualifications bullet names experience with pre-training or mid-training of language models (Track 1) and language-model post-training (Track 2), so `llms` is a required skill and the agreed raw_text appears verbatim in the posting.

DECISION: ok

## 76. golden_106 - skill `reinforcement-learning` (uncertain)

> ...Track 2, it should include language-model post-training, or reinforcement learning and decision-model training relevant to the specialisation. - Evidence of original...

- A: `reinforcement-learning` · required · raw_text: "or reinforcement learning and decision-model training"
- B: `reinforcement-learning` · required · raw_text: "reinforcement learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the Minimum qualifications bullet names reinforcement learning as an accepted Track 2 experience, and under Rule 3 that required mention stands, with the quoted raw_text appearing word for word.

DECISION: ok

## 77. golden_094 - attribute `degree` (spot-check)

> ...in a downstream application. Minimum qualifications - A PhD or equivalent industry research experience in machine learning, computer science, statistics or a...

- agreed label: value="phd" · requirement="required" · or_equivalent=true · signal="A PhD or equivalent industry research experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The only degree level named is PhD, which is the lowest level the posting names; it sits in the requirements list so it is required, and 'or equivalent industry research experience' sets degree_or_equivalent to true, all as the agreed label states.

DECISION: ok

## 78. golden_094 - skill `distributed-training` (spot-check)

> ...codebase. Research on large language models requires hands-on experience with distributed training. - Clear communication and a collaborative approach to...

- agreed label: `distributed-training` · required · raw_text: "hands-on experience with distributed training"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 79. golden_094 - skill `recommender-systems` (spot-check)

> ...review and mentoring. Preferred qualifications - Experience with recommender systems, generative retrieval, semantic IDs, continual learning,...

- agreed label: `recommender-systems` · nice_to_have · raw_text: "Experience with recommender systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 80. golden_095 - attribute `degree` (spot-check)

> ...in a highly quantitative field, with a focus on AI (MSc or PhD) - At least 6 months of practical experience with LLMs,...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="(MSc or PhD)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "MSc or PhD"} - Per the degree rule, `degree` is the lowest level named, and the posting says "(MSc or PhD)" as a required mention, so the value is `master`, not the older highest-level `phd`.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "MSc or PhD"}

## 81. golden_095 - attribute `german` (spot-check)

> AI Quantitative Researcher | Internship | '27

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 82. golden_095 - skill `agents` (spot-check)

> ...least 6 months of practical experience with LLMs, agents, and harnesses. - Comfort designing evaluation and feedback loops that...

- agreed label: `agents` · required · raw_text: "agents, and harnesses"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 83. golden_095 - skill `python` (spot-check)

> ...research, such as working on math problems. - Python, and exposure to trading. Dates, location, and...

- agreed label: `python` · nice_to_have · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 84. golden_096 - skill `distributed-systems` (spot-check)

> ...from experience building real projects (or close to it). Bonus points if you've worked with distributed systems. - You've actually used PyTorch and HuggingFace and you...

- agreed label: `distributed-systems` · nice_to_have · raw_text: "Bonus points if you've worked with distributed systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_097 - attribute `degree` (spot-check)

> Developer Advocate, Toqan (Prosus AI Platform)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting never names a degree, diploma, or completed studies; its only education reference is the diversity paragraph's 'access to education', so the degree rule's 'when no degree is mentioned' gives null.

DECISION: ok

## 86. golden_097 - attribute `german` (spot-check)

> Developer Advocate, Toqan (Prosus AI Platform)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 87. golden_097 - attribute `seniority` (spot-check)

> ...hours as community needs emerge. WHAT YOU’LL NEED - 3+ years of professional software engineering experience. Comfortable reading, writing, and debugging...

- agreed label: value="mid" · basis="inferred" · signal="3+ years of professional software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_097 - skill `agents` (spot-check)

> ...Backend or full-stack background both fine. - Real hands-on experience with agents or LLM-based systems, not just calling an API. You should...

- agreed label: `agents` · required · raw_text: "hands-on experience with agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_097 - skill `aws` (spot-check)

> ...on it and help others use it. - Some cloud experience (AWS or GCP). Comfortable with the terminal, Git and GitHub workflows,...

- agreed label: `aws` · required · raw_text: "AWS or GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_097 - skill `containerization` (spot-check)

> ...sandboxing or isolation concepts (Firecracker, gVisor, containers). - Experience running workshops, meetups, hackathons,...

- agreed label: `containerization` · nice_to_have · raw_text: "containers"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 91. golden_097 - skill `llms` (spot-check)

> ...both fine. - Real hands-on experience with agents or LLM-based systems, not just calling an API. You should be able to explain...

- agreed label: `llms` · required · raw_text: "LLM-based systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 92. golden_097 - skill `mcp` (spot-check)

> ...model router actually works. - Comfortable working with MCP server infrastructure. You don’t need to have architected one from scratch, but...

- agreed label: `mcp` · required · raw_text: "MCP server infrastructure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 93. golden_097 - skill `python` (spot-check)

> ...reading, writing, and debugging production-quality code. Ideally experienced in Go, Python or TypeScript. Backend or full-stack background both fine. - Real...

- agreed label: `python` · nice_to_have · raw_text: "Ideally experienced in Go, Python or TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_097 - skill `software-engineering` (spot-check)

> ...needs emerge. WHAT YOU’LL NEED - 3+ years of professional software engineering experience. Comfortable reading, writing, and debugging...

- agreed label: `software-engineering` · required · raw_text: "professional software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 95. golden_098 - attribute `degree` (spot-check)

> Machine Learning Engineer - LLMs

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting never names a degree (no bachelor, master, PhD, or 'degree in' wording appears), so under the degree rule's 'none (null) when no degree is mentioned' the agreed null value is correct.

DECISION: ok

## 96. golden_098 - attribute `german` (spot-check)

> Machine Learning Engineer - LLMs

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 97. golden_098 - attribute `seniority` (spot-check)

> ...team engineering standards MINIMUM QUALIFICATIONS - 3+ years of ML engineering experience - Proven experience training and deploying language...

- agreed label: value="mid" · basis="inferred" · signal="3+ years of ML engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_098 - skill `knowledge-distillation` (spot-check)

> ...for production inference: quantization, model compression, distillation, and serving frameworks (vLLM) - Understanding of memory...

- agreed label: `knowledge-distillation` · nice_to_have · raw_text: "distillation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_098 - skill `python` (spot-check)

> ...training stability across long-running multi-node jobs - Expert Python and PyTorch with production experience using training...

- agreed label: `python` · required · raw_text: "Expert Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_098 - skill `pytorch` (spot-check)

> ...across long-running multi-node jobs - Expert Python and PyTorch with production experience using training libraries...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_098 - skill `quantization` (spot-check)

> ...- Experience optimizing models for production inference: quantization, model compression, distillation, and serving frameworks...

- agreed label: `quantization` · nice_to_have · raw_text: "quantization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_099 - attribute `degree` (spot-check)

> Data Scientist, Trust & Safety

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting never names a degree, university qualification, or study level (it asks only for practical experience and a 'solid foundation' in ML, statistics and probability), so under the degree rule 'none (null) when no degree is mentioned' the agreed null is correct.

DECISION: ok

## 103. golden_099 - attribute `seniority` (spot-check)

> Data Scientist, Trust & Safety

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 104. golden_099 - skill `computer-vision` (spot-check)

> ...or behavioural data, natural language processing, or computer vision.</li> <li>Familiarity with the production ML lifecycle,...

- agreed label: `computer-vision` · required · raw_text: "computer vision"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_099 - skill `feature-engineering` (spot-check)

> ...experience preparing training datasets, engineering features, training models and evaluating them against baselines and...

- agreed label: `feature-engineering` · required · raw_text: "engineering features"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 106. golden_099 - skill `nlp` (spot-check)

> ...least one of the following: tabular or behavioural data, natural language processing, or computer vision.</li> <li>Familiarity with the...

- agreed label: `nlp` · required · raw_text: "natural language processing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_099 - skill `python` (spot-check)

> ...learning, statistics and probability theory.</li> <li>Proficiency in Python and SQL, and experience with ML libraries such as...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_099 - skill `scikit-learn` (spot-check)

> ...Python and SQL, and experience with ML libraries such as scikit-learn or PyTorch.</li> <li>Hands-on experience preparing...

- agreed label: `scikit-learn` · required · raw_text: "scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_099 - skill `transformers` (spot-check)

> ...or other Trust &amp; Safety applications.</li> <li>Experience with transformers, multimodal models or LLM-based...

- agreed label: `transformers` · nice_to_have · raw_text: "Experience with transformers"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_100 - attribute `degree` (spot-check)

> Backend Engineer, GenAI Platform

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting never names a degree, university qualification, or level (bachelor, master, PhD), so under the degree rule's 'null when no degree is mentioned' the agreed null is correct.

DECISION: ok

## 111. golden_100 - attribute `german` (spot-check)

> Backend Engineer, GenAI Platform

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 112. golden_100 - skill `argocd` (spot-check)

> ...Kubernetes (EKS) on AWS, Terraform, Helm and ArgoCD. - Observability: Grafana, Prometheus and...

- agreed label: `argocd` · required · raw_text: "ArgoCD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 113. golden_100 - skill `aws` (spot-check)

> ...TypeScript and Python for services and APIs. - Platform: Kubernetes (EKS) on AWS, Terraform, Helm and ArgoCD. - Observability: Grafana,...

- agreed label: `aws` · required · raw_text: "Kubernetes (EKS) on AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 114. golden_100 - skill `go` (spot-check)

> ...long-term scalability in mind. Our stack - Languages: Go for the platform control plane, TypeScript and Python for services and APIs. - Platform:...

- agreed label: `go` · required · raw_text: "Go for the platform control plane"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 115. golden_100 - skill `grafana` (spot-check)

> ...on AWS, Terraform, Helm and ArgoCD. - Observability: Grafana, Prometheus and OpenTelemetry. - CI/CD: GitHub...

- agreed label: `grafana` · required · raw_text: "Grafana"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_100 - skill `prometheus` (spot-check)

> ...Terraform, Helm and ArgoCD. - Observability: Grafana, Prometheus and OpenTelemetry. - CI/CD: GitHub Actions. At DPG...

- agreed label: `prometheus` · required · raw_text: "Prometheus"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_100 - skill `python` (spot-check)

> ...stack - Languages: Go for the platform control plane, TypeScript and Python for services and APIs. - Platform: Kubernetes (EKS) on AWS, Terraform, Helm and...

- agreed label: `python` · required · raw_text: "TypeScript and Python for services and APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_100 - skill `typescript` (spot-check)

> ...stack - Languages: Go for the platform control plane, TypeScript and Python for services and APIs. - Platform: Kubernetes (EKS) on AWS, Terraform, Helm and...

- agreed label: `typescript` · required · raw_text: "TypeScript and Python for services and APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_101 - skill `databricks` (spot-check)

> ...machine learning tools and MLOps systems such as Docker, Databricks, and MLflow • Strong communication skills to clearly...

- agreed label: `databricks` · required · raw_text: "Databricks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 120. golden_101 - skill `machine-learning` (spot-check)

> ...5+ years experience in a similar role • Deep expertise in data science and machine learning, enabling you to design, train, and implement models in...

- agreed label: `machine-learning` · required · raw_text: "data science and machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_101 - skill `mlops` (spot-check)

> ...solutions • Experience with machine learning tools and MLOps systems such as Docker, Databricks, and MLflow • Strong...

- agreed label: `mlops` · required · raw_text: "MLOps systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_102 - attribute `degree` (spot-check)

> Senior Machine Learning Engineer, Evals

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree or degree level anywhere (the only 'education' mention is in the diversity statement, not a requirement), so under the rule's 'none (null) when no degree is mentioned' the agreed null is correct.

DECISION: ok

## 123. golden_102 - attribute `german` (spot-check)

> Senior Machine Learning Engineer, Evals

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 124. golden_102 - skill `machine-learning` (spot-check)

> ...experience, including substantial hands-on work building and evaluating ML systems. - Experience owning evaluation frameworks, benchmarks or...

- agreed label: `machine-learning` · required · raw_text: "building and evaluating ML systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 125. golden_103 - attribute `degree` (spot-check)

> Senior Backend Engineer, AI Platform (Toqan)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree or level anywhere (no degree, bachelor, master, or PhD mention), so the Degree section's rule that `degree` is null when no degree is mentioned applies, and the agreed null values are correct.

DECISION: ok

## 126. golden_103 - attribute `seniority` (spot-check)

> Senior Backend Engineer, AI Platform (Toqan) Who We Are You've ordered dinner...

- agreed label: value="senior" · basis="stated" · signal="Senior Backend Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_103 - skill `ai-developer-tooling` (spot-check)

> ...and platform teams to deliver outcomes end-to-end - Regular, thoughtful use of AI coding tools as part of your development workflow Nice to haves -...

- agreed label: `ai-developer-tooling` · required · raw_text: "Regular, thoughtful use of AI coding tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_103 - skill `ai-infrastructure` (spot-check)

> ...event-sourced systems - Python programming skills - Experience with AI or ML infrastructure and developer productivity tooling Your Typical Day No...

- agreed label: `ai-infrastructure` · nice_to_have · raw_text: "Experience with AI or ML infrastructure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 129. golden_103 - skill `ci-cd` (spot-check)

> ...to reliability, scalability, performance and security - Experience with CI/CD, automated testing and production observability - A...

- agreed label: `ci-cd` · required · raw_text: "Experience with CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_103 - skill `codex` (spot-check)

> ...whether that's Claude Code, Cursor, GitHub Copilot, or OpenAI Codex, and you've developed real judgment about where they...

- agreed label: `codex` · required · raw_text: "OpenAI Codex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 131. golden_103 - skill `cursor` (spot-check)

> ...you work — you use them daily, whether that's Claude Code, Cursor, GitHub Copilot, or OpenAI Codex, and you've developed...

- agreed label: `cursor` · required · raw_text: "Cursor"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_103 - skill `github-copilot` (spot-check)

> ...— you use them daily, whether that's Claude Code, Cursor, GitHub Copilot, or OpenAI Codex, and you've developed real judgment about...

- agreed label: `github-copilot` · required · raw_text: "GitHub Copilot"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 133. golden_103 - skill `llms` (spot-check)

> ...and operating cloud-native services at scale - Experience integrating LLMs, AI models or tool-calling systems into production...

- agreed label: `llms` · required · raw_text: "Experience integrating LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_103 - skill `mcp` (spot-check)

> ...- Familiarity with agentic architectures and protocols such as MCP, A2A - A systems mindset, with attention to reliability,...

- agreed label: `mcp` · required · raw_text: "protocols such as MCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_103 - skill `python` (spot-check)

> ...building or maintaining event-sourced systems - Python programming skills - Experience with AI or ML infrastructure and developer...

- agreed label: `python` · nice_to_have · raw_text: "Python programming skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 136. golden_103 - skill `testing` (spot-check)

> ...performance and security - Experience with CI/CD, automated testing and production observability - A record of working...

- agreed label: `testing` · required · raw_text: "automated testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_103 - skill `tool-calling` (spot-check)

> ...at scale - Experience integrating LLMs, AI models or tool-calling systems into production applications - Familiarity with agentic...

- agreed label: `tool-calling` · required · raw_text: "tool-calling systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 138. golden_104 - attribute `german` (spot-check)

> Senior Machine Learning Engineer – LLMs

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_104 - attribute `seniority` (spot-check)

> Senior Machine Learning Engineer – LLMs Who We Are You've ordered dinner through Just Eat...

- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 140. golden_104 - skill `deepspeed` (spot-check)

> ...with production experience using training libraries (Transformers, DeepSpeed, Accelerate). PREFERRED QUALIFICATIONS - Experience with...

- agreed label: `deepspeed` · required · raw_text: "Transformers, DeepSpeed, Accelerate"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 141. golden_104 - skill `distributed-training` (spot-check)

> ...and data mixture design. - Hands-on experience with distributed training frameworks (Megatron-LM, DeepSpeed, FSDP or Axolotl), including...

- agreed label: `distributed-training` · required · raw_text: "distributed training frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 142. golden_104 - skill `knowledge-distillation` (spot-check)

> ...- Experience optimising models for production inference, including distillation, pruning, quantisation, compression and serving frameworks...

- agreed label: `knowledge-distillation` · nice_to_have · raw_text: "including distillation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_104 - skill `megatron-lm` (spot-check)

> ...and data mixture design. - Hands-on experience with distributed training frameworks (Megatron-LM, DeepSpeed, FSDP or Axolotl), including orchestrating...

- agreed label: `megatron-lm` · required · raw_text: "distributed training frameworks (Megatron-LM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_104 - skill `ml-engineering` (spot-check)

> ...QUALIFICATIONS - At least five years of ML engineering experience, including ownership of projects with measurable business...

- agreed label: `ml-engineering` · required · raw_text: "ML engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 145. golden_104 - skill `quantization` (spot-check)

> ...for production inference, including distillation, pruning, quantisation, compression and serving frameworks (vLLM, TensorRT-LLM). -...

- agreed label: `quantization` · nice_to_have · raw_text: "quantisation, compression"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 146. golden_104 - skill `reinforcement-learning` (spot-check)

> ...with post-training methods such as RLHF, DPO, GRPO or other reinforcement learning approaches for alignment and instruction following. - Experience...

- agreed label: `reinforcement-learning` · nice_to_have · raw_text: "other reinforcement learning approaches"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_104 - skill `tensorrt` (spot-check)

> ...quantisation, compression and serving frameworks (vLLM, TensorRT-LLM). - Experience evaluating models through online...

- agreed label: `tensorrt` · nice_to_have · raw_text: "TensorRT-LLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_104 - skill `vllm` (spot-check)

> ...pruning, quantisation, compression and serving frameworks (vLLM, TensorRT-LLM). - Experience evaluating models through...

- agreed label: `vllm` · nice_to_have · raw_text: "vLLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 149. golden_105 - attribute `seniority` (spot-check)

> Lead/Manager AI Infra Systems Engineering Team About the Role Lead a team of AI Infra (Systems...

- agreed label: value="senior" · basis="stated" · signal="Lead/Manager AI Infra Systems Engineering Team"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 150. golden_105 - skill `cloud` (spot-check)

> ...experience in monitoring and observability practices - Advanced knowledge of cloud services - Ability to thrive in a collaborative environment...

- agreed label: `cloud` · required · raw_text: "Advanced knowledge of cloud services"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_105 - skill `kubernetes` (spot-check)

> ...field or equivalent work experience - Expert knowledge of Ansible (roles, playbooks), Terraform, and Kubernetes - Proficiency in programming/scripting languages -...

- agreed label: `kubernetes` · required · raw_text: "Ansible (roles, playbooks), Terraform, and Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 152. golden_106 - attribute `seniority` (spot-check)

> Senior Applied AI Scientist, Commerce Foundation Models Who We Are You've ordered...

- agreed label: value="senior" · basis="stated" · signal="Senior Applied AI Scientist"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 153. golden_106 - skill `deepspeed` (spot-check)

> ...training methods in frameworks such as Megatron-LM, DeepSpeed, NeMo RL, verl or OpenRLHF, depending on the chosen...

- agreed label: `deepspeed` · nice_to_have · raw_text: "DeepSpeed"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 154. golden_106 - skill `machine-learning` (spot-check)

> ...statistics or a related field. - At least five years of research or applied science experience in machine learning, including doctoral research, with hands-on experience...

- agreed label: `machine-learning` · required · raw_text: "research or applied science experience in machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 155. golden_106 - skill `python` (spot-check)

> ...significant research contributions to deployed systems. - Strong Python and PyTorch skills, with experience implementing...

- agreed label: `python` · required · raw_text: "Strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 156. golden_106 - skill `pytorch` (spot-check)

> ...contributions to deployed systems. - Strong Python and PyTorch skills, with experience implementing experiments and debugging...

- agreed label: `pytorch` · required · raw_text: "PyTorch skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 157. golden_094 - groups `alternative_group` (groups)

> Principal Applied AI Scientist, Commerce Foundation Models

- `a-b-testing` · nice_to_have · raw_text: "online experimentation"
- `distributed-training` · required · raw_text: "hands-on experience with distributed training"
- `knowledge-distillation` · nice_to_have · raw_text: "distillation"
- `machine-learning` · required · raw_text: "applied science experience in machine learning"
- `model-development` · required · raw_text: "experience developing and training models"
- `python` · required · raw_text: "Strong Python"
- `pytorch` · required · raw_text: "PyTorch skills"
- `recommender-systems` · nice_to_have · raw_text: "Experience with recommender systems"
- `reinforcement-learning` · required · raw_text: "deep expertise in pre-training, post-training or reinforcement learning"
- `statistics` · required · raw_text: "statistical judgment"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["recommender-systems", "knowledge-distillation"]] - The preferred qualification 'Experience with recommender systems, generative retrieval, semantic IDs, continual learning, synthetic data, distillation or tabular foundation models' offers any one of several skills for a single ask, and the two labeled members here are not asked for on their own elsewhere, so they form one group under the 'X, Y or Z' marker.

DECISION: [["knowledge-distillation", "recommender-systems"]]

## 158. golden_095 - groups `alternative_group` (groups)

> AI Quantitative Researcher | Internship | '27

- `agents` · required · raw_text: "agents, and harnesses"
- `ai-ml` · required · raw_text: "focus on AI"
- `evaluation` · required · raw_text: "designing evaluation and feedback loops"
- `llms` · required · raw_text: "LLMs"
- `python` · nice_to_have · raw_text: "Python"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The labelled skills are asked together, not offered in place of each other: "at least 6 months of practical experience with LLMs, agents, and harnesses" is an "X, Y and Z" list, which the rule excludes, and no other labelled skill sits in an "at least one of" or "such as" construction.

DECISION: []

## 159. golden_096 - groups `alternative_group` (groups)

> ML Engineering Intern - LLM Research & Development

- `ai-developer-tooling` · nice_to_have · raw_text: "You're friends with AI assistants and use them regularly for coding"
- `distributed-systems` · nice_to_have · raw_text: "Bonus points if you've worked with distributed systems"
- `hugging-face` · nice_to_have · raw_text: "HuggingFace"
- `machine-learning` · nice_to_have · raw_text: "ML fundamentals"
- `model-development` · nice_to_have · raw_text: "trained models yourself"
- `python` · nice_to_have · raw_text: "write good Python code"
- `pytorch` · nice_to_have · raw_text: "used PyTorch"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting asks for PyTorch and HuggingFace together ('used PyTorch and HuggingFace') and offers no 'at least one of', 'X or Y', or example-for-one-ask wording among the labeled skills, so under the alternative_group rule no skills are offered in place of each other.

DECISION: []

## 160. golden_097 - groups `alternative_group` (groups)

> Developer Advocate, Toqan (Prosus AI Platform)

- `agents` · required · raw_text: "hands-on experience with agents"
- `ai-developer-tooling` · required · raw_text: "AI coding tools"
- `aws` · required · raw_text: "AWS or GCP"
- `backend-development` · required · raw_text: "Backend or full-stack background"
- `claude-code` · required · raw_text: "Claude Code"
- `cloud` · required · raw_text: "Some cloud experience"
- `codex` · required · raw_text: "Codex"
- `containerization` · nice_to_have · raw_text: "containers"
- `cursor` · required · raw_text: "Cursor"
- `docker` · required · raw_text: "Docker"
- `full-stack-development` · required · raw_text: "Backend or full-stack background"
- `gcp` · required · raw_text: "AWS or GCP"
- `git` · required · raw_text: "Git and GitHub workflows"
- `github-copilot` · required · raw_text: "Copilot"
- `go` · nice_to_have · raw_text: "Ideally experienced in Go, Python or TypeScript"
- `llms` · required · raw_text: "LLM-based systems"
- `mcp` · required · raw_text: "MCP server infrastructure"
- `python` · nice_to_have · raw_text: "Ideally experienced in Go, Python or TypeScript"
- `software-engineering` · required · raw_text: "professional software engineering experience"
- `tool-calling` · required · raw_text: "tool call"
- `typescript` · nice_to_have · raw_text: "Ideally experienced in Go, Python or TypeScript"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

DECISION: ?

## 161. golden_098 - groups `alternative_group` (groups)

> Machine Learning Engineer - LLMs

- `ai-deployment` · required · raw_text: "deploying language models to production"
- `ci-cd` · required · raw_text: "CI/CD"
- `data-pipelines` · nice_to_have · raw_text: "synthetic data generation pipelines"
- `deepspeed` · required · raw_text: "Transformers, DeepSpeed, Accelerate"
- `distributed-systems` · required · raw_text: "deep understanding of distributed systems"
- `distributed-training` · required · raw_text: "distributed training frameworks"
- `embeddings` · required · raw_text: "(embedding models"
- `evaluation` · required · raw_text: "rigorous evaluation"
- `fine-tuning` · required · raw_text: "or fine-tuning"
- `fsdp` · required · raw_text: "FSDP"
- `git` · required · raw_text: "version control"
- `hugging-face` · nice_to_have · raw_text: "released models on Hugging Face"
- `inference-optimization` · nice_to_have · raw_text: "optimizing models for production inference"
- `knowledge-distillation` · nice_to_have · raw_text: "distillation"
- `llms` · required · raw_text: "or large language models"
- `megatron-lm` · required · raw_text: "Megatron-LM, or Axolotl"
- `model-development` · required · raw_text: "training and deploying language models"
- `model-serving` · nice_to_have · raw_text: "serving frameworks"
- `open-source-llms` · nice_to_have · raw_text: "open-source LLM training projects or tools"
- `python` · required · raw_text: "Expert Python"
- `pytorch` · required · raw_text: "PyTorch"
- `quantization` · nice_to_have · raw_text: "quantization"
- `reinforcement-learning` · nice_to_have · raw_text: "other reinforcement learning approaches"
- `software-engineering` · required · raw_text: "Strong software engineering practices"
- `testing` · required · raw_text: "testing"
- `transformers` · required · raw_text: "Transformers, DeepSpeed"
- `vllm` · nice_to_have · raw_text: "vLLM"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["fsdp", "megatron-lm"], ["embeddings", "llms"]] - Under the alternative_group rule, the 'distributed training frameworks (DeepSpeed, FSDP, Megatron-LM, or Axolotl)' ask leaves deepspeed out because it reappears as an unmarked tech-stack entry, so fsdp and megatron-lm remain as a two-skill group, and the 'embedding models, encoder models, or large language models' examples for one training-experience ask group embeddings and llms.

DECISION: ?

## 162. golden_099 - groups `alternative_group` (groups)

> Data Scientist, Trust & Safety

- `ai-deployment` · required · raw_text: "including deployment"
- `computer-vision` · required · raw_text: "computer vision"
- `data-privacy-and-security` · required · raw_text: "care for data privacy"
- `evaluation` · required · raw_text: "evaluating them against baselines and metrics"
- `feature-engineering` · required · raw_text: "engineering features"
- `llms` · nice_to_have · raw_text: "LLM-based workflows"
- `machine-learning` · required · raw_text: "a solid foundation in machine learning"
- `mlops` · required · raw_text: "Familiarity with the production ML lifecycle"
- `model-development` · required · raw_text: "training models"
- `nlp` · required · raw_text: "natural language processing"
- `python` · required · raw_text: "Proficiency in Python"
- `pytorch` · required · raw_text: "PyTorch"
- `scikit-learn` · required · raw_text: "scikit-learn"
- `sql` · required · raw_text: "SQL"
- `statistics` · required · raw_text: "statistics and probability theory"
- `transformers` · nice_to_have · raw_text: "Experience with transformers"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["computer-vision", "nlp"], ["scikit-learn", "pytorch"], ["transformers", "llms"]] - Under the alternative_group rule's markers, 'at least one of ... computer vision, natural language processing' and 'ML libraries such as scikit-learn or PyTorch' each offer one ask with any one example meeting it, and 'transformers, multimodal models or LLM-based workflows' is an 'X, Y or Z' list where the labelled skills transformers and llms are alternatives, while Python and SQL are asked together and so stay out.

DECISION: [["computer-vision", "nlp"], ["llms", "transformers"], ["pytorch", "scikit-learn"]]

## 163. golden_100 - groups `alternative_group` (groups)

> Backend Engineer, GenAI Platform

- `apis` · required · raw_text: "integrating third-party APIs"
- `argocd` · required · raw_text: "ArgoCD"
- `aws` · required · raw_text: "Kubernetes (EKS) on AWS"
- `backend-development` · required · raw_text: "backend engineering experience"
- `ci-cd` · required · raw_text: "CI/CD: GitHub Actions"
- `github-actions` · required · raw_text: "GitHub Actions"
- `go` · required · raw_text: "Go for the platform control plane"
- `grafana` · required · raw_text: "Grafana"
- `helm` · required · raw_text: "Helm and ArgoCD"
- `kubernetes` · required · raw_text: "running services on Kubernetes"
- `llms` · nice_to_have · raw_text: "GenAI systems is considered an advantage"
- `oauth` · required · raw_text: "OAuth2/OIDC"
- `observability` · required · raw_text: "Observability: Grafana, Prometheus and OpenTelemetry"
- `opentelemetry` · required · raw_text: "OpenTelemetry"
- `prometheus` · required · raw_text: "Prometheus"
- `python` · required · raw_text: "TypeScript and Python for services and APIs"
- `software-architecture` · required · raw_text: "designing systems yourself"
- `terraform` · required · raw_text: "Terraform, Helm and ArgoCD"
- `typescript` · required · raw_text: "TypeScript and Python for services and APIs"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The 'at least one backend language' ask is an alternative set, but Go, TypeScript and Python each reappear as unmarked tech-stack requirements ('Go for the platform control plane', 'TypeScript and Python for services and APIs'), and the rule says a skill asked for on its own elsewhere, including as a tech-stack entry, leaves the group, which drops it below two members.

DECISION: []

## 164. golden_101 - groups `alternative_group` (groups)

> Amsterdam or Antwerp- Combine Data Science, AI, and Media to transform the advertising market. As a Data Scientist Total Video, you will tak

- `ai-deployment` · required · raw_text: "implement models in production environments"
- `data-modeling` · required · raw_text: "Experience transforming data models into scalable data products"
- `data-science` · required · raw_text: "Deep expertise in data science"
- `databricks` · required · raw_text: "Databricks"
- `docker` · required · raw_text: "Docker"
- `machine-learning` · required · raw_text: "data science and machine learning"
- `mlflow` · required · raw_text: "MLflow"
- `mlops` · required · raw_text: "MLOps systems"
- `model-development` · required · raw_text: "design, train, and implement models"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["databricks", "docker", "mlflow"]] - The sentence 'Experience with machine learning tools and MLOps systems such as Docker, Databricks, and MLflow' offers examples for a single ask (the 'such as' marker), so any one meets it and the three form one group, while the broad parent 'MLOps systems' (mlops) stays out per the 'broad skill named alongside its examples' rule.

DECISION: [["databricks", "docker", "mlflow"]]

## 165. golden_102 - groups `alternative_group` (groups)

> Senior Machine Learning Engineer, Evals

- `a-b-testing` · nice_to_have · raw_text: "online experimentation"
- `agents` · nice_to_have · raw_text: "agent or gaming environments"
- `evaluation` · required · raw_text: "owning evaluation frameworks"
- `fine-tuning` · nice_to_have · raw_text: "post-training"
- `llms` · nice_to_have · raw_text: "language-model training"
- `machine-learning` · required · raw_text: "building and evaluating ML systems"
- `model-development` · nice_to_have · raw_text: "language-model training"
- `python` · required · raw_text: "Strong Python"
- `pytorch` · required · raw_text: "PyTorch"
- `recommender-systems` · nice_to_have · raw_text: "recommendation metrics"
- `software-engineering` · required · raw_text: "reliable production software development"
- `statistics` · required · raw_text: "experimental design and statistics"
- `transformers` · required · raw_text: "Transformers"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["fine-tuning", "model-development"], ["a-b-testing", "recommender-systems"], ["pytorch", "transformers"]] - Under the alternative_group rule's markers ('X or Y' and 'X, Y or comparable' for a single ask), the posting offers post-training or language-model training, human evaluation/LLM-as-judge/recommendation metrics/online experimentation, and PyTorch or Transformers as one-of options, while 'or comparable' adds nothing and llms is left out as it is not clearly a named alternative member.

DECISION: ?

## 166. golden_103 - groups `alternative_group` (groups)

> Senior Backend Engineer, AI Platform (Toqan)

- `agent-architecture` · required · raw_text: "Familiarity with agentic architectures"
- `agents` · nice_to_have · raw_text: "Hands-on experience building agentic AI systems"
- `ai-developer-tooling` · required · raw_text: "Regular, thoughtful use of AI coding tools"
- `ai-infrastructure` · nice_to_have · raw_text: "Experience with AI or ML infrastructure"
- `ai-ml` · required · raw_text: "the AI and LLM space — not as a trend to track, but as a domain where you've already done hands-on integration work"
- `aws` · required · raw_text: "Hands-on AWS experience"
- `backend-development` · required · raw_text: "building and operating production backend services"
- `ci-cd` · required · raw_text: "Experience with CI/CD"
- `claude-code` · required · raw_text: "Claude Code"
- `cloud` · required · raw_text: "cloud-native services"
- `codex` · required · raw_text: "OpenAI Codex"
- `cursor` · required · raw_text: "Cursor"
- `event-driven-systems` · nice_to_have · raw_text: "Experience building or maintaining event-sourced systems"
- `github-copilot` · required · raw_text: "GitHub Copilot"
- `go` · required · raw_text: "Strong Go programming skills"
- `llms` · required · raw_text: "Experience integrating LLMs"
- `mcp` · required · raw_text: "protocols such as MCP"
- `observability` · required · raw_text: "production observability"
- `python` · nice_to_have · raw_text: "Python programming skills"
- `software-architecture` · required · raw_text: "owning architectural decisions"
- `testing` · required · raw_text: "automated testing"
- `tool-calling` · required · raw_text: "tool-calling systems"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["claude-code", "cursor", "github-copilot", "codex"]] - The line "regular, thoughtful use of AI coding tools ... whether that's Claude Code, Cursor, GitHub Copilot, or OpenAI Codex" gives examples offered for one ask, so under the markers section these four form one group, while the broad `ai-developer-tooling` skill stays out as the parent of its examples.

DECISION: ?

## 167. golden_104 - groups `alternative_group` (groups)

> Senior Machine Learning Engineer – LLMs

- `a-b-testing` · nice_to_have · raw_text: "online experiments and A/B tests"
- `ai-deployment` · required · raw_text: "deploying language models to production"
- `deepspeed` · required · raw_text: "Transformers, DeepSpeed, Accelerate"
- `distributed-training` · required · raw_text: "distributed training frameworks"
- `evaluation` · nice_to_have · raw_text: "Experience evaluating models"
- `fine-tuning` · nice_to_have · raw_text: "instruction tuning"
- `fsdp` · required · raw_text: "FSDP or Axolotl)"
- `hugging-face` · nice_to_have · raw_text: "released models on Hugging Face"
- `inference-optimization` · nice_to_have · raw_text: "optimising models for production inference"
- `knowledge-distillation` · nice_to_have · raw_text: "including distillation"
- `llms` · required · raw_text: "training and deploying language models to production"
- `megatron-lm` · required · raw_text: "distributed training frameworks (Megatron-LM"
- `ml-engineering` · required · raw_text: "ML engineering experience"
- `model-development` · required · raw_text: "training and deploying language models to production"
- `model-serving` · nice_to_have · raw_text: "serving frameworks"
- `python` · required · raw_text: "Strong Python"
- `pytorch` · required · raw_text: "PyTorch skills"
- `quantization` · nice_to_have · raw_text: "quantisation, compression"
- `reinforcement-learning` · nice_to_have · raw_text: "other reinforcement learning approaches"
- `tensorrt` · nice_to_have · raw_text: "TensorRT-LLM"
- `transformers` · required · raw_text: "training libraries (Transformers"
- `vllm` · nice_to_have · raw_text: "vLLM"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["megatron-lm", "fsdp"]] - The minimum qualifications say "distributed training frameworks (Megatron-LM, DeepSpeed, FSDP or Axolotl)", an 'or' list of examples for one ask, so Megatron-LM and FSDP form a group; DeepSpeed leaves it because "Transformers, DeepSpeed, Accelerate" asks for it on its own, and the broad "distributed training" parent stays out.

DECISION: [["fsdp", "megatron-lm"]]

## 168. golden_105 - groups `alternative_group` (groups)

> Lead/Manager AI Infra Systems Engineering Team

- `ansible` · required · raw_text: "Expert knowledge of Ansible"
- `cloud` · required · raw_text: "Advanced knowledge of cloud services"
- `distributed-systems` · nice_to_have · raw_text: "interests in algorithms and distributed systems"
- `kubernetes` · required · raw_text: "Ansible (roles, playbooks), Terraform, and Kubernetes"
- `networking` · required · raw_text: "You specialize in systems (operating systems, storage subsystems, networking)"
- `observability` · required · raw_text: "monitoring and observability practices"
- `terraform` · required · raw_text: "Ansible (roles, playbooks), Terraform"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - No alternative markers appear: Ansible, Terraform and Kubernetes are all required together, and the networking entry lists areas of specialization rather than one ask that any one example meets, so no skills are offered in place of each other.

DECISION: []

## 169. golden_106 - groups `alternative_group` (groups)

> Senior Applied AI Scientist, Commerce Foundation Models

- `deepspeed` · nice_to_have · raw_text: "DeepSpeed"
- `distributed-training` · required · raw_text: "hands-on experience with distributed training"
- `knowledge-distillation` · required · raw_text: "entity representations, distillation"
- `llms` · required · raw_text: "pre-training or mid-training of language models"
- `machine-learning` · required · raw_text: "research or applied science experience in machine learning"
- `megatron-lm` · nice_to_have · raw_text: "Megatron-LM"
- `model-development` · required · raw_text: "designing and running model-training experiments"
- `python` · required · raw_text: "Strong Python"
- `pytorch` · required · raw_text: "PyTorch skills"
- `recommender-systems` · nice_to_have · raw_text: "Research in recommender systems"
- `reinforcement-learning` · required · raw_text: "or reinforcement learning and decision-model training"
- `statistics` · required · raw_text: "statistical analysis"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["megatron-lm", "deepspeed"]] - The preferred qualification offers frameworks such as Megatron-LM, DeepSpeed, NeMo RL, verl or OpenRLHF as examples for one ask (implementing and debugging training methods), so the two labeled members form one group, and the other listed frameworks are unlabeled and add nothing.

DECISION: [["deepspeed", "megatron-lm"]]
