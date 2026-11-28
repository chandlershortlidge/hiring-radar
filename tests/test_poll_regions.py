"""The daily collection in two regional runs (HIR-369): Europe at 07:00 Berlin, the US at
07:00 New York. Each run fetches its own region's feeds; company boards are in both."""

import subprocess
import sys
from pathlib import Path

import pytest

from app import geo, poll

ROOT = Path(__file__).resolve().parent.parent
DEPLOY = ROOT / "deploy"


def test_every_active_place_has_a_region():
    """A launched city with no region would be in neither run's log line."""
    for place in geo.ACTIVE_CITIES:
        assert geo.REGION_OF.get(place) in geo.REGIONS, place


def test_the_two_regions_are_the_cities_the_issue_names():
    assert set(geo.region_places(geo.EUROPE)) == {
        "Berlin", "Hamburg", "Frankfurt", "Munich", "Amsterdam", "London", geo.REMOTE_EU}
    assert set(geo.region_places(geo.US)) == {
        "New York", "San Francisco", "Seattle", "Los Angeles", "Chicago", "San Jose", "Austin", "Boston"}


@pytest.mark.parametrize("feed, regions", [
    ({"type": "greenhouse", "token": "intercom"}, ("europe", "us")),
    ({"type": "join", "token": "anni"}, ("europe", "us")),
    ({"type": "jsearch", "search": "AI engineer in Seattle", "country": "us"}, ("us",)),
    ({"type": "jsearch", "search": "AI engineer in Berlin", "country": "de"}, ("europe",)),
    ({"type": "jsearch", "search": "AI engineer in London", "country": "gb"}, ("europe",)),
    ({"type": "jsearch", "search": "remote AI engineer", "country": "de"}, ("europe",)),
    ({"type": "jsearch", "search": "AI engineer", "country": "us"}, ("us",)),
    ({"type": "arbeitsagentur", "search": "AI Engineer", "where": "München"}, ("europe",)),
    ({"type": "arbeitnow"}, ("europe",)),
    ({"type": "startup_jobs", "search": "AI engineer", "country": "DE"}, ("europe",)),
    ({"type": "startup_jobs", "search": "AI engineer"}, ("europe", "us")),   # unplaced: both
])
def test_feed_regions(feed, regions):
    assert poll.feed_regions(feed) == regions


def test_every_committed_feed_is_in_at_least_one_run_and_city_searches_in_one():
    feeds = poll.load_feeds()
    eu, us = poll.select_region(feeds, "europe"), poll.select_region(feeds, "us")
    labels = lambda fs: {id(f) for f in fs}  # noqa: E731
    assert labels(eu) | labels(us) == labels(feeds)
    seattle = [f for f in feeds if "Seattle" in f.get("search", "")]
    assert seattle and all(f in us and f not in eu for f in seattle)
    berlin = [f for f in feeds if "Berlin" in (f.get("search", "") + f.get("where", ""))]
    assert berlin and all(f in eu and f not in us for f in berlin)


def test_no_region_is_every_feed_and_an_unknown_one_is_an_error():
    feeds = [{"type": "arbeitnow"}]
    assert poll.select_region(feeds, None) == feeds
    with pytest.raises(ValueError, match="unknown region"):
        poll.select_region(feeds, "asia")


def test_the_region_line_names_the_cities_covered():
    feeds = [{"type": "ashby", "token": "x"}, {"type": "jsearch", "search": "AI engineer in Boston", "country": "us"}]
    line = poll.region_line("us", poll.select_region(feeds, "us"))
    assert line.startswith("region us: covers San Francisco, New York")
    assert "Boston" in line and "Berlin" not in line
    assert "2 feeds, 1 of them also fetched" in line


def test_cli_rejects_an_unknown_region():
    p = subprocess.run([sys.executable, "-m", "app", "poll", "--region", "asia", "--no-extract"],
                       cwd=ROOT, capture_output=True, text=True)
    assert p.returncode != 0 and "invalid choice" in p.stderr


# --- the two timers on the server ----------------------------------------------------------

def test_europe_and_us_each_have_a_timer_and_a_service():
    eu_timer = (DEPLOY / "hiring-radar-poll.timer").read_text()
    us_timer = (DEPLOY / "hiring-radar-poll-us.timer").read_text()
    assert "OnCalendar=*-*-* 07:00:00 Europe/Berlin" in eu_timer
    assert "OnCalendar=*-*-* 07:00:00 America/New_York" in us_timer
    assert "python -m app poll --region europe" in (DEPLOY / "hiring-radar-poll.service").read_text()
    assert "python -m app poll --region us" in (DEPLOY / "hiring-radar-poll-us.service").read_text()


def test_hamburg_and_frankfurt_each_have_their_two_google_for_jobs_searches():
    """HIR-466: both cities rested on one German feed; each gets the pair every city has,
    in the Europe run only, and the month's searches stay well under our own cap."""
    from app.sources import jsearch
    feeds = [f for f in poll.load_feeds() if f["type"] == jsearch.SOURCE and f.get("enabled", True)]
    for city in ("Hamburg", "Frankfurt"):
        searches = sorted(f["search"] for f in feeds if geo.city_of(f["search"]) == city)
        assert searches == [f"AI engineer in {city}", f"machine learning engineer in {city}"]
        assert all(poll.feed_regions(f) == (geo.EUROPE,) for f in feeds if geo.city_of(f["search"]) == city)
    assert all(f.get("num_pages", 1) == 1 for f in feeds)   # one request per search per day
    assert len(feeds) * 31 <= jsearch.MONTHLY_CAP * 0.8       # at least the 20% headroom HIR-352 asks


def test_every_us_city_has_its_two_google_for_jobs_searches():
    """HIR-467: San Francisco launched when the searches were capped at 200 a month and never
    got its pair, so it drew only from company boards. Every US city now has the pair, in the
    US run only, and the month's searches stay well under our own cap."""
    from app.sources import jsearch
    feeds = [f for f in poll.load_feeds() if f["type"] == jsearch.SOURCE and f.get("enabled", True)]
    for city in geo.region_places(geo.US):
        mine = [f for f in feeds if geo.city_of(f["search"]) == city]
        searches = {f["search"] for f in mine}
        assert {f"AI engineer in {city}", f"machine learning engineer in {city}"} <= searches, city
        assert all(poll.feed_regions(f) == (geo.US,) for f in mine), city
    assert len(feeds) * 31 <= jsearch.MONTHLY_CAP * 0.8       # at least the 20% headroom HIR-352 asks
