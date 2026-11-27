"""Software engineer, collected in Berlin and New York, unread and hidden (HIR-397,
decisions/2026-11-27-hir-397-software-engineer-incubating.md)."""

import json
from pathlib import Path

import pytest

from app import admin, check, db, discover, ingest, pipeline, scope
from app.ingest import family_of, in_scope_title, ingest_one
from app.sources import Posting

SWE = "software-engineer"
WHEN = "2026-11-20T07:00:00Z"
TEXT = "Build and run our payment services in Go and Postgres. We review code and ship daily." * 4


def posting(title="Senior Software Engineer", location="Berlin", sid="1", company="Acme", source="greenhouse"):
    return Posting(source, sid, f"https://example.com/{sid}", company, title, location, TEXT)


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


# --- the title rule ------------------------------------------------------------------------

@pytest.mark.parametrize("title", [
    "Senior Software Engineer", "Software Developer", "Software-Entwickler (m/w/d)",
    "Softwareentwickler Java", "Softwareingenieur", "Backend Engineer (Go)", "Back-End Developer",
    "Frontend-Entwickler", "Full-Stack Developer", "Fullstack Engineer", "Full Stack Engineer",
    "Platform Engineer, Payments", "Java Developer", "iOS Developer", "Java-Entwickler",
    "Anwendungsentwicklerin", "Senior Staff Software Engineer",
])
def test_a_software_title_is_collected_on_the_track(title):
    assert in_scope_title(title) and family_of(title) == SWE


@pytest.mark.parametrize("title", [
    "Business Developer", "Business Development Manager", "Developer Advocate",
    "Developer Relations Engineer", "Produktentwickler Lebensmittel", "Projektentwickler Immobilien",
    "Personalentwickler (m/w/d)", "Geschäftsentwickler", "Organisationsentwickler",
    "Sales Engineer", "Pre-Sales Developer", "Software Sales Engineer",   # selling (HIR-246)
    "Software Architect", "Backend Lead", "Frontend Designer", "Engineering Manager", "Accountant",
])
def test_a_title_outside_the_rule_is_not_collected(title):
    assert not in_scope_title(title)


@pytest.mark.parametrize("title,family", [
    ("AI Software Engineer", "ai-engineer"),                 # the built-in rule holds it
    ("Senior Backend Engineer, Machine Learning", "ai-engineer"),
    ("ML Platform Engineer", "ml-platform"),
    ("Software Engineer, Data Science Tools", "data-scientist"),
    ("Forward Deployed Software Engineer", "forward-deployed-engineer"),   # FDE decides first
    ("LLM Backend Developer", "ai-engineer"),
])
def test_a_title_another_track_holds_stays_there(title, family):
    assert family_of(title) == family


# --- the list ------------------------------------------------------------------------------

def test_it_is_incubating_read_later_in_two_places_and_finds_no_boards():
    track = scope.TRACKS[SWE]
    assert (track.state, track.read, track.places, track.finds_boards) == (
        scope.INCUBATING, scope.READ_LATER, ("Berlin", "New York"), False)
    assert scope.read_later_tracks() == (SWE,) and scope.read_later_places() == ()
    assert SWE not in scope.live_tracks()


def test_every_track_limited_to_places_names_collected_places():
    for name, track in scope.TRACKS.items():
        unknown = set(track.places or ()) - set(scope.PLACE_STATE)
        assert not unknown, f"{name} is limited to {sorted(unknown)}, which app/scope.py does not collect"


# --- Berlin and New York only ------------------------------------------------------------

@pytest.mark.parametrize("location", ["Berlin", "New York, NY", "Berlin; Munich", "Remote, New York"])
def test_stored_when_it_names_berlin_or_new_york(conn, location):
    stored = ingest_one(conn, posting(location=location), WHEN)
    assert stored.is_new
    assert conn.execute("SELECT family FROM job WHERE id = ?", (stored.job_id,)).fetchone()[0] == SWE


@pytest.mark.parametrize("location", ["Munich", "San Francisco, CA", "Remote (Germany)", "London"])
def test_passed_over_elsewhere_and_counted_as_such(conn, location):
    p = posting(location=location)
    assert ingest.screen(p) == ingest.SKIPPED_TRACK_PLACE
    report = ingest.ingest(conn, [p], WHEN)
    assert (report.new, report.skipped_track_place) == (0, 1) and "skipped_track_place=1" in report.line()
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 0


def test_the_other_tracks_are_still_collected_everywhere(conn):
    assert ingest_one(conn, posting(title="AI Engineer", location="Munich"), WHEN).is_new


def test_a_posting_added_by_hand_without_a_city_is_not_stopped(conn):
    assert ingest_one(conn, posting(location="Munich"), WHEN, require_city=False).is_new


def test_the_link_checker_says_why_in_words():
    assert check._why_stopped(ingest.SKIPPED_TRACK_PLACE, posting(location="Munich")) == (
        "title 'Senior Software Engineer' is the software-engineer track, which is collected only in "
        "Berlin, New York")


def test_the_model_does_not_read_them(conn):
    ingest_one(conn, posting(), WHEN)
    ingest_one(conn, posting(title="AI Engineer", sid="2", company="Other"), WHEN)
    queued = [r["title"] for r in pipeline.jobs_needing_extraction(conn, "v1", now=WHEN)]
    assert queued == ["AI Engineer"]
    assert pipeline.held_count(conn, "v1", now=WHEN) == 1


# --- no new boards for it -----------------------------------------------------------------

def test_the_board_search_does_not_count_its_roles():
    roles = [posting(title="Senior Software Engineer", sid="s1"), posting(title="Backend Developer", sid="s2"),
             posting(title="AI Engineer", sid="a1")]
    assert discover.relevant_roles(roles) == ["AI Engineer (Berlin)"]
    assert discover.relevant_roles(roles[:2], city="Berlin") == []


# --- the database --------------------------------------------------------------------------

def test_029_keeps_every_stored_family_and_accepts_the_new_one(tmp_path):
    import shutil
    upto28 = tmp_path / "upto28"
    upto28.mkdir()
    for m in sorted(db.MIGRATIONS_DIR.glob("*.sql")):
        if int(m.name[:3]) <= 28:
            shutil.copy(m, upto28 / m.name)
    c = db.connect(tmp_path / "t.db")
    db.migrate(c, upto28)
    families = ("ai-engineer", "ml-engineer", "data-scientist", "ml-platform", "research",
                "forward-deployed-engineer")
    for i, family in enumerate(families):
        # A software title stored by hand before today keeps the family it had.
        c.execute("INSERT INTO job (title, description_text, first_seen, last_seen, family)"
                  " VALUES (?, 'jd', ?, ?, ?)", (f"Software Engineer {i}", WHEN, WHEN, family))
    c.commit()
    before = dict(c.execute("SELECT id, family FROM job"))
    assert 29 in db.migrate(c)
    assert dict(c.execute("SELECT id, family FROM job")) == before
    c.execute("UPDATE job SET family = ? WHERE id = 1", (SWE,))
    assert c.execute("SELECT 1 FROM sqlite_master WHERE type = 'index' AND name = 'job_family'").fetchone()
    with pytest.raises(db.sqlite3.IntegrityError):
        c.execute("UPDATE job SET family = 'not-a-family' WHERE id = 1")


# --- the four searches ----------------------------------------------------------------------

def test_two_google_for_jobs_searches_per_city():
    feeds = json.loads((Path(__file__).resolve().parent.parent / "config" / "feeds.json").read_text())["feeds"]
    searches = {f["search"] for f in feeds if f["type"] == "jsearch" and f["enabled"]}
    assert {"software engineer in Berlin", "Softwareentwickler in Berlin",
            "software engineer in New York", "software developer in New York"} <= searches


# --- the Monday line ------------------------------------------------------------------------

def test_the_monday_line_gives_the_weeks_volume_per_city_source_and_duplicates(conn):
    ingest_one(conn, posting(location="Berlin", sid="b1"), "2026-11-17T07:00:00Z")
    ingest_one(conn, Posting("arbeitnow", "x1", "https://x/1", "Acme", "Senior Software Engineer", "Berlin", TEXT),
               "2026-11-18T07:00:00Z")                                     # the same posting again: a duplicate
    ingest_one(conn, posting(location="New York, NY", sid="n1", company="Beta", title="Backend Developer"),
               "2026-11-19T07:00:00Z")
    ingest_one(conn, posting(location="Berlin", sid="old", company="Gamma", title="Java Developer"),
               "2026-11-09T07:00:00Z")                                     # the week before: not counted
    line = admin.week_volume(conn, SWE, "2026-11-16", "2026-11-22")
    assert line == ("Last week (2026-11-16 to 2026-11-22): 2 new postings; a day: Berlin 0.1, New York 0.1; "
                    "from: greenhouse 67%, arbeitnow 33%; 1 duplicate caught (a listing of a posting already "
                    "stored).")
    assert admin.week_volume(conn, SWE, "2026-12-07", "2026-12-13") == (
        "Last week (2026-12-07 to 2026-12-13): nothing new stored.")


def test_the_monday_section_carries_it_under_the_tracks_line(conn):
    from app import caretaker_run
    ingest_one(conn, posting(), "2026-11-17T07:00:00Z")
    text = caretaker_run.incubating_text(conn, "2026-11-23T07:00:00Z", week=("2026-11-16", "2026-11-22"))
    assert "- software-engineer (career track): 1 posting stored" in text
    assert "\n  - Last week (2026-11-16 to 2026-11-22): 1 new posting; a day: Berlin 0.1, New York 0.0;" in text
    assert "Last week" not in caretaker_run.incubating_text(conn, "2026-11-23T07:00:00Z")
