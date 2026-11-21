## 2026-11-20 — release check for switching to the cheaper model: its lead holds on the sealed postings (HIR-383)

Three rounds of instruction changes (HIR-368) were all measured on the same 71 development
postings, so some of Claude Haiku 5.5's gain over Claude Sonnet 5.5 could have been fitted
to those postings. This is the one check on the 60 sealed (held-out) postings that nobody
has tuned against. Both models ran with the round-3 instructions
(`evals/experiments/trials/hir-368-round-3.md`), three readings per posting. Haiku ran at an
8192-token output cap, as in HIR-368; Sonnet at the live 4096. Nothing was changed because of
the sealed results.

| | Sonnet, dev | Haiku, dev | Sonnet, sealed | Haiku, sealed |
|---|---|---|---|---|
| skill F1 | 0.906 | 0.927 | 0.922 | **0.945** |
| precision | 0.903 | 0.941 | 0.957 | 0.974 |
| recall | 0.908 | 0.913 | 0.889 | 0.917 |
| required vs nice-to-have | 0.955 | 0.944 | 0.977 | 0.981 |
| seniority | 0.972 | 0.958 | 0.906 | 0.883 |
| production (dev 20 postings, sealed 4) | 0.917 | 0.900 | 1.000 | 0.750 |
| top-ten overlap | 9/10 | 9/10 | 7/10 | 7/10 |
| broad skills missed / added | 6 / 28 | 20 / 9 | 17 / 21 | 21 / 7 |
| cost per reading | $0.0159 | $0.0018 | $0.0167 | $0.0021 |

**Result: the lead holds.** Haiku's F1 lead is +0.021 on dev and +0.023 on sealed. Two of
Sonnet's 180 sealed readings (one posting, `golden_138`) hit Sonnet's live output cap and
returned nothing; without that posting Sonnet's sealed F1 is 0.936, so the like-for-like
lead is about +0.009: smaller, not flipped.

Where Haiku is weaker on the sealed set: seniority (0.883 vs 0.906, about one posting in
60 more wrong), the single nice-to-have production posting (missed in all three readings),
and the broad skill "cloud" (10 misses over 180 readings vs Sonnet's 2). These are recorded,
not fixed: a fix would have to come from patterns in the development set, or the sealed set
stops being an honest test.

Runs: `evals/experiments/20261120T171942Z_dev_x2-9b923cba1e` (Sonnet, dev),
`20261120T174218Z_heldout_x2-9b923cba1e` (Sonnet, sealed),
`20261120T174216Z_heldout_x2-848aaff6a5` (Haiku, sealed); Haiku dev is HIR-368's
`20261120T070628Z_dev_x2-6644e02806`.

The switch itself, and the one full re-read it needs, is a separate change and Chandler's
decision.
