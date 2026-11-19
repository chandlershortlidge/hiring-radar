## 2026-11-19 — Property tests run with a fixed seed on every PR; the random sweep is by hand (HIR-333)

A property test states a rule that must hold for every input ("comparing A to B gives the
same answer as B to A") and lets a tool generate the inputs: Hypothesis for Python,
fast-check for the web code. Chandler, 17 Nov, on the ticket:

> the property tests run with the normal suite on every PR. To keep a PR from failing on a
> bug it didn't cause, run Hypothesis derandomized in CI: a fixed seed, so every PR tries
> the same inputs. Also give a way to run a larger random sweep by hand [...] with
> `max_examples` around 2000 and not derandomized.

So:

- **Every run, every PR:** the same 200 generated inputs per rule. A red property test on
  a PR therefore means the PR broke the rule, never that the dice found an old bug.
- **By hand:** `HYPOTHESIS_PROFILE=sweep` in front of either test command tries 2000 random
  inputs per rule, different each run. This is the run that finds new bugs. The commands
  are in AGENTS.md under "Running and testing".
- **A failure the sweep finds** is fixed, and its input is pinned on the test (`@example`
  in Python, a plain regression test on the web side), because the fixed-seed run would
  otherwise never try it again.

The first sweep is why the last point exists. The fixed 200 inputs passed "a posting is a
duplicate of itself in a different letter case"; the sweep broke it with the text `0ß`,
which German capitals spell `0SS`.

**What "blank" means in the duplicate rules.** "A blank posting is never a duplicate of
anything" is tested for a posting with no title and no text. A posting with a title and no
text is not blank: the same company posting the identical title twice is a duplicate with
no text at all (HIR-108), and the tests pin that this is the only way a text-less posting
matches.

**Undo:** delete the two profiles in `tests/conftest.py` and the `RUNS` line in
`web/src/profile.property.test.js`; the tests then run with each library's defaults
(random, 100 inputs).
