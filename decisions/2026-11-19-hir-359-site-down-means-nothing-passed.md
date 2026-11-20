## 2026-11-19 — "Site down and rollback failed" means no visitor path passed after the rollback (HIR-359)

**What happened.** On 19 Nov two deploys in a row (14:42 and 14:49 Berlin) failed the robot
visitor, were rolled back, and failed it again on the rolled-back site. Both filed "Site
down and rollback failed", Urgent and assigned to Chandler. The site was up the whole
time: in all four robot runs the home page loaded and no run saw a server error or a
failed request. Every failure was an element that did not appear within 15 seconds.

**What the runs show.** The first run of each deploy failed one path, "each filter reaches
the server and the page redraws", at both widths: the check clicked the first city in the
home page's table before its job counts had arrived, which could be a city with no jobs
(fixed the same afternoon, HIR-356). The second runs, on the rolled-back site, failed
*other* paths: at 14:46 one path at phone width with eight of nine passing; at 14:57 the
home page's headline chart, twice on the phone and once on desktop before it passed on the
retry. Three earlier deploys that afternoon failed the same first path and passed after
their rollback. So the outcome followed timing, not which version was live.

**Two faults in the alarm.**

1. It fired on any failure of the second run, even one path at one width.
2. The ticket printed the *first* run's failures under "the robot visitor still fails".
   The second run's report was never read, so the ticket could not say what was wrong
   with the rolled-back site.

**Decided.** The second run's report is read (`--recheck-report`), and it picks the ticket:

- **No path passed on the rolled-back site** (a pass on the retry counts as a pass), or
  the report is missing, unreadable, or names no failing path: "Site down and rollback
  failed", Urgent, assigned to Chandler, as before. Doubt stays on the urgent side. The
  ticket now lists the second run's failures first and the first run's after, each named.
- **Some path passed:** the site is up. Each path that still fails gets the ordinary
  ticket `Site watch: "<path>" fails`, labelled autopilot, High, unassigned. It says the
  deploy was rolled back, that the path fails on the previous version too, and that the
  deploy is therefore probably not the cause: the data, a slow server just after its
  restart, the check itself, or a database change a rollback does not undo. The break
  that comes back after two fixes still goes to Chandler (HIR-260), since the title is
  the same one.

This keeps the 16 Nov entry (HIR-317): the title is "kept for what it says". It now says
it only when the robot could not get anywhere on the rolled-back site.

**Not changed.** The robot's paths, the rollback, and the ticket for a rollback that never
ran. The site still stays on the rolled-back version until the next deploy passes.

**Known limit.** A site where the home page and one city load but everything else fails
files agent tickets, not the urgent one. The outside check that the site answers
(`uptime.yml`) is the backstop for "nothing answers", and on 19 Nov it ran only twice
between 09:27 and 18:33 Berlin, not every five minutes: GitHub runs schedules when it has
room. That gap has its own ticket (HIR-371).

**To undo:** revert the pull request; every failure of the second run is then "site down"
again.
