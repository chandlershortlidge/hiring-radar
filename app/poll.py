"""The daily poll: fetch every enabled feed, ingest, then extract skills for new jobs.

Does: read config/feeds.json, call each adapter, hand postings to ingest, and run
extract_pending. Feeds that fail are logged and skipped so one bad source doesn't block
the rest.

Does NOT: schedule itself (the systemd timer on the VM / `python -m app poll` does), or
retry a failed feed within a run.

Invariant: safe to run twice in a row — the second run finds everything still-listed and
nothing pending.
"""

import json
import sqlite3
from pathlib import Path

from app.ingest import Report, ingest
from app.sources import arbeitnow, arbeitsagentur, ashby, greenhouse, join, jsearch, lever, startup_jobs

ROOT = Path(__file__).resolve().parent.parent
FEEDS_PATH = ROOT / "config" / "feeds.json"


def load_feeds(path: Path = FEEDS_PATH) -> list[dict]:
    return [f for f in json.loads(path.read_text())["feeds"] if f.get("enabled", True)]


def fetch_feed(feed: dict) -> list:
    t = feed["type"]
    if t == "arbeitnow":
        return arbeitnow.fetch(max_pages=feed.get("max_pages", 5))
    if t == "startup_jobs":
        return startup_jobs.fetch(feed["search"], feed.get("country"), feed.get("max_pages", 3))
    if t == "arbeitsagentur":
        return arbeitsagentur.fetch(feed["search"], feed.get("where", "Berlin"), feed.get("radius_km", 25),
                                    feed.get("days", 30), feed.get("max_pages", 2), feed.get("size", 50))
    if t == "jsearch":
        return jsearch.fetch(feed["search"], feed.get("country", "de"), feed.get("date_posted", "week"),
                             feed.get("num_pages", 1))
    if t == "greenhouse":
        return greenhouse.fetch(feed["token"], feed.get("company"))
    if t == "lever":
        return lever.fetch(feed["token"], feed.get("company"))
    if t == "ashby":
        return ashby.fetch(feed["token"], feed.get("company"))
    if t == "join":
        return join.fetch(feed["token"], feed.get("company"), feed.get("max_pages", 10))
    raise ValueError(f"unknown feed type {t!r}")


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


def _known_postings(conn: sqlite3.Connection, feed: dict) -> int:
    """How many job_source rows this company-board feed produced before. 0 for search feeds.

    A board that once yielded postings and now yields none is almost never an empty board;
    it is usually the page format changing under the adapter (JOIN did this in October 2026),
    which the adapter reports as "no jobs" rather than an error."""
    token = feed.get("token")
    if not token:
        return 0
    row = conn.execute("SELECT count(*) FROM job_source WHERE source=? AND url LIKE ?",
                       (feed["type"], f"%/{token}/%")).fetchone()
    return int(row[0]) if row else 0


def poll_feeds(conn: sqlite3.Connection, feeds: list[dict], fetch=fetch_feed, log=print) -> Report:
    total = Report()
    for feed in feeds:
        label = feed_label(feed)
        try:
            postings = fetch(feed)
        except Exception as e:
            log(f"{label}: FAILED {type(e).__name__}: {str(e)[:200]}")
            continue
        r = ingest(conn, postings)
        log(f"{label}: {r.line()}")
        if r.seen == 0 and (known := _known_postings(conn, feed)):
            log(f"{label}: WARNING seen=0 but {known} postings from this board are already in the "
                f"database; the board may have changed its page format (adapter needs checking)")
        for k in ("seen", "still_listed", "merged", "reposts", "new", "skipped_title", "skipped_city"):
            setattr(total, k, getattr(total, k) + getattr(r, k))
        total.new_job_ids += r.new_job_ids
    return total
