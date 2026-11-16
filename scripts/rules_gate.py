"""The rules gate: a PR that changes the agents' own rules has to ask Chandler first.

AGENTS.md "The rules gate". Since HIR-136 a reviewed PR merges itself, which would include
a PR that rewrites how review and merging work — so an agent could change its own rules and
the change would land unseen. The reviewer agent is told to stop such a PR, but the reviewer
is one of those rule files, so a change to it could switch the rule off. This script is the
backstop that does not live in the reviewer: it runs in CI, reads the PR's own file list,
and fails when the authorization block is missing.

Usage (from CI, see .github/workflows/rules-gate.yml):

    python3 scripts/rules_gate.py --paths-file changed.txt --body-file body.md

Exit 0: either the PR touches no rule file, or it carries the block. Exit 1: it touches one
and does not, with a message saying what is missing.

The watched paths (Chandler, 2026-11-04): anything under `.claude/`, `AGENTS.md`,
`.github/pull_request_template.md`, anything under `.github/workflows/` — the agents'
instructions, their skills, the PR form, and the automated checks themselves.

Does NOT: read the diff's contents, write anywhere, call a model, judge whether the change
is a good one, or decide who may merge. It answers one question — is the block there — so
the trigger is a file list and never a judgment. Pure functions plus a thin file reader;
`matched_paths` and `block_problem` are the whole of it.
"""

import argparse
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


def report(paths, body):
    """(ok, message) for a changed-file list and a PR description."""
    matched = matched_paths(paths)
    if not matched:
        return True, "No file in this PR changes the agents' own rules. Nothing to ask."

    listed = "\n".join(f"  {p}" for p in matched)
    ok = block_problem(body)
    if ok is None:
        return True, (
            "This PR changes the agents' own rules and asks whether that was "
            f"authorized:\n{listed}"
        )

    return False, (
        "This PR changes the agents' own rules, so it cannot merge on its own.\n\n"
        f"Files that trigger the gate:\n{listed}\n\n"
        f"What is missing: {ok}.\n\n"
        "The reviewer agent adds this block to the PR description (AGENTS.md "
        '"The rules gate") — the agent that made the change does not write it:\n\n'
        f"{BLOCK_SHAPE}\n\n"
        "One bullet per change, in plain words. Chandler answers by merging, or by "
        "sending it back."
    )


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--paths-file", required=True, help="file holding one changed path per line")
    ap.add_argument("--body-file", required=True, help="file holding the PR description")
    args = ap.parse_args(argv)

    with open(args.paths_file, encoding="utf-8") as fh:
        paths = fh.read().splitlines()
    with open(args.body_file, encoding="utf-8") as fh:
        body = fh.read()

    ok, message = report(paths, body)
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
