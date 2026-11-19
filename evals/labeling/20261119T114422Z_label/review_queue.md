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

DECISION: ?

## 15. golden_096 - skill `model-development` (disagreement)

> ...hood. - You understand ML fundamentals because you've trained models yourself and understand the core concepts. - You can make sense...

- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "trained models yourself"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 16. golden_098 - skill `data-pipelines` (disagreement)

> ...BF16, FP8), ZeRO optimization - Track record of building synthetic data generation pipelines for instruction tuning or domain adaptation - Research...

- A: (did not label this)
- B: `data-pipelines` · nice_to_have · raw_text: "synthetic data generation pipelines"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_098 - skill `open-source-llms` (disagreement)

> ...benchmarks used by the community - Contributions to open-source LLM training projects or tools WHAT WE OFFER - High-impact AI projects that are...

- A: (did not label this)
- B: `open-source-llms` · nice_to_have · raw_text: "open-source LLM training projects or tools"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_099 - skill `model-development` (disagreement)

> ...preparing training datasets, engineering features, training models and evaluating them against baselines and...

- A: (did not label this)
- B: `model-development` · required · raw_text: "training models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_100 - skill `software-architecture` (disagreement)

> ...5 years of backend engineering experience, including designing systems yourself. - Proficiency in at least one backend language. We work...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "designing systems yourself"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_101 - skill `ai-deployment` (disagreement)

> ...and machine learning, enabling you to design, train, and implement models in production environments • Experience transforming data models into scalable data...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "implement models in production environments"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_101 - skill `data-modeling` (disagreement)

> ...train, and implement models in production environments • Experience transforming data models into scalable data products, preferably within a media or advertising environment •...

- A: (did not label this)
- B: `data-modeling` · required · raw_text: "Experience transforming data models into scalable data products"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_101 - skill `model-development` (disagreement)

> ...in data science and machine learning, enabling you to design, train, and implement models in production environments • Experience transforming data...

- A: (did not label this)
- B: `model-development` · required · raw_text: "design, train, and implement models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_102 - skill `a-b-testing` (disagreement)

> ...LLM-as-judge calibration, recommendation metrics or online experimentation. - Contributions to evaluation frameworks, public...

- A: `a-b-testing` · nice_to_have · raw_text: "online experimentation"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_102 - skill `fine-tuning` (disagreement)

> ...with language-model training or post-training. - Experience with agent or gaming...

- A: `fine-tuning` · nice_to_have · raw_text: "post-training"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_102 - skill `model-development` (disagreement)

> ...qualifications - Experience with language-model training or post-training. - Experience with agent or gaming...

- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "language-model training"

Options: `A` / `B` / `both` / `drop`

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

DECISION: ?

## 28. golden_103 - skill `event-driven-systems` (disagreement)

> ...that use tools and execute multi-step workflows - Experience building or maintaining event-sourced systems - Python programming skills - Experience with AI or ML...

- A: `event-driven-systems` · nice_to_have · raw_text: "Experience building or maintaining event-sourced systems"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_103 - skill `software-architecture` (disagreement)

> ...patterns and into setting them. You're comfortable owning architectural decisions on novel infrastructure — the kind where the right answer...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "owning architectural decisions"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_104 - skill `model-development` (disagreement)

> ...review and architecture decisions. - Proven experience training and deploying language models to production. - Experience preparing large-scale training datasets:...

- A: (did not label this)
- B: `model-development` · required · raw_text: "training and deploying language models to production"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_105 - skill `software-engineering` (disagreement)

> ...smoothly. You are a blend of a pragmatic operator and a software engineer that applies sound engineering principles, operational discipline, and mature automation to our...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software engineer that applies sound engineering principles"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_106 - skill `model-development` (disagreement)

> ...including doctoral research, with hands-on experience designing and running model-training experiments. For Track 1, this should include pre-training or...

- A: (did not label this)
- B: `model-development` · required · raw_text: "designing and running model-training experiments"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_094 - skill `a-b-testing` (uncertain)

> ...foundation models. - Familiarity with commerce data and online experimentation. - We do not expect expertise in every area. What we...

- A: `a-b-testing` · nice_to_have · raw_text: "online experimentation"
- B: `a-b-testing` · nice_to_have · raw_text: "online experimentation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 34. golden_094 - skill `model-development` (uncertain)

> ...that were published or reached production. - Substantial experience developing and training models, with deep expertise in pre-training, post-training or...

- A: `model-development` · required · raw_text: "experience developing and training models"
- B: `model-development` · required · raw_text: "developing and training models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 35. golden_094 - skill `statistics` (uncertain)

> ...make better decisions. - Sound experimental and statistical judgment, including examples where the evidence changed your...

- A: `statistics` · required · raw_text: "statistical judgment"
- B: `statistics` · required · raw_text: "statistical judgment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 36. golden_095 - skill `evaluation` (uncertain)

> ...experience with LLMs, agents, and harnesses. - Comfort designing evaluation and feedback loops that tell you whether an agent is actually...

- A: `evaluation` · required · raw_text: "designing evaluation and feedback loops"
- B: `evaluation` · required · raw_text: "designing evaluation and feedback loops"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 37. golden_096 - attribute `degree` (uncertain)

> ...internship is open to candidates who are currently enrolled at a university and either hold EU citizenship or are studying in the...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="currently enrolled at a university"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="currently enrolled at a university"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 38. golden_096 - skill `ai-developer-tooling` (uncertain)

> ...from research to data processing when needed. - You're friends with AI assistants and use them regularly for coding and writing. - You can commit to 6-12 months working...

- A: `ai-developer-tooling` · nice_to_have · raw_text: "You're friends with AI assistants and use them regularly for coding"
- B: `ai-developer-tooling` · nice_to_have · raw_text: "AI assistants and use them regularly for coding and writing"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_097 - skill `backend-development` (uncertain)

> ...code. Ideally experienced in Go, Python or TypeScript. Backend or full-stack background both fine. - Real hands-on experience with agents or...

- A: `backend-development` · required · raw_text: "Backend or full-stack background"
- B: `backend-development` · required · raw_text: "Backend"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_097 - skill `claude-code` (uncertain)

> ...setup problems. - You use AI coding tools (Cursor, Claude Code, Copilot, Codex) daily as part of how you work. - Proven...

- A: `claude-code` · required · raw_text: "Claude Code"
- B: `claude-code` · required · raw_text: "Claude Code"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_097 - skill `codex` (uncertain)

> ...- You use AI coding tools (Cursor, Claude Code, Copilot, Codex) daily as part of how you work. - Proven technical...

- A: `codex` · required · raw_text: "Codex"
- B: `codex` · required · raw_text: "Codex"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_097 - skill `cursor` (uncertain)

> ...common setup problems. - You use AI coding tools (Cursor, Claude Code, Copilot, Codex) daily as part of how you...

- A: `cursor` · required · raw_text: "Cursor"
- B: `cursor` · required · raw_text: "Cursor"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

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

DECISION: ?

## 45. golden_097 - skill `open-source-llms` (uncertain)

> ...working AI-powered applications. It combines frontier and open-weight models, agents, tools, sandboxes, memory, context management,...

- A: `open-source-llms` · nice_to_have · raw_text: "open-weight models"
- B: `open-source-llms` · nice_to_have · raw_text: "open-weight models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_097 - skill `tool-calling` (uncertain)

> ...an API. You should be able to explain how an agent loop, tool call, or model router actually works. - Comfortable working...

- A: `tool-calling` · required · raw_text: "tool call"
- B: `tool-calling` · required · raw_text: "tool call"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_098 - skill `ai-deployment` (uncertain)

> ...engineering experience - Proven experience training and deploying language models to production (embedding models, encoder models, or large language...

- A: `ai-deployment` · required · raw_text: "deploying language models to production"
- B: `ai-deployment` · required · raw_text: "deploying language models to production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_098 - skill `embeddings` (uncertain)

> ...training and deploying language models to production (embedding models, encoder models, or large language models) including...

- A: `embeddings` · required · raw_text: "(embedding models"
- B: `embeddings` · required · raw_text: "hands-on experience training language models at scale (from embedding models to specialized LLMs)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_098 - skill `inference-optimization` (uncertain)

> ...for alignment and instruction-following - Experience optimizing models for production inference: quantization, model compression, distillation, and...

- A: `inference-optimization` · nice_to_have · raw_text: "optimizing models for production inference"
- B: `inference-optimization` · nice_to_have · raw_text: "optimizing models for production inference"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_098 - skill `llms` (uncertain)

> ...models to production (embedding models, encoder models, or large language models) including pre-training, continued pre-training, or...

- A: `llms` · required · raw_text: "or large language models"
- B: `llms` · required · raw_text: "hands-on experience training language models at scale (from embedding models to specialized LLMs)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_098 - skill `ml-engineering` (uncertain)

> ...team engineering standards MINIMUM QUALIFICATIONS - 3+ years of ML engineering experience - Proven experience training and deploying language...

- A: `ml-engineering` · required · raw_text: "3+ years of ML engineering experience"
- B: `ml-engineering` · required · raw_text: "ML engineering experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_098 - skill `model-development` (uncertain)

> ...years of ML engineering experience - Proven experience training and deploying language models to production (embedding models, encoder models, or large...

- A: `model-development` · required · raw_text: "training and deploying language models"
- B: `model-development` · required · raw_text: "training and deploying language models to production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

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

DECISION: ?

## 55. golden_099 - skill `data-privacy-and-security` (uncertain)

> ...to apply machine learning to member safety, with care for data privacy and the consequences of incorrect...

- A: `data-privacy-and-security` · required · raw_text: "care for data privacy"
- B: `data-privacy-and-security` · required · raw_text: "care for data privacy"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_099 - skill `evaluation` (uncertain)

> ...datasets, engineering features, training models and evaluating them against baselines and metrics.</li> <li>Experience applying machine learning to at least...

- A: `evaluation` · required · raw_text: "evaluating them against baselines and metrics"
- B: `evaluation` · required · raw_text: "evaluating them against baselines and metrics"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_099 - skill `mlops` (uncertain)

> ...natural language processing, or computer vision.</li> <li>Familiarity with the production ML lifecycle, including deployment, monitoring and...

- A: `mlops` · required · raw_text: "Familiarity with the production ML lifecycle"
- B: `mlops` · required · raw_text: "production ML lifecycle"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_099 - skill `observability` (uncertain)

> ...with the production ML lifecycle, including deployment, monitoring and retraining.</li> <li>Ability to break down problems into manageable...

- A: `observability` · required · raw_text: "monitoring and retraining"
- B: `observability` · required · raw_text: "monitoring"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_100 - attribute `seniority` (uncertain)

> ...scalable platform solutions. In addition, you bring: - Around 5 years of backend engineering experience, including designing systems yourself. - Proficiency in...

- A: value="mid" · basis="inferred" · signal="Around 5 years of backend engineering experience"
- B: value="mid" · basis="inferred" · signal="Around 5 years of backend engineering experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_100 - skill `llms` (uncertain)

> ...systems, usage metering, FinOps data, Terraform or GenAI systems is considered an advantage. How do you work? You take ownership of your work from...

- A: `llms` · nice_to_have · raw_text: "GenAI systems is considered an advantage"
- B: `llms` · nice_to_have · raw_text: "GenAI systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_100 - skill `observability` (uncertain)

> ...Kubernetes (EKS) on AWS, Terraform, Helm and ArgoCD. - Observability: Grafana, Prometheus and OpenTelemetry. - CI/CD: GitHub Actions. At DPG Media, we are open to...

- A: `observability` · required · raw_text: "Observability: Grafana, Prometheus and OpenTelemetry"
- B: `observability` · required · raw_text: "Observability"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_102 - skill `agents` (uncertain)

> ...training or post-training. - Experience with agent or gaming environments. - Experience with human evaluation, LLM-as-judge...

- A: `agents` · nice_to_have · raw_text: "agent or gaming environments"
- B: `agents` · nice_to_have · raw_text: "Experience with agent or gaming environments"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_102 - skill `llms` (uncertain)

> ...qualifications - Experience with language-model training or post-training. - Experience with agent or gaming...

- A: `llms` · nice_to_have · raw_text: "language-model training"
- B: `llms` · nice_to_have · raw_text: "language-model training"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_102 - skill `software-engineering` (uncertain)

> ...qualifications - At least five years of ML or software engineering experience, including substantial hands-on work building and...

- A: `software-engineering` · required · raw_text: "software engineering experience"
- B: `software-engineering` · required · raw_text: "reliable production software development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_102 - skill `transformers` (uncertain)

> ...decisions. - Strong Python and experience with PyTorch, Transformers or comparable ML libraries, alongside reliable production...

- A: `transformers` · required · raw_text: "Transformers"
- B: `transformers` · required · raw_text: "Transformers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_103 - skill `cloud` (uncertain)

> ...AWS experience — designing, deploying, and operating cloud-native services at scale - Experience integrating LLMs, AI models or...

- A: `cloud` · required · raw_text: "cloud-native services"
- B: `cloud` · required · raw_text: "cloud-native services"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_104 - skill `ai-deployment` (uncertain)

> ...architecture decisions. - Proven experience training and deploying language models to production. - Experience preparing large-scale training datasets:...

- A: `ai-deployment` · required · raw_text: "deploying language models to production"
- B: `ai-deployment` · required · raw_text: "deploying language models to production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_104 - skill `evaluation` (uncertain)

> ...and serving frameworks (vLLM, TensorRT-LLM). - Experience evaluating models through online experiments and A/B tests, and working with...

- A: `evaluation` · nice_to_have · raw_text: "Experience evaluating models"
- B: `evaluation` · nice_to_have · raw_text: "evaluating models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_104 - skill `fine-tuning` (uncertain)

> ...building synthetic data generation pipelines for instruction tuning or domain adaptation. - Understanding of memory and GPU...

- A: `fine-tuning` · nice_to_have · raw_text: "instruction tuning"
- B: `fine-tuning` · nice_to_have · raw_text: "instruction tuning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_104 - skill `llms` (uncertain)

> ...review and architecture decisions. - Proven experience training and deploying language models to production. - Experience preparing large-scale training datasets:...

- A: `llms` · required · raw_text: "training and deploying language models to production"
- B: `llms` · required · raw_text: "language models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_104 - skill `transformers` (uncertain)

> ...and PyTorch skills, with production experience using training libraries (Transformers, DeepSpeed, Accelerate). PREFERRED QUALIFICATIONS -...

- A: `transformers` · required · raw_text: "training libraries (Transformers"
- B: `transformers` · required · raw_text: "Transformers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

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

DECISION: ?

## 74. golden_106 - skill `knowledge-distillation` (uncertain)

> ...data mixture research, scaling laws, tokenisation, entity representations, distillation, or tabular foundation models such as TabPFN and...

- A: `knowledge-distillation` · required · raw_text: "entity representations, distillation"
- B: `knowledge-distillation` · required · raw_text: "distillation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_106 - skill `llms` (uncertain)

> ...experiments. For Track 1, this should include pre-training or mid-training of language models. For Track 2, it should include language-model...

- A: `llms` · required · raw_text: "pre-training or mid-training of language models"
- B: `llms` · required · raw_text: "large language models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_106 - skill `reinforcement-learning` (uncertain)

> ...Track 2, it should include language-model post-training, or reinforcement learning and decision-model training relevant to the specialisation. - Evidence of original...

- A: `reinforcement-learning` · required · raw_text: "or reinforcement learning and decision-model training"
- B: `reinforcement-learning` · required · raw_text: "reinforcement learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_094 - attribute `degree` (spot-check)

> ...in a downstream application. Minimum qualifications - A PhD or equivalent industry research experience in machine learning, computer science, statistics or a...

- agreed label: value="phd" · requirement="required" · or_equivalent=true · signal="A PhD or equivalent industry research experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 78. golden_094 - skill `distributed-training` (spot-check)

> ...codebase. Research on large language models requires hands-on experience with distributed training. - Clear communication and a collaborative approach to...

- agreed label: `distributed-training` · required · raw_text: "hands-on experience with distributed training"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 79. golden_094 - skill `recommender-systems` (spot-check)

> ...review and mentoring. Preferred qualifications - Experience with recommender systems, generative retrieval, semantic IDs, continual learning,...

- agreed label: `recommender-systems` · nice_to_have · raw_text: "Experience with recommender systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 80. golden_095 - attribute `degree` (spot-check)

> ...in a highly quantitative field, with a focus on AI (MSc or PhD) - At least 6 months of practical experience with LLMs,...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="(MSc or PhD)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 81. golden_095 - attribute `german` (spot-check)

> AI Quantitative Researcher | Internship | '27

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 82. golden_095 - skill `agents` (spot-check)

> ...least 6 months of practical experience with LLMs, agents, and harnesses. - Comfort designing evaluation and feedback loops that...

- agreed label: `agents` · required · raw_text: "agents, and harnesses"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 83. golden_095 - skill `python` (spot-check)

> ...research, such as working on math problems. - Python, and exposure to trading. Dates, location, and...

- agreed label: `python` · nice_to_have · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_096 - skill `distributed-systems` (spot-check)

> ...from experience building real projects (or close to it). Bonus points if you've worked with distributed systems. - You've actually used PyTorch and HuggingFace and you...

- agreed label: `distributed-systems` · nice_to_have · raw_text: "Bonus points if you've worked with distributed systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_097 - attribute `degree` (spot-check)

> Developer Advocate, Toqan (Prosus AI Platform)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_097 - attribute `german` (spot-check)

> Developer Advocate, Toqan (Prosus AI Platform)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_097 - attribute `seniority` (spot-check)

> ...hours as community needs emerge. WHAT YOU’LL NEED - 3+ years of professional software engineering experience. Comfortable reading, writing, and debugging...

- agreed label: value="mid" · basis="inferred" · signal="3+ years of professional software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_097 - skill `agents` (spot-check)

> ...Backend or full-stack background both fine. - Real hands-on experience with agents or LLM-based systems, not just calling an API. You should...

- agreed label: `agents` · required · raw_text: "hands-on experience with agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_097 - skill `aws` (spot-check)

> ...on it and help others use it. - Some cloud experience (AWS or GCP). Comfortable with the terminal, Git and GitHub workflows,...

- agreed label: `aws` · required · raw_text: "AWS or GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_097 - skill `containerization` (spot-check)

> ...sandboxing or isolation concepts (Firecracker, gVisor, containers). - Experience running workshops, meetups, hackathons,...

- agreed label: `containerization` · nice_to_have · raw_text: "containers"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_097 - skill `llms` (spot-check)

> ...both fine. - Real hands-on experience with agents or LLM-based systems, not just calling an API. You should be able to explain...

- agreed label: `llms` · required · raw_text: "LLM-based systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_097 - skill `mcp` (spot-check)

> ...model router actually works. - Comfortable working with MCP server infrastructure. You don’t need to have architected one from scratch, but...

- agreed label: `mcp` · required · raw_text: "MCP server infrastructure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_097 - skill `python` (spot-check)

> ...reading, writing, and debugging production-quality code. Ideally experienced in Go, Python or TypeScript. Backend or full-stack background both fine. - Real...

- agreed label: `python` · nice_to_have · raw_text: "Ideally experienced in Go, Python or TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_097 - skill `software-engineering` (spot-check)

> ...needs emerge. WHAT YOU’LL NEED - 3+ years of professional software engineering experience. Comfortable reading, writing, and debugging...

- agreed label: `software-engineering` · required · raw_text: "professional software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_098 - attribute `degree` (spot-check)

> Machine Learning Engineer - LLMs

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_098 - attribute `german` (spot-check)

> Machine Learning Engineer - LLMs

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_098 - attribute `seniority` (spot-check)

> ...team engineering standards MINIMUM QUALIFICATIONS - 3+ years of ML engineering experience - Proven experience training and deploying language...

- agreed label: value="mid" · basis="inferred" · signal="3+ years of ML engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_098 - skill `knowledge-distillation` (spot-check)

> ...for production inference: quantization, model compression, distillation, and serving frameworks (vLLM) - Understanding of memory...

- agreed label: `knowledge-distillation` · nice_to_have · raw_text: "distillation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_098 - skill `python` (spot-check)

> ...training stability across long-running multi-node jobs - Expert Python and PyTorch with production experience using training...

- agreed label: `python` · required · raw_text: "Expert Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_098 - skill `pytorch` (spot-check)

> ...across long-running multi-node jobs - Expert Python and PyTorch with production experience using training libraries...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_098 - skill `quantization` (spot-check)

> ...- Experience optimizing models for production inference: quantization, model compression, distillation, and serving frameworks...

- agreed label: `quantization` · nice_to_have · raw_text: "quantization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_099 - attribute `degree` (spot-check)

> Data Scientist, Trust & Safety

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_099 - attribute `seniority` (spot-check)

> Data Scientist, Trust & Safety

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_099 - skill `computer-vision` (spot-check)

> ...or behavioural data, natural language processing, or computer vision.</li> <li>Familiarity with the production ML lifecycle,...

- agreed label: `computer-vision` · required · raw_text: "computer vision"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_099 - skill `feature-engineering` (spot-check)

> ...experience preparing training datasets, engineering features, training models and evaluating them against baselines and...

- agreed label: `feature-engineering` · required · raw_text: "engineering features"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_099 - skill `nlp` (spot-check)

> ...least one of the following: tabular or behavioural data, natural language processing, or computer vision.</li> <li>Familiarity with the...

- agreed label: `nlp` · required · raw_text: "natural language processing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_099 - skill `python` (spot-check)

> ...learning, statistics and probability theory.</li> <li>Proficiency in Python and SQL, and experience with ML libraries such as...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_099 - skill `scikit-learn` (spot-check)

> ...Python and SQL, and experience with ML libraries such as scikit-learn or PyTorch.</li> <li>Hands-on experience preparing...

- agreed label: `scikit-learn` · required · raw_text: "scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_099 - skill `transformers` (spot-check)

> ...or other Trust &amp; Safety applications.</li> <li>Experience with transformers, multimodal models or LLM-based...

- agreed label: `transformers` · nice_to_have · raw_text: "Experience with transformers"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_100 - attribute `degree` (spot-check)

> Backend Engineer, GenAI Platform

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_100 - attribute `german` (spot-check)

> Backend Engineer, GenAI Platform

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_100 - skill `argocd` (spot-check)

> ...Kubernetes (EKS) on AWS, Terraform, Helm and ArgoCD. - Observability: Grafana, Prometheus and...

- agreed label: `argocd` · required · raw_text: "ArgoCD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_100 - skill `aws` (spot-check)

> ...TypeScript and Python for services and APIs. - Platform: Kubernetes (EKS) on AWS, Terraform, Helm and ArgoCD. - Observability: Grafana,...

- agreed label: `aws` · required · raw_text: "Kubernetes (EKS) on AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_100 - skill `go` (spot-check)

> ...long-term scalability in mind. Our stack - Languages: Go for the platform control plane, TypeScript and Python for services and APIs. - Platform:...

- agreed label: `go` · required · raw_text: "Go for the platform control plane"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

## 118. golden_100 - skill `typescript` (spot-check)

> ...stack - Languages: Go for the platform control plane, TypeScript and Python for services and APIs. - Platform: Kubernetes (EKS) on AWS, Terraform, Helm and...

- agreed label: `typescript` · required · raw_text: "TypeScript and Python for services and APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_101 - skill `databricks` (spot-check)

> ...machine learning tools and MLOps systems such as Docker, Databricks, and MLflow • Strong communication skills to clearly...

- agreed label: `databricks` · required · raw_text: "Databricks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

## 123. golden_102 - attribute `german` (spot-check)

> Senior Machine Learning Engineer, Evals

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_102 - skill `machine-learning` (spot-check)

> ...experience, including substantial hands-on work building and evaluating ML systems. - Experience owning evaluation frameworks, benchmarks or...

- agreed label: `machine-learning` · required · raw_text: "building and evaluating ML systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_103 - attribute `degree` (spot-check)

> Senior Backend Engineer, AI Platform (Toqan)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_103 - attribute `seniority` (spot-check)

> Senior Backend Engineer, AI Platform (Toqan) Who We Are You've ordered dinner...

- agreed label: value="senior" · basis="stated" · signal="Senior Backend Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_103 - skill `ai-developer-tooling` (spot-check)

> ...and platform teams to deliver outcomes end-to-end - Regular, thoughtful use of AI coding tools as part of your development workflow Nice to haves -...

- agreed label: `ai-developer-tooling` · required · raw_text: "Regular, thoughtful use of AI coding tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_103 - skill `ai-infrastructure` (spot-check)

> ...event-sourced systems - Python programming skills - Experience with AI or ML infrastructure and developer productivity tooling Your Typical Day No...

- agreed label: `ai-infrastructure` · nice_to_have · raw_text: "Experience with AI or ML infrastructure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_103 - skill `ci-cd` (spot-check)

> ...to reliability, scalability, performance and security - Experience with CI/CD, automated testing and production observability - A...

- agreed label: `ci-cd` · required · raw_text: "Experience with CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_103 - skill `codex` (spot-check)

> ...whether that's Claude Code, Cursor, GitHub Copilot, or OpenAI Codex, and you've developed real judgment about where they...

- agreed label: `codex` · required · raw_text: "OpenAI Codex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_103 - skill `cursor` (spot-check)

> ...you work — you use them daily, whether that's Claude Code, Cursor, GitHub Copilot, or OpenAI Codex, and you've developed...

- agreed label: `cursor` · required · raw_text: "Cursor"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_103 - skill `github-copilot` (spot-check)

> ...— you use them daily, whether that's Claude Code, Cursor, GitHub Copilot, or OpenAI Codex, and you've developed real judgment about...

- agreed label: `github-copilot` · required · raw_text: "GitHub Copilot"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_103 - skill `llms` (spot-check)

> ...and operating cloud-native services at scale - Experience integrating LLMs, AI models or tool-calling systems into production...

- agreed label: `llms` · required · raw_text: "Experience integrating LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_103 - skill `mcp` (spot-check)

> ...- Familiarity with agentic architectures and protocols such as MCP, A2A - A systems mindset, with attention to reliability,...

- agreed label: `mcp` · required · raw_text: "protocols such as MCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_103 - skill `python` (spot-check)

> ...building or maintaining event-sourced systems - Python programming skills - Experience with AI or ML infrastructure and developer...

- agreed label: `python` · nice_to_have · raw_text: "Python programming skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_103 - skill `testing` (spot-check)

> ...performance and security - Experience with CI/CD, automated testing and production observability - A record of working...

- agreed label: `testing` · required · raw_text: "automated testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_103 - skill `tool-calling` (spot-check)

> ...at scale - Experience integrating LLMs, AI models or tool-calling systems into production applications - Familiarity with agentic...

- agreed label: `tool-calling` · required · raw_text: "tool-calling systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_104 - attribute `german` (spot-check)

> Senior Machine Learning Engineer – LLMs

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_104 - attribute `seniority` (spot-check)

> Senior Machine Learning Engineer – LLMs Who We Are You've ordered dinner through Just Eat...

- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_104 - skill `deepspeed` (spot-check)

> ...with production experience using training libraries (Transformers, DeepSpeed, Accelerate). PREFERRED QUALIFICATIONS - Experience with...

- agreed label: `deepspeed` · required · raw_text: "Transformers, DeepSpeed, Accelerate"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_104 - skill `distributed-training` (spot-check)

> ...and data mixture design. - Hands-on experience with distributed training frameworks (Megatron-LM, DeepSpeed, FSDP or Axolotl), including...

- agreed label: `distributed-training` · required · raw_text: "distributed training frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

## 145. golden_104 - skill `quantization` (spot-check)

> ...for production inference, including distillation, pruning, quantisation, compression and serving frameworks (vLLM, TensorRT-LLM). -...

- agreed label: `quantization` · nice_to_have · raw_text: "quantisation, compression"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

## 149. golden_105 - attribute `seniority` (spot-check)

> Lead/Manager AI Infra Systems Engineering Team About the Role Lead a team of AI Infra (Systems...

- agreed label: value="senior" · basis="stated" · signal="Lead/Manager AI Infra Systems Engineering Team"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_105 - skill `cloud` (spot-check)

> ...experience in monitoring and observability practices - Advanced knowledge of cloud services - Ability to thrive in a collaborative environment...

- agreed label: `cloud` · required · raw_text: "Advanced knowledge of cloud services"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_105 - skill `kubernetes` (spot-check)

> ...field or equivalent work experience - Expert knowledge of Ansible (roles, playbooks), Terraform, and Kubernetes - Proficiency in programming/scripting languages -...

- agreed label: `kubernetes` · required · raw_text: "Ansible (roles, playbooks), Terraform, and Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_106 - attribute `seniority` (spot-check)

> Senior Applied AI Scientist, Commerce Foundation Models Who We Are You've ordered...

- agreed label: value="senior" · basis="stated" · signal="Senior Applied AI Scientist"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_106 - skill `deepspeed` (spot-check)

> ...training methods in frameworks such as Megatron-LM, DeepSpeed, NeMo RL, verl or OpenRLHF, depending on the chosen...

- agreed label: `deepspeed` · nice_to_have · raw_text: "DeepSpeed"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_106 - skill `machine-learning` (spot-check)

> ...statistics or a related field. - At least five years of research or applied science experience in machine learning, including doctoral research, with hands-on experience...

- agreed label: `machine-learning` · required · raw_text: "research or applied science experience in machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_106 - skill `python` (spot-check)

> ...significant research contributions to deployed systems. - Strong Python and PyTorch skills, with experience implementing...

- agreed label: `python` · required · raw_text: "Strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 156. golden_106 - skill `pytorch` (spot-check)

> ...contributions to deployed systems. - Strong Python and PyTorch skills, with experience implementing experiments and debugging...

- agreed label: `pytorch` · required · raw_text: "PyTorch skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
