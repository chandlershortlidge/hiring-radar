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
  - The key alone turns tracing on. `langsmith.trace` itself only posts when it reads
    `LANGSMITH_TRACING` (or `*_TRACING_V2`) as on, so without forcing that, a key with
    neither set traced nothing even though every call here ran (HIR-238: the 10 Nov VM
    needed both set, though the docstring above and the README promised just the key).
    `run()` overrides the SDK's switch for its whole span — the run, every job, and the
    model call nested under it — rather than requiring both.
  - A LangSmith failure never fails a run — not opening a trace, not closing one, not
    posting a span, and not the `import langsmith` itself. Every call goes through `_safe`,
    which warns on stderr and carries on: the daily poll cannot depend on a third party
    being reachable, nor on the package being installed (HIR-233). The package is a real
    project dependency so the VM has it, but a missing or broken one is tracing off, not a
    failed poll.
  - One trace per run, not per job, however many cities are added — the free plan allows
    5,000 traces a month and the eval shares it (HIR-160). Jobs are children of the run.
  - A run flushes its own client when it closes, capped at FLUSH_TIMEOUT_S. The SDK sends
    from a background thread, and the poll is a oneshot process that used to exit before
    that thread had sent anything, losing every trace silently (HIR-236).
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

# The SDK sends runs from a background thread; a oneshot process (the poll) can exit and
# kill that thread before anything is sent (HIR-236). Capped so an unreachable LangSmith
# delays a run by at most this long rather than hanging the 07:00 timer.
FLUSH_TIMEOUT_S = 30


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


# True once the "langsmith could not be imported" warning has been printed, so a poll of
# 200 jobs says it once rather than once per job (HIR-233).
_import_warned = False


def _module(name: str):
    """Import a langsmith module, or None if it cannot be imported.

    A missing or broken `langsmith` is tracing off, not a failed run: the deploy installs
    it as a project dependency, but an environment without it must still poll (HIR-233).
    """
    global _import_warned
    try:
        import importlib

        return importlib.import_module(name)
    except Exception as e:  # noqa: BLE001 - any import failure is non-fatal
        if not _import_warned:
            _import_warned = True
            print(f"  [langsmith] import failed, continuing without it: "
                  f"{type(e).__name__}: {e}", file=sys.stderr, flush=True)
        return None


def wrap_client(client):
    """Wrap the Anthropic client so each model call becomes an LLM child span with its
    tokens, latency and cost. A no-op when tracing is off, and idempotent: wrapping an
    already-wrapped client would nest every call twice.
    """
    if client is None or not enabled() or getattr(client, "_hiring_radar_traced", False):
        return client
    wrappers = _module("langsmith.wrappers")
    if wrappers is None:
        return client
    wrapped = _safe("wrap client", wrappers.wrap_anthropic, client) or client
    try:
        wrapped._hiring_radar_traced = True
    except Exception:  # noqa: BLE001 - a client that refuses attributes just gets re-wrapped
        pass
    return wrapped


@contextmanager
def _trace(what: str, **kw):
    """`langsmith.trace`, with every way it can fail turned into None instead of an error,
    including the package not being installed at all.

    Entered and exited by hand rather than with `with`, so that a failure to open the span
    yields None (callers then do nothing), and a failure to close it is warned about
    instead of replacing whatever the body was doing. An exception from the body is handed
    to the span, so a failed job is visible in LangSmith, and then re-raised unchanged.
    """
    langsmith = _module("langsmith")
    if langsmith is None:
        yield None
        return
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

    def result(self, extraction, grounded: int, quotes: int, usage: dict | None = None,
              usage_metadata: dict | None = None) -> None:
        """Put the answer, its token usage and its grounding on this job's span.

        `grounded`/`quotes` are app/grounding.py's count for this one posting: how many of
        the snippets the model offered as evidence were really in the ad. Jobs with
        `grounding_failures` above zero are the shape of a model inventing its evidence,
        which the skills themselves do not show; they are tagged so the dashboard can
        count them per day.

        `usage` overrides the extraction's own token counts, for a caller that knows
        something the extraction object does not (the Batch API's half price, HIR-222).

        `usage_metadata`, when given, is LangSmith's own cost-tracking shape
        (`langsmith.schemas.UsageMetadata`: token counts plus explicit `input_cost` /
        `output_cost` / `total_cost`). A batch reading has no nested LLM span of its own —
        the wrapped client only ever sees `messages.create`, never the Batch API — so
        without this LangSmith prices it at the standard rate, or shows nothing at all.
        """
        if self.run_tree is None:
            return
        used = usage if usage is not None else dict(getattr(extraction, "usage", {}) or {})
        failures = quotes - grounded
        outputs = {
            "skills": [m.skill_id for m in getattr(extraction, "mentions", [])],
            "n_mentions": len(getattr(extraction, "mentions", [])),
            "n_proposed": len(getattr(extraction, "proposed", [])),
            "n_rejected": len(getattr(extraction, "rejected", [])),
            "quotes": quotes,
            "grounded": grounded,
            "grounding_failures": failures,
            "grounding": (grounded / quotes) if quotes else None,
            "usage": used,
        }
        if usage_metadata:
            outputs["usage_metadata"] = usage_metadata
        _safe("job outputs", self.run_tree.add_outputs, outputs)
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


def _flush(run_tree) -> None:
    run_tree.client.flush(timeout=FLUSH_TIMEOUT_S)


@contextmanager
def _force_enabled():
    """Override `LANGSMITH_TRACING` for this block: `langsmith.trace` reads that env var
    (not the key) to decide whether a span actually posts, so without this the key alone
    was not enough (HIR-238). The override is LangSmith's own ambient tracing context, the
    same mechanism `_trace`'s nesting already relies on, so it stays in effect for every
    span opened anywhere inside the block — a run, its jobs, and the model calls nested
    under them — not just the one `trace()` call made directly inside it.

    A no-op when langsmith can't be imported or the override itself fails to open; either
    way the block still runs, just untraced, like any other LangSmith failure here.
    """
    langsmith = _module("langsmith")
    if langsmith is None:
        yield
        return
    try:
        cm = langsmith.tracing_context(enabled=True)
        cm.__enter__()
    except Exception as e:  # noqa: BLE001 - opening the override is non-fatal
        print(f"  [langsmith] force tracing on failed, continuing without it: "
              f"{type(e).__name__}: {e}", file=sys.stderr, flush=True)
        yield
        return
    try:
        yield
    except BaseException:
        _safe("force tracing on", cm.__exit__, *sys.exc_info())
        raise
    _safe("force tracing on", cm.__exit__, None, None, None)


@contextmanager
def run(kind: str, metadata: dict | None = None, inputs: dict | None = None):
    """One trace for a whole extraction run. Yields a `Run`; a do-nothing one when off.

    Flushes the run's client once the trace itself has closed, so the poll, a re-read, an
    add-by-link and a backfill all get this for free (HIR-236) rather than each caller
    having to remember it. Through `_safe`, so a stuck or unreachable LangSmith delays the
    run by at most FLUSH_TIMEOUT_S and never fails it.
    """
    if not enabled():
        yield Run(None)
        return
    with _force_enabled():
        with _trace("open run", name=kind, run_type="chain",
                    inputs=dict(inputs or {}),
                    project_name=project_name(),
                    tags=[kind],
                    metadata=dict(metadata or {})) as run_tree:
            yield Run(run_tree)
    if run_tree is not None:
        _safe("flush", _flush, run_tree)
