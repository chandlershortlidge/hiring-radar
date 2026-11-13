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
    and the caretaker's weekly section.

Does NOT: run a check, fetch anything, call a model, or write to the database. Filing the
ticket is the caretaker run's (app/caretaker_run.py); this module only writes its text.

Invariants: `count`, `over_threshold`, `week_section` and `ticket_text` are pure. A reason
is always one of app.check.MISS_REASONS. "Already had it" is never a miss: it is counted,
but never the biggest reason and never a ticket.
"""

import sqlite3
from collections import Counter
from dataclasses import dataclass

from app.check import ALREADY_HAD, MISS_REASONS, REASON_TEXT, careers_system, miss_reason
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
