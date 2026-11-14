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


# --- the big side comes in two kinds: to think about, to approve (HIR-297) -----------------

def the_two_kinds():
    """AGENTS.md's paragraph block on the two kinds of big call, as one line of text."""
    section = AGENTS_MD.read_text().split("**Big calls come in two kinds")[1].split("How the list is used:")[0]
    return " ".join(section.split())


def test_the_list_says_what_he_thinks_through_and_what_he_only_approves():
    text = the_two_kinds()
    for skill in ("how quality is measured", "the model and its instructions", "cost engineering",
                  "how the system is designed", "data-science work on the collected data"):
        assert skill in text, skill
    for chore in ("launch chores (domain, legal pages, analytics)", "deleting stored data",
                  "changes to the agents' own rules"):
        assert chore in text, chore


def test_a_recommendation_to_approve_is_three_fixed_lines():
    text = the_two_kinds()
    assert "> **Recommend:**" in text and "> **What it is:**" in text and "> **Why:**" in text
    assert "three lines at most" in text and "No options list" in text
    assert "If it cannot be said in those three lines, it is not ready to ask." in text


def test_a_question_to_think_about_says_what_he_would_learn():
    assert "**What you would learn**" in the_two_kinds()


def test_the_senior_agent_says_the_kind_and_doubt_never_costs_his_thinking_time():
    text = the_two_kinds()
    assert "The **senior agent**" in text
    assert "When unsure whether a call teaches a career skill, it is to approve" in text
    assert "Anything about how quality is measured is always to think about, never downgraded." in text


def test_the_split_puts_nothing_on_the_list_and_decides_nothing_without_him():
    # The ticket's "Out of scope": what is small does not change, no big call is decided alone.
    text = the_two_kinds()
    assert "puts nothing on the list and takes nothing off it" in text
    assert "no big call is decided without his yes" in text


def test_monday_and_the_speed_limit_are_written_where_the_list_is():
    text = " ".join(AGENTS_MD.read_text().split())
    assert "**To think about**, at most 3 a week" in text and "**To approve**, the rest of the" in text
    assert "Only the to-think-about pile slows the lead agent down." in text
    assert "Recommendations waiting for his yes do not count" in text


@pytest.mark.parametrize("path", POINT_AT_THE_LIST, ids=lambda p: p.parent.name + "/" + p.name)
def test_every_agent_and_skill_knows_the_two_kinds_and_keeps_no_copy_of_the_career_list(path):
    text = " ".join(path.read_text().split())
    assert "to approve" in text.lower() and "to think about" in text.lower()
    assert "Big calls come in two kinds" in text
    # What counts as a career skill is written in AGENTS.md only.
    assert "data-science work" not in text and "cost engineering" not in text


def test_a_rules_pull_request_opens_with_the_three_lines_and_the_reviewer_checks_them():
    gate = " ".join(AGENTS_MD.read_text().split("### The rules gate")[1].split("### Pitfalls")[0].split())
    assert "at the very top of the description" in gate and "The author writes those three lines" in gate
    reviewer = " ".join(REVIEWER.read_text().split())
    assert "The three lines to approve, at the very top of the description" in reviewer
    assert "Missing, or not in that form → SENT BACK" in reviewer
    template = (ROOT / ".github" / "pull_request_template.md").read_text()
    assert "**Recommend:**" in template and "**What it is:**" in template and "**Why:**" in template


def test_the_senior_agent_has_a_reply_for_each_kind():
    senior = " ".join((ROOT / ".claude" / "agents" / "senior.md").read_text().split())
    assert "**TO APPROVE:**" in senior and "**TO THINK ABOUT:**" in senior
    assert "**What you would learn:**" in senior
    decider = " ".join((ROOT / ".claude" / "agents" / "decider.md").read_text().split())
    assert "You do not say which" in decider
