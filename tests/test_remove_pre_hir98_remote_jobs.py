import importlib.util

from pathlib import Path

import pytest

from app import db

_spec = importlib.util.spec_from_file_location(
    "remove_pre_hir98_remote_jobs",
    Path(__file__).parent.parent / "scripts" / "remove_pre_hir98_remote_jobs.py")
script = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(script)

# The shapes seen on the 2026-11-01 production backup (HIR-110). Every one of these was
# stored with the pre-HIR-98 stamp; what differs is where today's intake would put it.
ZURICH = "Zürich (remote, Germany)"          # non-EU: today's intake drops it
STUTTGART = "Stuttgart (remote, Germany)"    # untracked German city: a person's call (HIR-102)
BERLIN = "Berlin (remote, Germany)"          # a city match wins, stored city unchanged
REMOTE_JOB = "Remote job (remote, Germany)"  # the feed's own literal, still EU-remote today


def _add_job(conn, company, location_raw, city, source="arbeitnow", mentions=0, rejects=0):
    job = conn.execute(
        "INSERT INTO job (company, title, title_key, city, location_raw, description_text, "
        "first_seen, last_seen) VALUES (?, 'AI Engineer', 'ai engineer', ?, ?, 'jd', 't1', 't2')",
        (company, city, location_raw)).lastrowid
    conn.execute("INSERT INTO job_source (job_id, source, source_job_id, first_seen, last_seen) "
                 "VALUES (?, ?, ?, 't1', 't2')", (job, source, f"sid-{job}"))
    for i in range(mentions):
        conn.execute("INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text, "
                     "taxonomy_version, extractor_version) VALUES (?, ?, 'required', 'q', 1, 'v1')",
                     (job, f"skill-{i}"))
    for i in range(rejects):
        conn.execute("INSERT INTO extraction_reject (job_id, reason, skill_id, raw_text, item, "
                     "extractor_version) VALUES (?, 'unknown_skill', ?, 'q', '{}', 'v1')",
                     (job, f"junk-{i}"))
    conn.commit()
    return job


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def test_only_rows_todays_intake_would_place_differently_are_candidates(conn):
    zurich = _add_job(conn, "Lightly AG", ZURICH, "Remote (EU)")
    stuttgart = _add_job(conn, "hurra.com", STUTTGART, "Remote (EU)")
    _add_job(conn, "Berlin GmbH", BERLIN, "Berlin")
    _add_job(conn, "Tether", REMOTE_JOB, "Remote (EU)")

    found = script.candidates(conn)

    # Berlin still resolves to Berlin and "Remote job" still resolves to Remote (EU), so
    # neither is damage this cleanup can see. The two bare city names are.
    assert sorted(c["id"] for c in found) == sorted([zurich, stuttgart])
    assert {c["place_today"] for c in found} == {None}


def test_a_stamp_from_a_feed_that_supplies_its_own_country_is_not_a_candidate(conn):
    # startup_jobs builds the same string out of the feed's own location.country, so it was
    # never fabricated — whatever the location looks like.
    _add_job(conn, "Kubermatic GmbH", "Hamburg (remote, Germany)", "Remote (EU)",
             source="startup_jobs")

    assert script.candidates(conn) == []


def test_an_unstamped_row_is_never_a_candidate(conn):
    _add_job(conn, "Acme", "Berlin", "Berlin")
    _add_job(conn, "Acme Remote", "Remote (Germany)", "Remote (EU)")

    assert script.candidates(conn) == []


def test_deletes_only_the_confirmed_candidate_and_cascades_its_children(conn):
    zurich = _add_job(conn, "Lightly AG", ZURICH, "Remote (EU)", mentions=4, rejects=2)
    stuttgart = _add_job(conn, "hurra.com", STUTTGART, "Remote (EU)", mentions=17)

    result = script.remove(conn, confirm={zurich})

    assert [c["id"] for c in result["removed"]] == [zurich]
    assert result["removed"][0]["mentions"] == 4
    assert [c["id"] for c in result["left"]] == [stuttgart]
    assert [r[0] for r in conn.execute("SELECT id FROM job ORDER BY id")] == [stuttgart]
    # The cascade took the Zürich row's children and left the Stuttgart row's alone.
    assert conn.execute("SELECT COUNT(*) FROM skill_mention").fetchone()[0] == 17
    assert conn.execute("SELECT COUNT(*) FROM extraction_reject").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM job_source").fetchone()[0] == 1


def test_confirming_nothing_deletes_nothing(conn):
    _add_job(conn, "Lightly AG", ZURICH, "Remote (EU)", mentions=4)

    result = script.remove(conn, confirm=set())

    assert result["removed"] == []
    assert len(result["left"]) == 1
    assert conn.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 1


def test_a_dry_run_reports_the_delete_and_rolls_it_back(conn):
    zurich = _add_job(conn, "Lightly AG", ZURICH, "Remote (EU)", mentions=4)

    result = script.remove(conn, confirm={zurich}, commit=False)

    assert [c["id"] for c in result["removed"]] == [zurich]
    assert conn.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM skill_mention").fetchone()[0] == 4


def test_confirming_a_job_that_is_not_a_candidate_is_refused(conn):
    # A typed id cannot reach a row this cleanup does not own: the Berlin row is placed by
    # today's intake exactly as it is stored.
    berlin = _add_job(conn, "Berlin GmbH", BERLIN, "Berlin", mentions=3)

    with pytest.raises(RuntimeError, match="not candidates"):
        script.remove(conn, confirm={berlin})
    assert conn.execute("SELECT COUNT(*) FROM job").fetchone()[0] == 1


def test_refuses_to_run_with_foreign_keys_off(conn):
    zurich = _add_job(conn, "Lightly AG", ZURICH, "Remote (EU)", mentions=4)
    conn.execute("PRAGMA foreign_keys = OFF")

    with pytest.raises(RuntimeError, match="foreign keys are off"):
        script.remove(conn, confirm={zurich})


def test_running_twice_finds_nothing_the_second_time(conn):
    zurich = _add_job(conn, "Lightly AG", ZURICH, "Remote (EU)", mentions=4)

    script.remove(conn, confirm={zurich})

    assert script.candidates(conn) == []
