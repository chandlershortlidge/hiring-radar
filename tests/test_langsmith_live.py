"""Live tracing: off by default, one trace per run with a child per job, never fatal.

conftest.py unsets LANGSMITH_API_KEY for every test, so "tracing is off" is the default
state here and the on-state is built from a fake tree — no test reaches LangSmith.
"""

import contextlib

import pytest

from app import db, langsmith_live, pipeline
from app.extract import EmptyExtractionError, Extraction, Mention, Proposed
from app.ingest import ingest_one
from app.sources import Posting
from app.taxonomy import Taxonomy

TAX = Taxonomy({"version": 2, "skills": [{"id": "python", "display": "Python"},
                                         {"id": "rag", "display": "RAG"}]})
POSTING_TEXT = "We need Python and RAG experience."


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    ingest_one(conn=c, p=Posting("arbeitnow", "a1", "", "Acme", "AI Engineer", "Berlin", POSTING_TEXT))
    return c


def extraction(mentions=(), proposed=(), rejected=(), usage=None):
    return Extraction(mentions=list(mentions), proposed=list(proposed), rejected=list(rejected),
                      extractor_version="v", taxonomy_version=2,
                      usage=usage if usage is not None else {"input_tokens": 11, "output_tokens": 3})


def fake_extract(ex):
    return lambda text, tax, model: ex


# --- the off state ----------------------------------------------------------------

def test_tracing_is_off_without_a_key():
    assert langsmith_live.enabled() is False


def test_off_run_and_job_do_nothing_and_never_touch_langsmith():
    with langsmith_live.run("poll") as run:
        assert run.run_tree is None
        run.note({"a": 1})
        run.tag("x")
        run.finish({"b": 2})
        with run.job(1, "AI Engineer", "text") as span:
            assert span.run_tree is None
            span.result(extraction(), 0, 0)
            span.failed("boom")


def test_off_wrap_client_returns_the_same_object():
    class Client:
        pass

    c = Client()
    assert langsmith_live.wrap_client(c) is c
    assert langsmith_live.wrap_client(None) is None


def test_a_poll_with_tracing_off_stores_exactly_what_it_always_did(conn):
    ex = extraction([Mention("python", "required", "Python")])
    report = pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None,
                                      run_kind=langsmith_live.POLL)
    assert (report.attempted, report.succeeded, report.mentions) == (1, 1, 1)
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 1


# --- grounding on every live reading ----------------------------------------------

def test_a_quote_that_is_in_the_posting_counts_as_grounded(conn):
    ex = extraction([Mention("python", "required", "Python")])
    report = pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None)
    assert (report.quotes, report.grounded, report.grounding_failures) == (1, 1, 0)
    assert report.grounding_line() is None


def test_an_invented_quote_is_counted_and_reported_but_still_stored(conn):
    """The check measures; it never changes what is stored (HIR-160)."""
    ex = extraction([Mention("python", "required", "Python"),
                     Mention("rag", "required", "ten years of RAG at NASA")])
    report = pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None)
    assert (report.quotes, report.grounded, report.grounding_failures) == (2, 1, 1)
    assert "inventing evidence" in report.grounding_line()
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 2


def test_a_quote_the_extractor_already_dropped_counts_against_the_total(conn):
    ex = extraction([Mention("python", "required", "Python")],
                    rejected=[{"item": {"raw_text": "Pythn"},
                               "reason": "raw_text not found in job text"}])
    report = pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None)
    assert (report.quotes, report.grounded, report.grounding_failures) == (2, 1, 1)


def test_a_proposed_skill_quote_is_checked_too(conn):
    ex = extraction(proposed=[Proposed("Rust", "required", "Rust")])
    report = pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None)
    assert (report.quotes, report.grounded) == (1, 0)


# --- the on state, against a fake tree --------------------------------------------

class FakeTree:
    """Stands in for a langsmith RunTree: records what was put on it."""

    def __init__(self, name):
        self.name = name
        self.outputs: dict = {}
        self.metadata: dict = {}
        self.tags: list[str] = []

    def add_outputs(self, outputs):
        self.outputs.update(outputs)

    def add_metadata(self, metadata):
        self.metadata.update(metadata)

    def add_tags(self, tags):
        self.tags += list(tags)


@pytest.fixture
def traced(monkeypatch):
    """Turn tracing on with fake trees, and hand back every tree that was opened."""
    trees: list[FakeTree] = []
    monkeypatch.setattr(langsmith_live, "enabled", lambda: True)

    @contextlib.contextmanager
    def fake_trace(what, **kw):
        tree = FakeTree(kw.get("name", what))
        tree.metadata.update(dict(kw.get("metadata") or {}))
        tree.tags += list(kw.get("tags") or [])
        trees.append(tree)
        yield tree

    monkeypatch.setattr(langsmith_live, "_trace", fake_trace)
    return trees


def test_a_run_is_one_trace_with_a_child_per_job(conn, traced):
    ingest_one(conn=conn, p=Posting("arbeitnow", "a2", "", "Globex", "ML Engineer", "Berlin",
                                    "A second Berlin role, also Python and RAG, at another company."))
    ex = extraction([Mention("python", "required", "Python")])
    pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None,
                             run_kind=langsmith_live.POLL)
    # Newest job first, the order the queue already uses (HIR-193).
    assert [t.name for t in traced] == ["poll", "job 2", "job 1"]


def test_the_run_trace_carries_the_queue_and_the_totals(conn, traced):
    ex = extraction([Mention("python", "required", "Python")])
    pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None,
                             run_kind=langsmith_live.POLL)
    run = traced[0]
    assert run.tags == ["poll"]
    assert run.metadata["taxonomy_version"] == 2 and run.metadata["model"] == "m"
    assert run.metadata["first_reads"] == 1 and run.metadata["reread_queued"] == 0
    assert run.outputs["attempted"] == 1 and run.outputs["succeeded"] == 1
    assert run.outputs["grounding_failures"] == 0


def test_a_job_child_carries_its_tokens_skills_and_grounding(conn, traced):
    ex = extraction([Mention("python", "required", "Python")], usage={"input_tokens": 90, "output_tokens": 7})
    pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None)
    job = traced[1]
    assert job.outputs["skills"] == ["python"]
    assert job.outputs["usage"] == {"input_tokens": 90, "output_tokens": 7}
    assert job.outputs["grounded"] == 1 and job.outputs["grounding"] == 1.0
    assert "grounding-failure" not in job.tags


def test_an_invented_quote_tags_the_job_and_the_run(conn, traced):
    ex = extraction([Mention("rag", "required", "ten years of RAG at NASA")])
    pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None)
    assert "grounding-failure" in traced[1].tags
    assert "grounding-failure" in traced[0].tags


def test_a_failed_reading_is_on_its_job_child_not_only_in_the_log(conn, traced):
    def boom(text, tax, model):
        raise RuntimeError("overloaded")

    pipeline.extract_pending(conn, TAX, boom, "m", log=lambda *_: None)
    assert traced[1].outputs["error"].startswith("RuntimeError: overloaded")
    assert traced[1].tags == ["extraction-failure"]


def test_a_dropped_posting_says_so_on_its_job_child(conn, traced):
    def blank(text, tax, model):
        raise EmptyExtractionError("nothing came back")

    pipeline.extract_pending(conn, TAX, blank, "m", log=lambda *_: None)   # blank read 1 of 2
    traced.clear()
    pipeline.extract_pending(conn, TAX, blank, "m", log=lambda *_: None)   # 2 of 2 -> dropped
    assert traced[1].outputs["dropped"] is True
    assert "dropped" in traced[1].tags


def test_a_re_read_run_is_tagged_and_counted(conn, traced):
    ex = extraction([Mention("python", "required", "Python")])
    pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None)
    traced.clear()
    pipeline.extract_pending(conn, TAX, fake_extract(ex), "m2", log=lambda *_: None)  # new version
    run = traced[0]
    assert "reread" in run.tags
    assert run.metadata["reread_queued"] == 1 and run.metadata["first_reads"] == 0


def test_a_skipped_run_opens_no_trace(conn, traced, monkeypatch):
    """Another extraction holds the lock: nothing was read, so there is nothing to trace."""
    monkeypatch.setattr(pipeline, "_extraction_lock",
                        lambda c: contextlib.nullcontext(False))
    report = pipeline.extract_pending(conn, TAX, fake_extract(extraction()), "m", log=lambda *_: None)
    assert report.skipped_busy is True and traced == []


# --- a LangSmith failure never fails a run ----------------------------------------

def test_a_tree_that_raises_on_every_call_does_not_fail_the_run(conn, monkeypatch, capsys):
    class AngryTree:
        def __getattr__(self, name):
            def fn(*a, **kw):
                raise RuntimeError("langsmith is down")
            return fn

    monkeypatch.setattr(langsmith_live, "enabled", lambda: True)

    @contextlib.contextmanager
    def angry_trace(what, **kw):
        yield AngryTree()

    monkeypatch.setattr(langsmith_live, "_trace", angry_trace)
    ex = extraction([Mention("python", "required", "Python")])
    report = pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None)
    assert report.succeeded == 1
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 1
    assert "langsmith is down" in capsys.readouterr().err


def test_a_trace_that_cannot_be_opened_leaves_the_run_untraced_and_working(conn, monkeypatch, capsys):
    """_trace yields None when LangSmith cannot be reached at all; everything downstream
    then behaves exactly as with tracing off."""
    monkeypatch.setattr(langsmith_live, "enabled", lambda: True)

    class Boom:
        def __init__(self, *a, **kw):
            raise RuntimeError("no network")

    fake = type("M", (), {"trace": Boom})
    monkeypatch.setitem(__import__("sys").modules, "langsmith", fake)
    ex = extraction([Mention("python", "required", "Python")])
    report = pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None)
    assert report.succeeded == 1
    assert "no network" in capsys.readouterr().err


# --- the wrapped client -----------------------------------------------------------

def test_wrap_client_is_idempotent(monkeypatch):
    monkeypatch.setattr(langsmith_live, "enabled", lambda: True)
    calls = []

    class Client:
        pass

    def fake_wrap(c):
        calls.append(c)
        return c

    monkeypatch.setitem(__import__("sys").modules, "langsmith.wrappers",
                        type("M", (), {"wrap_anthropic": staticmethod(fake_wrap)}))
    c = Client()
    once = langsmith_live.wrap_client(c)
    twice = langsmith_live.wrap_client(once)
    assert once is c and twice is c and len(calls) == 1


# --- the package not being installed at all (HIR-233) -----------------------------

@pytest.fixture
def no_langsmith_package(monkeypatch):
    """The VM's state before HIR-233: a key is set, but `import langsmith` fails.

    A None in sys.modules is how Python reports a module that cannot be imported, so this
    is the ModuleNotFoundError the poll hit, without uninstalling anything.
    """
    import sys

    monkeypatch.setattr(langsmith_live, "enabled", lambda: True)
    monkeypatch.setattr(langsmith_live, "_import_warned", False)
    for name in ("langsmith", "langsmith.wrappers"):
        monkeypatch.setitem(sys.modules, name, None)


def test_a_poll_runs_and_stores_when_langsmith_cannot_be_imported(
        conn, no_langsmith_package, capsys):
    """The crash this issue is about: with the key set and the package missing, the poll
    read nothing at all. It now reads and stores exactly as with tracing off."""
    ex = extraction([Mention("python", "required", "Python")])
    report = pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None,
                                      run_kind=langsmith_live.POLL)
    assert (report.attempted, report.succeeded, report.mentions) == (1, 1, 1)
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 1
    assert "[langsmith] import failed, continuing without it" in capsys.readouterr().err


def test_the_missing_package_is_reported_once_not_once_per_job(
        conn, no_langsmith_package, capsys):
    """A poll of 200 jobs would otherwise print 200 identical warnings."""
    ingest_one(conn=conn, p=Posting("arbeitnow", "a2", "", "Beta", "ML Engineer", "Berlin",
                                    POSTING_TEXT))
    ex = extraction([Mention("python", "required", "Python")])
    report = pipeline.extract_pending(conn, TAX, fake_extract(ex), "m", log=lambda *_: None,
                                      run_kind=langsmith_live.POLL)
    assert report.attempted == 2
    assert capsys.readouterr().err.count("[langsmith] import failed") == 1


def test_wrap_client_returns_the_plain_client_when_the_package_is_missing(
        no_langsmith_package):
    class Client:
        pass

    c = Client()
    assert langsmith_live.wrap_client(c) is c
