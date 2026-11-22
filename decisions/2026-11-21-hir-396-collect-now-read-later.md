## 2026-11-21 — An incubating city or track can be stored unread and read once in bulk (HIR-396)

Chandler, 20 Nov, with Claude's addition he agreed to: while a city or career track is
incubating, store its postings and their dates but do not have the model read them.
Reading a new track with a skill list that does not cover it wastes money and has to be
done again. Build the list from a sample, label the Goldens, then read everything once.

**Decision.** Every collected place and career track has a second setting next to its
state in `app/scope.py`: **read now** (the default, and what everything is today) or
**read later**.

- **Read later** changes one thing: the model does not read the posting. Fetching, the
  title and city filters, duplicate detection, the agency screen, the places a posting
  names, the day it was first seen, closing and reposts are all as before.
- **The ordinary reading never touches such a job**: not the daily collection, not a
  re-read after a change to the skill list, not a city launch's first collection. So the
  cost figure quoted for a re-read does not count them either.
- **`python -m app read-pending --city X` or `--family Y`** is the one bulk read. It
  prints how many jobs are waiting and what reading them costs (the same per-reading
  figure the re-read cost command uses, at batch prices), stops above the cap given on the
  command line, and otherwise reads them all as one batch. The jobs keep the day they were
  first collected. `--dry-run` prints the count and the cost and reads nothing.
- **`python -m app sample --family Y --n 50`** draws unread postings to build the skill
  list from, spread across cities and employers. It calls no model.

**Only an incubating place or track may read later.** A live one would put jobs with no
skills on the dashboard. A test fails, naming it, when a live place or track is set to
read later.

**A posting listed for a read-now city and a read-later city is read at once.** It is
shown in the read-now city (the rule for incubating places, 2026-11-21, HIR-395), so it
needs its skills. A posting on a read-later track waits wherever it is posted.

**A posting someone adds by hand is read whatever the setting** (the same exception as
HIR-395): a person chose that one posting and is waiting for the answer.

**The bulk read by city leaves out jobs on a read-later track.** `--city X` alone skips
them and says how many: their skill list is the thing still missing. Naming the track
(`--family Y`) reads them.

**The reports keep the two kinds of unread job apart.** The collection report prints
"stored unread on purpose" with the count and which places and tracks; the morning
check's "jobs are still waiting to be read" counts only jobs that should have been read.

**After the bulk read the setting has to be changed to read now**, or postings collected
the next day wait again. The command says so when it finishes.

**Not chosen: a column on each job.** The setting belongs to the place or track, and one
line in one list is what makes "start reading" a one-line change, like going live.

**Undo:** set the place or track back to read now and the next collection reads its
waiting jobs through the ordinary path. Reverting the pull request removes the setting;
no stored data is changed either way.
