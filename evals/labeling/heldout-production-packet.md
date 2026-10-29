# Held-out labeling packet — production experience (golden_021–024)

Source of the rules: `DECISIONS.md`, entry dated 2026-10-28, reproduced verbatim and in
full below (its rule bullets were revised 2026-10-29; this is the current text). Source of
the postings: the `job_description` field of `evals/goldens/golden_021.json` …
`golden_024.json`, reproduced verbatim. Nothing in this packet comes from `app/extract.py`
or from any predictions file.

---

## 1. The definition and the rules, verbatim

## 2026-10-28 — Production experience is a fourth per-job attribute, not a skill (HIR-69)

Does the posting **demand production work of the candidate — shipping or operating
software that real users depend on?** `required | nice_to_have | not mentioned`, with a
quoted signal — the German shape, in migration 013.

Not a skill: the taxonomy excludes work practices, and "production" or "produktiv" appears
in 168 of 243 stored descriptions, so as a skill it would sit atop every chart and measure
nothing. This is the first entry of HIR-59's role-demands vocabulary and answers HIR-35 for
this one practice.

Rule bullets revised 2026-10-29 — see that entry for what changed and why.

- **The line is the verb, not the tense.** A demand to build, ship, operate, deploy or run
  software in production is `required` in any tense or modality — "you have shipped
  production systems", "experience building production AI systems", "able to ship
  production-quality agentic systems", "track record of building and running production
  services", "commercial software engineering experience in production environments". A
  past record, a present ability and a stated expectation are the same demand; *build*
  alone carries it; and a hyphenated modifier on the object (production-grade,
  production-ready, production-oriented) does not weaken it.
- `nice_to_have`: that same demand marked optional. The marker may be explicit —
  "experience with production ML is a plus", "ideally…" — or soft phrasing that frames the
  demand as welcome rather than expected ("production ML would be highly relevant",
  golden_011).
- **Not mentioned** when the posting never asks the candidate for it. Most mentions of the
  word are responsibilities ("you'll deploy models to production", "turn prototypes into
  production-ready systems", "from idea to production"), and PRINCIPLES rule 1 already
  excludes responsibilities for technologies — the same rule applies here.
- **A quality bar on the code itself is not the demand**: "write production-grade code",
  "strong Python skills, including writing production-quality code and tests" → not
  mentioned. The attribute measures a demand to ship or run the software, not a standard
  for the code to be written. The verb is the test: *build*, *ship*, *operate*, *deploy*,
  *run* → `required`; *write*, *code to* a production standard → not mentioned. The corpus carries
  both one clause apart — golden_018 has each — so the verb decides, not the tense.
- **Knowledge of production is not a demand to have done production work.** "Knowledge of
  MLOps and the structured operation of AI models in production environments" (golden_006),
  "deep knowledge of … deployment and monitoring" (golden_005) → not mentioned. What the
  candidate is asked to *know about* is not what they are asked to have built or run.
- **A demand scoped to one seniority level is not a job-wide demand.** A posting open to
  several levels that asks for production experience only under a level heading
  ("Senior Level: several years … in the design and operation of productive AI systems")
  is not mentioned: the track the posting opens to a junior carries no such demand, and
  `production=not_required` has to keep showing that posting to a junior. golden_006 is the
  reference case.
- German postings: `required` on "Du hast bereits Produkte … in den produktiven Betrieb
  gebracht", "Erfahrung mit produktiven AI-Anwendungen, nicht nur Prototypen". Not mentioned
  on the common "von der Idee bis zum produktiven Einsatz" responsibility phrasing.
- **No `inferred` basis.** `production_basis` only ever holds `stated`: unlike German,
  nothing about the posting's own form implies the demand. The validation rule is otherwise
  German's — a value whose quoted signal is not found in the text collapses to not
  mentioned.

Amends the 2026-10-18 rule "three is the limit": column groups on `job` stay the pattern
through four demands. The fifth demand migrates all four groups into `job_requirement` in
one migration before it is added.

Filters mirror German's four keys exactly (`any | none | not_required | required`), because
`not_required` — not mentioned *or* nice_to_have — is the key the dashboard's headline set
needs and the ticket's proposed `nice_to_have`-only key is not asked for anywhere.

Why it matters: junior + German not required + production not required ≈ "jobs you can get
today", the set HIR-51's ranking should start from, and the number the Advisor (HIR-63)
needs to say how many doors a first production project opens.

Goldens, eval scoring and re-extraction are a separate change; `evals/LABELING.md` is frozen
and gains its `## Production experience` section there, with the relabeling, as a release
decision (2026-10-16).

---

## 2. Output format

Label all four postings. For each one, in this order, answer with exactly these three
lines and nothing else:

```
golden_0NN
class:  required | nice_to_have | none
signal: <the verbatim clause from the posting>   — or the word: none
why:    <one line>
```

Constraints on the answer:

- `class` is exactly one of `required`, `nice_to_have`, `none`. `none` means the posting
  does not mention the demand at all, i.e. not mentioned.
- `signal` must be copied **character for character** from that posting's text, as a
  contiguous substring. Do not paraphrase, do not normalise punctuation, do not join two
  separate clauses. Quote the clause that carries the demand, not the sentence around it.
  Keep the original language — a German posting gets a German signal.
- When `class` is `none`, `signal` is the word `none`.
- When one posting carries several candidate clauses, quote the single clause the class
  rests on.
- `why` is one line, referring to the rule that decided it.
- Label each posting only from its own text. Do not use the other three postings, and do
  not assume the four are meant to be spread across the classes.

---

## 3. The four postings, verbatim

Each posting is reproduced exactly as stored, in its original language, with no
highlighting and no commentary. Markdown artifacts (stray `*`, `##`, links) are present in
the stored text and are not labels or emphasis added here.


### golden_021

```text
Junior Data Scientist

This isn’t your regular job. Almedia is a place where those who want to push harder can accelerate their careers faster than anywhere else. We’re aiming to become Germany’s second bootstrapped unicorn. Almedia is already Europe’s #3 fastest-growing company in 2025 (FT1000).

We are building the future of marketing by rewarding our community of over 95 million users for engaging with our advertisers’ products. We are offering a new way to acquire users for the biggest companies in the world.

Berlin, On-site

€60K – €85K + Equity

Most Junior Data Scientists spend their first years building dashboards and reporting on what already happened. Here, you'll work on models that run in production and shape what millions of users see every day.

You'll join a small team of people who have built and shipped ML systems at scale, and learn from them directly. You get real problems from week one, and the support to solve them. Show us you can own more, and we'll give you more.

 

What You'll Do 🎯

-
Build models that predict user value, engagement and reward behaviour, and see them live in our product

-
Run A/B tests on offers, rewards and ranking, and work out what actually caused the result

-
Build and fix the data pipelines your models depend on

-
Take on new problems with no playbook yet, from first idea to production

 

What You'll Bring 💡

-
Strong Python and SQL. You use AI tools to move faster, and you still check the output

-
You get going on a vague problem without waiting for a spec, and you take it further than you were asked

-
You quickly see which number matters and which question to answer first

-
Proof that you aim high: a project, result or choice where you went past "good enough" when nobody asked you to

-
Bonus: a strong result in a Kaggle challenge, hackathon or competition, or a system you built and fixed yourself when it broke

 

Why Almedia

-
A small, selective team of very sharp people. We keep it small on purpose, so every hire raises the bar

-
Equity in Almedia. Every Berlin-based employee gets a stake, so you share in what you help build

-
Top-of-market pay as the baseline. Outlier impact gets paid accordingly

 

Small team, high bar. If that sounds like home, apply.

 

 

We believe in fostering talent, evaluating all skill levels during the hiring process, and providing a clear path for growth. Almedia is an equal opportunity employer. We embrace and celebrate diversity, and encourage individuals from all backgrounds to apply.

Compensation: €60K – €85K • Exceptional commitment deserves exceptional reward

- • €60K – €85K • Exceptional commitment deserves exceptional reward

Find more English Speaking Jobs in Germany on Arbeitnow
```

### golden_022

```text
Limebit ist ein Berliner Beratungsunternehmen für Data Science und Machine Learning im Gesundheitswesen. Seit zehn Jahren arbeiten wir mit Krankenkassen, Klinikgruppen, Forschungseinrichtungen und Pharmaunternehmen daran, aus Medizindaten belastbare Erkenntnisse und produktive Anwendungen zu machen.

**Unser Team aus Data Scientists, ML Engineers, Mathematiker:innen und Softwareentwickler:innen wächst weiter. Wir suchen eine Person mit erster Praxiserfahrung, die mit uns an anspruchsvollen Kundenprojekten arbeitet und sich bei uns fachlich weiterentwickeln will.**

Bei uns zählen ein wertschätzendes Miteinander, flache Hierarchien und eine selbstständige, verantwortungsbewusste Arbeitsweise.

## Aufgaben

Du arbeitest gemeinsam mit uns an Projekten für Kunden aus dem Gesundheitswesen, zum Beispiel:

* Analysen und ML-Modelle auf echten Versorgungsdaten wie GKV-Abrechnungsdaten, Krankenhausdaten oder Krebsregisterdaten
* Real-World-Evidence-Studien für Pharmaunternehmen, inklusive Überlebenszeitanalysen
* Prüf- und Scoring-Modelle für Krankenkassen, auch mit NLP auf unstrukturierten Texten
* Entwicklung von Datenpipelines und der Weg vom Prototyp in die Produktion
* Softwaredevelopment mit gängigen Machine Learning und Statistik Bibliotheken (scikit-learn, SciPy, NumPy, Pandas, PyTorch, Tensorflow etc.) und typischen Development-Tools (Git, GitFlow, GitHub, GitLab, Jira)
* Literaturrecherche und Umsetzung neuer Methoden als Prototyp
* Abstimmung mit Fachexpert:innen auf Kundenseite und Präsentation von Ergebnissen
* Optional: Lehrtätigkeiten im Bereich Data Science und Programmierung

## Qualifikation

**Das bringst du mit:**

* Abgeschlossenes Studium in Data Science, Informatik, Mathematik, Statistik, Physik, Bioinformatik oder einem vergleichbaren Fach, alternativ vergleichbare Praxiserfahrung
* Erste praktische Erfahrung, z. B. aus Projekten oder ersten Berufsjahren
* Sicherer Umgang mit **Python** und gängigen Bibliotheken (z. B. _pandas oder Polars, NumPy, SciPy, scikit-learn, PyTorch_) sowie SQL
* Solides Verständnis **statistischer Methoden und ML-Verfahren**
* Erfahrung mit Git und kollaborativer Entwicklung
* Sehr gute Deutschkenntnisse (mindestens C1), da unsere Kunden aus dem deutschen Gesundheitswesen und öffentlichen Umfeld kommen, sowie gute Englischkenntnisse

**Ein zusätzliches Plus gibt's für:**

* Erfahrung mit Gesundheitsdaten
* Survival Analysis oder kausale Inferenz
* R, Rust, Kubernetes oder Airflow

## Benefits

**Benefits**

* Flexibles Arbeiten: 2-3 Tage Home Office pro Woche
* Individuelle Weiterbildungsmöglichkeiten
* Erfahrenes Management, das jederzeit ansprechbar ist und dir früh Verantwortung überträgt
* Keine unbezahlten Überstunden, Mehrarbeit wird durch Freizeit ausgeglichen
* Edenred-Karte mit monatlichem Budget zur freien Verwendung
* Kostenloses Mittagessen, Getränke und Snacks im Büro
* MacBook als Arbeitsgerät
* 28 Urlaubstage

**Wer ist deine Ansprechpartner:in bei uns?**

Wir sind klein genug, dass du dich in jeder Situation auf Feedback und Unterstützung des ganzen Teams verlassen kannst. [Florian](https://www.linkedin.com/in/florian-richter-limebit/) und [Philipp](https://www.linkedin.com/in/philipp-gro%C3%9Fer/) werden dich einarbeiten, dir ein bisschen was über die Geschichte von Limebit erzählen, dir dein neues MacBook überreichen und dich ganz persönlich willkommen heißen. Danach arbeitet ihr als Team gemeinsam an Kundenprojekten.

Schick uns einfach deinen Lebenslauf, ein Anschreiben brauchen wir nicht. Wir freuen uns über alle Bewerbungen, unabhängig von Herkunft, Hautfarbe, Geschlecht, sexueller Orientierung, Religion, Alter oder Behinderung.
```

### golden_023

```text
Was du bei uns bewegen kannst
Gemeinsam mit deinem agilen, cross-funktionalen Projektteam hilfst du unseren Kunden aus unterschiedlichen Branchen, ihre Daten nutzbar zu machen.
Dein Job beginnt nicht erst mit der Entwicklung von Datenprojekten: Du stimmst dich eng mit unseren Kunden ab und berätst sie in Bezug auf die technische Machbarkeit und die konkrete Umsetzung ihrer digitalen Innovationen.
Als Senior Data Engineer* / Machine Learning Engineer* gestaltest du das Fundament für spätere Analysen sowie data-driven Services und entwickelst skalierbare, robuste und wartbare Architekturen.
Du konzipierst und implementierst Datenplattformen, Datenverarbeitungsprozesse und Daten-Services als hochskalierbare, verteilte Systeme in der Cloud, on premise oder hybrid.
Du bist Expert:in für die Ende-zu-Ende-Integration von Daten- / ETL-Pipelines und das Deployment von Machine-Learning-Modellen bis hin zur Bereitstellung der Ergebnisse innerhalb bestehender IT-Systeme.
Als Architect oder Technical Lead bist du verantwortlich für die Auswahl und Implementierung geeigneter Technologien, die Sicherstellung der Datenintegrität und -sicherheit, sowie für die effektive Zusammenarbeit mit anderen Teams und Stakeholdern, um die Kundenziele durch datenbasierte Lösungen zu erreichen.

In unseren Projekten verwenden wir häufig folgende Technologien:
Python, SQL, Java
Relationale und NoSQL-Datenbanken
Flask oder FastAPI
Databricks, Spark, Kafka, Airflow, dbt, BigQuery oder Snowflake
AWS, GCP, Azure
Docker, Kubernetes
Intern wie extern kannst du dich bei uns auf vielfältige Art einbringen: Deinen anfangs gewählten Schwerpunkt kannst du jederzeit verlagern. Als Senior hast du außerdem die Möglichkeit, jüngere Kolleg:innen als Mentor:in oder Coach zu unterstützen.
```

### golden_024

```text
## Was du unbedingt mitbringst

- Solide Grundlagen in Machine-Learning-Konzepten und der Bewertung von Modellen, welche du durch dein Studium, eine Weiterbildung oder praktische bzw. berufliche Erfahrung gesammelt hast.
- Praktische Python-Kenntnisse und die Fähigkeit, klaren und gut wartbaren Code zu schreiben.
- Erste Berührungspunkte im Umgang mit Daten und SQL.
- Erste praktische Erfahrung bei der Entwicklung einer ML-Lösung.
- Interesse daran zu lernen, wie Modelle und Datenpipelines in Produktionsumgebungen bereitgestellt, überwacht und verbessert werden.
- Eine strukturierte Herangehensweise an die Problemlösung.
- Klare Kommunikationsfähigkeiten sowie eine offene und kooperative Arbeitsweise.
- Gute Englischkenntnisse für die tägliche Kommunikation.

## Was du idealerweise noch mitbringst

- Erste Erfahrungen mit Docker oder einem anderen Containerisierungstool.
- Erste Berührungspunkte mit AWS, GCP oder einer anderen Cloud-Plattform.
- Vertrautheit mit NLP, Anwendungen großer Sprachmodelle (LLMs) oder KI-Agenten.
- Erfahrung mit NoSQL-Datenbanken, verteilter Datenverarbeitung oder Streaming-Technologien.
- Grundkenntnisse gängiger Software-Engineering-Praktiken wie Versionskontrolle, Testing und Continuous Integration.
- Erfahrung mit dem Betrieb, der Überwachung oder der Fehlerbehebung bei einem ML-Modell oder einer Datenpipeline.

## Was dich erwartet

- Gemeinsam mit erfahrenen Kolleg:innen übersetzt du Produkt- und Geschäftsfragen in klar definierte Machine-Learning-Aufgaben.
- Du entwickelst, evaluierst und verbesserst Machine-Learning-Modelle mit Python.
- Du trägst zu reproduzierbaren Daten- und ML-Pipelines bei – von ersten Experimenten bis zur Bereitstellung in der Produktion.
- Du bereitest Services oder Batch-Jobs mithilfe von Tools wie Docker für den produktiven Einsatz vor.
- Du arbeitest mit cloudbasierten ML-Umgebungen in AWS oder GCP.
- Du nutzt SQL, um Daten zu untersuchen, aufzubereiten und zu validieren.
- Du überwachst die Performance von Modellen, gehst möglichen Problemen auf den Grund und trägst dazu bei, die Zuverlässigkeit unserer produktiven Lösungen kontinuierlich zu verbessern.
- Du dokumentierst deine Arbeit sowie Annahmen, Abwägungen und Ergebnisse nachvollziehbar.
- Du arbeitest eng mit Kolleg:innen aus Data Engineering, Software Engineering, Product und weiteren Unternehmensbereichen zusammen.
- Du berücksichtigst bei der Entwicklung und Bewertung von Lösungen Aspekte wie Modellqualität, Robustheit und Fairness.
```
