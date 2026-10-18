"""The daily poll: fetch every enabled feed, ingest, then extract skills for new jobs.

Does: read config/feeds.json, call each adapter, hand postings to ingest, and run
extract_pending. Feeds that fail are logged and skipped so one bad source doesn't block
the rest.

Does NOT: schedule itself (Railway cron / crontab / `python -m app poll` does), or
retry a failed feed within a run.

Invariant: safe to run twice in a row — the second run finds everything still-listed and
nothing pending.
"""

import json
import sqlite3
from pathlib import Path

from app.ingest import Report, ingest
from app.sources import arbeitnow, arbeitsagentur, ashby, greenhouse, lever, startup_jobs

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
    if t == "greenhouse":
        return greenhouse.fetch(feed["token"], feed.get("company"))
    if t == "lever":
        return lever.fetch(feed["token"], feed.get("company"))
    if t == "ashby":
        return ashby.fetch(feed["token"], feed.get("company"))
    raise ValueError(f"unknown feed type {t!r}")


def poll_feeds(conn: sqlite3.Connection, feeds: list[dict], fetch=fetch_feed, log=print) -> Report:
    total = Report()
    for feed in feeds:
        label = feed["type"] + (f":{feed.get('token') or feed.get('search', '')}" if feed.get("token") or feed.get("search") else "")
        try:
            postings = fetch(feed)
        except Exception as e:
            log(f"{label}: FAILED {type(e).__name__}: {str(e)[:200]}")
            continue
        r = ingest(conn, postings)
        log(f"{label}: {r.line()}")
        for k in ("seen", "still_listed", "merged", "reposts", "new", "skipped_title", "skipped_city"):
            setattr(total, k, getattr(total, k) + getattr(r, k))
        total.new_job_ids += r.new_job_ids
    return total
