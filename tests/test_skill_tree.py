import math

import pytest

from app import db, queries as q
from app.skill_tree import (MIN_JOBS, PAD, RING, build_tree, fetch_jobs, skill_tree)
from tests.test_queries import NOW, RELATED_JOBS, add, ts


def corpus(rows):
    """[[skill | (skill, requirement), ...], ...] → the (mentioned, required) pairs build_tree takes."""
    out = []
    for row in rows:
        mentioned, required = set(), set()
        for item in row:
            sid, req = item if isinstance(item, tuple) else (item, "required")
            mentioned.add(sid)
            if req == "required":
                required.add(sid)
        out.append((mentioned, required))
    return out


# 20 jobs nesting python ⊃ llms ⊃ rag ⊃ snowflake, so every conditional up the chain is 1.0.
# Snowflake is mentioned in 6 and required in 1: Leoson's résumé-keyword-vs-gate gap.
CHAIN = corpus(
    [["python", "llms", "rag", "snowflake"]]
    + [["python", "llms", "rag", ("snowflake", "nice_to_have")]] * 5
    + [["python", "llms", "rag"]] * 4
    + [["python", "llms"]] * 4
    + [["python"]] * 6)


def tree(jobs, total=None, **kw):
    return build_tree(total if total is not None else len(jobs), jobs, **kw)


def nodes_by_id(t):
    return {n["skill_id"]: n for n in t["nodes"]}


def test_the_parent_is_the_nearest_gateway_not_the_trunk():
    """The regression that matters: every conditional in CHAIN is 1.0, so picking the most
    prevalent qualifying parent would hang llms, rag and snowflake all off python. The
    specialization path is the feature, so each node takes the *least* prevalent parent."""
    by = nodes_by_id(tree(CHAIN))
    assert [(n, by[n]["parent"], by[n]["depth"]) for n in ("python", "llms", "rag", "snowflake")] == [
        ("python", None, 1), ("llms", "python", 2), ("rag", "llms", 3), ("snowflake", "rag", 4)]
    assert by["python"]["children"] == ["llms"]


def test_both_shares_share_the_job_set_denominator():
    # 30 jobs in the filter set, 10 of them with no mention at all: still the denominator.
    by = nodes_by_id(tree(CHAIN, total=30))
    assert (by["snowflake"]["mentioned"], by["snowflake"]["required"]) == (6, 1)
    assert (by["snowflake"]["mentioned_pct"], by["snowflake"]["required_pct"]) == (20.0, 3.3)
    assert (by["python"]["mentioned_pct"], by["python"]["required_pct"]) == (66.7, 66.7)


def test_a_skill_under_min_jobs_is_not_a_node():
    jobs = CHAIN + corpus([["python", "cobol"]] * (MIN_JOBS - 1))
    by = nodes_by_id(tree(jobs))
    assert "cobol" not in by
    jobs = CHAIN + corpus([["python", "cobol"]] * MIN_JOBS)
    assert "cobol" in nodes_by_id(tree(jobs))


def test_max_nodes_keeps_the_most_mentioned():
    t = tree(CHAIN, max_nodes=2)
    assert [n["skill_id"] for n in t["nodes"]] == ["python", "llms"]


def test_a_weak_conditional_becomes_its_own_branch():
    """sql sits in 5 jobs, only 2 of which want python: 0.4 is under the threshold, so
    nothing in the market leads from python to sql and sql starts a branch of its own."""
    jobs = CHAIN + corpus([["python", "sql"]] * 2 + [["sql"]] * 3)
    by = nodes_by_id(tree(jobs))
    assert by["sql"]["parent"] is None and by["sql"]["depth"] == 1
    # Loosen the threshold under that share and the same pair becomes an edge.
    by = nodes_by_id(tree(jobs, min_conditional=0.4))
    assert by["sql"]["parent"] == "python"


def test_equally_prevalent_skills_are_never_parent_and_child():
    """Both directions have the same conditional probability, so neither leads to the
    other — there is no asymmetry to read, and both hang off the centre."""
    by = nodes_by_id(tree(corpus([["a", "b"]] * 8)))
    assert [by["a"]["parent"], by["b"]["parent"]] == [None, None]
    assert by["a"]["depth"] == by["b"]["depth"] == 1


def test_every_edge_climbs_in_prevalence_so_the_result_is_a_forest():
    jobs = CHAIN + corpus([["python", "sql"]] * 2 + [["sql"]] * 3 + [["python", "llms", "mlops"]] * 7)
    t = tree(jobs)
    by = nodes_by_id(t)
    for e in t["edges"]:
        if e["parent"] is not None:
            assert by[e["parent"]]["mentioned"] > by[e["child"]]["mentioned"]
    # Walking up from any node reaches a root, which is what "no cycle" means here.
    for n in by:
        seen, at = set(), n
        while by[at]["parent"] is not None:
            assert at not in seen
            seen.add(at)
            at = by[at]["parent"]
    # One edge per node: the parent edge, or the spoke from the centre.
    assert len(t["edges"]) == len(t["nodes"])


def test_the_layout_is_one_ring_per_depth_and_edges_carry_their_endpoints():
    t = tree(CHAIN)
    cx, cy = t["centre"]["x"], t["centre"]["y"]
    by = nodes_by_id(t)
    assert t["size"] == 2 * (RING * 4 + PAD) and cx == cy == t["size"] / 2
    for n in t["nodes"]:
        r = math.hypot(n["x"] - cx, n["y"] - cy)
        assert r == pytest.approx(RING * n["depth"], abs=0.2)
        t_rad = math.radians(n["angle"])
        assert n["x"] == pytest.approx(cx + r * math.sin(t_rad), abs=0.2)
        assert n["y"] == pytest.approx(cy - r * math.cos(t_rad), abs=0.2)
    for e in t["edges"]:
        child = by[e["child"]]
        assert (e["x2"], e["y2"]) == (child["x"], child["y"])
        if e["parent"] is None:
            assert (e["x1"], e["y1"]) == (cx, cy)      # a branch starts at the centre
        else:
            p = by[e["parent"]]
            assert (e["x1"], e["y1"]) == (p["x"], p["y"])


def test_an_edge_follows_the_parents_ring_before_turning_outward():
    """A straight chord from a parent to a child at a different angle would cut across the
    branches between them, so an edge arcs along the parent's ring first."""
    jobs = corpus([["a", "a1"]] * 6 + [["a", "a2"]] * 6 + [["b"]] * 6)
    t = tree(jobs)
    by = nodes_by_id(t)
    edges = {e["child"]: e for e in t["edges"]}
    cx, cy = t["centre"]["x"], t["centre"]["y"]
    # A branch has no ring to follow: a plain spoke out of the centre.
    assert edges["a"]["path"] == f"M{cx},{cy} L{by['a']['x']},{by['a']['y']}"
    assert edges["b"]["path"].startswith(f"M{cx},{cy} L")
    # a1 sits one ring out and to one side of a, so the edge arcs along a's ring (radius
    # RING, a being at depth 1) and only then runs straight out to the child.
    assert edges["a1"]["path"].startswith(f"M{by['a']['x']},{by['a']['y']} A{RING},{RING} 0 0 ")
    assert edges["a1"]["path"].endswith(f" L{by['a1']['x']},{by['a1']['y']}")
    # The two children sit on opposite sides of their parent, so the arcs sweep opposite ways.
    sweep = lambda c: edges[c]["path"].split(" A")[1].split()[3]
    assert {sweep("a1"), sweep("a2")} == {"0", "1"}
    # In a straight chain the child is dead ahead of its parent: no arc at all.
    chain = {e["child"]: e for e in tree(CHAIN)["edges"]}
    assert "A" not in chain["rag"]["path"]


def test_siblings_get_their_own_slice_of_the_circle():
    # Three branches off the centre, each with a different number of leaves below it.
    jobs = corpus([["a", "a1"]] * 6 + [["a", "a2"]] * 6 + [["b"]] * 6 + [["c"]] * 6)
    t = tree(jobs)
    by = nodes_by_id(t)
    assert by["a"]["children"] == ["a1", "a2"]
    angles = [by[n]["angle"] for n in ("a", "b", "c")]
    assert len(set(angles)) == 3
    # A branch sits at the middle of the arc its own children occupy.
    assert by["a"]["angle"] == pytest.approx((by["a1"]["angle"] + by["a2"]["angle"]) / 2)


def test_the_same_corpus_always_draws_the_same_picture():
    shuffled = list(reversed(CHAIN))
    assert tree(shuffled) == tree(CHAIN)


def test_an_empty_job_set_has_no_tree():
    assert tree([], total=0) == {"total": 0, "size": 2 * (RING + PAD),
                                 "centre": {"x": RING + PAD, "y": RING + PAD}, "nodes": [], "edges": []}


# --- the I/O half -----------------------------------------------------------------------

@pytest.fixture
def wide(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    for company, city, skills in RELATED_JOBS:
        add(c, company, "AI Engineer", city, "arbeitnow", ts(1), [(s, "required") for s in skills])
    return c


def test_fetch_jobs_counts_the_filtered_set_and_splits_required_from_mentioned(wide):
    add(wide, "Nice", "AI Engineer", "Berlin", "arbeitnow", ts(1),
        [("python", "required"), ("aws", "nice_to_have")])
    total, jobs = fetch_jobs(wide, q.Filters(window="all"), NOW)
    assert total == len(RELATED_JOBS) + 1
    assert ({"python", "aws"}, {"python"}) in jobs
    # The filters still narrow the set the tree is drawn over.
    berlin, _ = fetch_jobs(wide, q.Filters(window="all", cities=("Berlin",)), NOW)
    assert berlin == 12


def test_skill_tree_ignores_the_requirement_and_skill_filters(wide):
    f = q.Filters(window="all")
    base = skill_tree(wide, f, NOW)
    assert base["total"] == len(RELATED_JOBS) and base["nodes"]
    for other in (q.Filters(window="all", requirement="all"),
                  q.Filters(window="all", skill_ids=("rag",))):
        assert skill_tree(wide, other, NOW) == base
