"""The dashboard's option lists and the server's validated lists have to match (HIR-203).

The dashboard keeps its own copy of the five job families and of the German / degree /
production / seniority / time-window / required-or-nice-to-have filter choices, because each key needs the wording a
person reads next to it. The server keeps the same keys to validate requests against. The
two are not derivable from one another and nothing at runtime compares them: add a choice
on the server and the dashboard silently never offers it; drop one and the dashboard's
button starts returning "bad value" (HTTP 422).

This is the cheaper half of HIR-203, and the same answer HIR-200 gave the open-job rule
and its SQL twin: no endpoint, one test that fails until both sides agree.

Does NOT run the dashboard or parse JavaScript properly — it reads the literal
declarations out of the source with a regex, and fails loudly if a declaration it expects
is missing or stops being a flat literal.
"""

import re
from pathlib import Path

import pytest

from app import queries

WEB = Path(__file__).resolve().parent.parent / "web" / "src"


def _source(name: str) -> str:
    path = WEB / name
    assert path.exists(), f"{path} is gone; this test is pointing at the wrong file"
    return path.read_text()


def _body(src: str, name: str, open_: str, close: str) -> str:
    m = re.search(rf"const {re.escape(name)}\s*=\s*{re.escape(open_)}(.*?){re.escape(close)}\s*;",
                  src, re.S)
    assert m, f"no `const {name} = {open_}...{close};` declaration found — was it renamed?"
    return m.group(1)


def js_array(file: str, name: str) -> tuple[str, ...]:
    """The strings in a flat JS array literal, in source order."""
    body = _body(_source(file), name, "[", "]")
    values = tuple(re.findall(r'"([^"]*)"', body))
    assert values, f"{name} in {file} parsed as empty; it is no longer a flat array of strings"
    return values


def js_keys(file: str, name: str) -> tuple[str, ...]:
    """The keys of a flat JS object literal, in source order. Quoted or bare."""
    body = _body(_source(file), name, "{", "}")
    assert "{" not in body, f"{name} in {file} is nested; this reader only handles flat objects"
    keys = tuple(a or b or c for a, b, c in
                 re.findall(r"""(?:"([^"]+)"|'([^']+)'|([A-Za-z_$][\w$]*))\s*:""", body))
    assert keys, f"{name} in {file} parsed as no keys; it is no longer a flat object literal"
    return keys


# Each row: what the dashboard calls it, where, and the server's list it must match.
# "server" is the set of values the API accepts; the dashboard offers exactly these.
CHOICE_LISTS = [
    ("FAMILIES", "format.js", js_array, queries.FAMILIES),
    ("FAMILY_LABELS", "format.js", js_keys, queries.FAMILIES),
    ("SENIORITIES", "format.js", js_array, queries.SENIORITIES),
    ("GERMAN_FILTERS", "format.js", js_keys, tuple(queries.GERMAN_FILTERS)),
    ("PRODUCTION_FILTERS", "format.js", js_keys, tuple(queries.PRODUCTION_FILTERS)),
    ("DEGREE_FILTERS", "format.js", js_keys, tuple(queries.DEGREE_FILTERS)),
    ("WINDOWS", "App.jsx", js_keys, queries.WINDOWS),
    ("REQUIREMENTS", "App.jsx", js_keys, queries.REQUIREMENTS),  # HIR-206
]


@pytest.mark.parametrize("name, file, read, server", CHOICE_LISTS,
                         ids=[f"{f}:{n}" for n, f, _, _ in CHOICE_LISTS])
def test_dashboard_offers_exactly_the_choices_the_server_accepts(name, file, read, server):
    """Add a family or a filter choice on the server and this fails until the dashboard
    offers it; drop one and it fails until the dashboard stops sending it."""
    dashboard = set(read(file, name))
    expected = set(server)
    missing = sorted(expected - dashboard)
    extra = sorted(dashboard - expected)
    assert not missing, (
        f"the server accepts {missing} but web/src/{file}'s {name} does not offer them — "
        f"add each one there, with the wording a person should read")
    assert not extra, (
        f"web/src/{file}'s {name} offers {extra} but the server rejects them with 422 — "
        f"remove them there, or add them to the server's list")


def test_the_three_attribute_filters_share_one_set_of_keys():
    """German and production deliberately use the same four keys, so "not required" means
    the same thing for both (HIR-69). Degree swaps one key — "open", a person without a
    degree can still apply — and that difference is the only one allowed."""
    assert tuple(queries.GERMAN_FILTERS) == tuple(queries.PRODUCTION_FILTERS)
    assert set(queries.DEGREE_FILTERS) - set(queries.GERMAN_FILTERS) == {"open"}
    assert set(queries.GERMAN_FILTERS) - set(queries.DEGREE_FILTERS) == {"not_required"}


def test_the_readers_notice_a_declaration_that_is_gone():
    """If a list is renamed or restructured the test above must fail, not pass empty."""
    with pytest.raises(AssertionError, match="no `const NOT_A_LIST"):
        js_array("format.js", "NOT_A_LIST")
    with pytest.raises(AssertionError, match="no `const NOT_A_LIST"):
        js_keys("format.js", "NOT_A_LIST")
