"""launch_check: scoring the labeller panel's agreed labels against the stored extraction.

Mostly arithmetic — `compare` and `unsure_rule` are pure, so most of this needs neither a
database nor a run directory. The few tests that do build both in `tmp_path`: a run
directory of plain JSON and a one-table SQLite file. Nothing here calls a model.
"""

import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("launch_check", ROOT / "scripts" / "launch_check.py")
lc = importlib.util.module_from_spec(spec)
sys.modules["launch_check"] = lc
spec.loader.exec_module(lc)


def skills(*pairs):
    return [{"skill_id": s, "requirement": r} for s, r in pairs]


def unsure_item(golden_id, skill_id, requirement="required"):
    """A queue item of the kind HIR-159 is about: both labellers found the skill and agreed
    on it, and one of them flagged itself unsure."""
    side = {"skill_id": skill_id, "requirement": requirement, "raw_text": skill_id}
    return {"golden_id": golden_id, "kind": "skill", "key": skill_id, "reason": "uncertain",
            "a": dict(side), "b": dict(side), "excerpt": f"...{skill_id}...", "problems": [],
            "decision": "?"}


def queue(*verdicts):
    """A review_queue.md with one numbered item per verdict, in order."""
    return "\n\n".join(f"## {n}. an item\n\nDECISION: {v}"
                       for n, v in enumerate(verdicts, 1)) + "\n"


def write_run(tmp_path, merged, picks, items=(), verdicts=(), adjudication=None):
    """A labelling run directory on disk, as `load_run` reads one."""
    run = tmp_path / "20260101T000000Z_label"
    (run / "raw").mkdir(parents=True)
    (run / "merged.json").write_text(json.dumps(merged))
    (run / "picks.json").write_text(json.dumps(picks))
    (run / "items.json").write_text(json.dumps(list(items)))
    (run / "review_queue.md").write_text(queue(*verdicts) if verdicts else "")
    if adjudication is not None:
        (run / "adjudication.json").write_text(json.dumps(adjudication))
    return run


def one_job_db(tmp_path, rows):
    """A database with just the table launch_check reads: (job_id, skill_id, requirement)."""
    path = tmp_path / "test.db"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE skill_mention (job_id INTEGER, skill_id TEXT, requirement TEXT)")
    conn.executemany("INSERT INTO skill_mention VALUES (?, ?, ?)", rows)
    conn.commit()
    conn.close()
    return path


def test_a_perfect_match_scores_one():
    both = {"g1": skills(("python", "required"), ("pytorch", "nice_to_have"))}
    s = lc.compare(both, dict(both))
    assert s["precision"] == 1.0 and s["recall"] == 1.0 and s["f1"] == 1.0
    assert s["requirement_accuracy"] == 1.0
    assert (s["tp"], s["fp"], s["fn"]) == (2, 0, 0)


def test_a_skill_the_extractor_missed_is_a_false_negative():
    expected = {"g1": skills(("python", "required"), ("rag", "required"))}
    predicted = {"g1": skills(("python", "required"))}
    s = lc.compare(expected, predicted)
    assert (s["tp"], s["fp"], s["fn"]) == (1, 0, 1)
    assert s["precision"] == 1.0 and s["recall"] == 0.5


def test_a_skill_only_the_extractor_found_is_a_false_positive():
    s = lc.compare({"g1": skills(("python", "required"))},
                   {"g1": skills(("python", "required"), ("kubernetes", "required"))})
    assert (s["tp"], s["fp"], s["fn"]) == (1, 1, 0)
    assert s["recall"] == 1.0 and s["precision"] == 0.5


def test_the_same_skill_at_the_wrong_requirement_still_counts_as_found():
    """Requirement accuracy is reported apart from F1, as in the eval."""
    s = lc.compare({"g1": skills(("python", "required"))},
                   {"g1": skills(("python", "nice_to_have"))})
    assert (s["tp"], s["fp"], s["fn"]) == (1, 0, 0)
    assert s["f1"] == 1.0 and s["requirement_accuracy"] == 0.0


def test_a_posting_the_extractor_read_as_empty_is_all_false_negatives():
    s = lc.compare({"g1": skills(("python", "required"), ("sql", "required"))}, {"g1": []})
    assert (s["tp"], s["fp"], s["fn"]) == (0, 0, 2)
    assert s["recall"] == 0.0


def test_scores_are_micro_averaged_across_postings():
    """One posting's miss does not count as much as a posting with many labels."""
    expected = {"g1": skills(("python", "required")),
                "g2": skills(("rag", "required"), ("sql", "required"), ("pytorch", "required"))}
    predicted = {"g1": [], "g2": skills(("rag", "required"), ("sql", "required"),
                                        ("pytorch", "required"))}
    s = lc.compare(expected, predicted)
    assert (s["tp"], s["fn"]) == (3, 1)
    assert s["recall"] == pytest.approx(0.75)      # micro, not the 0.5 a per-posting mean gives


def test_load_run_skips_a_posting_the_panel_agreed_nothing_on(tmp_path, monkeypatch):
    """Nothing agreed is not the same as the extractor being wrong — it must not be scored."""
    run = write_run(
        tmp_path,
        merged={"golden_001": {"accepted_skills": [{"skill_id": "python",
                                                    "requirement": "required"}]},
                "golden_002": {"accepted_skills": []}},
        picks=[{"golden_id": "golden_001", "job_id": 11},
               {"golden_id": "golden_002", "job_id": 12}])
    monkeypatch.setattr(lc, "LABELING_DIR", tmp_path)
    r = lc.load_run(run.name)
    assert list(r.expected) == ["golden_001"]
    assert r.skipped == ["golden_002"]
    assert r.job_of == {"golden_001": 11, "golden_002": 12}
    assert (r.set_aside, r.waiting, r.n_set_aside) == ({}, 0, 0)


# The unsure rule (HIR-159): a skill both labellers found, one of them unsure about.


def test_an_unanswered_unsure_skill_is_set_aside_and_the_queue_is_counted():
    items = [unsure_item("golden_001", "python"),
             {"golden_id": "golden_001", "kind": "attribute", "key": "degree",
              "reason": "spot-check", "a": None, "b": None, "problems": []}]
    confirmed, set_aside, waiting = lc.unsure_rule(items, {1: "?", 2: ""}, set())
    assert confirmed == {}
    assert set_aside == {"golden_001": {"python"}}
    assert waiting == 2            # the queue's length counts every kind of item, not only skills


def test_a_person_keeping_an_unsure_skill_puts_it_back_in_the_yardstick():
    items = [unsure_item("golden_001", "python", "nice_to_have")]
    confirmed, set_aside, waiting = lc.unsure_rule(items, {1: "ok"}, set())
    assert confirmed == {"golden_001": [{"skill_id": "python", "requirement": "nice_to_have"}]}
    assert (set_aside, waiting) == ({}, 0)


def test_a_person_rejecting_an_unsure_skill_leaves_it_out_and_the_extractor_answers_for_it():
    """`drop` is an answer: the skill is not a label, so the rule stops protecting it."""
    confirmed, set_aside, waiting = lc.unsure_rule([unsure_item("golden_001", "python")],
                                                   {1: "drop"}, set())
    assert (confirmed, set_aside, waiting) == ({}, {}, 0)


def test_a_person_can_pick_one_labeller_or_rewrite_the_label():
    items = [unsure_item("golden_001", "python"), unsure_item("golden_002", "sql")]
    items[0]["b"] = {"skill_id": "python", "requirement": "nice_to_have", "raw_text": "Python"}
    confirmed, _, _ = lc.unsure_rule(
        items, {1: "B", 2: '{"requirement": "nice_to_have"}'}, set())
    assert confirmed == {
        "golden_001": [{"skill_id": "python", "requirement": "nice_to_have"}],
        "golden_002": [{"skill_id": "sql", "requirement": "nice_to_have"}]}


def test_a_verdict_written_by_a_model_is_not_a_hand_check():
    """The rule waits for Chandler. A judge or third labeller settling an item in the queue
    leaves it set aside, because a model has not checked it (DECISIONS 2026-11-03)."""
    confirmed, set_aside, waiting = lc.unsure_rule([unsure_item("golden_001", "python")],
                                                   {1: "ok"}, {1})
    assert confirmed == {}
    assert set_aside == {"golden_001": {"python"}}
    assert waiting == 0            # it does carry a verdict, so it is not waiting to be written


def test_a_verdict_the_item_does_not_allow_stops_the_script():
    """A typo must not read as "still waiting": that would silently set the skill aside."""
    with pytest.raises(SystemExit) as e:
        lc.unsure_rule([unsure_item("golden_001", "python")], {1: "yes"}, set())
    assert "python" in str(e.value) and "'yes'" in str(e.value)


def test_a_set_aside_skill_counts_neither_for_nor_against_the_extractor(tmp_path, monkeypatch):
    """HIR-139's finding, as arithmetic: 29 of New York's 35 extractor "mistakes" were
    skills both labellers found and one flagged unsure. Set aside, such a skill leaves the
    score untouched — no false positive for storing it, no false negative for missing it."""
    run = write_run(
        tmp_path,
        merged={"golden_001": {"accepted_skills": [{"skill_id": "sql",
                                                    "requirement": "required"}]}},
        picks=[{"golden_id": "golden_001", "job_id": 11}],
        items=[unsure_item("golden_001", "python")],
        verdicts=["?"])
    monkeypatch.setattr(lc, "LABELING_DIR", tmp_path)
    monkeypatch.setattr(lc, "DB", one_job_db(tmp_path, [(11, "sql", "required"),
                                                        (11, "python", "required")]))
    s, r = lc.score_run(run.name)
    assert (s["tp"], s["fp"], s["fn"]) == (1, 0, 0)
    assert s["precision"] == 1.0 and s["f1"] == 1.0
    assert (r.n_set_aside, r.waiting) == (1, 1)
    assert lc.counts_line(run.name, r) == (
        f"run {run.name}: 1 posting scored, 1 skill set aside unchecked, "
        "1 item waiting in the hand-check queue")


def test_before_the_rule_that_same_skill_was_a_mistake():
    """What the old behaviour scored, for contrast: the unsure skill stayed out of the
    yardstick and the extractor's copy of it was a false positive."""
    s = lc.compare({"golden_001": skills(("sql", "required"))},
                   {"golden_001": skills(("sql", "required"), ("python", "required"))})
    assert (s["tp"], s["fp"], s["fn"]) == (1, 1, 0)
    assert s["precision"] == 0.5


def test_a_confirmed_unsure_skill_is_scored_like_any_other_label(tmp_path, monkeypatch):
    """Once answered it counts normally: here the extractor missed it, so it is a miss."""
    run = write_run(
        tmp_path,
        merged={"golden_001": {"accepted_skills": [{"skill_id": "sql",
                                                    "requirement": "required"}]}},
        picks=[{"golden_id": "golden_001", "job_id": 11}],
        items=[unsure_item("golden_001", "python")],
        verdicts=["ok"])
    monkeypatch.setattr(lc, "LABELING_DIR", tmp_path)
    monkeypatch.setattr(lc, "DB", one_job_db(tmp_path, [(11, "sql", "required")]))
    s, r = lc.score_run(run.name)
    assert (s["tp"], s["fp"], s["fn"]) == (1, 0, 1)
    assert r.n_set_aside == 0


def test_a_posting_scored_only_because_of_a_confirmed_skill_is_no_longer_skipped(
        tmp_path, monkeypatch):
    run = write_run(
        tmp_path,
        merged={"golden_001": {"accepted_skills": []}},
        picks=[{"golden_id": "golden_001", "job_id": 11}],
        items=[unsure_item("golden_001", "python")],
        verdicts=["ok"])
    monkeypatch.setattr(lc, "LABELING_DIR", tmp_path)
    r = lc.load_run(run.name)
    assert r.skipped == []
    assert r.expected == {"golden_001": [{"skill_id": "python", "requirement": "required"}]}


def test_skills_set_aside_in_a_skipped_posting_are_not_counted_against_the_score(
        tmp_path, monkeypatch):
    """The first number is about postings that were scored, so the second must be too."""
    run = write_run(
        tmp_path,
        merged={"golden_001": {"accepted_skills": []}},
        picks=[{"golden_id": "golden_001", "job_id": 11}],
        items=[unsure_item("golden_001", "python")],
        verdicts=["?"])
    monkeypatch.setattr(lc, "LABELING_DIR", tmp_path)
    r = lc.load_run(run.name)
    assert r.skipped == ["golden_001"]
    assert r.set_aside == {"golden_001": {"python"}} and r.n_set_aside == 0


def test_a_run_without_its_queue_is_an_error_not_an_empty_queue(tmp_path, monkeypatch):
    """Reading a missing queue as "nothing unsure" would silently score the old way."""
    run = tmp_path / "20260101T000000Z_label"
    run.mkdir()
    (run / "merged.json").write_text(json.dumps({"golden_001": {"accepted_skills": []}}))
    (run / "picks.json").write_text(json.dumps([{"golden_id": "golden_001", "job_id": 11}]))
    monkeypatch.setattr(lc, "LABELING_DIR", tmp_path)
    with pytest.raises(FileNotFoundError):
        lc.load_run(run.name)


def test_one_sided_and_unfound_skills_are_untouched_by_the_rule():
    """Out of HIR-159's scope: only a skill both labellers found is set aside."""
    items = [{"golden_id": "golden_001", "kind": "skill", "key": "python",
              "reason": "disagreement",
              "a": {"skill_id": "python", "requirement": "required", "raw_text": "Python"},
              "b": None, "problems": []},
             {"golden_id": "golden_001", "kind": "attribute", "key": "degree",
              "reason": "uncertain", "a": {"degree": "bachelor"}, "b": {"degree": "bachelor"},
              "problems": []}]
    confirmed, set_aside, waiting = lc.unsure_rule(items, {1: "?", 2: "?"}, set())
    assert (confirmed, set_aside) == ({}, {})
    assert waiting == 2
