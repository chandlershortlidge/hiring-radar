import sqlite3

import pytest

from app import db


def test_migrate_creates_core_tables_and_is_idempotent(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    assert db.migrate(conn) == [1]
    assert db.migrate(conn) == []
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"job", "job_source", "screenshot", "skill_mention", "proposed_skill"} <= tables


def _job(conn):
    cur = conn.execute(
        "INSERT INTO job (description_text, first_seen, last_seen) VALUES ('jd', '2026-10-16T00:00:00Z', '2026-10-16T00:00:00Z')"
    )
    return cur.lastrowid


def test_same_source_id_cannot_be_inserted_twice(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    jid = _job(conn)
    row = (jid, "greenhouse", "123", "2026-10-16", "2026-10-16")
    sql = "INSERT INTO job_source (job_id, source, source_job_id, first_seen, last_seen) VALUES (?,?,?,?,?)"
    conn.execute(sql, row)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(sql, row)


def test_manual_sources_may_share_null_source_id(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    jid = _job(conn)
    sql = "INSERT INTO job_source (job_id, source, first_seen, last_seen) VALUES (?, 'paste', 'x', 'x')"
    conn.execute(sql, (jid,))
    conn.execute(sql, (jid,))  # NULL source_job_id is distinct in SQLite UNIQUE


def test_unknown_source_and_requirement_are_rejected(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    jid = _job(conn)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO job_source (job_id, source, first_seen, last_seen) VALUES (?, 'linkedin', 'x', 'x')", (jid,))
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text, taxonomy_version, extractor_version)"
            " VALUES (?, 'llms', 'mandatory', 'x', 1, 'v0')", (jid,))


def test_deleting_a_job_cascades(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    jid = _job(conn)
    conn.execute("INSERT INTO job_source (job_id, source, first_seen, last_seen) VALUES (?, 'paste', 'x', 'x')", (jid,))
    conn.execute("DELETE FROM job WHERE id = ?", (jid,))
    assert conn.execute("SELECT COUNT(*) FROM job_source").fetchone()[0] == 0


def test_bad_migration_filename_is_rejected(tmp_path):
    (tmp_path / "1_oops.sql").write_text("SELECT 1;")
    with pytest.raises(ValueError):
        db.pending_migrations(set(), tmp_path)


def test_failed_migration_records_nothing(tmp_path):
    mdir = tmp_path / "m"
    mdir.mkdir()
    (mdir / "001_ok.sql").write_text("CREATE TABLE a (x INTEGER);")
    (mdir / "002_bad.sql").write_text("CREATE TABLE b (x INTEGER); THIS IS NOT SQL;")
    conn = db.connect(tmp_path / "t.db")
    with pytest.raises(sqlite3.Error):
        db.migrate(conn, mdir)
    applied = {r[0] for r in conn.execute("SELECT version FROM schema_migrations")}
    assert applied == {1}
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert "b" not in tables
