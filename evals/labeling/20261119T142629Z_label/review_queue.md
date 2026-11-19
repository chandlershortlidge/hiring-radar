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

DECISION: ?

## 17. golden_095 - skill `ai-ml` (disagreement)

> ...scalable test automation, or productivity tools. - Experience with AI tools, with an understanding of practical use to improve testing...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Experience with AI tools"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_095 - skill `workflow-automation` (disagreement)

> ...AI testing frameworks, autonomous testing agents or intelligent automation solutions - Working knowledge of large-scale distributed systems...

- A: (did not label this)
- B: `workflow-automation` · nice_to_have · raw_text: "intelligent automation solutions"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_098 - attribute `seniority` (disagreement)

> ...and deliver documentation and demonstrations Requirements 1 to 3 years of related experience Bachelor’s degree or equivalent combination of education...

- A: value="junior" · basis="inferred" · signal="1 to 3 years of related experience"
- B: value="senior" · basis="inferred" · signal="Lead hardware engineering use case projects"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_099 - skill `ai-ml` (disagreement)

> ...your application may not move forward in the process. At Adobe, we empower employees to innovate with AI — and we look for candidates eager to do the same. As part of the hiring experience, we provide clear...

- A: (did not label this)
- B: `ai-ml` · nice_to_have · raw_text: "At Adobe, we empower employees to innovate with AI — and we look for candidates eager to do the same."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_101 - skill `machine-learning` (disagreement)

> ...& Scalable Systems TikTok USDS Joint Venture is seeking a PhD-level candidate to advance machine learning across recommendation, search, and e-commerce systems. You...

- A: `machine-learning` · required · raw_text: "seeking a PhD-level candidate to advance machine learning"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_101 - skill `recommender-systems` (disagreement)

> ...USDS Joint Venture is seeking a PhD-level candidate to advance machine learning across recommendation, search, and e-commerce systems. You will design scalable...

- A: `recommender-systems` · required · raw_text: "advance machine learning across recommendation"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_103 - skill `evaluation` (disagreement)

> ...equivalent like Agent Development Kit). Knowledge of standard ML evaluation metrics for Generative and Classification models (e.g., BLEURT,...

- A: `evaluation` · nice_to_have · raw_text: "standard ML evaluation metrics"
- B: `evaluation` · required · raw_text: "model training, evaluation, and deployment"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_103 - skill `google-adk` (disagreement)

> ...AutoGen, LlamaIndex, or internal equivalent like Agent Development Kit). Knowledge of standard ML evaluation metrics for...

- A: `google-adk` · nice_to_have · raw_text: "Agent Development Kit"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_103 - skill `model-development` (disagreement)

> ...and implement end-to-end ML pipelines for data management, model training, evaluation, and deployment. Demonstrated ability to lead...

- A: (did not label this)
- B: `model-development` · required · raw_text: "model training"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_104 - skill `data-pipelines` (disagreement)

> ...systems • Understand that the hardest problems are in data ingestion, normalization, temporal alignment and ground truth •...

- A: (did not label this)
- B: `data-pipelines` · required · raw_text: "data ingestion"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_106 - skill `mlops` (disagreement)

> ...capabilities. What you'll need to succeed 8+ years building and operating production ML systems, ideally in fraud, abuse, risk, identity, trust & safety,...

- A: (did not label this)
- B: `mlops` · required · raw_text: "building and operating production ML systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_108 - skill `distributed-training` (disagreement)

> ...novel techniques in production • Proficiency in designing distributed systems for model training, evaluation, and online inference at petabyte scale •...

- A: `distributed-training` · nice_to_have · raw_text: "distributed systems for model training"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_108 - skill `evaluation` (disagreement)

> ...workflows, similarity search, guardrails, model evaluation, experimentation, governance, and observability, etc. •...

- A: (did not label this)
- B: `evaluation` · nice_to_have · raw_text: "evaluation"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_108 - skill `machine-learning` (disagreement)

> ...plus at least 4 years of experience developing AI and ML algorithms or technologies, or a Master's degree in Computer Science, AI, Electrical...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "ML algorithms or technologies"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_108 - skill `model-development` (disagreement)

> ...and support AI software components including foundation model training, large language model inference, agents and multi-agent...

- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "model training"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_108 - skill `model-serving` (disagreement)

> ...distributed systems for model training, evaluation, and online inference at petabyte scale • Experience defining AI model...

- A: (did not label this)
- B: `model-serving` · nice_to_have · raw_text: "online inference"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_108 - skill `software-architecture` (disagreement)

> ...retaining schedules • Demonstrated ability to influence architectural decisions across multiple AI product lines or platforms Capital One...

- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "architectural decisions"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 34. golden_094 - skill `agents` (uncertain)

> ...deploying production-grade LLM-based systems, including at least one agentic system with active tool use. • Experience developing evaluation...

- A: `agents` · required · raw_text: "at least one agentic system"
- B: `agents` · required · raw_text: "agentic system with active tool use"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 35. golden_094 - skill `cloud` (uncertain)

> ...tracing and alerting workflows. • Experience working with cloud-native infrastructure at scale, specifically Kubernetes. • History of active open-source...

- A: `cloud` · nice_to_have · raw_text: "cloud-native infrastructure at scale"
- B: `cloud` · nice_to_have · raw_text: "cloud-native infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 36. golden_094 - skill `mcp` (uncertain)

> ...or observability ecosystems (e.g., OpenTelemetry, MCP). • Experience leading customer-zero or field-deployed...

- A: `mcp` · nice_to_have · raw_text: "MCP"
- B: `mcp` · nice_to_have · raw_text: "MCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 37. golden_094 - skill `observability` (uncertain)

> ...security guardrails for AI. Preferred Qualifications • Experience with Observability, SRE, or incident management domains, including...

- A: `observability` · nice_to_have · raw_text: "Experience with Observability"
- B: `observability` · nice_to_have · raw_text: "Observability"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 38. golden_094 - skill `rag` (uncertain)

> ...scoring, and release validation. • Experience engineering retrieval and context pipelines for structured and semi-structured data, such as...

- A: `rag` · required · raw_text: "retrieval and context pipelines"
- B: `rag` · required · raw_text: "retrieval and context pipelines"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_094 - skill `software-engineering` (uncertain)

> ...product features. Minimum Qualifications • 12+ years of professional software engineering experience. • 3+ years of experience designing, building, and...

- A: `software-engineering` · required · raw_text: "professional software engineering experience"
- B: `software-engineering` · required · raw_text: "professional software engineering experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_095 - skill `evaluation` (uncertain)

> ...testing workflow or engineering pipelines - Background in benchmarking and evaluating AI agents for effectiveness, reliability, and output quality -...

- A: `evaluation` · nice_to_have · raw_text: "benchmarking and evaluating AI agents"
- B: `evaluation` · nice_to_have · raw_text: "benchmarking and evaluating AI agents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_096 - attribute `seniority` (uncertain)

> ...workflows with Langchain, Langgraph and LangSmith, and lead prompt engineering to improve model performance. You will perform...

- A: value="senior" · basis="inferred" · signal="lead prompt engineering"
- B: value="senior" · basis="inferred" · signal="lead prompt engineering to improve model performance"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_097 - skill `nlp` (uncertain)

> ...in one or more of the following fields: Machine Learning, Natural Language Processing (NLP), or Computer Vision. • Proficiency in software development...

- A: `nlp` · required · raw_text: "Natural Language Processing (NLP)"
- B: `nlp` · required · raw_text: "Natural Language Processing (NLP)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_097 - skill `software-engineering` (uncertain)

> ...Natural Language Processing (NLP), or Computer Vision. • Proficiency in software development with at least one of the following programming languages:...

- A: `software-engineering` · required · raw_text: "Proficiency in software development"
- B: `software-engineering` · required · raw_text: "software development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_099 - skill `software-engineering` (uncertain)

> ...applied statistics, machine learning, data mining, and software development. Familiarity with working with large-scale datasets and...

- A: `software-engineering` · required · raw_text: "software development"
- B: `software-engineering` · required · raw_text: "software development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

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

DECISION: ?

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

DECISION: ?

## 51. golden_102 - skill `llms` (uncertain)

> ...and SQL experience. • Hands-on experience delivering LLM agent systems, evaluations, FastAPI, and Async Python. • Experience with...

- A: `llms` · required · raw_text: "LLM agent systems"
- B: `llms` · required · raw_text: "LLM agent systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_103 - skill `data-privacy-and-security` (uncertain)

> ...managing highly sensitive data (e.g., PII/PHI) and implementing strict access control and encryption mechanisms. Strong analytical and debugging skills, with the ability...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "implementing strict access control and encryption mechanisms"
- B: `data-privacy-and-security` · nice_to_have · raw_text: "Experience managing highly sensitive data (e.g., PII/PHI) and implementing strict access control and encryption mechanisms."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_103 - skill `devops` (uncertain)

> ...of experience in software engineering, ML engineering, or MLOps/DevOps, focusing on the ML lifecycle (continuous training, model...

- A: `devops` · required · raw_text: "MLOps/DevOps"
- B: `devops` · required · raw_text: "DevOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_103 - skill `docker` (uncertain)

> ...Experience working with large-scale production deployment, container orchestration (e.g., Kubernetes, Docker), and CI/CD pipelines (e.g., Jenkins, GitLab CI)....

- A: `docker` · required · raw_text: "container orchestration (e.g., Kubernetes, Docker)"
- B: `docker` · required · raw_text: "Kubernetes, Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_103 - skill `gcp` (uncertain)

> ...2+ years in a technical lead role. Strong experience with Google Cloud Platform (GCP) MLOps services (Vertex AI, Kubeflow) or equivalent...

- A: `gcp` · required · raw_text: "Google Cloud Platform (GCP)"
- B: `gcp` · required · raw_text: "Google Cloud Platform (GCP)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_103 - skill `kubernetes` (uncertain)

> ...Experience working with large-scale production deployment, container orchestration (e.g., Kubernetes, Docker), and CI/CD pipelines (e.g., Jenkins, GitLab CI)....

- A: `kubernetes` · required · raw_text: "container orchestration (e.g., Kubernetes, Docker)"
- B: `kubernetes` · required · raw_text: "Kubernetes, Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_103 - skill `ml-engineering` (uncertain)

> ...8+ years of experience in software engineering, ML engineering, or MLOps/DevOps, focusing on the ML lifecycle (continuous...

- A: `ml-engineering` · required · raw_text: "ML engineering"
- B: `ml-engineering` · required · raw_text: "ML engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_103 - skill `mlops` (uncertain)

> ...of experience in software engineering, ML engineering, or MLOps/DevOps, focusing on the ML lifecycle (continuous training, model...

- A: `mlops` · required · raw_text: "MLOps/DevOps"
- B: `mlops` · required · raw_text: "MLOps services"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_103 - skill `software-engineering` (uncertain)

> ...Minimum Qualifications: 8+ years of experience in software engineering, ML engineering, or MLOps/DevOps, focusing on the ML...

- A: `software-engineering` · required · raw_text: "software engineering"
- B: `software-engineering` · required · raw_text: "software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_104 - attribute `seniority` (uncertain)

> ...zero-to-one product development. What we’re looking for • 3+ years experience (5+ preferred) building and shipping production AI systems, ideally...

- A: value="mid" · basis="inferred" · signal="3+ years experience (5+ preferred)"
- B: value="mid" · basis="inferred" · signal="3+ years experience (5+ preferred)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_104 - skill `agent-state-management` (uncertain)

> ...agent systems in production with orchestration, tool use, state management and human-in-the-loop workflows • Worked with...

- A: `agent-state-management` · required · raw_text: "state management"
- B: `agent-state-management` · required · raw_text: "state management"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_104 - skill `llm-orchestration` (uncertain)

> ...sensor streams) What you have done • Built and shipped agent systems in production with orchestration, tool use, state management and human-in-the-loop...

- A: `llm-orchestration` · required · raw_text: "agent systems in production with orchestration"
- B: `llm-orchestration` · required · raw_text: "orchestration"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_106 - attribute `degree` (uncertain)

> ...and ability to solve ambiguous, adversarial problems. Bachelor's or equivalent experience in Computer Science, Statistics, Mathematics, or related field; advanced degree a plus. Preferred Attributes Device...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor's or equivalent experience in Computer Science, Statistics, Mathematics, or related field"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor's or equivalent experience in Computer Science, Statistics, Mathematics, or related field; advanced degree a plus."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_106 - skill `ai-deployment` (uncertain)

> ...SQL, and current ML frameworks like PyTorch. Experience guiding ML systems from feature engineering to production deployment and monitoring. Strong software/data engineering skills...

- A: `ai-deployment` · required · raw_text: "guiding ML systems from feature engineering to production deployment"
- B: `ai-deployment` · required · raw_text: "production deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_106 - skill `evaluation` (uncertain)

> ...and automated control systems. Human-in-the-loop or AI-assisted evaluation systems. Distributed systems and high-scale data pipelines. Strong...

- A: `evaluation` · nice_to_have · raw_text: "AI-assisted evaluation systems"
- B: `evaluation` · nice_to_have · raw_text: "Human-in-the-loop or AI-assisted evaluation systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_106 - skill `observability` (uncertain)

> ...guiding ML systems from feature engineering to production deployment and monitoring. Strong software/data engineering skills across ML,...

- A: `observability` · required · raw_text: "production deployment and monitoring"
- B: `observability` · required · raw_text: "monitoring"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_107 - skill `ai-deployment` (uncertain)

> ...ML leadership, systems thinking, and a track record in deploying large-scale AI with Generative AI capabilities across complex, matrixed...

- A: `ai-deployment` · required · raw_text: "deploying large-scale AI"
- B: `ai-deployment` · required · raw_text: "deploying large-scale AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_107 - skill `machine-learning` (uncertain)

> ...to push voice and vision integration. This role demands extensive ML leadership, systems thinking, and a track record in deploying...

- A: `machine-learning` · required · raw_text: "extensive ML leadership"
- B: `machine-learning` · required · raw_text: "extensive ML leadership"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

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

DECISION: ?

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

DECISION: ?

## 73. golden_108 - skill `ai-ml` (uncertain)

> ...or related fields plus at least 4 years of experience developing AI and ML algorithms or technologies, or a Master's degree in Computer Science, AI, Electrical...

- A: `ai-ml` · required · raw_text: "developing AI and ML algorithms or technologies"
- B: `ai-ml` · required · raw_text: "developing AI and ML algorithms or technologies"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_108 - skill `inference-optimization` (uncertain)

> ...developing and applying state-of-the-art techniques for optimizing training and inference software to improve hardware utilization, latency, throughput, and...

- A: `inference-optimization` · nice_to_have · raw_text: "optimizing training and inference software"
- B: `inference-optimization` · nice_to_have · raw_text: "optimizing training and inference software"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_108 - skill `vector-search` (uncertain)

> ...AI and ML algorithms or technologies (e.g. LLM Inference, Similarity Search and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or...

- A: `vector-search` · nice_to_have · raw_text: "Similarity Search and VectorDBs"
- B: `vector-search` · nice_to_have · raw_text: "Similarity Search"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_094 - attribute `degree` (spot-check)

> Principal Software Engineer, Applied AI – Splunk Observability Cloud

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 77. golden_094 - attribute `german` (spot-check)

> Principal Software Engineer, Applied AI – Splunk Observability Cloud

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 78. golden_094 - skill `llms` (spot-check)

> ...3+ years of experience designing, building, and deploying production-grade LLM-based systems, including at least one agentic system with active tool...

- agreed label: `llms` · required · raw_text: "production-grade LLM-based systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 79. golden_094 - skill `opentelemetry` (spot-check)

> ...AI, agent frameworks, or observability ecosystems (e.g., OpenTelemetry, MCP). • Experience leading customer-zero or...

- agreed label: `opentelemetry` · nice_to_have · raw_text: "OpenTelemetry"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 80. golden_094 - skill `tool-calling` (spot-check)

> ...systems, including at least one agentic system with active tool use. • Experience developing evaluation frameworks for AI/ML...

- agreed label: `tool-calling` · required · raw_text: "active tool use"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 81. golden_095 - attribute `degree` (spot-check)

> ...practices Qualifications Minimum Qualifications - BS in Computer Science or related fields - Proficiency in at least one programming language (e.g.,...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="BS in Computer Science or related fields"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 82. golden_095 - attribute `german` (spot-check)

> Software Quality Engineer - AI & Automation

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 83. golden_095 - attribute `seniority` (spot-check)

> ...Go, Java, etc.). - Experience with web and mobile tests - Proven experience building scalable test automation, or productivity tools. - Experience with AI tools, with...

- agreed label: value="mid" · basis="inferred" · signal="Proven experience building scalable test automation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_095 - skill `agents` (spot-check)

> ...test strategies and use cases - Experience with integrating AI agents into testing workflow or engineering pipelines -...

- agreed label: `agents` · nice_to_have · raw_text: "integrating AI agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_095 - skill `go` (spot-check)

> ...in at least one programming language (e.g., Python, Go, Java, etc.). - Experience with web and mobile tests -...

- agreed label: `go` · required · raw_text: "Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_095 - skill `testing` (spot-check)

> ...web and mobile tests - Proven experience building scalable test automation, or productivity tools. - Experience with AI tools, with...

- agreed label: `testing` · required · raw_text: "test automation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_097 - skill `computer-vision` (spot-check)

> ...Machine Learning, Natural Language Processing (NLP), or Computer Vision. • Proficiency in software development with at least one...

- agreed label: `computer-vision` · required · raw_text: "Computer Vision"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_097 - skill `cpp` (spot-check)

> ...with at least one of the following programming languages: C++, Python, Go, or Java. Preferred Qualifications •...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_097 - skill `go` (spot-check)

> ...and efficient shopping experience while upholding a robust governance and risk control framework to ensure platform...

- agreed label: `go` · required · raw_text: "Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_097 - skill `knowledge-distillation` (spot-check)

> ...Qualifications • Experience in fine-tuning, distillation, or reinforcement learning for large language models in conversational AI...

- agreed label: `knowledge-distillation` · nice_to_have · raw_text: "distillation, or reinforcement learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_097 - skill `llms` (spot-check)

> ...fine-tuning, distillation, or reinforcement learning for large language models in conversational AI applications. • Proficiency in...

- agreed label: `llms` · nice_to_have · raw_text: "large language models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_097 - skill `machine-learning` (spot-check)

> Senior Machine Learning Engineer, E-Commerce San Jose Regular R&D Job ID:...

- agreed label: `machine-learning` · required · raw_text: "Machine Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_097 - skill `python` (spot-check)

> ...at least one of the following programming languages: C++, Python, Go, or Java. Preferred Qualifications • Experience in...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_098 - attribute `degree` (spot-check)

> ...Requirements 1 to 3 years of related experience Bachelor’s degree or equivalent combination of education and experience Benefits A comprehensive benefits package is offered in...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor’s degree or equivalent combination of education and experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_099 - attribute `degree` (spot-check)

> ...new products and features. What You Need to Succeed • PhD or MS in Computer Science, Statistics, Electrical Engineering, Applied Math, Operations Research, Econometrics or equivalent experience required with an expected graduation date of December 2026 – June...

- agreed label: value="phd" · requirement="required" · or_equivalent=true · signal="PhD or MS in Computer Science, Statistics, Electrical Engineering, Applied Math, Operations Research, Econometrics or equivalent experience required"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_099 - attribute `german` (spot-check)

> 2027 University Graduate - Machine Learning Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_099 - attribute `seniority` (spot-check)

> 2027 University Graduate - Machine Learning Engineer The Opportunity Adobe is...

- agreed label: value="junior" · basis="stated" · signal="University Graduate"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_099 - skill `deep-learning` (spot-check)

> ...understanding of statistical modeling, machine learning, deep learning, or data mining concepts, and a track record of solving...

- agreed label: `deep-learning` · required · raw_text: "deep learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_099 - skill `java` (spot-check)

> ...one or more programming languages such as Python, Scala, Java and C • Familiar with one or more machine learning or...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_099 - skill `machine-learning` (spot-check)

> ...0-2+ years of experience in specific relevant skills • Deep understanding of statistical modeling, machine learning, deep learning, or data mining concepts, and a track...

- agreed label: `machine-learning` · required · raw_text: "Deep understanding of statistical modeling, machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_099 - skill `scala` (spot-check)

> ...and analytics techniques. • Develop and implement scalable and efficient modeling algorithms that can work with...

- agreed label: `scala` · required · raw_text: "Scala"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_100 - attribute `seniority` (spot-check)

> ...science, software engineering, or a related field.- At least 3 years of experience in software engineering and be proficient in developing using common programming...

- agreed label: value="mid" · basis="inferred" · signal="At least 3 years of experience in software engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_101 - attribute `seniority` (spot-check)

> Machine Learning Engineer, Personalization & Scalable Systems

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_102 - attribute `degree` (spot-check)

> AI & Data Engineer – Python / FastAPI

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_102 - attribute `german` (spot-check)

> AI & Data Engineer – Python / FastAPI

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_102 - skill `airflow` (spot-check)

> ...grounding, and citation checks. • Strong experience with Apache Airflow and Apache Iceberg or similar lakehouse technologies. •...

- agreed label: `airflow` · required · raw_text: "Apache Airflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_102 - skill `claude-code` (spot-check)

> ...with pytest, ruff, and mypy. • Daily experience using Claude Code or Codex. Nice to Have • LangGraph, entity resolution,...

- agreed label: `claude-code` · required · raw_text: "Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_102 - skill `codex` (spot-check)

> ...ruff, and mypy. • Daily experience using Claude Code or Codex. Nice to Have • LangGraph, entity resolution, and...

- agreed label: `codex` · required · raw_text: "Codex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_102 - skill `evaluation` (spot-check)

> ...Hands-on experience delivering LLM agent systems, evaluations, FastAPI, and Async Python. • Experience with structured...

- agreed label: `evaluation` · required · raw_text: "evaluations"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_102 - skill `langgraph` (spot-check)

> ...experience using Claude Code or Codex. Nice to Have • LangGraph, entity resolution, and graph/entity data. • AWS Lake...

- agreed label: `langgraph` · nice_to_have · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_102 - skill `postgresql` (spot-check)

> ...technologies. • Knowledge of Trino, AWS Athena, AWS Glue, PostgreSQL, and Cube semantic layer. • Experience with pytest, ruff,...

- agreed label: `postgresql` · required · raw_text: "PostgreSQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_102 - skill `sql` (spot-check)

> ...Skills • 5+ years of production Python and SQL experience. • Hands-on experience delivering LLM agent systems,...

- agreed label: `sql` · required · raw_text: "SQL experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_103 - attribute `degree` (spot-check)

> AI Engineer Lead - Visa Independent Consultants Only

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

## 117. golden_103 - skill `ci-cd` (spot-check)

> ...container orchestration (e.g., Kubernetes, Docker), and CI/CD pipelines (e.g., Jenkins, GitLab CI). Experience with production...

- agreed label: `ci-cd` · required · raw_text: "CI/CD pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_103 - skill `containerization` (spot-check)

> ...Experience working with large-scale production deployment, container orchestration (e.g., Kubernetes, Docker), and CI/CD pipelines (e.g.,...

- agreed label: `containerization` · required · raw_text: "container orchestration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

## 122. golden_103 - skill `kubeflow` (spot-check)

> ...experience with Google Cloud Platform (GCP) MLOps services (Vertex AI, Kubeflow) or equivalent open-source ecosystems (Apache Airflow,...

- agreed label: `kubeflow` · required · raw_text: "(Vertex AI, Kubeflow)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_103 - skill `langchain` (spot-check)

> ...Models (LLMs) and open-source Agentic AI frameworks (e.g., LangChain, AutoGen, LlamaIndex, or internal equivalent like Agent...

- agreed label: `langchain` · nice_to_have · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_103 - skill `llms` (spot-check)

> ...multiple partner priorities. Preferred Qualifications: Familiarity with Large Language Models (LLMs) and open-source Agentic AI frameworks (e.g., LangChain,...

- agreed label: `llms` · nice_to_have · raw_text: "Familiarity with Large Language Models (LLMs)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_103 - skill `python` (spot-check)

> ...Airflow, MLflow). Proficiency in programming languages such as Python or Go, and experience with large-scale data processing and...

- agreed label: `python` · required · raw_text: "such as Python or Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_103 - skill `vertex-ai` (spot-check)

> ...experience with Google Cloud Platform (GCP) MLOps services (Vertex AI, Kubeflow) or equivalent open-source ecosystems (Apache Airflow,...

- agreed label: `vertex-ai` · required · raw_text: "(Vertex AI, Kubeflow)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_104 - attribute `degree` (spot-check)

> Remote AI Engineer

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_104 - attribute `german` (spot-check)

> Remote AI Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_104 - skill `fastapi` (spot-check)

> ...both depth and execution Tech stackTypeScript, Python, FastAPI, Agentic AI, OpenCV, PostgreSQL, React Native Why...

- agreed label: `fastapi` · required · raw_text: "FastAPI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_104 - skill `knowledge-graphs` (spot-check)

> ...operational data • Designed or contributed to ontology, knowledge graph or structured context systems grounded in real asset...

- agreed label: `knowledge-graphs` · required · raw_text: "knowledge graph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_104 - skill `model-serving` (spot-check)

> ...mapping • Shipped end-to-end systems from ingestion and model serving through backend services (Python, TypeScript) to frontend...

- agreed label: `model-serving` · required · raw_text: "model serving"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_104 - skill `postgresql` (spot-check)

> ...stackTypeScript, Python, FastAPI, Agentic AI, OpenCV, PostgreSQL, React Native Why candidates should joinCategory-defining...

- agreed label: `postgresql` · required · raw_text: "PostgreSQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_104 - skill `python` (spot-check)

> ...systems from ingestion and model serving through backend services (Python, TypeScript) to frontend interfaces What you will build • Agent...

- agreed label: `python` · required · raw_text: "backend services (Python, TypeScript)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_104 - skill `tool-calling` (spot-check)

> ...shipped agent systems in production with orchestration, tool use, state management and human-in-the-loop workflows •...

- agreed label: `tool-calling` · required · raw_text: "tool use"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_105 - attribute `german` (spot-check)

> Field AI Engineer — Edge

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_105 - attribute `seniority` (spot-check)

> Field AI Engineer — Edge

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_106 - attribute `seniority` (spot-check)

> Senior AI / Machine Learning Engineer Fraud Prevention Senior AI / Machine Learning Engineer —...

- agreed label: value="senior" · basis="stated" · signal="Senior AI / Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_106 - skill `feature-engineering` (spot-check)

> ...ML frameworks like PyTorch. Experience guiding ML systems from feature engineering to production deployment and monitoring. Strong software/data engineering skills...

- agreed label: `feature-engineering` · required · raw_text: "from feature engineering to production deployment"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_106 - skill `llms` (spot-check)

> ...skills across ML, backend, and data infrastructure. Experience building with LLMs and/or AI agents, particularly for AI/generation-abuse use...

- agreed label: `llms` · required · raw_text: "Experience building with LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

## 143. golden_106 - skill `sql` (spot-check)

> ...ML background with practical experience in Python, SQL, and current ML frameworks like PyTorch. Experience...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_107 - attribute `degree` (spot-check)

> Senior Staff AI Engineer — Multimodal for Smart Glasses

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

## 148. golden_108 - skill `cloud` (spot-check)

> ...deploying scalable and responsible AI solutions on cloud platforms (e.g. AWS, Google Cloud, Azure, or equivalent private...

- agreed label: `cloud` · nice_to_have · raw_text: "cloud platforms"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_108 - skill `cpp` (spot-check)

> ...Search and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or Golang • Experience developing and...

- agreed label: `cpp` · nice_to_have · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_108 - skill `csharp` (spot-check)

> ...and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or Golang • Experience developing and...

- agreed label: `csharp` · nice_to_have · raw_text: "C#"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_108 - skill `gcp` (spot-check)

> ...and responsible AI solutions on cloud platforms (e.g. AWS, Google Cloud, Azure, or equivalent private cloud) • Experience...

- agreed label: `gcp` · nice_to_have · raw_text: "Google Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_108 - skill `go` (spot-check)

> ...responsible and reliable AI systems, changing banking for good. For years, Capital One has been an industry leader in...

- agreed label: `go` · required · raw_text: "Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_108 - skill `llm-guardrails` (spot-check)

> ...(e.g. LLM Inference, Similarity Search and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or Golang • Experience...

- agreed label: `llm-guardrails` · nice_to_have · raw_text: "Guardrails, Memory"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_108 - skill `llms` (spot-check)

> ...developing AI and ML algorithms or technologies (e.g. LLM Inference, Similarity Search and VectorDBs, Guardrails, Memory)...

- agreed label: `llms` · nice_to_have · raw_text: "LLM Inference"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_108 - skill `python` (spot-check)

> ...or technologies • At least 4 years of experience programming with Python, Go, Scala, CUDA, or Java Preferred Qualifications: •...

- agreed label: `python` · required · raw_text: "programming with Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
