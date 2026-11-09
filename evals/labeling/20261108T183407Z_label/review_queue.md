# Review queue - 20261108T183407Z_label

134 items from 13 postings. Labeler A: `claude-opus-5-5` (anthropic).
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

Spot-check items are a seeded random sample (80 of 164 accepted labels,
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

## 1. golden_049 - scope `in_scope` (in-scope)

> Data & AI Engineer (m/w/d)

- Fitness First Germany GmbH · Data & AI Engineer (m/w/d)
- Frankfurt · de · arbeitsagentur · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_050 - scope `in_scope` (in-scope)

> Senior AI Voicebot & Automation Engineer (all gender)

- ALTEN GmbH München · Senior AI Voicebot & Automation Engineer (all gender)
- Frankfurt · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_051 - scope `in_scope` (in-scope)

> AI Engineer (w|m|d)

- BridgingIT GmbH · AI Engineer (w|m|d)
- Frankfurt · de · arbeitsagentur · 17 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_052 - scope `in_scope` (in-scope)

> (Senior) AI-Native Software Engineer / Architect Node.js/TypeScript (m/w/d), Frankfurt am Main

- Institutional Investment Group · (Senior) AI-Native Software Engineer / Architect Node.js/TypeScript (m/w/d), Frankfurt am Main
- Frankfurt · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_053 - scope `in_scope` (in-scope)

> Wir suchen eine/n engagierte/n KI / AI-Engineer (m/w/d) zur Verstärkung unseres IT-Teams. In dieser Position sind Sie verantwortlich für die

- NEXALL · KI / AI-Engineer (m/w/d)
- Frankfurt · de · arbeitsagentur · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_054 - scope `in_scope` (in-scope)

> AI Engineer / KI-Entwickler (m/w/d)

- Finanz Informatik GmbH & Co. KG · AI Engineer / KI-Entwickler (m/w/d)
- Frankfurt · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_055 - scope `in_scope` (in-scope)

> AI & Automation Engineer – Life Sciences (all gender)

- ALTEN GmbH München · AI & Automation Engineer – Life Sciences (all gender)
- Frankfurt · de · arbeitsagentur · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_056 - scope `in_scope` (in-scope)

> AI Innovation Engineer, Deutsche Borse Group, Google Cloud

- Google Germany GmbH · AI Innovation Engineer, Deutsche Borse Group, Google Cloud
- Frankfurt · en · arbeitsagentur · 21 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_057 - scope `in_scope` (in-scope)

> AI Inference Engineer (all genders)

- EXXETA AG · AI Inference Engineer (all genders)
- Frankfurt · en · arbeitsagentur · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_058 - scope `in_scope` (in-scope)

> Agentic AI Software Engineer (m/w/d) | Frankfurt | 80% Remote | JBA15245

- freelance.de · Agentic AI Software Engineer (m/w/d) | Frankfurt | 80% Remote | JBA15245
- Frankfurt · en · jsearch · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_059 - scope `in_scope` (in-scope)

> #15245 Agentic AI Software Engineer (m/w/d)

- Constaff GmbH · #15245 Agentic AI Software Engineer (m/w/d)
- Frankfurt · de · arbeitsagentur · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_060 - scope `in_scope` (in-scope)

> AI Innovation Engineer, Google Cloud

- Google Germany GmbH · AI Innovation Engineer, Google Cloud
- Frankfurt · en · arbeitsagentur · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_061 - scope `in_scope` (in-scope)

> Für den Standort Frankfurt am Main suchen wir:

- Guldberg GmbH · Plattform AI Engineer (m/w/d)
- Frankfurt · de · arbeitsagentur · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_049 - skill `ai-ml` (disagreement)

> ...Du arbeitest mit aktuellen Cloud-, Data- und AI-Technologien – unter anderem mit Snowflake, Python und modernen...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI-Technologien"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 15. golden_049 - skill `cloud` (disagreement)

> ...Moderner Technologie-Stack: Du arbeitest mit aktuellen Cloud-, Data- und AI-Technologien – unter anderem mit Snowflake, Python und modernen...

- A: (did not label this)
- B: `cloud` · required · raw_text: "Cloud-, Data- und AI-Technologien"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 16. golden_051 - attribute `seniority` (disagreement)

> ...erfolgreich abgeschlossen und es bildet die Basis deiner mehrjährigen Berufserfahrung. - Du bringst praxiserprobte Programmierkenntnisse in...

- A: value="mid" · basis="inferred" · signal="mehrjährigen Berufserfahrung"
- B: value=null · basis=null · signal=null

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_056 - skill `data-privacy-and-security` (disagreement)

> ...or custody. Experience with FSI regulatory practices and data residency, encryption at rest/transit (CMEK), and "explainable AI" requirements in banking. Experience...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "data residency, encryption at rest/transit (CMEK)"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_056 - skill `vertex-ai` (disagreement)

> ...utilizing frameworks (e.g., LangChain, CrewAI, or Vertex AI Agent Builder) and vector databases. Preferred...

- A: `vertex-ai` · required · raw_text: "Vertex AI Agent Builder"
- B: `vertex-ai` · nice_to_have · raw_text: "Experience in BigQuery, Vertex AI"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_060 - skill `data-privacy-and-security` (disagreement)

> ...or custody. Experience with FSI regulatory practices and data residency, encryption at rest/transit (CMEK), and "explainable AI" requirements in banking. Experience...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "data residency, encryption at rest/transit (CMEK)"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_060 - skill `software-engineering` (disagreement)

> ...equivalent practical experience. 6 years of experience in software or data engineering. Experience solving real-world problems using machine...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software or data engineering"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_060 - skill `vertex-ai` (disagreement)

> ...utilizing frameworks (e.g., LangChain, CrewAI, or Vertex AI Agent Builder) and vector databases. Experience with one of the...

- A: `vertex-ai` · required · raw_text: "Vertex AI Agent Builder"
- B: `vertex-ai` · nice_to_have · raw_text: "Experience in BigQuery, Vertex AI"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_061 - attribute `seniority` (disagreement)

> ...z. B. Kiro CLI, GitHub Copilot, Claude Code oder Cursor. - Mehrjährige Erfahrung in Wissensvermittlung und Beratung im IT-Umfeld. - Sicheres Verständnis von LLM, Context Window,...

- A: value="mid" · basis="inferred" · signal="Mehrjährige Erfahrung in Wissensvermittlung und Beratung im IT-Umfeld"
- B: value="junior" · basis="inferred" · signal="Mindestens 12 Monate kontinuierliche praktische Erfahrung mit KI-Werkzeugen in der Softwareentwicklung"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_061 - skill `hallucination-detection` (disagreement)

> ...Orchestrierung, Guardrails, Prompt Injection, Evaluation, Halluzinationen und Kosten je Token. - Erfahrung darin, Grenzen und...

- A: `hallucination-detection` · required · raw_text: "Halluzinationen"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_061 - skill `software-engineering` (disagreement)

> ...praktische Erfahrung mit KI-Werkzeugen in der Softwareentwicklung, z. B. Kiro CLI, GitHub Copilot, Claude Code oder...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "Softwareentwicklung"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_049 - attribute `degree` (uncertain)

> Data & AI Engineer (m/w/d)

- A: value=null · requirement=null · or_equivalent=false · signal=null
- B: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 26. golden_049 - attribute `seniority` (uncertain)

> Data & AI Engineer (m/w/d)

- A: value=null · basis=null · signal=null
- B: value=null · basis=null · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 27. golden_049 - skill `python` (uncertain)

> ...Data- und AI-Technologien – unter anderem mit Snowflake, Python und modernen Engineering-Werkzeugen.✓ Individueller...

- A: `python` · required · raw_text: "Python"
- B: `python` · required · raw_text: "Python"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 28. golden_049 - skill `snowflake` (uncertain)

> ...unsere Unternehmensgruppe.✓ Moderner Technologie-Stack: Du arbeitest mit aktuellen Cloud-, Data- und AI-Technologien – unter anderem mit Snowflake, Python und modernen Engineering-Werkzeugen.✓...

- A: `snowflake` · required · raw_text: "Du arbeitest mit aktuellen Cloud-, Data- und AI-Technologien – unter anderem mit Snowflake"
- B: `snowflake` · required · raw_text: "Snowflake"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 29. golden_050 - skill `cloud` (uncertain)

> ...hast Kenntnisse in Microsoft Azure und cloud-nativen Architekturen - bringst idealerweise Erfahrung mit TTS/STT oder...

- A: `cloud` · required · raw_text: "cloud-nativen Architekturen"
- B: `cloud` · required · raw_text: "cloud-nativen Architekturen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 30. golden_051 - skill `ai-ml` (uncertain)

> ...Classification Models und Entity Extraction. - Mit KI-Konzepten und/oder Verfahren des maschinellen Lernens kennst du dich...

- A: `ai-ml` · required · raw_text: "KI-Konzepten"
- B: `ai-ml` · required · raw_text: "KI-Konzepten"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 31. golden_051 - skill `gcp` (uncertain)

> ...mit relevanten Cloud-Services wie Azure, AWS oder Google sind Teil deines Profils. - Du beherrschst Deutsch auf...

- A: `gcp` · required · raw_text: "Google"
- B: `gcp` · required · raw_text: "Google"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 32. golden_051 - skill `llm-guardrails` (uncertain)

> ...Embeddings, Retrieval Augmented Generation, Re-ranking, Guardrails, Clustering, Classification Models und Entity...

- A: `llm-guardrails` · required · raw_text: "Guardrails"
- B: `llm-guardrails` · required · raw_text: "Guardrails"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 33. golden_051 - skill `nlp` (uncertain)

> ...Guardrails, Clustering, Classification Models und Entity Extraction. - Mit KI-Konzepten und/oder Verfahren des maschinellen...

- A: `nlp` · required · raw_text: "Entity Extraction"
- B: `nlp` · required · raw_text: "Entity Extraction"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 34. golden_052 - skill `backend-development` (uncertain)

> ...Tiefgreifende Node.js /TypeScript DNA: Du hast mehrjährige Erfahrung mit JavaScript/TypeScript (inkl. Node.js im Backend) und verstehst, was unter der Haube passiert. Du hast ein...

- A: `backend-development` · required · raw_text: "Erfahrung mit JavaScript/TypeScript (inkl. Node.js im Backend)"
- B: `backend-development` · required · raw_text: "Node.js im Backend"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 35. golden_052 - skill `cloud` (uncertain)

> ...Sicherheitslücken und Logikfehler. Lernbereitschaft: Du hast Lust, deine Node.js/TypeScript -Komfortzone zu verlassen und dich von der KI in neue Tech-Stacks (Cloud Native, Python Data Services etc.) begleiten zu lassen. Warum wir? VERGÜTUNGSPAKET...

- A: `cloud` · nice_to_have · raw_text: "Du hast Lust, deine Node.js/TypeScript -Komfortzone zu verlassen und dich von der KI in neue Tech-Stacks (Cloud Native, Python Data Services etc.)"
- B: `cloud` · nice_to_have · raw_text: "Du hast Lust, deine Node.js/TypeScript -Komfortzone zu verlassen und dich von der KI in neue Tech-Stacks (Cloud Native, Python Data Services etc.) begleiten zu lassen."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 36. golden_052 - skill `containerization` (uncertain)

> ...sofort - egal ob von einem Menschen oder einer KI. Modernes Web Development & Container: Erfahrung mit React sowie Docker und Kubernetes. Du...

- A: `containerization` · required · raw_text: "Modernes Web Development & Container"
- B: `containerization` · required · raw_text: "Container"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 37. golden_052 - skill `distributed-systems` (uncertain)

> ...Erfahrung mit React sowie Docker und Kubernetes. Du weißt, wie moderne verteilte Anwendungen laufen. DevOps Praktiker: CI/CD (z.B. GitLab, Jenkins) ist für...

- A: `distributed-systems` · required · raw_text: "wie moderne verteilte Anwendungen laufen"
- B: `distributed-systems` · required · raw_text: "Du weißt, wie moderne verteilte Anwendungen laufen."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 38. golden_052 - skill `gitlab-ci` (uncertain)

> ...moderne verteilte Anwendungen laufen. DevOps Praktiker: CI/CD (z.B. GitLab, Jenkins) ist für dich kein Fremdwort, sondern Teil deiner täglichen...

- A: `gitlab-ci` · required · raw_text: "CI/CD (z.B. GitLab, Jenkins)"
- B: `gitlab-ci` · required · raw_text: "CI/CD (z.B. GitLab, Jenkins)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_052 - skill `hallucination-detection` (uncertain)

> ...vertraust der KI nicht blind. Dein Code-Review-Blick ist geschärft für Halluzinationen, Sicherheitslücken und Logikfehler. Lernbereitschaft: Du...

- A: `hallucination-detection` · required · raw_text: "geschärft für Halluzinationen"
- B: `hallucination-detection` · required · raw_text: "Dein Code-Review-Blick ist geschärft für Halluzinationen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_052 - skill `software-architecture` (uncertain)

> ...so strukturieren, dass eine KI sie fehlerfrei umsetzt. Architektur vor Syntax: Du denkst in Systemen, Schnittstellen und Datenflüssen....

- A: `software-architecture` · required · raw_text: "Architektur vor Syntax"
- B: `software-architecture` · required · raw_text: "Architektur vor Syntax"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_053 - attribute `degree` (uncertain)

> ...IT-Systemintegrator **Qualifikationen:** - Abgeschlossene Ausbildung oder Studium im Bereich Informatik oder eine vergleichbare Qualifikation - Fundierte Kenntnisse in der Systemadministration,...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossene Ausbildung oder Studium im Bereich Informatik oder eine vergleichbare Qualifikation"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossene Ausbildung oder Studium im Bereich Informatik oder eine vergleichbare Qualifikation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_053 - skill `networking` (uncertain)

> ...Jenkins sowie in agilen Arbeitsmethoden sind von Vorteil - Sicherer Umgang mit Netzwerkprotokollen und Sicherheitsstandards - Teamfähigkeit,...

- A: `networking` · required · raw_text: "Sicherer Umgang mit Netzwerkprotokollen"
- B: `networking` · required · raw_text: "Netzwerkprotokollen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_053 - skill `sql` (uncertain)

> ...Umgang mit VPN-Technologien sowie Shell Scripting (Bash), T-SQL oder Python ist wünschenswert - Kenntnisse in JavaScript,...

- A: `sql` · nice_to_have · raw_text: "T-SQL"
- B: `sql` · nice_to_have · raw_text: "T-SQL"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_055 - skill `ai-ml` (uncertain)

> ...AI, Engineering oder vergleichbarer Fachrichtung - bringst praktische Erfahrung mit AI, GenAI oder Prozessautomatisierung mit - hast Kenntnisse...

- A: `ai-ml` · required · raw_text: "praktische Erfahrung mit AI"
- B: `ai-ml` · required · raw_text: "praktische Erfahrung mit AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_058 - attribute `german` (uncertain)

> Agentic AI Software Engineer (m/w/d) | Frankfurt | 80% Remote | JBA15245

- A: value="required" · basis="inferred" · signal=null
- B: value="required" · basis="inferred" · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_059 - attribute `seniority` (uncertain)

> #15245 Agentic AI Software Engineer (m/w/d)

- A: value=null · basis=null · signal=null
- B: value=null · basis=null · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_059 - skill `evaluation` (uncertain)

> ...mit AWS Glue oder Lake Formation - Kenntnisse in der Bewertung und Qualitätssicherung KI-generierter Ergebnisse - Analytische, eigenständige und lösungsorientierte...

- A: `evaluation` · required · raw_text: "Bewertung und Qualitätssicherung KI-generierter Ergebnisse"
- B: `evaluation` · required · raw_text: "Bewertung und Qualitätssicherung KI-generierter Ergebnisse"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_059 - skill `llm-orchestration` (uncertain)

> ...in Python, TypeScript oder Java - Erfahrung mit KI-Agenten und deren Orchestrierung - Praxis im Einsatz agentischer Entwicklungstools, z. B....

- A: `llm-orchestration` · required · raw_text: "KI-Agenten und deren Orchestrierung"
- B: `llm-orchestration` · required · raw_text: "KI-Agenten und deren Orchestrierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_060 - skill `aiops` (uncertain)

> ...reinforced learning), model identification, selection and AI operations (e.g., model monitoring). Experience solving real-world...

- A: `aiops` · required · raw_text: "AI operations"
- B: `aiops` · required · raw_text: "AI operations"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_060 - skill `llm-orchestration` (uncertain)

> ...solving real-world problems using Generative AI and agentic orchestration utilizing frameworks (e.g., LangChain, CrewAI, or Vertex AI Agent Builder) and...

- A: `llm-orchestration` · required · raw_text: "agentic orchestration utilizing frameworks"
- B: `llm-orchestration` · required · raw_text: "agentic orchestration"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_060 - skill `model-selection` (uncertain)

> ...methodologies (deep learning, reinforced learning), model identification, selection and AI operations (e.g., model monitoring). Experience...

- A: `model-selection` · required · raw_text: "model identification, selection"
- B: `model-selection` · required · raw_text: "selection"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_061 - skill `aws-bedrock` (uncertain)

> ...IT-Organisationen, idealerweise im SAFe-Umfeld. - Kenntnisse in AWS Bedrock AgentCore, Microsoft Foundry Agents Service und Microsoft Copilot...

- A: `aws-bedrock` · nice_to_have · raw_text: "Kenntnisse in AWS Bedrock AgentCore"
- B: `aws-bedrock` · nice_to_have · raw_text: "AWS Bedrock AgentCore"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_061 - skill `llm-orchestration` (uncertain)

> ...Context Window, Embeddings, RAG, Tool Calling, Agenten, Orchestrierung, Guardrails, Prompt Injection, Evaluation, Halluzinationen...

- A: `llm-orchestration` · required · raw_text: "Orchestrierung"
- B: `llm-orchestration` · required · raw_text: "Orchestrierung"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_056 - skill `mlops|aiops` (mapping)

> ...reinforced learning), model identification, selection and AI operations (e.g., model monitoring). Experience using Generative AI...

- A: `mlops` · required · raw_text: "AI operations"
- B: `aiops` · required · raw_text: "AI operations"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 55. golden_049 - attribute `german` (spot-check)

> Data & AI Engineer (m/w/d)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 56. golden_050 - attribute `seniority` (spot-check)

> Senior AI Voicebot & Automation Engineer (all gender) ### #weareALTEN – the home of forward...

- agreed label: value="senior" · basis="stated" · signal="Senior AI Voicebot & Automation Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 57. golden_050 - skill `llms` (spot-check)

> ...hast praktische Erfahrung im Prompt Engineering und mit LLMs - beherrschst Python, JavaScript oder TypeScript und REST...

- agreed label: `llms` · required · raw_text: "mit LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 58. golden_050 - skill `prompt-engineering` (spot-check)

> ...AI oder Voicebots - hast praktische Erfahrung im Prompt Engineering und mit LLMs - beherrschst Python, JavaScript oder...

- agreed label: `prompt-engineering` · required · raw_text: "Prompt Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 59. golden_050 - skill `python` (spot-check)

> ...Erfahrung im Prompt Engineering und mit LLMs - beherrschst Python, JavaScript oder TypeScript und REST APIs/JSON - verfügst...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 60. golden_050 - skill `typescript` (spot-check)

> ...und mit LLMs - beherrschst Python, JavaScript oder TypeScript und REST APIs/JSON - verfügst über Erfahrung mit n8n (Must-have) und...

- agreed label: `typescript` · required · raw_text: "TypeScript und REST APIs/JSON"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 61. golden_051 - attribute `degree` (spot-check)

> ...deiner Resultate runden deine Aufgabe ab. DEINE Skills - Dein Studium in Data Science, Wirtschaftsinformatik, Mathematik, Physik oder Statistik hast du erfolgreich abgeschlossen und es bildet die Basis deiner mehrjährigen...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="Dein Studium in Data Science, Wirtschaftsinformatik, Mathematik, Physik oder Statistik hast du erfolgreich abgeschlossen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 62. golden_051 - skill `aws` (spot-check)

> ...Erfahrungen mit relevanten Cloud-Services wie Azure, AWS oder Google sind Teil deines Profils. - Du beherrschst...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 63. golden_051 - skill `llamaindex` (spot-check)

> ...Frameworks wie z.B. Tensorflow, Pytorch, Keras, LangChain, LlamaIndex, OpenAI, Spark und Scala. - Du hast Kenntnisse in LLMs,...

- agreed label: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 64. golden_051 - skill `llms` (spot-check)

> ...LangChain, LlamaIndex, OpenAI, Spark und Scala. - Du hast Kenntnisse in LLMs, Embeddings, Retrieval Augmented Generation, Re-ranking,...

- agreed label: `llms` · required · raw_text: "Kenntnisse in LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 65. golden_051 - skill `machine-learning` (spot-check)

> ...Models und Entity Extraction. - Mit KI-Konzepten und/oder Verfahren des maschinellen Lernens kennst du dich sehr gut aus. - Erfahrungen mit relevanten...

- agreed label: `machine-learning` · required · raw_text: "Verfahren des maschinellen Lernens"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 66. golden_051 - skill `openai-api` (spot-check)

> ...z.B. Tensorflow, Pytorch, Keras, LangChain, LlamaIndex, OpenAI, Spark und Scala. - Du hast Kenntnisse in LLMs,...

- agreed label: `openai-api` · required · raw_text: "OpenAI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 67. golden_051 - skill `pytorch` (spot-check)

> ...Tools und Frameworks wie z.B. Tensorflow, Pytorch, Keras, LangChain, LlamaIndex, OpenAI, Spark und Scala. -...

- agreed label: `pytorch` · required · raw_text: "Pytorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 68. golden_051 - skill `rag` (spot-check)

> ...Spark und Scala. - Du hast Kenntnisse in LLMs, Embeddings, Retrieval Augmented Generation, Re-ranking, Guardrails, Clustering, Classification Models...

- agreed label: `rag` · required · raw_text: "Retrieval Augmented Generation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 69. golden_051 - skill `scala` (spot-check)

> ...Pytorch, Keras, LangChain, LlamaIndex, OpenAI, Spark und Scala. - Du hast Kenntnisse in LLMs, Embeddings, Retrieval...

- agreed label: `scala` · required · raw_text: "Scala"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 70. golden_052 - attribute `german` (spot-check)

> (Senior) AI-Native Software Engineer / Architect Node.js/TypeScript (m/w/d), Frankfurt am Main

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 71. golden_052 - skill `chain-of-thought` (spot-check)

> ...nicht als Spielerei, sondern als Engineering-Disziplin (Chain-of-Thought, Context Window Management). Du kannst Anforderungen so strukturieren, dass eine KI...

- agreed label: `chain-of-thought` · required · raw_text: "(Chain-of-Thought, Context Window Management)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 72. golden_052 - skill `ci-cd` (spot-check)

> ...moderne verteilte Anwendungen laufen. DevOps Praktiker: CI/CD (z.B. GitLab, Jenkins) ist für dich kein Fremdwort, sondern Teil deiner täglichen...

- agreed label: `ci-cd` · required · raw_text: "CI/CD (z.B. GitLab, Jenkins)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 73. golden_052 - skill `docker` (spot-check)

> ...Modernes Web Development & Container: Erfahrung mit React sowie Docker und Kubernetes. Du weißt, wie moderne verteilte...

- agreed label: `docker` · required · raw_text: "sowie Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 74. golden_052 - skill `javascript` (spot-check)

> ...Tiefgreifende Node.js /TypeScript DNA: Du hast mehrjährige Erfahrung mit JavaScript/TypeScript (inkl. Node.js im Backend) und verstehst, was unter der...

- agreed label: `javascript` · required · raw_text: "Erfahrung mit JavaScript/TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 75. golden_052 - skill `kubernetes` (spot-check)

> ...Development & Container: Erfahrung mit React sowie Docker und Kubernetes. Du weißt, wie moderne verteilte Anwendungen laufen....

- agreed label: `kubernetes` · required · raw_text: "und Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 76. golden_053 - skill `javascript` (spot-check)

> ...T-SQL oder Python ist wünschenswert - Kenntnisse in JavaScript, Java, Jenkins sowie in agilen Arbeitsmethoden sind von...

- agreed label: `javascript` · nice_to_have · raw_text: "JavaScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 77. golden_054 - attribute `german` (spot-check)

> AI Engineer / KI-Entwickler (m/w/d)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 78. golden_054 - skill `apis` (spot-check)

> ...Generative AI (Prompting, Fine-Tuning). - Erfahrung mit API-Entwicklung (REST) und Git-basierter Softwareentwicklung. - Grundverständnis...

- agreed label: `apis` · required · raw_text: "API-Entwicklung (REST)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 79. golden_054 - skill `llamaindex` (spot-check)

> ...in Python und modernen KI-Frameworks (z. B. LangChain, LlamaIndex). - Praxiserfahrung im Umgang mit LLMs und Generative AI...

- agreed label: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 80. golden_054 - skill `llms` (spot-check)

> ...B. LangChain, LlamaIndex). - Praxiserfahrung im Umgang mit LLMs und Generative AI (Prompting, Fine-Tuning). - Erfahrung mit API-Entwicklung...

- agreed label: `llms` · required · raw_text: "LLMs und Generative AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 81. golden_054 - skill `prompt-engineering` (spot-check)

> ...Praxiserfahrung im Umgang mit LLMs und Generative AI (Prompting, Fine-Tuning). - Erfahrung mit API-Entwicklung (REST) und...

- agreed label: `prompt-engineering` · required · raw_text: "Prompting"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 82. golden_054 - skill `python` (spot-check)

> ...Aufgabenbereich und in der Softwareentwicklung. - Kenntnisse in Python und modernen KI-Frameworks (z. B. LangChain,...

- agreed label: `python` · required · raw_text: "Kenntnisse in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 83. golden_054 - skill `software-engineering` (spot-check)

> ...Git-basierter Softwareentwicklung. - Grundverständnis von Software-Engineering-Prinzipien (Testing, CI/CD). - Ausgeprägte kommunikative Stärken...

- agreed label: `software-engineering` · required · raw_text: "Software-Engineering-Prinzipien"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_055 - attribute `german` (spot-check)

> AI & Automation Engineer – Life Sciences (all gender)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_055 - attribute `seniority` (spot-check)

> AI & Automation Engineer – Life Sciences (all gender)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_055 - skill `apis` (spot-check)

> ...in Python, JavaScript oder TypeScript und Erfahrung mit REST APIs, JSON oder Webhooks - kennst dich aus mit Azure, Azure AI...

- agreed label: `apis` · required · raw_text: "REST APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_055 - skill `llms` (spot-check)

> ...Power Automate oder vergleichbaren Plattformen - bringst Erfahrung mit LLMs, Prompt Engineering oder RAG-Ansätzen mit - hast Interesse...

- agreed label: `llms` · required · raw_text: "Erfahrung mit LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_055 - skill `n8n` (spot-check)

> ...über Kenntnisse in Workflow Automation, beispielsweise n8n, Microsoft Power Automate oder vergleichbaren...

- agreed label: `n8n` · required · raw_text: "n8n"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_055 - skill `prompt-engineering` (spot-check)

> ...oder vergleichbaren Plattformen - bringst Erfahrung mit LLMs, Prompt Engineering oder RAG-Ansätzen mit - hast Interesse an Conversational...

- agreed label: `prompt-engineering` · required · raw_text: "LLMs, Prompt Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_055 - skill `python` (spot-check)

> ...GenAI oder Prozessautomatisierung mit - hast Kenntnisse in Python, JavaScript oder TypeScript und Erfahrung mit REST APIs,...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_056 - attribute `degree` (spot-check)

> ...Munich, Germany; London, UK. Minimum qualifications: Bachelor's degree in Computer Science, a related field, or equivalent practical experience. 7 years of experience in software or data engineering,...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Bachelor's degree in Computer Science, a related field, or equivalent practical experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_056 - attribute `german` (spot-check)

> AI Innovation Engineer, Deutsche Borse Group, Google Cloud

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_056 - skill `crewai` (spot-check)

> ...orchestration utilizing frameworks (e.g., LangChain, CrewAI, or Vertex AI Agent Builder) and vector...

- agreed label: `crewai` · required · raw_text: "CrewAI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_056 - skill `data-modeling` (spot-check)

> ..."explainable AI" requirements in banking. Experience with data modeling of relational, NoSQL, and analytical data modeling (Star...

- agreed label: `data-modeling` · nice_to_have · raw_text: "data modeling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_056 - skill `deep-learning` (spot-check)

> ...design. Experience using machine learning methodologies (deep learning, reinforced learning), model identification, selection and...

- agreed label: `deep-learning` · required · raw_text: "deep learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_056 - skill `explainable-ai` (spot-check)

> ...data residency, encryption at rest/transit (CMEK), and "explainable AI" requirements in banking. Experience with data modeling of...

- agreed label: `explainable-ai` · nice_to_have · raw_text: "explainable AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_056 - skill `llms` (spot-check)

> ...AI operations (e.g., model monitoring). Experience using Generative AI and agentic orchestration utilizing frameworks (e.g.,...

- agreed label: `llms` · required · raw_text: "Generative AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_056 - skill `model-selection` (spot-check)

> ...methodologies (deep learning, reinforced learning), model identification, selection and AI operations (e.g., model monitoring). Experience...

- agreed label: `model-selection` · required · raw_text: "model identification, selection"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_056 - skill `observability` (spot-check)

> ...model identification, selection and AI operations (e.g., model monitoring). Experience using Generative AI and agentic orchestration...

- agreed label: `observability` · required · raw_text: "model monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_056 - skill `python` (spot-check)

> ...including one or more programming languages (e.g., Python, Go, Java), and with design patterns, testing frameworks,...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_056 - skill `software-engineering` (spot-check)

> ...equivalent practical experience. 7 years of experience in software or data engineering, including one or more programming languages (e.g.,...

- agreed label: `software-engineering` · required · raw_text: "software or data engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_056 - skill `vector-databases` (spot-check)

> ...(e.g., LangChain, CrewAI, or Vertex AI Agent Builder) and vector databases. Preferred qualifications: Experience in financial...

- agreed label: `vector-databases` · required · raw_text: "vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_058 - attribute `degree` (spot-check)

> Agentic AI Software Engineer (m/w/d) | Frankfurt | 80% Remote | JBA15245

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_058 - attribute `seniority` (spot-check)

> Agentic AI Software Engineer (m/w/d) | Frankfurt | 80% Remote | JBA15245

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_059 - attribute `degree` (spot-check)

> ...Ownern und Entwicklungsteams **Anforderungen:** - Abgeschlossenes IT-Studium oder vergleichbare Qualifikation - Fundierte Erfahrung im Software Engineering,...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossenes IT-Studium oder vergleichbare Qualifikation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_059 - attribute `german` (spot-check)

> ...Product Mindset sowie Team- und Kommunikationsfähigkeit - Verhandlungssichere Deutsch- und gute Englischkenntnisse Aufgrund von Kundenvorgaben wird eine projektbezogene...

- agreed label: value="required" · basis="stated" · signal="Verhandlungssichere Deutsch- und gute Englischkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_059 - skill `ai-developer-tooling` (spot-check)

> ...KI-Agenten und deren Orchestrierung - Praxis im Einsatz agentischer Entwicklungstools, z. B. Claude Code, Cursor oder vergleichbare Lösungen -...

- agreed label: `ai-developer-tooling` · required · raw_text: "agentischer Entwicklungstools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_059 - skill `aws` (spot-check)

> ...Cursor oder vergleichbare Lösungen - Cloud-Erfahrung, idealerweise AWS, sowie Kenntnisse in Infrastructure as Code - Erfahrung im...

- agreed label: `aws` · nice_to_have · raw_text: "idealerweise AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_059 - skill `ci-cd` (spot-check)

> ...Fundierte Erfahrung im Software Engineering, Architekturdesign und CI/CD - Praktische Programmierkenntnisse in Python, TypeScript...

- agreed label: `ci-cd` · required · raw_text: "Architekturdesign und CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_059 - skill `cloud` (spot-check)

> ...z. B. Claude Code, Cursor oder vergleichbare Lösungen - Cloud-Erfahrung, idealerweise AWS, sowie Kenntnisse in Infrastructure as...

- agreed label: `cloud` · required · raw_text: "Cloud-Erfahrung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_059 - skill `infrastructure-as-code` (spot-check)

> ...Lösungen - Cloud-Erfahrung, idealerweise AWS, sowie Kenntnisse in Infrastructure as Code - Erfahrung im Data Engineering, idealerweise mit AWS Glue...

- agreed label: `infrastructure-as-code` · required · raw_text: "Kenntnisse in Infrastructure as Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_059 - skill `python` (spot-check)

> ...und CI/CD - Praktische Programmierkenntnisse in Python, TypeScript oder Java - Erfahrung mit KI-Agenten und deren...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_059 - skill `software-architecture` (spot-check)

> ...Fundierte Erfahrung im Software Engineering, Architekturdesign und CI/CD - Praktische Programmierkenntnisse in Python,...

- agreed label: `software-architecture` · required · raw_text: "Architekturdesign"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_059 - skill `software-engineering` (spot-check)

> ...IT-Studium oder vergleichbare Qualifikation - Fundierte Erfahrung im Software Engineering, Architekturdesign und CI/CD - Praktische...

- agreed label: `software-engineering` · required · raw_text: "Erfahrung im Software Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_059 - skill `typescript` (spot-check)

> ...und CI/CD - Praktische Programmierkenntnisse in Python, TypeScript oder Java - Erfahrung mit KI-Agenten und deren...

- agreed label: `typescript` · required · raw_text: "TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_060 - attribute `german` (spot-check)

> AI Innovation Engineer, Google Cloud

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_060 - attribute `seniority` (spot-check)

> ...a related field, or equivalent practical experience. 6 years of experience in software or data engineering. Experience solving real-world problems using machine...

- agreed label: value="senior" · basis="inferred" · signal="6 years of experience in software or data engineering."

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_060 - skill `deep-learning` (spot-check)

> ...real-world problems using machine learning methodologies (deep learning, reinforced learning), model identification, selection and...

- agreed label: `deep-learning` · required · raw_text: "deep learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_060 - skill `devops` (spot-check)

> ...(Star Schema, Data Vault, etc.). Experience working in a high-maturity DevOps culture (trunk-based development, automated testing, blue/green...

- agreed label: `devops` · nice_to_have · raw_text: "high-maturity DevOps culture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_060 - skill `explainable-ai` (spot-check)

> ...and data residency, encryption at rest/transit (CMEK), and "explainable AI" requirements in banking. Experience with data modeling of...

- agreed label: `explainable-ai` · nice_to_have · raw_text: "\"explainable AI\""

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_060 - skill `llms` (spot-check)

> ...monitoring). Experience solving real-world problems using Generative AI and agentic orchestration utilizing frameworks (e.g.,...

- agreed label: `llms` · required · raw_text: "Generative AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_060 - skill `machine-learning` (spot-check)

> ...engineering. Experience solving real-world problems using machine learning methodologies (deep learning, reinforced learning), model...

- agreed label: `machine-learning` · required · raw_text: "machine learning methodologies"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_060 - skill `observability` (spot-check)

> ...model identification, selection and AI operations (e.g., model monitoring). Experience solving real-world problems using Generative...

- agreed label: `observability` · required · raw_text: "model monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_060 - skill `python` (spot-check)

> ...with one of the following programming languages: Python, Go, or Java. Experience with design patterns, testing...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_060 - skill `testing` (spot-check)

> ...Python, Go, or Java. Experience with design patterns, testing frameworks, and API contract design. Preferred...

- agreed label: `testing` · required · raw_text: "testing frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_061 - attribute `degree` (spot-check)

> Für den Standort Frankfurt am Main suchen wir:

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_061 - attribute `german` (spot-check)

> ...an Security, Datenschutz und Compliance von Vorteil. - Sehr gute Deutschkenntnisse (C1 oder höher). - Ausgeprägte Abstraktionsfähigkeit, analytisches Denken...

- agreed label: value="required" · basis="stated" · signal="Sehr gute Deutschkenntnisse (C1 oder höher)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_061 - skill `claude-code` (spot-check)

> ...der Softwareentwicklung, z. B. Kiro CLI, GitHub Copilot, Claude Code oder Cursor. - Mehrjährige Erfahrung in Wissensvermittlung...

- agreed label: `claude-code` · required · raw_text: "Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_061 - skill `cursor` (spot-check)

> ...z. B. Kiro CLI, GitHub Copilot, Claude Code oder Cursor. - Mehrjährige Erfahrung in Wissensvermittlung und...

- agreed label: `cursor` · required · raw_text: "Cursor"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_061 - skill `embeddings` (spot-check)

> ...IT-Umfeld. - Sicheres Verständnis von LLM, Context Window, Embeddings, RAG, Tool Calling, Agenten, Orchestrierung, Guardrails,...

- agreed label: `embeddings` · required · raw_text: "Embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_061 - skill `evaluation` (spot-check)

> ...Agenten, Orchestrierung, Guardrails, Prompt Injection, Evaluation, Halluzinationen und Kosten je Token. - Erfahrung darin,...

- agreed label: `evaluation` · required · raw_text: "Evaluation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_061 - skill `llm-guardrails` (spot-check)

> ...Embeddings, RAG, Tool Calling, Agenten, Orchestrierung, Guardrails, Prompt Injection, Evaluation, Halluzinationen und Kosten...

- agreed label: `llm-guardrails` · required · raw_text: "Guardrails"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_061 - skill `llms` (spot-check)

> ...und Beratung im IT-Umfeld. - Sicheres Verständnis von LLM, Context Window, Embeddings, RAG, Tool Calling, Agenten,...

- agreed label: `llms` · required · raw_text: "LLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_061 - skill `mcp` (spot-check)

> ...und des end-to-end SDLC. - Praktische Erfahrung mit MCP-Servern und agentischen Skills. - Mindestens 12 Monate...

- agreed label: `mcp` · required · raw_text: "MCP-Servern"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
