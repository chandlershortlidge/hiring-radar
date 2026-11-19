# Review queue - 20261119T140709Z_label

159 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261119T140709Z_label` refuses while any `?` is left, then writes the Goldens.

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

> Real-Time Voice AI Engineer — Equity & In-Office LA

- Loop Voice · Real-Time Voice AI Engineer — Equity & In-Office LA
- Los Angeles · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_095 - scope `in_scope` (in-scope)

> Founding AI Engineer

- Skiffra · Founding AI Engineer
- Los Angeles · en · jsearch · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_096 - scope `in_scope` (in-scope)

> Lead ML Engineer

- Skydance · Lead ML Engineer
- Los Angeles · en · jsearch · 19 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_097 - scope `in_scope` (in-scope)

> Technical Intern — AI Engineering (In Person + Remote)

- Ormidon Labs · Technical Intern — AI Engineering (In Person + Remote)
- Los Angeles · en · jsearch · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_098 - scope `in_scope` (in-scope)

> Remote ML Engineer Intern – Gaming Data & AI

- Riot Games, Inc. · Remote ML Engineer Intern – Gaming Data & AI
- Los Angeles · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_099 - scope `in_scope` (in-scope)

> The Role

- Cogniify · Snowflake Cortex AI Engineer
- Los Angeles · en · jsearch · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_100 - scope `in_scope` (in-scope)

> Machine Learning Engineer, Distributed Data Systems

- OpenAI · Machine Learning Engineer, Distributed Data Systems
- Los Angeles · en · jsearch · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_101 - scope `in_scope` (in-scope)

> Senior AI Engineer

- metropolis · Senior AI Engineer
- Los Angeles · en · greenhouse · 27 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_102 - scope `in_scope` (in-scope)

> Senior Data Engineer, Taxonomy, AI Data Modeling, MLOps, YouTube Business

- Google · Senior Data Engineer, Taxonomy, AI Data Modeling, MLOps, YouTube Business
- Los Angeles · en · jsearch · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_103 - scope `in_scope` (in-scope)

> AI Engineer / Data Scientist, AI Director

- PwC · AI Engineer / Data Scientist, AI Director
- Los Angeles · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_104 - scope `in_scope` (in-scope)

> Client-Facing AI Workflow Engineer

- Fullypowered · Client-Facing AI Workflow Engineer
- Los Angeles · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_105 - scope `in_scope` (in-scope)

> Cyber - AI Engineer - Senior - Consulting

- EY · Cyber - AI Engineer - Senior - Consulting
- Los Angeles · en · jsearch · 19 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_106 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer, Perception - Autonomous Driving

- NVIDIA Corporation · Senior Machine Learning Engineer, Perception - Autonomous Driving
- Los Angeles · en · jsearch · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_107 - scope `in_scope` (in-scope)

> Cortex AI Engineer — Scale AI on the Snowflake Data Cloud

- Cogniify, Inc. · Cortex AI Engineer — Scale AI on the Snowflake Data Cloud
- Los Angeles · en · jsearch · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_108 - scope `in_scope` (in-scope)

> AI Full-Stack Engineer

- Indium · AI Full-Stack Engineer
- Los Angeles · en · jsearch · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_095 - skill `data-privacy-and-security` (disagreement)

> ...in agents) and how to build guardrails against them • Security Mindset: You treat access to enterprise data as part of the design, not an afterthought • Clear communicator with founder-level ownership...

- A: (did not label this)
- B: `data-privacy-and-security` · required · raw_text: "Security Mindset: You treat access to enterprise data as part of the design, not an afterthought"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_096 - attribute `degree` (disagreement)

> ...Dataplex), and with data-product or data-mesh delivery. • Master’s or PhD in Computer Science, Machine Learning or Information Science; publications, patents or open-source contributions in...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s or PhD in Computer Science, Machine Learning or Information Science"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=true · signal="Master’s or PhD in Computer Science, Machine Learning or Information Science"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_099 - attribute `seniority` (disagreement)

> ...is hiring a Snowflake Cortex AI Engineer with 3 to 6 years of experience to build production AI solutions on the Snowflake AI Data...

- A: value="mid" · basis="inferred" · signal="3 to 6 years of experience"
- B: value="senior" · basis="inferred" · signal="support junior team members"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_099 - skill `data-privacy-and-security` (disagreement)

> ...can grow from hundreds to thousands of users. • Apply security, governance and responsible AI controls, including RBAC,...

- A: (did not label this)
- B: `data-privacy-and-security` · required · raw_text: "security"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_101 - skill `ai-deployment` (disagreement)

> ...2+ years of hands-on experience designing, building, and deploying LLM-based or AI-powered applications in production - Exceptional communication and stakeholder management...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying LLM-based or AI-powered applications in production"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_101 - skill `ai-ml` (disagreement)

> ...specifications - Prototype, build, and deploy AI-powered applications and agentic workflows that transform manual business...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI-powered applications"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_101 - skill `vector-search` (disagreement)

> ...role - Experience with vector databases, embeddings, or semantic search Our Stack - Languages + Frameworks: TypeScript, React,...

- A: `vector-search` · nice_to_have · raw_text: "semantic search"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_103 - skill `ai-ml` (disagreement)

> ...Systems, Engineering - Demonstrating director-level AI and data strategy across client engagements - Establishing rigorous AI...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI and data strategy"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_103 - skill `evaluation` (disagreement)

> ...strategy across client engagements - Establishing rigorous AI evaluation standards covering failure modes, bias, drift,...

- A: `evaluation` · nice_to_have · raw_text: "AI evaluation"
- B: `evaluation` · required · raw_text: "AI evaluation standards"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_103 - skill `explainable-ai` (disagreement)

> ...for AI-system behavior, performance, robustness, bias, explainability, and failure modes - Establishing review standards for...

- A: `explainable-ai` · nice_to_have · raw_text: "explainability"
- B: `explainable-ai` · required · raw_text: "explainability"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_103 - skill `hallucination-detection` (disagreement)

> ...evaluation standards covering failure modes, bias, drift, hallucinations, explainability, and guardrails - Setting enterprise...

- A: `hallucination-detection` · nice_to_have · raw_text: "hallucinations"
- B: `hallucination-detection` · required · raw_text: "AI evaluation standards covering failure modes, bias, drift, hallucinations"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_103 - skill `llm-guardrails` (disagreement)

> ...modes, bias, drift, hallucinations, explainability, and guardrails - Setting enterprise architecture trade-offs and...

- A: `llm-guardrails` · nice_to_have · raw_text: "guardrails"
- B: `llm-guardrails` · required · raw_text: "guardrails"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_103 - skill `software-architecture` (disagreement)

> ...hallucinations, explainability, and guardrails - Setting enterprise architecture trade-offs and portfolio-level methods to measure and...

- A: `software-architecture` · nice_to_have · raw_text: "enterprise architecture"
- B: `software-architecture` · required · raw_text: "enterprise architecture"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_105 - skill `software-architecture` (disagreement)

> ...contributing to engineering workshops, live prototyping, architecture reviews, and client demos. • Experience building cyber evaluation...

- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "architecture reviews"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_106 - skill `ai-deployment` (disagreement)

> ...tasks. • AV Production Experience: A history of delivering ML features and models into a production autonomous vehicle stack or a related robotics product. • Performance...

- A: (did not label this)
- B: `ai-deployment` · nice_to_have · raw_text: "delivering ML features and models into a production autonomous vehicle stack"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_106 - skill `computer-vision` (disagreement)

> ...train, and optimize innovative machine learning models for LiDAR/camera perception and multi-sensor fusion (e.g., object...

- A: (did not label this)
- B: `computer-vision` · required · raw_text: "lidar/camera perception"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_106 - skill `model-development` (disagreement)

> ...understanding of the mathematical foundations of ML. • Building and sustaining training and essential metric workflows for large-scale datasets. • Excellent communication and analytical skills....

- A: (did not label this)
- B: `model-development` · required · raw_text: "Building and sustaining training and essential metric workflows for large-scale datasets."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_108 - skill `cloud` (disagreement)

> ...AI/ML capabilities into enterprise solutions, and building scalable cloud-native applications on Azure. Required Skills • Angular (preferred latest...

- A: (did not label this)
- B: `cloud` · required · raw_text: "building scalable cloud-native applications"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 34. golden_108 - skill `data-privacy-and-security` (disagreement)

> ...and data integration experience • Strong understanding of secure healthcare application development AI Experience • Experience building AI-powered...

- A: (did not label this)
- B: `data-privacy-and-security` · required · raw_text: "secure healthcare application development"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 35. golden_108 - skill `software-architecture` (disagreement)

> ...(8-10+ years) • One lead/senior engineer (10+ years with architecture and technical leadership experience) Location • Remote work acceptable with Pacific Time...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "architecture and technical leadership experience"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 36. golden_095 - skill `backend-development` (uncertain)

> ...builder who can move fluidly between prompt engineering, backend systems, and model optimization. You will design the "brain" of...

- A: `backend-development` · required · raw_text: "backend systems"
- B: `backend-development` · required · raw_text: "backend systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 37. golden_095 - skill `llm-guardrails` (uncertain)

> ...API timeouts, "infinite loops" in agents) and how to build guardrails against them • Security Mindset: You treat access to enterprise data...

- A: `llm-guardrails` · required · raw_text: "how to build guardrails against them"
- B: `llm-guardrails` · required · raw_text: "build guardrails against them"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 38. golden_095 - skill `open-source-llms` (uncertain)

> ...experience with Fine-tuning and PEFT (LoRA/QLoRA) to adapt open-weight models for domain-specific tasks • Experience with human-in-the-loop workflows and...

- A: `open-source-llms` · nice_to_have · raw_text: "open-weight models for domain-specific tasks"
- B: `open-source-llms` · nice_to_have · raw_text: "open-weight models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_095 - skill `prompt-engineering` (uncertain)

> ...for a high-leverage builder who can move fluidly between prompt engineering, backend systems, and model optimization. You will design...

- A: `prompt-engineering` · required · raw_text: "prompt engineering"
- B: `prompt-engineering` · required · raw_text: "prompt engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_095 - skill `software-engineering` (uncertain)

> ...For • Systems Engineering: 7+ years of experience and a deep background in building production software. You understand that "AI" is only as good as the...

- A: `software-engineering` · required · raw_text: "a deep background in building production software"
- B: `software-engineering` · required · raw_text: "building production software"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_096 - skill `ai-deployment` (uncertain)

> ...Involving thorough offline and online evaluation. • Experience deploying ML on a major cloud (Google Cloud preferred; AWS or Azure...

- A: `ai-deployment` · required · raw_text: "Experience deploying ML"
- B: `ai-deployment` · required · raw_text: "deploying ML"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_096 - skill `data-modeling` (uncertain)

> ...engineering, including 3+ years building knowledge graphs, semantic data models, or entity-resolution systems in production. • Expertise...

- A: `data-modeling` · required · raw_text: "semantic data models"
- B: `data-modeling` · required · raw_text: "semantic data models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_096 - skill `embeddings` (uncertain)

> ...with graph machine learning is required. This includes working on graph embeddings and link prediction using PyTorch Geometric or DGL....

- A: `embeddings` · required · raw_text: "working on graph embeddings"
- B: `embeddings` · required · raw_text: "graph embeddings"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_096 - skill `gcp` (uncertain)

> ...evaluation. • Experience deploying ML on a major cloud (Google Cloud preferred; AWS or Azure acceptable) with MLOps practices such as...

- A: `gcp` · nice_to_have · raw_text: "Google Cloud preferred"
- B: `gcp` · nice_to_have · raw_text: "Google Cloud preferred"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_096 - skill `knowledge-graphs` (uncertain)

> ...machine learning, data, or software engineering, including 3+ years building knowledge graphs, semantic data models, or entity-resolution systems in...

- A: `knowledge-graphs` · required · raw_text: "3+ years building knowledge graphs"
- B: `knowledge-graphs` · required · raw_text: "building knowledge graphs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_096 - skill `machine-learning` (uncertain)

> ...and model capabilities. Required Qualifications • 8+ years of experience in machine learning, data, or software engineering, including 3+ years...

- A: `machine-learning` · required · raw_text: "8+ years of experience in machine learning"
- B: `machine-learning` · required · raw_text: "Hands-on experience with graph machine learning is required."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_096 - skill `nlp` (uncertain)

> ...patents or open-source contributions in knowledge graphs, NLP or graph ML. • Experience with Wikidata / Wikibase, Palantir Foundry...

- A: `nlp` · nice_to_have · raw_text: "NLP or graph ML"
- B: `nlp` · nice_to_have · raw_text: "NLP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_096 - skill `rag` (uncertain)

> ...avails) or experience with rights-management platforms. • Experience with GraphRAG, including hybrid retrieval (vector search plus graph...

- A: `rag` · nice_to_have · raw_text: "Experience with GraphRAG"
- B: `rag` · nice_to_have · raw_text: "GraphRAG"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_096 - skill `structured-data-extraction` (uncertain)

> ...matching, Splink, Zingg, Senzing) and LLM-based information extraction from documents. • Hands-on experience with graph machine learning is...

- A: `structured-data-extraction` · required · raw_text: "information extraction from documents"
- B: `structured-data-extraction` · required · raw_text: "information extraction from documents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_097 - skill `ai-ml` (uncertain)

> ...with Python and SQL, plus foundational knowledge of machine learning, AI models, statistical analysis, and database design. • Preferred:...

- A: `ai-ml` · required · raw_text: "machine learning, AI models"
- B: `ai-ml` · required · raw_text: "AI models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_099 - skill `agents` (uncertain)

> ...work with Streamlit in Snowflake, Snowflake Native Apps or external agent frameworks is a plus. • Experience with data in industries common in Los...

- A: `agents` · nice_to_have · raw_text: "external agent frameworks is a plus"
- B: `agents` · nice_to_have · raw_text: "Experience building or scaling production agentic AI systems, including evaluations, guardrails, cost and latency tuning and multi-user concurrency, is a plus."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_099 - skill `ai-ml` (uncertain)

> ...engineering, analytics engineering, data architecture or AI/ML delivery. • Production experience with Snowflake Cortex, including...

- A: `ai-ml` · required · raw_text: "AI/ML delivery"
- B: `ai-ml` · required · raw_text: "AI/ML delivery"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_099 - skill `llm-guardrails` (uncertain)

> ...or scaling production agentic AI systems, including evaluations, guardrails, cost and latency tuning and multi-user concurrency, is a...

- A: `llm-guardrails` · nice_to_have · raw_text: "evaluations, guardrails"
- B: `llm-guardrails` · nice_to_have · raw_text: "Experience building or scaling production agentic AI systems, including evaluations, guardrails, cost and latency tuning and multi-user concurrency, is a plus."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_100 - skill `software-engineering` (uncertain)

> ...building and maintaining reliable systems. • Demonstrate excellent software engineering fundamentals and organizational skills. • Are comfortable with...

- A: `software-engineering` · required · raw_text: "excellent software engineering fundamentals"
- B: `software-engineering` · required · raw_text: "software engineering fundamentals"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_101 - skill `agents` (uncertain)

> ...(OpenAI, Anthropic, or similar), prompt engineering, and agentic patterns including function calling, multi-step reasoning, and tool...

- A: `agents` · required · raw_text: "agentic patterns"
- B: `agents` · required · raw_text: "agentic patterns"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_101 - skill `observability` (uncertain)

> ...control: Git & GitHub - AI Tooling: Copilot on GitHub - Observability: Datadog 4 Days in Office: Metropolis values in-person...

- A: `observability` · required · raw_text: "Observability: Datadog"
- B: `observability` · required · raw_text: "Observability"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_102 - attribute `degree` (uncertain)

> ...learning data pipelines. Preferred qualifications: • Master's degree in Computer Science, Engineering, Statistics, Mathematics, or a related quantitative discipline or equivalent professional experience. • Experience designing ontologies, versioned taxonomies,...

- A: value="master" · requirement="nice_to_have" · or_equivalent=true · signal="Master's degree in Computer Science, Engineering, Statistics, Mathematics, or a related quantitative discipline or equivalent professional experience"
- B: value="master" · requirement="nice_to_have" · or_equivalent=true · signal="Master's degree in Computer Science, Engineering, Statistics, Mathematics, or a related quantitative discipline or equivalent professional experience."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_102 - skill `apis` (uncertain)

> ...evaluation golden sets, and AI coding tools. • Experience building APIs or architecting data models from the ground up. About The...

- A: `apis` · nice_to_have · raw_text: "building APIs"
- B: `apis` · nice_to_have · raw_text: "building APIs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_102 - skill `data-modeling` (uncertain)

> Senior Data Engineer, Taxonomy, AI Data Modeling, MLOps, YouTube Business In most instances, this position...

- A: `data-modeling` · required · raw_text: "data modeling"
- B: `data-modeling` · required · raw_text: "data modeling"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_102 - skill `data-pipelines` (uncertain)

> ...data engineering, data modeling, or building and operating production ETL/ELT pipelines and distributed data warehouses. • 3 years of experience...

- A: `data-pipelines` · required · raw_text: "production ETL/ELT pipelines"
- B: `data-pipelines` · required · raw_text: "ETL/ELT pipelines"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_103 - attribute `seniority` (uncertain)

> AI Engineer / Data Scientist, AI Director The Opportunity As part of the AI Engineering team within...

- A: value="senior" · basis="stated" · signal="AI Director"
- B: value="senior" · basis="stated" · signal="AI Director"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_105 - skill `agent-architecture` (uncertain)

> ...Practical understanding of frontier AI models, LLMs, agentic architectures, and retrieval-augmented generation for cybersecurity. •...

- A: `agent-architecture` · required · raw_text: "agentic architectures"
- B: `agent-architecture` · required · raw_text: "agentic architectures"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_105 - skill `ai-deployment` (uncertain)

> ...for AI services • Cloud engineering and secure AI deployment on AWS, Azure, or GCP • API integration with SIEM, SOAR,...

- A: `ai-deployment` · required · raw_text: "secure AI deployment"
- B: `ai-deployment` · required · raw_text: "deploy production AI applications"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_105 - skill `aws` (uncertain)

> ...services • Cloud engineering and secure AI deployment on AWS, Azure, or GCP • API integration with SIEM, SOAR, EDR,...

- A: `aws` · required · raw_text: "AWS"
- B: `aws` · required · raw_text: "AWS"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_105 - skill `azure` (uncertain)

> ...Cloud engineering and secure AI deployment on AWS, Azure, or GCP • API integration with SIEM, SOAR, EDR,...

- A: `azure` · required · raw_text: "Azure"
- B: `azure` · required · raw_text: "Azure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_105 - skill `ci-cd` (uncertain)

> ...detection engineering, or incident response automation • DevSecOps, CI/CD, containers, and infrastructure-as-code for AI services •...

- A: `ci-cd` · required · raw_text: "DevSecOps, CI/CD"
- B: `ci-cd` · required · raw_text: "CI/CD, containers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_105 - skill `cloud` (uncertain)

> ...containers, and infrastructure-as-code for AI services • Cloud engineering and secure AI deployment on AWS, Azure, or GCP • API...

- A: `cloud` · required · raw_text: "Cloud engineering"
- B: `cloud` · required · raw_text: "Cloud engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_105 - skill `cybersecurity` (uncertain)

> ...We Look For We seek hands-on engineers who pair cybersecurity knowledge with practical AI skills. You can build with client teams,...

- A: `cybersecurity` · required · raw_text: "cybersecurity knowledge"
- B: `cybersecurity` · required · raw_text: "retrieval-augmented generation for cybersecurity"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_105 - skill `data-privacy-and-security` (uncertain)

> ...of security architecture, identity and access management, data protection, and secure AI operations. • Experience contributing to...

- A: `data-privacy-and-security` · required · raw_text: "data protection"
- B: `data-privacy-and-security` · required · raw_text: "data protection"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_105 - skill `gcp` (uncertain)

> ...engineering and secure AI deployment on AWS, Azure, or GCP • API integration with SIEM, SOAR, EDR, vulnerability...

- A: `gcp` · required · raw_text: "GCP"
- B: `gcp` · required · raw_text: "GCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_105 - skill `llm-guardrails` (uncertain)

> ...of prompt injection, data leakage, unsafe tool use, and safeguards informed by OWASP Top 10 for LLMs and MITRE ATLAS. • Working knowledge of security...

- A: `llm-guardrails` · required · raw_text: "safeguards informed by OWASP Top 10 for LLMs"
- B: `llm-guardrails` · required · raw_text: "safeguards informed by OWASP Top 10 for LLMs and MITRE ATLAS"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_106 - skill `inference-optimization` (uncertain)

> ...product. • Performance Optimization: Experience with model optimization for real-time inference on embedded or automotive platforms (e.g., using...

- A: `inference-optimization` · nice_to_have · raw_text: "model optimization for real-time inference"
- B: `inference-optimization` · nice_to_have · raw_text: "model optimization for real-time inference"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_108 - skill `ai-ml` (uncertain)

> ...designing and developing AI-powered applications, integrating AI/ML capabilities into enterprise solutions, and building scalable...

- A: `ai-ml` · required · raw_text: "integrating AI/ML capabilities"
- B: `ai-ml` · required · raw_text: "integrating AI/ML capabilities"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_108 - skill `angular` (uncertain)

> ...cloud-native applications on Azure. Required Skills • Angular (preferred latest versions) for frontend application development • Java / Spring Boot...

- A: `angular` · required · raw_text: "Angular (preferred latest versions)"
- B: `angular` · required · raw_text: "Angular"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_108 - skill `apis` (uncertain)

> ...development • Java / Spring Boot for middleware and API development • Microsoft Azure (App Services, Functions, API...

- A: `apis` · required · raw_text: "API development"
- B: `apis` · required · raw_text: "API development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_108 - skill `conversational-ai` (uncertain)

> ...and agent-based architectures • Experience implementing conversational assistants, summarization, document intelligence, and knowledge...

- A: `conversational-ai` · required · raw_text: "conversational assistants"
- B: `conversational-ai` · required · raw_text: "conversational assistants"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_108 - skill `frontend-development` (uncertain)

> ...Skills • Angular (preferred latest versions) for frontend application development • Java / Spring Boot for middleware and API development •...

- A: `frontend-development` · required · raw_text: "frontend application development"
- B: `frontend-development` · required · raw_text: "frontend application development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_108 - skill `full-stack-development` (uncertain)

> ...We are seeking a highly skilled AI Engineer with strong Full Stack development expertise in Java, Azure, and Angular to join our growing team. The...

- A: `full-stack-development` · required · raw_text: "Full Stack development expertise"
- B: `full-stack-development` · required · raw_text: "Full Stack development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 79. golden_108 - skill `openai-api` (uncertain)

> ...applications and workflow automation • Familiarity with Azure OpenAI and agent-based architectures • Experience implementing...

- A: `openai-api` · required · raw_text: "Azure OpenAI"
- B: `openai-api` · required · raw_text: "Azure OpenAI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 80. golden_094 - attribute `degree` (spot-check)

> Real-Time Voice AI Engineer — Equity & In-Office LA

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 81. golden_095 - attribute `degree` (spot-check)

> Founding AI Engineer

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 82. golden_095 - skill `langgraph` (spot-check)

> ...complex, multi-step workflows using frameworks such as LangGraph, LlamaIndex or PydanticAI • Hands-on experience with...

- agreed label: `langgraph` · nice_to_have · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 83. golden_095 - skill `llms` (spot-check)

> ...context window management • Production LLM Experience: 2+ years shipping LLM-based products to real users in production • Python Power-User: You are...

- agreed label: `llms` · required · raw_text: "2+ years shipping LLM-based products"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_095 - skill `pydanticai` (spot-check)

> ...using frameworks such as LangGraph, LlamaIndex or PydanticAI • Hands-on experience with Fine-tuning and PEFT...

- agreed label: `pydanticai` · nice_to_have · raw_text: "PydanticAI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_095 - skill `tool-calling` (spot-check)

> ...the transformer-based stack: embeddings, vector databases, tool-calling, and context window management • Production LLM...

- agreed label: `tool-calling` · required · raw_text: "tool-calling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_095 - skill `vector-databases` (spot-check)

> ...experience with the transformer-based stack: embeddings, vector databases, tool-calling, and context window management • Production...

- agreed label: `vector-databases` · required · raw_text: "vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_096 - skill `agents` (spot-check)

> ...search plus graph traversal) and connecting knowledge to agent frameworks (e.g., Google ADK, LangGraph) via MCP. • Experience with...

- agreed label: `agents` · nice_to_have · raw_text: "agent frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_096 - skill `evaluation` (spot-check)

> ...classical predictive modeling is also needed. Involving thorough offline and online evaluation. • Experience deploying ML on a major cloud (Google Cloud...

- agreed label: `evaluation` · required · raw_text: "thorough offline and online evaluation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_096 - skill `google-adk` (spot-check)

> ...and connecting knowledge to agent frameworks (e.g., Google ADK, LangGraph) via MCP. • Experience with master data...

- agreed label: `google-adk` · nice_to_have · raw_text: "Google ADK"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_096 - skill `langgraph` (spot-check)

> ...knowledge to agent frameworks (e.g., Google ADK, LangGraph) via MCP. • Experience with master data management and...

- agreed label: `langgraph` · nice_to_have · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_096 - skill `llms` (spot-check)

> ...or embedding-based matching, Splink, Zingg, Senzing) and LLM-based information extraction from documents. • Hands-on experience with graph machine learning is...

- agreed label: `llms` · required · raw_text: "LLM-based information extraction from documents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_096 - skill `mlops` (spot-check)

> ...(Google Cloud preferred; AWS or Azure acceptable) with MLOps practices such as CI/CD pipelines, model registry, and monitoring. •...

- agreed label: `mlops` · required · raw_text: "MLOps practices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_096 - skill `python` (spot-check)

> ...data models, or entity-resolution systems in production. • Expertise in Python and SQL, and proficiency with ML frameworks (PyTorch or...

- agreed label: `python` · required · raw_text: "Expertise in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_096 - skill `pytorch` (spot-check)

> ...in Python and SQL, and proficiency with ML frameworks (PyTorch or TensorFlow, plus scikit-learn). • Hands-on experience with at least...

- agreed label: `pytorch` · required · raw_text: "PyTorch or TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_096 - skill `tensorflow` (spot-check)

> ...and SQL, and proficiency with ML frameworks (PyTorch or TensorFlow, plus scikit-learn). • Hands-on experience with at least one graph database...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow, plus scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_097 - attribute `degree` (spot-check)

> Technical Intern — AI Engineering (In Person + Remote)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_097 - attribute `german` (spot-check)

> Technical Intern — AI Engineering (In Person + Remote)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_097 - skill `apache-spark` (spot-check)

> ...C, R, SAS, VBA, Bash (Unix shell), Talend, linked data, Spark implementation, and machine learning/AI-based analysis. • Interest in...

- agreed label: `apache-spark` · nice_to_have · raw_text: "Spark implementation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_097 - skill `bash` (spot-check)

> ...design. • Preferred: Exposure to Java, C, R, SAS, VBA, Bash (Unix shell), Talend, linked data, Spark implementation, and machine...

- agreed label: `bash` · nice_to_have · raw_text: "Bash (Unix shell)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_097 - skill `java` (spot-check)

> ...AI models, statistical analysis, and database design. • Preferred: Exposure to Java, C, R, SAS, VBA, Bash (Unix shell), Talend, linked data,...

- agreed label: `java` · nice_to_have · raw_text: "Preferred: Exposure to Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_099 - attribute `german` (spot-check)

> The Role

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_099 - skill `evaluation` (spot-check)

> ...of RAG, embeddings, text-to-SQL, prompt engineering, and evaluation and observability practices. • Strong SQL and Python skills. • Hands-on Snowflake...

- agreed label: `evaluation` · required · raw_text: "evaluation and observability practices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_099 - skill `prompt-engineering` (spot-check)

> ...Document AI, Snowpark, RAG, embeddings, text-to-SQL, prompt engineering, LLM evaluation, SQL and Python. What You Will Do •...

- agreed label: `prompt-engineering` · required · raw_text: "prompt engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_099 - skill `streamlit` (spot-check)

> ...multi-user concurrency, is a plus. • Hands-on work with Streamlit in Snowflake, Snowflake Native Apps or external agent frameworks is a...

- agreed label: `streamlit` · nice_to_have · raw_text: "Streamlit in Snowflake"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_100 - attribute `degree` (spot-check)

> Machine Learning Engineer, Distributed Data Systems

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_100 - attribute `german` (spot-check)

> Machine Learning Engineer, Distributed Data Systems

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_100 - attribute `seniority` (spot-check)

> Machine Learning Engineer, Distributed Data Systems

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_100 - skill `distributed-systems` (spot-check)

> ...looking for engineers who are detail-oriented, have strong experience with distributed systems, and excel at building reliable infrastructure in...

- agreed label: `distributed-systems` · required · raw_text: "strong experience with distributed systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_101 - attribute `seniority` (spot-check)

> Senior AI Engineer Who we are The real world is the next frontier, and at...

- agreed label: value="senior" · basis="stated" · signal="Senior AI Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_101 - skill `airflow` (spot-check)

> ...Experience with workflow orchestration tools (Airflow, Prefect, or similar) and cloud infrastructure (AWS) -...

- agreed label: `airflow` · required · raw_text: "Airflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_101 - skill `apis` (spot-check)

> ...Strong Python skills to write clean, maintainable code and build APIs, data pipelines, and backend services - Practical...

- agreed label: `apis` · required · raw_text: "build APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_101 - skill `data-pipelines` (spot-check)

> ...skills to write clean, maintainable code and build APIs, data pipelines, and backend services - Practical experience with LLM APIs (OpenAI,...

- agreed label: `data-pipelines` · required · raw_text: "data pipelines, and backend services"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_101 - skill `embeddings` (spot-check)

> ...technical role - Experience with vector databases, embeddings, or semantic search Our Stack - Languages + Frameworks:...

- agreed label: `embeddings` · nice_to_have · raw_text: "embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_101 - skill `git` (spot-check)

> ...Datastores: MySQL, PostgreSQL, Snowflake - Cloud: AWS - Version control: Git & GitHub - AI Tooling: Copilot on GitHub - Observability:...

- agreed label: `git` · required · raw_text: "Version control: Git & GitHub"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_101 - skill `github-copilot` (spot-check)

> ...Cloud: AWS - Version control: Git & GitHub - AI Tooling: Copilot on GitHub - Observability: Datadog 4 Days in Office: Metropolis...

- agreed label: `github-copilot` · required · raw_text: "Copilot on GitHub"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_101 - skill `openai-api` (spot-check)

> ...backend services - Practical experience with LLM APIs (OpenAI, Anthropic, or similar), prompt engineering, and agentic...

- agreed label: `openai-api` · required · raw_text: "OpenAI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_101 - skill `postgresql` (spot-check)

> ...Scala (principally), Java (limited) - Datastores: MySQL, PostgreSQL, Snowflake - Cloud: AWS - Version control: Git &...

- agreed label: `postgresql` · required · raw_text: "PostgreSQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_101 - skill `react` (spot-check)

> ...search Our Stack - Languages + Frameworks: TypeScript, React, Scala (principally), Java (limited) - Datastores: MySQL,...

- agreed label: `react` · required · raw_text: "React"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_101 - skill `scala` (spot-check)

> ...Stack - Languages + Frameworks: TypeScript, React, Scala (principally), Java (limited) - Datastores: MySQL, PostgreSQL,...

- agreed label: `scala` · required · raw_text: "Scala (principally)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_101 - skill `snowflake` (spot-check)

> ...fundamentals including SQL, data transformation, and cloud data warehouses such as Snowflake - Experience with workflow orchestration tools...

- agreed label: `snowflake` · required · raw_text: "cloud data warehouses such as Snowflake"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_101 - skill `sql` (spot-check)

> ...Familiarity with data engineering fundamentals including SQL, data transformation, and cloud data warehouses such as...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_102 - attribute `seniority` (spot-check)

> Senior Data Engineer, Taxonomy, AI Data Modeling, MLOps, YouTube Business In...

- agreed label: value="senior" · basis="stated" · signal="Senior Data Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_102 - skill `embeddings` (spot-check)

> ...optimizing ML vs. LLM compute unit economics using vector embeddings, lightweight classifiers, evaluation golden sets, and AI...

- agreed label: `embeddings` · nice_to_have · raw_text: "vector embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_102 - skill `llms` (spot-check)

> ...image, or video datasets. • Experience optimizing ML vs. LLM compute unit economics using vector embeddings, lightweight classifiers,...

- agreed label: `llms` · nice_to_have · raw_text: "LLM compute unit economics"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_102 - skill `machine-learning` (spot-check)

> ...text classification, natural language processing (NLP), or machine learning data pipelines. Preferred qualifications: • Master's degree in Computer...

- agreed label: `machine-learning` · required · raw_text: "machine learning data pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_102 - skill `python` (spot-check)

> ...3 years of experience writing production code in Python or a general-purpose programming language, and with SQL...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_103 - attribute `degree` (spot-check)

> ...and professional conduct expectations What You Must Have - At least a Bachelor's degree - At least 8 years of experience What Sets You Apart -...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="At least a Bachelor's degree"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_104 - attribute `seniority` (spot-check)

> Client-Facing AI Workflow Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_105 - attribute `degree` (spot-check)

> ...capabilities. To Qualify for the Role, You Must Have • A bachelor's degree in Cybersecurity, Computer Science, Information Systems, Engineering, or a related field and 3–5 years of relevant experience, including hands-on...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="A bachelor's degree in Cybersecurity, Computer Science, Information Systems, Engineering, or a related field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_105 - attribute `german` (spot-check)

> Cyber - AI Engineer - Senior - Consulting

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_105 - attribute `seniority` (spot-check)

> ...world. The Opportunity As a Cyber AI Engineer at the Senior Consultant level in EY's Cyber practice, you will work as a...

- agreed label: value="senior" · basis="stated" · signal="Senior Consultant level"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_105 - skill `ai-ml` (spot-check)

> ...software engineering and experience building or deploying AI/ML solutions. • Proficiency in Python, APIs, Git, automated testing,...

- agreed label: `ai-ml` · required · raw_text: "AI/ML solutions"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_105 - skill `apis` (spot-check)

> ...or deploying AI/ML solutions. • Proficiency in Python, APIs, Git, automated testing, and production delivery, plus...

- agreed label: `apis` · required · raw_text: "APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_105 - skill `containerization` (spot-check)

> ...or incident response automation • DevSecOps, CI/CD, containers, and infrastructure-as-code for AI services • Cloud...

- agreed label: `containerization` · required · raw_text: "containers"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_105 - skill `evaluation` (spot-check)

> ...building model integrations, tool-calling agents, evaluation harnesses, and secure security-platform connections. • Ability to...

- agreed label: `evaluation` · required · raw_text: "evaluation harnesses"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_105 - skill `git` (spot-check)

> ...deploying AI/ML solutions. • Proficiency in Python, APIs, Git, automated testing, and production delivery, plus...

- agreed label: `git` · required · raw_text: "Git"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_105 - skill `llm-orchestration` (spot-check)

> ...selection, adaptation, and evaluation. • Experience with agent orchestration, model serving, LLM observability, and CI/CD evaluation...

- agreed label: `llm-orchestration` · nice_to_have · raw_text: "agent orchestration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_105 - skill `llms` (spot-check)

> ...Success • Practical understanding of frontier AI models, LLMs, agentic architectures, and retrieval-augmented generation...

- agreed label: `llms` · required · raw_text: "LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_105 - skill `model-selection` (spot-check)

> ...Experience with frontier model providers or cyber-focused model selection, adaptation, and evaluation. • Experience with agent...

- agreed label: `model-selection` · nice_to_have · raw_text: "model selection"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_105 - skill `model-serving` (spot-check)

> ...and evaluation. • Experience with agent orchestration, model serving, LLM observability, and CI/CD evaluation gates. •...

- agreed label: `model-serving` · nice_to_have · raw_text: "model serving"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_105 - skill `python` (spot-check)

> ...building or deploying AI/ML solutions. • Proficiency in Python, APIs, Git, automated testing, and production delivery,...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_105 - skill `rag` (spot-check)

> ...of frontier AI models, LLMs, agentic architectures, and retrieval-augmented generation for cybersecurity. • Ability to work with engagement...

- agreed label: `rag` · required · raw_text: "retrieval-augmented generation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_106 - attribute `german` (spot-check)

> Senior Machine Learning Engineer, Perception - Autonomous Driving

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_106 - attribute `seniority` (spot-check)

> Senior Machine Learning Engineer, Perception - Autonomous Driving Intelligent machines...

- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_106 - skill `cpp` (spot-check)

> ...machine learning to address real-world problems. • Strong C++ and Python programming and debugging skills with...

- agreed label: `cpp` · required · raw_text: "Strong C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_106 - skill `pytorch` (spot-check)

> ...fields. • Experience with deep learning frameworks (e.g., PyTorch, Tensor Flow) and a strong understanding of the...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_106 - skill `tensorflow` (spot-check)

> ...Experience with deep learning frameworks (e.g., PyTorch, Tensor Flow) and a strong understanding of the mathematical...

- agreed label: `tensorflow` · required · raw_text: "Tensor Flow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_106 - skill `transformers` (spot-check)

> ...environment. • Advanced Model Knowledge: Familiarity with modern network architectures like Transformers and their application to visual recognition tasks. • AV...

- agreed label: `transformers` · nice_to_have · raw_text: "modern network architectures like Transformers"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_107 - attribute `degree` (spot-check)

> Cortex AI Engineer — Scale AI on the Snowflake Data Cloud

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_107 - attribute `seniority` (spot-check)

> Cortex AI Engineer — Scale AI on the Snowflake Data Cloud

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_107 - skill `rag` (spot-check)

> ...and experience with Cortex components, Semantic Views, and RAG-based workflows.

- agreed label: `rag` · required · raw_text: "RAG-based workflows"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_107 - skill `sql` (spot-check)

> ...The role blends data engineering with AI, requiring strong SQL and Python skills and experience with Cortex components,...

- agreed label: `sql` · required · raw_text: "strong SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_108 - attribute `seniority` (spot-check)

> ...testing, and production deployment Experience Level • One senior engineer (8-10+ years) • One lead/senior engineer (10+ years with architecture...

- agreed label: value="senior" · basis="stated" · signal="One senior engineer (8-10+ years)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_108 - skill `api-design` (spot-check)

> ...Functions, API Management, Storage, Azure AI Services) • REST API design and integration • Azure DevOps, Git, CI/CD pipelines • SQL...

- agreed label: `api-design` · required · raw_text: "REST API design"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_108 - skill `azure` (spot-check)

> ...Java / Spring Boot for middleware and API development • Microsoft Azure (App Services, Functions, API Management, Storage, Azure...

- agreed label: `azure` · required · raw_text: "Microsoft Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 156. golden_108 - skill `azure-devops` (spot-check)

> ...Azure AI Services) • REST API design and integration • Azure DevOps, Git, CI/CD pipelines • SQL and data integration...

- agreed label: `azure-devops` · required · raw_text: "Azure DevOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 157. golden_108 - skill `git` (spot-check)

> ...Indium Software Indium Software is a fast-growing digital engineering and technology services company specializing...

- agreed label: `git` · required · raw_text: "Git"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 158. golden_108 - skill `java` (spot-check)

> ...latest versions) for frontend application development • Java / Spring Boot for middleware and API development • Microsoft Azure (App...

- agreed label: `java` · required · raw_text: "Java / Spring Boot"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 159. golden_108 - skill `spring-boot` (spot-check)

> ...latest versions) for frontend application development • Java / Spring Boot for middleware and API development • Microsoft Azure (App...

- agreed label: `spring-boot` · required · raw_text: "Java / Spring Boot"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
