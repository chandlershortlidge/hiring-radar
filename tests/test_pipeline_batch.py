"""The poll and a re-read submit their readings as one Anthropic Message Batch instead of
one call per job (HIR-222). `batch_fn` stands in for the Batch API the same way `extract_fn`
stands in for a direct call — no live call anywhere here.
"""

from types import SimpleNamespace

import pytest

from app import db, langsmith_live, pipeline
from app.extract import extractor_version
from app.ingest import ingest_one
from app.reread_cost import price_eur
from app.sources import Posting
from app.taxonomy import Taxonomy

TAX = Taxonomy({"version": 2, "skills": [{"id": "python", "display": "Python"}, {"id": "rag", "display": "RAG"}]})
USAGE = dict(input_tokens=100, output_tokens=20, cache_read_input_tokens=80, cache_creation_input_tokens=0)


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    for i in range(3):
        ingest_one(conn=c, p=Posting("arbeitnow", f"a{i}", "", f"Co{i}", "AI Engineer", "Berlin", f"Python and RAG job {i}"))
    return c


def succeeded(items, usage=None):
    """A batch item whose result is a successful read — the same message shape a direct
    `client.messages.create` call returns (confirmed against the real Batches API)."""
    block = SimpleNamespace(type="tool_use", name="record_skills", input={"skills": items})
    message = SimpleNamespace(stop_reason="tool_use", content=[block], usage=SimpleNamespace(**(usage or USAGE)))
    return SimpleNamespace(type="succeeded", message=message)


def errored(msg="boom"):
    return SimpleNamespace(type="errored", error=SimpleNamespace(message=msg))


def expired():
    return SimpleNamespace(type="expired")


def item(skill_id, raw_text, requirement="required"):
    return {"skill_id": skill_id, "requirement": requirement, "raw_text": raw_text}


def batch_fn_returning(results: dict):
    """A fake Batch API: ignores the submitted requests and hands back canned results,
    keyed by custom_id (== str(job_id)), exactly like `default_batch_fn` would once the
    real batch had finished."""
    def fn(requests):
        return dict(results)
    return fn


def test_batch_results_are_stored_like_direct_ones(conn):
    results = {str(i): succeeded([item("python", "Python")]) for i in (1, 2, 3)}
    r = pipeline.extract_pending(conn, TAX, model="m", log=lambda *_: None,
                                 batch=True, batch_fn=batch_fn_returning(results))
    assert (r.attempted, r.succeeded, r.mentions) == (3, 3, 3)
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 3
    assert conn.execute("SELECT count(*) FROM job WHERE extracted_version IS NULL").fetchone()[0] == 0
    # The extraction_log row carries the real token usage the batch returned, same as a
    # direct call would log (HIR-170) — unaffected by the batch's half price.
    logged = conn.execute("SELECT usage FROM extraction_log LIMIT 1").fetchone()[0]
    assert '"input_tokens": 100' in logged
    # Second run: nothing left to batch.
    assert pipeline.extract_pending(conn, TAX, model="m", log=lambda *_: None, batch=True,
                                    batch_fn=batch_fn_returning({})).attempted == 0


def test_a_partly_failed_batch_leaves_the_failed_jobs_unread(conn):
    results = {"1": succeeded([item("python", "Python")]), "2": errored(), "3": expired()}
    r = pipeline.extract_pending(conn, TAX, model="m", log=lambda *_: None,
                                 batch=True, batch_fn=batch_fn_returning(results))
    assert r.succeeded == 1 and sorted(j for j, _ in r.failed) == [2, 3]
    rows = {row["id"]: row["extracted_version"] for row in conn.execute("SELECT id, extracted_version FROM job")}
    assert rows[1] is not None
    assert rows[2] is None and rows[3] is None   # left pending, same as a failed direct call


def test_a_missing_batch_result_is_a_failure_not_a_crash(conn):
    """A custom_id the Batch API never returned (should not happen, but the queue must not
    stay silently unresolved if it does)."""
    results = {"1": succeeded([item("python", "Python")])}   # jobs 2 and 3 get nothing back
    r = pipeline.extract_pending(conn, TAX, model="m", log=lambda *_: None,
                                 batch=True, batch_fn=batch_fn_returning(results))
    assert sorted(j for j, _ in r.failed) == [2, 3]


def test_a_batch_run_with_nothing_pending_never_calls_the_batch_api(conn):
    conn.execute("DELETE FROM job")
    conn.commit()

    def boom(requests):
        raise AssertionError("submitted a batch with nothing pending")

    assert pipeline.extract_pending(conn, TAX, model="m", log=lambda *_: None,
                                    batch=True, batch_fn=boom).attempted == 0


def test_add_never_uses_the_batch_api(conn, monkeypatch):
    """Adding a job by hand stays on the direct API: a person is waiting for that one
    (HIR-222). `batch` defaults to False, so plumbing it through a run_kind=ADD call must
    never even construct a batch function."""
    monkeypatch.setattr(pipeline, "default_batch_fn",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("used the batch API")))

    def fn(text, tax, model):
        v = extractor_version(tax, model)
        from app.extract import Extraction, Mention
        return Extraction(mentions=[Mention("python", "required", "Python")],
                          extractor_version=v, taxonomy_version=tax.version)

    r = pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None,
                                 job_ids=[1], run_kind=langsmith_live.ADD)
    assert r.succeeded == 1


def test_the_report_names_the_jobs_the_batch_never_resolved():
    assert "failed=2" in pipeline.ExtractReport(attempted=2, failed=[(2, "x"), (3, "y")]).line()


# --- cost: the batch price lands on the report, not the standard rate -----------------

def test_the_report_prices_a_batch_run_at_half_the_standard_rate(conn):
    results = {str(i): succeeded([item("python", "Python")]) for i in (1, 2, 3)}
    r = pipeline.extract_pending(conn, TAX, model="m", log=lambda *_: None,
                                 batch=True, batch_fn=batch_fn_returning(results))
    tokens = pipeline.Tokens(input=USAGE["input_tokens"], output=USAGE["output_tokens"],
                             cache_read=USAGE["cache_read_input_tokens"], cache_write=USAGE["cache_creation_input_tokens"])
    assert r.cost_eur == pytest.approx(3 * price_eur(tokens, "m", batch=True))
    assert r.cost_eur == pytest.approx(3 * price_eur(tokens, "m") / 2)
    assert "cost: €" in r.cost_line()


def test_a_direct_run_prices_at_the_standard_rate(conn):
    def fn(text, tax, model):
        from app.extract import Extraction, Mention
        v = extractor_version(tax, model)
        ex = Extraction(mentions=[Mention("python", "required", "Python")],
                        extractor_version=v, taxonomy_version=tax.version)
        ex.usage = dict(USAGE)
        return ex

    r = pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    tokens = pipeline.Tokens(input=USAGE["input_tokens"], output=USAGE["output_tokens"],
                             cache_read=USAGE["cache_read_input_tokens"], cache_write=USAGE["cache_creation_input_tokens"])
    assert r.cost_eur == pytest.approx(3 * price_eur(tokens, "m"))


def test_cost_line_is_none_when_nothing_succeeded():
    assert pipeline.ExtractReport().cost_line() is None


# --- the LangSmith usage_metadata a batch job carries (HIR-222) -----------------------

def test_batch_usage_metadata_is_priced_at_half_the_standard_rate():
    meta = pipeline._batch_usage_metadata(USAGE, "m")
    assert meta["input_tokens"] == 100 and meta["output_tokens"] == 20
    standard_in = (100 * 2.00 + 80 * 0.20) / 1e6   # claude-sonnet-5-5 falls back to DEFAULT_MODEL rates for "m"
    standard_out = 20 * 10.00 / 1e6
    assert meta["input_cost"] == pytest.approx(standard_in / 2)
    assert meta["output_cost"] == pytest.approx(standard_out / 2)
    assert meta["total_cost"] == pytest.approx(meta["input_cost"] + meta["output_cost"])
