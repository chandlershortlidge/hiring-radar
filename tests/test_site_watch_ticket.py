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

    def __init__(self, open_title=None, fixed=()):
        # `fixed`: identifiers of tickets with the asked title closed as done in the window.
        self.open_title, self.fixed, self.sent = open_title, list(fixed), []

    def __call__(self, payload):
        self.sent.append(payload)
        q, v = payload["query"], payload["variables"]
        if "issues(" in q and "completedAt" in q:
            return {"data": {"issues": {"nodes": [{"identifier": i, "completedAt": f"2026-11-{n:02d}T10:00:00Z"}
                                                  for n, i in enumerate(self.fixed, 1)]}}}
        if "issues(" in q:
            nodes = [{"id": "uuid-1", "identifier": "HIR-900"}] if v["title"] == self.open_title else []
            return {"data": {"issues": {"nodes": nodes}}}
        if "issueLabels" in q:
            return {"data": {"issueLabels": {"nodes": [{"id": f"label-{v['name']}"}]}}}
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


def test_a_broken_mcp_tool_is_named_as_a_tool_not_a_screen_width(tmp_path):
    """HIR-366: the MCP checks run as their own project, "mcp", which is not a width."""
    fake = FakeLinear()
    title = "MCP tool get_job: get the full details of one job from that search"
    rep = write_report(tmp_path, report(spec(title, ("mcp", "unexpected"))))
    assert run(["--kind", "deploy", "--report", rep, "--change", "abc1234 Merge pull request #150",
                "--rolled-back-to", "def5678"], fake) == 0
    [issue] = fake.created()
    assert issue["title"] == f'Site watch: "{title}" fails'
    assert issue["labelIds"] == ["label-autopilot"]
    body = issue["description"]
    assert f"**Failing MCP tool:** {title}." in body and "what the tool answered" in body
    assert "width" not in body and "The deploy was rolled back" in body


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


def test_an_outage_already_ticketed_adds_nothing():
    # Uptime is checked every five minutes; a comment each time would bury the ticket.
    fake = FakeLinear(open_title="Site watch: the site does not answer")
    run(["--kind", "uptime", "--detail", "HTTP 502"], fake)
    assert fake.created() == []
    assert not [p for p in fake.sent if "commentCreate" in p["query"]]


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


# --- the same break after two fixes (HIR-260) ---------------------------------------------

def test_one_earlier_fix_still_goes_to_an_agent(tmp_path):
    fake = FakeLinear(fixed=["HIR-300"])
    rep = write_report(tmp_path, report(spec("compare mode", ("desktop", "unexpected"))))
    run(["--kind", "deploy", "--report", rep], fake)
    [issue] = fake.created()
    assert issue["labelIds"] == ["label-autopilot"]
    assert "broken again" not in issue["description"]


def test_the_third_break_after_two_fixes_is_not_handed_to_an_agent(tmp_path, capsys):
    fake = FakeLinear(fixed=["HIR-300", "HIR-310"])
    rep = write_report(tmp_path, report(spec("compare mode", ("desktop", "unexpected"))))
    assert run(["--kind", "deploy", "--report", rep], fake) == 0
    [issue] = fake.created()
    assert issue["title"] == 'Site watch: "compare mode" fails'      # same title: a 4th failure comments
    assert issue["labelIds"] == ["label-attended"]
    assert "assigneeId" not in issue                                 # Monday, not a ping
    assert issue["description"].startswith(
        "**This has broken again after 2 fixes in the last 30 days** (HIR-300, HIR-310)")
    assert "rolled back" in issue["description"]                     # the ordinary ticket text follows
    assert "Monday summary" in capsys.readouterr().out


def test_fixes_are_counted_per_title_among_done_tickets_of_the_last_30_days(tmp_path):
    fake = FakeLinear(fixed=["HIR-300", "HIR-310"])
    rep = write_report(tmp_path, report(spec("compare mode", ("desktop", "unexpected"))))
    run(["--kind", "morning", "--report", rep], fake)
    [q] = [p for p in fake.sent if "completedAt" in p["query"]]
    assert q["variables"]["title"] == 'Site watch: "compare mode" fails'
    assert 'type: {eq: "completed"}' in q["query"] and '"-P30D"' in q["query"]


def test_an_outage_after_two_fixes_is_not_handed_to_an_agent():
    fake = FakeLinear(fixed=["HIR-300", "HIR-310"])
    run(["--kind", "uptime", "--detail", "HTTP 502"], fake)
    assert fake.created()[0]["labelIds"] == ["label-attended"]


def test_an_open_ticket_is_commented_on_without_counting_fixes(tmp_path):
    fake = FakeLinear(open_title='Site watch: "compare mode" fails', fixed=["HIR-300", "HIR-310"])
    rep = write_report(tmp_path, report(spec("compare mode", ("desktop", "unexpected"))))
    run(["--kind", "morning", "--report", rep], fake)
    assert fake.created() == [] and not [p for p in fake.sent if "completedAt" in p["query"]]


def test_rollback_failed_is_unchanged_by_earlier_fixes(tmp_path):
    fake = FakeLinear(fixed=["HIR-300", "HIR-310"])
    run(["--kind", "rollback-failed", "--report", str(tmp_path / "none.json")], fake)
    [issue] = fake.created()
    assert issue["assigneeId"] == swt.CHANDLER_ID and "labelIds" not in issue


def test_when_earlier_fixes_cannot_be_counted_the_ticket_is_still_filed_for_an_agent(tmp_path, capsys):
    class NoCount(FakeLinear):
        def __call__(self, payload):
            if "completedAt" in payload["query"]:
                return {"errors": [{"message": "bad filter"}]}
            return super().__call__(payload)

    fake = NoCount()
    rep = write_report(tmp_path, report(spec("compare mode", ("desktop", "unexpected"))))
    assert run(["--kind", "deploy", "--report", rep], fake) == 0
    assert fake.created()[0]["labelIds"] == ["label-autopilot"]
    assert "could not count earlier fixes" in capsys.readouterr().err


# --- a rollback that never ran is not "site down and rollback failed" (HIR-317) -----------

def test_a_rollback_that_could_not_log_in_says_so_and_goes_to_chandler(tmp_path):
    fake = FakeLinear()
    rep = write_report(tmp_path, report(spec("a job card", ("phone", "unexpected"))))
    run(["--kind", "rollback-not-done", "--rollback-problem", "login", "--report", rep,
         "--change", "8a8bffe Merge #185", "--rolled-back-to", "733607b"], fake)
    [issue] = fake.created()
    assert issue["title"] == "Deploy failed the robot visitor and the rollback did not run"
    body = issue["description"]
    assert "The rollback could not log in to the server." in body
    assert "The site is still on the new version:** 8a8bffe Merge #185" in body
    assert "The rollback would have put back:** 733607b" in body
    assert "a job card (phone)" in body and "not run a second time" in body
    # Not the wording of the ticket for a rollback that ran and did not help.
    assert "Site down" not in issue["title"] and "still fails" not in body
    # A version the robot failed is live and no agent can reach the server: Chandler's.
    assert issue["assigneeId"] == swt.CHANDLER_ID and issue["priority"] == 1
    assert "labelIds" not in issue


def test_a_rollback_that_failed_for_another_reason_does_not_claim_a_login_problem(tmp_path):
    fake = FakeLinear()
    run(["--kind", "rollback-not-done", "--report", str(tmp_path / "none.json")], fake)
    [issue] = fake.created()
    assert "The rollback job failed before it finished." in issue["description"]
    assert "could not log in" not in issue["description"]


def test_the_workflow_files_the_right_ticket_for_each_way_a_rollback_ends():
    """The shell lines in site-watch.yml that pick the ticket, run as they are."""
    import subprocess

    import yaml
    wf = yaml.safe_load((ROOT / ".github" / "workflows" / "site-watch.yml").read_text())
    [step] = [s for s in wf["jobs"]["report"]["steps"] if s.get("name") == "File the ticket"]
    assert step["env"]["ROLLBACK_LOGIN"] == "${{ needs.rollback.outputs.login }}"
    script = step["run"]
    picker = script[script.index('if [ "$MODE" = morning ]'):script.index('echo "Filing')]
    assert '--rollback-problem "$problem"' in script

    def pick(mode, rollback, recheck, login=""):
        out = subprocess.run(["bash", "-ec", picker + '\necho "$kind $problem"'], capture_output=True, text=True,
                             env={"PATH": "/usr/bin:/bin", "MODE": mode, "ROLLBACK": rollback,
                                  "RECHECK": recheck, "ROLLBACK_LOGIN": login}, check=True)
        return out.stdout.strip()

    assert pick("morning", "skipped", "") == "morning other"
    assert pick("deploy", "success", "true") == "deploy other"
    assert pick("deploy", "success", "false") == "rollback-failed other"
    assert pick("deploy", "failure", "", "refused") == "rollback-not-done login"
    assert pick("deploy", "failure", "") == "rollback-not-done other"
    # deploy.yml hands the reason up: the step, the job and the workflow each pass it on.
    dep = yaml.safe_load((ROOT / ".github" / "workflows" / "deploy.yml").read_text())
    assert dep[True]["workflow_call"]["outputs"]["login"]["value"] == "${{ jobs.deploy.outputs.login }}"
    assert dep["jobs"]["deploy"]["outputs"]["login"] == "${{ steps.vm.outputs.login }}"
    assert 'if [ "$rc" = 75 ]; then echo "login=refused" >> "$GITHUB_OUTPUT"; fi' in dep["jobs"]["deploy"]["steps"][-1]["run"]


# --- "site down" only when nothing passed on the rolled-back site (HIR-359) ----------------

def two_reports(tmp_path, first, recheck):
    a, b = tmp_path / "first.json", tmp_path / "recheck.json"
    a.write_text(json.dumps(first))
    b.write_text(json.dumps(recheck))
    return ["--kind", "rollback-failed", "--report", str(a), "--recheck-report", str(b),
            "--change", "8d329b6 Merge pull request #217", "--rolled-back-to", "46b4276", "--run-url", "https://gh/run/7"]


def test_a_path_that_still_fails_on_a_site_that_is_up_goes_to_an_agent_not_to_chandler(tmp_path):
    """19 Nov: the rolled-back site passed eight of nine paths and Chandler got "site down"."""
    fake = FakeLinear()
    first = report(spec("each filter reaches the server", ("desktop", "unexpected"), ("phone", "unexpected")))
    recheck = report(spec("home loads", ("desktop", "expected"), ("phone", "flaky")),
                     spec("a job card", ("desktop", "expected"), ("phone", "unexpected")))
    assert run(two_reports(tmp_path, first, recheck), fake) == 0
    [issue] = fake.created()
    assert issue["title"] == 'Site watch: "a job card" fails'   # the second run's failure, not the first's
    assert issue["labelIds"] == ["label-autopilot"]
    assert "assigneeId" not in issue and issue["priority"] == 2
    body = issue["description"]
    for needle in ("**the site is up**", "probably not caused by the deploy", "a job card — at phone width",
                   "8d329b6 Merge pull request #217", "put back by the rollback:** 46b4276",
                   "- each filter reaches the server (desktop and phone)", "https://gh/run/7"):
        assert needle in body
    # The Monday summary reads this sentence to say the change was rolled back (app/site_watch_week.py).
    assert "The deploy was rolled back" in body
    assert "![screenshot]" not in body   # the second run's screenshots are not published


def test_every_path_that_still_fails_gets_its_own_ticket(tmp_path):
    fake = FakeLinear()
    recheck = report(spec("home loads", ("desktop", "flaky"), ("phone", "unexpected")),
                     spec("each filter", ("desktop", "unexpected"), ("phone", "skipped")))
    run(two_reports(tmp_path, report(spec("each filter", ("desktop", "unexpected"))), recheck), fake)
    assert [i["title"] for i in fake.created()] == ['Site watch: "home loads" fails', 'Site watch: "each filter" fails']


def test_site_down_when_no_path_passed_after_the_rollback_and_the_ticket_shows_both_runs(tmp_path):
    fake = FakeLinear()
    first = report(spec("compare mode", ("desktop", "unexpected")))
    recheck = report(spec("home loads", ("desktop", "unexpected"), ("phone", "unexpected")),
                     spec("each filter", ("desktop", "skipped"), ("phone", "skipped")))
    run(two_reports(tmp_path, first, recheck), fake)
    [issue] = fake.created()
    assert issue["title"] == "Site down and rollback failed"
    assert issue["assigneeId"] == swt.CHANDLER_ID and issue["priority"] == 1 and "labelIds" not in issue
    after, before = issue["description"].split("What it found on the new version, before the rollback:")
    assert "No visitor path passed on the rolled-back site" in after
    assert "- home loads (desktop and phone)" in after and "compare mode" not in after
    assert "- compare mode (desktop)" in before and "home loads" not in before


def test_site_down_when_the_second_report_is_missing_unreadable_or_names_no_failure(tmp_path):
    """Any doubt about the rolled-back site stays on the urgent side."""
    first = report(spec("compare mode", ("desktop", "unexpected")))
    argv = two_reports(tmp_path, first, report(spec("home loads", ("desktop", "expected"))))
    for case in ("no failing path", "not json", "missing", "not passed at all"):
        recheck = tmp_path / "recheck.json"
        if case == "not json":
            recheck.write_text("<html>")
        elif case == "missing":
            recheck.unlink()
        elif case == "not passed at all":
            argv = [a for a in argv if a not in ("--recheck-report", str(recheck))]
        fake = FakeLinear()
        assert run(argv, fake) == 0, case
        [issue] = fake.created()
        assert issue["title"] == "Site down and rollback failed", case
        assert "could not be read or names no failing path" in issue["description"], case
        assert "- compare mode (desktop)" in issue["description"], case


def test_the_workflow_hands_the_second_report_to_the_ticket_script():
    import yaml
    wf = yaml.safe_load((ROOT / ".github" / "workflows" / "site-watch.yml").read_text())
    steps = wf["jobs"]["report"]["steps"]
    [get] = [s for s in steps if s.get("with", {}).get("name") == "watch-recheck"]
    # The robot's composite action uploads web/watch-out/ under this name from the recheck job.
    assert wf["jobs"]["recheck"]["steps"][-1]["with"]["artifact"] == "watch-recheck"
    assert get["continue-on-error"] is True   # a missing artifact must not stop the ticket
    [file] = [s for s in steps if s.get("name") == "File the ticket"]
    assert steps.index(get) < steps.index(file)
    assert f"--recheck-report {get['with']['path']}/report.json" in file["run"]
