"""Stored jobs gain the tracked cities their location names (HIR-331)."""

import re

import pytest

from app import __main__ as cli
from app import backfill_places as bp
from app import db, discover, geo, queries
from app.sources import brave

NOW = "2026-11-19T00:00:00Z"
SQL = ("INSERT INTO job (company, title, city, location_raw, description_text, first_seen, last_seen)"
       " VALUES (?, 'AI Engineer', ?, ?, ?, ?, ?)")


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def add(conn, company, city, location, first="2026-11-10T00:00:00Z", last=NOW, text="jd"):
    job_id = conn.execute(SQL, (company, city, location, text, first, last)).lastrowid
    conn.commit()
    return job_id


def places(conn, job_id):
    return {r[0] for r in conn.execute("SELECT place FROM job_place WHERE job_id=?", (job_id,))}


def track(monkeypatch, city, *aliases):
    """`city` becomes a tracked city, as a launch PR makes it."""
    cities = {**geo.CITIES, city: aliases or (city.lower(),)}
    monkeypatch.setattr(geo, "CITIES", cities)
    monkeypatch.setattr(bp, "CITIES", cities)
    monkeypatch.setattr(geo, "_PATTERNS", {c: re.compile(r"\b(" + "|".join(map(re.escape, a)) + r")\b", re.I)
                                           for c, a in cities.items()})


def test_a_berlin_job_naming_paris_gains_paris_once_paris_is_tracked(conn, monkeypatch):
    job = add(conn, "Acme", "Berlin", "Berlin, Paris")
    assert bp.backfill(conn).gains == []                 # Paris not a city yet
    track(monkeypatch, "Paris")
    assert bp.backfill(conn).counts() == {"Paris": 1}
    assert places(conn, job) == {"Berlin", "Paris"}
    assert conn.execute("SELECT city FROM job WHERE id=?", (job,)).fetchone()[0] == "Berlin"


def test_a_second_run_adds_nothing(conn, monkeypatch):
    add(conn, "Acme", "Berlin", "Berlin, Paris")
    track(monkeypatch, "Paris")
    assert bp.backfill(conn).counts() == {"Paris": 1}
    assert bp.backfill(conn).gains == []


def test_dry_run_writes_nothing(conn, monkeypatch):
    job = add(conn, "Acme", "Berlin", "Berlin, Paris")
    track(monkeypatch, "Paris")
    b = bp.backfill(conn, apply=False)
    assert b.counts() == {"Paris": 1} and not b.applied
    assert places(conn, job) == {"Berlin"}
    assert "dry run, nothing written" in "\n".join(bp.report_lines(b))


def test_a_closed_job_is_backfilled_and_counts_only_when_it_was_open(conn, monkeypatch):
    closed = add(conn, "OldCo", "Berlin", "Berlin; Paris",
                 first="2026-06-01T00:00:00Z", last="2026-07-01T00:00:00Z",
                 text="a full posting " * queries.MIN_TEXT_CHARS)   # the chart skips fragments
    track(monkeypatch, "Paris")
    assert bp.backfill(conn).counts() == {"Paris": 1}
    assert places(conn, closed) == {"Berlin", "Paris"}
    paris = lambda window: queries.city_totals(       # noqa: E731
        conn, queries.make_filters(set(), cities=["Paris"], window=window), NOW).get("Paris", 0)
    # Closed in July: not open now, not in the last 90 days, but in all-time.
    assert (paris("open"), paris("90d"), paris("all")) == (0, 0, 1)
    total, _ = queries._open_during(conn, queries.make_filters(set(), cities=["Paris"], window="all"),
                                    "2026-06-10T00:00:00Z", "2026-06-20T00:00:00Z")
    assert total == 1                                    # counted in the weeks it was open


def test_city_limits_the_run_to_that_city(conn, monkeypatch):
    job = add(conn, "Acme", "Berlin", "Berlin, Paris, Munich")
    track(monkeypatch, "Paris")
    assert bp.backfill(conn, city="Paris").counts() == {"Paris": 1}
    assert places(conn, job) == {"Berlin", "Paris"}
    with pytest.raises(ValueError):
        bp.backfill(conn, city="Atlantis")


def test_remote_eu_is_never_added(conn):
    job = add(conn, "Acme", None, "Remote", text="We are a fully remote team across Europe.")
    assert geo.places_of("Remote", "AI Engineer", "We are a fully remote team across Europe.") == [geo.REMOTE_EU]
    assert bp.backfill(conn).gains == [] and places(conn, job) == set()


def test_posting_text_alone_never_adds_a_city(conn, monkeypatch):
    job = add(conn, "Acme", "Berlin", "Berlin", text="Work with our Paris office and clients in Paris.")
    track(monkeypatch, "Paris")
    assert bp.backfill(conn).gains == [] and places(conn, job) == {"Berlin"}


def test_a_job_gaining_more_than_three_cities_is_listed_for_a_look(conn):
    job = add(conn, "Everywhere", "Berlin", "Berlin, Munich, Hamburg, Frankfurt, New York")
    conn.execute("DELETE FROM job_place WHERE job_id=? AND place != 'Berlin'", (job,))
    conn.commit()
    b = bp.backfill(conn, apply=False)
    assert [g.job_id for g in b.many()] == [job]
    assert "for a look" in "\n".join(bp.report_lines(b))


def test_the_launch_runs_the_backfill_for_the_launched_city(conn, monkeypatch, capsys):
    job = add(conn, "Acme", "Berlin", "Berlin, Paris")
    track(monkeypatch, "Paris")
    monkeypatch.setattr(geo, "ACTIVE_CITIES", (*geo.ACTIVE_CITIES, "Paris"))
    monkeypatch.setattr(geo, "REGION_OF", {**geo.REGION_OF, "Paris": geo.EUROPE})   # HIR-369
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(brave, "api_key", lambda: "k")
    monkeypatch.setattr(discover, "run", lambda *a, **k: discover.Report())
    cli.main(["discover-boards", "--launch", "Paris"])
    assert places(conn, job) == {"Berlin", "Paris"}
    out = capsys.readouterr().out
    assert "Paris: 1" in out and "job " in out


def test_a_dry_run_launch_reports_the_gain_and_writes_nothing(conn, monkeypatch, capsys):
    job = add(conn, "Acme", "Berlin", "Berlin, Paris")
    track(monkeypatch, "Paris")
    monkeypatch.setattr(geo, "ACTIVE_CITIES", (*geo.ACTIVE_CITIES, "Paris"))
    monkeypatch.setattr(geo, "REGION_OF", {**geo.REGION_OF, "Paris": geo.EUROPE})   # HIR-369
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(brave, "api_key", lambda: "k")
    monkeypatch.setattr(discover, "run", lambda *a, **k: discover.Report())
    cli.main(["discover-boards", "--launch", "Paris", "--dry-run"])
    assert places(conn, job) == {"Berlin"}
    assert "would gain" in capsys.readouterr().out
