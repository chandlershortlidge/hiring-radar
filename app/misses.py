"""Count why checked jobs were missed (HIR-290): per reason, per city, per careers system.

Does:
  - read the check log (`url_check`), one record per URL — its first check, the same rule
    the coverage line in `stats` uses, because /check-url re-checks a URL after adding its
    board and that re-check must not count as a second miss (or as "already had it");
  - recover the reason, company, city and careers system of checks logged before those
    were recorded (migration 023), from what each row already stored: the diagnosis
    sentence, the URL, and the matched job. Nothing is written back;
  - count records per reason, city and careers system, for any date range;
  - say which reason passed the weekly threshold, and write the Linear ticket text for it
    and the caretaker's weekly section;
  - write the Monday summary's trend (HIR-321): the weekly share of checked links a feed
    already had over 8 weeks, overall and per city, how many of each week's misses a feed
    would catch today, the misses by kind of fix, and each city's first-two-weeks baseline.

Does NOT: run a check, fetch anything, call a model, or write to the database. Filing the
ticket is the caretaker run's (app/caretaker_run.py); this module only writes its text.

Invariants: `count`, `over_threshold`, `week_section`, `trend_section`, `fix_kind`,
`baselines` and `ticket_text` are pure. A reason
is always one of app.check.MISS_REASONS. "Already had it" is never a miss: it is counted,
but never the biggest reason and never a ticket.
"""

import sqlite3
from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta

from app.check import (ALREADY_HAD, BOARD_ADDED, JOB_BOARD, LINKEDIN_ONLY, LOCATION_FILTER,
                       MISS_REASONS, NOT_IN_SOURCES, OTHER, OWN_SITE, REASON_TEXT, TITLE_FILTER,
                       UNREADABLE_SYSTEM, careers_system, miss_reason, reach_of)
from app.geo import city_of

# One reason passing this many misses in 7 days gets a ticket. Picked from the checks
# logged 17 Oct to 12 Nov: see DECISIONS 2026-11-13 (HIR-290).
WEEKLY_TICKET_THRESHOLD = 5
# A reason already ticketed is not ticketed again for this many days.
TICKET_QUIET_DAYS = 28
UNKNOWN = "(unknown)"


@dataclass(frozen=True)
class Miss:
    url: str
    checked_at: str
    company: str | None
    city: str | None
    careers_system: str
    reason: str
    detail: str
    recovered: bool        # True: logged before reasons were recorded; read back from the row


def _quoted(text: str, after: str) -> str | None:
    """The value of `after '…'` in a diagnosis sentence ("location 'Paris, France' maps…")."""
    i = text.find(after + " '")
    if i < 0:
        return None
    start = i + len(after) + 2
    end = text.find("'", start)
    return text[start:end] if end > start else None


def recover(row: dict) -> Miss:
    """One url_check row → a Miss. A row written since migration 023 carries its own
    fields; an older one has them worked out from its URL, diagnosis and matched job."""
    if row["reason"]:
        return Miss(row["url"], row["checked_at"], row["company"], row["city"],
                    row["careers_system"] or careers_system(row["url"]), row["reason"],
                    row["reason_detail"] or "", False)
    reason, detail = miss_reason(row["url"], row["verdict"], bool(row["feed_had_it"]), row["diagnosis"])
    diag = row["diagnosis"] or ""
    company, city = row.get("job_company"), row.get("job_city")
    if company is None and '"company": "' in diag:
        company = diag.split('"company": "', 1)[1].split('"', 1)[0] or None
    if city is None:
        city = city_of(_quoted(diag, "location"))
    return Miss(row["url"], row["checked_at"], company, city, careers_system(row["url"]),
                reason, detail, True)


def records(conn: sqlite3.Connection, since: str | None = None, until: str | None = None) -> list[Miss]:
    """The first check of each URL whose date falls in [since, until] (YYYY-MM-DD, either
    end open), oldest first."""
    # An old miss names no job, but the same URL is often added and found by a later check:
    # that job's company and city are the posting's.
    rows = conn.execute("""
        SELECT c.*, j.company AS job_company, j.city AS job_city
        FROM url_check c LEFT JOIN job j ON j.id = coalesce(c.job_id, (
            SELECT c2.job_id FROM url_check c2
            WHERE c2.url = c.url AND c2.job_id IS NOT NULL ORDER BY c2.id LIMIT 1))
        WHERE c.id = (SELECT min(id) FROM url_check WHERE url = c.url)
          AND (:since IS NULL OR substr(c.checked_at, 1, 10) >= :since)
          AND (:until IS NULL OR substr(c.checked_at, 1, 10) <= :until)
        ORDER BY c.id
    """, {"since": since, "until": until}).fetchall()
    return [recover(dict(r)) for r in rows]


def count(misses: list[Miss]) -> dict[str, Counter]:
    """{'reason' | 'city' | 'careers_system': Counter}. Reasons in the fixed list's order,
    every reason present even at 0, so a report always shows the whole list."""
    reasons = Counter(dict.fromkeys(MISS_REASONS, 0))
    reasons.update(m.reason for m in misses)
    return {"reason": reasons,
            "city": Counter(m.city or UNKNOWN for m in misses),
            "careers_system": Counter(m.careers_system for m in misses)}


def biggest(misses: list[Miss]) -> tuple[str, int] | None:
    """The most common real miss reason, or None when there was no miss."""
    c = Counter(m.reason for m in misses if m.reason != ALREADY_HAD)
    if not c:
        return None
    top = max(c.values())
    return next((r, top) for r in MISS_REASONS if c.get(r) == top)


def over_threshold(misses: list[Miss], threshold: int = WEEKLY_TICKET_THRESHOLD) -> list[tuple[str, int]]:
    """Reasons with at least `threshold` misses among `misses` (the caller passes 7 days),
    in the fixed list's order. "Already had it" never counts."""
    c = Counter(m.reason for m in misses if m.reason != ALREADY_HAD)
    return [(r, c[r]) for r in MISS_REASONS if c.get(r, 0) >= threshold]


def report_lines(misses: list[Miss], since: str | None, until: str | None) -> list[str]:
    """The `miss-reasons` command's output."""
    span = f"{since or 'the first check'} to {until or 'today'}"
    if not misses:
        return [f"No checked URLs from {span}."]
    c = count(misses)
    real = sum(n for r, n in c["reason"].items() if r != ALREADY_HAD)
    recovered = sum(m.recovered for m in misses)
    lines = [f"{len(misses)} checked URLs from {span} (first check of each): {real} missed, "
             f"{c['reason'][ALREADY_HAD]} already in the poll."]
    if recovered:
        lines.append(f"{recovered} of them were checked before reasons were recorded; their "
                     f"reason was recovered from what the check printed.")
    lines += ["", "by reason:"] + [f"  {n:>4}  {REASON_TEXT[r]}" for r, n in c["reason"].items()]
    for key, title in (("city", "by city"), ("careers_system", "by careers system")):
        lines += ["", f"{title}:"] + [f"  {n:>4}  {k}" for k, n in c[key].most_common()]
    return lines


def week_section(misses: list[Miss], start: str, end: str) -> str:
    """Markdown for the caretaker's weekly summary: the 7 days' count and the biggest reason."""
    head = f"## Jobs we missed, {start} to {end}\n\n"
    real = [m for m in misses if m.reason != ALREADY_HAD]
    had = len(misses) - len(real)
    if not misses:
        return head + "No job links were checked this week.\n"
    top = biggest(misses)
    lines = [f"{len(misses)} job links checked: {len(real)} we had missed, {had} we already had."]
    if top:
        lines.append(f"Biggest reason: {REASON_TEXT[top[0]]} ({top[1]} of {len(real)}).")
    c = count(real)
    lines += [""] + [f"- {REASON_TEXT[r]}: {n}" for r, n in c["reason"].items() if n and r != ALREADY_HAD]
    return head + "\n".join(lines) + "\n"


# --- the trend: is the share of jobs we miss going down? (HIR-321) ------------------------

TREND_WEEKS = 8
# A week with fewer checks than this shows its numbers but says "too few checks", so a
# quiet week is not read as a trend (HIR-321).
MIN_WEEK_CHECKS = 10
BASELINE_DAYS = 14

# The kind of fix that would have caught a miss, and so how far that fix carries.
EVERY_CITY, CITY_BY_CITY, BY_HAND, UNSORTED = "every_city", "city_by_city", "by_hand", "unsorted"
FIX_TEXT = {
    EVERY_CITY: "a careers system we cannot read, or a filter that read the job wrong: one fix helps every city",
    CITY_BY_CITY: "one company's board not added yet: fixed city by city",
    BY_HAND: "a posting no feed can reach (company's own site, LinkedIn, a job board or recruiter): only by hand",
    UNSORTED: "other (closed or re-posted, or a result the checker could not sort)",
}


def fix_kind(m: Miss) -> str:
    """Pure: which kind of fix would have caught this miss. Uses only the stored reason and
    careers system, so it never changes how a miss was recorded."""
    if m.reason == NOT_IN_SOURCES:
        return CITY_BY_CITY
    if m.reason in (TITLE_FILTER, LOCATION_FILTER):
        return EVERY_CITY
    if m.reason == UNREADABLE_SYSTEM:
        return BY_HAND if m.careers_system == OWN_SITE else EVERY_CITY
    if m.reason == LINKEDIN_ONLY or (m.reason == OTHER and m.careers_system == JOB_BOARD):
        return BY_HAND
    return UNSORTED


def _shift(day: str, days: int) -> str:
    return (date.fromisoformat(day) + timedelta(days=days)).isoformat()


def _share(had: int, n: int) -> str:
    return f"{round(100 * had / n)}%" if n else "-"


def _rate(rows: list[Miss]) -> str:
    """'62% (13)' — the share a feed already had, and how many links it is out of."""
    had = sum(m.reason == ALREADY_HAD for m in rows)
    return f"{_share(had, len(rows))} ({len(rows)})"


def _note(n: int) -> str:
    return "" if n >= MIN_WEEK_CHECKS else "too few checks"


def trend_section(all_misses: list[Miss], end: str, feeds: list[dict], weeks: int = TREND_WEEKS) -> str:
    """Markdown for the Monday summary: the last `weeks` weeks ending on `end`, each the
    share of first-checked links a feed already had, overall and per city; how many of each
    week's misses a feed would catch today; the misses by kind of fix; each city's starting
    point. `all_misses` is every record (records(conn)), since a city's starting point can
    be older than the table. Pure, given `feeds`."""
    head = f"## Are we missing fewer jobs? The last {weeks} weeks\n\n"
    spans = [(_shift(end, -7 * i - 6), _shift(end, -7 * i)) for i in reversed(range(weeks))]
    in_span = [m for m in all_misses if spans[0][0] <= m.checked_at[:10] <= end]
    if not in_span:
        return head + f"No job links were checked in the last {weeks} weeks.\n"
    by_week = [[m for m in in_span if a <= m.checked_at[:10] <= b] for a, b in spans]

    lines = ["Of the job links checked by hand (first check of each link), the share a feed "
             "already had. \"Would catch today\" is how many of that week's misses a feed reads "
             "now, because the board or careers system was added since.", "",
             "| week from | checked | feed had it | share | missed | would catch today | |",
             "|---|---|---|---|---|---|---|"]
    for (a, _), rows in zip(spans, by_week):
        had = sum(m.reason == ALREADY_HAD for m in rows)
        missed = [m for m in rows if m.reason != ALREADY_HAD]
        now = sum(reach_of(m.url, False, feeds) == BOARD_ADDED for m in missed)
        lines.append(f"| {a} | {len(rows)} | {had} | {_share(had, len(rows))} | {len(missed)} | "
                     f"{now} | {_note(len(rows))} |")

    # Unknown last: it is not a city, and it is mostly misses (a link a feed had always
    # names its job's city), so it is the caveat on the other columns, not a column to read.
    cities = sorted({m.city or UNKNOWN for m in in_span}, key=lambda c: (
        c == UNKNOWN, -sum((m.city or UNKNOWN) == c for m in in_span), c))
    lines += ["", "Per city: the share a feed already had (links checked). Fewer than "
              f"{MIN_WEEK_CHECKS} checks in a week is too few to read as a trend."]
    if UNKNOWN in cities:
        lines.append(f"{UNKNOWN} is a link whose city could not be read, almost always a miss, "
                     "so each city's share is higher than its true share by about that much.")
    lines += ["",
              "| week from | " + " | ".join(cities) + " |", "|---" * (len(cities) + 1) + "|"]
    for (a, _), rows in zip(spans, by_week):
        cells = []
        for c in cities:
            mine = [m for m in rows if (m.city or UNKNOWN) == c]
            cells.append(_rate(mine) if mine else "-")
        lines.append(f"| {a} | " + " | ".join(cells) + " |")

    real = [m for m in in_span if m.reason != ALREADY_HAD]
    kinds = Counter(fix_kind(m) for m in real)
    lines += ["", f"The {len(real)} misses of these {weeks} weeks, by the kind of fix that would have caught them:", ""]
    lines += [f"- {FIX_TEXT[k]}: {kinds.get(k, 0)}" for k in (EVERY_CITY, CITY_BY_CITY, BY_HAND, UNSORTED)
              if k != UNSORTED or kinds.get(k)]

    lines += ["", f"Each city's starting point: the share a feed already had in its first "
              f"{BASELINE_DAYS} days of checks.", ""]
    for c, first, rows in baselines(all_misses):
        lines.append(f"- {c}, from {first}: {_rate(rows)}" + (f", {_note(len(rows))}" if _note(len(rows)) else ""))
    return head + "\n".join(lines) + "\n"


def baselines(all_misses: list[Miss]) -> list[tuple[str, str, list[Miss]]]:
    """Pure: (city, day of its first check, its checks in the first BASELINE_DAYS days) for
    every city with a check, oldest city first. A city's baseline is fixed once its first
    two weeks are over, so a new city can be compared with Berlin from the start. A check
    with no city has no starting point."""
    first: dict[str, str] = {}
    for m in sorted(all_misses, key=lambda m: m.checked_at):
        if m.city:
            first.setdefault(m.city, m.checked_at[:10])
    out = []
    for c, day in sorted(first.items(), key=lambda kv: (kv[1], kv[0])):
        last = _shift(day, BASELINE_DAYS - 1)
        out.append((c, day, [m for m in all_misses if m.city == c and day <= m.checked_at[:10] <= last]))
    return out


def ticket_text(reason: str, n: int, misses: list[Miss], start: str, end: str) -> tuple[str, str]:
    """(title, body) of the ticket the caretaker files when `reason` passes the threshold.
    The body lists every record, so the fix can be written from it alone."""
    title = f"Missed jobs: {n} in a week because {REASON_TEXT[reason]}"
    rows = [m for m in misses if m.reason == reason]
    body = [f"From {start} to {end}, {n} job links Chandler checked had been missed because "
            f"{REASON_TEXT[reason]}. That passes the caretaker's limit of "
            f"{WEEKLY_TICKET_THRESHOLD} a week for one reason, so this ticket was filed "
            f"automatically (HIR-290).", "", "| checked | company | city | careers system | detail | link |",
            "|---|---|---|---|---|---|"]
    body += [f"| {m.checked_at[:10]} | {m.company or UNKNOWN} | {m.city or UNKNOWN} | "
             f"{m.careers_system} | {m.detail.replace('|', '/') or '-'} | {m.url} |" for m in rows]
    body += ["", "Count any range again with `uv run python -m app miss-reasons --since <day>`."]
    return title, "\n".join(body) + "\n"
