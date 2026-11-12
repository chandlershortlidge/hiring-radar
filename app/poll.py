"""The daily poll: fetch every enabled feed, ingest, then extract skills for new jobs.

Does: read config/feeds.json, call each adapter, hand postings to ingest, and run
extract_pending. Feeds that fail are logged and skipped so one bad source doesn't block
the rest. Each feed's result (worked or not, how many postings, which fields they carried)
is also kept in `feed_run`, which the morning caretaker reads (HIR-257).

Does NOT: schedule itself (the systemd timer on the VM / `python -m app poll` does), or
retry a failed feed within a run.

Invariant: safe to run twice in a row — the second run finds everything still-listed and
nothing pending.
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.ingest import Report, ingest
from app.sources import registry

ROOT = Path(__file__).resolve().parent.parent
FEEDS_PATH = ROOT / "config" / "feeds.json"


def load_feeds(path: Path = FEEDS_PATH) -> list[dict]:
    return [f for f in json.loads(path.read_text())["feeds"] if f.get("enabled", True)]


def fetch_feed(feed: dict) -> list:
    """Dispatch one feeds.json entry to its adapter. Which types exist and how each is
    fetched lives in the source registry (app/sources/registry.py), not here."""
    return registry.fetch(feed)


def feed_label(feed: dict) -> str:
    """`ashby:jupus`, `startup_jobs:AI engineer`, `arbeitnow` — what poll logs and `--only` matches."""
    key = feed.get("token") or feed.get("search")
    return feed["type"] + (f":{key}" if key else "")


def select_feeds(feeds: list[dict], only: list[str]) -> list[dict]:
    """Pure: the feeds whose label is in `only` (all of them when `only` is empty).
    An unknown label is an error, not a silent no-op poll."""
    if not only:
        return feeds
    unknown = set(only) - {feed_label(f) for f in feeds}
    if unknown:
        raise ValueError(f"no enabled feed labelled {sorted(unknown)}")
    return [f for f in feeds if feed_label(f) in only]


# Posting fields an adapter fills when the source gives them. One that was there last week
# and is missing today means the source changed its shape under the adapter (HIR-257).
OPTIONAL_FIELDS = ("company", "location_raw", "posted_at", "url")


def posting_fields(postings: list) -> list[str]:
    """Pure: the optional fields at least one posting filled, in OPTIONAL_FIELDS order."""
    return [f for f in OPTIONAL_FIELDS if any(getattr(p, f, None) for p in postings)]


def record_run(conn: sqlite3.Connection, feed: dict, postings: list | None,
               error: str | None = None, day: str | None = None) -> None:
    """Keep one feed's result in feed_run. `postings` is None when the fetch raised."""
    source = registry.BY_NAME.get(feed["type"])
    conn.execute("INSERT INTO feed_run (day, label, kind, ok, seen, error, fields) VALUES (?,?,?,?,?,?,?)",
                 (day or datetime.now(timezone.utc).date().isoformat(), feed_label(feed),
                  source.kind if source else "unknown", int(postings is not None),
                  len(postings or []), error, json.dumps(posting_fields(postings or []))))
    conn.commit()


def board_history(conn: sqlite3.Connection, feed: dict) -> tuple[int, str | None]:
    """How many job_source rows this company-board feed produced, and when any of them was
    last seen. (0, None) for search feeds and boards that never gave us anything."""
    token = feed.get("token")
    if not token:
        return 0, None
    row = conn.execute("SELECT count(*), max(last_seen) FROM job_source WHERE source=? AND url LIKE ?",
                       (feed["type"], f"%/{token}/%")).fetchone()
    return (int(row[0]), row[1]) if row else (0, None)


def _known_postings(conn: sqlite3.Connection, feed: dict) -> int:
    """How many job_source rows this company-board feed produced before. 0 for search feeds.

    A board that once yielded postings and now yields none is almost never an empty board;
    it is usually the page format changing under the adapter (JOIN did this in October 2026),
    which the adapter reports as "no jobs" rather than an error."""
    return board_history(conn, feed)[0]


def poll_feeds(conn: sqlite3.Connection, feeds: list[dict], fetch=fetch_feed, log=print) -> Report:
    total = Report()
    for feed in feeds:
        label = feed_label(feed)
        try:
            postings = fetch(feed)
        except Exception as e:
            log(f"{label}: FAILED {type(e).__name__}: {str(e)[:200]}")
            record_run(conn, feed, None, f"{type(e).__name__}: {str(e)[:200]}")
            continue
        record_run(conn, feed, postings)
        r = ingest(conn, postings)
        log(f"{label}: {r.line()}")
        if r.seen == 0 and (known := _known_postings(conn, feed)):
            log(f"{label}: WARNING seen=0 but {known} postings from this board are already in the "
                f"database; the board may have changed its page format (adapter needs checking)")
        for k in ("seen", "still_listed", "merged", "reposts", "new", "skipped_title", "skipped_city",
                  "skipped_company", "skipped_agency"):
            setattr(total, k, getattr(total, k) + getattr(r, k))
        total.new_job_ids += r.new_job_ids
    return total
