"""The admin page: every collected place and career track with its state, and the month's
spending against each limit we have (HIR-398).

Does: answer three questions from what is already stored, and draw them as one page.
`overview` gives one row per place and per track (app/scope.py's list, in its order):
state, read mode, postings stored, open now, waiting to be read, first and last collection
day, days collected, kinds of source, and for an incubating row how ready it is to go live.
`spend` gives the month's model reading, JSearch requests and board searches, each next to
its limit. `page` turns both into HTML; `incubating_section` turns the same rows into the
Monday summary's lines, so the page and the summary cannot print different numbers.

Does NOT: change anything. There is no button and no write: switching a place or track to
live is a line in app/scope.py, through a reviewed pull request. It does not check who is
asking either: `/admin` is kept private by the web server's password
(decisions/2026-11-23-hir-398-…, tests/test_admin.py reads deploy/Caddyfile). It calls no
model, and it is the one reader that shows incubating places and tracks, so nothing a
visitor can reach (app/api.py's read routes, app/mcp_server.py) may call it.

Invariants: every count is a count of distinct jobs; a job posted for two places counts
in both rows, a job in a place and on a track counts in both tables' rows. "Open" is
app/queries.py's open rule and "waiting to be read" is the pipeline's own queue with the
held jobs included, so neither can drift from what the dashboard and the collector mean.
"""

import html
import json
import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from app import caretaker, poll, scope
from app.ingest import family_of
from app.launch_read import MAX_LAUNCH_COST_EUR
from app.pipeline import pending_count
from app.queries import open_clause
from app.reread_cost import USAGE_KEYS, Tokens, price_eur
from app.sources import jsearch

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
PLACE, TRACK = "place", "track"


# --- how ready an incubating row is ---------------------------------------------------------

@dataclass(frozen=True)
class Ready:
    """What is on record towards switching an incubating place or track to live."""
    skill_list: bool | None       # None for a place: every place uses the one shared list
    goldens: int                  # reviewed Goldens drawn from its postings
    launch_sample: str | None     # day of the latest labelling sample drawn only from it

    def text(self) -> str:
        skills = {None: "skill list: the shared one", True: "skill list: yes",
                  False: "skill list: not yet"}[self.skill_list]
        sample = f"launch check sample: {self.launch_sample}" if self.launch_sample else "launch check sample: none"
        return f"{skills}; Goldens: {self.goldens}; {sample}"


def labelling_picks(evals: Path = EVALS) -> list[tuple[str, list[dict]]]:
    """Every labelling run's picked postings, as (run id, picks), oldest run first. A run
    whose record cannot be read is skipped: the page must still load."""
    runs = []
    for path in sorted((evals / "labeling").glob("*/picks.json")):
        try:
            picks = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if isinstance(picks, list) and picks:
            runs.append((path.parent.name, [p for p in picks if isinstance(p, dict)]))
    return runs


def reviewed_goldens(evals: Path = EVALS) -> set[str]:
    """The ids of the Goldens that exist and are not drafts."""
    out = set()
    for path in (evals / "goldens").glob("golden_*.json"):
        try:
            golden = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if not golden.get("draft"):
            out.add(golden.get("id") or path.stem)
    return out


def _belongs(kind: str, name: str, pick: dict) -> bool:
    """Was this labelled posting one of the place's, or one of the track's? A labelling run
    records a posting's first place and its title; the track is read off the title by the
    rule that sorted the job when it was stored."""
    if kind == PLACE:
        return pick.get("place") == name
    return family_of(pick.get("title") or "") == name


def _run_day(run_id: str) -> str:
    return f"{run_id[:4]}-{run_id[4:6]}-{run_id[6:8]}" if run_id[:8].isdigit() else run_id


def readiness(kind: str, name: str, runs: list[tuple[str, list[dict]]], goldens: set[str]) -> Ready:
    """Pure: the ready hint for one incubating place or track, from the labelling runs'
    picks and the ids of the reviewed Goldens."""
    drawn = {p.get("golden_id") for _, picks in runs for p in picks if _belongs(kind, name, p)}
    whole = [run_id for run_id, picks in runs if all(_belongs(kind, name, p) for p in picks)]
    skill_list = None if kind == PLACE else scope.TRACKS[name].read == scope.READ_NOW
    return Ready(skill_list, len(drawn & goldens), _run_day(whole[-1]) if whole else None)


# --- the rows -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Row:
    kind: str                # PLACE or TRACK
    name: str
    state: str               # scope.LIVE or scope.INCUBATING
    read: str                # scope.READ_NOW or scope.READ_LATER
    stored: int
    open_now: int
    waiting: int             # stored and still to be read by the model, held on purpose or not
    first_day: str | None    # YYYY-MM-DD the first posting was stored; None with nothing stored
    last_day: str | None     # YYYY-MM-DD a posting was last seen
    days: int                # first_day to last_day, both included; 0 with nothing stored
    sources: int             # kinds of source that supplied a posting
    ready: Ready | None      # incubating rows only


def _member(kind: str) -> str:
    """SQL (over alias j, one ? for the name) true for the jobs of a place or of a track."""
    if kind == PLACE:
        return "EXISTS (SELECT 1 FROM job_place ap WHERE ap.job_id = j.id AND ap.place = ?)"
    return "j.family = ?"


def _row(conn: sqlite3.Connection, kind: str, name: str, state: str, read: str, now: str,
         version: str, ready: Ready | None) -> Row:
    member = _member(kind)
    stored, first, last = conn.execute(
        f"SELECT count(*), min(j.first_seen), max(j.last_seen) FROM job j WHERE {member}", [name]).fetchone()
    open_sql, open_params = open_clause(now)
    open_now = conn.execute(f"SELECT count(*) FROM job j WHERE {member} AND {open_sql}",
                            [name, *open_params]).fetchone()[0]
    where = {"place": name} if kind == PLACE else {"family": name}
    waiting = pending_count(conn, version, include_held=True, now=now, **where)
    sources = conn.execute(f"SELECT count(DISTINCT s.source) FROM job_source s JOIN job j ON j.id = s.job_id"
                           f" WHERE {member}", [name]).fetchone()[0]
    first_day, last_day = (first[:10], last[:10]) if stored else (None, None)
    days = (date.fromisoformat(last_day) - date.fromisoformat(first_day)).days + 1 if stored else 0
    return Row(kind, name, state, read, stored, open_now, waiting, first_day, last_day, days, sources, ready)


def overview(conn: sqlite3.Connection, now: str, version: str, evals: Path = EVALS) -> list[Row]:
    """One row per collected place, then one per career track, in app/scope.py's order.
    `version` is the current extractor's: a job read at an older one and still open is
    waiting to be read again, exactly as the collector counts it."""
    runs, goldens = labelling_picks(evals), reviewed_goldens(evals)

    def ready(kind, name, state):
        return readiness(kind, name, runs, goldens) if state == scope.INCUBATING else None

    rows = [_row(conn, PLACE, place, state, scope.PLACE_READ.get(place, scope.READ_NOW), now, version,
                 ready(PLACE, place, state)) for place, state in scope.PLACE_STATE.items()]
    rows += [_row(conn, TRACK, name, track.state, track.read, now, version, ready(TRACK, name, track.state))
             for name, track in scope.TRACKS.items()]
    return rows


def _n(count: int, word: str, plural: str | None = None) -> str:
    return f"{count:,} {word if count == 1 else plural or word + 's'}"


def incubating_line(row: Row) -> str:
    """One Monday line for an incubating place or track, from the row the page shows."""
    kind = "city" if row.kind == PLACE else "career track"
    if not row.stored:
        return f"- {row.name} ({kind}): nothing stored yet. Ready? {row.ready.text()}."
    return (f"- {row.name} ({kind}): {_n(row.stored, 'posting')} stored, {row.open_now:,} open now, "
            f"{row.waiting:,} waiting to be read, {_n(row.days, 'day')} collected "
            f"({row.first_day} to {row.last_day}). Ready? {row.ready.text()}.")


def incubating_section(rows: list[Row], weeks: dict[str, str] | None = None) -> str:
    """The Monday summary's part: one line per incubating place or track, or "" when
    nothing is incubating, so the summary is then exactly what it was. `weeks` gives a
    row's week line (`week_volume`), printed under it."""
    lines = [incubating_line(r) + (f"\n  - {weeks[r.name]}" if r.name in (weeks or {}) else "")
             for r in rows if r.state == scope.INCUBATING]
    if not lines:
        return ""
    return "# Collected in the background, not shown yet\n\n" + "\n".join(lines) + "\n"


def week_volume(conn: sqlite3.Connection, track: str, start: str, end: str) -> str:
    """One Monday line for a track (HIR-397): the postings first stored from `start` to
    `end` (days, both included), a day in each of its places, where the week's listings
    came from, and how many of them were a copy of a posting already stored, which dedup
    joined to it instead of storing twice. A job posted for two places counts in both."""
    since = f"{start}T00:00:00Z"
    until = (date.fromisoformat(end) + timedelta(days=1)).isoformat() + "T00:00:00Z"
    days = (date.fromisoformat(end) - date.fromisoformat(start)).days + 1
    new = conn.execute("SELECT count(*) FROM job WHERE family = ? AND first_seen >= ? AND first_seen < ?",
                       (track, since, until)).fetchone()[0]
    places = scope.track_places(track) or scope.places()
    per_place = {p: conn.execute(
        "SELECT count(*) FROM job j JOIN job_place jp ON jp.job_id = j.id WHERE j.family = ?"
        " AND jp.place = ? AND j.first_seen >= ? AND j.first_seen < ?", (track, p, since, until)).fetchone()[0]
        for p in places}
    sightings = conn.execute(
        "SELECT s.source, count(*) AS n,"
        " sum(s.id != (SELECT min(f.id) FROM job_source f WHERE f.job_id = s.job_id)) AS copies"
        " FROM job_source s JOIN job j ON j.id = s.job_id WHERE j.family = ?"
        " AND s.first_seen >= ? AND s.first_seen < ? GROUP BY s.source ORDER BY n DESC, s.source",
        (track, since, until)).fetchall()
    head = f"Last week ({start} to {end}): "
    if not new and not sightings:
        return head + "nothing new stored."
    listed = sum(r["n"] for r in sightings)
    a_day = ", ".join(f"{p} {per_place[p] / days:.1f}" for p in places if per_place[p] or scope.track_places(track))
    shares = ", ".join(f"{r['source']} {round(100 * r['n'] / listed)}%" for r in sightings)
    copies = sum(r["copies"] or 0 for r in sightings)
    return (head + f"{_n(new, 'new posting')}; a day: {a_day or 'none in any place'}; "
            f"from: {shares}; {_n(copies, 'duplicate')} caught (a listing of a posting already stored).")


# --- the month's spending -----------------------------------------------------------------

@dataclass(frozen=True)
class Spend:
    what: str
    used: str
    limit: str
    note: str = ""


def model_reading(conn: sqlite3.Connection, month: str) -> tuple[float, int, int]:
    """(euros, readings priced, readings with no token counts) for the readings stored in
    `month` (YYYY-MM), each priced at its model's full rate. An upper bound: a reading
    sent as a batch cost half, and the record does not say which were."""
    eur, priced, blank = 0.0, 0, 0
    for row in conn.execute("SELECT model, usage FROM extraction_log WHERE created_at LIKE ?", (f"{month}-%",)):
        try:
            usage = json.loads(row["usage"])
        except (ValueError, TypeError):
            usage = {}
        if not (isinstance(usage, dict) and any(usage.get(k) for k in USAGE_KEYS)):
            blank += 1
            continue
        eur += price_eur(Tokens(*[(usage.get(k) or 0) for k in USAGE_KEYS]), row["model"])
        priced += 1
    return eur, priced, blank


def search_spend(conn: sqlite3.Connection, month: str) -> float:
    """Euros the morning caretaker recorded spending on board searches in `month`."""
    total = 0.0
    for row in conn.execute("SELECT data FROM caretaker_log WHERE finding = 'spend' AND day LIKE ?", (f"{month}-%",)):
        try:
            total += float(json.loads(row["data"]).get("eur", 0))
        except (ValueError, TypeError, AttributeError):
            continue
    return total


def spend(conn: sqlite3.Connection, month: str) -> list[Spend]:
    """This month's use next to each limit we have, read from the counters that exist."""
    eur, priced, blank = model_reading(conn, month)
    searches = search_spend(conn, month)
    return [
        Spend("Model reading",
              f"at most €{eur:.2f} ({_n(priced, 'reading')})",
              f"no monthly limit; one city launch or bulk read stops above €{MAX_LAUNCH_COST_EUR:.0f}",
              "Priced at the full rate; readings sent as a batch cost half."
              + (f" {_n(blank, 'reading')} came with no token counts and could not be priced." if blank else "")),
        Spend("Google for Jobs searches (JSearch)",
              f"{_n(poll.jsearch_requests(conn, month), 'request')}",
              f"{jsearch.MONTHLY_CAP:,} requests a month",
              "At the limit those searches stop until the month turns."),
        Spend("Board searches (Brave)",
              f"€{searches:.2f} (about {_n(round(searches / caretaker.SEARCH_EUR), 'search', 'searches')})",
              f"€{caretaker.DAILY_CAP_EUR:.2f} a day",
              "The morning caretaker's searches for boards that moved. The searches a city launch runs are not counted anywhere."),
    ]


# --- the page -----------------------------------------------------------------------------

_CSS = """
:root { color-scheme: light dark; --fg: #1a1a1a; --bg: #fff; --muted: #666; --line: #ddd; --mark: #fff3cd; }
@media (prefers-color-scheme: dark) { :root { --fg: #eee; --bg: #161616; --muted: #aaa; --line: #3a3a3a; --mark: #4a3d0c; } }
body { font: 14px/1.45 system-ui, sans-serif; color: var(--fg); background: var(--bg); margin: 0; padding: 24px 16px; }
main { max-width: 1200px; margin: 0 auto; }
h1 { font-size: 20px; margin: 0 0 4px; } h2 { font-size: 16px; margin: 28px 0 8px; }
p { color: var(--muted); margin: 0 0 12px; max-width: 80ch; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; }
th, td { text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--line); vertical-align: top; white-space: nowrap; }
td.wrap { white-space: normal; min-width: 22ch; }
th { font-weight: 600; color: var(--muted); }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
tr.incubating td { background: var(--mark); }
"""


def _cell(value, cls: str = "") -> str:
    text = "" if value is None else (f"{value:,}" if isinstance(value, int) else str(value))
    return f"<td{f' class={cls!r}' if cls else ''}>{html.escape(text)}</td>"


def _rows_table(rows: list[Row], first_column: str) -> str:
    head = "".join(f"<th{' class=n' if n else ''}>{html.escape(h)}</th>" for h, n in (
        (first_column, 0), ("State", 0), ("Read", 0), ("Stored", 1), ("Open now", 1), ("Waiting to be read", 1),
        ("First collected", 0), ("Last seen", 0), ("Days collected", 1), ("Sources", 1), ("Ready?", 0)))
    body = "".join(
        f"<tr class={html.escape(r.state)!r}>" + _cell(r.name) + _cell(r.state) + _cell(r.read)
        + _cell(r.stored, "n") + _cell(r.open_now, "n") + _cell(r.waiting, "n") + _cell(r.first_day)
        + _cell(r.last_day) + _cell(r.days, "n") + _cell(r.sources, "n")
        + _cell(r.ready.text() if r.ready else "", "wrap") + "</tr>" for r in rows)
    return f"<div class=scroll><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def page(rows: list[Row], spending: list[Spend], now: str) -> str:
    """The whole page as HTML. Pure; every value is escaped."""
    spend_rows = "".join("<tr>" + _cell(s.what) + _cell(s.used) + _cell(s.limit) + _cell(s.note, "wrap") + "</tr>"
                         for s in spending)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>hiring-radar admin</title><style>{_CSS}</style></head>
<body><main>
<h1>What is collected</h1>
<p>Every city and career track, live or incubating (collected in the background and shown nowhere public).
Read-only: switching one to live is a reviewed change to the list of places and tracks. As of {html.escape(now)}.</p>
<h2>Cities</h2>
{_rows_table([r for r in rows if r.kind == PLACE], "City")}
<h2>Career tracks</h2>
{_rows_table([r for r in rows if r.kind == TRACK], "Career track")}
<p>A posting for two cities counts in both rows. "Waiting to be read" counts every stored posting the model has
still to read, held back on purpose or not. "Days collected" runs from the first collection day to the day a
posting was last seen.</p>
<h2>Spending in {html.escape(now[:7])}</h2>
<div class=scroll><table><thead><tr><th>What</th><th>Used this month</th><th>Limit</th><th>Note</th></tr></thead>
<tbody>{spend_rows}</tbody></table></div>
</main></body></html>
"""
