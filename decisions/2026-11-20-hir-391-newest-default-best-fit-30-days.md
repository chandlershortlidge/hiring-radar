## 2026-11-20 — The job list opens newest first; Best fit ranks only the last 30 days (HIR-391)

Chandler, 20 Nov, in the ticket: "N = 30 days. The sort menu option itself reads
'Best fit (last 30 days)'. Saved view: keep all saved jobs (no age rule there)."

- **Newest first is the starting sort for everyone.** It used to be Best fit for anyone
  with a profile. Best fit stays in the sort menu.
- **Best fit only ranks jobs first seen in the last 30 days.** Why: a great match first
  seen seven weeks ago is probably filled, and it could sit at the top. Older jobs are
  left out of that view only; they are still listed under every other sort. 30 rather
  than 14 because in a thin city 14 days leaves a handful of jobs.
- **The 30 is one named number** (`FIT_DAYS` in `web/src/profile.js`) that the filter,
  the menu label and the line under the list all read. Change it there and nowhere else.
- **The age check runs before the ranking**, not inside it: the ranking is unchanged and
  is simply handed a shorter list.
- **A job first seen exactly 30 days ago is in.** A job with no readable date is out.
- **Saved jobs have no age rule.** They were saved on purpose, so Best fit there ranks
  all of them, and the menu option reads plain "Best fit" while Saved is on, since
  "(last 30 days)" would not be true there.
- **The 200-job limit still holds** (the earlier entry '"Best fit" ranks in the browser,
  over at most 200 jobs'): the browser fetches the 200 newest jobs and keeps the recent
  ones. The line under the list names the 200 only when all 200 are recent, which is the
  one case where recent jobs can be missing.

Undo: revert the pull request. Nothing is stored and nothing is re-read by the model.
