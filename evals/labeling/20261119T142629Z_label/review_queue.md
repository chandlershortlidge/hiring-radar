# Review queue - 20261119T142629Z_label

155 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261119T142629Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 143 accepted labels,
seed 0) of labels A and B already agreed on. They measure the error rate that
agreement alone cannot: two labelers can agree and both be wrong. They print the posting
excerpt and the agreed label only - no `A:`/`B:` lines - so you check the label against the
posting rather than against the labelers, who by construction both said the same thing.

The first 15 items ask whether each posting belongs in the held-out set at all.
They come pre-answered `yes`, so leaving them alone keeps every posting. Answer `no <why>`
and that posting is written to `evals/goldens/excluded.json` with your reason instead of
becoming a Golden, and neither this script nor `new_goldens.py` will pick it again. Use it
for a posting that got past the title and city filters but is not the job market we
measure - a marketing role, a listing in the wrong field. The rest of that posting's items
are then ignored, so you can answer `no` and skip them.

## 1. golden_094 - scope `in_scope` (in-scope)

> Principal Software Engineer, Applied AI – Splunk Observability Cloud

- Cisco · Principal Software Engineer, Applied AI – Splunk Observability Cloud
- San Jose · en · jsearch · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_095 - scope `in_scope` (in-scope)

> Software Quality Engineer - AI & Automation

- TikTok USDS Joint Venture · Software Quality Engineer - AI & Automation
- San Jose · en · jsearch · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_096 - scope `in_scope` (in-scope)

> Gen AI Engineer: Prompting, LLMs

- Valiant Technologies LLC · Gen AI Engineer: Prompting, LLMs
- San Jose · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_097 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer, E-Commerce

- TikTok USDS Joint Venture LLC · Senior Machine Learning Engineer, E-Commerce San Jose Regular R&D Job ID: A106976
- San Jose · en · jsearch · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_098 - scope `in_scope` (in-scope)

> AI Software Engineer (LLM Agents & RAG Pipelines)

- Celestica International LP · AI Software Engineer (LLM Agents & RAG Pipelines)
- San Jose · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_099 - scope `in_scope` (in-scope)

> 2027 University Graduate - Machine Learning Engineer

- Adobe · 2027 University Graduate - Machine Learning Engineer
- San Jose · en · jsearch · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_100 - scope `in_scope` (in-scope)

> Machine Learning Platform Engineer, Applied Machine Learning Team San Jose Regular

- Bytedance · Machine Learning Platform Engineer, Applied Machine Learning Team San Jose Regular
- San Jose · en · jsearch · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_101 - scope `in_scope` (in-scope)

> Machine Learning Engineer, Personalization & Scalable Systems

- TikTok Inc. · Machine Learning Engineer, Personalization & Scalable Systems
- San Jose · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_102 - scope `in_scope` (in-scope)

> AI & Data Engineer – Python / FastAPI

- Programming.com · AI & Data Engineer – Python / FastAPI
- San Jose · en · jsearch · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_103 - scope `in_scope` (in-scope)

> AI Engineer Lead - Visa Independent Consultants Only

- Shrive Technologies · AI Engineer Lead - Visa Independent Consultants Only
- San Jose · en · jsearch · 20 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_104 - scope `in_scope` (in-scope)

> Remote AI Engineer

- Turnblock.io · Remote AI Engineer
- San Jose · en · jsearch · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_105 - scope `in_scope` (in-scope)

> Field AI Engineer — Edge

- Analog Devices, Inc. · Field AI Engineer — Edge
- San Jose · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_106 - scope `in_scope` (in-scope)

> Senior AI / Machine Learning Engineer Fraud Prevention

- Adobe Systems Inc · Senior AI / Machine Learning Engineer Fraud Prevention
- San Jose · en · jsearch · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_107 - scope `in_scope` (in-scope)

> Senior Staff AI Engineer — Multimodal for Smart Glasses

- Google LLC · Senior Staff AI Engineer — Multimodal for Smart Glasses
- San Jose · en · jsearch · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_108 - scope `in_scope` (in-scope)

> AI Engineer 4 (AI Platforms)

- Capital One · AI Engineer 4 (AI Platforms)
- San Jose · en · jsearch · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_094 - skill `ai-deployment` (disagreement)

> ...3+ years of experience designing, building, and deploying production-grade LLM-based systems, including at least one agentic system with active tool...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying production-grade LLM-based systems"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Rule 1 applies: the required Minimum Qualifications bullet names deploying production-grade LLM-based systems, and that quote appears verbatim in the posting, so labeler B's required ai-deployment tag stands (rule 3).

DECISION: B

## 17. golden_095 - skill `ai-ml` (disagreement)

> ...scalable test automation, or productivity tools. - Experience with AI tools, with an understanding of practical use to improve testing...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Experience with AI tools"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the Minimum Qualifications bullet "Experience with AI tools, with an understanding of practical use to improve testing efficiency" names an AI skill as a required qualification, and rule 3 makes that required mention win, so labeler B's `ai-ml` tag stands.

DECISION: B

## 18. golden_095 - skill `workflow-automation` (disagreement)

> ...AI testing frameworks, autonomous testing agents or intelligent automation solutions - Working knowledge of large-scale distributed systems...

- A: (did not label this)
- B: `workflow-automation` · nice_to_have · raw_text: "intelligent automation solutions"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the Preferred Qualifications sentence 'building AI testing frameworks, autonomous testing agents or intelligent automation solutions' names an automation skill as a qualification, and the nice_to_have requirement and quoted raw_text match the posting verbatim, so labeler B's version stands.

DECISION: ?

## 19. golden_098 - attribute `seniority` (disagreement)

> ...and deliver documentation and demonstrations Requirements 1 to 3 years of related experience Bachelor’s degree or equivalent combination of education...

- A: value="junior" · basis="inferred" · signal="1 to 3 years of related experience"
- B: value="senior" · basis="inferred" · signal="Lead hardware engineering use case projects"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 4, the "Lead hardware engineering use case projects" bullet is a responsibility the candidate is not asked to have, so it cannot support senior; the only requirement-side signal is "1 to 3 years of related experience," which supports junior as labeler A said.

DECISION: A

## 20. golden_099 - skill `ai-ml` (disagreement)

> ...your application may not move forward in the process. At Adobe, we empower employees to innovate with AI — and we look for candidates eager to do the same. As part of the hiring experience, we provide clear...

- A: (did not label this)
- B: `ai-ml` · nice_to_have · raw_text: "At Adobe, we empower employees to innovate with AI — and we look for candidates eager to do the same."

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1, the only AI mention is company-culture and interview-policy boilerplate ('we empower employees to innovate with AI', 'eager to do the same'), not a qualification bullet naming a skill the candidate must or should have, so ai-ml does not belong in the key.

DECISION: drop

## 21. golden_101 - skill `machine-learning` (disagreement)

> ...& Scalable Systems TikTok USDS Joint Venture is seeking a PhD-level candidate to advance machine learning across recommendation, search, and e-commerce systems. You...

- A: `machine-learning` · required · raw_text: "seeking a PhD-level candidate to advance machine learning"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the sentence "seeking a PhD-level candidate to advance machine learning" is a candidate-facing qualification that names the skill, not just the job title, and under rule 3 the required framing stands, so labeler A's required tag is supported.

DECISION: ?

## 22. golden_101 - skill `recommender-systems` (disagreement)

> ...USDS Joint Venture is seeking a PhD-level candidate to advance machine learning across recommendation, search, and e-commerce systems. You will design scalable...

- A: `recommender-systems` · required · raw_text: "advance machine learning across recommendation"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 3, the candidate is sought "to advance machine learning across recommendation" systems, so the required mention of recommendation work stands as labeled by A, and rule 4 does not exclude it because the candidate is explicitly asked for this.

DECISION: ?

## 23. golden_103 - skill `evaluation` (disagreement)

> ...equivalent like Agent Development Kit). Knowledge of standard ML evaluation metrics for Generative and Classification models (e.g., BLEURT,...

- A: `evaluation` · nice_to_have · raw_text: "standard ML evaluation metrics"
- B: `evaluation` · required · raw_text: "model training, evaluation, and deployment"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Rule 3: the required qualification ('Proven ability to design and implement end-to-end ML pipelines for data management, model training, evaluation, and deployment') is a required mention that outranks the preferred-section mention labeler A used, so `evaluation` is required.

DECISION: B

## 24. golden_103 - skill `google-adk` (disagreement)

> ...AutoGen, LlamaIndex, or internal equivalent like Agent Development Kit). Knowledge of standard ML evaluation metrics for...

- A: `google-adk` · nice_to_have · raw_text: "Agent Development Kit"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the preferred-qualifications sentence explicitly names the Agent Development Kit as an example framework, and that mention is the determining quote, so the skill counts as nice_to_have as labeler A had it.

DECISION: A

## 25. golden_103 - skill `model-development` (disagreement)

> ...and implement end-to-end ML pipelines for data management, model training, evaluation, and deployment. Demonstrated ability to lead...

- A: (did not label this)
- B: `model-development` · required · raw_text: "model training"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualification sentence "design and implement end-to-end ML pipelines for ... model training, evaluation, and deployment" names model training as a required skill, and rule 3 keeps the required mention quoted as "model training".

DECISION: B

## 26. golden_104 - skill `data-pipelines` (disagreement)

> ...systems • Understand that the hardest problems are in data ingestion, normalization, temporal alignment and ground truth •...

- A: (did not label this)
- B: `data-pipelines` · required · raw_text: "data ingestion"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'Who you are' qualification sentence names data ingestion ('the hardest problems are in data ingestion, normalization, temporal alignment'), which supports data-pipelines as required, and rule 3 keeps that required mention, so B's label stands.

DECISION: ?

## 27. golden_106 - skill `mlops` (disagreement)

> ...capabilities. What you'll need to succeed 8+ years building and operating production ML systems, ideally in fraud, abuse, risk, identity, trust & safety,...

- A: (did not label this)
- B: `mlops` · required · raw_text: "building and operating production ML systems"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 3, the required qualification "building and operating production ML systems" (with the required bullet on taking ML systems to production deployment and monitoring) supports mlops, and labeler A did not label it, so B's required tag stands.

DECISION: ?

## 28. golden_108 - skill `distributed-training` (disagreement)

> ...novel techniques in production • Proficiency in designing distributed systems for model training, evaluation, and online inference at petabyte scale •...

- A: `distributed-training` · nice_to_have · raw_text: "distributed systems for model training"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under Rule 1, the Preferred Qualifications sentence "Proficiency in designing distributed systems for model training, evaluation, and online inference" names distributed model training as a skill, and Rule 3 doesn't apply because nothing in the posting makes it required, so A's nice_to_have label with that raw_text stands.

DECISION: A

## 29. golden_108 - skill `evaluation` (disagreement)

> ...workflows, similarity search, guardrails, model evaluation, experimentation, governance, and observability, etc. •...

- A: (did not label this)
- B: `evaluation` · nice_to_have · raw_text: "evaluation"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 4, the only mention of "model evaluation" sits in the "What You'll Do" responsibilities list, and the excerpt shows no qualification bullet asking for it, so the skill does not belong in the key.

DECISION: drop

## 30. golden_108 - skill `machine-learning` (disagreement)

> ...plus at least 4 years of experience developing AI and ML algorithms or technologies, or a Master's degree in Computer Science, AI, Electrical...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "ML algorithms or technologies"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the Basic Qualifications bullet requiring experience developing AI and ML algorithms or technologies names a skill, and rule 3 makes that required mention count, with the quoted raw_text appearing verbatim in the posting.

DECISION: B

## 31. golden_108 - skill `model-development` (disagreement)

> ...and support AI software components including foundation model training, large language model inference, agents and multi-agent...

- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "model training"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 4, the only shown text mentioning model training ('foundation model training') sits in the 'What You'll Do' responsibilities list, and no qualification asks the candidate for this skill, so it does not belong in the key.

DECISION: drop

## 32. golden_108 - skill `model-serving` (disagreement)

> ...distributed systems for model training, evaluation, and online inference at petabyte scale • Experience defining AI model...

- A: (did not label this)
- B: `model-serving` · nice_to_have · raw_text: "online inference"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the preferred-qualifications sentence names designing systems for online inference at petabyte scale, which supports a nice_to_have model-serving tag quoted as "online inference" (rule 5 is not violated because the serving context is named).

DECISION: B

## 33. golden_108 - skill `software-architecture` (disagreement)

> ...retaining schedules • Demonstrated ability to influence architectural decisions across multiple AI product lines or platforms Capital One...

- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "architectural decisions"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under Rule 1, the Preferred Qualifications bullet "Demonstrated ability to influence architectural decisions across multiple AI product lines or platforms" names a skill, so software-architecture stands as nice_to_have with the verbatim raw_text "architectural decisions" (Rule 5 is not violated because the text names architecture work directly).

DECISION: B

## 34. golden_094 - skill `agents` (uncertain)

> ...deploying production-grade LLM-based systems, including at least one agentic system with active tool use. • Experience developing evaluation...

- A: `agents` · required · raw_text: "at least one agentic system"
- B: `agents` · required · raw_text: "agentic system with active tool use"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Minimum Qualifications bullet names experience with an agentic system, and under rule 3 the required mention 'at least one agentic system' (quoted verbatim) supports the agreed `agents` label at required level.

DECISION: ok

## 35. golden_094 - skill `cloud` (uncertain)

> ...tracing and alerting workflows. • Experience working with cloud-native infrastructure at scale, specifically Kubernetes. • History of active open-source...

- A: `cloud` · nice_to_have · raw_text: "cloud-native infrastructure at scale"
- B: `cloud` · nice_to_have · raw_text: "cloud-native infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Qualifications bullet names cloud-native infrastructure at scale, so `cloud` counts, and the nice_to_have requirement and verbatim raw_text match the posting (rule 5 doesn't call for adding anything beyond that).

DECISION: ok

## 36. golden_094 - skill `mcp` (uncertain)

> ...or observability ecosystems (e.g., OpenTelemetry, MCP). • Experience leading customer-zero or field-deployed...

- A: `mcp` · nice_to_have · raw_text: "MCP"
- B: `mcp` · nice_to_have · raw_text: "MCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Qualifications bullet names MCP directly as an open-source ecosystem the candidate should have contributed to, so the nice_to_have label with raw_text "MCP" is supported as agreed.

DECISION: ok

## 37. golden_094 - skill `observability` (uncertain)

> ...security guardrails for AI. Preferred Qualifications • Experience with Observability, SRE, or incident management domains, including...

- A: `observability` · nice_to_have · raw_text: "Experience with Observability"
- B: `observability` · nice_to_have · raw_text: "Observability"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Qualifications bullet "Experience with Observability, SRE, or incident management domains" names observability as a qualification, so the agreed nice_to_have label and its verbatim raw_text are correct.

DECISION: ok

## 38. golden_094 - skill `rag` (uncertain)

> ...scoring, and release validation. • Experience engineering retrieval and context pipelines for structured and semi-structured data, such as...

- A: `rag` · required · raw_text: "retrieval and context pipelines"
- B: `rag` · required · raw_text: "retrieval and context pipelines"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required minimum-qualifications bullet on "retrieval and context pipelines" for structured and semi-structured data, set alongside LLM-based systems, names retrieval-augmented work, so the agreed required `rag` label stands.

DECISION: ok

## 39. golden_094 - skill `software-engineering` (uncertain)

> ...product features. Minimum Qualifications • 12+ years of professional software engineering experience. • 3+ years of experience designing, building, and...

- A: `software-engineering` · required · raw_text: "professional software engineering experience"
- B: `software-engineering` · required · raw_text: "professional software engineering experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only mention of software engineering is the years-of-experience bullet "12+ years of professional software engineering experience," which does not count as a skill, and no other required mention names it.

DECISION: drop

## 40. golden_095 - skill `evaluation` (uncertain)

> ...testing workflow or engineering pipelines - Background in benchmarking and evaluating AI agents for effectiveness, reliability, and output quality -...

- A: `evaluation` · nice_to_have · raw_text: "benchmarking and evaluating AI agents"
- B: `evaluation` · nice_to_have · raw_text: "benchmarking and evaluating AI agents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Qualifications bullet "Background in benchmarking and evaluating AI agents for effectiveness, reliability, and output quality" names the evaluation activity as a qualification, so the agreed nice_to_have label and raw_text stand.

DECISION: ok

## 41. golden_096 - attribute `seniority` (uncertain)

> ...workflows with Langchain, Langgraph and LangSmith, and lead prompt engineering to improve model performance. You will perform...

- A: value="senior" · basis="inferred" · signal="lead prompt engineering"
- B: value="senior" · basis="inferred" · signal="lead prompt engineering to improve model performance"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 4, "lead prompt engineering" is a responsibility listed under "You will" and does not establish a required seniority level, and the title "Gen AI Engineer" carries no seniority word (rule 1), so the seniority attribute should be null.

DECISION: drop

## 42. golden_097 - skill `nlp` (uncertain)

> ...in one or more of the following fields: Machine Learning, Natural Language Processing (NLP), or Computer Vision. • Proficiency in software development...

- A: `nlp` · required · raw_text: "Natural Language Processing (NLP)"
- B: `nlp` · required · raw_text: "Natural Language Processing (NLP)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"requirement": "nice_to_have", "raw_text": "multilingual NLP"} - Under rule 1 the required 'Natural Language Processing (NLP)' is only inside a years-of-experience line, which does not count, but the preferred bullet 'Proficiency in multilingual NLP' names NLP as a skill, so the skill stays as nice_to_have.

DECISION: ?

## 43. golden_097 - skill `software-engineering` (uncertain)

> ...Natural Language Processing (NLP), or Computer Vision. • Proficiency in software development with at least one of the following programming languages:...

- A: `software-engineering` · required · raw_text: "Proficiency in software development"
- B: `software-engineering` · required · raw_text: "software development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Minimum Qualifications, the bullet "Proficiency in software development with at least one of the following programming languages" is a required skill named in a qualification bullet, so rule 1 supports keeping software-engineering as required (rule 3 also applies).

DECISION: ok

## 44. golden_099 - skill `software-engineering` (uncertain)

> ...applied statistics, machine learning, data mining, and software development. Familiarity with working with large-scale datasets and...

- A: `software-engineering` · required · raw_text: "software development"
- B: `software-engineering` · required · raw_text: "software development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the sentence "Ideal candidates will have ... technical skills including ... software development" names the skill as a candidate qualification, and the quoted raw_text appears verbatim, so the agreed required label stands.

DECISION: ok

## 45. golden_100 - skill `distributed-systems` (uncertain)

> ...languages (such as Python and Golang).- In-depth understanding of distributed computing and principles and technologies of large-scale data...

- A: `distributed-systems` · required · raw_text: "understanding of distributed computing"
- B: `distributed-systems` · required · raw_text: "distributed computing"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_100 - skill `go` (uncertain)

> ...using common programming languages (such as Python and Golang).- In-depth understanding of distributed computing and...

- A: `go` · required · raw_text: "Golang"
- B: `go` · required · raw_text: "Golang"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Minimum Qualifications bullet names Golang as a required programming language, and rule 3 makes that required mention decisive, so the agreed `go` label with raw_text "Golang" is correct.

DECISION: ok

## 47. golden_100 - skill `python` (uncertain)

> ...in developing using common programming languages (such as Python and Golang).- In-depth understanding of distributed...

- A: `python` · required · raw_text: "Python"
- B: `python` · required · raw_text: "Python"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_100 - skill `software-engineering` (uncertain)

> ...engineering, or a related field.- At least 3 years of experience in software engineering and be proficient in developing using common programming...

- A: `software-engineering` · required · raw_text: "experience in software engineering"
- B: `software-engineering` · required · raw_text: "experience in software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only mention is the years-of-experience line "At least 3 years of experience in software engineering," which does not count as a skill, and the other occurrence is a degree field in the education line, so the skill should not be in the key.

DECISION: ?

## 49. golden_101 - attribute `degree` (uncertain)

> ...& Scalable Systems TikTok USDS Joint Venture is seeking a PhD-level candidate to advance machine learning across recommendation, search,...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="PhD-level candidate"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="PhD-level candidate"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_102 - skill `async-processing` (uncertain)

> ...delivering LLM agent systems, evaluations, FastAPI, and Async Python. • Experience with structured outputs, web-search...

- A: `async-processing` · required · raw_text: "Async Python"
- B: `async-processing` · required · raw_text: "Async Python"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Required Skills bullet names "Async Python" as a skill the candidate must have hands-on experience with, and rule 3 makes that required mention decisive, so the agreed required label stands.

DECISION: ok

## 51. golden_102 - skill `llms` (uncertain)

> ...and SQL experience. • Hands-on experience delivering LLM agent systems, evaluations, FastAPI, and Async Python. • Experience with...

- A: `llms` · required · raw_text: "LLM agent systems"
- B: `llms` · required · raw_text: "LLM agent systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Required Skills bullet "Hands-on experience delivering LLM agent systems" names an LLM skill as required, and rule 3 supports the verbatim raw_text "LLM agent systems", so the agreed label stands.

DECISION: ok

## 52. golden_103 - skill `data-privacy-and-security` (uncertain)

> ...managing highly sensitive data (e.g., PII/PHI) and implementing strict access control and encryption mechanisms. Strong analytical and debugging skills, with the ability...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "implementing strict access control and encryption mechanisms"
- B: `data-privacy-and-security` · nice_to_have · raw_text: "Experience managing highly sensitive data (e.g., PII/PHI) and implementing strict access control and encryption mechanisms."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Qualifications sentence names data privacy work (managing PII/PHI with strict access control and encryption), and the agreed raw_text appears verbatim and supports the skill at nice_to_have, so the agreed label stands.

DECISION: ok

## 53. golden_103 - skill `devops` (uncertain)

> ...of experience in software engineering, ML engineering, or MLOps/DevOps, focusing on the ML lifecycle (continuous training, model...

- A: `devops` · required · raw_text: "MLOps/DevOps"
- B: `devops` · required · raw_text: "DevOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only mention of DevOps is inside the 8+ years of experience line ('experience in software engineering, ML engineering, or MLOps/DevOps'), which is a years-of-experience line and does not count as naming a skill; the visible CI/CD and container bullets name other tools, not `devops`.

DECISION: ?

## 54. golden_103 - skill `docker` (uncertain)

> ...Experience working with large-scale production deployment, container orchestration (e.g., Kubernetes, Docker), and CI/CD pipelines (e.g., Jenkins, GitLab CI)....

- A: `docker` · required · raw_text: "container orchestration (e.g., Kubernetes, Docker)"
- B: `docker` · required · raw_text: "Kubernetes, Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Minimum Qualifications sentence names Docker directly in "container orchestration (e.g., Kubernetes, Docker)", and under rule 3 that required mention is the determining quote, so the agreed required `docker` label stands.

DECISION: ok

## 55. golden_103 - skill `gcp` (uncertain)

> ...2+ years in a technical lead role. Strong experience with Google Cloud Platform (GCP) MLOps services (Vertex AI, Kubeflow) or equivalent...

- A: `gcp` · required · raw_text: "Google Cloud Platform (GCP)"
- B: `gcp` · required · raw_text: "Google Cloud Platform (GCP)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Minimum Qualifications bullet names GCP as a required experience area, and the quoted raw_text "Google Cloud Platform (GCP)" is the determining mention, so the agreed required label stands even though an open-source alternative is offered.

DECISION: ok

## 56. golden_103 - skill `kubernetes` (uncertain)

> ...Experience working with large-scale production deployment, container orchestration (e.g., Kubernetes, Docker), and CI/CD pipelines (e.g., Jenkins, GitLab CI)....

- A: `kubernetes` · required · raw_text: "container orchestration (e.g., Kubernetes, Docker)"
- B: `kubernetes` · required · raw_text: "Kubernetes, Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Minimum Qualifications sentence asks for container orchestration experience and names Kubernetes as its example, and under rule 3 that required mention, quoted word for word, supports keeping the agreed label.

DECISION: ok

## 57. golden_103 - skill `ml-engineering` (uncertain)

> ...8+ years of experience in software engineering, ML engineering, or MLOps/DevOps, focusing on the ML lifecycle (continuous...

- A: `ml-engineering` · required · raw_text: "ML engineering"
- B: `ml-engineering` · required · raw_text: "ML engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only mention of "ML engineering" is inside the years-of-experience line ("8+ years of experience in software engineering, ML engineering, or MLOps/DevOps"), which does not count, and the job title "AI Engineer Lead" does not count either.

DECISION: drop

## 58. golden_103 - skill `mlops` (uncertain)

> ...of experience in software engineering, ML engineering, or MLOps/DevOps, focusing on the ML lifecycle (continuous training, model...

- A: `mlops` · required · raw_text: "MLOps/DevOps"
- B: `mlops` · required · raw_text: "MLOps services"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"requirement": "required", "raw_text": "Strong experience with Google Cloud Platform (GCP) MLOps services"} - Under rule 1 the agreed quote "MLOps/DevOps" sits in a years-of-experience line that doesn't count, but the qualification sentence "Strong experience with Google Cloud Platform (GCP) MLOps services" names MLOps as a required skill, so rule 3 makes that the determining mention.

DECISION: {"requirement": "required", "raw_text": "Strong experience with Google Cloud Platform (GCP) MLOps services"}

## 59. golden_103 - skill `software-engineering` (uncertain)

> ...Minimum Qualifications: 8+ years of experience in software engineering, ML engineering, or MLOps/DevOps, focusing on the ML...

- A: `software-engineering` · required · raw_text: "software engineering"
- B: `software-engineering` · required · raw_text: "software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only quoted mention is "8+ years of experience in software engineering, ML engineering, or MLOps/DevOps", which is a years-of-experience line rather than a named skill, so `software-engineering` should not be in the key.

DECISION: drop

## 60. golden_104 - attribute `seniority` (uncertain)

> ...zero-to-one product development. What we’re looking for • 3+ years experience (5+ preferred) building and shipping production AI systems, ideally...

- A: value="mid" · basis="inferred" · signal="3+ years experience (5+ preferred)"
- B: value="mid" · basis="inferred" · signal="3+ years experience (5+ preferred)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1 the quoted years-of-experience line is the only seniority evidence, and the 3+ minimum with a 5+ preference supports the agreed 'mid' value at inferred basis, with the signal quoted verbatim.

DECISION: ok

## 61. golden_104 - skill `agent-state-management` (uncertain)

> ...agent systems in production with orchestration, tool use, state management and human-in-the-loop workflows • Worked with...

- A: `agent-state-management` · required · raw_text: "state management"
- B: `agent-state-management` · required · raw_text: "state management"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What you have done' list is candidate experience the posting asks for, so the bullet naming 'state management' counts, and the agreed required label with raw_text 'state management' is supported verbatim (rules 1 and 3).

DECISION: ok

## 62. golden_104 - skill `llm-orchestration` (uncertain)

> ...sensor streams) What you have done • Built and shipped agent systems in production with orchestration, tool use, state management and human-in-the-loop...

- A: `llm-orchestration` · required · raw_text: "agent systems in production with orchestration"
- B: `llm-orchestration` · required · raw_text: "orchestration"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification bullet 'Built and shipped agent systems in production with orchestration, tool use, state management' names agent orchestration as a required experience, so the agreed required llm-orchestration label stands as written.

DECISION: ok

## 63. golden_106 - attribute `degree` (uncertain)

> ...and ability to solve ambiguous, adversarial problems. Bachelor's or equivalent experience in Computer Science, Statistics, Mathematics, or related field; advanced degree a plus. Preferred Attributes Device...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor's or equivalent experience in Computer Science, Statistics, Mathematics, or related field"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor's or equivalent experience in Computer Science, Statistics, Mathematics, or related field; advanced degree a plus."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under the degree rule, the lowest level named is bachelor, and the bare requirements-list mention "Bachelor's or equivalent experience" is required with or_equivalent true; "advanced degree a plus" is a higher level the posting welcomes, so it is not recorded.

DECISION: ok

## 64. golden_106 - skill `ai-deployment` (uncertain)

> ...SQL, and current ML frameworks like PyTorch. Experience guiding ML systems from feature engineering to production deployment and monitoring. Strong software/data engineering skills...

- A: `ai-deployment` · required · raw_text: "guiding ML systems from feature engineering to production deployment"
- B: `ai-deployment` · required · raw_text: "production deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification sentence "Experience guiding ML systems from feature engineering to production deployment and monitoring" names the deployment skill, and the agreed raw_text is quoted verbatim from it, so the agreed required label stands.

DECISION: ok

## 65. golden_106 - skill `evaluation` (uncertain)

> ...and automated control systems. Human-in-the-loop or AI-assisted evaluation systems. Distributed systems and high-scale data pipelines. Strong...

- A: `evaluation` · nice_to_have · raw_text: "AI-assisted evaluation systems"
- B: `evaluation` · nice_to_have · raw_text: "Human-in-the-loop or AI-assisted evaluation systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Attributes bullet "Human-in-the-loop or AI-assisted evaluation systems" is a qualification that names the skill, and the agreed nice_to_have requirement and raw_text quote it word for word, so the label stands.

DECISION: ok

## 66. golden_106 - skill `observability` (uncertain)

> ...guiding ML systems from feature engineering to production deployment and monitoring. Strong software/data engineering skills across ML,...

- A: `observability` · required · raw_text: "production deployment and monitoring"
- B: `observability` · required · raw_text: "monitoring"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet names monitoring of production ML systems ("production deployment and monitoring"), which is a reasonable mapping to observability, and rule 5 doesn't block it because the text names monitoring directly.

DECISION: ?

## 67. golden_107 - skill `ai-deployment` (uncertain)

> ...ML leadership, systems thinking, and a track record in deploying large-scale AI with Generative AI capabilities across complex, matrixed...

- A: `ai-deployment` · required · raw_text: "deploying large-scale AI"
- B: `ai-deployment` · required · raw_text: "deploying large-scale AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification sentence "a track record in deploying large-scale AI" names the skill, and the agreed required label and verbatim raw_text "deploying large-scale AI" match the posting.

DECISION: ok

## 68. golden_107 - skill `machine-learning` (uncertain)

> ...to push voice and vision integration. This role demands extensive ML leadership, systems thinking, and a track record in deploying...

- A: `machine-learning` · required · raw_text: "extensive ML leadership"
- B: `machine-learning` · required · raw_text: "extensive ML leadership"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification sentence "This role demands extensive ML leadership" names machine learning (ML), and rule 3 makes that required mention decisive, so the agreed label stands.

DECISION: ok

## 69. golden_108 - attribute `degree` (uncertain)

> ...developing AI and ML algorithms or technologies, or a Master's degree in Computer Science, AI, Electrical Engineering, Computer Engineering, or related fields plus at least 2 years of experience developing AI and ML...

- A: value="master" · requirement="required" · or_equivalent=false · signal="a Master's degree in Computer Science, AI, Electrical Engineering, Computer Engineering, or related fields"
- B: value="master" · requirement="required" · or_equivalent=false · signal="Bachelor's Degree in Computer Science, AI, Electrical Engineering, Computer Engineering, or related fields plus at least 4 years of experience developing AI and ML algorithms or technologies, or a Master's degree in Computer Science, AI, Electrical Engineering, Computer Engineering, or related fields plus at least 2 years of experience developing AI and ML algorithms or technologies"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_108 - attribute `seniority` (uncertain)

> ...data governance, and compliance standards are met • Mentor Principal and Senior Associates on scalable design, performance tuning and research-to-production...

- A: value="senior" · basis="inferred" · signal="Mentor Principal and Senior Associates on scalable design"
- B: value="senior" · basis="inferred" · signal="Mentor Principal and Senior Associates on scalable design, performance tuning and research-to-production translation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the responsibilities describe senior-level ownership and leadership, and the quoted signal 'Mentor Principal and Senior Associates on scalable design' appears verbatim in the posting, so the agreed 'senior' value with basis 'inferred' is supported.

DECISION: ok

## 71. golden_108 - skill `agent-state-management` (uncertain)

> ...(e.g. LLM Inference, Similarity Search and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or Golang • Experience...

- A: `agent-state-management` · nice_to_have · raw_text: "Guardrails, Memory"
- B: `agent-state-management` · nice_to_have · raw_text: "Memory"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_108 - skill `ai-deployment` (uncertain)

> ...latency, throughput and accuracy • 6+ years of experience deploying scalable and responsible AI solutions on cloud platforms (e.g. AWS, Google Cloud, Azure, or...

- A: `ai-deployment` · nice_to_have · raw_text: "deploying scalable and responsible AI solutions"
- B: `ai-deployment` · nice_to_have · raw_text: "deploying scalable and responsible AI solutions"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the preferred-qualifications bullet "6+ years of experience deploying scalable and responsible AI solutions on cloud platforms" names the skill, and the nice_to_have level and quoted raw_text both match the posting.

DECISION: ok

## 73. golden_108 - skill `ai-ml` (uncertain)

> ...or related fields plus at least 4 years of experience developing AI and ML algorithms or technologies, or a Master's degree in Computer Science, AI, Electrical...

- A: `ai-ml` · required · raw_text: "developing AI and ML algorithms or technologies"
- B: `ai-ml` · required · raw_text: "developing AI and ML algorithms or technologies"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Basic Qualifications bullet requiring "at least 4 years of experience developing AI and ML algorithms or technologies" is a qualification that names the ai-ml skill, and rule 3 makes that required mention decisive, so the agreed required label stands.

DECISION: ok

## 74. golden_108 - skill `inference-optimization` (uncertain)

> ...developing and applying state-of-the-art techniques for optimizing training and inference software to improve hardware utilization, latency, throughput, and...

- A: `inference-optimization` · nice_to_have · raw_text: "optimizing training and inference software"
- B: `inference-optimization` · nice_to_have · raw_text: "optimizing training and inference software"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the Preferred Qualifications bullet about optimizing training and inference software for latency, throughput, and cost names this skill, the nice_to_have tier matches the section heading, and the agreed raw_text appears word for word (Rule 3).

DECISION: ok

## 75. golden_108 - skill `vector-search` (uncertain)

> ...AI and ML algorithms or technologies (e.g. LLM Inference, Similarity Search and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or...

- A: `vector-search` · nice_to_have · raw_text: "Similarity Search and VectorDBs"
- B: `vector-search` · nice_to_have · raw_text: "Similarity Search"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Qualifications bullet names "Similarity Search and VectorDBs" as an experience area, so vector-search counts as a nice_to_have skill with the agreed raw_text, and rule 5 adds nothing broader.

DECISION: ok

## 76. golden_094 - attribute `degree` (spot-check)

> Principal Software Engineer, Applied AI – Splunk Observability Cloud

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree level or degree phrase anywhere; the only mention is the generic word "education" in the pay-determination paragraph, so under the rule `degree` is null (`null` when no degree is mentioned).

DECISION: ok

## 77. golden_094 - attribute `german` (spot-check)

> Principal Software Engineer, Applied AI – Splunk Observability Cloud

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 78. golden_094 - skill `llms` (spot-check)

> ...3+ years of experience designing, building, and deploying production-grade LLM-based systems, including at least one agentic system with active tool...

- agreed label: `llms` · required · raw_text: "production-grade LLM-based systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 79. golden_094 - skill `opentelemetry` (spot-check)

> ...AI, agent frameworks, or observability ecosystems (e.g., OpenTelemetry, MCP). • Experience leading customer-zero or...

- agreed label: `opentelemetry` · nice_to_have · raw_text: "OpenTelemetry"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 80. golden_094 - skill `tool-calling` (spot-check)

> ...systems, including at least one agentic system with active tool use. • Experience developing evaluation frameworks for AI/ML...

- agreed label: `tool-calling` · required · raw_text: "active tool use"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 81. golden_095 - attribute `degree` (spot-check)

> ...practices Qualifications Minimum Qualifications - BS in Computer Science or related fields - Proficiency in at least one programming language (e.g.,...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="BS in Computer Science or related fields"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The only degree level named is 'BS in Computer Science or related fields' under Minimum Qualifications, so the lowest-level rule gives bachelor; a bare mention in a requirements list is required, 'or related fields' widens the field and not the requirement, so or_equivalent is false and the agreed label stands.

DECISION: ok

## 82. golden_095 - attribute `german` (spot-check)

> Software Quality Engineer - AI & Automation

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 83. golden_095 - attribute `seniority` (spot-check)

> ...Go, Java, etc.). - Experience with web and mobile tests - Proven experience building scalable test automation, or productivity tools. - Experience with AI tools, with...

- agreed label: value="mid" · basis="inferred" · signal="Proven experience building scalable test automation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_095 - skill `agents` (spot-check)

> ...test strategies and use cases - Experience with integrating AI agents into testing workflow or engineering pipelines -...

- agreed label: `agents` · nice_to_have · raw_text: "integrating AI agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 85. golden_095 - skill `go` (spot-check)

> ...in at least one programming language (e.g., Python, Go, Java, etc.). - Experience with web and mobile tests -...

- agreed label: `go` · required · raw_text: "Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 86. golden_095 - skill `testing` (spot-check)

> ...web and mobile tests - Proven experience building scalable test automation, or productivity tools. - Experience with AI tools, with...

- agreed label: `testing` · required · raw_text: "test automation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 87. golden_097 - skill `computer-vision` (spot-check)

> ...Machine Learning, Natural Language Processing (NLP), or Computer Vision. • Proficiency in software development with at least one...

- agreed label: `computer-vision` · required · raw_text: "Computer Vision"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_097 - skill `cpp` (spot-check)

> ...with at least one of the following programming languages: C++, Python, Go, or Java. Preferred Qualifications •...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_097 - skill `go` (spot-check)

> ...and efficient shopping experience while upholding a robust governance and risk control framework to ensure platform...

- agreed label: `go` · required · raw_text: "Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_097 - skill `knowledge-distillation` (spot-check)

> ...Qualifications • Experience in fine-tuning, distillation, or reinforcement learning for large language models in conversational AI...

- agreed label: `knowledge-distillation` · nice_to_have · raw_text: "distillation, or reinforcement learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 91. golden_097 - skill `llms` (spot-check)

> ...fine-tuning, distillation, or reinforcement learning for large language models in conversational AI applications. • Proficiency in...

- agreed label: `llms` · nice_to_have · raw_text: "large language models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_097 - skill `machine-learning` (spot-check)

> Senior Machine Learning Engineer, E-Commerce San Jose Regular R&D Job ID:...

- agreed label: `machine-learning` · required · raw_text: "Machine Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 93. golden_097 - skill `python` (spot-check)

> ...at least one of the following programming languages: C++, Python, Go, or Java. Preferred Qualifications • Experience in...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 94. golden_098 - attribute `degree` (spot-check)

> ...Requirements 1 to 3 years of related experience Bachelor’s degree or equivalent combination of education and experience Benefits A comprehensive benefits package is offered in...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor’s degree or equivalent combination of education and experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names only one degree level, a Bachelor's, so `degree: bachelor` is the lowest and only level under the degree rule; it is a bare requirements-list mention, so `required` is correct, and the "or equivalent combination of education and experience" wording sets `degree_or_equivalent` to true and matches the quoted signal.

DECISION: ok

## 95. golden_099 - attribute `degree` (spot-check)

> ...new products and features. What You Need to Succeed • PhD or MS in Computer Science, Statistics, Electrical Engineering, Applied Math, Operations Research, Econometrics or equivalent experience required with an expected graduation date of December 2026 – June...

- agreed label: value="phd" · requirement="required" · or_equivalent=true · signal="PhD or MS in Computer Science, Statistics, Electrical Engineering, Applied Math, Operations Research, Econometrics or equivalent experience required"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": true, "degree_signal": "PhD or MS in Computer Science, Statistics, Electrical Engineering, Applied Math, Operations Research, Econometrics or equivalent experience required"} - The degree rule records the lowest level named, and this posting names "PhD or MS", so the level is master rather than the older highest-level phd; the bare requirements-list mention stays required and "or equivalent experience" sets degree_or_equivalent to true.

DECISION: {"degree": "master", "degree_or_equivalent": true, "degree_requirement": "required", "degree_signal": "PhD or MS in Computer Science, Statistics, Electrical Engineering, Applied Math, Operations Research, Econometrics or equivalent experience required"}

## 96. golden_099 - attribute `german` (spot-check)

> 2027 University Graduate - Machine Learning Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 97. golden_099 - attribute `seniority` (spot-check)

> 2027 University Graduate - Machine Learning Engineer The Opportunity Adobe is...

- agreed label: value="junior" · basis="stated" · signal="University Graduate"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_099 - skill `deep-learning` (spot-check)

> ...understanding of statistical modeling, machine learning, deep learning, or data mining concepts, and a track record of solving...

- agreed label: `deep-learning` · required · raw_text: "deep learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_099 - skill `java` (spot-check)

> ...one or more programming languages such as Python, Scala, Java and C • Familiar with one or more machine learning or...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_099 - skill `machine-learning` (spot-check)

> ...0-2+ years of experience in specific relevant skills • Deep understanding of statistical modeling, machine learning, deep learning, or data mining concepts, and a track...

- agreed label: `machine-learning` · required · raw_text: "Deep understanding of statistical modeling, machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_099 - skill `scala` (spot-check)

> ...and analytics techniques. • Develop and implement scalable and efficient modeling algorithms that can work with...

- agreed label: `scala` · required · raw_text: "Scala"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_100 - attribute `seniority` (spot-check)

> ...science, software engineering, or a related field.- At least 3 years of experience in software engineering and be proficient in developing using common programming...

- agreed label: value="mid" · basis="inferred" · signal="At least 3 years of experience in software engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_101 - attribute `seniority` (spot-check)

> Machine Learning Engineer, Personalization & Scalable Systems

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 104. golden_102 - attribute `degree` (spot-check)

> AI & Data Engineer – Python / FastAPI

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree anywhere (no bachelor, master, PhD, or 'degree in' wording), so the rule's 'none (null) when no degree is mentioned' applies and the agreed null label is correct.

DECISION: ok

## 105. golden_102 - attribute `german` (spot-check)

> AI & Data Engineer – Python / FastAPI

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 106. golden_102 - skill `airflow` (spot-check)

> ...grounding, and citation checks. • Strong experience with Apache Airflow and Apache Iceberg or similar lakehouse technologies. •...

- agreed label: `airflow` · required · raw_text: "Apache Airflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_102 - skill `claude-code` (spot-check)

> ...with pytest, ruff, and mypy. • Daily experience using Claude Code or Codex. Nice to Have • LangGraph, entity resolution,...

- agreed label: `claude-code` · required · raw_text: "Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_102 - skill `codex` (spot-check)

> ...ruff, and mypy. • Daily experience using Claude Code or Codex. Nice to Have • LangGraph, entity resolution, and...

- agreed label: `codex` · required · raw_text: "Codex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_102 - skill `evaluation` (spot-check)

> ...Hands-on experience delivering LLM agent systems, evaluations, FastAPI, and Async Python. • Experience with structured...

- agreed label: `evaluation` · required · raw_text: "evaluations"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_102 - skill `langgraph` (spot-check)

> ...experience using Claude Code or Codex. Nice to Have • LangGraph, entity resolution, and graph/entity data. • AWS Lake...

- agreed label: `langgraph` · nice_to_have · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_102 - skill `postgresql` (spot-check)

> ...technologies. • Knowledge of Trino, AWS Athena, AWS Glue, PostgreSQL, and Cube semantic layer. • Experience with pytest, ruff,...

- agreed label: `postgresql` · required · raw_text: "PostgreSQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 112. golden_102 - skill `sql` (spot-check)

> ...Skills • 5+ years of production Python and SQL experience. • Hands-on experience delivering LLM agent systems,...

- agreed label: `sql` · required · raw_text: "SQL experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 113. golden_103 - attribute `degree` (spot-check)

> AI Engineer Lead - Visa Independent Consultants Only

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree or level anywhere (no bachelor, master, PhD, or 'degree' wording), so the degree rule's 'none (`null`) when no degree is mentioned' applies and the agreed null is correct.

DECISION: ok

## 114. golden_103 - attribute `german` (spot-check)

> AI Engineer Lead - Visa Independent Consultants Only

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_103 - attribute `seniority` (spot-check)

> AI Engineer Lead - Visa Independent Consultants Only Key Responsibilities:...

- agreed label: value="senior" · basis="stated" · signal="AI Engineer Lead"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_103 - skill `a-b-testing` (spot-check)

> ...in production, including data/concept drift detection, A/B testing, and building quality dashboards (e.g., Grafana, Datadog)...

- agreed label: `a-b-testing` · nice_to_have · raw_text: "A/B testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 117. golden_103 - skill `ci-cd` (spot-check)

> ...container orchestration (e.g., Kubernetes, Docker), and CI/CD pipelines (e.g., Jenkins, GitLab CI). Experience with production...

- agreed label: `ci-cd` · required · raw_text: "CI/CD pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_103 - skill `containerization` (spot-check)

> ...Experience working with large-scale production deployment, container orchestration (e.g., Kubernetes, Docker), and CI/CD pipelines (e.g.,...

- agreed label: `containerization` · required · raw_text: "container orchestration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_103 - skill `distributed-systems` (spot-check)

> ...languages such as Python or Go, and experience with large-scale data processing and distributed systems. Experience working with large-scale production...

- agreed label: `distributed-systems` · required · raw_text: "large-scale data processing and distributed systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_103 - skill `gitlab-ci` (spot-check)

> ...(e.g., Kubernetes, Docker), and CI/CD pipelines (e.g., Jenkins, GitLab CI). Experience with production operations for distributed...

- agreed label: `gitlab-ci` · required · raw_text: "(e.g., Jenkins, GitLab CI)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_103 - skill `go` (spot-check)

> ...Airflow, MLflow). Proficiency in programming languages such as Python or Go, and experience with large-scale data processing and...

- agreed label: `go` · required · raw_text: "such as Python or Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 122. golden_103 - skill `kubeflow` (spot-check)

> ...experience with Google Cloud Platform (GCP) MLOps services (Vertex AI, Kubeflow) or equivalent open-source ecosystems (Apache Airflow,...

- agreed label: `kubeflow` · required · raw_text: "(Vertex AI, Kubeflow)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 123. golden_103 - skill `langchain` (spot-check)

> ...Models (LLMs) and open-source Agentic AI frameworks (e.g., LangChain, AutoGen, LlamaIndex, or internal equivalent like Agent...

- agreed label: `langchain` · nice_to_have · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 124. golden_103 - skill `llms` (spot-check)

> ...multiple partner priorities. Preferred Qualifications: Familiarity with Large Language Models (LLMs) and open-source Agentic AI frameworks (e.g., LangChain,...

- agreed label: `llms` · nice_to_have · raw_text: "Familiarity with Large Language Models (LLMs)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 125. golden_103 - skill `python` (spot-check)

> ...Airflow, MLflow). Proficiency in programming languages such as Python or Go, and experience with large-scale data processing and...

- agreed label: `python` · required · raw_text: "such as Python or Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 126. golden_103 - skill `vertex-ai` (spot-check)

> ...experience with Google Cloud Platform (GCP) MLOps services (Vertex AI, Kubeflow) or equivalent open-source ecosystems (Apache Airflow,...

- agreed label: `vertex-ai` · required · raw_text: "(Vertex AI, Kubeflow)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_104 - attribute `degree` (spot-check)

> Remote AI Engineer

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting never names a degree or level (no degree, bachelor's, master's, or PhD requirement); the only university mention is that the team includes researchers from Harvard/MIT, so the degree label should stay null under the 'none (null) when no degree is mentioned' rule.

DECISION: ok

## 128. golden_104 - attribute `german` (spot-check)

> Remote AI Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 129. golden_104 - skill `fastapi` (spot-check)

> ...both depth and execution Tech stackTypeScript, Python, FastAPI, Agentic AI, OpenCV, PostgreSQL, React Native Why...

- agreed label: `fastapi` · required · raw_text: "FastAPI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_104 - skill `knowledge-graphs` (spot-check)

> ...operational data • Designed or contributed to ontology, knowledge graph or structured context systems grounded in real asset...

- agreed label: `knowledge-graphs` · required · raw_text: "knowledge graph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 131. golden_104 - skill `model-serving` (spot-check)

> ...mapping • Shipped end-to-end systems from ingestion and model serving through backend services (Python, TypeScript) to frontend...

- agreed label: `model-serving` · required · raw_text: "model serving"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_104 - skill `postgresql` (spot-check)

> ...stackTypeScript, Python, FastAPI, Agentic AI, OpenCV, PostgreSQL, React Native Why candidates should joinCategory-defining...

- agreed label: `postgresql` · required · raw_text: "PostgreSQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_104 - skill `python` (spot-check)

> ...systems from ingestion and model serving through backend services (Python, TypeScript) to frontend interfaces What you will build • Agent...

- agreed label: `python` · required · raw_text: "backend services (Python, TypeScript)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_104 - skill `tool-calling` (spot-check)

> ...shipped agent systems in production with orchestration, tool use, state management and human-in-the-loop workflows •...

- agreed label: `tool-calling` · required · raw_text: "tool use"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_105 - attribute `german` (spot-check)

> Field AI Engineer — Edge

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 136. golden_105 - attribute `seniority` (spot-check)

> Field AI Engineer — Edge

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_106 - attribute `seniority` (spot-check)

> Senior AI / Machine Learning Engineer Fraud Prevention Senior AI / Machine Learning Engineer —...

- agreed label: value="senior" · basis="stated" · signal="Senior AI / Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 138. golden_106 - skill `feature-engineering` (spot-check)

> ...ML frameworks like PyTorch. Experience guiding ML systems from feature engineering to production deployment and monitoring. Strong software/data engineering skills...

- agreed label: `feature-engineering` · required · raw_text: "from feature engineering to production deployment"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 139. golden_106 - skill `llms` (spot-check)

> ...skills across ML, backend, and data infrastructure. Experience building with LLMs and/or AI agents, particularly for AI/generation-abuse use...

- agreed label: `llms` · required · raw_text: "Experience building with LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 140. golden_106 - skill `machine-learning` (spot-check)

> ...identity, trust & safety, or other adversarial domains. Solid ML background with practical experience in Python, SQL, and current ML...

- agreed label: `machine-learning` · required · raw_text: "Solid ML background"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_106 - skill `python` (spot-check)

> ...domains. Solid ML background with practical experience in Python, SQL, and current ML frameworks like PyTorch. Experience...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_106 - skill `software-engineering` (spot-check)

> ...engineering to production deployment and monitoring. Strong software/data engineering skills across ML, backend, and data infrastructure. Experience...

- agreed label: `software-engineering` · required · raw_text: "Strong software/data engineering skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 143. golden_106 - skill `sql` (spot-check)

> ...ML background with practical experience in Python, SQL, and current ML frameworks like PyTorch. Experience...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 144. golden_107 - attribute `degree` (spot-check)

> Senior Staff AI Engineer — Multimodal for Smart Glasses

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree or level anywhere (only 'extensive ML leadership' and 'a track record'), so the rule's 'none (null) when no degree is mentioned' applies and the agreed null is correct.

DECISION: ok

## 145. golden_107 - attribute `seniority` (spot-check)

> Senior Staff AI Engineer — Multimodal for Smart Glasses Google LLC in California...

- agreed label: value="senior" · basis="stated" · signal="Senior Staff AI Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_108 - skill `agents` (spot-check)

> ...utilization, latency, throughput, and cost • Experience in building agentic AI systems and agentic workflows • Passion for staying abreast of the latest AI research...

- agreed label: `agents` · nice_to_have · raw_text: "building agentic AI systems and agentic workflows"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_108 - skill `azure` (spot-check)

> ...and responsible AI solutions on cloud platforms (e.g. AWS, Google Cloud, Azure, or equivalent private cloud) • Experience designing,...

- agreed label: `azure` · nice_to_have · raw_text: "AWS, Google Cloud, Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 148. golden_108 - skill `cloud` (spot-check)

> ...deploying scalable and responsible AI solutions on cloud platforms (e.g. AWS, Google Cloud, Azure, or equivalent private...

- agreed label: `cloud` · nice_to_have · raw_text: "cloud platforms"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 149. golden_108 - skill `cpp` (spot-check)

> ...Search and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or Golang • Experience developing and...

- agreed label: `cpp` · nice_to_have · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_108 - skill `csharp` (spot-check)

> ...and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or Golang • Experience developing and...

- agreed label: `csharp` · nice_to_have · raw_text: "C#"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 151. golden_108 - skill `gcp` (spot-check)

> ...and responsible AI solutions on cloud platforms (e.g. AWS, Google Cloud, Azure, or equivalent private cloud) • Experience...

- agreed label: `gcp` · nice_to_have · raw_text: "Google Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 152. golden_108 - skill `go` (spot-check)

> ...responsible and reliable AI systems, changing banking for good. For years, Capital One has been an industry leader in...

- agreed label: `go` · required · raw_text: "Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 153. golden_108 - skill `llm-guardrails` (spot-check)

> ...(e.g. LLM Inference, Similarity Search and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or Golang • Experience...

- agreed label: `llm-guardrails` · nice_to_have · raw_text: "Guardrails, Memory"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 154. golden_108 - skill `llms` (spot-check)

> ...developing AI and ML algorithms or technologies (e.g. LLM Inference, Similarity Search and VectorDBs, Guardrails, Memory)...

- agreed label: `llms` · nice_to_have · raw_text: "LLM Inference"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 155. golden_108 - skill `python` (spot-check)

> ...or technologies • At least 4 years of experience programming with Python, Go, Scala, CUDA, or Java Preferred Qualifications: •...

- agreed label: `python` · required · raw_text: "programming with Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 156. golden_097 - attribute `degree` (rule-change)

> ...vLLM). Qualifications Minimum Qualifications • MS or PhD in Computer Science, AI, Mathematics, or a related field. • 5+ years of professional experience in one or more of...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="MS or PhD in Computer Science, AI, Mathematics, or a related field"

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "MS or PhD in Computer Science, AI, Mathematics, or a related field"} - Under the degree rule, `degree` is the lowest level named, and "MS or PhD" → `master`, so the agreed `phd` came from the older highest-level rule and should be `master`.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "MS or PhD in Computer Science, AI, Mathematics, or a related field"}

## 157. golden_094 - groups `alternative_group` (groups)

> Principal Software Engineer, Applied AI – Splunk Observability Cloud

- `agents` · required · raw_text: "at least one agentic system"
- `ai-deployment` · required · raw_text: "deploying production-grade LLM-based systems"
- `ai-ml` · required · raw_text: "AI/ML systems"
- `cloud` · nice_to_have · raw_text: "cloud-native infrastructure at scale"
- `evaluation` · required · raw_text: "evaluation frameworks"
- `kubernetes` · nice_to_have · raw_text: "specifically Kubernetes"
- `llm-guardrails` · required · raw_text: "security guardrails for AI"
- `llms` · required · raw_text: "production-grade LLM-based systems"
- `mcp` · nice_to_have · raw_text: "MCP"
- `observability` · nice_to_have · raw_text: "Experience with Observability"
- `opentelemetry` · nice_to_have · raw_text: "OpenTelemetry"
- `rag` · required · raw_text: "retrieval and context pipelines"
- `tool-calling` · required · raw_text: "active tool use"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["mcp", "opentelemetry"]] - The preferred qualification 'open-source contributions in AI, agent frameworks, or observability ecosystems (e.g., OpenTelemetry, MCP)' offers examples for a single ask, so under the Markers rule any one of them meets it and both get one group, while 'observability' is the broad domain and stays out.

DECISION: [["mcp", "opentelemetry"]]

## 158. golden_095 - groups `alternative_group` (groups)

> Software Quality Engineer - AI & Automation

- `agents` · nice_to_have · raw_text: "integrating AI agents"
- `ai-ml` · required · raw_text: "Experience with AI tools"
- `distributed-systems` · nice_to_have · raw_text: "large-scale distributed systems architecture"
- `evaluation` · nice_to_have · raw_text: "benchmarking and evaluating AI agents"
- `go` · required · raw_text: "Go"
- `java` · required · raw_text: "Java"
- `python` · required · raw_text: "Python"
- `testing` · required · raw_text: "test automation"
- `workflow-automation` · nice_to_have · raw_text: "intelligent automation solutions"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["go", "java", "python"]] - The minimum qualification asks for "at least one programming language (e.g., Python, Go, Java, etc.)", an "at least one of" marker with examples offered for a single ask, so go, java and python form one group, and the "etc." adds nothing.

DECISION: [["go", "java", "python"]]

## 159. golden_097 - groups `alternative_group` (groups)

> Senior Machine Learning Engineer, E-Commerce

- `computer-vision` · required · raw_text: "Computer Vision"
- `conversational-ai` · nice_to_have · raw_text: "conversational AI applications"
- `cpp` · required · raw_text: "C++"
- `fine-tuning` · nice_to_have · raw_text: "Experience in fine-tuning"
- `go` · required · raw_text: "Go"
- `java` · required · raw_text: "Java"
- `knowledge-distillation` · nice_to_have · raw_text: "distillation, or reinforcement learning"
- `llms` · nice_to_have · raw_text: "large language models"
- `machine-learning` · required · raw_text: "Machine Learning"
- `nlp` · required · raw_text: "Natural Language Processing (NLP)"
- `python` · required · raw_text: "Python"
- `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning for large language models"
- `software-engineering` · required · raw_text: "Proficiency in software development"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["machine-learning", "nlp", "computer-vision"], ["cpp", "python", "go", "java"]] - Under the alternative_group rule's 'X, Y or Z' marker, the minimum qualifications accept 'one or more of' the fields Machine Learning, NLP or Computer Vision, and 'at least one of' the languages C++, Python, Go or Java, with no skill in either set asked for separately elsewhere, while 'software-engineering' stays out as the broad parent.

DECISION: ?

## 160. golden_099 - groups `alternative_group` (groups)

> 2027 University Graduate - Machine Learning Engineer

- `deep-learning` · required · raw_text: "deep learning"
- `java` · required · raw_text: "Java"
- `machine-learning` · required · raw_text: "Deep understanding of statistical modeling, machine learning"
- `python` · required · raw_text: "Python"
- `r-lang` · required · raw_text: "such as R"
- `scala` · required · raw_text: "Scala"
- `scikit-learn` · required · raw_text: "scikit learn"
- `software-engineering` · required · raw_text: "software development"
- `sql` · required · raw_text: "SQL"
- `statistics` · required · raw_text: "Deep understanding of statistical modeling"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["python", "scala", "java"], ["r-lang", "scikit-learn"]] - Under the alternative_group rule, 'one or more programming languages such as Python, Scala, Java and C' and 'one or more ... tools such as R, Matlab and scikit learn' each offer examples for a single ask, so the labelled members form two groups; C and Matlab are unlabelled and add nothing, and none of these skills is asked for elsewhere in the posting.

DECISION: [["java", "python", "scala"], ["r-lang", "scikit-learn"]]

## 161. golden_100 - groups `alternative_group` (groups)

> Machine Learning Platform Engineer, Applied Machine Learning Team San Jose Regular

- `apache-spark` · required · raw_text: "Spark"
- `distributed-systems` · required · raw_text: "understanding of distributed computing"
- `go` · required · raw_text: "Golang"
- `hadoop` · required · raw_text: "Hadoop"
- `python` · required · raw_text: "Python"
- `software-engineering` · required · raw_text: "experience in software engineering"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["apache-spark", "hadoop"]] - The posting gives Hadoop and Spark as examples for one ask ('familiar with related open source tools and frameworks (such as Hadoop, Spark, etc.)'), so any one meets it, which matches the examples-for-a-single-ask marker; Python and Golang are joined by 'and' in 'such as Python and Golang', which the rule excludes as skills asked together.

DECISION: ?

## 162. golden_101 - groups `alternative_group` (groups)

> Machine Learning Engineer, Personalization & Scalable Systems

- `machine-learning` · required · raw_text: "seeking a PhD-level candidate to advance machine learning"
- `recommender-systems` · required · raw_text: "advance machine learning across recommendation"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting names no 'at least one of', 'X or Y', or example-set marker for any skill; machine-learning and recommender-systems are each asked for in their own right, so under the alternative_group rule they are not alternatives and no group applies.

DECISION: []

## 163. golden_102 - groups `alternative_group` (groups)

> AI & Data Engineer – Python / FastAPI

- `agents` · required · raw_text: "LLM agent systems"
- `airflow` · required · raw_text: "Apache Airflow"
- `async-processing` · required · raw_text: "Async Python"
- `claude-code` · required · raw_text: "Claude Code"
- `codex` · required · raw_text: "Codex"
- `evaluation` · required · raw_text: "evaluations"
- `fastapi` · required · raw_text: "FastAPI, and Async Python"
- `langgraph` · nice_to_have · raw_text: "LangGraph"
- `llms` · required · raw_text: "LLM agent systems"
- `postgresql` · required · raw_text: "PostgreSQL"
- `python` · required · raw_text: "production Python"
- `sql` · required · raw_text: "SQL experience"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["claude-code", "codex"]] - The required line "Daily experience using Claude Code or Codex" is one ask met by either tool, so under the "X or Y" marker the two form a single alternative_group, and neither is asked for elsewhere in the posting.

DECISION: [["claude-code", "codex"]]

## 164. golden_103 - groups `alternative_group` (groups)

> AI Engineer Lead - Visa Independent Consultants Only

- `a-b-testing` · nice_to_have · raw_text: "A/B testing"
- `agents` · nice_to_have · raw_text: "open-source Agentic AI frameworks"
- `ai-deployment` · required · raw_text: "model deployment"
- `airflow` · required · raw_text: "(Apache Airflow, MLflow)"
- `autogen` · nice_to_have · raw_text: "AutoGen"
- `ci-cd` · required · raw_text: "CI/CD pipelines"
- `containerization` · required · raw_text: "container orchestration"
- `data-privacy-and-security` · nice_to_have · raw_text: "implementing strict access control and encryption mechanisms"
- `devops` · required · raw_text: "MLOps/DevOps"
- `distributed-systems` · required · raw_text: "large-scale data processing and distributed systems"
- `docker` · required · raw_text: "container orchestration (e.g., Kubernetes, Docker)"
- `evaluation` · required · raw_text: "model training, evaluation, and deployment"
- `gcp` · required · raw_text: "Google Cloud Platform (GCP)"
- `gitlab-ci` · required · raw_text: "(e.g., Jenkins, GitLab CI)"
- `go` · required · raw_text: "such as Python or Go"
- `google-adk` · nice_to_have · raw_text: "Agent Development Kit"
- `grafana` · nice_to_have · raw_text: "(e.g., Grafana, Datadog)"
- `jenkins` · required · raw_text: "(e.g., Jenkins, GitLab CI)"
- `kubeflow` · required · raw_text: "(Vertex AI, Kubeflow)"
- `kubernetes` · required · raw_text: "container orchestration (e.g., Kubernetes, Docker)"
- `langchain` · nice_to_have · raw_text: "LangChain"
- `llamaindex` · nice_to_have · raw_text: "LlamaIndex"
- `llms` · nice_to_have · raw_text: "Familiarity with Large Language Models (LLMs)"
- `mlflow` · required · raw_text: "(Apache Airflow, MLflow)"
- `mlops` · required · raw_text: "Strong experience with Google Cloud Platform (GCP) MLOps services"
- `model-development` · required · raw_text: "model training"
- `observability` · required · raw_text: "monitoring and alerting"
- `python` · required · raw_text: "such as Python or Go"
- `vertex-ai` · required · raw_text: "(Vertex AI, Kubeflow)"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["python", "go"], ["kubernetes", "docker"], ["jenkins", "gitlab-ci"], ["langchain", "autogen", "llamaindex", "google-adk"], ["airflow", "kubeflow", "mlflow"]] - Each bracketed set is offered as examples for one ask ('such as Python or Go', 'e.g., Kubernetes, Docker', 'e.g., Jenkins, GitLab CI', frameworks 'e.g., LangChain, AutoGen, LlamaIndex, or ... Agent Development Kit', and 'concepts similar to Kubeflow, MLflow, or Apache Airflow'), which the alternative_group markers cover, while the broad parents (ci-cd, agents, mlops) stay out; grafana is left ungrouped because datadog is not a labeled skill.

DECISION: ?

## 165. golden_104 - groups `alternative_group` (groups)

> Remote AI Engineer

- `agent-state-management` · required · raw_text: "state management"
- `agents` · required · raw_text: "Agentic AI"
- `ai-ml` · required · raw_text: "Strong background in AI/ML"
- `backend-development` · required · raw_text: "backend services"
- `computer-vision` · required · raw_text: "OpenCV"
- `data-pipelines` · required · raw_text: "data ingestion"
- `fastapi` · required · raw_text: "FastAPI"
- `frontend-development` · required · raw_text: "frontend interfaces"
- `knowledge-graphs` · required · raw_text: "knowledge graph"
- `llm-orchestration` · required · raw_text: "agent systems in production with orchestration"
- `model-serving` · required · raw_text: "model serving"
- `postgresql` · required · raw_text: "PostgreSQL"
- `python` · required · raw_text: "backend services (Python, TypeScript)"
- `tool-calling` · required · raw_text: "tool use"
- `typescript` · required · raw_text: "Tech stackTypeScript"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting lists its skills together ("backend services (Python, TypeScript)", and the tech stack list) with no "at least one of", "or", or example-for-one-ask markers, so under the alternative_group rule no skills are offered in place of each other.

DECISION: []

## 166. golden_106 - groups `alternative_group` (groups)

> Senior AI / Machine Learning Engineer Fraud Prevention

- `agents` · required · raw_text: "LLMs and/or AI agents"
- `ai-deployment` · required · raw_text: "guiding ML systems from feature engineering to production deployment"
- `backend-development` · required · raw_text: "across ML, backend, and data infrastructure"
- `data-pipelines` · nice_to_have · raw_text: "high-scale data pipelines"
- `distributed-systems` · nice_to_have · raw_text: "Distributed systems"
- `evaluation` · nice_to_have · raw_text: "AI-assisted evaluation systems"
- `feature-engineering` · required · raw_text: "from feature engineering to production deployment"
- `llms` · required · raw_text: "Experience building with LLMs"
- `machine-learning` · required · raw_text: "Solid ML background"
- `mlops` · required · raw_text: "building and operating production ML systems"
- `observability` · required · raw_text: "production deployment and monitoring"
- `python` · required · raw_text: "Python"
- `pytorch` · required · raw_text: "current ML frameworks like PyTorch"
- `software-engineering` · required · raw_text: "Strong software/data engineering skills"
- `sql` · required · raw_text: "SQL"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The 'and/or' in 'Experience building with LLMs and/or AI agents' would group llms and agents, but the responsibilities separately say to 'Apply LLMs and AI agents', which asks for both together, so neither is only an alternative under the rule's 'skill also asked for on its own elsewhere' exclusion.

DECISION: []

## 167. golden_107 - groups `alternative_group` (groups)

> Senior Staff AI Engineer — Multimodal for Smart Glasses

- `ai-deployment` · required · raw_text: "deploying large-scale AI"
- `llms` · required · raw_text: "Generative AI"
- `machine-learning` · required · raw_text: "extensive ML leadership"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting asks for deploying large-scale AI, Generative AI capabilities and ML leadership together, with no 'at least one of', 'or', or example-for-one-ask markers, so no skills are offered in place of each other under the alternative_group rule.

DECISION: []

## 168. golden_108 - groups `alternative_group` (groups)

> AI Engineer 4 (AI Platforms)

- `agent-state-management` · nice_to_have · raw_text: "Guardrails, Memory"
- `agents` · nice_to_have · raw_text: "building agentic AI systems and agentic workflows"
- `ai-deployment` · nice_to_have · raw_text: "deploying scalable and responsible AI solutions"
- `ai-ml` · required · raw_text: "developing AI and ML algorithms or technologies"
- `aws` · nice_to_have · raw_text: "AWS, Google Cloud, Azure"
- `azure` · nice_to_have · raw_text: "AWS, Google Cloud, Azure"
- `cloud` · nice_to_have · raw_text: "cloud platforms"
- `cpp` · nice_to_have · raw_text: "C++"
- `csharp` · nice_to_have · raw_text: "C#"
- `cuda` · required · raw_text: "Python, Go, Scala, CUDA, or Java"
- `distributed-systems` · nice_to_have · raw_text: "designing distributed systems"
- `distributed-training` · nice_to_have · raw_text: "distributed systems for model training"
- `gcp` · nice_to_have · raw_text: "Google Cloud"
- `go` · required · raw_text: "Go"
- `inference-optimization` · nice_to_have · raw_text: "optimizing training and inference software"
- `java` · required · raw_text: "Python, Go, Scala, CUDA, or Java"
- `llm-guardrails` · nice_to_have · raw_text: "Guardrails, Memory"
- `llms` · nice_to_have · raw_text: "LLM Inference"
- `machine-learning` · required · raw_text: "ML algorithms or technologies"
- `model-serving` · nice_to_have · raw_text: "online inference"
- `python` · required · raw_text: "programming with Python"
- `scala` · required · raw_text: "Scala"
- `software-architecture` · nice_to_have · raw_text: "architectural decisions"
- `vector-databases` · nice_to_have · raw_text: "Similarity Search and VectorDBs"
- `vector-search` · nice_to_have · raw_text: "Similarity Search and VectorDBs"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["python", "go", "scala", "cuda", "java"], ["aws", "gcp", "azure"]] - The basic qualification's 'at least 4 years of experience programming with Python, Go, Scala, CUDA, or Java' and the cloud-platform 'e.g. AWS, Google Cloud, Azure' each offer one ask with any one example meeting it, so each gets its own group, while the broad 'cloud' stays out per the rule's broad-skill exclusion. I left out the preferred-qualification examples (LLM Inference, Similarity Search/VectorDBs, Guardrails, Memory) and the C++/C# languages because the 'Similarity Search and VectorDBs' example is a conjunction, not a single member, and the rest are illustrations of a broad ask rather than clear alternatives.

DECISION: ?
