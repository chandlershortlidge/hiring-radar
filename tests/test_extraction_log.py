"""The extractor's answer is kept for every reading, and re-reading never destroys the first (HIR-170)."""

import hashlib
import json

import pytest

from app import db, labels, pipeline
from app.extract import Extraction, Mention, extraction_input, extractor_version
from app.ingest import ingest_one
from app.sources import Posting
from app.taxonomy import Taxonomy

TAX = Taxonomy({"version": 2, "skills": [{"id": "python", "display": "Python"}, {"id": "rag", "display": "RAG"}]})


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    ingest_one(conn=c, p=Posting("arbeitnow", "a0", "", "Co0", "AI Engineer", "Berlin",
                                 "Python and RAG job"))
    return c


def fake_extract(mentions, raw_output=None, usage=None):
    """An extractor whose answer carries the model's own tool call, as the real one does."""
    def fn(text, tax, model):
        ex = Extraction(mentions=list(mentions), extractor_version=extractor_version(tax, model),
                        taxonomy_version=tax.version, usage=dict(usage or {}))
        if raw_output is not None:
            # set, not passed to the constructor, so this test does not depend on the field's
            # position and still exercises log_extraction's getattr fallback.
            ex.raw_output = raw_output
        return ex
    return fn


def test_every_extraction_is_logged_with_its_versions_and_raw_output(conn):
    raw = {"skills": [{"skill_id": "python", "requirement": "required", "raw_text": "Python"}],
           "seniority": None}
    fn = fake_extract([Mention("python", "required", "Python")], raw_output=raw,
                      usage={"input_tokens": 1200, "output_tokens": 80})
    pipeline.extract_pending(conn, TAX, fn, "model-x", log=lambda *_: None)

    rows = conn.execute("SELECT * FROM extraction_log").fetchall()
    assert len(rows) == 1
    row = rows[0]
    assert row["model"] == "model-x"
    assert row["taxonomy_version"] == TAX.version
    assert row["extractor_version"] == extractor_version(TAX, "model-x")
    assert json.loads(row["raw_output"]) == raw
    assert json.loads(row["usage"])["input_tokens"] == 1200
    assert row["created_at"].endswith("Z")
    # The hash is of the exact text the model was sent, so a logged answer can be tied back to it.
    sent = extraction_input("AI Engineer", "Python and RAG job")
    assert row["input_sha256"] == hashlib.sha256(sent.encode()).hexdigest()


def test_re_extraction_appends_a_row_and_leaves_the_first(conn):
    """The Done-when of HIR-170: the second reading must not overwrite the first."""
    job_id = conn.execute("SELECT id FROM job").fetchone()[0]
    first = Extraction(mentions=[Mention("python", "required", "Python")],
                       extractor_version="x2-first", taxonomy_version=1)
    first.raw_output = {"skills": ["first answer"]}
    pipeline.store_extraction(conn, job_id, first, "model-old", "the posting text")

    second = Extraction(mentions=[Mention("rag", "required", "RAG")],
                        extractor_version="x2-second", taxonomy_version=2)
    second.raw_output = {"skills": ["second answer"]}
    pipeline.store_extraction(conn, job_id, second, "model-new", "the posting text")

    rows = conn.execute("SELECT extractor_version, model, raw_output FROM extraction_log ORDER BY id").fetchall()
    assert [r["extractor_version"] for r in rows] == ["x2-first", "x2-second"]
    assert [r["model"] for r in rows] == ["model-old", "model-new"]
    assert json.loads(rows[0]["raw_output"]) == {"skills": ["first answer"]}
    # The job itself still holds exactly one current answer, the latest.
    assert [r[0] for r in conn.execute("SELECT skill_id FROM skill_mention")] == ["rag"]


def test_a_failed_extraction_logs_nothing(conn):
    def fn(text, tax, model):
        raise RuntimeError("the provider timed out")
    r = pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    assert r.succeeded == 0 and r.logged == 0
    assert conn.execute("SELECT count(*) FROM extraction_log").fetchone()[0] == 0


def test_deleting_the_posting_keeps_the_reading_we_paid_for(conn):
    """A dropped or cleaned-up posting must not take the model's answer with it."""
    fn = fake_extract([Mention("python", "required", "Python")], raw_output={"skills": []})
    pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    job_id = conn.execute("SELECT id FROM job").fetchone()[0]
    with conn:
        conn.execute("DELETE FROM job WHERE id = ?", (job_id,))
    row = conn.execute("SELECT job_id, input_sha256 FROM extraction_log").fetchone()
    assert row is not None and row["job_id"] is None and row["input_sha256"]
    # The skills went with the job, as before; only the log survives.
    assert conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0] == 0


def test_an_extraction_stored_without_a_reading_logs_nothing(conn):
    """seed_demo and the legacy import build an Extraction by hand; they must not claim a reading."""
    job_id = conn.execute("SELECT id FROM job").fetchone()[0]
    pipeline.store_extraction(conn, job_id, Extraction(mentions=[Mention("python", "required", "Python")],
                                                       extractor_version="legacy", taxonomy_version=1))
    assert conn.execute("SELECT count(*) FROM extraction_log").fetchone()[0] == 0


def test_the_poll_report_counts_logged_and_missing(conn):
    job_id = conn.execute("SELECT id FROM job").fetchone()[0]
    # An extraction from before this logging existed: stored, never logged.
    pipeline.store_extraction(conn, job_id, Extraction(extractor_version="x2-old", taxonomy_version=1))
    assert pipeline.unlogged_extractions(conn) == 1

    fn = fake_extract([Mention("python", "required", "Python")], raw_output={"skills": []})
    r = pipeline.extract_pending(conn, TAX, fn, "m", log=lambda *_: None)
    assert r.logged == 1
    assert pipeline.unlogged_extractions(conn) == 0
    assert r.log_line(pipeline.unlogged_extractions(conn)) == "extraction log: logged=1 missing=0"


def test_jobs_stamped_legacy_are_not_counted_as_missing(conn):
    """Legacy jobs carry an old summary, not a posting, and are never re-read, so a reading
    that was never made must not show up for ever as a gap."""
    job_id = conn.execute("SELECT id FROM job").fetchone()[0]
    with conn:
        conn.execute("UPDATE job SET extracted_version = 'legacy' WHERE id = ?", (job_id,))
    assert pipeline.unlogged_extractions(conn) == 0


# --- the labellers' own answers ---------------------------------------------------


def write_run(tmp_path, run, files):
    raw = tmp_path / run / "raw"
    raw.mkdir(parents=True)
    for name, doc in files.items():
        (raw / name).write_text(json.dumps(doc))
    return tmp_path


def test_import_keeps_one_row_per_labeller_so_disagreement_survives(conn, tmp_path):
    runs = write_run(tmp_path, "20261103T223629Z_label", {
        "golden_049.A.json": {"labeler": "A", "provider": "anthropic", "model": "claude-opus-5-5",
                              "raw": "```json\n{}\n```", "parsed": {"seniority": "junior"},
                              "error": None, "posting_sha256": "aa", "prompt_sha256": "bb"},
        "golden_049.B.json": {"labeler": "B", "provider": "anthropic", "model": "claude-opus-5-5",
                              "raw": "```json\n{}\n```", "parsed": {"seniority": "mid"},
                              "error": None, "posting_sha256": "aa", "prompt_sha256": "bb"},
    })
    r = labels.import_answers(conn, runs, log=lambda *_: None)
    assert (r.runs, r.files, r.inserted, r.already) == (1, 2, 2, 0)
    rows = conn.execute("SELECT labeler, golden_id, answer, posting_sha256 FROM label_answer"
                        " ORDER BY labeler").fetchall()
    assert [row["labeler"] for row in rows] == ["A", "B"]
    assert all(row["golden_id"] == "golden_049" for row in rows)
    # The two labellers disagreed; both answers are readable, not just the agreed one.
    assert [json.loads(row["answer"])["seniority"] for row in rows] == ["junior", "mid"]


def test_a_second_import_adds_nothing_and_overwrites_nothing(conn, tmp_path):
    doc = {"labeler": "A", "parsed": {"seniority": "junior"}, "raw": "x", "error": None}
    runs = write_run(tmp_path, "r1", {"golden_001.A.json": doc})
    labels.import_answers(conn, runs, log=lambda *_: None)
    # The run folder is edited after the import; the imported row must not change.
    (runs / "r1" / "raw" / "golden_001.A.json").write_text(
        json.dumps({**doc, "parsed": {"seniority": "senior"}}))
    r = labels.import_answers(conn, runs, log=lambda *_: None)
    assert (r.inserted, r.already) == (0, 1)
    rows = conn.execute("SELECT answer FROM label_answer").fetchall()
    assert len(rows) == 1
    assert json.loads(rows[0]["answer"])["seniority"] == "junior"


def test_the_earlier_runs_hash_names_and_missing_golden_id_are_handled(conn, tmp_path):
    """The 29 Oct run named its hashes differently and the 27 Oct files carry no golden_id."""
    runs = write_run(tmp_path, "20261029T153540Z_heldout_production", {
        "golden_021.A.json": {"golden_id": "golden_021", "labeler": "A", "parsed": {"german": None},
                              "raw": "x", "error": None, "prompt_sha": "pp", "rules_sha": "rr"},
        "golden_022.B.json": {"labeler": "B", "parsed": {"german": "required"}, "raw": "x", "error": None},
    })
    labels.import_answers(conn, runs, log=lambda *_: None)
    rows = conn.execute("SELECT golden_id, prompt_sha256, posting_sha256 FROM label_answer"
                        " ORDER BY golden_id").fetchall()
    assert [row["golden_id"] for row in rows] == ["golden_021", "golden_022"]
    assert rows[0]["prompt_sha256"] == "pp"
    assert rows[0]["posting_sha256"] is None   # not recorded by that run; not invented


def test_a_labeller_answer_that_did_not_parse_is_kept_verbatim(conn, tmp_path):
    runs = write_run(tmp_path, "r1", {
        "golden_002.A.json": {"labeler": "A", "parsed": None, "raw": "I cannot answer",
                              "error": "no JSON object in the reply"}})
    labels.import_answers(conn, runs, log=lambda *_: None)
    row = conn.execute("SELECT answer, raw, error FROM label_answer").fetchone()
    assert row["answer"] is None
    assert row["raw"] == "I cannot answer"
    assert row["error"] == "no JSON object in the reply"


def test_an_unreadable_file_is_reported_and_the_rest_still_load(conn, tmp_path):
    runs = write_run(tmp_path, "r1", {"golden_003.A.json": {"labeler": "A", "parsed": {}, "raw": "x"}})
    (runs / "r1" / "raw" / "golden_004.B.json").write_text("{not json")
    r = labels.import_answers(conn, runs, log=lambda *_: None)
    assert r.inserted == 1
    assert len(r.skipped) == 1 and "golden_004.B.json" in r.skipped[0][0]


def test_the_real_run_folders_all_import(conn):
    """Against the run folders actually in the repo, not a fixture: every file parses, and the
    3 Nov postings come back with every labeller's answer."""
    r = labels.import_answers(conn, log=lambda *_: None)
    assert r.skipped == []
    assert r.runs >= 4 and r.inserted == r.files
    nov3 = conn.execute(
        "SELECT count(DISTINCT golden_id) FROM label_answer WHERE run LIKE '20261103%'").fetchone()[0]
    assert nov3 == 15
    # Five answers per posting on 3 Nov: a panel of three, then a second run with two.
    assert conn.execute(
        "SELECT count(*) FROM label_answer WHERE run LIKE '20261103%' AND golden_id='golden_049'"
    ).fetchone()[0] == 5
