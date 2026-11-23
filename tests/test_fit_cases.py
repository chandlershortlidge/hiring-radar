"""The fit logic in Python gives the browser's answers (HIR-435).

tests/fixtures/fit_cases.json holds profiles, jobs and what web/src/profile.js answers for
each; web/src/fitCases.test.js checks the browser against the same file. So a change to
fit, gates or ranking on one side fails the other side's tests until both agree."""

import json
from pathlib import Path

import pytest

from app import fit as F

CASES = json.loads((Path(__file__).parent / "fixtures" / "fit_cases.json").read_text())
JOBS = CASES["jobs"]
BY_ID = {str(j["id"]): j for j in JOBS}
PROFILES = list(CASES["expected"])


def same(a, b):
    """Equal, with scores compared to 1e-12: the two languages do the same float steps."""
    if isinstance(a, float) or isinstance(b, float):
        return a == pytest.approx(b, abs=1e-12)
    return a == b


def test_the_fixture_covers_every_case_the_tool_relies_on():
    # Guards against the file being cut down to cases that agree trivially.
    assert len(JOBS) >= 20 and len(PROFILES) >= 4
    assert CASES["fit_days"] == F.FIT_DAYS


@pytest.mark.parametrize("name", PROFILES)
def test_fit_matches_the_browser(name):
    profile, expected = CASES["profiles"][name], CASES["expected"][name]
    for jid, want in expected["fit"].items():
        got = F.fit(profile, BY_ID[jid], CASES["demand"])
        assert got.keys() == want.keys(), jid
        for k in want:
            assert same(got[k], want[k]), (name, jid, k, got[k], want[k])


@pytest.mark.parametrize("name", PROFILES)
def test_missing_keeps_arrival_order_without_demand(name):
    profile = CASES["profiles"][name]
    for jid, want in CASES["expected"][name]["fit_without_demand_missing"].items():
        assert F.fit(profile, BY_ID[jid])["missing"] == want, jid


@pytest.mark.parametrize("name", PROFILES)
def test_gates_and_met_skills_match_the_browser(name):
    profile, expected = CASES["profiles"][name], CASES["expected"][name]
    for jid, job in BY_ID.items():
        assert F.gates(profile, job) == expected["gates"][jid], jid
        assert sorted(F.met_skills(profile, job)) == expected["met_skills"][jid], jid


@pytest.mark.parametrize("name", PROFILES)
def test_ranking_matches_the_browser(name):
    profile, expected = CASES["profiles"][name], CASES["expected"][name]
    assert [j["id"] for j in F.rank_jobs(profile, JOBS, CASES["demand"])] == expected["order"]
    recent = F.recent_jobs(JOBS, CASES["now"])
    assert [j["id"] for j in F.rank_jobs(profile, recent, CASES["demand"])] == expected["order_recent"]


@pytest.mark.parametrize("name", PROFILES)
def test_is_match_matches_the_browser(name):
    profile = CASES["profiles"][name]
    assert [j["id"] for j in JOBS if F.is_match(profile, j)] == CASES["expected"][name]["matches"]


def test_job_seniority_and_recent_jobs_match_the_browser():
    assert {str(j["id"]): F.job_seniority(j) for j in JOBS} == CASES["job_seniority"]
    assert [j["id"] for j in F.recent_jobs(JOBS, CASES["now"])] == CASES["recent"]


# The cases the fixture is built around, checked by hand so the file cannot drift into
# agreeing on wrong answers.

def test_hand_checked_cases():
    mid = CASES["profiles"]["mid_python_rag"]
    assert F.job_seniority(BY_ID["9"]) is None          # "Junior Lead": both words, so silent
    assert F.job_seniority(BY_ID["10"]) == "mid"        # the stored level beats "Lead" in the title
    assert F.job_seniority(BY_ID["19"]) is None         # "Internal" is not "intern"
    assert F.gates(mid, BY_ID["7"]) == []               # degree with "or equivalent" never gates
    assert F.gates(mid, BY_ID["6"]) == ["degree"]
    assert F.fit(mid, BY_ID["2"])["rank_score"] == pytest.approx(0.1500, abs=1e-4)   # 2/2 as 2 of 4
    assert F.fit(mid, BY_ID["11"])["total"] == 2        # a group of alternatives is one requirement
    blank = CASES["profiles"]["blank"]
    assert F.fit(blank, BY_ID["15"])["rank_score"] == 0.0   # exactly 0, not float noise (HIR-333)
    assert F.fit(blank, BY_ID["13"])["score"] is None       # no required skill: unknown, not 0
    ids = [j["id"] for j in F.recent_jobs(JOBS, CASES["now"])]
    assert 19 in ids and 20 not in ids and 21 not in ids    # 30 days in, 30 days + 1 hour out, no date out


def test_no_profile_means_no_fit_and_no_reordering():
    assert F.fit(None, JOBS[0]) is None
    assert F.rank_jobs(None, JOBS) is JOBS
    assert F.gates(None, JOBS[3]) == []
