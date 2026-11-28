"""What each model run actually cost (HIR-449): recorded after the run, shown on the admin
page by day and kind and per model, flagged once in the morning note when one run passes
the alert, and added up on Monday."""

import json
import sqlite3

import pytest

from app import __main__ as cli
from app import admin, db, pipeline, run_cost
from app import caretaker_run as run
from app.extract import Extraction, Mention, extractor_version
from app.ingest import ingest_one
from app.reread_cost import Tokens, price_eur
from app.sources import Posting
from app.taxonomy import Taxonomy

TAX = Taxonomy({"version": 2, "skills": [{"id": "python", "display": "Python"}]})
MODEL = "claude-haiku-5-5"
USAGE = {"input_tokens": 1_000, "output_tokens": 500, "cache_read_input_tokens": 6_000,
         "cache_creation_input_tokens": 0}
ONE = Tokens(1_000, 500, 6_000, 0)


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    for i in range(3):
        ingest_one(conn=c, p=Posting("arbeitnow", f"a{i}", "", f"Co{i}", "AI Engineer", "Berlin", f"Python job {i}"))
    return c


def read_with_usage(text, tax, model):
    return Extraction(mentions=[Mention("python", "required", "Python")], usage=dict(USAGE),
                      extractor_version=extractor_version(tax, model), taxonomy_version=tax.version)


def add_run(conn, kind, started_at, cost, readings=10, model=MODEL):
    conn.execute("INSERT INTO model_run (kind, model, batch, started_at, attempted, readings, input_tokens,"
                 " output_tokens, cache_read_tokens, cache_write_tokens, cost_eur)"
                 " VALUES (?,?,1,?,?,?,0,0,0,0,?)", (kind, model, started_at, readings, readings, cost))
    conn.commit()


# --- recording ------------------------------------------------------------------------------

def test_a_run_records_the_providers_token_counts_and_what_they_cost(conn):
    report = pipeline.extract_pending(conn, TAX, read_with_usage, MODEL, log=lambda *_: None)
    run_id = run_cost.record(conn, run_cost.POLL, report, "2026-11-28T02:00:00Z", batch=False)
    row = conn.execute("SELECT * FROM model_run WHERE id = ?", (run_id,)).fetchone()
    assert (row["kind"], row["model"], row["batch"], row["attempted"], row["readings"]) == ("poll", MODEL, 0, 3, 3)
    assert (row["input_tokens"], row["output_tokens"], row["cache_read_tokens"], row["cache_write_tokens"]) == \
        (3_000, 1_500, 18_000, 0)
    assert row["cost_eur"] == pytest.approx(3 * price_eur(ONE, MODEL))


def test_a_batch_run_is_recorded_at_the_batch_half_rate(conn):
    report = pipeline.extract_pending(conn, TAX, read_with_usage, MODEL, log=lambda *_: None)
    report.cost_eur = 3 * price_eur(ONE, MODEL, batch=True)   # what the batch path itself sums
    run_id = run_cost.record(conn, run_cost.POLL, report, "2026-11-28T02:00:00Z", batch=True)
    row = conn.execute("SELECT batch, cost_eur FROM model_run WHERE id = ?", (run_id,)).fetchone()
    assert row["batch"] == 1 and row["cost_eur"] == pytest.approx(1.5 * price_eur(ONE, MODEL))


def test_a_run_that_read_nothing_or_was_skipped_writes_no_row(conn):
    assert run_cost.record(conn, run_cost.POLL, pipeline.ExtractReport(), "2026-11-28T02:00:00Z", True) is None
    assert run_cost.record(conn, run_cost.POLL, pipeline.ExtractReport(skipped_busy=True),
                           "2026-11-28T02:00:00Z", True) is None
    assert conn.execute("SELECT count(*) FROM model_run").fetchone()[0] == 0


def test_a_recorded_run_cannot_be_changed_or_deleted(conn):
    add_run(conn, "poll", "2026-11-28T02:00:00Z", 1.0)
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        conn.execute("UPDATE model_run SET cost_eur = 0")
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        conn.execute("DELETE FROM model_run")


def test_an_unknown_kind_of_run_is_refused(conn):
    with pytest.raises(sqlite3.IntegrityError):
        add_run(conn, "nightly", "2026-11-28T02:00:00Z", 1.0)


@pytest.mark.parametrize("argv, kind", [(["extract"], "re-read")])
def test_the_command_line_records_each_run_under_its_kind(conn, monkeypatch, argv, kind):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "extract_pending", lambda c, tax, **kw: pipeline.extract_pending(
        c, TAX, read_with_usage, MODEL, log=lambda *_: None, job_ids=kw.get("job_ids")))
    cli.main(argv)
    assert [tuple(r) for r in conn.execute("SELECT kind, readings FROM model_run")] == [(kind, 3)]


@pytest.mark.parametrize("cost_kind", ["poll", "launch", "bulk-read", "add"])
def test_every_kind_the_command_line_passes_is_one_the_table_takes(conn, monkeypatch, cost_kind):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(cli, "extract_pending", lambda c, tax, **kw: pipeline.extract_pending(
        c, TAX, read_with_usage, MODEL, log=lambda *_: None))
    cli.run_extraction(conn, cost_kind=cost_kind, batch=True)
    assert tuple(conn.execute("SELECT kind, batch FROM model_run").fetchone()) == (cost_kind, 1)


# --- adding up ------------------------------------------------------------------------------

def test_runs_add_up_by_day_and_kind_newest_day_first():
    rows = [run_cost.Run(1, "poll", MODEL, "2026-11-27T02:00:00Z", 100, 0.20),
            run_cost.Run(2, "add", MODEL, "2026-11-27T10:00:00Z", 1, 0.01),
            run_cost.Run(3, "poll", MODEL, "2026-11-28T02:00:00Z", 50, 0.10),
            run_cost.Run(4, "poll", MODEL, "2026-11-28T14:00:00Z", 50, 6.00)]
    days = run_cost.by_day_and_kind(rows)
    assert [(d.day, d.kind, d.runs, d.readings, round(d.cost_eur, 2), d.over) for d in days] == [
        ("2026-11-28", "poll", 2, 100, 6.10, True),
        ("2026-11-27", "poll", 1, 100, 0.20, False),
        ("2026-11-27", "add", 1, 1, 0.01, False)]
    assert days[1].per_posting == pytest.approx(0.002)


def test_cost_per_posting_by_model_shows_a_switch_as_two_rows(conn):
    def log(model, created_at, usage):
        conn.execute("INSERT INTO extraction_log (job_id, extractor_version, taxonomy_version, model,"
                     " created_at, raw_output, usage, input_sha256) VALUES (1,'v',1,?,?,'{}',?,'h')",
                     (model, created_at, json.dumps(usage)))
    log("claude-sonnet-5-5", "2026-11-20T02:00:00Z", USAGE)
    log("claude-sonnet-5-5", "2026-11-24T02:00:00Z", USAGE)
    log(MODEL, "2026-11-26T02:00:00Z", USAGE)
    log(MODEL, "2026-11-27T02:00:00Z", {})                       # no counts: not priced, not counted
    log("claude-sonnet-5-5", "2026-09-01T02:00:00Z", USAGE)      # before the window
    models = run_cost.per_model(conn, "2026-10-01")
    assert [(m.model, m.readings, m.first_day, m.last_day) for m in models] == [
        ("claude-sonnet-5-5", 2, "2026-11-20", "2026-11-24"), (MODEL, 1, "2026-11-26", "2026-11-26")]
    assert models[0].eur_per_reading == pytest.approx(price_eur(ONE, "claude-sonnet-5-5", batch=True))
    assert models[1].eur_per_reading < models[0].eur_per_reading


def write_eval(results, run_id, model, usages):
    d = results / run_id
    d.mkdir(parents=True)
    (d / "summary.json").write_text(json.dumps({"meta": {"run_id": run_id, "model": model}}))
    (d / "predictions.jsonl").write_text("".join(json.dumps({"golden_id": "g", "usage": u}) + "\n" for u in usages))


def test_an_eval_run_is_costed_from_its_own_result_files(tmp_path):
    write_eval(tmp_path, "20261125T091600Z_dev_x2-abc", MODEL, [USAGE, USAGE, {}])
    (tmp_path / "broken").mkdir()
    (tmp_path / "broken" / "summary.json").write_text("not json")
    [e] = run_cost.eval_runs(tmp_path)
    assert (e.kind, e.label, e.model, e.readings, e.started_at) == \
        ("eval", "20261125T091600Z_dev_x2-abc", MODEL, 2, "2026-11-25T09:16:00Z")
    assert e.cost_eur == pytest.approx(2 * price_eur(ONE, MODEL))


def test_the_monday_line_gives_the_total_the_split_and_the_collections_cost_per_posting():
    rows = [run_cost.Run(1, "poll", MODEL, "2026-11-17T02:00:00Z", 400, 0.40),
            run_cost.Run(2, "re-read", MODEL, "2026-11-18T02:00:00Z", 800, 0.80),
            run_cost.Run(None, "eval", MODEL, "2026-11-19T09:00:00Z", 213, 0.30, label="r")]
    text = run_cost.week_text(rows, "2026-11-16", "2026-11-22")
    assert text.startswith("Model spend 2026-11-16 to 2026-11-22: €1.50 (")
    assert "daily collection €0.40, re-read €0.80, eval €0.30" in text
    assert "€0.0010 a posting read" in text and "alert" not in text
    over = run_cost.week_text(rows + [run_cost.Run(3, "launch", MODEL, "2026-11-20T02:00:00Z", 9000, 7.0)],
                              "2026-11-16", "2026-11-22")
    assert "1 run cost more than the €5 alert." in over
    assert run_cost.week_text([], "2026-11-16", "2026-11-22") == \
        "Model spend 2026-11-16 to 2026-11-22: €0.00 (no model runs recorded).\n"


# --- the alert ------------------------------------------------------------------------------

def test_a_run_over_the_alert_is_in_the_morning_note_once(conn, monkeypatch):
    monkeypatch.setattr(run, "pending_count", lambda c: 0)
    add_run(conn, "re-read", "2026-11-27T23:50:00Z", 6.25, readings=3000)   # last night, before midnight
    add_run(conn, "poll", "2026-11-28T02:00:00Z", 0.40)                    # under the alert
    add_run(conn, "launch", "2026-11-20T02:00:00Z", 9.0)                   # a week ago: not this morning's news
    found = run.cost_findings(conn, "2026-11-28")
    assert [f.finding for f in found] == ["run_over_cost"]
    assert found[0].detail == ("The re-read run of 2026-11-27 23:50 UTC cost €6.25, above the €5 alert "
                               "for one run (3,000 postings read, claude-haiku-5-5).")
    run.write_log(conn, found, "2026-11-28")
    assert found[0].detail in run.urgent_now(conn, "2026-11-28")
    assert run.cost_findings(conn, "2026-11-29") == []                     # reported once, not again


def test_the_alert_is_one_setting():
    assert run_cost.RUN_ALERT_EUR == 5.0
    assert run_cost.over_alert([run_cost.Run(1, "poll", MODEL, "2026-11-28T02:00:00Z", 1, 5.0)]) == []


def test_the_monday_summary_carries_the_weeks_model_spend(conn, monkeypatch, tmp_path):
    monkeypatch.setattr(run, "EVAL_RESULTS", tmp_path)
    add_run(conn, "poll", "2026-11-12T02:00:00Z", 0.75)
    posted = []
    run.report(conn, "2026-11-16", lambda t, b: posted.append(b) or "HIR-900", log=lambda *_: None)
    assert any("Model spend 2026-11-09 to 2026-11-15: €0.75 (daily collection €0.75)" in b for b in posted)


# --- the admin page -------------------------------------------------------------------------

def test_the_admin_page_shows_cost_by_day_and_kind_per_model_and_evals(conn, tmp_path):
    add_run(conn, "poll", "2026-11-28T02:00:00Z", 0.50, readings=500)
    add_run(conn, "re-read", "2026-11-27T02:00:00Z", 6.00, readings=900)
    write_eval(tmp_path, "20261125T091600Z_dev_x2-abc", MODEL, [USAGE])
    costs = admin.costs(conn, "2026-11-28T09:00:00Z", tmp_path)
    assert [(d.day, d.kind) for d in costs.days] == [
        ("2026-11-28", "poll"), ("2026-11-27", "re-read"), ("2026-11-25", "eval")]
    out = admin.page([], [], "2026-11-28T09:00:00Z", costs)
    assert "<h2>Model cost</h2>" in out and "daily collection" in out and "€0.0010" in out
    assert "<tr class=incubating><td>2026-11-27</td><td>re-read</td>" in out   # the run over the alert stands out
    assert "20261125T091600Z_dev_x2-abc" in out
    assert "<h2>Model cost</h2>" not in admin.page([], [], "2026-11-28T09:00:00Z")
