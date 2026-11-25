## 2026-11-25 — Claude Haiku 5.5 is the live reader, released on the sealed check (HIR-409)

Chandler decided on 21 Nov to switch, and on 25 Nov to ship it as soon as possible. The
live reader that turns each posting into skills moves from Claude Sonnet 5.5 to Claude
Haiku 5.5.

**Release check: HIR-383** (decisions/2026-11-20-hir-383-sealed-check-for-cheaper-model.md).
On the 60 sealed postings nobody had tuned against, Haiku scored a skill F1 of 0.945
against Sonnet's 0.922 (about +0.009 like for like), at about an eighth of the cost per
posting ($0.0021 vs $0.0167).

What ships is exactly what that check measured:

- the model `claude-haiku-5-5`;
- HIR-368's round-3 rules (a broad skill counts in any written form; years of experience
  count however they are written), copied verbatim from
  `evals/experiments/trials/hir-368-round-3.md` and placed where the trial placed them,
  after the closing line of the rules. A test fails if the live text drifts from the trial
  file;
- an output cap of 8192 tokens. Haiku's answers run longer, and a reading cut off at the
  cap returns nothing (HIR-223).

This pull request also carries HIR-389's rule (a tool named only in the company's own
tech-stack section is nice-to-have). The two were merged together so that the open jobs
are re-read once, on the cheaper model, not twice.

**Weaknesses accepted** (from HIR-383): "cloud" is missed more often (10 vs 2 in 180
sealed readings), so it will sit a little lower on the chart; seniority is wrong on about
one more posting in 60; production experience marked nice-to-have was missed on the one
sealed posting that had it. A follow-up ticket covers "cloud".

**How to revert:** set `HIRING_RADAR_MODEL=claude-sonnet-5-5` where the poll runs, and
the open jobs are re-read once. Sonnet fits the 8192 cap as well, so nothing else needs to
change.
