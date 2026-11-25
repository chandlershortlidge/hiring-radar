## 2026-11-24 — A title that ties a remote job to a non-EU country outranks the location (HIR-455)

Chandler found FullStack's "Senior Forward Deployed AI Engineer - LLMs & RAG - Remote -
USA" (job 1826) under Remote (EU). The title says the job is remote within the USA.

**Where the tag came from.** The posting reached us through the web-wide job search
(JSearch), on a German search, as a copy on JobLeads' German site. JobLeads files the
postings it copies under a German town (here Geldern) and marks them remote. Our adapter
writes a posting the board marks remote as its town plus "Remote (<the board's country>)",
so this one was stored with a location like "Geldern; Remote (Germany)". Geldern is not a
city we track, and the rule of 26 Oct counts "remote" beside "Germany" as EU-remote. The
word "Remote" in the title played no part: the title is read only when the location is
empty, and the description is read only when the location names no region at all. So
neither the title's "USA" nor anything in the text was ever looked at.

This is read from the code and the ticket. The stored row of job 1826 could not be read
in the session that wrote this (no copy of the database), so the exact stored location is
not confirmed.

**Decision.** A title that ties a remote job to a non-EU country is never EU-remote,
whatever the location says. It does so when all three hold:

- it names a non-EU country from the list the description rule already uses (US, USA,
  U.S., United States, Canada, North America, Latin America, LATAM, India, UK, United
  Kingdom). The short forms count in capitals only, so "Join us" is not the US;
- it has a remote word ("Remote - USA") or the word "only" ("US only", "UK only");
- it names no EU-wide region and not Germany. "Remote (US or Europe)" is left to the
  location, as before.

"AI Engineer, US Market" is untouched: it has no remote word and no "only", and says who
the customers are, not where the engineer may live.

A tracked city still wins: "New York; Remote (US)" stays New York.

**What happens to such a posting.** With no tracked city and no EU-remote, it names no
place we collect, so a feed's copy is not stored.

**Stored jobs.** `scripts/untag_non_eu_remote.py` lists the stored jobs under Remote (EU)
whose title is restricted this way, or whose stored location names a non-EU country, and
with `--apply` takes Remote (EU) off them. It deletes nothing. This narrows one line of
the note on the table of a job's places (migration 022, HIR-289: "a place a posting once
named is not taken away"): a place the
posting never named, and only an aggregator gave it, is taken away. A job left with no
place is out of every city and the remote view but still counts when no place is chosen;
removing it altogether is a delete, which is Chandler's call.

**Known limits.**

- Only the title is new. A posting whose title is silent and whose description says "US
  only", stored with an aggregator's "Remote (Germany)", is still EU-remote: the
  description is read only when the location names no region.
- Countries outside the list (Australia, Brazil, "APAC") are not recognised in a title.
- "Remote Sensing Engineer, US" would read as restricted. Not seen in stored titles.

**To undo:** remove the title check from `geo.is_remote_eu`. For a stored job, add its
`Remote (EU)` row back to `job_place` and set `job.city` back to `Remote (EU)`.
