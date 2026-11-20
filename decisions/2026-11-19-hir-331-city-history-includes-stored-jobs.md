## 2026-11-19 — A city's history includes the jobs stored before it launched whose posting named it (HIR-331)

**What was decided.** Chandler, 17 Nov, in the ticket: when a city launches, the jobs we
already stored, open and closed, whose location named that city count under it too. A
posting stored last month as "Berlin, London or Amsterdam" was credited to Berlin only,
because London was not a city yet; once London is a city, it counts under London as well.

**What that means in practice.**

- `python -m app backfill-places [--city CITY] [--dry-run]` reads every stored job's
  location through the same matching ingest uses (`geo.places_of`) and adds the city rows
  it is missing. It only adds: no place is removed, `job.city` (the job's main city, shown
  on the job list) never changes. Running it twice adds nothing the second time.
- `discover-boards --launch CITY` runs it for the launched city, so every launch does it
  without anyone remembering, and the launch report says how many stored jobs the city gained.
- A closed job counts under the new city only in the time windows when it was open: the
  windows read the job's own first and last sighting, which the backfill does not touch.
- **Cities only, never "Remote (EU)".** Whether a job is EU-remote is judged from its whole
  posting, and those rules have changed since some jobs were stored; re-judging old jobs as
  remote is a different question from crediting a city its posting named.
- **The stored location only.** We keep one location line per job (the first sighting's),
  not one per sighting merged into it, so a city named only by a merged copy is not
  recovered. Postings never stored are not recovered either.
- Any job that would gain more than three cities at once is listed in the output, for a look
  at whether its location line is a real multi-city posting or a list of offices.
