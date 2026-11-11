"""Adding skills re-reads only the open postings that name one (HIR-224). Any other change
to what the extractor's version stamp covers still re-reads every open job. No model call
anywhere here: `fake_extract` stands in for the reading, as in test_pipeline_poll.py.
"""

import shutil

import pytest

from app import db, extract, pipeline, reread_cost, targeted_reread as tr
from app.extract import Extraction, Mention, extractor_version
from app.ingest import ingest_one
from app.sources import Posting
from app.taxonomy import Taxonomy

PY = {"id": "python", "display": "Python"}
RAG = {"id": "rag", "display": "RAG", "aliases": ["retrieval-augmented generation"]}
TAX = Taxonomy({"version": 2, "skills": [PY, RAG]})
RUST = {"id": "rust", "display": "Rust", "aliases": ["rust-lang"]}
TAX_RUST = Taxonomy({"version": 3, "skills": [PY, RAG, RUST]})
TEXTS = {1: "Python and Rust services", 2: "Python; we trust our team", 3: "Python and RAG only"}
QUIET = dict(log=lambda *_: None)


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    for i in (1, 2, 3):
        ingest_one(conn=c, p=Posting("arbeitnow", f"a{i}", "", f"Co{i}", "AI Engineer", "Berlin", TEXTS[i]))
    return c


def reads():
    """A fake extractor that records which postings it was asked to read."""
    seen = []

    def fn(text, tax, model):
        seen.append(text)
        return Extraction(mentions=[Mention("python", "required", "Python")], proposed=[],
                          extractor_version=extractor_version(tax, model), taxonomy_version=tax.version)
    fn.seen = seen
    return fn


def read_all_at(conn, tax):
    fn = reads()
    pipeline.extract_pending(conn, tax, fn, "m", **QUIET)
    return fn


def job(conn, job_id):
    return conn.execute("SELECT extracted_version, read_version FROM job WHERE id=?", (job_id,)).fetchone()


def _close(conn, job_id):
    conn.execute("UPDATE job SET last_seen='2020-01-01T00:00:00Z' WHERE id=?", (job_id,))
    conn.execute("UPDATE job_source SET last_seen='2020-01-01T00:00:00Z' WHERE job_id=?", (job_id,))


# --- the Done-when cases ---------------------------------------------------------------

def test_adding_one_skill_rereads_only_the_postings_that_name_it(conn):
    read_all_at(conn, TAX)
    old, new = extractor_version(TAX, "m"), extractor_version(TAX_RUST, "m")
    logged = conn.execute("SELECT count(*) FROM extraction_log").fetchone()[0]

    fn = reads()
    r = pipeline.extract_pending(conn, TAX_RUST, fn, "m", **QUIET)

    assert fn.seen == [f"AI Engineer\n\n{TEXTS[1]}"]          # "trust" is not "Rust"
    assert (r.attempted, r.reread_queued, r.carried_over) == (1, 1, 2)
    # Every job is current; the carried-over ones say their reading came from the old version.
    assert tuple(job(conn, 1)) == (new, new)
    assert tuple(job(conn, 2)) == (new, old)
    assert tuple(job(conn, 3)) == (new, old)
    # Their skills and the reading log are untouched: no reading is claimed that never happened.
    assert conn.execute("SELECT extractor_version FROM skill_mention WHERE job_id=2").fetchone()[0] == old
    assert conn.execute("SELECT count(*) FROM extraction_log").fetchone()[0] == logged + 1
    assert pipeline.unlogged_extractions(conn) == 0
    # Nothing left to do on the next run.
    assert pipeline.extract_pending(conn, TAX_RUST, reads(), "m", **QUIET).attempted == 0


def test_adding_a_skill_and_changing_the_prompt_rereads_everything(conn, monkeypatch):
    read_all_at(conn, TAX)
    monkeypatch.setattr(extract, "PRINCIPLES", extract.PRINCIPLES + "\nOne more rule.")
    fn = reads()
    r = pipeline.extract_pending(conn, TAX_RUST, fn, "m", **QUIET)
    assert (r.attempted, r.carried_over) == (3, 0)
    new = extractor_version(TAX_RUST, "m")
    assert all(tuple(job(conn, i)) == (new, new) for i in (1, 2, 3))


def test_the_batch_path_carries_over_the_same_way(conn):
    from tests.test_pipeline_batch import succeeded, item
    read_all_at(conn, TAX)
    submitted = []

    def batch_fn(requests):
        submitted.extend(r["custom_id"] for r in requests)
        return {cid: succeeded([item("python", "Python")]) for cid in submitted}

    r = pipeline.extract_pending(conn, TAX_RUST, model="m", batch=True, batch_fn=batch_fn, **QUIET)
    assert submitted == ["1"]
    assert r.carried_over == 2


# --- what counts as "only added" -------------------------------------------------------

@pytest.mark.parametrize("skills, why", [
    ([RAG, RUST], "a skill removed"),
    ([{"id": "python", "display": "Python 3"}, RAG, RUST], "a skill renamed"),
    ([PY, {"id": "rag", "display": "RAG"}, RUST], "a spelling taken away"),
])
def test_anything_but_an_addition_rereads_everything(conn, skills, why):
    read_all_at(conn, TAX)
    r = pipeline.extract_pending(conn, Taxonomy({"version": 3, "skills": skills}), reads(), "m", **QUIET)
    assert (r.attempted, r.carried_over) == (3, 0), why


def test_an_alias_added_to_an_existing_skill_rereads_the_postings_using_it(conn):
    ingest_one(conn=conn, p=Posting("arbeitnow", "a4", "", "Co4", "AI Engineer", "Berlin", "Build GraphRAG-free retrieval augmented generation"))
    read_all_at(conn, TAX)
    tax2 = Taxonomy({"version": 3, "skills": [PY, {**RAG, "aliases": RAG["aliases"] + ["retrieval augmented generation"]}]})
    fn = reads()
    r = pipeline.extract_pending(conn, tax2, fn, "m", **QUIET)
    assert (r.attempted, r.carried_over) == (1, 3)
    assert "retrieval augmented generation" in fn.seen[0]


def test_a_stamp_with_no_recorded_skill_list_rereads_everything(conn):
    read_all_at(conn, TAX)
    conn.execute("DELETE FROM extractor_snapshot")
    conn.commit()
    r = pipeline.extract_pending(conn, TAX_RUST, reads(), "m", **QUIET)
    assert (r.attempted, r.carried_over) == (3, 0)


def test_two_additions_in_a_row_stay_targeted_and_keep_the_first_reading(conn):
    read_all_at(conn, TAX)
    first = extractor_version(TAX, "m")
    pipeline.extract_pending(conn, TAX_RUST, reads(), "m", **QUIET)
    tax3 = Taxonomy({"version": 4, "skills": [PY, RAG, RUST, {"id": "trust-safety", "display": "Trust"}]})
    fn = reads()
    r = pipeline.extract_pending(conn, tax3, fn, "m", **QUIET)
    assert fn.seen == [f"AI Engineer\n\n{TEXTS[2]}"]
    assert r.carried_over == 2
    assert job(conn, 3)["read_version"] == first


def test_closed_jobs_are_left_alone(conn):
    read_all_at(conn, TAX)
    old = extractor_version(TAX, "m")
    _close(conn, 3)
    r = pipeline.extract_pending(conn, TAX_RUST, reads(), "m", **QUIET)
    assert (r.attempted, r.carried_over, r.skipped_closed) == (1, 1, 1)
    assert tuple(job(conn, 3)) == (old, old)


def test_adding_one_posting_by_hand_never_moves_other_jobs(conn):
    read_all_at(conn, TAX)
    ingest_one(conn=conn, p=Posting("arbeitnow", "a4", "", "Co4", "AI Engineer", "Berlin", "Python"))
    r = pipeline.extract_pending(conn, TAX_RUST, reads(), "m", job_ids=[4], **QUIET)
    assert (r.attempted, r.carried_over) == (1, 0)
    assert job(conn, 2)["extracted_version"] == extractor_version(TAX, "m")


# --- the suggestion queue closes the alias gap (Chandler, 11 Nov) ------------------------

def _suggest(conn, job_id, label, raw):
    conn.execute("INSERT INTO proposed_skill (job_id, label, raw_text) VALUES (?,?,?)", (job_id, label, raw))
    conn.commit()


def test_a_job_the_model_suggested_the_skill_for_is_reread_whatever_its_words(conn):
    read_all_at(conn, TAX)
    # Job 3's text never says "Rust", but the model suggested it from other wording.
    _suggest(conn, 3, "Rust", "systems language with a borrow checker")
    fn = reads()
    r = pipeline.extract_pending(conn, TAX_RUST, fn, "m", **QUIET)
    assert sorted(t[-6:] for t in fn.seen) == sorted([TEXTS[1][-6:], TEXTS[3][-6:]])
    assert r.carried_over == 1


def test_a_suggestion_for_some_other_skill_does_not_trigger_a_reread(conn):
    read_all_at(conn, TAX)
    _suggest(conn, 3, "Kubernetes", "k8s")
    r = pipeline.extract_pending(conn, TAX_RUST, reads(), "m", **QUIET)
    assert (r.attempted, r.carried_over) == (1, 2)


def test_the_models_own_words_are_offered_as_aliases(conn):
    read_all_at(conn, TAX)
    _suggest(conn, 3, "Rust", "rustlang")
    _suggest(conn, 2, "Rust (language)", "Rust programming")  # both already contain "Rust"
    _suggest(conn, 2, "Kubernetes", "k8s")                    # another skill's words
    _suggest(conn, 1, "Rust", "x" * 60)                       # a sentence, not a spelling
    cost = reread_cost.reread_cost(conn, model="m", tax=TAX_RUST, git_ref=None)
    assert cost.offers == (("rust", ("rustlang",)),)
    text = "\n".join(reread_cost.report_lines(cost))
    assert "offer them as aliases" in text and "rust: rustlang" in text


# --- the pure parts --------------------------------------------------------------------

def test_the_core_hash_ignores_the_skill_list_and_nothing_else(monkeypatch):
    a, b = tr.snapshot(TAX, "m"), tr.snapshot(TAX_RUST, "m")
    assert a.version != b.version and a.core == b.core
    assert tr.snapshot(TAX, "other-model").core != a.core
    for name, value in [("PRINCIPLES", extract.PRINCIPLES + "x"), ("INPUT_FORMAT", "other"),
                        ("TOOL", {**extract.TOOL, "name": "other"})]:
        with monkeypatch.context() as m:
            m.setattr(extract, name, value)
            assert tr.snapshot(TAX, "m").core != a.core, name


def test_names_match_case_insensitively_on_word_boundaries():
    pat = tr.names_pattern(["Rust", ".NET", "Ruby on Rails", "C#"])
    for text in ["RUST", "rust,", "We use .NET 8", "ruby  on\nrails", "C# or Java"]:
        assert pat.search(tr._norm(text)), text
    for text in ["trust", "rusty", "dotnet", "ASP.NETCore", "C#m"]:
        assert not pat.search(tr._norm(text)), text


def test_added_names_cover_the_id_display_and_aliases():
    names, ids = tr.added_names(tr.snapshot(TAX, "m"), tr.snapshot(TAX_RUST, "m"))
    assert ids == ["rust"]
    assert {"rust", "Rust", "rust-lang"} <= set(names)


# --- the cost figure -------------------------------------------------------------------

def test_reread_cost_counts_only_the_jobs_a_skill_addition_rereads(conn):
    read_all_at(conn, TAX)
    cost = reread_cost.reread_cost(conn, model="m", tax=TAX_RUST, git_ref=None)
    assert (cost.jobs, cost.full_jobs, cost.carried, cost.added_ids) == (1, 3, 2, ("rust",))
    assert "keep their reading, 2 of them" in "\n".join(reread_cost.report_lines(cost))


def test_reread_cost_on_an_unchanged_branch_reports_the_full_figure(conn):
    read_all_at(conn, TAX)
    cost = reread_cost.reread_cost(conn, model="m", tax=TAX, git_ref=None)
    assert (cost.jobs, cost.unchanged) == (3, True)
    assert "re-reads nothing" in "\n".join(reread_cost.report_lines(cost))


def test_reread_cost_falls_back_to_the_main_branch_skill_list(conn, monkeypatch):
    read_all_at(conn, TAX)
    conn.execute("DELETE FROM extractor_snapshot")
    conn.commit()
    monkeypatch.setattr(tr, "snapshot_from_git", lambda model, ref: tr.snapshot(TAX, model))
    assert reread_cost.reread_cost(conn, model="m", tax=TAX_RUST).jobs == 1


# --- storage ---------------------------------------------------------------------------

def test_the_migration_backfills_read_version_from_the_existing_stamp(tmp_path):
    before = tmp_path / "migrations"
    before.mkdir()
    for f in sorted(db.MIGRATIONS_DIR.glob("*.sql")):
        if int(f.name[:3]) < 19:
            shutil.copy(f, before / f.name)
    c = db.connect(tmp_path / "old.db")
    db.migrate(c, before)
    ingest_one(conn=c, p=Posting("arbeitnow", "a1", "", "Co1", "AI Engineer", "Berlin", TEXTS[1]))
    c.execute("UPDATE job SET extracted_version='x2-old'")
    c.commit()
    db.migrate(c)
    assert tuple(c.execute("SELECT extracted_version, read_version FROM job").fetchone()) == ("x2-old", "x2-old")


def test_the_dashboard_records_the_skill_list_it_starts_with(tmp_path):
    from app.api import create_app
    create_app(tmp_path / "api.db", taxonomy=TAX)
    c = db.connect(tmp_path / "api.db")
    assert set(tr.load_snapshots(c)) == {extractor_version(TAX, extract.DEFAULT_MODEL)}
