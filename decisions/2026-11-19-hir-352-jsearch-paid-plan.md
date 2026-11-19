## 2026-11-19 — Google for Jobs moves to a paid plan; the four new cities get their two searches each, under our own cap of 5,000 a month (HIR-352)

Chandler chose the paid plan on HIR-352 (option 2) and subscribed to JSearch **Pro on
RapidAPI**: $25 a month, 10,000 requests a month, then $0.003 per extra request, 5 requests a
second. This replaces the sum in 2026-11-12 (HIR-255) and the "no country-wide search" in
2026-11-19 (HIR-252).

**The limit was read from the API, with the server's key.** The server's key was first an
OpenWeb Ninja key, which the RapidAPI plan does not cover; Chandler put the RapidAPI key on
the server and set `JSEARCH_HOST=rapidapi`. One call then returned
`x-ratelimit-requests-limit: 10000` (remaining 9,999).

**RapidAPI's search lives at `/search-v2`.** `/search` answers 404 "Endpoint '/search' does
not exist", and `/search-v2` nests the job list one level deeper (`{"data": {"jobs": [...]}}`).
The adapter now calls `/search-v2` on RapidAPI and reads both shapes. Without this, every
Google for Jobs search, Berlin's and New York's included, would have failed from the first
poll after the key switch.

**Going over now costs money instead of stopping the searches, so we stop ourselves.** The
poll counts this month's Google for Jobs requests (one per search run, failed runs included)
and skips every such search once the count reaches 5,000; every other feed carries on, and
the searches resume when the month turns. Calls are kept at least 0.25 s apart (the plan
allows 5 a second). The Monday summary gets one line: this month's searches against the cap.

**The monthly sum.** Each search asks for one page, once a day: about 30.4 requests a month.

| searches | count | requests a month |
| -- | -- | -- |
| Berlin (2) and remote-from-Germany (1) | 3 | ~91 |
| New York | 2 | ~61 |
| Austin, Boston, London, Amsterdam (new) | 8 | ~243 |
| **total** | **13** | **~395** |

395 is 8% of our cap of 5,000 and 4% of the plan's 10,000: far more than the 20% headroom the
ticket asks for. Seattle, Los Angeles, Chicago and San Jose (HIR-302) would add 8 more, to
21 searches and ~640 a month (13% of the cap); they get their two each when they launch.
Any further search still needs this sum redone.

**The new searches copy New York's shape**: "AI engineer in <city>" and "machine learning
engineer in <city>", one page, the past week. London searches with country `gb`, Amsterdam
with `nl`.

**A remote job from a UK or Dutch search is not read as open to Berlin.** JSearch writes
"Anywhere" as the place of a remote job with no region, and the place reader takes a bare
"Anywhere" as remote-from-the-EU. HIR-255 stopped that for US searches; it now holds for every
search outside Germany, so a London- or Amsterdam-only remote job lands in neither the EU
remote list nor a city, unless it names its city. The German searches are unchanged.

**Undo:** revert the PR. The eight searches stop, and RapidAPI calls go back to `/search`,
which fails: also set `JSEARCH_HOST` back to `openwebninja` with the old key on the server,
or cancel the plan. Nothing stored is deleted or changed.
