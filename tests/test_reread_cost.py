"""`reread-cost`: the price of the next full re-read, computed rather than quoted (HIR-221).

A small database with token counts we chose, so every euro figure here is arithmetic that
can be checked by hand. No model call anywhere — the command only reads the database.
"""

import json
import shutil
import sqlite3

import pytest

import app.__main__ as cli
from app import db, pipeline, reread_cost
from app.ingest import ingest_one
from app.sources import Posting

MODEL = "claude-sonnet-5-5"


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    for i in range(3):
        ingest_one(conn=c, p=Posting("arbeitnow", f"a{i}", "", f"Co{i}", "AI Engineer",
                                     "Berlin", f"Python and RAG job {i}"))
    return c


def log_readings(conn, n, usage):
    """n logged readings all carrying the same token counts."""
    for _ in range(n):
        conn.execute(
            "INSERT INTO extraction_log (job_id, extractor_version, taxonomy_version, model,"
            " raw_output, usage, input_sha256) VALUES (1, 'x2-old', 2, ?, '{}', ?, 'sha')",
            (MODEL, json.dumps(usage)))
    conn.commit()


def close_job(conn, job_id):
    """Make a job closed under the dashboard's open rule: no sighting for years."""
    conn.execute("UPDATE job SET last_seen='2020-01-01T00:00:00Z' WHERE id=?", (job_id,))
    conn.execute("UPDATE job_source SET last_seen='2020-01-01T00:00:00Z' WHERE job_id=?", (job_id,))
    conn.commit()


# --- the price of one reading ---------------------------------------------------------

def test_a_reading_is_priced_per_kind_of_token():
    """1M of each kind on Sonnet: $2 in + $10 out + $0.20 cached + $2.50 written = $14.70."""
    tokens = reread_cost.Tokens(input=1e6, output=1e6, cache_read=1e6, cache_write=1e6)
    assert reread_cost.price_eur(tokens, MODEL) == pytest.approx(14.70 * 0.93)


def test_a_cached_read_costs_a_tenth_of_a_fresh_one():
    fresh = reread_cost.price_eur(reread_cost.Tokens(input=1e6), MODEL)
    cached = reread_cost.price_eur(reread_cost.Tokens(cache_read=1e6), MODEL)
    assert cached == pytest.approx(fresh / 10)


def test_the_same_reading_costs_more_on_a_bigger_model():
    """The tokens are measured, the price is the model's: a switch reprices the same shape."""
    tokens = reread_cost.Tokens(input=1e6, output=1e6)
    assert (reread_cost.price_eur(tokens, "claude-opus-5-5")
            == pytest.approx(2 * reread_cost.price_eur(tokens, MODEL)))


def test_an_unpriced_model_falls_back_to_the_default_rather_than_raising():
    tokens = reread_cost.Tokens(input=1e6)
    assert (reread_cost.price_eur(tokens, "some-model-we-have-never-heard-of")
            == pytest.approx(reread_cost.price_eur(tokens, reread_cost.DEFAULT_MODEL)))


def test_batch_pricing_halves_every_rate():
    """The Message Batches API's discount applies to input, output and cached tokens
    alike, and stacks with the cache discount already in the standard rate (HIR-222)."""
    tokens = reread_cost.Tokens(input=1e6, output=1e6, cache_read=1e6, cache_write=1e6)
    standard = reread_cost.price_eur(tokens, MODEL)
    batch = reread_cost.price_eur(tokens, MODEL, batch=True)
    assert batch == pytest.approx(standard / 2)


# --- averaging the readings we paid for -----------------------------------------------

def test_the_average_is_of_the_token_counts_the_provider_reported():
    usages = [{"input_tokens": 100, "output_tokens": 10},
              {"input_tokens": 300, "output_tokens": 30}]
    assert reread_cost.mean_tokens(usages) == reread_cost.Tokens(input=200, output=20)


def test_a_missing_cache_field_reads_as_zero_not_as_a_gap():
    """The provider sends no cache fields at all when caching is off; that is a real zero."""
    assert reread_cost.mean_tokens([{"input_tokens": 100}]).cache_read == 0


def test_readings_the_provider_sent_no_counts_for_are_left_out(conn):
    """Averaging '{}' rows in would drag the figure towards zero and understate the merge."""
    log_readings(conn, 20, {"input_tokens": 1000, "output_tokens": 100})
    log_readings(conn, 50, {})
    usages = reread_cost.logged_usages(conn)
    assert len(usages) == 20
    assert reread_cost.mean_tokens(usages) == reread_cost.Tokens(input=1000, output=100)


def test_only_the_most_recent_readings_are_averaged(conn):
    """A reading's token count tracks the size of a prompt that grows, so old ones mislead."""
    log_readings(conn, 10, {"input_tokens": 1, "output_tokens": 1})
    log_readings(conn, reread_cost.READINGS_SAMPLED, {"input_tokens": 9000, "output_tokens": 900})
    assert reread_cost.mean_tokens(reread_cost.logged_usages(conn)) == reread_cost.Tokens(
        input=9000, output=900)


# --- the whole figure -----------------------------------------------------------------

def test_the_cost_is_the_queue_times_the_average_reading(conn):
    # 3 open jobs never read; every reading cost 1M in + 1M out = $12 at the standard rate,
    # halved to $6 = €5.58 since a re-read always runs as a batch now (HIR-222).
    log_readings(conn, reread_cost.MIN_READINGS_TO_AVERAGE,
                 {"input_tokens": 1_000_000, "output_tokens": 1_000_000})
    cost = reread_cost.reread_cost(conn, model=MODEL)
    assert cost.jobs == 3
    assert cost.measured
    assert cost.readings == reread_cost.MIN_READINGS_TO_AVERAGE
    assert cost.eur_per_reading == pytest.approx(6.00 * 0.93)
    assert cost.eur_total == pytest.approx(3 * 6.00 * 0.93)


def test_reread_cost_prices_at_the_batch_rate_not_the_standard_one(conn):
    """A re-read always submits as a batch (HIR-222), so the figure quoted for a merge
    must be half the standard rate, not the full price `price_eur` gives by default."""
    log_readings(conn, reread_cost.MIN_READINGS_TO_AVERAGE,
                 {"input_tokens": 1_000_000, "output_tokens": 1_000_000})
    cost = reread_cost.reread_cost(conn, model=MODEL)
    standard = reread_cost.price_eur(cost.tokens, MODEL)
    assert cost.eur_per_reading == pytest.approx(standard * reread_cost.BATCH_DISCOUNT)


def test_too_few_readings_is_reported_as_an_estimate_not_smoothed_over(conn):
    log_readings(conn, reread_cost.MIN_READINGS_TO_AVERAGE - 1,
                 {"input_tokens": 1_000_000, "output_tokens": 1_000_000})
    cost = reread_cost.reread_cost(conn, model=MODEL)
    assert not cost.measured
    assert cost.readings == 0
    assert cost.found == reread_cost.MIN_READINGS_TO_AVERAGE - 1
    # The fallback is the hand-made token estimate, not the readings that were too few.
    assert cost.tokens == reread_cost.Tokens(input=reread_cost.ESTIMATE_INPUT_TOKENS,
                                             output=reread_cost.ESTIMATE_OUTPUT_TOKENS)
    assert "ESTIMATE, not measured" in "\n".join(reread_cost.report_lines(cost))


def test_an_empty_database_says_nothing_would_be_read(tmp_path):
    c = db.connect(tmp_path / "empty.db")
    db.migrate(c)
    cost = reread_cost.reread_cost(c)
    assert (cost.jobs, cost.eur_total) == (0, 0)


# --- the count is the queue's own, so it cannot drift ---------------------------------

def test_closed_jobs_are_not_counted_because_they_are_not_re_read(conn):
    """HIR-195: a bump re-reads only open jobs, so only those may be charged for."""
    conn.execute("UPDATE job SET extracted_version='x2-old'")
    close_job(conn, 1)
    assert pipeline.reread_queue_size(conn) == 2


def test_a_closed_job_never_read_is_counted_because_a_first_read_is_not_a_re_read(conn):
    close_job(conn, 1)
    assert pipeline.reread_queue_size(conn) == 3


def test_legacy_imports_are_never_counted(conn):
    """They hold an old summary rather than the posting, so they are never re-read."""
    conn.execute("UPDATE job SET extracted_version='legacy' WHERE id=1")
    assert pipeline.reread_queue_size(conn) == 2


@pytest.mark.parametrize("prepare", [
    lambda c: None,                                                  # all never read
    lambda c: c.execute("UPDATE job SET extracted_version='x2-old'"),
    lambda c: c.execute("UPDATE job SET extracted_version='legacy' WHERE id=2"),
])
def test_the_count_always_matches_the_queue_that_actually_runs(conn, prepare):
    """The drift guard: the figure Chandler reads counts the jobs the poll would read.

    Both sides are built from one WHERE clause, and this pins them together so a later
    change to the queue's rule cannot leave the cost quietly measuring the old one."""
    prepare(conn)
    conn.commit()
    close_job(conn, 1)
    queued = pipeline.jobs_needing_extraction(conn, "a-version-no-job-carries")
    assert pipeline.reread_queue_size(conn) == len(queued)


# --- what the command prints ----------------------------------------------------------

def test_the_report_leads_with_the_figure_for_the_pull_request(conn):
    log_readings(conn, reread_cost.MIN_READINGS_TO_AVERAGE,
                 {"input_tokens": 1_000_000, "output_tokens": 1_000_000})
    lines = reread_cost.report_lines(reread_cost.reread_cost(conn, model=MODEL))
    assert "would re-read 3 jobs: about €16.74." in lines[0]   # half of €33.48, HIR-222
    assert any("Measured from the last 20 readings" in l for l in lines)


def test_one_job_is_not_called_jobs(conn):
    conn.execute("DELETE FROM job WHERE id IN (2, 3)")
    conn.commit()
    assert "re-read 1 job:" in reread_cost.report_lines(reread_cost.reread_cost(conn))[0]


# --- the command only reads: it never migrates the database it is pointed at (HIR-265) --

def schema_state(path):
    """Everything a migration could change: the applied-migrations list and the schema."""
    c = sqlite3.connect(path)
    try:
        return (c.execute("SELECT version FROM schema_migrations ORDER BY version").fetchall(),
                c.execute("SELECT type, name, sql FROM sqlite_master ORDER BY type, name").fetchall())
    finally:
        c.close()


def database_behind(tmp_path, keep):
    """A database built from only the migrations `keep` accepts, as a checkout that did
    not have the others yet would have left it."""
    older = tmp_path / "migrations"
    older.mkdir()
    for f in sorted(db.MIGRATIONS_DIR.glob("*.sql")):
        if keep(int(f.name[:3])):
            shutil.copy(f, older / f.name)
    path = tmp_path / "behind.db"
    c = db.connect(path)
    db.migrate(c, older)
    c.close()
    return path


def newest_migration():
    return max(int(f.name[:3]) for f in db.MIGRATIONS_DIR.glob("*.sql"))


def test_the_command_leaves_a_database_one_migration_behind_exactly_as_it_was(
        tmp_path, monkeypatch, capsys):
    newest = newest_migration()
    path = database_behind(tmp_path, lambda v: v != newest)
    before = schema_state(path)
    assert (newest,) not in before[0]
    monkeypatch.setattr(cli, "DB_PATH", path)
    cli.main(["reread-cost"])
    out = capsys.readouterr().out
    assert "would re-read 0 jobs: about €0.00." in out
    assert "applied migrations" not in out
    assert schema_state(path) == before


def test_the_commands_figure_on_an_up_to_date_database_is_the_one_it_always_gave(
        tmp_path, conn, monkeypatch, capsys):
    log_readings(conn, reread_cost.MIN_READINGS_TO_AVERAGE,
                 {"input_tokens": 1_000_000, "output_tokens": 1_000_000})
    expected = reread_cost.report_lines(reread_cost.reread_cost(conn, tax=cli.Taxonomy.load()))
    assert "would re-read 3 jobs: about €16.74." in expected[0]
    conn.close()
    before = schema_state(tmp_path / "t.db")
    monkeypatch.setattr(cli, "DB_PATH", tmp_path / "t.db")
    cli.main(["reread-cost"])
    assert capsys.readouterr().out.splitlines() == expected
    assert schema_state(tmp_path / "t.db") == before


def test_a_database_too_old_for_the_estimate_is_reported_and_left_alone(tmp_path, monkeypatch):
    """Before migration 16 there is no log of paid readings to average."""
    path = database_behind(tmp_path, lambda v: v < 16)
    before = schema_state(path)
    monkeypatch.setattr(cli, "DB_PATH", path)
    with pytest.raises(SystemExit) as stop:
        cli.main(["reread-cost"])
    assert "older than this code" in str(stop.value)
    assert "Nothing was changed" in str(stop.value)
    assert schema_state(path) == before


def test_the_command_does_not_create_a_database_that_is_not_there(tmp_path, monkeypatch):
    path = tmp_path / "nowhere" / "missing.db"
    monkeypatch.setattr(cli, "DB_PATH", path)
    with pytest.raises(SystemExit) as stop:
        cli.main(["reread-cost"])
    assert "no database at" in str(stop.value)
    assert not path.parent.exists()


def test_a_read_only_connection_refuses_every_write(tmp_path, conn):
    conn.close()
    ro = db.connect_readonly(tmp_path / "t.db")
    assert ro.execute("SELECT count(*) FROM job").fetchone()[0] == 3
    with pytest.raises(sqlite3.OperationalError, match="readonly"):
        ro.execute("DELETE FROM job")
    with pytest.raises(sqlite3.OperationalError):
        db.connect_readonly(tmp_path / "missing.db")
