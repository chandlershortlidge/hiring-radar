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

PROPOSED: A - Under rule 3, the only required content is in the 'What You Must Have' section (degree and years), and the AWS mention sits in the 'What Sets You Apart' section as one option among credentials, so nice_to_have (labeler A) is correct.

DECISION: A

## 17. golden_094 - skill `azure` (disagreement)

> ...visualization tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing...

- A: `azure` · nice_to_have · raw_text: "Azure"
- B: `azure` · required · raw_text: "Azure"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1 the only Azure mention sits inside the 'What Sets You Apart' section, which is the preferred tier and not 'What You Must Have', so under rule 3 no required mention exists and nice_to_have fits; the credential is also just one option among several cloud platforms.

DECISION: A

## 18. golden_094 - skill `cloud` (disagreement)

> ...(Databricks, MS SQL), visualization tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing...

- A: `cloud` · nice_to_have · raw_text: "cloud platforms (AWS, Azure, GCP)"
- B: `cloud` · required · raw_text: "cloud platforms"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1 the cloud mention sits in the 'What Sets You Apart' section as one option in an 'at least one of the following' credential list, so it is nice_to_have, not required (rule 3 does not apply because no required mention exists).

DECISION: A

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

PROPOSED: A - Under rule 1 the visualization skill is named only in the 'What Sets You Apart' preference section, as one option among several credentials, and the 'What You Must Have' list does not mention it, so under rule 3 no required mention exists and nice_to_have with Labeler A's raw_text is correct.

DECISION: A

## 21. golden_094 - skill `databricks` (disagreement)

> ...least one of the following: a Certification in databases (Databricks, MS SQL), visualization tools (Power BI), cloud platforms...

- A: `databricks` · nice_to_have · raw_text: "Databricks"
- B: `databricks` · required · raw_text: "Databricks"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1 the Databricks mention counts because it sits in a qualification bullet, but it appears under the 'What Sets You Apart' preference section as one option in an 'at least one of the following' credential list, so it is nice_to_have, not a required mention (rule 3 does not apply).

DECISION: A

## 22. golden_094 - skill `gcp` (disagreement)

> ...tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing...

- A: `gcp` · nice_to_have · raw_text: "GCP"
- B: `gcp` · required · raw_text: "GCP"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 3, the only GCP mention sits in the "What Sets You Apart" section as one option among alternative cloud certifications (AWS, Azure, GCP), not in "What You Must Have," so nice_to_have is correct (rule 1 applies since it names a skill in a qualification line).

DECISION: A

## 23. golden_094 - skill `knowledge-graphs` (disagreement)

> ...experience in ontology development and management - Designing and implementing knowledge graphs using technologies such as RDF, OWL, SPARQL, or similar -...

- A: `knowledge-graphs` · nice_to_have · raw_text: "Designing and implementing knowledge graphs"
- B: `knowledge-graphs` · required · raw_text: "Designing and implementing knowledge graphs"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1 the knowledge-graphs bullet is a qualification, but it sits under the heading "What Sets You Apart" and the surrounding text is framed as a preference, so it is nice_to_have rather than required, and rule 3 does not apply because no other required mention appears in the excerpt.

DECISION: A

## 24. golden_094 - skill `machine-learning` (disagreement)

> ...tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing governance frameworks and data...

- A: `machine-learning` · nice_to_have · raw_text: "predictive modeling/ML"
- B: `machine-learning` · required · raw_text: "predictive modeling/ML"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1 the ML mention sits in the 'What Sets You Apart' section, not 'What You Must Have', and rule 3 finds no required mention, so nice_to_have (labeler A) is correct.

DECISION: A

## 25. golden_094 - skill `power-bi` (disagreement)

> ...in databases (Databricks, MS SQL), visualization tools (Power BI), cloud platforms (AWS, Azure, GCP), or predictive...

- A: `power-bi` · nice_to_have · raw_text: "Power BI"
- B: `power-bi` · required · raw_text: "Power BI"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1 the Power BI mention sits in the 'What Sets You Apart' preferred block, not 'What You Must Have', and it is one option in an 'at least one of' credential list, so under rule 3 no required mention exists and it is nice_to_have.

DECISION: A

## 26. golden_094 - skill `python` (disagreement)

> ...platforms (AWS, Azure, GCP), or predictive modeling/ML (Python, SAS) - Designing governance frameworks and data...

- A: `python` · nice_to_have · raw_text: "Python"
- B: `python` · required · raw_text: "Python"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, Python appears only in the "What Sets You Apart" section as one option in a certification list for a stated preference, not in "What You Must Have," so rule 3 does not make it required and nice_to_have (labeler A) is correct.

DECISION: A

## 27. golden_094 - skill `sql` (disagreement)

> ...the following: a Certification in databases (Databricks, MS SQL), visualization tools (Power BI), cloud platforms (AWS,...

- A: `sql` · nice_to_have · raw_text: "MS SQL"
- B: `sql` · required · raw_text: "MS SQL"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1 the MS SQL mention sits inside the 'What Sets You Apart' list, and it is one option among several certifications ('at least one of the following'), so it is a preference rather than a requirement, which makes nice_to_have correct under rule 3.

DECISION: A

## 28. golden_095 - skill `ai-infrastructure` (disagreement)

> ...Demonstrated hands- on experience delivering end-to-end ML systems, spanning model development, deployment, and production infrastructure • Proficiency with modern ML engineering tooling,...

- A: (did not label this)
- B: `ai-infrastructure` · required · raw_text: "ML systems, spanning model development, deployment, and production infrastructure"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualification sentence ("Demonstrated hands-on experience delivering end-to-end ML systems, spanning model development, deployment, and production infrastructure") names ML production infrastructure as a required skill, and B's raw_text quotes that wording verbatim.

DECISION: B

## 29. golden_097 - skill `ai-infrastructure` (disagreement)

> ...be on Python across backend services, data pipelines, and ML infrastructure, with collaboration from researchers to refine AI-driven...

- A: `ai-infrastructure` · required · raw_text: "ML infrastructure"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 4, "ML infrastructure" appears only in the role's focus/work description ("Focus will be on...") and in the section title, which rule 1 excludes, and the posting never asks the candidate to have ML infrastructure experience, so the required tag isn't supported.

DECISION: drop

## 30. golden_097 - skill `backend-development` (disagreement)

> ...large language models. Focus will be on Python across backend services, data pipelines, and ML infrastructure, with collaboration...

- A: `backend-development` · required · raw_text: "backend services"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 4, "Focus will be on Python across backend services" describes what the evaluator will work on, not a qualification the candidate must hold, so the required backend-development tag isn't supported.

DECISION: drop

## 31. golden_097 - skill `data-pipelines` (disagreement)

> ...models. Focus will be on Python across backend services, data pipelines, and ML infrastructure, with collaboration from...

- A: `data-pipelines` · required · raw_text: "data pipelines"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 4, "Focus will be on Python across backend services, data pipelines, and ML infrastructure" describes the work the role will do, not a qualification the candidate must already have, and the only candidate requirement here is communication skills.

DECISION: drop

## 32. golden_097 - skill `python` (disagreement)

> AI-Driven Full Stack Engineer (Python & ML Infra) Turing is seeking a Software Engineering Evaluator to...

- A: `python` · required · raw_text: "Python & ML Infra"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: {"requirement": "required", "raw_text": "Focus will be on Python across backend services"} - Under rule 1 the title fragment "Python & ML Infra" does not count, so I anchor python to the body sentence naming Python as the focus of the evaluator's work, and I keep it required under rule 3.

DECISION: ?

## 33. golden_098 - skill `ai-ml` (disagreement)

> ...Python, JavaScript/Node.js, HTML5, CSS, and SQL/BigQuery AI & LLM Engineering to design and develop machine learning applications and...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI & LLM Engineering"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'Specific Knowledge and Skills' list is a qualification section that names AI & LLM engineering (machine learning applications and language generation systems), and rule 3 makes that required mention count, so labeler B's ai-ml tag with that raw_text stands.

DECISION: B

## 34. golden_098 - skill `workflow-automation` (disagreement)

> ...present solutions across diverse audiences Experience with Google Docs automation preferred Proficiency with IDEs such as VSCode, Microsoft Office,...

- A: (did not label this)
- B: `workflow-automation` · nice_to_have · raw_text: "Google Docs automation preferred"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualification sentence "Experience with Google Docs automation preferred" names an automation skill, and rule 3 supports B's nice_to_have tag because the quoted raw_text is the word-for-word "preferred" mention.

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

PROPOSED: drop - Under rule 5, "financial/tax automation" in the Bonus line names a finance/tax domain, not a workflow-automation skill, so the broader skill is not named by the text and should not be added.

DECISION: drop

## 37. golden_100 - skill `model-development` (disagreement)

> ...to build scalable and efficient data pipelines and model training and deployment systems • Develop and maintain monitoring...

- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "model training"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Rule 4 applies: "model training" appears only in the "In This Role, You'll Get to:" responsibilities bullets, and the visible excerpt does not ask the candidate for model development skills.

DECISION: drop

## 38. golden_101 - skill `agents` (disagreement)

> ...GenAI apps, LLM-powered services, AI agents, RAG, vector search, or shared enterprise AI...

- A: `agents` · nice_to_have · raw_text: "AI agents"
- B: `agents` · required · raw_text: "agent evaluation"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 3, B's required claim rests on the phrase "agent evaluation," which does not appear in the visible posting, while A's "AI agents" appears verbatim in the Nice-to-Haves section, so the nice_to_have ruling is the one the text supports.

DECISION: A

## 39. golden_101 - skill `ai-deployment` (disagreement)

> ...management; audit evidenceNice-to-Haves-Deploying/operating GenAI apps, LLM-powered services, AI agents, RAG, vector search, or...

- A: (did not label this)
- B: `ai-deployment` · nice_to_have · raw_text: "Deploying/operating GenAI apps"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the Nice-to-Haves bullet "Deploying/operating GenAI apps, LLM-powered services..." names the skill directly, and B's raw_text quotes that wording exactly, so the nice_to_have tag stands.

DECISION: B

## 40. golden_101 - skill `llmops` (disagreement)

> ...RAG, vector search, or shared enterprise AI platforms.-GenAIOps, MLOps, AgentOps, model/endpoint lifecycle management,...

- A: (did not label this)
- B: `llmops` · nice_to_have · raw_text: "GenAIOps"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the Nice-to-Haves bullet literally names "GenAIOps" as a qualification, so llmops applies at nice_to_have, and no required mention of it appears elsewhere in the visible excerpt (rule 3 doesn't override).

DECISION: B

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

PROPOSED: A - Under rule 1, the qualification list names "Azure OpenAI" as a required technology, and rule 3 makes that required mention win, so openai-api stands as labeled by A.

DECISION: A

## 43. golden_105 - skill `ai-ml` (disagreement)

> ...us immediately at IT-Security@Maneva.ai. Remote Skills: Artificial Intelligence (AI), Benchmarking, CUDA (Compute Unified Device Architecture),...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Artificial Intelligence (AI)"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the skills list explicitly names "Artificial Intelligence (AI)" under the posting's Skills heading, which counts as a skill mention, and rule 5 is satisfied because ai-ml is named rather than inferred, so labeler B's required-level label stands.

DECISION: B

## 44. golden_105 - skill `cloud` (disagreement)

> ...Benchmarking, CUDA (Compute Unified Device Architecture), Cloud Computing, Code Reviews, Computer Vision, Customer Satisfaction,...

- A: (did not label this)
- B: `cloud` · required · raw_text: "Cloud Computing"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the "Skills:" section names "Cloud Computing" as a skill the candidate is asked for, so the cloud label stands, and rule 3 supports it as required since the posting lists it as a skill without marking it optional.

DECISION: B

## 45. golden_105 - skill `cuda` (disagreement)

> ...Edge and embedded deployment experience (TensorRT, CUDA, quantization-aware training). • Experience with LLM...

- A: `cuda` · nice_to_have · raw_text: "CUDA"
- B: `cuda` · required · raw_text: "CUDA (Compute Unified Device Architecture)"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 3, the quoted mention sits in the "Nice to have" section, so nice_to_have is correct, and B's raw_text "CUDA (Compute Unified Device Architecture)" does not appear in the posting; rule 5 rules out adding anything beyond what the text names.

DECISION: A

## 46. golden_105 - skill `model-development` (disagreement)

> ...segmentation (YOLO family, DETR-style models), including training, tuning, and production deployment. • Hands-on experience...

- A: (did not label this)
- B: `model-development` · required · raw_text: "training"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the requirement bullet "Deep hands-on experience with object detection and segmentation... including training, tuning, and production deployment" names model training as a qualification, and rule 3 says a required mention wins, so labeler B's required model-development with raw_text "training" stands.

DECISION: ?

## 47. golden_094 - attribute `seniority` (uncertain)

> ...and address complex business questions. As a Manager, you will lead client workstreams with accountability for planning, budgets, timelines, and...

- A: value="senior" · basis="inferred" · signal="you will lead client workstreams"
- B: value="senior" · basis="inferred" · signal="you will lead client workstreams"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the posting's explicit 'As a Manager, you will lead client workstreams with accountability for planning, budgets, timelines, and deliverables' supports a senior-level seniority, so the agreed 'senior' value stands, though the truncated title and inferred basis leave some doubt.

DECISION: ok

## 48. golden_095 - skill `ai-deployment` (uncertain)

> ...foundations • Demonstrated hands- on experience delivering end-to-end ML systems, spanning model development, deployment, and production infrastructure • Proficiency with modern...

- A: `ai-deployment` · required · raw_text: "end-to-end ML systems, spanning model development, deployment"
- B: `ai-deployment` · required · raw_text: "ML systems, spanning model development, deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required bullet 'Demonstrated hands-on experience delivering end-to-end ML systems, spanning model development, deployment' under 'Experience Required' names deployment as a qualification, and the agreed raw_text appears verbatim, so the required label stands (rule 3).

DECISION: ok

## 49. golden_095 - skill `machine-learning` (uncertain)

> ...Learning, or a related field • 5+ years of experience building and operating machine learning solutions in cloud environments, with focus on AI services and MLOps...

- A: `machine-learning` · required · raw_text: "building and operating machine learning solutions"
- B: `machine-learning` · required · raw_text: "building and operating machine learning solutions"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet ('5+ years of experience building and operating machine learning solutions') names machine learning as a skill rather than only a job title, and rule 3 makes that required mention the determining one, so the agreed label stands.

DECISION: ok

## 50. golden_095 - skill `model-serving` (uncertain)

> ...Experience Preferred • Experience designing and scaling real-time and batch inference systems in production • Hands- on experience with deep learning frameworks and...

- A: `model-serving` · nice_to_have · raw_text: "real-time and batch inference systems in production"
- B: `model-serving` · nice_to_have · raw_text: "designing and scaling real-time and batch inference systems in production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Experience Preferred' bullet names designing and scaling real-time and batch inference systems in production, which supports model-serving as nice_to_have, and the quoted raw_text appears verbatim in the posting.

DECISION: ok

## 51. golden_096 - attribute `seniority` (uncertain)

> ...own end-to-end AI projects from discovery to production, leading architecture, testing, and governance efforts. Responsibilities include prototyping AI workflows,...

- A: value="senior" · basis="inferred" · signal="leading architecture, testing, and governance efforts"
- B: value="senior" · basis="inferred" · signal="leading architecture, testing, and governance efforts"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 4, the only support for seniority is responsibilities ('You'll own end-to-end AI projects', 'leading architecture...'), and the posting never asks the candidate for a seniority level, title, or years of experience, so the attribute should be null.

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

PROPOSED: ok - Under rule 1, the 'Specific Knowledge and Skills' bullet names 'Cloud & API Architecture' and asks the candidate to implement REST APIs, which is building APIs rather than just consuming them (rule 2), and the raw_text 'API Architecture' appears verbatim in the posting.

DECISION: ok

## 54. golden_098 - skill `gemini` (uncertain)

> ...using Agile methodologies, Git workflows, GitHub, and AI coding assistants such as Gemini or Windsurf Technical Communication to translate complex...

- A: `gemini` · required · raw_text: "AI coding assistants such as Gemini"
- B: `gemini` · required · raw_text: "Gemini"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification sentence names Gemini as a tool the candidate must use ("collaborate using ... AI coding assistants such as Gemini or Windsurf"), and it is not marked preferred, so the required label and quoted raw_text stand under rule 3.

DECISION: ok

## 55. golden_098 - skill `software-engineering` (uncertain)

> ...permit sponsorship is not available for this position. Software Development to design, build, and deploy applications utilizing Python, JavaScript/Node.js, HTML5, CSS, and...

- A: `software-engineering` · required · raw_text: "Software Development to design, build, and deploy applications"
- B: `software-engineering` · required · raw_text: "Software Development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Specific Knowledge and Skills' list is a qualification section that names software development as a skill, and the agreed raw_text quotes it word for word, so the required software-engineering label stands (rules 1 and 3).

DECISION: ok

## 56. golden_099 - attribute `seniority` (uncertain)

> ...like IRS form completion. • Lead & Future-Proof: Guide offshore mid-level engineers through code reviews and architectural alignment, while building Model Context Protocol (MCP) servers to...

- A: value="senior" · basis="inferred" · signal="Guide offshore mid-level engineers through code reviews and architectural alignment"
- B: value="senior" · basis="inferred" · signal="Guide offshore mid-level engineers through code reviews and architectural alignment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 4, the only signal for "senior" is the "Lead & Future-Proof" bullet under What You'll Do, which is a responsibility the candidate is not asked to have, and the only stated requirement is 3+ years, which does not support senior on its own, so the attribute should be null.

DECISION: ?

## 57. golden_099 - skill `backend-development` (uncertain)

> ...Fabric, Snowflake, or Databricks). • Proven experience supporting the data backend for active, production AI applications and unstructured...

- A: `backend-development` · required · raw_text: "supporting the data backend"
- B: `backend-development` · required · raw_text: "supporting the data backend"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification 'Proven experience supporting the data backend for active, production AI applications' names backend work, and the agreed required label with that raw_text is supported by the posting.

DECISION: ?

## 58. golden_099 - skill `cloud` (uncertain)

> ...Strong proficiency in Python, Microsoft Azure, and modern cloud data platforms (Microsoft Fabric, Snowflake, or Databricks). • Proven...

- A: `cloud` · required · raw_text: "modern cloud data platforms"
- B: `cloud` · required · raw_text: "modern cloud data platforms"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet ('Strong proficiency in Python, Microsoft Azure, and modern cloud data platforms') names cloud, and rule 3 says the required mention wins, so the agreed required `cloud` label stands.

DECISION: ok

## 59. golden_099 - skill `mcp` (uncertain)

> ...tools and strong cross-cultural communication skills. • Bonus: Experience with MCP servers/connectors, Streamlit/React, financial/tax automation, or mentoring...

- A: `mcp` · nice_to_have · raw_text: "Bonus: Experience with MCP servers/connectors"
- B: `mcp` · nice_to_have · raw_text: "MCP servers/connectors"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Bonus: Experience with MCP servers/connectors' bullet under What You Bring names MCP as a qualification, and the agreed nice_to_have requirement and verbatim raw_text match that bonus line.

DECISION: ok

## 60. golden_099 - skill `react` (uncertain)

> ...skills. • Bonus: Experience with MCP servers/connectors, Streamlit/React, financial/tax automation, or mentoring offshore...

- A: `react` · nice_to_have · raw_text: "Streamlit/React"
- B: `react` · nice_to_have · raw_text: "React"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Bonus: Experience with ... Streamlit/React' bullet sits in the 'What You Bring' qualifications and names React, so tagging react as nice_to_have with raw_text "Streamlit/React" is supported and the verbatim quote checks out.

DECISION: ok

## 61. golden_099 - skill `streamlit` (uncertain)

> ...skills. • Bonus: Experience with MCP servers/connectors, Streamlit/React, financial/tax automation, or mentoring offshore...

- A: `streamlit` · nice_to_have · raw_text: "Streamlit/React"
- B: `streamlit` · nice_to_have · raw_text: "Streamlit"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Bonus:' qualification bullet names Streamlit, so it counts as a nice_to_have, and the raw_text "Streamlit/React" appears verbatim in the posting.

DECISION: ok

## 62. golden_100 - skill `ai-deployment` (uncertain)

> ...to build scalable and efficient data pipelines and model training and deployment systems • Develop and maintain monitoring and management tools to...

- A: `ai-deployment` · nice_to_have · raw_text: "model training and deployment systems"
- B: `ai-deployment` · nice_to_have · raw_text: "model training and deployment systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 4, the quoted phrase "model training and deployment systems" sits in the "In This Role, You'll Get to:" responsibilities list, and nothing shown asks the candidate for this skill, so it does not support a nice_to_have requirement.

DECISION: drop

## 63. golden_100 - skill `apache-spark` (uncertain)

> ...PyTorch etc. • Experience with Big Data tools – Spark, S3, Hadoop • Strong knowledge of containerization and...

- A: `apache-spark` · nice_to_have · raw_text: "Spark"
- B: `apache-spark` · nice_to_have · raw_text: "Spark"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'It's Great if you have' bullet 'Experience with Big Data tools – Spark, S3, Hadoop' names Spark as a qualification, so the agreed nice_to_have label and the verbatim raw_text 'Spark' are correct.

DECISION: ok

## 64. golden_100 - skill `aws-s3` (uncertain)

> ...PyTorch etc. • Experience with Big Data tools – Spark, S3, Hadoop • Strong knowledge of containerization and...

- A: `aws-s3` · nice_to_have · raw_text: "S3"
- B: `aws-s3` · nice_to_have · raw_text: "S3"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the nice-to-have bullet 'Experience with Big Data tools – Spark, S3, Hadoop' names S3 as a tool the candidate should have, and 'S3' is the AWS S3 service, so the agreed aws-s3 tag, nice_to_have requirement, and raw_text 'S3' are supported as they stand.

DECISION: ok

## 65. golden_100 - skill `hadoop` (uncertain)

> ...etc. • Experience with Big Data tools – Spark, S3, Hadoop • Strong knowledge of containerization and container...

- A: `hadoop` · nice_to_have · raw_text: "Hadoop"
- B: `hadoop` · nice_to_have · raw_text: "Hadoop"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the "It's Great if you have" bullet "Experience with Big Data tools – Spark, S3, Hadoop" names Hadoop explicitly as a nice-to-have qualification, so the agreed label and raw_text stand.

DECISION: ok

## 66. golden_100 - skill `machine-learning` (uncertain)

> ...with MLOps platforms, such as Kubeflow or MLFlow • Experience with ML frameworks – like scikit-learn, LGBM, Tensorflow, PyTorch etc. •...

- A: `machine-learning` · nice_to_have · raw_text: "Experience with ML frameworks"
- B: `machine-learning` · nice_to_have · raw_text: "ML frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Rule 1 applies: the nice-to-have bullet "Experience with ML frameworks" in the "It's Great if you have" section names an ML skill, and "machine learning" also appears in the posting, so the agreed nice_to_have label with that raw_text stands.

DECISION: ok

## 67. golden_100 - skill `mlops` (uncertain)

> ...and debugging user issues What You’ll Need to Succeed • 5+ years of experience in MLOps, Software engineering, Data engineering, or a related...

- A: `mlops` · required · raw_text: "5+ years of experience in MLOps"
- B: `mlops` · required · raw_text: "5+ years of experience in MLOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only required mention of MLOps is the years-of-experience line "5+ years of experience in MLOps," which does not count, and the other MLOps mentions are responsibilities, which rule 4 excludes.

DECISION: ?

## 68. golden_100 - skill `observability` (uncertain)

> ...training and deployment systems • Develop and maintain monitoring and management tools to ensure the reliability and performance of our...

- A: `observability` · nice_to_have · raw_text: "monitoring and management tools"
- B: `observability` · nice_to_have · raw_text: "monitoring and management tools"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 4, the only visible mention of monitoring is in the 'In This Role, You'll Get to' responsibilities list, and the qualifications section is cut off, so the posting does not show the candidate being asked for observability.

DECISION: drop

## 69. golden_100 - skill `software-engineering` (uncertain)

> ...workflows. Our AI Ops team combines the best practices of software engineering with data science to help Machine Learning Engineers and...

- A: `software-engineering` · required · raw_text: "Software engineering"
- B: `software-engineering` · required · raw_text: "Software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only visible mention of software engineering describes the AI Ops team's practices ('combines the best practices of software engineering with data science'), not a skill the candidate is asked for, and rule 4 excludes responsibilities unless the candidate is also asked for the skill; the visible excerpt has no qualification sentence requiring it.

DECISION: drop

## 70. golden_101 - skill `azure-ai-foundry` (uncertain)

> ...stakeholders in a regulated enterprise environment.-Azure; Microsoft Foundry / Azure AI services; Azure Machine Learning; Azure OpenAI; AKS; API...

- A: `azure-ai-foundry` · required · raw_text: "Microsoft Foundry / Azure AI services"
- B: `azure-ai-foundry` · required · raw_text: "Microsoft Foundry"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification list names "Microsoft Foundry / Azure AI services" as a skill, and the excerpt gives no sign it is optional, so the agreed required label stands under rule 3.

DECISION: ok

## 71. golden_101 - skill `cloud` (uncertain)

> ...& Experience-7+ years in DevOps, platform engineering, cloud engineering, site reliability engineering, software engineering, or a...

- A: `cloud` · required · raw_text: "cloud engineering"
- B: `cloud` · required · raw_text: "cloud engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"requirement": "required", "raw_text": "cloud security fundamentals"} - Under rule 1, the agreed raw_text "cloud engineering" sits in a years-of-experience line and doesn't count, but the required list under "Required Skills & Experience" names "cloud security fundamentals", which supports a required cloud mention under rule 3.

DECISION: ?

## 72. golden_101 - skill `cybersecurity` (uncertain)

> ...Linux, networking, identity, secrets management, and cloud security fundamentals.-Proficiency in Python plus scripting with Bash,...

- A: `cybersecurity` · required · raw_text: "cloud security fundamentals"
- B: `cybersecurity` · required · raw_text: "cloud security fundamentals"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet names "cloud security fundamentals" in its list of skills, which supports the agreed cybersecurity label with that raw_text, and rule 5 does not block it because the security skill is actually named.

DECISION: ok

## 73. golden_101 - skill `databricks` (uncertain)

> ...APIs; JSON/YAML; microservices; event-driven integration; Snowflake/Databricks familiarity-DevSecOps scanning; secrets management; identity and...

- A: `databricks` · required · raw_text: "Snowflake/Databricks familiarity"
- B: `databricks` · required · raw_text: "Databricks familiarity"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, "Snowflake/Databricks familiarity" sits in the main qualifications list above the Nice-to-Haves heading, so it is a required skill mention that rule 3 keeps as agreed.

DECISION: ok

## 74. golden_101 - skill `devops` (uncertain)

> ...MLOps, or AI engineering.Required Skills & Experience-7+ years in DevOps, platform engineering, cloud engineering, site reliability...

- A: `devops` · required · raw_text: "7+ years in DevOps"
- B: `devops` · required · raw_text: "Certifications: Microsoft Azure, GitHub, Kubernetes, Terraform, DevOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"requirement": "required", "raw_text": "Certifications: Microsoft Azure, GitHub, Kubernetes, Terraform, DevOps, MLOps, or AI engineering"} - Under rule 1 the years-of-experience line ('7+ years in DevOps') does not count, but the section headed 'Required Certification' names DevOps, so the skill stays and the raw_text is re-quoted from that required mention (rule 3).

DECISION: {"requirement": "required", "raw_text": "Certifications: Microsoft Azure, GitHub, Kubernetes, Terraform, DevOps, MLOps, or AI engineering"}

## 75. golden_101 - skill `snowflake` (uncertain)

> ...APIs; JSON/YAML; microservices; event-driven integration; Snowflake/Databricks familiarity-DevSecOps scanning; secrets management; identity and...

- A: `snowflake` · required · raw_text: "Snowflake/Databricks familiarity"
- B: `snowflake` · required · raw_text: "Snowflake"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, "Snowflake/Databricks familiarity" sits in the required list before the Nice-to-Haves heading and names Snowflake, so the required snowflake tag and its verbatim raw_text stand (rule 3).

DECISION: ok

## 76. golden_101 - skill `software-engineering` (uncertain)

> ...cloud engineering, site reliability engineering, software engineering, or a related discipline.-3+ years of hands-on experience building and supporting...

- A: `software-engineering` · required · raw_text: "software engineering, or a related discipline"
- B: `software-engineering` · required · raw_text: "software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only mention of software engineering is inside a years-of-experience line ('7+ years in DevOps, ... software engineering, or a related discipline'), which does not count as a named skill.

DECISION: drop

## 77. golden_104 - skill `ai-deployment` (uncertain)

> ...Contribute to the shared ML platform Requirements • Experience deploying deep learning models in production • Solid ML fundamentals and evaluation design • Strong...

- A: `ai-deployment` · required · raw_text: "Experience deploying deep learning models in production"
- B: `ai-deployment` · required · raw_text: "deploying deep learning models in production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Requirements bullet "Experience deploying deep learning models in production" names the skill as a qualification, and rule 3 makes that required mention the determining one, so the agreed label stands.

DECISION: ok

## 78. golden_104 - skill `distributed-systems` (uncertain)

> ...and evaluation design • Strong Python and SQL, PyTorch and distributed compute • Knowledge of AWS, SageMaker, Airflow, Kafka, Redis or...

- A: `distributed-systems` · required · raw_text: "distributed compute"
- B: `distributed-systems` · required · raw_text: "distributed compute"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, "distributed compute" sits in the Requirements list as a candidate qualification, and under rule 3 that required mention is the determining quote, so the agreed required `distributed-systems` label stands.

DECISION: ok

## 79. golden_105 - skill `ai-deployment` (uncertain)

> ...DETR-style models), including training, tuning, and production deployment. • Hands-on experience with VLMs (for example LLaVA-,...

- A: `ai-deployment` · required · raw_text: "production deployment"
- B: `ai-deployment` · required · raw_text: "production deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet names production deployment of ML models ('training, tuning, and production deployment'), and rule 3 makes that required mention decisive, so the agreed required label stands.

DECISION: ok

## 80. golden_105 - skill `inference-optimization` (uncertain)

> ...Track record of taking models from research to production: model optimization, inference serving, monitoring, and iteration on...

- A: `inference-optimization` · required · raw_text: "model optimization"
- B: `inference-optimization` · required · raw_text: "model optimization"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1 the bullet is a required qualification, and under rule 3 the quoted "model optimization" sits beside "inference serving" in a production-deployment track-record requirement, so inference-optimization is supported as agreed.

DECISION: ok

## 81. golden_105 - skill `llms` (uncertain)

> ...CUDA, quantization-aware training). • Experience with LLM tooling such as vLLM, or with RLHF-style post-training for...

- A: `llms` · nice_to_have · raw_text: "LLM tooling"
- B: `llms` · nice_to_have · raw_text: "LLM tooling"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet names LLM tooling (vLLM) as a skill, and it sits under the 'Nice to have' heading, so nice_to_have and the quoted raw_text 'LLM tooling' are supported as agreed.

DECISION: ok

## 82. golden_105 - skill `machine-learning` (uncertain)

> ...product. Requirements What we're looking for • 5+ years building and shipping ML systems, with focus on computer vision; BS/MS/PhD in CS, EE, or a...

- A: `machine-learning` · required · raw_text: "building and shipping ML systems"
- B: `machine-learning` · required · raw_text: "ML systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the requirements bullet "5+ years building and shipping ML systems, with focus on computer vision" names machine learning as a qualification the candidate must have, and the years framing describes the ML work itself rather than a job title, so the agreed required label stands.

DECISION: ok

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

PROPOSED: ok - Under rule 1, the Required qualification bullet names guardrails directly ('evaluation and guardrails'), and the agreed requirement level and raw_text match the posting verbatim.

DECISION: ok

## 85. golden_094 - attribute `degree` (spot-check)

> ...risks to clients and project leaders What You Must Have - At least a Bachelor's degree - At least 4 years of experience What Sets You Apart -...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="At least a Bachelor's degree"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The only degree level named is "At least a Bachelor's degree" in the requirements list, so under the lowest-level rule the label `bachelor`, `required`, `or_equivalent=false`, with that exact signal, is correct as it stands.

DECISION: ok

## 86. golden_094 - attribute `german` (spot-check)

> The Opportunity

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 87. golden_095 - skill `data-pipelines` (spot-check)

> ...modern ML engineering tooling, including cloud platforms, data pipelines, and CI/CD workflows Experience Preferred • Experience...

- agreed label: `data-pipelines` · required · raw_text: "data pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_095 - skill `deep-learning` (spot-check)

> ...systems in production • Hands- on experience with deep learning frameworks and model optimization for performance and cost •...

- agreed label: `deep-learning` · nice_to_have · raw_text: "deep learning frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_095 - skill `mlops` (spot-check)

> ...learning solutions in cloud environments, with focus on AI services and MLOps foundations • Demonstrated hands- on experience delivering end-to-end...

- agreed label: `mlops` · required · raw_text: "AI services and MLOps foundations"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_095 - skill `model-development` (spot-check)

> ...on experience delivering end-to-end ML systems, spanning model development, deployment, and production infrastructure • Proficiency...

- agreed label: `model-development` · required · raw_text: "model development"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 91. golden_096 - attribute `degree` (spot-check)

> Forward Deployed AI Engineer — Global Impact

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting mentions no degree or qualification level anywhere, so under the rule ('one label per posting, or none (`null`) when no degree is mentioned') the agreed null value is correct.

DECISION: ok

## 92. golden_097 - attribute `degree` (spot-check)

> AI-Driven Full Stack Engineer (Python & ML Infra)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree or level anywhere, and the degree rule says the label is none (`null`) when no degree is mentioned, which matches the agreed null label.

DECISION: ok

## 93. golden_098 - attribute `degree` (spot-check)

> ...and system performance Specific Knowledge and Skills Bachelor's Degree 2+ years of experience in software development Legal...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="Bachelor's Degree"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The only degree level named is "Bachelor's Degree", listed bare under Specific Knowledge and Skills and Basic Requirements, so under the degree rule it is `bachelor`, `required`, with no equivalent-experience wording, and the signal quotes the posting exactly.

DECISION: ok

## 94. golden_098 - skill `cloud` (spot-check)

> ...learning applications and language generation systems Cloud & API Architecture to implement complex service-to-service OAuth2...

- agreed label: `cloud` · required · raw_text: "Cloud & API Architecture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_098 - skill `gcp` (spot-check)

> ...OAuth2 authentication flows and REST APIs across Google Cloud and AWS Database Management to design, deploy, maintain,...

- agreed label: `gcp` · required · raw_text: "Google Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 96. golden_098 - skill `git` (spot-check)

> ...Tooling to collaborate using Agile methodologies, Git workflows, GitHub, and AI coding assistants such as Gemini or Windsurf...

- agreed label: `git` · required · raw_text: "Git workflows, GitHub"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 97. golden_098 - skill `llms` (spot-check)

> ...Python, JavaScript/Node.js, HTML5, CSS, and SQL/BigQuery AI & LLM Engineering to design and develop machine learning applications and...

- agreed label: `llms` · required · raw_text: "AI & LLM Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_098 - skill `node-js` (spot-check)

> ...design, build, and deploy applications utilizing Python, JavaScript/Node.js, HTML5, CSS, and SQL/BigQuery AI & LLM Engineering to...

- agreed label: `node-js` · required · raw_text: "JavaScript/Node.js"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_098 - skill `oauth` (spot-check)

> ...& API Architecture to implement complex service-to-service OAuth2 authentication flows and REST APIs across Google Cloud and AWS Database...

- agreed label: `oauth` · required · raw_text: "OAuth2 authentication flows"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_099 - attribute `german` (spot-check)

> AI Data Engineer (remote)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_099 - skill `azure` (spot-check)

> ...of experience as a Data Engineer. • Strong proficiency in Python, Microsoft Azure, and modern cloud data platforms (Microsoft Fabric,...

- agreed label: `azure` · required · raw_text: "Python, Microsoft Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_099 - skill `databricks` (spot-check)

> ...modern cloud data platforms (Microsoft Fabric, Snowflake, or Databricks). • Proven experience supporting the data backend for...

- agreed label: `databricks` · required · raw_text: "or Databricks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_099 - skill `python` (spot-check)

> ...You Bring • 3+ years of experience as a Data Engineer. • Strong proficiency in Python, Microsoft Azure, and modern cloud data platforms...

- agreed label: `python` · required · raw_text: "Strong proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 104. golden_099 - skill `snowflake` (spot-check)

> ...Azure, and modern cloud data platforms (Microsoft Fabric, Snowflake, or Databricks). • Proven experience supporting the data...

- agreed label: `snowflake` · required · raw_text: "Snowflake"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 105. golden_100 - attribute `degree` (spot-check)

> [Data Engineer] Senior / Staff MLOps Engineer (Bangkok Based, relocation provided)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree or degree level anywhere, and the rule says `degree` is `null` when no degree is mentioned, so the agreed null is correct.

DECISION: ok

## 106. golden_100 - skill `java` (spot-check)

> ...programming skills in a modern programming language (Java, Scala, Python, Kotlin) • Hands-on experience with...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_100 - skill `kotlin` (spot-check)

> ...in a modern programming language (Java, Scala, Python, Kotlin) • Hands-on experience with Kubernetes—deploying and...

- agreed label: `kotlin` · required · raw_text: "Kotlin"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_100 - skill `lightgbm` (spot-check)

> ...Experience with ML frameworks – like scikit-learn, LGBM, Tensorflow, PyTorch etc. • Experience with Big Data...

- agreed label: `lightgbm` · nice_to_have · raw_text: "LGBM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_100 - skill `model-serving` (spot-check)

> ...with DevOps and CI/CD practices • Has experience building and scaling model serving tools, i.e building APIs with tight SLAs • Passion for the...

- agreed label: `model-serving` · nice_to_have · raw_text: "building and scaling model serving tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_100 - skill `tensorflow` (spot-check)

> ...Experience with ML frameworks – like scikit-learn, LGBM, Tensorflow, PyTorch etc. • Experience with Big Data tools – Spark,...

- agreed label: `tensorflow` · nice_to_have · raw_text: "Tensorflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_101 - attribute `degree` (spot-check)

> AI DevOps Engineer Azure and GenAI Required Education-Bachelor's degree in Computer Science, Engineering, Information Technology, or a related discipline, or equivalent practical experience.Required Certification-Certifications: Microsoft Azure,...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor's degree in Computer Science, Engineering, Information Technology, or a related discipline, or equivalent practical experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names only a bachelor's level ('Bachelor's degree in Computer Science, Engineering, Information Technology, or a related discipline'), so the lowest and only named level is bachelor, which is required under the bare-mention-in-requirements rule, and 'or equivalent practical experience' correctly sets degree_or_equivalent to true.

DECISION: ok

## 112. golden_101 - attribute `german` (spot-check)

> AI DevOps Engineer Azure and GenAI

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 113. golden_101 - attribute `seniority` (spot-check)

> ...MLOps, or AI engineering.Required Skills & Experience-7+ years in DevOps, platform engineering, cloud engineering, site reliability...

- agreed label: value="senior" · basis="inferred" · signal="7+ years in DevOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_101 - skill `apis` (spot-check)

> ...capacity and cost monitoring-Python; Bash; PowerShell; REST APIs; JSON/YAML; microservices; event-driven integration;...

- agreed label: `apis` · required · raw_text: "REST APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 115. golden_101 - skill `azure-devops` (spot-check)

> ...AKS; API Management; Key Vault; Entra ID; Azure Monitor-Azure DevOps; Azure Boards; GitHub; GitHub Actions; Git; pull requests;...

- agreed label: `azure-devops` · required · raw_text: "Azure DevOps; Azure Boards"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 116. golden_101 - skill `azure-key-vault` (spot-check)

> ...Azure Machine Learning; Azure OpenAI; AKS; API Management; Key Vault; Entra ID; Azure Monitor-Azure DevOps; Azure Boards;...

- agreed label: `azure-key-vault` · required · raw_text: "Key Vault"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 117. golden_101 - skill `ci-cd` (spot-check)

> ...Azure environments and production delivery pipelines.-CI/CD & Source Control-Strong experience with Azure DevOps and/or GitHub: source...

- agreed label: `ci-cd` · required · raw_text: "CI/CD & Source Control"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_101 - skill `event-driven-systems` (spot-check)

> ...Bash; PowerShell; REST APIs; JSON/YAML; microservices; event-driven integration; Snowflake/Databricks familiarity-DevSecOps scanning;...

- agreed label: `event-driven-systems` · required · raw_text: "event-driven integration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_101 - skill `git` (spot-check)

> ...DevOps; Azure Boards; GitHub; GitHub Actions; Git; pull requests; pipeline-as-code; artifact repositories; release...

- agreed label: `git` · required · raw_text: "Git; pull requests"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 120. golden_101 - skill `github-actions` (spot-check)

> ...ID; Azure Monitor-Azure DevOps; Azure Boards; GitHub; GitHub Actions; Git; pull requests; pipeline-as-code; artifact...

- agreed label: `github-actions` · required · raw_text: "GitHub Actions"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 121. golden_101 - skill `gitops` (spot-check)

> ...Insights, Datadog, Dynatrace, Splunk, or equivalent).-GitOps/deployment tooling (Argo CD, Helm, or equivalent).-ServiceNow and enterprise...

- agreed label: `gitops` · nice_to_have · raw_text: "GitOps/deployment tooling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_101 - skill `linux` (spot-check)

> ...cloud-native templating (beneficial).-Docker, Kubernetes, Linux, networking, identity, secrets management, and cloud...

- agreed label: `linux` · required · raw_text: "Linux"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 123. golden_101 - skill `llms` (spot-check)

> ...evidenceNice-to-Haves-Deploying/operating GenAI apps, LLM-powered services, AI agents, RAG, vector search, or shared enterprise AI...

- agreed label: `llms` · nice_to_have · raw_text: "LLM-powered services"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 124. golden_101 - skill `microsoft-entra-id` (spot-check)

> ...Learning; Azure OpenAI; AKS; API Management; Key Vault; Entra ID; Azure Monitor-Azure DevOps; Azure Boards; GitHub; GitHub...

- agreed label: `microsoft-entra-id` · required · raw_text: "Entra ID"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_101 - skill `opentelemetry` (spot-check)

> ...operations; regression testing; safety and approval gates-Open Telemetry; logs, metrics, traces, dashboards, alerting; SLI/SLO...

- agreed label: `opentelemetry` · required · raw_text: "Open Telemetry"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 126. golden_101 - skill `python` (spot-check)

> ...secrets management, and cloud security fundamentals.-Proficiency in Python plus scripting with Bash, PowerShell, or a comparable...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_101 - skill `rag` (spot-check)

> ...and agent evaluation; prompt and configuration versioning; RAG quality; model and endpoint operations; regression testing; safety...

- agreed label: `rag` · required · raw_text: "RAG quality"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_101 - skill `secrets-management` (spot-check)

> ...Kubernetes, Linux, networking, identity, secrets management, and cloud security fundamentals.-Proficiency in Python...

- agreed label: `secrets-management` · required · raw_text: "secrets management"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_101 - skill `vector-search` (spot-check)

> ...GenAI apps, LLM-powered services, AI agents, RAG, vector search, or shared enterprise AI platforms.-GenAIOps, MLOps,...

- agreed label: `vector-search` · nice_to_have · raw_text: "vector search"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_102 - attribute `german` (spot-check)

> Senior AI Platform & MLOps Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 131. golden_102 - skill `databricks` (spot-check)

> ...strong experience with AI platforms like SageMaker, Databricks, and Terraform, along with MLflow for model management....

- agreed label: `databricks` · required · raw_text: "Databricks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_102 - skill `terraform` (spot-check)

> ...with AI platforms like SageMaker, Databricks, and Terraform, along with MLflow for model management. You will...

- agreed label: `terraform` · required · raw_text: "Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 133. golden_103 - attribute `german` (spot-check)

> Forward-Deployed AI Engineer for Trading

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_104 - attribute `degree` (spot-check)

> AI/ML Engineer (Deep Learning, PyTorch) at Chime Chicago

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The degree rule sets the label to null when no degree is mentioned, and this posting names no degree or level anywhere, so the agreed null stands.

DECISION: ok

## 135. golden_104 - skill `aws` (spot-check)

> ...Strong Python and SQL, PyTorch and distributed compute • Knowledge of AWS, SageMaker, Airflow, Kafka, Redis or Snowflake Location...

- agreed label: `aws` · required · raw_text: "Knowledge of AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 136. golden_104 - skill `evaluation` (spot-check)

> ...learning models in production • Solid ML fundamentals and evaluation design • Strong Python and SQL, PyTorch and distributed compute •...

- agreed label: `evaluation` · required · raw_text: "evaluation design"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 137. golden_104 - skill `machine-learning` (spot-check)

> ...Experience deploying deep learning models in production • Solid ML fundamentals and evaluation design • Strong Python and SQL, PyTorch and...

- agreed label: `machine-learning` · required · raw_text: "Solid ML fundamentals"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 138. golden_104 - skill `python` (spot-check)

> ...production • Solid ML fundamentals and evaluation design • Strong Python and SQL, PyTorch and distributed compute • Knowledge of...

- agreed label: `python` · required · raw_text: "Strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 139. golden_104 - skill `pytorch` (spot-check)

> ...ML fundamentals and evaluation design • Strong Python and SQL, PyTorch and distributed compute • Knowledge of AWS, SageMaker,...

- agreed label: `pytorch` · required · raw_text: "SQL, PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 140. golden_104 - skill `redis` (spot-check)

> ...compute • Knowledge of AWS, SageMaker, Airflow, Kafka, Redis or Snowflake Location and schedule • Chicago, IL • In...

- agreed label: `redis` · required · raw_text: "Redis"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 141. golden_104 - skill `snowflake` (spot-check)

> ...compute • Knowledge of AWS, SageMaker, Airflow, Kafka, Redis or Snowflake Location and schedule • Chicago, IL • In office four days...

- agreed label: `snowflake` · required · raw_text: "Redis or Snowflake"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_105 - attribute `degree` (spot-check)

> ...and shipping ML systems, with focus on computer vision; BS/MS/PhD in CS, EE, or a related field, or equivalent experience. • Deep hands-on experience with object detection and...

- agreed label: value="phd" · requirement="required" · or_equivalent=true · signal="BS/MS/PhD in CS, EE, or a related field, or equivalent experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": true, "degree_signal": "BS/MS/PhD in CS, EE, or a related field, or equivalent experience"} - Under the degree rule the label is the lowest level named, and this bare mention in the requirements list names BS/MS/PhD, so the level is bachelor, not the highest level phd recorded under the old rule; the "or equivalent experience" wording keeps degree_or_equivalent true and the signal is quoted verbatim from the posting.

DECISION: {"degree": "bachelor", "degree_or_equivalent": true, "degree_requirement": "required", "degree_signal": "BS/MS/PhD in CS, EE, or a related field, or equivalent experience"}

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

DECISION: ok

## 147. golden_105 - skill `pytorch` (spot-check)

> ...or a clear record in adjacent multimodal work. • Strong PyTorch skills and fluency with distributed training, mixed precision,...

- agreed label: `pytorch` · required · raw_text: "Strong PyTorch skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_105 - skill `reinforcement-learning` (spot-check)

> ...Experience with simulation, sim-to-real transfer, or reinforcement and imitation learning. • Edge and embedded deployment experience (TensorRT,...

- agreed label: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement and imitation learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 149. golden_105 - skill `vllm` (spot-check)

> ...training). • Experience with LLM tooling such as vLLM, or with RLHF-style post-training for multimodal models. •...

- agreed label: `vllm` · nice_to_have · raw_text: "vLLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 150. golden_106 - attribute `degree` (spot-check)

> Senior AI/ML Engineer — Hybrid, Impactful ML Solutions

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The degree rule sets the label to `null` when no degree is mentioned, and this posting names no degree or qualification level, so the agreed null stands.

DECISION: ok

## 151. golden_106 - attribute `german` (spot-check)

> Senior AI/ML Engineer — Hybrid, Impactful ML Solutions

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 152. golden_106 - attribute `seniority` (spot-check)

> Senior AI/ML Engineer — Hybrid, Impactful ML Solutions LHH in Chicago is...

- agreed label: value="senior" · basis="stated" · signal="Senior AI/ML Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 153. golden_107 - attribute `german` (spot-check)

> W2 role - AI Lead Platform Engineer 12+ years local to IL required

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_107 - attribute `seniority` (spot-check)

> W2 role - AI Lead Platform Engineer 12+ years local to IL required Role: AI Lead Platform...

- agreed label: value="senior" · basis="stated" · signal="AI Lead Platform Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 155. golden_108 - attribute `german` (spot-check)

> Slalom Flex (Project Based) AWS Agentic AI Engineer – Amazon Quick Suite

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 156. golden_108 - skill `agents` (spot-check)

> ...Amazon Quick Suite experience • Strong Python skills and experience building agents and LLM solutions across semantic and knowledge layers •...

- agreed label: `agents` · required · raw_text: "experience building agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 157. golden_108 - skill `aws` (spot-check)

> ...and engineers. What You’ll Bring Required • Senior/architect-level AWS expertise, with hands-on Amazon Quick Suite experience • Strong...

- agreed label: `aws` · required · raw_text: "Senior/architect-level AWS expertise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 158. golden_108 - skill `evaluation` (spot-check)

> ...knowledge layers • Bedrock agents, tool use, text-to-SQL, evaluation and guardrails • Snowflake, Iceberg, S3, Glue, Athena and IAM • Comfort...

- agreed label: `evaluation` · required · raw_text: "evaluation and guardrails"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 159. golden_108 - skill `git` (spot-check)

> ...SAP, JDE and M3 data concepts • Terraform/CloudFormation, Git, CI/CD, testing and Jira • Experience with the Atlan data...

- agreed label: `git` · nice_to_have · raw_text: "Git, CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 160. golden_108 - skill `llms` (spot-check)

> ...Strong Python skills and experience building agents and LLM solutions across semantic and knowledge layers • Bedrock agents,...

- agreed label: `llms` · required · raw_text: "LLM solutions"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 161. golden_108 - skill `power-bi` (spot-check)

> ...while staying highly organized and thoughtful Preferred • Power BI/DAX; SAP, JDE and M3 data concepts • Terraform/CloudFormation,...

- agreed label: `power-bi` · nice_to_have · raw_text: "Power BI/DAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 162. golden_108 - skill `snowflake` (spot-check)

> ...agents, tool use, text-to-SQL, evaluation and guardrails • Snowflake, Iceberg, S3, Glue, Athena and IAM • Comfort trying new techniques...

- agreed label: `snowflake` · required · raw_text: "Snowflake, Iceberg"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 163. golden_108 - skill `terraform` (spot-check)

> ...Power BI/DAX; SAP, JDE and M3 data concepts • Terraform/CloudFormation, Git, CI/CD, testing and Jira • Experience with the Atlan...

- agreed label: `terraform` · nice_to_have · raw_text: "Terraform/CloudFormation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 164. golden_108 - skill `testing` (spot-check)

> ...M3 data concepts • Terraform/CloudFormation, Git, CI/CD, testing and Jira • Experience with the Atlan data catalog • Certifications:...

- agreed label: `testing` · nice_to_have · raw_text: "testing and Jira"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok
