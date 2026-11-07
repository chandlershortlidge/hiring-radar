import sqlite3

import pytest

from app import db


def test_migrate_creates_core_tables_and_is_idempotent(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    applied = db.migrate(conn)
    assert applied[0] == 1 and applied == sorted(applied)
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


def test_every_feed_adapter_source_is_allowed_by_the_schema(tmp_path):
    # Regression: arbeitsagentur/jsearch postings hit the job_source CHECK at ingest.
    from app.sources import arbeitnow, arbeitsagentur, ashby, greenhouse, join, jsearch, lever, startup_jobs
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    job_id = _job(conn)
    for i, mod in enumerate((arbeitnow, arbeitsagentur, ashby, greenhouse, join, jsearch, lever, startup_jobs)):
        conn.execute("INSERT INTO job_source (job_id, source, source_job_id, first_seen, last_seen) "
                     "VALUES (?, ?, ?, 'now', 'now')", (job_id, mod.SOURCE, f"id{i}"))


def test_migration_007_keeps_existing_job_source_rows(tmp_path):
    import shutil
    old = tmp_path / "old"
    old.mkdir()
    for p in sorted(db.MIGRATIONS_DIR.glob("*.sql")):
        if int(p.name[:3]) < 7:
            shutil.copy(p, old / p.name)
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn, old)
    job_id = _job(conn)
    conn.execute("INSERT INTO job_source (job_id, source, source_job_id, url, first_seen, last_seen, posted_at) "
                 "VALUES (?, 'arbeitnow', 'a1', 'u', 'f', 'l', 'p')", (job_id,))
    conn.commit()
    db.migrate(conn)
    rows = [tuple(r) for r in conn.execute(
        "SELECT job_id, source, source_job_id, url, first_seen, last_seen, posted_at FROM job_source")]
    assert rows == [(job_id, "arbeitnow", "a1", "u", "f", "l", "p")]
    conn.execute("DELETE FROM job WHERE id=?", (job_id,))   # cascade still wired
    assert conn.execute("SELECT COUNT(*) FROM job_source").fetchone()[0] == 0


def test_migration_017_backfills_a_family_on_every_existing_job(tmp_path):
    """A database with rows from before 017 comes out of the migration with no null family,
    and the column refuses a family outside the five (HIR-186)."""
    import shutil
    old = tmp_path / "old"
    old.mkdir()
    for p in sorted(db.MIGRATIONS_DIR.glob("*.sql")):
        if int(p.name[:3]) < 17:
            shutil.copy(p, old / p.name)
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn, old)
    for title in ("Senior Data Scientist", "MLOps Engineer", "AI Engineer", None):
        conn.execute("INSERT INTO job (title, description_text, first_seen, last_seen)"
                     " VALUES (?, 'jd', '2026-10-16T00:00:00Z', '2026-10-16T00:00:00Z')", (title,))
    conn.commit()
    assert 17 in db.migrate(conn)
    assert conn.execute("SELECT COUNT(*) FROM job WHERE family IS NULL").fetchone()[0] == 0
    assert [r[0] for r in conn.execute("SELECT family FROM job ORDER BY id")] == [
        "data-scientist", "ml-platform", "ai-engineer", "ai-engineer"]
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE job SET family='nonsense' WHERE id=1")


# --- 018: the two append-only tables refuse to lose a row (HIR-209) -------------------

def _log_row(conn, job_id=None):
    conn.execute(
        "INSERT INTO extraction_log (job_id, extractor_version, taxonomy_version, model,"
        " raw_output, usage, input_sha256) VALUES (?, 'v1', 2, 'model-x', '{}', '{}', 'abc')",
        (job_id,))
    return conn.execute("SELECT id FROM extraction_log ORDER BY id DESC").fetchone()[0]


def _label_row(conn):
    conn.execute("INSERT INTO label_answer (run, golden_id, labeler) VALUES ('r1', 'g1', 'A')")
    return conn.execute("SELECT id FROM label_answer ORDER BY id DESC").fetchone()[0]


def test_a_stored_reading_cannot_be_changed_or_deleted(tmp_path):
    """016 says extraction_log is append-only; 018 makes the database say so too."""
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    job_id = _job(conn)
    rid = _log_row(conn, job_id)
    for sql, args in [("UPDATE extraction_log SET raw_output='{\"x\":1}' WHERE id=?", (rid,)),
                      ("UPDATE extraction_log SET model='other' WHERE id=?", (rid,)),
                      ("UPDATE extraction_log SET job_id=NULL, model='other' WHERE id=?", (rid,)),
                      ("UPDATE extraction_log SET created_at='2020-01-01T00:00:00Z' WHERE id=?", (rid,)),
                      ("DELETE FROM extraction_log WHERE id=?", (rid,))]:
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            conn.execute(sql, args)
    assert conn.execute("SELECT COUNT(*) FROM extraction_log").fetchone()[0] == 1


def test_a_reading_may_still_be_moved_or_unlinked_but_not_rewritten(tmp_path):
    """The guard freezes the reading, not which posting it hangs off: dropping a posting
    unlinks its readings (016) and folding a duplicate moves them (HIR-208)."""
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    job_id = _job(conn)
    rid = _log_row(conn, job_id)
    conn.execute("DELETE FROM job WHERE id=?", (job_id,))
    assert [tuple(r) for r in conn.execute("SELECT id, job_id, model FROM extraction_log")] == [
        (rid, None, "model-x")]
    # Both link changes are allowed when written by hand too, so the guard does not depend
    # on recursive_triggers being off.
    keep, drop = _job(conn), _job(conn)
    rid2 = _log_row(conn, drop)
    conn.execute("UPDATE extraction_log SET job_id=? WHERE job_id=?", (keep, drop))
    conn.execute("UPDATE extraction_log SET job_id=NULL WHERE id=?", (rid2,))
    # ...but not when anything about the reading itself changes with it.
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        conn.execute("UPDATE extraction_log SET job_id=?, input_sha256='other' WHERE id=?", (keep, rid2))


def test_a_stored_label_cannot_be_changed_or_deleted(tmp_path):
    """label_answer has no job link, so every UPDATE and DELETE is refused (HIR-209)."""
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    lid = _label_row(conn)
    for sql in ("UPDATE label_answer SET answer='{}' WHERE id=?", "DELETE FROM label_answer WHERE id=?"):
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            conn.execute(sql, (lid,))
    assert conn.execute("SELECT COUNT(*) FROM label_answer").fetchone()[0] == 1


def test_appending_to_the_two_tables_is_untouched(tmp_path):
    """The guard refuses changes, not new rows: the import that loads a labelling run and
    the pipeline that logs a reading both still work."""
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    job_id = _job(conn)
    _log_row(conn, job_id)
    _log_row(conn, job_id)
    _label_row(conn)
    conn.execute("INSERT OR IGNORE INTO label_answer (run, golden_id, labeler) VALUES ('r1', 'g1', 'A')")
    assert conn.execute("SELECT COUNT(*) FROM extraction_log").fetchone()[0] == 2
    assert conn.execute("SELECT COUNT(*) FROM label_answer").fetchone()[0] == 1
