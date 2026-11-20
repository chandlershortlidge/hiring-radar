## 2026-11-19 — Chicago and San Jose get their board search: Chicago adds none, San Jose adds 11 (HIR-361)

HIR-302 launched Chicago and San Jose without their company-board search, because Brave
(the search engine that search uses) had run out of November's credit. Chandler topped
the account up on 19 Nov ("brave should be topped up now", the ticket's **Answered**
comment), so the search ran the same day instead of waiting for 1 Dec. Brave answered
all 140 searches of each launch.

The board policy is unchanged (2026-11-03, HIR-132): add an employer board with 5 or more
AI roles in the city being launched, skip agencies and aggregators, record nothing else.

| city | boards judged | added | one-time reading | postings/day added |
| -- | -- | -- | -- | -- |
| Chicago | 577 | none (the best board, EvolutionIQ, had 4 roles there) | €0 | 0 |
| San Jose | 577 | 11 (board names as in the feed list): applied, wayve, samsungsemiconductor, figureai, okx, etched, zscaler, roku, archer56, xai, floqast | €1.73 | 2,063 |

**First poll of San Jose's 11 boards** (local copy of the database): 2,063 postings seen,
94 new jobs stored, 84 of them in San Jose; 20 merged into jobs already stored from other
sources. Crediting stored jobs whose postings already named the city added 32 to San
Jose and 5 to Chicago on that copy; the server's stored jobs are credited by HIR-362.

Chicago therefore stays fed by its two Google for Jobs searches and multi-city postings.
Its nearest boards (evolutioniq 4 roles, drweng 3, braze 3) are under the line.

**Undo:** remove the 11 lines from `config/feeds.json`. Jobs already stored from them stay
and close as they stop being seen.
