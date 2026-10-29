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


def test_extraction_stores_german_and_degree_on_the_job(conn):
    from app.extract import Degree, German
    def fn(text, tax, model):
        return Extraction(mentions=[], german=German("required", "inferred", None),
                          degree=Degree("master", "required", True, "M.Sc."),
                          extractor_version=extractor_version(tax, model), taxonomy_version=tax.version)
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    row = conn.execute("SELECT german, german_basis, german_signal, degree, degree_requirement, degree_or_equivalent, degree_signal"
                       " FROM job WHERE id=1").fetchone()
    assert tuple(row) == ("required", "inferred", None, "master", "required", 1, "M.Sc.")


def test_extraction_stores_production_on_the_job(conn):
    from app.extract import Production
    def fn(text, tax, model):
        return Extraction(mentions=[], production=Production("required", "stated", "shipped to production"),
                          extractor_version=extractor_version(tax, model), taxonomy_version=tax.version)
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    row = conn.execute("SELECT production, production_basis, production_signal FROM job WHERE id=1").fetchone()
    assert tuple(row) == ("required", "stated", "shipped to production")


def test_extraction_clears_production_when_not_asked_for(conn):
    """Re-extraction overwrites, so a job that loses the demand must go back to NULL."""
    conn.execute("UPDATE job SET production='required', production_basis='stated', production_signal='x' WHERE id=1")
    def fn(text, tax, model):
        return Extraction(mentions=[], extractor_version=extractor_version(tax, model), taxonomy_version=tax.version)
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    row = conn.execute("SELECT production, production_basis, production_signal FROM job WHERE id=1").fetchone()
    assert tuple(row) == (None, None, None)


def test_legacy_stamped_jobs_are_never_re_extracted(conn):
    conn.execute("UPDATE job SET extracted_version='legacy' WHERE id=1")
    r = pipeline.extract_pending(conn, TAX, fake_extract([Mention("python", "required", "Python")]), "m", log=lambda *_: None)
    assert r.attempted == 2
    assert conn.execute("SELECT extracted_version FROM job WHERE id=1").fetchone()[0] == "legacy"


def test_a_rejected_label_is_not_re_queued(conn):
    fn = fake_extract([], [Proposed("Search", "required", "search"), Proposed("Rust", "required", "Rust")])
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    conn.execute("UPDATE proposed_skill SET status='rejected' WHERE label='Search'")
    pipeline.extract_pending(conn, TAX, fn, "m2", log=lambda *_: None)  # new version: everything re-extracts
    pending = [r[0] for r in conn.execute("SELECT label FROM proposed_skill WHERE status='pending'")]
    assert sorted(set(pending)) == ["Rust"] and len(pending) == 3


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


def test_poll_feeds_warns_when_a_known_board_comes_back_empty(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    feed = {"type": "join", "token": "motor-ai", "company": "MOTOR Ai"}
    posting = [Posting("join", "16835641", "https://join.com/companies/motor-ai/16835641-ai-ml-engineer",
                       "MOTOR Ai", "AI Engineer", "Berlin", "Python please")]

    lines = []
    poll.poll_feeds(conn, [feed], fetch=lambda f: posting, log=lines.append)
    assert not any("WARNING" in l for l in lines)  # first run, nothing to compare against

    lines.clear()
    poll.poll_feeds(conn, [feed], fetch=lambda f: [], log=lines.append)
    assert any("join:motor-ai: WARNING seen=0 but 1 postings" in l for l in lines)

    lines.clear()  # a search feed with no history stays quiet
    poll.poll_feeds(conn, [{"type": "arbeitnow"}], fetch=lambda f: [], log=lines.append)
    assert not any("WARNING" in l for l in lines)


def test_load_feeds_skips_disabled(tmp_path):
    p = tmp_path / "feeds.json"
    p.write_text(json.dumps({"feeds": [{"type": "arbeitnow", "enabled": True}, {"type": "lever", "enabled": False, "token": "x"}]}))
    assert [f["type"] for f in poll.load_feeds(p)] == ["arbeitnow"]


def test_committed_feeds_config_is_valid():
    for f in poll.load_feeds():
        assert f["type"] in ("arbeitnow", "arbeitsagentur", "jsearch", "startup_jobs", "greenhouse", "lever", "ashby", "join")


def test_extraction_stores_seniority_on_the_job(conn):
    from app.extract import Seniority

    def fn(text, tax, model):
        x = fake_extract([Mention("python", "required", "Python")])(text, tax, model)
        x.seniority = Seniority("junior", "stated", "Junior")
        return x

    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    row = conn.execute("SELECT seniority, seniority_basis, seniority_signal FROM job WHERE id=1").fetchone()
    assert tuple(row) == ("junior", "stated", "Junior")


def test_select_feeds_by_label():
    import pytest
    feeds = [{"type": "arbeitnow"}, {"type": "ashby", "token": "jupus"},
             {"type": "startup_jobs", "search": "AI engineer"}]
    assert poll.select_feeds(feeds, []) == feeds
    assert poll.select_feeds(feeds, ["ashby:jupus"]) == [feeds[1]]
    assert poll.select_feeds(feeds, ["startup_jobs:AI engineer", "arbeitnow"]) == [feeds[0], feeds[2]]
    with pytest.raises(ValueError, match="ashby:nope"):
        poll.select_feeds(feeds, ["ashby:nope"])


def test_extract_pending_sends_the_title_with_the_text(conn):
    seen = []

    def fn(text, tax, model):
        seen.append(text)
        return fake_extract([])(text, tax, model)

    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    assert seen and all(t.startswith("AI Engineer\n\nPython and RAG job") for t in seen)


def test_store_extraction_keeps_rejects_and_replaces_them_on_re_extract(conn):
    job_id = conn.execute("SELECT id FROM job ORDER BY id LIMIT 1").fetchone()[0]
    v = extractor_version(TAX, "m")
    first = Extraction(extractor_version=v, taxonomy_version=TAX.version, rejected=[
        {"item": {"skill_id": "python", "requirement": "required", "raw_text": "Pythn"}, "reason": "raw_text not found in job text"},
        {"item": "junk", "reason": "not an object"},
    ])
    pipeline.store_extraction(conn, job_id, first)
    rows = conn.execute("SELECT reason, skill_id, raw_text, extractor_version FROM extraction_reject"
                        " WHERE job_id=? ORDER BY id", (job_id,)).fetchall()
    assert [tuple(r) for r in rows] == [("raw_text not found in job text", "python", "Pythn", v),
                                        ("not an object", None, None, v)]

    pipeline.store_extraction(conn, job_id, Extraction(extractor_version=v, taxonomy_version=TAX.version))
    assert conn.execute("SELECT count(*) FROM extraction_reject WHERE job_id=?", (job_id,)).fetchone()[0] == 0
