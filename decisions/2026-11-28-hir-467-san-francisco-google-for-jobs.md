## 2026-11-28 — San Francisco gets its two Google for Jobs searches (HIR-467)

A per-city collection check on 25 Nov (window 12–25 Nov) found all 41 San Francisco jobs
collected in 14 days came from company boards (Ashby 24, Greenhouse 17), and 25 new jobs in
the last 7 days against New York's 54 from 10+ sources.

**Why San Francisco had no job-board source: never configured, not filtered or failing.**
San Francisco launched on 2026-11-03 (HIR-12) on company boards, when Google for Jobs (the
JSearch feed) was on a free plan capped at 200 requests a month. New York got its two
searches on 2026-11-12 (HIR-255) because it was adding about one job a day; San Francisco
had enough boards then and was not given any. When the paid plan lifted the cap
(2026-11-19, HIR-352), the searches went to the cities launched that day and later
(Austin, Boston, London, Amsterdam, then Seattle, Los Angeles, Chicago, San Jose), and
Hamburg and Frankfurt followed (HIR-466). San Francisco, launched before the cap was lifted,
was the one city left out. Nothing drops San Francisco postings from a search: a search
for the city is read as the city and runs in the US morning collection, like the others.
The other job-board feeds we have do not cover the US (the Bundesagentur, arbeitnow and
startup.jobs are searched for Germany), and board discovery already searches San Francisco
by name twice, so it was not missing.

**Added:** "AI engineer in San Francisco" and "machine learning engineer in San
Francisco", country `us`, one page, the past week — the same pair every city has. Postings
from JobLeads arrive through these searches; they often come cut short with no skills read
(HIR-456, out of scope here).

**Not added:** New York's two "software engineer" searches. They are the HIR-397 trial of a
second career track, limited to Berlin and New York.

**The monthly sum, redone as 2026-11-19 (HIR-352) requires.** One page once a day is about
30.4 requests a month per search.

| searches | count | requests a month |
| -- | -- | -- |
| before this change | 29 | ~882 |
| San Francisco (new) | 2 | ~61 |
| **total** | **31** | **~943** |

943 is 19% of our own cap of 5,000 and 9% of the plan's 10,000. The plan is a flat $25 a
month under 10,000, so this adds no cost. A test now checks that every US city has its
pair, so the next city to launch cannot be left out the same way.

**Before and after.** Before: 25 new San Francisco jobs in the 7 days to 25 Nov, all from
company boards. After: the first weekly collection check after this merges; it is not
available from the session that made the change.

**Undo:** revert the PR; the two searches stop. Nothing stored is deleted or changed.
