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
    and map to an active place (geo.ACTIVE_CITIES), or to one named city for a launch;
  - append a board to feeds.json (`add_board`) or boards_rejected.json (`reject_board`)
    when the person says so;
  - or, launching a city (`--launch <city>`, HIR-132), apply Chandler's written board
    policy itself and add what passes: 5+ roles in that city, employers only, the rest
    left unrecorded, and two spending caps that stop the launch instead of adding.

Does NOT: ingest postings, call a model, or page through search results. A search hit is
only a lead. The board is checked live before it is reported, because indexed postings go
stale (cortea, 2026-10-19).

A launch is the one path that writes without being asked, and only within the policy
above (DECISIONS 2026-11-03, HIR-132, which supersedes the 2026-10-19 manual-approval
rule). Everywhere else approval is still manual, and rejecting stays manual always —
a rejection hides a board from every future search.

Invariants: `search_queries`, `harvest`, `new_boards`, `relevant_roles`, `feeds_entry`,
`agency_word`, `estimate_extraction_cost_eur`, `launch_decisions` and `launch_caps` are
pure. `run` does network I/O only through the injected `search` and `fetch_board`, so
tests never touch the network. A failed board fetch is reported and the run goes on, and
is never added — an empty role list from a dead board must not read as "too few roles".
A query with no results is reported, not skipped silently. A cap breach adds nothing at
all, rather than adding boards up to the limit: a half-launched city is worse than none.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

from app.check import default_fetch_board, parse_ats_url
from app.geo import active_place
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


def relevant_roles(postings, city: str | None = None) -> list[str]:
    """Titles (with city) of postings that would pass ingest's title and active-city filters.

    With `city`, only roles in that one city count — what a launch needs, because a board
    full of Berlin roles is not evidence that it hires in New York.
    """
    out = []
    for p in postings:
        place = active_place(p.location_raw, p.title, p.description_text)
        if in_scope_title(p.title) and place and (city is None or place == city):
            out.append(f"{p.title} ({place})")
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
        fetch_board=default_fetch_board, city: str | None = None) -> Report:
    """search(query) -> list[url]; fetch_board(source, token) -> list[Posting].

    With `city`, a candidate's relevant roles are counted in that city only — what a
    launch judges boards on.
    """
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
            c.total, c.relevant = len(postings), relevant_roles(postings, city)
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


# --- launching a city: the written policy, applied without asking (HIR-132) ------------
#
# Chandler's SF choices (HIR-123) turned into code. Every threshold here is his, written on
# the HIR-132 ticket; none of it is this module's judgment to re-tune.

MIN_ROLES_TO_ADD = 5          # "add every board with 5 or more roles that pass the filters"
MAX_LAUNCH_COST_EUR = 10.0    # stop and report rather than add, above this
MAX_DAILY_POSTINGS = 5000     # ...or above this many postings added to the daily download

# One extraction call, measured against app/extract.py on claude-sonnet-5-5 ($2.00 per
# MTok in, $10.00 per MTok out). The system prompt with the taxonomy inlined is ~3.9k
# tokens; a posting runs ~1.7k; the tool schema and the JSON answer make up the rest.
# Deliberately rounded up: a cap that stops a launch too early is cheap to re-run, one
# that stops it too late is not.
EXTRACT_INPUT_TOKENS = 6_500
EXTRACT_OUTPUT_TOKENS = 700
USD_PER_MTOK_IN = 2.00
USD_PER_MTOK_OUT = 10.00
EUR_PER_USD = 0.93

# A conservative screen for "recruitment agency or job aggregator", which the policy skips.
# Substring match on the board token and the company name, both lowercased with separators
# removed, so "talent-partners" and "talentpartners" read alike. Conservative on purpose:
# a missed agency is one noisy feed that can be disabled, while a false positive silently
# drops a real employer. Every verdict is reported, so the screen is auditable.
AGENCY_WORDS = (
    "recruit", "staffing", "headhunt", "jobboard", "jobportal", "jobsite", "aggregator",
    "personalberatung", "personalvermittlung", "zeitarbeit", "workforce", "placement",
    "resourcing", "talentpartner", "talentsolutions", "talentacquisition", "talentgroup",
    "manpower", "randstad", "adecco", "hays", "michaelpage", "roberthalf", "kellyservices",
    "experis", "robertwalters", "pagegroup", "huntscanlon", "jobrapido", "jobleads",
    "learn4good", "ziprecruiter", "indeed", "glassdoor", "monsterjobs",
)


def _squashed(*parts: str | None) -> str:
    return "".join(ch for p in parts if p for ch in p.lower() if ch.isalnum())


def agency_word(board: Board, company: str | None = None) -> str | None:
    """The agency/aggregator word this board's name matches, or None. Pure."""
    text = _squashed(board[1], company)
    return next((w for w in AGENCY_WORDS if w in text), None)


def estimate_extraction_cost_eur(n_postings: int) -> float:
    """What reading `n_postings` once with the current extractor costs, in euros. Pure."""
    usd = n_postings * (EXTRACT_INPUT_TOKENS / 1e6 * USD_PER_MTOK_IN
                        + EXTRACT_OUTPUT_TOKENS / 1e6 * USD_PER_MTOK_OUT)
    return usd * EUR_PER_USD


@dataclass
class LaunchDecision:
    board: Board
    verdict: str                  # "add" | "skip-agency" | "too-few-roles" | "failed"
    why: str
    roles: list[str] = field(default_factory=list)
    total: int = 0


def launch_decisions(candidates: list[Candidate], min_roles: int = MIN_ROLES_TO_ADD,
                     ) -> list[LaunchDecision]:
    """The policy, applied to each candidate. Pure; the order of the checks is the policy's.

    A board that failed to fetch is reported, never added — an empty role list from a dead
    board must not read as "too few roles".
    """
    out = []
    for c in candidates:
        n = len(c.relevant)
        if c.error:
            out.append(LaunchDecision(c.board, "failed", c.error, c.relevant, c.total))
        elif (w := agency_word(c.board)):
            out.append(LaunchDecision(c.board, "skip-agency", f"name contains {w!r}",
                                      c.relevant, c.total))
        elif n >= min_roles:
            out.append(LaunchDecision(c.board, "add", f"{n} roles in the city",
                                      c.relevant, c.total))
        else:
            out.append(LaunchDecision(c.board, "too-few-roles",
                                      f"{n} roles, under the {min_roles} needed; left unrecorded",
                                      c.relevant, c.total))
    return out


def launch_caps(decisions: list[LaunchDecision]) -> tuple[float, int, str | None]:
    """(cost in euros, postings added to the daily download, breach reason or None). Pure.

    The cost is of reading the roles that would actually be stored; the daily figure is
    every posting on the added boards, because a poll downloads a whole board.
    """
    adds = [d for d in decisions if d.verdict == "add"]
    to_read = sum(len(d.roles) for d in adds)
    daily = sum(d.total for d in adds)
    cost = estimate_extraction_cost_eur(to_read)
    breach = None
    if cost > MAX_LAUNCH_COST_EUR:
        breach = (f"reading {to_read} new postings would cost about €{cost:.2f}, "
                  f"over the €{MAX_LAUNCH_COST_EUR:.0f} cap")
    elif daily > MAX_DAILY_POSTINGS:
        breach = (f"the {len(adds)} boards carry {daily} postings to download daily, "
                  f"over the {MAX_DAILY_POSTINGS} cap")
    return cost, daily, breach


def launch_report_lines(city: str, decisions: list[LaunchDecision],
                        cost: float, daily: int, breach: str | None, applied: bool) -> list[str]:
    by = lambda v: [d for d in decisions if d.verdict == v]   # noqa: E731
    lines = [f"launch {city}: {len(decisions)} new boards judged"]
    for verdict, heading in (("add", "added"), ("skip-agency", "skipped (agency/aggregator)"),
                             ("too-few-roles", "left unrecorded"), ("failed", "FAILED to fetch")):
        ds = by(verdict)
        if not ds:
            continue
        lines.append(f"{heading}: {len(ds)}")
        for d in ds:
            lines.append(f"  {d.board[0]}:{d.board[1]}: {d.why}"
                         + (f" — {'; '.join(d.roles[:6])}" if d.roles else ""))
    lines.append(f"one-time model reading: about €{cost:.2f} (cap €{MAX_LAUNCH_COST_EUR:.0f}); "
                 f"{daily} postings added to the daily download (cap {MAX_DAILY_POSTINGS})")
    if breach:
        lines.append(f"STOPPED, nothing added: {breach}")
    elif not applied:
        lines.append("dry run: nothing written")
    else:
        lines.append(f"{len(by('add'))} boards written to config/feeds.json")
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
