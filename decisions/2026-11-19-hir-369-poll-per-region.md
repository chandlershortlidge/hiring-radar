## 2026-11-19 — The daily collection runs twice: Europe at 07:00 Berlin, the US at 07:00 New York (HIR-369)

Chandler asked for it on HIR-369. The single 07:00 Berlin run is 01:00 in New York and
22:00 the evening before in San Francisco, so a job posted during the US workday waited
most of a day to show up. Now:

- **Europe** (Berlin, Hamburg, Frankfurt, Munich, Amsterdam, London, Remote EU) runs at
  07:00 Europe/Berlin, as before: `hiring-radar-poll.timer`, `python -m app poll --region europe`.
- **US** (New York, San Francisco, Seattle, Los Angeles, Chicago, San Jose, Austin, Boston)
  runs at 07:00 America/New_York (13:00 Berlin; systemd follows each zone's own daylight
  saving): `hiring-radar-poll-us.timer`, `python -m app poll --region us`.

Each run starts with one line naming its region and the cities it covers.

**Which city is in which region** is `geo.REGION_OF`, next to the list of active cities. A
test fails while an active city has no region, so a launch cannot forget it.

**Which feed is in which region** is worked out from the feed, not written in
`config/feeds.json`:

- a city search (Google for Jobs, Arbeitsagentur) belongs to the region of the city it
  names ("AI engineer in Seattle" → US, `where: München` → Europe);
- a search that names no city goes by its country (`us` → US, any other → Europe);
- Arbeitsagentur and Arbeitnow are German sources → Europe;
- a company's own job board (Greenhouse, Lever, Ashby, JOIN) can list jobs in both regions,
  so it is fetched in **both** runs. The second fetch of the day finds the morning's jobs
  already stored and only notes them as still listed; nothing is stored or read twice.
- anything else is fetched in both runs, so a feed can never fall out of both.

Why derived, not a new field: a new city's searches then land in the right run with no
second edit, and the file stays as it was for the pull requests editing it.

**The model reads each job once, as before.** Each run reads only what it newly stored, so
the cost does not change. Google for Jobs searches are per city, so each runs once a day as
before and the monthly count is unchanged.

**The morning health check** (10:00 Berlin) runs before the US collection. For a feed with
no run yet today it now judges that feed's run from yesterday, so US searches are still
checked, one day behind. A board runs in the Europe collection, so it is judged on today's.

`python -m app poll` without `--region` still fetches every feed, as a hand run always did.
