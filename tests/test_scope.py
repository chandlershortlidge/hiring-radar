"""The one list of collected places and career tracks, and their states (HIR-395)."""

import re

import pytest

from app import geo, ingest, queries, scope


def test_every_state_is_live_or_incubating():
    assert set(scope.PLACE_STATE.values()) <= set(scope.STATES)
    assert {t.state for t in scope.TRACKS.values()} <= set(scope.STATES)


def test_every_place_is_one_geo_recognises():
    """A name geo cannot find in a location string would be collected by nothing."""
    unknown = sorted(set(scope.PLACE_STATE) - {*geo.CITIES, geo.REMOTE_EU})
    assert not unknown, f"{unknown} are in app/scope.py's PLACE_STATE but app/geo.py does not know them"


def test_collection_reads_every_place_and_track_whatever_its_state():
    assert geo.ACTIVE_CITIES == scope.places() == tuple(scope.PLACE_STATE)
    assert ingest.FAMILIES == scope.tracks() == tuple(scope.TRACKS)


def test_the_public_lists_are_the_live_ones_and_something_is_live():
    assert queries.FAMILIES == scope.live_tracks() and scope.live_tracks()
    assert scope.live_places()
    assert set(scope.live_places()) | set(scope.incubating_places()) == set(scope.places())
    assert set(scope.live_tracks()) | set(scope.incubating_tracks()) == set(scope.tracks())


def test_every_track_pattern_is_a_regular_expression_and_the_first_five_have_none():
    for name, track in scope.TRACKS.items():
        if track.title_pattern is not None:
            re.compile(track.title_pattern)
    for name in ("ai-engineer", "ml-engineer", "data-scientist", "ml-platform", "research"):
        assert scope.TRACKS[name].title_pattern is None, f"{name} is sorted by the built-in title rule"


def test_a_state_is_read_when_asked_not_when_imported(monkeypatch):
    monkeypatch.setitem(scope.PLACE_STATE, "Chicago", scope.INCUBATING)
    monkeypatch.setitem(scope.TRACKS, "research", scope.Track(scope.INCUBATING))
    assert scope.incubating_places() == ("Chicago",) and "Chicago" not in scope.live_places()
    assert scope.incubating_tracks() == ("research",) and "research" not in scope.live_tracks()
    assert "Chicago" in scope.places() and "research" in scope.tracks()
    with pytest.raises(ValueError, match="bad family 'research'"):
        queries.make_filters({}, families=["research"])


# --- read now or later (HIR-396) -----------------------------------------------------------

def test_every_read_setting_is_now_or_later_and_names_a_collected_place():
    assert set(scope.PLACE_READ.values()) <= set(scope.READS)
    assert {t.read for t in scope.TRACKS.values()} <= set(scope.READS)
    unknown = sorted(set(scope.PLACE_READ) - set(scope.PLACE_STATE))
    assert not unknown, f"{unknown} are in app/scope.py's PLACE_READ but not in PLACE_STATE"


def test_only_an_incubating_place_or_track_reads_later():
    """A live one set to read later would put jobs with no skills on the dashboard."""
    live = sorted({*scope.read_later_places()} & {*scope.live_places()}
                  | {*scope.read_later_tracks()} & {*scope.live_tracks()})
    assert not live, (f"{live} are live and set to read later in app/scope.py: run "
                      f"`python -m app read-pending` for each and set it to read now before it goes live")
