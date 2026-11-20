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

PROPOSED: B - Under rule 1, the 'You should apply if' bullets name ML/AI as a qualification (e.g., 'thoughtful about responsible ML/AI'), and under rule 3 that required mention wins over labeler A's omission.

DECISION: B

## 18. golden_095 - skill `model-development` (disagreement)

> ...a multiple year track record of excellence leading the development and deployment of advanced Machine Learning models to tackle real business problems, preferably in a...

- A: (did not label this)
- B: `model-development` · required · raw_text: "development and deployment of advanced Machine Learning models"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualification bullet in the "You should apply if" section names model development ("leading the development and deployment of advanced Machine Learning models"), and rule 3 makes that required mention decisive, so labeler B's required tag is right and labeler A simply omitted it.

DECISION: B

## 19. golden_095 - skill `rag` (disagreement)

> ...Experience with GenAI, LLMs, agentic workflows, retrieval, evaluation frameworks, or human-in-the-loop product...

- A: `rag` · nice_to_have · raw_text: "retrieval"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 5, the posting never names RAG; "retrieval" appears only as a generic item in a GenAI list and could mean information retrieval, so adding the specific `rag` skill goes beyond what the text states.

DECISION: drop

## 20. golden_095 - skill `software-engineering` (disagreement)

> ...product experiences. - Commercial experience writing critical production code and working with microservices. - Experience designing...

- A: (did not label this)
- B: `software-engineering` · nice_to_have · raw_text: "writing critical production code"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the nice-to-have bullet "Commercial experience writing critical production code" is a qualification that names a software engineering skill, and the quoted raw_text appears verbatim in the posting.

DECISION: ?

## 21. golden_096 - skill `cybersecurity` (disagreement)

> ...our Defence clients, you will need to be eligible for UK Security Clearance (SC) and willing to work between 2 to 4 days per...

- A: (did not label this)
- B: `cybersecurity` · required · raw_text: "security"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1, the only quoted mention, "security", appears in "UK Security Clearance (SC)", which is an eligibility requirement and not a named cybersecurity skill, so the label should not stand (rule 5 bars adding a skill the text does not name).

DECISION: drop

## 22. golden_096 - skill `machine-learning` (disagreement)

> ...technical depth WHO WE'RE LOOKING FOR: - You understand the full ML lifecycle and have significant experience operationalising models...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "understand the full ML lifecycle"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualification bullet "You understand the full ML lifecycle and have significant experience operationalising models" names machine learning as a required qualification, and rule 3 supports B's quoted raw_text "understand the full ML lifecycle" as the determining mention.

DECISION: B

## 23. golden_097 - attribute `seniority` (disagreement)

> ...training jobs and high-availability inference services - Ideally, 3-5 years of relevant experience in ML systems deployment with specific focus on cluster...

- A: value="mid" · basis="inferred" · signal="Ideally, 3-5 years of relevant experience"
- B: value="senior" · basis="stated" · signal="Member of Technical Staff"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1 a years-of-experience line does not establish seniority, and A's only signal is the hedged "Ideally, 3-5 years" nice-to-have. B's quoted signal "Member of Technical Staff" does not appear in the excerpt, so the attribute is unsupported and should be null.

DECISION: ?

## 24. golden_097 - skill `ai-infrastructure` (disagreement)

> ...roles in SRE, DevOps, or Platform Engineering with focus on ML infrastructure - Experience supporting both long-running training jobs...

- A: `ai-infrastructure` · required · raw_text: "focus on ML infrastructure"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 3, the required-section phrase "focus on ML infrastructure" is a verbatim, explicit mention of the ai-infrastructure domain, and it is not merely a job title under rule 1, so the required label stands.

DECISION: A

## 25. golden_097 - skill `aws` (disagreement)

> ...We work with Kubernetes, Slurm, Python, C++, PyTorch, and primarily on AWS. As an AI Infrastructure Engineer, you will be partnering...

- A: `aws` · required · raw_text: "primarily on AWS"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the sentence "We work with ... and primarily on AWS" names AWS as the platform the candidate will work on, and rule 3 keeps a mention that the text supports, so labeler A's aws skill stands.

DECISION: ?

## 26. golden_097 - skill `model-serving` (disagreement)

> ...Experience supporting both long-running training jobs and high-availability inference services - Ideally, 3-5 years of relevant experience in ML...

- A: `model-serving` · required · raw_text: "high-availability inference services"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under the REQUIRED EXPERIENCE heading, the bullet 'Experience supporting both long-running training jobs and high-availability inference services' names serving models in production (rule 1), and rule 3 makes that required mention decisive, with A's raw_text appearing verbatim.

DECISION: A

## 27. golden_098 - skill `software-engineering` (disagreement)

> ...advanced coding skills in Python and proven experience building and maintaining scalable codebases. - You enjoy mentoring junior colleagues and have prior...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "building and maintaining scalable codebases"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualification bullet 'proven experience building and maintaining scalable codebases' is a required qualification that names the skill, and rule 3 makes that required mention control, so B's label stands.

DECISION: ?

## 28. golden_100 - skill `ai-deployment` (disagreement)

> ...production systems with modern DevOps practices - Experience deploying AI systems in enterprise environments is a plus - Experience working across cloud platforms (AWS, GCP,...

- A: `ai-deployment` · nice_to_have · raw_text: "Experience deploying AI systems in enterprise environments is a plus"
- B: `ai-deployment` · required · raw_text: "deploying LLM-powered applications or AI agents in production"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 3, the required mention wins: the unhedged bullet "Experience building and deploying LLM-powered applications or AI agents in production" sits in the required list and is quoted by labeler B, so the nice_to_have "enterprise" line does not override it.

DECISION: B

## 29. golden_100 - skill `llm-orchestration` (disagreement)

> ...- Experience implementing RAG pipelines, tool use, or multi-step AI workflows - Strong understanding of AI system evaluation,...

- A: (did not label this)
- B: `llm-orchestration` · required · raw_text: "multi-step AI workflows"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualification bullet "Experience implementing RAG pipelines, tool use, or multi-step AI workflows" names the skill, and it sits in the WHO YOU ARE list rather than a "plus" line, so labeler B's required tag and quoted raw_text are supported (rule 3).

DECISION: ?

## 30. golden_101 - skill `ai-deployment` (disagreement)

> ...simulation tools (e.g. Isaac SIM), with a track record of shipping models on real robots. - Not afraid of contributing to a big codebase; finds...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "shipping models on real robots"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required ABOUT YOU bullet asking for a "track record of shipping models on real robots" names a qualification, and rule 3 makes that required mention win, so B's required ai-deployment tag with its verbatim raw_text stands.

DECISION: B

## 31. golden_102 - skill `software-architecture` (disagreement)

> ...Android apps used by real users. - Good understanding of Android architecture, Jetpack, Coroutines, Flow and modern Android...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "Android architecture"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualification bullet under WHAT WE'RE LOOKING FOR names "Android architecture" as a required understanding, and rule 5 is not violated because the text itself names architecture, so labeler B's software-architecture tag stands.

DECISION: B

## 32. golden_103 - attribute `seniority` (disagreement)

> Member of Technical Staff (Machine Learning Engineer, Search Agent RL) Perplexity...

- A: value=null · basis=null · signal=null
- B: value="senior" · basis="stated" · signal="Member of Technical Staff"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the signal "Member of Technical Staff" is a job title, which does not count, and "experienced" does not state a seniority level, so seniority should be null.

DECISION: A

## 33. golden_103 - skill `agent-architecture` (disagreement)

> ...- Multi-agent training, coordination, or evaluation. - Building agent harnesses, distributed training systems, or scalable inference...

- A: `agent-architecture` · nice_to_have · raw_text: "Building agent harnesses"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the nice-to-have bullet "Building agent harnesses" names agent system design directly, so labeler A's nice_to_have tag with that raw_text stands, and labeler B's omission does not remove it.

DECISION: A

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

PROPOSED: drop - Rule 5: the required line names "LLM post-training," a broader parent category, not "fine-tuning," and it is only one of four alternatives in "one or more of," so the text does not clearly name the fine-tuning skill itself.

DECISION: drop

## 36. golden_103 - skill `llms` (disagreement)

> ...complex problems. Our work spans search and retrieval, LLM post-training, multi-agent training, and the harnesses that make these...

- A: (did not label this)
- B: `llms` · required · raw_text: "LLM post-training"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 4 the only visible mention of LLM post-training is in the company description and the responsibilities bullet, and the excerpt shows no candidate requirement for it, so the required tag on raw_text "LLM post-training" isn't supported.

DECISION: drop

## 37. golden_103 - skill `model-development` (disagreement)

> ...software engineering skills and the ability to work across model training, experimentation infrastructure, and production systems....

- A: (did not label this)
- B: `model-development` · required · raw_text: "model training"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the QUALIFICATIONS sentence 'the ability to work across model training, experimentation infrastructure, and production systems' names model training as a required skill, and rule 3 makes that required mention win, so labeler B's required model-development tag is correct.

DECISION: B

## 38. golden_104 - attribute `seniority` (disagreement)

> ...culture. We’d love to hear from you if you have: - 3+ years of experience shipping user-facing features or products as a full-stack developer - Demonstrated strong fluency with React & Typescript -...

- A: value="mid" · basis="inferred" · signal="3+ years of experience shipping user-facing features or products as a full-stack developer"
- B: value="senior" · basis="inferred" · signal="Be a mentor to, and be mentored by, exceptional peers across engineering, product & design"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 4, the mentoring signal sits in the 'What you'll do' responsibilities and the candidate isn't asked for it, so B's basis fails; A's '3+ years' qualification line is the only requirement-side seniority evidence, so A's mid reading stands.

DECISION: A

## 39. golden_105 - skill `full-stack-development` (disagreement)

> ...(open source or SaaS) and cloud infrastructure - High-load web applications or large-scale APIs - Performance-critical systems such...

- A: (did not label this)
- B: `full-stack-development` · nice_to_have · raw_text: "High-load web applications"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 5, "High-load web applications" does not name full-stack development; it is at most a generic web-development mention, so the `full-stack-development` skill is not supported by the posting.

DECISION: drop

## 40. golden_105 - skill `software-engineering` (disagreement)

> ...may be a good fit if you: - Have 8+ years of experience as a software engineer working on production backend systems - Have strong...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "experience as a software engineer"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1, the only quoted support, "experience as a software engineer", is a job-title/years-of-experience line, which does not count as a named skill, so `software-engineering` should not be in the answer key.

DECISION: drop

## 41. golden_106 - skill `ai-deployment` (disagreement)

> ...We’re Looking For - Hands-on experience building and deploying data science solutions in Python and related ML libraries. - Strong background...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying data science solutions"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under Rule 1, the 'What We're Looking For' bullet requires hands-on experience 'building and deploying data science solutions', which names ML deployment as a required skill, and Rule 3 makes that required mention decisive.

DECISION: B

## 42. golden_106 - skill `ai-ml` (disagreement)

> ...technical concepts clearly to non-technical audiences and apply AI-enabled approaches to deliver practical business value. Bonus Points For -...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "apply AI-enabled approaches"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualification bullets name applied machine learning and model development, so ai-ml belongs in the key as required, and the quoted phrase "apply AI-enabled approaches" appears word for word in that required section (rule 3).

DECISION: B

## 43. golden_108 - attribute `seniority` (disagreement)

> ...time-to-value. The qualifications you need: - Executive-Facing Presales & Value Engineering (2+ years): Demonstrated experience supporting the technical close...

- A: value="mid" · basis="inferred" · signal="Executive-Facing Presales & Value Engineering (2+ years)"
- B: value="junior" · basis="inferred" · signal="Executive-Facing Presales & Value Engineering (2+ years)"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the qualification line's explicit requirement of 2+ years of executive-facing presales experience, alongside the senior-level responsibilities in the posting, supports the "mid" reading over "junior" (the excerpt contains no junior-level signal).

DECISION: A

## 44. golden_108 - skill `ai-ml` (disagreement)

> ...Python proficiency, API design, SQL, data integration, and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "ML/AI libraries"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualifications list names ML/AI libraries (PyTorch, TensorFlow, scikit-learn) as a required qualification, and rule 3 makes that required mention win, so labeler B's `ai-ml` tag with the quoted raw_text is supported.

DECISION: B

## 45. golden_108 - skill `azure` (disagreement)

> ...lifecycle management across cloud services (AWS Bedrock, Azure AI, GCP Vertex AI). - AI Architecture & Security:...

- A: `azure` · required · raw_text: "Azure AI"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under Rule 1, the qualifications-section bullet on production ML/LLMOps names Azure AI as a cloud service the candidate must have experience with, and that bullet is not marked as a plus, so it is a required mention (Rule 3) and `azure` belongs in the key.

DECISION: A

## 46. golden_108 - skill `software-engineering` (disagreement)

> ...operational bottlenecks to strategic AI solutions. - Software/Data Engineering: Python proficiency, API design, SQL, data integration,...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "Software/Data Engineering"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualifications bullet "Software/Data Engineering" names software engineering explicitly, and rule 3 makes that required mention decisive, so labeler B's version stands.

DECISION: B

## 47. golden_108 - skill `transformers` (disagreement)

> ...libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). - Agentic AI Systems: Hands-on experience with agentic...

- A: (did not label this)
- B: `transformers` · required · raw_text: "Hugging Face Transformers"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualifications list under "The qualifications you need" names "Hugging Face Transformers" as an ML/AI library, and rule 3 makes that required mention count, so labeler B's required tag is right.

DECISION: B

## 48. golden_094 - attribute `seniority` (uncertain)

> ...AI models. This is a highly technical EM role - you’ll lead a team of expert engineers in a fast-evolving technical domain. In order to empower...

- A: value="senior" · basis="inferred" · signal="lead a team of expert engineers"
- B: value="senior" · basis="inferred" · signal="you’ll lead a team of expert engineers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the quoted signal "lead a team of expert engineers" appears verbatim in the posting and supports a senior, management-level role, and the "inferred" basis fits since no explicit seniority term is stated.

DECISION: ok

## 49. golden_094 - skill `ai-ml` (uncertain)

> ...In order to empower this team to be most effective, you will need prior experience in AI, and the appetite to continually invest in deepening your...

- A: `ai-ml` · required · raw_text: "you will need prior experience in AI"
- B: `ai-ml` · required · raw_text: "prior experience in AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the sentence "you will need prior experience in AI" is a required qualification that names AI as a skill, not just a title or years line, and rule 3 makes that required mention decisive, so the agreed `ai-ml` required label stands.

DECISION: ok

## 50. golden_094 - skill `mlops` (uncertain)

> ...domain. Nice to have - Experience training ML models and operating them in production, at scale. #LI-Hybrid Unleash Your Potential When you join...

- A: `mlops` · nice_to_have · raw_text: "operating them in production, at scale"
- B: `mlops` · nice_to_have · raw_text: "Experience training ML models and operating them in production, at scale."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1 the nice-to-have bullet names the skill by describing training ML models and operating them in production at scale, which is MLOps, and rule 3 is satisfied because the agreed raw_text appears verbatim and no required mention overrides it; the posting explicitly calls this 'not a hard requirement', so nice_to_have is correct.

DECISION: ?

## 51. golden_094 - skill `model-development` (uncertain)

> ...shape over time. - Curiosity and enthusiasm for AI. Experience training ML models and operating them in production at scale is a significant...

- A: `model-development` · nice_to_have · raw_text: "Experience training ML models"
- B: `model-development` · nice_to_have · raw_text: "Experience training ML models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1 the training-ML-models sentence is a qualification that names the skill, and under rule 3 no required mention exists because the posting says it is 'not a hard requirement' and repeats it under 'Nice to have', so the agreed nice_to_have label and quoted raw_text are right.

DECISION: ok

## 52. golden_095 - skill `agents` (uncertain)

> ...risk or business software. - Experience with GenAI, LLMs, agentic workflows, retrieval, evaluation frameworks, or human-in-the-loop...

- A: `agents` · nice_to_have · raw_text: "agentic workflows"
- B: `agents` · nice_to_have · raw_text: "agentic workflows"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the nice-to-have qualification bullet "Experience with GenAI, LLMs, agentic workflows..." names the skill, and nice_to_have is the correct requirement level, so the agreed label stands.

DECISION: ok

## 53. golden_095 - skill `ai-deployment` (uncertain)

> ...tech company. - You have experience developing and shipping state-of-the-art ML models to production and delivering business impact. - You're impact-driven...

- A: `ai-deployment` · required · raw_text: "shipping state-of-the-art ML models to production"
- B: `ai-deployment` · required · raw_text: "deployment of advanced Machine Learning models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'You should apply if' qualification bullet 'experience developing and shipping state-of-the-art ML models to production' names the skill as a requirement, and the agreed raw_text appears verbatim in the posting.

DECISION: ok

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

PROPOSED: ok - Under rule 1, the Nice to haves bullet names recommendation problems as a qualification, and the agreed raw_text "recommendation" appears verbatim, so the nice_to_have label stands.

DECISION: ok

## 56. golden_096 - skill `mlops` (uncertain)

> ...You understand the full ML lifecycle and have significant experience operationalising models built with frameworks like TensorFlow or PyTorch - You...

- A: `mlops` · required · raw_text: "experience operationalising models"
- B: `mlops` · required · raw_text: "significant experience operationalising models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the qualification bullet asks for "significant experience operationalising models" (the verbatim raw_text), which is required and names the MLOps skill, so the agreed label stands.

DECISION: ok

## 57. golden_097 - skill `ai-deployment` (uncertain)

> ...training jobs and high-availability inference services - Ideally, 3-5 years of relevant experience in ML systems deployment with specific focus on cluster orchestration and resource...

- A: `ai-deployment` · nice_to_have · raw_text: "Ideally, 3-5 years of relevant experience in ML systems deployment"
- B: `ai-deployment` · nice_to_have · raw_text: "Ideally, 3-5 years of relevant experience in ML systems deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"requirement": "required", "raw_text": "Experience supporting both long-running training jobs and high-availability inference services"} - Under rule 1 the agreed quote is a years-of-experience line that cannot count, and under rule 3 a required qualification bullet naming ML inference service deployment wins, so the skill should be required and quote that bullet.

DECISION: ?

## 58. golden_097 - skill `ansible` (uncertain)

> ...- Knowledge of infrastructure as code (Terraform, Ansible) and GitOps practices - Experience with container...

- A: `ansible` · nice_to_have · raw_text: "Ansible"
- B: `ansible` · nice_to_have · raw_text: "Ansible"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the PREFERRED SKILLS bullet names Ansible directly in a qualification line ('Knowledge of infrastructure as code (Terraform, Ansible)'), so the skill counts as nice_to_have and the agreed raw_text 'Ansible' is quoted verbatim.

DECISION: ok

## 59. golden_097 - skill `devops` (uncertain)

> ...cluster administration and HPC workload management - Previous roles in SRE, DevOps, or Platform Engineering with focus on ML infrastructure - Experience supporting...

- A: `devops` · required · raw_text: "Previous roles in SRE, DevOps, or Platform Engineering"
- B: `devops` · required · raw_text: "Previous roles in SRE, DevOps, or Platform Engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only devops mention is "Previous roles in SRE, DevOps, or Platform Engineering," which names job titles rather than a skill, and rule 5 bars adding devops from the broader GitOps or infrastructure-as-code wording.

DECISION: ?

## 60. golden_097 - skill `terraform` (uncertain)

> ...networking - Knowledge of infrastructure as code (Terraform, Ansible) and GitOps practices - Experience with...

- A: `terraform` · nice_to_have · raw_text: "Terraform"
- B: `terraform` · nice_to_have · raw_text: "Terraform"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the PREFERRED SKILLS bullet 'Knowledge of infrastructure as code (Terraform, Ansible)' names Terraform, so it counts as nice_to_have, and 'Terraform' appears verbatim in the posting.

DECISION: ok

## 61. golden_098 - skill `agents` (uncertain)

> ...including experience building Generative AI and agentic AI applications with Large Language Models - You have advanced coding...

- A: `agents` · required · raw_text: "agentic AI applications"
- B: `agents` · required · raw_text: "agentic AI applications"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet "You bring broad knowledge... including experience building Generative AI and agentic AI applications" names agentic AI as a required skill, so the agreed `agents` label with raw_text "agentic AI applications" stands.

DECISION: ok

## 62. golden_099 - skill `agents` (uncertain)

> ...Experience with text-to-SQL, table question answering, or spreadsheet agents. - Experience with reinforcement learning using...

- A: `agents` · nice_to_have · raw_text: "spreadsheet agents"
- B: `agents` · nice_to_have · raw_text: "spreadsheet agents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the nice-to-have qualification bullet names experience with "spreadsheet agents", which is a skill mention, so the agreed `agents` label with nice_to_have and that raw_text stands.

DECISION: ok

## 63. golden_099 - skill `model-development` (uncertain)

> ...audiences. - Expert with PyTorch or JAX. - Experience training or fine-tuning large language models, or tabular foundation models (e.g. TabPFN). - Strong...

- A: `model-development` · required · raw_text: "training or fine-tuning large language models"
- B: `model-development` · required · raw_text: "training"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the ABOUT YOU qualification bullet "Experience training or fine-tuning large language models" names model training as a required skill, and the quoted raw_text appears verbatim in the posting, so the agreed label stands (rule 3).

DECISION: ok

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

PROPOSED: ok - Under rule 1 the 'Guardrails' item sits in the required WHO YOU ARE list (not a 'plus' line), and under rule 3 the required mention in 'Experience with modern LLM tooling such as ... Guardrails ...' supports the agreed required label, though the 'such as' list makes it one of several acceptable examples.

DECISION: ok

## 66. golden_101 - skill `machine-learning` (uncertain)

> ...collection. - Experience working on large code bases or large machine learning models at scale. - Contributions to a large open-source or industry...

- A: `machine-learning` · nice_to_have · raw_text: "large machine learning models at scale"
- B: `machine-learning` · nice_to_have · raw_text: "large machine learning models at scale"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the nice-to-have qualification sentence "Experience working on large code bases or large machine learning models at scale" names machine learning as an experience requirement, and the agreed raw_text quotes it word for word, so the agreed label stands.

DECISION: ok

## 67. golden_103 - skill `tool-calling` (uncertain)

> ...working system. NICE TO HAVE - Experience with training models to use tools or complete tasks over many steps. - Multi-agent...

- A: `tool-calling` · nice_to_have · raw_text: "training models to use tools"
- B: `tool-calling` · nice_to_have · raw_text: "training models to use tools"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the NICE TO HAVE bullet "Experience with training models to use tools" names the skill, and the agreed nice_to_have requirement and verbatim raw_text match the posting (rule 3 has no required mention to override it).

DECISION: ok

## 68. golden_104 - skill `agents` (uncertain)

> ...Data & Research - Working with user facing LLM and agentic product features - Experience curating and developing eval sets and LLMs...

- A: `agents` · nice_to_have · raw_text: "agentic product features"
- B: `agents` · nice_to_have · raw_text: "agentic product features"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet "Working with user facing LLM and agentic product features" is a qualification that names agent work, and the "not required... added plus" framing correctly makes it nice_to_have, so the agreed label stands.

DECISION: ok

## 69. golden_104 - skill `llms` (uncertain)

> ...levels in the UK. We’re looking for people who have built generative AI products and are eager to lead AI efforts end-to-end, from early...

- A: `llms` · required · raw_text: "built generative AI products"
- B: `llms` · required · raw_text: "have built generative AI products"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 3, the required qualification "built generative AI products" is a qualification bullet that names the skill (rule 1), and the agreed llms label fits it, so I see no grounds to change it.

DECISION: ?

## 70. golden_105 - skill `networking` (uncertain)

> ...Understand performance at a systems level — CPU, memory, networking, and data access - Have operated your own code in production: deployed it,...

- A: `networking` · required · raw_text: "networking, and data access"
- B: `networking` · required · raw_text: "networking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required 'You may be a good fit if you' bullet names networking as a systems-level performance area candidates must understand, and rule 3 makes that required mention control, so the agreed required label stands.

DECISION: ok

## 71. golden_106 - skill `aws` (uncertain)

> ...principles. - Experience with cloud environments (Azure, AWS, GCP) and tools such as Spark, Hive, and Redshift. -...

- A: `aws` · required · raw_text: "AWS"
- B: `aws` · required · raw_text: "AWS"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What We're Looking For' section names AWS in a required experience line ('Experience with cloud environments (Azure, AWS, GCP)'), and the agreed raw_text 'AWS' appears verbatim, so the required aws label stands.

DECISION: ok

## 72. golden_106 - skill `azure` (uncertain)

> ...AI principles. - Experience with cloud environments (Azure, AWS, GCP) and tools such as Spark, Hive, and Redshift. -...

- A: `azure` · required · raw_text: "Azure"
- B: `azure` · required · raw_text: "Azure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, "Experience with cloud environments (Azure, AWS, GCP)" is a qualification bullet under "What We're Looking For" that names Azure, and Rule 3 makes that required mention decisive, so the agreed required label with raw_text "Azure" stands.

DECISION: ok

## 73. golden_106 - skill `data-science` (uncertain)

> ...applicable. What We’re Looking For - Hands-on experience building and deploying data science solutions in Python and related ML libraries. - Strong background...

- A: `data-science` · required · raw_text: "building and deploying data science solutions"
- B: `data-science` · required · raw_text: "building and deploying data science solutions"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What We're Looking For' bullet names data science as a required qualification ('Hands-on experience building and deploying data science solutions'), and rule 3 makes that required mention decisive, so the agreed label stands.

DECISION: ok

## 74. golden_106 - skill `gcp` (uncertain)

> ...Experience with cloud environments (Azure, AWS, GCP) and tools such as Spark, Hive, and Redshift. -...

- A: `gcp` · required · raw_text: "GCP"
- B: `gcp` · required · raw_text: "GCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, GCP is named in the 'What We're Looking For' qualification bullet ('Experience with cloud environments (Azure, AWS, GCP)'), so it is a required mention and the agreed required label with raw_text 'GCP' stands (rules 1 and 3).

DECISION: ok

## 75. golden_107 - skill `ai-developer-tooling` (uncertain)

> ...impact. - You have a clear, informed point of view on using AI to improve how ML engineers work, and you can inspire a team to adopt it. - You think...

- A: `ai-developer-tooling` · required · raw_text: "using AI to improve how ML engineers work"
- B: `ai-developer-tooling` · required · raw_text: "using AI to improve how ML engineers work"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Who You Are' qualification bullet names the skill (a point of view on using AI to improve how ML engineers work, and inspiring a team to adopt it), and the agreed required label and quoted raw_text match the posting word for word.

DECISION: ok

## 76. golden_108 - skill `data-privacy-and-security` (uncertain)

> ...of cloud reference architectures, identity and access, data governance, privacy, and compliance. - Math & Operations Research: Applied knowledge of...

- A: `data-privacy-and-security` · required · raw_text: "data governance, privacy, and compliance"
- B: `data-privacy-and-security` · required · raw_text: "privacy"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under the "qualifications you need" heading, the AI Architecture & Security bullet names data governance, privacy, and compliance as required understanding, so the agreed required label with its verbatim raw_text stands under rules 1 and 3.

DECISION: ok

## 77. golden_108 - skill `hugging-face` (uncertain)

> ...libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). - Agentic AI Systems: Hands-on experience with agentic...

- A: `hugging-face` · required · raw_text: "Hugging Face Transformers"
- B: `hugging-face` · required · raw_text: "Hugging Face Transformers"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the qualifications section ('The qualifications you need') names Hugging Face Transformers in the ML/AI libraries list, and Rule 3 makes that required mention decisive, with the raw_text quoted verbatim.

DECISION: ok

## 78. golden_108 - skill `pytorch` (uncertain)

> ...API design, SQL, data integration, and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face...

- A: `pytorch` · required · raw_text: "PyTorch"
- B: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under the heading "The qualifications you need," the Software/Data Engineering bullet names PyTorch among the ML/AI libraries, so by rules 1 and 3 it is a required mention quoted verbatim as "PyTorch".

DECISION: ok

## 79. golden_108 - skill `scikit-learn` (uncertain)

> ...integration, and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). - Agentic AI...

- A: `scikit-learn` · required · raw_text: "scikit-learn"
- B: `scikit-learn` · required · raw_text: "scikit-learn"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, scikit-learn is named in a qualification bullet ('The qualifications you need'), and rule 3 makes that required mention decisive, with the agreed raw_text 'scikit-learn' appearing verbatim in the posting.

DECISION: ok

## 80. golden_108 - skill `tensorflow` (uncertain)

> ...SQL, data integration, and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). -...

- A: `tensorflow` · required · raw_text: "TensorFlow"
- B: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, TensorFlow is named in the "qualifications you need" section (the Software/Data Engineering bullet), and under rule 3 that required mention makes the agreed required label with raw_text "TensorFlow" correct as it stands.

DECISION: ok

## 81. golden_108 - skill `xgboost` (uncertain)

> ...and ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers). - Agentic AI Systems:...

- A: `xgboost` · required · raw_text: "XGBoost"
- B: `xgboost` · required · raw_text: "XGBoost"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, XGBoost is named in the qualifications bullet "ML/AI libraries (PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face Transformers)" under "The qualifications you need:", so it is a required skill and the agreed label with raw_text "XGBoost" stands.

DECISION: ok

## 82. golden_103 - skill `ml-engineering|machine-learning` (mapping)

> ...QUALIFICATIONS - A strong track record of building and shipping ML systems, with deep experience in one or more of LLM post-training,...

- A: `ml-engineering` · required · raw_text: "building and shipping ML systems"
- B: `machine-learning` · required · raw_text: "building and shipping ML systems"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 5 the phrase should map to the specific skill it names: "building and shipping ML systems" centers on productionizing systems, which is ml-engineering, while the broader machine-learning field is not separately named beyond the "ML" abbreviation.

DECISION: A

## 83. golden_094 - attribute `degree` (spot-check)

> Engineering Manager, AI Models Infrastructure

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting never names a degree, university, or level (no bachelor, master, PhD, or 'degree in' wording), so under the degree rule's 'none (null) when no degree is mentioned' the agreed null value is correct.

DECISION: ok

## 84. golden_095 - attribute `german` (spot-check)

> Lead Machine Learning Scientist, Business Banking

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 85. golden_095 - skill `go` (spot-check)

> ...with scikit-learn. You are comfortable using SQL, and keen to learn Go, which is used in many of our backend microservices. -...

- agreed label: `go` · nice_to_have · raw_text: "keen to learn Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 86. golden_095 - skill `machine-learning` (spot-check)

> ...You have a multiple year track record of excellence leading the development and deployment of advanced Machine Learning models to tackle real business problems, preferably in a...

- agreed label: `machine-learning` · required · raw_text: "leading the development and deployment of advanced Machine Learning models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 87. golden_095 - skill `microservices` (spot-check)

> ...Commercial experience writing critical production code and working with microservices. - Experience designing experiments, A/B tests or other...

- agreed label: `microservices` · nice_to_have · raw_text: "working with microservices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_095 - skill `scikit-learn` (spot-check)

> ...being told to do so. - You speak Python fluently and have extensive, hands-on experience with scikit-learn. You are comfortable using SQL, and keen to learn Go,...

- agreed label: `scikit-learn` · required · raw_text: "extensive, hands-on experience with scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_096 - attribute `degree` (spot-check)

> Senior Machine Learning Engineer

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree or level anywhere (no bachelor, master, PhD, or 'degree' wording), and the degree rule sets the label to `null` when no degree is mentioned, so the agreed null is correct.

DECISION: ok

## 90. golden_096 - skill `aws` (spot-check)

> ...hands-on experience with cloud platforms (e.g., AWS, Azure, GCP), including architecture, security, and...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_096 - skill `gcp` (spot-check)

> ...experience with cloud platforms (e.g., AWS, Azure, GCP), including architecture, security, and infrastructure -...

- agreed label: `gcp` · required · raw_text: "GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 92. golden_096 - skill `kubernetes` (spot-check)

> ...with container and orchestration tools such at Docker & Kubernetes to build and manage applications at scale - You thrive...

- agreed label: `kubernetes` · required · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 93. golden_096 - skill `python` (spot-check)

> ...- You bring deep expertise in software engineering and strong Python skills, focusing on building robust, reusable systems - You...

- agreed label: `python` · required · raw_text: "strong Python skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_096 - skill `pytorch` (spot-check)

> ...models built with frameworks like TensorFlow or PyTorch - You bring deep expertise in software engineering and...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 95. golden_096 - skill `tensorflow` (spot-check)

> ...operationalising models built with frameworks like TensorFlow or PyTorch - You bring deep expertise in software...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 96. golden_097 - attribute `german` (spot-check)

> Member of Technical Staff (AI Infrastructure Engineer)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 97. golden_097 - skill `apis` (spot-check)

> ...and compute resource management for ML workloads - Experience developing APIs and managing distributed systems for both batch and...

- agreed label: `apis` · required · raw_text: "Experience developing APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_097 - skill `distributed-systems` (spot-check)

> ...- Deep understanding of container orchestration and distributed systems architecture - High level familiarity with LLM architecture and...

- agreed label: `distributed-systems` · required · raw_text: "distributed systems architecture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_097 - skill `gitops` (spot-check)

> ...of infrastructure as code (Terraform, Ansible) and GitOps practices - Experience with container registries, image...

- agreed label: `gitops` · nice_to_have · raw_text: "GitOps practices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_097 - skill `infrastructure-as-code` (spot-check)

> ...and high-performance networking - Knowledge of infrastructure as code (Terraform, Ansible) and GitOps practices - Experience...

- agreed label: `infrastructure-as-code` · nice_to_have · raw_text: "infrastructure as code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_097 - skill `llms` (spot-check)

> ...and distributed systems architecture - High level familiarity with LLM architecture and training processes (Multi-Head Attention,...

- agreed label: `llms` · required · raw_text: "familiarity with LLM architecture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

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

DECISION: ok

## 105. golden_099 - attribute `seniority` (spot-check)

> Applied Scientist - Tabular Data, EMEA

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 106. golden_099 - skill `fine-tuning` (spot-check)

> ...- Expert with PyTorch or JAX. - Experience training or fine-tuning large language models, or tabular foundation models (e.g. TabPFN). - Strong...

- agreed label: `fine-tuning` · required · raw_text: "fine-tuning large language models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_099 - skill `python` (spot-check)

> ...- Writes clean, readable, high-performance, fault-tolerant Python code. - Doesn’t need roadmaps: moves independently and...

- agreed label: `python` · required · raw_text: "Python code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_099 - skill `pytorch` (spot-check)

> ...technical and non-technical audiences. - Expert with PyTorch or JAX. - Experience training or fine-tuning large...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_099 - skill `reinforcement-learning` (spot-check)

> ...answering, or spreadsheet agents. - Experience with reinforcement learning using verifiable rewards (e.g. query execution). - Experience working on large...

- agreed label: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning using verifiable rewards"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_099 - skill `sql` (spot-check)

> ...classical baselines (e.g. gradient boosting), and comfortable with SQL, pandas, and messy real-world data. - Not afraid of...

- agreed label: `sql` · required · raw_text: "comfortable with SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_099 - skill `testing` (spot-check)

> ...conferences. - Enjoys improving existing code: typing, tests, CI pipelines. WHAT WE OFFER We offer a comprehensive...

- agreed label: `testing` · nice_to_have · raw_text: "tests"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 112. golden_100 - attribute `seniority` (spot-check)

> ...AI platform continues to evolve WHO YOU ARE - 8+ years of professional software engineering experience - Strong proficiency in Python or TypeScript -...

- agreed label: value="senior" · basis="inferred" · signal="8+ years of professional software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_100 - skill `agent-architecture` (spot-check)

> ...(AWS, GCP, or Azure) is a plus - Experience with agent architectures and long-horizon task execution is a plus - Familiarity...

- agreed label: `agent-architecture` · nice_to_have · raw_text: "agent architectures"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 114. golden_100 - skill `azure` (spot-check)

> ...- Experience working across cloud platforms (AWS, GCP, or Azure) is a plus - Experience with agent architectures and...

- agreed label: `azure` · nice_to_have · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 115. golden_100 - skill `langchain` (spot-check)

> ...production - Experience with modern LLM tooling such as LangChain, LlamaIndex, Guardrails, MCP, or agent frameworks -...

- agreed label: `langchain` · required · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 116. golden_100 - skill `llamaindex` (spot-check)

> ...- Experience with modern LLM tooling such as LangChain, LlamaIndex, Guardrails, MCP, or agent frameworks - Experience...

- agreed label: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 117. golden_100 - skill `llms` (spot-check)

> ...Python or TypeScript - Experience building and deploying LLM-powered applications or AI agents in production - Experience with modern LLM...

- agreed label: `llms` · required · raw_text: "LLM-powered applications"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_100 - skill `mcp` (spot-check)

> ...LLM tooling such as LangChain, LlamaIndex, Guardrails, MCP, or agent frameworks - Experience implementing RAG...

- agreed label: `mcp` · required · raw_text: "MCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_100 - skill `software-engineering` (spot-check)

> ...continues to evolve WHO YOU ARE - 8+ years of professional software engineering experience - Strong proficiency in Python or TypeScript -...

- agreed label: `software-engineering` · required · raw_text: "professional software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 120. golden_100 - skill `tool-calling` (spot-check)

> ...MCP, or agent frameworks - Experience implementing RAG pipelines, tool use, or multi-step AI workflows - Strong understanding of AI...

- agreed label: `tool-calling` · required · raw_text: "RAG pipelines, tool use"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 121. golden_101 - attribute `seniority` (spot-check)

> Applied Scientist Lead - Robotics, EMEA ABOUT MISTRAL Mistral provides...

- agreed label: value="senior" · basis="stated" · signal="Applied Scientist Lead"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 122. golden_101 - skill `ci-cd` (spot-check)

> ...- Enjoys improving existing code: typing, tests, CI pipelines. WHAT WE OFFER We offer a comprehensive benefits...

- agreed label: `ci-cd` · nice_to_have · raw_text: "CI pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 123. golden_101 - skill `jax` (spot-check)

> ...work with team leadership and stakeholder management. - Expert with PyTorch or JAX. - Deep experience with Vision Language Models (VLM),...

- agreed label: `jax` · required · raw_text: "Expert with PyTorch or JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_101 - skill `pytorch` (spot-check)

> ...work with team leadership and stakeholder management. - Expert with PyTorch or JAX. - Deep experience with Vision Language Models (VLM),...

- agreed label: `pytorch` · required · raw_text: "Expert with PyTorch or JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 125. golden_102 - skill `kotlin` (spot-check)

> ...attention to reliability. WHAT WE'RE LOOKING FOR - Strong native Android experience using Kotlin. - Experience shipping Android apps used by real...

- agreed label: `kotlin` · required · raw_text: "Strong native Android experience using Kotlin"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 126. golden_103 - attribute `german` (spot-check)

> Member of Technical Staff (Machine Learning Engineer, Search Agent RL)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_103 - skill `distributed-training` (spot-check)

> ...coordination, or evaluation. - Building agent harnesses, distributed training systems, or scalable inference infrastructure. - Large-scale...

- agreed label: `distributed-training` · nice_to_have · raw_text: "distributed training systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_103 - skill `evaluation` (spot-check)

> ...infrastructure, and production systems. - Experience designing rigorous evaluations, diagnosing failures, and translating experimental results...

- agreed label: `evaluation` · required · raw_text: "designing rigorous evaluations"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 129. golden_103 - skill `recommender-systems` (spot-check)

> ...infrastructure. - Large-scale retrieval, ranking, or recommendation systems.

- agreed label: `recommender-systems` · nice_to_have · raw_text: "recommendation systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_103 - skill `software-engineering` (spot-check)

> ...learning, search and retrieval, or agent systems. - Strong software engineering skills and the ability to work across model training,...

- agreed label: `software-engineering` · required · raw_text: "Strong software engineering skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_104 - skill `full-stack-development` (spot-check)

> ...of experience shipping user-facing features or products as a full-stack developer - Demonstrated strong fluency with React & Typescript -...

- agreed label: `full-stack-development` · required · raw_text: "as a full-stack developer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_104 - skill `react` (spot-check)

> ...a full-stack developer - Demonstrated strong fluency with React & Typescript - Experience communicating and working...

- agreed label: `react` · required · raw_text: "React"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 133. golden_104 - skill `typescript` (spot-check)

> ...developer - Demonstrated strong fluency with React & Typescript - Experience communicating and working across functions...

- agreed label: `typescript` · required · raw_text: "Typescript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_105 - attribute `degree` (spot-check)

> Staff Software Engineer (Agentic Search) - Runtime

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree anywhere (the only education-adjacent mentions are "SHAD or similar advanced technical programmes" and competitive programming/CTF, which are not degrees), so the degree rule's "none (null) when no degree is mentioned" applies and the agreed null is correct.

DECISION: ok

## 135. golden_105 - attribute `seniority` (spot-check)

> Staff Software Engineer (Agentic Search) - Runtime About Nebius: Nebius is...

- agreed label: value="senior" · basis="stated" · signal="Staff Software Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_105 - skill `apis` (spot-check)

> ...and cloud infrastructure - High-load web applications or large-scale APIs - Performance-critical systems such as trading platforms...

- agreed label: `apis` · nice_to_have · raw_text: "large-scale APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 137. golden_105 - skill `backend-development` (spot-check)

> ...8+ years of experience as a software engineer working on production backend systems - Have strong hands-on expertise in C++ or Rust in...

- agreed label: `backend-development` · required · raw_text: "production backend systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_105 - skill `cpp` (spot-check)

> ...backend systems - Have strong hands-on expertise in C++ or Rust in real-world, high-load services - Have built...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 139. golden_105 - skill `rust` (spot-check)

> ...and AI R&D. The Product In a rapidly evolving world, trust in AI depends on AI agents being grounded in fresh,...

- agreed label: `rust` · required · raw_text: "Rust"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_106 - attribute `german` (spot-check)

> Senior Data Scientist

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 141. golden_106 - attribute `seniority` (spot-check)

> Senior Data Scientist Location: London (Hybrid) | Practice Area: Data &...

- agreed label: value="senior" · basis="stated" · signal="Senior Data Scientist"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 142. golden_106 - skill `apache-spark` (spot-check)

> ...cloud environments (Azure, AWS, GCP) and tools such as Spark, Hive, and Redshift. - Demonstrated ability to lead...

- agreed label: `apache-spark` · required · raw_text: "Spark"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 143. golden_106 - skill `ci-cd` (spot-check)

> ...science competitions. - Experience with MLOps practices (CI/CD, model monitoring, DevOps integration). - Familiarity...

- agreed label: `ci-cd` · nice_to_have · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 144. golden_106 - skill `devops` (spot-check)

> ...Experience with MLOps practices (CI/CD, model monitoring, DevOps integration). - Familiarity with advanced NLP frameworks such as...

- agreed label: `devops` · nice_to_have · raw_text: "DevOps integration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 145. golden_106 - skill `llms` (spot-check)

> ...or Transformers and exposure to AI technologies including Generative AI or LLMs. - MSc or PhD in a numerate discipline. - Financial...

- agreed label: `llms` · nice_to_have · raw_text: "Generative AI or LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 146. golden_106 - skill `observability` (spot-check)

> ...competitions. - Experience with MLOps practices (CI/CD, model monitoring, DevOps integration). - Familiarity with advanced NLP...

- agreed label: `observability` · nice_to_have · raw_text: "model monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

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

DECISION: ok

## 150. golden_107 - skill `nlp` (spot-check)

> ...hands-on when it matters. - You bring experience across NLP, audio / music content understanding and recommender...

- agreed label: `nlp` · required · raw_text: "NLP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_108 - attribute `degree` (spot-check)

> ...English with exceptional executive presence. - Degree: Masters Degree in computer science, engineering, mathematics, business engineering, business information or related fields , or equivalent work experience preferred. #LI-NS1 What Celonis can offer you: - Pioneer...

- agreed label: value="master" · requirement="nice_to_have" · or_equivalent=true · signal="Masters Degree in computer science, engineering, mathematics, business engineering, business information or related fields , or equivalent work experience preferred"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names only one degree level (Masters), so the lowest-named-level rule still yields `master`; the trailing "preferred" marks the whole mention optional (nice_to_have), and "or equivalent work experience" sets degree_or_equivalent to true, matching the agreed label and quoted signal.

DECISION: ok

## 152. golden_108 - attribute `german` (spot-check)

> Applied Value Engineer - AI and Pre-Sales Consultant

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_108 - skill `ai-deployment` (spot-check)

> ...workflows. - Production ML/LLMOps: Experience with model deployment, monitoring, MLOps/LLMOps, and lifecycle management across...

- agreed label: `ai-deployment` · required · raw_text: "model deployment"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 154. golden_108 - skill `aws-bedrock` (spot-check)

> ...and lifecycle management across cloud services (AWS Bedrock, Azure AI, GCP Vertex AI). - AI Architecture & Security:...

- agreed label: `aws-bedrock` · required · raw_text: "AWS Bedrock"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 155. golden_108 - skill `cloud` (spot-check)

> ...monitoring, MLOps/LLMOps, and lifecycle management across cloud services (AWS Bedrock, Azure AI, GCP Vertex AI). - AI Architecture...

- agreed label: `cloud` · required · raw_text: "cloud services"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 156. golden_108 - skill `llmops` (spot-check)

> ...ML/LLMOps: Experience with model deployment, monitoring, MLOps/LLMOps, and lifecycle management across cloud services (AWS...

- agreed label: `llmops` · required · raw_text: "MLOps/LLMOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 157. golden_108 - skill `observability` (spot-check)

> ...Production ML/LLMOps: Experience with model deployment, monitoring, MLOps/LLMOps, and lifecycle management across cloud...

- agreed label: `observability` · required · raw_text: "monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 158. golden_108 - skill `prompt-engineering` (spot-check)

> ...LLM orchestration, tool use/function calling, RAG, agents, prompt engineering, or agentic patterns for enterprise workflows. -...

- agreed label: `prompt-engineering` · required · raw_text: "prompt engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 159. golden_108 - skill `python` (spot-check)

> ...to strategic AI solutions. - Software/Data Engineering: Python proficiency, API design, SQL, data integration, and ML/AI libraries...

- agreed label: `python` · required · raw_text: "Python proficiency"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 160. golden_108 - skill `reinforcement-learning` (spot-check)

> ...of linear/nonlinear optimization, statistical analysis, reinforcement learning, and forecasting is a plus. - Strong presentation skills...

- agreed label: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 161. golden_108 - skill `sql` (spot-check)

> ...Software/Data Engineering: Python proficiency, API design, SQL, data integration, and ML/AI libraries (PyTorch,...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 162. golden_108 - skill `statistics` (spot-check)

> ...Applied knowledge of linear/nonlinear optimization, statistical analysis, reinforcement learning, and forecasting is a plus. -...

- agreed label: `statistics` · nice_to_have · raw_text: "statistical analysis"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 163. golden_099 - attribute `degree` (rule-change)

> ...NICE TO HAVE - Ex-founder or builder - PhD / Master in a relevant field (Computer Science, Statistics, Machine Learning) — exceptional candidates from other backgrounds welcome....

- agreed label: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="PhD / Master in a relevant field (Computer Science, Statistics, Machine Learning)"

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "nice_to_have", "degree_or_equivalent": false, "degree_signal": "PhD / Master in a relevant field (Computer Science, Statistics, Machine Learning)"} - Under the degree rule, the level recorded is the lowest named (Master, not PhD), and since the whole mention is under NICE TO HAVE it stays nice_to_have; the 'exceptional candidates from other backgrounds welcome' line widens the field rather than accepting experience in place of a degree, so or_equivalent stays false.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "nice_to_have", "degree_signal": "PhD / Master in a relevant field (Computer Science, Statistics, Machine Learning)"}

## 164. golden_101 - attribute `degree` (rule-change)

> ...or academia. NICE TO HAVE - Ex-founder or builder - PhD / Master in a relevant field (Robotics, Machine Learning) — exceptional candidates from other backgrounds welcome....

- agreed label: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="PhD / Master in a relevant field (Robotics, Machine Learning)"

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "nice_to_have", "degree_or_equivalent": false, "degree_signal": "PhD / Master in a relevant field (Robotics, Machine Learning)"} - Under the rule, `degree` is the lowest level named, and the posting names both PhD and Master in the optional NICE TO HAVE list, so the value is `master` rather than the older highest-level `phd`.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "nice_to_have", "degree_signal": "PhD / Master in a relevant field (Robotics, Machine Learning)"}

## 165. golden_106 - attribute `degree` (rule-change)

> ...to AI technologies including Generative AI or LLMs. - MSc or PhD in a numerate discipline. - Financial services or banking experience. Why Join...

- agreed label: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="MSc or PhD in a numerate discipline"

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "nice_to_have", "degree_or_equivalent": false, "degree_signal": "MSc or PhD in a numerate discipline"} - Under the degree rule the level is the lowest named, so 'MSc or PhD' gives master rather than the older highest-level phd, and the whole mention sits under 'Bonus Points For', so it is nice_to_have.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "nice_to_have", "degree_signal": "MSc or PhD in a numerate discipline"}

## 166. golden_094 - groups `alternative_group` (groups)

> Engineering Manager, AI Models Infrastructure

- `ai-ml` · required · raw_text: "you will need prior experience in AI"
- `machine-learning` · nice_to_have · raw_text: "Experience training ML models"
- `mlops` · nice_to_have · raw_text: "operating them in production, at scale"
- `model-development` · nice_to_have · raw_text: "Experience training ML models"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting offers no skills in place of each other: its only ask-level phrasing joins training and operating models with "and" (skills asked together, not alternatives), and no "at least one of", "or", or example-list marker appears in the labelled skills, so the alternative_group rule yields no group.

DECISION: []

## 167. golden_095 - groups `alternative_group` (groups)

> Lead Machine Learning Scientist, Business Banking

- `a-b-testing` · nice_to_have · raw_text: "A/B tests"
- `agents` · nice_to_have · raw_text: "agentic workflows"
- `ai-deployment` · required · raw_text: "shipping state-of-the-art ML models to production"
- `ai-ml` · required · raw_text: "thoughtful about responsible ML/AI"
- `evaluation` · nice_to_have · raw_text: "evaluation frameworks"
- `explainable-ai` · nice_to_have · raw_text: "explainability"
- `forecasting` · nice_to_have · raw_text: "forecasting"
- `go` · nice_to_have · raw_text: "keen to learn Go"
- `llms` · nice_to_have · raw_text: "Experience with GenAI, LLMs"
- `machine-learning` · required · raw_text: "leading the development and deployment of advanced Machine Learning models"
- `microservices` · nice_to_have · raw_text: "working with microservices"
- `model-development` · required · raw_text: "development and deployment of advanced Machine Learning models"
- `python` · required · raw_text: "You speak Python fluently"
- `recommender-systems` · nice_to_have · raw_text: "recommendation"
- `scikit-learn` · required · raw_text: "extensive, hands-on experience with scikit-learn"
- `software-engineering` · nice_to_have · raw_text: "writing critical production code"
- `sql` · required · raw_text: "You are comfortable using SQL"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The 'Experience with GenAI, LLMs, agentic workflows, retrieval, evaluation frameworks, or human-in-the-loop' list is an 'or' alternative set, but its labeled members llms and evaluation are also asked on their own in the responsibilities (LLM-powered experiences; design robust evaluation), which removes them from the group and leaves fewer than two members, so under the 'a group needs at least two skills' and 'asked on its own elsewhere' rules there is no group.

DECISION: ?

## 168. golden_096 - groups `alternative_group` (groups)

> Senior Machine Learning Engineer

- `aws` · required · raw_text: "AWS"
- `azure` · required · raw_text: "Azure"
- `cloud` · required · raw_text: "cloud platforms"
- `containerization` · required · raw_text: "container and orchestration tools"
- `docker` · required · raw_text: "Docker"
- `gcp` · required · raw_text: "GCP"
- `kubernetes` · required · raw_text: "Kubernetes"
- `machine-learning` · required · raw_text: "understand the full ML lifecycle"
- `mlops` · required · raw_text: "experience operationalising models"
- `python` · required · raw_text: "strong Python skills"
- `pytorch` · required · raw_text: "PyTorch"
- `software-engineering` · required · raw_text: "deep expertise in software engineering"
- `tensorflow` · required · raw_text: "TensorFlow"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["tensorflow", "pytorch"], ["aws", "azure", "gcp"]] - Per the alternative_group rule, "frameworks like TensorFlow or PyTorch" and "cloud platforms (e.g., AWS, Azure, GCP)" each offer one example that meets a single ask, so each forms a group, with the broad "cloud" left out; Docker and Kubernetes are joined by "&" (asked together, not alternatives) so they stay ungrouped.

DECISION: [["aws", "azure", "gcp"], ["pytorch", "tensorflow"]]

## 169. golden_097 - groups `alternative_group` (groups)

> Member of Technical Staff (AI Infrastructure Engineer)

- `ai-deployment` · nice_to_have · raw_text: "Ideally, 3-5 years of relevant experience in ML systems deployment"
- `ai-infrastructure` · required · raw_text: "focus on ML infrastructure"
- `ansible` · nice_to_have · raw_text: "Ansible"
- `apis` · required · raw_text: "Experience developing APIs"
- `aws` · required · raw_text: "primarily on AWS"
- `containerization` · required · raw_text: "container orchestration"
- `cpp` · required · raw_text: "C++ programming"
- `cuda` · nice_to_have · raw_text: "CUDA optimization"
- `devops` · required · raw_text: "Previous roles in SRE, DevOps, or Platform Engineering"
- `distributed-systems` · required · raw_text: "distributed systems architecture"
- `distributed-training` · required · raw_text: "managing distributed training systems"
- `gitops` · nice_to_have · raw_text: "GitOps practices"
- `infrastructure-as-code` · nice_to_have · raw_text: "infrastructure as code"
- `kubernetes` · required · raw_text: "Strong expertise in Kubernetes administration"
- `llms` · required · raw_text: "familiarity with LLM architecture"
- `model-serving` · required · raw_text: "high-availability inference services"
- `networking` · required · raw_text: "Strong understanding of networking"
- `observability` · required · raw_text: "expertise in observability tools"
- `python` · required · raw_text: "Python and C++ programming"
- `pytorch` · required · raw_text: "ML frameworks such as PyTorch"
- `slurm` · required · raw_text: "Hands-on experience with Slurm workload management"
- `tensorflow` · nice_to_have · raw_text: "other ML frameworks like TensorFlow"
- `terraform` · nice_to_have · raw_text: "Terraform"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["ansible", "terraform"]] - Under the alternative_group rule, "infrastructure as code (Terraform, Ansible)" offers two examples for one ask, with the broad skill infrastructure-as-code left out of the group, while the PyTorch and TensorFlow mentions are separate asks (the required PyTorch line and the preferred "other ML frameworks like TensorFlow") and so are not grouped.

DECISION: [["ansible", "terraform"]]

## 170. golden_098 - groups `alternative_group` (groups)

> Principal Data Scientist

- `agents` · required · raw_text: "agentic AI applications"
- `llms` · required · raw_text: "Large Language Models"
- `machine-learning` · required · raw_text: "machine learning techniques"
- `python` · required · raw_text: "Python"
- `software-engineering` · required · raw_text: "building and maintaining scalable codebases"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting asks for each listed skill (Python, machine learning techniques, Generative/agentic AI with LLMs, scalable codebases) as separate requirements with no 'at least one of', 'or', or example-for-one-ask marker, so no skills are offered in place of each other under the alternative_group rule.

DECISION: []

## 171. golden_099 - groups `alternative_group` (groups)

> Applied Scientist - Tabular Data, EMEA

- `agents` · nice_to_have · raw_text: "spreadsheet agents"
- `ci-cd` · nice_to_have · raw_text: "CI pipelines"
- `fine-tuning` · required · raw_text: "fine-tuning large language models"
- `jax` · required · raw_text: "JAX"
- `llms` · required · raw_text: "large language models"
- `machine-learning` · required · raw_text: "machine learning on tabular data"
- `model-development` · required · raw_text: "training or fine-tuning large language models"
- `pandas` · required · raw_text: "pandas"
- `python` · required · raw_text: "Python code"
- `pytorch` · required · raw_text: "PyTorch"
- `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning using verifiable rewards"
- `sql` · required · raw_text: "comfortable with SQL"
- `testing` · nice_to_have · raw_text: "tests"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["jax", "pytorch"]] - The posting says "Expert with PyTorch or JAX", an "X or Y" marker for one ask that either skill meets, so the two form one group; the "training or fine-tuning" phrasing is a choice between verbs for the same LLM ask, not between labelled skills, so it does not form a group.

DECISION: [["jax", "pytorch"]]

## 172. golden_100 - groups `alternative_group` (groups)

> AI Engineer, UK

- `agent-architecture` · nice_to_have · raw_text: "agent architectures"
- `agents` · required · raw_text: "AI agents in production"
- `ai-deployment` · required · raw_text: "deploying LLM-powered applications or AI agents in production"
- `aws` · nice_to_have · raw_text: "AWS"
- `azure` · nice_to_have · raw_text: "Azure"
- `cloud` · nice_to_have · raw_text: "cloud platforms"
- `devops` · required · raw_text: "modern DevOps practices"
- `evaluation` · required · raw_text: "AI system evaluation"
- `gcp` · nice_to_have · raw_text: "GCP"
- `langchain` · required · raw_text: "LangChain"
- `llamaindex` · required · raw_text: "LlamaIndex"
- `llm-guardrails` · required · raw_text: "Guardrails"
- `llm-orchestration` · required · raw_text: "multi-step AI workflows"
- `llms` · required · raw_text: "LLM-powered applications"
- `mcp` · required · raw_text: "MCP"
- `observability` · required · raw_text: "debugging, and observability"
- `python` · required · raw_text: "Strong proficiency in Python"
- `rag` · required · raw_text: "RAG pipelines"
- `software-engineering` · required · raw_text: "professional software engineering experience"
- `tool-calling` · required · raw_text: "RAG pipelines, tool use"
- `typescript` · required · raw_text: "TypeScript"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["python", "typescript"], ["langchain", "llamaindex", "llm-guardrails", "mcp"], ["aws", "gcp", "azure"], ["rag", "llm-orchestration"]] - Under the rule's markers, 'Python or TypeScript', the 'such as LangChain, LlamaIndex, Guardrails, MCP, or agent frameworks' examples, and the parenthesised 'AWS, GCP, or Azure' (with 'cloud' left out) each form a group of alternatives; 'RAG pipelines, tool use, or multi-step AI workflows' also reads as an 'X, Y or Z' set, but tool use is also asked on its own in the responsibilities list, so tool-calling leaves that group and the remaining two form it.

DECISION: [["aws", "azure", "gcp"], ["langchain", "llamaindex", "llm-guardrails", "mcp"], ["llm-orchestration", "rag"], ["python", "typescript"]]

## 173. golden_101 - groups `alternative_group` (groups)

> Applied Scientist Lead - Robotics, EMEA

- `ai-deployment` · required · raw_text: "shipping models on real robots"
- `ci-cd` · nice_to_have · raw_text: "CI pipelines"
- `jax` · required · raw_text: "Expert with PyTorch or JAX"
- `machine-learning` · nice_to_have · raw_text: "large machine learning models at scale"
- `python` · required · raw_text: "Python code"
- `pytorch` · required · raw_text: "Expert with PyTorch or JAX"
- `testing` · nice_to_have · raw_text: "tests"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["jax", "pytorch"]] - "Expert with PyTorch or JAX" is a single ask with an "or" marker, so under the alternative_group rule jax and pytorch form one group, and neither is asked for on its own elsewhere in the posting.

DECISION: [["jax", "pytorch"]]

## 174. golden_102 - groups `alternative_group` (groups)

> Android Developer - AI Finance Agent

- `kotlin` · required · raw_text: "Strong native Android experience using Kotlin"
- `software-architecture` · required · raw_text: "Android architecture"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting asks for Kotlin and for Android architecture as separate requirements with no 'at least one of', 'or', or example-marker wording linking them, so under the alternative_group rule (skills asked for together are not alternatives) neither forms a group.

DECISION: []

## 175. golden_103 - groups `alternative_group` (groups)

> Member of Technical Staff (Machine Learning Engineer, Search Agent RL)

- `agent-architecture` · nice_to_have · raw_text: "Building agent harnesses"
- `agents` · required · raw_text: "or agent systems"
- `ai-infrastructure` · nice_to_have · raw_text: "scalable inference infrastructure"
- `distributed-training` · nice_to_have · raw_text: "distributed training systems"
- `evaluation` · required · raw_text: "designing rigorous evaluations"
- `ml-engineering` · required · raw_text: "building and shipping ML systems"
- `model-development` · required · raw_text: "model training"
- `multi-agent-systems` · nice_to_have · raw_text: "Multi-agent training, coordination, or evaluation"
- `recommender-systems` · nice_to_have · raw_text: "recommendation systems"
- `reinforcement-learning` · required · raw_text: "reinforcement learning, search and retrieval"
- `software-engineering` · required · raw_text: "Strong software engineering skills"
- `tool-calling` · nice_to_have · raw_text: "training models to use tools"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The 'one or more of' qualification names reinforcement learning and agent systems, but reinforcement learning is also asked on its own in the responsibilities ('Develop LLM post-training methods, including reinforcement learning'), so it leaves the group and only `agents` remains, below the two-skill minimum.

DECISION: ?

## 176. golden_104 - groups `alternative_group` (groups)

> Software Engineer - AI Product (London, United Kingdom)

- `agents` · nice_to_have · raw_text: "agentic product features"
- `evaluation` · nice_to_have · raw_text: "curating and developing eval sets and LLMs as judges"
- `full-stack-development` · required · raw_text: "as a full-stack developer"
- `llms` · required · raw_text: "built generative AI products"
- `react` · required · raw_text: "React"
- `typescript` · required · raw_text: "Typescript"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting asks for React and Typescript together and for generative AI products, with no 'at least one of', 'X or Y' or example-set markers, so no skills are offered in place of each other under the alternative_group rule.

DECISION: []

## 177. golden_105 - groups `alternative_group` (groups)

> Staff Software Engineer (Agentic Search) - Runtime

- `apis` · nice_to_have · raw_text: "large-scale APIs"
- `backend-development` · required · raw_text: "production backend systems"
- `cloud` · nice_to_have · raw_text: "cloud infrastructure"
- `cpp` · required · raw_text: "C++"
- `data-pipelines` · nice_to_have · raw_text: "real-time data pipelines"
- `networking` · required · raw_text: "networking, and data access"
- `rust` · required · raw_text: "Rust"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["cpp", "rust"]] - The posting asks for "strong hands-on expertise in C++ or Rust" for one ask, and neither skill is asked for elsewhere on its own, so the "X or Y" marker makes them one alternative_group.

DECISION: [["cpp", "rust"]]

## 178. golden_106 - groups `alternative_group` (groups)

> Senior Data Scientist

- `ai-deployment` · required · raw_text: "deploying data science solutions"
- `ai-ml` · required · raw_text: "apply AI-enabled approaches"
- `apache-spark` · required · raw_text: "Spark"
- `aws` · required · raw_text: "AWS"
- `azure` · required · raw_text: "Azure"
- `ci-cd` · nice_to_have · raw_text: "CI/CD"
- `cloud` · required · raw_text: "cloud environments"
- `data-science` · required · raw_text: "building and deploying data science solutions"
- `devops` · nice_to_have · raw_text: "DevOps integration"
- `gcp` · required · raw_text: "GCP"
- `llms` · nice_to_have · raw_text: "Generative AI or LLMs"
- `machine-learning` · required · raw_text: "applied machine learning"
- `mlops` · nice_to_have · raw_text: "MLOps practices"
- `model-development` · required · raw_text: "model development"
- `nlp` · nice_to_have · raw_text: "advanced NLP frameworks such as spaCy"
- `observability` · nice_to_have · raw_text: "model monitoring"
- `python` · required · raw_text: "Python"
- `transformers` · nice_to_have · raw_text: "Transformers"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["aws", "azure", "gcp"]] - The posting asks for "cloud environments (Azure, AWS, GCP)", which the rule's own example treats as one group of alternatives, with the broad "cloud" skill left out of it. The Spark, Hive and Redshift list and the spaCy/Transformers examples do not form a group under the rule, since only one skill from each is labeled, or the broad NLP parent would have to be excluded.

DECISION: [["aws", "azure", "gcp"]]

## 179. golden_107 - groups `alternative_group` (groups)

> Senior Machine Learning Engineering Manager - Content Platform

- `ai-developer-tooling` · required · raw_text: "using AI to improve how ML engineers work"
- `machine-learning` · required · raw_text: "deep machine learning expertise"
- `nlp` · required · raw_text: "NLP"
- `recommender-systems` · required · raw_text: "recommender systems"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting asks for experience across NLP, audio/music content understanding and recommender systems together ('You bring experience across...'), which is a set of skills asked for jointly, not one of several accepted for a single ask, so no alternative_group applies.

DECISION: []

## 180. golden_108 - groups `alternative_group` (groups)

> Applied Value Engineer - AI and Pre-Sales Consultant

- `agents` · required · raw_text: "RAG, agents"
- `ai-deployment` · required · raw_text: "model deployment"
- `ai-ml` · required · raw_text: "ML/AI libraries"
- `api-design` · required · raw_text: "API design"
- `aws-bedrock` · required · raw_text: "AWS Bedrock"
- `azure` · required · raw_text: "Azure AI"
- `cloud` · required · raw_text: "cloud services"
- `data-privacy-and-security` · required · raw_text: "data governance, privacy, and compliance"
- `forecasting` · nice_to_have · raw_text: "forecasting is a plus"
- `hugging-face` · required · raw_text: "Hugging Face Transformers"
- `llm-orchestration` · required · raw_text: "LLM orchestration"
- `llmops` · required · raw_text: "MLOps/LLMOps"
- `mlops` · required · raw_text: "MLOps/LLMOps"
- `observability` · required · raw_text: "monitoring"
- `prompt-engineering` · required · raw_text: "prompt engineering"
- `python` · required · raw_text: "Python proficiency"
- `pytorch` · required · raw_text: "PyTorch"
- `rag` · required · raw_text: "function calling, RAG"
- `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning"
- `scikit-learn` · required · raw_text: "scikit-learn"
- `software-engineering` · required · raw_text: "Software/Data Engineering"
- `sql` · required · raw_text: "SQL"
- `statistics` · nice_to_have · raw_text: "statistical analysis"
- `tensorflow` · required · raw_text: "TensorFlow"
- `tool-calling` · required · raw_text: "tool use/function calling"
- `transformers` · required · raw_text: "Hugging Face Transformers"
- `vertex-ai` · required · raw_text: "GCP Vertex AI"
- `xgboost` · required · raw_text: "XGBoost"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["llm-orchestration", "tool-calling", "prompt-engineering"]] - The Agentic AI Systems line offers LLM orchestration, tool use/function calling, RAG, agents, prompt engineering or agentic patterns for one ask, with 'or' marking the alternatives; rag and agents are also asked on their own in the duties ('LLM/agent systems with RAG'), so they leave the group, leaving three members. The cloud and ML-library parentheticals have no 'or' or 'such as' marker, so they are not grouped.

DECISION: [["llm-orchestration", "prompt-engineering", "tool-calling"]]
