"""`check --add` must not store a posting the check just found (it would duplicate it)."""

import app.__main__ as cli
from app import db
from app.check import CheckResult
from app.sources import Posting


def test_add_skips_a_posting_the_check_found(tmp_path, monkeypatch, capsys):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    page = Posting("url", "", "https://acme.com/j/1", "Acme", "AI Engineer", "Berlin", "page text")
    found = CheckResult(url=page.url, verdict="found", how="text 0.87", job_id=51,
                        job_title="AI Engineer", sources=["screenshot"], posting=page)
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "check_url", lambda *a, **k: found)
    monkeypatch.setattr(cli, "log_check", lambda *a, **k: None)
    monkeypatch.setattr(cli, "ingest_one", lambda *a, **k: (_ for _ in ()).throw(AssertionError("ingested")))
    cli.main(["check", page.url, "--add"])
    assert "add: skipped — already job 51" in capsys.readouterr().out


def test_check_takes_a_batch_and_one_bad_url_does_not_stop_it(tmp_path, monkeypatch, capsys):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    listing = tmp_path / "urls.txt"
    listing.write_text("# from LinkedIn\nhttps://b.example/2\n\nhttps://a.example/1\n")

    def fake_check(conn, url, *a, **k):
        if url.startswith("https://b."):
            raise OSError("dead page")
        return CheckResult(url=url, verdict="not_found", how="", diagnosis="not a hosted ATS page")

    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "load_feeds", lambda: [])
    monkeypatch.setattr(cli, "check_url", fake_check)
    monkeypatch.setattr(cli, "log_check", lambda *a, **k: None)
    cli.main(["check", "https://a.example/1", "--file", str(listing)])
    out = capsys.readouterr().out
    # a.example/1 appears twice in the input but is checked once; order kept
    assert out.count("== https://a.example/1") == 1
    assert out.index("== https://a.example/1") < out.index("== https://b.example/2")
    assert "error: OSError: dead page" in out
    assert "not found: not a hosted ATS page" in out


def test_check_refuses_per_posting_flags_on_a_batch(monkeypatch):
    import pytest
    monkeypatch.setattr(cli, "open_db", lambda: (_ for _ in ()).throw(AssertionError("opened db")))
    with pytest.raises(SystemExit):
        cli.main(["check", "https://a.example/1", "https://b.example/2", "--title", "AI Engineer"])


def test_add_refuses_a_posting_with_no_readable_text(tmp_path, monkeypatch, capsys):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    empty = Posting("url", "", "https://jobs.gem.com/x/1", "sennder", "ML Engineer", "Berlin", "")
    r = CheckResult(url=empty.url, verdict="not_found", how="", diagnosis="not a hosted ATS page", posting=empty)
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "check_url", lambda *a, **k: r)
    monkeypatch.setattr(cli, "log_check", lambda *a, **k: None)
    monkeypatch.setattr(cli, "ingest_one", lambda *a, **k: (_ for _ in ()).throw(AssertionError("ingested")))
    cli.main(["check", empty.url, "--add"])
    assert "add: refused — only 0 characters" in capsys.readouterr().out


def test_add_extracts_only_the_job_it_added(tmp_path, monkeypatch, capsys):
    """A pending queue (e.g. after an extractor version bump) must not be drained by an add."""
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    page = Posting("url", "", "https://acme.com/j/2", "Acme", "AI Engineer", "Berlin", "Python and RAG. " * 40)
    r = CheckResult(url=page.url, verdict="not_found", how="", diagnosis="not a hosted ATS page", posting=page)
    calls = []
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "check_url", lambda *a, **k: r)
    monkeypatch.setattr(cli, "log_check", lambda *a, **k: None)
    monkeypatch.setattr(cli, "ingest_one", lambda *a, **k: "new:248")
    monkeypatch.setattr(cli, "run_extraction", lambda conn, limit=None, job_ids=None: calls.append(job_ids))
    cli.main(["check", page.url, "--add"])
    assert calls == [[248]]


def test_add_text_extracts_only_the_job_it_added(tmp_path, monkeypatch):
    import io
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    calls = []
    monkeypatch.setattr(cli.sys, "stdin", io.StringIO("Python and RAG. " * 40))
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "ingest_one", lambda *a, **k: "new:7")
    monkeypatch.setattr(cli, "run_extraction", lambda conn, limit=None, job_ids=None: calls.append(job_ids))
    cli.main(["add-text", "--company", "Acme", "--title", "AI Engineer"])
    assert calls == [[7]]
