## 2026-11-27 — The production-quote score is gated on flipped Goldens, not on 0.02 (HIR-169)

Chandler decided on 16 Nov (option 1 of three, confirmed in voice).

`production_signal_agreement` asks whether the model quoted the right sentence when it
said a job wants production experience. It is counted only on Goldens where the model and
the label agree on a production class, which is 8 or 9 postings per repeat in the current
dev set. One posting is about 12% of the score, so the 0.02 drop rule fired on any single
miss. In the run of 25 Nov it fell 0.042 — one quote, in one of three repeats — and the
gate called it a regression.

**Rule:** it joins the per-Golden attribute scores that HIR-164 moved onto counted flips
(DECISIONS 2026-11-04): more than 2 Goldens going from right to wrong stops the merge.

**Why:** the reason recorded for the other four applies word for word — one yes/no answer
per Golden, so a fraction cannot tell one unlucky posting from a regression. Waiting for
the set to grow (the original recommendation) would not have fixed it: the 28 Goldens
added since carry no production label, so the denominator is not growing.

**How a Golden counts:** it is scored only in the repeats where the model got the
production class right (a wrong class is already a miss on `production_accuracy`, not a
second one here). Its majority is taken over those repeats; a Golden with no such repeat
in a run, or a tie, is in neither flip count.

**Known limit:** with so few production labels the gate is weak in both directions — a
real regression on quotes has at most ~9 postings to show in. Labelling production on the
newer Goldens is what makes this score mean more; it is not part of this change.

To undo: remove `production_signal_agreement` from `ATTRIBUTE_METRICS` in
`app/evaluation.py`; it falls back to the 0.02 rule.
