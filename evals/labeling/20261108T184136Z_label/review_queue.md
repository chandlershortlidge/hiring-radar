# Review queue - 20261108T184136Z_label

147 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
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

Spot-check items are a seeded random sample (80 of 227 accepted labels,
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

> MaxIT | Applied AI Competence Center AI-DevOps Engineer (m/w/d) Die

- Max Planck Information and Technology · AI-DevOps Engineer (m/w/d)
- Munich · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_050 - scope `in_scope` (in-scope)

> AI Native Developer (m/w/d)

- TechMinds GmbH · AI Native Developer (m/w/d)
- Munich · de · arbeitsagentur · 17 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_051 - scope `in_scope` (in-scope)

> Senior AI Engineer / AI Architect (all gender)

- ALTEN GmbH München · Senior AI Engineer / AI Architect (all gender)
- Munich · de · arbeitsagentur · 21 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_052 - scope `in_scope` (in-scope)

> Machine Learning Innovation Engineer (m/w/d)

- ARRK Engineering GmbH · Machine Learning Innovation Engineer (m/w/d)
- Munich · de · arbeitsagentur · 25 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_053 - scope `in_scope` (in-scope)

> Cloud Software Engineer mit KI-Fokus (m/w/d)

- TekkMinds AG · Cloud Software Engineer mit KI-Fokus (m/w/d)
- Munich · de · arbeitsagentur · 26 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_054 - scope `in_scope` (in-scope)

> AI & Machine Learning Engineer (m/w/d)

- MONTANA Energie-Handel GmbH & Co. KG · AI & Machine Learning Engineer (m/w/d)
- Munich · de · arbeitsagentur · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_055 - scope `in_scope` (in-scope)

> Automotive Security Backend AI Engineer (f/m/x)

- BMW AG · Automotive Security Backend AI Engineer (f/m/x)
- Munich · en · arbeitsagentur · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_056 - scope `in_scope` (in-scope)

> Senior AI / Reinforcement Learning Engineer (m/f/d)

- agilerobotsse · Senior AI / Reinforcement Learning Engineer (m/f/d)
- Munich · en · greenhouse · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_057 - scope `in_scope` (in-scope)

> Wir suchen Dich als

- accu Personalservice GmbH · Engineer, Software AI DevOps (m/w/d)
- Munich · de · arbeitsagentur · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_058 - scope `in_scope` (in-scope)

> Principal Data Scientist (m/f/d)

- AutoScout24 · Principal Data Scientist (m/f/d)
- Munich · en · greenhouse · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_059 - scope `in_scope` (in-scope)

> Associate Applied (AI) Value Engineer (DACH) - Orbit Program

- celonis · Associate Applied (AI) Value Engineer (DACH) - Orbit Program
- Munich · en · greenhouse · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_060 - scope `in_scope` (in-scope)

> Automotive AI Security Engineer (f/m/x)

- BMW AG · Automotive AI Security Engineer (f/m/x)
- Munich · en · arbeitsagentur · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_061 - scope `in_scope` (in-scope)

> AI Forward Deployed Engineer - Germany

- databricks · AI Forward Deployed Engineer - Germany
- Munich · en · greenhouse · 15 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_062 - scope `in_scope` (in-scope)

> Senior IT Engineer (w/m/d) API, AI, Infrastruktur

- Robert Half Deutschland GmbH & Co. KG · Senior IT Engineer (w/m/d) API, AI, Infrastruktur
- Munich · de · arbeitsagentur · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_063 - scope `in_scope` (in-scope)

> AI Process & Agent Solutions Engineer (m/w/d)

- C-P-S Group · AI Process & Agent Solutions Engineer (m/w/d)
- Munich · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_049 - skill `ai-deployment` (disagreement)

> ...Vektordatenbanken Erfahrung in der Entwicklung und Bereitstellung von KI-Agenten und automatisierten Gesprächssystemen (Chatbots/KI-Bots)...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "Bereitstellung von KI-Agenten"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_050 - skill `ai-deployment` (disagreement)

> ...und einem starken Fokus auf Testautomatisierung Du hast bereits LLM-basierte Agenten oder KI-Funktionen entwickelt und produktiv eingesetzt, beispielsweise mit Tool Calling, Retrieval oder...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "Du hast bereits LLM-basierte Agenten oder KI-Funktionen entwickelt und produktiv eingesetzt"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_050 - skill `evaluation` (disagreement)

> ...Cursor oder Codex, entwickelst spezifikationsbasiert und überprüfst KI-generierte Ergebnisse systematisch Du beherrschst automatisierte Tests auf unterschiedlichen...

- A: (did not label this)
- B: `evaluation` · required · raw_text: "überprüfst KI-generierte Ergebnisse systematisch"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_050 - skill `rag` (disagreement)

> ...und produktiv eingesetzt, beispielsweise mit Tool Calling, Retrieval oder mehrstufigen Workflows Du bringst Erfahrung in der...

- A: `rag` · required · raw_text: "Retrieval"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_052 - skill `inference-optimization` (disagreement)

> ...Embeddings und Fine-Tuning • Erfahrung mit Edge AI und Model Optimization, z. B. Quantization, Pruning, ONNX, CUDA/TensorRT oder...

- A: `inference-optimization` · required · raw_text: "Model Optimization"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_053 - skill `ai-ml` (disagreement)

> ...wie ArgoCD oder Flux ### Persönliche Eigenschaften - Ausgeprägtes Interesse an KI-Themen und die Motivation, in diesem dynamischen Feld am Ball zu...

- A: `ai-ml` · nice_to_have · raw_text: "Ausgeprägtes Interesse an KI-Themen"
- B: `ai-ml` · required · raw_text: "Du verstehst sowohl die klassische Backend-Welt als auch KI-Konzepte"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_054 - attribute `degree` (disagreement)

> ...im AI Engineering oder Machine Learning gearbeitet. Ein abgeschlossenes Studium in Informatik, Data Science oder einem verwandten Bereich ist willkommen – ebenso eine vergleichbare Qualifikation durch Praxiserfahrung.✓ Du übernimmst gerne Verantwortung: Du arbeitest...

- A: value="bachelor" · requirement="nice_to_have" · or_equivalent=true · signal="Ein abgeschlossenes Studium in Informatik, Data Science oder einem verwandten Bereich ist willkommen – ebenso eine vergleichbare Qualifikation durch Praxiserfahrung"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Ein abgeschlossenes Studium in Informatik, Data Science oder einem verwandten Bereich ist willkommen – ebenso eine vergleichbare Qualifikation durch Praxiserfahrung."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_054 - skill `ai-deployment` (disagreement)

> ...Du denkst über den Prototyp hinaus: Themen wie Testing, Deployment, Skalierbarkeit, Sicherheit und zuverlässiger...

- A: `ai-deployment` · required · raw_text: "Deployment"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_056 - skill `ai-deployment` (disagreement)

> ...Demonstrated success in sim-to-real transfer and deploying learning-based policies on physical robots - Strong problem-solving skills and the ability to work...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying learning-based policies on physical robots"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_056 - skill `model-development` (disagreement)

> ...simulators (IsaacSim, MuJoCo or equivalent) for large-scale policy training - Strong understanding of control theory, motion...

- A: (did not label this)
- B: `model-development` · required · raw_text: "large-scale policy training"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_059 - skill `machine-learning` (disagreement)

> ...automated text processors. - Good knowledge of Python and common ML libraries (such as LangChain, pandas, pydantic, sklearn, PyTorch) as...

- A: `machine-learning` · required · raw_text: "common ML libraries"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_059 - skill `multi-agent-systems` (disagreement)

> ...like RAG, few shot learning, prompt/context engineering, multi-agent orchestration, multimodal understanding, or fine-tuning that are used to...

- A: (did not label this)
- B: `multi-agent-systems` · required · raw_text: "multi-agent orchestration"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_063 - skill `ai-deployment` (disagreement)

> ...Machine Learning oder AI- Engineering sowie in der Umsetzung produktiver KI-Lösungen. • Erfahrung mit Frameworks wie LangChain, LangGraph,...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "Umsetzung produktiver KI-Lösungen"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_049 - skill `conversational-ai` (uncertain)

> ...in der Entwicklung und Bereitstellung von KI-Agenten und automatisierten Gesprächssystemen (Chatbots/KI-Bots) Grundkenntnisse in DevOps-Methoden, insbesondere...

- A: `conversational-ai` · required · raw_text: "automatisierten Gesprächssystemen (Chatbots/KI-Bots)"
- B: `conversational-ai` · required · raw_text: "automatisierten\nGesprächssystemen (Chatbots/KI-Bots)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 30. golden_049 - skill `llms` (uncertain)

> ...Enthusiast oder Vibe Coder mit Proof Record Erfahrung mit Large Language Model (LLM)-Frameworks (z. B. LangChain, LlamaIndex, Hugging Face) Kenntnisse im...

- A: `llms` · required · raw_text: "Large Language Model (LLM)-Frameworks"
- B: `llms` · required · raw_text: "Large Language Model (LLM)-Frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 31. golden_050 - skill `data-privacy-and-security` (uncertain)

> ...mit und verstehst Anforderungen an Berechtigungen, Datenschutz und Mandantentrennung Du arbeitest regelmäßig mit...

- A: `data-privacy-and-security` · required · raw_text: "Datenschutz"
- B: `data-privacy-and-security` · required · raw_text: "Berechtigungen, Datenschutz und Mandantentrennung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 32. golden_050 - skill `llm-orchestration` (uncertain)

> ...mit Tool Calling, Retrieval oder mehrstufigen Workflows Du bringst Erfahrung in der Modellierung komplexer...

- A: `llm-orchestration` · required · raw_text: "mehrstufigen Workflows"
- B: `llm-orchestration` · required · raw_text: "mehrstufigen Workflows"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 33. golden_051 - skill `agents` (uncertain)

> ...(Azure, AWS, GCP) - Praktische Erfahrung mit LLMs, RAG, Agentic AI, Vektordatenbanken und Orchestrierungsframeworks...

- A: `agents` · required · raw_text: "Agentic AI"
- B: `agents` · required · raw_text: "Agentic AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 34. golden_052 - attribute `degree` (uncertain)

> ...am Standort Unterschleißheim möglich • IHR PROFIL • Erfolgreich abgeschlossenes Studium der Informatik, Künstlichen Intelligenz, Data Science, Robotik, Mathematik, Physik oder einer vergleichbaren Fachrichtung, Promotion erwünscht • Mehrjährige Erfahrung in Machine Learning und Deep...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Erfolgreich abgeschlossenes Studium der Informatik, Künstlichen Intelligenz, Data Science, Robotik, Mathematik, Physik oder einer vergleichbaren Fachrichtung, Promotion erwünscht"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Erfolgreich abgeschlossenes Studium der Informatik, Künstlichen Intelligenz, Data Science, Robotik, Mathematik, Physik oder einer vergleichbaren Fachrichtung, Promotion erwünscht"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 35. golden_052 - attribute `seniority` (uncertain)

> ...mit unseren Teams und Kunden • Fachliche Begleitung und Mentoring innerhalb des Teams sowie aktive Weitergabe von Wissen und Best Practices. •...

- A: value="senior" · basis="inferred" · signal="Mentoring innerhalb des Teams"
- B: value="senior" · basis="inferred" · signal="Fachliche Begleitung und Mentoring innerhalb des Teams"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 36. golden_052 - skill `ai-deployment` (uncertain)

> ...oder vergleichbaren Technologien • Kenntnisse der MLOps und Deployment, z. B. Docker, Kubernetes, MLflow und CI/CD • Azure oder...

- A: `ai-deployment` · required · raw_text: "MLOps und Deployment"
- B: `ai-deployment` · required · raw_text: "Deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 37. golden_052 - skill `deep-learning` (uncertain)

> ...erwünscht • Mehrjährige Erfahrung in Machine Learning und Deep Learning, idealerweise in produktiven Projekten • Fundierte Kenntnisse in Computer Vision, z. B. Object...

- A: `deep-learning` · required · raw_text: "Deep Learning, idealerweise in produktiven Projekten"
- B: `deep-learning` · required · raw_text: "Deep Learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 38. golden_053 - skill `apis` (uncertain)

> ...Enterprise Edition (oder vergleichbares) - Verständnis von REST API-Design und -Implementierung - Hands-on Erfahrung mit Containerisierungstechnologien...

- A: `apis` · required · raw_text: "REST API-Design und -Implementierung"
- B: `apis` · required · raw_text: "REST API-Design und -Implementierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_053 - skill `backend-development` (uncertain)

> ...intensiv in dieses spannende Feld einzuarbeiten. Wenn du solide Backend-Entwicklungsskills hast und die Zukunft der KI-Integration mitgestalten...

- A: `backend-development` · required · raw_text: "solide Backend-Entwicklungsskills"
- B: `backend-development` · required · raw_text: "solide Backend-Entwicklungsskills"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_053 - skill `git` (uncertain)

> ...(AWS, Azure, GCP) - Praxiserfahrung mit CI/CD-Tools (GitLab, GitHub, Jenkins, AWS CodeBuild/CodePipeline, Azure DevOps) **KI...

- A: `git` · required · raw_text: "GitLab, GitHub"
- B: `git` · required · raw_text: "GitHub"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_053 - skill `gitlab-ci` (uncertain)

> ...Cloud-Plattformen (AWS, Azure, GCP) - Praxiserfahrung mit CI/CD-Tools (GitLab, GitHub, Jenkins, AWS CodeBuild/CodePipeline, Azure...

- A: `gitlab-ci` · required · raw_text: "CI/CD-Tools (GitLab"
- B: `gitlab-ci` · required · raw_text: "CI/CD-Tools (GitLab"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_053 - skill `llm-orchestration` (uncertain)

> ...einzuarbeiten - Idealerweise erste Erfahrungen mit Agent-Frameworks oder Orchestrierung - Optional: Kenntnisse in Model Fine-tuning, Prompt...

- A: `llm-orchestration` · nice_to_have · raw_text: "Agent-Frameworks oder Orchestrierung"
- B: `llm-orchestration` · nice_to_have · raw_text: "Idealerweise erste Erfahrungen mit Agent-Frameworks oder Orchestrierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_054 - attribute `seniority` (uncertain)

> ...Softwareentwicklung.✓ Du bringst praktische Erfahrung mit: Idealerweise hast du bereits 3–5 Jahre in der Softwareentwicklung, im AI Engineering oder Machine Learning gearbeitet. Ein abgeschlossenes Studium in Informatik, Data Science...

- A: value="mid" · basis="inferred" · signal="Idealerweise hast du bereits 3–5 Jahre in der Softwareentwicklung, im AI Engineering oder Machine Learning gearbeitet"
- B: value="mid" · basis="inferred" · signal="Idealerweise hast du bereits 3–5 Jahre in der Softwareentwicklung, im AI Engineering oder Machine Learning gearbeitet."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_054 - skill `model-development` (uncertain)

> ...Machine Learning: Du kennst grundlegende ML-Verfahren, Modelltraining und Evaluation und hast idealerweise bereits mit...

- A: `model-development` · required · raw_text: "Modelltraining"
- B: `model-development` · required · raw_text: "Modelltraining"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_054 - skill `software-engineering` (uncertain)

> ...Erfahrung mit APIs, Datenbanken, Softwarearchitektur und der Entwicklung professioneller Softwarelösungen.✓ Du kennst dich mit moderner AI aus: Du hast praktische...

- A: `software-engineering` · required · raw_text: "der Entwicklung professioneller Softwarelösungen"
- B: `software-engineering` · required · raw_text: "Entwicklung professioneller Softwarelösungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_055 - attribute `seniority` (uncertain)

> ...in Computer Science or a comparable IT-related field. - Several years of professional experience in Automotive Cybersecurity. - Strong expertise in...

- A: value="mid" · basis="inferred" · signal="Several years of professional experience"
- B: value="mid" · basis="inferred" · signal="Several years of professional experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_055 - skill `agents` (uncertain)

> ...in Automotive Cybersecurity. - Strong expertise in building, operating, and maintaining agentic AI toolchains using both commercial and open-source technologies. -...

- A: `agents` · required · raw_text: "building, operating, and maintaining agentic AI toolchains"
- B: `agents` · required · raw_text: "agentic AI toolchains"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_055 - skill `cybersecurity` (uncertain)

> ...IT-related field. - Several years of professional experience in Automotive Cybersecurity. - Strong expertise in building, operating, and...

- A: `cybersecurity` · required · raw_text: "experience in Automotive Cybersecurity"
- B: `cybersecurity` · required · raw_text: "Automotive Cybersecurity"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_056 - skill `cpp` (uncertain)

> ...common RL algorithms (PPO, SAC, ...) - Proficiency in Python and/or C++, PyTorch, ONNX, and common RL frameworks (e.g, Stable...

- A: `cpp` · required · raw_text: "Python and/or C++"
- B: `cpp` · required · raw_text: "C++"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_057 - skill `agents` (uncertain)

> ...mit C#/.NET, PowerShell oder TypeScript - Ausgeprägtes Interesse an AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering - Ganzheitliches Denkvermögen,...

- A: `agents` · required · raw_text: "Interesse an AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz"
- B: `agents` · required · raw_text: "Ausgeprägtes Interesse an AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_057 - skill `ai-developer-tooling` (uncertain)

> ...beispielsweise mit C#/.NET, PowerShell oder TypeScript - Ausgeprägtes Interesse an AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering - Ganzheitliches Denkvermögen, hohe Eigenverantwortung und...

- A: `ai-developer-tooling` · required · raw_text: "Ausgeprägtes Interesse an AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering"
- B: `ai-developer-tooling` · required · raw_text: "Ausgeprägtes Interesse an AI-Assistenten und agentischen Workflows sowie Erfahrung mit deren sicherem und praxisorientiertem Einsatz im Software Engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_057 - skill `distributed-systems` (uncertain)

> ...in Softwareentwicklung oder Testautomatisierung für verteilte Softwarelösungen on-premise und in der Cloud - Sehr gute Kenntnisse in...

- A: `distributed-systems` · required · raw_text: "verteilte Softwarelösungen"
- B: `distributed-systems` · required · raw_text: "verteilte Softwarelösungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_059 - skill `agents` (uncertain)

> ...technical Proof of Concept projects - Hands-on experience building agentic systems using LLM orchestration, RAG, function calling, and prompt...

- A: `agents` · nice_to_have · raw_text: "building agentic systems"
- B: `agents` · nice_to_have · raw_text: "building agentic systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_059 - skill `llm-orchestration` (uncertain)

> ...like RAG, few shot learning, prompt/context engineering, multi-agent orchestration, multimodal understanding, or fine-tuning that are used to...

- A: `llm-orchestration` · required · raw_text: "multi-agent orchestration"
- B: `llm-orchestration` · required · raw_text: "multi-agent orchestration"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_060 - attribute `degree` (uncertain)

> ...toolchain performance. What should you bring along? - University degree in Computer Science, Electrical Engineering, or a comparable qualification. - Several years of professional experience in Automotive...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="University degree in Computer Science, Electrical Engineering, or a comparable qualification"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="University degree in Computer Science, Electrical Engineering, or a comparable qualification."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_060 - attribute `seniority` (uncertain)

> ...Electrical Engineering, or a comparable qualification. - Several years of professional experience in Automotive Cybersecurity. - Strong expertise in...

- A: value="mid" · basis="inferred" · signal="Several years of professional experience"
- B: value="mid" · basis="inferred" · signal="Several years of professional experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_061 - attribute `degree` (uncertain)

> ...machine learning deployments on AWS, Azure, or GCP - Graduate degree in a quantitative discipline (Computer Science, Engineering, Statistics, Operations Research, etc.) or equivalent practical experience - Experience communicating and/or teaching technical...

- A: value="master" · requirement="required" · or_equivalent=true · signal="Graduate degree in a quantitative discipline (Computer Science, Engineering, Statistics, Operations Research, etc.) or equivalent practical experience"
- B: value="master" · requirement="required" · or_equivalent=true · signal="Graduate degree in a quantitative discipline (Computer Science, Engineering, Statistics, Operations Research, etc.) or equivalent practical experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_061 - skill `ai-deployment` (uncertain)

> ...such as HuggingFace, LangChain, and DSPy - Expertise in deploying production-grade GenAI applications, including evaluation and optimisations - Extensive...

- A: `ai-deployment` · required · raw_text: "deploying production-grade GenAI applications"
- B: `ai-deployment` · required · raw_text: "deploying production-grade GenAI applications"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_061 - skill `llms` (uncertain)

> ...Own production rollouts of consumer and internally facing GenAI applications - Serve as a trusted technical advisor to customers...

- A: `llms` · required · raw_text: "GenAI applications"
- B: `llms` · required · raw_text: "Experience building GenAI applications"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_061 - skill `machine-learning` (uncertain)

> ...industry data science experience, leveraging common machine learning and data science tools, i.e. pandas, scikit-learn, PyTorch, etc. - Experience...

- A: `machine-learning` · required · raw_text: "machine learning and data science tools"
- B: `machine-learning` · required · raw_text: "common machine learning and data science tools"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_062 - attribute `degree` (uncertain)

> ...und technischen Rollout-Konzepten ## Anforderungen: - Studium oder abgeschlossene Berufsausbildung IT (z.B. Systemintegration, Anwendungsentwicklung, Computer...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Studium oder abgeschlossene Berufsausbildung IT"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Studium oder abgeschlossene Berufsausbildung IT (z.B. Systemintegration, Anwendungsentwicklung, Computer Science)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_062 - skill `ai-ml` (uncertain)

> ...sowie komplexen Systemlandschaften - Gute Kenntnisse AI, GenAI, Automatisierung oder datengetriebenen...

- A: `ai-ml` · required · raw_text: "Gute Kenntnisse AI"
- B: `ai-ml` · required · raw_text: "AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_062 - skill `backend-development` (uncertain)

> ...Know-how im Umgang mit Docker, Power Platform, Backend-Systemen und API-gesteuerten Anwendungen - Erfahrung in der...

- A: `backend-development` · required · raw_text: "Backend-Systemen"
- B: `backend-development` · required · raw_text: "Backend-Systemen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_062 - skill `cloud` (uncertain)

> ...Praxiserfahrung mit MS Azure, Microsoft 365, Entra ID und Cloud-Services - Know-how im Umgang mit Docker, Power Platform,...

- A: `cloud` · required · raw_text: "Cloud-Services"
- B: `cloud` · required · raw_text: "Cloud-Services"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_062 - skill `workflow-automation` (uncertain)

> ...komplexen Systemlandschaften - Gute Kenntnisse AI, GenAI, Automatisierung oder datengetriebenen Anwendungen - Strukturierte,...

- A: `workflow-automation` · required · raw_text: "Automatisierung"
- B: `workflow-automation` · required · raw_text: "Automatisierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_063 - attribute `seniority` (uncertain)

> ...oder einer vergleichbaren Fachrichtung. • Mindestens zwei Jahre Erfahrung in Data Science, Machine Learning oder AI- Engineering...

- A: value="junior" · basis="inferred" · signal="Mindestens zwei Jahre Erfahrung"
- B: value="junior" · basis="inferred" · signal="Mindestens zwei Jahre Erfahrung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_063 - skill `agents` (uncertain)

> ...oder PyTorch sowie Kenntnisse in Generativer KI, NLP oder agentenbasierten KI-Systemen. • Gute Kenntnisse in Python und SQL; idealerweise...

- A: `agents` · required · raw_text: "agentenbasierten KI-Systemen"
- B: `agents` · required · raw_text: "agentenbasierten KI-Systemen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_049 - attribute `degree` (spot-check)

> ...Bereitstellung von Best Practices WAS SIE MITBRINGEN Abgeschlossenes wissenschaftliches Hochschulstudium (min. Bachelor) in einem MINT-Fach, oder vergleichbare Qualifikation als Quereinsteiger, Tech Enthusiast oder Vibe Coder mit Proof Record...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossenes wissenschaftliches Hochschulstudium (min. Bachelor) in einem MINT-Fach, oder vergleichbare Qualifikation als Quereinsteiger"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 69. golden_049 - skill `agents` (spot-check)

> ...Erfahrung in der Entwicklung und Bereitstellung von KI-Agenten und automatisierten Gesprächssystemen (Chatbots/KI-Bots)...

- agreed label: `agents` · required · raw_text: "KI-Agenten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 70. golden_049 - skill `langchain` (spot-check)

> ...Erfahrung mit Large Language Model (LLM)-Frameworks (z. B. LangChain, LlamaIndex, Hugging Face) Kenntnisse im Aufbau von...

- agreed label: `langchain` · required · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 71. golden_050 - attribute `german` (spot-check)

> ...und qualitätsorientiert und verfügst über Deutschkenntnisse auf C2-Niveau sowie Englischkenntnisse auf C1-Niveau Zusätzlich...

- agreed label: value="required" · basis="stated" · signal="Deutschkenntnisse auf C2-Niveau"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 72. golden_050 - attribute `seniority` (spot-check)

> ...aktiv ins Team ein Profil Du hast mindestens 4 Jahre Erfahrung in der professionellen Softwareentwicklung, idealerweise...

- agreed label: value="mid" · basis="inferred" · signal="mindestens 4 Jahre Erfahrung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 73. golden_050 - skill `ai-developer-tooling` (spot-check)

> ...und Mandantentrennung Du arbeitest regelmäßig mit AI-Coding-Tools wie Claude Code, Cursor oder Codex, entwickelst...

- agreed label: `ai-developer-tooling` · required · raw_text: "AI-Coding-Tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 74. golden_050 - skill `claude-code` (spot-check)

> ...Du arbeitest regelmäßig mit AI-Coding-Tools wie Claude Code, Cursor oder Codex, entwickelst spezifikationsbasiert...

- agreed label: `claude-code` · required · raw_text: "Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 75. golden_050 - skill `cursor` (spot-check)

> ...arbeitest regelmäßig mit AI-Coding-Tools wie Claude Code, Cursor oder Codex, entwickelst spezifikationsbasiert...

- agreed label: `cursor` · required · raw_text: "Cursor"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 76. golden_050 - skill `data-modeling` (spot-check)

> ...oder mehrstufigen Workflows Du bringst Erfahrung in der Modellierung komplexer Geschäftsdaten mit und verstehst Anforderungen an Berechtigungen,...

- agreed label: `data-modeling` · required · raw_text: "Modellierung komplexer Geschäftsdaten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 77. golden_050 - skill `forecasting` (spot-check)

> ...oder ERP-Software, XRechnung, ZUGFeRD oder Forecasting Wir bieten Du arbeitest flexibel im Home-Office, bis zu...

- agreed label: `forecasting` · nice_to_have · raw_text: "Forecasting"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 78. golden_050 - skill `langgraph` (spot-check)

> ...Agenten-Frameworks und Schnittstellen wie MCP, A2A oder LangGraph aus und bringst Verständnis für...

- agreed label: `langgraph` · required · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 79. golden_050 - skill `software-engineering` (spot-check)

> ...ein Profil Du hast mindestens 4 Jahre Erfahrung in der professionellen Softwareentwicklung, idealerweise mit produktiven Cloud- oder SaaS-Anwendungen...

- agreed label: `software-engineering` · required · raw_text: "professionellen Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 80. golden_051 - attribute `german` (spot-check)

> ...Ausgeprägte Beratungskompetenz, Workshop-Leitung - Fließend in Deutsch und Englisch Wir wertschätzen Vielfalt und begrüßen daher alle...

- agreed label: value="required" · basis="stated" · signal="Fließend in Deutsch und Englisch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 81. golden_051 - attribute `seniority` (spot-check)

> Senior AI Engineer / AI Architect (all gender) **Wir sind die Gestalter von...

- agreed label: value="senior" · basis="stated" · signal="Senior AI Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 82. golden_051 - skill `ai-ml` (spot-check)

> ...**Erfahrung**: - Relevante Praxis in Softwareentwicklung, AI/ML oder Generative AI - Fundierte Kenntnisse in Python,...

- agreed label: `ai-ml` · required · raw_text: "AI/ML"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 83. golden_051 - skill `llm-orchestration` (spot-check)

> ...Erfahrung mit LLMs, RAG, Agentic AI, Vektordatenbanken und Orchestrierungsframeworks (LangGraph, CrewAI, LlamaIndex) - MLOps/LLMOps, CI/CD,...

- agreed label: `llm-orchestration` · required · raw_text: "Orchestrierungsframeworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_051 - skill `python` (spot-check)

> ...AI/ML oder Generative AI - Fundierte Kenntnisse in Python, Software-Architektur, Cloud-Plattformen (Azure, AWS,...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_051 - skill `software-engineering` (spot-check)

> ...oder vergleichbar - **Erfahrung**: - Relevante Praxis in Softwareentwicklung, AI/ML oder Generative AI - Fundierte Kenntnisse in...

- agreed label: `software-engineering` · required · raw_text: "Praxis in Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_051 - skill `testing` (spot-check)

> ...LlamaIndex) - MLOps/LLMOps, CI/CD, Kubernetes, Git und automatisiertes Testing. - **Soft Skills**: - Ausgeprägte Beratungskompetenz,...

- agreed label: `testing` · required · raw_text: "automatisiertes Testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_052 - skill `ci-cd` (spot-check)

> ...MLOps und Deployment, z. B. Docker, Kubernetes, MLflow und CI/CD • Azure oder AWS sowie On-Premise- und hybrides...

- agreed label: `ci-cd` · required · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_052 - skill `computer-vision` (spot-check)

> ...Deep Learning, idealerweise in produktiven Projekten • Fundierte Kenntnisse in Computer Vision, z. B. Object Detection, Segmentation, Tracking, Vision...

- agreed label: `computer-vision` · required · raw_text: "Fundierte Kenntnisse in Computer Vision"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_052 - skill `cuda` (spot-check)

> ...und Model Optimization, z. B. Quantization, Pruning, ONNX, CUDA/TensorRT oder vergleichbaren Technologien • Kenntnisse...

- agreed label: `cuda` · required · raw_text: "CUDA"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_052 - skill `embeddings` (spot-check)

> ...Generative AI, z. B. LLMs, Vision-Language Models, RAG, Embeddings und Fine-Tuning • Erfahrung mit Edge AI und Model...

- agreed label: `embeddings` · required · raw_text: "Embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_052 - skill `machine-learning` (spot-check)

> ...Fachrichtung, Promotion erwünscht • Mehrjährige Erfahrung in Machine Learning und Deep Learning, idealerweise in produktiven...

- agreed label: `machine-learning` · required · raw_text: "Erfahrung in Machine Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_052 - skill `mlops` (spot-check)

> ...ONNX, CUDA/TensorRT oder vergleichbaren Technologien • Kenntnisse der MLOps und Deployment, z. B. Docker, Kubernetes, MLflow und...

- agreed label: `mlops` · required · raw_text: "Kenntnisse der MLOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_052 - skill `pytorch` (spot-check)

> ...und hybrides Infrastrukturen Wissen • Sehr gute Python, PyTorch/TensorFlow und OpenCV Kenntnisse • Sehr gutes...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_052 - skill `rag` (spot-check)

> ...und Generative AI ein, bewerten neue Technologien und übertragen diese in robuste, skalierbare Lösungen. Durch Ihre...

- agreed label: `rag` · required · raw_text: "RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_052 - skill `software-engineering` (spot-check)

> ...PyTorch/TensorFlow und OpenCV Kenntnisse • Sehr gutes Software-Engineering Know how mit Git, Linux und Testing; C++ • Idealerweise Erfahrung...

- agreed label: `software-engineering` · required · raw_text: "Software-Engineering Know how"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_052 - skill `tensorflow` (spot-check)

> ...Infrastrukturen Wissen • Sehr gute Python, PyTorch/TensorFlow und OpenCV Kenntnisse • Sehr gutes Software-Engineering...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_052 - skill `testing` (spot-check)

> ...gutes Software-Engineering Know how mit Git, Linux und Testing; C++ • Idealerweise Erfahrung im wissenschaftlichen...

- agreed label: `testing` · required · raw_text: "Testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_053 - attribute `degree` (spot-check)

> Cloud Software Engineer mit KI-Fokus (m/w/d)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_053 - attribute `german` (spot-check)

> Cloud Software Engineer mit KI-Fokus (m/w/d)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_053 - skill `azure` (spot-check)

> ...Kenntnisse in Kubernetes/OpenShift und Cloud-Plattformen (AWS, Azure, GCP) - Praxiserfahrung mit CI/CD-Tools (GitLab, GitHub,...

- agreed label: `azure` · required · raw_text: "AWS, Azure, GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_053 - skill `ci-cd` (spot-check)

> ...Cloud-Plattformen (AWS, Azure, GCP) - Praxiserfahrung mit CI/CD-Tools (GitLab, GitHub, Jenkins, AWS CodeBuild/CodePipeline,...

- agreed label: `ci-cd` · required · raw_text: "CI/CD-Tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_053 - skill `gitops` (spot-check)

> ...(Pinecone, Weaviate, Qdrant, ChromaDB) - Verständnis von GitOps-Prinzipien und Tools wie ArgoCD oder Flux ### Persönliche...

- agreed label: `gitops` · nice_to_have · raw_text: "GitOps-Prinzipien"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_053 - skill `langchain` (spot-check)

> ...evolvierende KI-Technologien einzuarbeiten **Bonus:** - Erfahrung mit LangChain, LlamaIndex, LangChain4J oder vergleichbaren Frameworks -...

- agreed label: `langchain` · nice_to_have · raw_text: "Erfahrung mit LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_053 - skill `llamaindex` (spot-check)

> ...einzuarbeiten **Bonus:** - Erfahrung mit LangChain, LlamaIndex, LangChain4J oder vergleichbaren Frameworks - Kenntnisse...

- agreed label: `llamaindex` · nice_to_have · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_053 - skill `prompt-engineering` (spot-check)

> ...Optional: Kenntnisse in Model Fine-tuning, Prompt Engineering oder MLOps - Bereitschaft, sich kontinuierlich in schnell...

- agreed label: `prompt-engineering` · nice_to_have · raw_text: "Prompt Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_053 - skill `vector-databases` (spot-check)

> ...LlamaIndex, LangChain4J oder vergleichbaren Frameworks - Kenntnisse in Vektordatenbanken (Pinecone, Weaviate, Qdrant, ChromaDB) - Verständnis von...

- agreed label: `vector-databases` · nice_to_have · raw_text: "Kenntnisse in Vektordatenbanken"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_054 - attribute `german` (spot-check)

> ...technische Zusammenhänge verständlich vermitteln und verfügst über gute Deutsch- und Englischkenntnisse. Attraktive Vorteile:✓ Gestalten statt nur umsetzen:...

- agreed label: value="required" · basis="stated" · signal="verfügst über gute Deutsch- und Englischkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_054 - skill `agents` (spot-check)

> ...von AI-Modellen. Konzepte wie Prompt Engineering, RAG oder AI Agents sind dir vertraut.✓ Du verstehst Machine Learning: Du kennst grundlegende...

- agreed label: `agents` · required · raw_text: "RAG oder AI Agents sind dir vertraut"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_054 - skill `python` (spot-check)

> ...Voraussetzungen:✓ Du bist technisch stark: Python gehört zu deinem Werkzeugkasten. Du hast Erfahrung mit APIs, Datenbanken,...

- agreed label: `python` · required · raw_text: "Python gehört zu deinem Werkzeugkasten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_054 - skill `rag` (spot-check)

> ...AI und der Integration von AI-Modellen. Konzepte wie Prompt Engineering, RAG oder AI Agents sind dir vertraut.✓ Du verstehst Machine...

- agreed label: `rag` · required · raw_text: "Prompt Engineering, RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_054 - skill `software-architecture` (spot-check)

> ...Werkzeugkasten. Du hast Erfahrung mit APIs, Datenbanken, Softwarearchitektur und der Entwicklung professioneller Softwarelösungen.✓ Du...

- agreed label: `software-architecture` · required · raw_text: "Softwarearchitektur"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_054 - skill `testing` (spot-check)

> ...Du denkst über den Prototyp hinaus: Themen wie Testing, Deployment, Skalierbarkeit, Sicherheit und zuverlässiger...

- agreed label: `testing` · required · raw_text: "Testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_055 - attribute `degree` (spot-check)

> ...future analysis cycles. What should you bring along? - University degree in Computer Science or a comparable IT-related field. - Several years of professional experience in Automotive...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="University degree in Computer Science or a comparable IT-related field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_055 - skill `aws` (spot-check)

> ...tools). - Hands-on experience with cloud platforms (AWS/Azure), containerization and orchestration technologies...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_055 - skill `azure` (spot-check)

> ...tools). - Hands-on experience with cloud platforms (AWS/Azure), containerization and orchestration technologies...

- agreed label: `azure` · required · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_055 - skill `containerization` (spot-check)

> ...Hands-on experience with cloud platforms (AWS/Azure), containerization and orchestration technologies (Docker/Kubernetes), as well as CI/CD and...

- agreed label: `containerization` · required · raw_text: "containerization and orchestration technologies"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_055 - skill `gitlab-ci` (spot-check)

> ...Infrastructure-as-Code tools (e.g., Terraform, Ansible, GitHub Actions/GitLab CI). - Business-fluent German and English language...

- agreed label: `gitlab-ci` · required · raw_text: "GitHub Actions/GitLab CI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_055 - skill `terraform` (spot-check)

> ...technologies (Docker/Kubernetes), as well as CI/CD and Infrastructure-as-Code tools (e.g., Terraform, Ansible, GitHub Actions/GitLab CI). - Business-fluent...

- agreed label: `terraform` · required · raw_text: "Infrastructure-as-Code tools (e.g., Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_056 - attribute `degree` (spot-check)

> ...on open-ended, evolving tasks Essential Skills - Master’s or PhD in robotics, computer science, engineering, or a related field - Proven experience (5+ years) applying RL or IL in...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s or PhD in robotics, computer science, engineering, or a related field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_056 - attribute `german` (spot-check)

> Senior AI / Reinforcement Learning Engineer (m/f/d)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_056 - skill `onnx` (spot-check)

> ...SAC, ...) - Proficiency in Python and/or C++, PyTorch, ONNX, and common RL frameworks (e.g, Stable Baselines 3,...

- agreed label: `onnx` · required · raw_text: "ONNX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_056 - skill `pytorch` (spot-check)

> ...(PPO, SAC, ...) - Proficiency in Python and/or C++, PyTorch, ONNX, and common RL frameworks (e.g, Stable Baselines 3,...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_057 - attribute `seniority` (spot-check)

> Wir suchen Dich als

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_057 - skill `devsecops` (spot-check)

> ...Qualifikation mit einschlägiger Berufserfahrung - Fundierte Erfahrung in DevSecOps, CI/CD, Infrastructure as Code und Container, in...

- agreed label: `devsecops` · required · raw_text: "Fundierte Erfahrung in DevSecOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_057 - skill `software-engineering` (spot-check)

> ...in DevSecOps, CI/CD, Infrastructure as Code und Container, in Softwareentwicklung oder Testautomatisierung für verteilte Softwarelösungen...

- agreed label: `software-engineering` · required · raw_text: "in Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_057 - skill `typescript` (spot-check)

> ...Programmierung und Scripting, beispielsweise mit C#/.NET, PowerShell oder TypeScript - Ausgeprägtes Interesse an AI-Assistenten und agentischen...

- agreed label: `typescript` · required · raw_text: "PowerShell oder TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_058 - attribute `german` (spot-check)

> Principal Data Scientist (m/f/d)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_058 - skill `ai-ml` (spot-check)

> ...years of experience in data science, machine learning, or applied AI - strong hands-on skills in Python, SQL, and common ML...

- agreed label: `ai-ml` · required · raw_text: "applied AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_058 - skill `python` (spot-check)

> ...in data science, machine learning, or applied AI - strong hands-on skills in Python, SQL, and common ML frameworks - proven experience with...

- agreed label: `python` · required · raw_text: "hands-on skills in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_059 - attribute `german` (spot-check)

> ...on deadlines. - Excellent communication skills and fluency in German and English (must). - Foundational business acumen and domain...

- agreed label: value="required" · basis="stated" · signal="fluency in German and English (must)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_059 - skill `fine-tuning` (spot-check)

> ...multi-agent orchestration, multimodal understanding, or fine-tuning that are used to build high-impact use cases like...

- agreed label: `fine-tuning` · required · raw_text: "fine-tuning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_059 - skill `llms` (spot-check)

> ...of business and technology. - Understanding of generative AI techniques like RAG, few shot learning, prompt/context engineering,...

- agreed label: `llms` · required · raw_text: "generative AI techniques"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_059 - skill `python` (spot-check)

> ...intelligent chatbots and automated text processors. - Good knowledge of Python and common ML libraries (such as LangChain, pandas,...

- agreed label: `python` · required · raw_text: "Good knowledge of Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_059 - skill `scikit-learn` (spot-check)

> ...common ML libraries (such as LangChain, pandas, pydantic, sklearn, PyTorch) as well as data engineering tools and...

- agreed label: `scikit-learn` · required · raw_text: "sklearn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_061 - skill `apache-spark` (spot-check)

> ...Experience using the Databricks Intelligence Platform and Apache Spark™ to process large-scale distributed datasets - Willing to...

- agreed label: `apache-spark` · nice_to_have · raw_text: "Apache Spark™"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_061 - skill `aws` (spot-check)

> ...building production-grade machine learning deployments on AWS, Azure, or GCP - Graduate degree in a quantitative...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_061 - skill `data-science` (spot-check)

> ...and optimisations - Extensive years of hands-on industry data science experience, leveraging common machine learning and data science...

- agreed label: `data-science` · required · raw_text: "data science experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_061 - skill `databricks` (spot-check)

> ...learning, and driving business value through AI - [Preferred] Experience using the Databricks Intelligence Platform and Apache Spark™ to process large-scale distributed...

- agreed label: `databricks` · nice_to_have · raw_text: "[Preferred] Experience using the Databricks Intelligence Platform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_061 - skill `gcp` (spot-check)

> ...machine learning deployments on AWS, Azure, or GCP - Graduate degree in a quantitative discipline (Computer...

- agreed label: `gcp` · required · raw_text: "GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_062 - attribute `seniority` (spot-check)

> Senior IT Engineer (w/m/d) API, AI, Infrastruktur Robert Half gehört zu den...

- agreed label: value="senior" · basis="stated" · signal="Senior IT Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_062 - skill `docker` (spot-check)

> ...Microsoft 365, Entra ID und Cloud-Services - Know-how im Umgang mit Docker, Power Platform, Backend-Systemen und API-gesteuerten...

- agreed label: `docker` · required · raw_text: "Umgang mit Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_063 - attribute `degree` (spot-check)

> ...Inhalte. Diese Qualifikationen solltest Du mitbringen • Abgeschlossenes Studium der Informatik, Data Science, Wirtschaftsinformatik oder einer vergleichbaren Fachrichtung. • Mindestens zwei Jahre Erfahrung in Data Science,...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="Abgeschlossenes Studium der Informatik, Data Science, Wirtschaftsinformatik oder einer vergleichbaren Fachrichtung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_063 - attribute `german` (spot-check)

> ...auf Niveau C1 oder C2, (Projektsprache ist Englisch); Deutschkenntnisse auf mindestens B12 Niveau. Gestalten Sie mit uns die nächste Generation...

- agreed label: value="required" · basis="stated" · signal="Deutschkenntnisse auf mindestens B12 Niveau"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_063 - skill `data-science` (spot-check)

> ...einer vergleichbaren Fachrichtung. • Mindestens zwei Jahre Erfahrung in Data Science, Machine Learning oder AI- Engineering sowie in der...

- agreed label: `data-science` · required · raw_text: "Erfahrung in Data Science"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_063 - skill `llms` (spot-check)

> ...LangGraph, LlamaIndex oder PyTorch sowie Kenntnisse in Generativer KI, NLP oder agentenbasierten KI-Systemen. • Gute Kenntnisse...

- agreed label: `llms` · required · raw_text: "Generativer KI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_063 - skill `machine-learning` (spot-check)

> ...Mindestens zwei Jahre Erfahrung in Data Science, Machine Learning oder AI- Engineering sowie in der Umsetzung produktiver...

- agreed label: `machine-learning` · required · raw_text: "Machine Learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_063 - skill `python` (spot-check)

> ...oder agentenbasierten KI-Systemen. • Gute Kenntnisse in Python und SQL; idealerweise Erfahrung mit...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
