## 2026-11-23 — The admin page is kept private by the web server's password, and reads only (HIR-398)

Chandler, 20 Nov: a place to see what is being collected in the background and what is
live. Start small. The page is `/admin`: one row per collected place and per career
track, and this month's spending against each limit we have.

**Decision 1: the password is the web server's, not a second one inside the app.** The
ticket says "behind the existing admin login". The only login that exists is the one
password the web server (Caddy) asks for in front of everything except the MCP server.
The page uses that and adds nothing: no second password to set on the server, and
nothing to do by hand when this merges.

What that leaves open is the day the dashboard goes public (HIR-82), when the password
comes off the read-only pages. A test reads the web server's settings file and fails,
naming `/admin`, as soon as that address would be answered without the password. So the
change that opens the site cannot merge until the admin page has its own password block.
The test reads the repository's copy of the settings; the server's own copy is applied by
hand, as it always has been, and the runbook's "check from the Mac" step covers it.

**Not chosen: a password checked by the app itself.** It needs a new secret written on
the server by hand before the page works at all, and a second login to keep in step with
the first. It is the right step if the app is ever reachable without the web server in
front of it; today it listens on the server's own loopback address only.

**Decision 2: the page changes nothing.** It has no buttons. Switching a place or track
to live stays one line in the list of places and tracks, through a reviewed pull request.

**Decision 3: one query feeds the page and the Monday summary.** The summary's line for
each incubating place or track is written from the same rows the page shows, so the two
cannot print different numbers.

**What the numbers mean.**

- *Stored* is every posting kept for the place or track, open or closed. *Open now* uses
  the dashboard's own rule for an open job. *Waiting to be read* is every stored posting
  the model has still to read, whether it is held back on purpose (read later) or simply
  not reached yet.
- *Days collected* is the number of days from the day the first posting was stored to the
  day one was last seen, both included. A place collected for three weeks says 21 even if
  no new posting arrived on some of those days; the last-seen day next to it is what
  shows a collection that has stopped.
- *Sources* counts the kinds of source that have supplied a posting (Greenhouse, Lever,
  the German job agency, and so on), not the individual company boards: the database
  records the kind, not the board.
- *Ready?* is shown for incubating rows only, and says three things that are on record.
  **Skill list:** a place uses the one shared list; a track counts as having one once it
  is set to be read as postings arrive, because a track is stored unread exactly until
  its list exists (2026-11-21, HIR-396). **Goldens:** how many reviewed Goldens were
  drawn from postings of that place or track, read from the labelling runs' own records.
  **Launch check:** the day of the latest labelling sample drawn only from that place or
  track, which is the sample the launch check scores. The check itself prints its result
  and keeps no record, so the page can say the sample exists, not what the score was.

**Spending.** Model reading is this month's stored readings priced at the full rate, so
it is an upper bound: readings sent as a batch cost half, and the record does not say
which were. There is no monthly limit on model reading, only the €10 stop on a single
launch or bulk read, and the page says so. Board searches are the morning caretaker's
recorded spend against its daily limit; the searches a city launch runs keep no count
anywhere, and the page says that too.

**Undo:** revert the pull request. The page, its test and the Monday line go; no stored
data is touched either way.
