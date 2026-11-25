## 2026-11-24 — A checked link with no readable location is filed under the city the check was run for (HIR-322)

**What:** every link check is run for one city (`check --city`, Berlin unless told
otherwise). When a link is not found, its page gives no location at all, and its title and
text do not say it is EU-remote, the check log stores that city instead of nothing.

**Why:** a link a feed already had always carries its job's city; a missed link on a
company's own site, LinkedIn or a recruiter page carried none. On the log of 17 Oct to
12 Nov, 55 of 81 links had no city and every one was a miss, so each city's share of
"links a feed already had" read higher than it was.

**Limits, on purpose:**
- A location that was read and is not a tracked city ("Paris, France") stays unknown.
  The posting says where it is, and that is not the city the check was run for.
- The city never reaches the posting: the verdict, the reason a miss is filed under and
  `--add` are unchanged. `--location` is still the way to correct one posting's location.
- Checks logged before this are not filled in: that changes numbers already reported, and
  is a separate decision.
- Berlin is the default because every link pasted so far is a Berlin job. A batch for
  another city must be run with `--city`; the output names the assumed city on every link
  it was used for, so a wrong default is visible in the run.

**Undo:** drop `run_for` from `log_check` and the `--city` option; new misses with no
location go back to no city.
