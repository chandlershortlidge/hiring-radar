"""Tests for scripts/site_watch_ticket.py (HIR-258). Linear is never called: a fake poster
stands in for the HTTP request and records what would have been sent."""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("site_watch_ticket", ROOT / "scripts" / "site_watch_ticket.py")
swt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(swt)


def result(status="failed", msg="\x1b[2mexpect\x1b[22m(locator).toBeVisible() failed", shot="/r/x-desktop/test-failed-1.png"):
    return {"status": status, "error": {"message": msg}, "errors": [{"message": msg}],
            "attachments": [{"name": "screenshot", "contentType": "image/png", "path": shot},
                            {"name": "error-context", "contentType": "text/markdown", "path": "/r/x/error-context.md"}]}


def spec(title, *tests):
    return {"title": title, "tests": [{"projectName": p, "status": s, "results": [result(shot=f"/r/{p}/shot.png")]} for p, s in tests]}


def report(*specs):
    # Playwright nests describe blocks as suites inside the file's suite.
    return {"suites": [{"title": "site-watch.spec.js", "specs": list(specs[:1]), "suites": [{"title": "inner", "specs": list(specs[1:])}]}]}


def test_one_failure_per_path_with_both_widths_merged():
    r = report(spec("the add-a-job drawer opens", ("desktop", "unexpected"), ("phone", "unexpected")),
               spec("compare mode", ("desktop", "expected"), ("phone", "skipped")))
    f = swt.failures(r)
    assert [x["test"] for x in f] == ["the add-a-job drawer opens"]
    assert f[0]["projects"] == ["desktop", "phone"]
    assert f[0]["screenshots"] == ["/r/desktop/shot.png", "/r/phone/shot.png"]


def test_colour_codes_are_stripped_from_the_error():
    f = swt.failures(report(spec("p", ("desktop", "unexpected"))))
    assert f[0]["error"] == "expect(locator).toBeVisible() failed"


def test_a_path_that_passed_on_retry_is_not_a_failure():
    assert swt.failures(report(spec("p", ("desktop", "flaky")))) == []


def test_failures_found_in_nested_suites():
    r = report(spec("top", ("desktop", "expected")), spec("nested", ("phone", "unexpected")))
    assert [x["test"] for x in swt.failures(r)] == ["nested"]


def test_screenshot_url_is_relative_to_the_results_folder(tmp_path):
    shot = tmp_path / "results" / "a-desktop" / "test-failed-1.png"
    assert swt.shot_url(str(shot), str(tmp_path / "results"), "https://raw.example/site-watch/9/") \
        == "https://raw.example/site-watch/9/a-desktop/test-failed-1.png"
    # A file outside the published folder has no public URL: no broken image in the ticket.
    assert swt.shot_url("/elsewhere/x.png", str(tmp_path / "results"), "https://raw.example") is None


class FakeLinear:
    """Answers the three queries the script makes; `open` is the title of an already-open issue."""

    def __init__(self, open_title=None):
        self.open_title, self.sent = open_title, []

    def __call__(self, payload):
        self.sent.append(payload)
        q, v = payload["query"], payload["variables"]
        if "issues(" in q:
            nodes = [{"id": "uuid-1", "identifier": "HIR-900"}] if v["title"] == self.open_title else []
            return {"data": {"issues": {"nodes": nodes}}}
        if "issueLabels" in q:
            return {"data": {"issueLabels": {"nodes": [{"id": "label-autopilot"}]}}}
        if "issueCreate" in q:
            return {"data": {"issueCreate": {"issue": {"identifier": "HIR-901"}}}}
        if "commentCreate" in q:
            return {"data": {"commentCreate": {"success": True}}}
        raise AssertionError(q)

    def created(self):
        return [p["variables"]["input"] for p in self.sent if "issueCreate" in p["query"]]


def write_report(tmp_path, r):
    p = tmp_path / "report.json"
    p.write_text(json.dumps(r))
    return str(p)


def run(argv, fake):
    return swt.main(argv, linear=swt.Linear("k", post=fake))


def test_deploy_failure_files_an_autopilot_ticket_saying_it_was_rolled_back(tmp_path):
    fake = FakeLinear()
    rep = write_report(tmp_path, report(spec("the add-a-job drawer opens", ("phone", "unexpected"))))
    assert run(["--kind", "deploy", "--report", rep, "--change", "abc1234 Merge pull request #150",
                "--rolled-back-to", "def5678", "--run-url", "https://gh/run/1"], fake) == 0
    [issue] = fake.created()
    assert issue["title"] == 'Site watch: "the add-a-job drawer opens" fails'
    assert issue["labelIds"] == ["label-autopilot"]
    assert "assigneeId" not in issue
    for needle in ("rolled back", "abc1234 Merge pull request #150", "def5678", "phone", "https://gh/run/1"):
        assert needle in issue["description"]


def test_a_break_already_ticketed_gets_a_comment_not_a_second_ticket(tmp_path):
    fake = FakeLinear(open_title='Site watch: "compare mode" fails')
    rep = write_report(tmp_path, report(spec("compare mode", ("desktop", "unexpected"))))
    assert run(["--kind", "morning", "--report", rep], fake) == 0
    assert fake.created() == []
    [comment] = [p["variables"] for p in fake.sent if "commentCreate" in p["query"]]
    assert comment["issue"] == "uuid-1"
    assert "morning run" in comment["body"]


def test_two_broken_paths_are_two_tickets(tmp_path):
    fake = FakeLinear()
    rep = write_report(tmp_path, report(spec("a", ("desktop", "unexpected")), spec("b", ("phone", "unexpected"))))
    run(["--kind", "morning", "--report", rep], fake)
    assert [i["title"] for i in fake.created()] == ['Site watch: "a" fails', 'Site watch: "b" fails']


def test_rollback_failed_goes_to_chandler_and_not_to_an_agent(tmp_path):
    fake = FakeLinear()
    rep = write_report(tmp_path, report(spec("home loads", ("desktop", "unexpected"))))
    run(["--kind", "rollback-failed", "--report", rep, "--change", "abc", "--rolled-back-to", "def"], fake)
    [issue] = fake.created()
    assert issue["title"] == "Site down and rollback failed"
    assert issue["assigneeId"] == swt.CHANDLER_ID
    assert issue["priority"] == 1
    assert "labelIds" not in issue
    assert "home loads" in issue["description"]


def test_uptime_ticket(tmp_path):
    fake = FakeLinear()
    run(["--kind", "uptime", "--detail", "HTTP 502 from /api/stats"], fake)
    [issue] = fake.created()
    assert issue["title"] == "Site watch: the site does not answer"
    assert "HTTP 502" in issue["description"]
    assert issue["labelIds"] == ["label-autopilot"]


def test_a_red_run_with_no_failing_path_still_files_a_ticket(tmp_path):
    fake = FakeLinear()
    run(["--kind", "deploy", "--report", str(tmp_path / "missing.json")], fake)
    [issue] = fake.created()
    assert "robot visitor itself" in issue["title"]


def test_without_a_key_it_prints_the_ticket_and_exits_2(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("LINEAR_API_KEY", raising=False)
    assert swt.main(["--kind", "uptime"]) == 2
    out = capsys.readouterr()
    assert "would file: Site watch: the site does not answer" in out.out
    assert "LINEAR_API_KEY is not set" in out.err


def test_a_linear_error_is_raised_not_swallowed():
    import pytest
    lin = swt.Linear("k", post=lambda p: {"errors": [{"message": "bad"}]})
    with pytest.raises(RuntimeError, match="bad"):
        lin.open_issue("x")
