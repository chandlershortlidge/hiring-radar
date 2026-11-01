"""scripts/spot_check.py — the human spot-check sampler (HIR-92).

What is worth a test here: who is eligible for the draw, that the draw is reproducible and
stratified, that a rendered item names the right section (three ways of getting that wrong
are fixed in this file), that the compact reply parses, and that applying answers only ever
adds provenance.
"""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("spot_check", ROOT / "scripts" / "spot_check.py")
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)


def golden(gid="golden_900", **over):
    g = {"id": gid, "split": "heldout", "labeled_by": ["model-a", "model-b"],
         "seniority": None, "seniority_basis": None, "seniority_signal": None,
         "german": None, "german_basis": None, "german_signal": None,
         "degree": None, "degree_requirement": None, "degree_or_equivalent": False,
         "degree_signal": None,
         "seniority_reviewed": False, "attrs_reviewed": False,
         "adjudicated": [], "adjudicated_by_model": [],
         "job_description": "Requirements:\n\n- Strong **Python**\n", "expected": []}
    g.update(over)
    return g


# --- the pool ---------------------------------------------------------------------

def test_the_pool_is_every_label_no_person_has_read():
    g = golden(expected=[{"skill_id": "python", "requirement": "required", "raw_text": "Python"},
                         {"skill_id": "go", "requirement": "required", "raw_text": "Go"}],
               adjudicated=["skill:go", "degree"])
    assert sc.pool([g]) == [("golden_900", "attribute", "german"),
                            ("golden_900", "attribute", "seniority"),
                            ("golden_900", "skill", "python")]


def test_a_reviewed_flag_takes_its_attributes_out_of_the_pool():
    # attrs_reviewed covers German and degree; seniority has its own flag.
    g = golden(seniority_reviewed=True, attrs_reviewed=True)
    assert sc.pool([g]) == []
    assert ("golden_900", "attribute", "seniority") in sc.pool([golden(attrs_reviewed=True)])


@pytest.mark.parametrize("provenance", [{"spot_checked": True},
                                        {"spot_checked_by": "claude-fable-5-1 (assistant)"}])
def test_a_label_only_a_model_spot_checked_is_still_in_the_pool(provenance):
    """The reason this ticket exists: the 2026-10-30 spot-check was answered by a model, so
    neither spelling of that provenance takes a label out of the pool."""
    g = golden(adjudicated_by_model=["skill:python"], **provenance,
               expected=[{"skill_id": "python", "requirement": "required", "raw_text": "Python"}])
    assert ("golden_900", "skill", "python") in sc.pool([g])


def test_a_label_this_process_already_checked_is_not_drawn_again():
    g = golden(spot_checked_by_human=["skill:python", "german"],
               expected=[{"skill_id": "python", "requirement": "required", "raw_text": "Python"}])
    assert sc.pool([g]) == [("golden_900", "attribute", "degree"),
                            ("golden_900", "attribute", "seniority")]


def test_a_null_attribute_is_a_label_in_its_own_right():
    assert ("golden_900", "attribute", "german") in sc.pool([golden()])


def test_the_batch_is_the_heldout_goldens_a_model_labeled(tmp_path):
    (tmp_path / "golden_001.json").write_text(json.dumps(golden("golden_001", split="dev")))
    (tmp_path / "golden_002.json").write_text(json.dumps(
        golden("golden_002", labeled_by=[])))              # hand-labeled, predates HIR-70
    (tmp_path / "golden_003.json").write_text(json.dumps(golden("golden_003")))
    (tmp_path / "golden_004.json").write_text(json.dumps(golden("golden_004", draft=True)))
    assert [g["id"] for g in sc.batch_goldens(tmp_path)] == ["golden_003"]


# --- the draw ---------------------------------------------------------------------

def many_labels():
    items = [(f"golden_{i:03d}", "skill", f"s{j}") for i in range(10) for j in range(10)]
    items += [(f"golden_{i:03d}", "attribute", a) for i in range(10) for a in sc.ATTRS]
    return sorted(items)


def test_the_draw_is_reproducible_and_depends_only_on_the_seed():
    items = many_labels()
    assert sc.draw(items, 24, 2, 0) == sc.draw(list(reversed(items)), 24, 2, 0)
    assert sc.draw(items, 24, 2, 0) != sc.draw(items, 24, 2, 1)


def test_the_draw_is_stratified_so_every_attribute_appears():
    drawn = sc.draw(many_labels(), 24, 2, 0)
    assert sum(1 for d in drawn if d[1] == "skill") == 24
    for attr in sc.ATTRS:
        assert sum(1 for d in drawn if d[1] == "attribute" and d[2] == attr) == 2
    assert len(drawn) == 30


def test_the_draw_never_asks_for_more_than_the_pool_holds():
    small = sorted([("golden_001", "skill", "python"), ("golden_001", "attribute", "german")])
    assert sc.draw(small, 24, 2, 0) == small


# --- headings ---------------------------------------------------------------------

def test_a_partial_line_at_the_quote_is_not_a_heading():
    """Regression: `posting[:at]` cuts mid-line, and that fragment passed for a heading, so
    a requirements bullet was reported as its own section."""
    posting = "Dein Profil:\n\n- Erfahrung in der Backend-Entwicklung mit Python, Go, Rust\n"
    at = posting.index("Go")
    assert sc.section_heading(posting, at) == "Dein Profil:"


def test_a_bullet_is_not_a_heading_but_a_bold_heading_is():
    assert sc.is_bullet("* Fundierte Erfahrung in GenAI") is True
    assert sc.is_bullet("**Deine Benefits**") is False
    assert sc.looks_like_heading("**Deine Benefits**") is True
    assert sc.looks_like_heading("* Fundierte Erfahrung in GenAI") is False


def test_a_sentence_is_not_a_heading():
    """Regression: golden_038's "...not hard requirements." read as a requirements heading."""
    posting = ("Nice to have\n\nThese are meant to be indicative, not hard requirements.\n\n"
               "- Deep knowledge of Python etc.\n")
    at = posting.index("Python")
    assert sc.section_heading(posting, at) == "Nice to have"
    assert sc.classify_heading(sc.section_heading(posting, at)) == "optional"


def test_a_flattened_posting_still_finds_its_heading_inside_the_line():
    # One line, no punctuation: a line scan finds no heading at all and would call the
    # section intro prose. golden_026 is this shape from end to end.
    posting = ("Das sind Deine Aufgaben: Du gestaltest die Plattformarchitektur und "
               "arbeitest eng mit Anwendungs- und Datenteams zusammen "
               "Das bringst Du mit: Du denkst in Automatisierungslösungen wie Terraform, Helm")
    at = posting.index("Terraform")
    heading = sc.section_heading(posting, at)
    assert heading.endswith("Das bringst Du mit")
    assert heading.startswith("...")            # a fragment of a run-on line, and says so
    assert sc.classify_heading(heading) == "requirements"


def test_a_bullets_own_label_is_not_read_as_the_section_heading():
    """golden_032 opens straight into its qualifications list with no heading. The bullets
    label themselves ("Cloud-native development: ..."), and reporting that label as the
    section would hide that there is no heading - which is what rule 1's default rests on."""
    posting = ("AI Systems Engineer (d/f/m)\n\n"
               "- Agentic platform engineering: Hands-on experience operating agents.\n"
               "- Cloud-native development: Proficient in AWS infrastructure (S3, IAM).\n")
    at = posting.index("S3")
    # The title line is the nearest thing to a heading this posting has; the bullet's own
    # label is not it, and classifying on the title keeps the list unlabelled, as it is.
    assert sc.section_heading(posting, at) == "AI Systems Engineer (d/f/m)"
    assert sc.classify_heading(sc.section_heading(posting, at)) == "intro prose"


def test_a_short_inline_heading_is_not_marked_as_a_fragment():
    assert sc.trim_heading("Dein Profil") == "Dein Profil"
    assert sc.trim_heading("a b c " * 20).startswith("...")


@pytest.mark.parametrize("heading,kind", [
    ("Nice to have", "optional"),
    ("Bonus points", "optional"),
    ("Your profile", "requirements"),
    ("Dein Profil:", "requirements"),
    ("Deine Aufgaben", "responsibilities"),
    ("Our tech stack", "tech stack"),
    ("", "intro prose"),
    ("About Ubiquiti", "intro prose"),
    ("Nice-to-have requirements", "optional"),   # optional wins over the requirements words
    ("Profile we're looking for", "requirements"),
    ("Als Qualitätsingenieur KI-Fokus sollten Sie mitbringen:", "requirements"),
    ("IN ORDER FOR YOU TO BE SUCCESSFUL, YOU BRING:", "requirements"),
])
def test_classify_heading(heading, kind):
    assert sc.classify_heading(heading) == kind


# --- context ----------------------------------------------------------------------

def test_a_lone_bullet_marker_is_joined_to_the_text_under_it():
    posting = "Dein Profil:\n\n-\n\nErfahrung in der Evaluation\n\n-\n\nErfahrung mit Go\n"
    m = sc.locate(posting, "Erfahrung in der Evaluation")
    lines = sc.context_block(posting, m)
    assert any("**Erfahrung in der Evaluation**" in ln for ln in lines)
    assert not any(ln.strip() == "-" for ln in lines)


def test_a_flattened_posting_gets_a_window_not_the_whole_posting():
    posting = "Intro. " + "x" * 3000 + " wie Terraform, Helm " + "y" * 3000
    m = sc.locate(posting, "Terraform")
    lines = sc.context_block(posting, m)
    assert len(lines) == 1
    assert len(lines[0]) < 2 * sc.WINDOW + 200
    assert "**Terraform**" in lines[0] and lines[0].startswith("...")


def test_the_quote_is_bolded_without_spacing_the_punctuation_out():
    posting = "- Du denkst in Lösungen wie Terraform, Helm und (GitOps) dazu\n"
    m = sc.locate(posting, "Terraform")
    assert "**Terraform**," in sc.context_block(posting, m)[0]
    m2 = sc.locate(posting, "GitOps")
    assert "(**GitOps**)" in sc.context_block(posting, m2)[0]


def test_a_quote_wrapped_across_lines_is_still_located():
    posting = "- strong hands-on\n  TypeScript skills\n"
    assert sc.locate(posting, "hands-on TypeScript skills") is not None


def test_a_null_attribute_shows_the_trigger_words_it_was_decided_against():
    g = golden(job_description="Requirements:\n\n- Sehr gute Deutschkenntnisse\n")
    item = sc.attribute_item(g, "german")
    assert item["context"]["triggers"]
    assert "Deutschkenntnisse" in item["context"]["triggers"][0]
    assert "null" in sc.render_item(1, 1, item)


def test_a_null_attribute_with_nothing_to_show_says_so():
    item = sc.attribute_item(golden(job_description="We build things.\n"), "german")
    assert item["context"]["triggers"] == []
    assert "never mentions" in sc.render_item(1, 1, item)


def test_a_skill_mentioned_elsewhere_names_the_other_section():
    g = golden(job_description=("Deine Rolle\n\n- Du baust Pipelines mit Python\n\n"
                                "Dein Profil\n\n- Du programmierst sicher mit Python\n"),
               expected=[{"skill_id": "python", "requirement": "required",
                          "raw_text": "programmierst sicher mit Python"}])
    item = sc.skill_item(g, "python", sc.Taxonomy.load())
    assert item["context"]["heading"] == "Dein Profil"
    assert item["also_under"] == ["Deine Rolle"]


def test_a_rendered_item_leaves_the_judgment_lines_to_fill():
    g = golden(expected=[{"skill_id": "python", "requirement": "required",
                          "raw_text": "Python"}])
    out = sc.render_item(3, 30, sc.skill_item(g, "python", sc.Taxonomy.load()))
    assert out.startswith("## 3 of 30 — golden_900 · skill")
    assert out.count(sc.TODO) == 3                      # two checks and the watch-for line
    assert "wrong: <required | nice_to_have | drop>" in out


# --- the reply --------------------------------------------------------------------

def test_all_ok_answers_every_item_in_the_batch():
    assert sc.parse_batch_reply("all ok", [1, 2, 3]) == {1: "ok", 2: "ok", 3: "ok"}
    assert sc.parse_batch_reply("All OK.", [1]) == {1: "ok"}


def test_a_named_item_is_wrong_and_the_rest_are_ok():
    assert sc.parse_batch_reply("3 wrong: nice_to_have", [1, 2, 3]) == {
        1: "ok", 2: "ok", 3: "wrong: nice_to_have"}


def test_several_wrong_in_one_reply():
    got = sc.parse_batch_reply("3 wrong: nice_to_have; 5 wrong: drop", [3, 4, 5])
    assert got == {3: "wrong: nice_to_have", 4: "ok", 5: "wrong: drop"}


def test_items_sharing_one_correction():
    got = sc.parse_batch_reply("3 and 4 wrong: drop", [3, 4, 5])
    assert got == {3: "wrong: drop", 4: "wrong: drop", 5: "ok"}


@pytest.mark.parametrize("reply", ["", "looks fine to me", "3 nice_to_have", "99 wrong: drop"])
def test_an_unreadable_reply_is_refused_rather_than_guessed(reply):
    with pytest.raises(ValueError):
        sc.parse_batch_reply(reply, [1, 2, 3])


# --- the numbers and the provenance ----------------------------------------------

def items_for(n_ok, n_wrong, kind="skill"):
    items = [{"golden_id": "golden_900", "kind": kind, "key": f"s{i}"}
             for i in range(n_ok + n_wrong)]
    verdicts = {sc.key_of(it): ("ok" if i < n_ok else "wrong: drop")
                for i, it in enumerate(items)}
    return items, verdicts


def test_no_errors_still_reports_an_interval_that_admits_error():
    items, verdicts = items_for(30, 0)
    stats = sc.tally(items, verdicts)["overall"]
    assert stats == {"errors": 0, "n": 30, "rate": 0.0,
                     "wilson95": [pytest.approx(0.0), pytest.approx(0.113, abs=0.01)]}


def test_the_rate_is_reported_per_kind_as_well():
    skills, v1 = items_for(20, 1, "skill")
    attrs, v2 = items_for(5, 1, "attribute")
    for it in attrs:
        it["key"] += "-attr"
    stats = sc.tally(skills + attrs, {**v1, **{sc.key_of(it): v for it, v in
                                               zip(attrs, ["ok"] * 5 + ["wrong: none"])}})
    assert stats["overall"]["n"] == 27
    assert stats["skill"]["errors"] == 1
    assert stats["attribute"] == {"errors": 1, "n": 6, "rate": pytest.approx(1 / 6),
                                  "wilson95": [pytest.approx(0.030, abs=0.01),
                                               pytest.approx(0.564, abs=0.01)]}


def test_stamping_adds_provenance_and_changes_no_label():
    g = golden(expected=[{"skill_id": "python", "requirement": "required", "raw_text": "Python"}])
    out = sc.stamp(g, ["skill:python", "german"])
    assert out["spot_checked_by_human"] == ["german", "skill:python"]
    assert out["expected"] == g["expected"]
    assert {k: v for k, v in out.items() if k != "spot_checked_by_human"} == g


def test_stamping_twice_does_not_duplicate_a_key():
    g = sc.stamp(golden(), ["german"])
    assert sc.stamp(g, ["german", "degree"])["spot_checked_by_human"] == ["degree", "german"]


def test_the_provenance_key_matches_adjudicated_s_own_format():
    assert sc.provenance_key({"kind": "skill", "key": "python"}) == "skill:python"
    assert sc.provenance_key({"kind": "attribute", "key": "german"}) == "german"


# --- the real batch ---------------------------------------------------------------

def test_the_committed_batch_renders_without_an_unlocated_quote():
    """Every sampled label must be judgeable from the packet alone: a quote the renderer
    cannot find in its posting leaves a reviewer nothing to read."""
    tax = sc.Taxonomy.load()
    goldens = {g["id"]: g for g in sc.batch_goldens()}
    assert len(goldens) == 22
    drawn = sc.draw(sc.pool(list(goldens.values())), 24, 2, 0)
    unlocated = []
    for gid, kind, key in drawn:
        item = (sc.skill_item(goldens[gid], key, tax) if kind == "skill"
                else sc.attribute_item(goldens[gid], key))
        value_is_null = kind == "attribute" and item["value"][key] is None
        if not item["context"]["located"] and not value_is_null:
            unlocated.append((gid, kind, key))
    assert unlocated == []
