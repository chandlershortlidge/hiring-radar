import math

import pytest

from app import db, queries as q
from app.skill_tree import (BRANCH_HUES, LINE_H, MIN_BAND, MIN_JOBS, PAD, RING,
                            _mono_width, _text_width, build_tree, fetch_jobs, skill_tree)
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
    t = tree([], total=0)
    assert (t["total"], t["nodes"], t["edges"]) == (0, [], [])
    assert t["size"] == 2 * (RING + PAD) and t["centre"] == {"x": RING + PAD, "y": RING + PAD}


# --- branches ---------------------------------------------------------------------------

def wide_corpus():
    """One trunk with three lobes of 6 / 3 / 2 nodes and two lone leaves hanging off it."""
    rows = []
    rows += [["t", "cloud", f"c{i}"] for i in range(1, 6) for _ in range(8 - i)]
    rows += [["t", "agents", f"a{i}"] for i in (1, 2) for _ in range(7)]
    rows += [["t", "apis", "api1"] for _ in range(6)] + [["t", "apis"] for _ in range(3)]
    rows += [["t", "solo"] for _ in range(6)]
    rows += [["t", "lonely"] for _ in range(5)]
    rows += [["t"]] * 40
    return corpus(rows)


def test_a_branch_is_a_lobe_not_a_root():
    """The tree has one root holding everything, so a hue per root would paint the whole
    picture one colour. The biggest branch is split until none holds half the nodes, and
    the heads that were split become trunk — neutral, with no branch of their own."""
    by = nodes_by_id(tree(wide_corpus()))
    assert by["t"]["branch"] is None and by["t"]["branch_index"] is None   # the trunk
    assert by["cloud"]["branch"] == "cloud"
    assert by["c1"]["branch"] == "cloud"          # a descendant inherits its branch
    assert by["agents"]["branch"] == "agents" and by["a1"]["branch"] == "agents"
    assert by["solo"]["branch"] == "solo"


def test_only_the_largest_branches_are_coloured():
    by = nodes_by_id(tree(wide_corpus()))
    hues = {n["branch"]: n["branch_index"] for n in by.values() if n["branch_index"] is not None}
    assert len(hues) == BRANCH_HUES
    assert [h for h, i in sorted(hues.items(), key=lambda kv: kv[1])] == ["cloud", "agents", "apis"]
    # A lone leaf never takes a hue off a real lobe, however the sizes fall.
    assert by["solo"]["branch_index"] is None and by["lonely"]["branch_index"] is None
    # Hue follows the branch head, so every node of a lobe carries the same one.
    assert {by[n]["branch_index"] for n in ("cloud", "c1", "c3")} == {0}


def test_a_straight_chain_has_at_most_one_branch():
    """Splitting stops as soon as no branch holds half the tree, so a chain gives up its
    head nodes to the trunk one at a time and what is left is a single tail — one hue at
    most, never three."""
    by = nodes_by_id(tree(CHAIN))
    hues = {n["branch_index"] for n in by.values()} - {None}
    assert len(hues) <= 1
    assert by["python"]["branch"] is None and by["llms"]["branch"] is None   # trunk


def test_the_ring_always_shows_a_band_where_a_gap_exists():
    by = nodes_by_id(tree(CHAIN))
    # snowflake is mentioned 6 and required 1: a wide band, the whole point of the encoding.
    assert by["snowflake"]["core_r"] < by["snowflake"]["r"] * 0.5
    # python is required every time it is mentioned: a solid circle, not a faked band.
    assert by["python"]["core_r"] == by["python"]["r"]
    # rag is required in 10 of 10 as well; llms likewise — but a node with any gap at all
    # keeps a visible band even when the ratio is close to one.
    jobs = corpus([["a", "b"]] * 19 + [["a", ("b", "nice_to_have")]])
    t = tree(jobs)
    b = nodes_by_id(t)["b"]
    # 19 of 20 would be a hairline at true scale; MIN_BAND holds it open instead. The
    # constant is in reference units, so it is compared against the box's own scale.
    assert b["r"] - b["core_r"] == pytest.approx(MIN_BAND * t["size"] / 1000, abs=0.2)


def test_a_node_is_sized_by_how_many_jobs_mention_it():
    by = nodes_by_id(tree(CHAIN))
    assert by["python"]["r"] > by["llms"]["r"] > by["rag"]["r"] > by["snowflake"]["r"]


# --- labels -----------------------------------------------------------------------------

def thirty_node_corpus():
    """A deterministic 30-node tree with real skill names, so the label test is run against
    the kind of width the dashboard actually draws — the longest names are the ones that
    collide. Each skill is nested under the one before it in its lobe, so every lobe is a
    chain off the trunk and the whole thing fills the circle."""
    lobes = [
        ["Machine Learning", "PyTorch", "TensorFlow", "scikit-learn", "Deep Learning"],
        ["Cloud", "Amazon Web Services", "Microsoft Azure", "Google Cloud Platform"],
        ["Docker", "Kubernetes", "Containerization", "Infrastructure as Code"],
        ["Agents", "Retrieval Augmented Generation", "LangChain", "Vector Databases"],
        ["Evaluation", "Observability", "Prompt engineering", "Model Context Protocol"],
        ["APIs", "Software Architecture", "Backend development", "TypeScript"],
        ["CI/CD", "Testing", "Git", "Data pipelines"],
    ]
    rows = []
    for lobe in lobes:
        for i in range(len(lobe)):
            # the first i+1 of the lobe together, often enough to nest them in order
            rows += [["Python"] + lobe[:i + 1]] * (9 - i)
    rows += [["Python"]] * 60
    return corpus(rows)


def boxes(t):
    """Every label's box, the way _place_labels measured it."""
    out = {}
    for n in t["nodes"]:
        w = _text_width(n["display"], t["font"])
        h = t["font"] * LINE_H
        x0 = n["label_x"] if n["label_anchor"] == "start" else n["label_x"] - w
        cy = n["label_y"] - t["font"] * 0.35
        out[n["skill_id"]] = (x0, cy - h / 2, x0 + w, cy + h / 2)
    return out


def test_no_two_labels_overlap_at_thirty_nodes():
    t = tree(thirty_node_corpus())
    assert len(t["nodes"]) == 30
    assert all(n["label_placed"] for n in t["nodes"]), \
        [n["skill_id"] for n in t["nodes"] if not n["label_placed"]]
    b = boxes(t)
    ids = sorted(b)
    for i, a in enumerate(ids):
        for c in ids[i + 1:]:
            ax0, ay0, ax1, ay1 = b[a]
            cx0, cy0, cx1, cy1 = b[c]
            assert not (ax0 < cx1 and cx0 < ax1 and ay0 < cy1 and cy0 < ay1), f"{a} overlaps {c}"


def test_a_label_never_sits_on_a_node_or_leaves_the_box():
    t = tree(thirty_node_corpus())
    b = boxes(t)
    for n in t["nodes"]:
        x0, y0, x1, y1 = b[n["skill_id"]]
        assert 0 <= x0 and x1 <= t["size"] and 0 <= y0 and y1 <= t["size"]
        for other in t["nodes"]:      # including its own node: a name never covers a circle
            ox0, oy0 = other["x"] - other["r"], other["y"] - other["r"]
            ox1, oy1 = other["x"] + other["r"], other["y"] + other["r"]
            assert not (x0 < ox1 and ox0 < x1 and y0 < oy1 and oy0 < y1), \
                f"{n['skill_id']}'s label sits on {other['skill_id']}"


def test_a_label_that_moved_gets_a_leader_line_and_one_that_did_not_does_not():
    t = tree(thirty_node_corpus())
    moved = [n for n in t["nodes"] if n["leader"]]
    assert moved, "the fixture is meant to be crowded enough that something moves"
    for n in t["nodes"]:
        on_its_own_row = abs(n["label_y"] - t["font"] * 0.35 - n["y"]) <= 1
        natural_side = "start" if n["x"] >= t["centre"]["x"] else "end"
        if n["leader"] is None:
            assert on_its_own_row and n["label_anchor"] == natural_side


def test_label_placement_is_deterministic():
    a, b = tree(thirty_node_corpus()), tree(list(reversed(thirty_node_corpus())))
    assert [(n["skill_id"], n["label_x"], n["label_y"]) for n in a["nodes"]] == \
           [(n["skill_id"], n["label_x"], n["label_y"]) for n in b["nodes"]]


def test_the_width_estimate_is_conservative():
    """It has to over-estimate: the browser's metrics are not available here, and a label
    that fits by this measure is what makes the no-overlap test a guarantee."""
    # IBM Plex Sans averages near 0.5 em across mixed text; the estimate must sit above a
    # safe floor for every label the dashboard draws, not just on average.
    for name in ("Infrastructure as Code", "Retrieval Augmented Generation", "MLOps", "Git"):
        assert _text_width(name, 13) >= 0.45 * 13 * len(name), name
    assert _text_width("MMMM", 13) > _text_width("iiii", 13) * 2
    assert _text_width("", 13) == 0
    assert _text_width("abc", 26) == 2 * _text_width("abc", 13)      # linear in the size


def test_the_tooltip_box_holds_its_own_text():
    """The tip is set in the mono face, so its box is measured per advance rather than per
    glyph shape — the proportional estimate under-measures mono and the box clipped the
    line it was drawn around."""
    t = tree(thirty_node_corpus())
    for n in t["nodes"]:
        widest = max(_mono_width(l, t["tip_font"]) for l in n["tip"]["lines"])
        assert n["tip"]["w"] >= widest, n["skill_id"]
        assert 0 <= n["tip"]["x"] and n["tip"]["x"] + n["tip"]["w"] <= t["size"]
        assert 0 <= n["tip"]["y"] and n["tip"]["y"] + n["tip"]["h"] <= t["size"]
    assert _mono_width("iiii", 13) == _mono_width("MMMM", 13)      # one advance each


def test_display_names_are_used_for_the_label_and_its_width():
    t = build_tree(20, CHAIN, {"python": "Python", "llms": "LLMs"})
    by = nodes_by_id(t)
    assert by["python"]["display"] == "Python"
    assert by["rag"]["display"] == "rag"          # missing ids fall back to the id


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
