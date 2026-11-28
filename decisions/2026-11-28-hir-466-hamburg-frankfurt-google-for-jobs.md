## 2026-11-28 — Hamburg and Frankfurt get their two Google for Jobs searches (HIR-466)

A collection check on 25 Nov found Hamburg with 5 new jobs in a week and Frankfurt with
10, about half of each from the Bundesagentur für Arbeit, and days with nothing when that
one source was quiet. Munich does better on the same German feeds because three company
boards add to it; Hamburg and Frankfurt have none (the 2026-11-08 launch, HIR-165, judged
284 and 337 boards and found none with 5 or more roles in either city).

**What the two cities draw from today.** The two Bundesagentur searches each ("AI
Engineer" and "Machine Learning Engineer", 25 km), and the two country-wide feeds that
cover all of Germany (arbeitnow, and startup.jobs searched for Germany). Company boards
already collected for other cities count a posting here when it names Hamburg or
Frankfurt, but none was added for them. Board discovery searches each city by name twice
("AI engineer" and "machine learning").

**What Berlin has that they did not: Google for Jobs.** Berlin has had its JSearch
searches since October; Hamburg and Frankfurt never got theirs, because until HIR-352 the
plan was capped at 200 requests a month. That cap is gone. Each city now gets the same
pair as every other city: "AI engineer in <city>" and "machine learning engineer in
<city>", Germany, one page, the past week.

**The monthly sum, redone as 2026-11-19 (HIR-352) requires for any further search.** One
page once a day is about 30.4 requests a month per search.

| searches | count | requests a month |
| -- | -- | -- |
| before this change (Berlin 4, remote-from-Germany 1, New York 4, eight other cities 2 each) | 25 | ~760 |
| Hamburg and Frankfurt (new) | 4 | ~122 |
| **total** | **29** | **~882** |

882 is 18% of our own cap of 5,000 and 9% of the plan's 10,000. The plan is a flat $25 a
month under 10,000, so this adds no cost. The cap still stops every search before any
request is billed extra.

**Munich is left as it is.** It has no Google for Jobs searches either, but it was not
short of jobs, and the ticket names only Hamburg and Frankfurt. Two more searches would
bring the total to ~943 a month, still under the cap.

**Not done here, for lack of access from this session:** whether the Bundesagentur
adapter failed on 21 and 23 Nov (the server's run log answers it), and a fresh board
search for the two cities (it needs the board search key and live board fetches). Both are
a follow-up ticket.

**Undo:** revert the PR; the four searches stop. Nothing stored is deleted or changed.
