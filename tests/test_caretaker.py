"""The caretaker's decisions (HIR-257): what it notices, what it would fix, and the lines
it never crosses. No network, no database, no model: search and board fetches are fakes."""

import json

import pytest

from app import caretaker as ct
from app.caretaker import Budget, Finding, FeedRun, Refused
from app.sources import Posting

DAY = "2026-11-12"


def posting(title="AI Engineer", location="Berlin", company="Doctolib", **kw):
    return Posting(source="ashby", source_job_id=title, url="https://x/1", company=company, title=title,
                   location_raw=location, description_text="Build ML systems in Berlin.", **kw)


def feeds_doc():
    return {"_comment": "x", "feeds": [
        {"type": "arbeitnow", "enabled": True, "max_pages": 5},
        {"type": "greenhouse", "enabled": True, "token": "doctolib", "company": "Doctolib"},
        {"type": "lever", "enabled": True, "token": "pipedrive", "company": "Pipedrive"},
        {"type": "ashby", "enabled": False, "token": "turnedoff", "company": "Turned Off"},
    ]}


def search_returning(urls):
    calls = []

    def search(q):
        calls.append(q)
        return urls
    search.calls = calls
    return search


# --- noticing ----------------------------------------------------------------------------

def test_gone_board_is_switched_to_the_companys_new_board():
    """The Doctolib case: the old board answers 404, the company is now on Ashby."""
    feed = feeds_doc()["feeds"][1]
    search = search_returning(["https://jobs.ashbyhq.com/doctolib/0b8f6f8e-3a1c-4d5e-9f00-1a2b3c4d5e6f", "https://jobs.ashbyhq.com/other/1c8f6f8e-3a1c-4d5e-9f00-1a2b3c4d5e6f"])
    fetch = {("ashby", "doctolib"): [posting()], ("ashby", "other"): [posting(company="Other")]}
    run = FeedRun("greenhouse:doctolib", "board", ok=False, error="HTTPError: HTTP Error 404: Not Found", day=DAY)
    found = ct.judge_board(feed, run, [], known_postings=3, last_seen="2026-10-23T08:00:49Z",
                           find_move=lambda: ct.find_moved_board(feed, search, Budget(), set(), set(),
                                                                 lambda s, t: fetch[(s, t)]))
    assert [(f.finding, f.action, f.data["to"]) for f in found] == [("board_moved", "switch", ["ashby", "doctolib"])]


def test_empty_board_with_no_new_home_is_paused():
    """The Pipedrive case: answers, returns nothing, last posting seen weeks ago."""
    run = FeedRun("lever:pipedrive", "board", ok=True, seen=0, day=DAY)
    found = ct.judge_board(feeds_doc()["feeds"][2], run, [], 1, "2026-10-23T08:00:33Z", lambda: None)
    assert [(f.finding, f.action) for f in found] == [("board_dead", "pause")]


def test_board_quiet_for_less_than_three_days_is_left_alone():
    run = FeedRun("lever:pipedrive", "board", ok=True, seen=0, day=DAY)
    assert ct.judge_board({}, run, [], 1, "2026-11-10T07:00:00Z", lambda: pytest.fail("searched")) == []


def test_gone_board_without_a_new_home_is_reported_not_paused_on_day_one():
    run = FeedRun("greenhouse:x", "board", ok=False, error="HTTP Error 404", day=DAY)
    found = ct.judge_board({}, run, [], 2, "2026-11-11T07:00:00Z", lambda: None)
    assert [(f.finding, f.action) for f in found] == [("board_gone", "report")]


def test_timeout_is_an_error_not_a_gone_board():
    run = FeedRun("greenhouse:x", "board", ok=False, error="TimeoutError: timed out", day=DAY)
    found = ct.judge_board({}, run, [], 2, "2026-11-11T07:00:00Z", lambda: pytest.fail("searched"))
    assert [f.finding for f in found] == ["board_error"]


def test_a_field_missing_since_last_week_is_a_shape_change():
    past = FeedRun("join:x", "board", True, 5, fields=frozenset({"company", "location_raw"}), day="2026-11-08")
    run = FeedRun("join:x", "board", True, 5, fields=frozenset({"company"}), day=DAY)
    found = ct.judge_board({}, run, [past], 5, "2026-11-12T07:00:00Z", lambda: None)
    assert [(f.finding, f.data["missing"]) for f in found] == [("shape_changed", ["location_raw"])]


def test_posting_fields_reads_the_optional_fields():
    assert ct.posting_fields([posting(location=None)]) == {"company", "url"}


def test_feed_far_below_its_median_is_reported():
    hist = [FeedRun("arbeitnow", "feed", True, n, day=f"2026-11-0{i}") for i, n in enumerate([100, 90, 110, 95, 105], 1)]
    assert [f.finding for f in ct.judge_feed(FeedRun("arbeitnow", "feed", True, 40, day=DAY), hist)] == ["feed_low"]
    assert ct.judge_feed(FeedRun("arbeitnow", "feed", True, 60, day=DAY), hist) == []
    assert ct.judge_feed(FeedRun("arbeitnow", "feed", True, 1, day=DAY), hist[:4]) == []  # too little history


def test_collection_missing_or_all_failed_is_rerun():
    assert [f.action for f in ct.judge_collection(DAY, [])] == ["rerun_collection"]
    failed = [FeedRun("a", "feed", False, day=DAY), FeedRun("b", "board", False, day=DAY)]
    assert [f.finding for f in ct.judge_collection(DAY, failed)] == ["collection_failed"]
    assert ct.judge_collection(DAY, failed + [FeedRun("c", "feed", True, 3, day=DAY)]) == []


def test_unfinished_reread_is_reported():
    assert [f.finding for f in ct.judge_pending(12)] == ["extraction_unfinished"]
    assert ct.judge_pending(0) == []


def test_sharp_city_drop_is_reported_small_city_wobble_is_not():
    found = ct.judge_cities({"Berlin": 50, "Hamburg": 5}, {"Berlin": 100, "Hamburg": 15})
    assert [f.subject for f in found] == ["city:Berlin"]
    assert ct.judge_cities({"Berlin": 80}, {"Berlin": 100}) == []


def test_paused_board_comes_back_when_postings_return():
    feed = {"type": "lever", "token": "pipedrive", "paused": {"since": "2026-11-05"}}
    assert [f.action for f in ct.recheck_paused(feed, [posting()], None)] == ["unpause"]
    assert [f.action for f in ct.recheck_paused(feed, [], None)] == ["none"]
    assert ct.is_recheck_day(DAY, "2026-11-05") and not ct.is_recheck_day(DAY, "2026-11-06")


def test_moved_board_must_be_the_same_company_and_have_postings_we_keep():
    feed = feeds_doc()["feeds"][1]
    search = search_returning(["https://jobs.lever.co/acme/1", "https://jobs.ashbyhq.com/doctolib/2"])
    fetch = {("lever", "acme"): [posting(company="Acme")],                      # other company
             ("ashby", "doctolib"): [posting(location="Lisbon")]}               # nothing we keep
    assert ct.find_moved_board(feed, search, Budget(), set(), set(), lambda s, t: fetch[(s, t)]) is None


# --- never does --------------------------------------------------------------------------

def test_never_deletes_a_board_or_any_entry():
    doc = feeds_doc()
    paused = ct.apply(doc, Finding("lever:pipedrive", "board_dead", "pause", "quiet"), DAY)
    assert len(paused["feeds"]) == len(doc["feeds"])
    entry = next(f for f in paused["feeds"] if f.get("token") == "pipedrive")
    assert entry["enabled"] is False and entry["paused"]["since"] == DAY
    assert doc["feeds"][2]["enabled"] is True                     # input not mutated
    with pytest.raises(Refused):
        Finding("lever:pipedrive", "x", "delete", "remove it")


def test_never_touches_extractor_skill_list_or_rule_files():
    for target in ("app/extract.py", "taxonomy/skills.json", "app/migrations/099_x.sql",
                   ".claude/agents/caretaker.md", "AGENTS.md", ".github/workflows/ci.yml",
                   "config/boards_rejected.json", "app/geo.py"):
        with pytest.raises(Refused):
            ct.write_feeds(feeds_doc(), ct.ROOT / target)


def test_writes_a_feeds_copy_outside_the_repo(tmp_path):
    out = tmp_path / "feeds.json"
    ct.write_feeds(feeds_doc(), out)
    assert len(json.loads(out.read_text())["feeds"]) == 4


def test_never_adds_a_board_for_another_company_or_a_second_entry():
    doc = feeds_doc()
    other = Finding("greenhouse:doctolib", "board_moved", "switch", "x",
                    {"to": ["ashby", "acme"], "company": "Acme"})
    with pytest.raises(Refused):
        ct.apply(doc, other, DAY)
    dup = Finding("greenhouse:doctolib", "board_moved", "switch", "x",
                  {"to": ["lever", "pipedrive"], "company": "Pipedrive"})
    with pytest.raises(Refused):
        ct.apply(doc, dup, DAY)
    ok = ct.apply(doc, Finding("greenhouse:doctolib", "board_moved", "switch", "x",
                               {"to": ["ashby", "doctolib"], "company": "Doctolib"}), DAY)
    assert len(ok["feeds"]) == len(doc["feeds"])
    moved = next(f for f in ok["feeds"] if f.get("moved_from"))
    assert (moved["type"], moved["token"], moved["company"]) == ("ashby", "doctolib", "Doctolib")


def test_never_switches_on_a_board_a_person_turned_off_or_a_feed():
    with pytest.raises(Refused):
        ct.apply(feeds_doc(), Finding("ashby:turnedoff", "board_back", "unpause", "x"), DAY)
    with pytest.raises(Refused):
        ct.apply(feeds_doc(), Finding("arbeitnow", "feed_low", "pause", "x"), DAY)
    with pytest.raises(Refused):
        ct.apply(feeds_doc(), Finding("greenhouse:notlisted", "board_dead", "pause", "x"), DAY)


def test_never_turns_on_a_city():
    """No caretaker action names a city, and the module never imports the city list writer."""
    src = (ct.ROOT / "app" / "caretaker.py").read_text()
    assert "ACTIVE_CITIES" not in src
    assert set(ct.ACTIONS) == {"none", "report", "pause", "unpause", "switch", "rerun_collection"}


def test_never_spends_past_the_daily_cap():
    feed = feeds_doc()["feeds"][1]
    search = search_returning([])
    budget = Budget(spent=ct.DAILY_CAP_EUR - 2 * ct.SEARCH_EUR)   # room for two searches today
    ct.find_moved_board(feed, search, budget, set(), set(), lambda s, t: [])
    assert len(search.calls) == 2 and budget.hit
    assert budget.spent <= ct.DAILY_CAP_EUR
    assert [f.finding for f in ct.spend_findings(budget)] == ["spend_cap"]


def test_never_calls_a_model():
    src = (ct.ROOT / "app" / "caretaker.py").read_text()
    assert "anthropic" not in src.lower() and "extract_pending" not in src


# --- reporting ---------------------------------------------------------------------------

def test_weekly_summary_groups_by_latest_finding_and_says_report_only():
    rows = [ct.as_row(Finding("lever:pipedrive", "board_dead", "pause", "Pipedrive is quiet."), "2026-11-10", "report", False),
            ct.as_row(Finding("greenhouse:doctolib", "board_moved", "switch", "Doctolib moved."), "2026-11-10", "report", False),
            ct.as_row(Finding("arbeitnow", "feed_low", "report", "Arbeitnow is low."), "2026-11-11", "report", False)]
    text = ct.weekly_summary(rows, "2026-11-09", "2026-11-15", acting=False)
    assert "report-only" in text and "## What it would have fixed" in text
    assert text.index("Doctolib moved") < text.index("Pipedrive is quiet") < text.index("Arbeitnow is low")
    assert ct.weekly_summary([], "a", "b", acting=True).endswith("Every source worked all week.")
    acted = ct.weekly_summary(rows, "2026-11-09", "2026-11-15", acting=True)        # HIR-261
    assert "report-only" not in acted and "would have" not in acted
    assert "## What it fixed or filed to fix" in acted and "## What it filed to pause" in acted


# --- the day's fixes as a ticket, and back (HIR-261) --------------------------------------

def fix_rows():
    return [ct.as_row(Finding("lever:pipedrive", "board_dead", "pause", "lever:pipedrive is quiet, so pause it.",
                              {"last_seen": "2026-10-23T08:00:00Z"}), DAY, "act", False),
            ct.as_row(Finding("greenhouse:doctolib", "board_moved", "switch", "Doctolib moved to ashby:doctolib.",
                              {"to": ["ashby", "doctolib"], "relevant": 3, "company": "Doctolib"}), DAY, "act", False)]


def test_a_fix_ticket_reads_back_as_the_same_fixes_and_applies_only_them():
    title, body = ct.fix_ticket_text(fix_rows(), DAY)
    assert title == f"Caretaker: job-source fixes for {DAY}"
    assert "found 2 fixes" in body and "- lever:pipedrive is quiet, so pause it." in body
    assert ct.NO_SPEND_LINE in body
    assert body.index("+++ Agent notes") < body.index("```json") < body.rindex("+++")
    back = ct.fixes_from_text(body)
    assert back == [Finding(r["subject"], r["finding"], r["action"], r["detail"], r["data"]) for r in fix_rows()]
    doc = feeds_doc()
    after = ct.apply_fixes(doc, body)
    assert after["feeds"][0] == doc["feeds"][0] and after["feeds"][3] == doc["feeds"][3]
    assert after["feeds"][1] == {"type": "ashby", "enabled": True, "token": "doctolib", "company": "Doctolib",
                                 "moved_from": "greenhouse:doctolib"}
    assert after["feeds"][2]["enabled"] is False and after["feeds"][2]["paused"]["since"] == DAY
    assert after["_comment"] == "x" and doc["feeds"][2]["enabled"] is True          # input not mutated


def test_a_fix_ticket_carries_only_edits_of_the_job_source_list():
    rerun = ct.as_row(Finding("collection", "collection_missing", "rerun_collection", "x"), DAY, "act", False)
    with pytest.raises(Refused):
        ct.fix_ticket_text([rerun], DAY)
    _, body = ct.fix_ticket_text(fix_rows(), DAY)
    for tampered in (body.replace('"action": "pause"', '"action": "rerun_collection"'),
                     body.replace('"action": "pause"', '"action": "delete"'),
                     body.replace('"day": "2026-11-12"', '"day": "soon"'),
                     body.replace('"subject": "lever:pipedrive",', ""),
                     body + body,                                   # two blocks: which one?
                     "no block at all",
                     '```json\n{"caretaker_fixes": []}\n```'):
        with pytest.raises(Refused):
            ct.fixes_from_text(tampered)


def test_applying_a_ticket_is_all_or_nothing_and_keeps_every_never_does_line():
    _, body = ct.fix_ticket_text(fix_rows(), DAY)
    doc = feeds_doc()
    once = ct.apply_fixes(doc, body)
    with pytest.raises(Refused):                 # the switch was already made: nothing to match
        ct.apply_fixes(once, body)
    other_company = body.replace('"doctolib"\n', '"acme"\n').replace('"company": "Doctolib"', '"company": "Acme"')
    assert other_company != body
    with pytest.raises(Refused):
        ct.apply_fixes(doc, other_company)
    person_disabled = ct.fix_ticket_text([ct.as_row(
        Finding("ashby:turnedoff", "board_back", "unpause", "x"), DAY, "act", False)], DAY)[1]
    with pytest.raises(Refused):
        ct.apply_fixes(doc, person_disabled)
    no_target = body.replace('"to": [', '"elsewhere": [')
    with pytest.raises(Refused):
        ct.apply_fixes(doc, no_target)


def test_apply_fixes_refuses_anything_but_the_feeds_file(tmp_path, monkeypatch, capsys):
    """The command a pull request runs: it writes the feeds file and nothing else, and a
    refused fix leaves the file as it was."""
    import argparse

    import app.__main__ as cli
    _, body = ct.fix_ticket_text(fix_rows(), DAY)
    ticket = tmp_path / "ticket.md"
    ticket.write_text(body)
    feeds = tmp_path / "feeds.json"
    ct.write_feeds(feeds_doc(), feeds)
    monkeypatch.setattr(cli, "FEEDS_PATH", feeds)
    cli.cmd_caretaker_apply_fixes(argparse.Namespace(file=str(ticket)))
    written = json.loads(feeds.read_text())
    assert written == ct.apply_fixes(feeds_doc(), body)
    assert "2 fixes written to feeds.json" in capsys.readouterr().out
    assert sorted(p.name for p in tmp_path.iterdir()) == ["feeds.json", "ticket.md"]

    with pytest.raises(SystemExit, match="refused, nothing was written"):   # a second time: already made
        cli.cmd_caretaker_apply_fixes(argparse.Namespace(file=str(ticket)))
    assert json.loads(feeds.read_text()) == written

    monkeypatch.setattr(cli, "FEEDS_PATH", tmp_path / "skills.json")        # any other file name
    (tmp_path / "skills.json").write_text(json.dumps(feeds_doc()))
    with pytest.raises(SystemExit, match="writes only feeds.json"):
        cli.cmd_caretaker_apply_fixes(argparse.Namespace(file=str(ticket)))
    assert json.loads((tmp_path / "skills.json").read_text()) == feeds_doc()


def test_urgent_only_for_two_failed_days_or_the_cap():
    down = Finding("collection", "collection_missing", "rerun_collection", "x")
    assert ct.urgent([down], []) == []
    assert ct.urgent([down], [down]) == ["The job collection has failed two days running."]
    assert ct.urgent([Finding("caretaker", "spend_cap", "report", "cap")], []) == ["cap"]


def test_post_to_linear_sends_one_issue_and_raises_on_refusal():
    sent = []

    def post(url, payload, headers):
        sent.append((url, payload, headers))
        return {"data": {"issueCreate": {"success": True, "issue": {"identifier": "HIR-999"}}}}
    assert ct.post_to_linear("t", "b", "key", "team", post) == "HIR-999"
    assert sent[0][1]["variables"]["input"] == {"teamId": "team", "title": "t", "description": "b"}
    with pytest.raises(RuntimeError):
        ct.post_to_linear("t", "b", "key", "team", lambda *a: {"errors": [{"message": "no"}]})
