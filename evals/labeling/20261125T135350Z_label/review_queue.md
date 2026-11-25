# Review queue - 20261125T135350Z_label

160 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-haiku-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261125T135350Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 158 accepted labels,
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

> AI Engineer (m/w/d) LLM - 100 % Remote

- Michael Page · AI Engineer (m/w/d) LLM - 100 % Remote
- Remote (EU) · de · jsearch · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_150 - scope `in_scope` (in-scope)

> Sorge gemeinsam mit uns für die digitale Zukunftsfähigkeit der Bundeswehr.

- BWI GmbH · DevSecOps Engineer für Analytics & KI (m/w/d)
- Berlin · de · arbeitsagentur · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_151 - scope `in_scope` (in-scope)

> Java Backend Developer (m/w/d) – AdTech, Spring Boot & AI

- streamboost GmbH · Java Backend Developer (m/w/d) – AdTech, Spring Boot & AI
- Berlin · de · arbeitnow · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_152 - scope `in_scope` (in-scope)

> Partner Applied AI Engineer, AWS

- openai · Partner Applied AI Engineer, AWS
- San Francisco · en · ashby · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_153 - scope `in_scope` (in-scope)

> Manager, Software Engineering - AI Infrastructure

- figma · Manager, Software Engineering - AI Infrastructure
- San Francisco · en · greenhouse · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_154 - scope `in_scope` (in-scope)

> Lead AI Engineer (Robotics Application Startup)

- Newbury Capital Partners, LLC · Lead AI Engineer (Robotics Application Startup)
- New York · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_155 - scope `in_scope` (in-scope)

> Principal Software Engineer, Back End (AI-powered Data Querying) (Bangkok based, Relocation provided)

- Agoda · Principal Software Engineer, Back End (AI-powered Data Querying) (Bangkok based, Relocation provided)
- Berlin · en · jsearch · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_156 - scope `in_scope` (in-scope)

> Senior Full-Stack AI Engineer — Shoreditch, 5 Days/Week

- Owen Thomas | B Corp™ · Senior Full-Stack AI Engineer — Shoreditch, 5 Days/Week
- London · en · jsearch · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_157 - scope `in_scope` (in-scope)

> Principal Software Engineer, Applied AI – Splunk Observability Cloud

- Cisco · Principal Software Engineer, Applied AI – Splunk Observability Cloud
- San Jose · en · jsearch · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_158 - scope `in_scope` (in-scope)

> Senior AI & RAG Engineer (m/w/d)

- Deloitte GmbH · Senior AI & RAG Engineer (m/w/d)
- Berlin · de · arbeitsagentur · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_159 - scope `in_scope` (in-scope)

> Lead Software Engineer AI Engineering

- Walbusch-Gruppe · Lead Software Engineer AI Engineering
- Berlin · de · jsearch · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_160 - scope `in_scope` (in-scope)

> Sr. Staff Applied AI Engineer, GTM

- zscaler · Sr. Staff Applied AI Engineer, GTM
- San Jose · en · greenhouse · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_161 - scope `in_scope` (in-scope)

> AI Engineer - US Remote

- Maneva · AI Engineer - US Remote
- Boston · en · jsearch · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_162 - scope `in_scope` (in-scope)

> Remote Senior AI Agentic Engineer

- Salesforce, Inc. · Remote Senior AI Agentic Engineer
- Chicago · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_163 - scope `in_scope` (in-scope)

> AI Inference Engineer LLM Plattformen

- EXXETA AG · AI Inference Engineer LLM Plattformen
- Berlin · de · jsearch · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_149 - skill `ai-deployment` (disagreement)

> ...in TensorFlow oder PyTorch sowie MLOps, Docker und Deployment-Prozessen • Erfahrung mit produktiven KI-Systemen, idealerweise in...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "Deployment-Prozessen"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_150 - skill `bash` (disagreement)

> ...Kenntnisse in Skript- und Programmiersprachen (bevorzugt Python, Go, Shell) zur Automatisierung und...

- A: `bash` · nice_to_have · raw_text: "bevorzugt Python, Go, Shell"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_151 - skill `testing` (disagreement)

> ...der Optimierung von Entwicklungsworkflows - Fähigkeit, AI-generierten Code eigenständig zu bewerten, zu testen und qualitativ abzusichern - Idealerweise Erfahrung mit Cloud-Technologien wie AWS...

- A: (did not label this)
- B: `testing` · required · raw_text: "AI-generierten Code eigenständig zu bewerten, zu testen und qualitativ abzusichern"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_152 - attribute `seniority` (disagreement)

> ...the ADE function. You’ll thrive in this role if you: - Have 8+ years of technical consulting (or equivalent) experience, managing C-level technical and business relationships...

- A: value="senior" · basis="inferred" · signal="Have 8+ years of technical consulting (or equivalent) experience"
- B: value="senior" · basis="stated" · signal="Serve as the senior technical counterpart to AWS field leadership"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_153 - skill `ai-infrastructure` (disagreement)

> ...or LLM/agent tooling platforms. - Experience building high-scale production infrastructure (e.g., traffic/inference systems, metering, anti-abuse and billing systems). - A background in adjacent platform domains, like...

- A: (did not label this)
- B: `ai-infrastructure` · nice_to_have · raw_text: "high-scale production infrastructure (e.g., traffic/inference systems, metering, anti-abuse and billing systems)"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_155 - skill `ai-ml` (disagreement)

> ...Scala or similar) • Experience building or working with: • AI/LLM-based applications (e.g., text-to-SQL, conversational interfaces, cursor,...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI/LLM-based applications"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_158 - skill `context-engineering` (disagreement)

> ...sowie Hybrid Search ein. Darüber hinaus verfügst du über fundierte Kenntnisse in Context Engineering, Metadata Filtering, Reranking sowie der Integration...

- A: `context-engineering` · required · raw_text: "fundierte Kenntnisse in Context Engineering"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_158 - skill `embeddings` (disagreement)

> ...Engineering, Metadata Filtering, Reranking sowie der Integration moderner Embedding- und LLM-APIs. - Architektur: Du unterstützt bei der...

- A: `embeddings` · required · raw_text: "Integration moderner Embedding-"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_159 - skill `java` (disagreement)

> ...bewerten und passend zur jeweiligen Aufgabe einzusetzen. Java und Spring Boot sind dabei weiterhin wichtige Bestandteile unserer Systemlandschaft. Erfahrung darin, technische Standards,...

- A: `java` · required · raw_text: "Java und Spring Boot sind dabei weiterhin wichtige Bestandteile unserer Systemlandschaft"
- B: `java` · nice_to_have · raw_text: "Java"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_159 - skill `spring-boot` (disagreement)

> ...bewerten und passend zur jeweiligen Aufgabe einzusetzen. Java und Spring Boot sind dabei weiterhin wichtige Bestandteile unserer Systemlandschaft. Erfahrung darin, technische Standards,...

- A: `spring-boot` · required · raw_text: "Java und Spring Boot sind dabei weiterhin wichtige Bestandteile unserer Systemlandschaft"
- B: `spring-boot` · nice_to_have · raw_text: "Spring Boot"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_160 - skill `cybersecurity` (disagreement)

> ...both technical and non-technical audiences - Experience securing AI systems and the data they access, including least-privilege access...

- A: (did not label this)
- B: `cybersecurity` · required · raw_text: "securing AI systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_160 - skill `data-privacy-and-security` (disagreement)

> ...both technical and non-technical audiences - Experience securing AI systems and the data they access, including least-privilege access and defending against...

- A: (did not label this)
- B: `data-privacy-and-security` · required · raw_text: "securing AI systems and the data they access"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_160 - skill `llm-guardrails` (disagreement)

> ...the data they access, including least-privilege access and defending against risks such as prompt injection, data leakage, and unsafe or non-compliant outputs - Strong engineering skills with experience deploying and...

- A: `llm-guardrails` · required · raw_text: "defending against risks such as prompt injection, data leakage, and unsafe or non-compliant outputs"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_160 - skill `machine-learning` (disagreement)

> ...including 3+ years working directly on AI and/or ML projects - Direct experience driving both AI strategy and...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "ML projects"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_160 - skill `mlops` (disagreement)

> ...outputs - Strong engineering skills with experience deploying and running AI at scale, proficiency in Python, comfort integrating across GTM...

- A: (did not label this)
- B: `mlops` · required · raw_text: "deploying and running AI at scale"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_160 - skill `rag` (disagreement)

> ...the components that make up modern AI solutions, including retrieval methods, reusable skill development, agentic orchestration,...

- A: `rag` · required · raw_text: "retrieval methods"
- B: `rag` · nice_to_have · raw_text: "GraphRAG"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_161 - skill `ai-ml` (disagreement)

> ...us immediately at IT-Security@Maneva.ai. Remote Skills: Artificial Intelligence (AI), Benchmarking, CUDA (Compute Unified Device Architecture),...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Artificial Intelligence (AI)"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_161 - skill `cloud` (disagreement)

> ...Benchmarking, CUDA (Compute Unified Device Architecture), Cloud Computing, Code Reviews, Computer Vision, Customer Satisfaction,...

- A: (did not label this)
- B: `cloud` · required · raw_text: "Cloud Computing"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 34. golden_161 - skill `cuda` (disagreement)

> ...Edge and embedded deployment experience (TensorRT, CUDA, quantization-aware training). • Experience with LLM...

- A: `cuda` · nice_to_have · raw_text: "CUDA"
- B: `cuda` · required · raw_text: "CUDA (Compute Unified Device Architecture)"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 35. golden_161 - skill `mlops` (disagreement)

> ...mixed precision, and GPU profiling. • Track record of taking models from research to production: model optimization, inference serving, monitoring, and iteration on real-world failures. • Evidence of staff-level impact: setting direction...

- A: (did not label this)
- B: `mlops` · required · raw_text: "taking models from research to production: model optimization, inference serving, monitoring, and iteration on real-world failures"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 36. golden_163 - skill `inference-optimization` (disagreement)

> ...dein Antrieb zu schneller persönlicher Weiterentwicklung Inference Engineering: Du verstehst die technischen und wirtschaftlichen...

- A: `inference-optimization` · required · raw_text: "Inference Engineering"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 37. golden_150 - attribute `seniority` (uncertain)

> ...Qualifikation mit fundierter Berufserfahrung (min. 5 Jahre) im DevSecOps- oder Cloud-Platform-Umfeld - Erprobte...

- A: value="senior" · basis="inferred" · signal="min. 5 Jahre"
- B: value="senior" · basis="inferred" · signal="fundierter Berufserfahrung (min. 5 Jahre)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 38. golden_150 - skill `cloud` (uncertain)

> ...Berufserfahrung (min. 5 Jahre) im DevSecOps- oder Cloud-Platform-Umfeld - Erprobte Kenntnisse in Containerisierung (Docker,...

- A: `cloud` · required · raw_text: "Cloud-Platform-Umfeld"
- B: `cloud` · required · raw_text: "DevSecOps- oder Cloud-Platform-Umfeld"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_150 - skill `devsecops` (uncertain)

> ...mit fundierter Berufserfahrung (min. 5 Jahre) im DevSecOps- oder Cloud-Platform-Umfeld - Erprobte Kenntnisse in Containerisierung (Docker,...

- A: `devsecops` · required · raw_text: "DevSecOps- oder Cloud-Platform-Umfeld"
- B: `devsecops` · required · raw_text: "DevSecOps- oder Cloud-Platform-Umfeld"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_150 - skill `go` (uncertain)

> ...Kenntnisse in Skript- und Programmiersprachen (bevorzugt Python, Go, Shell) zur Automatisierung und...

- A: `go` · nice_to_have · raw_text: "bevorzugt Python, Go"
- B: `go` · nice_to_have · raw_text: "bevorzugt Python, Go"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_150 - skill `python` (uncertain)

> ...Kenntnisse in Skript- und Programmiersprachen (bevorzugt Python, Go, Shell) zur Automatisierung und...

- A: `python` · nice_to_have · raw_text: "bevorzugt Python"
- B: `python` · nice_to_have · raw_text: "bevorzugt Python"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_151 - skill `ai-developer-tooling` (uncertain)

> ...in SQL- und NoSQL-Datenbanken - Praktische Erfahrung mit AI-gestützter Softwareentwicklung, beispielsweise mit GitHub Copilot, Cursor, Claude Code...

- A: `ai-developer-tooling` · required · raw_text: "Praktische Erfahrung mit AI-gestützter Softwareentwicklung"
- B: `ai-developer-tooling` · required · raw_text: "Praktische Erfahrung mit AI-gestützter Softwareentwicklung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_153 - attribute `seniority` (uncertain)

> ...fast-moving teams, ideally in the AI space. - 8+ years of total engineering experience, ideally reaching a staff engineering level as an...

- A: value="senior" · basis="inferred" · signal="8+ years of total engineering experience"
- B: value="senior" · basis="inferred" · signal="8+ years of total engineering experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_153 - skill `ai-ml` (uncertain)

> ...a staff engineering level as an individual contributor. - Experience working on production AI systems. - A proven track record of motivating, mentoring, and...

- A: `ai-ml` · required · raw_text: "Experience working on production AI systems"
- B: `ai-ml` · required · raw_text: "Experience working on production AI systems."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_153 - skill `llms` (uncertain)

> ...Experience building AI agents, agent harnesses/loops, or LLM/agent tooling platforms. - Experience building high-scale production...

- A: `llms` · nice_to_have · raw_text: "LLM/agent tooling platforms"
- B: `llms` · nice_to_have · raw_text: "LLM/agent tooling platforms"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_155 - skill `ci-cd` (uncertain)

> ...of releases per day, so we must employ state-of-the-art CI/CD and testing techniques in order to make sure everything...

- A: `ci-cd` · nice_to_have · raw_text: "CI/CD"
- B: `ci-cd` · nice_to_have · raw_text: "CI/CD"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_155 - skill `conversational-ai` (uncertain)

> ...with: • AI/LLM-based applications (e.g., text-to-SQL, conversational interfaces, cursor, copilots) • Data platforms or analytical...

- A: `conversational-ai` · required · raw_text: "conversational interfaces"
- B: `conversational-ai` · required · raw_text: "conversational interfaces"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_155 - skill `data-engineering` (uncertain)

> ...10+ years of experience in software engineering, data engineering, or related fields • Strong hands-on experience with: •...

- A: `data-engineering` · required · raw_text: "data engineering"
- B: `data-engineering` · required · raw_text: "data engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_155 - skill `go` (uncertain)

> ...In order to accomplish this, we use state-of-the-art languages like Scala and Go, data technologies like Kafka and Aerospike, and agile...

- A: `go` · nice_to_have · raw_text: "languages like Scala and Go"
- B: `go` · nice_to_have · raw_text: "Go"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_155 - skill `kafka` (uncertain)

> ...languages like Scala and Go, data technologies like Kafka and Aerospike, and agile development practices. Most...

- A: `kafka` · nice_to_have · raw_text: "Kafka"
- B: `kafka` · nice_to_have · raw_text: "Kafka"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_155 - skill `observability` (uncertain)

> ...analytical engines such as StarRocks • Background in data observability, quality, or governance frameworks • Experience with tools...

- A: `observability` · nice_to_have · raw_text: "data observability"
- B: `observability` · nice_to_have · raw_text: "data observability"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_155 - skill `scala` (uncertain)

> ...BigQuery, ClickHouse) • Backend development (e.g., Python, Java, Scala or similar) • Experience building or working with: • AI/LLM-based...

- A: `scala` · required · raw_text: "Python, Java, Scala or similar"
- B: `scala` · required · raw_text: "Python, Java, Scala or similar"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_155 - skill `software-engineering` (uncertain)

> ...you'll Need to Succeed: • 10+ years of experience in software engineering, data engineering, or related fields • Strong hands-on...

- A: `software-engineering` · required · raw_text: "software engineering"
- B: `software-engineering` · required · raw_text: "software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_155 - skill `testing` (uncertain)

> ...per day, so we must employ state-of-the-art CI/CD and testing techniques in order to make sure everything works without any...

- A: `testing` · nice_to_have · raw_text: "testing techniques"
- B: `testing` · nice_to_have · raw_text: "testing techniques"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_157 - skill `agents` (uncertain)

> ...production-grade LLM-based systems, including at least one agentic system with active tool use. • Experience developing evaluation...

- A: `agents` · required · raw_text: "agentic system"
- B: `agents` · required · raw_text: "agentic system"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_157 - skill `ai-ml` (uncertain)

> ...use. • Experience developing evaluation frameworks for AI/ML systems, including dataset creation, offline/online scoring, and...

- A: `ai-ml` · required · raw_text: "AI/ML systems"
- B: `ai-ml` · required · raw_text: "AI/ML systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_157 - skill `cloud` (uncertain)

> ...tracing and alerting workflows. • Experience working with cloud-native infrastructure at scale, specifically Kubernetes. • History of active...

- A: `cloud` · nice_to_have · raw_text: "cloud-native infrastructure"
- B: `cloud` · nice_to_have · raw_text: "cloud-native infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_157 - skill `context-engineering` (uncertain)

> ...scoring, and release validation. • Experience engineering retrieval and context pipelines for structured and semi-structured data, such as...

- A: `context-engineering` · required · raw_text: "engineering retrieval and context pipelines"
- B: `context-engineering` · required · raw_text: "context pipelines"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_157 - skill `rag` (uncertain)

> ...scoring, and release validation. • Experience engineering retrieval and context pipelines for structured and semi-structured data, such as...

- A: `rag` · required · raw_text: "retrieval and context pipelines"
- B: `rag` · required · raw_text: "retrieval and context pipelines"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_157 - skill `software-engineering` (uncertain)

> ...product features. Minimum Qualifications • 12+ years of professional software engineering experience. • 3+ years of experience designing, building, and...

- A: `software-engineering` · required · raw_text: "professional software engineering experience"
- B: `software-engineering` · required · raw_text: "software engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_158 - skill `ai-ml` (uncertain)

> ...von RAG-Lösungen, Large Language Models (LLMs) und KI-Anwendungen - Fundierte Kenntnisse in Python, API-Entwicklung sowie...

- A: `ai-ml` · required · raw_text: "KI-Anwendungen"
- B: `ai-ml` · required · raw_text: "KI-Anwendungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_158 - skill `networking` (uncertain)

> ...und bringst Kenntnisse in den Bereichen SD-WAN, Netzwerkoptimierung, Zero Trust, OT-Infrastrukturen, Microsoft 365 sowie...

- A: `networking` · nice_to_have · raw_text: "Netzwerkoptimierung"
- B: `networking` · nice_to_have · raw_text: "Netzwerkoptimierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_158 - skill `software-architecture` (uncertain)

> ...Studiengang - Du verfügst über Erfahrung im Bereich IoT, IT-Architektur sowie in der Entwicklung von RAG-Lösungen, Large Language...

- A: `software-architecture` · required · raw_text: "IT-Architektur"
- B: `software-architecture` · required · raw_text: "IT-Architektur"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_159 - skill `software-architecture` (uncertain)

> ...Erfahrung in der Softwareentwicklung sowie ein gutes Verständnis für moderne Softwarearchitekturen, Integrationen und gewachsene...

- A: `software-architecture` · required · raw_text: "gutes Verständnis für moderne Softwarearchitekturen"
- B: `software-architecture` · required · raw_text: "ein gutes Verständnis für moderne Softwarearchitekturen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_160 - skill `ai-deployment` (uncertain)

> ...outputs - Strong engineering skills with experience deploying and running AI at scale, proficiency in Python, comfort integrating across GTM...

- A: `ai-deployment` · required · raw_text: "deploying and running AI at scale"
- B: `ai-deployment` · required · raw_text: "deploying and running AI at scale"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_160 - skill `ai-ml` (uncertain)

> ...experience, including 3+ years working directly on AI and/or ML projects - Direct experience driving both AI strategy and...

- A: `ai-ml` · required · raw_text: "AI and/or ML projects"
- B: `ai-ml` · required · raw_text: "AI and/or ML projects"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_160 - skill `knowledge-graphs` (uncertain)

> ...GTM Strategy being a strong plus - Direct experience with graph-based knowledge systems and long-term agent memory, including account and...

- A: `knowledge-graphs` · nice_to_have · raw_text: "graph-based knowledge systems"
- B: `knowledge-graphs` · nice_to_have · raw_text: "graph-based knowledge systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_160 - skill `llm-orchestration` (uncertain)

> ...including retrieval methods, reusable skill development, agentic orchestration, connecting to tools and data through the Model Context...

- A: `llm-orchestration` · required · raw_text: "agentic orchestration"
- B: `llm-orchestration` · required · raw_text: "agentic orchestration"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_160 - skill `observability` (uncertain)

> ...across GTM systems of record, and experience releasing and monitoring AI systems on a major cloud platform What Will Make You Stand Out...

- A: `observability` · required · raw_text: "monitoring AI systems"
- B: `observability` · required · raw_text: "monitoring AI systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_160 - skill `testing` (uncertain)

> ...automated evaluation frameworks, such as LLM-as-judge or regression testing for AI quality, ideally paired with A/B or holdout experiments that...

- A: `testing` · nice_to_have · raw_text: "regression testing for AI quality"
- B: `testing` · nice_to_have · raw_text: "regression testing for AI quality"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_161 - skill `ai-deployment` (uncertain)

> ...DETR-style models), including training, tuning, and production deployment. • Hands-on experience with VLMs (for example LLaVA-,...

- A: `ai-deployment` · required · raw_text: "production deployment"
- B: `ai-deployment` · required · raw_text: "production deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_161 - skill `llms` (uncertain)

> ...CUDA, quantization-aware training). • Experience with LLM tooling such as vLLM, or with RLHF-style post-training for...

- A: `llms` · nice_to_have · raw_text: "LLM tooling"
- B: `llms` · nice_to_have · raw_text: "LLM tooling"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_161 - skill `machine-learning` (uncertain)

> ...product. Requirements What we're looking for • 5+ years building and shipping ML systems, with focus on computer vision; BS/MS/PhD in CS, EE, or a...

- A: `machine-learning` · required · raw_text: "building and shipping ML systems"
- B: `machine-learning` · required · raw_text: "building and shipping ML systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_161 - skill `model-development` (uncertain)

> ...and segmentation (YOLO family, DETR-style models), including training, tuning, and production deployment. • Hands-on experience...

- A: `model-development` · required · raw_text: "including training"
- B: `model-development` · required · raw_text: "training"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_161 - skill `prompt-engineering` (uncertain)

> ...LLaVA-, Qwen-VL-, or PaliGemma-style models): fine-tuning, prompting, grounding, and evaluation. • Experience with VLAs or...

- A: `prompt-engineering` · required · raw_text: "prompting"
- B: `prompt-engineering` · required · raw_text: "prompting"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_163 - skill `access-control` (uncertain)

> ...AI-Systeme treffen. Security & Governance: Themen wie Identitäten, Berechtigungen, Secrets, Logging, Auditierung und Compliance denkst du,...

- A: `access-control` · required · raw_text: "Identitäten, Berechtigungen"
- B: `access-control` · required · raw_text: "Identitäten, Berechtigungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_163 - skill `cloud` (uncertain)

> ...Background: Erfahrung in Platform Engineering, Cloud Infrastructure, MLOps, LLMOps, DevOps, Backend Engineering oder Machine...

- A: `cloud` · required · raw_text: "Cloud Infrastructure"
- B: `cloud` · required · raw_text: "Cloud Infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_163 - skill `quantization` (uncertain)

> ...LLM-Inferenz, von Model-Serving und GPU-Auslastung über Quantisierung, Batching und KV-Cache-Management bis hin zu Latenz,...

- A: `quantization` · required · raw_text: "über Quantisierung"
- B: `quantization` · required · raw_text: "Quantisierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 79. golden_163 - skill `secrets-management` (uncertain)

> ...treffen. Security & Governance: Themen wie Identitäten, Berechtigungen, Secrets, Logging, Auditierung und Compliance denkst du,...

- A: `secrets-management` · required · raw_text: "Berechtigungen, Secrets"
- B: `secrets-management` · required · raw_text: "Secrets"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 80. golden_155 - skill `github-copilot|ai-developer-tooling` (mapping)

> ...(e.g., text-to-SQL, conversational interfaces, cursor, copilots) • Data platforms or analytical infrastructure at scale •...

- A: `github-copilot` · required · raw_text: "copilots"
- B: `ai-developer-tooling` · required · raw_text: "copilots"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 81. golden_149 - attribute `degree` (spot-check)

> AI Engineer (m/w/d) LLM - 100 % Remote

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 82. golden_149 - attribute `german` (spot-check)

> ...idealerweise in Cloud-Umgebungen (z. B. AWS) • Sehr gute Deutsch- und Englischkenntnisse Vergütungspaket • 100 % Remote-Arbeit innerhalb...

- agreed label: value="required" · basis="stated" · signal="Sehr gute Deutsch- und Englischkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 83. golden_149 - skill `llms` (spot-check)

> ...Praktische Erfahrung mit Speech-to-Text, Speech AI und Large Language Models • Kenntnisse in TensorFlow oder PyTorch sowie MLOps,...

- agreed label: `llms` · required · raw_text: "Large Language Models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_149 - skill `machine-learning` (spot-check)

> ...vergleichbaren Rolle • Sehr gute Python-Kenntnisse sowie Erfahrung mit Machine Learning und Deep Learning • Praktische Erfahrung mit...

- agreed label: `machine-learning` · required · raw_text: "Erfahrung mit Machine Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_149 - skill `python` (spot-check)

> ...Engineer, ML Engineer oder in einer vergleichbaren Rolle • Sehr gute Python-Kenntnisse sowie Erfahrung mit Machine Learning und Deep Learning •...

- agreed label: `python` · required · raw_text: "Sehr gute Python-Kenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_149 - skill `pytorch` (spot-check)

> ...AI und Large Language Models • Kenntnisse in TensorFlow oder PyTorch sowie MLOps, Docker und Deployment-Prozessen • Erfahrung...

- agreed label: `pytorch` · required · raw_text: "oder PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_149 - skill `tensorflow` (spot-check)

> ...mit Speech-to-Text, Speech AI und Large Language Models • Kenntnisse in TensorFlow oder PyTorch sowie MLOps, Docker und...

- agreed label: `tensorflow` · required · raw_text: "Kenntnisse in TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_150 - attribute `german` (spot-check)

> Sorge gemeinsam mit uns für die digitale Zukunftsfähigkeit der Bundeswehr.

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_150 - skill `ci-cd` (spot-check)

> ...Erfahrung in Bereitstellung und Administration moderner CI/CD-Toolchains (z. B. GitLab CI, ArgoCD, Nexus, Harbor,...

- agreed label: `ci-cd` · required · raw_text: "CI/CD-Toolchains"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_150 - skill `kubeflow` (spot-check)

> ...Anbindung von MLOps-Frameworks (z. B. Kubeflow, MLflow) Deine Aufgaben: - Entwicklung, Pflege und...

- agreed label: `kubeflow` · nice_to_have · raw_text: "Kubeflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_150 - skill `kubernetes` (spot-check)

> ...Optimierung sicherer, portabler Container-Images sowie in Kubernetes-Orchestrierung - Fundierte Erfahrung in Bereitstellung und...

- agreed label: `kubernetes` · required · raw_text: "Kubernetes-Orchestrierung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_150 - skill `linux` (spot-check)

> ...cloud-nativer Konzepte, Netzwerksicherheit sowie sicherer Linux-Serveradministration und Secrets-Management (z. B. HashiCorp...

- agreed label: `linux` · required · raw_text: "Linux-Serveradministration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_150 - skill `mlops` (spot-check)

> ...gängiger Datenbanken (SQL, NoSQL, Vektordatenbanken) - Von Vorteil: Erfahrung mit der infrastrukturseitigen Anbindung von MLOps-Frameworks (z. B. Kubeflow, MLflow) Deine Aufgaben: - Entwicklung,...

- agreed label: `mlops` · nice_to_have · raw_text: "Von Vorteil: Erfahrung mit der infrastrukturseitigen Anbindung von MLOps-Frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_150 - skill `secrets-management` (spot-check)

> ...sowie sicherer Linux-Serveradministration und Secrets-Management (z. B. HashiCorp Vault) - Fundierte Kenntnisse in...

- agreed label: `secrets-management` · required · raw_text: "Secrets-Management"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_150 - skill `sql` (spot-check)

> ...in der Administration gängiger Datenbanken (SQL, NoSQL, Vektordatenbanken) - Von Vorteil: Erfahrung mit...

- agreed label: `sql` · required · raw_text: "Datenbanken (SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_150 - skill `vector-databases` (spot-check)

> ...in der Administration gängiger Datenbanken (SQL, NoSQL, Vektordatenbanken) - Von Vorteil: Erfahrung mit der infrastrukturseitigen...

- agreed label: `vector-databases` · required · raw_text: "Vektordatenbanken"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_151 - attribute `german` (spot-check)

> Java Backend Developer (m/w/d) – AdTech, Spring Boot & AI

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_151 - skill `apis` (spot-check)

> ...in der Backend-Entwicklung mit Java und Spring Boot - Erfahrung mit RESTful APIs und Microservices-Architekturen - Kenntnisse in SQL- und...

- agreed label: `apis` · required · raw_text: "Erfahrung mit RESTful APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_151 - skill `aws` (spot-check)

> ...und qualitativ abzusichern - Idealerweise Erfahrung mit Cloud-Technologien wie AWS oder Azure - Verständnis für skalierbare und performante...

- agreed label: `aws` · nice_to_have · raw_text: "Cloud-Technologien wie AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_151 - skill `backend-development` (spot-check)

> ...Einbringen neuer Ideen Das bringst du mit - Fundierte Erfahrung in der Backend-Entwicklung mit Java und Spring Boot - Erfahrung mit RESTful APIs und...

- agreed label: `backend-development` · required · raw_text: "Erfahrung in der Backend-Entwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_151 - skill `claude-code` (spot-check)

> ...beispielsweise mit GitHub Copilot, Cursor, Claude Code oder vergleichbaren Tools - Sicherer Umgang mit AI bei...

- agreed label: `claude-code` · required · raw_text: "Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_151 - skill `cloud` (spot-check)

> ...zu bewerten, zu testen und qualitativ abzusichern - Idealerweise Erfahrung mit Cloud-Technologien wie AWS oder Azure - Verständnis für skalierbare und...

- agreed label: `cloud` · nice_to_have · raw_text: "Idealerweise Erfahrung mit Cloud-Technologien"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_152 - attribute `degree` (spot-check)

> Partner Applied AI Engineer, AWS

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_152 - attribute `german` (spot-check)

> Partner Applied AI Engineer, AWS

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_153 - skill `agent-harnesses` (spot-check)

> ...plus if you also have: - Experience building AI agents, agent harnesses/loops, or LLM/agent tooling platforms. - Experience...

- agreed label: `agent-harnesses` · nice_to_have · raw_text: "agent harnesses"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_153 - skill `networking` (spot-check)

> ...adjacent platform domains, like recommendation systems or networking. At Figma, one of our values is Grow as you go. We...

- agreed label: `networking` · nice_to_have · raw_text: "networking"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_155 - attribute `degree` (spot-check)

> Principal Software Engineer, Back End (AI-powered Data Querying) (Bangkok based, Relocation provided)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_155 - attribute `german` (spot-check)

> Principal Software Engineer, Back End (AI-powered Data Querying) (Bangkok based, Relocation provided)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_155 - attribute `seniority` (spot-check)

> Principal Software Engineer, Back End (AI-powered Data Querying) (Bangkok based,...

- agreed label: value="senior" · basis="stated" · signal="Principal Software Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_155 - skill `airflow` (spot-check)

> ...or governance frameworks • Experience with tools like dbt, Airflow, Spark, or similar #Bengaluru #SãoPaulo #Delhi...

- agreed label: `airflow` · nice_to_have · raw_text: "Airflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_155 - skill `apache-spark` (spot-check)

> ...frameworks • Experience with tools like dbt, Airflow, Spark, or similar #Bengaluru #SãoPaulo #Delhi #NewYorkCity...

- agreed label: `apache-spark` · nice_to_have · raw_text: "Spark"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_155 - skill `cursor` (spot-check)

> ...(e.g., text-to-SQL, conversational interfaces, cursor, copilots) • Data platforms or analytical infrastructure...

- agreed label: `cursor` · required · raw_text: "cursor"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_155 - skill `data-modeling` (spot-check)

> ...infrastructure at scale • Strong understanding of data modeling, query execution, and performance optimization • Proven...

- agreed label: `data-modeling` · required · raw_text: "data modeling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_155 - skill `dbt` (spot-check)

> ...or governance frameworks • Experience with tools like dbt, Airflow, Spark, or similar #Bengaluru #SãoPaulo #Delhi...

- agreed label: `dbt` · nice_to_have · raw_text: "dbt"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_155 - skill `sql` (spot-check)

> ...or related fields • Strong hands-on experience with: • SQL and large-scale data systems • Modern analytical databases / data warehouses (e.g.,...

- agreed label: `sql` · required · raw_text: "SQL and large-scale data systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_156 - attribute `degree` (spot-check)

> Senior Full-Stack AI Engineer — Shoreditch, 5 Days/Week

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_156 - attribute `german` (spot-check)

> Senior Full-Stack AI Engineer — Shoreditch, 5 Days/Week

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_156 - attribute `seniority` (spot-check)

> Senior Full-Stack AI Engineer — Shoreditch, 5 Days/Week Owen Thomas | B Corp is seeking...

- agreed label: value="senior" · basis="stated" · signal="Senior Full-Stack AI Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_157 - attribute `degree` (spot-check)

> Principal Software Engineer, Applied AI – Splunk Observability Cloud

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_157 - attribute `german` (spot-check)

> Principal Software Engineer, Applied AI – Splunk Observability Cloud

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_157 - skill `llms` (spot-check)

> ...designing, building, and deploying production-grade LLM-based systems, including at least one agentic system with active tool...

- agreed label: `llms` · required · raw_text: "LLM-based systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_157 - skill `mcp` (spot-check)

> ...or observability ecosystems (e.g., OpenTelemetry, MCP). • Experience leading customer-zero or field-deployed...

- agreed label: `mcp` · nice_to_have · raw_text: "MCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_157 - skill `observability` (spot-check)

> ...security guardrails for AI. Preferred Qualifications • Experience with Observability, SRE, or incident management domains, including...

- agreed label: `observability` · nice_to_have · raw_text: "Experience with Observability"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_157 - skill `opentelemetry` (spot-check)

> ...AI, agent frameworks, or observability ecosystems (e.g., OpenTelemetry, MCP). • Experience leading customer-zero or...

- agreed label: `opentelemetry` · nice_to_have · raw_text: "OpenTelemetry"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_158 - skill `apis` (spot-check)

> ...und KI-Anwendungen - Fundierte Kenntnisse in Python, API-Entwicklung sowie modernen KI- und Machine-Learning-Frameworks -...

- agreed label: `apis` · required · raw_text: "API-Entwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_158 - skill `llms` (spot-check)

> ...IT-Architektur sowie in der Entwicklung von RAG-Lösungen, Large Language Models (LLMs) und KI-Anwendungen - Fundierte Kenntnisse in Python, API-Entwicklung sowie...

- agreed label: `llms` · required · raw_text: "Large Language Models (LLMs) und KI-Anwendungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_158 - skill `python` (spot-check)

> ...Models (LLMs) und KI-Anwendungen - Fundierte Kenntnisse in Python, API-Entwicklung sowie modernen KI- und...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_158 - skill `rag` (spot-check)

> ...über Erfahrung im Bereich IoT, IT-Architektur sowie in der Entwicklung von RAG-Lösungen, Large Language Models (LLMs) und KI-Anwendungen -...

- agreed label: `rag` · required · raw_text: "Entwicklung von RAG-Lösungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_159 - attribute `degree` (spot-check)

> Lead Software Engineer AI Engineering

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_159 - attribute `german` (spot-check)

> Lead Software Engineer AI Engineering

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_159 - skill `ai-developer-tooling` (spot-check)

> ...für AI-Driven Development und praktische Erfahrung mit AI-Coding-Tools, Coding Agents oder vergleichbaren AI-gestützten...

- agreed label: `ai-developer-tooling` · required · raw_text: "praktische Erfahrung mit AI-Coding-Tools, Coding Agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_160 - attribute `german` (spot-check)

> Sr. Staff Applied AI Engineer, GTM

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_160 - attribute `seniority` (spot-check)

> Sr. Staff Applied AI Engineer, GTM Zscaler (NASDAQ: ZS) accelerates digital...

- agreed label: value="senior" · basis="stated" · signal="Sr. Staff Applied AI Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_160 - skill `a-b-testing` (spot-check)

> ...such as LLM-as-judge or regression testing for AI quality, ideally paired with A/B or holdout experiments that measure business lift in the field #LI-DY1...

- agreed label: `a-b-testing` · nice_to_have · raw_text: "ideally paired with A/B or holdout experiments"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_160 - skill `access-control` (spot-check)

> ...securing AI systems and the data they access, including least-privilege access and defending against risks such as prompt injection, data...

- agreed label: `access-control` · required · raw_text: "least-privilege access"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_160 - skill `mcp` (spot-check)

> ...orchestration, connecting to tools and data through the Model Context Protocol (MCP), and agent-to-agent (A2A) frameworks - A track record of...

- agreed label: `mcp` · required · raw_text: "Model Context Protocol (MCP)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_160 - skill `software-engineering` (spot-check)

> ...We’re Looking for (Minimum Qualifications) - 5+ years of professional software engineering experience, including 3+ years working directly on AI and/or ML...

- agreed label: `software-engineering` · required · raw_text: "professional software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_161 - attribute `degree` (spot-check)

> ...and shipping ML systems, with focus on computer vision; BS/MS/PhD in CS, EE, or a related field, or equivalent experience. • Deep hands-on experience with object detection and...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="BS/MS/PhD in CS, EE, or a related field, or equivalent experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_161 - attribute `german` (spot-check)

> AI Engineer - US Remote

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_161 - attribute `seniority` (spot-check)

> ...monitoring, and iteration on real-world failures. • Evidence of staff-level impact: setting direction across teams, making sound...

- agreed label: value="senior" · basis="stated" · signal="Evidence of staff-level impact"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_161 - skill `distributed-training` (spot-check)

> ...multimodal work. • Strong PyTorch skills and fluency with distributed training, mixed precision, and GPU profiling. • Track record of...

- agreed label: `distributed-training` · required · raw_text: "distributed training"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_161 - skill `model-serving` (spot-check)

> ...models from research to production: model optimization, inference serving, monitoring, and iteration on real-world failures. •...

- agreed label: `model-serving` · required · raw_text: "inference serving"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_161 - skill `pytorch` (spot-check)

> ...or a clear record in adjacent multimodal work. • Strong PyTorch skills and fluency with distributed training, mixed precision,...

- agreed label: `pytorch` · required · raw_text: "Strong PyTorch skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_161 - skill `quantization` (spot-check)

> ...Edge and embedded deployment experience (TensorRT, CUDA, quantization-aware training). • Experience with LLM tooling such as vLLM, or with...

- agreed label: `quantization` · nice_to_have · raw_text: "quantization-aware training"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_161 - skill `tensorrt` (spot-check)

> ...learning. • Edge and embedded deployment experience (TensorRT, CUDA, quantization-aware training). • Experience with LLM tooling such as vLLM, or with...

- agreed label: `tensorrt` · nice_to_have · raw_text: "TensorRT, CUDA, quantization-aware training"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_162 - attribute `degree` (spot-check)

> Remote Senior AI Agentic Engineer

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_162 - attribute `german` (spot-check)

> Remote Senior AI Agentic Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_162 - attribute `seniority` (spot-check)

> Remote Senior AI Agentic Engineer Salesforce, Inc. seeks a Senior Member of Technical Staff...

- agreed label: value="senior" · basis="stated" · signal="Remote Senior AI Agentic Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_163 - attribute `degree` (spot-check)

> AI Inference Engineer LLM Plattformen

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_163 - attribute `seniority` (spot-check)

> AI Inference Engineer LLM Plattformen

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_163 - skill `backend-development` (spot-check)

> ...Engineering, Cloud Infrastructure, MLOps, LLMOps, DevOps, Backend Engineering oder Machine Learning Engineering. Entscheidend ist deine...

- agreed label: `backend-development` · required · raw_text: "Backend Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_163 - skill `devops` (spot-check)

> ...Platform Engineering, Cloud Infrastructure, MLOps, LLMOps, DevOps, Backend Engineering oder Machine Learning Engineering....

- agreed label: `devops` · required · raw_text: "DevOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_163 - skill `embeddings` (spot-check)

> ...kannst Transformer-basierte Modelle wie LLMs und Embeddings einordnen und fundierte technische Entscheidungen für...

- agreed label: `embeddings` · required · raw_text: "Embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_163 - skill `helm` (spot-check)

> ...und Kosten. Cloud & Plattformen: Docker, Kubernetes, Helm, Terraform, CI/CD, Linux sowie Observability gehören für...

- agreed label: `helm` · required · raw_text: "Helm"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_163 - skill `llms` (spot-check)

> ...kannst Transformer-basierte Modelle wie LLMs und Embeddings einordnen und fundierte technische...

- agreed label: `llms` · required · raw_text: "LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 156. golden_163 - skill `mlops` (spot-check)

> ...in Platform Engineering, Cloud Infrastructure, MLOps, LLMOps, DevOps, Backend Engineering oder Machine Learning...

- agreed label: `mlops` · required · raw_text: "MLOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 157. golden_163 - skill `observability` (spot-check)

> ...Kubernetes, Helm, Terraform, CI/CD, Linux sowie Observability gehören für dich zum Arbeitsalltag. AI-Verständnis: Du...

- agreed label: `observability` · required · raw_text: "sowie Observability"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 158. golden_163 - skill `sglang` (spot-check)

> ...Projektumfeldern sicher. Pluspunkt: Erfahrung mit vLLM, SGLang oder vergleichbaren Inference-Technologien, GPU-Clustern,...

- agreed label: `sglang` · nice_to_have · raw_text: "SGLang"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 159. golden_163 - skill `terraform` (spot-check)

> ...und Kosten. Cloud & Plattformen: Docker, Kubernetes, Helm, Terraform, CI/CD, Linux sowie Observability gehören für dich zum...

- agreed label: `terraform` · required · raw_text: "Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 160. golden_163 - skill `transformers` (spot-check)

> ...für dich zum Arbeitsalltag. AI-Verständnis: Du kannst Transformer-basierte Modelle wie LLMs und Embeddings einordnen und fundierte technische...

- agreed label: `transformers` · required · raw_text: "Transformer-basierte Modelle"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
