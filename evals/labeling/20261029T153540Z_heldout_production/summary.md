# Held-out production labels, two blind labelers — 20261029T153540Z_heldout_production

- labeler A: `claude-opus-5-5` (anthropic)
- labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded from labeling): `claude-sonnet-5-5`
- rules: DECISIONS.md 2026-10-28 rule bullets, sha256 `9ccf26aac331`
- prompt sha256: `d3440ff6a7e5`

Nothing here is applied. Agreement is a proposal; a person decides.

## Side by side

| posting | labeler A | labeler B | state |
|---|---|---|---|
| golden_021 | null (not mentioned) | null (not mentioned) | agree · uncertain |
| golden_022 | null (not mentioned) | null (not mentioned) | agree |
| golden_023 | null (not mentioned) | null (not mentioned) | agree · uncertain |
| golden_024 | nice_to_have — "Erfahrung mit dem Betrieb, der Überwach…" | null (not mentioned) | DISAGREE · uncertain |

## Agreed (3)

### golden_021
- **labeler A** — null (not mentioned)
  - why: Every production mention ('models that run in production', 'from first idea to production') is a responsibility, so it is not mentioned under PRINCIPLES rule 1. The bonus 'a system you built and fixed yourself when it broke' never says production or real users, so on a literal reading it is not a production demand.
  - **flagged uncertain by the labeler**
- **labeler B** — null (not mentioned)
  - why: The responsibilities exclusion applies: production work describes what the hire will do, while shipped ML experience describes existing teammates; no candidate qualification demands production work.

### golden_022
- **labeler A** — null (not mentioned)
  - why: The only production mention, 'der Weg vom Prototyp in die Produktion', is a responsibility (excluded per PRINCIPLES rule 1). The qualifications ask only for 'Erste praktische Erfahrung' and tool skills, with no demand to ship or operate software.
- **labeler B** — null (not mentioned)
  - why: Die Produktionsnennung unter „Aufgaben“ ist eine Verantwortung; nach der Verantwortlichkeiten-Regel ist sie keine Anforderung an Produktionserfahrung der Kandidat:innen.

### golden_023
- **labeler A** — null (not mentioned)
  - why: Every production mention is a responsibility (rule 1 exclusion). 'Expert:in für ... das Deployment von Machine-Learning-Modellen' describes the role, and the knowledge-of-production rule (golden_005) does not count expertise as a demand to have shipped or run systems. There is no requirements section.
  - **flagged uncertain by the labeler**
- **labeler B** — null (not mentioned)
  - why: Die Aussagen zu Implementierung, Deployment und Bereitstellung stehen unter „Was du bei uns bewegen kannst“ und beschreiben Verantwortlichkeiten; diese zählen nach der Verantwortlichkeiten-Regel nicht als Produktionsanforderung an Kandidat:innen.

## Disagreement — needs a decision (1)

### golden_024
- **labeler A** — nice_to_have — "Erfahrung mit dem Betrieb, der Überwachung oder der Fehlerbehebung bei einem ML-Modell oder einer Datenpipeline."
  - why: Operating ('Betrieb') an ML model or pipeline is the operate/run demand, and it sits under 'Was du idealerweise noch mitbringst', so it is optional. The must-haves only ask for 'Interesse daran zu lernen' and first development experience, and the production phrases under 'Was dich erwartet' are responsibilities.
  - **flagged uncertain by the labeler**
- **labeler B** — null (not mentioned)
  - why: Wörtliche Auslegung: Die optionale Betriebserfahrung nennt keinen produktiven Einsatz; Interesse am Lernen ist keine Betriebserfahrung, und die ausdrücklichen Produktionsbezüge stehen unter Verantwortlichkeiten.
  - **flagged uncertain by the labeler**

## Auto-check failures (0)

None.

## Flagged uncertain (3)

### golden_021
- **labeler A** — null (not mentioned)
  - why: Every production mention ('models that run in production', 'from first idea to production') is a responsibility, so it is not mentioned under PRINCIPLES rule 1. The bonus 'a system you built and fixed yourself when it broke' never says production or real users, so on a literal reading it is not a production demand.
  - **flagged uncertain by the labeler**
- **labeler B** — null (not mentioned)
  - why: The responsibilities exclusion applies: production work describes what the hire will do, while shipped ML experience describes existing teammates; no candidate qualification demands production work.

### golden_023
- **labeler A** — null (not mentioned)
  - why: Every production mention is a responsibility (rule 1 exclusion). 'Expert:in für ... das Deployment von Machine-Learning-Modellen' describes the role, and the knowledge-of-production rule (golden_005) does not count expertise as a demand to have shipped or run systems. There is no requirements section.
  - **flagged uncertain by the labeler**
- **labeler B** — null (not mentioned)
  - why: Die Aussagen zu Implementierung, Deployment und Bereitstellung stehen unter „Was du bei uns bewegen kannst“ und beschreiben Verantwortlichkeiten; diese zählen nach der Verantwortlichkeiten-Regel nicht als Produktionsanforderung an Kandidat:innen.

### golden_024
- **labeler A** — nice_to_have — "Erfahrung mit dem Betrieb, der Überwachung oder der Fehlerbehebung bei einem ML-Modell oder einer Datenpipeline."
  - why: Operating ('Betrieb') an ML model or pipeline is the operate/run demand, and it sits under 'Was du idealerweise noch mitbringst', so it is optional. The must-haves only ask for 'Interesse daran zu lernen' and first development experience, and the production phrases under 'Was dich erwartet' are responsibilities.
  - **flagged uncertain by the labeler**
- **labeler B** — null (not mentioned)
  - why: Wörtliche Auslegung: Die optionale Betriebserfahrung nennt keinen produktiven Einsatz; Interesse am Lernen ist keine Betriebserfahrung, und die ausdrücklichen Produktionsbezüge stehen unter Verantwortlichkeiten.
  - **flagged uncertain by the labeler**
