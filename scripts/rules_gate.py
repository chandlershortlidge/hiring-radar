"""The rules gate: a PR that changes the agents' own rules has to ask Chandler first.

AGENTS.md "The rules gate". Since HIR-136 a reviewed PR merges itself, which would include
a PR that rewrites how review and merging work — so an agent could change its own rules and
the change would land unseen. The reviewer agent is told to stop such a PR, but the reviewer
is one of those rule files, so a change to it could switch the rule off. This script is the
backstop that does not live in the reviewer: it runs in CI, reads the PR's own file list,
and fails when the authorization block is missing.

Usage (from CI, see .github/workflows/rules-gate.yml):

    python3 scripts/rules_gate.py --files-jsonl files.jsonl --body-file body.md
    python3 scripts/rules_gate.py --paths-file changed.txt --body-file body.md   # paths only

Two triggers ask for the same block (HIR-332 added the second):
1. a rule file changed (the list below);
2. a test was removed or switched off: a test file deleted, a test function or `it(...)` /
   `test(...)` removed and not re-added anywhere in the PR (a move or rename is fine), or a
   skip / xfail marker added. Making a failing test pass by removing it is the failure this
   catches. It needs the diff, so it reads GitHub's file list with each file's patch
   (`--files-jsonl`); with `--paths-file` only the rule-file trigger runs.

CI runs the BASE branch's copy of this script (`pull_request_target`, HIR-332), so a PR
that rewrites this file or its workflow is judged by the version it is trying to change.

Exit 0: either the PR touches no rule file, or it carries the block. Exit 1: it touches one
and does not, with a message saying what is missing.

The watched paths (Chandler, 2026-11-04): anything under `.claude/`, `AGENTS.md`,
`.github/pull_request_template.md`, anything under `.github/workflows/` — the agents'
instructions, their skills, the PR form, and the automated checks themselves.

Does NOT: write anywhere, call a model, judge whether the change
is a good one, or decide who may merge. It answers one question — is the block there — so
the trigger is a file list and never a judgment. Pure functions plus a thin file reader;
`matched_paths` and `block_problem` are the whole of it.
"""

import argparse
import json
import re
import sys

# Prefix match for the two directories, exact match for the two files.
RULE_DIRS = (".claude/", ".github/workflows/")
# `scripts/rules_gate.py` is on the list too: it is this gate's own code, and a PR that
# rewrote it to always pass would otherwise walk straight through (HIR-142 decision).
# `scripts/merge_reviewed.py` decides when GitHub merges a reviewed PR with no session
# involved (HIR-262), so loosening it is a change to who merges.
RULE_FILES = (
    "AGENTS.md",
    ".github/pull_request_template.md",
    "scripts/rules_gate.py",
    "scripts/merge_reviewed.py",
)

# The block's fixed wording. The reviewer writes it; this script only looks for it, so the
# words have to be fixed or there would be nothing to look for.
HEADLINE = "Changes were made to .claude/agents/skills:"
QUESTION = "Did you authorize these?"

BLOCK_SHAPE = f"""{HEADLINE}

* <one plain-words line per change>
* <another>

{QUESTION}"""


def is_rule_path(path):
    """Is this one of the agents' own rule files?"""
    # Not lstrip("./"): that would eat the leading dot of `.claude/`.
    p = path.strip()
    if p.startswith("./"):
        p = p[2:]
    if not p:
        return False
    return p in RULE_FILES or p.startswith(RULE_DIRS)


# Test files: Python tests under tests/, web unit tests, and the Playwright specs.
_TEST_PATH = re.compile(r"(^|/)tests/.*\.py$|(^|/)test_[^/]*\.py$|_test\.py$|\.(test|spec)\.[jt]sx?$")
_PY_TEST = re.compile(r"^\s*(?:async\s+)?def\s+(test_\w+)\s*\(")
_JS_TEST = re.compile(r"""^\s*(?:it|test)(?:\.only)?\s*\(\s*(['"`])(.+?)\1""")
_SKIP = re.compile(
    r"pytest\.mark\.(?:skip|skipif|xfail)\b|pytest\.(?:skip|xfail)\s*\("
    r"|unittest\.skip|\b(?:it|test|describe)\.(?:skip|todo)\s*\(|\bx(?:it|describe|test)\s*\("
)


def is_test_path(path):
    """Is this file a test (Python or web)?"""
    return bool(_TEST_PATH.search((path or "").strip()))


def _test_names(line):
    m = _PY_TEST.match(line) or _JS_TEST.match(line)
    if not m:
        return None
    return m.group(1) if m.re is _PY_TEST else m.group(2)


def removed_tests(files):
    """Plain-words findings for tests removed or switched off in a PR; [] when none.

    `files` is GitHub's PR file list (dicts with filename, status, patch, and for renames
    previous_filename). A test name removed in one place and added in another (a move or a
    rename of its file) is not a removal. A test file whose patch GitHub did not send (too
    large) cannot be checked, so it is reported for a person to look at.
    """
    findings = []
    removed, added = {}, set()
    for f in files:
        name = f.get("filename", "")
        if not is_test_path(name) and not is_test_path(f.get("previous_filename", "")):
            continue
        if f.get("status") == "removed":
            findings.append(f"test file deleted: {name}")
            continue
        patch = f.get("patch")
        if patch is None:
            if f.get("status") != "renamed":
                findings.append(f"changes to {name} are too large to read here; check its tests by hand")
            continue
        for line in patch.splitlines():
            if line.startswith(("+++", "---")):
                continue
            if line.startswith("-"):
                t = _test_names(line[1:])
                if t:
                    removed.setdefault(t, name)
            elif line.startswith("+"):
                t = _test_names(line[1:])
                if t:
                    added.add(t)
                if _SKIP.search(line[1:]):
                    findings.append(f"a test is switched off (skip/xfail) in {name}: {line[1:].strip()[:100]}")
    for t, where in sorted(removed.items()):
        if t not in added:
            findings.append(f"test removed: {t} ({where})")
    return findings


def matched_paths(paths):
    """The rule files in a changed-file list, sorted, duplicates dropped."""
    return sorted({p.strip() for p in paths if is_rule_path(p)})


def _lines(body):
    """Body lines, stripped of blockquote markers and surrounding space.

    The block reads as a quote on the Linear ticket and authors paste it either way, so
    `> Did you authorize these?` counts exactly as the bare line does.
    """
    out = []
    for raw in (body or "").splitlines():
        line = raw.strip()
        while line.startswith(">"):
            line = line[1:].strip()
        out.append(line)
    return out


def _is_bullet(line):
    return any(line.startswith(m) for m in ("* ", "- ", "+ ")) and len(line) > 2


def block_problem(body):
    """None when the body carries the block; otherwise what is missing, in plain words.

    Order matters: the headline, then at least one bullet after it, then the question after
    the bullets. A heading with no bullets is not a list of changes, and the question on its
    own is not an answerable one.
    """
    lines = _lines(body)
    lowered = [line.lower() for line in lines]
    try:
        start = lowered.index(HEADLINE.lower())
    except ValueError:
        return f'the line "{HEADLINE}" is not in the PR description'

    bullets = [i for i, line in enumerate(lines[start + 1 :], start + 1) if _is_bullet(line)]
    if not bullets:
        return "no bullet list of the changes follows that line"

    after_last_bullet = lowered[bullets[-1] + 1 :]
    if QUESTION.lower() not in after_last_bullet:
        return f'the line "{QUESTION}" does not follow the bullets'
    return None


def report(paths, body, files=None):
    """(ok, message) for a changed-file list, a PR description, and optionally the diff.

    `files` is GitHub's file list with patches; when given, removed or switched-off tests
    trigger the gate too.
    """
    matched = matched_paths(paths)
    tests = removed_tests(files) if files is not None else []
    if not matched and not tests:
        return True, "No file in this PR changes the agents' own rules or removes a test. Nothing to ask."

    listed = "\n".join([f"  {p}" for p in matched] + [f"  {t}" for t in tests])
    ok = block_problem(body)
    if ok is None:
        return True, (
            "This PR changes the agents' own rules or removes tests, and asks whether that was "
            f"authorized:\n{listed}"
        )

    return False, (
        "This PR changes the agents' own rules or removes or switches off a test, so it "
        "cannot merge on its own.\n\n"
        f"What triggers the gate:\n{listed}\n\n"
        f"What is missing: {ok}.\n\n"
        "The reviewer agent adds this block to the PR description (AGENTS.md "
        '"The rules gate") — the agent that made the change does not write it:\n\n'
        f"{BLOCK_SHAPE}\n\n"
        "One bullet per change, in plain words. Chandler answers by merging, or by "
        "sending it back."
    )


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--paths-file", help="file holding one changed path per line (rule files only)")
    src.add_argument("--files-jsonl", help="GitHub's PR file list, one JSON object per line, with patches")
    ap.add_argument("--body-file", required=True, help="file holding the PR description")
    args = ap.parse_args(argv)

    files = None
    if args.files_jsonl:
        with open(args.files_jsonl, encoding="utf-8") as fh:
            files = [json.loads(line) for line in fh if line.strip()]
        paths = [f.get("filename", "") for f in files]
    else:
        with open(args.paths_file, encoding="utf-8") as fh:
            paths = fh.read().splitlines()
    with open(args.body_file, encoding="utf-8") as fh:
        body = fh.read()

    ok, message = report(paths, body, files)
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
