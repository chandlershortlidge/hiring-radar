# Review queue - 20261119T141542Z_label

164 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261119T141542Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 159 accepted labels,
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

> The Opportunity

- PwC · AI Data Governance Engineer- Manager
- Chicago · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_095 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer - Remote

- Hyatt · Senior Machine Learning Engineer - Remote
- Chicago · en · jsearch · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_096 - scope `in_scope` (in-scope)

> Forward Deployed AI Engineer — Global Impact

- United Airlines · Forward Deployed AI Engineer — Global Impact
- Chicago · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_097 - scope `in_scope` (in-scope)

> AI-Driven Full Stack Engineer (Python & ML Infra)

- Turing Enterprises, Inc. · AI-Driven Full Stack Engineer (Python & ML Infra)
- Chicago · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_098 - scope `in_scope` (in-scope)

> AI Software Engineer (Proposal Tools)

- 100000 Motorola Solutions, Inc. · AI Software Engineer (Proposal Tools)
- Chicago · en · jsearch · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_099 - scope `in_scope` (in-scope)

> AI Data Engineer (remote)

- Visionaire Partners · AI Data Engineer (remote)
- Chicago · en · jsearch · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_100 - scope `in_scope` (in-scope)

> [Data Engineer] Senior / Staff MLOps Engineer (Bangkok Based, relocation provided)

- Agoda · [Data Engineer] Senior / Staff MLOps Engineer (Bangkok Based, relocation provided)
- Chicago · en · jsearch · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_101 - scope `in_scope` (in-scope)

> AI DevOps Engineer Azure and GenAI

- Rose International · AI DevOps Engineer Azure and GenAI
- Chicago · en · jsearch · 31 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_102 - scope `in_scope` (in-scope)

> Senior AI Platform & MLOps Engineer

- AbbVie Inc. · Senior AI Platform & MLOps Engineer
- Chicago · en · jsearch · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_103 - scope `in_scope` (in-scope)

> Forward-Deployed AI Engineer for Trading

- Brookfield Properties · Forward-Deployed AI Engineer for Trading
- Chicago · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_104 - scope `in_scope` (in-scope)

> AI/ML Engineer (Deep Learning, PyTorch) at Chime Chicago

- Chime · AI/ML Engineer (Deep Learning, PyTorch) at Chime Chicago
- Chicago · en · jsearch · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_105 - scope `in_scope` (in-scope)

> AI Engineer - US Remote

- Maneva · AI Engineer - US Remote
- Chicago · en · jsearch · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_106 - scope `in_scope` (in-scope)

> Senior AI/ML Engineer — Hybrid, Impactful ML Solutions

- LHH · Senior AI/ML Engineer — Hybrid, Impactful ML Solutions
- Chicago · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_107 - scope `in_scope` (in-scope)

> W2 role - AI Lead Platform Engineer 12+ years local to IL required

- Synchron Technologies · W2 role - AI Lead Platform Engineer 12+ years local to IL required
- Chicago · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_108 - scope `in_scope` (in-scope)

> Slalom Flex (Project Based) AWS Agentic AI Engineer – Amazon Quick Suite

- Slalom · Slalom Flex (Project Based) AWS Agentic AI Engineer – Amazon Quick Suite
- Chicago · en · jsearch · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_094 - skill `aws` (disagreement)

> ...MS SQL), visualization tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) -...

- A: `aws` · nice_to_have · raw_text: "AWS"
- B: `aws` · required · raw_text: "AWS"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_094 - skill `azure` (disagreement)

> ...visualization tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing...

- A: `azure` · nice_to_have · raw_text: "Azure"
- B: `azure` · required · raw_text: "Azure"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_094 - skill `cloud` (disagreement)

> ...(Databricks, MS SQL), visualization tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing...

- A: `cloud` · nice_to_have · raw_text: "cloud platforms (AWS, Azure, GCP)"
- B: `cloud` · required · raw_text: "cloud platforms"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_094 - skill `data-modeling` (disagreement)

> ...or similar - Familiarity with semantic layer creation, conceptual modeling, and query optimization - Applying complex data analysis...

- A: `data-modeling` · nice_to_have · raw_text: "conceptual modeling"
- B: `data-modeling` · required · raw_text: "conceptual modeling"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_094 - skill `data-visualization` (disagreement)

> ...a Certification in databases (Databricks, MS SQL), visualization tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive...

- A: `data-visualization` · nice_to_have · raw_text: "visualization tools (Power BI)"
- B: `data-visualization` · required · raw_text: "visualization tools"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_094 - skill `databricks` (disagreement)

> ...least one of the following: a Certification in databases (Databricks, MS SQL), visualization tools (Power BI), cloud platforms...

- A: `databricks` · nice_to_have · raw_text: "Databricks"
- B: `databricks` · required · raw_text: "Databricks"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_094 - skill `gcp` (disagreement)

> ...tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing...

- A: `gcp` · nice_to_have · raw_text: "GCP"
- B: `gcp` · required · raw_text: "GCP"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_094 - skill `knowledge-graphs` (disagreement)

> ...experience in ontology development and management - Designing and implementing knowledge graphs using technologies such as RDF, OWL, SPARQL, or similar -...

- A: `knowledge-graphs` · nice_to_have · raw_text: "Designing and implementing knowledge graphs"
- B: `knowledge-graphs` · required · raw_text: "Designing and implementing knowledge graphs"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_094 - skill `machine-learning` (disagreement)

> ...tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing governance frameworks and data...

- A: `machine-learning` · nice_to_have · raw_text: "predictive modeling/ML"
- B: `machine-learning` · required · raw_text: "predictive modeling/ML"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_094 - skill `power-bi` (disagreement)

> ...in databases (Databricks, MS SQL), visualization tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive...

- A: `power-bi` · nice_to_have · raw_text: "Power BI"
- B: `power-bi` · required · raw_text: "Power BI"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_094 - skill `python` (disagreement)

> ...platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing governance frameworks and data...

- A: `python` · nice_to_have · raw_text: "Python"
- B: `python` · required · raw_text: "Python"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_094 - skill `sql` (disagreement)

> ...the following: a Certification in databases (Databricks, MS SQL), visualization tools (Power BI), cloud platforms (AWS,...

- A: `sql` · nice_to_have · raw_text: "MS SQL"
- B: `sql` · required · raw_text: "MS SQL"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_095 - skill `ai-infrastructure` (disagreement)

> ...Demonstrated hands- on experience delivering end-to-end ML systems, spanning model development, deployment, and production infrastructure • Proficiency with modern ML engineering tooling,...

- A: (did not label this)
- B: `ai-infrastructure` · required · raw_text: "ML systems, spanning model development, deployment, and production infrastructure"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_097 - skill `ai-infrastructure` (disagreement)

> ...be on Python across backend services, data pipelines, and ML infrastructure, with collaboration from researchers to refine AI-driven...

- A: `ai-infrastructure` · required · raw_text: "ML infrastructure"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_097 - skill `backend-development` (disagreement)

> ...large language models. Focus will be on Python across backend services, data pipelines, and ML infrastructure, with collaboration...

- A: `backend-development` · required · raw_text: "backend services"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_097 - skill `data-pipelines` (disagreement)

> ...models. Focus will be on Python across backend services, data pipelines, and ML infrastructure, with collaboration from...

- A: `data-pipelines` · required · raw_text: "data pipelines"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_097 - skill `python` (disagreement)

> AI-Driven Full Stack Engineer (Python & ML Infra) Turing is seeking a Software Engineering Evaluator to...

- A: `python` · required · raw_text: "Python & ML Infra"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_098 - skill `ai-ml` (disagreement)

> ...Python, JavaScript/Node.js, HTML5, CSS, and SQL/BigQuery AI & LLM Engineering to design and develop machine learning applications and...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI & LLM Engineering"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 34. golden_098 - skill `workflow-automation` (disagreement)

> ...present solutions across diverse audiences Experience with Google Docs automation preferred Proficiency with IDEs such as VSCode, Microsoft Office,...

- A: (did not label this)
- B: `workflow-automation` · nice_to_have · raw_text: "Google Docs automation preferred"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 35. golden_099 - skill `structured-data-extraction` (disagreement)

> ...data backend for active, production AI applications and unstructured document parsing. • Proficiency with AI coding tools and strong...

- A: `structured-data-extraction` · required · raw_text: "unstructured document parsing"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 36. golden_099 - skill `workflow-automation` (disagreement)

> ...Experience with MCP servers/connectors, Streamlit/React, financial/tax automation, or mentoring offshore teams. Details & Benefits:...

- A: (did not label this)
- B: `workflow-automation` · nice_to_have · raw_text: "financial/tax automation"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 37. golden_100 - skill `model-development` (disagreement)

> ...to build scalable and efficient data pipelines and model training and deployment systems • Develop and maintain monitoring...

- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "model training"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 38. golden_101 - skill `agents` (disagreement)

> ...GenAI apps, LLM-powered services, AI agents, RAG, vector search, or shared enterprise AI...

- A: `agents` · nice_to_have · raw_text: "AI agents"
- B: `agents` · required · raw_text: "agent evaluation"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 39. golden_101 - skill `ai-deployment` (disagreement)

> ...management; audit evidenceNice-to-Haves-Deploying/operating GenAI apps, LLM-powered services, AI agents, RAG, vector search, or...

- A: (did not label this)
- B: `ai-deployment` · nice_to_have · raw_text: "Deploying/operating GenAI apps"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 40. golden_101 - skill `llmops` (disagreement)

> ...RAG, vector search, or shared enterprise AI platforms.-GenAIOps, MLOps, AgentOps, model/endpoint lifecycle management,...

- A: (did not label this)
- B: `llmops` · nice_to_have · raw_text: "GenAIOps"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 41. golden_101 - skill `mlops` (disagreement)

> ...RAG, vector search, or shared enterprise AI platforms.-GenAIOps, MLOps, AgentOps, model/endpoint lifecycle management, prompt/agent...

- A: `mlops` · nice_to_have · raw_text: "GenAIOps, MLOps, AgentOps"
- B: `mlops` · required · raw_text: "model and endpoint operations"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 42. golden_101 - skill `openai-api` (disagreement)

> ...Foundry / Azure AI services; Azure Machine Learning; Azure OpenAI; AKS; API Management; Key Vault; Entra ID; Azure...

- A: `openai-api` · required · raw_text: "Azure OpenAI"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 43. golden_105 - skill `ai-ml` (disagreement)

> ...us immediately at IT-Security@Maneva.ai. Remote Skills: Artificial Intelligence (AI), Benchmarking, CUDA (Compute Unified Device Architecture),...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Artificial Intelligence (AI)"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 44. golden_105 - skill `cloud` (disagreement)

> ...Benchmarking, CUDA (Compute Unified Device Architecture), Cloud Computing, Code Reviews, Computer Vision, Customer Satisfaction,...

- A: (did not label this)
- B: `cloud` · required · raw_text: "Cloud Computing"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 45. golden_105 - skill `cuda` (disagreement)

> ...Edge and embedded deployment experience (TensorRT, CUDA, quantization-aware training). • Experience with LLM...

- A: `cuda` · nice_to_have · raw_text: "CUDA"
- B: `cuda` · required · raw_text: "CUDA (Compute Unified Device Architecture)"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 46. golden_105 - skill `model-development` (disagreement)

> ...segmentation (YOLO family, DETR-style models), including training, tuning, and production deployment. • Hands-on experience...

- A: (did not label this)
- B: `model-development` · required · raw_text: "training"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 47. golden_094 - attribute `seniority` (uncertain)

> ...and address complex business questions. As a Manager, you will lead client workstreams with accountability for planning, budgets, timelines, and...

- A: value="senior" · basis="inferred" · signal="you will lead client workstreams"
- B: value="senior" · basis="inferred" · signal="you will lead client workstreams"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_095 - skill `ai-deployment` (uncertain)

> ...foundations • Demonstrated hands- on experience delivering end-to-end ML systems, spanning model development, deployment, and production infrastructure • Proficiency with modern...

- A: `ai-deployment` · required · raw_text: "end-to-end ML systems, spanning model development, deployment"
- B: `ai-deployment` · required · raw_text: "ML systems, spanning model development, deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_095 - skill `machine-learning` (uncertain)

> ...Learning, or a related field • 5+ years of experience building and operating machine learning solutions in cloud environments, with focus on AI services and MLOps...

- A: `machine-learning` · required · raw_text: "building and operating machine learning solutions"
- B: `machine-learning` · required · raw_text: "building and operating machine learning solutions"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_095 - skill `model-serving` (uncertain)

> ...Experience Preferred • Experience designing and scaling real-time and batch inference systems in production • Hands- on experience with deep learning frameworks and...

- A: `model-serving` · nice_to_have · raw_text: "real-time and batch inference systems in production"
- B: `model-serving` · nice_to_have · raw_text: "designing and scaling real-time and batch inference systems in production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_096 - attribute `seniority` (uncertain)

> ...own end-to-end AI projects from discovery to production, leading architecture, testing, and governance efforts. Responsibilities include prototyping AI workflows,...

- A: value="senior" · basis="inferred" · signal="leading architecture, testing, and governance efforts"
- B: value="senior" · basis="inferred" · signal="leading architecture, testing, and governance efforts"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_098 - attribute `seniority` (uncertain)

> ...Specific Knowledge and Skills Bachelor's Degree 2+ years of experience in software development Legal authorization to work in the U.S. indefinitely is...

- A: value="junior" · basis="inferred" · signal="2+ years of experience in software development"
- B: value="junior" · basis="inferred" · signal="2+ years of experience in software development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_098 - skill `api-design` (uncertain)

> ...applications and language generation systems Cloud & API Architecture to implement complex service-to-service OAuth2...

- A: `api-design` · required · raw_text: "API Architecture"
- B: `api-design` · required · raw_text: "API Architecture"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_098 - skill `gemini` (uncertain)

> ...using Agile methodologies, Git workflows, GitHub, and AI coding assistants such as Gemini or Windsurf Technical Communication to translate complex...

- A: `gemini` · required · raw_text: "AI coding assistants such as Gemini"
- B: `gemini` · required · raw_text: "Gemini"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_098 - skill `software-engineering` (uncertain)

> ...permit sponsorship is not available for this position. Software Development to design, build, and deploy applications utilizing Python, JavaScript/Node.js, HTML5, CSS, and...

- A: `software-engineering` · required · raw_text: "Software Development to design, build, and deploy applications"
- B: `software-engineering` · required · raw_text: "Software Development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_099 - attribute `seniority` (uncertain)

> ...like IRS form completion. • Lead & Future-Proof: Guide offshore mid-level engineers through code reviews and architectural alignment, while building Model Context Protocol (MCP) servers to...

- A: value="senior" · basis="inferred" · signal="Guide offshore mid-level engineers through code reviews and architectural alignment"
- B: value="senior" · basis="inferred" · signal="Guide offshore mid-level engineers through code reviews and architectural alignment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_099 - skill `backend-development` (uncertain)

> ...Fabric, Snowflake, or Databricks). • Proven experience supporting the data backend for active, production AI applications and unstructured...

- A: `backend-development` · required · raw_text: "supporting the data backend"
- B: `backend-development` · required · raw_text: "supporting the data backend"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_099 - skill `cloud` (uncertain)

> ...Strong proficiency in Python, Microsoft Azure, and modern cloud data platforms (Microsoft Fabric, Snowflake, or Databricks). • Proven...

- A: `cloud` · required · raw_text: "modern cloud data platforms"
- B: `cloud` · required · raw_text: "modern cloud data platforms"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_099 - skill `mcp` (uncertain)

> ...tools and strong cross-cultural communication skills. • Bonus: Experience with MCP servers/connectors, Streamlit/React, financial/tax automation, or mentoring...

- A: `mcp` · nice_to_have · raw_text: "Bonus: Experience with MCP servers/connectors"
- B: `mcp` · nice_to_have · raw_text: "MCP servers/connectors"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_099 - skill `react` (uncertain)

> ...skills. • Bonus: Experience with MCP servers/connectors, Streamlit/React, financial/tax automation, or mentoring offshore...

- A: `react` · nice_to_have · raw_text: "Streamlit/React"
- B: `react` · nice_to_have · raw_text: "React"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_099 - skill `streamlit` (uncertain)

> ...skills. • Bonus: Experience with MCP servers/connectors, Streamlit/React, financial/tax automation, or mentoring offshore...

- A: `streamlit` · nice_to_have · raw_text: "Streamlit/React"
- B: `streamlit` · nice_to_have · raw_text: "Streamlit"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_100 - skill `ai-deployment` (uncertain)

> ...to build scalable and efficient data pipelines and model training and deployment systems • Develop and maintain monitoring and management tools to...

- A: `ai-deployment` · nice_to_have · raw_text: "model training and deployment systems"
- B: `ai-deployment` · nice_to_have · raw_text: "model training and deployment systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_100 - skill `apache-spark` (uncertain)

> ...PyTorch etc. • Experience with Big Data tools – Spark, S3, Hadoop • Strong knowledge of containerization and...

- A: `apache-spark` · nice_to_have · raw_text: "Spark"
- B: `apache-spark` · nice_to_have · raw_text: "Spark"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_100 - skill `aws-s3` (uncertain)

> ...PyTorch etc. • Experience with Big Data tools – Spark, S3, Hadoop • Strong knowledge of containerization and...

- A: `aws-s3` · nice_to_have · raw_text: "S3"
- B: `aws-s3` · nice_to_have · raw_text: "S3"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_100 - skill `hadoop` (uncertain)

> ...etc. • Experience with Big Data tools – Spark, S3, Hadoop • Strong knowledge of containerization and container...

- A: `hadoop` · nice_to_have · raw_text: "Hadoop"
- B: `hadoop` · nice_to_have · raw_text: "Hadoop"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_100 - skill `machine-learning` (uncertain)

> ...with MLOps platforms, such as Kubeflow or MLFlow • Experience with ML frameworks – like scikit-learn, LGBM, Tensorflow, PyTorch etc. •...

- A: `machine-learning` · nice_to_have · raw_text: "Experience with ML frameworks"
- B: `machine-learning` · nice_to_have · raw_text: "ML frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_100 - skill `mlops` (uncertain)

> ...and debugging user issues What You’ll Need to Succeed • 5+ years of experience in MLOps, Software engineering, Data engineering, or a related...

- A: `mlops` · required · raw_text: "5+ years of experience in MLOps"
- B: `mlops` · required · raw_text: "5+ years of experience in MLOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_100 - skill `observability` (uncertain)

> ...training and deployment systems • Develop and maintain monitoring and management tools to ensure the reliability and performance of our...

- A: `observability` · nice_to_have · raw_text: "monitoring and management tools"
- B: `observability` · nice_to_have · raw_text: "monitoring and management tools"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_100 - skill `software-engineering` (uncertain)

> ...workflows. Our AI Ops team combines the best practices of software engineering with data science to help Machine Learning Engineers and...

- A: `software-engineering` · required · raw_text: "Software engineering"
- B: `software-engineering` · required · raw_text: "Software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_101 - skill `azure-ai-foundry` (uncertain)

> ...stakeholders in a regulated enterprise environment.-Azure; Microsoft Foundry / Azure AI services; Azure Machine Learning; Azure OpenAI; AKS; API...

- A: `azure-ai-foundry` · required · raw_text: "Microsoft Foundry / Azure AI services"
- B: `azure-ai-foundry` · required · raw_text: "Microsoft Foundry"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_101 - skill `cloud` (uncertain)

> ...& Experience-7+ years in DevOps, platform engineering, cloud engineering, site reliability engineering, software engineering, or a...

- A: `cloud` · required · raw_text: "cloud engineering"
- B: `cloud` · required · raw_text: "cloud engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_101 - skill `cybersecurity` (uncertain)

> ...Linux, networking, identity, secrets management, and cloud security fundamentals.-Proficiency in Python plus scripting with Bash,...

- A: `cybersecurity` · required · raw_text: "cloud security fundamentals"
- B: `cybersecurity` · required · raw_text: "cloud security fundamentals"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_101 - skill `databricks` (uncertain)

> ...APIs; JSON/YAML; microservices; event-driven integration; Snowflake/Databricks familiarity-DevSecOps scanning; secrets management; identity and...

- A: `databricks` · required · raw_text: "Snowflake/Databricks familiarity"
- B: `databricks` · required · raw_text: "Databricks familiarity"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_101 - skill `devops` (uncertain)

> ...MLOps, or AI engineering.Required Skills & Experience-7+ years in DevOps, platform engineering, cloud engineering, site reliability...

- A: `devops` · required · raw_text: "7+ years in DevOps"
- B: `devops` · required · raw_text: "Certifications: Microsoft Azure, GitHub, Kubernetes, Terraform, DevOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_101 - skill `snowflake` (uncertain)

> ...APIs; JSON/YAML; microservices; event-driven integration; Snowflake/Databricks familiarity-DevSecOps scanning; secrets management; identity and...

- A: `snowflake` · required · raw_text: "Snowflake/Databricks familiarity"
- B: `snowflake` · required · raw_text: "Snowflake"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_101 - skill `software-engineering` (uncertain)

> ...cloud engineering, site reliability engineering, software engineering, or a related discipline.-3+ years of hands-on experience building and supporting...

- A: `software-engineering` · required · raw_text: "software engineering, or a related discipline"
- B: `software-engineering` · required · raw_text: "software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_104 - skill `ai-deployment` (uncertain)

> ...Contribute to the shared ML platform Requirements • Experience deploying deep learning models in production • Solid ML fundamentals and evaluation design • Strong...

- A: `ai-deployment` · required · raw_text: "Experience deploying deep learning models in production"
- B: `ai-deployment` · required · raw_text: "deploying deep learning models in production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_104 - skill `distributed-systems` (uncertain)

> ...and evaluation design • Strong Python and SQL, PyTorch and distributed compute • Knowledge of AWS, SageMaker, Airflow, Kafka, Redis or...

- A: `distributed-systems` · required · raw_text: "distributed compute"
- B: `distributed-systems` · required · raw_text: "distributed compute"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 79. golden_105 - skill `ai-deployment` (uncertain)

> ...DETR-style models), including training, tuning, and production deployment. • Hands-on experience with VLMs (for example LLaVA-,...

- A: `ai-deployment` · required · raw_text: "production deployment"
- B: `ai-deployment` · required · raw_text: "production deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 80. golden_105 - skill `inference-optimization` (uncertain)

> ...Track record of taking models from research to production: model optimization, inference serving, monitoring, and iteration on...

- A: `inference-optimization` · required · raw_text: "model optimization"
- B: `inference-optimization` · required · raw_text: "model optimization"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 81. golden_105 - skill `llms` (uncertain)

> ...CUDA, quantization-aware training). • Experience with LLM tooling such as vLLM, or with RLHF-style post-training for...

- A: `llms` · nice_to_have · raw_text: "LLM tooling"
- B: `llms` · nice_to_have · raw_text: "LLM tooling"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 82. golden_105 - skill `machine-learning` (uncertain)

> ...product. Requirements What we're looking for • 5+ years building and shipping ML systems, with focus on computer vision; BS/MS/PhD in CS, EE, or a...

- A: `machine-learning` · required · raw_text: "building and shipping ML systems"
- B: `machine-learning` · required · raw_text: "ML systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 83. golden_105 - skill `prompt-engineering` (uncertain)

> ...LLaVA-, Qwen-VL-, or PaliGemma-style models): fine-tuning, prompting, grounding, and evaluation. • Experience with VLAs or...

- A: `prompt-engineering` · required · raw_text: "prompting"
- B: `prompt-engineering` · required · raw_text: "prompting"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 84. golden_108 - skill `llm-guardrails` (uncertain)

> ...knowledge layers • Bedrock agents, tool use, text-to-SQL, evaluation and guardrails • Snowflake, Iceberg, S3, Glue, Athena and IAM • Comfort...

- A: `llm-guardrails` · required · raw_text: "evaluation and guardrails"
- B: `llm-guardrails` · required · raw_text: "guardrails"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 85. golden_094 - attribute `degree` (spot-check)

> ...risks to clients and project leaders What You Must Have - At least a Bachelor's degree - At least 4 years of experience What Sets You Apart -...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="At least a Bachelor's degree"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_094 - attribute `german` (spot-check)

> The Opportunity

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_095 - skill `data-pipelines` (spot-check)

> ...modern ML engineering tooling, including cloud platforms, data pipelines, and CI/CD workflows Experience Preferred • Experience...

- agreed label: `data-pipelines` · required · raw_text: "data pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_095 - skill `deep-learning` (spot-check)

> ...systems in production • Hands- on experience with deep learning frameworks and model optimization for performance and cost •...

- agreed label: `deep-learning` · nice_to_have · raw_text: "deep learning frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_095 - skill `mlops` (spot-check)

> ...learning solutions in cloud environments, with focus on AI services and MLOps foundations • Demonstrated hands- on experience delivering end-to-end...

- agreed label: `mlops` · required · raw_text: "AI services and MLOps foundations"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_095 - skill `model-development` (spot-check)

> ...on experience delivering end-to-end ML systems, spanning model development, deployment, and production infrastructure • Proficiency...

- agreed label: `model-development` · required · raw_text: "model development"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_096 - attribute `degree` (spot-check)

> Forward Deployed AI Engineer — Global Impact

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_097 - attribute `degree` (spot-check)

> AI-Driven Full Stack Engineer (Python & ML Infra)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_098 - attribute `degree` (spot-check)

> ...and system performance Specific Knowledge and Skills Bachelor's Degree 2+ years of experience in software development Legal...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="Bachelor's Degree"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_098 - skill `cloud` (spot-check)

> ...learning applications and language generation systems Cloud & API Architecture to implement complex service-to-service OAuth2...

- agreed label: `cloud` · required · raw_text: "Cloud & API Architecture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_098 - skill `gcp` (spot-check)

> ...OAuth2 authentication flows and REST APIs across Google Cloud and AWS Database Management to design, deploy, maintain,...

- agreed label: `gcp` · required · raw_text: "Google Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_098 - skill `git` (spot-check)

> ...Tooling to collaborate using Agile methodologies, Git workflows, GitHub, and AI coding assistants such as Gemini or Windsurf...

- agreed label: `git` · required · raw_text: "Git workflows, GitHub"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_098 - skill `llms` (spot-check)

> ...Python, JavaScript/Node.js, HTML5, CSS, and SQL/BigQuery AI & LLM Engineering to design and develop machine learning applications and...

- agreed label: `llms` · required · raw_text: "AI & LLM Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_098 - skill `node-js` (spot-check)

> ...design, build, and deploy applications utilizing Python, JavaScript/Node.js, HTML5, CSS, and SQL/BigQuery AI & LLM Engineering to...

- agreed label: `node-js` · required · raw_text: "JavaScript/Node.js"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_098 - skill `oauth` (spot-check)

> ...& API Architecture to implement complex service-to-service OAuth2 authentication flows and REST APIs across Google Cloud and AWS Database...

- agreed label: `oauth` · required · raw_text: "OAuth2 authentication flows"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_099 - attribute `german` (spot-check)

> AI Data Engineer (remote)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_099 - skill `azure` (spot-check)

> ...of experience as a Data Engineer. • Strong proficiency in Python, Microsoft Azure, and modern cloud data platforms (Microsoft Fabric,...

- agreed label: `azure` · required · raw_text: "Python, Microsoft Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_099 - skill `databricks` (spot-check)

> ...modern cloud data platforms (Microsoft Fabric, Snowflake, or Databricks). • Proven experience supporting the data backend for...

- agreed label: `databricks` · required · raw_text: "or Databricks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_099 - skill `python` (spot-check)

> ...You Bring • 3+ years of experience as a Data Engineer. • Strong proficiency in Python, Microsoft Azure, and modern cloud data platforms...

- agreed label: `python` · required · raw_text: "Strong proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_099 - skill `snowflake` (spot-check)

> ...Azure, and modern cloud data platforms (Microsoft Fabric, Snowflake, or Databricks). • Proven experience supporting the data...

- agreed label: `snowflake` · required · raw_text: "Snowflake"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_100 - attribute `degree` (spot-check)

> [Data Engineer] Senior / Staff MLOps Engineer (Bangkok Based, relocation provided)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_100 - skill `java` (spot-check)

> ...programming skills in a modern programming language (Java, Scala, Python, Kotlin) • Hands-on experience with...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_100 - skill `kotlin` (spot-check)

> ...in a modern programming language (Java, Scala, Python, Kotlin) • Hands-on experience with Kubernetes—deploying and...

- agreed label: `kotlin` · required · raw_text: "Kotlin"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_100 - skill `lightgbm` (spot-check)

> ...Experience with ML frameworks – like scikit-learn, LGBM, Tensorflow, PyTorch etc. • Experience with Big Data...

- agreed label: `lightgbm` · nice_to_have · raw_text: "LGBM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_100 - skill `model-serving` (spot-check)

> ...with DevOps and CI/CD practices • Has experience building and scaling model serving tools, i.e building APIs with tight SLAs • Passion for the...

- agreed label: `model-serving` · nice_to_have · raw_text: "building and scaling model serving tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_100 - skill `tensorflow` (spot-check)

> ...Experience with ML frameworks – like scikit-learn, LGBM, Tensorflow, PyTorch etc. • Experience with Big Data tools – Spark,...

- agreed label: `tensorflow` · nice_to_have · raw_text: "Tensorflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_101 - attribute `degree` (spot-check)

> AI DevOps Engineer Azure and GenAI Required Education-Bachelor's degree in Computer Science, Engineering, Information Technology, or a related discipline, or equivalent practical experience.Required Certification-Certifications: Microsoft Azure,...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor's degree in Computer Science, Engineering, Information Technology, or a related discipline, or equivalent practical experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_101 - attribute `german` (spot-check)

> AI DevOps Engineer Azure and GenAI

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_101 - attribute `seniority` (spot-check)

> ...MLOps, or AI engineering.Required Skills & Experience-7+ years in DevOps, platform engineering, cloud engineering, site reliability...

- agreed label: value="senior" · basis="inferred" · signal="7+ years in DevOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_101 - skill `apis` (spot-check)

> ...capacity and cost monitoring-Python; Bash; PowerShell; REST APIs; JSON/YAML; microservices; event-driven integration;...

- agreed label: `apis` · required · raw_text: "REST APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_101 - skill `azure-devops` (spot-check)

> ...AKS; API Management; Key Vault; Entra ID; Azure Monitor-Azure DevOps; Azure Boards; GitHub; GitHub Actions; Git; pull requests;...

- agreed label: `azure-devops` · required · raw_text: "Azure DevOps; Azure Boards"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_101 - skill `azure-key-vault` (spot-check)

> ...Azure Machine Learning; Azure OpenAI; AKS; API Management; Key Vault; Entra ID; Azure Monitor-Azure DevOps; Azure Boards;...

- agreed label: `azure-key-vault` · required · raw_text: "Key Vault"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_101 - skill `ci-cd` (spot-check)

> ...Azure environments and production delivery pipelines.-CI/CD & Source Control-Strong experience with Azure DevOps and/or GitHub: source...

- agreed label: `ci-cd` · required · raw_text: "CI/CD & Source Control"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_101 - skill `event-driven-systems` (spot-check)

> ...Bash; PowerShell; REST APIs; JSON/YAML; microservices; event-driven integration; Snowflake/Databricks familiarity-DevSecOps scanning;...

- agreed label: `event-driven-systems` · required · raw_text: "event-driven integration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_101 - skill `git` (spot-check)

> ...DevOps; Azure Boards; GitHub; GitHub Actions; Git; pull requests; pipeline-as-code; artifact repositories; release...

- agreed label: `git` · required · raw_text: "Git; pull requests"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_101 - skill `github-actions` (spot-check)

> ...ID; Azure Monitor-Azure DevOps; Azure Boards; GitHub; GitHub Actions; Git; pull requests; pipeline-as-code; artifact...

- agreed label: `github-actions` · required · raw_text: "GitHub Actions"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_101 - skill `gitops` (spot-check)

> ...Insights, Datadog, Dynatrace, Splunk, or equivalent).-GitOps/deployment tooling (Argo CD, Helm, or equivalent).-ServiceNow and enterprise...

- agreed label: `gitops` · nice_to_have · raw_text: "GitOps/deployment tooling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_101 - skill `linux` (spot-check)

> ...cloud-native templating (beneficial).-Docker, Kubernetes, Linux, networking, identity, secrets management, and cloud...

- agreed label: `linux` · required · raw_text: "Linux"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_101 - skill `llms` (spot-check)

> ...evidenceNice-to-Haves-Deploying/operating GenAI apps, LLM-powered services, AI agents, RAG, vector search, or shared enterprise AI...

- agreed label: `llms` · nice_to_have · raw_text: "LLM-powered services"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_101 - skill `microsoft-entra-id` (spot-check)

> ...Learning; Azure OpenAI; AKS; API Management; Key Vault; Entra ID; Azure Monitor-Azure DevOps; Azure Boards; GitHub; GitHub...

- agreed label: `microsoft-entra-id` · required · raw_text: "Entra ID"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_101 - skill `opentelemetry` (spot-check)

> ...operations; regression testing; safety and approval gates-Open Telemetry; logs, metrics, traces, dashboards, alerting; SLI/SLO...

- agreed label: `opentelemetry` · required · raw_text: "Open Telemetry"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_101 - skill `python` (spot-check)

> ...secrets management, and cloud security fundamentals.-Proficiency in Python plus scripting with Bash, PowerShell, or a comparable...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_101 - skill `rag` (spot-check)

> ...and agent evaluation; prompt and configuration versioning; RAG quality; model and endpoint operations; regression testing; safety...

- agreed label: `rag` · required · raw_text: "RAG quality"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_101 - skill `secrets-management` (spot-check)

> ...Kubernetes, Linux, networking, identity, secrets management, and cloud security fundamentals.-Proficiency in Python...

- agreed label: `secrets-management` · required · raw_text: "secrets management"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_101 - skill `vector-search` (spot-check)

> ...GenAI apps, LLM-powered services, AI agents, RAG, vector search, or shared enterprise AI platforms.-GenAIOps, MLOps,...

- agreed label: `vector-search` · nice_to_have · raw_text: "vector search"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_102 - attribute `german` (spot-check)

> Senior AI Platform & MLOps Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_102 - skill `databricks` (spot-check)

> ...strong experience with AI platforms like SageMaker, Databricks, and Terraform, along with MLflow for model management....

- agreed label: `databricks` · required · raw_text: "Databricks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_102 - skill `terraform` (spot-check)

> ...with AI platforms like SageMaker, Databricks, and Terraform, along with MLflow for model management. You will...

- agreed label: `terraform` · required · raw_text: "Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_103 - attribute `german` (spot-check)

> Forward-Deployed AI Engineer for Trading

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_104 - attribute `degree` (spot-check)

> AI/ML Engineer (Deep Learning, PyTorch) at Chime Chicago

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_104 - skill `aws` (spot-check)

> ...Strong Python and SQL, PyTorch and distributed compute • Knowledge of AWS, SageMaker, Airflow, Kafka, Redis or Snowflake Location...

- agreed label: `aws` · required · raw_text: "Knowledge of AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_104 - skill `evaluation` (spot-check)

> ...learning models in production • Solid ML fundamentals and evaluation design • Strong Python and SQL, PyTorch and distributed compute •...

- agreed label: `evaluation` · required · raw_text: "evaluation design"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_104 - skill `machine-learning` (spot-check)

> ...Experience deploying deep learning models in production • Solid ML fundamentals and evaluation design • Strong Python and SQL, PyTorch and...

- agreed label: `machine-learning` · required · raw_text: "Solid ML fundamentals"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_104 - skill `python` (spot-check)

> ...production • Solid ML fundamentals and evaluation design • Strong Python and SQL, PyTorch and distributed compute • Knowledge of...

- agreed label: `python` · required · raw_text: "Strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_104 - skill `pytorch` (spot-check)

> ...ML fundamentals and evaluation design • Strong Python and SQL, PyTorch and distributed compute • Knowledge of AWS, SageMaker,...

- agreed label: `pytorch` · required · raw_text: "SQL, PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_104 - skill `redis` (spot-check)

> ...compute • Knowledge of AWS, SageMaker, Airflow, Kafka, Redis or Snowflake Location and schedule • Chicago, IL • In...

- agreed label: `redis` · required · raw_text: "Redis"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_104 - skill `snowflake` (spot-check)

> ...compute • Knowledge of AWS, SageMaker, Airflow, Kafka, Redis or Snowflake Location and schedule • Chicago, IL • In office four days...

- agreed label: `snowflake` · required · raw_text: "Redis or Snowflake"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_105 - attribute `degree` (spot-check)

> ...and shipping ML systems, with focus on computer vision; BS/MS/PhD in CS, EE, or a related field, or equivalent experience. • Deep hands-on experience with object detection and...

- agreed label: value="phd" · requirement="required" · or_equivalent=true · signal="BS/MS/PhD in CS, EE, or a related field, or equivalent experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_105 - attribute `german` (spot-check)

> AI Engineer - US Remote

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_105 - attribute `seniority` (spot-check)

> ...monitoring, and iteration on real-world failures. • Evidence of staff-level impact: setting direction across teams, making sound...

- agreed label: value="senior" · basis="stated" · signal="Evidence of staff-level impact"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_105 - skill `model-serving` (spot-check)

> ...models from research to production: model optimization, inference serving, monitoring, and iteration on real-world failures. •...

- agreed label: `model-serving` · required · raw_text: "inference serving"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_105 - skill `observability` (spot-check)

> ...to production: model optimization, inference serving, monitoring, and iteration on real-world failures. • Evidence of...

- agreed label: `observability` · required · raw_text: "monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_105 - skill `pytorch` (spot-check)

> ...or a clear record in adjacent multimodal work. • Strong PyTorch skills and fluency with distributed training, mixed precision,...

- agreed label: `pytorch` · required · raw_text: "Strong PyTorch skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_105 - skill `reinforcement-learning` (spot-check)

> ...Experience with simulation, sim-to-real transfer, or reinforcement and imitation learning. • Edge and embedded deployment experience (TensorRT,...

- agreed label: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement and imitation learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_105 - skill `vllm` (spot-check)

> ...training). • Experience with LLM tooling such as vLLM, or with RLHF-style post-training for multimodal models. •...

- agreed label: `vllm` · nice_to_have · raw_text: "vLLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_106 - attribute `degree` (spot-check)

> Senior AI/ML Engineer — Hybrid, Impactful ML Solutions

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_106 - attribute `german` (spot-check)

> Senior AI/ML Engineer — Hybrid, Impactful ML Solutions

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_106 - attribute `seniority` (spot-check)

> Senior AI/ML Engineer — Hybrid, Impactful ML Solutions LHH in Chicago is...

- agreed label: value="senior" · basis="stated" · signal="Senior AI/ML Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_107 - attribute `german` (spot-check)

> W2 role - AI Lead Platform Engineer 12+ years local to IL required

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_107 - attribute `seniority` (spot-check)

> W2 role - AI Lead Platform Engineer 12+ years local to IL required Role: AI Lead Platform...

- agreed label: value="senior" · basis="stated" · signal="AI Lead Platform Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_108 - attribute `german` (spot-check)

> Slalom Flex (Project Based) AWS Agentic AI Engineer – Amazon Quick Suite

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 156. golden_108 - skill `agents` (spot-check)

> ...Amazon Quick Suite experience • Strong Python skills and experience building agents and LLM solutions across semantic and knowledge layers •...

- agreed label: `agents` · required · raw_text: "experience building agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 157. golden_108 - skill `aws` (spot-check)

> ...and engineers. What You’ll Bring Required • Senior/architect-level AWS expertise, with hands-on Amazon Quick Suite experience • Strong...

- agreed label: `aws` · required · raw_text: "Senior/architect-level AWS expertise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 158. golden_108 - skill `evaluation` (spot-check)

> ...knowledge layers • Bedrock agents, tool use, text-to-SQL, evaluation and guardrails • Snowflake, Iceberg, S3, Glue, Athena and IAM • Comfort...

- agreed label: `evaluation` · required · raw_text: "evaluation and guardrails"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 159. golden_108 - skill `git` (spot-check)

> ...SAP, JDE and M3 data concepts • Terraform/CloudFormation, Git, CI/CD, testing and Jira • Experience with the Atlan data...

- agreed label: `git` · nice_to_have · raw_text: "Git, CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 160. golden_108 - skill `llms` (spot-check)

> ...Strong Python skills and experience building agents and LLM solutions across semantic and knowledge layers • Bedrock agents,...

- agreed label: `llms` · required · raw_text: "LLM solutions"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 161. golden_108 - skill `power-bi` (spot-check)

> ...while staying highly organized and thoughtful Preferred • Power BI/DAX; SAP, JDE and M3 data concepts • Terraform/CloudFormation,...

- agreed label: `power-bi` · nice_to_have · raw_text: "Power BI/DAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 162. golden_108 - skill `snowflake` (spot-check)

> ...agents, tool use, text-to-SQL, evaluation and guardrails • Snowflake, Iceberg, S3, Glue, Athena and IAM • Comfort trying new techniques...

- agreed label: `snowflake` · required · raw_text: "Snowflake, Iceberg"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 163. golden_108 - skill `terraform` (spot-check)

> ...Power BI/DAX; SAP, JDE and M3 data concepts • Terraform/CloudFormation, Git, CI/CD, testing and Jira • Experience with the Atlan...

- agreed label: `terraform` · nice_to_have · raw_text: "Terraform/CloudFormation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 164. golden_108 - skill `testing` (spot-check)

> ...M3 data concepts • Terraform/CloudFormation, Git, CI/CD, testing and Jira • Experience with the Atlan data catalog • Certifications:...

- agreed label: `testing` · nice_to_have · raw_text: "testing and Jira"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
