## 2026-11-19 — Austin, Boston, London and Amsterdam are collected, on company boards only (HIR-252)

Chandler named these four cities on the HIR-252 ticket, so the 2026-11-03 rule (HIR-132)
applies as written: a city he has named is launched by the automated path, and neither it
nor its boards waits on approval. `geo.ACTIVE_CITIES` now ends `"Austin", "Boston",
"London", "Amsterdam"`, each collected since 2026-11-19. The dashboard's place list gains
two headings, "United Kingdom" and "Netherlands".

**What the four launches added.** The board policy (add an employer board with 5 or more AI
roles in the city being launched, skip agencies and aggregators) applied to each:

| city | boards judged | added | one-time reading | postings/day added |
| -- | -- | -- | -- | -- |
| Austin | 377 | 4: Tenstorrent, Avride, Striveworks, webAI | €0.58 | 237 |
| Boston | 426 | 1: Flagship Pioneering | €0.17 | 101 |
| London | 465 | 7: Faculty, Bjak, Mistral AI, Monzo, Graphcore, Deliveroo, Indicium | €1.79 | 2,423 |
| Amsterdam | 484 | 1: Prosus | €0.15 | 19 |

No cap was reached (€10 of one-time reading and 5,000 postings a day, per city).

**No country-wide search was added, though the ticket asked for one for the US cities.**
Google for Jobs (the JSearch feed) is on a free plan with a hard 200 requests a month, and
the five searches we run use about 150 (2026-11-12, HIR-255: "any further JSearch feed needs
this sum redone"). Two searches per new city would need about 390. Going over switches off
every search, Berlin's and New York's included, until the month resets. The rule beat the
ticket; the rules agent confirmed it. HIR-352 holds the three ways out, two of which are
Chandler's (a paid source, or moving searches away from Berlin or New York). Until then
Boston and Amsterdam rest mostly on one employer each, and will grow slowly, as New York did
before HIR-255. The other existing country-wide feeds add nothing here: startup.jobs is
searched for Germany only, and arbeitnow returned no Amsterdam posting.

**Which places count as each city.** "Cambridge, MA" is Boston, the way the Bay Area is San
Francisco; Cambridge in England is not. "London, Ontario", "London, ON", "London, Canada"
and "New London, CT" are not London; the province code is matched in capitals only, so
"London, on-site" still is. A bare "London, Canada" is lost if an office list ever writes
"London, Canada, US"; that is rarer than the Ontario city. "Amsterdam, Noord-Holland" and
"Amsterdam-Zuidoost" are Amsterdam. Tests pin each.

**Dutch postings read well, so Amsterdam was turned on.** The ticket asked to stop before
Amsterdam if Dutch reading was poor. None of Amsterdam's first 13 postings is in Dutch, so
five real Dutch postings from Dutch employers' boards (an ML engineer, three data
engineers, an advertising data role) were read by the production extractor and stored
nowhere. Skills and their quotes came back correct and verbatim in Dutch, no posting was
read as asking for German, the degree line "hbo- of wo-opleiding" read as a required
bachelor's, and the advertising role correctly got no technical skills. Of 33,392 postings
read from the boards Amsterdam's launch looked at, 104 were Dutch-language postings in the
Netherlands, and almost none were AI roles: Dutch will be rare on the Amsterdam chart.

**The launch quality check.** Each city's sample was labelled by the same two-model panel
(Claude Opus and GPT) as the run it is measured against. New York's run also had a third
labeller, so the script prints an uneven-panel warning on the US comparison against New
York; San Francisco's is the clean one.

| city | postings scored | F1 | against |
| -- | -- | -- | -- |
| Austin | 14 of 15 | 0.979 | San Francisco 0.897 (+0.082); New York 0.940 (+0.039, uneven panel) |
| Boston | 9 of 9 | 0.898 | San Francisco 0.897 (+0.001); New York 0.940 (−0.042, uneven panel) |
| London | 14 of 15 | 0.961 | Berlin 0.926 (+0.035) |
| Amsterdam | 13 of 13 | 0.948 | Berlin 0.926 (+0.022) |

None is clearly worse (the check's line is 0.05). Boston is the weakest on precision
(0.815): the extractor adds about two skills per posting the panel did not agree on, on a
sample of 9 postings nearly all from one employer. Too small to act on.

**What the new cities ask for that the chart cannot show.** Austin's boards are chip design
(physical design, static timing analysis, SystemVerilog) as much as AI; Austin and Boston
add reinforcement learning and robotics; London adds AI safety and evaluation. HIR-351 is
the batch review, due 22 Nov.

**Undo:** revert the PR. No migration and nothing deleted; postings already stored for the
four cities stop being shown, because an inactive city is filtered out of every query.
