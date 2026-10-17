import json

import pytest

from app import db, pipeline, poll
from app.extract import Extraction, Mention, Proposed, extractor_version
from app.ingest import ingest_one
from app.sources import Posting
from app.taxonomy import Taxonomy

TAX = Taxonomy({"version": 2, "skills": [{"id": "python", "display": "Python"}, {"id": "rag", "display": "RAG"}]})


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    for i in range(3):
        ingest_one(conn=c, p=Posting("arbeitnow", f"a{i}", "", f"Co{i}", "AI Engineer", "Berlin", f"Python and RAG job {i}"))
    return c


def fake_extract(mentions, proposed=()):
    def fn(text, tax, model):
        v = extractor_version(tax, model)
        return Extraction(mentions=list(mentions), proposed=list(proposed), extractor_version=v, taxonomy_version=tax.version)
    return fn


def test_extract_pending_stores_mentions_and_stamps_jobs(conn):
    fn = fake_extract([Mention("python", "required", "Python")], [Proposed("Rust", "required", "Rust")])
    r = pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    assert (r.attempted, r.succeeded, r.mentions, r.proposed) == (3, 3, 3, 3)
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 3
    assert conn.execute("SELECT count(*) FROM proposed_skill WHERE status='pending'").fetchone()[0] == 3
    assert conn.execute("SELECT count(*) FROM job WHERE extracted_version IS NULL").fetchone()[0] == 0
    # Second run: nothing to do.
    assert pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None).attempted == 0


def test_zero_skill_job_is_stamped_and_not_retried(conn):
    r = pipeline.extract_pending(conn, TAX, fake_extract([]), "m", log=lambda *_: None)
    assert r.succeeded == 3 and r.mentions == 0
    assert pipeline.extract_pending(conn, TAX, fake_extract([]), "m", log=lambda *_: None).attempted == 0


def test_failed_job_stays_pending_and_others_proceed(conn):
    calls = {"n": 0}

    def flaky(text, tax, model):
        calls["n"] += 1
        if "job 1" in text:
            raise RuntimeError("boom")
        return fake_extract([Mention("rag", "required", "RAG")])(text, tax, model)

    r = pipeline.extract_pending(conn, TAX, flaky, "m", log=lambda *_: None)
    assert r.succeeded == 2 and [j for j, _ in r.failed] == [2]
    assert conn.execute("SELECT count(*) FROM job WHERE extracted_version IS NULL").fetchone()[0] == 1


def test_version_bump_requeues_everything(conn):
    fn = fake_extract([Mention("python", "required", "Python")])
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    tax2 = Taxonomy({"version": 3, "skills": [{"id": "python", "display": "Python"}]})
    r = pipeline.extract_pending(conn, tax2, fn, "m", log=lambda *_: None)
    assert r.attempted == 3
    versions = {r[0] for r in conn.execute("SELECT DISTINCT extractor_version FROM skill_mention")}
    assert versions == {extractor_version(tax2, "m")}  # replaced, not accumulated
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 3


def test_poll_feeds_continues_past_a_failing_feed(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    feeds = [{"type": "arbeitnow"}, {"type": "greenhouse", "token": "acme"}]
    good = [Posting("greenhouse", "1", "", "Acme", "AI Engineer", "Berlin", "Python please")]

    def fetch(feed):
        if feed["type"] == "arbeitnow":
            raise OSError("timeout")
        return good

    lines = []
    r = poll.poll_feeds(conn, feeds, fetch=fetch, log=lines.append)
    assert r.new == 1 and r.new_job_ids == [1]
    assert any("arbeitnow: FAILED OSError" in l for l in lines)


def test_load_feeds_skips_disabled(tmp_path):
    p = tmp_path / "feeds.json"
    p.write_text(json.dumps({"feeds": [{"type": "arbeitnow", "enabled": True}, {"type": "lever", "enabled": False, "token": "x"}]}))
    assert [f["type"] for f in poll.load_feeds(p)] == ["arbeitnow"]


def test_committed_feeds_config_is_valid():
    for f in poll.load_feeds():
        assert f["type"] in ("arbeitnow", "startup_jobs", "greenhouse", "lever", "ashby")


def test_extraction_stores_seniority_on_the_job(conn):
    from app.extract import Seniority

    def fn(text, tax, model):
        x = fake_extract([Mention("python", "required", "Python")])(text, tax, model)
        x.seniority = Seniority("junior", "stated", "Junior")
        return x

    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    row = conn.execute("SELECT seniority, seniority_basis, seniority_signal FROM job WHERE id=1").fetchone()
    assert tuple(row) == ("junior", "stated", "Junior")
