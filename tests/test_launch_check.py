"""launch_check: scoring the labeller panel's agreed labels against the stored extraction.

The arithmetic only — `compare` is pure, so none of this needs a database or a run
directory. Nothing here calls a model.
"""

import importlib.util
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


def test_per_posting_splits_precision_into_its_two_sides():
    """Agreed labels and extras are reported apart, so a shorter yardstick is visible."""
    expected = {"g1": skills(("python", "required"), ("sql", "required")),
                "g2": skills(("rag", "required"), ("pytorch", "required"))}
    predicted = {"g1": skills(("python", "required"), ("sql", "required"),
                              ("kubernetes", "required")),
                 "g2": skills(("rag", "required"), ("pytorch", "required"),
                              ("docker", "required"))}
    p = lc.per_posting(lc.compare(expected, predicted))
    assert p["n"] == 2
    assert p["agreed"] == pytest.approx(2.0)
    assert p["extras"] == pytest.approx(1.0)


def test_the_same_extras_on_fewer_agreed_labels_lowers_precision():
    """HIR-139: identical extractor behaviour scores worse where postings name fewer skills.

    Two cities, one unagreed extra per posting in both. The city with half the agreed
    labels scores lower precision, so the extras count — not precision — is what says
    whether the extractor behaved differently.
    """
    wordy = {"g1": skills(("python", "required"), ("sql", "required"),
                          ("rag", "required"), ("pytorch", "required"))}
    wordy_pred = {"g1": skills(("python", "required"), ("sql", "required"),
                               ("rag", "required"), ("pytorch", "required"),
                               ("kubernetes", "required"))}
    terse = {"g1": skills(("python", "required"), ("sql", "required"))}
    terse_pred = {"g1": skills(("python", "required"), ("sql", "required"),
                               ("kubernetes", "required"))}

    w, t = lc.compare(wordy, wordy_pred), lc.compare(terse, terse_pred)
    assert t["precision"] < w["precision"]                      # the gap the ticket chased
    assert lc.per_posting(w)["extras"] == lc.per_posting(t)["extras"] == 1.0   # behaviour is flat


def test_per_posting_on_nothing_scored_is_not_a_division_by_zero():
    p = lc.per_posting(lc.compare({}, {}))
    assert p == {"agreed": None, "extras": None, "n": 0}
    assert "no postings scored" in lc.per_posting_line("new city", lc.compare({}, {}))


def test_per_posting_line_reports_both_counts():
    s = lc.compare({"g1": skills(("python", "required"))},
                   {"g1": skills(("python", "required"), ("kubernetes", "required"))})
    assert lc.per_posting_line("new city", s) == (
        "new city: 1.0 agreed labels per posting, 1.0 unagreed extras per posting")


def test_load_run_skips_a_posting_the_panel_agreed_nothing_on(tmp_path, monkeypatch):
    """Nothing agreed is not the same as the extractor being wrong — it must not be scored."""
    import json

    run = tmp_path / "20260101T000000Z_label"
    (run / "raw").mkdir(parents=True)
    (run / "merged.json").write_text(json.dumps({
        "golden_001": {"accepted_skills": [{"skill_id": "python", "requirement": "required"}]},
        "golden_002": {"accepted_skills": []},
    }))
    (run / "picks.json").write_text(json.dumps([
        {"golden_id": "golden_001", "job_id": 11},
        {"golden_id": "golden_002", "job_id": 12},
    ]))
    monkeypatch.setattr(lc, "LABELING_DIR", tmp_path)
    expected, job_of, skipped = lc.load_run(run.name)
    assert list(expected) == ["golden_001"]
    assert skipped == ["golden_002"]
    assert job_of == {"golden_001": 11, "golden_002": 12}
