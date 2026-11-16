"""Checks run on a laptop reach the server's count (HIR-294): what is sent, what the
server keeps, and that a failed send never fails a check."""

import json
import subprocess
from types import SimpleNamespace

import pytest

import app.__main__ as cli
from app import db, misses, send_checks
from app.check import ALREADY_HAD, UNREADABLE_SYSTEM, CheckResult, log_check
from app.ingest import ingest_one
from app.sources import Posting

GH = "https://boards.greenhouse.io/acme/jobs/1"
OWN = "https://careers.acme.com/jobs/ai-engineer"
JD = "Build LLM agents in Python and ship them to production."


def fresh(tmp_path, name):
    c = db.connect(tmp_path / name)
    db.migrate(c)
    return c


@pytest.fixture
def laptop(tmp_path):
    return fresh(tmp_path, "laptop.db")


@pytest.fixture
def server(tmp_path):
    return fresh(tmp_path, "server.db")


def miss(conn, url=OWN, now="2026-11-12T09:00:00Z"):
    page = Posting("url", "", url, "Acme", "AI Engineer", "Berlin", JD)
    log_check(conn, CheckResult(url=url, verdict="not_found", how="", posting=page,
                                diagnosis="not a hosted ATS page"), "linkedin", now)


def old_row(conn, url, verdict, job_id, had, diagnosis, now):
    """A check logged before reasons were recorded (migration 023): the new columns NULL."""
    conn.execute("INSERT INTO url_check (url, checked_at, found_via, verdict, job_id, feed_had_it, diagnosis)"
                 " VALUES (?, ?, 'company_site', ?, ?, ?, ?)", (url, now, verdict, job_id, had, diagnosis))
    conn.commit()


def test_a_check_logged_on_the_laptop_is_counted_on_the_server(laptop, server):
    miss(laptop)
    assert send_checks.receive(server, send_checks.outgoing(laptop)) == (1, 0)
    [m] = misses.records(server)
    assert (m.url, m.reason, m.company, m.city, m.checked_at) == (
        OWN, UNREADABLE_SYSTEM, "Acme", "Berlin", "2026-11-12T09:00:00Z")
    assert misses.records(server) == misses.records(laptop)
    row = server.execute("SELECT found_via, verdict, feed_had_it, job_id FROM url_check").fetchone()
    assert tuple(row) == ("linkedin", "not_found", 0, None)


def test_sending_the_same_log_again_adds_nothing(laptop, server):
    miss(laptop)
    send_checks.receive(server, send_checks.outgoing(laptop))
    miss(laptop, url=GH, now="2026-11-13T09:00:00Z")
    assert send_checks.receive(server, send_checks.outgoing(laptop)) == (1, 1)
    assert send_checks.receive(server, send_checks.outgoing(laptop)) == (0, 2)
    assert server.execute("SELECT count(*) FROM url_check").fetchone()[0] == 2


def test_the_recheck_after_adding_a_board_is_not_a_second_record_on_the_server(laptop, server):
    miss(laptop, url=GH, now="2026-11-12T09:00:00Z")
    job = ingest_one(laptop, Posting("greenhouse", "acme:1", GH, "Acme", "AI Engineer", "Berlin", JD)).job_id
    log_check(laptop, CheckResult(url=GH, verdict="found", how="ats id", job_id=job, sources=["greenhouse"]),
              "linkedin", "2026-11-12T09:05:00Z")
    assert send_checks.receive(server, send_checks.outgoing(laptop)) == (2, 0)
    [m] = misses.records(server)
    assert m.reason != ALREADY_HAD and m.checked_at == "2026-11-12T09:00:00Z"


def test_an_old_check_goes_up_with_its_reason_and_the_laptop_jobs_company_and_city(laptop, server):
    job = ingest_one(laptop, Posting("greenhouse", "acme:1", GH, "Acme", "AI Engineer", "Berlin", JD)).job_id
    old_row(laptop, GH, "found", job, 1, None, "2026-10-20T08:00:00Z")
    [rec] = send_checks.outgoing(laptop)
    assert (rec["reason"], rec["company"], rec["city"], rec["careers_system"]) == (
        ALREADY_HAD, "Acme", "Berlin", "greenhouse")
    assert "job_id" not in rec          # the laptop's job id means nothing on the server
    send_checks.receive(server, [rec])
    [m] = misses.records(server)
    assert (m.reason, m.company, m.city) == (ALREADY_HAD, "Acme", "Berlin")


def test_a_check_already_on_the_server_keeps_its_place_as_the_first(laptop, server):
    miss(server, now="2026-11-01T10:00:00Z")            # the dashboard's box, on the server
    miss(laptop, now="2026-11-12T09:00:00Z")
    send_checks.receive(server, send_checks.outgoing(laptop))
    [m] = misses.records(server)
    assert m.checked_at == "2026-11-01T10:00:00Z"


def test_a_malformed_record_stores_nothing(laptop, server):
    miss(laptop)
    good = send_checks.outgoing(laptop)
    with pytest.raises(ValueError):
        send_checks.receive(server, good + [{"url": OWN}])
    bad_verdict = dict(good[0], checked_at="2026-11-13T00:00:00Z", verdict="maybe")
    with pytest.raises(Exception):
        send_checks.receive(server, good + [bad_verdict])
    assert server.execute("SELECT count(*) FROM url_check").fetchone()[0] == 0


def ran(stdout="", stderr="", code=0):
    return lambda *a, **k: SimpleNamespace(stdout=stdout, stderr=stderr, returncode=code)


def raises(error):
    def run(*a, **k):
        raise error
    return run


def test_send_pipes_the_records_to_the_servers_command_and_reads_its_answer():
    seen = {}

    def run(argv, **kw):
        seen.update(argv=argv, **kw)
        return SimpleNamespace(stdout='applied migrations: [23]\n{"added": 2, "already_held": 5}\n',
                               stderr="WARNING: install NumPy", returncode=0)

    assert send_checks.send([{"url": OWN}], run=run) == (2, 5)
    assert seen["argv"][:3] == ["gcloud", "compute", "ssh"] and "--tunnel-through-iap" in seen["argv"]
    assert seen["argv"][-1].endswith("-m app receive-checks'")
    assert json.loads(seen["input"]) == {"checks": [{"url": OWN}]}


@pytest.mark.parametrize("run", [
    ran(stderr="ERROR: (gcloud.compute.ssh) could not fetch resource", code=1),
    ran(stdout="{not json"),
    ran(stdout='{"added": 1}'),
    raises(subprocess.TimeoutExpired("gcloud", 120)),
    raises(FileNotFoundError("gcloud")),
])
def test_send_says_so_when_the_server_did_not_answer(run):
    with pytest.raises(send_checks.SendError):
        send_checks.send([], run=run)


def test_after_check_reports_what_the_server_stored(laptop, monkeypatch):
    monkeypatch.setattr(send_checks, "enabled", lambda path: True)
    miss(laptop)
    lines = []
    send_checks.after_check(laptop, "x.db", log=lines.append, send=lambda records: (len(records), 0))
    assert lines == ["checks sent to the server: 1 new there, 0 it already had"]


def test_a_failed_send_is_one_line_and_never_an_error(laptop, monkeypatch):
    monkeypatch.setattr(send_checks, "enabled", lambda path: True)
    miss(laptop)
    lines = []
    send_checks.after_check(laptop, "x.db", log=lines.append,
                            send=raises(send_checks.SendError("exit 1: no network")))
    assert lines == ["checks not sent to the server (exit 1: no network); they go with the next check"]


def test_nothing_is_sent_when_switched_off_on_the_server_or_without_gcloud(laptop, monkeypatch):
    monkeypatch.setattr(send_checks.shutil, "which", lambda name: "/usr/bin/gcloud")
    assert not send_checks.enabled("data/hiring-radar.db")          # the suite's switch is off
    monkeypatch.delenv(send_checks.SWITCH)
    assert send_checks.enabled("data/hiring-radar.db")
    assert not send_checks.enabled(send_checks.SERVER_DB)
    monkeypatch.setattr(send_checks.shutil, "which", lambda name: None)
    assert not send_checks.enabled("data/hiring-radar.db")
    miss(laptop)
    send_checks.after_check(laptop, "data/hiring-radar.db", log=pytest.fail, send=pytest.fail)


def test_the_check_command_ends_by_sending_and_the_server_command_stores(tmp_path, monkeypatch, capsys):
    laptop_db, server_db = fresh(tmp_path, "l.db"), fresh(tmp_path, "s.db")
    monkeypatch.setattr(cli, "open_db", lambda: laptop_db)
    monkeypatch.setattr(cli, "load_feeds", lambda: [])
    page = Posting("url", "", OWN, "Acme", "AI Engineer", "Berlin", JD)
    monkeypatch.setattr(cli, "check_url", lambda *a, **k: CheckResult(
        url=OWN, verdict="not_found", how="", posting=page, diagnosis="not a hosted ATS page"))
    sent = []
    monkeypatch.setattr(send_checks, "after_check", lambda conn, path: sent.append(send_checks.outgoing(conn)))
    cli.main(["check", OWN])
    assert [r["url"] for r in sent[0]] == [OWN]

    # the server's end: the same records on stdin, the answer as one JSON line
    monkeypatch.setattr(cli, "open_db", lambda: server_db)
    monkeypatch.setattr(cli.sys, "stdin", SimpleNamespace(read=lambda: json.dumps({"checks": sent[0]})))
    capsys.readouterr()
    cli.main(["receive-checks"])
    assert json.loads(capsys.readouterr().out) == {"added": 1, "already_held": 0}
    assert [m.url for m in misses.records(server_db)] == [OWN]

    monkeypatch.setattr(cli.sys, "stdin", SimpleNamespace(read=lambda: "not json"))
    with pytest.raises(SystemExit) as e:
        cli.main(["receive-checks"])
    assert "receive-checks" in str(e.value)
