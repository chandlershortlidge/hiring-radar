import json

import pytest

from app import db, pipeline, poll
from app.extract import EmptyExtractionError, Extraction, Mention, Proposed, extractor_version
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


def _blank(text, tax, model):
    raise EmptyExtractionError("tool call carried nothing")


def _blanks(conn, job_id):
    return conn.execute("SELECT blank_extractions FROM job WHERE id=?", (job_id,)).fetchone()[0]


def test_a_blank_read_is_counted_and_the_job_stays_for_one_more_try(conn):
    # HIR-172: try twice, then drop (Chandler's decision of 5 Nov). First read: counted only.
    r = pipeline.extract_pending(conn, TAX, _blank, "m", log=lambda *_: None)
    assert sorted(j for j, _ in r.failed) == [1, 2, 3] and r.dropped == []  # queue order is newest first (HIR-193)
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 3
    assert [_blanks(conn, i) for i in (1, 2, 3)] == [1, 1, 1]
    assert conn.execute("SELECT count(*) FROM job WHERE extracted_version IS NULL").fetchone()[0] == 3


def test_a_second_blank_read_drops_the_posting(conn):
    pipeline.extract_pending(conn, TAX, _blank, "m", log=lambda *_: None)
    r = pipeline.extract_pending(conn, TAX, _blank, "m", log=lambda *_: None)
    assert sorted(j for j, _ in r.dropped) == [1, 2, 3]  # queue order is newest first (HIR-193)
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 0
    assert conn.execute("SELECT count(*) FROM job_source").fetchone()[0] == 0  # cascaded
    # Nothing is left to attempt, so a third run is free.
    assert pipeline.extract_pending(conn, TAX, _blank, "m", log=lambda *_: None).attempted == 0


def test_a_posting_that_reads_blank_once_then_fine_is_kept(conn):
    reads = {"n": 0}

    def blank_then_fine(text, tax, model):
        reads["n"] += 1
        if reads["n"] <= 3:
            raise EmptyExtractionError("tool call carried nothing")
        return fake_extract([Mention("python", "required", "Python")])(text, tax, model)

    pipeline.extract_pending(conn, TAX, blank_then_fine, "m", log=lambda *_: None)
    r = pipeline.extract_pending(conn, TAX, blank_then_fine, "m", log=lambda *_: None)
    assert r.succeeded == 3 and r.dropped == []
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 3
    assert [_blanks(conn, i) for i in (1, 2, 3)] == [1, 1, 1]  # the count is not reset, by design


def test_an_ordinary_failure_is_never_counted_as_blank_or_dropped(conn):
    # A connection error says nothing about the posting, so it is retried for ever.
    def boom(text, tax, model):
        raise RuntimeError("boom")

    for _ in range(3):
        r = pipeline.extract_pending(conn, TAX, boom, "m", log=lambda *_: None)
    assert r.dropped == [] and len(r.failed) == 3
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 3
    assert [_blanks(conn, i) for i in (1, 2, 3)] == [0, 0, 0]


def test_the_report_line_names_dropped_postings(conn):
    pipeline.extract_pending(conn, TAX, _blank, "m", log=lambda *_: None)
    r = pipeline.extract_pending(conn, TAX, _blank, "m", log=lambda *_: None)
    assert "failed=3 dropped=3" in r.line()


def test_version_bump_requeues_everything(conn):
    fn = fake_extract([Mention("python", "required", "Python")])
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    tax2 = Taxonomy({"version": 3, "skills": [{"id": "python", "display": "Python"}]})
    r = pipeline.extract_pending(conn, tax2, fn, "m", log=lambda *_: None)
    assert r.attempted == 3
    versions = {r[0] for r in conn.execute("SELECT DISTINCT extractor_version FROM skill_mention")}
    assert versions == {extractor_version(tax2, "m")}  # replaced, not accumulated
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 3


def test_never_extracted_jobs_come_before_re_reads_newest_first(conn):
    # Stamp jobs 1 and 3 with an old version; job 2 was never read. After a version bump the
    # queue holds all three, and the unread job must come first so a fresh posting never waits
    # behind a database-wide re-read (HIR-193). Within each group: newest first.
    conn.execute("UPDATE job SET extracted_version='x2-old' WHERE id IN (1, 3)")
    rows = pipeline.jobs_needing_extraction(conn, "x2-new")
    assert [r["id"] for r in rows] == [2, 3, 1]


def _close(conn, job_id):
    """Make a job closed under the dashboard's open rule: no sighting for years."""
    conn.execute("UPDATE job SET last_seen='2020-01-01T00:00:00Z' WHERE id=?", (job_id,))
    conn.execute("UPDATE job_source SET last_seen='2020-01-01T00:00:00Z' WHERE job_id=?", (job_id,))


def test_version_bump_requeues_only_open_jobs(conn):
    # All three jobs carry an old stamp; job 1 is closed. The bump re-reads only the open
    # two, and the closed job keeps its old skills and old version stamp (HIR-195).
    fn = fake_extract([Mention("python", "required", "Python")])
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    old = extractor_version(TAX, "m")
    _close(conn, 1)
    tax2 = Taxonomy({"version": 3, "skills": [{"id": "python", "display": "Python"}]})
    assert [r["id"] for r in pipeline.jobs_needing_extraction(conn, extractor_version(tax2, "m"))] == [3, 2]
    r = pipeline.extract_pending(conn, tax2, fn, "m", log=lambda *_: None)
    assert (r.attempted, r.reread_queued, r.skipped_closed) == (2, 2, 1)
    assert conn.execute("SELECT extracted_version FROM job WHERE id=1").fetchone()[0] == old
    assert conn.execute("SELECT extractor_version FROM skill_mention WHERE job_id=1").fetchone()[0] == old


def test_a_closed_job_never_read_still_gets_its_first_read(conn):
    # Only re-reads are limited to open jobs: a job with no extraction at all is read
    # whatever its status, or it would stay blank for ever.
    _close(conn, 2)
    assert [r["id"] for r in pipeline.jobs_needing_extraction(conn, "v1")] == [3, 2, 1]


def test_a_reopened_repost_with_a_stale_stamp_is_requeued(conn):
    fn = fake_extract([Mention("python", "required", "Python")])
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    _close(conn, 1)
    assert 1 not in [r["id"] for r in pipeline.jobs_needing_extraction(conn, "v-new")]
    # The poll sees the same posting again: ingest bumps last_seen, the job counts as open.
    ingest_one(conn=conn, p=Posting("arbeitnow", "a0", "", "Co0", "AI Engineer", "Berlin", "Python and RAG job 0"))
    assert 1 in [r["id"] for r in pipeline.jobs_needing_extraction(conn, "v-new")]


def test_the_log_states_reread_and_closed_skip_counts(conn):
    fn = fake_extract([Mention("python", "required", "Python")])
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    _close(conn, 3)
    lines = []
    tax2 = Taxonomy({"version": 3, "skills": [{"id": "python", "display": "Python"}]})
    pipeline.extract_pending(conn, tax2, fn, "m", log=lines.append)
    assert any("2 open jobs queued" in l and "1 closed jobs skipped" in l for l in lines)


def test_extract_pending_processes_the_queue_in_that_order(conn):
    conn.execute("UPDATE job SET extracted_version='x2-old' WHERE id IN (1, 3)")
    seen = []
    def fn(text, tax, model):
        seen.append(text)
        return fake_extract([Mention("python", "required", "Python")])(text, tax, model)
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    assert [t[-1] for t in seen] == ["1", "2", "0"]  # job text ends in its index: ids 2, 3, 1


def test_a_run_of_three_with_no_skills_at_all_is_flagged_all_blank(conn):
    fn = fake_extract([])  # succeeds, zero mentions, every time
    r = pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    assert (r.attempted, r.mentions) == (3, 0)
    assert r.all_blank


def test_a_small_or_partly_successful_run_is_not_all_blank(conn):
    fn = fake_extract([])
    r = pipeline.extract_pending(conn, TAX, fn, "m", limit=2, log=lambda *_: None)
    assert r.attempted == 2 and not r.all_blank  # below ALL_BLANK_MIN: could be sparse postings
    one = fake_extract([Mention("python", "required", "Python")])
    r2 = pipeline.extract_pending(conn, TAX, one, "m", log=lambda *_: None)
    assert r2.mentions > 0 and not r2.all_blank
    busy = pipeline.ExtractReport(skipped_busy=True)
    assert not busy.all_blank


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


def test_a_second_extraction_on_the_same_database_skips(conn, tmp_path):
    import fcntl
    path = next(r[2] for r in conn.execute("PRAGMA database_list") if r[1] == "main")
    called = []

    def fn(text, tax, model):
        called.append(text)
        return fake_extract([])(text, tax, model)

    with open(path + ".extract.lock", "w") as fh:  # another run holds the lock
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        r = pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    assert r.skipped_busy and r.attempted == 0 and not called
    assert "skipped" in r.line()
    # released: the next run extracts the pending jobs
    assert pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None).attempted == 3
