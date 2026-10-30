"""Skill tree: the co-occurrence graph of the filtered job set, reduced to one radial tree.

Does: count, over the jobs the filters describe, how many mention each skill and how many
require it; drop the skills too rare to place; give every remaining skill a parent — the
more common skill its own jobs nearly always also ask for — and then every coordinate the
drawing needs: ring position, node and core radius, which branch it reads as part of, and
a spot for its name that overlaps nothing.

Does NOT: read the taxonomy (a parent here comes from the market, not from
taxonomy/skills.json; display names are passed in, for their widths), draw anything, or
honour the `requirement` and `skill_ids` filters.
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
  * build_tree is a pure function of the counts and the display names, so one corpus
    always draws one picture; every tie is broken by skill id rather than by dict order.
  * No two labels overlap, and none leaves the box — `_place_labels` holds that, and
    `label_placed` is False on any node it could not manage.
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
PAD = 150

# Everything below is sized against a 1000-unit reference box and scaled to the box the
# tree actually needs, so a node and its label stay the same size on screen however deep
# the tree goes. (Growing RING on its own changes nothing: the box grows with it.)
NAME_SIZE = 13          # the node's name, the only thing written on the drawing
TIP_SIZE = 11           # the two shares, which live in the hover/focus tooltip
LINE_H = 1.35
LABEL_GAP = 7           # from the edge of a node's circle to the start of its name
MIN_R, MAX_R = 6, 26    # node radius: area carries the mentioned share
MIN_BAND = 4            # the thinnest ring band drawn when required < mentioned
HUB_R = 23
# How far a label may slide to get out of the way, in half-label steps. Running out of
# steps means the drawing is too crowded for its node count — lower MAX_NODES rather than
# raise this, and the label test will say so.
MAX_LABEL_STEPS = 14

# Branch colour. A branch is a subtree big enough to read as its own path. Splitting stops
# once no branch holds more than TRUNK_SHARE of the nodes; the heads that were split are
# the trunk and stay neutral. Only BRANCH_HUES of them can be coloured: a tree shows every
# branch at once, and the dataviz palette validates at most three hues for an all-pairs
# form (four fail the normal-vision floor). The rest stay neutral — the skill's own "past
# three, fold to Other" rule. See DECISIONS 2026-10-30, "The skill tree, made readable".
TRUNK_SHARE = 0.5
BRANCH_HUES = 3
# A lone leaf never takes a hue off a real lobe, however the sizes tie.
MIN_BRANCH = 2

# Rough text metrics. Python has no font metrics, so a label's width is estimated per
# character and deliberately *over*-estimated: a label that fits by this measure fits in
# the browser too, which is what makes the no-overlap test a guarantee rather than a
# coincidence.
_WIDE = set("mwMW@%")
_NARROW = set("iljtfrI.,;:'|!()[] ")
# The tooltip is set in the mono face, where every glyph is one advance wide — the
# proportional estimate above badly under-measures it and the box would clip its own text.
MONO_W = 0.63


def _mono_width(text: str, size: float) -> float:
    return len(text) * MONO_W * size


def _text_width(text: str, size: float) -> float:
    w = 0.0
    for ch in text:
        if ch in _WIDE:
            w += 0.95
        elif ch in _NARROW:
            w += 0.40
        elif ch.isupper() or ch.isdigit():
            w += 0.68
        else:
            w += 0.60
    return w * size


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
    other — and it has to be one the child's jobs ask for at least min_conditional of the
    time. Among those, the winner is the *least* prevalent: the nearest gateway above the
    child rather than the trunk far above it. A tie goes to the candidate the child's jobs
    ask for most often. Since a parent is always strictly more prevalent, no cycle can close.
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


def _subtree_sizes(order: list[str], children: dict[str, list[str]]) -> dict[str, int]:
    size: dict[str, int] = {}

    def walk(n: str) -> int:
        if n not in size:
            size[n] = 1 + sum(walk(k) for k in children.get(n, []))
        return size[n]

    for n in order:
        walk(n)
    return size


def _pick_branches(roots: list[str], children: dict[str, list[str]], order: list[str],
                   trunk_share: float = TRUNK_SHARE, hues: int = BRANCH_HUES,
                   min_branch: int = MIN_BRANCH) -> tuple[dict[str, str], dict[str, int]]:
    """({node: the branch head it belongs to}, {branch head: hue index}).

    One hue per *root* is useless here: the tree normally has a single root (python) with
    one child holding most of the nodes, so every node would be the same colour. Instead
    the biggest branch is split into its children, repeatedly, until none holds more than
    trunk_share of the tree. The heads that were split are the trunk: they belong to no
    branch and are left out of both maps, which is what makes them neutral.

    Only the `hues` largest branches get an index, and a branch under `min_branch` nodes
    never does — a single leaf taking a hue off a real lobe reads as a mistake. Ties go by
    skill id, so one corpus always draws one picture.
    """
    size = _subtree_sizes(order, children)
    total = len(order)
    heads = list(roots)
    while heads:
        heads.sort(key=lambda h: (-size[h], h))
        big = heads[0]
        if size[big] <= trunk_share * total or not children.get(big):
            break
        heads = heads[1:] + list(children[big])
    heads.sort(key=lambda h: (-size[h], h))

    branch: dict[str, str] = {}

    def mark(n: str, head: str) -> None:
        branch[n] = head
        for k in children.get(n, []):
            mark(k, head)

    for h in heads:
        mark(h, h)
    big_enough = [h for h in heads if size[h] >= min_branch]
    return branch, {h: i for i, h in enumerate(big_enough[:hues])}


def _place_labels(nodes: list[dict], cx: float, size: float, font: float,
                  obstacles: list[tuple[float, float, float, float]]) -> None:
    """Give every node a label box that touches nothing else, in place.

    A name sits beside its node, on the side of the picture the node is on. Where that
    spot is taken — by another name, by a node, or by the hub — it slides up or down in
    half-label steps until it is clear, and a leader line is drawn so it stays obvious
    which node it belongs to. Boxes are tested in two dimensions, so names at different
    depths are not pushed apart when they never met in the first place.

    Nodes are placed most-prevalent first: the skills a reader goes looking for keep their
    natural spot, and the rare ones do the moving.
    """
    h = font * LINE_H
    step = h * 0.55
    offsets = [0.0]
    for i in range(1, MAX_LABEL_STEPS + 1):
        offsets += [i * step, -i * step]
    placed = list(obstacles)

    def free(box):
        x0, y0, x1, y1 = box
        if x0 < 0 or y0 < 0 or x1 > size or y1 > size:
            return False
        return not any(x0 < b[2] and b[0] < x1 and y0 < b[3] and b[1] < y1 for b in placed)

    for n in sorted(nodes, key=lambda n: (-n["mentioned"], n["skill_id"])):
        w = _text_width(n["display"], font)
        gap = LABEL_GAP * (font / NAME_SIZE)
        sides = [1, -1] if n["x"] >= cx else [-1, 1]
        best, best_side = None, sides[0]
        for side in sides:                 # the node's own side first, the other as relief
            x0 = n["x"] + n["r"] + gap if side > 0 else n["x"] - n["r"] - gap - w
            for d in offsets:
                box = (x0, n["y"] + d - h / 2, x0 + w, n["y"] + d + h / 2)
                if free(box):
                    best, best_side = box, side
                    break
            if best:
                break
        if best is None:                   # too crowded to place: leave it where it lands
            side = sides[0]
            x0 = n["x"] + n["r"] + gap if side > 0 else n["x"] - n["r"] - gap - w
            best, best_side = (x0, n["y"] - h / 2, x0 + w, n["y"] + h / 2), side
            n["label_placed"] = False
        else:
            n["label_placed"] = True
        placed.append(best)
        cy_label = (best[1] + best[3]) / 2
        n["label_x"] = round(best[0] if best_side > 0 else best[2], 1)
        n["label_y"] = round(cy_label + font * 0.35, 1)      # baseline, optically centred
        n["label_anchor"] = "start" if best_side > 0 else "end"
        moved = abs(cy_label - n["y"]) > 1 or best_side != (1 if n["x"] >= cx else -1)
        n["leader"] = (f"M{round(n['x'] + best_side * n['r'], 1)},{n['y']}"
                       f" L{round(n['label_x'] - best_side * 3, 1)},{round(cy_label, 1)}") if moved else None


def build_tree(total: int, jobs: list[tuple[set, set]], display: dict[str, str] | None = None,
               min_jobs: int = MIN_JOBS, max_nodes: int = MAX_NODES,
               min_conditional: float = MIN_CONDITIONAL) -> dict:
    """The whole tree as plain data, every coordinate included — see the module docstring.

    Returns {'total', 'size', 'font', 'centre', 'nodes', 'edges'}. A node's `parent` is
    None when it is a branch off the centre; `parent_share` is P(parent|node), the number
    that earned the edge. `branch` names the subtree it reads as part of (None for the
    trunk) and `branch_index` is its hue slot, set on only the largest few. `r` and
    `core_r` are the two circles — area carries the mentioned share, the core the required
    one. `label_*` and `leader` are where the name goes once nothing overlaps, and `tip`
    is the hover/focus tooltip's own box and lines.

    `display` maps skill ids to the names actually drawn; a label's width depends on them,
    so the layout cannot be computed without them. Missing ids fall back to the id.

    Everything is in the user units of the returned `size` box, so the drawing side never
    does arithmetic of its own.
    """
    display = display or {}
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
    # Scale the reference sizes to this box (see NAME_SIZE), so type and nodes stay put on
    # screen however deep the tree runs.
    k = size / 1000
    font, tip_font = NAME_SIZE * k, TIP_SIZE * k
    branch, branch_index = _pick_branches(roots, children, order)
    max_pct = max((mentioned[n] for n in order), default=0)

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

    def node_r(n: str) -> float:
        """Area carries the share, so a skill in twice as many postings draws twice the ink."""
        return round((MIN_R + (MAX_R - MIN_R) * math.sqrt(mentioned[n] / max_pct)) * k, 1)

    def core_r(n: str, r: float) -> float:
        """The required share of the node's area. Where there is any gap at all, the band
        around the core is held to at least MIN_BAND so it stays visible at a small radius
        — but a skill that is always required keeps a solid, honest circle."""
        share = required[n] / mentioned[n] if mentioned[n] else 0.0
        c = r * math.sqrt(share)
        return round(max(0.0, min(c, r - MIN_BAND * k) if share < 1 else c), 1)

    def tip_box(n: str, x: float, y: float, r: float, m_pct: float, r_pct: float) -> dict:
        """The tooltip that carries the two shares, now that only the name is drawn."""
        lines = [f"mentioned in {mentioned[n]} of {total} jobs · {m_pct}%",
                 f"required in {required[n]} · {r_pct}%"]
        w = max(_mono_width(l, tip_font) for l in lines) + 16 * k
        h = 2 * tip_font * LINE_H + 10 * k
        # Opposite the label, so the tip never covers the name it belongs to.
        tx = x - (r + 8 * k) - w if x >= cx else x + r + 8 * k
        return {"x": round(min(max(tx, 2 * k), size - w - 2 * k), 1),
                "y": round(min(max(y - h / 2, 2 * k), size - h - 2 * k), 1),
                "w": round(w, 1), "h": round(h, 1), "lines": lines}

    # Every node is placed: the first in `order` has nothing more prevalent above it, so
    # it is always a root, and the rest hang off one.
    nodes = []
    for n in order:
        x, y = xy(n)
        r = node_r(n)
        m_pct = round(100 * mentioned[n] / total, 1) if total else 0.0
        r_pct = round(100 * required[n] / total, 1) if total else 0.0
        head = branch.get(n)
        nodes.append({
            "skill_id": n, "display": display.get(n, n),
            "mentioned": mentioned[n], "required": required[n],
            "mentioned_pct": m_pct, "required_pct": r_pct,
            "depth": depth[n], "angle": round(angle[n], 2), "x": x, "y": y,
            "r": r, "core_r": core_r(n, r),
            "branch": head, "branch_index": branch_index.get(head) if head else None,
            "parent": parents[n][0] if n in parents else None,
            "parent_share": round(parents[n][1], 3) if n in parents else None,
            "children": list(children.get(n, [])),
            "tip": tip_box(n, x, y, r, m_pct, r_pct),
        })
    nodes.sort(key=lambda s: (s["depth"], s["angle"], s["skill_id"]))

    # Names last: they have to dodge the nodes and the hub, which are now all placed.
    blocks = [(nd["x"] - nd["r"], nd["y"] - nd["r"], nd["x"] + nd["r"], nd["y"] + nd["r"])
              for nd in nodes]
    hub = HUB_R * k
    blocks.append((cx - hub, cy - hub, cx + hub, cy + hub))
    _place_labels(nodes, cx, size, font, blocks)

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
            "font": round(font, 2), "tip_font": round(tip_font, 2), "hub_r": round(hub, 1),
            "nodes": nodes, "edges": edges}


def skill_tree(conn: sqlite3.Connection, f: Filters, now: str,
               display: dict[str, str] | None = None) -> dict:
    """The I/O wrapper: read the filtered job set, then lay it out."""
    total, jobs = fetch_jobs(conn, f, now)
    return build_tree(total, jobs, display)
