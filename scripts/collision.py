"""Which collided files may be repaired by keeping both sides, and which may not (HIR-305).

Run in a checkout where `git merge origin/main` has stopped on conflicts. For every
collided file it answers one of two things:

- **kept both**: both sides only *added* text, at the same place, in a prose file (a log
  or a list in a `.md`, `.txt` or `.rst` file). Neither side changed or removed a line
  the other touched, so nothing is lost by keeping both additions. With `--apply` the file
  is rewritten that way (the branch's addition first, then main's) and staged.
- **for the senior agent**: everything else. The same lines changed on both sides; a file
  one side deleted or both sides created; a file git cannot merge as text; and any
  collision in a code or data file, even one where both sides only added lines. Two
  additions to code at one place can each be right and still break each other, and
  telling which is a judgment, not a rule. Such a file is never touched here.

A worker repairing a collided pull request (`/work-issue` "Repairing a collided pull
request") runs this instead of deciding by eye, so "do not guess" is code.

Does NOT: start or finish a merge, commit, choose between two versions, edit a file it
lists for the senior agent, run tests, or talk to GitHub or Linear. It reads git's own
three versions of each file (the common ancestor, the branch's, main's), never the
conflict markers git wrote into the working file, so text that happens to look like a
marker cannot mislead it.

Invariants:
  - a file is rewritten only when every one of its collisions is add-only and it is
    prose; one collision of the other kind sends the whole file to the senior agent;
  - without `--apply` nothing is written;
  - exit status 0 only when no file is left for the senior agent.

    python scripts/collision.py            # say what would happen
    python scripts/collision.py --apply    # keep both where that is safe, list the rest
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PROSE = (".md", ".txt", ".rst")
# Longer than any run of the same character a real file is likely to start a line with.
MARKER = 31
OURS, BASE, SEP, THEIRS = ("<" * MARKER, "|" * MARKER, "=" * MARKER, ">" * MARKER)


# --- pure --------------------------------------------------------------------------------

def is_prose(path: str) -> bool:
    return path.lower().endswith(PROSE)


def keep_both(merged: str) -> tuple[str, bool]:
    """`merged` is a three-way merge written with both sides and their common ancestor
    between markers of length MARKER. Returns the text with each collision replaced by the
    first side's lines followed by the second's, and whether every collision was add-only:
    its ancestor part empty, so neither side changed or removed anything there.

    When the second value is False the first must not be used."""
    out, add_only = [], True
    part, sides = None, {}
    for line in merged.splitlines(keepends=True):
        mark = line.split(" ")[0].rstrip("\n")
        if part is None and mark == OURS:
            part, sides = "ours", {"ours": [], "base": [], "theirs": []}
        elif part == "ours" and mark == BASE:
            part = "base"
        elif part in ("ours", "base") and mark == SEP:
            part = "theirs"
        elif part == "theirs" and mark == THEIRS:
            if sides["base"] or not sides["ours"] or not sides["theirs"]:
                add_only = False
            out += sides["ours"] + sides["theirs"]
            part = None
        elif part is None:
            out.append(line)
        else:
            sides[part].append(line)
    if part is not None:  # a collision that never closed: not something to rewrite
        add_only = False
    return "".join(out), add_only


def verdict(path: str, stages: dict, merged: str | None) -> tuple[str, str]:
    """("keep", "") or ("senior", why) for one collided file. `stages` is which of git's
    three versions exist (1 the ancestor, 2 the branch's, 3 main's); `merged` is the
    three-way merge text, or None when git could not merge the file as text."""
    if set(stages) != {1, 2, 3}:
        return "senior", "one side deleted this file, or both sides created it"
    if merged is None:
        return "senior", "git cannot merge this file as text"
    if not keep_both(merged)[1]:
        return "senior", "both sides changed the same lines"
    if not is_prose(path):
        return "senior", "both sides added lines at the same place in a code or data file"
    return "keep", ""


# --- git ---------------------------------------------------------------------------------

def _git(*args, cwd=None, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True)


def unmerged(cwd=None) -> dict:
    """{path: {stage: blob id}} for every file the merge stopped on."""
    files = {}
    for entry in _git("ls-files", "-u", "-z", cwd=cwd).stdout.decode().split("\0"):
        if entry:
            meta, path = entry.split("\t", 1)
            _, blob, stage = meta.split()
            files.setdefault(path, {})[int(stage)] = blob
    return files


def three_way(stages: dict, cwd=None) -> str | None:
    """Git's own merge of the three versions, with long markers and the ancestor shown."""
    with tempfile.TemporaryDirectory() as tmp:
        names = {}
        for stage in (1, 2, 3):
            names[stage] = Path(tmp) / str(stage)
            names[stage].write_bytes(_git("cat-file", "blob", stages[stage], cwd=cwd).stdout)
        done = _git("merge-file", "-p", "--diff3", f"--marker-size={MARKER}",
                    str(names[2]), str(names[1]), str(names[3]), cwd=cwd, check=False)
    if done.returncode < 0 or done.returncode > 127:  # an error, not a count of collisions
        return None
    try:
        return done.stdout.decode()
    except UnicodeDecodeError:
        return None


def repair(apply: bool, cwd=None) -> dict:
    root = Path(_git("rev-parse", "--show-toplevel", cwd=cwd).stdout.decode().strip())
    answer = {"kept_both": [], "for_senior": []}
    for path, stages in sorted(unmerged(cwd).items()):
        merged = three_way(stages, cwd) if set(stages) == {1, 2, 3} else None
        what, why = verdict(path, stages, merged)
        if what == "senior":
            answer["for_senior"].append({"path": path, "why": why})
            continue
        if apply:
            (root / path).write_text(keep_both(merged)[0])
            _git("add", "--", path, cwd=root)
        answer["kept_both"].append(path)
    return answer


def main(argv=None):
    parser = argparse.ArgumentParser(description="Keep both sides of add-only collisions in prose; list the rest.")
    parser.add_argument("--apply", action="store_true", help="rewrite and stage the files that are safe to keep both in")
    args = parser.parse_args(argv)
    answer = repair(args.apply)
    print(json.dumps(answer, indent=2, ensure_ascii=False))
    return 1 if answer["for_senior"] else 0


if __name__ == "__main__":
    sys.exit(main())
