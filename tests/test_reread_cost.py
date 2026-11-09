"""`reread-cost`: the price of the next full re-read, computed rather than quoted (HIR-221).

A small database with token counts we chose, so every euro figure here is arithmetic that
can be checked by hand. No model call anywhere — the command only reads the database.
"""

import json

import pytest

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
    # 3 open jobs never read; every reading cost 1M in + 1M out = $12 = €11.16.
    log_readings(conn, reread_cost.MIN_READINGS_TO_AVERAGE,
                 {"input_tokens": 1_000_000, "output_tokens": 1_000_000})
    cost = reread_cost.reread_cost(conn, model=MODEL)
    assert cost.jobs == 3
    assert cost.measured
    assert cost.readings == reread_cost.MIN_READINGS_TO_AVERAGE
    assert cost.eur_per_reading == pytest.approx(12.00 * 0.93)
    assert cost.eur_total == pytest.approx(3 * 12.00 * 0.93)


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
    assert "would re-read 3 jobs: about €33.48." in lines[0]
    assert any("Measured from the last 20 readings" in l for l in lines)


def test_one_job_is_not_called_jobs(conn):
    conn.execute("DELETE FROM job WHERE id IN (2, 3)")
    conn.commit()
    assert "re-read 1 job:" in reread_cost.report_lines(reread_cost.reread_cost(conn))[0]
