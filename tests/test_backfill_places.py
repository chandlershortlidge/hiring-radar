import importlib.util
from pathlib import Path

from app import db

_spec = importlib.util.spec_from_file_location(
    "backfill_places", Path(__file__).parent.parent / "scripts" / "backfill_places.py")
backfill_places = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(backfill_places)


def _setup(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    sql = ("INSERT INTO job (company, title, city, location_raw, description_text, first_seen, last_seen)"
           " VALUES (?, 'AI Engineer', ?, ?, 'jd', '2026-11-01T00:00:00Z', '2026-11-01T00:00:00Z')")
    # Stored before migration 022 with its first city only (a perplexity posting, HIR-289).
    two = conn.execute(sql, ("Perplexity", "San Francisco", "San Francisco; New York City")).lastrowid
    one = conn.execute(sql, ("Acme", "Berlin", "Berlin")).lastrowid
    conn.commit()
    return conn, two, one


def places(conn, job_id):
    return {r[0] for r in conn.execute("SELECT place FROM job_place WHERE job_id=?", (job_id,))}


def test_backfill_adds_the_other_cities_and_nothing_else(tmp_path):
    conn, two, one = _setup(tmp_path)
    assert backfill_places.backfill(conn) == {"New York": 1}
    assert places(conn, two) == {"San Francisco", "New York"} and places(conn, one) == {"Berlin"}
    assert conn.execute("SELECT city FROM job WHERE id=?", (two,)).fetchone()[0] == "San Francisco"
    assert backfill_places.backfill(conn) == {}          # a second run adds nothing


def test_dry_run_writes_nothing(tmp_path):
    conn, two, _ = _setup(tmp_path)
    assert backfill_places.backfill(conn, commit=False) == {"New York": 1}
    assert places(conn, two) == {"San Francisco"}
