from collections import Counter
from types import SimpleNamespace

import pytest

from app import evaluation as ev
from app.extract import Mention


def e(sid, req="required"):
    return {"skill_id": sid, "requirement": req}


def test_score_golden_sets_and_requirement_matches():
    s = ev.score_golden("g", [e("a"), e("b", "nice_to_have"), e("c")], [e("a"), e("b"), e("d")])
    assert (s.tp, s.fp, s.fn) == (["a", "b"], ["d"], ["c"])
    assert s.requirement_matches == 1  # b disagrees


def test_summary_is_micro_averaged():
    # Golden 1: 1/1 right. Golden 2: 1 of 9 right. Macro recall would be ~0.56; micro is 2/10.
    g1 = ev.score_golden("g1", [e("a")], [e("a")])
    g2 = ev.score_golden("g2", [e(x) for x in "bcdefghij"], [e("b")])
    s = ev.summarize([g1, g2], {"g1": [e("a")], "g2": [e(x) for x in "bcdefghij"]},
                     {"g1": [e("a")], "g2": [e("b")]})
    assert s["recall"] == pytest.approx(0.2)
    assert s["precision"] == 1.0


def test_spearman_known_values():
    assert ev.spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert ev.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)
    assert ev.spearman([1, 1, 1], [1, 2, 3]) is None  # no variance
    assert ev.spearman([1], [1]) is None


def test_ranks_average_ties():
    assert ev._rank([5, 3, 3, 1]) == [1.0, 2.5, 2.5, 4.0]


def test_top_k_breaks_ties_alphabetically():
    assert ev.top_k(Counter({"b": 2, "a": 2, "c": 1}), 2) == ["a", "b"]


def _extraction(ids):
    return SimpleNamespace(mentions=[Mention(i, "required", i) for i in ids], proposed=[], rejected=[], usage={})


def test_run_once_counts_errors_as_misses_and_keeps_going():
    goldens = [
        {"id": "g1", "job_description": "one", "expected": [e("a"), e("b")]},
        {"id": "g2", "job_description": "two", "expected": [e("c")]},
    ]

    def fake(text):
        if text == "one":
            raise RuntimeError("boom")
        return _extraction(["c"])

    r = ev.run_once(goldens, fake)
    assert r.summary["n_errors"] == 1
    assert r.summary["tp"] == 1 and r.summary["fn"] == 2
    assert "boom" in r.predictions["g1"]["error"]


def test_perfect_extractor_scores_one_everywhere():
    goldens = [{"id": f"g{i}", "job_description": str(i), "expected": [e(x) for x in ids]}
               for i, ids in enumerate([["a", "b"], ["a", "c"], ["a", "b", "d"]])]
    lookup = {g["job_description"]: [x["skill_id"] for x in g["expected"]] for g in goldens}
    r = ev.run_once(goldens, lambda t: _extraction(lookup[t]))
    s = r.summary
    assert s["precision"] == s["recall"] == s["f1"] == s["requirement_accuracy"] == 1.0
    assert s["rank_spearman"] == pytest.approx(1.0)


def test_across_runs_reports_mean_and_spread():
    runs = [SimpleNamespace(summary={m: v for m in ev.METRICS}) for v in (0.8, 0.9, 1.0)]
    agg = ev.across_runs(runs)
    assert agg["recall"] == {"mean": pytest.approx(0.9), "min": 0.8, "max": 1.0, "n": 3}


def test_seniority_accuracy_counts_only_labeled_goldens():
    goldens = [
        {"id": "g1", "job_description": "a", "expected": [e("a")], "seniority": "junior"},
        {"id": "g2", "job_description": "b", "expected": [e("b")], "seniority": "senior"},
        {"id": "g3", "job_description": "c", "expected": [e("c")]},  # unlabeled
    ]
    from app.extract import Seniority
    levels = {"a": "junior", "b": "mid", "c": "senior"}

    def fake(text):
        x = _extraction([text])
        x.seniority = Seniority(levels[text], "inferred", None)
        return x

    s = ev.run_once(goldens, fake).summary
    assert s["seniority_n"] == 2 and s["seniority_accuracy"] == pytest.approx(0.5)


def test_seniority_accuracy_is_none_when_nothing_is_labeled():
    goldens = [{"id": "g1", "job_description": "a", "expected": [e("a")]}]
    s = ev.run_once(goldens, lambda t: _extraction(["a"])).summary
    assert s["seniority_accuracy"] is None and s["seniority_n"] == 0
