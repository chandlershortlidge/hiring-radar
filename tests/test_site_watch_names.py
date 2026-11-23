"""A name the robot visitor matches has to mean one control (HIR-430).

The robot visitor (web/e2e/site-watch.spec.js) finds most controls the way a screen reader
names them: `getByRole("button", { name: "Your profile" })`. That match is a *substring*
match unless the locator says `exact: true` — so a second control whose own name merely
contains the first one's makes the locator resolve to several elements, and Playwright
fails the step ("strict mode violation") on a site that is working perfectly. That is
exactly what happened when HIR-411 added the gaps line: each chip is named
"Python, 56% of jobs, not in your profile. Filter job list", which contains "Your profile",
so the step that sets up a profile failed after a deploy and the deploy was rolled back.

Nothing at runtime can catch that: the robot visitor only runs against the live site, after
the deploy. So this is the same answer HIR-203 gave the dashboard's option lists — one test
that fails until the two sides agree. It fails on a loose name in the spec whose text is
contained in another control's name, and names both.

Does NOT parse JavaScript or JSX. It reads the `aria-label` values out of `web/src/*.jsx`
and the `getByRole` calls out of the spec with balanced-brace scans, and fails loudly if it
stops finding either. So it checks only the names set by an `aria-label` — the ones that do
not depend on words a phone hides (AGENTS.md, HIR-263) — and not names that come from an
element's visible text. It ignores the role, on purpose: a name that reads as two controls'
names is a poor name for the visitor to match loosely whatever their roles are.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "web" / "e2e" / "site-watch.spec.js"
WEB = ROOT / "web" / "src"


def _balanced(src: str, start: int) -> str:
    """The text inside the brackets opening at `start`, nesting included."""
    opener = src[start]
    closer = {"{": "}", "(": ")"}[opener]
    depth = 0
    for i in range(start, len(src)):
        if src[i] == opener:
            depth += 1
        elif src[i] == closer:
            depth -= 1
            if depth == 0:
                return src[start + 1 : i]
    raise AssertionError(f"unclosed {opener} at {start}")


def aria_labels(src: str) -> list[str]:
    """Every aria-label in one JSX file, as the source text of its value.

    A quoted label comes back verbatim; a template literal comes back with its `${...}`
    holes in place, which is enough to tell whether a fixed phrase sits inside it.
    """
    out = []
    for m in re.finditer(r"aria-label=", src):
        i = m.end()
        if src[i] == '"':
            out.append(src[i + 1 : src.index('"', i + 1)])
        elif src[i] == "{":
            out.append(_balanced(src, i))
    return out


def named_locators(src: str) -> list[tuple[str, str, bool]]:
    """(role, name, exact) for every `getByRole("role", { name: "..." })` in the spec.

    Only plain double-quoted names: a regular-expression name says what it matches on its
    own face, so it is not a trap.
    """
    out = []
    for m in re.finditer(r"getByRole\(", src):
        args = _balanced(src, m.end() - 1)
        role = re.match(r'\s*"(\w+)"', args)
        if not role or "{" not in args:
            continue
        opts = _balanced(args, args.index("{"))
        name = re.search(r'name:\s*"([^"]*)"', opts)
        if name:
            out.append((role.group(1), name.group(1), "exact: true" in opts))
    return out


def ambiguous(locators, labels) -> list[str]:
    """One line per loose locator whose name sits inside another control's name."""
    out = []
    for role, name, exact in locators:
        if exact:
            continue
        for where, label in labels:
            if name.lower() in label.lower() and label.strip() != name:
                out.append(
                    f'getByRole("{role}", {{ name: "{name}" }}) also matches the control '
                    f"named `{label}` in {where}: add exact: true, or give one of the two "
                    f"a name the other does not contain"
                )
    return out


def _spec() -> str:
    assert SPEC.exists(), f"{SPEC} is gone; this test is pointing at the wrong file"
    return SPEC.read_text()


def _labels() -> list[tuple[str, str]]:
    found = [(p.name, label) for p in sorted(WEB.rglob("*.jsx")) for label in aria_labels(p.read_text())]
    assert found, f"no aria-label found under {WEB}; this test has stopped reading the dashboard"
    return found


def test_every_name_the_robot_visitor_matches_loosely_means_one_control():
    assert ambiguous(named_locators(_spec()), _labels()) == []


def test_the_readers_still_find_the_locators_and_the_labels():
    """A silent zero on either side would make the check above pass on nothing."""
    locators = named_locators(_spec())
    assert len(locators) >= 5, locators
    # The two steps HIR-430 broke, each matching the one control it means.
    assert ("button", "Your profile", True) in locators
    assert ("button", "Save", True) in locators
    assert any(label.strip() == "Your profile" for _, label in _labels())


def test_the_gaps_line_is_still_the_case_this_came_from():
    """HIR-430 itself: the gaps chips are named with the profile button's name inside them,
    so the spec's profile steps may never go back to a loose match."""
    labels = [label for where, label in _labels() if where == "FitLine.jsx"]
    assert any("not in your profile" in label for label in labels), labels
    assert ambiguous([("button", "Your profile", False)], _labels())


@pytest.mark.parametrize(
    "label,flagged",
    [
        ("Python, 56% of jobs, not in your profile. Filter job list", True),  # HIR-430
        ("Your profile", False),  # the control the visitor means
        # A second control named the same words in another case is matched too, because a
        # loose match ignores case; `exact: true` does not.
        ("your profile", True),
        ("Set up a profile", False),  # a name that does not contain it
    ],
)
def test_a_name_contained_in_another_name_is_what_gets_flagged(label, flagged):
    found = ambiguous([("button", "Your profile", False)], [("X.jsx", label)])
    assert bool(found) is flagged, found


def test_an_exact_locator_is_never_flagged():
    chip = [("X.jsx", "Python, 56% of jobs, not in your profile. Filter job list")]
    assert ambiguous([("button", "Your profile", True)], chip) == []


def test_the_label_reader_takes_a_template_literal_whole():
    src = """<button aria-label={`${g.name}, ${g.pct}% of jobs, not in your profile. ${sel ? "Remove from" : "Filter"} job list`} />"""
    assert aria_labels(src) == ['`${g.name}, ${g.pct}% of jobs, not in your profile. ${sel ? "Remove from" : "Filter"} job list`']


def test_the_locator_reader_skips_a_regular_expression_name():
    src = 'page.getByRole("button", { name: /Compare with/ }).click();'
    assert named_locators(src) == []
