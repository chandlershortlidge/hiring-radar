"""What each model run actually cost: record it, add it up, and flag a run that cost too much
(HIR-449).

Does: write one `model_run` row (migration 030) after every run that sent at least one
posting to the model — its kind, model, whether it went as a batch, the provider's token
counts summed over its readings, the euros those come to and how many postings it read;
add the rows up by day and kind for the admin page and by week for the Monday summary;
price the readings already on record (`extraction_log`) per model, which is the before and
after of a model switch; cost the eval runs from their own result files; and pick out the
runs above RUN_ALERT_EUR for the morning caretaker's "needs you now" note.

Does NOT: call a model, estimate anything ahead of a run (that is app/reread_cost.py), or
change any spending cap: the caps stop a run before it starts, this only reports what one
spent afterwards.

Invariants: a cost is always priced from token counts the provider sent back, through
`reread_cost.price_eur`, the one price table — never from a per-posting guess. A batch
run is priced at the Batch API's half rate, exactly as the run's own "cost:" line is. A
run that read nothing writes no row. Eval runs are never in the database: they run on a
laptop, so the server's copy of the committed result files is where their cost comes from.
"""

import json
import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from app.reread_cost import USAGE_KEYS, Tokens, price_eur

# The one setting for the alert: a single run that costs more than this, in euros, is put
# in the morning caretaker's "needs you now" note (and an eval run prints a warning).
RUN_ALERT_EUR = 5.0

POLL, LAUNCH, REREAD, BULK_READ, ADD, EVAL = "poll", "launch", "re-read", "bulk-read", "add", "eval"
# Order on the page and in the Monday line; the plain words each kind is shown as.
KIND_WORDS = {POLL: "daily collection", LAUNCH: "city launch", REREAD: "re-read",
              BULK_READ: "bulk read", ADD: "added by hand", EVAL: "eval"}


@dataclass(frozen=True)
class Run:
    id: int | None            # None for an eval run, which has no database row
    kind: str
    model: str
    started_at: str           # ISO 8601 UTC; an eval run's is read from its run id
    readings: int
    cost_eur: float
    batch: bool = False
    label: str = ""           # an eval run's id

    @property
    def day(self) -> str:
        return self.started_at[:10]

    def words(self) -> str:
        """One plain sentence for the alert."""
        what = KIND_WORDS.get(self.kind, self.kind)
        return (f"The {what} run of {self.started_at[:16].replace('T', ' ')} UTC cost €{self.cost_eur:.2f}, "
                f"above the €{RUN_ALERT_EUR:.0f} alert for one run ({self.readings:,} postings read, {self.model}).")


# --- writing --------------------------------------------------------------------------------

def record(conn: sqlite3.Connection, kind: str, report, started_at: str, batch: bool) -> int | None:
    """Write the run `report` (a pipeline.ExtractReport) describes. Returns the row id, or
    None when the run sent nothing to the model and so cost nothing."""
    if report.skipped_busy or not report.attempted:
        return None
    t: Tokens = report.tokens
    with conn:
        cur = conn.execute(
            "INSERT INTO model_run (kind, model, batch, started_at, attempted, readings, input_tokens,"
            " output_tokens, cache_read_tokens, cache_write_tokens, cost_eur) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (kind, report.model, int(batch), started_at, report.attempted, report.succeeded,
             int(t.input), int(t.output), int(t.cache_read), int(t.cache_write), report.cost_eur))
    return cur.lastrowid


# --- reading --------------------------------------------------------------------------------

def runs(conn: sqlite3.Connection, since: str, until: str) -> list[Run]:
    """The recorded runs that started on days `since`..`until` (YYYY-MM-DD, both included)."""
    rows = conn.execute(
        "SELECT id, kind, model, batch, started_at, readings, cost_eur FROM model_run"
        " WHERE substr(started_at, 1, 10) BETWEEN ? AND ? ORDER BY started_at, id", (since, until)).fetchall()
    return [Run(r["id"], r["kind"], r["model"], r["started_at"], r["readings"], r["cost_eur"], bool(r["batch"]))
            for r in rows]


def _usage_tokens(raw) -> Tokens | None:
    """A stored usage (JSON text or dict) as Tokens; None when the provider sent no counts."""
    try:
        usage = json.loads(raw) if isinstance(raw, str) else raw
    except ValueError:
        return None
    if not (isinstance(usage, dict) and any(usage.get(k) for k in USAGE_KEYS)):
        return None
    return Tokens(*(float(usage.get(k) or 0) for k in USAGE_KEYS))


def eval_runs(results: Path) -> list[Run]:
    """Every eval run under `results` (evals/results/), costed from its own readings at the
    standard rate: an eval calls the model one posting at a time, never as a batch. A run
    whose files cannot be read is skipped, so a broken folder never stops the page."""
    out = []
    for summary in sorted(results.glob("*/summary.json")):
        try:
            meta = json.loads(summary.read_text())["meta"]
            lines = (summary.parent / "predictions.jsonl").read_text().splitlines()
        except (OSError, ValueError, KeyError, TypeError):
            continue
        model, cost, n = meta.get("model", ""), 0.0, 0
        for line in lines:
            try:
                tokens = _usage_tokens(json.loads(line).get("usage"))
            except (ValueError, AttributeError):
                continue
            if tokens is not None:
                cost += price_eur(tokens, model)
                n += 1
        run_id = meta.get("run_id") or summary.parent.name
        try:
            stamp = run_id[:16]   # 20261125T091600Z
            started = f"{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}T{stamp[9:11]}:{stamp[11:13]}:{stamp[13:15]}Z"
            date.fromisoformat(started[:10])
        except ValueError:
            continue
        out.append(Run(None, EVAL, model, started, n, cost, label=run_id))
    return out


@dataclass(frozen=True)
class DayKind:
    day: str
    kind: str
    runs: int
    readings: int
    cost_eur: float
    over: bool                # one of its runs was above RUN_ALERT_EUR

    @property
    def per_posting(self) -> float | None:
        return self.cost_eur / self.readings if self.readings else None


def by_day_and_kind(rows: list[Run]) -> list[DayKind]:
    """Runs added up per day and kind, newest day first, kinds in KIND_WORDS order. Pure."""
    groups: dict[tuple[str, str], list[Run]] = {}
    for r in rows:
        groups.setdefault((r.day, r.kind), []).append(r)
    order = {k: i for i, k in enumerate(KIND_WORDS)}
    keys = sorted(groups, key=lambda k: order.get(k[1], len(order)))   # kinds in order ...
    keys.sort(key=lambda k: k[0], reverse=True)                         # ... within newest day first
    return [DayKind(d, k, len(groups[d, k]), sum(r.readings for r in groups[d, k]),
                    sum(r.cost_eur for r in groups[d, k]),
                    any(r.cost_eur > RUN_ALERT_EUR for r in groups[d, k])) for d, k in keys]


@dataclass(frozen=True)
class ModelCost:
    model: str
    readings: int
    first_day: str
    last_day: str
    eur_per_reading: float


def per_model(conn: sqlite3.Connection, since: str) -> list[ModelCost]:
    """Cost per posting read, per model, over the readings on record since `since`
    (YYYY-MM-DD), oldest model first. Priced at the batch rate the daily collection and
    re-reads pay: the record does not say which readings went as a batch, and nearly all
    of them did. This is the before and after of a model switch."""
    acc: dict[str, list] = {}
    for row in conn.execute("SELECT model, usage, created_at FROM extraction_log WHERE created_at >= ?"
                            " ORDER BY created_at", (since,)):
        tokens = _usage_tokens(row["usage"])
        if tokens is None:
            continue
        a = acc.setdefault(row["model"], [0, 0.0, row["created_at"][:10], row["created_at"][:10]])
        a[0] += 1
        a[1] += price_eur(tokens, row["model"], batch=True)
        a[3] = row["created_at"][:10]
    return [ModelCost(m, n, first, last, eur / n) for m, (n, eur, first, last) in acc.items()]


def over_alert(rows: list[Run], threshold: float = RUN_ALERT_EUR) -> list[Run]:
    """The runs that cost more than `threshold`. Pure."""
    return [r for r in rows if r.cost_eur > threshold]


def week_text(rows: list[Run], start: str, end: str) -> str:
    """The Monday summary's line: the week's model spend, split by kind, and the cost per
    posting of the daily collection. Pure; `rows` are the week's runs, eval runs included."""
    total = sum(r.cost_eur for r in rows)
    head = f"Model spend {start} to {end}: €{total:.2f}"
    if not rows:
        return head + " (no model runs recorded).\n"
    split: dict[str, float] = {}
    for r in rows:
        split[r.kind] = split.get(r.kind, 0.0) + r.cost_eur
    parts = ", ".join(f"{KIND_WORDS.get(k, k)} €{split[k]:.2f}" for k in KIND_WORDS if k in split)
    polls = [r for r in rows if r.kind == POLL]
    read = sum(r.readings for r in polls)
    per = (f"; the daily collection paid €{sum(r.cost_eur for r in polls) / read:.4f} a posting read"
           if read else "")
    over = over_alert(rows)
    alert = (f" {len(over)} run{'' if len(over) == 1 else 's'} cost more than the €{RUN_ALERT_EUR:.0f} alert."
             if over else "")
    return f"{head} ({parts}){per}.{alert}\n"


def week_rows(conn: sqlite3.Connection, start: str, end: str, results: Path | None) -> list[Run]:
    """The week's recorded runs plus the eval runs whose result files are dated in it."""
    evals = [r for r in eval_runs(results) if start <= r.day <= end] if results else []
    return sorted(runs(conn, start, end) + evals, key=lambda r: r.started_at)


def days_before(day: str, n: int) -> str:
    return (date.fromisoformat(day) - timedelta(days=n)).isoformat()
