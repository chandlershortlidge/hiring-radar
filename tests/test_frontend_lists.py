"""The dashboard's option lists and the server's validated lists have to match (HIR-203).

The dashboard keeps its own copy of the job families and of the German / degree /
production / seniority / time-window / required-or-nice-to-have filter choices, because each key needs the wording a
person reads next to it. The server keeps the same keys to validate requests against. The
two are not derivable from one another and nothing at runtime compares them: add a choice
on the server and the dashboard silently never offers it; drop one and the dashboard's
button starts returning "bad value" (HTTP 422).

This is the cheaper half of HIR-203, and the same answer HIR-200 gave the open-job rule
and its SQL twin: no endpoint, one test that fails until both sides agree.

The list of places is held to the same standard (HIR-312). A city launch edits three lists
that do not know about each other: the collector's switched-on places (app/scope.py, read
as `geo.ACTIVE_CITIES`), the dashboard's `PLACES`, and the board-search phrases in
config/discover.json. Since HIR-395 a switched-on place is live or incubating: the
dashboard lists exactly the live ones, so an incubating city is never offered, and the
board search covers both, because both are collected. Miss the
dashboard and the city's jobs are collected but nobody can pick it; miss the collector and
the home grid shows a card that never fills; miss the phrases and the weekly search for
new boards never looks there. The checks below fail on each, naming the city.

Does NOT run the dashboard or parse JavaScript properly — it reads the literal
declarations out of the source with a regex, and fails loudly if a declaration it expects
is missing or stops being a flat literal.
"""

import json
import re
from pathlib import Path

import pytest

from app import discover, geo, queries, scope

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


def js_names(file: str, name: str) -> tuple[str, ...]:
    """The `name` of every entry in a JS array of object literals, in source order."""
    body = _body(_source(file), name, "[", "]")
    names = tuple(re.findall(r'\bname:\s*"([^"]*)"', body))
    assert names, f"{name} in {file} parsed as no names; it is no longer an array of {{ name: \"...\" }}"
    assert len(names) == body.count("{"), (
        f"{name} in {file} has {body.count('{')} entries but {len(names)} literal names; "
        f"every entry needs a `name: \"...\"` this reader can see")
    return names


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


# --- places: the collector, the dashboard and the board search (HIR-312) -----------------

def check_places(dashboard, collected) -> None:
    """The dashboard offers exactly the places the collector has switched on and live."""
    missing = sorted(set(collected) - set(dashboard))
    extra = sorted(set(dashboard) - set(collected))
    assert not missing, (
        f"the collector has {missing} switched on and live (app/scope.py PLACE_STATE) but "
        f"web/src/format.js's PLACES does not list them, so their jobs are collected and "
        f"nobody can pick them — add each one to PLACES")
    assert not extra, (
        f"web/src/format.js's PLACES lists {extra} but the collector does not have them "
        f"switched on and live (app/scope.py PLACE_STATE), so the dashboard shows a place that "
        f"never fills — remove them from PLACES, or switch them on (an incubating place is "
        f"collected but must not be listed until it is live)")


def check_search_phrases(collected, queries_) -> None:
    """Every switched-on city is named by at least one board-search phrase. EU-remote is
    exempt: it is not a city to search for."""
    unsearched = sorted(
        city for city in collected
        if city != geo.REMOTE_EU
        and not any(re.search(rf"\b{re.escape(city)}\b", q, re.I) for q in queries_))
    assert not unsearched, (
        f"{unsearched} are switched on (app/geo.py ACTIVE_CITIES) but no phrase in "
        f"config/discover.json's queries names them, so the search for new job boards "
        f"never looks there — add the phrases for each")


def _search_phrases() -> list[str]:
    return json.loads(discover.CONFIG_PATH.read_text())["queries"]


def test_dashboard_lists_exactly_the_places_the_collector_has_switched_on():
    check_places(js_names("format.js", "PLACES"), scope.live_places())


def test_an_incubating_place_listed_on_the_dashboard_fails_by_name(monkeypatch):
    """The dashboard's pickers and the robot visitor read PLACES, so this is what keeps
    both off an incubating city (HIR-395); switching it to live then asks for its entry."""
    monkeypatch.setitem(scope.PLACE_STATE, "Chicago", scope.INCUBATING)
    with pytest.raises(AssertionError, match=r"PLACES lists \['Chicago'\]"):
        check_places(js_names("format.js", "PLACES"), scope.live_places())


def test_every_switched_on_city_has_a_board_search_phrase():
    check_search_phrases(geo.ACTIVE_CITIES, _search_phrases())


def test_a_city_switched_on_but_missing_from_the_dashboard_fails_by_name():
    with pytest.raises(AssertionError, match=r"\['Atlantis'\] switched on .* does not list them"):
        check_places(js_names("format.js", "PLACES"), scope.live_places() + ("Atlantis",))


def test_a_dashboard_place_the_collector_has_not_switched_on_fails_by_name():
    with pytest.raises(AssertionError, match=r"PLACES lists \['Atlantis'\]"):
        check_places(js_names("format.js", "PLACES") + ("Atlantis",), scope.live_places())


def test_a_switched_on_city_with_no_search_phrase_fails_by_name():
    with pytest.raises(AssertionError, match=r"^\['Atlantis'\] are switched on"):
        check_search_phrases(geo.ACTIVE_CITIES + ("Atlantis",), _search_phrases())


def test_eu_remote_needs_no_search_phrase_and_a_longer_name_does_not_count():
    check_search_phrases((geo.REMOTE_EU,), [])
    # "New York" is not named by a phrase about "New Yorkshire"; whole words only.
    with pytest.raises(AssertionError, match="New York"):
        check_search_phrases(("New York",), ['"AI engineer" "New Yorkshire"'])
    check_search_phrases(("New York",), ['"machine learning" "new york"'])


def test_the_place_reader_notices_a_declaration_that_is_gone():
    with pytest.raises(AssertionError, match="no `const NOT_A_LIST"):
        js_names("format.js", "NOT_A_LIST")
