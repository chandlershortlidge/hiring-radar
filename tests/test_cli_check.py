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
