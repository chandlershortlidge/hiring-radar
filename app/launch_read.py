"""What a city launch's first collection reads: the launched city's new jobs, nothing else.

Does: given the jobs a poll just stored, pick the ones placed in the launched city that
still need a reading; count what is left unread (the poll's new jobs elsewhere, and the
older jobs in this copy whose reading is out of date); price the reading with the same
per-reading figure as `python -m app reread-cost` (`reread_cost.cost_of_reading`); and
say whether it is over the launch cap.

Does NOT: poll, call the model, or write anything. `python -m app poll --launch CITY`
(app/__main__.py) does the poll before and the reading after.

Why it exists (HIR-380): a launch's first collection runs on the Mac's copy of the
database, and a plain poll reads every job in the queue — after a prompt change that is
hundreds of older jobs. Those readings stay on the Mac; the server keeps its own database
and does its own re-reading. Twice a launch paid three to four times its estimate for
nothing (Hamburg/Frankfurt/Munich, about €10.50 against €3; San Jose, €6.90 against
€1.73), and the launch cap never saw it coming.

Invariants: the jobs read are a subset of the poll's own new jobs, never the whole queue —
an empty list of new jobs reads nothing.
The three counts are disjoint and together make up the whole queue.
"""

import sqlite3
from dataclasses import dataclass

from app.pipeline import pending_count, pending_jobs
from app.reread_cost import RereadCost, cost_of_reading

# The launch's spending cap, the board policy's own (HIR-132); not this module's to change.
from app.discover import MAX_LAUNCH_COST_EUR


@dataclass
class LaunchRead:
    city: str
    to_read: list[int]       # new jobs in the city that still need a reading
    other_new: int           # new jobs placed elsewhere, left unread
    stale_left: int          # older jobs in this copy waiting for a reading, left unread
    cost: RereadCost

    @property
    def over_cap(self) -> bool:
        return self.cost.eur_total > MAX_LAUNCH_COST_EUR

    def lines(self) -> list[str]:
        n = len(self.to_read)
        out = [f"launch {self.city}: reading {n} new job{'' if n == 1 else 's'} in {self.city}, "
               f"about €{self.cost.eur_total:.2f} (cap €{MAX_LAUNCH_COST_EUR:.0f})"]
        if self.other_new or self.stale_left:
            out.append(f"left unread: {self.other_new} new jobs placed in other cities and "
                       f"{self.stale_left} older jobs waiting for a reading (out of date or never read). "
                       f"This is the "
                       f"Mac's copy of the database; the server reads its own jobs, so reading "
                       f"them here would buy nothing")
        if self.over_cap:
            out.append(f"STOPPED, nothing read: over the €{MAX_LAUNCH_COST_EUR:.0f} launch cap. "
                       f"The jobs stay stored; `python -m app extract` reads them if wanted")
        return out


def plan(conn: sqlite3.Connection, new_job_ids: list[int], city: str, version: str,
         now: str | None = None) -> LaunchRead:
    """Which of `new_job_ids` to read for `city`, and what is left alone. Reads only."""
    queue = pending_count(conn, version, now=now)
    pending_new = [r["id"] for r in pending_jobs(conn, version, job_ids=new_job_ids, now=now)]
    in_city = {r["id"] for r in pending_jobs(conn, version, job_ids=new_job_ids, place=city, now=now)}
    to_read = [i for i in pending_new if i in in_city]
    return LaunchRead(city=city, to_read=to_read, other_new=len(pending_new) - len(to_read),
                      stale_left=queue - len(pending_new),
                      cost=cost_of_reading(conn, len(to_read)))
