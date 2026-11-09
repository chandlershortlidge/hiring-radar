"""LangSmith tracing for the live system: one trace per extraction run, one child per job.

Does: open a run-level trace around a poll, a re-read or an add; add a child span per job
carrying its tokens, the model's cost and whether the evidence the model quoted really
appears in the posting; and close the run with its counts. Wraps the Anthropic client so
the model call itself nests under its job with its own tokens and cost, measured by
LangSmith rather than guessed here.

Does NOT: decide anything, change what is stored, or affect what the dashboard shows. It
is a view onto runs that happen anyway. It does not score or gate: the eval gate stays
the committed `evals/results/` directory (AGENTS.md "The eval gate"); this is the record
of production traffic beside it. Nothing here reads the Goldens or the held-out split.

Invariants:
  - Off unless LANGSMITH_API_KEY is set. With it unset every call here is a no-op, so the
    poll, the API and the whole test suite behave exactly as before and no test sends
    anything to LangSmith.
  - A LangSmith failure never fails a run — not opening a trace, not closing one, not
    posting a span. Every call goes through `_safe`, which warns on stderr and carries on:
    the daily poll cannot depend on a third party being reachable.
  - One trace per run, not per job, however many cities are added — the free plan allows
    5,000 traces a month and the eval shares it (HIR-160). Jobs are children of the run.
  - Only the public job ad already being sent to the model goes out: the job's title and
    posting text, its database id, and the model's own answer. Nothing about a person.

Nesting is by LangSmith's own tracing context, not by hand: a span opened here while
another is open becomes its child. That is what makes the model call a child of its job
rather than a sibling, and what lets `run()` be called inside an outer trace without
starting a second one.

Cost: the wrapped client reports real token counts, and LangSmith prices them at the
standard rate. A caller that paid a different rate (the Batch API's half price, HIR-222)
has to pass its own numbers in; `JobSpan.result` takes `usage` for exactly that.
"""

import os
import sys
from contextlib import contextmanager

# The LangSmith project the live traces land in — separate from the eval's experiments, so
# production traffic and eval runs are never read as one number.
DEFAULT_PROJECT = "hiring-radar-live"

# What opened the run. Goes on the trace as its name and its first tag, so a poll and a
# full re-read of the same database are told apart at a glance.
POLL = "poll"
REREAD = "re-read"
ADD = "add"
BACKFILL = "backfill"


def enabled() -> bool:
    """Tracing is on exactly when a key is set; nothing else turns it on."""
    return bool(os.environ.get("LANGSMITH_API_KEY"))


def project_name() -> str:
    return os.environ.get("LANGSMITH_LIVE_PROJECT") or DEFAULT_PROJECT


def _safe(what: str, fn, *a, **kw):
    """Run a LangSmith call; on failure warn and return None. The run keeps going."""
    try:
        return fn(*a, **kw)
    except Exception as e:  # noqa: BLE001 - any client, network or auth failure is non-fatal
        print(f"  [langsmith] {what} failed, continuing without it: {type(e).__name__}: {e}",
              file=sys.stderr, flush=True)
        return None


def wrap_client(client):
    """Wrap the Anthropic client so each model call becomes an LLM child span with its
    tokens, latency and cost. A no-op when tracing is off, and idempotent: wrapping an
    already-wrapped client would nest every call twice.
    """
    if client is None or not enabled() or getattr(client, "_hiring_radar_traced", False):
        return client
    from langsmith.wrappers import wrap_anthropic

    wrapped = _safe("wrap client", wrap_anthropic, client) or client
    try:
        wrapped._hiring_radar_traced = True
    except Exception:  # noqa: BLE001 - a client that refuses attributes just gets re-wrapped
        pass
    return wrapped


@contextmanager
def _trace(what: str, **kw):
    """`langsmith.trace`, with every way it can fail turned into None instead of an error.

    Entered and exited by hand rather than with `with`, so that a failure to open the span
    yields None (callers then do nothing), and a failure to close it is warned about
    instead of replacing whatever the body was doing. An exception from the body is handed
    to the span, so a failed job is visible in LangSmith, and then re-raised unchanged.
    """
    import langsmith

    cm = _safe(what, langsmith.trace, **kw)
    if cm is None:
        yield None
        return
    run_tree = _safe(what, cm.__enter__)
    if run_tree is None:
        yield None
        return
    try:
        yield run_tree
    except BaseException:
        _safe(what, cm.__exit__, *sys.exc_info())
        raise
    _safe(what, cm.__exit__, None, None, None)


class JobSpan:
    """One job's reading, as a child of the run. `run_tree` is None when tracing is off."""

    def __init__(self, run_tree):
        self.run_tree = run_tree

    def result(self, extraction, grounded: int, quotes: int, usage: dict | None = None) -> None:
        """Put the answer, its token usage and its grounding on this job's span.

        `grounded`/`quotes` are app/grounding.py's count for this one posting: how many of
        the snippets the model offered as evidence were really in the ad. Jobs with
        `grounding_failures` above zero are the shape of a model inventing its evidence,
        which the skills themselves do not show; they are tagged so the dashboard can
        count them per day.

        `usage` overrides the extraction's own token counts, for a caller that knows
        something the extraction object does not (the Batch API's half price, HIR-222).
        """
        if self.run_tree is None:
            return
        used = usage if usage is not None else dict(getattr(extraction, "usage", {}) or {})
        failures = quotes - grounded
        _safe("job outputs", self.run_tree.add_outputs, {
            "skills": [m.skill_id for m in getattr(extraction, "mentions", [])],
            "n_mentions": len(getattr(extraction, "mentions", [])),
            "n_proposed": len(getattr(extraction, "proposed", [])),
            "n_rejected": len(getattr(extraction, "rejected", [])),
            "quotes": quotes,
            "grounded": grounded,
            "grounding_failures": failures,
            "grounding": (grounded / quotes) if quotes else None,
            "usage": used,
        })
        if failures:
            _safe("job tags", self.run_tree.add_tags, ["grounding-failure"])

    def failed(self, error: str, dropped: bool = False) -> None:
        """A job the model could not read. Recorded, not raised: the run carries on, and a
        failure that leaves no trace is what this exists to prevent."""
        if self.run_tree is None:
            return
        _safe("job outputs", self.run_tree.add_outputs, {"error": error, "dropped": dropped})
        _safe("job tags", self.run_tree.add_tags,
              ["extraction-failure"] + (["dropped"] if dropped else []))


class Run:
    """One extraction run. `run_tree` is None when tracing is off, and then every method
    here does nothing at all."""

    def __init__(self, run_tree):
        self.run_tree = run_tree

    def note(self, metadata: dict) -> None:
        """Facts about the run learned after it opened — how much of the queue is re-reads,
        which skill triggered a targeted re-read (HIR-224)."""
        if self.run_tree is None:
            return
        _safe("run metadata", self.run_tree.add_metadata, dict(metadata))

    def tag(self, *tags: str) -> None:
        if self.run_tree is None or not tags:
            return
        _safe("run tags", self.run_tree.add_tags, list(tags))

    def finish(self, outputs: dict) -> None:
        if self.run_tree is None:
            return
        _safe("run outputs", self.run_tree.add_outputs, dict(outputs))

    @contextmanager
    def job(self, job_id: int, title: str | None, sent: str):
        """One job's span, with the model call nesting under it through the wrapped client.

        The body's exception propagates: the pipeline turns a failed reading into a
        reported failure itself, and swallowing it here would change what gets stored.
        """
        if self.run_tree is None:
            yield JobSpan(None)
            return
        with _trace("job span", name=f"job {job_id}", run_type="chain",
                    inputs={"job_id": job_id, "title": title, "sent": sent}) as child:
            yield JobSpan(child)


@contextmanager
def run(kind: str, metadata: dict | None = None, inputs: dict | None = None):
    """One trace for a whole extraction run. Yields a `Run`; a do-nothing one when off."""
    if not enabled():
        yield Run(None)
        return
    with _trace("open run", name=kind, run_type="chain",
                inputs=dict(inputs or {}),
                project_name=project_name(),
                tags=[kind],
                metadata=dict(metadata or {})) as run_tree:
        yield Run(run_tree)
