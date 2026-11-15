"""The robot visitor's part of the Monday summary (HIR-260): what broke on the live site
last week, what was rolled back, what was fixed, and what broke again after two fixes.

Does:
  - read the robot visitor's own tickets from Linear (scripts/site_watch_ticket.py files
    them; HIR-258), one read-only request a week with the key the caretaker posts with;
  - write two pieces of Markdown for app/caretaker_run.py: a short "needs you" block that
    goes at the very top of the Monday post, and the week's report that goes after the
    pull requests.

Does NOT: file, label, close or comment on a ticket, decide what counts as "after two
fixes" (the ticket script does, and marks such a ticket `attended`), touch the site, or
call a model.

Invariants:
  - Only the robot's tickets are read: the fixed titles the ticket script writes. Any other
    ticket whose title happens to start with "Site watch" (HIR-258 itself) is ignored.
  - "Needs you" is every *open* robot ticket labelled `attended`, plus an open "site down
    and rollback failed". The label is the whole test; this module never recounts fixes.
  - "Rolled back" is read from the sentence the ticket script puts in a deploy ticket
    (ROLLED_BACK); tests/test_site_watch_week.py fails if that wording drifts.
  - If Linear cannot be read, or there is no key, `week_text` says so in one line instead
    of raising: the rest of the Monday post must still go out.

DECISIONS 2026-11-15 (HIR-260).
"""

import re

LINEAR_URL = "https://api.linear.app/graphql"
PATH_TITLE = re.compile(r'^Site watch: "(.*)" fails$')
UPTIME_TITLE = "Site watch: the site does not answer"
DOWN_TITLE = "Site down and rollback failed"
ROLLED_BACK = "The deploy was rolled back"     # scripts/site_watch_ticket.py, WHAT_HAPPENED["deploy"]
ATTENDED = "attended"
HEADING = "# The robot visitor"


# --- pure --------------------------------------------------------------------------------

def is_robot_ticket(title: str) -> bool:
    return bool(PATH_TITLE.match(title)) or title in (UPTIME_TITLE, DOWN_TITLE)


def what(title: str) -> str:
    """What a visitor would have seen, from the ticket's title."""
    if title == UPTIME_TITLE:
        return "The site did not answer"
    if title == DOWN_TITLE:
        return "The site went down and the automatic rollback did not fix it"
    name = PATH_TITLE.match(title).group(1)
    if name == "the robot visitor itself":
        return "The robot visitor itself could not finish its run"
    return f'"{name}" stopped working'


def is_open(i: dict) -> bool:
    return not (i.get("completed") or i.get("canceled"))


def _ref(i: dict) -> str:
    return f"[{i['id']}]({i['url']})" if i.get("url") else i["id"]


def _day(stamp: str) -> str:
    return stamp[:10]


def how(i: dict) -> str:
    """The second half of a "what broke" line: how it was found and what was done at once."""
    if i["title"] == DOWN_TITLE:
        return "this went to you at once"
    if i["title"] == UPTIME_TITLE:
        return "found by the outside check that runs every five minutes"
    if ROLLED_BACK in (i.get("description") or ""):
        return "right after a change went live; the change was rolled back, so the site kept working"
    return "found on the morning check; nothing was rolled back, because no change had just gone live"


def needs_you(issues: list[dict]) -> str:
    """The block for the top of the Monday post, or "" when nothing waits for Chandler."""
    waiting = [i for i in issues if is_open(i) and (ATTENDED in i["labels"] or i["title"] == DOWN_TITLE)]
    if not waiting:
        return ""
    lines = ["# The live site: needs you", ""]
    for i in sorted(waiting, key=lambda i: i["created"]):
        if i["title"] == DOWN_TITLE:
            lines.append(f"- {what(i['title'])}. Open since {_day(i['created'])}: {_ref(i)}.")
        else:
            lines.append(f"- {what(i['title'])} again after two fixes in 30 days, so no agent is "
                         f"working on it. Open since {_day(i['created'])}: {_ref(i)}.")
    return "\n".join(lines) + "\n"


def report(issues: list[dict], start: str, end: str) -> str:
    """What broke, what was fixed and what is still open, for `start`..`end` (dates)."""
    in_week = lambda stamp: bool(stamp) and start <= _day(stamp) <= end  # noqa: E731
    broke = sorted((i for i in issues if in_week(i["created"])), key=lambda i: i["created"])
    fixed = sorted((i for i in issues if in_week(i.get("completed"))), key=lambda i: i["completed"])
    still = sorted((i for i in issues if is_open(i)), key=lambda i: i["created"])
    if not (broke or fixed or still):
        return f"{HEADING}\n\nNothing broke on the live site all week.\n"
    lines = [HEADING, ""]
    if broke:
        lines += ["## What broke", ""]
        lines += [f"- {_day(i['created'])}: {what(i['title'])}, {how(i)} ({_ref(i)})." for i in broke]
        lines.append("")
    if fixed:
        lines += ["## What was fixed", ""]
        for i in fixed:
            again = [j for j in issues if j["title"] == i["title"] and j["created"] > i["completed"]]
            tail = (f"it broke again on {_day(min(j['created'] for j in again))}" if again
                    else "the robot visitor has not seen it break since")
            lines.append(f"- {_day(i['completed'])}: the fix for {_ref(i)} went in "
                         f"({what(i['title'])} on {_day(i['created'])}); {tail}.")
        lines.append("")
    if still:
        lines += ["## Still open", ""]
        for i in still:
            who = ("waiting for you" if ATTENDED in i["labels"] or i["title"] == DOWN_TITLE
                   else "for an agent to fix")
            lines.append(f"- {what(i['title'])}, open since {_day(i['created'])}, {who} ({_ref(i)}).")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# --- reading Linear ----------------------------------------------------------------------

def fetch(start: str, key: str, team_id: str, post_json) -> list[dict]:
    """The robot's tickets touched since `start` (a date) or still open. One request.
    post_json(url, payload, headers) is injected so tests never reach Linear."""
    q = ("""query($team: ID!) { issues(first: 250, filter: {team: {id: {eq: $team}}, title: {startsWith: "Site "},
             or: [{updatedAt: {gte: "%sT00:00:00.000Z"}}, {state: {type: {nin: ["completed", "canceled"]}}}]})
             { nodes { identifier title description url createdAt completedAt canceledAt
                       labels { nodes { name } } } } }""" % start)
    r = post_json(LINEAR_URL, {"query": q, "variables": {"team": team_id}},
                  {"Authorization": key, "Content-Type": "application/json"})
    if r.get("errors") or "data" not in r:
        raise RuntimeError(f"Linear: {str(r.get('errors') or r)[:200]}")
    return [{"id": n["identifier"], "title": n["title"], "description": n.get("description") or "",
             "url": n.get("url"), "created": n["createdAt"], "completed": n.get("completedAt"),
             "canceled": n.get("canceledAt"),
             "labels": [x["name"] for x in (n.get("labels") or {}).get("nodes", [])]}
            for n in r["data"]["issues"]["nodes"] if is_robot_ticket(n["title"])]


def week_text(start: str, end: str, key: str | None, team_id: str, post_json) -> tuple[str, str]:
    """(the "needs you" block for the top of the post or "", the week's report). Never
    raises: a Monday without Linear still gets its post."""
    if not key:
        return "", f"{HEADING}\n\nNot read: there is no Linear key on the server.\n"
    try:
        issues = fetch(start, key, team_id, post_json)
    except Exception as e:  # noqa: BLE001 - any failure here must not stop the Monday post
        return "", (f"{HEADING}\n\nLinear could not be read this morning ({type(e).__name__}: "
                    f"{str(e)[:120]}), so this week has no list of what broke on the live site. "
                    "The robot visitor's tickets all start with \"Site watch\".\n")
    return needs_you(issues), report(issues, start, end)
