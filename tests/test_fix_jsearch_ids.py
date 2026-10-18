import importlib.util
from pathlib import Path

from app import db
from tests.test_sources import JSEARCH_IDS_SAME_POSTING

_spec = importlib.util.spec_from_file_location(
    "fix_jsearch_ids", Path(__file__).parent.parent / "scripts" / "fix_jsearch_ids.py")
fix_jsearch_ids = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fix_jsearch_ids)


def _setup(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    job = conn.execute("INSERT INTO job (description_text, first_seen, last_seen, repost_count) "
                       "VALUES ('jd', 't1', 't2', 3)").lastrowid
    sql = ("INSERT INTO job_source (job_id, source, source_job_id, first_seen, last_seen) "
           "VALUES (?, ?, ?, ?, ?)")
    a, b = JSEARCH_IDS_SAME_POSTING
    conn.execute(sql, (job, "jsearch", a, "2026-10-18T17:00", "2026-10-18T17:00"))
    conn.execute(sql, (job, "jsearch", b, "2026-10-18T17:30", "2026-10-18T17:30"))
    conn.execute(sql, (job, "arbeitnow", "slug", "2026-10-01", "2026-10-18"))
    conn.commit()
    return conn, job


def test_fix_collapses_duplicates_and_undoes_their_repost_counts(tmp_path):
    conn, job = _setup(tmp_path)
    assert fix_jsearch_ids.fix(conn) == {"jsearch_rows": 2, "kept": 1, "removed": 1, "renamed": 1}
    rows = [tuple(r) for r in conn.execute(
        "SELECT source, source_job_id, first_seen, last_seen FROM job_source ORDER BY source")]
    assert rows == [("arbeitnow", "slug", "2026-10-01", "2026-10-18"),
                    ("jsearch", "9quzt2CcAsrk_XVKAAAAAA==", "2026-10-18T17:00", "2026-10-18T17:30")]
    assert conn.execute("SELECT repost_count FROM job WHERE id=?", (job,)).fetchone()[0] == 2
    assert fix_jsearch_ids.fix(conn) == {"jsearch_rows": 1, "kept": 1, "removed": 0, "renamed": 0}


def test_fix_dry_run_writes_nothing(tmp_path):
    conn, job = _setup(tmp_path)
    assert fix_jsearch_ids.fix(conn, commit=False)["removed"] == 1
    assert conn.execute("SELECT COUNT(*) FROM job_source WHERE source='jsearch'").fetchone()[0] == 2
    assert conn.execute("SELECT repost_count FROM job WHERE id=?", (job,)).fetchone()[0] == 3
