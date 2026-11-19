# Review queue - 20261108T183407Z_label

135 items from 13 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261108T183407Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 172 accepted labels,
seed 0) of labels A and B already agreed on. They measure the error rate that
agreement alone cannot: two labelers can agree and both be wrong. They print the posting
excerpt and the agreed label only - no `A:`/`B:` lines - so you check the label against the
posting rather than against the labelers, who by construction both said the same thing.

The first 13 items ask whether each posting belongs in the held-out set at all.
They come pre-answered `yes`, so leaving them alone keeps every posting. Answer `no <why>`
and that posting is written to `evals/goldens/excluded.json` with your reason instead of
becoming a Golden, and neither this script nor `new_goldens.py` will pick it again. Use it
for a posting that got past the title and city filters but is not the job market we
measure - a marketing role, a listing in the wrong field. The rest of that posting's items
are then ignored, so you can answer `no` and skip them.

## 1. golden_121 - scope `in_scope` (in-scope)

> Data & AI Engineer (m/w/d)

- Fitness First Germany GmbH · Data & AI Engineer (m/w/d)
- Frankfurt · de · arbeitsagentur · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_122 - scope `in_scope` (in-scope)

> Senior AI Voicebot & Automation Engineer (all gender)

- ALTEN GmbH München · Senior AI Voicebot & Automation Engineer (all gender)
- Frankfurt · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_123 - scope `in_scope` (in-scope)

> AI Engineer (w|m|d)

- BridgingIT GmbH · AI Engineer (w|m|d)
- Frankfurt · de · arbeitsagentur · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_124 - scope `in_scope` (in-scope)

> (Senior) AI-Native Software Engineer / Architect Node.js/TypeScript (m/w/d), Frankfurt am Main

- Institutional Investment Group · (Senior) AI-Native Software Engineer / Architect Node.js/TypeScript (m/w/d), Frankfurt am Main
- Frankfurt · de · arbeitsagentur · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_125 - scope `in_scope` (in-scope)

> Wir suchen eine/n engagierte/n KI / AI-Engineer (m/w/d) zur Verstärkung unseres IT-Teams. In dieser Position sind Sie verantwortlich für die

- NEXALL · KI / AI-Engineer (m/w/d)
- Frankfurt · de · arbeitsagentur · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_126 - scope `in_scope` (in-scope)

> AI Engineer / KI-Entwickler (m/w/d)

- Finanz Informatik GmbH & Co. KG · AI Engineer / KI-Entwickler (m/w/d)
- Frankfurt · de · arbeitsagentur · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_127 - scope `in_scope` (in-scope)

> AI & Automation Engineer – Life Sciences (all gender)

- ALTEN GmbH München · AI & Automation Engineer – Life Sciences (all gender)
- Frankfurt · de · arbeitsagentur · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_128 - scope `in_scope` (in-scope)

> AI Innovation Engineer, Deutsche Borse Group, Google Cloud

- Google Germany GmbH · AI Innovation Engineer, Deutsche Borse Group, Google Cloud
- Frankfurt · en · arbeitsagentur · 20 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_129 - scope `in_scope` (in-scope)

> AI Inference Engineer (all genders)

- EXXETA AG · AI Inference Engineer (all genders)
- Frankfurt · en · arbeitsagentur · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_130 - scope `in_scope` (in-scope)

> Agentic AI Software Engineer (m/w/d) | Frankfurt | 80% Remote | JBA15245

- freelance.de · Agentic AI Software Engineer (m/w/d) | Frankfurt | 80% Remote | JBA15245
- Frankfurt · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_131 - scope `in_scope` (in-scope)

> #15245 Agentic AI Software Engineer (m/w/d)

- Constaff GmbH · #15245 Agentic AI Software Engineer (m/w/d)
- Frankfurt · de · arbeitsagentur · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_132 - scope `in_scope` (in-scope)

> AI Innovation Engineer, Google Cloud

- Google Germany GmbH · AI Innovation Engineer, Google Cloud
- Frankfurt · en · arbeitsagentur · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_133 - scope `in_scope` (in-scope)

> Für den Standort Frankfurt am Main suchen wir:

- Guldberg GmbH · Plattform AI Engineer (m/w/d)
- Frankfurt · de · arbeitsagentur · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_121 - skill `ai-ml` (disagreement)

> ...Du arbeitest mit aktuellen Cloud-, Data- und AI-Technologien – unter anderem mit Snowflake, Python und modernen...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI-Technologien"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 15. golden_123 - attribute `seniority` (disagreement)

> ...erfolgreich abgeschlossen und es bildet die Basis deiner mehrjährigen Berufserfahrung. - Du bringst praxiserprobte Programmierkenntnisse in...

- A: value="mid" · basis="inferred" · signal="mehrjährigen Berufserfahrung"
- B: value=null · basis=null · signal=null

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 16. golden_124 - skill `cloud` (disagreement)

> ...Sicherheitslücken und Logikfehler. Lernbereitschaft: Du hast Lust, deine Node.js/TypeScript -Komfortzone zu verlassen und dich von der KI in neue Tech-Stacks (Cloud Native, Python Data Services etc.) begleiten zu lassen. Warum...

- A: `cloud` · nice_to_have · raw_text: "Du hast Lust, deine Node.js/TypeScript -Komfortzone zu verlassen und dich von der KI in neue Tech-Stacks (Cloud Native"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 17. golden_124 - skill `cybersecurity` (disagreement)

> ...Kritischer Kurator: Du vertraust der KI nicht blind. Dein Code-Review-Blick ist geschärft für Halluzinationen, Sicherheitslücken und Logikfehler. Lernbereitschaft: Du hast Lust, deine Node.js/TypeScript...

- A: (did not label this)
- B: `cybersecurity` · required · raw_text: "Dein Code-Review-Blick ist geschärft für Halluzinationen, Sicherheitslücken und Logikfehler."

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 18. golden_124 - skill `full-stack-development` (disagreement)

> ...sofort - egal ob von einem Menschen oder einer KI. Modernes Web Development & Container: Erfahrung mit React sowie Docker und...

- A: (did not label this)
- B: `full-stack-development` · required · raw_text: "Modernes Web Development"

Options: `A` / `B` / `both` / `drop`

DECISION: drop

## 19. golden_124 - skill `software-architecture` (disagreement)

> ...so strukturieren, dass eine KI sie fehlerfrei umsetzt. Architektur vor Syntax: Du denkst in Systemen, Schnittstellen und Datenflüssen. Die Programmiersprache ist für dich nur ein Werkzeug, das...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "Architektur vor Syntax: Du denkst in Systemen, Schnittstellen und Datenflüssen."

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 20. golden_125 - skill `sql` (disagreement)

> ...Umgang mit VPN-Technologien sowie Shell Scripting (Bash), T-SQL oder Python ist wünschenswert - Kenntnisse in JavaScript,...

- A: `sql` · nice_to_have · raw_text: "T-SQL"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 21. golden_128 - skill `vertex-ai` (disagreement)

> ...utilizing frameworks (e.g., LangChain, CrewAI, or Vertex AI Agent Builder) and vector databases. Preferred...

- A: `vertex-ai` · required · raw_text: "Vertex AI Agent Builder"
- B: `vertex-ai` · nice_to_have · raw_text: "Vertex AI,"

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 22. golden_132 - skill `data-privacy-and-security` (disagreement)

> ...with FSI regulatory practices and data residency, encryption at rest/transit (CMEK), and "explainable AI" requirements in banking. Experience...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "encryption at rest/transit (CMEK)"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 23. golden_132 - skill `vertex-ai` (disagreement)

> ...utilizing frameworks (e.g., LangChain, CrewAI, or Vertex AI Agent Builder) and vector databases. Experience with one of the...

- A: `vertex-ai` · required · raw_text: "Vertex AI Agent Builder"
- B: `vertex-ai` · nice_to_have · raw_text: "Experience in BigQuery, Vertex AI, Dataflow, and Pub/Sub"

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 24. golden_133 - skill `aws-bedrock` (disagreement)

> ...idealerweise im SAFe-Umfeld. - Kenntnisse in AWS Bedrock AgentCore, Microsoft Foundry Agents Service und Microsoft Copilot...

- A: `aws-bedrock` · nice_to_have · raw_text: "AWS Bedrock AgentCore"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 25. golden_133 - skill `azure-ai-foundry` (disagreement)

> ...im SAFe-Umfeld. - Kenntnisse in AWS Bedrock AgentCore, Microsoft Foundry Agents Service und Microsoft Copilot Studio von Vorteil. - Erfahrung im...

- A: `azure-ai-foundry` · nice_to_have · raw_text: "Microsoft Foundry Agents Service"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 26. golden_133 - skill `hallucination-detection` (disagreement)

> ...Orchestrierung, Guardrails, Prompt Injection, Evaluation, Halluzinationen und Kosten je Token. - Erfahrung darin, Grenzen und...

- A: `hallucination-detection` · required · raw_text: "Halluzinationen"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 27. golden_121 - skill `cloud` (uncertain)

> ...Moderner Technologie-Stack: Du arbeitest mit aktuellen Cloud-, Data- und AI-Technologien – unter anderem mit Snowflake, Python und modernen...

- A: `cloud` · required · raw_text: "aktuellen Cloud-, Data- und AI-Technologien"
- B: `cloud` · required · raw_text: "Cloud-, Data- und AI-Technologien"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 28. golden_121 - skill `python` (uncertain)

> ...Data- und AI-Technologien – unter anderem mit Snowflake, Python und modernen Engineering-Werkzeugen.✓ Individueller...

- A: `python` · required · raw_text: "Python"
- B: `python` · required · raw_text: "Python"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 29. golden_121 - skill `snowflake` (uncertain)

> ...mit aktuellen Cloud-, Data- und AI-Technologien – unter anderem mit Snowflake, Python und modernen Engineering-Werkzeugen.✓...

- A: `snowflake` · required · raw_text: "unter anderem mit Snowflake"
- B: `snowflake` · required · raw_text: "Snowflake"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 30. golden_122 - skill `cloud` (uncertain)

> ...hast Kenntnisse in Microsoft Azure und cloud-nativen Architekturen - bringst idealerweise Erfahrung mit TTS/STT oder...

- A: `cloud` · required · raw_text: "cloud-nativen Architekturen"
- B: `cloud` · required · raw_text: "cloud-nativen Architekturen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 31. golden_123 - skill `ai-ml` (uncertain)

> ...Classification Models und Entity Extraction. - Mit KI-Konzepten und/oder Verfahren des maschinellen Lernens kennst du dich...

- A: `ai-ml` · required · raw_text: "KI-Konzepten"
- B: `ai-ml` · required · raw_text: "KI-Konzepten"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 32. golden_123 - skill `llm-guardrails` (uncertain)

> ...Embeddings, Retrieval Augmented Generation, Re-ranking, Guardrails, Clustering, Classification Models und Entity...

- A: `llm-guardrails` · required · raw_text: "Guardrails"
- B: `llm-guardrails` · required · raw_text: "Guardrails"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 33. golden_123 - skill `nlp` (uncertain)

> ...Guardrails, Clustering, Classification Models und Entity Extraction. - Mit KI-Konzepten und/oder Verfahren des maschinellen...

- A: `nlp` · required · raw_text: "Entity Extraction"
- B: `nlp` · required · raw_text: "Entity Extraction"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 34. golden_124 - skill `backend-development` (uncertain)

> ...Tiefgreifende Node.js /TypeScript DNA: Du hast mehrjährige Erfahrung mit JavaScript/TypeScript (inkl. Node.js im Backend) und verstehst, was unter der Haube passiert. Du hast ein...

- A: `backend-development` · required · raw_text: "Erfahrung mit JavaScript/TypeScript (inkl. Node.js im Backend)"
- B: `backend-development` · required · raw_text: "Node.js im Backend"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 35. golden_124 - skill `containerization` (uncertain)

> ...sofort - egal ob von einem Menschen oder einer KI. Modernes Web Development & Container: Erfahrung mit React sowie Docker und Kubernetes. Du...

- A: `containerization` · required · raw_text: "Modernes Web Development & Container"
- B: `containerization` · required · raw_text: "Modernes Web Development & Container"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: {"raw_text": "Container"}

## 36. golden_124 - skill `distributed-systems` (uncertain)

> ...mit React sowie Docker und Kubernetes. Du weißt, wie moderne verteilte Anwendungen laufen. DevOps Praktiker: CI/CD (z.B. GitLab, Jenkins)...

- A: `distributed-systems` · required · raw_text: "moderne verteilte Anwendungen"
- B: `distributed-systems` · required · raw_text: "Du weißt, wie moderne verteilte Anwendungen laufen."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 37. golden_124 - skill `hallucination-detection` (uncertain)

> ...vertraust der KI nicht blind. Dein Code-Review-Blick ist geschärft für Halluzinationen, Sicherheitslücken und Logikfehler. Lernbereitschaft: Du...

- A: `hallucination-detection` · required · raw_text: "geschärft für Halluzinationen"
- B: `hallucination-detection` · required · raw_text: "Dein Code-Review-Blick ist geschärft für Halluzinationen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 38. golden_125 - attribute `degree` (uncertain)

> ...IT-Systemintegrator **Qualifikationen:** - Abgeschlossene Ausbildung oder Studium im Bereich Informatik oder eine vergleichbare Qualifikation - Fundierte Kenntnisse in der Systemadministration,...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossene Ausbildung oder Studium im Bereich Informatik oder eine vergleichbare Qualifikation"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossene Ausbildung oder Studium im Bereich Informatik oder eine vergleichbare Qualifikation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 39. golden_125 - skill `cybersecurity` (uncertain)

> ...von Vorteil - Sicherer Umgang mit Netzwerkprotokollen und Sicherheitsstandards - Teamfähigkeit, Kommunikationsstärke und...

- A: `cybersecurity` · required · raw_text: "Sicherheitsstandards"
- B: `cybersecurity` · required · raw_text: "Sicherheitsstandards"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 40. golden_125 - skill `networking` (uncertain)

> ...Arbeitsmethoden sind von Vorteil - Sicherer Umgang mit Netzwerkprotokollen und Sicherheitsstandards - Teamfähigkeit,...

- A: `networking` · required · raw_text: "Netzwerkprotokollen"
- B: `networking` · required · raw_text: "Netzwerkprotokollen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 41. golden_126 - skill `software-engineering` (uncertain)

> ...Git-basierter Softwareentwicklung. - Grundverständnis von Software-Engineering-Prinzipien (Testing, CI/CD). - Ausgeprägte kommunikative Stärken...

- A: `software-engineering` · required · raw_text: "Software-Engineering-Prinzipien"
- B: `software-engineering` · required · raw_text: "Softwareentwicklung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 42. golden_127 - skill `ai-ml` (uncertain)

> ...AI, Engineering oder vergleichbarer Fachrichtung - bringst praktische Erfahrung mit AI, GenAI oder Prozessautomatisierung mit - hast Kenntnisse...

- A: `ai-ml` · required · raw_text: "praktische Erfahrung mit AI"
- B: `ai-ml` · required · raw_text: "praktische Erfahrung mit AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 43. golden_127 - skill `llms` (uncertain)

> ...Make it happen **DU…** - entwickelst AI- und GenAI-Anwendungen für Life-Science-Prozesse - entwickelst...

- A: `llms` · required · raw_text: "GenAI"
- B: `llms` · required · raw_text: "GenAI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 44. golden_128 - skill `data-engineering` (uncertain)

> ...practical experience. 7 years of experience in software or data engineering, including one or more programming languages (e.g.,...

- A: `data-engineering` · required · raw_text: "data engineering"
- B: `data-engineering` · required · raw_text: "software or data engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 45. golden_128 - skill `software-engineering` (uncertain)

> ...equivalent practical experience. 7 years of experience in software or data engineering, including one or more programming languages (e.g.,...

- A: `software-engineering` · required · raw_text: "software or data engineering"
- B: `software-engineering` · required · raw_text: "software or data engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 46. golden_131 - skill `evaluation` (uncertain)

> ...mit AWS Glue oder Lake Formation - Kenntnisse in der Bewertung und Qualitätssicherung KI-generierter Ergebnisse - Analytische, eigenständige und lösungsorientierte...

- A: `evaluation` · required · raw_text: "Bewertung und Qualitätssicherung KI-generierter Ergebnisse"
- B: `evaluation` · required · raw_text: "Bewertung und Qualitätssicherung KI-generierter Ergebnisse"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 47. golden_131 - skill `llm-orchestration` (uncertain)

> ...in Python, TypeScript oder Java - Erfahrung mit KI-Agenten und deren Orchestrierung - Praxis im Einsatz agentischer Entwicklungstools, z. B....

- A: `llm-orchestration` · required · raw_text: "KI-Agenten und deren Orchestrierung"
- B: `llm-orchestration` · required · raw_text: "KI-Agenten und deren Orchestrierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 48. golden_132 - skill `data-engineering` (uncertain)

> ...practical experience. 6 years of experience in software or data engineering. Experience solving real-world problems using machine...

- A: `data-engineering` · required · raw_text: "data engineering"
- B: `data-engineering` · required · raw_text: "data engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 49. golden_132 - skill `model-selection` (uncertain)

> ...methodologies (deep learning, reinforced learning), model identification, selection and AI operations (e.g., model monitoring). Experience...

- A: `model-selection` · required · raw_text: "model identification, selection"
- B: `model-selection` · required · raw_text: "model identification, selection"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 50. golden_132 - skill `reinforcement-learning` (uncertain)

> ...using machine learning methodologies (deep learning, reinforced learning), model identification, selection and AI operations (e.g.,...

- A: `reinforcement-learning` · required · raw_text: "reinforced learning"
- B: `reinforcement-learning` · required · raw_text: "reinforced learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 51. golden_132 - skill `software-engineering` (uncertain)

> ...equivalent practical experience. 6 years of experience in software or data engineering. Experience solving real-world problems using machine...

- A: `software-engineering` · required · raw_text: "software or data engineering"
- B: `software-engineering` · required · raw_text: "software or data engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 52. golden_133 - attribute `seniority` (uncertain)

> ...z. B. Kiro CLI, GitHub Copilot, Claude Code oder Cursor. - Mehrjährige Erfahrung in Wissensvermittlung und Beratung im IT-Umfeld. - Sicheres Verständnis von LLM, Context Window,...

- A: value="mid" · basis="inferred" · signal="Mehrjährige Erfahrung in Wissensvermittlung und Beratung im IT-Umfeld"
- B: value="mid" · basis="inferred" · signal="Mehrjährige Erfahrung in Wissensvermittlung und Beratung im IT-Umfeld."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 53. golden_133 - skill `llm-orchestration` (uncertain)

> ...Context Window, Embeddings, RAG, Tool Calling, Agenten, Orchestrierung, Guardrails, Prompt Injection, Evaluation, Halluzinationen...

- A: `llm-orchestration` · required · raw_text: "Orchestrierung"
- B: `llm-orchestration` · required · raw_text: "Orchestrierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 54. golden_128 - skill `mlops|aiops` (mapping)

> ...reinforced learning), model identification, selection and AI operations (e.g., model monitoring). Experience using Generative AI...

- A: `mlops` · required · raw_text: "AI operations"
- B: `aiops` · required · raw_text: "AI operations"

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 55. golden_132 - skill `mlops|aiops` (mapping)

> ...reinforced learning), model identification, selection and AI operations (e.g., model monitoring). Experience solving real-world...

- A: `mlops` · required · raw_text: "AI operations"
- B: `aiops` · required · raw_text: "AI operations"

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 56. golden_121 - attribute `degree` (spot-check)

> Data & AI Engineer (m/w/d)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 57. golden_122 - attribute `degree` (spot-check)

> Senior AI Voicebot & Automation Engineer (all gender)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 58. golden_122 - skill `llms` (spot-check)

> ...hast praktische Erfahrung im Prompt Engineering und mit LLMs - beherrschst Python, JavaScript oder TypeScript und REST...

- agreed label: `llms` · required · raw_text: "mit LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 59. golden_122 - skill `n8n` (spot-check)

> ...oder TypeScript und REST APIs/JSON - verfügst über Erfahrung mit n8n (Must-have) und Workflow-Automatisierung - hast Kenntnisse in...

- agreed label: `n8n` · required · raw_text: "Erfahrung mit n8n (Must-have)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 60. golden_122 - skill `python` (spot-check)

> ...Erfahrung im Prompt Engineering und mit LLMs - beherrschst Python, JavaScript oder TypeScript und REST APIs/JSON - verfügst...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 61. golden_122 - skill `typescript` (spot-check)

> ...und mit LLMs - beherrschst Python, JavaScript oder TypeScript und REST APIs/JSON - verfügst über Erfahrung mit n8n...

- agreed label: `typescript` · required · raw_text: "TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 62. golden_122 - skill `workflow-automation` (spot-check)

> ...verfügst über Erfahrung mit n8n (Must-have) und Workflow-Automatisierung - hast Kenntnisse in Microsoft Azure und cloud-nativen...

- agreed label: `workflow-automation` · required · raw_text: "Workflow-Automatisierung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 63. golden_123 - attribute `german` (spot-check)

> ...wie Azure, AWS oder Google sind Teil deines Profils. - Du beherrschst Deutsch auf mind. C1 Niveau und kannst es erfolgreich im Berufsalltag einsetzen - Your...

- agreed label: value="required" · basis="stated" · signal="Du beherrschst Deutsch auf mind. C1 Niveau"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 64. golden_123 - skill `embeddings` (spot-check)

> ...OpenAI, Spark und Scala. - Du hast Kenntnisse in LLMs, Embeddings, Retrieval Augmented Generation, Re-ranking, Guardrails,...

- agreed label: `embeddings` · required · raw_text: "Embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 65. golden_123 - skill `gcp` (spot-check)

> ...mit relevanten Cloud-Services wie Azure, AWS oder Google sind Teil deines Profils. - Du beherrschst Deutsch auf...

- agreed label: `gcp` · required · raw_text: "Google"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 66. golden_123 - skill `langchain` (spot-check)

> ...Tools und Frameworks wie z.B. Tensorflow, Pytorch, Keras, LangChain, LlamaIndex, OpenAI, Spark und Scala. - Du hast Kenntnisse...

- agreed label: `langchain` · required · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 67. golden_123 - skill `llamaindex` (spot-check)

> ...Frameworks wie z.B. Tensorflow, Pytorch, Keras, LangChain, LlamaIndex, OpenAI, Spark und Scala. - Du hast Kenntnisse in LLMs,...

- agreed label: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 68. golden_123 - skill `machine-learning` (spot-check)

> ...Models und Entity Extraction. - Mit KI-Konzepten und/oder Verfahren des maschinellen Lernens kennst du dich sehr gut aus. - Erfahrungen mit relevanten...

- agreed label: `machine-learning` · required · raw_text: "Verfahren des maschinellen Lernens"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 69. golden_123 - skill `python` (spot-check)

> ...Du bringst praxiserprobte Programmierkenntnisse in Python und/oder R sowie SQL mit. - Du hast einschlägige Erfahrung im Umgang...

- agreed label: `python` · required · raw_text: "Python und/oder R"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Python"}

## 70. golden_123 - skill `sql` (spot-check)

> ...praxiserprobte Programmierkenntnisse in Python und/oder R sowie SQL mit. - Du hast einschlägige Erfahrung im Umgang mit...

- agreed label: `sql` · required · raw_text: "sowie SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 71. golden_123 - skill `tensorflow` (spot-check)

> ...mit technologierelevanten Tools und Frameworks wie z.B. Tensorflow, Pytorch, Keras, LangChain, LlamaIndex, OpenAI, Spark und...

- agreed label: `tensorflow` · required · raw_text: "Tensorflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 72. golden_124 - attribute `degree` (spot-check)

> (Senior) AI-Native Software Engineer / Architect Node.js/TypeScript (m/w/d), Frankfurt am Main

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 73. golden_124 - attribute `german` (spot-check)

> (Senior) AI-Native Software Engineer / Architect Node.js/TypeScript (m/w/d), Frankfurt am Main

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 74. golden_124 - skill `chain-of-thought` (spot-check)

> ...nicht als Spielerei, sondern als Engineering-Disziplin (Chain-of-Thought, Context Window Management). Du kannst Anforderungen so...

- agreed label: `chain-of-thought` · required · raw_text: "Chain-of-Thought"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 75. golden_124 - skill `context-engineering` (spot-check)

> ...sondern als Engineering-Disziplin (Chain-of-Thought, Context Window Management). Du kannst Anforderungen so strukturieren, dass eine KI...

- agreed label: `context-engineering` · required · raw_text: "Context Window Management"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 76. golden_124 - skill `node-js` (spot-check)

> ...Tiefgreifende Node.js /TypeScript DNA: Du hast mehrjährige Erfahrung mit JavaScript/TypeScript (inkl. Node.js im Backend) und verstehst, was unter der Haube passiert. Du hast ein...

- agreed label: `node-js` · required · raw_text: "Erfahrung mit JavaScript/TypeScript (inkl. Node.js im Backend)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Node.js im Backend"}

## 77. golden_124 - skill `react` (spot-check)

> ...oder einer KI. Modernes Web Development & Container: Erfahrung mit React sowie Docker und Kubernetes. Du weißt, wie moderne...

- agreed label: `react` · required · raw_text: "Erfahrung mit React"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 78. golden_125 - attribute `seniority` (spot-check)

> Wir suchen eine/n engagierte/n KI / AI-Engineer (m/w/d) zur Verstärkung unseres IT-Teams. In dieser Position sind Sie verantwortlich für die

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 79. golden_125 - skill `bash` (spot-check)

> ...Server - Erfahrung im Umgang mit VPN-Technologien sowie Shell Scripting (Bash), T-SQL oder Python ist wünschenswert - Kenntnisse in...

- agreed label: `bash` · nice_to_have · raw_text: "Shell Scripting (Bash)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 80. golden_125 - skill `java` (spot-check)

> ...oder Python ist wünschenswert - Kenntnisse in JavaScript, Java, Jenkins sowie in agilen Arbeitsmethoden sind von Vorteil -...

- agreed label: `java` · nice_to_have · raw_text: "Java, Jenkins"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Java"}

## 81. golden_126 - attribute `german` (spot-check)

> AI Engineer / KI-Entwickler (m/w/d)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 82. golden_126 - skill `apis` (spot-check)

> ...Generative AI (Prompting, Fine-Tuning). - Erfahrung mit API-Entwicklung (REST) und Git-basierter Softwareentwicklung. - Grundverständnis...

- agreed label: `apis` · required · raw_text: "API-Entwicklung (REST)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 83. golden_126 - skill `ci-cd` (spot-check)

> ...von Software-Engineering-Prinzipien (Testing, CI/CD). - Ausgeprägte kommunikative Stärken sowie die...

- agreed label: `ci-cd` · required · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 84. golden_126 - skill `fine-tuning` (spot-check)

> ...im Umgang mit LLMs und Generative AI (Prompting, Fine-Tuning). - Erfahrung mit API-Entwicklung (REST) und Git-basierter...

- agreed label: `fine-tuning` · required · raw_text: "Fine-Tuning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 85. golden_126 - skill `llamaindex` (spot-check)

> ...in Python und modernen KI-Frameworks (z. B. LangChain, LlamaIndex). - Praxiserfahrung im Umgang mit LLMs und Generative AI...

- agreed label: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 86. golden_126 - skill `llms` (spot-check)

> ...modernen KI-Frameworks (z. B. LangChain, LlamaIndex). - Praxiserfahrung im Umgang mit LLMs und Generative AI (Prompting, Fine-Tuning). - Erfahrung mit API-Entwicklung...

- agreed label: `llms` · required · raw_text: "Praxiserfahrung im Umgang mit LLMs und Generative AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 87. golden_126 - skill `python` (spot-check)

> ...Aufgabenbereich und in der Softwareentwicklung. - Kenntnisse in Python und modernen KI-Frameworks (z. B. LangChain,...

- agreed label: `python` · required · raw_text: "Kenntnisse in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_127 - attribute `german` (spot-check)

> AI & Automation Engineer – Life Sciences (all gender)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_127 - attribute `seniority` (spot-check)

> AI & Automation Engineer – Life Sciences (all gender)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_127 - skill `agents` (spot-check)

> ...mit LLMs, Prompt Engineering oder RAG-Ansätzen mit - hast Interesse an Conversational AI, Chatbots, Voicebots oder AI Agents Wir wertschätzen Vielfalt und begrüßen daher alle...

- agreed label: `agents` · nice_to_have · raw_text: "Interesse an Conversational AI, Chatbots, Voicebots oder AI Agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 91. golden_127 - skill `azure` (spot-check)

> ...und Erfahrung mit REST APIs, JSON oder Webhooks - kennst dich aus mit Azure, Azure AI oder vergleichbaren Cloud-Technologien -...

- agreed label: `azure` · required · raw_text: "kennst dich aus mit Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 92. golden_127 - skill `conversational-ai` (spot-check)

> ...mit LLMs, Prompt Engineering oder RAG-Ansätzen mit - hast Interesse an Conversational AI, Chatbots, Voicebots oder AI Agents Wir wertschätzen...

- agreed label: `conversational-ai` · nice_to_have · raw_text: "Interesse an Conversational AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 93. golden_127 - skill `power-automate` (spot-check)

> ...Kenntnisse in Workflow Automation, beispielsweise n8n, Microsoft Power Automate oder vergleichbaren Plattformen - bringst Erfahrung mit...

- agreed label: `power-automate` · required · raw_text: "Microsoft Power Automate"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 94. golden_127 - skill `prompt-engineering` (spot-check)

> ...Power Automate oder vergleichbaren Plattformen - bringst Erfahrung mit LLMs, Prompt Engineering oder RAG-Ansätzen mit - hast Interesse an Conversational...

- agreed label: `prompt-engineering` · required · raw_text: "Erfahrung mit LLMs, Prompt Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Prompt Engineering"}

## 95. golden_127 - skill `python` (spot-check)

> ...GenAI oder Prozessautomatisierung mit - hast Kenntnisse in Python, JavaScript oder TypeScript und Erfahrung mit REST APIs,...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 96. golden_128 - attribute `german` (spot-check)

> AI Innovation Engineer, Deutsche Borse Group, Google Cloud

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 97. golden_128 - attribute `seniority` (spot-check)

> ...a related field, or equivalent practical experience. 7 years of experience in software or data engineering, including one or more programming languages (e.g.,...

- agreed label: value="senior" · basis="inferred" · signal="7 years of experience in software or data engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_128 - skill `explainable-ai` (spot-check)

> ...and data residency, encryption at rest/transit (CMEK), and "explainable AI" requirements in banking. Experience with data modeling of...

- agreed label: `explainable-ai` · nice_to_have · raw_text: "\"explainable AI\""

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_128 - skill `llm-orchestration` (spot-check)

> ...model monitoring). Experience using Generative AI and agentic orchestration utilizing frameworks (e.g., LangChain, CrewAI, or Vertex...

- agreed label: `llm-orchestration` · required · raw_text: "agentic orchestration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_128 - skill `llms` (spot-check)

> ...AI operations (e.g., model monitoring). Experience using Generative AI and agentic orchestration utilizing frameworks (e.g.,...

- agreed label: `llms` · required · raw_text: "Generative AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_128 - skill `machine-learning` (spot-check)

> ...frameworks, and API contract design. Experience using machine learning methodologies (deep learning, reinforced learning), model...

- agreed label: `machine-learning` · required · raw_text: "machine learning methodologies"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_128 - skill `observability` (spot-check)

> ...model identification, selection and AI operations (e.g., model monitoring). Experience using Generative AI and agentic orchestration...

- agreed label: `observability` · required · raw_text: "model monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: drop

## 103. golden_128 - skill `python` (spot-check)

> ...including one or more programming languages (e.g., Python, Go, Java), and with design patterns, testing frameworks,...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 104. golden_128 - skill `vector-databases` (spot-check)

> ...(e.g., LangChain, CrewAI, or Vertex AI Agent Builder) and vector databases. Preferred qualifications: Experience in financial...

- agreed label: `vector-databases` · required · raw_text: "vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 105. golden_129 - attribute `degree` (spot-check)

> AI Inference Engineer (all genders)

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 106. golden_129 - attribute `german` (spot-check)

> AI Inference Engineer (all genders)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_129 - attribute `seniority` (spot-check)

> AI Inference Engineer (all genders)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_130 - attribute `german` (spot-check)

> Agentic AI Software Engineer (m/w/d) | Frankfurt | 80% Remote | JBA15245

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_130 - attribute `seniority` (spot-check)

> Agentic AI Software Engineer (m/w/d) | Frankfurt | 80% Remote | JBA15245

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_131 - attribute `degree` (spot-check)

> ...Ownern und Entwicklungsteams **Anforderungen:** - Abgeschlossenes IT-Studium oder vergleichbare Qualifikation - Fundierte Erfahrung im Software Engineering,...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossenes IT-Studium oder vergleichbare Qualifikation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_131 - attribute `seniority` (spot-check)

> #15245 Agentic AI Software Engineer (m/w/d)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 112. golden_131 - skill `agents` (spot-check)

> ...Programmierkenntnisse in Python, TypeScript oder Java - Erfahrung mit KI-Agenten und deren Orchestrierung - Praxis im Einsatz agentischer...

- agreed label: `agents` · required · raw_text: "Erfahrung mit KI-Agenten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 113. golden_131 - skill `ai-developer-tooling` (spot-check)

> ...KI-Agenten und deren Orchestrierung - Praxis im Einsatz agentischer Entwicklungstools, z. B. Claude Code, Cursor oder vergleichbare Lösungen -...

- agreed label: `ai-developer-tooling` · required · raw_text: "agentischer Entwicklungstools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 114. golden_131 - skill `ci-cd` (spot-check)

> ...Fundierte Erfahrung im Software Engineering, Architekturdesign und CI/CD - Praktische Programmierkenntnisse in Python, TypeScript...

- agreed label: `ci-cd` · required · raw_text: "Architekturdesign und CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "CI/CD"}

## 115. golden_131 - skill `cloud` (spot-check)

> ...z. B. Claude Code, Cursor oder vergleichbare Lösungen - Cloud-Erfahrung, idealerweise AWS, sowie Kenntnisse in Infrastructure as...

- agreed label: `cloud` · required · raw_text: "Cloud-Erfahrung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 116. golden_131 - skill `infrastructure-as-code` (spot-check)

> ...Cloud-Erfahrung, idealerweise AWS, sowie Kenntnisse in Infrastructure as Code - Erfahrung im Data Engineering, idealerweise mit AWS Glue...

- agreed label: `infrastructure-as-code` · required · raw_text: "Infrastructure as Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 117. golden_131 - skill `java` (spot-check)

> ...und CI/CD - Praktische Programmierkenntnisse in Python, TypeScript oder Java - Erfahrung mit KI-Agenten und deren Orchestrierung -...

- agreed label: `java` · required · raw_text: "Python, TypeScript oder Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Java"}

## 118. golden_131 - skill `software-engineering` (spot-check)

> ...oder vergleichbare Qualifikation - Fundierte Erfahrung im Software Engineering, Architekturdesign und CI/CD - Praktische...

- agreed label: `software-engineering` · required · raw_text: "Software Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_132 - attribute `german` (spot-check)

> AI Innovation Engineer, Google Cloud

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 120. golden_132 - skill `api-design` (spot-check)

> ...with design patterns, testing frameworks, and API contract design. Preferred qualifications: Experience in financial...

- agreed label: `api-design` · required · raw_text: "API contract design"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 121. golden_132 - skill `devops` (spot-check)

> ...Data Vault, etc.). Experience working in a high-maturity DevOps culture (trunk-based development, automated testing, blue/green...

- agreed label: `devops` · nice_to_have · raw_text: "DevOps culture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 122. golden_132 - skill `explainable-ai` (spot-check)

> ...data residency, encryption at rest/transit (CMEK), and "explainable AI" requirements in banking. Experience with data modeling of...

- agreed label: `explainable-ai` · nice_to_have · raw_text: "explainable AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 123. golden_132 - skill `llms` (spot-check)

> ...monitoring). Experience solving real-world problems using Generative AI and agentic orchestration utilizing frameworks (e.g.,...

- agreed label: `llms` · required · raw_text: "Generative AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 124. golden_132 - skill `machine-learning` (spot-check)

> ...engineering. Experience solving real-world problems using machine learning methodologies (deep learning, reinforced learning), model...

- agreed label: `machine-learning` · required · raw_text: "machine learning methodologies"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 125. golden_132 - skill `observability` (spot-check)

> ...model identification, selection and AI operations (e.g., model monitoring). Experience solving real-world problems using Generative...

- agreed label: `observability` · required · raw_text: "model monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: drop

## 126. golden_132 - skill `python` (spot-check)

> ...with one of the following programming languages: Python, Go, or Java. Experience with design patterns, testing...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_132 - skill `vector-databases` (spot-check)

> ...(e.g., LangChain, CrewAI, or Vertex AI Agent Builder) and vector databases. Experience with one of the following programming...

- agreed label: `vector-databases` · required · raw_text: "vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_133 - attribute `german` (spot-check)

> ...an Security, Datenschutz und Compliance von Vorteil. - Sehr gute Deutschkenntnisse (C1 oder höher). - Ausgeprägte Abstraktionsfähigkeit, analytisches Denken...

- agreed label: value="required" · basis="stated" · signal="Sehr gute Deutschkenntnisse (C1 oder höher)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 129. golden_133 - skill `agents` (spot-check)

> ...von LLM, Context Window, Embeddings, RAG, Tool Calling, Agenten, Orchestrierung, Guardrails, Prompt Injection, Evaluation,...

- agreed label: `agents` · required · raw_text: "Agenten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_133 - skill `ai-developer-tooling` (spot-check)

> ...12 Monate kontinuierliche praktische Erfahrung mit KI-Werkzeugen in der Softwareentwicklung, z. B. Kiro CLI, GitHub Copilot, Claude Code oder...

- agreed label: `ai-developer-tooling` · required · raw_text: "KI-Werkzeugen in der Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 131. golden_133 - skill `cloud` (spot-check)

> ...der messbaren Bewertung der Ergebnisgüte. - Erfahrung mit Cloud-Umgebungen und großen bzw. regulierten IT-Organisationen,...

- agreed label: `cloud` · required · raw_text: "Cloud-Umgebungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_133 - skill `cursor` (spot-check)

> ...z. B. Kiro CLI, GitHub Copilot, Claude Code oder Cursor. - Mehrjährige Erfahrung in Wissensvermittlung und...

- agreed label: `cursor` · required · raw_text: "Cursor"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 133. golden_133 - skill `embeddings` (spot-check)

> ...IT-Umfeld. - Sicheres Verständnis von LLM, Context Window, Embeddings, RAG, Tool Calling, Agenten, Orchestrierung, Guardrails,...

- agreed label: `embeddings` · required · raw_text: "Embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_133 - skill `llms` (spot-check)

> ...und Beratung im IT-Umfeld. - Sicheres Verständnis von LLM, Context Window, Embeddings, RAG, Tool Calling, Agenten,...

- agreed label: `llms` · required · raw_text: "LLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 135. golden_133 - skill `mcp` (spot-check)

> ...und des end-to-end SDLC. - Praktische Erfahrung mit MCP-Servern und agentischen Skills. - Mindestens 12 Monate...

- agreed label: `mcp` · required · raw_text: "MCP-Servern"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok
