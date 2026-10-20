import json
from pathlib import Path

import pytest

from app.taxonomy import Taxonomy, TaxonomyError

ROOT = Path(__file__).resolve().parent.parent


def tax(skills):
    return Taxonomy({"version": 1, "skills": skills})


def s(id, display, aliases=(), parents=()):
    return {"id": id, "display": display, "aliases": list(aliases), "parents": list(parents)}


def test_resolve_by_display_and_alias_case_insensitively():
    t = tax([s("llms", "LLMs", ["large language models"])])
    assert t.resolve("LLMs") == "llms"
    assert t.resolve("  large Language Models ") == "llms"
    assert t.resolve("Large language model") is None  # no fuzzy guessing


def test_react_and_react_agent_pattern_stay_distinct():
    t = tax([s("react", "React"), s("react-agent-pattern", "ReAct")])
    assert t.resolve("React") == "react"
    assert t.resolve("ReAct") == "react-agent-pattern"


def test_alias_claimed_by_two_skills_is_rejected():
    with pytest.raises(TaxonomyError):
        tax([s("a", "A", ["shared"]), s("b", "B", ["shared"])])


def test_unknown_parent_and_cycles_are_rejected():
    with pytest.raises(TaxonomyError):
        tax([s("a", "A", parents=["missing"])])
    with pytest.raises(TaxonomyError):
        tax([s("a", "A", parents=["b"]), s("b", "B", parents=["a"])])


def test_ancestors_are_transitive():
    t = tax([s("vertex-ai", "Vertex AI", parents=["gcp"]), s("gcp", "GCP", parents=["cloud"]), s("cloud", "Cloud")])
    assert t.ancestors("vertex-ai") == {"gcp", "cloud"}
    assert t.ancestors("cloud") == set()


def test_committed_taxonomy_loads_and_covers_every_golden_label():
    t = Taxonomy.load()
    for p in sorted((ROOT / "evals/goldens").glob("*.json")):
        g = json.loads(p.read_text())
        for e in g["expected"]:
            assert e["skill_id"] in t.skills, f"{p.name}: {e['skill_id']} not in taxonomy"


def test_every_golden_has_a_valid_seniority_label():
    # None ("no usable signal", LABELING.md) is a label; a level needs a basis, a stated
    # level needs a signal, and a signal must be quoted from the posting.
    for p in sorted((ROOT / "evals/goldens").glob("*.json")):
        g = json.loads(p.read_text())
        if g.get("draft"):
            continue
        assert "seniority" in g, p.name
        if g["seniority"] is None:
            assert g.get("seniority_basis") is None, p.name
            continue
        assert g["seniority"] in ("junior", "mid", "senior"), p.name
        assert g["seniority_basis"] in ("stated", "inferred"), p.name
        sig = g.get("seniority_signal")
        assert sig or g["seniority_basis"] == "inferred", f"{p.name}: stated without a signal"
        if sig:
            norm = lambda x: " ".join(x.split()).lower()
            assert norm(sig) in norm(g["job_description"]), f"{p.name}: signal not in text"
