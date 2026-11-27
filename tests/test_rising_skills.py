"""What's rising (HIR-232): which jobs count as open during a period, when a comparison is
shown at all, and the two things held back because their early numbers would be an
artefact: a newly launched city and a skill added to the list part-way through.

The comparison itself (shares, change, the trust thresholds) is app.rising's and is tested
in tests/test_rising.py; these tests only feed it counts.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import db, geo, queries as q, scope
from app.api import create_app
from app.taxonomy import Taxonomy, load_added
from scripts.record_skill_ids import with_dates
from tests.test_queries import add

NOW = "2027-03-01T12:00:00Z"
ROOT = Path(__file__).resolve().parent.parent
OLD = {"Berlin": "2026-10-18", "San Francisco": "2026-11-03"}     # both long before either period
ADDED = {s: "2026-10-16" for s in ("python", "rag", "docker", "agents", "kubernetes")}
BERLIN_AI = q.Filters(cities=("Berlin",), families=("ai-engineer",))
TAX = Taxonomy({"version": 3, "skills": [
    {"id": "python", "display": "Python"}, {"id": "rag", "display": "RAG"}, {"id": "docker", "display": "Docker"},
    {"id": "agents", "display": "Agents"}, {"id": "kubernetes", "display": "Kubernetes"}]})


def ago(days: int) -> str:
    return q._days_ago(NOW, days)


_n = iter(range(10_000))


def job(conn, first: int, last: int, skills=(), city="Berlin", title="AI Engineer"):
    """One feed job first seen `first` days ago and last listed `last` days ago."""
    job_id = add(conn, f"Co{next(_n)}", title, city, "greenhouse", ago(first), [(s, "required") for s in skills])
    conn.execute("UPDATE job SET last_seen = ? WHERE id = ?", (ago(last), job_id))
    conn.execute("UPDATE job_source SET last_seen = ? WHERE job_id = ?", (ago(last), job_id))
    return job_id


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    yield c
    c.close()


def market(conn, both=20, earlier_only=10, later_only=10):
    """A Berlin AI Engineer market over the two periods (earlier = 56 to 28 days ago, later
    = the last 28): `both` jobs open throughout, all wanting python and 6 of them rag;
    `earlier_only` jobs that closed in the earlier period, 6 wanting docker; `later_only`
    jobs that opened in the later one, 8 wanting agents and 2 kubernetes."""
    for i in range(both):
        job(conn, 50, 0, ["python", "rag"] if i < 6 else ["python"])
    for i in range(earlier_only):
        job(conn, 50, 40, ["docker"] if i < 6 else [])
    for i in range(later_only):
        job(conn, 10, 0, ["agents"] if i < 8 else ["kubernetes"])


def rising(conn, f=BERLIN_AI, now=NOW, added=ADDED, since=OLD):
    return q.rising_skills(conn, f, now, added, since)


# --- the open-in-window rule ------------------------------------------------------------

def test_a_job_counts_in_every_period_it_was_open_in(conn):
    job(conn, 70, 60, ["python"])    # closed before the earlier period began: in neither
    job(conn, 50, 40, ["python"])    # opened and closed inside the earlier period
    job(conn, 50, 1, ["python"])     # open throughout: in both
    job(conn, 10, 0, ["python"])     # opened in the later period: only there
    earlier = q._open_during(conn, BERLIN_AI, ago(56), ago(28))
    later = q._open_during(conn, BERLIN_AI, ago(28), NOW)
    assert earlier == (2, {"python": 2})
    assert later == (2, {"python": 2})


def test_open_at_a_periods_start_follows_the_dashboards_open_rule(conn):
    # The dashboard calls a feed job open for FEED_OPEN_DAYS after its last listing. So a
    # job last listed 30 days ago was still shown as open 28 days ago, when the later
    # period began, and one last listed 32 days ago was not.
    job(conn, 50, 28 + q.FEED_OPEN_DAYS - 1)
    job(conn, 50, 28 + q.FEED_OPEN_DAYS + 1)
    assert q._open_during(conn, BERLIN_AI, ago(56), ago(28))[0] == 2
    assert q._open_during(conn, BERLIN_AI, ago(28), NOW)[0] == 1


def test_only_the_chosen_city_and_family_are_counted(conn):
    job(conn, 50, 0, ["python"])
    job(conn, 50, 0, ["python"], city="San Francisco")
    job(conn, 50, 0, ["python"], title="ML Engineer")
    assert q._open_during(conn, BERLIN_AI, ago(28), NOW) == (1, {"python": 1})
    assert q._open_during(conn, q.Filters(cities=("Berlin",)), ago(28), NOW)[0] == 2


def test_nice_to_have_counts_only_when_asked_for(conn):
    add(conn, "Nice", "AI Engineer", "Berlin", "greenhouse", ago(1), [("rag", "nice_to_have")])
    assert q._open_during(conn, BERLIN_AI, ago(28), NOW) == (1, {})
    wide = q.Filters(cities=("Berlin",), families=("ai-engineer",), requirement="all")
    assert q._open_during(conn, wide, ago(28), NOW) == (1, {"rag": 1})


# --- risers and fallers -----------------------------------------------------------------

def test_risers_and_fallers_carry_the_counts_behind_them(conn):
    market(conn)
    r = rising(conn)
    assert r["status"] == "ok" and r["reason"] is None and r["window_days"] == 28
    assert r["current"] == {"start": ago(28), "end": NOW, "open_jobs": 30}
    assert r["previous"] == {"start": ago(56), "end": ago(28), "open_jobs": 30}
    assert r["risers"] == [{"skill_id": "agents", "current_count": 8, "previous_count": 0,
                            "current_share": 26.7, "previous_share": 0.0, "change": 26.7}]
    assert r["fallers"] == [{"skill_id": "docker", "current_count": 0, "previous_count": 6,
                             "current_share": 0.0, "previous_share": 20.0, "change": -20.0}]


def test_a_share_that_did_not_move_is_neither_rising_nor_falling(conn):
    market(conn)
    shown = {s["skill_id"] for s in rising(conn)["risers"] + rising(conn)["fallers"]}
    assert "python" not in shown and "rag" not in shown      # 20 of 30 and 6 of 30, both periods


def test_a_skill_in_too_few_jobs_is_left_out(conn):
    market(conn)
    assert "kubernetes" not in {s["skill_id"] for s in rising(conn)["risers"]}   # 2 jobs, then 0


def test_the_biggest_moves_come_first_and_the_list_is_short(conn):
    for _ in range(30):
        job(conn, 50, 0)
    names = [f"s{i}" for i in range(q.RISING_LIMIT + 2)]
    for i, name in enumerate(names):                      # s0 in 5 new jobs, s1 in 6, ...
        for _ in range(5 + i):
            job(conn, 10, 0, [name])
    r = rising(conn, added={n: "2026-10-16" for n in names})
    assert [s["skill_id"] for s in r["risers"]] == names[::-1][:q.RISING_LIMIT]
    assert r["fallers"] == []


# --- the minimum-data threshold ---------------------------------------------------------

def test_too_few_open_jobs_in_one_period_shows_nothing(conn):
    market(conn, both=12, earlier_only=7, later_only=10)      # 19 jobs in the earlier period
    r = rising(conn)
    assert (r["status"], r["reason"]) == ("not_enough_data", "few_jobs")
    assert r["risers"] == [] and r["fallers"] == []
    assert r["previous"]["open_jobs"] == 19 and r["current"]["open_jobs"] == 22


def test_one_more_job_is_enough(conn):
    market(conn, both=12, earlier_only=8, later_only=10)      # 20 in the earlier period
    assert rising(conn)["status"] == "ok"


def test_an_empty_market_is_not_enough_data(conn):
    assert rising(conn)["reason"] == "few_jobs"


# --- a newly launched city --------------------------------------------------------------

def test_a_newly_launched_city_is_hidden_until_both_periods_are_covered(conn):
    market(conn)
    r = rising(conn, since={"Berlin": ago(30)[:10]})          # launched 30 days ago
    assert (r["status"], r["reason"]) == ("not_enough_data", "new_city")
    assert r["risers"] == [] and r["fallers"] == []
    assert r["ready_from"] == q._days_ago(NOW, 30 - 56)[:10]  # 56 days after the launch
    assert r["current"]["open_jobs"] is None                  # nothing was counted


def test_a_city_is_shown_from_the_day_the_earlier_period_starts_at_its_launch(conn):
    market(conn)
    assert rising(conn, since={"Berlin": ago(55)[:10]})["reason"] == "new_city"
    assert rising(conn, since={"Berlin": ago(56)[:10]})["status"] == "ok"


def test_the_german_cities_launched_on_8_november_show_from_3_january(conn):
    f = q.Filters(cities=("Hamburg",))
    before = q.rising_skills(conn, f, "2027-01-02T23:00:00Z", ADDED)
    assert (before["reason"], before["ready_from"]) == ("new_city", "2027-01-03")
    assert q.rising_skills(conn, f, "2027-01-03T00:00:00Z", ADDED)["reason"] == "few_jobs"


def test_several_cities_wait_for_the_newest_of_them(conn):
    market(conn)
    f = q.Filters(cities=("Berlin", "San Francisco"))
    r = rising(conn, f, since={"Berlin": ago(100)[:10], "San Francisco": ago(20)[:10]})
    assert r["reason"] == "new_city" and r["ready_from"] == q._days_ago(NOW, 20 - 56)[:10]


def test_a_city_with_no_start_date_is_hidden(conn):
    market(conn)
    r = rising(conn, since={})
    assert (r["reason"], r["ready_from"]) == ("new_city", None)


def test_no_city_compares_the_places_that_are_ready_and_names_the_rest(conn):
    """HIR-442: with no city chosen, a newly launched place is left out rather than holding
    the answer back for every other place; the answer says which places were counted."""
    market(conn)
    for _ in range(5):
        job(conn, 10, 0, ["agents"], city="San Francisco")         # would move the shares if counted
    f = q.Filters(families=("ai-engineer",))
    r = rising(conn, f, since={"Berlin": ago(100)[:10], "San Francisco": ago(20)[:10]})
    assert (r["status"], r["reason"], r["ready_from"]) == ("ok", None, None)
    assert r["places"]["included"] == ["Berlin"]
    excluded = {w["place"]: w["ready_from"] for w in r["places"]["excluded"]}
    assert excluded["San Francisco"] == q._days_ago(NOW, 20 - 56)[:10]
    assert excluded["Munich"] is None                              # no start date: not collected
    berlin_only = rising(conn, BERLIN_AI, since={"Berlin": ago(100)[:10]})
    assert {k: r[k] for k in ("current", "previous", "risers", "fallers")} == \
        {k: berlin_only[k] for k in ("current", "previous", "risers", "fallers")}


def test_no_city_with_every_place_ready_counts_every_job(conn):
    market(conn)
    every = {place: "2020-01-01" for place in scope.live_places()}
    r = rising(conn, q.Filters(families=("ai-engineer",)), since=every)
    assert r["status"] == "ok" and r["places"]["excluded"] == []
    assert r["places"]["included"] == list(scope.live_places())
    assert r["current"]["open_jobs"] == 30


def test_no_city_with_no_place_ready_waits_for_the_first_one(conn):
    market(conn)
    r = rising(conn, q.Filters(), since={"Berlin": ago(20)[:10], "San Francisco": ago(10)[:10]})
    assert (r["status"], r["reason"]) == ("not_enough_data", "new_city")
    assert r["ready_from"] == q._days_ago(NOW, 20 - 56)[:10]        # Berlin's day, the earliest
    assert r["places"]["included"] == [] and r["current"]["open_jobs"] is None


def test_a_named_city_still_holds_the_answer_back(conn):
    market(conn)
    r = rising(conn, q.Filters(cities=("Berlin", "San Francisco")),
               since={"Berlin": ago(100)[:10], "San Francisco": ago(20)[:10]})
    assert r["reason"] == "new_city" and r["places"]["included"] == []
    assert r["places"]["excluded"] == [{"place": "San Francisco", "ready_from": q._days_ago(NOW, 20 - 56)[:10]}]


def test_every_active_place_has_the_day_its_collection_began():
    assert set(geo.ACTIVE_CITIES) <= set(geo.COLLECTING_SINCE), (
        "a newly launched city needs its launch day in geo.COLLECTING_SINCE, "
        "or \"what's rising\" stays hidden for it")


# --- a skill added part-way through -----------------------------------------------------

def test_a_skill_added_mid_window_is_not_shown_as_rising_from_zero(conn):
    market(conn)
    r = rising(conn, added={**ADDED, "agents": ago(40)[:10]})    # added inside the earlier period
    assert r["status"] == "ok" and r["risers"] == []
    assert [s["skill_id"] for s in r["fallers"]] == ["docker"]   # the rest is unaffected


def test_a_skill_is_compared_once_it_existed_through_both_periods(conn):
    market(conn)
    assert rising(conn, added={**ADDED, "agents": ago(55)[:10]})["risers"] == []
    assert [s["skill_id"] for s in rising(conn, added={**ADDED, "agents": ago(56)[:10]})["risers"]] == ["agents"]


def test_a_skill_with_no_date_is_left_out(conn):
    market(conn)
    assert rising(conn, added={})["risers"] == []


def test_every_skill_on_the_list_has_the_day_it_was_added():
    ids = {s["id"] for s in json.loads((ROOT / "taxonomy" / "skills.json").read_text())["skills"]}
    added = load_added()
    assert ids == set(added), (
        "taxonomy/added.json and taxonomy/skills.json disagree; "
        "run `uv run python scripts/record_skill_ids.py` after adding a skill")
    assert all(len(d) == 10 and d[4] == d[7] == "-" for d in added.values())


def test_recording_dates_a_new_skill_today_and_keeps_the_old_dates():
    assert with_dates({"python", "agents"}, {"python": "2026-10-16"}, "2027-03-01") == {
        "agents": "2027-03-01", "python": "2026-10-16"}


# --- the endpoint -----------------------------------------------------------------------

@pytest.fixture
def client(tmp_path, monkeypatch):
    path = tmp_path / "t.db"
    c = db.connect(path)
    db.migrate(c)
    market(c)
    c.close()
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    return TestClient(create_app(path, TAX, skill_added=ADDED))


def test_the_endpoint_returns_risers_and_fallers_for_berlin_ai_engineers(client):
    r = client.get("/api/skills/rising", params={"city": "Berlin", "family": "ai-engineer"}).json()
    assert r["status"] == "ok"
    assert r["current"]["open_jobs"] == 30 and r["previous"]["open_jobs"] == 30
    assert r["risers"] == [{"skill_id": "agents", "display": "Agents", "current_count": 8, "previous_count": 0,
                            "current_share": 26.7, "previous_share": 0.0, "change": 26.7}]
    assert r["fallers"] == [{"skill_id": "docker", "display": "Docker", "current_count": 0, "previous_count": 6,
                             "current_share": 0.0, "previous_share": 20.0, "change": -20.0}]


def test_the_endpoint_ignores_the_other_filters_and_rejects_a_bad_family(client):
    narrowed = client.get("/api/skills/rising", params={"city": "Berlin", "seniority": "junior", "window": "30d"}).json()
    assert narrowed["status"] == "ok" and narrowed["current"]["open_jobs"] == 30
    assert client.get("/api/skills/rising", params={"city": "Berlin", "family": "plumber"}).status_code == 422
    # A place we do not collect has no start date, so it is "not enough data", never an error.
    assert client.get("/api/skills/rising", params={"city": "Paris"}).json()["reason"] == "new_city"
