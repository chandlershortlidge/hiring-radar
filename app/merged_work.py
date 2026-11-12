"""The pull-request half of the Monday summary (HIR-264): what needs Chandler, what merged
last week, and what the reviewer sent back that was then fixed and merged.

Does:
  - read this repository's pull requests from GitHub's public API (no token: the repo is
    public), two or three requests a week;
  - read which files each merged change touched from the server's own checkout with git,
    so the hourly limit on unsigned API requests is never a concern;
  - sort each merged change into one group by those files — the chart, the job list, the
    cities, elsewhere on the site, or nothing a visitor would see;
  - write the three sections as Markdown, for app/caretaker_run.py to put in the one
    Monday post next to the job-source report.

Does NOT: post anything, write to GitHub, label or merge a pull request, call a model, or
decide what Chandler is asked (AGENTS.md "What Chandler is asked"). It reports labels that
the reviewer set; it never sets one.

Invariants:
  - "Needs you" is every *open* pull request labelled `needs-chandler`, whether or not it
    ever @mentioned him. That label is the whole test.
  - A merged change appears in exactly one group. A change whose files could not be read is
    listed as unsorted, never dropped and never guessed.
  - If GitHub cannot be read, `week_text` says so in plain words instead of raising: the
    job-source report must still go out.

The sorting is a guess from file paths, not a judgment about the change: DECISIONS
2026-11-12 (HIR-264).
"""

import json
import re
import subprocess
import urllib.request
from pathlib import Path

REPO = "chandlershortlidge/hiring-radar"
API = f"https://api.github.com/repos/{REPO}"
ROOT = Path(__file__).resolve().parent.parent
NEEDS = "needs-chandler"
SENT_BACK = "sent-back"
MAX_PAGES = 10          # 1,000 closed pull requests back; a week is far fewer

# Where a visitor would notice a change, first match wins, in this order. Each entry is
# (heading, path prefixes). A change touching none of them is "nothing a visitor would see".
GROUPS = (
    ("On the chart", (
        "web/src/SkillChart", "web/src/CompareChart", "web/src/SkillTree", "web/src/RelatedSkills",
        "app/skill_tree.py", "taxonomy/skills.json")),
    ("In the job list", (
        "web/src/JobList", "web/src/JobPage", "web/src/AddJobDrawer", "web/src/QueryBar",
        "app/ingest.py", "app/dedup.py", "app/add.py", "app/sources/")),
    ("Cities", ("web/src/CityPicker", "app/geo.py", "config/feeds.json", "config/discover.json")),
    ("Elsewhere on the site", ("web/src/",)),
)
UNSEEN = "Nothing a visitor would see"
UNSORTED = "Not sorted (the server could not read which files these changed)"


# --- pure --------------------------------------------------------------------------------

def group_of(files: list[str] | None) -> str:
    """The one group a merged change is listed under. Test files never decide it."""
    if files is None:
        return UNSORTED
    real = [f for f in files if ".test." not in f and not f.startswith("tests/")]
    for heading, prefixes in GROUPS:
        if any(f.startswith(prefixes) for f in real):
            return heading
    return UNSEEN


def plain_title(title: str) -> str:
    """A pull request's title without its ticket prefix: 'HIR-263: the button…' → 'The button…'."""
    t = re.sub(r"^\s*HIR-\d+\s*[:\-–]\s*", "", title, flags=re.I).strip() or title.strip()
    return t[:1].upper() + t[1:]


def labels(pr: dict) -> set[str]:
    return {label["name"] for label in pr.get("labels") or []}


def merged_in(prs: list[dict], start: str, end: str) -> list[dict]:
    """Pull requests merged from `start` to `end` (UTC days, inclusive), oldest first."""
    hit = [p for p in prs if p.get("merged_at") and start <= p["merged_at"][:10] <= end]
    return sorted(hit, key=lambda p: p["merged_at"])


def question(body: str | None) -> str:
    """The first line under the pull request's "Needs Chandler" heading, when it is a real
    question; '' when the section is absent, empty or says "None"."""
    m = re.search(r"^##\s*Needs Chandler\s*$(.*?)(?=^##\s|\Z)", body or "", flags=re.M | re.S | re.I)
    if not m:
        return ""
    text = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S)
    for line in text.splitlines():
        line = line.strip().lstrip("-*> ").strip()
        if line:
            return "" if line.lower().startswith("none") else line[:300]
    return ""


def _link(pr: dict) -> str:
    return f"[{plain_title(pr['title'])}]({pr['html_url']})"


def needs_lines(waiting: list[dict]) -> list[str]:
    out = []
    for pr in sorted(waiting, key=lambda p: p["created_at"]):
        line = f"- {_link(pr)}, waiting since {pr['created_at'][:10]}."
        if (q := question(pr.get("body"))):
            line += f" {q}"
        out.append(line)
    return out


def sections(merged: list[dict], waiting: list[dict], start: str, end: str) -> str:
    """Markdown for the three parts. `merged` items carry `files` (a list, or None when
    they could not be read); `waiting` are the open pull requests labelled needs-chandler."""
    lines = ["# Needs you", ""]
    if waiting:
        n = len(waiting)
        lines += [f"{n} pull request{'s' if n != 1 else ''} will not merge until you decide:", ""]
        lines += needs_lines(waiting)
    else:
        lines.append("Nothing is waiting for you.")
    lines += ["", f"# What merged, {start} to {end}", ""]
    if not merged:
        lines.append("Nothing merged.")
    else:
        n = len(merged)
        lines += [f"{n} change{'s' if n != 1 else ''} merged, grouped by where a visitor would notice.", ""]
        by_group: dict[str, list[dict]] = {}
        for pr in merged:
            by_group.setdefault(group_of(pr.get("files")), []).append(pr)
        for heading in [g[0] for g in GROUPS] + [UNSEEN, UNSORTED]:
            if heading in by_group:
                lines += [f"## {heading}", ""] + [f"- {_link(p)}" for p in by_group[heading]] + [""]
    fixed = [p for p in merged if SENT_BACK in labels(p)]
    lines += ["", "# Sent back and fixed", ""]
    if fixed:
        lines += ["The reviewer sent these back to their author; they were fixed and then merged:", ""]
        lines += [f"- {_link(p)}" for p in fixed]
    else:
        lines.append("Nothing was sent back.")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).rstrip() + "\n"


# --- reading GitHub and the checkout ------------------------------------------------------

def get_json(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "weekly-summary"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def git_files(sha: str, repo_dir: Path = ROOT) -> list[str] | None:
    """Files a merge changed, read from the local checkout: the merge commit against the
    main branch just before it. None when this checkout does not have the commit."""
    try:
        out = subprocess.run(["git", "-C", str(repo_dir), "diff", "--name-only", f"{sha}^1", sha],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.split("\n")[:-1] if out.returncode == 0 else None


def git_refresh(repo_dir: Path = ROOT) -> None:
    """Bring the checkout's copy of main's history up to date, so a merge made since the
    last deploy can be read. Touches no file in the working tree; a failure is ignored,
    and the changes it would have covered are then listed as unsorted."""
    try:
        subprocess.run(["git", "-C", str(repo_dir), "fetch", "--quiet", "origin", "main"],
                       capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        pass


def fetch(start: str, end: str, get=get_json, files_of=git_files,
          refresh=git_refresh) -> tuple[list[dict], list[dict]]:
    """(merged last week with their files, open and waiting for Chandler). Closed pull
    requests are read newest-updated first and reading stops at the first one last touched
    before `start`: a pull request is always touched when it merges."""
    closed: list[dict] = []
    for page in range(1, MAX_PAGES + 1):
        batch = get(f"{API}/pulls?state=closed&sort=updated&direction=desc&per_page=100&page={page}")
        closed += batch
        if len(batch) < 100 or batch[-1]["updated_at"][:10] < start:
            break
    merged = merged_in(closed, start, end)
    if merged:
        refresh()
    for pr in merged:
        pr["files"] = files_of(pr["merge_commit_sha"]) if pr.get("merge_commit_sha") else None
    opened = get(f"{API}/pulls?state=open&per_page=100")
    return merged, [p for p in opened if NEEDS in labels(p)]


def week_text(start: str, end: str, get=get_json, files_of=git_files, refresh=git_refresh) -> str:
    """The three sections, or one plain paragraph saying GitHub could not be read."""
    try:
        merged, waiting = fetch(start, end, get, files_of, refresh)
    except Exception as e:  # noqa: BLE001 - any failure here must not stop the Monday post
        return ("# Needs you\n\nGitHub could not be read this morning "
                f"({type(e).__name__}: {str(e)[:120]}), so this week's summary has no list of what "
                f"merged and no list of what is waiting for you. The pull requests labelled "
                f"`{NEEDS}` are the list: https://github.com/{REPO}/pulls?q=is%3Aopen+label%3A{NEEDS}\n")
    return sections(merged, waiting, start, end)
