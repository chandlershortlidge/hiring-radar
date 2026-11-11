"""What it would cost, right now, to have the model read every job it would re-read.

Does: hold the model's prices in one place; average the token counts of the readings we
have already paid for (`extraction_log.usage`, HIR-170); multiply by the number of jobs an
extractor change merged today would queue; report all of it in plain words.

Does NOT: make any model call, touch the network, or write anything. Reading the database
is the whole job, so running it costs nothing.

Why it exists: the agents' instructions used to quote a flat "about €3" for a full re-read.
That was true at a few hundred jobs. Launching three German cities took the stored jobs to
730 and the same re-read to about €10.5, and the figure grows with every city — so a pull
request that said €3 understated what merging it would spend. The number is now computed
and pasted into the pull request instead of remembered (HIR-221).

Invariants: the cost is per *reading*, measured in tokens and priced at the model that
would do the next reading — so swapping models reprices honestly instead of carrying an
old model's euros forward. Too few logged readings to average is reported as an estimate,
never silently smoothed over. The job count is the queue's own definition
(`pipeline.reread_queue_size`), so it can't drift from what actually runs. Priced at the
Batch API's half rate, since a re-read always runs as a batch now (HIR-222); the logged
token counts themselves are unaffected by how a reading was billed.
"""

import json
import sqlite3
from dataclasses import dataclass

from app.extract import DEFAULT_MODEL

# Per million tokens, in US dollars, from the published Anthropic price list.
# (input, output, cache read, cache write) — a cached read is a tenth of the input price
# and writing the cache is a quarter more, which matters here because the extractor's
# system prompt carries the whole skill list and is cached on every call after the first.
MODEL_PRICES_USD_PER_MTOK: dict[str, tuple[float, float, float, float]] = {
    "claude-sonnet-5-5": (2.00, 10.00, 0.20, 2.50),
    "claude-sonnet-5": (2.00, 10.00, 0.20, 2.50),
    "claude-opus-5-5": (4.00, 20.00, 0.40, 5.00),
    "claude-haiku-5-5": (0.10, 0.50, 0.01, 0.125),
}

EUR_PER_USD = 0.93

# The Message Batches API charges half the standard input and output price, and the
# discount stacks with prompt caching (HIR-222). Every re-read now goes through a batch
# (app/pipeline.py), so this is the rate `reread_cost` prices at.
BATCH_DISCOUNT = 0.5

# The fallback, used only when the database holds too few readings to average. Measured
# against app/extract.py by hand and rounded up; the same figures the city-launch spending
# cap has always used. An over-estimate is the safe direction for a number someone reads
# before deciding whether to spend.
ESTIMATE_INPUT_TOKENS = 6_500
ESTIMATE_OUTPUT_TOKENS = 700

# How many logged readings make an average worth trusting, and how many to average over.
# The most recent readings, not all of them: the token count of a reading tracks the size
# of the prompt and the skill list, both of which grow, so old readings describe an
# extractor that no longer exists.
MIN_READINGS_TO_AVERAGE = 20
READINGS_SAMPLED = 200

USAGE_KEYS = ("input_tokens", "output_tokens", "cache_read_input_tokens",
              "cache_creation_input_tokens")


@dataclass(frozen=True)
class Tokens:
    """Mean tokens of one reading, by how each kind is billed."""
    input: float = 0.0
    output: float = 0.0
    cache_read: float = 0.0
    cache_write: float = 0.0

    def total(self) -> float:
        return self.input + self.output + self.cache_read + self.cache_write


@dataclass(frozen=True)
class RereadCost:
    jobs: int                 # jobs the next extractor change would read
    tokens: Tokens            # per reading
    readings: int             # logged readings the average came from; 0 when estimated
    found: int                # logged readings with usable token counts, however few
    model: str                # the model the next reading would use
    eur_per_reading: float
    eur_total: float
    # HIR-224. Set only when the cost was asked about a branch's own skill list (`tax`):
    # what a full re-read would have been, and, when the branch only adds skills, which
    # ones and how many open jobs keep their reading.
    full_jobs: int | None = None
    carried: int = 0
    added_ids: tuple[str, ...] = ()
    unchanged: bool = False   # the branch's extractor is the one the jobs were read with
    by_suggestion: int = 0    # re-read because the model had suggested an added skill there
    offers: tuple[tuple[str, tuple[str, ...]], ...] = ()  # (skill id, spellings to offer)

    @property
    def measured(self) -> bool:
        """True when the figure came from readings we paid for, rather than the fallback."""
        return self.readings > 0


def price_eur(tokens: Tokens, model: str, batch: bool = False) -> float:
    """What one reading of that token shape costs, in euros, on `model`. Pure.

    An unpriced model falls back to the current default's prices rather than raising: a
    missing row in the table must not stop someone finding out roughly what a merge costs.

    `batch=True` halves every rate (HIR-222): the Message Batches API's own discount,
    which applies to input, output and cached tokens alike and stacks with the cache
    discount already baked into `usd_read`/`usd_write`.
    """
    usd_in, usd_out, usd_read, usd_write = MODEL_PRICES_USD_PER_MTOK.get(
        model, MODEL_PRICES_USD_PER_MTOK[DEFAULT_MODEL])
    if batch:
        usd_in, usd_out, usd_read, usd_write = (
            usd_in * BATCH_DISCOUNT, usd_out * BATCH_DISCOUNT,
            usd_read * BATCH_DISCOUNT, usd_write * BATCH_DISCOUNT)
    usd = (tokens.input * usd_in + tokens.output * usd_out
           + tokens.cache_read * usd_read + tokens.cache_write * usd_write) / 1e6
    return usd * EUR_PER_USD


def mean_tokens(usages: list[dict]) -> Tokens:
    """Mean of the token counts the provider reported. Pure.

    A missing or null count reads as zero: the provider sends no cache fields at all when
    caching is off, and that is a real zero, not a gap in the data.
    """
    if not usages:
        return Tokens()
    n = len(usages)
    mean = [sum((u.get(k) or 0) for u in usages) / n for k in USAGE_KEYS]
    return Tokens(*mean)


def logged_usages(conn: sqlite3.Connection, limit: int = READINGS_SAMPLED) -> list[dict]:
    """The token counts of the most recent readings, newest first.

    Rows whose usage is '{}' are skipped — the provider sent no counts, so they say nothing
    about what a reading costs and would drag the average towards zero if averaged in.
    """
    rows = conn.execute("SELECT usage FROM extraction_log ORDER BY id DESC LIMIT ?",
                        (int(limit),)).fetchall()
    out = []
    for row in rows:
        try:
            usage = json.loads(row["usage"])
        except (ValueError, TypeError):
            continue
        if isinstance(usage, dict) and any(usage.get(k) for k in USAGE_KEYS):
            out.append(usage)
    return out


def reread_cost(conn: sqlite3.Connection, now: str | None = None,
                model: str = DEFAULT_MODEL, tax=None, git_ref: str | None = "origin/main") -> RereadCost:
    """Measure the cost of the re-read an extractor change merged now would trigger.

    Without `tax`: every open job, as any extractor change used to re-read (HIR-221).
    With `tax` (the branch's skill list): the jobs that change would really re-read. A
    branch that only adds skills re-reads only the open jobs naming one (HIR-224); the old
    skill list comes from the database's recorded snapshots or, failing those, from
    `git_ref`'s skill list."""
    # Imported here, not at the top: the price table below is read by app/discover.py, and
    # a module-level import would drag the whole extraction pipeline into the board search.
    from app.pipeline import reread_queue_size
    full = jobs = reread_queue_size(conn, now)
    targeted: dict = {}
    if tax is not None:
        from app import targeted_reread as tr
        snaps = tr.load_snapshots(conn)
        from_ref = tr.snapshot_from_git(model, git_ref) if git_ref else None
        if from_ref is not None:
            snaps.setdefault(from_ref.version, from_ref)
        p = tr.plan(conn, tax, model, snaps, now)
        if p.stale:
            jobs = full - p.stale + len(p.reread)   # never-read jobs are read either way
            targeted = dict(full_jobs=full, carried=len(p.carry), added_ids=tuple(p.added_ids),
                            by_suggestion=len(p.by_suggestion),
                            offers=tuple((sid, tuple(ws)) for sid, ws in p.offers.items()))
        else:
            targeted = dict(full_jobs=full, unchanged=True)
    usages = logged_usages(conn)
    if len(usages) >= MIN_READINGS_TO_AVERAGE:
        tokens, readings = mean_tokens(usages), len(usages)
    else:
        tokens, readings = Tokens(input=ESTIMATE_INPUT_TOKENS, output=ESTIMATE_OUTPUT_TOKENS), 0
    # Logged usages are real token counts regardless of how they were read; the re-read
    # this merge would trigger always runs as a batch now (HIR-222), so price it as one.
    per = price_eur(tokens, model, batch=True)
    return RereadCost(jobs=jobs, tokens=tokens, readings=readings, found=len(usages),
                      model=model, eur_per_reading=per, eur_total=per * jobs, **targeted)


def report_lines(cost: RereadCost) -> list[str]:
    """The command's output: the figure for the pull request first, then where it came from."""
    lines = [f"A change to the extractor or the skill list, merged now, would re-read "
             f"{cost.jobs} job{'' if cost.jobs == 1 else 's'}: about €{cost.eur_total:.2f}.",
             ""]
    if cost.measured:
        lines.append(f"Measured from the last {cost.readings} readings we paid for: "
                     f"{cost.tokens.total():,.0f} tokens per reading on average "
                     f"(€{cost.eur_per_reading:.4f} each at {cost.model} Batch API prices, "
                     f"half the standard rate — a re-read always runs as a batch, HIR-222).")
    else:
        lines.append(f"ESTIMATE, not measured: only {cost.found} stored reading"
                     f"{'' if cost.found == 1 else 's'} carry token counts, fewer than the "
                     f"{MIN_READINGS_TO_AVERAGE} needed to average. This uses a hand-made guess "
                     f"of {ESTIMATE_INPUT_TOKENS:,} tokens in and {ESTIMATE_OUTPUT_TOKENS:,} out "
                     f"per reading (€{cost.eur_per_reading:.4f} each at {cost.model} Batch API "
                     f"prices). Treat it as the right order of magnitude, not a quote.")
    if cost.unchanged:
        lines.append("")
        lines.append("This branch does not change the extractor or the skill list, so merging it "
                     "re-reads nothing. The figure above is what a change other than added skills "
                     "would cost.")
    elif cost.carried:
        lines.append("")
        lines.append(f"Only added skills ({', '.join(cost.added_ids)}): the open jobs whose text "
                     f"names none of them keep their reading, {cost.carried} of them (HIR-224). "
                     f"A full re-read would be {cost.full_jobs} jobs, about "
                     f"€{cost.eur_per_reading * cost.full_jobs:.2f}.")
        if cost.by_suggestion:
            lines.append(f"{cost.by_suggestion} of the re-reads are jobs whose text never names "
                         f"the skill but where the model had already suggested it.")
    if cost.offers:
        lines.append("")
        lines.append("Spellings the model used when it suggested these skills, not yet in the "
                     "skill list — offer them as aliases in the pull request:")
        for sid, words in cost.offers:
            lines.append(f"  {sid}: {', '.join(words)}")
    lines.append("")
    lines.append("Closed jobs are not re-read, so they are not counted (HIR-195). "
                 "Paste the figure above into the pull request body.")
    return lines
