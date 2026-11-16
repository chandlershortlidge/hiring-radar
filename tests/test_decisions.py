"""The decisions log is one file per decision (HIR-305).

A new decision is a file in `decisions/`, not a block added to `DECISIONS.md`, so two pull
requests that each record one cannot collide. Agents and people find an entry by its date
and ticket, so each file's name and its heading must carry both, and agree.

Does NOT check `DECISIONS.md`: its entries up to 16 Nov 2026 stay as they are, and pull
requests opened before the change may still add to it (decisions/2026-11-16-hir-305-…).
"""

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "decisions"
NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-hir-(\d+)-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — \S.*\(.*HIR-(\d+).*\)$")
ENTRIES = sorted(FOLDER.glob("*"))


def test_the_folder_holds_at_least_the_entry_that_created_it():
    assert FOLDER / "2026-11-16-hir-305-one-file-per-decision.md" in ENTRIES


@pytest.mark.parametrize("path", ENTRIES, ids=lambda p: p.name)
def test_an_entry_is_named_by_date_and_ticket_and_its_heading_agrees(path):
    name = NAME.match(path.name)
    assert name, "name it YYYY-MM-DD-hir-N-short-title.md (lower case, hyphens)"
    heading = HEADING.match(path.read_text().splitlines()[0])
    assert heading, "first line: ## YYYY-MM-DD — what was decided (HIR-N)"
    assert heading.group(1) == name.group(1), "the heading's date is not the file name's"
    assert name.group(2) in re.findall(r"HIR-(\d+)", path.read_text().splitlines()[0])


def test_two_branches_that_each_record_a_decision_merge_without_a_collision(tmp_path):
    """The reason for the folder, on a real merge: two entries added as two files merge;
    the same two entries added at the top of one shared file do not."""
    def git(*args, ok=True):
        done = subprocess.run(["git", *args], cwd=tmp_path, capture_output=True, text=True)
        assert not ok or done.returncode == 0, done.stderr
        return done.returncode

    git("init", "-q", "-b", "main")
    for key, value in (("user.email", "t@example.com"), ("user.name", "t"), ("commit.gpgsign", "false")):
        git("config", key, value)
    (tmp_path / "LOG.md").write_text("# Log\n\n## old entry\n")
    git("add", "-A")
    git("commit", "-q", "-m", "base")
    for ticket in ("401", "402"):
        git("switch", "-q", "-c", f"hir-{ticket}", "main")
        (tmp_path / "decisions").mkdir(exist_ok=True)
        (tmp_path / "decisions" / f"2026-11-20-hir-{ticket}-a-rule.md").write_text(
            f"## 2026-11-20 — a rule (HIR-{ticket})\n")
        git("add", "-A")
        git("commit", "-q", "-m", f"folder {ticket}")
        git("switch", "-q", "-c", f"old-{ticket}", "main")
        (tmp_path / "LOG.md").write_text(f"# Log\n\n## 2026-11-20 — a rule (HIR-{ticket})\n\n## old entry\n")
        git("commit", "-q", "-am", f"shared file {ticket}")

    git("switch", "-q", "main")
    assert git("merge", "-q", "--no-edit", "hir-401") == 0
    assert git("merge", "-q", "--no-edit", "hir-402") == 0
    assert len(list((tmp_path / "decisions").glob("*.md"))) == 2
    assert git("merge", "-q", "--no-edit", "old-401") == 0
    assert git("merge", "-q", "--no-edit", "old-402", ok=False) != 0  # the old way collides


def test_the_old_log_points_at_the_folder():
    top = (ROOT / "DECISIONS.md").read_text().split("\n---\n")[0]
    assert "decisions/" in top and "not added to this file" in top
