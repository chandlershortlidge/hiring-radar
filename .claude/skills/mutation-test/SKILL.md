---
name: mutation-test
description: Run mutation testing on chosen modules to find tests that pass even when the code is broken, triage the survivors, and file or verify a ticket. Use when the person asks to mutation-test or check test quality, or invokes /mutation-test.
---

# /mutation-test [find | verify HIR-n] [<module> …]

Mutation testing makes small deliberate breaks in the code (flip a comparison, turn `continue` into `break`, drop an argument) and runs the tests. A break no test catches "survives": the tests pass even with that code broken. It measures whether tests check behaviour, which a test count or line coverage can't.

It's slow: about 25 minutes for the Python side, about 2 for a JS file. Run it on demand, never per PR, never in CI.

## Two modes

- **find** (default): run it, triage the survivors, and file one ticket for the gaps that matter.
- **verify HIR-n**: after that ticket's PR merges, run it again on main and check each listed gap really closed. Don't trust a "done" report without this. The first run (HIR-237) found 10 of 12 closed when the report said 12.

## Steps

1. **Scope.** Default targets, where a silent bug hurts users most: `app/extract.py`, `app/dedup.py` (Python), and `web/src/profile.js` (CV fit, JS). The person may name others. Pick the test files that exercise each target.

2. **Scratch copy, never the repo.** Pull main, `cp -r` the repo to `/tmp/mut`, and delete its `.git`. Install the tools there only; nothing is added to the project's dependencies.

3. **Python (mutmut 3).** `uv pip install mutmut` in the copy. Append to its `pyproject.toml`:
   ```toml
   [tool.mutmut]
   paths_to_mutate = ["app/extract.py", "app/dedup.py"]
   source_paths = ["app"]
   pytest_add_cli_args_test_selection = ["tests/test_extract.py", "tests/test_dedup.py", "tests/test_ingest.py"]
   also_copy = ["taxonomy", "config", "tests", "scripts", "evals", "docs"]
   ```
   mutmut generates mutants for all of `app/` regardless, so pass name patterns to run only the targets: `.venv/bin/mutmut run --max-children 8 "app.extract*" "app.dedup*"`. It takes about 25 minutes, so run it in the background. Then `mutmut results` lists survivors, `mutmut show <name>` prints each diff, and `mutmut results --all true` gives killed and survived counts per function.

4. **JS (Stryker).** In the copy's `web/`: `npm install --no-save @stryker-mutator/core @stryker-mutator/vitest-runner`, plus a `stryker.conf.json` with `"testRunner": "vitest"`, `"mutate": ["src/profile.js"]`, `"reporters": ["json", "clear-text"]`, `"coverageAnalysis": "perTest"`. Run `npx stryker run` and read the survivors from the JSON report (status `Survived` or `NoCoverage`).

5. **Triage.** Most survivors are noise: log or error-message wording, dict key names in logs, token-usage logging, sort keys of internal lists, `>=` vs `>` exactly at a threshold. Keep only the ones that would change **what a user sees** or **what gets stored**. Examples from the first run:
   - skipping to the next item becomes stopping, which drops every later skill;
   - a rule like "required beats nice-to-have" removed;
   - an input never checked to reach the model;
   - a loop that stops at the first non-match.

   For each one, check the existing tests: a test can pass for the wrong reason. In the first run, a cut-off-answer test failed on a later check, not the one it was meant to test.

6. **File (find mode).** One Linear ticket, labelled `autopilot`, in the current launch milestone. It contains:
   - a short table of breaks caught per area, as killed of total;
   - the meaningful gaps as a numbered list in plain words, each with the break that should be caught;
   - a "Done when": each gap has a test that fails on that break; tests only; app code changes only if a new test exposes a real bug, as its own commit;
   - an Agent notes section with the surviving mutant names and how the run was set up.

7. **Verify (verify mode).** Re-run on merged main. Comment on the ticket with the new counts, which gaps are closed, and which are half closed and why. File one small follow-up only for what's really left.

## Reporting

Three lines at most, in plain words, with no mutant names or file paths. In find mode: what share of breaks the tests caught, how many real gaps there are with one example in user terms, and that a ticket is filed. In verify mode: how many gaps closed. Detail goes in the Linear ticket.
