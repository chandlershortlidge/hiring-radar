"""Score extractions against Goldens and run the eval suite.

Does: per-Golden set comparison on skill ids, micro-averaged precision/recall/F1,
requirement accuracy on matched skills, the grounding check of app/grounding.py (every
quoted snippet the model offered as evidence really appears in the posting) turned into a
score, seniority accuracy over Goldens
that carry a seniority label, per-class precision/recall and a confusion matrix for production
experience (plus signal agreement, so a right class off the wrong clause shows), and rank
agreement between predicted and gold
skill frequencies across the suite (the chart is a frequency ranking, so we measure it
directly). Runs a suite N times and summarizes mean and spread.

Does NOT: call a model itself (an extract function is injected), read files, or score
anything the chart doesn't use (no non-skill audit). Alternative groups (HIR-251) are
scored, as pair agreement, on Goldens marked `groups_reviewed` only.

Invariants: micro-averaging (every skill criterion weighs the same, regardless of JD
length); scoring is deterministic for a given input; a Golden whose extraction raised
counts as an error and contributes all its expected skills as misses.
"""

import statistics
from collections import Counter
from contextlib import nullcontext
from dataclasses import dataclass, field

from app import grounding as _grounding


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
    # Production: same shape as German, plus the quoted signals so a right class reached
    # through the wrong clause is visible (HIR-69).
    production: tuple | None = None         # (expected, predicted) or None = unlabeled
    production_signal: tuple | None = None  # (expected_signal, predicted_signal)
    # Grounding (HIR-78): quoted evidence that is really in the posting, out of every quote
    # the model offered. Gold-independent — it asks whether the model invented its evidence,
    # not whether the skill was the right one, so it stays separate from fp/fn.
    grounded: int = 0
    quotes: int = 0
    # Alternative groups (HIR-251): (expected pairs, predicted pairs) of matched skills that
    # share a group, or None when the Golden's groups were never reviewed. Only reviewed
    # Goldens are scored, since an unreviewed one would call every predicted group wrong.
    group_pairs: tuple | None = None


def score_golden(golden_id: str, expected: list[dict], predicted: list[dict],
                 seniority_expected: str | None = None, seniority_predicted: str | None = None,
                 german: tuple | None = None, degree: tuple | None = None,
                 seniority_labeled: bool | None = None, production: tuple | None = None,
                 production_signal: tuple | None = None,
                 grounding: tuple[int, int] = (0, 0), groups_reviewed: bool = False) -> GoldenScore:
    exp = {e["skill_id"]: e["requirement"] for e in expected}
    pred = {p["skill_id"]: p["requirement"] for p in predicted}
    tp = sorted(exp.keys() & pred.keys())
    group_pairs = ((group_pairs_of(expected, tp), group_pairs_of(predicted, tp))
                   if groups_reviewed else None)
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
        production=production,
        production_signal=production_signal,
        grounded=grounding[0],
        quotes=grounding[1],
        group_pairs=group_pairs,
    )


def group_pairs_of(mentions: list[dict], among: list[str]) -> frozenset:
    """Unordered pairs of skills in `among` that share an alternative group in `mentions`.

    Pairs, not group numbers, because numbers are arbitrary per posting: what has to agree
    is which skills were offered as alternatives to each other. Restricted to skills both
    sides found, so a missed skill costs recall once, not again here."""
    keep = set(among)
    by_group: dict = {}
    for m in mentions:
        g = m.get("alternative_group")
        if g is not None and m["skill_id"] in keep:
            by_group.setdefault(g, set()).add(m["skill_id"])
    return frozenset((a, b) for ids in by_group.values() for a in ids for b in ids if a < b)


# The grounding check itself lives in app/grounding.py, below both callers, so the eval
# and the live poll cannot measure it differently (HIR-160). Re-exported here because
# `evaluation.grounding` and `evaluation.UNGROUNDED_REASON` are what the eval and its
# tests have always called.
grounding = _grounding.grounding
UNGROUNDED_REASON = _grounding.UNGROUNDED_REASON


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


PRODUCTION_CLASSES = ("required", "nice_to_have", None)


def _label(c: str | None) -> str:
    return c if c else "none"


def per_class(pairs: list[tuple]) -> dict:
    """Per-class precision/recall over (expected, predicted) pairs. None is a class of its
    own ("none"), not an abstention, so every Golden lands in exactly one row."""
    out = {}
    for c in PRODUCTION_CLASSES:
        tp = sum(1 for e, pr in pairs if e == c and pr == c)
        fp = sum(1 for e, pr in pairs if e != c and pr == c)
        fn = sum(1 for e, pr in pairs if e == c and pr != c)
        out[_label(c)] = {"support": tp + fn, "tp": tp, "fp": fp, "fn": fn,
                          "precision": tp / (tp + fp) if tp + fp else None,
                          "recall": tp / (tp + fn) if tp + fn else None}
    return out


def confusion(pairs: list[tuple]) -> dict:
    """{expected: {predicted: n}}, every cell present so an empty one reads as zero."""
    return {_label(e): {_label(pr): sum(1 for a, b in pairs if a == e and b == pr)
                        for pr in PRODUCTION_CLASSES} for e in PRODUCTION_CLASSES}


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
    prod = [s.production for s in scores if s.production is not None]
    prod_acc = sum(1 for e, p in prod if e == p) / len(prod) if prod else None
    # A right class off the wrong clause is not a win: count signal agreement separately,
    # over the Goldens where both sides set a class (HIR-69).
    sig = [s.production_signal for s in scores
           if s.production is not None and s.production[0] == s.production[1] and s.production[0] is not None]
    sig_ok = sum(1 for e, p in sig if e and p and (e in p or p in e)) if sig else 0

    reviewed = [s.group_pairs for s in scores if s.group_pairs is not None]
    g_tp = sum(len(e & p) for e, p in reviewed)
    g_fp = sum(len(p - e) for e, p in reviewed)
    g_fn = sum(len(e - p) for e, p in reviewed)
    group_f1 = 2 * g_tp / (2 * g_tp + g_fp + g_fn) if g_tp + g_fp + g_fn else None

    quotes = sum(s.quotes for s in scores)
    grounding_acc = sum(s.grounded for s in scores) / quotes if quotes else None

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
        "production_accuracy": prod_acc, "production_n": len(prod),
        "production_per_class": per_class(prod),
        "production_confusion": confusion(prod),
        "production_signal_agreement": sig_ok / len(sig) if sig else None,
        "production_signal_n": len(sig),
        "grounding_accuracy": grounding_acc,
        "grounding_n": quotes,
        "group_f1": group_f1,
        "group_n": len(reviewed),
        "rank_spearman": rho,
        f"top{k}_overlap": len(set(gold_top) & set(pred_top)) / k if gold_top else None,
        "gold_top": gold_top, "pred_top": pred_top,
    }


@dataclass
class RunResult:
    summary: dict
    scores: list[GoldenScore]
    predictions: dict[str, dict] = field(default_factory=dict)


# The four per-Golden attributes the eval gate counts flips on (HIR-164). Each is one
# yes/no answer per Golden, so on a small dev set one Golden is a large slice of the score
# and a fractional threshold cannot separate noise from a regression. The skill scores pool
# hundreds of mentions and keep the 0.02 rule. See DECISIONS 2026-11-04 (HIR-164).
ATTRIBUTE_METRICS = ("seniority_accuracy", "german_accuracy", "degree_accuracy",
                     "production_accuracy")

# metric name -> the GoldenScore/attribute_pairs key holding its (expected, predicted) pair
_PAIR_OF = {"german_accuracy": "german", "degree_accuracy": "degree",
            "production_accuracy": "production"}


def attribute_pairs(g: dict, prediction: dict) -> dict:
    """The expected/predicted attribute arguments for one Golden, off a stored prediction.

    Returns exactly the attribute keyword arguments `score_golden` takes. The live run and
    anything that re-reads `predictions.jsonl` later both go through here, so the eval gate's
    flip counts and the run's own accuracies can never drift apart (HIR-164) — a gate that
    compared attributes by its own slightly different rules could stop a PR the run called
    clean. `prediction` is the dict `_score_one` stores, including the `{"error": ...}` form,
    where every predicted side is absent and reads as "said nothing".
    """
    sen = prediction.get("seniority") or {}
    ger = prediction.get("german") or {}
    deg = prediction.get("degree") or None
    prod = prediction.get("production") or {}
    return {
        "seniority_expected": g.get("seniority"),
        "seniority_predicted": sen.get("level"),
        "seniority_labeled": "seniority" in g,
        "german": (g["german"], ger.get("requirement")) if "german" in g else None,
        "degree": ((g["degree"], bool(g.get("degree_or_equivalent"))),
                   (deg.get("level"), deg.get("or_equivalent")) if deg else (None, False)
                   ) if "degree" in g else None,
        "production": (g["production"], prod.get("requirement")) if "production" in g else None,
        "production_signal": (g.get("production_signal"), prod.get("signal")) if "production" in g else None,
    }


def attribute_hits(g: dict, prediction: dict) -> dict[str, bool | None]:
    """Per-attribute correctness for one Golden: True, False, or None when not scored.

    None means the Golden does not carry that attribute, so it is outside the metric's
    denominator — never counted as a miss, and never as a flip.
    """
    p = attribute_pairs(g, prediction)
    hits: dict[str, bool | None] = {
        "seniority_accuracy": (p["seniority_predicted"] == p["seniority_expected"])
        if p["seniority_labeled"] else None,
    }
    for metric, key in _PAIR_OF.items():
        pair = p[key]
        hits[metric] = None if pair is None else pair[0] == pair[1]
    return hits


def _score_one(g: dict, extract_fn, span):
    """One Golden: extract, score, report. Returns (predicted_mentions, prediction, score).

    A Golden whose extraction raises is scored as a total miss and reported as an error,
    so one bad posting cannot hide the rest of the run.
    """
    try:
        ex = extract_fn(g["job_description"])
    except Exception as e:  # one bad Golden must not hide the rest of the run
        prediction = {"error": f"{type(e).__name__}: {e}"}
        score = GoldenScore(
            g["id"], [], [], sorted(x["skill_id"] for x in g["expected"]), 0, error=str(e),
            **attribute_pairs(g, prediction))
        return [], prediction, score

    pred = [{"skill_id": m.skill_id, "requirement": m.requirement, "raw_text": m.raw_text,
             "alternative_group": getattr(m, "alternative_group", None)} for m in ex.mentions]
    sen = getattr(ex, "seniority", None)
    ger = getattr(ex, "german", None)
    deg = getattr(ex, "degree", None)
    prod = getattr(ex, "production", None)
    prediction = {
        "mentions": pred,
        "proposed": [vars(p) for p in ex.proposed],
        "rejected": ex.rejected,
        "seniority": vars(sen) if sen else None,
        "german": vars(ger) if ger else None,
        "degree": vars(deg) if deg else None,
        "production": vars(prod) if prod else None,
        "usage": getattr(ex, "usage", {}),
    }
    if span is not None:
        span.mapping(ex)
    score = score_golden(g["id"], g["expected"], pred,
                         grounding=grounding(g["job_description"], ex.mentions,
                                             ex.proposed, ex.rejected),
                         groups_reviewed=bool(g.get("groups_reviewed")),
                         **attribute_pairs(g, prediction))
    return pred, prediction, score


def run_once(goldens: list[dict], extract_fn, trace=None) -> RunResult:
    """extract_fn(jd_text) -> Extraction-like object with .mentions/.proposed/.rejected.

    trace(golden) is an optional context manager yielding a span with .mapping(extraction),
    .result(prediction) and .record(score) — the reporting backend, injected the same way
    extract_fn is, so this module knows nothing about where anything is sent
    (app/langsmith_eval.py).
    """
    scores, predicted_by_id, predictions = [], {}, {}
    expected_by_id = {g["id"]: g["expected"] for g in goldens}
    for g in goldens:
        with (trace(g) if trace else nullcontext()) as span:
            pred, prediction, score = _score_one(g, extract_fn, span)
            if span is not None:
                span.result(prediction)
                span.record(score)
        predictions[g["id"]] = prediction
        predicted_by_id[g["id"]] = pred
        scores.append(score)
    return RunResult(summarize(scores, expected_by_id, predicted_by_id), scores, predictions)


METRICS = ("precision", "recall", "f1", "requirement_accuracy", "seniority_accuracy", "german_accuracy", "degree_accuracy",
           "production_accuracy", "production_signal_agreement", "grounding_accuracy", "group_f1",
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
