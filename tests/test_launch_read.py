"""A launch's first collection reads only the launched city's new jobs (HIR-380)."""

import pytest

from app import db, discover, launch_read, pipeline, poll, reread_cost
from app.extract import Extraction, Mention, extractor_version
from app.ingest import ingest_one
from app.sources import Posting
from app.taxonomy import Taxonomy

TAX = Taxonomy({"version": 2, "skills": [{"id": "python", "display": "Python"}]})
MODEL = "m"
VERSION = extractor_version(TAX, MODEL)


def fake_extract(text, tax, model):
    return Extraction(mentions=[Mention("python", "required", "Python")],
                      extractor_version=extractor_version(tax, model), taxonomy_version=tax.version)


@pytest.fixture
def conn(tmp_path):
    """A local copy with 4 older Berlin jobs, all open, read by an extractor since replaced."""
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    for i in range(4):
        ingest_one(conn=c, p=Posting("arbeitnow", f"old{i}", "", f"Old{i}", "AI Engineer", "Berlin",
                                     f"Python job {i}"))
    c.execute("UPDATE job SET extracted_version = 'an-older-extractor'")
    c.commit()
    return c


def launch_board(feed):
    """The launched city's new board: two San Jose roles and one in San Francisco."""
    return [Posting("greenhouse", "sj1", "", "Wayve", "Machine Learning Engineer", "San Jose, CA", "Python 1"),
            Posting("greenhouse", "sj2", "", "Wayve", "AI Engineer", "San Jose, CA", "Python 2"),
            Posting("greenhouse", "sf1", "", "Wayve", "Machine Learning Researcher", "San Francisco, CA", "Python 3")]


def first_collection(conn):
    r = poll.poll_feeds(conn, [{"type": "greenhouse", "token": "wayve", "enabled": True}],
                        fetch=launch_board, log=lambda *_: None)
    return r, launch_read.plan(conn, r.new_job_ids, "San Jose", VERSION)


def stale_old_jobs(conn) -> int:
    return conn.execute("SELECT count(*) FROM job WHERE extracted_version = 'an-older-extractor'"
                        ).fetchone()[0]


def test_stale_old_jobs_are_skipped_and_the_new_citys_jobs_are_read(conn):
    r, plan = first_collection(conn)
    assert len(r.new_job_ids) == 3
    assert len(plan.to_read) == 2 and (plan.other_new, plan.stale_left) == (1, 4)

    report = pipeline.extract_pending(conn, TAX, fake_extract, MODEL, log=lambda *_: None,
                                      job_ids=plan.to_read)
    assert report.attempted == 2
    read = {row[0] for row in conn.execute("SELECT location_raw FROM job WHERE extracted_version = ?",
                                           (VERSION,))}
    assert read == {"San Jose, CA"}
    assert stale_old_jobs(conn) == 4            # the older jobs kept their old reading


def test_the_price_is_of_exactly_the_jobs_read(conn):
    _, plan = first_collection(conn)
    assert plan.cost.jobs == 2
    assert plan.cost.eur_total == pytest.approx(
        reread_cost.cost_of_reading(conn, 1).eur_total * 2)
    assert plan.cost.eur_total < reread_cost.reread_cost(conn).eur_total   # not the whole queue


def test_no_new_jobs_reads_nothing_rather_than_everything(conn):
    """The pipeline reads the whole queue when handed no job ids; the plan must hand it none."""
    plan = launch_read.plan(conn, [], "San Jose", VERSION)
    assert plan.to_read == [] and plan.stale_left == 4 and plan.cost.eur_total == 0


def test_the_report_says_what_was_left_unread_and_why(conn):
    _, plan = first_collection(conn)
    text = "\n".join(plan.lines())
    assert "reading 2 new jobs in San Jose" in text
    assert "1 new jobs placed in other cities and 4 older jobs" in text
    assert "server reads its own" in text and "STOPPED" not in text


def test_over_the_launch_cap_it_stops(conn, monkeypatch):
    monkeypatch.setattr(launch_read, "MAX_LAUNCH_COST_EUR", 0.0)
    _, plan = first_collection(conn)
    assert plan.over_cap
    assert "STOPPED, nothing read" in "\n".join(plan.lines())


def test_the_launch_report_prints_the_first_collection_command():
    ds = discover.launch_decisions([discover.Candidate(("greenhouse", "wayve"))])
    ds[0].verdict = "add"
    lines = discover.launch_report_lines("San Jose", ds, 0.1, 10, None, applied=True)
    assert lines[-1].endswith('poll --launch "San Jose" --only greenhouse:wayve')


def test_poll_launch_hands_the_reader_only_the_citys_new_jobs(conn, monkeypatch):
    """The command, end to end: no model call, and never the whole queue."""
    import app.__main__ as cli
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "load_feeds", lambda: [{"type": "greenhouse", "token": "wayve", "enabled": True}])
    monkeypatch.setattr(cli, "poll_feeds", lambda c, feeds: poll.poll_feeds(c, feeds, fetch=launch_board,
                                                                              log=lambda *_: None))
    monkeypatch.setattr(cli.Taxonomy, "load", classmethod(lambda cls: TAX))
    monkeypatch.setattr("app.extract.DEFAULT_MODEL", MODEL)
    calls = []
    monkeypatch.setattr(cli, "run_extraction", lambda c, **kw: calls.append(kw))
    cli.main(["poll", "--launch", "San Jose", "--only", "greenhouse:wayve"])
    assert len(calls) == 1
    ids = calls[0]["job_ids"]
    assert [r[0] for r in conn.execute(
        f"SELECT location_raw FROM job WHERE id IN ({','.join('?' * len(ids))})", ids)] == ["San Jose, CA"] * 2


def test_poll_launch_rejects_a_city_that_is_not_collected(monkeypatch):
    import app.__main__ as cli
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    monkeypatch.setattr(cli, "load_feeds", lambda: [])
    with pytest.raises(SystemExit, match="not collected"):
        cli.main(["poll", "--launch", "Atlantis"])


def test_a_launch_read_with_no_skills_at_all_stops_with_the_outage_error(conn, monkeypatch):
    """A broken model during a city's first read trips the same alarm as the daily
    collection, though the launch names its jobs (HIR-425)."""
    import app.__main__ as cli

    def three_in_san_jose(feed):
        return [Posting("greenhouse", f"sj{i}", "", "Wayve", f"AI Engineer {i}", "San Jose, CA", f"Python {i}")
                for i in range(3)]

    def blank(text, tax, model):
        return Extraction(mentions=[], extractor_version=extractor_version(tax, model), taxonomy_version=tax.version)

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "load_feeds", lambda: [{"type": "greenhouse", "token": "wayve", "enabled": True}])
    monkeypatch.setattr(cli, "poll_feeds", lambda c, feeds: poll.poll_feeds(c, feeds, fetch=three_in_san_jose,
                                                                              log=lambda *_: None))
    monkeypatch.setattr(cli.Taxonomy, "load", classmethod(lambda cls: TAX))
    monkeypatch.setattr("app.extract.DEFAULT_MODEL", MODEL)
    monkeypatch.setattr(cli, "extract_pending", lambda c, tax, batch=False, **kw: pipeline.extract_pending(
        c, tax, blank, MODEL, log=lambda *_: None, **kw))
    with pytest.raises(SystemExit, match="extraction produced zero skills across all 3 jobs"):
        cli.main(["poll", "--launch", "San Jose", "--only", "greenhouse:wayve"])
