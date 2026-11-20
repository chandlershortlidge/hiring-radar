## 2026-11-20 — A company board the dashboard finds missing is added through a ticket the site files (HIR-324)

"Add a job" on the dashboard stored the one posting and stopped. When the posting sat on a
company job board we do not collect, the company's next posting was missed again. The
link checker run from a terminal closes that hole by adding the board to the list of
boards we collect. The site cannot: that list is a file in the repository.

**Decision.** When a link check made by the dashboard ends in "this company's board is
not in our list", the site records the board in its database and files one Linear ticket
naming every recorded board that no ticket names yet, with the exact lines to add. An
agent adds them in an ordinary pull request, which is reviewed and merged like any other,
and the next morning's collection picks the boards up. The ticket is filed right after
the add. The caretaker's morning run files it again for any board whose ticket did not
reach Linear.

- **Screening.** A board is not recorded when its name or the company's matches the word
  list that keeps recruiters and job boards out of board discovery, when it was rejected
  before, or when it is in the list but switched off (someone, or the caretaker, turned
  it off on purpose).
- **One row per board**, however many postings led to it, so a company is asked for once.
- **Pasted text and screenshots** record the same check when their link was given, from
  the text already in hand, with nothing fetched: the link is often one no fetch can
  read, which is why the text was pasted. Without a link nothing is recorded, as before.
- **What the visitor is told** after an add that came with a link: the company's other
  jobs will be collected from tomorrow, are already collected, or cannot be collected
  automatically yet. Without a link nothing was checked and the line is left out.

**Not chosen:** the ticket's first idea, a table the lead agent reads. The lead agent
runs in the cloud and cannot reach the server's database, and teaching it to would have
changed its own instructions. A ticket uses the path that already exists: the caretaker
files tickets from the server, and agents pick tickets up.

**Not chosen:** letting the server change the list itself. The list would then differ
between the server and the repository, and the next deploy would undo it.

**To undo:** revert the pull request. The table stays in the database, unused.
