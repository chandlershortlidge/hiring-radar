"""The reviewer's definition must work in a cloud run as well as on the Mac (HIR-151).

Two things stopped every review in the lead agent's first cloud run: the reviewer was
granted the Linear tools under the Mac's name only, and its instructions used `gh pr …`
commands that fail there. These read the rule files as text; no agent is started.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
REVIEWER = ROOT / ".claude" / "agents" / "reviewer.md"
RULE_FILES = [
    REVIEWER,
    ROOT / ".claude" / "skills" / "work-issue" / "SKILL.md",
    ROOT / ".claude" / "skills" / "work-issue-orchestrator" / "SKILL.md",
    ROOT / ".claude" / "skills" / "lead-agent" / "SKILL.md",
]

LINEAR_PREFIXES = ("mcp__claude_ai_Linear__", "mcp__Linear__")  # the Mac's name, the cloud's
LINEAR_TOOLS = ("get_issue", "list_comments", "save_comment")
BOTH_NAMES = [prefix + tool for prefix in LINEAR_PREFIXES for tool in LINEAR_TOOLS]


def reviewer_tools():
    front = REVIEWER.read_text().split("---")[1]
    line = next(l for l in front.splitlines() if l.startswith("tools:"))
    return [t.strip() for t in line.removeprefix("tools:").split(",")]


@pytest.mark.parametrize("name", BOTH_NAMES)
def test_reviewer_is_granted_each_linear_tool_under_both_names(name):
    assert name in reviewer_tools()


def test_reviewer_can_look_its_linear_tools_up():
    assert "ToolSearch" in reviewer_tools()


def test_reviewer_holds_no_tool_that_edits_an_issue():
    assert not [t for t in reviewer_tools() if t.endswith("save_issue")]


def test_reviewer_loads_both_names_in_one_lookup():
    query = re.search(r"`(select:[^`]+)`", REVIEWER.read_text()).group(1)
    assert sorted(query.removeprefix("select:").split(",")) == sorted(BOTH_NAMES)


@pytest.mark.parametrize("path", RULE_FILES, ids=lambda p: p.parent.name)
def test_no_instruction_runs_a_gh_pr_command(path):
    """`gh pr list/create/edit/merge/checks` fail in a cloud run; `gh api` works in both.

    A line may name those commands to say they fail; it may not carry one with arguments,
    which is what an instruction to run it looks like.
    """
    runs = re.findall(r"gh pr (?:list|create|edit|merge|checks|view) +[-<\d][^`\n]*",
                      path.read_text())
    assert runs == []


# --- the small and the big side of Chandler's list (HIR-278) -------------------------------

AGENTS_MD = ROOT / "AGENTS.md"
POINT_AT_THE_LIST = RULE_FILES + [
    ROOT / ".claude" / "agents" / "decider.md",
    ROOT / ".claude" / "agents" / "senior.md",
    ROOT / ".github" / "pull_request_template.md",
]


def the_list():
    """The six numbered items under AGENTS.md "What Chandler is asked", by number."""
    section = AGENTS_MD.read_text().split("### What Chandler is asked")[1].split("**Small calls:")[0]
    items = re.split(r"^(\d)\. \*\*", section, flags=re.M)[1:]
    return {int(n): " ".join(text.split()) for n, text in zip(items[::2], items[1::2])}


def test_the_one_list_has_six_items_each_with_a_big_side():
    items = the_list()
    assert sorted(items) == [1, 2, 3, 4, 5, 6]
    assert all("big" in text for text in items.values())


def test_the_score_and_the_agents_own_rules_have_no_small_side():
    items = the_list()
    assert "nothing small" in items[2] and "labelling guide" in items[2]
    assert "nothing small" in items[6]
    assert all("*Small:*" in items[n] for n in (1, 3, 4, 5))


def test_the_small_side_keeps_the_tickets_limits():
    items = the_list()
    assert "up to 5 stored jobs" in items[4] and "copy of the database" in items[4]
    assert "last night's backup" in items[4] and "deleting stored jobs, at any count" in items[4]
    assert "up to €10 a week that he can switch off" in items[5]


@pytest.mark.parametrize("path", POINT_AT_THE_LIST, ids=lambda p: p.parent.name + "/" + p.name)
def test_every_agent_and_skill_points_at_the_list_and_keeps_no_copy(path):
    text = " ".join(path.read_text().split())
    assert "What Chandler is asked" in text and "small" in text.lower()
    # The limits live in AGENTS.md only: a second copy is one that drifts.
    assert "5 stored jobs" not in text and "€10 a week" not in text
