"""The source registry is the one list of job sources (HIR-202).

The test that matters most here is `test_registry_matches_database_check`: a migration is
SQL and cannot read Python, so nothing but a test can catch a source added to the registry
without being allowed in the database. Without it, the new source's sightings would fail to
store at the first poll, in production, with an IntegrityError.

The rest pins the derived lists to the values they had when they were separate copies, so
this restructure is provably behaviour-preserving, and pins the dispatch (which adapter is
called with which arguments) that used to be an if-chain in the poller.
"""

import re

import pytest

from app import check, db, discover, ingest, poll, queries
from app.sources import registry

# The kind each source had when the lists were written out by hand, before the registry
# existed. Changing one of these changes behaviour (which jobs count as open, which
# sightings can be reposts), so it is not tidying. Stated per source rather than as whole
# lists so that adding a source stays one registry entry plus one migration line.
KIND_WAS = {
    "greenhouse": "board", "lever": "board", "ashby": "board", "join": "board",
    "startup_jobs": "feed", "arbeitnow": "feed",
    "jsearch": "search", "arbeitsagentur": "search",
    "url": "manual", "paste": "manual", "screenshot": "manual",
}


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def _check_names(conn) -> set[str]:
    """The source names the database actually allows, read from its own schema."""
    sql = conn.execute("SELECT sql FROM sqlite_master WHERE name='job_source'").fetchone()[0]
    m = re.search(r"source\s+TEXT NOT NULL CHECK \(source IN\s*\((.*?)\)\)", sql, re.S)
    assert m, f"no source CHECK found in job_source schema:\n{sql}"
    return set(re.findall(r"'([^']*)'", m.group(1)))


def test_registry_matches_database_check(conn):
    """Add a source to the registry and forget the migration, and this fails."""
    assert _check_names(conn) == set(registry.NAMES)


def test_every_registry_source_can_be_stored(conn):
    """The CHECK read above is the real constraint: each name inserts without error."""
    conn.execute("INSERT INTO job (id, description_text, first_seen, last_seen) VALUES (1,'x','t','t')")
    for i, name in enumerate(registry.NAMES):
        conn.execute("INSERT INTO job_source (job_id, source, source_job_id, first_seen, last_seen) "
                     "VALUES (1, ?, ?, 't', 't')", (name, f"id{i}"))
    stored = {r[0] for r in conn.execute("SELECT DISTINCT source FROM job_source")}
    assert stored == set(registry.NAMES)


def test_unknown_source_is_still_refused(conn):
    conn.execute("INSERT INTO job (id, description_text, first_seen, last_seen) VALUES (1,'x','t','t')")
    with pytest.raises(Exception):
        conn.execute("INSERT INTO job_source (job_id, source, first_seen, last_seen) "
                     "VALUES (1, 'not_a_source', 't', 't')")


def test_names_are_unique_and_kinds_are_known():
    assert len(registry.NAMES) == len(set(registry.NAMES))
    assert {s.kind for s in registry.SOURCES} <= set(registry.KINDS)


def test_only_manual_sources_have_no_fetch():
    for s in registry.SOURCES:
        assert (s.fetch is None) == (s.kind == "manual"), s.name


def test_of_kind_rejects_a_kind_that_does_not_exist():
    with pytest.raises(ValueError):
        registry.of_kind("board", "bord")


@pytest.mark.parametrize("name, kind", sorted(KIND_WAS.items()))
def test_each_source_keeps_the_kind_it_had(name, kind):
    assert registry.BY_NAME[name].kind == kind


def test_the_four_kinds_cover_every_source_once():
    kinds = (registry.BOARD_SOURCES, registry.of_kind("feed"),
             registry.SEARCH_SOURCES, registry.MANUAL_SOURCES)
    assert sum(len(k) for k in kinds) == len(registry.NAMES)
    assert set(registry.COMPLETE_SOURCES) == set(registry.BOARD_SOURCES + registry.of_kind("feed"))


def test_every_copy_now_reads_the_registry():
    """The lists the app used to keep separately are the registry's, not equal to it."""
    assert ingest.REPOST_SOURCES is registry.BOARD_SOURCES
    assert discover.BOARD_SOURCES is registry.BOARD_SOURCES
    assert check.MANUAL_SOURCES is registry.MANUAL_SOURCES
    assert queries.FEED_SOURCES is registry.COMPLETE_SOURCES
    assert queries.SEARCH_SOURCES is registry.SEARCH_SOURCES
    assert queries.MANUAL_SOURCES is registry.MANUAL_SOURCES


def test_url_patterns_only_name_board_sources():
    """The link check resolves a job URL to a (source, token) board; every source it can
    name has to be a board in the registry, or its token could not be fetched."""
    for source, _host, _path in check._ATS_PATTERNS:
        assert source in registry.BOARD_SOURCES, source


# --- dispatch: what used to be the if-chain in poll.fetch_feed ---

def _spy(monkeypatch, module_name):
    calls = []
    monkeypatch.setattr(getattr(registry, module_name), "fetch",
                        lambda *a, **kw: calls.append((a, kw)) or ["posting"])
    return calls


@pytest.mark.parametrize("feed, module, expected", [
    ({"type": "greenhouse", "token": "acme", "company": "Acme"}, "greenhouse", (("acme", "Acme"), {})),
    ({"type": "lever", "token": "acme"}, "lever", (("acme", None), {})),
    ({"type": "ashby", "token": "acme"}, "ashby", (("acme", None), {})),
    ({"type": "join", "token": "acme"}, "join", (("acme", None, 10), {})),
    ({"type": "arbeitnow"}, "arbeitnow", ((), {"max_pages": 5})),
    ({"type": "startup_jobs", "search": "AI"}, "startup_jobs", (("AI", None, 3), {})),
    ({"type": "jsearch", "search": "AI"}, "jsearch", (("AI", "de", "week", 1), {})),
])
def test_fetch_calls_the_right_adapter(monkeypatch, feed, module, expected):
    calls = _spy(monkeypatch, module)
    assert registry.fetch(feed) == ["posting"]
    assert calls == [expected]
    # The poller is now a one-line wrapper over this, so it must agree.
    calls.clear()
    assert poll.fetch_feed(feed) == ["posting"]
    assert calls == [expected]


def test_arbeitsagentur_fetch_passes_the_title_filter(monkeypatch):
    """Its descriptions cost a request each, so the title filter runs during the fetch
    (HIR-56). Losing that would quietly multiply the requests per poll."""
    calls = _spy(monkeypatch, "arbeitsagentur")
    registry.fetch({"type": "arbeitsagentur", "search": "AI Engineer"})
    (args, kwargs), = calls
    assert args == ("AI Engineer", "Berlin", 25, 30, 2, 50)
    assert kwargs["title_filter"] is ingest.in_scope_title


def test_fetch_refuses_an_unknown_or_unfetchable_type():
    with pytest.raises(ValueError, match="unknown feed type"):
        registry.fetch({"type": "not_a_source"})
    for manual in registry.MANUAL_SOURCES:
        with pytest.raises(ValueError, match="unknown feed type"):
            registry.fetch({"type": manual})


def test_fetch_board_goes_through_the_registry(monkeypatch):
    calls = _spy(monkeypatch, "greenhouse")
    assert check.default_fetch_board("greenhouse", "acme") == ["posting"]
    assert calls == [(("acme", None), {})]


def test_fetch_board_refuses_a_source_that_is_not_a_board():
    for name in registry.SEARCH_SOURCES + registry.MANUAL_SOURCES + ("not_a_source",):
        with pytest.raises(KeyError):
            check.default_fetch_board(name, "acme")
