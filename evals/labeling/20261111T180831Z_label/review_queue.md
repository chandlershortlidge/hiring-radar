# Review queue - 20261111T180831Z_label

155 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261111T180831Z_label` refuses while any `?` is left, then writes the Goldens.

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
seed 1) of labels A and B already agreed on. They measure the error rate that
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

## 1. golden_079 - scope `in_scope` (in-scope)

> Software Engineer - AI Product

- figma · Software Engineer - AI Product
- San Francisco · en · greenhouse · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_080 - scope `in_scope` (in-scope)

> Enterprise AI Architect

- distyl · Enterprise AI Architect
- San Francisco · en · ashby · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_081 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer, Drive

- doordashusa · Senior Machine Learning Engineer, Drive
- San Francisco · en · greenhouse · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_082 - scope `in_scope` (in-scope)

> Research Engineer, Safety & Alignment

- cognition · Research Engineer, Safety & Alignment
- San Francisco · en · ashby · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_083 - scope `in_scope` (in-scope)

> Security Engineer / Research Engineer, RL Security

- anthropic · Security Engineer / Research Engineer, RL Security
- San Francisco · en · greenhouse · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_084 - scope `in_scope` (in-scope)

> Frontier Agents Engineer (Applied AI)

- scaleai · Frontier Agents Engineer (Applied AI)
- San Francisco · en · greenhouse · 22 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_085 - scope `in_scope` (in-scope)

> Applied AI Engineer (Matching & Search)

- Clera · Applied AI Engineer (Matching & Search)
- San Francisco · en · ashby · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_086 - scope `in_scope` (in-scope)

> Applied AI Engineer

- cognition · Applied AI Engineer
- San Francisco · en · ashby · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_087 - scope `in_scope` (in-scope)

> Applied AI, Research Engineer

- anthropic · Applied AI, Research Engineer
- San Francisco · en · greenhouse · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_088 - scope `in_scope` (in-scope)

> Member of Technical Staff (ML Engineer, Recommendations & User Modeling)

- Perplexity · Member of Technical Staff (ML Engineer, Recommendations & User Modeling)
- San Francisco · en · ashby · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_089 - scope `in_scope` (in-scope)

> Lead Data Scientist, Credit Risk

- chime · Lead Data Scientist, Credit Risk
- San Francisco · en · greenhouse · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_090 - scope `in_scope` (in-scope)

> Senior Data Scientist - Embedded Insights

- plaid · Senior Data Scientist - Embedded Insights
- San Francisco · en · ashby · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_091 - scope `in_scope` (in-scope)

> ABOUT THE ROLE

- Clera · AI/ML Engineer
- San Francisco · en · ashby · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_092 - scope `in_scope` (in-scope)

> AI Security Engineer, 2027 New Grad

- brainco · AI Security Engineer, 2027 New Grad
- San Francisco · en · ashby · 21 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_093 - scope `in_scope` (in-scope)

> Software Engineer, ML Serving Platform

- doordashusa · Software Engineer, ML Serving Platform
- San Francisco · en · greenhouse · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_079 - skill `ai-ml` (disagreement)

> ...implementing the full lifecycle of an early-phase AI development, from ideating on which models to use through...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI development"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 17. golden_079 - skill `mlops` (disagreement)

> ...the full lifecycle of an early-phase AI development, from ideating on which models to use through productionizing and maintaining them - Experience in developing deep product and business...

- A: (did not label this)
- B: `mlops` · required · raw_text: "from ideating on which models to use through productionizing and maintaining them"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 18. golden_079 - skill `rag` (disagreement)

> ...added plus if you also have: - Demonstrated expertise in AI indexing, retrieval systems, personalization, and/or natural language processing -...

- A: `rag` · nice_to_have · raw_text: "AI indexing, retrieval systems"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 19. golden_080 - skill `cybersecurity` (disagreement)

> ...enterprise areas such as customer support, voice, MarTech, Cybersecurity, IAM, or Document processing. - Able to travel 25% and...

- A: `cybersecurity` · required · raw_text: "Cybersecurity"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 20. golden_080 - skill `data-privacy-and-security` (disagreement)

> ...cloud and enterprise architecture, data flows, security considerations, and modern AI systems; coding fluency to prototype,...

- A: (did not label this)
- B: `data-privacy-and-security` · required · raw_text: "security considerations"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 21. golden_081 - skill `mlops` (disagreement)

> ...Experience building, deploying, monitoring, and maintaining production ML systems end-to-end. - Strong software engineering skills in Python and...

- A: (did not label this)
- B: `mlops` · required · raw_text: "maintaining production ML systems end-to-end"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 22. golden_081 - skill `model-development` (disagreement)

> ...(Bachelor's, Master's, or PhD). - Strong experience developing production machine learning models using modern deep learning frameworks such as PyTorch and...

- A: (did not label this)
- B: `model-development` · required · raw_text: "developing production machine learning models"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 23. golden_082 - skill `explainable-ai` (disagreement)

> ...Hands-on work on evaluations, red-teaming, alignment, or interpretability at a frontier AI lab or in published research. You have...

- A: (did not label this)
- B: `explainable-ai` · required · raw_text: "interpretability"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 24. golden_084 - skill `anthropic-api` (disagreement)

> ...Experience with modern AI tooling, including OpenAI, Claude, MCP, agent frameworks, vector databases, or retrieval...

- A: `anthropic-api` · required · raw_text: "Claude"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: {"requirement": "nice_to_have", "raw_text": "Claude"}

## 25. golden_084 - skill `rag` (disagreement)

> ...Claude, MCP, agent frameworks, vector databases, or retrieval systems. - Strong understanding of machine learning fundamentals...

- A: `rag` · required · raw_text: "retrieval systems"
- B: `rag` · nice_to_have · raw_text: "RAG"

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 26. golden_084 - skill `software-architecture` (disagreement)

> ...Ability to translate ambiguous business problems into technical architectures. - Strong written and verbal communication skills. -...

- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "technical architectures"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 27. golden_084 - skill `vector-search` (disagreement)

> ...for LLMs and agentic systems. - Experience with RAG, semantic search, knowledge graphs, customer intelligence systems, or...

- A: `vector-search` · nice_to_have · raw_text: "semantic search"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 28. golden_086 - skill `ai-deployment` (disagreement)

> ...— and you can point to the before/after metrics - Have deployed or integrated LLM or agent-based systems in production settings - Have previously founded or joined early-stage startups...

- A: (did not label this)
- B: `ai-deployment` · nice_to_have · raw_text: "Have deployed or integrated LLM or agent-based systems in production settings"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 29. golden_086 - skill `software-engineering` (disagreement)

> ...SOFTWARE AGENTS. We're the makers of Devin, the first AI software engineer. Our team is extremely talent-dense. Among our founding...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software engineer"

Options: `A` / `B` / `both` / `drop`

DECISION: {"requirement": "required", "raw_text": "3+ years as a software engineer"}

## 30. golden_087 - skill `ai-deployment` (disagreement)

> ...LLM-powered products, developing agents or workflows, or integrating models into production systems - Experience designing evals, building prototypes, or...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "integrating models into production systems"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 31. golden_088 - skill `a-b-testing` (disagreement)

> ...model calibration, offline and online metrics, and online experimentation. - Experience integrating LLMs into ranking, retrieval,...

- A: `a-b-testing` · required · raw_text: "online experimentation"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 32. golden_088 - skill `ai-infrastructure` (disagreement)

> ...projects. NICE TO HAVE - Experience with large-scale ranking and training infrastructure (multi-stage retrieval and ranking, feature stores,...

- A: (did not label this)
- B: `ai-infrastructure` · nice_to_have · raw_text: "large-scale ranking and training infrastructure"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 33. golden_088 - skill `evaluation` (disagreement)

> ...areas such as engagement modeling, model calibration, offline and online metrics, and online experimentation. - Experience integrating...

- A: (did not label this)
- B: `evaluation` · required · raw_text: "offline and online metrics"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 34. golden_089 - attribute `degree` (disagreement)

> ...team's analytical bar To thrive in this role, you have - A Master's degree (required) in Statistics, Economics, Engineering, Math, Finance,...

- A: value="master" · requirement="required" · or_equivalent=false · signal="A Master's degree (required)"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="a PhD is a plus"

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 35. golden_091 - skill `model-development` (disagreement)

> ...WE'RE LOOKING FOR Required: - 4+ years of experience developing and deploying AI/ML models with a proven track record of delivering impact in applied...

- A: (did not label this)
- B: `model-development` · required · raw_text: "developing and deploying AI/ML models"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 36. golden_092 - skill `apis` (disagreement)

> ...or internal automation. - Experience building with AI/LLM APIs, agent frameworks, or evaluation pipelines. - Exposure...

- A: (did not label this)
- B: `apis` · nice_to_have · raw_text: "AI/LLM APIs"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 37. golden_092 - skill `workflow-automation` (disagreement)

> ...involving developer tools, platform engineering, or internal automation. - Experience building with AI/LLM APIs, agent...

- A: (did not label this)
- B: `workflow-automation` · nice_to_have · raw_text: "internal automation"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 38. golden_093 - skill `testing` (disagreement)

> ...turn a defined problem into a technical design, tested implementation, and safe production rollout. - You have experience...

- A: (did not label this)
- B: `testing` · required · raw_text: "tested implementation"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 39. golden_079 - skill `ai-deployment` (uncertain)

> ...development, from ideating on which models to use through productionizing and maintaining them - Experience in developing deep product and business...

- A: `ai-deployment` · required · raw_text: "productionizing and maintaining them"
- B: `ai-deployment` · required · raw_text: "productionizing"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 40. golden_079 - skill `model-selection` (uncertain)

> ...the full lifecycle of an early-phase AI development, from ideating on which models to use through productionizing and maintaining them - Experience...

- A: `model-selection` · required · raw_text: "ideating on which models to use"
- B: `model-selection` · required · raw_text: "ideating on which models to use"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: drop

## 41. golden_080 - skill `agents` (uncertain)

> ...You have designed, built, and shipped Enterprise-grade Agentic AI/ML systems and can reason credibly about implementation...

- A: `agents` · required · raw_text: "Agentic AI"
- B: `agents` · required · raw_text: "Agentic AI/ML systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 42. golden_080 - skill `software-engineering` (uncertain)

> ...flows, security considerations, and modern AI systems; coding fluency to prototype, inspect systems, and engage deeply with...

- A: `software-engineering` · required · raw_text: "coding fluency"
- B: `software-engineering` · required · raw_text: "coding fluency"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 43. golden_081 - attribute `degree` (uncertain)

> ...machine learning systems with measurable business impact (Bachelor's, Master's, or PhD). - Strong experience developing production machine...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="(Bachelor's, Master's, or PhD)"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="Bachelor's, Master's, or PhD"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "(Bachelor's, Master's, or PhD)"}

## 44. golden_081 - skill `ai-deployment` (uncertain)

> ...data processing technologies such as Spark and Airflow. - Experience building, deploying, monitoring, and maintaining production ML systems end-to-end. - Strong software engineering skills in...

- A: `ai-deployment` · required · raw_text: "Experience building, deploying, monitoring, and maintaining production ML systems"
- B: `ai-deployment` · required · raw_text: "building, deploying, monitoring, and maintaining production ML systems end-to-end"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 45. golden_081 - skill `ai-infrastructure` (uncertain)

> ...software engineering skills in Python and experience with modern ML infrastructure and tooling. - Deep expertise in at least one of the following...

- A: `ai-infrastructure` · required · raw_text: "modern ML infrastructure and tooling"
- B: `ai-infrastructure` · required · raw_text: "modern ML infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 46. golden_081 - skill `observability` (uncertain)

> ...as Spark and Airflow. - Experience building, deploying, monitoring, and maintaining production ML systems end-to-end. - Strong software engineering skills in...

- A: `observability` · required · raw_text: "monitoring, and maintaining production ML systems"
- B: `observability` · required · raw_text: "monitoring, and maintaining production ML systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 47. golden_082 - attribute `degree` (uncertain)

> ...company, or developer tools company. - Advanced degree: PhD in Computer Science, Machine Learning, Physics, Mathematics, or a related discipline; or equivalent industry research experience. OUR COMMITMENT Equal Opportunity. Cognition is an...

- A: value="phd" · requirement="required" · or_equivalent=true · signal="PhD in Computer Science, Machine Learning, Physics, Mathematics, or a related discipline; or equivalent industry research experience"
- B: value="phd" · requirement="required" · or_equivalent=true · signal="PhD in Computer Science, Machine Learning, Physics, Mathematics, or a related discipline; or equivalent industry research experience."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 48. golden_082 - skill `agents` (uncertain)

> ...that changed how a model was trained or deployed. - Agentic systems understanding: You know how agents fail in practice: tool misuse,...

- A: `agents` · required · raw_text: "Agentic systems understanding"
- B: `agents` · required · raw_text: "Agentic systems understanding"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 49. golden_083 - skill `ai-infrastructure` (uncertain)

> ...documents Preferred qualifications - Experience running ML training or inference infrastructure at scale - Experience with infrastructure security, such...

- A: `ai-infrastructure` · nice_to_have · raw_text: "ML training or inference infrastructure"
- B: `ai-infrastructure` · nice_to_have · raw_text: "ML training or inference infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 50. golden_083 - skill `cybersecurity` (uncertain)

> ...security systems in production - Strong understanding of security fundamentals - Working knowledge of Linux, containers, and cloud...

- A: `cybersecurity` · required · raw_text: "security fundamentals"
- B: `cybersecurity` · required · raw_text: "security fundamentals"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 51. golden_083 - skill `llms` (uncertain)

> ...users - Familiarity with reinforcement learning or large language model training workloads The annual compensation range for this role is listed...

- A: `llms` · nice_to_have · raw_text: "large language model training workloads"
- B: `llms` · nice_to_have · raw_text: "large language model training workloads"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 52. golden_084 - skill `agent-state-management` (uncertain)

> ...leverage the latest advances in large language models, reasoning, retrieval, memory, and tool use. - Architect intelligent systems that...

- A: `agent-state-management` · nice_to_have · raw_text: "reasoning, retrieval, memory"
- B: `agent-state-management` · nice_to_have · raw_text: "memory"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 53. golden_084 - skill `ai-ml` (uncertain)

> ...4+ years of software engineering, machine learning, or applied AI experience. - Strong Python programming skills. - Experience...

- A: `ai-ml` · required · raw_text: "applied AI experience"
- B: `ai-ml` · required · raw_text: "applied AI experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 54. golden_084 - skill `software-engineering` (uncertain)

> ...successful in production. Required Qualifications - 4+ years of software engineering, machine learning, or applied AI experience. - Strong...

- A: `software-engineering` · required · raw_text: "4+ years of software engineering"
- B: `software-engineering` · required · raw_text: "software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 55. golden_085 - attribute `seniority` (uncertain)

> Applied AI Engineer (Matching & Search)

- A: value=null · basis=null · signal=null
- B: value=null · basis=null · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 56. golden_085 - skill `ai-developer-tooling` (uncertain)

> ...experience working with AI: We work 24/7 in Cursor - ideally you have experience coding with AI. Bonus if you have an experience working with LLM APIs -...

- A: `ai-developer-tooling` · nice_to_have · raw_text: "ideally you have experience coding with AI"
- B: `ai-developer-tooling` · nice_to_have · raw_text: "ideally you have experience coding with AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 57. golden_085 - skill `ai-ml` (uncertain)

> ...background: Experience in TypeScript and React - Strong practical experience working with AI: We work 24/7 in Cursor - ideally you have experience...

- A: `ai-ml` · required · raw_text: "Strong practical experience working with AI"
- B: `ai-ml` · required · raw_text: "Strong practical experience working with AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 58. golden_085 - skill `llms` (uncertain)

> ...stack: TypeScript, React, Cursor, Supabase, Prisma, Typesense, LLM APIs, Trigger.dev http://Trigger.dev Working in hacker-house...

- A: `llms` · required · raw_text: "Typesense, LLM APIs"
- B: `llms` · required · raw_text: "Tech stack: TypeScript, React, Cursor, Supabase, Prisma, Typesense, LLM APIs, Trigger.dev"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: {"requirement": "required", "raw_text": "LLM APIs"}

## 59. golden_086 - attribute `seniority` (uncertain)

> ...in a STEM field or equivalent hands-on experience - 3+ years as a software engineer, technical consultant, deployment strategist, forward...

- A: value="mid" · basis="inferred" · signal="3+ years as a software engineer"
- B: value="mid" · basis="inferred" · signal="3+ years"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 60. golden_086 - skill `agents` (uncertain)

> ...metrics - Have deployed or integrated LLM or agent-based systems in production settings - Have previously founded or...

- A: `agents` · nice_to_have · raw_text: "agent-based systems"
- B: `agents` · nice_to_have · raw_text: "agent-based systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 61. golden_086 - skill `llms` (uncertain)

> ...— and you can point to the before/after metrics - Have deployed or integrated LLM or agent-based systems in production settings - Have...

- A: `llms` · nice_to_have · raw_text: "deployed or integrated LLM"
- B: `llms` · nice_to_have · raw_text: "LLM"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 62. golden_087 - skill `agents` (uncertain)

> ...language models -- whether shipping LLM-powered products, developing agents or workflows, or integrating models into production...

- A: `agents` · required · raw_text: "developing agents"
- B: `agents` · required · raw_text: "developing agents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 63. golden_087 - skill `evaluation` (uncertain)

> ...or integrating models into production systems - Experience designing evals, building prototypes, or developing technical enablement...

- A: `evaluation` · required · raw_text: "Experience designing evals"
- B: `evaluation` · required · raw_text: "Experience designing evals"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 64. golden_088 - attribute `seniority` (uncertain)

> Member of Technical Staff (ML Engineer, Recommendations & User Modeling)

- A: value=null · basis=null · signal=null
- B: value=null · basis=null · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 65. golden_088 - skill `model-serving` (uncertain)

> ...(multi-stage retrieval and ranking, feature stores, real-time serving). - Background in user understanding, feed ranking,...

- A: `model-serving` · nice_to_have · raw_text: "real-time serving"
- B: `model-serving` · nice_to_have · raw_text: "real-time serving"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 66. golden_089 - skill `data-science` (uncertain)

> ...quantitative discipline; a PhD is a plus - 7+ years of analytical or data science experience in Financial Services, preferably at a FinTech company -...

- A: `data-science` · required · raw_text: "analytical or data science experience"
- B: `data-science` · required · raw_text: "data science experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 67. golden_090 - skill `data-science` (uncertain)

> ...to decision-making across Plaid. WHAT EXCITES US - 6+ years of industry experience in Data Science or a related analytics role. - Deep familiarity with SQL...

- A: `data-science` · required · raw_text: "6+ years of industry experience in Data Science"
- B: `data-science` · required · raw_text: "6+ years of industry experience in Data Science"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 68. golden_090 - skill `evaluation` (uncertain)

> ...such as classification, clustering, and optimization. - Experience evaluating model performance, identifying opportunities for improvement, and connecting...

- A: `evaluation` · required · raw_text: "Experience evaluating model performance"
- B: `evaluation` · required · raw_text: "Experience evaluating model performance"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 69. golden_091 - attribute `degree` (uncertain)

> ...principles in simulation, modeling, and optimization. - Bachelor's or advanced degree in Computer Science, Mechanical Engineering, Electrical Engineering, or a related field. Nice to Have: - Experience with CAE, CAD, and/or PLM...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="Bachelor's or advanced degree in Computer Science, Mechanical Engineering, Electrical Engineering, or a related field"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="Bachelor's or advanced degree in Computer Science, Mechanical Engineering, Electrical Engineering, or a related field."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 70. golden_091 - attribute `seniority` (uncertain)

> ...impact in applied engineering or scientific domains. - 2+ years of technical leadership guiding AI/ML projects from research to production. - Proficiency in Python and modern AI/ML frameworks...

- A: value="senior" · basis="inferred" · signal="2+ years of technical leadership guiding AI/ML projects from research to production"
- B: value="senior" · basis="inferred" · signal="2+ years of technical leadership guiding AI/ML projects from research to production."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 71. golden_091 - skill `ai-deployment` (uncertain)

> ...FOR Required: - 4+ years of experience developing and deploying AI/ML models with a proven track record of delivering impact in applied...

- A: `ai-deployment` · required · raw_text: "deploying AI/ML models"
- B: `ai-deployment` · required · raw_text: "deploying AI/ML models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 72. golden_092 - skill `cybersecurity` (uncertain)

> ...GitHub Actions, or a major cloud (AWS, GCP, Azure). - Any prior security exposure including coursework, CTFs, bug bounties, research, or a...

- A: `cybersecurity` · nice_to_have · raw_text: "Any prior security exposure"
- B: `cybersecurity` · nice_to_have · raw_text: "Any prior security exposure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 73. golden_092 - skill `prompt-engineering` (uncertain)

> ...project. - Have hands-on experience building with LLMs, or are eager to: prompting, agents, evals, or AI-assisted developer tooling. - Have...

- A: `prompt-engineering` · nice_to_have · raw_text: "or are eager to: prompting"
- B: `prompt-engineering` · nice_to_have · raw_text: "Have hands-on experience building with LLMs, or are eager to: prompting"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 74. golden_093 - attribute `seniority` (uncertain)

> ...to operate. We’re excited about you because… - You have 2+ years of software engineering experience building and maintaining production services or...

- A: value="junior" · basis="inferred" · signal="2+ years of software engineering experience"
- B: value="junior" · basis="inferred" · signal="2+ years of software engineering experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 75. golden_093 - skill `model-serving` (uncertain)

> ...practical experience. Nice to Have - Experience with ML inference infrastructure, online feature retrieval, or other latency-sensitive...

- A: `model-serving` · nice_to_have · raw_text: "ML inference infrastructure"
- B: `model-serving` · nice_to_have · raw_text: "ML inference infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 76. golden_079 - attribute `degree` (spot-check)

> ...shorter-term projects ladder up to the long-term vision - A relevant advanced degree (Masters or PhD) in Machine Learning, Artificial Intelligence, Statistics,...

- agreed label: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="A relevant advanced degree (Masters or PhD)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"degree": "master", "degree_requirement": "nice_to_have", "degree_or_equivalent": false, "degree_signal": "A relevant advanced degree (Masters or PhD)"}

## 77. golden_079 - attribute `seniority` (spot-check)

> ...AI talent We’d love to hear from you if you have: - 5+ years of experience of Software Engineering, with 1 or more years of developing generative AI...

- agreed label: value="senior" · basis="inferred" · signal="5+ years of experience of Software Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 78. golden_079 - skill `github-copilot` (spot-check)

> ...Experience using AI-assisted development tools (e.g., GitHub Copilot, ChatGPT, Claude) to write, debug, and optimize...

- agreed label: `github-copilot` · required · raw_text: "GitHub Copilot"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"requirement": "nice_to_have", "raw_text": "GitHub Copilot"}

## 79. golden_079 - skill `llms` (spot-check)

> ...of Software Engineering, with 1 or more years of developing generative AI products - Comfort in prototyping and pathfinding new...

- agreed label: `llms` · required · raw_text: "developing generative AI products"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 80. golden_079 - skill `nlp` (spot-check)

> ...in AI indexing, retrieval systems, personalization, and/or natural language processing - Proven track record of planning a multi-year roadmap in...

- agreed label: `nlp` · nice_to_have · raw_text: "natural language processing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 81. golden_079 - skill `software-engineering` (spot-check)

> ...AI talent We’d love to hear from you if you have: - 5+ years of experience of Software Engineering, with 1 or more years of developing generative AI...

- agreed label: `software-engineering` · required · raw_text: "5+ years of experience of Software Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 82. golden_080 - skill `ai-ml` (spot-check)

> ...You have designed, built, and shipped Enterprise-grade Agentic AI/ML systems and can reason credibly about implementation tradeoffs,...

- agreed label: `ai-ml` · required · raw_text: "Agentic AI/ML systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 83. golden_080 - skill `apis` (spot-check)

> ...maintaining continuity. - Strong working knowledge of APIs, integrations, cloud and enterprise architecture, data...

- agreed label: `apis` · required · raw_text: "APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 84. golden_081 - attribute `german` (spot-check)

> Senior Machine Learning Engineer, Drive

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 85. golden_081 - attribute `seniority` (spot-check)

> Senior Machine Learning Engineer, Drive About the Team DoorDash Drive powers deliveries...

- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 86. golden_081 - skill `cursor` (spot-check)

> ...AI-assisted development tools (e.g. Claude Code, Codex, Cursor) throughout the software development lifecycle. - You are...

- agreed label: `cursor` · required · raw_text: "Cursor"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"requirement": "nice_to_have", "raw_text": "Cursor"}

## 87. golden_081 - skill `deep-learning` (spot-check)

> ...developing production machine learning models using modern deep learning frameworks such as PyTorch and distributed data processing...

- agreed label: `deep-learning` · required · raw_text: "modern deep learning frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_081 - skill `llms` (spot-check)

> ...efficiency. - Build AI-native product experiences using large language models (LLMs) and vision-language models (VLMs). For example, transform...

- agreed label: `llms` · required · raw_text: "Large Language Models (LLMs)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_081 - skill `python` (spot-check)

> ...ML systems end-to-end. - Strong software engineering skills in Python and experience with modern ML infrastructure and...

- agreed label: `python` · required · raw_text: "skills in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_081 - skill `reinforcement-learning` (spot-check)

> ...signals to improve prediction accuracy. - Apply reinforcement learning and optimization techniques to improve logistics...

- agreed label: `reinforcement-learning` · required · raw_text: "Reinforcement Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 91. golden_081 - skill `software-engineering` (spot-check)

> ...and maintaining production ML systems end-to-end. - Strong software engineering skills in Python and experience with modern ML infrastructure and...

- agreed label: `software-engineering` · required · raw_text: "Strong software engineering skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 92. golden_082 - attribute `german` (spot-check)

> Research Engineer, Safety & Alignment

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 93. golden_082 - attribute `seniority` (spot-check)

> Research Engineer, Safety & Alignment

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 94. golden_082 - skill `python` (spot-check)

> ...ideas about how to. - Strong engineering fundamentals: Proficiency in Python and PyTorch (or JAX). You can build eval infrastructure,...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 95. golden_083 - attribute `degree` (spot-check)

> ...USD Logistics Minimum education: Bachelor’s degree or an equivalent combination of education, training, and/or experience Required field of study: A field relevant to the role as...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor’s degree or an equivalent combination of education, training, and/or experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 96. golden_083 - attribute `german` (spot-check)

> Security Engineer / Research Engineer, RL Security

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 97. golden_083 - attribute `seniority` (spot-check)

> Security Engineer / Research Engineer, RL Security

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_083 - skill `distributed-systems` (spot-check)

> ...or Go - Experience designing, building, and operating large-scale distributed systems or security systems in production - Strong understanding...

- agreed label: `distributed-systems` · required · raw_text: "large-scale distributed systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_083 - skill `kubernetes` (spot-check)

> ...with container orchestration such as Kubernetes, and with sandboxed or virtualized code execution at...

- agreed label: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_083 - skill `networking` (spot-check)

> ...security, such as isolation, access control, networking, or identity - Experience with container orchestration...

- agreed label: `networking` · nice_to_have · raw_text: "networking"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_083 - skill `observability` (spot-check)

> ...with sandboxed or virtualized code execution at scale - Experience building observability for large fleets - Experience supporting research teams or other...

- agreed label: `observability` · nice_to_have · raw_text: "Experience building observability for large fleets"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_083 - skill `rust` (spot-check)

> ...skills in Python and at least one systems language such as Rust, C++, or Go - Experience designing, building, and...

- agreed label: `rust` · required · raw_text: "Rust"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 103. golden_083 - skill `software-engineering` (spot-check)

> ...documents for what you build Minimum qualifications - Strong software engineering skills in Python and at least one systems language such as Rust,...

- agreed label: `software-engineering` · required · raw_text: "Strong software engineering skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 104. golden_084 - attribute `german` (spot-check)

> Frontier Agents Engineer (Applied AI)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 105. golden_084 - attribute `seniority` (spot-check)

> ...successful in production. Required Qualifications - 4+ years of software engineering, machine learning, or applied AI experience. - Strong Python programming skills. - Experience...

- agreed label: value="mid" · basis="inferred" · signal="4+ years of software engineering, machine learning, or applied AI experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 106. golden_084 - skill `agents` (spot-check)

> ...with modern AI tooling, including OpenAI, Claude, MCP, agent frameworks, vector databases, or retrieval systems. - Strong...

- agreed label: `agents` · required · raw_text: "agent frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_084 - skill `aws` (spot-check)

> ...systems. - Experience with cloud platforms such as AWS, Azure, or GCP. - Experience with Docker, Kubernetes,...

- agreed label: `aws` · nice_to_have · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_084 - skill `ci-cd` (spot-check)

> ...AWS, Azure, or GCP. - Experience with Docker, Kubernetes, CI/CD, and production observability. - Experience integrating...

- agreed label: `ci-cd` · nice_to_have · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_084 - skill `docker` (spot-check)

> ...platforms such as AWS, Azure, or GCP. - Experience with Docker, Kubernetes, CI/CD, and production observability. -...

- agreed label: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_084 - skill `fine-tuning` (spot-check)

> ...structured knowledge representations. - Experience with fine-tuning, distillation, reinforcement learning, small language...

- agreed label: `fine-tuning` · nice_to_have · raw_text: "fine-tuning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_084 - skill `gcp` (spot-check)

> ...Experience with cloud platforms such as AWS, Azure, or GCP. - Experience with Docker, Kubernetes, CI/CD, and...

- agreed label: `gcp` · nice_to_have · raw_text: "GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 112. golden_084 - skill `knowledge-distillation` (spot-check)

> ...knowledge representations. - Experience with fine-tuning, distillation, reinforcement learning, small language models, or model...

- agreed label: `knowledge-distillation` · nice_to_have · raw_text: "distillation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 113. golden_084 - skill `llms` (spot-check)

> ...AI experience. - Strong Python programming skills. - Experience building production AI systems using LLMs. - Experience with modern AI tooling, including OpenAI,...

- agreed label: `llms` · required · raw_text: "Experience building production AI systems using LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 114. golden_084 - skill `mcp` (spot-check)

> ...with modern AI tooling, including OpenAI, Claude, MCP, agent frameworks, vector databases, or retrieval...

- agreed label: `mcp` · required · raw_text: "MCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"requirement": "nice_to_have", "raw_text": "MCP"}

## 115. golden_084 - skill `observability` (spot-check)

> ...or GCP. - Experience with Docker, Kubernetes, CI/CD, and production observability. - Experience integrating AI systems into enterprise...

- agreed label: `observability` · nice_to_have · raw_text: "production observability"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 116. golden_084 - skill `tool-calling` (spot-check)

> ...large language models, reasoning, retrieval, memory, and tool use. - Architect intelligent systems that combine LLMs,...

- agreed label: `tool-calling` · nice_to_have · raw_text: "tool use"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 117. golden_085 - skill `react` (spot-check)

> ...Very strong software engineering background: Experience in TypeScript and React - Strong practical experience working with AI: We work...

- agreed label: `react` · required · raw_text: "TypeScript and React"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_085 - skill `software-engineering` (spot-check)

> ...the headhunting process end-to-end. Your Experience: - Very strong software engineering background: Experience in TypeScript and React - Strong practical...

- agreed label: `software-engineering` · required · raw_text: "Very strong software engineering background"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_085 - skill `typescript` (spot-check)

> ...- Very strong software engineering background: Experience in TypeScript and React - Strong practical experience working with AI:...

- agreed label: `typescript` · required · raw_text: "Experience in TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 120. golden_086 - skill `javascript` (spot-check)

> ...or similar roles with strong coding proficiency (Python, JavaScript/TypeScript, or similar) - Proven ability to communicate...

- agreed label: `javascript` · required · raw_text: "JavaScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 121. golden_086 - skill `python` (spot-check)

> ...engineer or similar roles with strong coding proficiency (Python, JavaScript/TypeScript, or similar) - Proven ability to...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 122. golden_087 - skill `llms` (spot-check)

> ...in at least one programming language - Meaningful experience building with large language models -- whether shipping LLM-powered products, developing...

- agreed label: `llms` · required · raw_text: "experience building with large language models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 123. golden_088 - attribute `degree` (spot-check)

> Member of Technical Staff (ML Engineer, Recommendations & User Modeling)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 124. golden_088 - skill `machine-learning` (spot-check)

> ...ranking, or personalization systems at scale. - Strong ML fundamentals, covering areas such as engagement modeling, model...

- agreed label: `machine-learning` · required · raw_text: "Strong ML fundamentals"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 125. golden_089 - attribute `german` (spot-check)

> Lead Data Scientist, Credit Risk

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 126. golden_089 - skill `business-intelligence` (spot-check)

> ...Excel skills, and experience working in Looker or a similar business intelligence tool - A strong grounding in statistics and machine learning...

- agreed label: `business-intelligence` · required · raw_text: "a similar business intelligence tool"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_089 - skill `machine-learning` (spot-check)

> ...intelligence tool - A strong grounding in statistics and machine learning for credit, including scorecards / gradient-boosted models, swap-set...

- agreed label: `machine-learning` · required · raw_text: "machine learning for credit"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_089 - skill `sql` (spot-check)

> ...(FCRA, ECOA / Reg B, fair lending, adverse action) - Excellent SQL and Python skills, advanced Microsoft Excel skills, and...

- agreed label: `sql` · required · raw_text: "Excellent SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 129. golden_090 - attribute `seniority` (spot-check)

> Senior Data Scientist - Embedded Insights We believe that the way people...

- agreed label: value="senior" · basis="stated" · signal="Senior Data Scientist"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_090 - skill `airflow` (spot-check)

> ...building or partnering on data pipelines using dbt or Airflow is a plus. - Bachelor’s degree or equivalent work...

- agreed label: `airflow` · nice_to_have · raw_text: "Airflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 131. golden_090 - skill `data-pipelines` (spot-check)

> ...audiences. - Experience building or partnering on data pipelines using dbt or Airflow is a plus. - Bachelor’s degree or...

- agreed label: `data-pipelines` · nice_to_have · raw_text: "data pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_090 - skill `data-visualization` (spot-check)

> ...related analytics role. - Deep familiarity with SQL and data visualization tools. - Understanding of modern machine learning techniques,...

- agreed label: `data-visualization` · required · raw_text: "data visualization tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 133. golden_090 - skill `dbt` (spot-check)

> ...Experience building or partnering on data pipelines using dbt or Airflow is a plus. - Bachelor’s degree or equivalent...

- agreed label: `dbt` · nice_to_have · raw_text: "dbt"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_090 - skill `python` (spot-check)

> ...problems while working with cross-functional partners. - Ability to code and iterate independently in Python, particularly for exploratory data analysis. - Strong...

- agreed label: `python` · required · raw_text: "Ability to code and iterate independently in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 135. golden_091 - attribute `german` (spot-check)

> ABOUT THE ROLE

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 136. golden_091 - skill `ai-ml` (spot-check)

> ...from research to production. - Proficiency in Python and modern AI/ML frameworks (e.g., PyTorch, JAX, TensorFlow). - Experience with...

- agreed label: `ai-ml` · required · raw_text: "modern AI/ML frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 137. golden_091 - skill `jax` (spot-check)

> ...in Python and modern AI/ML frameworks (e.g., PyTorch, JAX, TensorFlow). - Experience with AI/ML algorithms for...

- agreed label: `jax` · required · raw_text: "JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"requirement": "nice_to_have", "raw_text": "JAX"}

## 138. golden_091 - skill `python` (spot-check)

> ...guiding AI/ML projects from research to production. - Proficiency in Python and modern AI/ML frameworks (e.g., PyTorch, JAX,...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 139. golden_091 - skill `tensorflow` (spot-check)

> ...in Python and modern AI/ML frameworks (e.g., PyTorch, JAX, TensorFlow). - Experience with AI/ML algorithms for sequential,...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"requirement": "nice_to_have", "raw_text": "TensorFlow"}

## 140. golden_092 - skill `agents` (spot-check)

> ...automation. - Experience building with AI/LLM APIs, agent frameworks, or evaluation pipelines. - Exposure to Kubernetes,...

- agreed label: `agents` · nice_to_have · raw_text: "agent frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 141. golden_092 - skill `ai-developer-tooling` (spot-check)

> ...project. - Have hands-on experience building with LLMs, or are eager to: prompting, agents, evals, or AI-assisted developer tooling. - Have a working mental model of how code gets to...

- agreed label: `ai-developer-tooling` · nice_to_have · raw_text: "or are eager to: prompting, agents, evals, or AI-assisted developer tooling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 142. golden_092 - skill `aws` (spot-check)

> ...Docker, Terraform, GitHub Actions, or a major cloud (AWS, GCP, Azure). - Any prior security exposure including...

- agreed label: `aws` · nice_to_have · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 143. golden_092 - skill `azure` (spot-check)

> ...Terraform, GitHub Actions, or a major cloud (AWS, GCP, Azure). - Any prior security exposure including coursework,...

- agreed label: `azure` · nice_to_have · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 144. golden_092 - skill `ci-cd` (spot-check)

> ...a working mental model of how code gets to production — version control, CI/CD, containers, cloud — even if you've never owned it...

- agreed label: `ci-cd` · required · raw_text: "version control, CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 145. golden_092 - skill `docker` (spot-check)

> ...or evaluation pipelines. - Exposure to Kubernetes, Docker, Terraform, GitHub Actions, or a major cloud (AWS, GCP,...

- agreed label: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 146. golden_092 - skill `evaluation` (spot-check)

> ...Experience building with AI/LLM APIs, agent frameworks, or evaluation pipelines. - Exposure to Kubernetes, Docker, Terraform, GitHub...

- agreed label: `evaluation` · nice_to_have · raw_text: "evaluation pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 147. golden_092 - skill `github-actions` (spot-check)

> ...pipelines. - Exposure to Kubernetes, Docker, Terraform, GitHub Actions, or a major cloud (AWS, GCP, Azure). - Any prior...

- agreed label: `github-actions` · nice_to_have · raw_text: "GitHub Actions"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 148. golden_092 - skill `kubernetes` (spot-check)

> ...agent frameworks, or evaluation pipelines. - Exposure to Kubernetes, Docker, Terraform, GitHub Actions, or a major cloud (AWS,...

- agreed label: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 149. golden_093 - attribute `degree` (spot-check)

> ...make complex infrastructure easier to adopt. - You hold a degree in Computer Science or a related field, or have equivalent practical experience. Nice to Have - Experience with ML inference...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="degree in Computer Science or a related field, or have equivalent practical experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 150. golden_093 - attribute `german` (spot-check)

> Software Engineer, ML Serving Platform

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 151. golden_093 - skill `apis` (spot-check)

> ...management, or autoscaling. - Experience building self-serve developer platforms, APIs, or automation that helps other engineers move faster. -...

- agreed label: `apis` · nice_to_have · raw_text: "self-serve developer platforms, APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 152. golden_093 - skill `containerization` (spot-check)

> ...distributed services. - Experience operating containerized workloads on Kubernetes, including deployment, resource management,...

- agreed label: `containerization` · nice_to_have · raw_text: "containerized workloads"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 153. golden_093 - skill `cpp` (spot-check)

> ...or systems programming language such as Java, Kotlin, Go, C++, or Python. - You understand distributed systems...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 154. golden_093 - skill `java` (spot-check)

> ...in a backend or systems programming language such as Java, Kotlin, Go, C++, or Python. - You understand distributed...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 155. golden_093 - skill `python` (spot-check)

> ...programming language such as Java, Kotlin, Go, C++, or Python. - You understand distributed systems fundamentals,...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok
