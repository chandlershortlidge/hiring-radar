# Review queue - 20261125T135346Z_label

176 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-haiku-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261125T135346Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 245 accepted labels,
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

## 1. golden_149 - scope `in_scope` (in-scope)

> Forward-Deployed AI Engineer – AVP

- Citigroup Inc. · Forward-Deployed AI Engineer – AVP
- New York · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_150 - scope `in_scope` (in-scope)

> Principal Forward Deployed AI Engineers

- indiciumai · Principal Forward Deployed AI Engineers
- London · en · greenhouse · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_151 - scope `in_scope` (in-scope)

> NTT DATA Deutschland SE: Forward Deployed Engineer (w/m/x) - AI & Enterprise Solutions 1 1

- NTT DATA Deutschland SE · NTT DATA Deutschland SE: Forward Deployed Engineer (w/m/x) - AI & Enterprise Solutions 1 1
- Berlin · de · arbeitsagentur · 22 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_152 - scope `in_scope` (in-scope)

> Advisory AI Data Specialist (Forward Deployment Engineering)

- Dell Technologies · Advisory AI Data Specialist (Forward Deployment Engineering)
- Berlin · en · jsearch · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_153 - scope `in_scope` (in-scope)

> Forward Deployed AI Engineer-Anthropic-Netherlands/Western Europe

- NewRocket · Forward Deployed AI Engineer-Anthropic-Netherlands/Western Europe
- Amsterdam · en · jsearch · 36 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_154 - scope `in_scope` (in-scope)

> (Junior) Forward Deployed Engineer – AI

- Reply · (Junior) Forward Deployed Engineer – AI
- Berlin · de · jsearch · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_155 - scope `in_scope` (in-scope)

> Applied AI, Forward Deployed Engineer - CyberSecurity (Europe)

- mistral.ai · Applied AI, Forward Deployed Engineer - CyberSecurity (Europe)
- Berlin · en · ashby · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_156 - scope `in_scope` (in-scope)

> Applied AI, Forward Deployed Machine Learning Engineer - London

- mistral.ai · Applied AI, Forward Deployed Machine Learning Engineer - London
- London · en · ashby · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_157 - scope `in_scope` (in-scope)

> Applied AI, Forward Deployed Machine Learning Engineer

- mistral.ai · Applied AI, Forward Deployed Machine Learning Engineer
- San Francisco · en · ashby · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_158 - scope `in_scope` (in-scope)

> Job Title AI Engineer / Forward Deployed Engineer

- L'Oreal · AI Engineer / Forward Deployed Engineer
- New York · en · jsearch · 25 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_159 - scope `in_scope` (in-scope)

> Forward Deployed AI Engineer (m/w/d) – Multi-Agent Systems | München

- advanced engineering GmbH · Forward Deployed AI Engineer (m/w/d) – Multi-Agent Systems | München
- Munich · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_160 - scope `in_scope` (in-scope)

> AI Forward Deployed Engineer - Netherlands

- databricks · AI Forward Deployed Engineer - Netherlands
- Amsterdam · en · arbeitnow · 17 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_161 - scope `in_scope` (in-scope)

> Forward Deployed AI Engineer (m/f/d)

- agilerobotsse · Forward Deployed AI Engineer (m/f/d)
- Munich · en · arbeitnow · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_162 - scope `in_scope` (in-scope)

> AI Builder, Forward Deployed Engineering, Research and Product

- Clera · AI Builder, Forward Deployed Engineering, Research and Product
- New York · en · ashby · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_163 - scope `in_scope` (in-scope)

> Forward Deployed Engineer, Physical AI Infrastructure

- Nebius · Forward Deployed Engineer, Physical AI Infrastructure
- Remote (EU) · en · greenhouse · 25 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_150 - skill `anthropic-api` (disagreement)

> ...presence in AI engineering - Experience working alongside partner ecosystems such as Anthropic, Databricks, or AWS What we are not asking for: a...

- A: `anthropic-api` · nice_to_have · raw_text: "partner ecosystems such as Anthropic"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_150 - skill `aws` (disagreement)

> ...partner ecosystems such as Anthropic, Databricks, or AWS What we are not asking for: a specific number of years, a...

- A: `aws` · nice_to_have · raw_text: "or AWS"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_150 - skill `databricks` (disagreement)

> ...working alongside partner ecosystems such as Anthropic, Databricks, or AWS What we are not asking for: a specific number of years, a...

- A: `databricks` · nice_to_have · raw_text: "Databricks, or AWS"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_151 - skill `cybersecurity` (disagreement)

> ...technisches Know-how mit einem sicheren Verständnis für Security, Privacy und Sovereign AI, überzeugst im Umgang mit...

- A: (did not label this)
- B: `cybersecurity` · required · raw_text: "Security"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_151 - skill `software-architecture` (disagreement)

> ...über 10–13 Jahre IT-Erfahrung, davon mindestens 5 Jahre in AI/ML-Architektur, und hast Enterprise-AI-/GenAI-Lösungen in Private-Cloud-,...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "AI/ML-Architektur"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_152 - skill `data-privacy-and-security` (disagreement)

> ...configuring data governance and compliance controls for secure and compliant use of data, including sensitive data. • Proven ability to scale data pipelines from pilot to...

- A: (did not label this)
- B: `data-privacy-and-security` · required · raw_text: "secure and compliant use of data, including sensitive data"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_152 - skill `embeddings` (disagreement)

> ...and AI/ML-related data patterns (e.g., feature stores, vectorization, RAG-related data flows). • Experience configuring data...

- A: (did not label this)
- B: `embeddings` · required · raw_text: "vectorization"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_153 - skill `agents` (disagreement)

> ...generation (RAG), tool use, structured outputs, agentic workflows, model evaluation, and responsible AI controls—to deliver...

- A: (did not label this)
- B: `agents` · required · raw_text: "agentic workflows"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_153 - skill `conversational-ai` (disagreement)

> ...AI/LLM-powered applications, AI-enabled automations, conversational experiences, RAG systems, or agentic workflows. • Experience...

- A: (did not label this)
- B: `conversational-ai` · required · raw_text: "conversational experiences"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_153 - skill `data-modeling` (disagreement)

> ...and platform development patterns. • Understanding of ServiceNow data models and enterprise workflow concepts, including: • • CMDB •...

- A: (did not label this)
- B: `data-modeling` · nice_to_have · raw_text: "ServiceNow data models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_153 - skill `data-pipelines` (disagreement)

> ...Experience with vector databases, embeddings, document ingestion, chunking, retrieval strategies, and knowledge-grounding...

- A: (did not label this)
- B: `data-pipelines` · nice_to_have · raw_text: "document ingestion"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_153 - skill `data-privacy-and-security` (disagreement)

> ...AI concepts, including hallucination mitigation, sensitive-data handling, identity and access controls, human oversight, AI safety,...

- A: (did not label this)
- B: `data-privacy-and-security` · required · raw_text: "sensitive-data handling"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_153 - skill `hallucination-detection` (disagreement)

> ...Understanding of responsible AI concepts, including hallucination mitigation, sensitive-data handling, identity and access controls,...

- A: `hallucination-detection` · required · raw_text: "hallucination mitigation"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_154 - skill `ai-ml` (disagreement)

> ...über konkrete eigene Projekte oder Praxiserfahrung • Interesse an modernen Cloud- und AI-Technologien sowie Motivation, neue Ansätze schnell auszuprobieren und...

- A: (did not label this)
- B: `ai-ml` · nice_to_have · raw_text: "Interesse an modernen Cloud- und AI-Technologien"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_155 - skill `ai-ml` (disagreement)

> ...on AI-based products - You have proven experience in AI or machine learning product implementation with APIs, back-end, and front-end interfaces - You have...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI or machine learning product implementation"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_156 - skill `ai-ml` (disagreement)

> ...contributor (data scientist or software engineer) on AI-based products - You have proven experience in AI or machine learning...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI-based products"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_157 - attribute `seniority` (disagreement)

> ...You hold a PhD / master in AI / data science. • You have 2+ years as a technical individual contributor (data scientist or software engineer) on AI-based...

- A: value="junior" · basis="inferred" · signal="You have 2+ years as a technical individual contributor"
- B: value="mid" · basis="inferred" · signal="proven experience"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_157 - skill `ai-deployment` (disagreement)

> ...learning and LLMs • You're experienced with building and deploying LLMs or NLP applications • You have proven experience in AI or...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying LLMs"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 34. golden_157 - skill `ai-ml` (disagreement)

> ...contributor (data scientist or software engineer) on AI-based products • You have experience in Fine Tuning LLMs, tackling...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI-based products"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 35. golden_158 - attribute `seniority` (disagreement)

> ...AI/ML models (internships, co-ops, or full-time roles) (2+ years). Core technical skills: • A strong foundation in...

- A: value="junior" · basis="inferred" · signal="(2+ years)"
- B: value="mid" · basis="inferred" · signal="Proven real-world experience deploying AI/ML models (internships, co-ops, or full-time roles) (2+ years)."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 36. golden_158 - skill `crewai` (disagreement)

> ...or LLM orchestration using tools such as LangGraph, CrewAI, or Google ADK. • Diffusion models and other generative AI...

- A: `crewai` · nice_to_have · raw_text: "CrewAI"
- B: `crewai` · required · raw_text: "Agentic workflows or LLM orchestration using tools such as LangGraph, CrewAI, or Google ADK."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 37. golden_158 - skill `evaluation` (disagreement)

> ...A solid understanding of LLMs and experience developing or evaluating LLM-powered /Agentic applications. • Familiarity with version control, testing,...

- A: (did not label this)
- B: `evaluation` · required · raw_text: "evaluating LLM-powered /Agentic applications"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 38. golden_158 - skill `google-adk` (disagreement)

> ...orchestration using tools such as LangGraph, CrewAI, or Google ADK. • Diffusion models and other generative AI approaches. •...

- A: `google-adk` · nice_to_have · raw_text: "Google ADK"
- B: `google-adk` · required · raw_text: "Google ADK"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 39. golden_158 - skill `infrastructure-as-code` (disagreement)

> ...models and other generative AI approaches. • CI/CD, infrastructure as code, and MLOps tools such as Terraform, Jenkins, MLflow, or...

- A: `infrastructure-as-code` · nice_to_have · raw_text: "infrastructure as code"
- B: `infrastructure-as-code` · required · raw_text: "infrastructure as code"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 40. golden_158 - skill `langgraph` (disagreement)

> ...Agentic workflows or LLM orchestration using tools such as LangGraph, CrewAI, or Google ADK. • Diffusion models and other...

- A: `langgraph` · nice_to_have · raw_text: "LangGraph"
- B: `langgraph` · required · raw_text: "Agentic workflows or LLM orchestration using tools such as LangGraph, CrewAI, or Google ADK."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 41. golden_158 - skill `llm-orchestration` (disagreement)

> ...experience we value: • Agentic workflows or LLM orchestration using tools such as LangGraph, CrewAI, or Google ADK. •...

- A: `llm-orchestration` · nice_to_have · raw_text: "LLM orchestration"
- B: `llm-orchestration` · required · raw_text: "LLM orchestration"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 42. golden_160 - skill `ai-deployment` (disagreement)

> ...as HuggingFace, LangChain, and DSPy</li> <li>Expertise in deploying production-grade GenAI applications, including evaluation and...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying production-grade GenAI applications"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 43. golden_161 - skill `ai-ml` (disagreement)

> ...four years of professional experience in machine learning, AI for robotics, or computer vision - Hands-on experience working with...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI for robotics"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 44. golden_161 - skill `model-development` (disagreement)

> ...policies, imitation or reinforcement learning policies), covering training, fine-tuning, and deployment - Strong programming skills in both Python and C++ -...

- A: (did not label this)
- B: `model-development` · required · raw_text: "covering training, fine-tuning, and deployment"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 45. golden_162 - attribute `seniority` (disagreement)

> ...and non-technical audiences. WHAT WE'RE LOOKING FOR - At least 3 years of experience in applied machine learning, reinforcement learning,...

- A: value="mid" · basis="inferred" · signal="At least 3 years of experience"
- B: value="senior" · basis="inferred" · signal="Lead technical discovery with senior stakeholders and scope solutions to ambiguous business problems."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 46. golden_162 - skill `data-science` (disagreement)

> ...software engineering, physics, machine learning, or data science. COMPENSATION & BENEFITS Base salary range: $140,000 to...

- A: (did not label this)
- B: `data-science` · required · raw_text: "data science"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 47. golden_163 - skill `ai-infrastructure` (disagreement)

> ...the cost and complexity of building large in-house AI/ML infrastructure. Built by engineers, for engineers. From large-scale GPU...

- A: (did not label this)
- B: `ai-infrastructure` · required · raw_text: "ML infrastructure"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 48. golden_150 - skill `agents` (uncertain)

> ...up in production - Set the architectural patterns for agentic systems at scale, including state and memory design, failure modes...

- A: `agents` · required · raw_text: "agentic systems"
- B: `agents` · required · raw_text: "agentic systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_150 - skill `ai-deployment` (uncertain)

> ...sound like you, we encourage you to apply. - You have taken AI systems from ambiguous problem to production deployment, including agentic systems, retrieval architectures and...

- A: `ai-deployment` · required · raw_text: "taken AI systems from ambiguous problem to production deployment"
- B: `ai-deployment` · required · raw_text: "AI systems from ambiguous problem to production deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_150 - skill `claude-code` (uncertain)

> ...are equipped with Claude licenses for Chat, Cowork and Claude Code. We are building a team of engineers who work at the...

- A: `claude-code` · nice_to_have · raw_text: "Claude Code"
- B: `claude-code` · nice_to_have · raw_text: "Claude Code"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_150 - skill `cybersecurity` (uncertain)

> ...a the reality of working in a large organisation: security reviews, compliance, legacy systems, and multiple teams with...

- A: `cybersecurity` · required · raw_text: "security reviews"
- B: `cybersecurity` · required · raw_text: "security reviews"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_150 - skill `rag` (uncertain)

> ...regulated environments - Build advanced RAG pipelines - retrieval architectures, embedding strategies, reranking, hybrid search, and the...

- A: `rag` · required · raw_text: "retrieval architectures"
- B: `rag` · required · raw_text: "retrieval architectures"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_150 - skill `software-architecture` (uncertain)

> ...owned the technical direction of a project or workstream, made the architecture calls, and been accountable for the decisions made - You are...

- A: `software-architecture` · required · raw_text: "made the architecture calls"
- B: `software-architecture` · required · raw_text: "made the architecture calls"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_151 - skill `agents` (uncertain)

> ...LLMs, RAG, Vector Databases, Prompt Engineering und Agentic AI sowie Frameworks wie LangChain, LlamaIndex, Haystack oder Semantic Kernel...

- A: `agents` · required · raw_text: "Agentic AI sowie Frameworks"
- B: `agents` · required · raw_text: "Agentic AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_151 - skill `ai-infrastructure` (uncertain)

> ...Detection und Production Support. - Du kennst dich mit GPU- und AI-Infrastrukturen aus – einschließlich NVIDIA Stack, CUDA, MIG, Model...

- A: `ai-infrastructure` · required · raw_text: "GPU- und AI-Infrastrukturen"
- B: `ai-infrastructure` · required · raw_text: "AI-Infrastrukturen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_151 - skill `ai-ml` (uncertain)

> ...Du verfügst über 10–13 Jahre IT-Erfahrung, davon mindestens 5 Jahre in AI/ML-Architektur, und hast Enterprise-AI-/GenAI-Lösungen in Private-Cloud-,...

- A: `ai-ml` · required · raw_text: "mindestens 5 Jahre in AI/ML-Architektur"
- B: `ai-ml` · required · raw_text: "AI/ML-Architektur"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_151 - skill `cloud` (uncertain)

> ...und hast Enterprise-AI-/GenAI-Lösungen in Private-Cloud-, On-Premises- oder Hybrid-Umgebungen erfolgreich umgesetzt. - Du bringst ausgeprägte...

- A: `cloud` · required · raw_text: "Private-Cloud-, On-Premises- oder Hybrid-Umgebungen"
- B: `cloud` · required · raw_text: "Private-Cloud-"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_151 - skill `data-privacy-and-security` (uncertain)

> ...technisches Know-how mit einem sicheren Verständnis für Security, Privacy und Sovereign AI, überzeugst im Umgang mit...

- A: `data-privacy-and-security` · required · raw_text: "Security, Privacy"
- B: `data-privacy-and-security` · required · raw_text: "Security, Privacy"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_151 - skill `llmops` (uncertain)

> ...oder Qwen. - Du bist sicher im Umgang mit Kubernetes, Docker/OpenShift und MLOps/LLMOps und kennst Technologien wie MLflow, Kubeflow, KServe, Ray,...

- A: `llmops` · required · raw_text: "Docker/OpenShift und MLOps/LLMOps"
- B: `llmops` · required · raw_text: "LLMOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_151 - skill `mlops` (uncertain)

> ...oder Qwen. - Du bist sicher im Umgang mit Kubernetes, Docker/OpenShift und MLOps/LLMOps und kennst Technologien wie MLflow, Kubeflow, KServe, Ray,...

- A: `mlops` · required · raw_text: "Docker/OpenShift und MLOps/LLMOps"
- B: `mlops` · required · raw_text: "MLOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_151 - skill `open-source-llms` (uncertain)

> ...LangChain, LlamaIndex, Haystack oder Semantic Kernel und Open-Source-Modelle wie Llama, Mistral, DeepSeek oder Qwen. - Du bist sicher im Umgang mit Kubernetes,...

- A: `open-source-llms` · required · raw_text: "Open-Source-Modelle wie Llama, Mistral, DeepSeek oder Qwen"
- B: `open-source-llms` · required · raw_text: "Open-Source-Modelle"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_152 - skill `data-engineering` (uncertain)

> ...and governance practices. Essential Requirements • 7-10+ years in data engineering, analytics platforms or AI data roles within large or...

- A: `data-engineering` · required · raw_text: "7-10+ years in data engineering"
- B: `data-engineering` · required · raw_text: "data engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_153 - skill `ai-deployment` (uncertain)

> ...and access controls, human oversight, AI safety, and secure AI deployment. • Experience operating in customer-facing engineering,...

- A: `ai-deployment` · required · raw_text: "secure AI deployment"
- B: `ai-deployment` · required · raw_text: "secure AI deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_155 - attribute `seniority` (uncertain)

> ...scientist or software engineer) on AI-based products - You have proven experience in AI or machine learning product implementation with...

- A: value="mid" · basis="inferred" · signal="You have proven experience"
- B: value="mid" · basis="inferred" · signal="proven experience in AI or machine learning product implementation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_155 - skill `agents` (uncertain)

> ...interfaces - You have experience tackling advanced RAG, building agentic use cases, or fine-tuning LLMs - You have a deep understanding of...

- A: `agents` · required · raw_text: "building agentic use cases"
- B: `agents` · required · raw_text: "building agentic use cases"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_155 - skill `backend-development` (uncertain)

> ...AI or machine learning product implementation with APIs, back-end, and front-end interfaces - You have experience tackling...

- A: `backend-development` · required · raw_text: "back-end"
- B: `backend-development` · required · raw_text: "back-end"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_155 - skill `cybersecurity` (uncertain)

> ...attitude - Pentesting knowledge - Experience developing a cybersecurity product - Experience building agentic harnesses or multi-agent...

- A: `cybersecurity` · nice_to_have · raw_text: "developing a cybersecurity product"
- B: `cybersecurity` · nice_to_have · raw_text: "Experience with security tooling or workflows"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_155 - skill `evaluation` (uncertain)

> ...multi-agent systems end-to-end - A strong background in evals and benchmarking of agent systems - Experience with security tooling or...

- A: `evaluation` · nice_to_have · raw_text: "evals and benchmarking"
- B: `evaluation` · nice_to_have · raw_text: "evals"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_155 - skill `frontend-development` (uncertain)

> ...learning product implementation with APIs, back-end, and front-end interfaces - You have experience tackling advanced RAG, building...

- A: `frontend-development` · required · raw_text: "front-end interfaces"
- B: `frontend-development` · required · raw_text: "front-end interfaces"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_156 - attribute `seniority` (uncertain)

> ...or software engineer) on AI-based products - You have proven experience in AI or machine learning product implementation with...

- A: value="mid" · basis="inferred" · signal="proven experience"
- B: value="mid" · basis="inferred" · signal="proven experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_156 - skill `agents` (uncertain)

> ...experience in Fine Tuning LLMs, tackling advanced RAG or agentic use cases - You have deep understanding of concepts and algorithms...

- A: `agents` · required · raw_text: "agentic use cases"
- B: `agents` · required · raw_text: "agentic use cases"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_156 - skill `fine-tuning` (uncertain)

> ...with APIs, back-end and front-end interfaces. - You have experience in Fine Tuning LLMs, tackling advanced RAG or agentic use cases - You have...

- A: `fine-tuning` · required · raw_text: "experience in Fine Tuning LLMs"
- B: `fine-tuning` · required · raw_text: "Fine Tuning LLMs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_156 - skill `rag` (uncertain)

> ...You have experience in Fine Tuning LLMs, tackling advanced RAG or agentic use cases - You have deep understanding of...

- A: `rag` · required · raw_text: "advanced RAG"
- B: `rag` · required · raw_text: "advanced RAG"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_157 - skill `backend-development` (uncertain)

> ...and ensuring the best production integration with back-end and front-end interfaces. • You’ll work on...

- A: `backend-development` · required · raw_text: "back-end"
- B: `backend-development` · required · raw_text: "back-end"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_157 - skill `frontend-development` (uncertain)

> ...ensuring the best production integration with back-end and front-end interfaces. • You’ll work on state-of-the-art GenAI applications...

- A: `frontend-development` · required · raw_text: "front-end interfaces"
- B: `frontend-development` · required · raw_text: "front-end interfaces"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_158 - skill `agents` (uncertain)

> ...of LLMs and experience developing or evaluating LLM-powered /Agentic applications. • Familiarity with version control, testing,...

- A: `agents` · required · raw_text: "LLM-powered /Agentic applications"
- B: `agents` · required · raw_text: "experience developing or evaluating LLM-powered /Agentic applications"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_158 - skill `ai-deployment` (uncertain)

> ...related quantitative field. • Proven real-world experience deploying AI/ML models (internships, co-ops, or full-time roles) (2+...

- A: `ai-deployment` · required · raw_text: "deploying AI/ML models"
- B: `ai-deployment` · required · raw_text: "deploying AI/ML models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_158 - skill `ai-ml` (uncertain)

> ...field. • Proven real-world experience deploying AI/ML models (internships, co-ops, or full-time roles) (2+...

- A: `ai-ml` · required · raw_text: "AI/ML models"
- B: `ai-ml` · required · raw_text: "experience deploying AI/ML models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 79. golden_158 - skill `autogen` (uncertain)

> ...building agentic workflows (e.g., using LangGraph, CrewAI, AutoGen) or chaining LLMs for complex reasoning tasks is highly...

- A: `autogen` · nice_to_have · raw_text: "AutoGen"
- B: `autogen` · nice_to_have · raw_text: "Familiarity with building agentic workflows (e.g., using LangGraph, CrewAI, AutoGen) or chaining LLMs for complex reasoning tasks is highly desirable."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 80. golden_158 - skill `data-science` (uncertain)

> ...software engineering practices. • Experience with the Python data science ecosystem, including tools such as pandas, NumPy, SciPy,...

- A: `data-science` · required · raw_text: "Python data science ecosystem"
- B: `data-science` · required · raw_text: "proficiency in the Data Science ecosystem"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 81. golden_158 - skill `observability` (uncertain)

> ...containerization, and the fundamentals of deploying and monitoring models. Additional experience we value: • Agentic workflows or...

- A: `observability` · required · raw_text: "monitoring models"
- B: `observability` · required · raw_text: "monitoring models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 82. golden_159 - attribute `seniority` (uncertain)

> ...oder eine vergleichbare praktische Qualifikation - Mehrere Jahre Erfahrung damit, Software in Produktion zu bringen, idealerweise...

- A: value="mid" · basis="inferred" · signal="Mehrere Jahre Erfahrung"
- B: value="mid" · basis="inferred" · signal="Mehrere Jahre Erfahrung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 83. golden_159 - skill `llm-orchestration` (uncertain)

> ...(FastAPI) und TypeScript/React - Praktische Erfahrung mit Multi-Agent-Orchestrierung (z. B. LangGraph oder vergleichbare Frameworks), RAG und...

- A: `llm-orchestration` · required · raw_text: "Multi-Agent-Orchestrierung"
- B: `llm-orchestration` · required · raw_text: "Multi-Agent-Orchestrierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 84. golden_159 - skill `llms` (uncertain)

> ...Jahre Erfahrung damit, Software in Produktion zu bringen, idealerweise LLM-Produkte mit echten Nutzern - Sicheres Arbeiten mit Python...

- A: `llms` · nice_to_have · raw_text: "idealerweise LLM-Produkte"
- B: `llms` · nice_to_have · raw_text: "idealerweise LLM-Produkte mit echten Nutzern"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 85. golden_159 - skill `multi-agent-systems` (uncertain)

> ...(FastAPI) und TypeScript/React - Praktische Erfahrung mit Multi-Agent-Orchestrierung (z. B. LangGraph oder vergleichbare Frameworks), RAG und...

- A: `multi-agent-systems` · required · raw_text: "Multi-Agent-Orchestrierung"
- B: `multi-agent-systems` · required · raw_text: "Multi-Agent-Orchestrierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 86. golden_160 - attribute `degree` (uncertain)

> ...learning deployments on AWS, Azure, or GCP</li> <li>Graduate degree in a quantitative discipline (Computer Science, Engineering, Statistics, Operations Research, etc.) or equivalent practical experience</li> <li>Experience communicating and/or teaching...

- A: value="master" · requirement="required" · or_equivalent=true · signal="Graduate degree in a quantitative discipline (Computer Science, Engineering, Statistics, Operations Research, etc.) or equivalent practical experience"
- B: value="master" · requirement="required" · or_equivalent=true · signal="Graduate degree in a quantitative discipline (Computer Science, Engineering, Statistics, Operations Research, etc.) or equivalent practical experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 87. golden_161 - skill `evaluation` (uncertain)

> ...(e.g., PyTorch, TensorFlow) and the full model lifecycle: data curation, training, evaluation, and deployment - Experience with modern computer vision models such as...

- A: `evaluation` · required · raw_text: "data curation, training, evaluation, and deployment"
- B: `evaluation` · required · raw_text: "evaluation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 88. golden_161 - skill `machine-learning` (uncertain)

> ...field — or equivalent practical experience - Minimum of four years of professional experience in machine learning, AI for robotics, or computer vision - Hands-on...

- A: `machine-learning` · required · raw_text: "four years of professional experience in machine learning"
- B: `machine-learning` · required · raw_text: "Solid command of machine learning frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 89. golden_161 - skill `transformers` (uncertain)

> ...segmentation, and pose estimation based on YOLO, SAM, vision transformers, and self-supervised backbones such as DINOv2 - Integrate...

- A: `transformers` · required · raw_text: "vision transformers"
- B: `transformers` · required · raw_text: "vision transformers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 90. golden_162 - attribute `degree` (uncertain)

> AI Builder, Forward Deployed Engineering, Research and Product

- A: value=null · requirement=null · or_equivalent=false · signal=null
- B: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 91. golden_162 - skill `ai-deployment` (uncertain)

> ...- Model-level machine learning understanding and hands-on experience deploying AI to solve real-world problems. - Knowledge of ML...

- A: `ai-deployment` · required · raw_text: "hands-on experience deploying AI"
- B: `ai-deployment` · required · raw_text: "hands-on experience deploying AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 92. golden_162 - skill `model-development` (uncertain)

> ...AI to solve real-world problems. - Knowledge of ML evaluation, training, and problem decomposition, with experience in...

- A: `model-development` · required · raw_text: "ML evaluation, training"
- B: `model-development` · required · raw_text: "ML evaluation, training"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 93. golden_162 - skill `reinforcement-learning` (uncertain)

> ...WE'RE LOOKING FOR - At least 3 years of experience in applied machine learning, reinforcement learning, product engineering, or technical consulting involving...

- A: `reinforcement-learning` · required · raw_text: "applied machine learning, reinforcement learning"
- B: `reinforcement-learning` · required · raw_text: "experience in applied machine learning, reinforcement learning, product engineering, or technical consulting"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 94. golden_163 - skill `access-control` (uncertain)

> ...with enterprise infrastructure requirements, including identity and access management, network isolation, security, monitoring, and...

- A: `access-control` · required · raw_text: "identity and access management"
- B: `access-control` · required · raw_text: "identity and access management"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 95. golden_163 - skill `cybersecurity` (uncertain)

> ...requirements, including identity and access management, network isolation, security, monitoring, and reliability. - Strong Python and Linux...

- A: `cybersecurity` · required · raw_text: "network isolation, security"
- B: `cybersecurity` · required · raw_text: "security"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 96. golden_163 - skill `evaluation` (uncertain)

> ...(e.g., transformers, KV caching, or tool calling) and how to evaluate their outputs. - Familiarity with enterprise infrastructure...

- A: `evaluation` · required · raw_text: "how to evaluate their outputs"
- B: `evaluation` · required · raw_text: "how to evaluate their outputs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 97. golden_149 - attribute `degree` (spot-check)

> Forward-Deployed AI Engineer – AVP

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_150 - attribute `degree` (spot-check)

> Principal Forward Deployed AI Engineers

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_150 - skill `mcp` (spot-check)

> ...contributed to shaping or estimating work commercially - MCP server development and enterprise tool ecosystem integration - Prompt and...

- agreed label: `mcp` · nice_to_have · raw_text: "MCP server development"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_151 - attribute `seniority` (spot-check)

> ...Du bringst sie vom Design bis in den produktiven Betrieb. Als Private AI Architect (w/m/x) entwickelst du sichere, skalierbare und souveräne AI- und...

- agreed label: value="senior" · basis="stated" · signal="Als Private AI Architect (w/m/x)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_151 - skill `cuda` (spot-check)

> ...und AI-Infrastrukturen aus – einschließlich NVIDIA Stack, CUDA, MIG, Model Serving, Quantization, Distributed...

- agreed label: `cuda` · required · raw_text: "CUDA"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_151 - skill `docker` (spot-check)

> ...oder Qwen. - Du bist sicher im Umgang mit Kubernetes, Docker/OpenShift und MLOps/LLMOps und kennst Technologien wie MLflow,...

- agreed label: `docker` · required · raw_text: "Docker/OpenShift"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_151 - skill `kserve` (spot-check)

> ...MLOps/LLMOps und kennst Technologien wie MLflow, Kubeflow, KServe, Ray, vLLM oder Ollama sowie Evaluation, Tracing,...

- agreed label: `kserve` · required · raw_text: "KServe"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_151 - skill `langchain` (spot-check)

> ...Prompt Engineering und Agentic AI sowie Frameworks wie LangChain, LlamaIndex, Haystack oder Semantic Kernel und...

- agreed label: `langchain` · required · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_151 - skill `llamaindex` (spot-check)

> ...Engineering und Agentic AI sowie Frameworks wie LangChain, LlamaIndex, Haystack oder Semantic Kernel und Open-Source-Modelle wie...

- agreed label: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_151 - skill `llms` (spot-check)

> ...Hands-on-Erfahrung mit Private AI und GenAI mit und beherrschst LLMs, RAG, Vector Databases, Prompt Engineering und Agentic AI...

- agreed label: `llms` · required · raw_text: "beherrschst LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_151 - skill `semantic-kernel` (spot-check)

> ...sowie Frameworks wie LangChain, LlamaIndex, Haystack oder Semantic Kernel und Open-Source-Modelle wie Llama, Mistral, DeepSeek oder...

- agreed label: `semantic-kernel` · required · raw_text: "Semantic Kernel"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_151 - skill `vector-databases` (spot-check)

> ...mit Private AI und GenAI mit und beherrschst LLMs, RAG, Vector Databases, Prompt Engineering und Agentic AI sowie Frameworks wie...

- agreed label: `vector-databases` · required · raw_text: "RAG, Vector Databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_151 - skill `vllm` (spot-check)

> ...und kennst Technologien wie MLflow, Kubeflow, KServe, Ray, vLLM oder Ollama sowie Evaluation, Tracing, Monitoring, Drift...

- agreed label: `vllm` · required · raw_text: "vLLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_153 - skill `apis` (spot-check)

> ...with hands-on experience in full-stack development, scripting, APIs, microservices, enterprise integrations, or cloud-native...

- agreed label: `apis` · required · raw_text: "scripting, APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_153 - skill `claude-code` (spot-check)

> ...with the Anthropic API, Claude models, Anthropic Console, Claude Code, or Anthropic implementation guidance. • Completion of...

- agreed label: `claude-code` · nice_to_have · raw_text: "Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_153 - skill `docker` (spot-check)

> ...developer tooling, or product capabilities. • Familiarity with Docker, CI/CD, SQL, Git, infrastructure-as-code, and secure cloud...

- agreed label: `docker` · nice_to_have · raw_text: "Familiarity with Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_153 - skill `embeddings` (spot-check)

> ...concepts, including prompt engineering, context windows, token usage, embeddings, vector search, RAG, tool use/function calling, structured...

- agreed label: `embeddings` · required · raw_text: "token usage, embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_153 - skill `infrastructure-as-code` (spot-check)

> ...capabilities. • Familiarity with Docker, CI/CD, SQL, Git, infrastructure-as-code, and secure cloud deployment practices. Why This Role...

- agreed label: `infrastructure-as-code` · nice_to_have · raw_text: "infrastructure-as-code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_153 - skill `javascript` (spot-check)

> ...or workflow systems in production environments. • Proficiency in JavaScript/TypeScript, Python, or similar programming and scripting...

- agreed label: `javascript` · required · raw_text: "Proficiency in JavaScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_153 - skill `langgraph` (spot-check)

> ...and application frameworks such as LangChain, LangGraph, LlamaIndex, Semantic Kernel, or comparable tools. •...

- agreed label: `langgraph` · nice_to_have · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_153 - skill `llm-orchestration` (spot-check)

> ...and knowledge-grounding patterns. • Familiarity with LLM orchestration and application frameworks such as LangChain, LangGraph, LlamaIndex, Semantic Kernel,...

- agreed label: `llm-orchestration` · nice_to_have · raw_text: "LLM orchestration and application frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_153 - skill `python` (spot-check)

> ...in production environments. • Proficiency in JavaScript/TypeScript, Python, or similar programming and scripting languages. •...

- agreed label: `python` · required · raw_text: "TypeScript, Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_153 - skill `tool-calling` (spot-check)

> ...context windows, token usage, embeddings, vector search, RAG, tool use/function calling, structured outputs, and model evaluation. •...

- agreed label: `tool-calling` · required · raw_text: "RAG, tool use/function calling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_153 - skill `vector-databases` (spot-check)

> ...into enterprise applications and business processes. • Experience with vector databases, embeddings, document ingestion, chunking, retrieval...

- agreed label: `vector-databases` · nice_to_have · raw_text: "Experience with vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_153 - skill `vector-search` (spot-check)

> ...engineering, context windows, token usage, embeddings, vector search, RAG, tool use/function calling, structured outputs, and...

- agreed label: `vector-search` · required · raw_text: "vector search"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_153 - skill `workflow-automation` (spot-check)

> ...experience in software engineering, systems integration, enterprise platforms, workflow automation, or related technical delivery roles. • Strong...

- agreed label: `workflow-automation` · required · raw_text: "enterprise platforms, workflow automation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_154 - attribute `german` (spot-check)

> ...verstehen und gemeinsam passende Lösungen zu entwickeln • Sehr gute Deutsch- und Englischkenntnisse sowie Bereitschaft zu gelegentlichen Reisen runden dein...

- agreed label: value="required" · basis="stated" · signal="Sehr gute Deutsch- und Englischkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_154 - attribute `seniority` (spot-check)

> (Junior) Forward Deployed Engineer – AI Aufgaben Als Forward Deployed Engineer (m/w/d)...

- agreed label: value="junior" · basis="stated" · signal="(Junior) Forward Deployed Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_154 - skill `agents` (spot-check)

> ...von APIs • Erste praktische Erfahrung mit LLMs, RAG, AI Agents oder Tool Calling – idealerweise über konkrete eigene...

- agreed label: `agents` · required · raw_text: "AI Agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_154 - skill `llms` (spot-check)

> ...Erfahrung mit der Entwicklung und Integration von APIs • Erste praktische Erfahrung mit LLMs, RAG, AI Agents oder Tool Calling – idealerweise über...

- agreed label: `llms` · required · raw_text: "Erste praktische Erfahrung mit LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_154 - skill `python` (spot-check)

> ...oder Werkstudierendentätigkeiten • Gute Kenntnisse in Python, Java und/oder TypeScript/JavaScript sowie Erfahrung mit...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_155 - skill `agent-harnesses` (spot-check)

> ...developing a cybersecurity product - Experience building agentic harnesses or multi-agent systems end-to-end - A strong background...

- agreed label: `agent-harnesses` · nice_to_have · raw_text: "agentic harnesses"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_155 - skill `llm-orchestration` (spot-check)

> ...Product Manager - Hands-on experience building agents, LLM orchestration, context engineering, evals, and RAG systems - A bias...

- agreed label: `llm-orchestration` · nice_to_have · raw_text: "LLM orchestration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_155 - skill `llms` (spot-check)

> ...understanding of the concepts and algorithms underlying machine learning and LLMs - You have strong technical coding skills in Python -...

- agreed label: `llms` · required · raw_text: "machine learning and LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_155 - skill `rag` (spot-check)

> ...and front-end interfaces - You have experience tackling advanced RAG, building agentic use cases, or fine-tuning LLMs - You...

- agreed label: `rag` · required · raw_text: "advanced RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_156 - skill `backend-development` (spot-check)

> ...AI or machine learning product implementation with APIs, back-end and front-end interfaces. - You have experience in Fine...

- agreed label: `backend-development` · required · raw_text: "back-end"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_156 - skill `frontend-development` (spot-check)

> ...learning product implementation with APIs, back-end and front-end interfaces. - You have experience in Fine Tuning LLMs, tackling...

- agreed label: `frontend-development` · required · raw_text: "front-end interfaces"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_156 - skill `llms` (spot-check)

> ...deep understanding of concepts and algorithms underlying machine learning and LLMs - You have strong technical coding skills in Python -...

- agreed label: `llms` · required · raw_text: "machine learning and LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_157 - skill `agents` (spot-check)

> ...deep learning with Pytorch • You have experience with agents framework such as Langchain, vector DBs • You hold strong...

- agreed label: `agents` · required · raw_text: "agents framework"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_157 - skill `deep-learning` (spot-check)

> ...coding skills in Python • You have experience with deep learning with Pytorch • You have experience with agents framework such as...

- agreed label: `deep-learning` · required · raw_text: "deep learning with Pytorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_157 - skill `langchain` (spot-check)

> ...with Pytorch • You have experience with agents framework such as Langchain, vector DBs • You hold strong communication skills with...

- agreed label: `langchain` · required · raw_text: "such as Langchain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_157 - skill `llms` (spot-check)

> ...use cases • You have deep understanding of concepts and algorithms underlying machine learning and LLMs • You're experienced with building and deploying LLMs or...

- agreed label: `llms` · required · raw_text: "algorithms underlying machine learning and LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_157 - skill `machine-learning` (spot-check)

> ...RAG or agentic use cases • You have deep understanding of concepts and algorithms underlying machine learning and LLMs • You're experienced with building and deploying...

- agreed label: `machine-learning` · required · raw_text: "concepts and algorithms underlying machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_157 - skill `pytorch` (spot-check)

> ...in Python • You have experience with deep learning with Pytorch • You have experience with agents framework such as...

- agreed label: `pytorch` · required · raw_text: "Pytorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_157 - skill `rag` (spot-check)

> ...You have experience in Fine Tuning LLMs, tackling advanced RAG or agentic use cases • You have deep understanding of...

- agreed label: `rag` · required · raw_text: "advanced RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_158 - attribute `german` (spot-check)

> Job Title AI Engineer / Forward Deployed Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_158 - skill `containerization` (spot-check)

> ...applications. • Familiarity with version control, testing, containerization, and the fundamentals of deploying and monitoring...

- agreed label: `containerization` · required · raw_text: "containerization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_158 - skill `docker` (spot-check)

> ...DevOps & MLOps: Familiarity with development tools (Git, Docker, Terraform), CI/CD pipelines (Jenkins, CircleCI), and...

- agreed label: `docker` · required · raw_text: "Git, Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_158 - skill `gcp` (spot-check)

> ...Experience working within cloud environments, particularly Google Cloud Platform (GCP) and Databricks. Soft Skills & Mindset: • Entrepreneurial...

- agreed label: `gcp` · required · raw_text: "Google Cloud Platform (GCP)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_158 - skill `gemini` (spot-check)

> ...Deep understanding of Large Language Models (GPT, Claude, Llama, Gemini) and Diffusion Models. Familiarity with building agentic...

- agreed label: `gemini` · required · raw_text: "Llama, Gemini"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_158 - skill `jenkins` (spot-check)

> ...with development tools (Git, Docker, Terraform), CI/CD pipelines (Jenkins, CircleCI), and MLOps platforms (Vertex AI, MLflow,...

- agreed label: `jenkins` · required · raw_text: "CI/CD pipelines (Jenkins"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_158 - skill `machine-learning` (spot-check)

> ...Master’s or Bachelor’s degree in Computer Science, Statistics, Machine Learning, or a related quantitative field. • Proven real-world...

- agreed label: `machine-learning` · required · raw_text: "statistics, machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_158 - skill `pandas` (spot-check)

> ...the Python data science ecosystem, including tools such as pandas, NumPy, SciPy, scikit-learn, and TensorFlow or equivalent...

- agreed label: `pandas` · required · raw_text: "pandas"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_158 - skill `statistics` (spot-check)

> ...or full-time roles) (2+ years). Core technical skills: • A strong foundation in statistics, machine learning, and deep learning. • Strong Python and...

- agreed label: `statistics` · required · raw_text: "A strong foundation in statistics"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_158 - skill `terraform` (spot-check)

> ...DevOps & MLOps: Familiarity with development tools (Git, Docker, Terraform), CI/CD pipelines (Jenkins, CircleCI), and MLOps platforms...

- agreed label: `terraform` · required · raw_text: "Docker, Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_158 - skill `vertex-ai` (spot-check)

> ...Terraform), CI/CD pipelines (Jenkins, CircleCI), and MLOps platforms (Vertex AI, MLflow, DVC). • Cloud Platforms: Experience working...

- agreed label: `vertex-ai` · required · raw_text: "MLOps platforms (Vertex AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_159 - attribute `german` (spot-check)

> ...eine Pipeline zu debuggen - Fließendes Englisch, Deutsch ist ein Plus Besonders spannend ist dein Profil, wenn du bereits...

- agreed label: value="nice_to_have" · basis="stated" · signal="Deutsch ist ein Plus"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_159 - skill `devops` (spot-check)

> ...Frameworks), RAG und LLM-Evaluation - Erfahrung mit Cloud, DevOps und MLOps sowie mit APIs und Authentifizierungskonzepten - Eine...

- agreed label: `devops` · required · raw_text: "DevOps und MLOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_159 - skill `typescript` (spot-check)

> ...Nutzern - Sicheres Arbeiten mit Python (FastAPI) und TypeScript/React - Praktische Erfahrung mit...

- agreed label: `typescript` · required · raw_text: "TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 156. golden_160 - skill `aws` (spot-check)

> ...building production-grade machine learning deployments on AWS, Azure, or GCP</li> <li>Graduate degree in a quantitative...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 157. golden_160 - skill `fine-tuning` (spot-check)

> ...including RAG, multi-agent systems, Text2SQL, fine-tuning, etc., with tools such as HuggingFace, LangChain, and...

- agreed label: `fine-tuning` · required · raw_text: "fine-tuning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 158. golden_160 - skill `gcp` (spot-check)

> ...machine learning deployments on AWS, Azure, or GCP</li> <li>Graduate degree in a quantitative discipline...

- agreed label: `gcp` · required · raw_text: "GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 159. golden_160 - skill `llms` (spot-check)

> ...4 years' experience&nbsp;</li> <li>Experience building GenAI applications, including RAG, multi-agent systems, Text2SQL,...

- agreed label: `llms` · required · raw_text: "Experience building GenAI applications"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 160. golden_160 - skill `multi-agent-systems` (spot-check)

> ...building GenAI applications, including RAG, multi-agent systems, Text2SQL, fine-tuning, etc., with tools such as...

- agreed label: `multi-agent-systems` · required · raw_text: "multi-agent systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 161. golden_160 - skill `rag` (spot-check)

> ...building GenAI applications, including RAG, multi-agent systems, Text2SQL, fine-tuning, etc., with...

- agreed label: `rag` · required · raw_text: "RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 162. golden_161 - attribute `seniority` (spot-check)

> ...or a related field — or equivalent practical experience - Minimum of four years of professional experience in machine learning, AI for robotics, or computer...

- agreed label: value="mid" · basis="inferred" · signal="Minimum of four years of professional experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 163. golden_161 - skill `computer-vision` (spot-check)

> ...data curation, training, evaluation, and deployment - Experience with modern computer vision models such as YOLO, SAM, vision transformers, and...

- agreed label: `computer-vision` · required · raw_text: "Experience with modern computer vision models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 164. golden_161 - skill `mlops` (spot-check)

> ...embedded platforms (e.g., Jetson Orin, AGX, Xavier) - Experience with MLOps tooling: experiment tracking, dataset versioning, and continuous...

- agreed label: `mlops` · nice_to_have · raw_text: "Experience with MLOps tooling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 165. golden_161 - skill `quantization` (spot-check)

> ...Experience optimizing inference (e.g., TensorRT, ONNX, quantization) and deploying on NVIDIA embedded platforms (e.g., Jetson...

- agreed label: `quantization` · nice_to_have · raw_text: "quantization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 166. golden_161 - skill `tensorrt` (spot-check)

> ...processing) - Experience optimizing inference (e.g., TensorRT, ONNX, quantization) and deploying on NVIDIA embedded...

- agreed label: `tensorrt` · nice_to_have · raw_text: "TensorRT"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 167. golden_162 - skill `java` (spot-check)

> ...- Software engineering skills and proficiency in Python, Java, C++, TypeScript, or JavaScript. - Experience conducting...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 168. golden_162 - skill `javascript` (spot-check)

> ...skills and proficiency in Python, Java, C++, TypeScript, or JavaScript. - Experience conducting technical discovery with senior...

- agreed label: `javascript` · required · raw_text: "or JavaScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 169. golden_162 - skill `typescript` (spot-check)

> ...engineering skills and proficiency in Python, Java, C++, TypeScript, or JavaScript. - Experience conducting technical...

- agreed label: `typescript` · required · raw_text: "TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 170. golden_163 - skill `cuda` (spot-check)

> ...GPU workloads, including memory management, drivers, CUDA, NCCL, and monitoring. - Model serving with vLLM, SGLang,...

- agreed label: `cuda` · nice_to_have · raw_text: "CUDA"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 171. golden_163 - skill `kubernetes` (spot-check)

> ...debug from logs and metrics. - Practical experience with containers and Kubernetes, including configuration, networking, storage, and...

- agreed label: `kubernetes` · required · raw_text: "containers and Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 172. golden_163 - skill `linux` (spot-check)

> ...monitoring, and reliability. - Strong Python and Linux skills: you can read unfamiliar code, automate a setup, and debug...

- agreed label: `linux` · required · raw_text: "Linux skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 173. golden_163 - skill `nccl` (spot-check)

> ...GPU workloads, including memory management, drivers, CUDA, NCCL, and monitoring. - Model serving with vLLM, SGLang,...

- agreed label: `nccl` · nice_to_have · raw_text: "NCCL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 174. golden_163 - skill `python` (spot-check)

> ...isolation, security, monitoring, and reliability. - Strong Python and Linux skills: you can read unfamiliar code, automate a...

- agreed label: `python` · required · raw_text: "Strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 175. golden_163 - skill `sglang` (spot-check)

> ...CUDA, NCCL, and monitoring. - Model serving with vLLM, SGLang, TensorRT-LLM, or TGI. - Robotics, simulation, synthetic data,...

- agreed label: `sglang` · nice_to_have · raw_text: "SGLang, TensorRT-LLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 176. golden_163 - skill `slurm` (spot-check)

> ...problem to adoption. - Distributed compute such as Ray, Slurm, Spark, or multi-GPU jobs. - NVIDIA GPU workloads,...

- agreed label: `slurm` · nice_to_have · raw_text: "Slurm"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
