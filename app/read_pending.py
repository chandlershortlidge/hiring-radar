"""The one bulk read of a place's or track's waiting jobs (HIR-396).

Does: given a city, a career track or both, list the stored jobs there that still need a
reading at the current extractor, including the ones a read-later setting (app/scope.py)
has been holding back; price reading them with the same per-reading figure as
`python -m app reread-cost` (`reread_cost.cost_of_reading`, batch prices); and say whether
that is over the cap the caller gave.

Does NOT: call the model or write anything. `python -m app read-pending` (app/__main__.py)
prints the plan and then hands its job ids to the pipeline as one batch. It does not change
a read-later setting either: that is a line in app/scope.py, changed by hand once the bulk
read is done.

Why it exists: a new career track is collected for weeks before its skill list exists.
Reading those postings as they arrive, with a skill list that does not cover them, is paid
for twice. They are stored unread instead, and read once, here, when the list is ready.

Invariants: the jobs are a subset of the queue with held jobs included
(`pipeline._pending_clause(include_held=True)`), so nothing already read at this version
is read again. Asked by city alone, jobs on a read-later track are left out and counted:
their skill list is what is still missing, and naming the track reads them. A plan with no
cap is never over it; the command refuses a real run without one.
"""

import sqlite3
from dataclasses import dataclass

from app import scope
from app.pipeline import _pending_clause
from app.reread_cost import RereadCost, cost_of_reading


@dataclass
class PendingRead:
    what: str                # "Chicago", "research", or "research in Chicago"
    to_read: list[int]       # the waiting jobs, oldest first
    left_for_track: int      # in the city, on a track still set to read later: left out
    cost: RereadCost
    cap: float | None        # euros; None when only the count and cost were asked for

    @property
    def over_cap(self) -> bool:
        return self.cap is not None and self.cost.eur_total > self.cap

    def lines(self) -> list[str]:
        n = len(self.to_read)
        cap = "" if self.cap is None else f" (cap €{self.cap:.2f})"
        how = "" if self.cost.measured else ", an estimate: too few stored readings to measure from"
        out = [f"read-pending {self.what}: {n} job{'' if n == 1 else 's'} waiting to be read, "
               f"about €{self.cost.eur_total:.2f} as one batch{cap}{how}"]
        if self.left_for_track:
            out.append(f"left out: {self.left_for_track} more on a career track still set to read "
                       f"later ({', '.join(scope.read_later_tracks())}); name the track with "
                       f"--family to read them")
        if self.over_cap:
            out.append(f"STOPPED, nothing read: over the €{self.cap:.2f} cap. The jobs stay stored")
        return out


def plan(conn: sqlite3.Connection, version: str, city: str | None = None, family: str | None = None,
         cap: float | None = None, now: str | None = None) -> PendingRead:
    """Which jobs a bulk read of `city` and/or `family` would read, and what it costs.
    Reads only. Raises ValueError on a place or track that is not collected."""
    if not city and not family:
        raise ValueError("read-pending: name a place with --city or a career track with --family")
    if city and city not in scope.places():
        raise ValueError(f"{city!r} is not a collected place; one of: {', '.join(scope.places())}")
    if family and family not in scope.tracks():
        raise ValueError(f"{family!r} is not a career track; one of: {', '.join(scope.tracks())}")
    where, params = _pending_clause(version, now, include_held=True)
    if city:
        where += " AND EXISTS (SELECT 1 FROM job_place rp WHERE rp.job_id = j.id AND rp.place = ?)"
        params.append(city)
    if family:
        where += " AND j.family = ?"
        params.append(family)
    rows = conn.execute(f"SELECT j.id, j.family FROM job j WHERE {where} ORDER BY j.id", params).fetchall()
    skip = set() if family else set(scope.read_later_tracks())
    to_read = [r["id"] for r in rows if r["family"] not in skip]
    what = f"{family} in {city}" if city and family else (family or city)
    return PendingRead(what=what, to_read=to_read, left_for_track=len(rows) - len(to_read),
                       cost=cost_of_reading(conn, len(to_read)), cap=cap)
