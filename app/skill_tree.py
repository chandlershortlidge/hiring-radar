"""Skill tree: the co-occurrence graph of the filtered job set, reduced to one radial tree.

Does: count, over the jobs the filters describe, how many mention each skill and how many
require it; drop the skills too rare to place; give every remaining skill a parent — the
more common skill its own jobs nearly always also ask for — and a position on a radial
layout drawn outward from a single centre.

Does NOT: read the taxonomy (a parent here comes from the market, not from
taxonomy/skills.json), draw anything, or honour the `requirement` and `skill_ids` filters.
Every node carries the required *and* the mentioned share, so there is nothing for a
requirement filter to choose, and the tree maps the whole filtered market rather than a
selection.

Depth is prevalence: the skills in most postings sit near the centre, the ~3% ones on the
rim. Direction comes from the conditional-probability asymmetry between two skills, read
in the direction that keeps the common skills at the trunk: when P(a|b) is high and
P(b|a) is low, b's jobs nearly all want a but not the other way round, a is the more
common of the two, and so a is the parent. (HIR-81's worked example names the rarer skill
as the parent; that reading puts Snowflake above Python and no longer has a trunk.)

Invariants:
  * Every edge runs from a strictly more prevalent skill to a less prevalent one, so the
    parent relation is a subset of a strict order and the result is always a forest — a
    cycle cannot be built.
  * Both percentages on a node share one denominator: the jobs in the filtered set.
  * build_tree is a pure function of the counts, so one corpus always draws one picture;
    every tie is broken by skill id rather than by dict order.
"""

import math
import sqlite3
from collections import Counter

from app.queries import Filters, job_set_clause

# A skill needs this many jobs mentioning it before it can be a node. Below that its
# conditional probabilities are one odd stack of skills, not a market signal — the reason
# queries.MIN_CO_JOBS exists, at the same threshold.
MIN_JOBS = 5
# How many nodes the picture holds before it stops being readable, taken by mention count.
# Every node carries a two-line label, and past about thirty of them on one circle the
# labels start landing on each other at the width the card gives the drawing.
MAX_NODES = 30
# An edge is drawn only when the child's jobs ask for the parent at least this often.
# Below it, nothing in the market really leads from the parent to the child, and the child
# becomes a branch of its own off the centre.
MIN_CONDITIONAL = 0.6

# Layout, in SVG user units: one ring per depth, RING apart, with PAD of room outside the
# outermost ring for labels. Angle 0 is straight up and grows clockwise.
RING = 115
PAD = 110


def fetch_jobs(conn: sqlite3.Connection, f: Filters, now: str) -> tuple[int, list[tuple[set, set]]]:
    """(jobs in the filtered set, one (mentioned, required) skill-id pair per job with mentions).

    The thin I/O half: `total` counts every job in the set, including the ones with no
    mentions at all, because it is the denominator both percentages are taken over.
    """
    jc, jp = job_set_clause(f, now)
    total = conn.execute(f"SELECT count(*) FROM job j WHERE {jc}", jp).fetchone()[0]
    per: dict[int, tuple[set, set]] = {}
    for r in conn.execute(
            f"SELECT m.job_id, m.skill_id, m.requirement FROM skill_mention m"
            f" JOIN job j ON j.id = m.job_id WHERE {jc}", jp):
        mentioned, required = per.setdefault(r["job_id"], (set(), set()))
        mentioned.add(r["skill_id"])
        if r["requirement"] == "required":
            required.add(r["skill_id"])
    return total, [per[k] for k in sorted(per)]


def _counts(jobs: list[tuple[set, set]]) -> tuple[Counter, Counter, Counter]:
    """Mentions per skill, requirements per skill, and co-mentions per unordered pair."""
    mentioned: Counter = Counter()
    required: Counter = Counter()
    co: Counter = Counter()
    for m, r in jobs:
        mentioned.update(m)
        required.update(r)
        ordered = sorted(m)
        for i, a in enumerate(ordered):
            for b in ordered[i + 1:]:
                co[(a, b)] += 1
    return mentioned, required, co


def _pick_parents(order: list[str], mentioned: Counter, co: Counter,
                  min_conditional: float) -> dict[str, tuple[str, float]]:
    """{child: (parent, P(parent|child))} for every node that clears min_conditional.

    `order` is the nodes by prevalence desc, id asc. A candidate parent has to be
    *strictly* more prevalent than the child — equally common skills have equal
    conditional probabilities in both directions, so neither can claim to lead to the
    other — and among the candidates the winner is the one the child's jobs ask for most
    often. Since a parent is always strictly more prevalent, no cycle can close.
    """
    parents: dict[str, tuple[str, float]] = {}
    for i, child in enumerate(order):
        best: tuple[int, float, int, str] | None = None
        for j, cand in enumerate(order[:i]):
            if mentioned[cand] <= mentioned[child]:
                continue
            shared = co[(cand, child) if cand < child else (child, cand)]
            p = shared / mentioned[child]
            if p < min_conditional:
                continue
            # The *least* prevalent qualifying candidate wins: the most specific skill
            # the child's jobs still nearly always ask for. Taking the most prevalent one
            # instead makes every node a child of Python — the specialization paths are
            # the whole point, so the parent is the nearest gateway above the child, not
            # the trunk. A tie goes to the more-asked-for candidate, then (via its
            # position in `order`, which breaks equal counts by id) to the lower id.
            key = (-mentioned[cand], p, -j, cand)
            if best is None or key > best:
                best = key
        if best is not None:
            parents[child] = (best[3], best[1])
    return parents


def _layout(roots: list[str], children: dict[str, list[str]]) -> tuple[dict[str, float], dict[str, int]]:
    """({node: angle in degrees}, {node: depth}) for a radial tree drawn outward.

    Every leaf gets an equal slice of the full circle, so sibling subtrees never overlap
    and a wide branch gets the room its leaves need. (Weighting a leaf's slice by 1/depth
    to equalize arc *length* instead of angle is tempting — an inner ring is shorter — but
    it squeezes exactly the long branches that carry the picture, and reads worse.)

    A branch sits at the middle of the arc its own children occupy rather than of the
    slice its leaves span: with an unbalanced subtree the two differ, and only the first
    keeps a parent in front of its children instead of off to one side with its edges
    reaching back across the picture.
    """
    leaves: dict[str, int] = {}

    def count(n: str) -> int:
        if n not in leaves:
            kids = children.get(n, [])
            leaves[n] = sum(count(k) for k in kids) if kids else 1
        return leaves[n]

    span = sum(count(r) for r in roots) or 1
    step = 360.0 / span
    angle: dict[str, float] = {}
    depth: dict[str, int] = {}

    def place(n: str, start: float, d: int) -> None:
        depth[n] = d
        kids = children.get(n, [])
        if not kids:
            angle[n] = (start + 0.5) * step      # a leaf owns exactly one slice
            return
        at = start
        for k in kids:
            place(k, at, d + 1)
            at += count(k)
        angle[n] = (angle[kids[0]] + angle[kids[-1]]) / 2

    at = 0.0
    for r in roots:
        place(r, at, 1)
        at += count(r)
    return angle, depth


def build_tree(total: int, jobs: list[tuple[set, set]], min_jobs: int = MIN_JOBS,
               max_nodes: int = MAX_NODES, min_conditional: float = MIN_CONDITIONAL) -> dict:
    """The whole tree as plain data, positions included — see the module docstring.

    Returns {'total', 'size', 'centre': {'x','y'}, 'nodes': [...], 'edges': [...]}.
    A node's `parent` is None when it is a branch off the centre; its `parent_share` is
    P(parent|node), the number that earned the edge. Edges carry their own endpoints and
    a ready-made SVG `path`, so the drawing side never does arithmetic.
    """
    mentioned, required, co = _counts(jobs)
    order = sorted((s for s in mentioned if mentioned[s] >= min_jobs),
                   key=lambda s: (-mentioned[s], s))[:max_nodes]
    parents = _pick_parents(order, mentioned, co, min_conditional)
    children: dict[str, list[str]] = {}
    for child in order:
        if child in parents:
            children.setdefault(parents[child][0], []).append(child)
    for kids in children.values():
        kids.sort(key=lambda s: (-mentioned[s], s))
    roots = [s for s in order if s not in parents]
    angle, depth = _layout(roots, children) if roots else ({}, {})

    max_depth = max(depth.values(), default=1)
    size = 2 * (RING * max_depth + PAD)
    cx = cy = size / 2

    def point(r: float, deg: float) -> tuple[float, float]:
        t = math.radians(deg)
        return round(cx + r * math.sin(t), 1), round(cy - r * math.cos(t), 1)

    def xy(n: str) -> tuple[float, float]:
        return point(RING * depth[n], angle[n])

    def edge_path(child: str, parent: str | None) -> str:
        """The SVG path of one edge: along the parent's ring to the child's angle, then
        straight outward. A straight chord between the two points would cut across the
        branches in between; this never leaves its own wedge. A spoke from the centre has
        no ring to follow and is just a line."""
        x2, y2 = xy(child)
        if parent is None:
            return f"M{cx},{cy} L{x2},{y2}"
        r = RING * depth[parent]
        x0, y0 = point(r, angle[parent])
        if abs(angle[child] - angle[parent]) < 0.01:      # dead ahead: no arc to draw
            return f"M{x0},{y0} L{x2},{y2}"
        xm, ym = point(r, angle[child])
        sweep = 1 if angle[child] > angle[parent] else 0   # angles grow clockwise on screen
        large = 1 if abs(angle[child] - angle[parent]) > 180 else 0
        return f"M{x0},{y0} A{r},{r} 0 {large} {sweep} {xm},{ym} L{x2},{y2}"

    # Every node is placed: the first in `order` has nothing more prevalent above it, so
    # it is always a root, and the rest hang off one.
    nodes = []
    for n in order:
        x, y = xy(n)
        nodes.append({
            "skill_id": n, "mentioned": mentioned[n], "required": required[n],
            "mentioned_pct": round(100 * mentioned[n] / total, 1) if total else 0.0,
            "required_pct": round(100 * required[n] / total, 1) if total else 0.0,
            "depth": depth[n], "angle": round(angle[n], 2), "x": x, "y": y,
            "parent": parents[n][0] if n in parents else None,
            "parent_share": round(parents[n][1], 3) if n in parents else None,
            "children": list(children.get(n, [])),
        })
    nodes.sort(key=lambda s: (s["depth"], s["angle"], s["skill_id"]))

    # One edge per node, in the nodes' own order: the parent edge, or the spoke out of
    # the centre that marks a branch of its own.
    edges = []
    for node in nodes:
        n = node["skill_id"]
        parent = node["parent"]
        x1, y1 = xy(parent) if parent else (cx, cy)
        edges.append({"parent": parent, "child": n, "share": node["parent_share"],
                      "x1": x1, "y1": y1, "x2": node["x"], "y2": node["y"],
                      "path": edge_path(n, parent)})
    return {"total": total, "size": size, "centre": {"x": cx, "y": cy},
            "nodes": nodes, "edges": edges}


def skill_tree(conn: sqlite3.Connection, f: Filters, now: str) -> dict:
    """The I/O wrapper: read the filtered job set, then lay it out."""
    return build_tree(*fetch_jobs(conn, f, now))
