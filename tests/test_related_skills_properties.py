"""Rules the related-skills panel must keep for every set of jobs and every filter.

Hypothesis generates the jobs, their skills and the filters (HIR-333); each job goes in
through the real ingest and extraction-storing path, the same helper tests/test_queries.py
uses, so the numbers checked are the ones the dashboard would show.

One migrated database is built per test and copied in memory for each generated input:
running every migration 200 times would cost more than the property itself.
"""

import sqlite3

import pytest
from hypothesis import event, given, strategies as st

from app import db, queries as q
from tests.test_queries import NOW, add, ts

# Fourteen skills, so a list can pass the ten the panel shows; and a job lists each one more
# often than not, so that enough jobs share skills for a list to appear at all. A generator
# that mostly produced empty lists would pass every rule below without testing anything.
SKILLS = ("python", "rag", "aws", "docker", "sql", "llm", "go", "rust", "k8s", "spark",
          "dbt", "java", "azure", "gcp")
CITIES = ("Berlin", "San Francisco")

side = st.sampled_from((None, "required", "required", "nice_to_have"))
job = st.tuples(
    st.sampled_from(CITIES),
    st.lists(side, min_size=len(SKILLS), max_size=len(SKILLS))
    .map(lambda sides: [(skill, s) for skill, s in zip(SKILLS, sides) if s]))
jobs = st.one_of(st.lists(job, max_size=5), st.lists(job, min_size=10, max_size=30))
filters = st.builds(
    q.Filters,
    window=st.just("all"),
    cities=st.sampled_from(((), ("Berlin",), ("San Francisco",))),
    requirement=st.sampled_from(("required", "all")),
    skill_ids=st.lists(st.sampled_from(SKILLS + ("nothing-asks-for-this",)),
                       min_size=1, max_size=2, unique=True).map(tuple),
)


@pytest.fixture(scope="module")
def template(tmp_path_factory):
    conn = db.connect(tmp_path_factory.mktemp("related") / "template.db")
    db.migrate(conn)
    conn.commit()
    yield conn
    conn.close()


def related(template, job_list, f):
    conn = db.connect(":memory:")
    try:
        template.backup(conn)
        for i, (city, skills) in enumerate(job_list):
            add(conn, f"Co{i}", "AI Engineer", city, "arbeitnow", ts(1), skills)
        r = q.related_skills(conn, f, NOW)
        event("rows listed" if r["skills"] else "no rows")
        return r
    finally:
        conn.close()


@given(jobs, filters)
def test_every_share_shown_is_between_0_and_100_percent(template, job_list, f):
    r = related(template, job_list, f)
    assert 0 <= r["selected_count"] <= r["total"] <= len(job_list)
    for s in r["skills"]:
        assert 0 <= s["pct"] <= 100
        assert 0 <= s["base_pct"] <= 100
        assert s["lift"] > 0


@given(jobs, filters)
def test_a_selected_skill_never_appears_in_its_own_list(template, job_list, f):
    r = related(template, job_list, f)
    listed = [s["skill_id"] for s in r["skills"]]
    assert not set(listed) & set(f.skill_ids)
    assert len(listed) == len(set(listed)) <= q.RELATED_LIMIT


@given(jobs, filters)
def test_every_listed_skill_is_in_at_least_the_minimum_number_of_the_chosen_jobs(template, job_list, f):
    r = related(template, job_list, f)
    for s in r["skills"]:
        assert q.MIN_CO_JOBS <= s["count"] <= r["selected_count"]
        # ...and the count is the real one: the chosen jobs (those listing every selected
        # skill, in the filtered city) that also list this skill, counted from the input.
        sides = ("required",) if f.requirement == "required" else ("required", "nice_to_have")
        chosen = [dict(skills) for city, skills in job_list
                  if (not f.cities or city in f.cities)
                  and all(dict(skills).get(sel) in sides for sel in f.skill_ids)]
        assert s["count"] == sum(1 for have in chosen if have.get(s["skill_id"]) in sides)
