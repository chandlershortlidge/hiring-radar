"""Credit stored jobs, open and closed, with every tracked city their location names (HIR-331).

Does: read each stored job's location through `geo.places_of`, the matching ingest uses,
and add the `job_place` rows for tracked cities it is missing. A posting stored as "Berlin,
London" before London was a city has a Berlin row only; once London is in `geo.CITIES`,
this gives it a London row too. `discover-boards --launch CITY` runs it for that city.

Does NOT: remove a place, change `job.city`, add "Remote (EU)" (judged from the whole
posting under rules that have changed since some jobs were stored), call a model, or read
the location of a sighting merged into a job (only the first sighting's location is
stored). Safe to run twice: the second run adds nothing.

Rule: decisions/2026-11-19-hir-331-city-history-includes-stored-jobs.md.
"""

import sqlite3
from dataclasses import dataclass, field

from app.geo import CITIES, places_of

EXAMPLES = 3          # jobs shown per city
MANY_CITIES = 3       # a job gaining more than this many cities at once is listed for a look


@dataclass
class Gain:
    job_id: int
    company: str | None
    title: str | None
    location_raw: str | None
    cities: list[str]


@dataclass
class Backfill:
    gains: list[Gain] = field(default_factory=list)
    applied: bool = False

    def per_city(self) -> dict[str, list[Gain]]:
        out: dict[str, list[Gain]] = {}
        for g in self.gains:
            for c in g.cities:
                out.setdefault(c, []).append(g)
        return {c: out[c] for c in CITIES if c in out}

    def many(self) -> list[Gain]:
        return [g for g in self.gains if len(g.cities) > MANY_CITIES]

    def counts(self) -> dict[str, int]:
        return {c: len(gs) for c, gs in self.per_city().items()}


def backfill(conn: sqlite3.Connection, city: str | None = None, apply: bool = True) -> Backfill:
    """Find, and unless apply=False add, the city rows stored jobs are missing.
    `city` limits it to one tracked city; ValueError for a name not in geo.CITIES."""
    if city is not None and city not in CITIES:
        raise ValueError(f"{city!r} is not a tracked city (geo.CITIES)")
    have: dict[int, set[str]] = {}
    for r in conn.execute("SELECT job_id, place FROM job_place"):
        have.setdefault(r[0], set()).add(r[1])
    result = Backfill(applied=apply)
    for r in conn.execute("SELECT id, company, title, location_raw, description_text FROM job ORDER BY id"):
        named = [p for p in places_of(r["location_raw"], r["title"], r["description_text"])
                 if p in CITIES and (city is None or p == city)]
        missing = [p for p in named if p not in have.get(r["id"], set())]
        if missing:
            result.gains.append(Gain(r["id"], r["company"], r["title"], r["location_raw"], missing))
    if apply and result.gains:
        with conn:
            conn.executemany("INSERT OR IGNORE INTO job_place (job_id, place) VALUES (?, ?)",
                             [(g.job_id, c) for g in result.gains for c in g.cities])
    return result


def _show(g: Gain) -> str:
    return f"job {g.job_id}: {g.company or '?'} — {g.title or '?'} ({g.location_raw})"


def report_lines(b: Backfill, city: str | None = None) -> list[str]:
    scope = city or "every tracked city"
    if not b.gains:
        return [f"stored jobs: none gained {scope}; nothing to add"]
    verb = "gained" if b.applied else "would gain"
    lines = [f"stored jobs (open and closed) that {verb} a city their location names"
             + ("" if b.applied else " — dry run, nothing written") + ":"]
    for c, gs in b.per_city().items():
        lines.append(f"  {c}: {len(gs)}")
        lines += [f"    {_show(g)}" for g in gs[:EXAMPLES]]
    many = b.many()
    if many:
        lines.append(f"jobs gaining more than {MANY_CITIES} cities at once, for a look:")
        lines += [f"  {_show(g)} +{', '.join(g.cities)}" for g in many]
    return lines
