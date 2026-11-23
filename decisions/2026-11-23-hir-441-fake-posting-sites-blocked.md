## 2026-11-23 — A posting that names a known fake-posting site is not collected, and a stored one is hidden (HIR-441)

Job 1060, "Northwind Intelligence — AI/ML Engineer, LLM Applications", was the top match
for a mid-level Berlin profile. It is not a real posting: the employer name is a stock
sample-company name, the link goes to `kerjainti.web.id`, and the text ends with an
application form on a second unrelated site, `infolokerupdate.web.id`. That is a posting
made to harvest applicants' data, not an aggregator's copy of a real job.

**How it got in.** By reading the code, not the stored row (the session that did this work
could not reach the server): JSearch, the Google-for-Jobs search, is the only source whose
links point anywhere on the web. Every other feed stores a link on its own site or on the
employer's board, and a hand-added posting is one Chandler chose. JSearch passes on
whatever Google indexed, and nothing checked where a posting's link led.

**Decision.**

- **Not collected.** A posting whose link or text names one of the sites in
  `ingest.BLOCKED_SITES` is not stored. This holds for every source, hand-added postings
  included: the agency screen lets a hand-added posting through because a person chose
  it, and there is no such reading of a scam.
- **Hidden, not deleted.** A job already stored with a link to one of those sites is left
  out of every public read: the job list, the charts, the counts, its own page, job
  matching and the Claude connection. The rule sits with the one that hides incubating
  places and tracks (`queries.public_clause`), so every public read gets it at once. The
  row, its skills and its history stay in the database, so removing a site from the list
  brings its jobs back.
- **The list holds only sites seen on a real fake posting.** Two today, both from job
  1060. Not the whole `.web.id` ending, and no guess at what a scam looks like: a wrong
  entry silently drops a real employer, and a general spam detector is out of the
  ticket's scope.

**Why hidden rather than deleted.** Deleting stored jobs is decided only with a trial on
a copy of the database and last night's backup in hand (AGENTS.md "What Chandler is
asked", item 4). Neither could be had in this session, so nothing was deleted. Hiding
gives a visitor the same result and can be undone.

**Not measured.** The numbers this job touched could not be read from the live site in
this session. From the rule: it leaves one job out of Berlin's open count and out of the
denominator of every Berlin skill share, and takes one mention off each skill it listed.
