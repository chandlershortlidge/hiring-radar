# Review queue - 20261103T224145Z_label

157 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261103T224145Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 246 accepted labels,
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

## 1. golden_049 - scope `in_scope` (in-scope)

> AI Engineer (LLM) - Remote

- dexter health · AI Engineer (LLM) - Remote
- Berlin · en · screenshot · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_050 - scope `in_scope` (in-scope)

> (Junior) AI Engineer (m/f/d)

- ZDF Sparks GmbH · (Junior) AI Engineer (m/f/d)
- Berlin · en · screenshot · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_051 - scope `in_scope` (in-scope)

> Staff Forward Deployed Engineer – AI-Native Software Development

- jetbrains · Staff Forward Deployed Engineer – AI-Native Software Development
- Berlin · en · arbeitnow · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_052 - scope `in_scope` (in-scope)

> Staff Machine Learning Engineer, LLM Inference Optimization

- Nebius · Staff Machine Learning Engineer, LLM Inference Optimization
- Berlin · en · greenhouse · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_053 - scope `in_scope` (in-scope)

> NTT DATA Deutschland SE: Senior AI Engineer (w/m/x)

- NTT DATA Deutschland SE · NTT DATA Deutschland SE: Senior AI Engineer (w/m/x)
- Berlin · de · arbeitsagentur · 31 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_054 - scope `in_scope` (in-scope)

> AI Integration Engineer (m/f/d)

- EGYM · AI Integration Engineer (m/f/d)
- Berlin · en · screenshot · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_055 - scope `in_scope` (in-scope)

> About the Position

- Bluefish · Staff AI Engineer
- Berlin · en · greenhouse · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_056 - scope `in_scope` (in-scope)

> Senior AI Engineer - Agentic Software Development (w/m/d)

- BWI GmbH · Senior AI Engineer - Agentic Software Development (w/m/d)
- Berlin · en · arbeitsagentur · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_057 - scope `in_scope` (in-scope)

> Senior Applied AI Engineer, AI Platform (f/m/d)

- Bunch · Senior Applied AI Engineer, AI Platform (f/m/d)
- Berlin · en · ashby · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_058 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer

- Takeaway · Senior Machine Learning Engineer
- Berlin · en · jsearch · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_059 - scope `in_scope` (in-scope)

> Senior GenAI Engineer (m/w/d)

- Abacus Medicine Group · Senior GenAI Engineer (m/w/d)
- Berlin · en · url · 20 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_060 - scope `in_scope` (in-scope)

> Fullstack Software Engineer Tech & AI (m/w/d)

- GSK Stockmann · Fullstack Software Engineer Tech & AI (m/w/d)
- Berlin · de · arbeitsagentur · 20 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_061 - scope `in_scope` (in-scope)

> AI Solutions Engineer (m/w/d) mit Fokus auf AWS/Bedrock

- Birds on Mars · AI Solutions Engineer (m/w/d) mit Fokus auf AWS/Bedrock
- Berlin · de · url · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_062 - scope `in_scope` (in-scope)

> PreSales Engineer Data & AI (m/w/d),Bielefeld,Berlin

- OEDIV · PreSales Engineer Data & AI (m/w/d),Bielefeld,Berlin
- Berlin · de · arbeitsagentur · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_063 - scope `in_scope` (in-scope)

> Software Engineer, Voice AI / Backend

- Clera · Software Engineer, Voice AI / Backend
- Berlin · en · ashby · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_049 - skill `ai-deployment` (disagreement)

> ...test, validate, and improve AI outputs • Experience integrating AI workflows into production systems • Strong debugging instincts across application logic,...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "integrating AI workflows into production systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_049 - skill `ai-ml` (disagreement)

> ...in Python or a comparable backend language • Experience building AI-powered product features or LLM-based workflows • Ability to turn ambiguous product...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "building AI-powered product features"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_050 - skill `software-architecture` (disagreement)

> ...learning how to translate business problems into technical architectures. • Language: English (Must-have): Excellent communication...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "technical architectures"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_051 - skill `software-engineering` (disagreement)

> ...partners to transform their customers’ AI-native software development lifecycle.</p> <h2><strong>About the role</strong></h2> <p>As a...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software development lifecycle"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_052 - skill `ai-deployment` (disagreement)

> ...and PyTorch engineering skills. - Hands-on experience deploying or optimizing LLM, VLM, or high-throughput transformer inference systems. - Practical knowledge of at least one modern inference...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying or optimizing LLM, VLM, or high-throughput transformer inference systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_052 - skill `model-serving` (disagreement)

> ...decoding, KV-cache optimization, engine selection, or long-context serving. - Create reusable evaluation, benchmarking, and rollout...

- A: (did not label this)
- B: `model-serving` · required · raw_text: "long-context serving"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_057 - skill `software-engineering` (disagreement)

> ...AI Platform. ABOUT YOU - Experience: 5+ years building production software, including at least one agent or LLM-powered capability...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "building production software"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_057 - skill `tool-calling` (disagreement)

> ...architecture. Orchestration and multi-agent design, tool contracts, memory, and context engineering (RAG, MCP) with clear...

- A: `tool-calling` · required · raw_text: "tool contracts"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_058 - skill `ai-deployment` (disagreement)

> ...and solve complex problems, with a demonstrated ability to productise and deploy using cloud services (eg. Amazon Web Services, Google Cloud Platform). • Strong...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "productise and deploy using cloud services"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_059 - skill `ai-deployment` (disagreement)

> ...for your success in the role</span></h5><div><p>You have shipped GenAI solutions into production and understand the realities behind them: messy data,...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "shipped GenAI solutions into production"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_060 - skill `frontend-development` (disagreement)

> ...und Erfahrung mit React oder einem vergleichbaren modernen Frontend-Framework - Gute Programmierkenntnisse in Python sowie Erfahrung in...

- A: `frontend-development` · required · raw_text: "modernen Frontend-Framework"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_061 - skill `ai-deployment` (disagreement)

> ...(z. B. Terraform oder AWS CDK/CloudFormation). - Du hast LLM-Anwendungen mit Amazon Bedrock in den produktiven Einsatz gebracht und dabei Vektordatenbanken angebunden. - Du nutzt...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "LLM-Anwendungen mit Amazon Bedrock in den produktiven Einsatz gebracht"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_061 - skill `ai-ml` (disagreement)

> ...Du bringst mind. 3 Jahre Erfahrung in der Software- oder KI-Entwicklung mit und hast ein abgeschlossenes Studium (Informatik,...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "KI-Entwicklung"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_061 - skill `evaluation` (disagreement)

> ...für KI-Systeme - Erfahrung in der systematischer Evaluation von Enterprise-KI-Anwendungen und KI-Pipelines -...

- A: `evaluation` · nice_to_have · raw_text: "Evaluation"
- B: `evaluation` · required · raw_text: "systematischer Evaluation von Enterprise-KI-Anwendungen und KI-Pipelines"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_061 - skill `mlops` (disagreement)

> ...dir bei der Arbeit helfen wird - Erfahrung mit MLOps und Observability für KI-Systeme - Erfahrung in der...

- A: `mlops` · nice_to_have · raw_text: "MLOps"
- B: `mlops` · required · raw_text: "MLOps"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_061 - skill `observability` (disagreement)

> ...dir bei der Arbeit helfen wird - Erfahrung mit MLOps und Observability für KI-Systeme - Erfahrung in der systematischer...

- A: `observability` · nice_to_have · raw_text: "Observability"
- B: `observability` · required · raw_text: "Observability"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_061 - skill `software-engineering` (disagreement)

> ...Enterprise-KI-Anwendungen und KI-Pipelines - Erfahrung in agiler Softwareentwicklung (Scrum, Kanban oder SAFe) und strukturierter technischer...

- A: `software-engineering` · nice_to_have · raw_text: "agiler Softwareentwicklung"
- B: `software-engineering` · required · raw_text: "Software- oder KI-Entwicklung"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_063 - skill `ai-ml` (disagreement)

> ...or voice infrastructure, and with production LLM, AI model, or agentic systems. - Experience with PostgreSQL,...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI model"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 34. golden_063 - skill `livekit` (disagreement)

> ...and fault tolerance. - Familiarity with tools such as LiveKit, Temporal, message queues, workflow orchestration, React,...

- A: `livekit` · nice_to_have · raw_text: "LiveKit"
- B: `livekit` · required · raw_text: "LiveKit"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 35. golden_063 - skill `observability` (disagreement)

> ...message queues, workflow orchestration, React, and observability platforms is valuable. - Independent, action-oriented approach,...

- A: `observability` · nice_to_have · raw_text: "observability platforms"
- B: `observability` · required · raw_text: "observability platforms"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 36. golden_063 - skill `react` (disagreement)

> ...LiveKit, Temporal, message queues, workflow orchestration, React, and observability platforms is valuable. - Independent,...

- A: `react` · nice_to_have · raw_text: "React"
- B: `react` · required · raw_text: "React"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 37. golden_063 - skill `temporal` (disagreement)

> ...tolerance. - Familiarity with tools such as LiveKit, Temporal, message queues, workflow orchestration, React, and...

- A: `temporal` · nice_to_have · raw_text: "Temporal"
- B: `temporal` · required · raw_text: "Temporal"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 38. golden_049 - skill `testing` (uncertain)

> ...and user-facing behavior • Experience with evaluation, testing, validation, or quality checks for AI-generated outputs •...

- A: `testing` · required · raw_text: "testing"
- B: `testing` · required · raw_text: "testing"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_050 - skill `langchain` (uncertain)

> ...of ML libraries (e.g., scikit-learn) and are eager to dive deep into LangChain, LLM orchestration, and vector databases. • Engineering...

- A: `langchain` · required · raw_text: "dive deep into LangChain"
- B: `langchain` · required · raw_text: "dive deep into LangChain"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_050 - skill `llm-orchestration` (uncertain)

> ...scikit-learn) and are eager to dive deep into LangChain, LLM orchestration, and vector databases. • Engineering Excellence: You value...

- A: `llm-orchestration` · required · raw_text: "LLM orchestration"
- B: `llm-orchestration` · required · raw_text: "LLM orchestration"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 41. golden_050 - skill `machine-learning` (uncertain)

> ...Notebooks. • AI Ecosystem: You have basic knowledge of ML libraries (e.g., scikit-learn) and are eager to dive deep into...

- A: `machine-learning` · required · raw_text: "ML libraries"
- B: `machine-learning` · required · raw_text: "ML libraries"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_050 - skill `vector-databases` (uncertain)

> ...eager to dive deep into LangChain, LLM orchestration, and vector databases. • Engineering Excellence: You value clean code....

- A: `vector-databases` · required · raw_text: "vector databases"
- B: `vector-databases` · required · raw_text: "vector databases"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_051 - skill `apis` (uncertain)

> ...lifecycle across developer tools, infrastructure, APIs, and cloud systems.</li> <li>Experienced at integrating...

- A: `apis` · required · raw_text: "APIs"
- B: `apis` · required · raw_text: "APIs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_051 - skill `cloud` (uncertain)

> ...across developer tools, infrastructure, APIs, and cloud systems.</li> <li>Experienced at integrating complex software...

- A: `cloud` · required · raw_text: "cloud systems"
- B: `cloud` · required · raw_text: "cloud systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_052 - skill `agents` (uncertain)

> ...other inference acceleration methods. - Experience with agentic workloads, including tool calling, structured outputs, streaming...

- A: `agents` · nice_to_have · raw_text: "agentic workloads"
- B: `agents` · nice_to_have · raw_text: "agentic workloads"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_052 - skill `inference-optimization` (uncertain)

> ...engineering skills. - Hands-on experience deploying or optimizing LLM, VLM, or high-throughput transformer inference systems. - Practical knowledge of at least one modern inference...

- A: `inference-optimization` · required · raw_text: "optimizing LLM, VLM, or high-throughput transformer inference systems"
- B: `inference-optimization` · required · raw_text: "optimizing LLM, VLM, or high-throughput transformer inference systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_053 - skill `ai-deployment` (uncertain)

> ...sowie mit Modelltraining, Evaluation, Optimierung und produktiver Bereitstellung mit. - Du hast Erfahrung in der Entwicklung von...

- A: `ai-deployment` · required · raw_text: "produktiver Bereitstellung"
- B: `ai-deployment` · required · raw_text: "produktiver Bereitstellung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_053 - skill `model-development` (uncertain)

> ...wie PyTorch, TensorFlow oder scikit-learn sowie mit Modelltraining, Evaluation, Optimierung und produktiver Bereitstellung...

- A: `model-development` · required · raw_text: "Modelltraining"
- B: `model-development` · required · raw_text: "Modelltraining"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_053 - skill `model-versioning` (uncertain)

> ...oder ein solides Verständnis von MLOps/LLMOps, Monitoring, Versionierung, Retraining und produktiven AI-Betriebsmodellen mit. - Du hast...

- A: `model-versioning` · required · raw_text: "Versionierung, Retraining"
- B: `model-versioning` · required · raw_text: "Versionierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_053 - skill `vector-databases` (uncertain)

> ...Models, beispielsweise in den Bereichen RAG, Embeddings, Vector Stores, Prompt Engineering und Guardrails, kommunizierst...

- A: `vector-databases` · required · raw_text: "Vector Stores"
- B: `vector-databases` · required · raw_text: "Vector Stores"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_054 - skill `agents` (uncertain)

> ...LLM-based systems such as MCP Servers, RAG pipelines, agentic workflows, ideally with at least one running in a real environment -...

- A: `agents` · required · raw_text: "agentic workflows"
- B: `agents` · required · raw_text: "agentic workflows"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_054 - skill `data-privacy-and-security` (uncertain)

> ...plus a strong grasp of authentication, authorization, and data security - Technical Skills: You are fluent in Python, Java or...

- A: `data-privacy-and-security` · required · raw_text: "data security"
- B: `data-privacy-and-security` · required · raw_text: "data security"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_054 - skill `multi-agent-systems` (uncertain)

> ...Frameworks and Lowcode: You acquired experience with multi-agent frameworks such as CrewAI and low-code platforms such as Dataleap or...

- A: `multi-agent-systems` · nice_to_have · raw_text: "multi-agent frameworks"
- B: `multi-agent-systems` · nice_to_have · raw_text: "multi-agent frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_055 - skill `ai-deployment` (uncertain)

> ...fundamentals. - Extensive experience with training and deploying machine learning models, particularly within the NLP/LLM domain. Familiarity with...

- A: `ai-deployment` · required · raw_text: "deploying machine learning models"
- B: `ai-deployment` · required · raw_text: "deploying machine learning models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: drop

## 55. golden_055 - skill `model-development` (uncertain)

> ...data modeling fundamentals. - Extensive experience with training and deploying machine learning models, particularly within the NLP/LLM domain. Familiarity with...

- A: `model-development` · required · raw_text: "training and deploying machine learning models"
- B: `model-development` · required · raw_text: "training and deploying machine learning models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_055 - skill `software-architecture` (uncertain)

> ...with Python and modern service architectures; strong system design and data modeling fundamentals. - Extensive experience...

- A: `software-architecture` · required · raw_text: "system design"
- B: `software-architecture` · required · raw_text: "system design"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_056 - skill `ai-ml` (uncertain)

> ...Ansatz gesucht. Mind. 5 Jahre Softwareentwicklung, davon 3 Jahre KI. Kenntnisse in **Python**, **TypeScript**, **Machine...

- A: `ai-ml` · required · raw_text: "3 Jahre KI"
- B: `ai-ml` · required · raw_text: "davon 3 Jahre KI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_056 - skill `software-engineering` (uncertain)

> ...mit agentischem Ansatz gesucht. Mind. 5 Jahre Softwareentwicklung, davon 3 Jahre KI. Kenntnisse in **Python**,...

- A: `software-engineering` · required · raw_text: "Softwareentwicklung"
- B: `software-engineering` · required · raw_text: "Softwareentwicklung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_057 - skill `agent-state-management` (uncertain)

> ...in orchestration and context engineering — tool contracts, memory, RAG, multi-agent design — with Mastra, ai-sdk, LangGraph or...

- A: `agent-state-management` · required · raw_text: "memory, RAG"
- B: `agent-state-management` · required · raw_text: "memory"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_057 - skill `backend-development` (uncertain)

> ...provider rate limits and fallback without drama - Backend: You have experience with TypeScript and/or Python. - Platform mindset: you...

- A: `backend-development` · required · raw_text: "Backend: You have experience"
- B: `backend-development` · required · raw_text: "Backend"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_057 - skill `frontend-development` (uncertain)

> ...EU data-residency constraints OUR TECH STACK - Frontend: TypeScript, Svelte and React - Backend: Node.js, Nest.js -...

- A: `frontend-development` · required · raw_text: "Frontend: TypeScript"
- B: `frontend-development` · required · raw_text: "Frontend"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_057 - skill `llm-orchestration` (uncertain)

> ...end to end and still owned once it was live - Agents: real depth in orchestration and context engineering — tool contracts, memory, RAG,...

- A: `llm-orchestration` · required · raw_text: "real depth in orchestration"
- B: `llm-orchestration` · required · raw_text: "orchestration"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 63. golden_057 - skill `testing` (uncertain)

> ...system measurable, from test cases built on real data to regression suites and human review, and you can tell the difference between a model that...

- A: `testing` · required · raw_text: "regression suites and human review"
- B: `testing` · required · raw_text: "regression suites"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_059 - skill `evaluation` (uncertain)

> ...behind them: messy data, stakeholder alignment, and continuous evaluation. You are excited about where the field is going and bring...

- A: `evaluation` · required · raw_text: "continuous evaluation"
- B: `evaluation` · required · raw_text: "continuous evaluation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 65. golden_059 - skill `llms` (uncertain)

> ...building production-grade GenAI applications: RAG pipelines, agent orchestration, fine-tuning, prompt...

- A: `llms` · required · raw_text: "production-grade GenAI applications"
- B: `llms` · required · raw_text: "GenAI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_060 - attribute `seniority` (uncertain)

> ...sowie gute Deutsch- und gute Englischkenntnisse. - Mehrjährige praktische Erfahrung in der Fullstack- oder Softwareentwicklung sowie...

- A: value="mid" · basis="inferred" · signal="Mehrjährige praktische Erfahrung"
- B: value="mid" · basis="inferred" · signal="Mehrjährige praktische Erfahrung in der Fullstack- oder Softwareentwicklung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_060 - skill `agents` (uncertain)

> ...OpenAI, LLMs, RAG-Architekturen, Prompt Engineering oder agentischen Systemen - Eine selbstständige, strukturierte und pragmatische...

- A: `agents` · nice_to_have · raw_text: "agentischen Systemen"
- B: `agents` · nice_to_have · raw_text: "agentischen Systemen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_060 - skill `observability` (uncertain)

> ...auf Microsoft Azure, sowie die Bereitschaft, Deployment, Logging, Monitoring und Fehleranalyse für die eigenen Anwendungen...

- A: `observability` · required · raw_text: "Logging, Monitoring"
- B: `observability` · required · raw_text: "Monitoring und Fehleranalyse für die eigenen Anwendungen mitzuverantworten"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_060 - skill `openai-api` (uncertain)

> ...sind wünschenswert - Interesse an KI-Anwendungen und idealerweise erste praktische Erfahrung mit Azure OpenAI, LLMs, RAG-Architekturen, Prompt Engineering oder...

- A: `openai-api` · nice_to_have · raw_text: "idealerweise erste praktische Erfahrung mit Azure OpenAI"
- B: `openai-api` · nice_to_have · raw_text: "idealerweise erste praktische Erfahrung mit Azure OpenAI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_060 - skill `workflow-automation` (uncertain)

> ...Integration von REST-APIs, Webanwendungen, Datenbanken und Automatisierungslösungen - Ein gutes Verständnis für Softwarearchitektur,...

- A: `workflow-automation` · required · raw_text: "Automatisierungslösungen"
- B: `workflow-automation` · required · raw_text: "Automatisierungslösungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_061 - attribute `degree` (uncertain)

> ...in der Software- oder KI-Entwicklung mit und hast ein abgeschlossenes Studium (Informatik, Software Engineering, Ingenieurwesen o. ä.) oder eine vergleichbare technische Vorbildung. - Du entwickelst sicher in Python, baust REST-APIs z. B....

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="abgeschlossenes Studium (Informatik, Software Engineering, Ingenieurwesen o. ä.) oder eine vergleichbare technische Vorbildung"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="ein abgeschlossenes Studium (Informatik, Software Engineering, Ingenieurwesen o. ä.) oder eine vergleichbare technische Vorbildung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_061 - skill `ai-developer-tooling` (uncertain)

> ...und dabei Vektordatenbanken angebunden. - Du nutzt Agentic Coding und KI-gestützte Tools routiniert in deinem Coding-Alltag. - Du gehst offen und...

- A: `ai-developer-tooling` · required · raw_text: "Agentic Coding und KI-gestützte Tools"
- B: `ai-developer-tooling` · required · raw_text: "Agentic Coding und KI-gestützte Tools"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 73. golden_062 - attribute `german` (uncertain)

> PreSales Engineer Data & AI (m/w/d),Bielefeld,Berlin

- A: value="required" · basis="inferred" · signal=null
- B: value="required" · basis="inferred" · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_062 - skill `ai-ml` (uncertain)

> ...Vertriebsrolle einzusetzen Du besitzt eine ausgeprägte Leidenschaft für Daten und KI und hast bereits in Projekten in diesem Umfeld gearbeitet,...

- A: `ai-ml` · required · raw_text: "Leidenschaft für Daten und KI"
- B: `ai-ml` · required · raw_text: "KI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_062 - skill `data-science` (uncertain)

> ...dem Data Engineering, Business Intelligence oder als Data Scientist, und die klare Motivation, Deine technische Expertise in...

- A: `data-science` · required · raw_text: "als Data Scientist"
- B: `data-science` · required · raw_text: "Data Scientist"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_063 - attribute `seniority` (uncertain)

> Software Engineer, Voice AI / Backend

- A: value=null · basis=null · signal=null
- B: value=null · basis=null · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_063 - skill `agents` (uncertain)

> ...infrastructure, and with production LLM, AI model, or agentic systems. - Experience with PostgreSQL, Redis, or similar data...

- A: `agents` · required · raw_text: "agentic systems"
- B: `agents` · required · raw_text: "agentic systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_049 - attribute `degree` (spot-check)

> AI Engineer (LLM) - Remote

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 79. golden_049 - skill `ai-developer-tooling` (spot-check)

> ...checks for AI-generated outputs • Serious experience using AI development tools such as Claude Code, Codex, Cursor, Copilot, or similar as...

- agreed label: `ai-developer-tooling` · required · raw_text: "AI development tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 80. golden_049 - skill `github-copilot` (spot-check)

> ...AI development tools such as Claude Code, Codex, Cursor, Copilot, or similar as part of your daily workflow • High...

- agreed label: `github-copilot` · required · raw_text: "Copilot"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 81. golden_049 - skill `python` (spot-check)

> ...Strong software engineering skills, especially in Python or a comparable backend language • Experience building...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 82. golden_049 - skill `software-engineering` (spot-check)

> ...(Remote) about outcomes more than titles. Must-have • Strong software engineering skills, especially in Python or a comparable backend language •...

- agreed label: `software-engineering` · required · raw_text: "Strong software engineering skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 83. golden_049 - skill `workflow-automation` (spot-check)

> ...extraction, documentation automation, voice workflows, or workflow automation • German language skills • Knowledge of nursing homes or...

- agreed label: `workflow-automation` · nice_to_have · raw_text: "workflow automation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_050 - attribute `german` (spot-check)

> ...are required to effectively interact with our team. German (Nice-to-have): Proficiency in German is a strong plus for collaborating...

- agreed label: value="nice_to_have" · basis="stated" · signal="German (Nice-to-have)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_050 - skill `data-visualization` (spot-check)

> ...beyond): Proficient in Python (pandas, NumPy), SQL, and data visualization. You are comfortable in Jupyter Notebooks. • AI Ecosystem:...

- agreed label: `data-visualization` · required · raw_text: "data visualization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_050 - skill `jupyter-notebooks` (spot-check)

> ...SQL, and data visualization. You are comfortable in Jupyter Notebooks. • AI Ecosystem: You have basic knowledge of ML libraries...

- agreed label: `jupyter-notebooks` · required · raw_text: "Jupyter Notebooks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_050 - skill `llms` (spot-check)

> ...very strong interest in designing algorithms and building Generative AI applications. • The Basics (and beyond): Proficient in Python (pandas,...

- agreed label: `llms` · required · raw_text: "Generative AI applications"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_051 - skill `ai-developer-tooling` (spot-check)

> ...with AI/LLM platforms, agent frameworks, or AI-assisted development tools.<br>Experience in solutions engineering, consulting, or...

- agreed label: `ai-developer-tooling` · nice_to_have · raw_text: "AI-assisted development tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_051 - skill `ci-cd` (spot-check)

> ...systems, or software solutions.</li> <li>Familiarity with modern development workflows (CI/CD, developer environments, internal developer platforms,...

- agreed label: `ci-cd` · required · raw_text: "modern development workflows (CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_051 - skill `java` (spot-check)

> ...or consulting environment.</li> <li>Familiarity with Java or Python.</li> <li>Experience building or integrating...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_052 - skill `llms` (spot-check)

> ...and PyTorch engineering skills. - Hands-on experience deploying or optimizing LLM, VLM, or high-throughput transformer inference...

- agreed label: `llms` · required · raw_text: "deploying or optimizing LLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_052 - skill `quantization` (spot-check)

> ...with quantization-aware training, post-training quantization, FP8, INT8, INT4, NVFP4, MXFP4, AWQ, GPTQ, SmoothQuant, or...

- agreed label: `quantization` · nice_to_have · raw_text: "post-training quantization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_052 - skill `sglang` (spot-check)

> ...knowledge of at least one modern inference stack such as vLLM, SGLang, TensorRT-LLM, Triton Inference Server, NVIDIA Dynamo, Ray...

- agreed label: `sglang` · required · raw_text: "stack such as vLLM, SGLang"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_052 - skill `speculative-decoding` (spot-check)

> ...SmoothQuant, or related techniques. - Experience with distillation, speculative decoding, EAGLE, Medusa, multi-token prediction, or other inference...

- agreed label: `speculative-decoding` · nice_to_have · raw_text: "distillation, speculative decoding"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_053 - attribute `degree` (spot-check)

> NTT DATA Deutschland SE: Senior AI Engineer (w/m/x)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_053 - attribute `german` (spot-check)

> ...Vector Stores, Prompt Engineering und Guardrails, kommunizierst verhandlungssicher auf Deutsch und sehr gut auf Englisch und kannst technische Themen...

- agreed label: value="required" · basis="stated" · signal="kommunizierst verhandlungssicher auf Deutsch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_053 - skill `apache-spark` (spot-check)

> ...Feature-Engineering-Prozessen mit Technologien wie pandas, Spark, Beam oder vergleichbaren Toolchains und verstehst die...

- agreed label: `apache-spark` · required · raw_text: "Spark"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_053 - skill `aws` (spot-check)

> ...Cloud- und Cloud-Native-Architekturen auf Azure, GCP oder AWS. - Du verfügst über Kenntnisse in Containerisierung und...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_053 - skill `embeddings` (spot-check)

> ...Language Models, beispielsweise in den Bereichen RAG, Embeddings, Vector Stores, Prompt Engineering und Guardrails,...

- agreed label: `embeddings` · required · raw_text: "Embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_053 - skill `gcp` (spot-check)

> ...moderne Cloud- und Cloud-Native-Architekturen auf Azure, GCP oder AWS. - Du verfügst über Kenntnisse in...

- agreed label: `gcp` · required · raw_text: "GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_053 - skill `kubernetes` (spot-check)

> ...in Containerisierung und Deployment mit Docker sowie idealerweise Kubernetes und bringst Erfahrung oder ein solides Verständnis von...

- agreed label: `kubernetes` · nice_to_have · raw_text: "idealerweise Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_053 - skill `llm-guardrails` (spot-check)

> ...RAG, Embeddings, Vector Stores, Prompt Engineering und Guardrails, kommunizierst verhandlungssicher auf Deutsch und sehr gut...

- agreed label: `llm-guardrails` · required · raw_text: "Guardrails"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_053 - skill `llmops` (spot-check)

> ...bringst Erfahrung oder ein solides Verständnis von MLOps/LLMOps, Monitoring, Versionierung, Retraining und produktiven...

- agreed label: `llmops` · required · raw_text: "LLMOps, Monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_053 - skill `machine-learning` (spot-check)

> ...und Code Reviews. - Du bringst praktische Erfahrung mit Machine-Learning-Frameworks wie PyTorch, TensorFlow oder scikit-learn sowie mit...

- agreed label: `machine-learning` · required · raw_text: "Machine-Learning-Frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_053 - skill `mlops` (spot-check)

> ...und bringst Erfahrung oder ein solides Verständnis von MLOps/LLMOps, Monitoring, Versionierung, Retraining und produktiven...

- agreed label: `mlops` · required · raw_text: "MLOps/LLMOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_053 - skill `observability` (spot-check)

> ...Erfahrung oder ein solides Verständnis von MLOps/LLMOps, Monitoring, Versionierung, Retraining und produktiven AI-Betriebsmodellen mit. - Du...

- agreed label: `observability` · required · raw_text: "Monitoring, Versionierung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_053 - skill `rag` (spot-check)

> ...Österreich, Schweiz) einen wesentlichen Wertbeitrag zum Unternehmenserfolg, in dem sie mittels ihrer...

- agreed label: `rag` · required · raw_text: "RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_053 - skill `scikit-learn` (spot-check)

> ...Machine-Learning-Frameworks wie PyTorch, TensorFlow oder scikit-learn sowie mit Modelltraining, Evaluation, Optimierung und...

- agreed label: `scikit-learn` · required · raw_text: "scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_054 - skill `apis` (spot-check)

> ...and the common AI tooling ecosystem, with the ability to integrate across enterprise APIs - Pragmatic Approach: You possess a pragmatic,...

- agreed label: `apis` · required · raw_text: "integrate across enterprise APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_054 - skill `gcp` (spot-check)

> ...You have a working knowledge of a major cloud platform, Google Cloud preferred, plus a strong grasp of authentication, authorization, and...

- agreed label: `gcp` · nice_to_have · raw_text: "Google Cloud preferred"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_054 - skill `java` (spot-check)

> ...security - Technical Skills: You are fluent in Python, Java or comparable languages and the common AI tooling...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_054 - skill `observability` (spot-check)

> ...or n8n - System reliability: You are familiar with CI/CD, observability, and reliability practices for AI or data systems

- agreed label: `observability` · nice_to_have · raw_text: "observability"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_055 - attribute `degree` (spot-check)

> About the Position

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_055 - attribute `seniority` (spot-check)

> About the Position As a Staff AI Engineer, you’ll serve as a technical leader for our LLM-powered...

- agreed label: value="senior" · basis="stated" · signal="Staff AI Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_055 - skill `ci-cd` (spot-check)

> ...NLP/LLM domain. Familiarity with infrastructure as code, CI/CD, and cloud infrastructure. - Fluency in operational...

- agreed label: `ci-cd` · required · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_055 - skill `llms` (spot-check)

> ...including leading cross-cutting architectural changes, and deploying LLMs in real‑world scenarios at scale. - Deep experience with...

- agreed label: `llms` · required · raw_text: "deploying LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_055 - skill `nlp` (spot-check)

> ...deploying machine learning models, particularly within the NLP/LLM domain. Familiarity with infrastructure as code, CI/CD, and cloud...

- agreed label: `nlp` · required · raw_text: "NLP/LLM domain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_055 - skill `python` (spot-check)

> ...in real‑world scenarios at scale. - Deep experience with Python and modern service architectures; strong system design and...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_056 - attribute `german` (spot-check)

> Senior AI Engineer - Agentic Software Development (w/m/d)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_056 - skill `machine-learning` (spot-check)

> ...3 Jahre KI. Kenntnisse in **Python**, **TypeScript**, **Machine Learning** und **Deep Learning** erforderlich....

- agreed label: `machine-learning` · required · raw_text: "Machine Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_056 - skill `python` (spot-check)

> ...Softwareentwicklung, davon 3 Jahre KI. Kenntnisse in **Python**, **TypeScript**, **Machine Learning** und **Deep...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_057 - attribute `german` (spot-check)

> Senior Applied AI Engineer, AI Platform (f/m/d)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_057 - skill `aws` (spot-check)

> ...AWS Bedrock fallback in EU regions - Infrastructure: Kubernetes on AWS - Observability: Datadog - Auth & Internal tools:...

- agreed label: `aws` · required · raw_text: "Kubernetes on AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_057 - skill `gemini` (spot-check)

> ...PostgreSQL - AI: Mastra, Vercel ai-sdk, Google Vertex (Gemini) with AWS Bedrock fallback in EU regions -...

- agreed label: `gemini` · required · raw_text: "(Gemini)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_057 - skill `kubernetes` (spot-check)

> ...AWS Bedrock fallback in EU regions - Infrastructure: Kubernetes on AWS - Observability: Datadog - Auth & Internal...

- agreed label: `kubernetes` · required · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_057 - skill `langgraph` (spot-check)

> ...memory, RAG, multi-agent design — with Mastra, ai-sdk, LangGraph or similar. You've integrated agents into a real product...

- agreed label: `langgraph` · required · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_057 - skill `multi-agent-systems` (spot-check)

> ...- Own the AI application architecture. Orchestration and multi-agent design, tool contracts, memory, and context engineering (RAG,...

- agreed label: `multi-agent-systems` · required · raw_text: "multi-agent design"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_057 - skill `node-js` (spot-check)

> ...- Frontend: TypeScript, Svelte and React - Backend: Node.js, Nest.js - Database: MySQL, PostgreSQL - AI: Mastra,...

- agreed label: `node-js` · required · raw_text: "Node.js"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_057 - skill `rag` (spot-check)

> ...design, tool contracts, memory, and context engineering (RAG, MCP) with clear domain boundaries — plus the guardrails,...

- agreed label: `rag` · required · raw_text: "RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_058 - attribute `german` (spot-check)

> Senior Machine Learning Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_058 - skill `airflow` (spot-check)

> ...is expected. A plus would be additional experience with Airflow/Mlflow/Docker/Flink • Experience collaborating closely...

- agreed label: `airflow` · nice_to_have · raw_text: "Airflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_058 - skill `cloud` (spot-check)

> ...with a demonstrated ability to productise and deploy using cloud services (eg. Amazon Web Services, Google Cloud Platform). • Strong...

- agreed label: `cloud` · required · raw_text: "cloud services"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_058 - skill `event-driven-systems` (spot-check)

> ...Strong background in working with microservices and event-driven architecture, serverless computing, and cloud architecture patterns. •...

- agreed label: `event-driven-systems` · required · raw_text: "event-driven architecture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_058 - skill `kubernetes` (spot-check)

> ...patterns. • Familiarity with tools and packages including Kubernetes (deployment in production) is expected. A plus would be...

- agreed label: `kubernetes` · required · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_059 - attribute `german` (spot-check)

> Senior GenAI Engineer (m/w/d)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_059 - skill `ci-cd` (spot-check)

> ...environment: you have worked with containerization, CI/CD pipelines and cloud-native tooling, and you know your way around at...

- agreed label: `ci-cd` · required · raw_text: "CI/CD pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_059 - skill `gcp` (spot-check)

> ...with at least one major cloud platform, such as Azure, AWS or GCP, in a production...

- agreed label: `gcp` · required · raw_text: "or GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_059 - skill `langchain` (spot-check)

> ...with LLM frameworks (LangChain, LangGraph, or similar) and workflow automation tools...

- agreed label: `langchain` · nice_to_have · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_059 - skill `machine-learning` (spot-check)

> ...experience in software engineering or machine learning / deep learning, with a meaningful portion in GenAI or...

- agreed label: `machine-learning` · required · raw_text: "machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_059 - skill `nlp` (spot-check)

> ...learning / deep learning, with a meaningful portion in GenAI or NLP.</span></p></li></ul></div><div><div><ul><li><p><span>Stron...

- agreed label: `nlp` · required · raw_text: "in GenAI or NLP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_059 - skill `rag` (spot-check)

> ...building production-grade GenAI applications: RAG pipelines, agent orchestration, fine-tuning, prompt engineering and...

- agreed label: `rag` · required · raw_text: "GenAI applications: RAG pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_060 - attribute `degree` (spot-check)

> ...wartbare Produkte zu übersetzen Das wünschen wir uns - Ein abgeschlossenes Studium der (Wirtschafts-)Informatik, der Ingenieurwissenschaften oder eine vergleichbare, durch praktische Erfahrung erworbene Qualifikation sowie gute Deutsch- und gute Englischkenntnisse. -...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Ein abgeschlossenes Studium der (Wirtschafts-)Informatik, der Ingenieurwissenschaften oder eine vergleichbare, durch praktische Erfahrung erworbene Qualifikation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_060 - attribute `german` (spot-check)

> ...durch praktische Erfahrung erworbene Qualifikation sowie gute Deutsch- und gute Englischkenntnisse. - Mehrjährige praktische Erfahrung in der Fullstack- oder...

- agreed label: value="required" · basis="stated" · signal="gute Deutsch- und gute Englischkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_060 - skill `containerization` (spot-check)

> ...Anwendungen mitzuverantworten - Vertrautheit mit CI/CD und containerisierten Anwendungen sowie tiefgehende Platform- oder DevOps-Spezialisierung...

- agreed label: `containerization` · nice_to_have · raw_text: "containerisierten Anwendungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_060 - skill `git` (spot-check)

> ...Verständnis für Softwarearchitektur, automatisierte Tests, Versionskontrolle und moderne Entwicklungsworkflows - Erfahrung mit...

- agreed label: `git` · required · raw_text: "Versionskontrolle"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_060 - skill `prompt-engineering` (spot-check)

> ...Erfahrung mit Azure OpenAI, LLMs, RAG-Architekturen, Prompt Engineering oder agentischen Systemen - Eine selbstständige,...

- agreed label: `prompt-engineering` · nice_to_have · raw_text: "Prompt Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_060 - skill `software-architecture` (spot-check)

> ...und Automatisierungslösungen - Ein gutes Verständnis für Softwarearchitektur, automatisierte Tests, Versionskontrolle und moderne...

- agreed label: `software-architecture` · required · raw_text: "Softwarearchitektur"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_060 - skill `software-engineering` (spot-check)

> ...Mehrjährige praktische Erfahrung in der Fullstack- oder Softwareentwicklung sowie Verantwortung für Anwendungen, die produktiv...

- agreed label: `software-engineering` · required · raw_text: "oder Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_061 - attribute `seniority` (spot-check)

> ...Verwaltung und Kultur. Wen wir suchen - Du bringst mind. 3 Jahre Erfahrung in der Software- oder KI-Entwicklung mit und hast ein...

- agreed label: value="mid" · basis="inferred" · signal="mind. 3 Jahre Erfahrung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_061 - skill `llms` (spot-check)

> ...(z. B. Terraform oder AWS CDK/CloudFormation). - Du hast LLM-Anwendungen mit Amazon Bedrock in den produktiven Einsatz gebracht und...

- agreed label: `llms` · required · raw_text: "LLM-Anwendungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_061 - skill `sql` (spot-check)

> ...REST-APIs z. B. mit FastAPI und Pydantic und arbeitest mit SQL-Datenbanken. - Du hast Cloud-Infrastruktur auf AWS aufgesetzt und...

- agreed label: `sql` · required · raw_text: "SQL-Datenbanken"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_061 - skill `terraform` (spot-check)

> ...Docker, CI/CD-Pipelines und Infrastructure-as-Code (z. B. Terraform oder AWS CDK/CloudFormation). - Du hast LLM-Anwendungen...

- agreed label: `terraform` · required · raw_text: "Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_062 - attribute `seniority` (spot-check)

> PreSales Engineer Data & AI (m/w/d),Bielefeld,Berlin

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_063 - attribute `german` (spot-check)

> Software Engineer, Voice AI / Backend

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_063 - skill `aws` (spot-check)

> ...or similar data stores, plus cloud infrastructure on AWS, GCP, or Azure. - Ability to design or debug systems...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 156. golden_063 - skill `distributed-systems` (spot-check)

> ...fail. WHAT WE'RE LOOKING FOR - Production experience building and owning distributed systems, with a track record of shipping product software and...

- agreed label: `distributed-systems` · required · raw_text: "building and owning distributed systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 157. golden_063 - skill `fastapi` (spot-check)

> ...- Strong software fundamentals and experience with Python, FastAPI, or TypeScript in production systems. - Experience with...

- agreed label: `fastapi` · required · raw_text: "FastAPI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
