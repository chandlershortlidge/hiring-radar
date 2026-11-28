""""This job doesn't belong here" flags (HIR-226): what a flag records, that it never
changes, and what `python -m app flags` concludes from it.

The two examples the ticket names are the first two tests of the diagnosis section: a
"Senior Staff Software Engineer" platform job seen under AI Engineer + Berlin, and a Senior
job seen under the Junior filter.
"""

import json
import sqlite3

import pytest
from fastapi.testclient import TestClient

import app.__main__ as cli
from app import db, flags, queries as q
from app.api import create_app
from app.extract import Extraction, Mention, Seniority
from app.ingest import ingest_one
from app.pipeline import store_extraction
from app.repair import merge_jobs
from app.sources import Posting
from app.taxonomy import Taxonomy
from tests.test_frontend_lists import js_keys

NOW = "2026-11-09T08:00:00Z"
TAX = Taxonomy({"version": 3, "skills": [{"id": "python", "display": "Python"},
                                         {"id": "kubernetes", "display": "Kubernetes"}]})

PLATFORM_TEXT = (
    "We are hiring a Senior Staff Software Engineer for our developer platform team in Berlin. "
    "You will own the infrastructure our product teams deploy on: Kubernetes clusters, Terraform, "
    "CI/CD pipelines and observability. You design distributed systems for the backend and keep the "
    "cloud bill honest. Some of the teams you support train ML models. Python and Go required. "
    + "We offer a fair salary, a quiet office and a team that reviews each other's work. " * 6)
JUNIOR_TEXT = ("Acme is looking for an engineer to build LLM features with our AI team. "
               "You have Python experience and want to grow. Entry-level candidates welcome. ") * 8


def job(conn, title, text, company="Acme", location="Berlin, Germany", source="arbeitnow",
        seniority=Seniority(None, None, None), skills=(("python", "Python"),)):
    p = Posting(source, "" if source == "paste" else f"{company}-{title}", "https://example.com/j", company,
                title, location, text)
    job_id = ingest_one(conn, p, "2026-11-08T07:00:00Z", require_city=False, trust_title=True).job_id
    store_extraction(conn, job_id, Extraction(
        seniority=seniority, mentions=[Mention(s, "required", quote) for s, quote in skills],
        extractor_version="x1", taxonomy_version=3))
    return job_id


def view(url="/berlin/ai-engineer", page="list", **filters):
    """The dashboard state as the browser sends it (web/src/flagView.js)."""
    base = {"cities": [], "compare": False, "seniorities": [], "families": [], "requirement": "required",
            "window": "open", "german": "any", "degree": "any", "production": "any", "skillIds": [],
            "query": "", "text": ""}
    return {"page": page, "url": url, "sort": "newest", "saved": False,
            "market": {"view": "city", "place": "berlin", "family": None, "cities": []},
            "filters": {**base, **filters}}


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def report(conn) -> str:
    return "\n".join(flags.report_lines(flags.open_flags(conn)))


def section(text: str, heading: str) -> str:
    """The lines under one cause heading, up to the next blank line."""
    assert heading in text, f"no “{heading}” group in:\n{text}"
    return text.split(heading, 1)[1].split("\n\n", 1)[0]


# --- the diagnosis: the ticket's two examples -------------------------------------------

def test_the_platform_job_seen_under_ai_engineer_in_berlin_is_a_wrong_family_reading(conn):
    # The ticket's title was "Senior Staff Software Engineer"; since HIR-397 that title is
    # the software engineer track, so the remainder case is shown with a title naming none.
    job_id = job(conn, "Senior Staff Engineer", PLATFORM_TEXT)
    assert q.job_detail(conn, job_id, NOW)["family"] == "ai-engineer"   # the title rule's remainder
    flags.add_flag(conn, job_id, view(families=["ai-engineer"], cities=["Berlin"]), "it's a platform role", NOW)
    out = section(report(conn), "job family reading is wrong (1)")
    assert "Acme — Senior Staff Engineer · arbeitnow" in out and "note: “it's a platform role”" in out
    assert "View: AI Engineer. Stored job family: AI Engineer." in out
    assert "names no AI or ML work" in out
    assert "Title and text describe platform/infrastructure engineering" in out and "AI or ML mentioned 1 time → job family reading is wrong." in out
    # Berlin was on screen too and is compared, but nothing is found against it.
    assert "View: Berlin. Stored city: Berlin." in out and "city reading is wrong" not in report(conn)


def test_a_senior_job_seen_under_the_junior_filter_is_a_wrong_seniority_reading(conn):
    job_id = job(conn, "Senior Staff AI Engineer", JUNIOR_TEXT,
                 seniority=Seniority("junior", "stated", "Entry-level candidates welcome"))
    flags.add_flag(conn, job_id, view(seniorities=["junior"]), None, NOW)
    out = section(report(conn), "seniority reading is wrong (1)")
    assert "View: Junior. Stored seniority: junior (stated: “Entry-level candidates welcome”)." in out
    assert "Title says “Senior Staff” → seniority reading is wrong." in out
    assert "job family reading is wrong" not in report(conn)


# --- the diagnosis: the other causes ----------------------------------------------------

def test_platform_text_alone_is_enough_when_the_title_does_name_ai(conn):
    job_id = job(conn, "Software Engineer, AI Platform", PLATFORM_TEXT.replace("ML models", "models"))
    flags.add_flag(conn, job_id, view(families=["ai-engineer"]), None, NOW)
    out = section(report(conn), "job family reading is wrong (1)")
    assert "AI or ML mentioned 0 times" in out and "names no AI or ML work" not in out


def test_a_job_that_fits_its_filters_is_listed_as_not_explained_with_its_evidence(conn):
    job_id = job(conn, "AI Engineer", JUNIOR_TEXT, seniority=Seniority("junior", "stated", "Entry-level candidates welcome"))
    flags.add_flag(conn, job_id, view(families=["ai-engineer"], seniorities=["junior"], cities=["Berlin"]), None, NOW)
    out = section(report(conn), "not explained by any rule (read the evidence) (1)")
    assert out.count("nothing found against it") == 4          # family, seniority, city, open
    assert "seen on: /berlin/ai-engineer" in out and "read by extractor version: x1" in out


def test_a_stored_value_the_filter_excludes_is_reported_as_the_filter_not_holding(conn):
    job_id = job(conn, "AI Engineer", JUNIOR_TEXT, seniority=Seniority("senior", "stated", "grow"))
    flags.add_flag(conn, job_id, view(seniorities=["junior"], german="required", degree="required",
                                      skillIds=["kubernetes"]), None, NOW)
    out = section(report(conn), "the filter did not hold (the stored value does not match it) (1)")
    for stored in ("Stored seniority: senior", "Stored German: not asked for", "Stored degree: not asked for",
                   "Stored skill: kubernetes not stored"):
        assert stored in out


def test_a_location_todays_rule_places_elsewhere_is_a_wrong_city_reading(conn):
    job_id = job(conn, "AI Engineer", JUNIOR_TEXT, location="Berlin, Germany")
    snap_view = view(cities=["Berlin"])
    flags.add_flag(conn, job_id, snap_view, None, NOW)
    f = flags.open_flags(conn)[0]
    moved = {**f["job"], "location_raw": "Munich, Germany"}       # stored as Berlin, the line says Munich
    checks = flags.diagnose(snap_view, moved, f["text"])
    assert flags.causes_of(checks) == [flags.CITY]
    assert "“Munich, Germany”, which today's rule places in Munich" in checks[0].line()


def test_a_quote_that_is_not_in_the_posting_is_a_wrong_reading(conn):
    job_id = job(conn, "AI Engineer", JUNIOR_TEXT, skills=(("python", "Python"), ("kubernetes", "K8s in anger")))
    flags.add_flag(conn, job_id, view(skillIds=["python", "kubernetes"]), None, NOW, skill_names={"kubernetes": "Kubernetes"})
    out = section(report(conn), "skill reading is wrong (1)")
    assert "View: requires Kubernetes. Stored skill: Kubernetes, required (“K8s in anger”). The quote it rests on is not in the posting" in out
    assert "View: requires python." in out and out.count("skill reading is wrong.") == 1


def test_an_out_of_scope_title_and_a_recruiter_are_causes_with_no_filter_on(conn):
    a = job(conn, "Senior Staff Engineer", PLATFORM_TEXT)
    b = job(conn, "AI Engineer", JUNIOR_TEXT, company="Hays Recruiting GmbH", source="greenhouse")
    by_hand = job(conn, "Office Manager", JUNIOR_TEXT, company="Beta", source="paste")
    for j in (a, b, by_hand):
        flags.add_flag(conn, j, view(url="/berlin"), None, NOW)
    out = report(conn)
    assert "Senior Staff Engineer" in section(out, "feed relevance (the job should not have been collected) (1)")
    assert "The company name contains “recruit”" in section(out, "agency (posted by a recruiter or a job board) (1)")
    # A job a person added by hand was chosen, not collected: the title rule does not apply.
    assert "Office Manager" in section(out, "not explained by any rule (read the evidence) (1)")


def test_no_filter_is_judged_for_a_flag_from_the_jobs_own_page_or_the_saved_list(conn):
    job_id = job(conn, "Senior Staff AI Engineer", JUNIOR_TEXT, seniority=Seniority("junior", "stated", "grow"))
    flags.add_flag(conn, job_id, view(url=f"/jobs/{job_id}", page="job", seniorities=["junior"]), None, NOW)
    flags.add_flag(conn, job_id, {**view(seniorities=["junior"]), "saved": True}, None, NOW)
    out = report(conn)
    assert "seniority reading is wrong" not in out and "not explained by any rule (read the evidence) (2)" in out
    assert f"the job's own page (/jobs/{job_id}); no filter decided that it showed" in out
    assert "the saved list, which no filter narrows" in out


def test_no_open_flags_says_so(conn):
    assert flags.report_lines(flags.open_flags(conn)) == ["No open flags."]


# --- every filter is captured -----------------------------------------------------------

def test_every_filter_the_dashboard_keeps_is_known_to_the_diagnosis():
    """Add a filter to the dashboard's state and this fails until the diagnosis either
    judges it or says why it says nothing about a job."""
    dashboard = set(js_keys("App.jsx", "DEFAULT"))
    assert dashboard == set(flags.VIEW_FILTERS), (
        f"dashboard only: {sorted(dashboard - set(flags.VIEW_FILTERS))};"
        f" diagnosis only: {sorted(set(flags.VIEW_FILTERS) - dashboard)}")


def test_every_filter_the_server_can_apply_has_a_dashboard_key_the_flag_carries():
    """The server's own filter list, from the other side: each field of queries.Filters
    arrives in a flag under the dashboard's name for it."""
    sent_as = {"skill_ids": "skillIds"}
    assert {sent_as.get(f, f) for f in q.Filters.__dataclass_fields__} <= set(flags.VIEW_FILTERS)


def test_a_filter_newer_than_the_diagnosis_is_stored_and_reported_not_dropped(conn):
    job_id = job(conn, "AI Engineer", JUNIOR_TEXT)
    flags.add_flag(conn, job_id, view(visa="sponsored"), None, NOW)
    assert flags.open_flags(conn)[0]["view"]["filters"]["visa"] == "sponsored"
    assert "View: visa = 'sponsored'." in report(conn) and "newer than the diagnosis" in report(conn)


# --- what a flag records, and that it stays ---------------------------------------------

def test_a_flag_records_the_job_as_stored_and_survives_a_re_read(conn):
    job_id = job(conn, "Senior Staff AI Engineer", JUNIOR_TEXT, seniority=Seniority("junior", "stated", "grow"))
    flags.add_flag(conn, job_id, view(seniorities=["junior"]), None, NOW, skill_names={"python": "Python"})
    before = flags.open_flags(conn)[0]["job"]
    assert {k: before[k] for k in ("title", "company", "city", "places", "family", "seniority", "seniority_basis",
                                   "seniority_signal", "german", "degree", "production", "extractor_version")} == {
        "title": "Senior Staff AI Engineer", "company": "Acme", "city": "Berlin", "places": ["Berlin"],
        "family": "ai-engineer", "seniority": "junior", "seniority_basis": "stated", "seniority_signal": "grow",
        "german": None, "degree": None, "production": None, "extractor_version": "x1"}
    assert [s["source"] for s in before["sources"]] == ["arbeitnow"]
    assert before["skills"] == [{"skill_id": "python", "requirement": "required", "raw_text": "Python",
                                 "alternative_group": None, "display": "Python"}]
    assert "description_text" not in before and before["text_chars"] > 400 and len(before["text_sha256"]) == 64

    # The job is read again and now says senior, with other skills.
    store_extraction(conn, job_id, Extraction(seniority=Seniority("senior", "stated", "Senior Staff"),
                                              mentions=[Mention("kubernetes", "required", "Python")],
                                              extractor_version="x2", taxonomy_version=3))
    assert q.job_detail(conn, job_id, NOW)["seniority"] == "senior"
    assert flags.open_flags(conn)[0]["job"] == before
    assert "seniority reading is wrong (1)" in report(conn)       # still diagnosed from what was on screen


def test_the_database_refuses_to_change_or_delete_what_a_flag_recorded(conn):
    job_id = job(conn, "AI Engineer", JUNIOR_TEXT)
    flag_id = flags.add_flag(conn, job_id, view(), None, NOW)
    for sql in ("UPDATE job_flag SET view = '{}'", "UPDATE job_flag SET job = '{}'",
                "UPDATE job_flag SET created_at = '2020-01-01T00:00:00Z'", "DELETE FROM job_flag"):
        with pytest.raises(sqlite3.IntegrityError, match="job_flag is append-only"):
            conn.execute(sql)
    assert flags.set_note(conn, flag_id, "  a note\nover two lines  ")      # the note is not the record
    assert flags.open_flags(conn)[0]["note"] == "a note over two lines"
    assert flags.unflag(conn, job_id, NOW) == 1
    # Closed is final: not reopened, not re-noted.
    for sql in ("UPDATE job_flag SET closed_at = NULL, closed_reason = NULL", "UPDATE job_flag SET note = 'x'"):
        with pytest.raises(sqlite3.IntegrityError, match="job_flag is append-only"):
            conn.execute(sql)
    assert not flags.set_note(conn, flag_id, "late")


def test_a_note_is_one_line_of_at_most_200_characters():
    assert flags.clean_note("  it's a\n platform   role ") == "it's a platform role"
    assert len(flags.clean_note("y" * 500)) == 200 and flags.clean_note("  \n ") is None


def test_a_flag_follows_a_merged_duplicate_and_outlives_a_removed_job(conn):
    keep = job(conn, "AI Engineer", JUNIOR_TEXT)
    dup = job(conn, "ML Engineer", PLATFORM_TEXT, company="Zeta")
    flag_id = flags.add_flag(conn, dup, view(), None, NOW)
    with conn:
        merge_jobs(conn, keep, dup)
    assert flags.flagged_job_ids(conn, [keep, dup]) == {keep}
    with conn:
        conn.execute("DELETE FROM job WHERE id = ?", (keep,))
    left = flags.open_flags(conn)
    assert [(f["id"], f["job_id"], f["text"]) for f in left] == [(flag_id, None, None)]
    out = report(conn)
    assert "job removed" in out and "the posting is no longer stored" in out


# --- the API and the command ------------------------------------------------------------

@pytest.fixture
def api(tmp_path, monkeypatch):
    path = tmp_path / "t.db"
    c = db.connect(path)
    db.migrate(c)
    job_id = job(c, "Senior Staff AI Engineer", JUNIOR_TEXT, seniority=Seniority("junior", "stated", "grow"))
    monkeypatch.setattr("app.api.now_iso", lambda: NOW)
    return TestClient(create_app(path, TAX)), c, job_id


def test_flag_note_and_unflag_over_the_api(api):
    client, conn, job_id = api
    assert client.get("/api/jobs", params={"window": "all"}).json()["jobs"][0]["flagged"] is False
    sent = view(seniorities=["junior"], visa="sponsored")
    r = client.post(f"/api/jobs/{job_id}/flag", json={"view": sent})
    assert r.status_code == 200 and r.json()["flagged"] is True
    flag_id = r.json()["flag_id"]
    stored = flags.open_flags(conn)[0]
    assert stored["view"] == sent                                  # as sent, unknown keys included
    assert stored["created_at"] == NOW and stored["job"]["skills"][0]["display"] == "Python"
    assert client.get("/api/jobs", params={"window": "all"}).json()["jobs"][0]["flagged"] is True
    assert client.get(f"/api/jobs/{job_id}").json()["flagged"] is True

    assert client.post(f"/api/flags/{flag_id}/note", json={"note": "it's a senior role"}).json()["note"] == "it's a senior role"
    assert flags.open_flags(conn)[0]["note"] == "it's a senior role"

    assert client.delete(f"/api/jobs/{job_id}/flag").json() == {"closed": 1, "flagged": False}
    assert client.get(f"/api/jobs/{job_id}").json()["flagged"] is False
    assert flags.open_flags(conn) == []
    # The row is kept, closed: nothing was deleted.
    assert conn.execute("SELECT closed_reason FROM job_flag").fetchall()[0][0] == "unflagged"
    assert client.post(f"/api/flags/{flag_id}/note", json={"note": "late"}).status_code == 404


def test_the_api_refuses_a_missing_job_and_an_oversized_view(api):
    client, conn, job_id = api
    assert client.post("/api/jobs/9999/flag", json={"view": view()}).status_code == 404
    assert client.post(f"/api/jobs/{job_id}/flag", json={"view": {"junk": "x" * 30_000}}).status_code == 422
    assert client.post(f"/api/jobs/{job_id}/flag", json={}).status_code == 422
    assert conn.execute("SELECT count(*) FROM job_flag").fetchone()[0] == 0


def test_the_flags_command_prints_the_report_and_fixed_closes_a_flag(conn, monkeypatch, capsys):
    job_id = job(conn, "Senior Staff AI Engineer", JUNIOR_TEXT, seniority=Seniority("junior", "stated", "grow"))
    flag_id = flags.add_flag(conn, job_id, view(seniorities=["junior"]), None, NOW)
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    cli.main(["flags"])
    out = capsys.readouterr().out
    assert out.startswith("1 open flag, 1 cause.") and "seniority reading is wrong (1)" in out
    cli.main(["flags", "--fixed", str(flag_id), "999"])
    assert "closed 1 of 2 flags as fixed" in capsys.readouterr().out
    assert flags.flagged_job_ids(conn, [job_id]) == set()
    cli.main(["flags"])
    assert capsys.readouterr().out.strip() == "No open flags."
    assert json.loads(conn.execute("SELECT job FROM job_flag").fetchone()[0])["seniority"] == "junior"
