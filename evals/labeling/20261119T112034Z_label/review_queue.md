# Review queue - 20261119T112034Z_label

162 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261119T112034Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 164 accepted labels,
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

> Engineering Manager, AI Models Infrastructure

- Intercom · Engineering Manager, AI Models Infrastructure
- London · en · greenhouse · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_095 - scope `in_scope` (in-scope)

> Lead Machine Learning Scientist, Business Banking

- monzo · Lead Machine Learning Scientist, Business Banking
- London · en · greenhouse · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_096 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer

- faculty · Senior Machine Learning Engineer
- London · en · ashby · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_097 - scope `in_scope` (in-scope)

> Member of Technical Staff (AI Infrastructure Engineer)

- Perplexity · Member of Technical Staff (AI Infrastructure Engineer)
- London · en · ashby · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_098 - scope `in_scope` (in-scope)

> Principal Data Scientist

- faculty · Principal Data Scientist
- London · en · ashby · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_099 - scope `in_scope` (in-scope)

> Applied Scientist - Tabular Data, EMEA

- mistral.ai · Applied Scientist - Tabular Data, EMEA
- London · en · ashby · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_100 - scope `in_scope` (in-scope)

> AI Engineer, UK

- distyl · AI Engineer, UK
- London · en · ashby · 17 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_101 - scope `in_scope` (in-scope)

> Applied Scientist Lead - Robotics, EMEA

- mistral.ai · Applied Scientist Lead - Robotics, EMEA
- London · en · ashby · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_102 - scope `in_scope` (in-scope)

> Android Developer - AI Finance Agent

- bjakcareer · Android Developer - AI Finance Agent
- London · en · ashby · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_103 - scope `in_scope` (in-scope)

> Member of Technical Staff (Machine Learning Engineer, Search Agent RL)

- Perplexity · Member of Technical Staff (Machine Learning Engineer, Search Agent RL)
- London · en · ashby · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_104 - scope `in_scope` (in-scope)

> Software Engineer - AI Product (London, United Kingdom)

- figma · Software Engineer - AI Product (London, United Kingdom)
- London · en · greenhouse · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_105 - scope `in_scope` (in-scope)

> Staff Software Engineer (Agentic Search) - Runtime

- Nebius · Staff Software Engineer (Agentic Search) - Runtime
- London · en · greenhouse · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_106 - scope `in_scope` (in-scope)

> Senior Data Scientist

- Capco · Senior Data Scientist
- London · en · greenhouse · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_107 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineering Manager - Content Platform

- spotify · Senior Machine Learning Engineering Manager - Content Platform
- London · en · lever · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_108 - scope `in_scope` (in-scope)

> Applied Value Engineer - AI and Pre-Sales Consultant

- celonis · Applied Value Engineer - AI and Pre-Sales Consultant
- London · en · greenhouse · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_094 - skill `machine-learning` (disagreement)

> ...shape over time. - Curiosity and enthusiasm for AI. Experience training ML models and operating them in production at scale is a significant...

- A: (did not label this)
- B: `machine-learning` · nice_to_have · raw_text: "Experience training ML models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_095 - skill `ai-ml` (disagreement)

> ...and build things that customers actually use. - You’re thoughtful about responsible ML/AI; especially in financial products where trust,...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "thoughtful about responsible ML/AI"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_095 - skill `model-development` (disagreement)

> ...a multiple year track record of excellence leading the development and deployment of advanced Machine Learning models to tackle real business problems, preferably in a...

- A: (did not label this)
- B: `model-development` · required · raw_text: "development and deployment of advanced Machine Learning models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_095 - skill `rag` (disagreement)

> ...Experience with GenAI, LLMs, agentic workflows, retrieval, evaluation frameworks, or human-in-the-loop product...

- A: `rag` · nice_to_have · raw_text: "retrieval"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_095 - skill `software-engineering` (disagreement)

> ...product experiences. - Commercial experience writing critical production code and working with microservices. - Experience designing...

- A: (did not label this)
- B: `software-engineering` · nice_to_have · raw_text: "writing critical production code"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_096 - skill `cybersecurity` (disagreement)

> ...our Defence clients, you will need to be eligible for UK Security Clearance (SC) and willing to work between 2 to 4 days per...

- A: (did not label this)
- B: `cybersecurity` · required · raw_text: "security"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_096 - skill `machine-learning` (disagreement)

> ...technical depth WHO WE'RE LOOKING FOR: - You understand the full ML lifecycle and have significant experience operationalising models...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "understand the full ML lifecycle"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_097 - attribute `seniority` (disagreement)

> ...training jobs and high-availability inference services - Ideally, 3-5 years of relevant experience in ML systems deployment with specific focus on cluster...

- A: value="mid" · basis="inferred" · signal="Ideally, 3-5 years of relevant experience"
- B: value="senior" · basis="stated" · signal="Member of Technical Staff"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_097 - skill `ai-infrastructure` (disagreement)

> ...roles in SRE, DevOps, or Platform Engineering with focus on ML infrastructure - Experience supporting both long-running training jobs...

- A: `ai-infrastructure` · required · raw_text: "focus on ML infrastructure"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_097 - skill `aws` (disagreement)

> ...We work with Kubernetes, Slurm, Python, C++, PyTorch, and primarily on AWS. As an AI Infrastructure Engineer, you will be partnering...

- A: `aws` · required · raw_text: "primarily on AWS"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_097 - skill `model-serving` (disagreement)

> ...Experience supporting both long-running training jobs and high-availability inference services - Ideally, 3-5 years of relevant experience in ML...

- A: `model-serving` · required · raw_text: "high-availability inference services"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_098 - skill `software-engineering` (disagreement)

> ...advanced coding skills in Python and proven experience building and maintaining scalable codebases. - You enjoy mentoring junior colleagues and have prior...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "building and maintaining scalable codebases"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_100 - skill `ai-deployment` (disagreement)

> ...production systems with modern DevOps practices - Experience deploying AI systems in enterprise environments is a plus - Experience working across cloud platforms (AWS, GCP,...

- A: `ai-deployment` · nice_to_have · raw_text: "Experience deploying AI systems in enterprise environments is a plus"
- B: `ai-deployment` · required · raw_text: "deploying LLM-powered applications or AI agents in production"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_100 - skill `llm-orchestration` (disagreement)

> ...- Experience implementing RAG pipelines, tool use, or multi-step AI workflows - Strong understanding of AI system evaluation,...

- A: (did not label this)
- B: `llm-orchestration` · required · raw_text: "multi-step AI workflows"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_101 - skill `ai-deployment` (disagreement)

> ...simulation tools (e.g. Isaac SIM), with a track record of shipping models on real robots. - Not afraid of contributing to a big codebase; finds...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "shipping models on real robots"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_102 - skill `software-architecture` (disagreement)

> ...Android apps used by real users. - Good understanding of Android architecture, Jetpack, Coroutines, Flow and modern Android...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "Android architecture"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_103 - attribute `seniority` (disagreement)

> Member of Technical Staff (Machine Learning Engineer, Search Agent RL) Perplexity...

- A: value=null · basis=null · signal=null
- B: value="senior" · basis="stated" · signal="Member of Technical Staff"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_103 - skill `agent-architecture` (disagreement)

> ...- Multi-agent training, coordination, or evaluation. - Building agent harnesses, distributed training systems, or scalable inference...

- A: `agent-architecture` · nice_to_have · raw_text: "Building agent harnesses"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 34. golden_103 - skill `ai-infrastructure` (disagreement)

> ...Building agent harnesses, distributed training systems, or scalable inference infrastructure. - Large-scale retrieval, ranking, or recommendation...

- A: `ai-infrastructure` · nice_to_have · raw_text: "scalable inference infrastructure"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 35. golden_103 - skill `fine-tuning` (disagreement)

> ...building and shipping ML systems, with deep experience in one or more of LLM post-training, reinforcement learning, search and retrieval, or agent...

- A: `fine-tuning` · required · raw_text: "one or more of LLM post-training"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 36. golden_103 - skill `llms` (disagreement)

> ...complex problems. Our work spans search and retrieval, LLM post-training, multi-agent training, and the harnesses that make these...

- A: (did not label this)
- B: `llms` · required · raw_text: "LLM post-training"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 37. golden_103 - skill `model-development` (disagreement)

> ...software engineering skills and the ability to work across model training, experimentation infrastructure, and production systems....

- A: (did not label this)
- B: `model-development` · required · raw_text: "model training"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 38. golden_104 - attribute `seniority` (disagreement)

> ...culture. We’d love to hear from you if you have: - 3+ years of experience shipping user-facing features or products as a full-stack developer - Demonstrated strong fluency with React & Typescript -...

- A: value="mid" · basis="inferred" · signal="3+ years of experience shipping user-facing features or products as a full-stack developer"
- B: value="senior" · basis="inferred" · signal="Be a mentor to, and be mentored by, exceptional peers across engineering, product & design"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 39. golden_105 - skill `full-stack-development` (disagreement)

> ...(open source or SaaS) and cloud infrastructure - High-load web applications or large-scale APIs - Performance-critical systems such...

- A: (did not label this)
- B: `full-stack-development` · nice_to_have · raw_text: "High-load web applications"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 40. golden_105 - skill `software-engineering` (disagreement)

> ...may be a good fit if you: - Have 8+ years of experience as a software engineer working on production backend systems - Have strong...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "experience as a software engineer"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 41. golden_106 - skill `ai-deployment` (disagreement)

> ...We’re Looking For - Hands-on experience building and deploying data science solutions in Python and related ML libraries. - Strong background...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying data science solutions"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 42. golden_106 - skill `ai-ml` (disagreement)

> ...technical concepts clearly to non-technical audiences and apply AI-enabled approaches to deliver practical business value. Bonus Points For -...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "apply AI-enabled approaches"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 43. golden_108 - attribute `seniority` (disagreement)

> ...time-to-value. The qualifications you need: - Executive-Facing Presales & Value Engineering (2+ years): Demonstrated experience supporting the technical close...

- A: value="mid" · basis="inferred" · signal="Executive-Facing Presales & Value Engineering (2+ years)"
- B: value="junior" · basis="inferred" · signal="Executive-Facing Presales & Value Engineering (2+ years)"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 44. golden_108 - skill `ai-ml` (disagreement)

> ...Python proficiency, API design, SQL, data integration, and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "ML/AI libraries"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 45. golden_108 - skill `azure` (disagreement)

> ...lifecycle management across cloud services (AWS Bedrock, Azure AI, GCP Vertex AI). - AI Architecture & Security:...

- A: `azure` · required · raw_text: "Azure AI"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 46. golden_108 - skill `software-engineering` (disagreement)

> ...operational bottlenecks to strategic AI solutions. - Software/Data Engineering: Python proficiency, API design, SQL, data integration,...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "Software/Data Engineering"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 47. golden_108 - skill `transformers` (disagreement)

> ...libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). - Agentic AI Systems: Hands-on experience with agentic...

- A: (did not label this)
- B: `transformers` · required · raw_text: "Hugging Face Transformers"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 48. golden_094 - attribute `seniority` (uncertain)

> ...AI models. This is a highly technical EM role - you’ll lead a team of expert engineers in a fast-evolving technical domain. In order to empower...

- A: value="senior" · basis="inferred" · signal="lead a team of expert engineers"
- B: value="senior" · basis="inferred" · signal="you’ll lead a team of expert engineers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_094 - skill `ai-ml` (uncertain)

> ...In order to empower this team to be most effective, you will need prior experience in AI, and the appetite to continually invest in deepening your...

- A: `ai-ml` · required · raw_text: "you will need prior experience in AI"
- B: `ai-ml` · required · raw_text: "prior experience in AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_094 - skill `mlops` (uncertain)

> ...domain. Nice to have - Experience training ML models and operating them in production, at scale. #LI-Hybrid Unleash Your Potential When you join...

- A: `mlops` · nice_to_have · raw_text: "operating them in production, at scale"
- B: `mlops` · nice_to_have · raw_text: "Experience training ML models and operating them in production, at scale."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_094 - skill `model-development` (uncertain)

> ...shape over time. - Curiosity and enthusiasm for AI. Experience training ML models and operating them in production at scale is a significant...

- A: `model-development` · nice_to_have · raw_text: "Experience training ML models"
- B: `model-development` · nice_to_have · raw_text: "Experience training ML models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_095 - skill `agents` (uncertain)

> ...risk or business software. - Experience with GenAI, LLMs, agentic workflows, retrieval, evaluation frameworks, or human-in-the-loop...

- A: `agents` · nice_to_have · raw_text: "agentic workflows"
- B: `agents` · nice_to_have · raw_text: "agentic workflows"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_095 - skill `ai-deployment` (uncertain)

> ...tech company. - You have experience developing and shipping state-of-the-art ML models to production and delivering business impact. - You're impact-driven...

- A: `ai-deployment` · required · raw_text: "shipping state-of-the-art ML models to production"
- B: `ai-deployment` · required · raw_text: "deployment of advanced Machine Learning models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_095 - skill `explainable-ai` (uncertain)

> ...working in regulated environments or with products where explainability, auditability and customer trust are especially...

- A: `explainable-ai` · nice_to_have · raw_text: "explainability"
- B: `explainable-ai` · nice_to_have · raw_text: "explainability"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_095 - skill `recommender-systems` (uncertain)

> ...haves - Experience working on personalisation, ranking, recommendation, forecasting, classification or decisioning problems for...

- A: `recommender-systems` · nice_to_have · raw_text: "recommendation"
- B: `recommender-systems` · nice_to_have · raw_text: "recommendation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_096 - skill `mlops` (uncertain)

> ...You understand the full ML lifecycle and have significant experience operationalising models built with frameworks like TensorFlow or PyTorch - You...

- A: `mlops` · required · raw_text: "experience operationalising models"
- B: `mlops` · required · raw_text: "significant experience operationalising models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_097 - skill `ai-deployment` (uncertain)

> ...training jobs and high-availability inference services - Ideally, 3-5 years of relevant experience in ML systems deployment with specific focus on cluster orchestration and resource...

- A: `ai-deployment` · nice_to_have · raw_text: "Ideally, 3-5 years of relevant experience in ML systems deployment"
- B: `ai-deployment` · nice_to_have · raw_text: "Ideally, 3-5 years of relevant experience in ML systems deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_097 - skill `ansible` (uncertain)

> ...- Knowledge of infrastructure as code (Terraform, Ansible) and GitOps practices - Experience with container...

- A: `ansible` · nice_to_have · raw_text: "Ansible"
- B: `ansible` · nice_to_have · raw_text: "Ansible"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_097 - skill `devops` (uncertain)

> ...cluster administration and HPC workload management - Previous roles in SRE, DevOps, or Platform Engineering with focus on ML infrastructure - Experience supporting...

- A: `devops` · required · raw_text: "Previous roles in SRE, DevOps, or Platform Engineering"
- B: `devops` · required · raw_text: "Previous roles in SRE, DevOps, or Platform Engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_097 - skill `terraform` (uncertain)

> ...networking - Knowledge of infrastructure as code (Terraform, Ansible) and GitOps practices - Experience with...

- A: `terraform` · nice_to_have · raw_text: "Terraform"
- B: `terraform` · nice_to_have · raw_text: "Terraform"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_098 - skill `agents` (uncertain)

> ...including experience building Generative AI and agentic AI applications with Large Language Models - You have advanced coding...

- A: `agents` · required · raw_text: "agentic AI applications"
- B: `agents` · required · raw_text: "agentic AI applications"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_099 - skill `agents` (uncertain)

> ...Experience with text-to-SQL, table question answering, or spreadsheet agents. - Experience with reinforcement learning using...

- A: `agents` · nice_to_have · raw_text: "spreadsheet agents"
- B: `agents` · nice_to_have · raw_text: "spreadsheet agents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_099 - skill `model-development` (uncertain)

> ...audiences. - Expert with PyTorch or JAX. - Experience training or fine-tuning large language models, or tabular foundation models (e.g. TabPFN). - Strong...

- A: `model-development` · required · raw_text: "training or fine-tuning large language models"
- B: `model-development` · required · raw_text: "training"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_100 - skill `agents` (uncertain)

> ...building and deploying LLM-powered applications or AI agents in production - Experience with modern LLM tooling such as LangChain,...

- A: `agents` · required · raw_text: "AI agents in production"
- B: `agents` · required · raw_text: "AI agents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_100 - skill `llm-guardrails` (uncertain)

> ...with modern LLM tooling such as LangChain, LlamaIndex, Guardrails, MCP, or agent frameworks - Experience implementing RAG...

- A: `llm-guardrails` · required · raw_text: "Guardrails"
- B: `llm-guardrails` · required · raw_text: "Guardrails"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_101 - skill `machine-learning` (uncertain)

> ...collection. - Experience working on large code bases or large machine learning models at scale. - Contributions to a large open-source or industry...

- A: `machine-learning` · nice_to_have · raw_text: "large machine learning models at scale"
- B: `machine-learning` · nice_to_have · raw_text: "large machine learning models at scale"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_103 - skill `tool-calling` (uncertain)

> ...working system. NICE TO HAVE - Experience with training models to use tools or complete tasks over many steps. - Multi-agent...

- A: `tool-calling` · nice_to_have · raw_text: "training models to use tools"
- B: `tool-calling` · nice_to_have · raw_text: "training models to use tools"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_104 - skill `agents` (uncertain)

> ...Data & Research - Working with user facing LLM and agentic product features - Experience curating and developing eval sets and LLMs...

- A: `agents` · nice_to_have · raw_text: "agentic product features"
- B: `agents` · nice_to_have · raw_text: "agentic product features"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_104 - skill `llms` (uncertain)

> ...levels in the UK. We’re looking for people who have built generative AI products and are eager to lead AI efforts end-to-end, from early...

- A: `llms` · required · raw_text: "built generative AI products"
- B: `llms` · required · raw_text: "have built generative AI products"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_105 - skill `networking` (uncertain)

> ...Understand performance at a systems level — CPU, memory, networking, and data access - Have operated your own code in production: deployed it,...

- A: `networking` · required · raw_text: "networking, and data access"
- B: `networking` · required · raw_text: "networking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_106 - skill `aws` (uncertain)

> ...principles. - Experience with cloud environments (Azure, AWS, GCP) and tools such as Spark, Hive, and Redshift. -...

- A: `aws` · required · raw_text: "AWS"
- B: `aws` · required · raw_text: "AWS"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_106 - skill `azure` (uncertain)

> ...AI principles. - Experience with cloud environments (Azure, AWS, GCP) and tools such as Spark, Hive, and Redshift. -...

- A: `azure` · required · raw_text: "Azure"
- B: `azure` · required · raw_text: "Azure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_106 - skill `data-science` (uncertain)

> ...applicable. What We’re Looking For - Hands-on experience building and deploying data science solutions in Python and related ML libraries. - Strong background...

- A: `data-science` · required · raw_text: "building and deploying data science solutions"
- B: `data-science` · required · raw_text: "building and deploying data science solutions"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_106 - skill `gcp` (uncertain)

> ...Experience with cloud environments (Azure, AWS, GCP) and tools such as Spark, Hive, and Redshift. -...

- A: `gcp` · required · raw_text: "GCP"
- B: `gcp` · required · raw_text: "GCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_107 - skill `ai-developer-tooling` (uncertain)

> ...impact. - You have a clear, informed point of view on using AI to improve how ML engineers work, and you can inspire a team to adopt it. - You think...

- A: `ai-developer-tooling` · required · raw_text: "using AI to improve how ML engineers work"
- B: `ai-developer-tooling` · required · raw_text: "using AI to improve how ML engineers work"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_108 - skill `data-privacy-and-security` (uncertain)

> ...of cloud reference architectures, identity and access, data governance, privacy, and compliance. - Math & Operations Research: Applied knowledge of...

- A: `data-privacy-and-security` · required · raw_text: "data governance, privacy, and compliance"
- B: `data-privacy-and-security` · required · raw_text: "privacy"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_108 - skill `hugging-face` (uncertain)

> ...libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). - Agentic AI Systems: Hands-on experience with agentic...

- A: `hugging-face` · required · raw_text: "Hugging Face Transformers"
- B: `hugging-face` · required · raw_text: "Hugging Face Transformers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_108 - skill `pytorch` (uncertain)

> ...API design, SQL, data integration, and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face...

- A: `pytorch` · required · raw_text: "PyTorch"
- B: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 79. golden_108 - skill `scikit-learn` (uncertain)

> ...integration, and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). - Agentic AI...

- A: `scikit-learn` · required · raw_text: "scikit-learn"
- B: `scikit-learn` · required · raw_text: "scikit-learn"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 80. golden_108 - skill `tensorflow` (uncertain)

> ...SQL, data integration, and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). -...

- A: `tensorflow` · required · raw_text: "TensorFlow"
- B: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 81. golden_108 - skill `xgboost` (uncertain)

> ...and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). - Agentic AI Systems:...

- A: `xgboost` · required · raw_text: "XGBoost"
- B: `xgboost` · required · raw_text: "XGBoost"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 82. golden_103 - skill `ml-engineering|machine-learning` (mapping)

> ...QUALIFICATIONS - A strong track record of building and shipping ML systems, with deep experience in one or more of LLM post-training,...

- A: `ml-engineering` · required · raw_text: "building and shipping ML systems"
- B: `machine-learning` · required · raw_text: "building and shipping ML systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 83. golden_094 - attribute `degree` (spot-check)

> Engineering Manager, AI Models Infrastructure

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_095 - attribute `german` (spot-check)

> Lead Machine Learning Scientist, Business Banking

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_095 - skill `go` (spot-check)

> ...with scikit-learn. You are comfortable using SQL, and keen to learn Go, which is used in many of our backend microservices. -...

- agreed label: `go` · nice_to_have · raw_text: "keen to learn Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_095 - skill `machine-learning` (spot-check)

> ...You have a multiple year track record of excellence leading the development and deployment of advanced Machine Learning models to tackle real business problems, preferably in a...

- agreed label: `machine-learning` · required · raw_text: "leading the development and deployment of advanced Machine Learning models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_095 - skill `microservices` (spot-check)

> ...Commercial experience writing critical production code and working with microservices. - Experience designing experiments, A/B tests or other...

- agreed label: `microservices` · nice_to_have · raw_text: "working with microservices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_095 - skill `scikit-learn` (spot-check)

> ...being told to do so. - You speak Python fluently and have extensive, hands-on experience with scikit-learn. You are comfortable using SQL, and keen to learn Go,...

- agreed label: `scikit-learn` · required · raw_text: "extensive, hands-on experience with scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_096 - attribute `degree` (spot-check)

> Senior Machine Learning Engineer

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_096 - skill `aws` (spot-check)

> ...hands-on experience with cloud platforms (e.g., AWS, Azure, GCP), including architecture, security, and...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_096 - skill `gcp` (spot-check)

> ...experience with cloud platforms (e.g., AWS, Azure, GCP), including architecture, security, and infrastructure -...

- agreed label: `gcp` · required · raw_text: "GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_096 - skill `kubernetes` (spot-check)

> ...with container and orchestration tools such at Docker & Kubernetes to build and manage applications at scale - You thrive...

- agreed label: `kubernetes` · required · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_096 - skill `python` (spot-check)

> ...- You bring deep expertise in software engineering and strong Python skills, focusing on building robust, reusable systems - You...

- agreed label: `python` · required · raw_text: "strong Python skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_096 - skill `pytorch` (spot-check)

> ...models built with frameworks like TensorFlow or PyTorch - You bring deep expertise in software engineering and...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_096 - skill `tensorflow` (spot-check)

> ...operationalising models built with frameworks like TensorFlow or PyTorch - You bring deep expertise in software...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_097 - attribute `german` (spot-check)

> Member of Technical Staff (AI Infrastructure Engineer)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_097 - skill `apis` (spot-check)

> ...and compute resource management for ML workloads - Experience developing APIs and managing distributed systems for both batch and...

- agreed label: `apis` · required · raw_text: "Experience developing APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_097 - skill `distributed-systems` (spot-check)

> ...- Deep understanding of container orchestration and distributed systems architecture - High level familiarity with LLM architecture and...

- agreed label: `distributed-systems` · required · raw_text: "distributed systems architecture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_097 - skill `gitops` (spot-check)

> ...of infrastructure as code (Terraform, Ansible) and GitOps practices - Experience with container registries, image...

- agreed label: `gitops` · nice_to_have · raw_text: "GitOps practices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_097 - skill `infrastructure-as-code` (spot-check)

> ...and high-performance networking - Knowledge of infrastructure as code (Terraform, Ansible) and GitOps practices - Experience...

- agreed label: `infrastructure-as-code` · nice_to_have · raw_text: "infrastructure as code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_097 - skill `llms` (spot-check)

> ...and distributed systems architecture - High level familiarity with LLM architecture and training processes (Multi-Head Attention,...

- agreed label: `llms` · required · raw_text: "familiarity with LLM architecture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_097 - skill `networking` (spot-check)

> ...such as PyTorch in distributed training contexts - Strong understanding of networking, storage, and compute resource management for ML...

- agreed label: `networking` · required · raw_text: "Strong understanding of networking"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_097 - skill `observability` (spot-check)

> ...workloads - Solid debugging and monitoring skills with expertise in observability tools for containerized environments PREFERRED SKILLS -...

- agreed label: `observability` · required · raw_text: "expertise in observability tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_098 - skill `python` (spot-check)

> ...Language Models - You have advanced coding skills in Python and proven experience building and maintaining scalable...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_099 - attribute `seniority` (spot-check)

> Applied Scientist - Tabular Data, EMEA

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_099 - skill `fine-tuning` (spot-check)

> ...- Expert with PyTorch or JAX. - Experience training or fine-tuning large language models, or tabular foundation models (e.g. TabPFN). - Strong...

- agreed label: `fine-tuning` · required · raw_text: "fine-tuning large language models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_099 - skill `python` (spot-check)

> ...- Writes clean, readable, high-performance, fault-tolerant Python code. - Doesn’t need roadmaps: moves independently and...

- agreed label: `python` · required · raw_text: "Python code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_099 - skill `pytorch` (spot-check)

> ...technical and non-technical audiences. - Expert with PyTorch or JAX. - Experience training or fine-tuning large...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_099 - skill `reinforcement-learning` (spot-check)

> ...answering, or spreadsheet agents. - Experience with reinforcement learning using verifiable rewards (e.g. query execution). - Experience working on large...

- agreed label: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning using verifiable rewards"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_099 - skill `sql` (spot-check)

> ...classical baselines (e.g. gradient boosting), and comfortable with SQL, pandas, and messy real-world data. - Not afraid of...

- agreed label: `sql` · required · raw_text: "comfortable with SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_099 - skill `testing` (spot-check)

> ...conferences. - Enjoys improving existing code: typing, tests, CI pipelines. WHAT WE OFFER We offer a comprehensive...

- agreed label: `testing` · nice_to_have · raw_text: "tests"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_100 - attribute `seniority` (spot-check)

> ...AI platform continues to evolve WHO YOU ARE - 8+ years of professional software engineering experience - Strong proficiency in Python or TypeScript -...

- agreed label: value="senior" · basis="inferred" · signal="8+ years of professional software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_100 - skill `agent-architecture` (spot-check)

> ...(AWS, GCP, or Azure) is a plus - Experience with agent architectures and long-horizon task execution is a plus - Familiarity...

- agreed label: `agent-architecture` · nice_to_have · raw_text: "agent architectures"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_100 - skill `azure` (spot-check)

> ...- Experience working across cloud platforms (AWS, GCP, or Azure) is a plus - Experience with agent architectures and...

- agreed label: `azure` · nice_to_have · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_100 - skill `langchain` (spot-check)

> ...production - Experience with modern LLM tooling such as LangChain, LlamaIndex, Guardrails, MCP, or agent frameworks -...

- agreed label: `langchain` · required · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_100 - skill `llamaindex` (spot-check)

> ...- Experience with modern LLM tooling such as LangChain, LlamaIndex, Guardrails, MCP, or agent frameworks - Experience...

- agreed label: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_100 - skill `llms` (spot-check)

> ...Python or TypeScript - Experience building and deploying LLM-powered applications or AI agents in production - Experience with modern LLM...

- agreed label: `llms` · required · raw_text: "LLM-powered applications"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_100 - skill `mcp` (spot-check)

> ...LLM tooling such as LangChain, LlamaIndex, Guardrails, MCP, or agent frameworks - Experience implementing RAG...

- agreed label: `mcp` · required · raw_text: "MCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_100 - skill `software-engineering` (spot-check)

> ...continues to evolve WHO YOU ARE - 8+ years of professional software engineering experience - Strong proficiency in Python or TypeScript -...

- agreed label: `software-engineering` · required · raw_text: "professional software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_100 - skill `tool-calling` (spot-check)

> ...MCP, or agent frameworks - Experience implementing RAG pipelines, tool use, or multi-step AI workflows - Strong understanding of AI...

- agreed label: `tool-calling` · required · raw_text: "RAG pipelines, tool use"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_101 - attribute `seniority` (spot-check)

> Applied Scientist Lead - Robotics, EMEA ABOUT MISTRAL Mistral provides...

- agreed label: value="senior" · basis="stated" · signal="Applied Scientist Lead"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_101 - skill `ci-cd` (spot-check)

> ...- Enjoys improving existing code: typing, tests, CI pipelines. WHAT WE OFFER We offer a comprehensive benefits...

- agreed label: `ci-cd` · nice_to_have · raw_text: "CI pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_101 - skill `jax` (spot-check)

> ...work with team leadership and stakeholder management. - Expert with PyTorch or JAX. - Deep experience with Vision Language Models (VLM),...

- agreed label: `jax` · required · raw_text: "Expert with PyTorch or JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_101 - skill `pytorch` (spot-check)

> ...work with team leadership and stakeholder management. - Expert with PyTorch or JAX. - Deep experience with Vision Language Models (VLM),...

- agreed label: `pytorch` · required · raw_text: "Expert with PyTorch or JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_102 - skill `kotlin` (spot-check)

> ...attention to reliability. WHAT WE'RE LOOKING FOR - Strong native Android experience using Kotlin. - Experience shipping Android apps used by real...

- agreed label: `kotlin` · required · raw_text: "Strong native Android experience using Kotlin"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_103 - attribute `german` (spot-check)

> Member of Technical Staff (Machine Learning Engineer, Search Agent RL)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_103 - skill `distributed-training` (spot-check)

> ...coordination, or evaluation. - Building agent harnesses, distributed training systems, or scalable inference infrastructure. - Large-scale...

- agreed label: `distributed-training` · nice_to_have · raw_text: "distributed training systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_103 - skill `evaluation` (spot-check)

> ...infrastructure, and production systems. - Experience designing rigorous evaluations, diagnosing failures, and translating experimental results...

- agreed label: `evaluation` · required · raw_text: "designing rigorous evaluations"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_103 - skill `recommender-systems` (spot-check)

> ...infrastructure. - Large-scale retrieval, ranking, or recommendation systems.

- agreed label: `recommender-systems` · nice_to_have · raw_text: "recommendation systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_103 - skill `software-engineering` (spot-check)

> ...learning, search and retrieval, or agent systems. - Strong software engineering skills and the ability to work across model training,...

- agreed label: `software-engineering` · required · raw_text: "Strong software engineering skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_104 - skill `full-stack-development` (spot-check)

> ...of experience shipping user-facing features or products as a full-stack developer - Demonstrated strong fluency with React & Typescript -...

- agreed label: `full-stack-development` · required · raw_text: "as a full-stack developer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_104 - skill `react` (spot-check)

> ...a full-stack developer - Demonstrated strong fluency with React & Typescript - Experience communicating and working...

- agreed label: `react` · required · raw_text: "React"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_104 - skill `typescript` (spot-check)

> ...developer - Demonstrated strong fluency with React & Typescript - Experience communicating and working across functions...

- agreed label: `typescript` · required · raw_text: "Typescript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_105 - attribute `degree` (spot-check)

> Staff Software Engineer (Agentic Search) - Runtime

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_105 - attribute `seniority` (spot-check)

> Staff Software Engineer (Agentic Search) - Runtime About Nebius: Nebius is...

- agreed label: value="senior" · basis="stated" · signal="Staff Software Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_105 - skill `apis` (spot-check)

> ...and cloud infrastructure - High-load web applications or large-scale APIs - Performance-critical systems such as trading platforms...

- agreed label: `apis` · nice_to_have · raw_text: "large-scale APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_105 - skill `backend-development` (spot-check)

> ...8+ years of experience as a software engineer working on production backend systems - Have strong hands-on expertise in C++ or Rust in...

- agreed label: `backend-development` · required · raw_text: "production backend systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_105 - skill `cpp` (spot-check)

> ...backend systems - Have strong hands-on expertise in C++ or Rust in real-world, high-load services - Have built...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_105 - skill `rust` (spot-check)

> ...and AI R&D. The Product In a rapidly evolving world, trust in AI depends on AI agents being grounded in fresh,...

- agreed label: `rust` · required · raw_text: "Rust"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_106 - attribute `german` (spot-check)

> Senior Data Scientist

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_106 - attribute `seniority` (spot-check)

> Senior Data Scientist Location: London (Hybrid) | Practice Area: Data &...

- agreed label: value="senior" · basis="stated" · signal="Senior Data Scientist"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_106 - skill `apache-spark` (spot-check)

> ...cloud environments (Azure, AWS, GCP) and tools such as Spark, Hive, and Redshift. - Demonstrated ability to lead...

- agreed label: `apache-spark` · required · raw_text: "Spark"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_106 - skill `ci-cd` (spot-check)

> ...science competitions. - Experience with MLOps practices (CI/CD, model monitoring, DevOps integration). - Familiarity...

- agreed label: `ci-cd` · nice_to_have · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_106 - skill `devops` (spot-check)

> ...Experience with MLOps practices (CI/CD, model monitoring, DevOps integration). - Familiarity with advanced NLP frameworks such as...

- agreed label: `devops` · nice_to_have · raw_text: "DevOps integration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_106 - skill `llms` (spot-check)

> ...or Transformers and exposure to AI technologies including Generative AI or LLMs. - MSc or PhD in a numerate discipline. - Financial...

- agreed label: `llms` · nice_to_have · raw_text: "Generative AI or LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_106 - skill `observability` (spot-check)

> ...competitions. - Experience with MLOps practices (CI/CD, model monitoring, DevOps integration). - Familiarity with advanced NLP...

- agreed label: `observability` · nice_to_have · raw_text: "model monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_106 - skill `python` (spot-check)

> ...building and deploying data science solutions in Python and related ML libraries. - Strong background in applied...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_106 - skill `transformers` (spot-check)

> ...Familiarity with advanced NLP frameworks such as spaCy or Transformers and exposure to AI technologies including Generative AI or...

- agreed label: `transformers` · nice_to_have · raw_text: "Transformers"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_107 - skill `machine-learning` (spot-check)

> ...align priorities and share context. Who You Are - You have deep machine learning expertise and Staff-level technical judgement, and you're...

- agreed label: `machine-learning` · required · raw_text: "deep machine learning expertise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_107 - skill `nlp` (spot-check)

> ...hands-on when it matters. - You bring experience across NLP, audio / music content understanding and recommender...

- agreed label: `nlp` · required · raw_text: "NLP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_108 - attribute `degree` (spot-check)

> ...English with exceptional executive presence. - Degree: Masters Degree in computer science, engineering, mathematics, business engineering, business information or related fields , or equivalent work experience preferred. #LI-NS1 What Celonis can offer you: - Pioneer...

- agreed label: value="master" · requirement="nice_to_have" · or_equivalent=true · signal="Masters Degree in computer science, engineering, mathematics, business engineering, business information or related fields , or equivalent work experience preferred"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_108 - attribute `german` (spot-check)

> Applied Value Engineer - AI and Pre-Sales Consultant

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_108 - skill `ai-deployment` (spot-check)

> ...workflows. - Production ML/LLMOps: Experience with model deployment, monitoring, MLOps/LLMOps, and lifecycle management across...

- agreed label: `ai-deployment` · required · raw_text: "model deployment"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_108 - skill `aws-bedrock` (spot-check)

> ...and lifecycle management across cloud services (AWS Bedrock, Azure AI, GCP Vertex AI). - AI Architecture & Security:...

- agreed label: `aws-bedrock` · required · raw_text: "AWS Bedrock"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_108 - skill `cloud` (spot-check)

> ...monitoring, MLOps/LLMOps, and lifecycle management across cloud services (AWS Bedrock, Azure AI, GCP Vertex AI). - AI Architecture...

- agreed label: `cloud` · required · raw_text: "cloud services"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 156. golden_108 - skill `llmops` (spot-check)

> ...ML/LLMOps: Experience with model deployment, monitoring, MLOps/LLMOps, and lifecycle management across cloud services (AWS...

- agreed label: `llmops` · required · raw_text: "MLOps/LLMOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 157. golden_108 - skill `observability` (spot-check)

> ...Production ML/LLMOps: Experience with model deployment, monitoring, MLOps/LLMOps, and lifecycle management across cloud...

- agreed label: `observability` · required · raw_text: "monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 158. golden_108 - skill `prompt-engineering` (spot-check)

> ...LLM orchestration, tool use/function calling, RAG, agents, prompt engineering, or agentic patterns for enterprise workflows. -...

- agreed label: `prompt-engineering` · required · raw_text: "prompt engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 159. golden_108 - skill `python` (spot-check)

> ...to strategic AI solutions. - Software/Data Engineering: Python proficiency, API design, SQL, data integration, and ML/AI libraries...

- agreed label: `python` · required · raw_text: "Python proficiency"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 160. golden_108 - skill `reinforcement-learning` (spot-check)

> ...of linear/nonlinear optimization, statistical analysis, reinforcement learning, and forecasting is a plus. - Strong presentation skills...

- agreed label: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 161. golden_108 - skill `sql` (spot-check)

> ...Software/Data Engineering: Python proficiency, API design, SQL, data integration, and ML/AI libraries (PyTorch,...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 162. golden_108 - skill `statistics` (spot-check)

> ...Applied knowledge of linear/nonlinear optimization, statistical analysis, reinforcement learning, and forecasting is a plus. -...

- agreed label: `statistics` · nice_to_have · raw_text: "statistical analysis"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
