"""Tests for scripts/eval_cost.py — what one eval run cost per reading (HIR-223)."""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("eval_cost", ROOT / "scripts" / "eval_cost.py")
ec = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ec)


def _usage(inp=0, read=0, write=0, out=0):
    return {"input_tokens": inp, "cache_read_input_tokens": read,
            "cache_creation_input_tokens": write, "output_tokens": out}


def _write_run(tmp_path, model, rows, run_id="20261119T000000Z_dev_x2-test"):
    d = tmp_path / "evals/results" / run_id
    d.mkdir(parents=True)
    (d / "summary.json").write_text(json.dumps(
        {"meta": {"run_id": run_id, "model": model, "split": "dev"}}))
    with (d / "predictions.jsonl").open("w") as f:
        for i, usage in enumerate(rows, 1):
            f.write(json.dumps({"run": 1, "golden_id": f"golden_{i:03d}", "usage": usage}) + "\n")
    return d


def test_cost_follows_the_published_prices_per_token_kind():
    """Ten thousand tokens of one kind is a thousandth of the published per-million price.

    The amounts are deliberately small: a million input tokens in one request would be
    over Claude Haiku 5.5's 100,000-token step and so billed in its higher band, which the
    next test covers. Here each reading stays in the ordinary band for both models.
    """
    assert ec.cost_of("claude-sonnet-5-5", _usage(inp=10_000)) == 2.00 / 100
    assert ec.cost_of("claude-haiku-5-5", _usage(inp=10_000)) == 0.10 / 100

    assert ec.cost_of("claude-sonnet-5-5", _usage(out=10_000)) == 10.00 / 100
    assert ec.cost_of("claude-haiku-5-5", _usage(out=10_000)) == 0.50 / 100

    # Cache reads are the cheap kind and cache writes the dear one; a run that reads the
    # cached prompt instead of writing it is most of why a reading is cheap at all.
    assert ec.cost_of("claude-sonnet-5-5", _usage(read=10_000)) == 0.10 / 100
    assert ec.cost_of("claude-sonnet-5-5", _usage(write=10_000)) == 2.50 / 100
    assert ec.cost_of("claude-haiku-5-5", _usage(read=10_000)) == 0.01 / 100
    assert ec.cost_of("claude-haiku-5-5", _usage(write=10_000)) == 0.125 / 100


def test_a_haiku_prompt_over_100k_tokens_is_billed_in_the_higher_band():
    """Claude Haiku 5.5's prices step up past 100,000 input tokens in one request, and the
    prompt counts cache reads too — so a mostly-cached long prompt still pays the step."""
    under = _usage(inp=50_000, out=1_000)
    over = _usage(inp=50_000, read=60_000, out=1_000)

    assert ec.price_for("claude-haiku-5-5", under)["input"] == 0.10
    assert ec.price_for("claude-haiku-5-5", over)["input"] == 0.50
    assert ec.cost_of("claude-haiku-5-5", over) > 5 * ec.cost_of("claude-haiku-5-5", under)

    # Sonnet has one band, so the same reading is priced the same either side of 100k.
    assert ec.price_for("claude-sonnet-5-5", over) == ec.price_for("claude-sonnet-5-5", under)


def test_an_unknown_model_reports_no_cost_rather_than_a_guess():
    assert ec.cost_of("claude-made-up-9", _usage(inp=1_000)) is None
    assert ec.fmt_cost(None) == "unknown price"


def test_a_reading_that_errored_is_left_out_of_the_mean(tmp_path):
    """An errored reading has no usage; counting it as zero would make the model look
    cheaper per reading than it is."""
    d = tmp_path / "evals/results/20261119T000000Z_dev_x2-test"
    d.mkdir(parents=True)
    (d / "summary.json").write_text(json.dumps({"meta": {"run_id": "r", "model": "claude-haiku-5-5"}}))
    with (d / "predictions.jsonl").open("w") as f:
        f.write(json.dumps({"golden_id": "golden_001", "usage": _usage(inp=1000, out=100)}) + "\n")
        f.write(json.dumps({"golden_id": "golden_002", "error": "boom"}) + "\n")

    s = ec.summarize(d)
    assert s["n_readings"] == 1
    assert s["means"]["input_tokens"] == 1000


def test_summarize_counts_readings_and_the_largest_prompt(tmp_path):
    d = _write_run(tmp_path, "claude-haiku-5-5",
                   [_usage(inp=10_000, out=500), _usage(inp=30_000, read=5_000, out=700)])
    s = ec.summarize(d)

    assert s["model"] == "claude-haiku-5-5"
    assert s["n_readings"] == 2
    assert s["means"]["input_tokens"] == 20_000
    assert s["max_prompt_tokens"] == 35_000
    assert s["over_long_band"] == 0
    assert s["cost_per_reading"] == s["total_cost"] / 2


def test_the_table_names_both_runs_and_says_the_prompts_stayed_under_the_band(tmp_path):
    a = _write_run(tmp_path, "claude-sonnet-5-5", [_usage(inp=10_000, out=500)],
                   run_id="20261119T000000Z_dev_x2-sonnet")
    b = _write_run(tmp_path, "claude-haiku-5-5", [_usage(inp=10_000, out=500)],
                   run_id="20261119T000001Z_dev_x2-haiku")
    out = ec.render([ec.summarize(a), ec.summarize(b)])

    assert "claude-sonnet-5-5" in out and "claude-haiku-5-5" in out
    assert "every prompt stayed under 100,000 tokens" in out
    assert "20261119T000000Z_dev_x2-sonnet" in out
