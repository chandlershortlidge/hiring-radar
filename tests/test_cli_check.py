"""`check --add` must not store a posting the check just found (it would duplicate it)."""

import subprocess

import pytest

import app.__main__ as cli
from app import add, db
from app.check import CheckResult
from app.ingest import Stored
from app.sources import Posting


def never_stores(monkeypatch):
    """Every add path stores through app/add.py's one hand-add function (HIR-210), so that
    is where a test asserting "this must not be stored" has to stand."""
    monkeypatch.setattr(add, "add_by_hand",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("stored")))


def stores_as(monkeypatch, job_id: int):
    monkeypatch.setattr(add, "add_by_hand", lambda *a, **k: Stored("new", job_id))


def test_add_skips_a_posting_the_check_found(tmp_path, monkeypatch, capsys):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    page = Posting("url", "", "https://acme.com/j/1", "Acme", "AI Engineer", "Berlin", "page text")
    found = CheckResult(url=page.url, verdict="found", how="text 0.87", job_id=51,
                        job_title="AI Engineer", sources=["screenshot"], posting=page)
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "check_url", lambda *a, **k: found)
    monkeypatch.setattr(cli, "log_check", lambda *a, **k: None)
    never_stores(monkeypatch)
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
    never_stores(monkeypatch)
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
    stores_as(monkeypatch, 248)
    monkeypatch.setattr(cli, "run_extraction",
                        lambda conn, limit=None, job_ids=None, **kw: calls.append(job_ids))
    cli.main(["check", page.url, "--add"])
    assert calls == [[248]]


def test_add_text_extracts_only_the_job_it_added(tmp_path, monkeypatch):
    import io
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    calls = []
    monkeypatch.setattr(cli.sys, "stdin", io.StringIO("Python and RAG. " * 40))
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    stores_as(monkeypatch, 7)
    monkeypatch.setattr(cli, "run_extraction",
                        lambda conn, limit=None, job_ids=None, **kw: calls.append(job_ids))
    cli.main(["add-text", "--company", "Acme", "--title", "AI Engineer"])
    assert calls == [[7]]


# --- the Batch API: poll and a full re-read use it, adding a job by hand never does ----
# (HIR-222)

def test_add_text_never_asks_for_the_batch_api(tmp_path, monkeypatch):
    import io
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    kwargs = []
    monkeypatch.setattr(cli.sys, "stdin", io.StringIO("Python and RAG. " * 40))
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    stores_as(monkeypatch, 7)
    monkeypatch.setattr(cli, "run_extraction",
                        lambda conn, limit=None, job_ids=None, **kw: kwargs.append(kw))
    cli.main(["add-text", "--company", "Acme", "--title", "AI Engineer"])
    assert not kwargs[0].get("batch")


def test_check_add_never_asks_for_the_batch_api(tmp_path, monkeypatch):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    page = Posting("url", "", "https://acme.com/j/3", "Acme", "AI Engineer", "Berlin", "Python and RAG. " * 40)
    r = CheckResult(url=page.url, verdict="not_found", how="", diagnosis="not a hosted ATS page", posting=page)
    kwargs = []
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "check_url", lambda *a, **k: r)
    monkeypatch.setattr(cli, "log_check", lambda *a, **k: None)
    stores_as(monkeypatch, 249)
    monkeypatch.setattr(cli, "run_extraction",
                        lambda conn, limit=None, job_ids=None, **kw: kwargs.append(kw))
    cli.main(["check", page.url, "--add"])
    assert not kwargs[0].get("batch")


def test_poll_and_extract_both_submit_the_queue_as_one_batch(tmp_path, monkeypatch):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    kwargs = []
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "load_feeds", lambda: [])
    monkeypatch.setattr(cli, "run_extraction",
                        lambda conn, limit=None, job_ids=None, **kw: kwargs.append(kw))
    cli.main(["poll"])
    cli.main(["extract"])
    assert kwargs[0]["batch"] and kwargs[1]["batch"]


# --- a missing Anthropic key stops the run with one line, before any work (HIR-127) ----

MISSING_KEY = "ANTHROPIC_API_KEY is not set: add it to .env"


def refuses(monkeypatch, *names):
    for name in names:
        monkeypatch.setattr(cli, name, lambda *a, **k: (_ for _ in ()).throw(AssertionError(name)))


@pytest.mark.parametrize("key", [None, "", "  "])
def test_poll_without_a_key_stops_before_fetching_anything(monkeypatch, key):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    if key is not None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", key)
    refuses(monkeypatch, "load_feeds", "open_db", "poll_feeds")
    with pytest.raises(SystemExit, match=MISSING_KEY):
        cli.main(["poll"])


def test_poll_that_skips_extraction_needs_no_key(tmp_path, monkeypatch):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "load_feeds", lambda: [])
    cli.main(["poll", "--no-extract"])


def test_extract_without_a_key_stops_before_the_first_job(tmp_path, monkeypatch):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    refuses(monkeypatch, "extract_pending")
    with pytest.raises(SystemExit, match=MISSING_KEY):
        cli.main(["extract"])


def test_add_screenshot_without_a_key_stops_before_transcribing(tmp_path, monkeypatch):
    shot = tmp_path / "shot.png"
    shot.write_bytes(b"not really a png")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    refuses(monkeypatch, "open_db", "make_client", "transcribe")
    with pytest.raises(SystemExit, match=MISSING_KEY):
        cli.main(["add-screenshot", str(shot), "--company", "Acme", "--title", "AI Engineer"])


# --- a worktree finds the main checkout's .env (HIR-127) -------------------------------

def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
                   cwd=cwd, check=True, capture_output=True)


def test_a_worktree_is_pointed_at_the_main_checkouts_env(tmp_path):
    main = tmp_path / "main"
    main.mkdir()
    git(main, "init", "-q")
    git(main, "commit", "-q", "--allow-empty", "-m", "first")
    git(main, "worktree", "add", "-q", str(tmp_path / "ticket"))
    assert cli.main_checkout_env(tmp_path / "ticket") == main.resolve() / ".env"
    assert cli.main_checkout_env(main) is None          # the main checkout has its own .env


def test_a_folder_that_is_not_a_worktree_has_no_shared_env(tmp_path):
    assert cli.main_checkout_env(tmp_path) is None                  # no git at all
    (tmp_path / ".git").write_text("gitdir: ../elsewhere/.git/modules/x\n")
    assert cli.main_checkout_env(tmp_path) is None                  # a .git file that leads nowhere
    (tmp_path / ".git").write_text("not a git file\n")
    assert cli.main_checkout_env(tmp_path) is None


def test_markup_postings_counts_stored_markup_by_source_and_changes_nothing(tmp_path, monkeypatch, capsys):
    """HIR-420: how many stored postings are web-page markup, and from where."""
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    markup = "<div><p>We build agents.</p><ul><li>Python</li></ul></div>"
    for job_id, text, source, url in ((1, markup, "jsearch", "https://jobs.example.com/1"),
                                      (2, "Plain text, with x < 3.", "greenhouse", "https://boards.greenhouse.io/a/2"),
                                      (3, markup, "jsearch", "https://jobs.example.com/3")):
        conn.execute("INSERT INTO job (id, company, title, title_key, description_text, first_seen, last_seen)"
                     " VALUES (?, 'Acme', 'AI Engineer', 'ai engineer', ?, '2026-11-01T00:00:00Z', '2026-11-01T00:00:00Z')",
                     (job_id, text))
        conn.execute("INSERT INTO job_source (job_id, source, source_job_id, url, first_seen, last_seen)"
                     " VALUES (?, ?, ?, ?, '2026-11-01T00:00:00Z', '2026-11-01T00:00:00Z')",
                     (job_id, source, str(job_id), url))
    monkeypatch.setattr(cli, "open_db", lambda: conn)
    cli.main(["markup-postings"])
    out = capsys.readouterr().out
    assert "stored postings whose text is markup: 2" in out
    assert "jsearch jobs.example.com" in out and "job ids: 1, 3" in out and "greenhouse" not in out
    assert conn.execute("SELECT description_text FROM job WHERE id = 1").fetchone()[0] == markup


def test_check_records_the_city_it_is_run_for_and_says_so_when_the_page_gives_none(tmp_path, monkeypatch, capsys):
    """HIR-322: through the real log, not a stub: a link whose page has no location is
    stored under --city (Berlin unless told otherwise), and the output says it was assumed."""
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)

    def fake_check(conn, url, *a, **k):
        located = "Berlin" if "located" in url else None
        page = Posting("url", "", url, "Acme", "AI Engineer", located, "Build LLM agents in Python.")
        return CheckResult(url=url, verdict="not_found", how="", posting=page, diagnosis="not a hosted ATS page")

    monkeypatch.setattr(cli, "open_db", lambda: conn)
    monkeypatch.setattr(cli, "load_feeds", lambda: [])
    monkeypatch.setattr(cli, "check_url", fake_check)
    monkeypatch.setattr(cli.send_checks, "after_check", lambda *a, **k: None)
    cli.main(["check", "https://acme.example/jobs/1", "https://acme.example/located/2"])
    cli.main(["check", "https://acme.example/jobs/3", "--city", "New York"])
    out = capsys.readouterr().out
    cities = dict(conn.execute("SELECT url, city FROM url_check").fetchall())
    assert cities == {"https://acme.example/jobs/1": "Berlin", "https://acme.example/located/2": "Berlin",
                      "https://acme.example/jobs/3": "New York"}
    assert out.count("city recorded as Berlin") == 1          # only the link with no location
    assert out.count("city recorded as New York") == 1
