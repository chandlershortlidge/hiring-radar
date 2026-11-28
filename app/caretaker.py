"""The caretaker: each morning, notice broken job sources and decide what to do about them.

Does:
  - judge one company board from what today's poll got and what the database already
    holds: gone (404/410), dead (nothing new for EMPTY_DAYS), shape changed, or fine;
  - judge a country-wide feed or search against its own recent runs (far below its usual);
  - judge the collection as a whole (did not run, or every feed failed) and the cities
    (open-job count fell sharply overnight);
  - search for a dead or gone board's new home with the discovery code, and accept one
    only when it is the same company and has postings the poll would keep;
  - turn a decision into an edit of config/feeds.json — pause, unpause, switch token —
    through the one writer that is allowed to touch only that file;
  - write the day's fixes as the text of one ticket and read them back from it
    (`fix_ticket_text`, `fixes_from_text`, `apply_fixes`): the morning run files the
    ticket, and the pull request that carries it out runs `caretaker apply-fixes`, so the
    edit is made in a reviewed pull request and never on the server (HIR-261);
  - write the weekly summary and the short "cannot wait a week" alert.

Does NOT: call a model, delete or rewrite stored jobs, add a board for a company we don't
track, turn on a city, or touch any rule file. Those are the "never does" lines of HIR-257
and each one is a test in tests/test_caretaker.py. It does not read the database or the
network itself either: callers hand it the poll's numbers and inject `search` and
`fetch_board`, so every decision here is testable without I/O.

Rules and thresholds: DECISIONS 2026-11-12 (HIR-257); acting through a ticket:
decisions/2026-11-19-hir-261-caretaker-acts-through-a-ticket-no-server-credential.md.
"""

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path
from statistics import median

from app import poll
from app.check import default_fetch_board
from app.discover import harvest, relevant_roles
from app.sources import Posting, registry

ROOT = Path(__file__).resolve().parent.parent
FEEDS_PATH = ROOT / "config" / "feeds.json"

EMPTY_DAYS = 3                 # a board silent this long, after giving us postings, is dead
GONE_MARKERS = ("404", "410")  # an error naming one of these means the board no longer exists
FEED_LOW_SHARE = 0.5           # a feed under half its median is "far fewer than usual"
FEED_MIN_HISTORY = 5           # ...judged only once it has this many good runs to compare to
FEED_HISTORY_DAYS = 14
CITY_DROP_SHARE = 0.3          # a city losing more than 30% of its open jobs overnight
CITY_MIN_JOBS = 20             # ...from at least this many; small cities wobble
DAILY_CAP_EUR = 0.50           # model calls plus searches, per day (HIR-257)
SEARCH_EUR = 0.005             # one Brave search: $5 per 1,000 (app/sources/brave.py), rounded up
MAX_CANDIDATES = 5             # boards fetched per moved-board search
# Where a moved board is looked for: one search per hosted board service, at the main
# address the one list of sources gives it. Also the list of what `apply` may pause or move.
BOARD_DOMAINS = registry.BOARD_MAIN_SITE
# The only actions there are. Anything else is refused by `apply`, which is how "never
# deletes, never adds a board, never turns on a city" stays true as code grows.
ACTIONS = ("none", "report", "pause", "unpause", "switch", "rerun_collection")


class Refused(RuntimeError):
    """The caretaker was asked to do something on its never-does list."""


@dataclass(frozen=True)
class FeedRun:
    """What one poll got from one feed."""
    label: str                    # poll's label: greenhouse:doctolib, arbeitnow, ...
    kind: str                     # registry kind: board / feed / search
    ok: bool                      # False when the fetch raised
    seen: int = 0
    error: str | None = None
    fields: frozenset[str] = frozenset()   # Posting fields non-empty on at least one posting
    day: str = ""                 # YYYY-MM-DD


@dataclass
class Finding:
    subject: str                  # feed label, "collection", or "city:<name>"
    finding: str                  # what is wrong, one word
    action: str                   # one of ACTIONS
    detail: str                   # one plain sentence for the weekly summary
    data: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.action not in ACTIONS:
            raise Refused(f"unknown caretaker action {self.action!r}")


# --- reading what the poll got ----------------------------------------------------------

def posting_fields(postings: list[Posting]) -> frozenset[str]:
    """The optional Posting fields that at least one posting filled (the poll records the
    same list in feed_run). A field that was there last week and is gone today means the
    source changed its shape under the adapter."""
    return frozenset(poll.posting_fields(postings))


def _days_before(day: str, n: int) -> str:
    return (date.fromisoformat(day) - timedelta(days=n)).isoformat()


def is_gone(error: str | None) -> bool:
    return bool(error) and any(re.search(rf"\b{m}\b", error) for m in GONE_MARKERS)


# --- spend -------------------------------------------------------------------------------

@dataclass
class Budget:
    """Daily spend, checked before anything that costs money. `spent` starts at what earlier
    runs the same day already spent, so two runs cannot each spend the whole cap."""
    spent: float = 0.0
    cap: float = DAILY_CAP_EUR
    hit: bool = False

    def take(self, eur: float) -> bool:
        if self.spent + eur > self.cap + 1e-9:
            self.hit = True
            return False
        self.spent += eur
        return True


# --- the moved-board search --------------------------------------------------------------

def _squash(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def same_company(company: str, token: str, postings: list[Posting]) -> bool:
    """A found board is this company's when the board token or a posting's company names
    it, case, spaces and punctuation aside. `company` is the name already in feeds.json, so
    a match can only ever point at a company we track."""
    want = _squash(company)
    if not want:
        return False
    if want in _squash(token) or (len(_squash(token)) >= 4 and _squash(token) in want):
        return True
    return any(_squash(p.company) == want for p in postings)


@dataclass
class Move:
    board: tuple[str, str]
    relevant: int
    company: str        # the tracked company's name the new board was matched against


def find_moved_board(feed: dict, search, budget: Budget, known: set, rejected: set,
                     fetch_board=default_fetch_board) -> Move | None:
    """search(query) -> list[url]. One search per board service for the company's name;
    each new board found is fetched and accepted only when it is the same company and has
    a posting the poll would keep. Stops searching when the budget says no."""
    company = feed.get("company") or feed.get("token")
    old = (feed["type"], feed["token"].lower())
    urls = []
    for domain in BOARD_DOMAINS.values():
        if not budget.take(SEARCH_EUR):
            break
        urls += search(f'site:{domain} "{company}"')
    boards, _ = harvest(urls)
    best = None
    for board in [b for b in boards if b != old and b not in known and b not in rejected][:MAX_CANDIDATES]:
        try:
            postings = fetch_board(*board)
        except Exception:  # a dead candidate is just not the answer
            continue
        n = len(relevant_roles(postings))
        if n and same_company(company, board[1], postings) and (best is None or n > best.relevant):
            best = Move(board, n, company)
    return best


# --- judging -----------------------------------------------------------------------------

def judge_board(feed: dict, run: FeedRun, history: list[FeedRun], known_postings: int,
                last_seen: str | None, find_move) -> list[Finding]:
    """One company board. `known_postings` and `last_seen` come from job_source (what this
    board gave us before, and when we last saw any of it); `find_move()` runs the search."""
    out = []
    label, day = run.label, run.day
    silent = (not run.ok) or run.seen == 0
    dead = silent and known_postings > 0 and last_seen is not None and last_seen[:10] <= _days_before(day, EMPTY_DAYS)
    gone = not run.ok and is_gone(run.error)
    if gone or dead:
        why = (f"answers {run.error}" if gone else
               f"has returned nothing we keep since {last_seen[:10]}")
        move = find_move()
        if move:
            new = f"{move.board[0]}:{move.board[1]}"
            out.append(Finding(label, "board_moved", "switch",
                               f"{label} {why}; the company's board is now {new} "
                               f"({move.relevant} postings we would keep), so switch to it.",
                               {"to": list(move.board), "relevant": move.relevant, "company": move.company}))
        elif dead:
            out.append(Finding(label, "board_dead", "pause",
                               f"{label} {why}, and no new board was found, so pause it.",
                               {"last_seen": last_seen}))
        else:
            out.append(Finding(label, "board_gone", "report",
                               f"{label} {why} and no new board was found yet; it is paused "
                               f"if this lasts {EMPTY_DAYS} days.", {"error": run.error}))
        return out
    if not run.ok:
        out.append(Finding(label, "board_error", "report", f"{label} failed: {run.error}.",
                           {"error": run.error}))
        return out
    out += judge_shape(run, history)
    return out


def judge_shape(run: FeedRun, history: list[FeedRun]) -> list[Finding]:
    """Fields every posting used to carry somewhere this week and none carries today."""
    if not run.ok or run.seen == 0:
        return []
    week = _days_before(run.day, 7)
    before = frozenset().union(*[h.fields for h in history if h.ok and h.seen and week <= h.day < run.day])
    missing = sorted(before - run.fields)
    if not missing:
        return []
    return [Finding(run.label, "shape_changed", "report",
                    f"{run.label} stopped sending {', '.join(missing)}; its adapter may need a look.",
                    {"missing": missing})]


def judge_feed(run: FeedRun, history: list[FeedRun]) -> list[Finding]:
    """A country-wide feed or search: an error, or far fewer postings than its usual."""
    if not run.ok:
        return [Finding(run.label, "feed_error", "report", f"{run.label} failed: {run.error}.",
                        {"error": run.error})]
    since = _days_before(run.day, FEED_HISTORY_DAYS)
    past = [h.seen for h in history if h.ok and since <= h.day < run.day]
    out = judge_shape(run, history)
    if len(past) >= FEED_MIN_HISTORY:
        usual = median(past)
        if run.seen < FEED_LOW_SHARE * usual:
            out.append(Finding(run.label, "feed_low", "report",
                               f"{run.label} returned {run.seen} postings; it usually returns about "
                               f"{usual:g}.", {"seen": run.seen, "usual": usual}))
    return out


def judge_collection(day: str, runs: list[FeedRun]) -> list[Finding]:
    """Did today's poll run, and did anything succeed. Either failure: re-run it once."""
    today = [r for r in runs if r.day == day]
    if not today:
        return [Finding("collection", "collection_missing", "rerun_collection",
                        f"The {day} collection did not run; re-run it once.")]
    if not any(r.ok for r in today):
        return [Finding("collection", "collection_failed", "rerun_collection",
                        f"Every source failed in the {day} collection; re-run it once.",
                        {"feeds": len(today)})]
    return []


def judge_pending(pending: int) -> list[Finding]:
    """Jobs still waiting for the model after the poll: a re-read that stopped half way."""
    if pending <= 0:
        return []
    return [Finding("collection", "extraction_unfinished", "report",
                    f"{pending} jobs are still waiting to be read by the model after the collection.",
                    {"pending": pending})]


def judge_cities(today: dict[str, int], yesterday: dict[str, int] | None) -> list[Finding]:
    out = []
    for city, before in sorted((yesterday or {}).items()):
        now = today.get(city, 0)
        if before >= CITY_MIN_JOBS and now < (1 - CITY_DROP_SHARE) * before:
            out.append(Finding(f"city:{city}", "city_drop", "report",
                               f"{city} fell from {before} to {now} open jobs overnight.",
                               {"before": before, "now": now}))
    return out


def recheck_paused(feed: dict, postings: list[Posting] | None, error: str | None) -> list[Finding]:
    """A board the caretaker paused, re-fetched on its weekly check."""
    label = f"{feed['type']}:{feed['token']}"
    if postings is not None and (n := len(relevant_roles(postings))):
        return [Finding(label, "board_back", "unpause",
                        f"{label} has {n} postings we would keep again, so switch it back on.",
                        {"relevant": n})]
    why = error or "still nothing we would keep"
    return [Finding(label, "still_paused", "none", f"{label} stays paused: {why}.")]


def is_recheck_day(day: str, paused_since: str) -> bool:
    """Weekly: the same weekday as the pause, from a week after it."""
    gap = (date.fromisoformat(day) - date.fromisoformat(paused_since)).days
    return gap >= 7 and gap % 7 == 0


# --- acting: the only writes, all to config/feeds.json ----------------------------------

def _label(f: dict) -> str:
    return f"{f['type']}:{f['token']}" if f.get("token") else f["type"]


def apply(doc: dict, finding: Finding, day: str) -> dict:
    """The feeds.json document with `finding`'s action applied. Never adds or removes an
    entry; touches only the one board the finding is about; refuses a switch to another
    company or onto a board already listed, and refuses to switch on a board a person
    disabled."""
    feeds = [dict(f) for f in doc["feeds"]]
    matches = [f for f in feeds if _label(f) == finding.subject]
    if finding.action in ("none", "report", "rerun_collection"):
        return {**doc, "feeds": feeds}
    if len(matches) != 1:
        raise Refused(f"{finding.subject!r} is not exactly one entry in feeds.json")
    f = matches[0]
    if f["type"] not in BOARD_DOMAINS:
        raise Refused(f"{finding.subject} is not a company board; only boards are paused or moved")
    if finding.action == "pause":
        f["enabled"] = False
        f["paused"] = {"since": day, "reason": finding.detail}
    elif finding.action == "unpause":
        if "paused" not in f:
            raise Refused(f"{finding.subject} was disabled by a person, not paused by the caretaker")
        f["enabled"] = True
        del f["paused"]
    elif finding.action == "switch":
        source, token = finding.data["to"]
        if (source, token.lower()) in {(g["type"], g.get("token", "").lower()) for g in feeds}:
            raise Refused(f"{source}:{token} is already in feeds.json")
        ours = f.get("company") or f["token"]
        if not (same_company(ours, token, []) or _squash(finding.data.get("company")) == _squash(ours)):
            raise Refused(f"{source}:{token} does not name {f.get('company')}")
        f["moved_from"] = finding.subject
        f["type"], f["token"] = source, token
        f.pop("paused", None)
        f["enabled"] = True
    return {**doc, "feeds": feeds}


def write_feeds(doc: dict, path: Path = FEEDS_PATH, allowed: Path = FEEDS_PATH) -> None:
    """The caretaker's one file write. `path` must be the feeds file (or, in a test or a dry
    run on a copy, a file with that same name outside the repo) — never the extractor, the
    skill list, a migration, or a rule file."""
    path = Path(path).resolve()
    if path.name != allowed.name:
        raise Refused(f"the caretaker writes only {allowed.name}, not {path}")
    if path.is_relative_to(ROOT) and path != allowed.resolve():
        raise Refused(f"the caretaker writes only {allowed}, not {path}")
    from app.discover import _write_one_per_line
    _write_one_per_line(path, doc, "feeds")


# --- the day's fixes as a ticket, and back (HIR-261) --------------------------------------

FIXES = ("switch", "pause", "unpause", "rerun_collection")
# The fixes that edit the list of job sources, so they travel as a ticket and are made in
# a pull request. Re-running the collection is the one fix made on the server itself.
FEED_FIXES = ("switch", "pause", "unpause")
FIXES_KEY = "caretaker_fixes"
APPLY_COMMAND = "uv run python -m app caretaker apply-fixes"
NO_SPEND_LINE = "Model-call spend: none. Changes only the list of job sources (config/feeds.json)."
_JSON_BLOCK = re.compile(r"```json\s*\n(.*?)\n```", re.S)


def fix_ticket_title(day: str) -> str:
    return f"Caretaker: job-source fixes for {day}"


def fix_ticket_text(rows: list[dict], day: str) -> tuple[str, str]:
    """(title, body) of the ticket that carries `day`'s fixes to a pull request. `rows` are
    logged findings (dicts with day + Finding fields). The body is one plain line per fix,
    then a collapsed block for the agent that picks the ticket up: the exact fixes as JSON
    and the one command that makes them. `fixes_from_text` reads that block back."""
    fixes = [{k: r[k] for k in ("subject", "finding", "action", "detail", "data", "day")} for r in rows]
    if bad := [f["action"] for f in fixes if f["action"] not in FEED_FIXES]:
        raise Refused(f"a fix ticket carries only {', '.join(FEED_FIXES)}, not {bad[0]!r}")
    n = len(fixes)
    body = [f"The morning check of the job sources on {day} found "
            f"{n} fix{'es' if n != 1 else ''} to make to the list of job sources:", ""]
    body += [f"- {f['detail']}" for f in fixes]
    body += ["", NO_SPEND_LINE, "",
             "**Done when:** a pull request that changes only the list of job sources makes "
             "exactly these fixes.", "",
             "+++ Agent notes", "",
             "Save this ticket's text to a file and run, from the repository root:", "",
             f"    {APPLY_COMMAND} <that file>", "",
             "It edits config/feeds.json and nothing else, or refuses and writes nothing "
             "when a fix no longer fits the file (already made, or the entry changed). "
             "Commit that one file and open the pull request.", "",
             "```json", json.dumps({FIXES_KEY: fixes}, indent=2, ensure_ascii=False), "```", "",
             "+++"]
    return fix_ticket_title(day), "\n".join(body) + "\n"


def _fix_rows(text: str) -> list[dict]:
    """The fixes a ticket's text carries, checked: exactly one block, and nothing in it but
    edits of the list of job sources."""
    blocks = []
    for raw in _JSON_BLOCK.findall(text):
        try:
            doc = json.loads(raw)
        except ValueError:
            continue
        if isinstance(doc, dict) and FIXES_KEY in doc:
            blocks.append(doc[FIXES_KEY])
    if len(blocks) != 1:
        raise Refused(f"expected one block of caretaker fixes in the text, found {len(blocks)}")
    rows = blocks[0]
    if not isinstance(rows, list) or not rows:
        raise Refused("the block of caretaker fixes is empty")
    for r in rows:
        if not isinstance(r, dict) or r.get("action") not in FEED_FIXES:
            raise Refused(f"a fix ticket carries only {', '.join(FEED_FIXES)}, not "
                          f"{r.get('action') if isinstance(r, dict) else r!r}")
        try:
            date.fromisoformat(r["day"])
            Finding(r["subject"], r["finding"], r["action"], r["detail"], r.get("data") or {})
        except (KeyError, TypeError, ValueError) as e:
            raise Refused(f"a caretaker fix is not readable: {type(e).__name__}: {e}") from e
    return rows


def _as_finding(r: dict) -> Finding:
    return Finding(r["subject"], r["finding"], r["action"], r["detail"], r.get("data") or {})


def fixes_from_text(text: str) -> list[Finding]:
    """The findings a fix ticket carries, rebuilt from its text."""
    return [_as_finding(r) for r in _fix_rows(text)]


def apply_fixes(doc: dict, text: str) -> dict:
    """The feeds.json document with every fix in a ticket's text applied, each with the day
    it was found. All or nothing: one fix `apply` refuses and nothing is returned."""
    for r in _fix_rows(text):
        try:
            doc = apply(doc, _as_finding(r), r["day"])
        except (KeyError, TypeError, ValueError) as e:   # a switch with no readable target
            raise Refused(f"the fix for {r['subject']} is not readable: {type(e).__name__}: {e}") from e
    return doc


# --- reporting ---------------------------------------------------------------------------

# What reaches Chandler before Monday (HIR-257): the collection down two days running, the
# spend cap hit, and one model run that cost more than app/run_cost.py's alert (HIR-449).
URGENT = ("spend_cap", "run_over_cost")


def spend_findings(budget: Budget) -> list[Finding]:
    if not budget.hit:
        return []
    return [Finding("caretaker", "spend_cap", "report",
                    f"The caretaker reached its €{budget.cap:.2f} daily spending cap and stopped "
                    "searching for moved boards until tomorrow.", {"spent": round(budget.spent, 4)})]


def urgent(today: list[Finding], yesterday: list[Finding]) -> list[str]:
    out = [f.detail for f in today if f.finding in URGENT]
    down = ("collection_missing", "collection_failed")
    if any(f.finding in down for f in today) and any(f.finding in down for f in yesterday):
        out.append("The job collection has failed two days running.")
    return out


def weekly_summary(rows: list[dict], start: str, end: str, acting: bool) -> str:
    """Markdown for the Monday post. `rows` are logged findings (dicts with day + Finding
    fields), oldest first; each subject is reported once, by its latest finding."""
    latest: dict[str, dict] = {}
    for r in rows:
        if r["action"] != "none" or r["subject"] not in latest:
            latest[r["subject"]] = r
    # Acting (HIR-261): a failed collection is re-run on the spot; an edit of the list of
    # job sources is filed as a ticket and made by the pull request that follows.
    fixed_title, paused_title = (("What it fixed or filed to fix", "What it filed to pause") if acting else
                                 ("What it would have fixed", "What it would have paused"))
    broke = [r for r in latest.values() if r["action"] == "report"]
    fixed = [r for r in latest.values() if r["action"] in ("switch", "unpause", "rerun_collection")]
    paused = [r for r in latest.values() if r["action"] == "pause"]
    lines = [f"# Caretaker: {start} to {end}" + ("" if acting else " (report-only: nothing was changed)"), ""]
    if not (broke or fixed or paused):
        return "\n".join(lines + ["Every source worked all week."])
    for title, group in ((fixed_title, fixed), (paused_title, paused),
                         ("What broke and needs you", broke)):
        if group:
            lines += [f"## {title}", ""] + [f"- {r['day']}: {r['detail']}" for r in group] + [""]
    return "\n".join(lines).rstrip() + "\n"


def as_row(f: Finding, day: str, mode: str, done: bool) -> dict:
    return {"day": day, "mode": mode, "done": done, **asdict(f)}


def post_to_linear(title: str, body: str, key: str, team_id: str, post_json) -> str:
    """Create one Linear issue; returns its identifier. post_json(url, payload, headers) is
    injected so tests never reach Linear."""
    q = ("mutation($input: IssueCreateInput!) { issueCreate(input: $input) "
         "{ success issue { identifier } } }")
    payload = {"query": q, "variables": {"input": {"teamId": team_id, "title": title, "description": body}}}
    r = post_json("https://api.linear.app/graphql", payload,
                  {"Authorization": key, "Content-Type": "application/json"})
    created = (r.get("data") or {}).get("issueCreate") or {}
    if not created.get("success"):
        raise RuntimeError(f"Linear refused the issue: {json.dumps(r)[:300]}")
    return created["issue"]["identifier"]
