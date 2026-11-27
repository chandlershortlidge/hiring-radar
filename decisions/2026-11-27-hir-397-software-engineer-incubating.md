## 2026-11-27 — Software engineer is collected in Berlin and New York, unread and hidden, from the titles below (HIR-397)

Chandler, 20 Nov, go on 24 Nov: software engineer is "the big one". It needs a skill list
of its own before anyone sees it, so for now it is collected and stored without being read
by the model and without being shown (the incubating, read-later states of 21 Nov, HIR-395
and HIR-396), in two cities only, to build two months of history before it goes live.

**Which titles are software engineer.** From the title alone, like every other track. A
title counts when it contains, ignoring case:

| the title says | example |
| -- | -- |
| "software" directly before engineer, developer, Entwickler or Ingenieur (a space or a hyphen between, or none) | "Senior Software Engineer", "Software-Entwickler (m/w/d)", "Softwareentwickler Java" |
| backend, frontend or full-stack (any spelling: "back-end", "Fullstack", "full stack") **and** engineer, developer or Entwickler anywhere | "Backend Engineer (Go)", "Full-Stack Developer", "Frontend-Entwickler" |
| "platform engineer" | "Platform Engineer, Payments" |
| "developer" as a word | "Java Developer", "iOS Developer" |
| a word ending in "Entwickler" or "Entwicklerin" | "Java-Entwickler", "Anwendungsentwickler" |

and is **not** one of:

- a title the other tracks already hold: anything with an AI or ML word and a role word
  stays where it was ("AI Software Engineer" is AI Engineer, "ML Platform Engineer" is ML
  Platform), and a Forward Deployed Engineer title stays FDE. This is the 21 Nov rule that a
  track added later takes only what the existing tracks do not.
- a sales title ("Sales Engineer", "Pre-Sales Developer"): the rule of 16 Nov (HIR-246).
- a developer who does not write software: "Business Developer", "Business Development",
  "Developer Advocate", "Developer Relations", and in German "Produktentwickler",
  "Projektentwickler" (property development), "Personalentwickler", "Geschäftsentwickler",
  "Organisationsentwickler". These are the
  common non-software uses of the two words in the feeds; anything else with "developer" or
  "Entwickler" is collected ("Real Estate Developer" is, a known limit), because the
  postings are read for skills later and a stray non-software posting costs one unread
  row. Titles that name none of the words above ("Software Architect", "Backend Lead",
  "Engineering Manager") are not collected.

**Only Berlin and New York.** A software engineer posting is stored only when it names
Berlin or New York. Every other track is collected in every city; this one says on its own
line which cities it takes. A posting for Berlin and Munich is stored (it names Berlin);
one for Munich only is passed over and counted as "outside its track's cities".

**No new company boards for it.** The weekly search for new company boards counts how many
roles a board has that we would collect. Software engineer roles are not counted there, so
no board is added because it lists many of them. The boards we already poll still give
their software engineer postings in Berlin and New York.

**Sources.** The country-wide feeds as they are (Bundesagentur, arbeitnow) and the boards
we already poll, plus four Google for Jobs searches: "software engineer" and
"Softwareentwickler" in Berlin, "software engineer" and "software developer" in New York.
That is about 120 more requests a month against our own cap of 5,000.

**Stored jobs.** None moves. The database change only adds the new name to the values a
job's track may take, and keeps every stored job's track. A collected job passed the old
title filter, which no software engineer title passes unless another track holds it. A job
added by hand skipped that filter, so one with a software title ("Senior Staff Software
Engineer") sits under AI Engineer today and stays there; re-sorting those is its own call,
since it would take them off the dashboard. A software title added by hand from now on
goes to the new track, hidden and read at once like any hand-added posting.

**The model reads none of these postings** until the skill list exists and someone runs
the bulk read for the track (phase 3 of the ticket, its own figure then). Cost now: no
model spend.

**To undo:** delete the track's line in `app/scope.py` and the four searches in
`config/feeds.json`. Postings already stored stay on the track, hidden and unread; delete
them in a ticket of their own if wanted (deleting stored jobs is Chandler's call).
