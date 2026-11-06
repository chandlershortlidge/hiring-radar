"""The one list of job sources: what exists, what kind each is, and how to fetch it.

Does: name every value `job_source.source` may hold, say which kind of source it is
(board / feed / search / manual), and hold the one function that turns a config/feeds.json
entry into postings. Every other source-name list in the app is derived from here — the
board list used by the CLI add, the API add, discovery and dedup's repost rule; the
complete-feed list behind the dashboard's open rule; the search and manual lists; and the
poller's dispatch. Adding a source is one entry here plus one name in a new migration.

Does NOT: read config/feeds.json (poll does), touch the database, decide what gets
ingested, or filter postings. A `fetch` here is the thin I/O wrapper of one adapter.

The four kinds, and why the difference matters:
  - `board`: one company's own job board (Greenhouse, Lever, Ashby, JOIN). Complete, and
    reachable from a job URL alone, so these are the ones discovery can add, the link
    check can fetch by token, and dedup can read a vanished id as a repost.
  - `feed`: a complete feed across many companies (Arbeitnow, Startup Jobs). Complete, so
    not seeing a job again means it closed, but not tied to one company.
  - `search`: a ranked or windowed sample (JSearch, Arbeitsagentur). Absence proves
    nothing, so these never close a job.
  - `manual`: a person brought the posting (a link, pasted text, a screenshot). No fetch.

Invariant: `NAMES` must match the `job_source.source` CHECK constraint in the newest
migration that rebuilt the table. A migration cannot read Python, so
tests/test_sources_registry.py asserts the two agree and fails if a new source is added
here without a migration (HIR-202).
"""

from collections.abc import Callable
from dataclasses import dataclass

from app.sources import (
    Posting,
    arbeitnow,
    arbeitsagentur,
    ashby,
    greenhouse,
    join,
    jsearch,
    lever,
    startup_jobs,
)

FeedFetch = Callable[[dict], list[Posting]]
KINDS = ("board", "feed", "search", "manual")


def _greenhouse(feed: dict) -> list[Posting]:
    return greenhouse.fetch(feed["token"], feed.get("company"))


def _lever(feed: dict) -> list[Posting]:
    return lever.fetch(feed["token"], feed.get("company"))


def _ashby(feed: dict) -> list[Posting]:
    return ashby.fetch(feed["token"], feed.get("company"))


def _join(feed: dict) -> list[Posting]:
    return join.fetch(feed["token"], feed.get("company"), feed.get("max_pages", 10))


def _arbeitnow(feed: dict) -> list[Posting]:
    return arbeitnow.fetch(max_pages=feed.get("max_pages", 5))


def _startup_jobs(feed: dict) -> list[Posting]:
    return startup_jobs.fetch(feed["search"], feed.get("country"), feed.get("max_pages", 3))


def _arbeitsagentur(feed: dict) -> list[Posting]:
    # Every search result costs a second request for its description, so the title filter
    # runs here, on the search result, instead of after the fetch (HIR-56). Imported in
    # the body because app.ingest derives its repost list from this module.
    from app.ingest import in_scope_title

    return arbeitsagentur.fetch(feed["search"], feed.get("where", "Berlin"), feed.get("radius_km", 25),
                                feed.get("days", 30), feed.get("max_pages", 2), feed.get("size", 50),
                                title_filter=in_scope_title)


def _jsearch(feed: dict) -> list[Posting]:
    return jsearch.fetch(feed["search"], feed.get("country", "de"), feed.get("date_posted", "week"),
                         feed.get("num_pages", 1))


@dataclass(frozen=True)
class Source:
    name: str                       # the value stored in job_source.source
    kind: str                       # one of KINDS
    fetch: FeedFetch | None = None  # None for a manual source: a person brings the posting


# Order is load-bearing only in that derived lists keep it; it is boards, then complete
# feeds, then searches, then the manual ways a person adds a job.
SOURCES: tuple[Source, ...] = (
    Source("greenhouse", "board", _greenhouse),
    Source("lever", "board", _lever),
    Source("ashby", "board", _ashby),
    Source("join", "board", _join),
    Source("startup_jobs", "feed", _startup_jobs),
    Source("arbeitnow", "feed", _arbeitnow),
    Source("arbeitsagentur", "search", _arbeitsagentur),
    Source("jsearch", "search", _jsearch),
    Source("url", "manual"),
    Source("paste", "manual"),
    Source("screenshot", "manual"),
)

BY_NAME: dict[str, Source] = {s.name: s for s in SOURCES}
NAMES: tuple[str, ...] = tuple(s.name for s in SOURCES)


def of_kind(*kinds: str) -> tuple[str, ...]:
    """The source names of these kinds, in registry order."""
    unknown = set(kinds) - set(KINDS)
    if unknown:
        raise ValueError(f"unknown source kind {sorted(unknown)}; one of {', '.join(KINDS)}")
    return tuple(s.name for s in SOURCES if s.kind in kinds)


# One company's own job board: what discovery adds, what the link check fetches by token,
# and the only sources whose vanished id means a repost rather than a concurrent duplicate.
BOARD_SOURCES: tuple[str, ...] = of_kind("board")
# Complete sources: they list every live posting on every poll, so not seeing a job for
# FEED_OPEN_DAYS means it closed (the dashboard's open rule, app/queries.py).
COMPLETE_SOURCES: tuple[str, ...] = of_kind("board", "feed")
# A sample, so absence proves nothing.
SEARCH_SOURCES: tuple[str, ...] = of_kind("search")
# A person added this sighting by hand.
MANUAL_SOURCES: tuple[str, ...] = of_kind("manual")


def fetch(feed: dict) -> list[Posting]:
    """Fetch one config/feeds.json entry through its source's adapter."""
    name = feed["type"]
    source = BY_NAME.get(name)
    if source is None or source.fetch is None:
        raise ValueError(f"unknown feed type {name!r}")
    return source.fetch(feed)
