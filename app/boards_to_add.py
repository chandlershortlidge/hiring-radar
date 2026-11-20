"""Company boards the dashboard found we do not collect, and the ticket that gets them added.

"Add a job" stores one posting. When the link is on a company's job board that is not in
config/feeds.json, that fills one gap and leaves the hole open: the company's next posting
is missed again (HIR-324). The /check-url skill closes the hole by adding the board to the
file; the server cannot, because the file lives in the repository. So:

Does:
  - `note`: after a check (app/check.py), say where the posting's company board stands,
    and record the board when it is one we do not collect and may add. The answer is one
    of three words: QUEUED (recorded, an agent will add it), COLLECTED (already in the
    list and switched on), NONE (no board we can collect: not a board link, a recruiter or
    job board by the shared word list, a board rejected before, or one switched off);
  - `waiting`: the recorded boards no ticket names yet and the list still lacks;
  - `file_ticket`: put every waiting board in one Linear ticket, written so an agent can
    carry it out with no access to this database, and mark the boards as asked for. The
    dashboard calls it right after an add, and the caretaker's morning run calls it again,
    which is the retry when Linear could not be reached.

Does NOT: change config/feeds.json, fetch a board, open a pull request, or decide what a
check found. The pull request is an agent's ordinary work on the ticket filed here.

Invariants: `standing`, `screened` and `ticket_text` are pure. One row per board, whatever
the spelling of its token. A board is never recorded when the screen that keeps recruiters
and job boards out of board discovery (app/discover.py `agency_word`) matches it, nor when
it was rejected before (config/boards_rejected.json). A board is marked as asked for only
after Linear accepted the ticket, so a failed post is tried again.
"""

import json
import sqlite3
from pathlib import Path

from app.check import CheckResult, parse_ats_url
from app.discover import REJECTED_PATH, Board, agency_word, feeds_entry, rejected_boards
from app.poll import FEEDS_PATH
from app.sources import registry

QUEUED, COLLECTED, NONE = "queued", "collected", "none"


def load_config(feeds_path: Path = FEEDS_PATH, rejected_path: Path = REJECTED_PATH) -> tuple[list[dict], set[Board]]:
    """(every entry of feeds.json, switched off or not; the boards rejected before)."""
    feeds = json.loads(feeds_path.read_text())["feeds"]
    rejected = rejected_boards(json.loads(rejected_path.read_text())) if rejected_path.exists() else set()
    return feeds, rejected


def _key(board: Board) -> Board:
    return board[0], board[1].lower()


def _listed(feeds: list[dict]) -> dict[Board, bool]:
    """Every board in feeds.json → whether it is switched on."""
    return {(f["type"], f["token"].lower()): f.get("enabled", True) for f in feeds if f.get("token")}


def screened(board: Board, company: str | None, rejected: set[Board]) -> str | None:
    """Why this board may not be added, or None. Pure."""
    if board[0] not in registry.BOARD_SOURCES:
        return f"{board[0]} is not a board system we read"
    if (w := agency_word(board, company)):
        return f"name contains {w!r} (recruiter or job board)"
    if _key(board) in rejected:
        return "rejected before"
    return None


def standing(result: CheckResult, feeds: list[dict], rejected: set[Board]) -> tuple[str, Board | None]:
    """Pure: where the checked posting's company board stands, and the board to record
    when the answer is QUEUED."""
    listed = _listed(feeds)
    board = result.missing_board
    if board is None:
        ref = parse_ats_url(result.url)
        on = ref is not None and ref.token is not None and listed.get((ref.source, ref.token.lower()))
        return (COLLECTED if on else NONE), None
    if _key(board) in listed:
        # In the list after all: switched on means the check ran against an older copy;
        # switched off means someone, or the caretaker, turned it off on purpose.
        return (COLLECTED if listed[_key(board)] else NONE), None
    company = result.posting.company if result.posting else None
    if screened(board, company, rejected):
        return NONE, None
    return QUEUED, board


def note(conn: sqlite3.Connection, result: CheckResult, feeds: list[dict], rejected: set[Board],
         now: str) -> str:
    """Record the board when the check found one to add; return its standing."""
    where, board = standing(result, feeds, rejected)
    if board is not None:
        company = result.posting.company if result.posting else None
        conn.execute("INSERT OR IGNORE INTO board_to_add (source, token, company, url, recorded_at)"
                     " VALUES (?, ?, ?, ?, ?)", (board[0], board[1], company, result.url, now))
        conn.commit()
    return where


def waiting(conn: sqlite3.Connection, feeds: list[dict]) -> list[dict]:
    """Recorded boards that no ticket names yet and feeds.json still lacks, oldest first."""
    listed = _listed(feeds)
    rows = conn.execute("SELECT * FROM board_to_add WHERE ticket IS NULL ORDER BY id").fetchall()
    return [dict(r) for r in rows if (r["source"], r["token"].lower()) not in listed]


def ticket_text(rows: list[dict]) -> tuple[str, str]:
    """Pure: the Linear ticket for these boards. Written for a reader, and an agent, with
    no access to the server: everything needed is in the text."""
    names = [r["company"] or r["token"] for r in rows]
    one = len(rows) == 1
    title = (f"We miss later jobs from {', '.join(names)}: "
             f"add {'its job board' if one else f'these {len(rows)} job boards'} to what we collect")
    entries = "\n".join(json.dumps(feeds_entry((r["source"], r["token"]), r["company"]), ensure_ascii=False)
                        for r in rows)
    labels = " ".join(f"--only {r['source']}:{r['token']}" for r in rows)
    links = "\n".join(f"* {r['company'] or r['token']}: {r['url']}" for r in rows)
    body = f"""Someone added a job on the dashboard from each company below. We stored that one job, but we do not collect the company's job board, so every later posting from the company is missed until the board is added.

{links}

## Build

1. Add each line below to the list of boards we collect (`feeds` in `config/feeds.json`). If a board is already in the list, leave it as it is. This is the same change the link checker makes when it finds a missing board.

```
{entries}
```

2. Check that each board answers, against a scratch database, with no model calls:
   `HIRING_RADAR_DB=<scratch file> uv run python -m app poll --no-extract {labels}`

## Done when

* Every board above is in the list, or the pull request says why one was left out (the board does not answer, or the company is a recruiter or a job board).
* The next morning's collection picks up the companies' open jobs that pass the usual title and city filters.

## Out of scope

Changing the title or city filters. How the dashboard records these boards.

## Agent notes

* Filed by the site itself (HIR-324), from the boards recorded when a job was added on the dashboard. Each board already passed the screen that keeps recruiters and job boards out, and none was rejected before.
* No stored job is read again by the model. The only model cost is reading the new jobs these boards bring.
* One bounded change with nothing on Chandler's list: `autopilot`.
"""
    return title, body


def file_ticket(conn: sqlite3.Connection, feeds: list[dict], post, now: str, log=print) -> str | None:
    """File one ticket for every waiting board and mark them as asked for. `post(title,
    body)` returns the Linear identifier; None when there is no Linear key, and then the
    boards keep waiting. Returns the identifier, or None when nothing was filed."""
    rows = waiting(conn, feeds)
    if not rows:
        return None
    title, body = ticket_text(rows)
    if post is None:
        log(f"{title}\n(not posted: no Linear key)")
        return None
    posted = post(title, body)
    conn.executemany("UPDATE board_to_add SET ticket=?, filed_at=? WHERE id=?",
                     [(posted, now, r["id"]) for r in rows])
    conn.commit()
    log(f"{title}\nposted as {posted}")
    return posted
