"""Draw unread postings to build a skill list from (HIR-396).

Does: list the stored postings of a career track and/or a place that the model has never
read, and pick `n` of them spread across places and employers, so the sample is not forty
postings from the one company with the biggest board. Seeded: the same database and seed
pick the same postings.

Does NOT: call a model, write to the database, or label anything. It hands the labellers
the posting texts; building the skill list and the Goldens from them is their work. It is
not the Golden sampler (`pick` in scripts/agent_label.py): that one spreads over seniority
and source, which only a posting the model has read carries, and it lives in a script this
package does not import.

Invariants: only never-read postings are drawn (a posting already read is not what a new
skill list is built from); legacy imports are never drawn; a sample smaller than asked is
returned as it is, with the number available, never padded.
"""

import random
import sqlite3

from app import scope


def unread(conn: sqlite3.Connection, family: str | None = None, city: str | None = None) -> list[dict]:
    """The never-read postings of `family` and/or `city`, oldest first, each with every
    place it is posted for. Raises ValueError on a place or track that is not collected."""
    if not family and not city:
        raise ValueError("sample: name a career track with --family or a place with --city")
    if family and family not in scope.tracks():
        raise ValueError(f"{family!r} is not a career track; one of: {', '.join(scope.tracks())}")
    if city and city not in scope.places():
        raise ValueError(f"{city!r} is not a collected place; one of: {', '.join(scope.places())}")
    where, params = "j.extracted_version IS NULL", []
    if family:
        where += " AND j.family = ?"
        params.append(family)
    if city:
        where += " AND EXISTS (SELECT 1 FROM job_place sp WHERE sp.job_id = j.id AND sp.place = ?)"
        params.append(city)
    rows = conn.execute(
        "SELECT j.id, j.company, j.title, j.family, j.first_seen, j.description_text,"
        " (SELECT GROUP_CONCAT(place, '|') FROM (SELECT place FROM job_place sp"
        "   WHERE sp.job_id = j.id ORDER BY place)) AS places"
        f" FROM job j WHERE {where} ORDER BY j.id", params).fetchall()
    return [{"job_id": r["id"], "company": r["company"], "title": r["title"], "family": r["family"],
             "places": r["places"].split("|") if r["places"] else [], "first_seen": r["first_seen"],
             "text": r["description_text"]} for r in rows]


def spread(postings: list[dict], n: int, seed: int = 0) -> list[dict]:
    """Pure: up to `n` of `postings`, one from each (place, employer) in turn before a
    second from any, in a seeded order; returned sorted by job id."""
    rng = random.Random(seed)
    pool = sorted(postings, key=lambda p: p["job_id"])
    rng.shuffle(pool)
    groups: dict[tuple, list[dict]] = {}
    for p in pool:
        groups.setdefault(((p["places"] or ["?"])[0], (p["company"] or "").lower()), []).append(p)
    order = sorted(groups)
    rng.shuffle(order)
    picked: list[dict] = []
    while len(picked) < n and any(groups[k] for k in order):
        for k in order:
            if len(picked) >= n:
                break
            if groups[k]:
                picked.append(groups[k].pop(0))
    return sorted(picked, key=lambda p: p["job_id"])
