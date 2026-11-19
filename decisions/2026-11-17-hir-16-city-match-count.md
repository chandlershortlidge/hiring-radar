## 2026-11-17 — The city comparison counts the jobs a visitor's profile matches, per city (HIR-16)

**What was approved.** Chandler, 16 Nov, to the recommendation "when a visitor has filled
in their skills, the city comparison shows one line per city with how many open jobs they
cover most of the required skills for": yes, as recommended.

**What counts as a match.** A job counts for a city when the profile has at least 70% of
its required skills, by the same count the job list's badge shows (a list of alternatives,
"Python, Go or Java", is one requirement). 70% is the ticket's own example.

- **A job that lists three or fewer required skills is not counted.** The job list already
  refuses to show a percentage for those jobs, because so short a list says more about
  what was read out of the posting than about the fit. Counting "2 of 2" as a full match
  here would contradict the badge next to it. Undo: drop the short-list test from the
  match rule in the profile code.
- **Skills only.** A job that insists on German, a degree, a level or production
  experience the profile lacks still counts when the skills match, as the ticket words it
  ("jobs where you have at least 70% of required skills"). The job list still marks those
  jobs. Undo: add the hard asks to the match rule.
- **A job with no required skills on record is not counted**: nothing to judge, as in the
  job list.

**What the line follows.** The filters set on the page (role family, seniority, German,
degree, production experience, time window), like the chart beside it, and not the skill
selection or the search box, which only narrow the job list. Each city's count is shown
against that city's number of jobs, because the cities differ in size.

**Where it is computed.** In the browser, like every other use of the profile. The browser
asks for each city's jobs, 200 at a time, the largest page the server gives, and counts
them itself; the profile is never sent.
