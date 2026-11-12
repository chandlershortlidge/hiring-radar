"""The pull-request half of the Monday summary (HIR-264). GitHub is a fake that answers
from a list; the one test that runs git builds its own small repository."""

import argparse
import subprocess

from app import caretaker_run as run
from app import db
from app import merged_work as mw

START, END = "2026-11-09", "2026-11-15"
MONDAY = "2026-11-16"


def pr(n, title, merged_at=None, labels=(), body="", created="2026-11-10T08:00:00Z", updated=None):
    return {"number": n, "title": title, "html_url": f"https://github.com/x/y/pull/{n}",
            "merged_at": merged_at, "merge_commit_sha": f"sha{n}" if merged_at else None,
            "labels": [{"name": name} for name in labels], "body": body, "created_at": created,
            "updated_at": updated or merged_at or created}


FILES = {
    "sha1": ["web/src/SkillChart.jsx", "tests/test_queries.py"],
    "sha2": ["web/src/JobList.jsx"],
    "sha3": ["app/geo.py", "tests/test_geo.py"],
    "sha4": ["web/src/ProfileDrawer.jsx"],
    "sha5": ["scripts/lead_pick.py", "DECISIONS.md"],
}
CLOSED = [
    pr(1, "HIR-301: bars on the chart keep their order", "2026-11-10T09:00:00Z"),
    pr(2, "HIR-302: a job card shows its city", "2026-11-11T09:00:00Z", labels=("sent-back", "review-passed")),
    pr(3, "HIR-303: Potsdam postings read as Berlin", "2026-11-12T09:00:00Z"),
    pr(4, "HIR-304: the profile drawer closes on Escape", "2026-11-13T09:00:00Z"),
    pr(5, "HIR-305: the lead agent counts a failed ticket once", "2026-11-15T23:59:00Z"),
    pr(6, "HIR-306: merged the Monday after", "2026-11-16T07:00:00Z"),
    pr(7, "HIR-307: merged the week before", "2026-11-08T23:00:00Z", updated="2026-11-08T23:00:00Z"),
    pr(8, "HIR-308: closed without merging", None, updated="2026-11-12T10:00:00Z"),
]
OPEN = [
    pr(20, "HIR-320: sent back three times, never pinged anyone", labels=("needs-chandler", "sent-back"),
       body="## Needs Chandler\n\nNone.\n\n## Testing\n", created="2026-11-13T08:00:00Z"),
    pr(21, "HIR-321: the reader gets a new instruction", labels=("needs-chandler",),
       body="## Decisions taken\n\nNone\n\n## Needs Chandler\n\n<!-- hint -->\n"
            "- This changes how postings are scored: merge, or send back?\n\n## Escalations\n",
       created="2026-11-11T08:00:00Z"),
    pr(22, "HIR-322: still in review", labels=("sent-back",)),
]


def fake_get(url):
    return OPEN if "state=open" in url else CLOSED


def text():
    return mw.week_text(START, END, fake_get, FILES.get, refresh=lambda: None)


def section(body, heading):
    """The lines under one '# heading', up to the next top-level heading."""
    out, on = [], False
    for line in body.splitlines():
        if line.startswith("# "):
            on = line[2:].startswith(heading)
        elif on:
            out.append(line)
    return "\n".join(out)


# --- the three parts ---------------------------------------------------------------------

def test_needs_you_lists_every_open_pr_with_the_label_pinged_or_not():
    needs = section(text(), "Needs you")
    assert "2 pull requests will not merge until you decide" in needs
    assert "Sent back three times, never pinged anyone" in needs      # no @mention anywhere
    assert "The reader gets a new instruction" in needs
    assert "Still in review" not in needs                             # sent back, not his
    # oldest first, and the question the pull request asks is carried over
    assert needs.index("The reader gets") < needs.index("Sent back three times")
    assert "waiting since 2026-11-11. This changes how postings are scored: merge, or send back?" in needs
    assert needs.rstrip().endswith("waiting since 2026-11-13.")       # "None." is not a question


def test_only_last_weeks_merges_are_listed_each_in_one_group():
    body = text()
    merged = section(body, "What merged")
    assert "5 changes merged" in merged
    assert "Merged the Monday after" not in body and "Merged the week before" not in body
    assert "Closed without merging" not in body
    groups, head = {}, None
    for line in merged.splitlines():
        if line.startswith("## "):
            head = line[3:]
        elif line.startswith("- "):
            groups.setdefault(head, []).append(line)
    assert {h: len(v) for h, v in groups.items()} == {
        "On the chart": 1, "In the job list": 1, "Cities": 1, "Elsewhere on the site": 1,
        "Nothing a visitor would see": 1}
    assert groups["Cities"] == ["- [Potsdam postings read as Berlin](https://github.com/x/y/pull/3)"]
    assert "HIR-30" not in merged                                     # no ticket ids as shorthand


def test_sent_back_and_fixed_is_the_merged_prs_that_carry_the_label():
    fixed = section(text(), "Sent back and fixed")
    assert [line for line in fixed.splitlines() if line.startswith("- ")] == [
        "- [A job card shows its city](https://github.com/x/y/pull/2)"]   # the open one is not fixed yet


def test_a_quiet_week_says_so_in_each_part():
    body = mw.week_text(START, END, lambda url: [], FILES.get, refresh=lambda: None)
    assert "Nothing is waiting for you." in body
    assert "Nothing merged." in body
    assert "Nothing was sent back." in body


# --- sorting -----------------------------------------------------------------------------

def test_a_change_goes_to_the_first_group_it_touches_and_tests_never_decide():
    assert mw.group_of(["app/geo.py", "web/src/SkillChart.jsx"]) == "On the chart"
    assert mw.group_of(["web/src/JobList.test.jsx", "tests/test_geo.py", "README.md"]) == mw.UNSEEN
    assert mw.group_of(["app/sources/ashby.py"]) == "In the job list"
    assert mw.group_of([]) == mw.UNSEEN


def test_a_change_whose_files_cannot_be_read_is_listed_unsorted_not_dropped():
    body = mw.week_text(START, END, fake_get, lambda sha: None, refresh=lambda: None)
    merged = section(body, "What merged")
    assert "5 changes merged" in merged
    assert len([line for line in merged.splitlines() if line.startswith("- ")]) == 5
    assert [line for line in merged.splitlines() if line.startswith("## ")] == [f"## {mw.UNSORTED}"]


def test_titles_lose_the_ticket_prefix_and_nothing_else():
    assert mw.plain_title("HIR-263: the Add a job button keeps its name on phones") == \
        "The Add a job button keeps its name on phones"
    assert mw.plain_title("Header stays on one row") == "Header stays on one row"
    assert mw.plain_title("HIR-9:") == "HIR-9:"


# --- reading -----------------------------------------------------------------------------

def test_reading_stops_at_the_first_page_that_reaches_back_before_the_week():
    asked = []
    old = pr(900, "old", "2026-10-01T00:00:00Z")
    week = [pr(100 + i, f"HIR-{i}: change {i}", "2026-11-10T09:00:00Z") for i in range(100)]

    def get(url):
        asked.append(url)
        if "state=open" in url:
            return []
        return week if url.endswith("&page=1") else [old] * 100
    merged, waiting = mw.fetch(START, END, get, lambda sha: [], refresh=lambda: None)
    assert len(merged) == 100 and waiting == []
    assert len([u for u in asked if "state=closed" in u]) == 2        # page 3 is never asked for


def test_github_unreachable_says_so_and_points_at_the_label():
    def down(url):
        raise OSError("HTTP Error 403: rate limit exceeded")
    body = mw.week_text(START, END, down, FILES.get, refresh=lambda: None)
    assert "GitHub could not be read this morning" in body
    assert "label%3Aneeds-chandler" in body and "rate limit" in body


def test_files_of_a_merge_are_read_from_the_checkout(tmp_path):
    def git(*args):
        subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=t", "-c", "user.email=t@example.com",
                        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *args],
                       check=True, capture_output=True)

    def commit(name, message):
        (tmp_path / name).parent.mkdir(exist_ok=True)
        (tmp_path / name).write_text(name)
        git("add", ".")
        git("commit", "-qm", message)

    git("init", "-q", "-b", "main")
    commit("a.txt", "first")
    git("switch", "-qc", "work")
    commit("web/b.txt", "work 1")
    commit("c.txt", "work 2")
    git("switch", "-q", "main")
    commit("d.txt", "main moved on meanwhile")
    git("merge", "-q", "--no-ff", "work", "-m", "Merge pull request #1")
    sha = subprocess.run(["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    assert mw.git_files(sha, tmp_path) == ["c.txt", "web/b.txt"]
    assert mw.git_files("0" * 40, tmp_path) is None                   # a commit this checkout lacks


# --- one message, not two ----------------------------------------------------------------

def test_monday_posts_one_message_with_the_three_parts_and_the_source_report(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    db.migrate(conn)
    posted = []
    run.report(conn, MONDAY, lambda t, b: posted.append((t, b)) or "HIR-900", log=lambda *_: None,
               changes=lambda s, e: mw.week_text(s, e, fake_get, FILES.get, refresh=lambda: None))
    assert [t for t, _ in posted] == [f"Monday summary: {START} to {END}"]
    body = posted[0][1]
    heads = [line for line in body.splitlines() if line.startswith("# ")]
    assert [h.split(":")[0].split(",")[0] for h in heads] == [
        "# Needs you", "# What merged", "# Sent back and fixed", "# Caretaker"]
    assert "Every source worked all week." in body


def test_the_cli_hands_the_pull_request_half_to_the_monday_post(tmp_path, monkeypatch):
    from app import __main__ as cli
    seen = {}
    monkeypatch.setattr(cli, "open_db", lambda: db.connect(tmp_path / "t.db"))
    monkeypatch.setattr(run, "morning", lambda *a, **k: [])
    monkeypatch.setattr(run, "report", lambda conn, day, post, **kw: seen.update(kw))
    monkeypatch.delenv("LINEAR_API_KEY", raising=False)
    cli.cmd_caretaker(argparse.Namespace(day=MONDAY, no_post=True))
    assert seen["changes"] is mw.week_text
