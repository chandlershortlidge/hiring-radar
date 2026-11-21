## 2026-11-21 — A city or career track can be incubating: collected, and never shown in public (HIR-395)

Chandler, 20 Nov: a city or a career track should be collectable for weeks before anyone
sees it, so that on the day it goes live it already has history for "what's rising", a
skill list built from real postings, and Goldens. "One day you just turn it on and it's
backfilled." Until now a city was either collected and shown, or not collected at all, and
career tracks had no switch.

**Decision.** Every collected place (a city, or EU-remote) and every career track has one
of two states, kept in one list, `app/scope.py`:

- **live**: collected and shown, as before.
- **incubating**: collected in exactly the same way. Fetching, the title and city
  filters, duplicate detection, the agency screen, recording every place a posting names,
  the model's reading and the caretaker make no difference between the two states.

**The public site never shows anything incubating.** A job on an incubating track, and a
job posted only for incubating places, is absent from the dashboard's job list and job
page, the chart, the skill tree, the related-skills panel, compare mode, "what's rising",
every count in the header, the queue of suggested skills, the public API and every MCP
tool. Asking for it by name answers as if it did not exist: an incubating city matches no
job, an incubating track is refused like a name nobody defined, and a job's own address
says "no such job". The rule is applied once, where the dashboard's queries choose their
jobs, so a new chart or tool gets it without being told. A test lists the MCP tools and
fails when one is added without a check that it hides incubating jobs.

**A job posted for a live city and an incubating one is shown**, as a job in its live
city only: it is a real job in a city visitors can see, and hiding it would make the live
city's numbers wrong. The incubating city is left out of its places and of every
per-city count.

**The tools behind the site still see everything.** The scripts that sample postings for
labelling and for building a skill list read the stored jobs directly, and the shared
queries take an explicit switch for the same purpose. Nothing a visitor can reach passes
that switch. One exception is deliberate and gives nothing away: adding a posting by hand
for an incubating city stores and reads it, and reports how many skills were found.

**Switching to live is one line**: the state in `app/scope.py`. Nothing is collected
again and no job changes; each keeps the day it was first seen, so the history is there
at once. Two existing checks then say what else that line needs. The dashboard's own list
of places and tracks must name it (a test fails, naming it, until it does; the same test
fails if an incubating place is listed there, which is also what keeps the robot visitor
off it). A city gets the launch check that every city launch already runs.

**Adding a career track** is its line in the same list, with the pattern that says which
job titles belong to it, plus a migration that adds its name to the values the database
accepts for a job's track. That second step is the standing rule that the database and the
code hold the same list of allowed values (HIR-311); it is kept, not loosened, and the
existing test names the column until both agree. A new track only takes titles that the
five original tracks do not: a title they already hold stays theirs. So adding a track,
in either state, cannot change what the live tracks collect or show.

**Not chosen: keeping incubating jobs in a second table or database.** Collection,
duplicate detection and repairs would each need to know two places, and switching to live
would become a data move that can fail half way. One table and a rule on the way out
keeps "switching on" a one-line change.

**Not chosen: hiding incubating data in the browser.** The public API and the MCP tools
would still serve it to anyone who asked.

**Not in this change:** which cities or tracks to incubate (HIR-397), collecting
incubating postings without having the model read them (HIR-396), and the admin page that
lists every place and track with its state (HIR-398). Today every place and track is
live, so nothing on the site changes when this merges.

**Undo:** set a place or track back to live in `app/scope.py` and its jobs are shown
again; reverting the pull request removes the states altogether. No stored data is
changed either way.
