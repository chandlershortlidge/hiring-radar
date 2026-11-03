"""The eval gate's table (AGENTS.md "The eval gate", HIR-133).

What matters here is the gate, not the prose: a drop past 0.02 must be caught and named,
a metric present on one side only must never become a delta against zero, and the
baseline must come from git rather than from whatever happens to be in the working tree.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import eval_table  # noqa: E402


def summary(run_id="20261103T120000Z_dev_x2-abc", split="dev", extractor="x2-abc",
            taxonomy_version=8, **metrics):
    return {
        "meta": {"run_id": run_id, "split": split, "n_goldens": 20, "repeats": 3,
                 "model": "claude-sonnet-5-5", "extractor_version": extractor,
                 "taxonomy_version": taxonomy_version},
        "aggregate": {k: {"mean": v, "min": v, "max": v, "n": 3} for k, v in metrics.items()},
    }


# ---------------------------------------------------------------- compare


def test_delta_is_current_minus_baseline():
    rows = compare_one(current=0.90, baseline=0.88)
    assert rows[0]["delta"] == pytest.approx(0.02)

    rows = compare_one(current=0.85, baseline=0.90)
    assert rows[0]["delta"] == pytest.approx(-0.05)


def compare_one(current, baseline):
    return eval_table.compare(summary(f1=current), summary(f1=baseline))


def test_metric_order_follows_the_current_run():
    rows = eval_table.compare(
        summary(precision=0.8, recall=0.9, f1=0.85),
        summary(f1=0.80, recall=0.9, precision=0.8),
    )
    assert [r["metric"] for r in rows] == ["precision", "recall", "f1"]


def test_metric_only_the_baseline_had_still_appears_with_no_delta():
    """A metric dropped from the suite must not silently leave the gate."""
    rows = eval_table.compare(summary(f1=0.9), summary(f1=0.9, top10_overlap=0.8))
    dropped = [r for r in rows if r["metric"] == "top10_overlap"]
    assert dropped and dropped[0]["current"] is None
    assert dropped[0]["baseline"] == 0.8
    assert dropped[0]["delta"] is None


def test_new_metric_has_no_delta_rather_than_a_delta_against_zero():
    rows = eval_table.compare(summary(f1=0.9, brand_new=0.5), summary(f1=0.9))
    new = [r for r in rows if r["metric"] == "brand_new"][0]
    assert new["baseline"] is None and new["delta"] is None
    assert eval_table.regressions(rows) == []


def test_no_baseline_leaves_every_delta_empty():
    rows = eval_table.compare(summary(f1=0.9, precision=0.8), None)
    assert all(r["baseline"] is None and r["delta"] is None for r in rows)


# ---------------------------------------------------------------- the stop line


def test_drop_past_the_stop_line_is_a_regression():
    rows = eval_table.compare(summary(f1=0.87), summary(f1=0.90))
    assert [r["metric"] for r in eval_table.regressions(rows)] == ["f1"]


def test_drop_of_exactly_the_stop_line_is_not_more_than_it():
    """AGENTS.md says "down more than 0.02", so 0.02 itself passes."""
    rows = eval_table.compare(summary(f1=0.88), summary(f1=0.90))
    assert eval_table.regressions(rows) == []


def test_a_rise_is_never_a_regression():
    rows = eval_table.compare(summary(f1=0.99), summary(f1=0.50))
    assert eval_table.regressions(rows) == []


def test_every_metric_is_gated_not_just_the_headline_ones():
    rows = eval_table.compare(
        summary(f1=0.90, degree_accuracy=0.60),
        summary(f1=0.90, degree_accuracy=0.95),
    )
    assert [r["metric"] for r in eval_table.regressions(rows)] == ["degree_accuracy"]


# ---------------------------------------------------------------- render


def test_table_names_the_regressed_metric_and_says_do_not_merge():
    cur, base = summary(f1=0.85), summary(f1=0.95, run_id="20261101T100707Z_dev_x2-old",
                                          extractor="x2-old", taxonomy_version=5)
    out = eval_table.render(eval_table.compare(cur, base), cur, base)
    assert "do not merge" in out
    assert "f1 (-0.100)" in out
    assert "Needs Chandler" in out


def test_clean_table_says_so_and_shows_both_run_ids():
    cur = summary(f1=0.9251, run_id="20261103T120000Z_dev_x2-new", extractor="x2-new")
    base = summary(f1=0.9237, run_id="20261101T100707Z_dev_x2-old", extractor="x2-old",
                   taxonomy_version=5)
    out = eval_table.render(eval_table.compare(cur, base), cur, base)
    assert "No metric down more than 0.02" in out
    assert "do not merge" not in out
    assert "20261103T120000Z_dev_x2-new" in out and "20261101T100707Z_dev_x2-old" in out
    assert "skill list v8" in out and "skill list v5" in out
    assert "| f1 | 0.924 | 0.925 | +0.001 |" in out


def test_first_ever_run_renders_without_deltas():
    cur = summary(f1=0.9)
    out = eval_table.render(eval_table.compare(cur, None), cur, None)
    assert "becomes the first baseline" in out
    assert "Δ" not in out


def test_an_unchanged_metric_reads_as_zero_not_as_a_rounding_sign():
    cur, base = summary(f1=0.9), summary(f1=0.9)
    out = eval_table.render(eval_table.compare(cur, base), cur, base)
    assert "±0.000" in out


# ---------------------------------------------------------------- baseline from git


@pytest.fixture
def repo(tmp_path):
    """A git repo holding two committed dev runs, one held-out run, and one uncommitted."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)

    def write(run_id, **kw):
        d = tmp_path / "evals/results" / run_id
        d.mkdir(parents=True)
        (d / "summary.json").write_text(json.dumps(summary(run_id=run_id, **kw)))

    write("20261016T084520Z_dev_x2-first", extractor="x2-first", f1=0.80)
    write("20261101T100707Z_dev_x2-latest", extractor="x2-latest", f1=0.92)
    write("20261102T100707Z_heldout_x2-latest", split="heldout", f1=0.99)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "runs"], cwd=tmp_path, check=True)

    write("20261103T120000Z_dev_x2-uncommitted", extractor="x2-new", f1=0.93)
    return tmp_path


def test_baseline_is_the_newest_committed_dev_run(repo):
    base = eval_table.load_baseline(repo)
    assert base["meta"]["run_id"] == "20261101T100707Z_dev_x2-latest"


def test_an_uncommitted_run_is_not_a_baseline(repo):
    """It has to be something the next branch will also see."""
    ids = [p.parent.name for p in eval_table.committed_dev_summaries(repo)]
    assert "20261103T120000Z_dev_x2-uncommitted" not in ids


def test_heldout_runs_are_never_the_baseline(repo):
    ids = [p.parent.name for p in eval_table.committed_dev_summaries(repo)]
    assert all("heldout" not in i for i in ids)


def test_the_run_being_reported_is_excluded_from_its_own_baseline(repo):
    """The gate commits the run in the same PR, so by table-building time it may already
    be committed — comparing it with itself would show every delta as zero."""
    base = eval_table.load_baseline(repo, exclude_run_id="20261101T100707Z_dev_x2-latest")
    assert base["meta"]["run_id"] == "20261016T084520Z_dev_x2-first"


def test_no_committed_dev_run_gives_no_baseline(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    assert eval_table.load_baseline(tmp_path) is None


# ---------------------------------------------------------------- CLI


def test_heldout_run_is_refused(repo, monkeypatch):
    monkeypatch.setattr(eval_table, "ROOT", repo)
    with pytest.raises(SystemExit, match="held-out is release-only"):
        eval_table.main([str(repo / "evals/results/20261102T100707Z_heldout_x2-latest")])


def test_exit_code_is_nonzero_on_a_regression(repo, monkeypatch, capsys):
    monkeypatch.setattr(eval_table, "ROOT", repo)
    bad = repo / "evals/results/20261103T120000Z_dev_x2-regressed"
    bad.mkdir(parents=True)
    (bad / "summary.json").write_text(json.dumps(
        summary(run_id=bad.name, extractor="x2-bad", f1=0.80)))

    assert eval_table.main([str(bad)]) == 1
    assert "do not merge" in capsys.readouterr().out


def test_exit_code_is_zero_on_a_clean_run(repo, monkeypatch, capsys):
    monkeypatch.setattr(eval_table, "ROOT", repo)
    good = repo / "evals/results/20261103T120000Z_dev_x2-uncommitted"
    assert eval_table.main([str(good)]) == 0
    assert "No metric down more than 0.02" in capsys.readouterr().out


def test_a_run_id_resolves_as_well_as_a_path(repo):
    p = eval_table.resolve_run("20261101T100707Z_dev_x2-latest", repo)
    assert p == repo / "evals/results/20261101T100707Z_dev_x2-latest/summary.json"


def test_an_unknown_run_says_so(repo):
    with pytest.raises(SystemExit, match="no summary.json"):
        eval_table.resolve_run("nope", repo)


# ---------------------------------------------------------------- the exemption


def test_version_check_matches_when_the_baseline_measured_this_extractor(repo, monkeypatch):
    """The exemption: same extractor_version means the committed baseline already scored
    this exact prompt, schema, model and skill list, so a run cannot say anything new."""
    monkeypatch.setattr(eval_table, "load_baseline",
                        lambda root=None: summary(extractor="x2-latest"))
    monkeypatch.setitem(sys.modules, "app.extract", _fake_extract("x2-latest"))
    current, baseline, measured = eval_table.version_check(ROOT)
    assert current == "x2-latest" and measured is True


def test_version_check_differs_when_the_extractor_moved(repo, monkeypatch):
    monkeypatch.setattr(eval_table, "load_baseline",
                        lambda root=None: summary(extractor="x2-old"))
    monkeypatch.setitem(sys.modules, "app.extract", _fake_extract("x2-new"))
    current, baseline, measured = eval_table.version_check(ROOT)
    assert current == "x2-new" and measured is False


def test_version_check_with_no_baseline_never_exempts(monkeypatch):
    monkeypatch.setattr(eval_table, "load_baseline", lambda root=None: None)
    monkeypatch.setitem(sys.modules, "app.extract", _fake_extract("x2-new"))
    _, baseline, measured = eval_table.version_check(ROOT)
    assert baseline is None and measured is False


def _fake_extract(version):
    import types
    m = types.ModuleType("app.extract")
    m.DEFAULT_MODEL = "claude-sonnet-5-5"
    m.extractor_version = lambda tax, model: version
    return m
