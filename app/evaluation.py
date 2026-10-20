"""Score extractions against Goldens and run the eval suite.

Does: per-Golden set comparison on skill ids, micro-averaged precision/recall/F1,
requirement accuracy on matched skills, seniority accuracy over Goldens that carry a
seniority label, and rank agreement between predicted and gold
skill frequencies across the suite (the chart is a frequency ranking, so we measure it
directly). Runs a suite N times and summarizes mean and spread.

Does NOT: call a model itself (an extract function is injected), read files, or score
anything the chart doesn't use (no non-skill audit, no alternative groups).

Invariants: micro-averaging (every skill criterion weighs the same, regardless of JD
length); scoring is deterministic for a given input; a Golden whose extraction raised
counts as an error and contributes all its expected skills as misses.
"""

import statistics
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class GoldenScore:
    golden_id: str
    tp: list[str]
    fp: list[str]
    fn: list[str]
    requirement_matches: int
    error: str | None = None
    seniority_expected: str | None = None   # None is a label ("no usable signal") when seniority_labeled
    seniority_predicted: str | None = None
    seniority_labeled: bool = False         # the Golden carries a seniority key; only then is it scored
    # German and degree: scored whenever the Golden carries the key, so "not mentioned"
    # (None) is a label like any other. Each is a tuple so a mismatch in any part counts.
    german: tuple | None = None             # (expected, predicted) or None = unlabeled
    degree: tuple | None = None             # ((level, or_equivalent), (level, or_equivalent)) or None


def score_golden(golden_id: str, expected: list[dict], predicted: list[dict],
                 seniority_expected: str | None = None, seniority_predicted: str | None = None,
                 german: tuple | None = None, degree: tuple | None = None,
                 seniority_labeled: bool | None = None) -> GoldenScore:
    exp = {e["skill_id"]: e["requirement"] for e in expected}
    pred = {p["skill_id"]: p["requirement"] for p in predicted}
    tp = sorted(exp.keys() & pred.keys())
    return GoldenScore(
        golden_id=golden_id,
        tp=tp,
        fp=sorted(pred.keys() - exp.keys()),
        fn=sorted(exp.keys() - pred.keys()),
        requirement_matches=sum(1 for s in tp if exp[s] == pred[s]),
        seniority_expected=seniority_expected,
        seniority_predicted=seniority_predicted,
        seniority_labeled=seniority_expected is not None if seniority_labeled is None else seniority_labeled,
        german=german,
        degree=degree,
    )


def _rank(values: list[float]) -> list[float]:
    """Average ranks (1 = largest), ties share the mean rank."""
    order = sorted(range(len(values)), key=lambda i: -values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        mean = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = mean
        i = j + 1
    return ranks


def spearman(a: list[float], b: list[float]) -> float | None:
    if len(a) != len(b) or len(a) < 2:
        return None
    ra, rb = _rank(a), _rank(b)
    ma, mb = statistics.fmean(ra), statistics.fmean(rb)
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    va = sum((x - ma) ** 2 for x in ra)
    vb = sum((y - mb) ** 2 for y in rb)
    if va == 0 or vb == 0:
        return None
    return cov / (va * vb) ** 0.5


def top_k(freq: Counter, k: int) -> list[str]:
    return [s for s, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:k]]


def summarize(scores: list[GoldenScore], expected_by_id: dict[str, list[dict]],
              predicted_by_id: dict[str, list[dict]], k: int = 10) -> dict:
    tp = sum(len(s.tp) for s in scores)
    fp = sum(len(s.fp) for s in scores)
    fn = sum(len(s.fn) for s in scores)
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = (2 * precision * recall / (precision + recall)) if precision and recall else None
    req_acc = sum(s.requirement_matches for s in scores) / tp if tp else None
    labeled = [s for s in scores if s.seniority_labeled]
    sen_acc = (sum(1 for s in labeled if s.seniority_predicted == s.seniority_expected) / len(labeled)
               if labeled else None)

    ger = [s.german for s in scores if s.german is not None]
    ger_acc = sum(1 for e, p in ger if e == p) / len(ger) if ger else None
    deg = [s.degree for s in scores if s.degree is not None]
    deg_acc = sum(1 for e, p in deg if e == p) / len(deg) if deg else None

    gold_freq = Counter(e["skill_id"] for es in expected_by_id.values() for e in es)
    pred_freq = Counter(p["skill_id"] for ps in predicted_by_id.values() for p in ps)
    universe = sorted(gold_freq.keys() | pred_freq.keys())
    rho = spearman([gold_freq[s] for s in universe], [pred_freq[s] for s in universe])
    gold_top, pred_top = top_k(gold_freq, k), top_k(pred_freq, k)

    return {
        "n_goldens": len(scores),
        "n_errors": sum(1 for s in scores if s.error),
        "tp": tp, "fp": fp, "fn": fn,
        "precision": precision, "recall": recall, "f1": f1,
        "requirement_accuracy": req_acc,
        "seniority_accuracy": sen_acc,
        "seniority_n": len(labeled),
        "german_accuracy": ger_acc, "german_n": len(ger),
        "degree_accuracy": deg_acc, "degree_n": len(deg),
        "rank_spearman": rho,
        f"top{k}_overlap": len(set(gold_top) & set(pred_top)) / k if gold_top else None,
        "gold_top": gold_top, "pred_top": pred_top,
    }


@dataclass
class RunResult:
    summary: dict
    scores: list[GoldenScore]
    predictions: dict[str, dict] = field(default_factory=dict)


def run_once(goldens: list[dict], extract_fn) -> RunResult:
    """extract_fn(jd_text) -> Extraction-like object with .mentions/.proposed/.rejected."""
    scores, predicted_by_id, predictions = [], {}, {}
    expected_by_id = {g["id"]: g["expected"] for g in goldens}
    for g in goldens:
        try:
            ex = extract_fn(g["job_description"])
            pred = [{"skill_id": m.skill_id, "requirement": m.requirement, "raw_text": m.raw_text} for m in ex.mentions]
            sen = getattr(ex, "seniority", None)
            ger = getattr(ex, "german", None)
            deg = getattr(ex, "degree", None)
            predictions[g["id"]] = {
                "mentions": pred,
                "proposed": [vars(p) for p in ex.proposed],
                "rejected": ex.rejected,
                "seniority": vars(sen) if sen else None,
                "german": vars(ger) if ger else None,
                "degree": vars(deg) if deg else None,
                "usage": getattr(ex, "usage", {}),
            }
            s = score_golden(g["id"], g["expected"], pred,
                             seniority_expected=g.get("seniority"),
                             seniority_predicted=sen.level if sen else None,
                             seniority_labeled="seniority" in g,
                             german=(g["german"], ger.requirement if ger else None) if "german" in g else None,
                             degree=((g["degree"], bool(g.get("degree_or_equivalent"))),
                                     (deg.level, deg.or_equivalent) if deg else (None, False)) if "degree" in g else None)
        except Exception as e:  # one bad Golden must not hide the rest of the run
            pred = []
            predictions[g["id"]] = {"error": f"{type(e).__name__}: {e}"}
            s = GoldenScore(g["id"], [], [], sorted(x["skill_id"] for x in g["expected"]), 0, error=str(e),
                            seniority_expected=g.get("seniority"), seniority_labeled="seniority" in g,
                            german=(g["german"], None) if "german" in g else None,
                            degree=((g["degree"], bool(g.get("degree_or_equivalent"))), (None, False)) if "degree" in g else None)
        predicted_by_id[g["id"]] = pred
        scores.append(s)
    return RunResult(summarize(scores, expected_by_id, predicted_by_id), scores, predictions)


METRICS = ("precision", "recall", "f1", "requirement_accuracy", "seniority_accuracy", "german_accuracy", "degree_accuracy",
           "rank_spearman", "top10_overlap")


def across_runs(runs: list[RunResult]) -> dict:
    out = {}
    for m in METRICS:
        vals = [r.summary[m] for r in runs if r.summary.get(m) is not None]
        out[m] = {
            "mean": statistics.fmean(vals) if vals else None,
            "min": min(vals) if vals else None,
            "max": max(vals) if vals else None,
            "n": len(vals),
        }
    return out
