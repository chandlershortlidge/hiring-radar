"""discover-boards: find company job boards we don't poll yet, from web search results.

Board feeds (Greenhouse, Lever, Ashby, JOIN) cover one company each, and none of those
services lists the companies using it. The search feeds never link to company ATS pages
(DECISIONS 2026-10-19), so the only way to find a new board is a page that mentions it.

Does:
  - build one `site:<domain> <query>` search per (domain × query) in config/discover.json;
  - harvest result URLs into distinct (source, token) boards via check.parse_ats_url,
    counting the URLs that are not a board job page;
  - drop boards already in config/feeds.json (enabled or not) or in
    config/boards_rejected.json;
  - fetch each remaining board live and keep the postings that pass ingest's title filter
    and map to a tracked city;
  - append a board to feeds.json (`add_board`) or boards_rejected.json (`reject_board`)
    when the person says so.

Does NOT: add a board on its own, ingest postings, call a model, or page through search
results. A search hit is only a lead. The board is checked live before it is reported,
because indexed postings go stale (cortea, 2026-10-19).

Invariants: `search_queries`, `harvest`, `new_boards`, `relevant_roles` and
`feeds_entry` are pure. `run` does network I/O only through the injected `search` and
`fetch_board`, so tests never touch the network. A failed board fetch is reported and the
run goes on. A query with no results is reported, not skipped silently.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

from app.check import default_fetch_board, parse_ats_url
from app.geo import city_of
from app.ingest import in_scope_title
from app.poll import FEEDS_PATH

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "discover.json"
REJECTED_PATH = ROOT / "config" / "boards_rejected.json"

Board = tuple[str, str]   # (source, token), e.g. ("greenhouse", "intercom")
BOARD_SOURCES = ("greenhouse", "lever", "ashby", "join")


def search_queries(config: dict) -> list[str]:
    return [f"site:{d} {q}" for d in config["domains"] for q in config["queries"]]


def harvest(urls: list[str]) -> tuple[list[Board], int]:
    """Result URLs → (distinct boards in first-seen order, URLs that name no board)."""
    boards, unparsed = {}, 0
    for url in urls:
        ref = parse_ats_url(url)
        if ref is None or ref.token is None:
            unparsed += 1
        else:
            boards.setdefault((ref.source, ref.token.lower()), None)
    return list(boards), unparsed


def known_boards(feeds_doc: dict) -> set[Board]:
    """Every board in feeds.json, disabled ones included."""
    return {(f["type"], f["token"].lower()) for f in feeds_doc.get("feeds", []) if f.get("token")}


def rejected_boards(rejected_doc: dict) -> set[Board]:
    return {(b["source"], b["token"].lower()) for b in rejected_doc.get("boards", [])}


def new_boards(found: list[Board], known: set[Board], rejected: set[Board]) -> list[Board]:
    return [b for b in found if b not in known and b not in rejected]


def relevant_roles(postings) -> list[str]:
    """Titles (with city) of postings that would pass ingest's title and city filters."""
    out = []
    for p in postings:
        city = city_of(p.location_raw)
        if in_scope_title(p.title) and city:
            out.append(f"{p.title} ({city})")
    return out


def feeds_entry(board: Board, company: str | None = None) -> dict:
    source, token = board
    return {"type": source, "enabled": True, "token": token, "company": company or token}


def parse_board(text: str) -> Board:
    source, sep, token = text.partition(":")
    if not sep or not source or not token:
        raise ValueError(f"expected source:token (e.g. greenhouse:intercom), got {text!r}")
    if source not in BOARD_SOURCES:
        raise ValueError(f"{source!r} is not a board source; one of {', '.join(BOARD_SOURCES)}")
    return source, token.lower()


@dataclass
class Candidate:
    board: Board
    total: int = 0
    relevant: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass
class Report:
    queries: list[tuple[str, int]] = field(default_factory=list)   # (query, result count)
    urls: int = 0
    unparsed: int = 0
    found: int = 0
    known: int = 0
    rejected: int = 0
    candidates: list[Candidate] = field(default_factory=list)


def run(config: dict, feeds_doc: dict, rejected_doc: dict, search,
        fetch_board=default_fetch_board) -> Report:
    """search(query) -> list[url]; fetch_board(source, token) -> list[Posting]."""
    r = Report()
    urls = []
    for q in search_queries(config):
        hits = search(q)
        r.queries.append((q, len(hits)))
        urls += hits
    r.urls = len(urls)
    found, r.unparsed = harvest(urls)
    known, rejected = known_boards(feeds_doc), rejected_boards(rejected_doc)
    r.found = len(found)
    r.known = sum(b in known for b in found)
    r.rejected = sum(b in rejected and b not in known for b in found)
    for board in new_boards(found, known, rejected):
        c = Candidate(board)
        try:
            postings = fetch_board(*board)
            c.total, c.relevant = len(postings), relevant_roles(postings)
        except Exception as e:  # one dead board must not stop the run
            c.error = f"{type(e).__name__}: {str(e)[:160]}"
        r.candidates.append(c)
    return r


def report_lines(r: Report) -> list[str]:
    lines = [f"search: {q} → {n} results" if n else f"search: {q} → 0 results (check the query)"
             for q, n in r.queries]
    lines.append(f"{len(r.queries)} Brave searches; {r.urls} URLs → {r.found} boards "
                 f"({r.unparsed} URLs were not a board job page); "
                 f"{r.known} already in feeds.json, {r.rejected} rejected before")
    relevant = [c for c in r.candidates if c.relevant and not c.error]
    nothing = [c for c in r.candidates if not c.relevant and not c.error]
    failed = [c for c in r.candidates if c.error]
    lines.append(f"new boards with relevant roles: {len(relevant)}")
    for c in relevant:
        lines.append(f"  {c.board[0]}:{c.board[1]}: {c.total} jobs, {len(c.relevant)} relevant: "
                     + "; ".join(c.relevant))
        lines.append(f"    feeds.json: {json.dumps(feeds_entry(c.board))}")
    lines.append(f"nothing relevant now: {len(nothing)}")
    for c in nothing:
        lines.append(f"  {c.board[0]}:{c.board[1]}: {c.total} jobs, 0 relevant")
    if failed:
        lines.append(f"board fetch FAILED: {len(failed)}")
        for c in failed:
            lines.append(f"  {c.board[0]}:{c.board[1]}: {c.error}")
    return lines


# --- approval: the only writes ---------------------------------------------------------

def add_board(board: Board, path: Path = FEEDS_PATH, company: str | None = None) -> bool:
    """Append the board to feeds.json, one object per line like the rest. False if present."""
    doc = json.loads(path.read_text())
    if board in known_boards(doc):
        return False
    doc["feeds"].append(feeds_entry(board, company))
    _write_one_per_line(path, doc, "feeds")
    return True


def reject_board(board: Board, reason: str, today: str, path: Path = REJECTED_PATH) -> bool:
    """Append to boards_rejected.json. False if it is already there."""
    doc = json.loads(path.read_text())
    if board in rejected_boards(doc):
        return False
    doc["boards"].append({"source": board[0], "token": board[1], "reason": reason, "date": today})
    _write_one_per_line(path, doc, "boards")
    return True


def _write_one_per_line(path: Path, doc: dict, key: str) -> None:
    head = {k: v for k, v in doc.items() if k != key}
    parts = [f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in head.items()]
    items = ",\n".join(f"    {json.dumps(x, ensure_ascii=False)}" for x in doc[key])
    parts.append(f'  {json.dumps(key)}: [\n{items}\n  ]' if items else f"  {json.dumps(key)}: []")
    path.write_text("{\n" + ",\n".join(parts) + "\n}\n")
