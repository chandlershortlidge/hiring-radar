## 2026-11-19 — Seattle, Los Angeles, Chicago and San Jose are collected; South Bay towns count as San Jose (HIR-302)

Chandler named these four cities on the HIR-302 ticket, so the 2026-11-03 rule (HIR-132)
applies as written: a city he has named is launched by the automated path, and neither it
nor its boards waits on approval. `geo.ACTIVE_CITIES` now also holds `"Seattle", "Los
Angeles", "Chicago", "San Jose"`, each collected since 2026-11-19, all under the dashboard's
"United States" heading. Each gets the two Google for Jobs searches the paid plan's sum
already counted for them (2026-11-19, HIR-352: 21 searches, about 640 requests a month
against our cap of 5,000).

**Which places count as each city.**

- **San Jose** is San Jose, Santa Clara, Sunnyvale, Mountain View, Palo Alto and
  Cupertino: the South Bay and the Peninsula's south end, where the big employers of that
  market sit. Menlo Park, Redwood City and Foster City are not on the list: they sit
  between the two cities and have never counted as San Francisco either.
- **"Bay Area" alone stays San Francisco.** A posting that names San Jose (or one of its
  towns) counts as San Jose only, even when it adds "Bay Area", "SF Bay Area" or "San
  Francisco Bay Area". It counts under San Francisco too only when it names San Francisco
  as a place in its own right ("San Francisco, CA; Sunnyvale, CA").
- **Not San Jose:** San José in Costa Rica (written with "Costa Rica" or "CR" in capitals),
  San Jose in the Philippines, the towns called "San Jose del …", and Santa Clara in Cuba.
- **Seattle** is Seattle, plus Bellevue and Redmond only when followed by "WA" or
  "Washington": both names exist in other states.
- **Los Angeles** is "Los Angeles", "LA, CA" and Santa Monica. A bare "LA" never is: it is
  also Louisiana's code ("New Orleans, LA") and a common word. Los Ángeles in Chile is not
  Los Angeles.
- **Chicago** is "Chicago". No other place of that name turns up in postings.

Tests pin each case, the near-misses included.

**Stored San Francisco postings are not moved.** The ticket asked how many would move. On
a copy of the local database: none. Every stored San Francisco posting that names a South
Bay town also names San Francisco itself ("San Francisco, CA; Sunnyvale, CA"), so under
this rule it keeps San Francisco and gains San Jose. 26 such postings gain San Jose when
San Jose's launch credits it with the stored jobs whose postings named it (HIR-331's
rule, which only adds a city and never removes one). The 20 that say only "San Francisco
Bay Area" stay San Francisco.

**Undo:** revert the PR. No migration and nothing deleted; postings already stored for the
four cities stop being shown, because an inactive city is filtered out of every query.
