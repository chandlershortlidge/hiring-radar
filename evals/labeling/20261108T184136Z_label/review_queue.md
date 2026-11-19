# Review queue - 20261108T184136Z_label

173 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261108T184136Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 213 accepted labels,
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

## 1. golden_134 - scope `in_scope` (in-scope)

> MaxIT | Applied AI Competence Center AI-DevOps Engineer (m/w/d) Die

- Max Planck Information and Technology · AI-DevOps Engineer (m/w/d)
- Munich · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_135 - scope `in_scope` (in-scope)

> AI Native Developer (m/w/d)

- TechMinds GmbH · AI Native Developer (m/w/d)
- Munich · de · arbeitsagentur · 17 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_136 - scope `in_scope` (in-scope)

> Senior AI Engineer / AI Architect (all gender)

- ALTEN GmbH München · Senior AI Engineer / AI Architect (all gender)
- Munich · de · arbeitsagentur · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_137 - scope `in_scope` (in-scope)

> Machine Learning Innovation Engineer (m/w/d)

- ARRK Engineering GmbH · Machine Learning Innovation Engineer (m/w/d)
- Munich · de · arbeitsagentur · 26 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_138 - scope `in_scope` (in-scope)

> Cloud Software Engineer mit KI-Fokus (m/w/d)

- TekkMinds AG · Cloud Software Engineer mit KI-Fokus (m/w/d)
- Munich · de · arbeitsagentur · 26 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_139 - scope `in_scope` (in-scope)

> AI & Machine Learning Engineer (m/w/d)

- MONTANA Energie-Handel GmbH & Co. KG · AI & Machine Learning Engineer (m/w/d)
- Munich · de · arbeitsagentur · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_140 - scope `in_scope` (in-scope)

> Automotive Security Backend AI Engineer (f/m/x)

- BMW AG · Automotive Security Backend AI Engineer (f/m/x)
- Munich · en · arbeitsagentur · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_141 - scope `in_scope` (in-scope)

> Senior AI / Reinforcement Learning Engineer (m/f/d)

- agilerobotsse · Senior AI / Reinforcement Learning Engineer (m/f/d)
- Munich · en · greenhouse · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_142 - scope `in_scope` (in-scope)

> Wir suchen Dich als

- accu Personalservice GmbH · Engineer, Software AI DevOps (m/w/d)
- Munich · de · arbeitsagentur · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_143 - scope `in_scope` (in-scope)

> Principal Data Scientist (m/f/d)

- AutoScout24 · Principal Data Scientist (m/f/d)
- Munich · en · greenhouse · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_144 - scope `in_scope` (in-scope)

> Associate Applied (AI) Value Engineer (DACH) - Orbit Program

- celonis · Associate Applied (AI) Value Engineer (DACH) - Orbit Program
- Munich · en · greenhouse · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_145 - scope `in_scope` (in-scope)

> Automotive AI Security Engineer (f/m/x)

- BMW AG · Automotive AI Security Engineer (f/m/x)
- Munich · en · arbeitsagentur · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_146 - scope `in_scope` (in-scope)

> AI Forward Deployed Engineer - Germany

- databricks · AI Forward Deployed Engineer - Germany
- Munich · en · greenhouse · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_147 - scope `in_scope` (in-scope)

> Senior IT Engineer (w/m/d) API, AI, Infrastruktur

- Robert Half Deutschland GmbH & Co. KG · Senior IT Engineer (w/m/d) API, AI, Infrastruktur
- Munich · de · arbeitsagentur · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_148 - scope `in_scope` (in-scope)

> AI Process & Agent Solutions Engineer (m/w/d)

- C-P-S Group · AI Process & Agent Solutions Engineer (m/w/d)
- Munich · de · arbeitsagentur · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_134 - skill `ai-deployment` (disagreement)

> ...Vektordatenbanken Erfahrung in der Entwicklung und Bereitstellung von KI-Agenten und automatisierten Gesprächssystemen (Chatbots/KI-Bots)...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "Bereitstellung von KI-Agenten"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_135 - skill `cybersecurity` (disagreement)

> ...Verständnis für Cloud-Architekturen, Monitoring und sichere KI-Anwendungen mit Du arbeitest strukturiert, eigenverantwortlich und...

- A: (did not label this)
- B: `cybersecurity` · required · raw_text: "sichere KI-Anwendungen"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_135 - skill `evaluation` (disagreement)

> ...Cursor oder Codex, entwickelst spezifikationsbasiert und überprüfst KI-generierte Ergebnisse systematisch Du beherrschst automatisierte Tests auf unterschiedlichen...

- A: (did not label this)
- B: `evaluation` · required · raw_text: "überprüfst KI-generierte Ergebnisse systematisch"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_137 - skill `inference-optimization` (disagreement)

> ...Embeddings und Fine-Tuning • Erfahrung mit Edge AI und Model Optimization, z. B. Quantization, Pruning, ONNX, CUDA/TensorRT oder...

- A: `inference-optimization` · required · raw_text: "Model Optimization"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_138 - skill `ai-ml` (disagreement)

> ...Softwareentwicklungsteams - Brückenbauer-Mentalität: Du verstehst sowohl die klassische Backend-Welt als auch KI-Konzepte - Problemlösungsorientierte Denkweise mit der Fähigkeit,...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Du verstehst sowohl die klassische Backend-Welt als auch KI-Konzepte"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_138 - skill `backend-development` (disagreement)

> ...intensiv in dieses spannende Feld einzuarbeiten. Wenn du solide Backend-Entwicklungsskills hast und die Zukunft der KI-Integration mitgestalten...

- A: (did not label this)
- B: `backend-development` · required · raw_text: "solide Backend-Entwicklungsskills"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_138 - skill `software-engineering` (disagreement)

> ...in diesem dynamischen Feld am Ball zu bleiben - Erfahrung in agilen Softwareentwicklungsteams - Brückenbauer-Mentalität: Du verstehst sowohl die...

- A: `software-engineering` · required · raw_text: "Erfahrung in agilen Softwareentwicklungsteams"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_139 - skill `cybersecurity` (disagreement)

> ...hinaus: Themen wie Testing, Deployment, Skalierbarkeit, Sicherheit und zuverlässiger Produktivbetrieb gehören für dich zu...

- A: (did not label this)
- B: `cybersecurity` · required · raw_text: "Sicherheit"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_141 - skill `ai-deployment` (disagreement)

> ...Demonstrated success in sim-to-real transfer and deploying learning-based policies on physical robots - Strong problem-solving skills and the ability to work...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying learning-based policies on physical robots"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_141 - skill `model-development` (disagreement)

> ...uncertain scenarios Beneficial Skills - Experience in training locomotion and locomanipulation policies - Experience in training and deploying on humanoid...

- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "training locomotion and locomanipulation policies"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_144 - skill `multi-agent-systems` (disagreement)

> ...like RAG, few shot learning, prompt/context engineering, multi-agent orchestration, multimodal understanding, or fine-tuning that are used to...

- A: (did not label this)
- B: `multi-agent-systems` · required · raw_text: "multi-agent orchestration"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_147 - skill `software-architecture` (disagreement)

> ...Fundierte Kenntnisse in REST APIs, OpenAPI, JSON und modernen Integrationsarchitekturen - Praxiserfahrung mit MS Azure, Microsoft 365, Entra ID...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "modernen Integrationsarchitekturen"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_134 - skill `conversational-ai` (uncertain)

> ...in der Entwicklung und Bereitstellung von KI-Agenten und automatisierten Gesprächssystemen (Chatbots/KI-Bots) Grundkenntnisse in DevOps-Methoden, insbesondere...

- A: `conversational-ai` · required · raw_text: "automatisierten Gesprächssystemen (Chatbots/KI-Bots)"
- B: `conversational-ai` · required · raw_text: "automatisierten Gesprächssystemen (Chatbots/KI-Bots)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 29. golden_134 - skill `llms` (uncertain)

> ...Enthusiast oder Vibe Coder mit Proof Record Erfahrung mit Large Language Model (LLM)-Frameworks (z. B. LangChain, LlamaIndex, Hugging Face) Kenntnisse im...

- A: `llms` · required · raw_text: "Erfahrung mit Large Language Model (LLM)-Frameworks"
- B: `llms` · required · raw_text: "Large Language Model (LLM)-Frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 30. golden_135 - skill `access-control` (uncertain)

> ...Geschäftsdaten mit und verstehst Anforderungen an Berechtigungen, Datenschutz und Mandantentrennung Du arbeitest regelmäßig...

- A: `access-control` · required · raw_text: "Berechtigungen"
- B: `access-control` · required · raw_text: "Berechtigungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 31. golden_135 - skill `data-privacy-and-security` (uncertain)

> ...mit und verstehst Anforderungen an Berechtigungen, Datenschutz und Mandantentrennung Du arbeitest regelmäßig mit...

- A: `data-privacy-and-security` · required · raw_text: "Datenschutz"
- B: `data-privacy-and-security` · required · raw_text: "Datenschutz"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 32. golden_135 - skill `git` (uncertain)

> ...beispielsweise mit Playwright, sowie CI/CD-Prozesse auf GitHub und legst großen Wert auf die Korrektheit...

- A: `git` · required · raw_text: "auf GitHub"
- B: `git` · required · raw_text: "GitHub"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 33. golden_135 - skill `llm-orchestration` (uncertain)

> ...mit Tool Calling, Retrieval oder mehrstufigen Workflows Du bringst Erfahrung in der Modellierung komplexer...

- A: `llm-orchestration` · required · raw_text: "mehrstufigen Workflows"
- B: `llm-orchestration` · required · raw_text: "mehrstufigen Workflows"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 34. golden_135 - skill `rag` (uncertain)

> ...und produktiv eingesetzt, beispielsweise mit Tool Calling, Retrieval oder mehrstufigen Workflows Du bringst Erfahrung in der...

- A: `rag` · required · raw_text: "Retrieval"
- B: `rag` · required · raw_text: "Retrieval"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 35. golden_136 - skill `aws` (uncertain)

> ...in Python, Software-Architektur, Cloud-Plattformen (Azure, AWS, GCP) - Praktische Erfahrung mit LLMs, RAG, Agentic AI,...

- A: `aws` · required · raw_text: "AWS"
- B: `aws` · required · raw_text: "AWS"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 36. golden_136 - skill `azure` (uncertain)

> ...in Python, Software-Architektur, Cloud-Plattformen (Azure, AWS, GCP) - Praktische Erfahrung mit LLMs, RAG, Agentic...

- A: `azure` · required · raw_text: "Azure"
- B: `azure` · required · raw_text: "Azure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 37. golden_136 - skill `crewai` (uncertain)

> ...und Orchestrierungsframeworks (LangGraph, CrewAI, LlamaIndex) - MLOps/LLMOps, CI/CD, Kubernetes, Git und...

- A: `crewai` · required · raw_text: "CrewAI"
- B: `crewai` · required · raw_text: "CrewAI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 38. golden_136 - skill `gcp` (uncertain)

> ...Software-Architektur, Cloud-Plattformen (Azure, AWS, GCP) - Praktische Erfahrung mit LLMs, RAG, Agentic AI,...

- A: `gcp` · required · raw_text: "GCP"
- B: `gcp` · required · raw_text: "GCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_136 - skill `langgraph` (uncertain)

> ...AI, Vektordatenbanken und Orchestrierungsframeworks (LangGraph, CrewAI, LlamaIndex) - MLOps/LLMOps, CI/CD, Kubernetes,...

- A: `langgraph` · required · raw_text: "LangGraph"
- B: `langgraph` · required · raw_text: "LangGraph"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_136 - skill `llamaindex` (uncertain)

> ...und Orchestrierungsframeworks (LangGraph, CrewAI, LlamaIndex) - MLOps/LLMOps, CI/CD, Kubernetes, Git und...

- A: `llamaindex` · required · raw_text: "LlamaIndex"
- B: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_137 - attribute `degree` (uncertain)

> ...Mathematik, Physik oder einer vergleichbaren Fachrichtung, Promotion erwünscht • Mehrjährige Erfahrung in Machine Learning und Deep...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Promotion erwünscht"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Promotion erwünscht"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_137 - attribute `seniority` (uncertain)

> ...mit unseren Teams und Kunden • Fachliche Begleitung und Mentoring innerhalb des Teams sowie aktive Weitergabe von Wissen und Best Practices. •...

- A: value="senior" · basis="inferred" · signal="Mentoring innerhalb des Teams"
- B: value="senior" · basis="inferred" · signal="Fachliche Begleitung und Mentoring innerhalb des Teams"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_137 - skill `ai-deployment` (uncertain)

> ...oder vergleichbaren Technologien • Kenntnisse der MLOps und Deployment, z. B. Docker, Kubernetes, MLflow und CI/CD • Azure oder...

- A: `ai-deployment` · required · raw_text: "MLOps und Deployment"
- B: `ai-deployment` · required · raw_text: "Kenntnisse der MLOps und Deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_137 - skill `transformers` (uncertain)

> ...Vision, z. B. Object Detection, Segmentation, Tracking, Vision Transformer und multimodale Modelle • Know how der Generative AI, z....

- A: `transformers` · required · raw_text: "Vision Transformer"
- B: `transformers` · required · raw_text: "Vision Transformer"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_138 - skill `apis` (uncertain)

> ...Enterprise Edition (oder vergleichbares) - Verständnis von REST API-Design und -Implementierung - Hands-on Erfahrung mit Containerisierungstechnologien...

- A: `apis` · required · raw_text: "REST API-Design und -Implementierung"
- B: `apis` · required · raw_text: "REST API-Design und -Implementierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_138 - skill `git` (uncertain)

> ...Azure, GCP) - Praxiserfahrung mit CI/CD-Tools (GitLab, GitHub, Jenkins, AWS CodeBuild/CodePipeline, Azure DevOps) **KI...

- A: `git` · required · raw_text: "GitHub"
- B: `git` · required · raw_text: "GitHub"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_138 - skill `gitlab-ci` (uncertain)

> ...(AWS, Azure, GCP) - Praxiserfahrung mit CI/CD-Tools (GitLab, GitHub, Jenkins, AWS CodeBuild/CodePipeline, Azure...

- A: `gitlab-ci` · required · raw_text: "GitLab"
- B: `gitlab-ci` · required · raw_text: "GitLab"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_138 - skill `java` (uncertain)

> ...Technisches Know-how **Backend-Entwicklung:** - Fundierte Erfahrung in Java/Kotlin und Python - Umfassende Erfahrung mit Spring (Boot) oder...

- A: `java` · required · raw_text: "Fundierte Erfahrung in Java/Kotlin"
- B: `java` · required · raw_text: "Java"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_138 - skill `kotlin` (uncertain)

> ...Technisches Know-how **Backend-Entwicklung:** - Fundierte Erfahrung in Java/Kotlin und Python - Umfassende Erfahrung mit Spring (Boot) oder...

- A: `kotlin` · required · raw_text: "Fundierte Erfahrung in Java/Kotlin"
- B: `kotlin` · required · raw_text: "Kotlin"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_138 - skill `kubernetes` (uncertain)

> ...(Docker, Podman) - Kenntnisse in Kubernetes/OpenShift und Cloud-Plattformen (AWS, Azure, GCP) - Praxiserfahrung...

- A: `kubernetes` · required · raw_text: "Kubernetes/OpenShift"
- B: `kubernetes` · required · raw_text: "Kubernetes"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_138 - skill `llm-orchestration` (uncertain)

> ...einzuarbeiten - Idealerweise erste Erfahrungen mit Agent-Frameworks oder Orchestrierung - Optional: Kenntnisse in Model Fine-tuning, Prompt...

- A: `llm-orchestration` · nice_to_have · raw_text: "Agent-Frameworks oder Orchestrierung"
- B: `llm-orchestration` · nice_to_have · raw_text: "Orchestrierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_138 - skill `openshift` (uncertain)

> ...(Docker, Podman) - Kenntnisse in Kubernetes/OpenShift und Cloud-Plattformen (AWS, Azure, GCP) - Praxiserfahrung...

- A: `openshift` · required · raw_text: "Kubernetes/OpenShift"
- B: `openshift` · required · raw_text: "OpenShift"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_139 - attribute `degree` (uncertain)

> ...im AI Engineering oder Machine Learning gearbeitet. Ein abgeschlossenes Studium in Informatik, Data Science oder einem verwandten Bereich ist willkommen – ebenso eine vergleichbare Qualifikation durch Praxiserfahrung.✓ Du übernimmst gerne Verantwortung: Du arbeitest...

- A: value="bachelor" · requirement="nice_to_have" · or_equivalent=true · signal="Ein abgeschlossenes Studium in Informatik, Data Science oder einem verwandten Bereich ist willkommen – ebenso eine vergleichbare Qualifikation durch Praxiserfahrung"
- B: value="bachelor" · requirement="nice_to_have" · or_equivalent=true · signal="Ein abgeschlossenes Studium in Informatik, Data Science oder einem verwandten Bereich ist willkommen – ebenso eine vergleichbare Qualifikation durch Praxiserfahrung."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_139 - skill `agents` (uncertain)

> ...von AI-Modellen. Konzepte wie Prompt Engineering, RAG oder AI Agents sind dir vertraut.✓ Du verstehst Machine Learning: Du kennst grundlegende...

- A: `agents` · required · raw_text: "AI Agents sind dir vertraut"
- B: `agents` · required · raw_text: "AI Agents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_139 - skill `model-development` (uncertain)

> ...Machine Learning: Du kennst grundlegende ML-Verfahren, Modelltraining und Evaluation und hast idealerweise bereits mit...

- A: `model-development` · required · raw_text: "Modelltraining"
- B: `model-development` · required · raw_text: "Modelltraining"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_139 - skill `prompt-engineering` (uncertain)

> ...AI und der Integration von AI-Modellen. Konzepte wie Prompt Engineering, RAG oder AI Agents sind dir vertraut.✓ Du verstehst...

- A: `prompt-engineering` · required · raw_text: "Prompt Engineering"
- B: `prompt-engineering` · required · raw_text: "Prompt Engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_139 - skill `rag` (uncertain)

> ...von AI-Modellen. Konzepte wie Prompt Engineering, RAG oder AI Agents sind dir vertraut.✓ Du verstehst Machine Learning: Du...

- A: `rag` · required · raw_text: "RAG oder AI Agents"
- B: `rag` · required · raw_text: "RAG"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_139 - skill `software-engineering` (uncertain)

> ...mit APIs, Datenbanken, Softwarearchitektur und der Entwicklung professioneller Softwarelösungen.✓ Du kennst dich mit moderner AI aus: Du hast praktische...

- A: `software-engineering` · required · raw_text: "Entwicklung professioneller Softwarelösungen"
- B: `software-engineering` · required · raw_text: "Entwicklung professioneller Softwarelösungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_140 - attribute `seniority` (uncertain)

> ...in Computer Science or a comparable IT-related field. - Several years of professional experience in Automotive Cybersecurity. - Strong expertise in...

- A: value="mid" · basis="inferred" · signal="Several years of professional experience"
- B: value="mid" · basis="inferred" · signal="Several years of professional experience in Automotive Cybersecurity."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_140 - skill `agents` (uncertain)

> ...in Automotive Cybersecurity. - Strong expertise in building, operating, and maintaining agentic AI toolchains using both commercial and open-source technologies. -...

- A: `agents` · required · raw_text: "building, operating, and maintaining agentic AI toolchains"
- B: `agents` · required · raw_text: "agentic AI toolchains"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_140 - skill `ansible` (uncertain)

> ...as well as CI/CD and Infrastructure-as-Code tools (e.g., Terraform, Ansible, GitHub Actions/GitLab CI). - Business-fluent German and English language...

- A: `ansible` · required · raw_text: "Terraform, Ansible, GitHub Actions"
- B: `ansible` · required · raw_text: "Ansible, GitHub Actions/GitLab CI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_140 - skill `cybersecurity` (uncertain)

> ...or a comparable IT-related field. - Several years of professional experience in Automotive Cybersecurity. - Strong expertise in building, operating, and...

- A: `cybersecurity` · required · raw_text: "professional experience in Automotive Cybersecurity"
- B: `cybersecurity` · required · raw_text: "Automotive Cybersecurity"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_140 - skill `docker` (uncertain)

> ...containerization and orchestration technologies (Docker/Kubernetes), as well as CI/CD and Infrastructure-as-Code tools (e.g.,...

- A: `docker` · required · raw_text: "Docker/Kubernetes"
- B: `docker` · required · raw_text: "Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_140 - skill `kubernetes` (uncertain)

> ...containerization and orchestration technologies (Docker/Kubernetes), as well as CI/CD and Infrastructure-as-Code tools (e.g.,...

- A: `kubernetes` · required · raw_text: "Docker/Kubernetes"
- B: `kubernetes` · required · raw_text: "Kubernetes"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_140 - skill `terraform` (uncertain)

> ...as well as CI/CD and Infrastructure-as-Code tools (e.g., Terraform, Ansible, GitHub Actions/GitLab CI). - Business-fluent German and English language...

- A: `terraform` · required · raw_text: "Terraform, Ansible, GitHub Actions"
- B: `terraform` · required · raw_text: "Terraform, Ansible, GitHub Actions/GitLab CI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_142 - skill `agents` (uncertain)

> ...TypeScript - Ausgeprägtes Interesse an AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering - Ganzheitliches Denkvermögen,...

- A: `agents` · required · raw_text: "agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz"
- B: `agents` · required · raw_text: "agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_142 - skill `ai-developer-tooling` (uncertain)

> ...mit C#/.NET, PowerShell oder TypeScript - Ausgeprägtes Interesse an AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering - Ganzheitliches Denkvermögen, hohe Eigenverantwortung und...

- A: `ai-developer-tooling` · required · raw_text: "Interesse an AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering"
- B: `ai-developer-tooling` · required · raw_text: "AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_142 - skill `distributed-systems` (uncertain)

> ...in Softwareentwicklung oder Testautomatisierung für verteilte Softwarelösungen on-premise und in der Cloud - Sehr gute Kenntnisse in...

- A: `distributed-systems` · required · raw_text: "verteilte Softwarelösungen"
- B: `distributed-systems` · required · raw_text: "verteilte Softwarelösungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_142 - skill `software-engineering` (uncertain)

> ...in DevSecOps, CI/CD, Infrastructure as Code und Container, in Softwareentwicklung oder Testautomatisierung für verteilte Softwarelösungen...

- A: `software-engineering` · required · raw_text: "in Softwareentwicklung"
- B: `software-engineering` · required · raw_text: "Softwareentwicklung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_143 - skill `access-control` (uncertain)

> ...its ML/data ecosystem (e.g. SageMaker, S3, EKS, Lambda, IAM) - solid background in cloud platforms, MLOps, and model...

- A: `access-control` · required · raw_text: "IAM"
- B: `access-control` · required · raw_text: "IAM"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_143 - skill `ai-ml` (uncertain)

> ...years of experience in data science, machine learning, or applied AI - strong hands-on skills in Python, SQL, and common ML...

- A: `ai-ml` · required · raw_text: "applied AI"
- B: `ai-ml` · required · raw_text: "applied AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_143 - skill `aws-s3` (uncertain)

> ...ML solutions using AWS services (e.g. SageMaker, S3, Lambda, EMR, etc.) - ensure model quality, monitoring,...

- A: `aws-s3` · required · raw_text: "S3"
- B: `aws-s3` · required · raw_text: "S3"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_143 - skill `data-science` (uncertain)

> ...senior technical advisor YOU COME WITH - 10+ years of experience in data science, machine learning, or applied AI - strong hands-on skills...

- A: `data-science` · required · raw_text: "experience in data science"
- B: `data-science` · required · raw_text: "data science"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_143 - skill `machine-learning` (uncertain)

> ...advisor YOU COME WITH - 10+ years of experience in data science, machine learning, or applied AI - strong hands-on skills in Python, SQL, and common ML...

- A: `machine-learning` · required · raw_text: "data science, machine learning, or applied AI"
- B: `machine-learning` · required · raw_text: "machine learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_143 - skill `sagemaker` (uncertain)

> ...production-ready ML solutions using AWS services (e.g. SageMaker, S3, Lambda, EMR, etc.) - ensure model quality,...

- A: `sagemaker` · required · raw_text: "SageMaker"
- B: `sagemaker` · required · raw_text: "SageMaker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_144 - skill `agents` (uncertain)

> ...technical Proof of Concept projects - Hands-on experience building agentic systems using LLM orchestration, RAG, function calling, and prompt...

- A: `agents` · nice_to_have · raw_text: "building agentic systems"
- B: `agents` · nice_to_have · raw_text: "agentic systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_144 - skill `llm-orchestration` (uncertain)

> ...like RAG, few shot learning, prompt/context engineering, multi-agent orchestration, multimodal understanding, or fine-tuning that are used to...

- A: `llm-orchestration` · required · raw_text: "multi-agent orchestration"
- B: `llm-orchestration` · required · raw_text: "multi-agent orchestration"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_144 - skill `prompt-engineering` (uncertain)

> ...of generative AI techniques like RAG, few shot learning, prompt/context engineering, multi-agent orchestration, multimodal understanding, or...

- A: `prompt-engineering` · required · raw_text: "prompt/context engineering"
- B: `prompt-engineering` · required · raw_text: "prompt/context engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 79. golden_144 - skill `rag` (uncertain)

> ...of business and technology. - Understanding of generative AI techniques like RAG, few shot learning, prompt/context engineering,...

- A: `rag` · required · raw_text: "generative AI techniques like RAG"
- B: `rag` · required · raw_text: "RAG"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 80. golden_145 - attribute `degree` (uncertain)

> ...toolchain performance. What should you bring along? - University degree in Computer Science, Electrical Engineering, or a comparable qualification. - Several years of professional experience in Automotive...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="University degree in Computer Science, Electrical Engineering, or a comparable qualification"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="University degree in Computer Science, Electrical Engineering, or a comparable qualification."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 81. golden_145 - attribute `seniority` (uncertain)

> ...Electrical Engineering, or a comparable qualification. - Several years of professional experience in Automotive Cybersecurity. - Strong expertise in building, operating, and...

- A: value="mid" · basis="inferred" · signal="Several years of professional experience in Automotive Cybersecurity"
- B: value="mid" · basis="inferred" · signal="Several years of professional experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 82. golden_145 - skill `cybersecurity` (uncertain)

> ...or a comparable qualification. - Several years of professional experience in Automotive Cybersecurity. - Strong expertise in building, operating, and...

- A: `cybersecurity` · required · raw_text: "professional experience in Automotive Cybersecurity"
- B: `cybersecurity` · required · raw_text: "Automotive Cybersecurity"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 83. golden_146 - attribute `degree` (uncertain)

> ...machine learning deployments on AWS, Azure, or GCP - Graduate degree in a quantitative discipline (Computer Science, Engineering, Statistics, Operations Research, etc.) or equivalent practical experience - Experience communicating and/or teaching technical...

- A: value="master" · requirement="required" · or_equivalent=true · signal="Graduate degree in a quantitative discipline (Computer Science, Engineering, Statistics, Operations Research, etc.) or equivalent practical experience"
- B: value="master" · requirement="required" · or_equivalent=true · signal="Graduate degree in a quantitative discipline (Computer Science, Engineering, Statistics, Operations Research, etc.) or equivalent practical experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 84. golden_146 - skill `ai-deployment` (uncertain)

> ...such as HuggingFace, LangChain, and DSPy - Expertise in deploying production-grade GenAI applications, including evaluation and optimisations - Extensive...

- A: `ai-deployment` · required · raw_text: "deploying production-grade GenAI applications"
- B: `ai-deployment` · required · raw_text: "deploying production-grade GenAI applications"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 85. golden_146 - skill `llms` (uncertain)

> ...roadmap What we look for: - Min 4 years' experience - Experience building GenAI applications, including RAG, multi-agent systems, Text2SQL,...

- A: `llms` · required · raw_text: "Experience building GenAI applications"
- B: `llms` · required · raw_text: "GenAI applications"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 86. golden_147 - attribute `degree` (uncertain)

> ...und technischen Rollout-Konzepten ## Anforderungen: - Studium oder abgeschlossene Berufsausbildung IT (z.B. Systemintegration, Anwendungsentwicklung, Computer...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Studium oder abgeschlossene Berufsausbildung IT"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Studium oder abgeschlossene Berufsausbildung IT (z.B. Systemintegration, Anwendungsentwicklung, Computer Science)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 87. golden_147 - skill `ai-ml` (uncertain)

> ...sowie komplexen Systemlandschaften - Gute Kenntnisse AI, GenAI, Automatisierung oder datengetriebenen...

- A: `ai-ml` · required · raw_text: "Gute Kenntnisse AI"
- B: `ai-ml` · required · raw_text: "AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 88. golden_147 - skill `backend-development` (uncertain)

> ...Know-how im Umgang mit Docker, Power Platform, Backend-Systemen und API-gesteuerten Anwendungen - Erfahrung in der...

- A: `backend-development` · required · raw_text: "Backend-Systemen"
- B: `backend-development` · required · raw_text: "Backend-Systemen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 89. golden_147 - skill `cloud` (uncertain)

> ...Praxiserfahrung mit MS Azure, Microsoft 365, Entra ID und Cloud-Services - Know-how im Umgang mit Docker, Power Platform,...

- A: `cloud` · required · raw_text: "Cloud-Services"
- B: `cloud` · required · raw_text: "Cloud-Services"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 90. golden_147 - skill `workflow-automation` (uncertain)

> ...komplexen Systemlandschaften - Gute Kenntnisse AI, GenAI, Automatisierung oder datengetriebenen Anwendungen - Strukturierte,...

- A: `workflow-automation` · required · raw_text: "Automatisierung"
- B: `workflow-automation` · required · raw_text: "Automatisierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 91. golden_148 - attribute `seniority` (uncertain)

> ...oder einer vergleichbaren Fachrichtung. • Mindestens zwei Jahre Erfahrung in Data Science, Machine Learning oder AI- Engineering...

- A: value="junior" · basis="inferred" · signal="Mindestens zwei Jahre Erfahrung"
- B: value="junior" · basis="inferred" · signal="Mindestens zwei Jahre Erfahrung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 92. golden_148 - skill `agents` (uncertain)

> ...oder PyTorch sowie Kenntnisse in Generativer KI, NLP oder agentenbasierten KI-Systemen. • Gute Kenntnisse in Python und SQL; idealerweise...

- A: `agents` · required · raw_text: "agentenbasierten KI-Systemen"
- B: `agents` · required · raw_text: "agentenbasierten KI-Systemen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 93. golden_148 - skill `mcp` (uncertain)

> ...sowie Grundlagen in KI-Governance (EU AI Act, DSGVO) und MCP. • Analytische Denkweise, hohe Eigenverantwortung und...

- A: `mcp` · nice_to_have · raw_text: "MCP"
- B: `mcp` · nice_to_have · raw_text: "idealerweise Erfahrung mit Low-Code-/No-Code-Plattformen sowie Grundlagen in KI-Governance (EU AI Act, DSGVO) und MCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 94. golden_134 - attribute `degree` (spot-check)

> ...Bereitstellung von Best Practices WAS SIE MITBRINGEN Abgeschlossenes wissenschaftliches Hochschulstudium (min. Bachelor) in einem MINT-Fach, oder vergleichbare Qualifikation als Quereinsteiger, Tech Enthusiast oder Vibe Coder mit Proof Record...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossenes wissenschaftliches Hochschulstudium (min. Bachelor) in einem MINT-Fach, oder vergleichbare Qualifikation als Quereinsteiger"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_134 - skill `agents` (spot-check)

> ...Erfahrung in der Entwicklung und Bereitstellung von KI-Agenten und automatisierten Gesprächssystemen (Chatbots/KI-Bots)...

- agreed label: `agents` · required · raw_text: "KI-Agenten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_134 - skill `langchain` (spot-check)

> ...Erfahrung mit Large Language Model (LLM)-Frameworks (z. B. LangChain, LlamaIndex, Hugging Face) Kenntnisse im Aufbau von...

- agreed label: `langchain` · required · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_135 - attribute `german` (spot-check)

> ...und qualitätsorientiert und verfügst über Deutschkenntnisse auf C2-Niveau sowie Englischkenntnisse auf C1-Niveau Zusätzlich...

- agreed label: value="required" · basis="stated" · signal="Deutschkenntnisse auf C2-Niveau"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_135 - attribute `seniority` (spot-check)

> ...aktiv ins Team ein Profil Du hast mindestens 4 Jahre Erfahrung in der professionellen Softwareentwicklung, idealerweise...

- agreed label: value="mid" · basis="inferred" · signal="mindestens 4\nJahre Erfahrung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_135 - skill `ai-developer-tooling` (spot-check)

> ...und Mandantentrennung Du arbeitest regelmäßig mit AI-Coding-Tools wie Claude Code, Cursor oder Codex, entwickelst...

- agreed label: `ai-developer-tooling` · required · raw_text: "AI-Coding-Tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_135 - skill `claude-code` (spot-check)

> ...Du arbeitest regelmäßig mit AI-Coding-Tools wie Claude Code, Cursor oder Codex, entwickelst spezifikationsbasiert...

- agreed label: `claude-code` · required · raw_text: "Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_135 - skill `cursor` (spot-check)

> ...arbeitest regelmäßig mit AI-Coding-Tools wie Claude Code, Cursor oder Codex, entwickelst spezifikationsbasiert...

- agreed label: `cursor` · required · raw_text: "Cursor"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_135 - skill `data-modeling` (spot-check)

> ...oder mehrstufigen Workflows Du bringst Erfahrung in der Modellierung komplexer Geschäftsdaten mit und verstehst Anforderungen an Berechtigungen,...

- agreed label: `data-modeling` · required · raw_text: "Modellierung komplexer Geschäftsdaten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_135 - skill `forecasting` (spot-check)

> ...oder ERP-Software, XRechnung, ZUGFeRD oder Forecasting Wir bieten Du arbeitest flexibel im Home-Office, bis zu...

- agreed label: `forecasting` · nice_to_have · raw_text: "Forecasting"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_135 - skill `llms` (spot-check)

> ...Fokus auf Testautomatisierung Du hast bereits LLM-basierte Agenten oder KI-Funktionen entwickelt und produktiv...

- agreed label: `llms` · required · raw_text: "LLM-basierte Agenten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_135 - skill `software-engineering` (spot-check)

> ...ein Profil Du hast mindestens 4 Jahre Erfahrung in der professionellen Softwareentwicklung, idealerweise mit produktiven Cloud- oder SaaS-Anwendungen...

- agreed label: `software-engineering` · required · raw_text: "professionellen Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_136 - attribute `german` (spot-check)

> ...Ausgeprägte Beratungskompetenz, Workshop-Leitung - Fließend in Deutsch und Englisch Wir wertschätzen Vielfalt und begrüßen daher alle...

- agreed label: value="required" · basis="stated" · signal="Fließend in Deutsch und Englisch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_136 - attribute `seniority` (spot-check)

> Senior AI Engineer / AI Architect (all gender) **Wir sind die Gestalter von heute für die...

- agreed label: value="senior" · basis="stated" · signal="Senior AI Engineer / AI Architect"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_136 - skill `agents` (spot-check)

> ...(Azure, AWS, GCP) - Praktische Erfahrung mit LLMs, RAG, Agentic AI, Vektordatenbanken und Orchestrierungsframeworks...

- agreed label: `agents` · required · raw_text: "Agentic AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_136 - skill `rag` (spot-check)

> ...(Azure, AWS, GCP) - Praktische Erfahrung mit LLMs, RAG, Agentic AI, Vektordatenbanken und Orchestrierungsframeworks...

- agreed label: `rag` · required · raw_text: "RAG, Agentic AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_136 - skill `vector-databases` (spot-check)

> ...GCP) - Praktische Erfahrung mit LLMs, RAG, Agentic AI, Vektordatenbanken und Orchestrierungsframeworks (LangGraph, CrewAI,...

- agreed label: `vector-databases` · required · raw_text: "Vektordatenbanken"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_137 - skill `azure` (spot-check)

> ...Deployment, z. B. Docker, Kubernetes, MLflow und CI/CD • Azure oder AWS sowie On-Premise- und hybrides Infrastrukturen Wissen •...

- agreed label: `azure` · required · raw_text: "Azure oder AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_137 - skill `ci-cd` (spot-check)

> ...MLOps und Deployment, z. B. Docker, Kubernetes, MLflow und CI/CD • Azure oder AWS sowie On-Premise- und hybrides...

- agreed label: `ci-cd` · required · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_137 - skill `docker` (spot-check)

> ...Kenntnisse der MLOps und Deployment, z. B. Docker, Kubernetes, MLflow und CI/CD • Azure oder AWS sowie...

- agreed label: `docker` · required · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_137 - skill `embeddings` (spot-check)

> ...Generative AI, z. B. LLMs, Vision-Language Models, RAG, Embeddings und Fine-Tuning • Erfahrung mit Edge AI und Model...

- agreed label: `embeddings` · required · raw_text: "Embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_137 - skill `git` (spot-check)

> ...Kenntnisse • Sehr gutes Software-Engineering Know how mit Git, Linux und Testing; C++ • Idealerweise Erfahrung im...

- agreed label: `git` · required · raw_text: "Git"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_137 - skill `linux` (spot-check)

> ...Sehr gutes Software-Engineering Know how mit Git, Linux und Testing; C++ • Idealerweise Erfahrung im...

- agreed label: `linux` · required · raw_text: "Linux"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_137 - skill `python` (spot-check)

> ...und hybrides Infrastrukturen Wissen • Sehr gute Python, PyTorch/TensorFlow und OpenCV Kenntnisse • Sehr gutes...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_137 - skill `pytorch` (spot-check)

> ...und hybrides Infrastrukturen Wissen • Sehr gute Python, PyTorch/TensorFlow und OpenCV Kenntnisse • Sehr gutes Software-Engineering...

- agreed label: `pytorch` · required · raw_text: "PyTorch/TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_137 - skill `quantization` (spot-check)

> ...Erfahrung mit Edge AI und Model Optimization, z. B. Quantization, Pruning, ONNX, CUDA/TensorRT oder vergleichbaren...

- agreed label: `quantization` · required · raw_text: "Quantization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_137 - skill `tensorflow` (spot-check)

> ...und hybrides Infrastrukturen Wissen • Sehr gute Python, PyTorch/TensorFlow und OpenCV Kenntnisse • Sehr gutes Software-Engineering...

- agreed label: `tensorflow` · required · raw_text: "PyTorch/TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_137 - skill `testing` (spot-check)

> ...gutes Software-Engineering Know how mit Git, Linux und Testing; C++ • Idealerweise Erfahrung im wissenschaftlichen...

- agreed label: `testing` · required · raw_text: "Testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_138 - attribute `degree` (spot-check)

> Cloud Software Engineer mit KI-Fokus (m/w/d)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_138 - attribute `german` (spot-check)

> Cloud Software Engineer mit KI-Fokus (m/w/d)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_138 - skill `agents` (spot-check)

> ...(MCP) oder Bereitschaft, sich intensiv einzuarbeiten - Idealerweise erste Erfahrungen mit Agent-Frameworks oder Orchestrierung - Optional: Kenntnisse in Model...

- agreed label: `agents` · nice_to_have · raw_text: "Idealerweise erste Erfahrungen mit Agent-Frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_138 - skill `api-design` (spot-check)

> ...Enterprise Edition (oder vergleichbares) - Verständnis von REST API-Design und -Implementierung - Hands-on Erfahrung mit...

- agreed label: `api-design` · required · raw_text: "REST API-Design"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_138 - skill `argocd` (spot-check)

> ...Verständnis von GitOps-Prinzipien und Tools wie ArgoCD oder Flux ### Persönliche Eigenschaften - Ausgeprägtes...

- agreed label: `argocd` · nice_to_have · raw_text: "ArgoCD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_138 - skill `cloud` (spot-check)

> ...(Docker, Podman) - Kenntnisse in Kubernetes/OpenShift und Cloud-Plattformen (AWS, Azure, GCP) - Praxiserfahrung mit CI/CD-Tools (GitLab, GitHub,...

- agreed label: `cloud` · required · raw_text: "Cloud-Plattformen (AWS, Azure, GCP)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_138 - skill `containerization` (spot-check)

> ...API-Design und -Implementierung - Hands-on Erfahrung mit Containerisierungstechnologien (Docker, Podman) - Kenntnisse in Kubernetes/OpenShift und...

- agreed label: `containerization` · required · raw_text: "Containerisierungstechnologien"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_138 - skill `langchain` (spot-check)

> ...evolvierende KI-Technologien einzuarbeiten **Bonus:** - Erfahrung mit LangChain, LlamaIndex, LangChain4J oder vergleichbaren Frameworks -...

- agreed label: `langchain` · nice_to_have · raw_text: "Erfahrung mit LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_138 - skill `mlops` (spot-check)

> ...Optional: Kenntnisse in Model Fine-tuning, Prompt Engineering oder MLOps - Bereitschaft, sich kontinuierlich in schnell...

- agreed label: `mlops` · nice_to_have · raw_text: "Prompt Engineering oder MLOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_138 - skill `prompt-engineering` (spot-check)

> ...Optional: Kenntnisse in Model Fine-tuning, Prompt Engineering oder MLOps - Bereitschaft, sich kontinuierlich in schnell...

- agreed label: `prompt-engineering` · nice_to_have · raw_text: "Prompt Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_138 - skill `vector-databases` (spot-check)

> ...LlamaIndex, LangChain4J oder vergleichbaren Frameworks - Kenntnisse in Vektordatenbanken (Pinecone, Weaviate, Qdrant, ChromaDB) - Verständnis von...

- agreed label: `vector-databases` · nice_to_have · raw_text: "Kenntnisse in Vektordatenbanken"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_139 - skill `apis` (spot-check)

> ...stark: Python gehört zu deinem Werkzeugkasten. Du hast Erfahrung mit APIs, Datenbanken, Softwarearchitektur und der Entwicklung...

- agreed label: `apis` · required · raw_text: "Erfahrung mit APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_139 - skill `llms` (spot-check)

> ...Du kennst dich mit moderner AI aus: Du hast praktische Erfahrung mit Large Language Models, Generative AI und der Integration von AI-Modellen....

- agreed label: `llms` · required · raw_text: "praktische Erfahrung mit Large Language Models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_139 - skill `machine-learning` (spot-check)

> ...Prompt Engineering, RAG oder AI Agents sind dir vertraut.✓ Du verstehst Machine Learning: Du kennst grundlegende ML-Verfahren, Modelltraining und...

- agreed label: `machine-learning` · required · raw_text: "Du verstehst Machine Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_140 - attribute `degree` (spot-check)

> ...future analysis cycles. What should you bring along? - University degree in Computer Science or a comparable IT-related field. - Several years of professional experience in Automotive...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="University degree in Computer Science or a comparable IT-related field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_140 - skill `aws` (spot-check)

> ...tools). - Hands-on experience with cloud platforms (AWS/Azure), containerization and orchestration technologies...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_140 - skill `ci-cd` (spot-check)

> ...and orchestration technologies (Docker/Kubernetes), as well as CI/CD and Infrastructure-as-Code tools (e.g., Terraform,...

- agreed label: `ci-cd` · required · raw_text: "as well as CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_140 - skill `cloud` (spot-check)

> ...and penetration testing tools). - Hands-on experience with cloud platforms (AWS/Azure), containerization and orchestration...

- agreed label: `cloud` · required · raw_text: "cloud platforms"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_140 - skill `containerization` (spot-check)

> ...Hands-on experience with cloud platforms (AWS/Azure), containerization and orchestration technologies (Docker/Kubernetes), as well as CI/CD and...

- agreed label: `containerization` · required · raw_text: "containerization and orchestration technologies"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_140 - skill `infrastructure-as-code` (spot-check)

> ...technologies (Docker/Kubernetes), as well as CI/CD and Infrastructure-as-Code tools (e.g., Terraform, Ansible, GitHub Actions/GitLab CI). -...

- agreed label: `infrastructure-as-code` · required · raw_text: "Infrastructure-as-Code tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_141 - attribute `degree` (spot-check)

> ...on open-ended, evolving tasks Essential Skills - Master’s or PhD in robotics, computer science, engineering, or a related field - Proven experience (5+ years) applying RL or IL in...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s or PhD in robotics, computer science, engineering, or a related field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_141 - skill `cpp` (spot-check)

> ...algorithms (PPO, SAC, ...) - Proficiency in Python and/or C++, PyTorch, ONNX, and common RL frameworks (e.g, Stable...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_141 - skill `pytorch` (spot-check)

> ...(PPO, SAC, ...) - Proficiency in Python and/or C++, PyTorch, ONNX, and common RL frameworks (e.g, Stable Baselines 3,...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_142 - attribute `german` (spot-check)

> ...der strukturierten Analyse komplexer Fehlersituationen - Sehr gute Sprachkenntnisse in Deutsch und Englisch in Wort und Schrift Interesse? Dann freuen wir uns auf Deine Bewerbung!Gerne...

- agreed label: value="required" · basis="stated" · signal="Sehr gute Sprachkenntnisse in Deutsch und Englisch in Wort und Schrift"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_142 - attribute `seniority` (spot-check)

> Wir suchen Dich als

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_142 - skill `ci-cd` (spot-check)

> ...mit einschlägiger Berufserfahrung - Fundierte Erfahrung in DevSecOps, CI/CD, Infrastructure as Code und Container, in...

- agreed label: `ci-cd` · required · raw_text: "DevSecOps, CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_142 - skill `containerization` (spot-check)

> ...Berufserfahrung - Fundierte Erfahrung in DevSecOps, CI/CD, Infrastructure as Code und Container, in Softwareentwicklung oder Testautomatisierung für...

- agreed label: `containerization` · required · raw_text: "Infrastructure as Code und Container"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_142 - skill `devsecops` (spot-check)

> ...Qualifikation mit einschlägiger Berufserfahrung - Fundierte Erfahrung in DevSecOps, CI/CD, Infrastructure as Code und Container, in...

- agreed label: `devsecops` · required · raw_text: "Fundierte Erfahrung in DevSecOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_142 - skill `infrastructure-as-code` (spot-check)

> ...Berufserfahrung - Fundierte Erfahrung in DevSecOps, CI/CD, Infrastructure as Code und Container, in Softwareentwicklung oder...

- agreed label: `infrastructure-as-code` · required · raw_text: "CI/CD, Infrastructure as Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_142 - skill `typescript` (spot-check)

> ...und Scripting, beispielsweise mit C#/.NET, PowerShell oder TypeScript - Ausgeprägtes Interesse an AI-Assistenten und agentischen...

- agreed label: `typescript` · required · raw_text: "oder TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_143 - skill `aws` (spot-check)

> ...proven experience with GenAI and LLMs in real products - strong experience with AWS and its ML/data ecosystem (e.g. SageMaker, S3, EKS,...

- agreed label: `aws` · required · raw_text: "strong experience with AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_143 - skill `llms` (spot-check)

> ...SQL, and common ML frameworks - proven experience with GenAI and LLMs in real products - strong experience with AWS and its...

- agreed label: `llms` · required · raw_text: "GenAI and LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_143 - skill `python` (spot-check)

> ...learning, or applied AI - strong hands-on skills in Python, SQL, and common ML frameworks - proven experience with...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_144 - attribute `degree` (spot-check)

> ...collateral, best practices, and tools. What You Need: - Degree in Engineering, Data Analytics/Science, Computer Science, Mathematics, or a related STEM field. - Excellent academic performance - Extensive internship...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="Degree in Engineering, Data Analytics/Science, Computer Science, Mathematics, or a related STEM field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 156. golden_144 - skill `context-engineering` (spot-check)

> ...of generative AI techniques like RAG, few shot learning, prompt/context engineering, multi-agent orchestration, multimodal understanding, or...

- agreed label: `context-engineering` · required · raw_text: "prompt/context engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 157. golden_144 - skill `data-engineering` (spot-check)

> ...LangChain, pandas, pydantic, sklearn, PyTorch) as well as data engineering tools and technologies. - Excellent analytical and creative problem-solving...

- agreed label: `data-engineering` · required · raw_text: "data engineering tools and technologies"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 158. golden_144 - skill `python` (spot-check)

> ...intelligent chatbots and automated text processors. - Good knowledge of Python and common ML libraries (such as LangChain, pandas,...

- agreed label: `python` · required · raw_text: "Good knowledge of Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 159. golden_144 - skill `tool-calling` (spot-check)

> ...building agentic systems using LLM orchestration, RAG, function calling, and prompt engineering - Working knowledge of tools in...

- agreed label: `tool-calling` · nice_to_have · raw_text: "function calling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 160. golden_145 - skill `agents` (spot-check)

> ...in Automotive Cybersecurity. - Strong expertise in building, operating, and maintaining agentic AI toolchains using both commercial and open-source technologies. -...

- agreed label: `agents` · required · raw_text: "building, operating, and maintaining agentic AI toolchains"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 161. golden_146 - skill `azure` (spot-check)

> ...production-grade machine learning deployments on AWS, Azure, or GCP - Graduate degree in a quantitative discipline...

- agreed label: `azure` · required · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 162. golden_146 - skill `evaluation` (spot-check)

> ...deploying production-grade GenAI applications, including evaluation and optimisations - Extensive years of hands-on industry...

- agreed label: `evaluation` · required · raw_text: "evaluation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 163. golden_146 - skill `gcp` (spot-check)

> ...machine learning deployments on AWS, Azure, or GCP - Graduate degree in a quantitative discipline (Computer...

- agreed label: `gcp` · required · raw_text: "GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 164. golden_146 - skill `rag` (spot-check)

> ...Experience building GenAI applications, including RAG, multi-agent systems, Text2SQL, fine-tuning, etc., with...

- agreed label: `rag` · required · raw_text: "RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 165. golden_146 - skill `scikit-learn` (spot-check)

> ...machine learning and data science tools, i.e. pandas, scikit-learn, PyTorch, etc. - Experience building production-grade...

- agreed label: `scikit-learn` · required · raw_text: "scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 166. golden_147 - attribute `german` (spot-check)

> ...Arbeitsweise sowie hohe Kunden- und Serviceorientierung - Sehr gute Deutsch- und Englischkenntnisse in Wort und Schrift ## Ihre Vorteile mit Robert Half - Kostenlose, schnelle...

- agreed label: value="required" · basis="stated" · signal="Sehr gute Deutsch- und Englischkenntnisse in Wort und Schrift"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 167. golden_147 - skill `azure` (spot-check)

> ...modernen Integrationsarchitekturen - Praxiserfahrung mit MS Azure, Microsoft 365, Entra ID und Cloud-Services - Know-how im...

- agreed label: `azure` · required · raw_text: "MS Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 168. golden_147 - skill `microsoft-entra-id` (spot-check)

> ...Integrationsarchitekturen - Praxiserfahrung mit MS Azure, Microsoft 365, Entra ID und Cloud-Services - Know-how im Umgang mit Docker, Power...

- agreed label: `microsoft-entra-id` · required · raw_text: "Microsoft 365, Entra ID"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 169. golden_148 - attribute `german` (spot-check)

> ...auf Niveau C1 oder C2, (Projektsprache ist Englisch); Deutschkenntnisse auf mindestens B12 Niveau. Gestalten Sie mit uns die nächste Generation...

- agreed label: value="required" · basis="stated" · signal="Deutschkenntnisse auf mindestens B12 Niveau"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 170. golden_148 - skill `data-science` (spot-check)

> ...einer vergleichbaren Fachrichtung. • Mindestens zwei Jahre Erfahrung in Data Science, Machine Learning oder AI- Engineering sowie in der...

- agreed label: `data-science` · required · raw_text: "Erfahrung in Data Science"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 171. golden_148 - skill `llms` (spot-check)

> ...LangGraph, LlamaIndex oder PyTorch sowie Kenntnisse in Generativer KI, NLP oder agentenbasierten KI-Systemen. • Gute Kenntnisse...

- agreed label: `llms` · required · raw_text: "Generativer KI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 172. golden_148 - skill `machine-learning` (spot-check)

> ...Mindestens zwei Jahre Erfahrung in Data Science, Machine Learning oder AI- Engineering sowie in der Umsetzung produktiver...

- agreed label: `machine-learning` · required · raw_text: "Machine Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 173. golden_148 - skill `sql` (spot-check)

> ...KI-Systemen. • Gute Kenntnisse in Python und SQL; idealerweise Erfahrung mit Low-Code-/No-Code-Plattformen...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
