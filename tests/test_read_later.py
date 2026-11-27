"""Collect now, read later (HIR-396): a place or career track set to `read: later` has its
postings stored, dated and looked after like any other, and never sent to the model until
`read-pending` reads them all in one batch.

One temporary database, filled through the same poll a daily collection uses. The model is
a fake Batch API that records every request it is handed, so "zero model calls" is counted,
not assumed. The settings are app/scope.py's; each test changes one line of them, which is
all a real switch is.
"""

import json
from types import SimpleNamespace

import pytest

import app.__main__ as cli
from app import caretaker as ct
from app import caretaker_run, db, ingest, launch_read, pipeline, poll, read_pending, reread_cost, sample, scope
from app.extract import DEFAULT_MODEL, extractor_version
from app.sources import Posting
from app.taxonomy import Taxonomy

TAX = Taxonomy({"version": 2, "skills": [{"id": "python", "display": "Python"}]})
MODEL = "m"
VERSION = extractor_version(TAX, MODEL)
DAY_ONE = "2026-11-01T07:00:00Z"     # collection day
USAGE = dict(input_tokens=100, output_tokens=20, cache_read_input_tokens=80, cache_creation_input_tokens=0)
BODY = " The team ships Python services to production and writes about it at length." * 6


def later_track(monkeypatch, track="research"):
    monkeypatch.setitem(scope.TRACKS, track, scope.Track(scope.INCUBATING, read=scope.READ_LATER))


def later_city(monkeypatch, city="Chicago"):
    monkeypatch.setitem(scope.PLACE_STATE, city, scope.INCUBATING)
    monkeypatch.setitem(scope.PLACE_READ, city, scope.READ_LATER)


def board(feed=None):
    """One board: an AI role in Berlin, two research roles (Berlin, New York), an AI role
    in Chicago only, and an AI role posted for Berlin and Chicago."""
    def p(sid, company, title, where):
        return Posting("greenhouse", sid, f"https://example.com/{sid}", company, title, where,
                       f"{company} is hiring a {title}." + BODY)
    return [p("a1", "Acme", "AI Engineer", "Berlin"),
            p("r1", "Lab", "Research Engineer, LLMs", "Berlin"),
            p("r2", "Deep", "Research Scientist, Machine Learning", "New York, NY"),
            p("c1", "Windy", "AI Engineer", "Chicago, IL"),
            p("b1", "Both", "ML Engineer", "Berlin; Chicago, IL")]


class FakeBatch:
    """Stands in for the Batch API: reads every request as one Python mention, and keeps
    the job ids it was asked to read."""

    def __init__(self):
        self.asked: list[int] = []

    def __call__(self, requests):
        self.asked += [int(r["custom_id"]) for r in requests]
        block = SimpleNamespace(type="tool_use", name="record_skills",
                                input={"skills": [{"skill_id": "python", "requirement": "required", "raw_text": "Python"}]})
        message = SimpleNamespace(stop_reason="tool_use", content=[block], usage=SimpleNamespace(**USAGE))
        return {r["custom_id"]: SimpleNamespace(type="succeeded", message=message) for r in requests}


@pytest.fixture(autouse=True)
def nothing_reads_later(monkeypatch):
    """Each test starts from a list where everything reads now and switches one line. The
    real list has software engineer reading later since HIR-397; it reads now here."""
    monkeypatch.setitem(scope.TRACKS, "software-engineer",
                        scope.Track(scope.INCUBATING, scope.SWE_PATTERN,
                                    places=scope.TRACKS["software-engineer"].places, finds_boards=False))


@pytest.fixture
def conn(tmp_path, monkeypatch):
    monkeypatch.setattr(poll, "ingest", lambda c, postings: ingest.ingest(c, postings, DAY_ONE))
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    yield c
    c.close()


def collect(conn, batch, tax=TAX):
    """One daily collection: fetch the board, store it, read whatever the queue holds."""
    poll.poll_feeds(conn, [{"type": "greenhouse", "token": "board", "enabled": True}],
                    fetch=board, log=lambda *_: None)
    return pipeline.extract_pending(conn, tax, model=MODEL, log=lambda *_: None, batch=True, batch_fn=batch)


def ids(conn, *companies) -> list[int]:
    marks = ",".join("?" * len(companies))
    return [r[0] for r in conn.execute(f"SELECT id FROM job WHERE company IN ({marks}) ORDER BY id", companies)]


def unread(conn) -> list[str]:
    return [r[0] for r in conn.execute("SELECT company FROM job WHERE extracted_version IS NULL ORDER BY company")]


# --- the setting ----------------------------------------------------------------------------

def test_with_everything_reading_now_nothing_is_held(conn):
    assert scope.read_later_places() == () and scope.read_later_tracks() == ()
    assert pipeline.held_clause() == ("0", [])
    batch = FakeBatch()
    collect(conn, batch)
    assert unread(conn) == [] and len(batch.asked) == 5
    assert pipeline.held_line(conn, VERSION) is None


def test_the_setting_is_read_when_asked_not_when_imported(monkeypatch):
    later_track(monkeypatch)
    later_city(monkeypatch)
    assert scope.read_later_tracks() == ("research",) and scope.read_later_places() == ("Chicago",)


# --- the skip -------------------------------------------------------------------------------

def test_a_read_later_track_collects_for_several_polls_with_no_model_call(conn, monkeypatch):
    later_track(monkeypatch)
    batch = FakeBatch()
    for _ in range(3):
        collect(conn, batch)
    research = ids(conn, "Lab", "Deep")
    assert len(research) == 2 and not set(research) & set(batch.asked)
    assert unread(conn) == ["Deep", "Lab"]
    # Everything else was read once, on the first poll, as on any other day.
    assert sorted(batch.asked) == ids(conn, "Acme", "Windy", "Both")
    # Stored as usual: text, day first seen, places, sources; still listed on every later poll.
    for job_id in research:
        row = conn.execute("SELECT description_text, first_seen, family FROM job WHERE id = ?", (job_id,)).fetchone()
        assert "is hiring" in row["description_text"] and row["first_seen"] == DAY_ONE and row["family"] == "research"
        assert conn.execute("SELECT count(*) FROM job_place WHERE job_id = ?", (job_id,)).fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM job_source WHERE job_id = ?", (job_id,)).fetchone()[0] == 1
    assert conn.execute("SELECT count(*) FROM job").fetchone()[0] == 5   # three polls, no duplicates


def test_a_read_later_city_holds_its_own_jobs_but_not_one_also_posted_for_a_read_now_city(conn, monkeypatch):
    later_city(monkeypatch)
    batch = FakeBatch()
    collect(conn, batch)
    assert unread(conn) == ["Windy"]
    assert ids(conn, "Both")[0] in batch.asked      # shown in Berlin, so it needs its skills


def test_a_re_read_after_a_skill_list_change_leaves_held_jobs_alone_and_is_not_priced_for_them(conn, monkeypatch):
    collect(conn, FakeBatch())                       # everything read once at the first skill list
    later_track(monkeypatch)
    assert pipeline.reread_queue_size(conn, DAY_ONE) == 3
    assert reread_cost.reread_cost(conn, DAY_ONE).jobs == 3
    bigger = Taxonomy({"version": 3, "skills": [{"id": "python", "display": "Python"}, {"id": "go", "display": "Go"}]})
    batch = FakeBatch()
    pipeline.extract_pending(conn, bigger, model=MODEL, log=lambda *_: None, batch=True, batch_fn=batch)
    assert not set(ids(conn, "Lab", "Deep")) & set(batch.asked)


def test_a_launch_first_collection_does_not_read_held_jobs(conn, monkeypatch):
    later_track(monkeypatch)
    r = poll.poll_feeds(conn, [{"type": "greenhouse", "token": "board", "enabled": True}],
                        fetch=board, log=lambda *_: None)
    plan = launch_read.plan(conn, r.new_job_ids, "Berlin", VERSION)
    assert plan.to_read == ids(conn, "Acme", "Both")


def test_a_posting_added_by_hand_is_read_whatever_the_setting(conn, monkeypatch):
    """The add paths name the one job they stored; a person is waiting for it (HIR-395)."""
    later_track(monkeypatch)
    batch = FakeBatch()
    collect(conn, batch)
    lab = ids(conn, "Lab")
    pipeline.extract_pending(conn, TAX, model=MODEL, log=lambda *_: None, job_ids=lab, batch=True, batch_fn=batch)
    assert lab[0] in batch.asked and unread(conn) == ["Deep"]


# --- the separate count ---------------------------------------------------------------------

def test_held_jobs_are_counted_apart_from_jobs_that_should_have_been_read(conn, monkeypatch):
    later_track(monkeypatch)
    later_city(monkeypatch)
    poll.poll_feeds(conn, [{"type": "greenhouse", "token": "board", "enabled": True}],
                    fetch=board, log=lambda *_: None)
    # Nothing read yet: two jobs are overdue (Acme, Both), three wait on purpose.
    assert len(pipeline.jobs_needing_extraction(conn, VERSION)) == 2
    assert pipeline.held_count(conn, VERSION) == 3
    assert pipeline.held_line(conn, VERSION) == (
        "stored unread on purpose: 3 jobs (read later: Chicago, research);"
        " `python -m app read-pending` reads them")


def test_the_morning_check_does_not_fire_on_jobs_held_on_purpose(conn, monkeypatch):
    later_track(monkeypatch)
    real_tax = Taxonomy.load()
    collect(conn, FakeBatch(), tax=real_tax)   # read by today's real extractor, as the caretaker counts
    conn.execute("UPDATE job SET extracted_version = ?, read_version = ? WHERE extracted_version IS NOT NULL",
                 (extractor_version(real_tax, DEFAULT_MODEL),) * 2)
    conn.commit()
    assert unread(conn) == ["Deep", "Lab"]
    assert ct.judge_pending(caretaker_run.pending_count(conn)) == []
    # A job that should have been read and was not still fires it.
    conn.execute("UPDATE job SET extracted_version = NULL WHERE company = 'Acme'")
    conn.commit()
    assert [f.data for f in ct.judge_pending(caretaker_run.pending_count(conn))] == [{"pending": 1}]


def test_the_poll_report_prints_the_held_count_on_its_own_line(conn, monkeypatch, capsys):
    later_track(monkeypatch)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "load_feeds", lambda: [{"type": "greenhouse", "token": "board", "enabled": True}])
    monkeypatch.setattr(poll, "fetch_feed", board)
    monkeypatch.setattr(cli, "poll_feeds", lambda c, feeds: poll.poll_feeds(c, feeds, fetch=board, log=lambda *_: None))
    cli.main(["poll", "--no-extract"])
    out = capsys.readouterr().out
    assert "stored unread on purpose: 2 jobs (read later: research)" in out


# --- the bulk read --------------------------------------------------------------------------

def test_the_plan_counts_the_waiting_jobs_and_prices_them_like_the_reread_cost_command(conn, monkeypatch):
    later_track(monkeypatch)
    collect(conn, FakeBatch())
    plan = read_pending.plan(conn, VERSION, family="research", cap=5.0)
    assert plan.to_read == ids(conn, "Lab", "Deep") and plan.left_for_track == 0
    assert plan.cost.eur_total == pytest.approx(reread_cost.cost_of_reading(conn, 2).eur_total)
    assert not plan.over_cap
    assert plan.lines()[0].startswith(
        f"read-pending research: 2 jobs waiting to be read, about €{plan.cost.eur_total:.2f} as one batch (cap €5.00)")


def test_the_bulk_read_reads_them_all_and_they_keep_their_collection_day(conn, monkeypatch):
    later_track(monkeypatch)
    batch = FakeBatch()
    for _ in range(3):
        collect(conn, batch)
    plan = read_pending.plan(conn, VERSION, family="research", cap=5.0)
    report = pipeline.extract_pending(conn, TAX, model=MODEL, log=lambda *_: None, job_ids=plan.to_read,
                                      batch=True, batch_fn=batch)
    assert (report.attempted, report.succeeded) == (2, 2)
    assert unread(conn) == []
    for job_id in plan.to_read:
        row = conn.execute("SELECT first_seen, extracted_version FROM job WHERE id = ?", (job_id,)).fetchone()
        assert row["first_seen"] == DAY_ONE and row["extracted_version"] == VERSION
        assert conn.execute("SELECT count(*) FROM skill_mention WHERE job_id = ?", (job_id,)).fetchone()[0] == 1
    # Read once: a second plan finds nothing waiting.
    assert read_pending.plan(conn, VERSION, family="research").to_read == []


def test_over_the_cap_is_said_and_a_plan_without_a_cap_is_never_over_it(conn, monkeypatch):
    later_track(monkeypatch)
    collect(conn, FakeBatch())
    over = read_pending.plan(conn, VERSION, family="research", cap=0.0001)
    assert over.over_cap and "STOPPED, nothing read: over the €0.00 cap" in over.lines()[-1]
    assert not read_pending.plan(conn, VERSION, family="research").over_cap


def test_by_city_alone_leaves_out_jobs_on_a_read_later_track_and_says_how_many(conn, monkeypatch):
    later_track(monkeypatch)
    later_city(monkeypatch, "New York")
    collect(conn, FakeBatch())
    conn.execute("UPDATE job SET extracted_version = NULL WHERE company = 'Acme'")   # an overdue Berlin job
    conn.commit()
    berlin = read_pending.plan(conn, VERSION, city="Berlin")
    assert berlin.to_read == ids(conn, "Acme") and berlin.left_for_track == 1
    assert "left out: 1 more on a career track still set to read later (research)" in berlin.lines()[1]
    assert read_pending.plan(conn, VERSION, city="Berlin", family="research").to_read == ids(conn, "Lab")
    assert read_pending.plan(conn, VERSION, city="New York", family="research").what == "research in New York"


@pytest.mark.parametrize("kwargs, message", [
    ({}, "name a place with --city or a career track with --family"),
    ({"city": "Atlantis"}, "'Atlantis' is not a collected place"),
    ({"family": "plumber"}, "'plumber' is not a career track"),
])
def test_the_plan_refuses_a_place_or_track_that_is_not_collected(conn, kwargs, message):
    with pytest.raises(ValueError, match=message):
        read_pending.plan(conn, VERSION, **kwargs)


# --- the command ----------------------------------------------------------------------------

@pytest.fixture
def command(conn, monkeypatch):
    """`python -m app read-pending` on the temporary database, with the fake Batch API
    where the real one would be. Returns the fake, so a test can count what was read."""
    later_track(monkeypatch)
    poll.poll_feeds(conn, [{"type": "greenhouse", "token": "board", "enabled": True}],
                    fetch=board, log=lambda *_: None)
    batch = FakeBatch()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "extract_pending", lambda c, tax, **kw: pipeline.extract_pending(
        c, tax, log=lambda *_: None, batch_fn=batch, **kw))
    return batch


def test_dry_run_prints_the_job_count_and_the_cost_and_reads_nothing(conn, command, monkeypatch, capsys):
    monkeypatch.delenv("ANTHROPIC_API_KEY")          # asking the question needs no key
    cli.main(["read-pending", "--family", "research", "--dry-run"])
    out = capsys.readouterr().out
    assert "read-pending research: 2 jobs waiting to be read, about €" in out
    assert "dry run: nothing read" in out
    assert command.asked == [] and unread(conn) == ["Acme", "Both", "Deep", "Lab", "Windy"]


def test_a_real_run_reads_exactly_the_waiting_jobs_of_that_track_as_one_batch(conn, command, capsys):
    cli.main(["read-pending", "--family", "research", "--cap", "5"])
    assert sorted(command.asked) == ids(conn, "Lab", "Deep")
    assert unread(conn) == ["Acme", "Both", "Windy"]          # the ordinary queue is not drained by it
    assert [r[0] for r in conn.execute("SELECT DISTINCT first_seen FROM job WHERE family = 'research'")] == [DAY_ONE]
    out = capsys.readouterr().out
    assert "extracted=2/2" in out and "set it to read now" in out


def test_a_real_run_needs_a_cap_and_stops_above_it(conn, command):
    with pytest.raises(SystemExit, match="a real run needs --cap EUR"):
        cli.main(["read-pending", "--family", "research"])
    with pytest.raises(SystemExit) as stop:
        cli.main(["read-pending", "--family", "research", "--cap", "0.0001"])
    assert stop.value.code == 2
    assert command.asked == []


def test_nothing_waiting_reads_nothing_rather_than_the_whole_queue(conn, command):
    cli.main(["read-pending", "--city", "Seattle", "--cap", "5"])
    assert command.asked == []


def test_an_unknown_place_stops_with_one_line(conn, command):
    with pytest.raises(SystemExit, match="'Atlantis' is not a collected place"):
        cli.main(["read-pending", "--city", "Atlantis", "--dry-run"])


# --- the sample for building a skill list ---------------------------------------------------

def many(conn, n_per_company=6):
    """Research postings never read: one employer with a big board, five with one each."""
    areas = ("Vision", "Speech", "Robotics", "Retrieval", "Safety", "Compilers")
    rows = [("Big", a) for a in areas[:n_per_company]] + [(f"Small{i}", "Agents") for i in range(5)]
    for company, area in rows:
        # A different text per posting, or the same employer's roles would be merged as one.
        text = " ".join(f"{company} {area} team, point {k}: {area.lower()} work item {k} for {company}." for k in range(40))
        ingest.ingest_one(conn, Posting("greenhouse", f"{company}-{area}", "", company,
                                        f"Research Engineer, {area}", "Berlin", text), DAY_ONE)


def test_the_sample_draws_only_unread_postings_of_the_track(conn, monkeypatch):
    later_track(monkeypatch)
    collect(conn, FakeBatch())
    pool = sample.unread(conn, family="research")
    assert [p["company"] for p in pool] == ["Lab", "Deep"]
    assert pool[0]["places"] == ["Berlin"] and pool[0]["first_seen"] == DAY_ONE and "is hiring" in pool[0]["text"]
    assert sample.unread(conn, family="ai-engineer") == []      # read already


def test_the_sample_spreads_across_employers_and_repeats_with_the_same_seed(conn):
    many(conn)
    pool = sample.unread(conn, family="research")
    picked = sample.spread(pool, 6, seed=1)
    assert len(picked) == 6
    assert {p["company"] for p in picked} == {"Big", "Small0", "Small1", "Small2", "Small3", "Small4"}
    assert picked == sample.spread(pool, 6, seed=1)
    assert len(sample.spread(pool, 50)) == len(pool) == 11       # fewer than asked: all of them, not padded


def test_the_sample_command_writes_the_postings_and_calls_no_model(conn, monkeypatch, tmp_path, capsys):
    many(conn)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "extract_pending", lambda *a, **k: (_ for _ in ()).throw(AssertionError("read")))
    out = tmp_path / "sample.json"
    cli.main(["sample", "--family", "research", "--n", "4", "--out", str(out)])
    doc = json.loads(out.read_text())
    assert (doc["asked"], doc["available"], len(doc["postings"])) == (4, 11, 4)
    assert set(doc["postings"][0]) == {"job_id", "company", "title", "family", "places", "first_seen", "text"}
    assert "sample: 4 of 11 unread postings" in capsys.readouterr().out
    with pytest.raises(SystemExit, match="'plumber' is not a career track"):
        cli.main(["sample", "--family", "plumber"])
