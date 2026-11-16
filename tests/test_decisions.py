"""The decisions log is one file per decision (HIR-305).

A new decision is a file in `decisions/`, not a block added to `DECISIONS.md`, so two pull
requests that each record one cannot collide. Agents and people find an entry by its date
and ticket, so each file's name and its heading must carry both, and agree.

Does NOT check `DECISIONS.md`: its entries up to 16 Nov 2026 stay as they are, and pull
requests opened before the change may still add to it (decisions/2026-11-16-hir-305-…).
"""

import re
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


def test_the_old_log_points_at_the_folder():
    top = (ROOT / "DECISIONS.md").read_text().split("\n---\n")[0]
    assert "decisions/" in top and "not added to this file" in top
