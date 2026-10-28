# Review queue - 20261027T110516Z_label

201 items from 24 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261027T110516Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 305 accepted labels,
seed 0) of labels A and B already agreed on. They measure the error rate that
agreement alone cannot: two labelers can agree and both be wrong. They print the posting
excerpt and the agreed label only - no `A:`/`B:` lines - so you check the label against the
posting rather than against the labelers, who by construction both said the same thing.

The first 24 items ask whether each posting belongs in the held-out set at all.
They come pre-answered `yes`, so leaving them alone keeps every posting. Answer `no <why>`
and that posting is written to `evals/goldens/excluded.json` with your reason instead of
becoming a Golden, and neither this script nor `new_goldens.py` will pick it again. Use it
for a posting that got past the title and city filters but is not the job market we
measure - a marketing role, a listing in the wrong field. The rest of that posting's items
are then ignored, so you can answer `no` and skip them.

## 1. golden_025 - scope `in_scope` (in-scope)

> Distinguished Engineer – Software & AI Products (w/m/d)

- ALDB GmbH · Distinguished Engineer – Software & AI Products (w/m/d)
- Berlin · de · arbeitsagentur · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_026 - scope `in_scope` (in-scope)

> (Senior) Platform Engineer - Kubernetes, Private AI  (m/w/d),Bielefeld,Augsburg,Ol...

- OEDIV · (Senior) Platform Engineer - Kubernetes, Private AI  (m/w/d),Bielefeld,Augsburg,Ol...
- Berlin · de · arbeitsagentur · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_027 - scope `in_scope` (in-scope)

> AI Solution Architect / Senior Engineer Financial Services (w/m/d)

- Capgemini Deutschland GmbH · AI Solution Architect / Senior Engineer Financial Services (w/m/d)
- Berlin · de · arbeitsagentur · 22 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_028 - scope `in_scope` (in-scope)

> Sorge gemeinsam mit uns für die digitale Zukunftsfähigkeit der Bundeswehr.

- BWI GmbH · Senior AI Engineer (w/m/d)
- Berlin · de · arbeitsagentur · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_029 - scope `in_scope` (in-scope)

> # Qualitätsingenieur KI-Fokus / Quality Engineer (AI-augmented) (m/w/d) IT-Consulting

- PTA GmbH · Qualitätsingenieur KI-Fokus / Quality Engineer (AI-augmented) (m/w/d) IT-Consulting
- Berlin · de · arbeitsagentur · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_030 - scope `in_scope` (in-scope)

> NTT DATA Deutschland SE: SAP AI Lead Architect (w/m/x)

- NTT DATA Deutschland SE · NTT DATA Deutschland SE: SAP AI Lead Architect (w/m/x)
- Berlin · de · arbeitsagentur · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_031 - scope `in_scope` (in-scope)

> Senior AI/LLM Engineer (Python) - Remote

- Kake · Senior AI/LLM Engineer (Python)
- Remote (EU) · en · url · 26 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_032 - scope `in_scope` (in-scope)

> AI Systems Engineer (d/f/m)

- mobile.de · AI Systems Engineer (d/f/m)
- Berlin · en · screenshot · 25 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_033 - scope `in_scope` (in-scope)

> AI-First Engineering Intern

- Xsolla · AI-First Engineering Intern
- Berlin · en · screenshot · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_034 - scope `in_scope` (in-scope)

> WHO ARE WE LOOKING FOR:

- Brighter AI Technologies GmbH · Senior Cloud Software Engineer AI (m/f/d)
- Berlin · en · arbeitnow · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_035 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer, LLM Inference Optimization

- Nebius · Senior Machine Learning Engineer, LLM Inference Optimization
- Berlin · en · greenhouse · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_036 - scope `in_scope` (in-scope)

> NTT DATA Deutschland SE: Senior AI & GenAI Architect (w/m/x)

- NTT DATA Deutschland SE · NTT DATA Deutschland SE: Senior AI & GenAI Architect (w/m/x)
- Berlin · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_037 - scope `in_scope` (in-scope)

> AI Engineer

- Kuro · AI Engineer
- Berlin · en · screenshot · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_038 - scope `in_scope` (in-scope)

> Staff Product Engineer, AI

- Intercom · Staff Product Engineer, AI
- Berlin · en · greenhouse · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_039 - scope `in_scope` (in-scope)

> AI Engineer Team Lead (all genders)

- EXXETA AG · AI Engineer Team Lead (all genders)
- Berlin · en · arbeitsagentur · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: no summary blurb under 400 chars, same threshold as the chart exclusion (6d3dcb4); too little to extract to measure anything

## 16. golden_040 - scope `in_scope` (in-scope)

> Senior AI/Computer Vision Engineer

- Ubiquiti Inc. · Senior AI/Computer Vision Engineer
- Berlin · en · jsearch · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 17. golden_041 - scope `in_scope` (in-scope)

> Senior Applied AI Engineer

- DKB Service GmbH · Senior Applied AI Engineer
- Berlin · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 18. golden_042 - scope `in_scope` (in-scope)

> Senior Machine Learning Research Engineer

- European Tech Recruit · Senior Machine Learning Research Engineer
- Berlin · en · jsearch · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 19. golden_043 - scope `in_scope` (in-scope)

> AI Reliability & Quality Engineer (m/w/d)

- Union Investment · AI Reliability & Quality Engineer (m/w/d)
- Berlin · de · arbeitsagentur · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 20. golden_044 - scope `in_scope` (in-scope)

> Lead AI Engineer, Agents & Infrastructure

- Clera · Lead AI Engineer, Agents & Infrastructure
- Berlin · en · ashby · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 21. golden_045 - scope `in_scope` (in-scope)

> Lead Product Engineer - AI

- Vicoland · Lead Product Engineer - AI
- Berlin · en · join · 15 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 22. golden_046 - scope `in_scope` (in-scope)

> AI Engineer Inbound SCM

- Deichmann · AI Engineer Inbound SCM
- Berlin · de · jsearch · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 23. golden_047 - scope `in_scope` (in-scope)

> (Junior) Agentic AI Software Engineer

- Reply Deutschland SE · (Junior) Agentic AI Software Engineer
- Berlin · de · jsearch · 20 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 24. golden_048 - scope `in_scope` (in-scope)

> Senior Performance Marketing Manager – Paid Social & AI (m/w/d)

- benuta GmbH · Senior Performance Marketing Manager – Paid Social & AI (m/w/d)
- Berlin · de · arbeitnow · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: no marketing role, outside the AI/data engineering scope

## 25. golden_025 - skill `software-engineering` (disagreement)

> ...auch anders geht - Fundierte Erfahrung in Architektur und Entwicklung komplexer Softwaresysteme sowie in einer technischen Führungsrolle - Tiefgreifende...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "Entwicklung komplexer Softwaresysteme"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 26. golden_027 - skill `cybersecurity` (disagreement)

> ...für produktive AI-Systeme sowie gutes Verständnis von Security, Skalierbarkeit und Architekturdesign in komplexen,...

- A: (did not label this)
- B: `cybersecurity` · required · raw_text: "Security"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 27. golden_028 - skill `tool-calling` (disagreement)

> ...von KI-Modellen - Erfahrung im Prompt-, Kontext- und Tool-Engineering von generativen KI-Modellen - Erfahrung in der...

- A: `tool-calling` · required · raw_text: "Tool-Engineering"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 28. golden_029 - skill `apis` (disagreement)

> ...und synthetische Testdatenerzeugung - Erfahrung in der Integration von LLM-APIs und KI-Services in Testframeworks sowie im Aufbau KI-nativer Testlösungen...

- A: (did not label this)
- B: `apis` · required · raw_text: "Integration von LLM-APIs und KI-Services"

Options: `A` / `B` / `both` / `drop`

DECISION: drop

## 29. golden_030 - skill `ai-ml` (disagreement)

> ...Kenntnisse moderner Architekturen, Cloud-Technologien und AI/ML sind von Vorteil - Als struktuierter Teamplayer (w/m/x)...

- A: `ai-ml` · nice_to_have · raw_text: "AI/ML"
- B: `ai-ml` · required · raw_text: "Hands-on Erfahrung in der technischen Umsetzung von AI- oder Automatisierungslösungen"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 30. golden_030 - skill `workflow-automation` (disagreement)

> ...Erfahrung in der technischen Umsetzung von AI- oder Automatisierungslösungen im SAP-Umfeld (z. B. SAP BTP, APIs, Integration,...

- A: (did not label this)
- B: `workflow-automation` · required · raw_text: "Automatisierungslösungen"

PROPOSED: `B` - qualification bullet names the practice; same bullet as item 29

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 31. golden_031 - skill `ai-deployment` (disagreement)

> ...experience, skilled in designing, building, and productionizing LLM-powered applications and AI systems at scale. It's a great fit for people who...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "productionizing LLM-powered applications"

PROPOSED: `B` - qualification bullet, "productionizing" names it

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 32. golden_031 - skill `backend-development` (disagreement)

> ...similar backend frameworks. -...

- A: `backend-development` · required · raw_text: "similar backend frameworks"
- B: (did not label this)

PROPOSED: `A` - "FastAPI or similar backend frameworks" names broad and specific, guide rule 1

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 33. golden_032 - skill `ai-deployment` (disagreement)

> ...generation), knowledge base design, and secure, scalable agentic product deployments in regulated environments. Job responsibilities -...

- A: (did not label this)
- B: `ai-deployment` · nice_to_have · raw_text: "agentic product deployments"

PROPOSED: `B` - qualification bullet, "agentic product deployments" names deployment

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 34. golden_033 - attribute `degree` (disagreement)

> ...fast you learn than what you already know cold. - Open to current undergraduate students, graduate students, and recent graduates of a Computer Science, Software Engineering, or related program. If you're pursuing a graduate degree and don't mind...

- A: value="master" · requirement="required" · or_equivalent=false · signal="current undergraduate students, graduate students, and recent graduates of a Computer Science, Software Engineering, or related program"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="Open to current undergraduate students, graduate students, and recent graduates of a Computer Science, Software Engineering, or related program."

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 35. golden_035 - skill `llm-orchestration` (disagreement)

> ...structured outputs, streaming APIs, high concurrency, and multi-step orchestration. - Familiarity with CUDA or Triton; the role does not...

- A: (did not label this)
- B: `llm-orchestration` · nice_to_have · raw_text: "multi-step orchestration"

PROPOSED: `B` - qualification bullet names multi-step orchestration

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 36. golden_035 - skill `model-serving` (disagreement)

> ...attention, memory bandwidth, batching, parallelism, and long-context serving. - Ability to quantify trade-offs among latency,...

- A: (did not label this)
- B: `model-serving` · required · raw_text: "long-context serving"

PROPOSED: `B` - parent above sglang/vllm, but allowed: the broad skill's own quote names serving

Options: `A` / `B` / `both` / `drop`

DECISION: {"requirement": "required", "raw_text": "at least one modern inference stack"}

## 37. golden_035 - skill `software-architecture` (disagreement)

> ...throughput, quality, utilization, and cost. - Experience designing or optimizing distributed inference system architecture, with hands-on work in one or more areas such as request...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "designing or optimizing distributed inference system architecture"

PROPOSED: `B` - qualification bullet; sharing the span with `distributed-systems` (item 84) does not matter, per item 27

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 38. golden_037 - skill `ai-deployment` (disagreement)

> ...challenges in the construction industry - You've build applied AI/ML use cases and brought them to production - You have at least 3+ years of experience as a software...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "applied AI/ML use cases and brought them to production"

PROPOSED: `B` - qualification bullet, "brought them to production"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 39. golden_037 - skill `apis` (disagreement)

> .../ AWS S3 - Backend (Document Pipelines & applied AI): Fastify API / TS + Python for ML Services - Hosting: Railway (Moving...

- A: (did not label this)
- B: `apis` · required · raw_text: "Fastify API"

PROPOSED: `drop` - an API being consumed is not `apis` (your rule 3)

Options: `A` / `B` / `both` / `drop`

DECISION: drop

## 40. golden_037 - skill `machine-learning` (disagreement)

> ...Pipelines & applied AI): Fastify API / TS + Python for ML Services - Hosting: Railway (Moving to AWS) - AI: Azure / OpenAI,...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "ML Services"

PROPOSED: `drop` - "ML Services" is what Python is used for in a stack line, not a named skill; `ai-ml` already accepted for this posting. Decide with item 42

Options: `A` / `B` / `both` / `drop`

DECISION: drop

## 41. golden_037 - skill `ml-engineering` (disagreement)

> ...at least 3+ years of experience as a software engineer, machine learning engineer or AI i in a fast paced environment - You are fluent in...

- A: (did not label this)
- B: `ml-engineering` · required · raw_text: "machine learning engineer"

PROPOSED: `drop` - "experience as a machine learning engineer" is a years/role line (your rule 2)

Options: `A` / `B` / `both` / `drop`

DECISION: drop

## 42. golden_037 - skill `serverless` (disagreement)

> ...our tech stack decisions. - Web-App: Typescript / Vite - Cloud Functions: Supabase - Database / Vector DB and File Storage:...

- A: `serverless` · required · raw_text: "Cloud Functions"
- B: (did not label this)

PROPOSED: `A` - a named component of the tech-stack list; requirement rule 3 makes it required. Decide with item 40

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 43. golden_037 - skill `software-engineering` (disagreement)

> ...production - You have at least 3+ years of experience as a software engineer, machine learning engineer or AI i in a fast paced...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software engineer"

PROPOSED: `drop` - "experience as a software engineer", same role line as item 41 (your rule 2)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 44. golden_038 - skill `machine-learning` (disagreement)

> ...takes an analytical approach to development and has some hands-on experience with ML systems, we'd love to hear from you! What will I be...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "hands-on experience with ML systems"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 45. golden_041 - skill `containerization` (disagreement)

> ...mit Cloud Computing und Docker mit; Kenntnisse in CI/CD, Container-Orchestrierung oder Infrastructure as Code sind willkommen * Du verstehst...

- A: `containerization` · nice_to_have · raw_text: "Container-Orchestrierung"
- B: (did not label this)

PROPOSED: `A` - the text names "Container-Orchestrierung", so the broad quote names itself; not parent-stacking

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 46. golden_044 - skill `agents` (disagreement)

> ...technology platform. WHAT YOU'LL DO - Build agent orchestration, context management, memory, and programmatic tool...

- A: `agents` · required · raw_text: "agent orchestration"
- B: (did not label this)

PROPOSED: `A` - qualification bullet names "agent orchestration"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 47. golden_045 - skill `ai-ml` (disagreement)

> ...in a startup or scale-up environment. - Prior experience integrating AI into SaaS business workflows, ideally in a client-facing or forward-deployed...

- A: (did not label this)
- B: `ai-ml` · nice_to_have · raw_text: "integrating AI into SaaS business workflows"

PROPOSED: `B` - Bonus Qualifications bullet, so nice_to_have; no required `ai-ml` mention elsewhere in golden_045

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 48. golden_045 - skill `full-stack-development` (disagreement)

> ...talk about, and still enjoy writing code yourself. - Have deep hands-on experience across the stack (frontend, backend, data, infrastructure/cloud) and a...

- A: (did not label this)
- B: `full-stack-development` · required · raw_text: "deep hands-on experience across the stack"

PROPOSED: `B` - qualification bullet names hands-on experience across the stack

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 49. golden_045 - skill `llm-orchestration` (disagreement)

> ...ecosystem (agents, memory systems, vector databases, orchestration frameworks). - Experience working with distributed or multi-location...

- A: `llm-orchestration` · nice_to_have · raw_text: "orchestration frameworks"
- B: (did not label this)

PROPOSED: `A` - Bonus Qualifications bullet names "orchestration frameworks", so nice_to_have

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 50. golden_045 - skill `software-architecture` (disagreement)

> ...backend, data, infrastructure/cloud) and a track record of architecting and shipping production-grade software, preferably with AI...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "architecting"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 51. golden_045 - skill `software-engineering` (disagreement)

> ...top of the latest tools, models and trends in AI-assisted software engineering. You are excellent at context engineering (incl....

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software engineering"

PROPOSED: `drop` - but on different ground than you gave: this bullet is under Requirements, not a responsibility. See the note in my reply

Options: `A` / `B` / `both` / `drop`

DECISION: drop

## 52. golden_046 - skill `ai-ml` (disagreement)

> ...interessierst Dich für aktuelle Entwicklungen rund um Künstliche Intelligenz, Large Language Models (LLM), AI-Agenten und moderne...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Künstliche Intelligenz"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 53. golden_046 - skill `llms` (disagreement)

> ...für aktuelle Entwicklungen rund um Künstliche Intelligenz, Large Language Models (LLM), AI-Agenten und moderne AI-Plattformen. Idealerweise konntest Du in...

- A: `llms` · nice_to_have · raw_text: "Large Language Models (LLM), AI-Agenten"
- B: `llms` · required · raw_text: "Large Language Models (LLM)"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 54. golden_046 - skill `rag` (disagreement)

> ...Model Context Protocol (MCP), Agenten-Frameworks oder Retrieval-Pipelines sind für Dich keine Fremdwörter oder Du hast großes...

- A: `rag` · required · raw_text: "Retrieval-Pipelines"
- B: (did not label this)

PROPOSED: `A` - qualification sentence names "Retrieval-Pipelines"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 55. golden_048 - skill `ai-ml` (disagreement)

> ...(Must-have): Du besitzt praxiserprobte Erfahrung im Einsatz von KI-Tools und LLMs im Marketing-Kontext (z. B. Prompting für...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Einsatz von KI-Tools"

PROPOSED: `B` - golden_048 is out of scope, so this is discarded either way; any answer only satisfies the all-decided guard

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 56. golden_025 - attribute `degree` (uncertain)

> ...der technischen Exzellenz in der ALDB. **Dein Profil** - Studium der Informatik oder vergleichbar, oder Du überzeugst uns, dass es auch anders geht - Fundierte Erfahrung in Architektur und Entwicklung...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Studium der Informatik oder vergleichbar, oder Du überzeugst uns, dass es auch anders geht"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Studium der Informatik oder vergleichbar, oder Du überzeugst uns, dass es auch anders geht"

PROPOSED: `ok` - degree named with no level -> bachelor; "oder vergleichbar" -> or_equivalent true

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_025 - attribute `seniority` (uncertain)

> Distinguished Engineer – Software & AI Products (w/m/d) **Ab sofort in Berlin,...

- A: value="senior" · basis="stated" · signal="Distinguished Engineer"
- B: value="senior" · basis="stated" · signal="Distinguished Engineer"

PROPOSED: `ok` - the title names the level. "Distinguished Engineer" is not in the guide's senior list, though

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_025 - skill `apis` (uncertain)

> ...Cloud, CI/CD, DevSecOps, Infrastructure as Code, REST, Datenpipelines sowie gängigen Technologien wie Java,...

- A: `apis` · required · raw_text: "REST"
- B: `apis` · required · raw_text: "REST"

PROPOSED: `ok` - "REST" is a named technology in a requirements list

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_025 - skill `software-architecture` (uncertain)

> ...uns, dass es auch anders geht - Fundierte Erfahrung in Architektur und Entwicklung komplexer Softwaresysteme sowie in einer technischen Führungsrolle - Tiefgreifende...

- A: `software-architecture` · required · raw_text: "Architektur und Entwicklung komplexer Softwaresysteme"
- B: `software-architecture` · required · raw_text: "Architektur"

PROPOSED: `B` - shortest verbatim phrase that supports the skill; A's quote is the whole bullet

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_026 - attribute `seniority` (uncertain)

> (Senior) Platform Engineer - Kubernetes, Private AI...

- A: value="senior" · basis="stated" · signal="(Senior) Platform Engineer"
- B: value="senior" · basis="stated" · signal="(Senior) Platform Engineer"

PROPOSED: `ok` - "(Senior)" in the title, basis stated

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_026 - skill `ai-infrastructure` (uncertain)

> ...Einsatz Du hast idealerweise erste Berührungspunkte mit AI-Plattform-Infrastruktur / GPU-Workloads oder großes Interesse, dich in diese...

- A: `ai-infrastructure` · nice_to_have · raw_text: "AI-Plattform-Infrastruktur"
- B: `ai-infrastructure` · nice_to_have · raw_text: "AI-Plattform-Infrastruktur"

PROPOSED: `ok` - named in an optional section, so nice_to_have

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_027 - skill `ai-deployment` (uncertain)

> ...(CI/CD, IaC, Container, Kubernetes) * Know-how in LLMOps (Deployment-Patterns, Versionierung, Testing, Monitoring) für produktive...

- A: `ai-deployment` · required · raw_text: "Deployment-Patterns"
- B: `ai-deployment` · required · raw_text: "Deployment-Patterns"

PROPOSED: `ok` - "Deployment-Patterns" names it in a requirements list

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_027 - skill `model-versioning` (uncertain)

> ...Kubernetes) * Know-how in LLMOps (Deployment-Patterns, Versionierung, Testing, Monitoring) für produktive AI-Systeme sowie...

- A: `model-versioning` · required · raw_text: "Versionierung"
- B: `model-versioning` · required · raw_text: "Versionierung"

PROPOSED: `ok` - "Versionierung" names model versioning in a list of MLOps practices

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_027 - skill `software-architecture` (uncertain)

> ...sowie gutes Verständnis von Security, Skalierbarkeit und Architekturdesign in komplexen, regulierten Umgebungen * Projektabhängige...

- A: `software-architecture` · required · raw_text: "Architekturdesign"
- B: `software-architecture` · required · raw_text: "Architekturdesign"

PROPOSED: `ok` - "Architekturdesign" names it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_028 - skill `ai-deployment` (uncertain)

> ...zwingend erforderlich - Erfahrung in der Evaluation, Deployment und dem produktiven Betrieb von KI-Modellen - Erfahrung...

- A: `ai-deployment` · required · raw_text: "Deployment"
- B: `ai-deployment` · required · raw_text: "Deployment und dem produktiven Betrieb von KI-Modellen"

PROPOSED: `A` - shortest phrase that supports the skill

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_028 - skill `llms` (uncertain)

> ...im Prompt-, Kontext- und Tool-Engineering von generativen KI-Modellen - Erfahrung in der Backend-Entwicklung mit Python, Go,...

- A: `llms` · required · raw_text: "generativen KI-Modellen"
- B: `llms` · required · raw_text: "generativen KI-Modellen"

PROPOSED: `ok` - "generativen KI-Modellen" is the posting's word for LLMs

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_028 - skill `model-development` (uncertain)

> ...Stakeholdern zu vertreten - Erfahrung in der Entwicklung, Fine-Tuning und Training von KI Modellen ist von Vorteil - Verhandlungssichere Deutschkenntnisse...

- A: `model-development` · nice_to_have · raw_text: "Entwicklung, Fine-Tuning und Training von KI Modellen"
- B: `model-development` · nice_to_have · raw_text: "Entwicklung, Fine-Tuning und Training von KI Modellen"

PROPOSED: `ok` - `fine-tuning` is already a separate accepted criterion, so the shared span loses nothing

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_029 - skill `ai-developer-tooling` (uncertain)

> ...darunter KI-gestützte Testfallgenerierung, KI-assistiertes Code-Authoring und synthetische Testdatenerzeugung - Erfahrung in der...

- A: `ai-developer-tooling` · required · raw_text: "KI-assistiertes Code-Authoring"
- B: `ai-developer-tooling` · required · raw_text: "KI-assistiertes Code-Authoring"

PROPOSED: `ok` - "KI-assistiertes Code-Authoring" names AI coding tooling

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_029 - skill `ai-ml` (uncertain)

> ...Erfahrung in der Integration von LLM-APIs und KI-Services in Testframeworks sowie im Aufbau KI-nativer Testlösungen...

- A: `ai-ml` · required · raw_text: "KI-Services"
- B: `ai-ml` · required · raw_text: "Einsatz von KI"

PROPOSED: `A` - "KI-Services" is the shorter of two phrases that each support it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_029 - skill `testing` (uncertain)

> ...in Java, Python oder C# mit gängigen Testautomatisierungstools / -frameworks wie Selenium, Robot Framework, Playwright, Cypress oder...

- A: `testing` · required · raw_text: "Testautomatisierungstools / -frameworks"
- B: `testing` · required · raw_text: "Testautomatisierungstools / -frameworks"

PROPOSED: `ok` - names test automation tooling in a requirements list

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_030 - skill `data-modeling` (uncertain)

> ...im SAP-Umfeld (z. B. SAP BTP, APIs, Integration, Datenmodelle) - Gutes Verständnis von SAP-Prozessen (z. B. Finance,...

- A: `data-modeling` · required · raw_text: "Datenmodelle"
- B: `data-modeling` · required · raw_text: "Datenmodelle"

PROPOSED: `ok` - "Datenmodelle" names data modeling

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_030 - skill `software-architecture` (uncertain)

> ...in technische Lösungen inkl. Prototyping - Kenntnisse moderner Architekturen, Cloud-Technologien und AI/ML sind von Vorteil - Als...

- A: `software-architecture` · nice_to_have · raw_text: "moderner Architekturen"
- B: `software-architecture` · nice_to_have · raw_text: "moderner Architekturen"

PROPOSED: `ok` - "von Vorteil" on the bullet -> nice_to_have, requirement rule 2

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_031 - skill `agents` (uncertain)

> ...Familiarity with prompt engineering best practices and agentic workflows. - Experience with distributed systems, streaming (e.g.,...

- A: `agents` · nice_to_have · raw_text: "agentic workflows"
- B: `agents` · nice_to_have · raw_text: "agentic workflows"

PROPOSED: `ok` - "agentic workflows" under an optional heading

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_032 - attribute `seniority` (uncertain)

> ...agentic and AI technologies, sharing best practices and mentoring peers to accelerate company-wide AI adoption.

- A: value="senior" · basis="inferred" · signal="mentoring peers"
- B: value="senior" · basis="inferred" · signal="mentoring peers"

PROPOSED: `ok` - "mentoring peers" is lead/mentoring duty, a valid inferred basis

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_032 - skill `agents` (uncertain)

> ...Hands-on experience designing, developing, and operating agentic systems using frameworks such as AWS AgentCore, Google Vertex AI,...

- A: `agents` · required · raw_text: "agentic systems"
- B: `agents` · required · raw_text: "agentic systems"

PROPOSED: `ok` - "agentic systems" names it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_032 - skill `cloud` (uncertain)

> ...LangChain, LangGraph, AutoGen, CrewAI or similar. - Cloud-native development: Proficient in AWS infrastructure (VPC, Lambda, S3, IAM,...

- A: `cloud` · required · raw_text: "Cloud-native development"
- B: `cloud` · required · raw_text: "Cloud-native development"

PROPOSED: `ok` - "Cloud-native development" names cloud

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_032 - skill `llm-guardrails` (uncertain)

> ...evaluation frameworks (for agents and prompts), runtime guardrails, and compliance controls for AI/agentic workflows. -...

- A: `llm-guardrails` · required · raw_text: "runtime guardrails"
- B: `llm-guardrails` · required · raw_text: "runtime guardrails"

PROPOSED: `ok` - "runtime guardrails" names it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_032 - skill `testing` (uncertain)

> ...of AI-powered development tools (e.g., code assistants, automated testing), and a commitment to responsible and innovative AI...

- A: `testing` · required · raw_text: "automated testing"
- B: `testing` · required · raw_text: "automated testing"

PROPOSED: `ok` - "automated testing" names it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 79. golden_033 - skill `ai-developer-tooling` (uncertain)

> ...actually used tools like Claude Code, Cursor, Copilot, or similar agentic coding tools to build something – not just asked ChatGPT to explain a...

- A: `ai-developer-tooling` · required · raw_text: "similar agentic coding tools"
- B: `ai-developer-tooling` · required · raw_text: "agentic coding tools"

PROPOSED: `B` - shortest phrase; A carries "similar" from the sentence

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 80. golden_034 - attribute `degree` (uncertain)

> WHO ARE WE LOOKING FOR:

- A: value=null · requirement=null · or_equivalent=false · signal=null
- B: value=null · requirement=null · or_equivalent=false · signal=null

PROPOSED: `ok` - the posting mentions no degree, so null is right

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 81. golden_035 - skill `agents` (uncertain)

> ...acceleration methods. - Experience supporting agentic workloads involving tool calling, structured outputs, streaming...

- A: `agents` · nice_to_have · raw_text: "agentic workloads"
- B: `agents` · nice_to_have · raw_text: "agentic workloads"

PROPOSED: `ok` - "agentic workloads" under an optional heading

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 82. golden_035 - skill `ai-deployment` (uncertain)

> ...skills in Python and PyTorch. - Hands-on experience deploying or optimizing LLM, VLM, or high-throughput transformer inference. -...

- A: `ai-deployment` · required · raw_text: "deploying or optimizing LLM"
- B: `ai-deployment` · required · raw_text: "deploying or optimizing LLM, VLM, or high-throughput transformer inference"

PROPOSED: `A` - shortest phrase that supports deployment; B's quote is the whole span, which item 85 uses for `inference-optimization`

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 83. golden_035 - skill `apis` (uncertain)

> ...workloads involving tool calling, structured outputs, streaming APIs, high concurrency, and multi-step orchestration. -...

- A: `apis` · nice_to_have · raw_text: "streaming APIs"
- B: `apis` · nice_to_have · raw_text: "streaming APIs"

PROPOSED: `ok` - "streaming APIs" named, optional marker on the bullet

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 84. golden_035 - skill `distributed-systems` (uncertain)

> ...and cost. - Experience designing or optimizing distributed inference system architecture, with hands-on work in one or more areas such as request...

- A: `distributed-systems` · required · raw_text: "distributed inference system architecture"
- B: `distributed-systems` · required · raw_text: "distributed inference system architecture"

PROPOSED: `ok` - "distributed inference system architecture" names it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 85. golden_035 - skill `inference-optimization` (uncertain)

> ...in Python and PyTorch. - Hands-on experience deploying or optimizing LLM, VLM, or high-throughput transformer inference. - Practical knowledge of at least one modern...

- A: `inference-optimization` · required · raw_text: "optimizing LLM, VLM, or high-throughput transformer inference"
- B: `inference-optimization` · required · raw_text: "optimizing LLM, VLM, or high-throughput transformer inference"

PROPOSED: `ok` - names inference optimization directly

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 86. golden_036 - attribute `degree` (uncertain)

> ...Intelligenz, Mathematik oder einem verwandten Bereich; ein Master oder Ph.D. ist von Vorteil. - Du bringst mindestens 5 Jahre praktische...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="ein Master oder Ph.D. ist von Vorteil"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="ein Master oder Ph.D. ist von Vorteil"

PROPOSED: `ok` by the guide: `degree` is the highest level named and the Master/PhD mention is marked "von Vorteil". But see the note in my reply - the posting also requires a degree outright

NOTE: decided `ok` on the guide's letter, and logged as guide-gap clarification candidate #4 (DECISIONS, after HIR-70): a posting that requires a degree and prefers a higher one loses the required level, because `degree` takes the highest level named and that mention carries the optional marker.

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 87. golden_036 - skill `ai-ml` (uncertain)

> ...Berufserfahrung in der Entwicklung und Implementierung von AI- und Machine-Learning-Lösungen mit und hast entsprechende Lösungen sowohl on Prem als...

- A: `ai-ml` · required · raw_text: "AI- und Machine-Learning-Lösungen"
- B: `ai-ml` · required · raw_text: "AI- und Machine-Learning-Lösungen"

PROPOSED: `ok` - "AI- und Machine-Learning-Lösungen" names it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 88. golden_036 - skill `software-architecture` (uncertain)

> ...und kennst agile Softwareentwicklungsmethoden sowie die Anforderungen moderner Enterprise-Architekturen. - Du arbeitest selbstständig und kooperativ in...

- A: `software-architecture` · required · raw_text: "Anforderungen moderner Enterprise-Architekturen"
- B: `software-architecture` · required · raw_text: "Softwarelösungen konzipieren, designen"

PROPOSED: `A` - "Enterprise-Architekturen" names architecture; B's quote is the span item 89 uses for `software-engineering`

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 89. golden_036 - skill `software-engineering` (uncertain)

> ...LangChain oder vergleichbaren Technologien. - Du kannst Softwarelösungen konzipieren, designen und entwickeln, idealerweise im AI-/GenAI-Umfeld, und kennst agile...

- A: `software-engineering` · required · raw_text: "Softwarelösungen konzipieren, designen und entwickeln"
- B: `software-engineering` · required · raw_text: "Softwarelösungen konzipieren, designen und entwickeln"

PROPOSED: `ok` - a qualification bullet naming the practice, the clean form of your rule 1

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 90. golden_037 - skill `aws` (uncertain)

> ...API / TS + Python for ML Services - Hosting: Railway (Moving to AWS) - AI: Azure / OpenAI, Gemini, Cohere - Obsv., Eval. &...

- A: `aws` · required · raw_text: "Moving to AWS"
- B: `aws` · required · raw_text: "Moving to AWS"

PROPOSED: `ok` - AWS is named in the tech-stack list, requirement rule 3. "Moving to AWS" is a plan, not current, so override if that matters

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 91. golden_037 - skill `backend-development` (uncertain)

> ...File Storage: Supabase (postgress) / Weaviate / AWS S3 - Backend (Document Pipelines & applied AI): Fastify API / TS +...

- A: `backend-development` · required · raw_text: "Backend"
- B: `backend-development` · required · raw_text: "Backend"

PROPOSED: `ok` - "Backend" heads a stack line

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 92. golden_037 - skill `evaluation` (uncertain)

> ...to AWS) - AI: Azure / OpenAI, Gemini, Cohere - Obsv., Eval. & Tracking: Langfuse, Datadog Your profile - You thrive...

- A: `evaluation` · required · raw_text: "Eval."
- B: `evaluation` · required · raw_text: "Eval."

PROPOSED: `ok` - "Eval." is the posting's own abbreviation in the stack list; raw_text must be verbatim

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 93. golden_037 - skill `llms` (uncertain)

> ...features - You are passionate about the potential of GenAI, a strong believer in its transformative power, and eager...

- A: `llms` · required · raw_text: "GenAI"
- B: `llms` · required · raw_text: "GenAI"

PROPOSED: `ok` - "GenAI" is the posting's word for LLMs

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 94. golden_037 - skill `observability` (uncertain)

> ...(Moving to AWS) - AI: Azure / OpenAI, Gemini, Cohere - Obsv., Eval. & Tracking: Langfuse, Datadog Your profile - You...

- A: `observability` · required · raw_text: "Obsv."
- B: `observability` · required · raw_text: "Obsv."

PROPOSED: `ok` - "Obsv." abbreviated in the stack list, same as item 92

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 95. golden_037 - skill `postgresql` (uncertain)

> ...Database / Vector DB and File Storage: Supabase (postgress) / Weaviate / AWS S3 - Backend (Document Pipelines &...

- A: `postgresql` · required · raw_text: "postgress"
- B: `postgresql` · required · raw_text: "postgress"

PROPOSED: `ok` - "postgress" is the posting's typo; raw_text is verbatim, the skill_id is not

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 96. golden_038 - attribute `degree` (uncertain)

> ...good outcomes - Bias towards progress over perfection - BSc in Computer Science, Maths or Statistics or related discipline Bonus skills & attributes - Previous experience in...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="BSc in Computer Science, Maths or Statistics or related discipline"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="BSc in Computer Science, Maths or Statistics or related discipline"

PROPOSED: `ok` - "BSc" names bachelor, no equivalence offered

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 97. golden_038 - skill `software-engineering` (uncertain)

> ...you can be highly effective immediately by bringing excellent software engineering skills, and learn ML as you work on the team. - You can...

- A: `software-engineering` · required · raw_text: "excellent software engineering skills"
- B: `software-engineering` · required · raw_text: "excellent software engineering skills"

PROPOSED: `ok` - "excellent software engineering skills", a qualification bullet naming the practice

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 98. golden_038 - skill `statistics` (uncertain)

> ...attributes - Previous experience in data analytics, or statistical role #LI-Hybrid Unleash Your Potential When you join...

- A: `statistics` · nice_to_have · raw_text: "statistical role"
- B: `statistics` · nice_to_have · raw_text: "statistical role"

PROPOSED: `ok` - "statistical role" under an optional heading

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 99. golden_040 - skill `ai-deployment` (uncertain)

> ...Experience beyond model training, including evaluation, deployment, and production support; • Experience optimizing models for edge or embedded...

- A: `ai-deployment` · required · raw_text: "deployment, and production support"
- B: `ai-deployment` · required · raw_text: "deployment"

PROPOSED: `B` - shortest phrase; A's quote carries "production support" too

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 100. golden_040 - skill `experiment-tracking` (uncertain)

> ...TensorRT, OpenVINO, or TFLite; • Experience with MLOps and experiment tools such as MLflow, Weights & Biases, or DVC; • Familiarity...

- A: `experiment-tracking` · nice_to_have · raw_text: "experiment tools"
- B: `experiment-tracking` · nice_to_have · raw_text: "experiment tools"

PROPOSED: `ok` - "experiment tools" under an optional heading

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 101. golden_040 - skill `inference-optimization` (uncertain)

> ...deployment, and production support; • Experience optimizing models for edge or embedded environments; • Strong software engineering skills, including C++...

- A: `inference-optimization` · required · raw_text: "optimizing models for edge or embedded environments"
- B: `inference-optimization` · required · raw_text: "optimizing models for edge or embedded environments"

PROPOSED: `ok` - names optimization for edge and embedded targets

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 102. golden_041 - skill `ci-cd` (uncertain)

> ...praktische Erfahrung mit Cloud Computing und Docker mit; Kenntnisse in CI/CD, Container-Orchestrierung oder Infrastructure as Code sind...

- A: `ci-cd` · nice_to_have · raw_text: "Kenntnisse in CI/CD"
- B: `ci-cd` · nice_to_have · raw_text: "Kenntnisse in CI/CD"

PROPOSED: `ok` - "von Vorteil" section -> nice_to_have. raw_text could trim to "CI/CD"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 103. golden_041 - skill `infrastructure-as-code` (uncertain)

> ...mit; Kenntnisse in CI/CD, Container-Orchestrierung oder Infrastructure as Code sind willkommen * Du verstehst Machine Learning und Data...

- A: `infrastructure-as-code` · nice_to_have · raw_text: "Infrastructure as Code"
- B: `infrastructure-as-code` · nice_to_have · raw_text: "Infrastructure as Code"

PROPOSED: `ok` - "Infrastructure as Code" named, optional section

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 104. golden_041 - skill `software-engineering` (uncertain)

> ...Du verfügst über mehrjährige Berufserfahrung in der professionellen Softwareentwicklung und hast bereits produktive Anwendungen entwickelt und...

- A: `software-engineering` · required · raw_text: "professionellen Softwareentwicklung"
- B: `software-engineering` · required · raw_text: "professionellen Softwareentwicklung"

PROPOSED: `ok` - "professionellen Softwareentwicklung" names the practice

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 105. golden_042 - attribute `degree` (uncertain)

> ...Engineering, Software Engineering or a related field. • MSc or higher in ML, Computer Science or a related discipline, or equivalent professional experience. • 5+ years' industry experience designing and...

- A: value="master" · requirement="required" · or_equivalent=true · signal="MSc or higher in ML, Computer Science or a related discipline, or equivalent professional experience"
- B: value="master" · requirement="required" · or_equivalent=true · signal="MSc or higher in ML, Computer Science or a related discipline, or equivalent professional experience"

PROPOSED: `ok` - "MSc or higher" -> master, "or equivalent professional experience" -> or_equivalent true

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 106. golden_042 - skill `deep-learning` (uncertain)

> ...or JAX. • Experience contributing to high-quality deep learning rese

- A: `deep-learning` · required · raw_text: "deep learning"
- B: `deep-learning` · required · raw_text: "deep learning"

PROPOSED: `ok` - "deep learning" named

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 107. golden_042 - skill `machine-learning` (uncertain)

> ...and large-scale ML workloads. • Extensive experience with ML frameworks such as PyTorch, TensorFlow or JAX. • Experience...

- A: `machine-learning` · required · raw_text: "ML frameworks"
- B: `machine-learning` · required · raw_text: "ML workflows"

PROPOSED: `B` - "ML workflows" is shorter and sits in the 5+ years requirement bullet; "ML frameworks" belongs to PyTorch/TensorFlow/JAX

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 108. golden_043 - skill `data-privacy-and-security` (uncertain)

> ...verzerrte Ergebnisse, unerwünschte Eingaben oder den Schutz sensibler Daten - Erfahrung in Banking- oder Fintech-Umfelder ist...

- A: `data-privacy-and-security` · required · raw_text: "den Schutz sensibler Daten"
- B: `data-privacy-and-security` · required · raw_text: "Schutz sensibler Daten"

PROPOSED: `B` - shortest phrase; A carries the article

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 109. golden_044 - skill `ai-infrastructure` (uncertain)

> ...can be measured. - Integrate models and build inference infrastructure to make AI practical at scale. - Create shared...

- A: `ai-infrastructure` · required · raw_text: "inference infrastructure"
- B: `ai-infrastructure` · required · raw_text: "inference infrastructure"

PROPOSED: `ok` - "inference infrastructure" names it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 110. golden_044 - skill `evaluation` (uncertain)

> ...and help other engineers succeed. - Familiarity with evaluation frameworks and failure investigation is useful; procurement...

- A: `evaluation` · required · raw_text: "evaluation frameworks"
- B: `evaluation` · required · raw_text: "evaluation frameworks"

PROPOSED: `ok` - "evaluation frameworks" names it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 111. golden_044 - skill `python` (uncertain)

> ...engineering fundamentals and hands-on TypeScript skills; Python experience is useful. - Experience shipping LLM-powered systems to real...

- A: `python` · required · raw_text: "Python experience is useful"
- B: `python` · required · raw_text: "Python experience is useful"

PROPOSED: override to nice_to_have, same raw_text - "Python experience is useful" is an inline optional marker (requirement rule 2); "is useful" has the force of the listed "is an advantage". Both labelers said required, so this is an agreed-and-wrong, not a disagreement

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: {"requirement": "nice_to_have", "raw_text": "Python experience is useful"}

## 112. golden_045 - skill `ai-developer-tooling` (uncertain)

> ...them into business workflows. - Be on top of the latest tools, models and trends in AI-assisted software engineering. You are excellent at context engineering (incl....

- A: `ai-developer-tooling` · required · raw_text: "tools, models and trends in AI-assisted software engineering"
- B: `ai-developer-tooling` · required · raw_text: "tools, models and trends in AI-assisted software engineering"

PROPOSED: `ok` - this is the bullet item 51 also quotes, and this is the skill it actually names

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 113. golden_045 - skill `model-selection` (uncertain)

> ...are excellent at context engineering (incl. prompting), know when to leverage which model, and have first-hand experience with Claude Code or...

- A: `model-selection` · required · raw_text: "know when to leverage which model"
- B: `model-selection` · required · raw_text: "know when to leverage which model"

PROPOSED: `ok` - "know when to leverage which model" names model selection

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 114. golden_046 - attribute `degree` (uncertain)

> ...und Betriebsprozess. Dein Profil: Du hast ein Studium der Informatik, Wirtschaftsinformatik oder eine vergleichbare technische Ausbildung erfolgreich abgeschlossen und bringst erste praktische Erfahrungen in der...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Studium der Informatik, Wirtschaftsinformatik oder eine vergleichbare technische Ausbildung erfolgreich abgeschlossen"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="ein Studium der Informatik, Wirtschaftsinformatik oder eine vergleichbare technische Ausbildung erfolgreich abgeschlossen"

PROPOSED: `A` - same values both sides; A's signal is the same span without the leading article

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 115. golden_046 - skill `agents` (uncertain)

> ...mit. Begriffe wie OpenAPI, Model Context Protocol (MCP), Agenten-Frameworks oder Retrieval-Pipelines sind für Dich keine Fremdwörter...

- A: `agents` · required · raw_text: "Agenten-Frameworks"
- B: `agents` · required · raw_text: "AI-Agenten"

PROPOSED: `B` - "AI-Agenten" is the shorter phrase naming agents; A's "Agenten-Frameworks" sits in the APIs/MCP bullet

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 116. golden_046 - skill `mcp` (uncertain)

> ...von APIs und Services mit. Begriffe wie OpenAPI, Model Context Protocol (MCP), Agenten-Frameworks oder Retrieval-Pipelines sind für Dich...

- A: `mcp` · required · raw_text: "Model Context Protocol (MCP)"
- B: `mcp` · required · raw_text: "Model Context Protocol (MCP)"

PROPOSED: `ok` - "Model Context Protocol (MCP)" named

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 117. golden_047 - skill `devops` (uncertain)

> ...LangChain/LangGraph) in Unternehmensumgebungen Dank deiner praktischen Erfahrung in DevOps-Projekten verfügst du über Kenntnisse in einer der folgenden...

- A: `devops` · required · raw_text: "praktischen Erfahrung in DevOps-Projekten"
- B: `devops` · required · raw_text: "DevOps-Projekten"

PROPOSED: `B` - shortest phrase that supports DevOps

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 118. golden_047 - skill `gcp` (uncertain)

> ...mit Microsoft Azure oder einem anderen Cloud-Anbieter wie AWS oder Google Mündliche und schriftliche Kommunikationsfähigkeit in...

- A: `gcp` · required · raw_text: "AWS oder Google"
- B: `gcp` · required · raw_text: "Google"

PROPOSED: `B` - "Google" alone; A's quote also names AWS, which is its own criterion

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 119. golden_047 - skill `llm-orchestration` (uncertain)

> ...KI-Lösungen (LLMs, Vektordatenbanken, RAG-Pipelines, Orchestrierungs-Frameworks wie LangChain/LangGraph) in Unternehmensumgebungen Dank...

- A: `llm-orchestration` · required · raw_text: "Orchestrierungs-Frameworks"
- B: `llm-orchestration` · required · raw_text: "Orchestrierungs-Frameworks"

PROPOSED: `ok` - "Orchestrierungs-Frameworks" names it

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 120. golden_048 - skill `prompt-engineering` (uncertain)

> ...Einsatz von KI-Tools und LLMs im Marketing-Kontext (z. B. Prompting für Reporting, Kampagnenanalysen oder Creative-Unterstützung). Du...

- A: `prompt-engineering` · required · raw_text: "Prompting für Reporting"
- B: `prompt-engineering` · required · raw_text: "Prompting"

PROPOSED: `B` - shortest phrase. golden_048 is out of scope, so this is discarded either way

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 121. golden_029 - skill `agents|agent-architecture` (mapping)

> ...wie Self-Healing Locators, autonome Testausführung und agentenbasierte Testarchitekturen - Erfahrung in der nahtlosen Integration automatisierter...

- A: `agents` · required · raw_text: "agentenbasierte Testarchitekturen"
- B: `agent-architecture` · required · raw_text: "agentenbasierte Testarchitekturen"

PROPOSED: `B` - the phrase names agent-based test *architectures*, and a specific skill does not imply its parents. `both` is defensible if "agentenbasierte" counts as naming agents on its own

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 122. golden_025 - attribute `german` (spot-check)

> ...und souveränes Auftreten auf oberster Führungsebene - Verhandlungssichere Deutsch- und Englischkenntnisse **Deine Benefits** - **Sicherer Arbeitsplatz**:...

- agreed label: value="required" · basis="stated" · signal="Verhandlungssichere Deutsch- und Englischkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_025 - skill `java` (spot-check)

> ...Code, REST, Datenpipelines sowie gängigen Technologien wie Java, Python, TypeScript und React - Gute Kenntnisse im Bereich...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_026 - skill `gitops` (spot-check)

> ...Du denkst in Automatisierungslösungen wie Terraform, Helm, GitOps und CI/CD Du fühlst dich in dynamischen...

- agreed label: `gitops` · required · raw_text: "GitOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_026 - skill `linux` (spot-check)

> ...diese Themen einzuarbeiten Du besitzt solide Kenntnisse in Linux, Netzwerken und Troubleshooting Du denkst in...

- agreed label: `linux` · required · raw_text: "Linux"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_026 - skill `networking` (spot-check)

> ...einzuarbeiten Du besitzt solide Kenntnisse in Linux, Netzwerken und Troubleshooting Du denkst in Automatisierungslösungen...

- agreed label: `networking` · required · raw_text: "Netzwerken"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_027 - skill `containerization` (spot-check)

> ...Azure oder GCP) sowie modernen DevOps-Stacks (CI/CD, IaC, Container, Kubernetes) * Know-how in LLMOps (Deployment-Patterns,...

- agreed label: `containerization` · required · raw_text: "Container"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_027 - skill `devops` (spot-check)

> ...mit Cloud-Plattformen (AWS, Azure oder GCP) sowie modernen DevOps-Stacks (CI/CD, IaC, Container, Kubernetes) * Know-how in LLMOps...

- agreed label: `devops` · required · raw_text: "DevOps-Stacks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_027 - skill `evaluation` (spot-check)

> ...(LLM APIs, Embeddings, RAG, Prompt Engineering, Evaluierung) * Starker Hintergrund in Software Engineering mit Fokus...

- agreed label: `evaluation` · required · raw_text: "Evaluierung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_027 - skill `infrastructure-as-code` (spot-check)

> ...(AWS, Azure oder GCP) sowie modernen DevOps-Stacks (CI/CD, IaC, Container, Kubernetes) * Know-how in LLMOps...

- agreed label: `infrastructure-as-code` · required · raw_text: "IaC"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_027 - skill `microservices` (spot-check)

> ...in Software Engineering mit Fokus auf Backend, APIs, Microservices oder verteilte Systeme * Praxiserfahrung mit...

- agreed label: `microservices` · required · raw_text: "Microservices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_027 - skill `software-engineering` (spot-check)

> ...Prompt Engineering, Evaluierung) * Starker Hintergrund in Software Engineering mit Fokus auf Backend, APIs, Microservices oder verteilte...

- agreed label: `software-engineering` · required · raw_text: "Software Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_027 - skill `testing` (spot-check)

> ...Know-how in LLMOps (Deployment-Patterns, Versionierung, Testing, Monitoring) für produktive AI-Systeme sowie gutes...

- agreed label: `testing` · required · raw_text: "Testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_028 - attribute `degree` (spot-check)

> ...uns auf unserer gemeinsamen Mission! Dein Profil: - Abgeschlossenes Masterstudium der Informatik, Mathematik oder einer vergleichbaren Fachrichtung - Mindestens 5 Jahre relevante Berufserfahrung nach...

- agreed label: value="master" · requirement="required" · or_equivalent=false · signal="Abgeschlossenes Masterstudium der Informatik, Mathematik oder einer vergleichbaren Fachrichtung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_028 - attribute `german` (spot-check)

> ...und Training von KI Modellen ist von Vorteil - Verhandlungssichere Deutschkenntnisse sowie sehr gute Englischkenntnisse in Wort und...

- agreed label: value="required" · basis="stated" · signal="Verhandlungssichere Deutschkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_028 - skill `backend-development` (spot-check)

> ...von generativen KI-Modellen - Erfahrung in der Backend-Entwicklung mit Python, Go, Rust oder Java - Erfahrung mit On-Prem...

- agreed label: `backend-development` · required · raw_text: "Backend-Entwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_028 - skill `cloud` (spot-check)

> ...mit Python, Go, Rust oder Java - Erfahrung mit On-Prem Cloud-Techniken (z. B. Kubernetes) und MLOps-Frameworks (MLFlow,...

- agreed label: `cloud` · required · raw_text: "On-Prem Cloud-Techniken"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_028 - skill `grafana` (spot-check)

> ...in Leistungsoptimierung und Monitoring (z. B. Prometheus, Grafana) - Fähigkeit, technische Konzepte eigenständig zu...

- agreed label: `grafana` · required · raw_text: "Grafana"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_028 - skill `prompt-engineering` (spot-check)

> ...dem produktiven Betrieb von KI-Modellen - Erfahrung im Prompt-, Kontext- und Tool-Engineering von generativen KI-Modellen - Erfahrung in der...

- agreed label: `prompt-engineering` · required · raw_text: "Prompt-, Kontext- und Tool-Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_029 - attribute `degree` (spot-check)

> ...KI-Fokus sollten Sie mitbringen:** - Abgeschlossenes Studium in Informatik, Wirtschaftsinformatik oder vergleichbare Qualifikation - Fundierte Programmier- und Automatisierungskenntnisse in...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossenes Studium in Informatik, Wirtschaftsinformatik oder vergleichbare Qualifikation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_029 - skill `github-actions` (spot-check)

> ...gängiger Plattformen wie Jenkins, GitLab CI, GitHub Actions und Azure DevOps - Kenntnisse im Einsatz von KI zur...

- agreed label: `github-actions` · required · raw_text: "GitHub Actions"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_029 - skill `gitlab-ci` (spot-check)

> ...Tests in CI/CD-Pipelines gängiger Plattformen wie Jenkins, GitLab CI, GitHub Actions und Azure DevOps - Kenntnisse im Einsatz...

- agreed label: `gitlab-ci` · required · raw_text: "GitLab CI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_029 - skill `python` (spot-check)

> ...Programmier- und Automatisierungskenntnisse in Java, Python oder C# mit gängigen Testautomatisierungstools /...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_030 - attribute `degree` (spot-check)

> ...Weiterentwicklung des Themas AI **Dein Skillset** - Abgeschlossenes Studium (Informatik, Wirtschaftsinformatik, BWL mit IT-Schwerpunkt) oder vergleichbare Qualifikation - Fundiertes Wissen in SAP Business AI (inkl. SAP Joule)...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossenes Studium (Informatik, Wirtschaftsinformatik, BWL mit IT-Schwerpunkt) oder vergleichbare Qualifikation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_031 - skill `llamaindex` (spot-check)

> ...e.g., OpenAI, Anthropic, or similar) and frameworks such as LangChain or LlamaIndex. - Experience with RAG architectures, embeddings, and...

- agreed label: `llamaindex` · required · raw_text: "LangChain or LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_031 - skill `llms` (spot-check)

> ...similar backend frameworks. - Experience working with LLM APIs (e.g., OpenAI, Anthropic, or similar) and frameworks such a...

- agreed label: `llms` · required · raw_text: "LLM APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_031 - skill `machine-learning` (spot-check)

> ...Kafka), or large-scale applications. - Background in machine learning fundamentals (e.g., scikit-learn, PyTorch, or TensorFlow). -...

- agreed label: `machine-learning` · nice_to_have · raw_text: "machine learning fundamentals"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_031 - skill `open-source-llms` (spot-check)

> ...Experience fine-tuning or evaluating open-source LLMs. -...

- agreed label: `open-source-llms` · nice_to_have · raw_text: "open-source LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_031 - skill `rag` (spot-check)

> ...Experience with RAG architectures, embeddings, and vector databases (e.g., Pinecone,...

- agreed label: `rag` · required · raw_text: "RAG architectures"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_032 - attribute `german` (spot-check)

> AI Systems Engineer (d/f/m)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_032 - skill `apis` (spot-check)

> ...record of building production-grade backend services and APIs. - System integration: Experience integrating agents with...

- agreed label: `apis` · required · raw_text: "APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_032 - skill `java` (spot-check)

> ...expertise: Strong coding skills in Python and/or Java, with a track record of building production-grade backend...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_032 - skill `kubernetes` (spot-check)

> ...experience in cross-account integrations, Terraform, and Kubernetes. - Programming expertise: Strong coding skills in Python...

- agreed label: `kubernetes` · required · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_032 - skill `langchain` (spot-check)

> ...such as AWS AgentCore, Google Vertex AI, Bedrock, LangChain, LangGraph, AutoGen, CrewAI or similar. - Cloud-native...

- agreed label: `langchain` · required · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_032 - skill `observability` (spot-check)

> ...Observability, evaluation and compliance: Familiarity with implementing observability, evaluation frameworks (for agents and prompts), runtime...

- agreed label: `observability` · required · raw_text: "implementing observability"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 156. golden_032 - skill `recommender-systems` (spot-check)

> ...Experience integrating agents with microservices, recommendation engines, and vector databases (e.g., S3 Vector, OpenSearch),...

- agreed label: `recommender-systems` · required · raw_text: "recommendation engines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 157. golden_032 - skill `terraform` (spot-check)

> ...with experience in cross-account integrations, Terraform, and Kubernetes. - Programming expertise: Strong coding...

- agreed label: `terraform` · required · raw_text: "Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 158. golden_034 - attribute `seniority` (spot-check)

> WHO ARE WE LOOKING FOR: We are looking for an experienced Senior Cloud Software Engineer AI (m/f/d) for our team working on the productization of our...

- agreed label: value="senior" · basis="stated" · signal="Senior Cloud Software Engineer AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 159. golden_034 - skill `cloud` (spot-check)

> ...C++. - You have several years of experience implementing cloud infrastructure solutions, specifically IaC with Terraform and...

- agreed label: `cloud` · required · raw_text: "cloud infrastructure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 160. golden_034 - skill `cpp` (spot-check)

> ...in at least one programming language, either Python or C++. - You have several years of experience implementing...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 161. golden_034 - skill `infrastructure-as-code` (spot-check)

> ...implementing cloud infrastructure solutions, specifically IaC with Terraform and Kubernetes. - You enjoy working in an...

- agreed label: `infrastructure-as-code` · required · raw_text: "IaC"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 162. golden_035 - attribute `german` (spot-check)

> Senior Machine Learning Engineer, LLM Inference Optimization

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 163. golden_035 - attribute `seniority` (spot-check)

> Senior Machine Learning Engineer, LLM Inference Optimization About Nebius: Nebius is...

- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 164. golden_035 - skill `pytorch` (spot-check)

> ...explanations. Must-haves - Strong engineering skills in Python and PyTorch. - Hands-on experience deploying or optimizing LLM, VLM,...

- agreed label: `pytorch` · required · raw_text: "Python and PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 165. golden_035 - skill `tool-calling` (spot-check)

> ...Experience supporting agentic workloads involving tool calling, structured outputs, streaming APIs, high concurrency, and...

- agreed label: `tool-calling` · nice_to_have · raw_text: "tool calling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 166. golden_035 - skill `vllm` (spot-check)

> ...Practical knowledge of at least one modern inference stack, such as vLLM, SGLang, TensorRT-LLM, Triton Inference Server, NVIDIA...

- agreed label: `vllm` · required · raw_text: "inference stack, such as vLLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 167. golden_036 - attribute `german` (spot-check)

> ...und kooperativ in internationalen Teams, kommunizierst verhandlungssicher auf Deutsch (mind. C1) und Englisch und überzeugst mit effizientem Zeitmanagement...

- agreed label: value="required" · basis="stated" · signal="verhandlungssicher auf Deutsch (mind. C1)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 168. golden_036 - skill `cloud` (spot-check)

> ...und hast entsprechende Lösungen sowohl on Prem als auch in der Cloud umgesetzt. - Du verfügst zwingend über praktische...

- agreed label: `cloud` · required · raw_text: "in der Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 169. golden_036 - skill `langchain` (spot-check)

> ...wie SciKit-Learn, PyTorch, KubeFlow, HuggingFace, LangChain oder vergleichbaren Technologien. - Du kannst...

- agreed label: `langchain` · required · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 170. golden_036 - skill `llms` (spot-check)

> ...Du hast mindestens 1 Jahr praktische Erfahrung in der Entwicklung von GenAI-Lösungen, beispielsweise mit RAG oder AI Agents/Agenten, und kennst...

- agreed label: `llms` · required · raw_text: "Entwicklung von GenAI-Lösungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 171. golden_037 - skill `azure` (spot-check)

> ...for ML Services - Hosting: Railway (Moving to AWS) - AI: Azure / OpenAI, Gemini, Cohere - Obsv., Eval. & Tracking:...

- agreed label: `azure` · required · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 172. golden_037 - skill `gemini` (spot-check)

> ...Hosting: Railway (Moving to AWS) - AI: Azure / OpenAI, Gemini, Cohere - Obsv., Eval. & Tracking: Langfuse, Datadog Your...

- agreed label: `gemini` · required · raw_text: "Gemini"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 173. golden_039 - skill `conversational-ai` (spot-check)

> ...mehrjährige **Führungserfahrung**, Kenntnisse in **Conversational-AI**, Local-AI und Explainable-AI sowie fließendes Deutsch...

- agreed label: `conversational-ai` · required · raw_text: "Conversational-AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 174. golden_040 - attribute `german` (spot-check)

> Senior AI/Computer Vision Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 175. golden_040 - skill `cpp` (spot-check)

> ...Strong software engineering skills, including C++ production pipelines or inference systems; • Fluent in English. Nice To...

- agreed label: `cpp` · required · raw_text: "C++ production pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 176. golden_040 - skill `llms` (spot-check)

> ...Fluent in English. Nice To Have • Experience with LLMs or multimodal models in production; • Experience with...

- agreed label: `llms` · nice_to_have · raw_text: "LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 177. golden_040 - skill `tensorflow` (spot-check)

> ...Strong Python skills; • Solid experience with PyTorch, TensorFlow, or similar frameworks; • 4+ years of experience building...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 178. golden_041 - skill `cloud` (spot-check)

> ...integrieren * Du bringst praktische Erfahrung mit Cloud Computing und Docker mit; Kenntnisse in CI/CD,...

- agreed label: `cloud` · required · raw_text: "Cloud Computing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 179. golden_041 - skill `llms` (spot-check)

> ...aus * Du hast fundierte Erfahrung mit NLP und generativer KI und kannst Modelle und Frameworks nicht nur anwenden,...

- agreed label: `llms` · required · raw_text: "generativer KI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 180. golden_041 - skill `machine-learning` (spot-check)

> ...oder Infrastructure as Code sind willkommen * Du verstehst Machine Learning und Data Science so gut, dass du geeignete Verfahren...

- agreed label: `machine-learning` · required · raw_text: "verstehst Machine Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 181. golden_041 - skill `python` (spot-check)

> ...produktive Anwendungen entwickelt und betrieben * Du programmierst sicher mit Python und kennst dich mit Softwarearchitektur, APIs,...

- agreed label: `python` · required · raw_text: "programmierst sicher mit Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 182. golden_043 - skill `testing` (spot-check)

> ...Qualität in messbare Maßnahmen übersetzen, z. B. durch geeignete Tests, nachvollziehbare Ergebnisse, Monitoring im Betrieb und...

- agreed label: `testing` · required · raw_text: "geeignete Tests"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 183. golden_044 - attribute `german` (spot-check)

> Lead AI Engineer, Agents & Infrastructure

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 184. golden_044 - attribute `seniority` (spot-check)

> Lead AI Engineer, Agents & Infrastructure ABOUT THE ROLE As Lead AI...

- agreed label: value="senior" · basis="stated" · signal="Lead AI Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 185. golden_044 - skill `typescript` (spot-check)

> ...with strong engineering fundamentals and hands-on TypeScript skills; Python experience is useful. - Experience...

- agreed label: `typescript` · required · raw_text: "TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 186. golden_045 - attribute `german` (spot-check)

> ...professional proficiency in English at C2 level. - Full professional proficiency in German at C1 level. Bonus Qualifications - Experience building or scaling...

- agreed label: value="required" · basis="stated" · signal="Full professional proficiency in German at C1 level"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 187. golden_045 - skill `agents` (spot-check)

> ...it, and measured whether it worked - Have experience developing AI agents and integrating them into business workflows. - Be on top...

- agreed label: `agents` · required · raw_text: "developing AI agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 188. golden_045 - skill `evaluation` (spot-check)

> ...a team. - Know how to evaluate what gets built. You can design eval sets, work with LLM-as-judge or ground-truth data, use tracing...

- agreed label: `evaluation` · required · raw_text: "design eval sets"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 189. golden_045 - skill `llms` (spot-check)

> ...production-grade software, preferably with AI components (LLMs, embeddings, RAG pipelines, autonomous agents,...

- agreed label: `llms` · nice_to_have · raw_text: "LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 190. golden_045 - skill `observability` (spot-check)

> ...sets, work with LLM-as-judge or ground-truth data, use tracing and observability tooling to find and fix regressions, and make evaluation a team...

- agreed label: `observability` · required · raw_text: "tracing and observability tooling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 191. golden_045 - skill `vector-databases` (spot-check)

> ...the modern AI-tooling ecosystem (agents, memory systems, vector databases, orchestration frameworks). - Experience working with...

- agreed label: `vector-databases` · nice_to_have · raw_text: "vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 192. golden_046 - skill `embeddings` (spot-check)

> ...in diese Themen einzuarbeiten. Erste Berührungspunkte mit Embeddings, Vektordatenbanken, AI-Frameworks oder...

- agreed label: `embeddings` · nice_to_have · raw_text: "Embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 193. golden_046 - skill `software-engineering` (spot-check)

> ...Ausbildung erfolgreich abgeschlossen und bringst erste praktische Erfahrungen in der Softwareentwicklung mit. Wichtig ist uns vor allem, dass Du Freude daran hast,...

- agreed label: `software-engineering` · required · raw_text: "erste praktische Erfahrungen in der Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 194. golden_047 - attribute `degree` (spot-check)

> ...und Remote-Arbeit Qualifikationen Wir freuen uns auf deinen Studienabschluss mit einem technischen Hintergrund, zum Beispiel in Informatik, Data Science, Künstliche...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="deinen Studienabschluss mit einem technischen Hintergrund"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 195. golden_047 - attribute `seniority` (spot-check)

> (Junior) Agentic AI Software Engineer Aufgaben Du unterstützt...

- agreed label: value="junior" · basis="stated" · signal="(Junior)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 196. golden_047 - skill `apis` (spot-check)

> ...wie NodeJS, Spring/SpringBoot, Flask/Django, REST APIs oder GraphQL, FastAPI sammeln Du hattest bereits...

- agreed label: `apis` · required · raw_text: "REST APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 197. golden_047 - skill `cloud` (spot-check)

> ...Berührungspunkte mit Microsoft Azure oder einem anderen Cloud-Anbieter wie AWS oder Google Mündliche und schriftliche...

- agreed label: `cloud` · required · raw_text: "Cloud-Anbieter"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 198. golden_047 - skill `flask` (spot-check)

> ...mit Backend-Technologien wie NodeJS, Spring/SpringBoot, Flask/Django, REST APIs oder GraphQL, FastAPI sammeln Du hattest...

- agreed label: `flask` · required · raw_text: "Flask"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 199. golden_047 - skill `langgraph` (spot-check)

> ...RAG-Pipelines, Orchestrierungs-Frameworks wie LangChain/LangGraph) in Unternehmensumgebungen Dank deiner praktischen...

- agreed label: `langgraph` · required · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 200. golden_047 - skill `python` (spot-check)

> ...Programmiersprachen:.NET Core, C#, JavaScript oder Python Praktische Erfahrung bei der Bereitstellung von...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 201. golden_047 - skill `vector-databases` (spot-check)

> ...in der Integration generativer KI-Lösungen (LLMs, Vektordatenbanken, RAG-Pipelines, Orchestrierungs-Frameworks wie...

- agreed label: `vector-databases` · required · raw_text: "Vektordatenbanken"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
