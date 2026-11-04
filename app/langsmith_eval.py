"""LangSmith reporting for the Golden eval: one dataset, one experiment per eval run.

Does: mirror the dev-split Goldens into a LangSmith dataset, open an experiment named
after the `extractor_version` so taxonomy versions sit side by side, send one trace per
Golden per repeat (the model call and the taxonomy-mapping step as children), and attach
the per-Golden scores as feedback and the whole-run scores to the experiment.

Does NOT: decide anything. The committed `evals/results/` directory stays the eval gate
(AGENTS.md "The eval gate"); LangSmith is the view onto it. Not used by the daily poll,
the API or the dashboard — only by scripts/run_eval.py.

Invariants:
  - Off unless LANGSMITH_API_KEY is set, so tests and anyone without a key run the eval
    exactly as before. No test sends anything to LangSmith.
  - Only the dev split is ever uploaded. A Golden from another split raises before
    anything is sent, rather than leaking held-out text (AGENTS.md: never tune on held-out).
  - A LangSmith failure never fails the eval. Every call goes through `_safe`, which warns
    on stderr and carries on: the gate cannot depend on a third party being reachable.
"""

import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone

DATASET_NAME = "goldens-dev"
DEV_SPLIT = "dev"

# Attributes scored as an (expected, predicted) pair on the GoldenScore, and only when the
# Golden carries that label. None ("not mentioned") is a label like any other, so a match
# on it counts — see app/evaluation.py.
PAIR_SCORES = ("german", "degree", "production")


def enabled() -> bool:
    """Tracing is on exactly when a key is set; nothing else turns it on."""
    return bool(os.environ.get("LANGSMITH_API_KEY"))


def _safe(what: str, fn, *a, **kw):
    """Run a LangSmith call; on failure warn and return None. The eval keeps going."""
    try:
        return fn(*a, **kw)
    except Exception as e:  # noqa: BLE001 - any client, network or auth failure is non-fatal
        print(f"  [langsmith] {what} failed, continuing without it: {type(e).__name__}: {e}",
              file=sys.stderr, flush=True)
        return None


def _by_golden_id(client, dataset_id) -> dict:
    return {(ex.metadata or {}).get("golden_id"): ex.id
            for ex in client.list_examples(dataset_id=dataset_id)}


# --- dataset ----------------------------------------------------------------------

def example_payload(g: dict) -> tuple[dict, dict, dict]:
    """(inputs, outputs, metadata) for one Golden, as a LangSmith example.

    Outputs carry the labels the eval scores against, so a trace shows gold beside
    prediction. An unlabeled attribute is left out rather than sent as null, so "this
    Golden has no German label" stays distinguishable from "German: not mentioned".
    """
    if g.get("split") != DEV_SPLIT:
        raise ValueError(f"Golden {g.get('id')!r} is split {g.get('split')!r}; "
                         f"only the {DEV_SPLIT} split goes to LangSmith")
    inputs = {"job_description": g["job_description"]}
    if g.get("title"):
        inputs["title"] = g["title"]
    outputs = {"expected": g["expected"]}
    for key in ("seniority", "german", "degree", "degree_or_equivalent", "production",
                "production_signal"):
        if key in g:
            outputs[key] = g[key]
    metadata = {"golden_id": g["id"], "split": g["split"],
                "source_sha256": g.get("source_sha256")}
    return inputs, outputs, metadata


def sync_dataset(client, goldens: list[dict], name: str = DATASET_NAME):
    """Create the dataset if it is new, then add or refresh one example per Golden.

    Keyed on the Golden's id in example metadata, so re-running an eval updates examples
    in place instead of piling up copies, and a Golden added since the last run appears on
    its first. Returns (dataset_id, {golden_id: example_id}); a Golden missing from the
    map is simply traced without an example link.
    """
    payloads = [example_payload(g) for g in goldens]  # raises before anything is uploaded

    dataset = _safe("read dataset", client.read_dataset, dataset_name=name)
    if dataset is None:
        dataset = _safe("create dataset", client.create_dataset, name,
                        description="Dev-split Goldens for the hiring-radar skill extractor "
                                    "(HIR-78). Held-out Goldens are never uploaded.")
    if dataset is None:
        return None, {}

    existing = _safe("list examples", _by_golden_id, client, dataset.id) or {}
    create, update = [], []
    for g, (inputs, outputs, metadata) in zip(goldens, payloads):
        if g["id"] in existing:
            update.append({"id": existing[g["id"]], "inputs": inputs, "outputs": outputs,
                           "metadata": metadata})
        else:
            create.append({"inputs": inputs, "outputs": outputs, "metadata": metadata})

    if create:
        _safe("create examples", client.create_examples, dataset_id=dataset.id, examples=create)
        existing = _safe("list examples", _by_golden_id, client, dataset.id) or existing
    if update:
        _safe("update examples", client.update_examples, dataset_id=dataset.id, updates=update)

    return dataset.id, existing


# --- experiment -------------------------------------------------------------------

class Span:
    """One Golden's trace. Collects the scores and posts them once the trace has closed."""

    def __init__(self, client, run_tree, session_id=None):
        self.client = client
        self.run_tree = run_tree
        self.session_id = session_id   # the experiment's project id, in feedback's terms
        self._feedback: list[tuple[str, float]] = []

    def mapping(self, extraction) -> None:
        """Log the taxonomy-mapping step as a child of this trace: what the model's labels
        turned into, what was kept, and what was rejected with the reason."""
        if self.run_tree is None:
            return
        child = _safe("mapping span", self.run_tree.create_child, "taxonomy_mapping",
                      run_type="parser",
                      inputs={"taxonomy_version": getattr(extraction, "taxonomy_version", None)})
        if child is None:
            return
        child.end(outputs={
            "kept": [vars(m) for m in extraction.mentions],
            "proposed": [vars(p) for p in extraction.proposed],
            "rejected": extraction.rejected,
        })
        _safe("mapping span", child.post)

    def result(self, prediction: dict) -> None:
        """Put what the extractor produced on the trace — or, when it failed, the error,
        so a failed Golden is visible in LangSmith and not just a gap."""
        if self.run_tree is None:
            return
        _safe("trace outputs", self.run_tree.add_outputs, dict(prediction))

    def record(self, score) -> None:
        """Queue this Golden's scores. The same measures as app/evaluation.py, but per
        Golden rather than micro-averaged over the suite, so one posting's row reads on
        its own."""
        tp, fp, fn = len(score.tp), len(score.fp), len(score.fn)
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        out = {
            "skill_precision": precision,
            "skill_recall": recall,
            "skill_f1": (2 * precision * recall / (precision + recall)
                         if precision and recall else None),
            "requirement_accuracy": score.requirement_matches / tp if tp else None,
            "grounding": score.grounded / score.quotes if score.quotes else None,
            "extras": float(fp),   # a count, not a rate: what the extras judge looks at
            "missed": float(fn),
        }
        if score.seniority_labeled:
            out["seniority"] = float(score.seniority_predicted == score.seniority_expected)
        for key in PAIR_SCORES:
            pair = getattr(score, key)
            if pair is not None:
                out[key] = float(pair[0] == pair[1])
        self._feedback = [(k, v) for k, v in out.items() if v is not None]

    def flush(self) -> None:
        if self.run_tree is None:
            return
        for key, value in self._feedback:
            # session_id, not project_id: feedback for a run without a session is
            # deprecated and stops working in a future SDK release, and `project_id` is
            # rejected outright next to a run_id ("project_id cannot be provided if run_id
            # or trace_id is provided"). session_id takes the same value — the experiment's
            # project id. A live run found that the hard way.
            _safe(f"feedback {key}", self.client.create_feedback,
                  run_id=self.run_tree.id, key=key, score=value,
                  trace_id=self.run_tree.trace_id, session_id=self.session_id)


class Experiment:
    """One eval run, as a LangSmith experiment over the Goldens dataset."""

    def __init__(self, client, project, examples: dict):
        self.client = client
        self.project = project
        self.examples = examples

    @property
    def name(self) -> str:
        return getattr(self.project, "name", "")

    @property
    def url(self) -> str | None:
        endpoint = os.environ.get("LANGSMITH_ENDPOINT") or "https://api.smith.langchain.com"
        host = endpoint.replace("api.smith.langchain.com", "smith.langchain.com")
        pid = getattr(self.project, "id", None)
        return f"{host}/o/projects/p/{pid}" if pid else None

    @contextmanager
    def trace(self, golden: dict):
        """One trace per Golden per repeat. The model call nests under it through the
        wrapped Anthropic client; the mapping step is added by Span.mapping.

        The body's exception propagates: run_once turns a failed extraction into a scored
        miss itself, and swallowing it here would change what the eval measures.
        """
        import langsmith

        span = None
        try:
            with langsmith.trace(
                name=golden["id"],
                run_type="chain",
                inputs={"job_description": golden["job_description"]},
                project_name=self.name,
                client=self.client,
                reference_example_id=self.examples.get(golden["id"]),
                metadata={"golden_id": golden["id"]},
            ) as run_tree:
                span = Span(self.client, run_tree, getattr(self.project, "id", None))
                yield span
        finally:
            if span is not None:
                span.flush()

    def finish(self, meta: dict, aggregate: dict, run_summaries: list[dict]) -> None:
        """Close the experiment and attach the whole-run scores to it.

        The suite-level metrics (overall P/R/F1, rank correlation, top-10 overlap) are
        properties of the run, not of any one posting, so they go on the experiment itself
        rather than being invented as feedback on an arbitrary trace.
        """
        pid = getattr(self.project, "id", None)
        if pid is None:
            return
        _safe("close experiment", self.client.update_project, pid,
              metadata={**meta,
                        "summary_scores": {k: v.get("mean") for k, v in aggregate.items()},
                        "per_repeat": [{k: r.get(k) for k in
                                        ("precision", "recall", "f1", "rank_spearman",
                                         "top10_overlap", "grounding_accuracy", "n_errors")}
                                       for r in run_summaries]},
              end_time=datetime.now(timezone.utc))


def start(goldens: list[dict], meta: dict, dataset_name: str = DATASET_NAME):
    """Sync the dataset and open the experiment. None when tracing is off or unreachable.

    The experiment is named after the extractor_version, with the run's timestamp, so a
    re-run of the same version sits beside the first rather than overwriting it.
    """
    if not enabled():
        return None
    from langsmith import Client

    client = _safe("create client", Client)
    if client is None:
        return None

    dataset_id, examples = sync_dataset(client, goldens, dataset_name)
    name = f"{meta['extractor_version']}-{meta['run_id'].split('_')[0]}"
    project = _safe("create experiment", client.create_project, name,
                    reference_dataset_id=dataset_id,
                    metadata=meta,
                    num_examples=len(goldens),
                    num_repetitions=meta.get("repeats"),
                    description=f"Dev eval of extractor {meta['extractor_version']} "
                                f"(taxonomy v{meta.get('taxonomy_version')}).")
    if project is None:
        return None
    return Experiment(client, project, examples)


def wrap_client(client):
    """Wrap the Anthropic client so each model call becomes an LLM child span carrying its
    tokens, latency and cost. A no-op when tracing is off."""
    if not enabled():
        return client
    from langsmith.wrappers import wrap_anthropic

    return _safe("wrap client", wrap_anthropic, client) or client
