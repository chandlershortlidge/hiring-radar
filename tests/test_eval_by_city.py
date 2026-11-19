"""Tests for scripts/eval_by_city.py — the per-city split of one eval run (HIR-348)."""

import collections
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("eval_by_city", ROOT / "scripts" / "eval_by_city.py")
ebc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ebc)


def _row(gid, tp=(), fp=(), fn=(), seniority=None, german=None, degree=None):
    return {"golden_id": gid, "tp": list(tp), "fp": list(fp), "fn": list(fn),
            "seniority": seniority, "german": german, "degree": degree}


def _key(gid, **fields):
    return {"id": gid, "split": "dev", **fields}


def test_skill_rates_are_pooled_per_city():
    rows = [_row("golden_001", tp=["python", "sql"], fp=["aws"]),
            _row("golden_002", tp=["python"], fn=["rag"]),
            _row("golden_003", tp=["go"], fp=["rust"], fn=["java"])]
    city = {"golden_001": "Hamburg", "golden_002": "Hamburg", "golden_003": "Berlin"}
    agg, seen = ebc.tally(rows, city, {})

    assert seen == {"Hamburg": {"golden_001", "golden_002"}, "Berlin": {"golden_003"}}
    p, r, f1 = ebc.prf(agg["Hamburg"])
    assert p == 3 / 4 and r == 3 / 4 and f1 == 0.75
    p, r, _ = ebc.prf(agg["Berlin"])
    assert p == 0.5 and r == 0.5


def test_a_posting_with_no_city_is_reported_as_not_recorded():
    agg, seen = ebc.tally([_row("golden_009", tp=["python"])], {}, {})
    assert set(seen) == {ebc.NOT_RECORDED}
    assert agg[ebc.NOT_RECORDED]["tp"] == 1


def test_repeats_of_one_posting_count_once_as_a_key_but_pool_their_rates():
    """A run measures each posting three times; that is one answer key, three rows."""
    rows = [_row("golden_001", tp=["python"], fp=["aws"]),
            _row("golden_001", tp=["python"]),
            _row("golden_001", tp=["python"])]
    agg, seen = ebc.tally(rows, {"golden_001": "Munich"}, {})
    assert len(seen["Munich"]) == 1
    p, r, _ = ebc.prf(agg["Munich"])
    assert p == 3 / 4 and r == 1.0


def test_attributes_use_the_evals_own_comparison():
    """Degree counts the "or equivalent" flag too, as the headline score does, so a right
    level with the wrong flag is a miss."""
    keys = {"golden_001": _key("golden_001", seniority="senior", german="required",
                               degree="bachelor", degree_or_equivalent=True)}
    right = _row("golden_001", seniority={"level": "senior"},
                 german={"requirement": "required"},
                 degree={"level": "bachelor", "or_equivalent": True})
    agg, _ = ebc.tally([right], {"golden_001": "Hamburg"}, keys)
    for metric in ebc.METRICS:
        assert agg["Hamburg"][f"{metric}_ok"] == 1, metric

    flag_wrong = _row("golden_001", seniority={"level": "mid"},
                      german={"requirement": "required"},
                      degree={"level": "bachelor", "or_equivalent": False})
    agg, _ = ebc.tally([flag_wrong], {"golden_001": "Hamburg"}, keys)
    a = agg["Hamburg"]
    assert a["degree_accuracy_ok"] == 0 and a["degree_accuracy_n"] == 1
    assert a["seniority_accuracy_ok"] == 0
    assert a["german_accuracy_ok"] == 1


def test_an_attribute_the_key_does_not_carry_is_outside_the_denominator():
    keys = {"golden_001": _key("golden_001", german="required")}
    rows = [_row("golden_001", german={"requirement": "required"},
                 seniority={"level": "senior"}, degree={"level": "phd"})]
    agg, _ = ebc.tally(rows, {"golden_001": "Hamburg"}, keys)
    a = agg["Hamburg"]
    assert a["german_accuracy_n"] == 1
    assert a["seniority_accuracy_n"] == 0 and a["degree_accuracy_n"] == 0


def test_the_bottom_row_pools_every_city():
    rows = [_row("golden_001", tp=["python"], fp=["aws"]),
            _row("golden_002", tp=["sql"], fn=["rag"])]
    city = {"golden_001": "Hamburg", "golden_002": "Berlin"}
    agg, seen = ebc.tally(rows, city, {})
    lines = ebc.render(agg, seen)

    assert lines[0].startswith("city")
    assert lines[-1].startswith("all of them")
    assert "    2" in lines[-1]            # two answer keys over both cities
    total = collections.Counter()
    for a in agg.values():
        total.update(a)
    p, r, _ = ebc.prf(total)
    assert f"{p:.3f}" in lines[-1] and f"{r:.3f}" in lines[-1]


def test_cities_come_from_the_labelling_runs_picks(tmp_path, monkeypatch):
    runs = tmp_path / "labeling"
    (runs / "20261108T182552Z_label").mkdir(parents=True)
    (runs / "20261108T182552Z_label" / "picks.json").write_text(json.dumps(
        [{"golden_id": "golden_107", "place": "Hamburg"},
         {"golden_id": "golden_108", "place": None}]))
    monkeypatch.setattr(ebc, "RUNS", runs)

    assert ebc.cities() == {"golden_107": "Hamburg", "golden_108": ebc.NOT_RECORDED}
