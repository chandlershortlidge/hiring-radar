"""collision: which collided files a repair may keep both sides of (HIR-305).

The rule under test is the ticket's: where both sides only added text to a log or a list,
keep both; where the same code was changed on both sides, do not guess. The pure part is
tested on merge text; the rest on real merges in a throwaway git repository.
"""

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("collision", ROOT / "scripts" / "collision.py")
co = importlib.util.module_from_spec(spec)
spec.loader.exec_module(co)


def block(ours, base, theirs):
    return (f"{co.OURS} ours\n{ours}{co.BASE} base\n{base}{co.SEP}\n{theirs}{co.THEIRS} theirs\n")


# --- pure --------------------------------------------------------------------------------

def test_two_additions_at_one_place_are_both_kept_branch_first():
    text, add_only = co.keep_both("# Log\n" + block("entry A\n", "", "entry B\n") + "old entry\n")
    assert add_only
    assert text == "# Log\nentry A\nentry B\nold entry\n"


def test_a_line_changed_on_both_sides_is_not_add_only():
    assert co.keep_both(block("x = 2\n", "x = 1\n", "x = 3\n"))[1] is False


def test_one_changed_collision_spoils_a_file_with_an_add_only_one():
    merged = block("A\n", "", "B\n") + "middle\n" + block("x = 2\n", "x = 1\n", "x = 3\n")
    assert co.keep_both(merged)[1] is False


def test_text_without_a_collision_comes_back_unchanged():
    assert co.keep_both("a\nb\n") == ("a\nb\n", True)


def test_ordinary_seven_character_markers_in_the_text_are_not_read_as_a_collision():
    prose = "Heading\n=======\n<<<<<<< not a marker\n"
    assert co.keep_both(prose) == (prose, True)


def test_a_collision_that_never_closes_is_not_add_only():
    assert co.keep_both(f"{co.OURS} ours\nA\n{co.SEP}\nB\n")[1] is False


ADD_ONLY = block("A\n", "", "B\n")


@pytest.mark.parametrize("path, stages, merged, what", [
    ("DECISIONS.md", {1: "a", 2: "b", 3: "c"}, ADD_ONLY, "keep"),
    ("docs/list.txt", {1: "a", 2: "b", 3: "c"}, ADD_ONLY, "keep"),
    # both sides only added, but it is code or data: two additions can break each other
    ("app/queries.py", {1: "a", 2: "b", 3: "c"}, ADD_ONLY, "senior"),
    ("config/feeds.json", {1: "a", 2: "b", 3: "c"}, ADD_ONLY, "senior"),
    # the same lines changed on both sides, prose or not
    ("AGENTS.md", {1: "a", 2: "b", 3: "c"}, block("new\n", "old\n", "other\n"), "senior"),
    # one side deleted the file; both sides created it; git cannot merge it as text
    ("notes.md", {1: "a", 3: "c"}, None, "senior"),
    ("notes.md", {2: "b", 3: "c"}, None, "senior"),
    ("logo.md", {1: "a", 2: "b", 3: "c"}, None, "senior"),
])
def test_only_add_only_prose_is_kept_everything_else_goes_to_the_senior_agent(path, stages, merged, what):
    got, why = co.verdict(path, stages, merged)
    assert got == what
    assert bool(why) == (what == "senior")


# --- on a real merge ---------------------------------------------------------------------

def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


@pytest.fixture
def collided(tmp_path):
    """A repository where `main` and a branch each added a log entry at the top of log.md,
    each added a function at the end of code.py, and each changed the same line of
    rule.md; the branch is mid-merge with main."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    git(repo, "config", "commit.gpgsign", "false")
    (repo / "log.md").write_text("# Log\n\n## old entry\n\ntext\n")
    (repo / "code.py").write_text("def a():\n    return 1\n")
    (repo / "rule.md").write_text("The limit is 5.\n")
    (repo / "clean.md").write_text("one\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")

    def change(who, limit):
        (repo / "log.md").write_text(f"# Log\n\n## entry from {who}\n\n{who} text\n\n## old entry\n\ntext\n")
        (repo / "code.py").write_text(f"def a():\n    return 1\n\n\ndef {who}():\n    return 2\n")
        (repo / "rule.md").write_text(f"The limit is {limit}.\n")
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", who)

    git(repo, "switch", "-q", "-c", "ticket")
    change("branch", 7)
    (repo / "clean.md").write_text("one\ntwo\n")  # changed on one side only: merges by itself
    git(repo, "commit", "-q", "-am", "clean")
    git(repo, "switch", "-q", "main")
    change("main", 9)
    git(repo, "switch", "-q", "ticket")
    merge = subprocess.run(["git", "merge", "main"], cwd=repo, capture_output=True)
    assert merge.returncode != 0  # it collided
    return repo


def test_the_log_keeps_both_entries_and_the_code_and_the_rule_are_left_for_the_senior_agent(collided):
    before = {name: (collided / name).read_text() for name in ("code.py", "rule.md")}
    answer = co.repair(apply=True, cwd=collided)

    assert answer["kept_both"] == ["log.md"]
    assert [item["path"] for item in answer["for_senior"]] == ["code.py", "rule.md"]
    log = (collided / "log.md").read_text()
    assert log == ("# Log\n\n## entry from branch\n\nbranch text\n\n"
                   "## entry from main\n\nmain text\n\n## old entry\n\ntext\n")
    # the two it may not judge are exactly as git left them, and still unmerged
    assert {name: (collided / name).read_text() for name in before} == before
    assert git(collided, "diff", "--name-only", "--diff-filter=U").split() == ["code.py", "rule.md"]


def test_without_apply_nothing_is_written(collided):
    before = (collided / "log.md").read_text()
    answer = co.repair(apply=False, cwd=collided)
    assert answer["kept_both"] == ["log.md"]
    assert (collided / "log.md").read_text() == before
    assert "log.md" in git(collided, "diff", "--name-only", "--diff-filter=U").split()


def test_the_command_fails_while_a_file_is_left_for_the_senior_agent(collided, monkeypatch, capsys):
    monkeypatch.chdir(collided)
    assert co.main(["--apply"]) == 1
    assert '"for_senior"' in capsys.readouterr().out
    # once those are settled by hand, nothing is left and it passes
    for name in ("code.py", "rule.md"):
        git(collided, "checkout", "--ours", "--", name)
        git(collided, "add", "--", name)
    assert co.main([]) == 0


def test_a_file_one_side_deleted_is_left_alone(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    git(repo, "config", "commit.gpgsign", "false")
    (repo / "notes.md").write_text("one\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "switch", "-q", "-c", "ticket")
    (repo / "notes.md").write_text("one\ntwo\n")
    git(repo, "commit", "-q", "-am", "edit")
    git(repo, "switch", "-q", "main")
    git(repo, "rm", "-q", "notes.md")
    git(repo, "commit", "-q", "-m", "delete")
    git(repo, "switch", "-q", "ticket")
    subprocess.run(["git", "merge", "main"], cwd=repo, capture_output=True)

    answer = co.repair(apply=True, cwd=repo)
    assert answer["kept_both"] == []
    assert answer["for_senior"][0]["path"] == "notes.md"
    assert (repo / "notes.md").read_text() == "one\ntwo\n"
