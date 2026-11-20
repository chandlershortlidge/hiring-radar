"""File a Linear ticket when the site watch finds a break (HIR-258).

Called by .github/workflows/site-watch.yml and uptime.yml, never by hand in normal use.

Does: read the robot visitor's Playwright report (web/watch-out/report.json), make one
ticket per failing visitor path (both widths in one ticket), with the error, a screenshot
link, the run link and the change that was live. A ticket that is already open under the
same title gets a comment instead of a twin, so a break that lasts a week is one ticket
with seven comments, not seven tickets.

Kinds:
    deploy           the robot failed right after a deploy; the deploy was rolled back
    morning          the robot failed on the daily run; nothing was rolled back
    uptime           the site did not answer the outside check
    rollback-failed  the robot failed after a deploy AND again on the previous version once
                     it was put back. What is filed depends on the second run (HIR-359):
                     when no path passed on the rolled-back site, or its report cannot be
                     read, "Site down and rollback failed" goes straight to Chandler: Urgent,
                     assigned to him, not labelled autopilot. When some path passed, the
                     site is up and the deploy is probably not the cause, so each path that
                     still fails gets the ordinary autopilot ticket, which says so.
    rollback-not-done  the robot failed right after a deploy and the rollback job itself
                     failed, so the site is still on the new version (HIR-317). The ticket
                     says why: `--rollback-problem login` when the server refused the login
                     on every try, otherwise that the job failed before it finished. Goes
                     straight to Chandler like rollback-failed: a version the robot failed
                     is live.

Every other ticket is labelled `autopilot`, so an agent picks it up without him — until
the same break comes back after two fixes (HIR-260). When REPEAT_FIXES tickets with the
same title were closed as done in the last REPEAT_DAYS days, the next one is labelled
`attended` instead: no agent picks it up, nobody is pinged, and the caretaker's Monday
summary lists it for Chandler (app/site_watch_week.py). DECISIONS 2026-11-15.

Does NOT: retry, roll anything back, or touch the site. Without LINEAR_API_KEY it prints
the ticket it would have filed and exits 2, so the workflow run goes red and the text is
in its log.

    python scripts/site_watch_ticket.py --kind deploy --report web/watch-out/report.json \
        --results-root web/watch-out/results --evidence-base https://raw.../site-watch/123 \
        --run-url https://github.com/.../runs/123 --change "abc1234 Merge pull request #150"
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

LINEAR_URL = "https://api.linear.app/graphql"
TEAM_ID = "536d7e60-8726-44aa-9e3a-b273910d72d5"  # Hiring-radar
CHANDLER_ID = "cbb0f6cd-bb63-498d-acb6-f852fd2d86ec"
ERROR_CHARS = 3000
ANSI = re.compile(r"\x1b\[[0-9;]*m")
REPEAT_FIXES = 2   # this many fixes of the same break...
REPEAT_DAYS = 30   # ...inside this many days, and the next ticket is Chandler's, not an agent's

WHAT_HAPPENED = {
    "deploy": "The robot visitor failed right after a deploy. **The deploy was rolled back** to the "
              "last version that passed, so the site is working; this fix is not urgent.",
    "morning": "The robot visitor failed on its morning run, after the day's collection. Nothing was "
               "rolled back: the code did not change, so the cause is likely in the data "
               "(an odd posting, an empty city).",
    "still-failing": "The robot visitor failed right after a deploy. **The deploy was rolled back** to "
                     "the last version that had passed, and this path failed on that version too. Other "
                     "paths passed there, so **the site is up**. A failure on both versions is probably not "
                     "caused by the deploy: look at the data (an empty city, an odd posting), a slow "
                     "server just after its restart, the check itself, or a database change the deploy "
                     "made that a rollback does not undo.",
}


def failures(report: dict) -> list[dict]:
    """One entry per failing visitor path, the widths it failed at merged into one.

    A path that passed on its retry ("flaky") is not a failure: one slow answer from the
    live site is not a break worth a ticket.
    """
    by_title: dict[str, dict] = {}

    def walk(suite):
        for spec in suite.get("specs", []):
            for t in spec.get("tests", []):
                if t.get("status") != "unexpected":
                    continue
                last = (t.get("results") or [{}])[-1]
                # Every error, not just the first: the step that timed out comes first, and the
                # browser's own error (the cause) is often the second.
                err = "\n\n".join(e.get("message", "") for e in last.get("errors", [])) or (
                    last.get("error") or {}).get("message", "")
                shots = [a["path"] for a in last.get("attachments", [])
                         if a.get("contentType") == "image/png" and a.get("path")]
                f = by_title.setdefault(spec["title"], {"test": spec["title"], "projects": [], "error": "", "screenshots": []})
                f["projects"].append(t.get("projectName", "?"))
                f["error"] = f["error"] or ANSI.sub("", err).strip()
                f["screenshots"] += shots
        for s in suite.get("suites", []):
            walk(s)

    for s in report.get("suites", []):
        walk(s)
    return list(by_title.values())


def anything_passed(report: dict) -> bool:
    """Whether any visitor path passed at any width; a pass on the retry counts."""
    def walk(suite) -> bool:
        return (any(t.get("status") in ("expected", "flaky") for spec in suite.get("specs", []) for t in spec.get("tests", []))
                or any(walk(s) for s in suite.get("suites", [])))
    return any(walk(s) for s in report.get("suites", []))


def shot_url(path: str, results_root: str | None, base: str | None) -> str | None:
    if not (results_root and base):
        return None
    try:
        rel = Path(path).resolve().relative_to(Path(results_root).resolve())
    except ValueError:
        return None
    return f"{base.rstrip('/')}/{rel.as_posix()}"


def robot_ticket(kind: str, f: dict, args, first: list[dict] | None = None) -> dict:
    """The ticket for one failing path. `first`, for "still-failing" only: what failed on the
    new version before the rollback, while `f` is from the rolled-back site."""
    widths = " and ".join(f["projects"])
    lines = [WHAT_HAPPENED[kind], "", f"**Failing path:** {f['test']} — at {widths} width."]
    if kind == "still-failing":
        # The error and the widths are the second run's, on the version that was put back.
        lines += [f"**Deploy that was rolled back:** {args.change or 'unknown'}.",
                  f"**Live version, put back by the rollback:** {args.rolled_back_to or 'unknown'}."]
        if first:
            lines += ["", "On the new version, before the rollback, the robot visitor had failed:", ""]
            lines += [f"- {x['test']} ({' and '.join(x['projects'])})" for x in first]
    else:
        lines.append(f"**Live version:** {args.change or 'unknown'}.")
        if kind == "deploy" and args.rolled_back_to:
            lines.append(f"**Rolled back to:** {args.rolled_back_to}.")
    lines += ["", "**Error:**", "```", f["error"][:ERROR_CHARS] or "(no message)", "```"]
    # Only the first run's screenshots are published, so a still-failing ticket links none.
    for p in ([] if kind == "still-failing" else f["screenshots"][:2]):
        url = shot_url(p, args.results_root, args.evidence_base)
        if url:
            lines += ["", f"![screenshot]({url})"]
    lines += ["", f"Run: {args.run_url or 'unknown'}", "",
              "Fix through a normal pull request with a test; the robot visitor confirms the fix "
              "on the live site on its next run (or run the site-watch workflow by hand)."]
    return {"title": f"Site watch: \"{f['test']}\" fails", "body": "\n".join(lines),
            "autopilot": True, "priority": 2, "assignee": None, "stop_after_two_fixes": True}


def uptime_ticket(args) -> dict:
    body = (f"The outside check could not reach the site twice in a row.\n\n"
            f"**What it saw:** {args.detail or 'no answer'}\n\nRun: {args.run_url or 'unknown'}\n\n"
            "If the site is already back, find what stopped it (the VM, the app service, Caddy) "
            "and close this with the cause.")
    return {"title": "Site watch: the site does not answer", "body": body,
            "autopilot": True, "priority": 1, "assignee": None, "stop_after_two_fixes": True,
            # Checked every five minutes: while the ticket is open, more misses add nothing.
            "comment_again": False}


def _paths(fails: list[dict]) -> str:
    return "\n".join(f"- {f['test']} ({' and '.join(f['projects'])}): {f['error'][:300]}" for f in fails) or "- (no report)"


def rollback_failed_ticket(args, fails: list[dict], still: list[dict] | None = None) -> dict:
    """`fails` is the first run, on the new version; `still` the second, on the rolled-back
    site. The ticket says which is which: before HIR-359 it printed the first run's failures
    as what "still fails"."""
    if still:
        after = f"No visitor path passed on the rolled-back site:\n\n{_paths(still)}"
    else:
        after = ("Its report from the rolled-back site could not be read or names no failing path; "
                 "the \"Robot visitor on the rolled-back site\" job in the run below has the cause.")
    # Assigning it to Chandler is what notifies him; an "@name" typed into an API body is
    # plain text, not a mention.
    body = ("The site is broken and the automatic rollback did not fix it.\n\n"
            f"**Deploy that broke it:** {args.change or 'unknown'}\n"
            f"**Rolled back to:** {args.rolled_back_to or 'unknown'}, and the robot visitor still fails. {after}\n\n"
            f"What it found on the new version, before the rollback:\n\n{_paths(fails)}\n\n"
            f"Run: {args.run_url or 'unknown'}")
    return {"title": "Site down and rollback failed", "body": body,
            "autopilot": False, "priority": 1, "assignee": CHANDLER_ID}


ROLLBACK_PROBLEM = {
    "login": "**The rollback could not log in to the server.** The server refused the login on "
             "every try, so nothing was run on it and the old version was not put back.",
    "other": "**The rollback job failed before it finished.** Whether the old version is back is "
             "not known; the \"Roll back to the last good version\" job in the run below says where it stopped.",
}


def rollback_not_done_ticket(args, fails: list[dict]) -> dict:
    """The robot failed after a deploy and the rollback never completed. Not "the site is
    down": the site is on the new version, with whatever the robot found on it."""
    paths = _paths(fails)
    body = ("A deploy failed the robot visitor and the automatic rollback did not run.\n\n"
            f"{ROLLBACK_PROBLEM[args.rollback_problem]}\n\n"
            f"**The site is still on the new version:** {args.change or 'unknown'}\n"
            f"**The rollback would have put back:** {args.rolled_back_to or 'unknown'}\n\n"
            f"What the robot visitor found on the new version (it was not run a second time):\n\n"
            f"{paths}\n\nRun: {args.run_url or 'unknown'}\n\n"
            "Re-running the failed run deploys the same version again and repeats the checks.")
    return {"title": "Deploy failed the robot visitor and the rollback did not run", "body": body,
            "autopilot": False, "priority": 1, "assignee": CHANDLER_ID}


def after_two_fixes(t: dict, fixed: list[str]) -> dict:
    """The ticket for a break that came back after REPEAT_FIXES fixes: the same title (so a
    further failure comments on it), but for Chandler's Monday summary, not for an agent."""
    note = (f"**This has broken again after {len(fixed)} fixes in the last {REPEAT_DAYS} days** "
            f"({', '.join(fixed)}). No agent picks it up this time: it is labelled `attended` "
            "and waits for Chandler in the Monday summary.")
    return {**t, "body": note + "\n\n" + t["body"], "autopilot": False, "label": "attended"}


class Linear:
    def __init__(self, key: str, post=None):
        self.key = key
        self.post = post or self._post

    def _post(self, payload: dict) -> dict:
        req = urllib.request.Request(LINEAR_URL, data=json.dumps(payload).encode(),
                                     headers={"content-type": "application/json", "authorization": self.key})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)

    def q(self, query: str, **variables) -> dict:
        out = self.post({"query": query, "variables": variables})
        if out.get("errors"):
            raise RuntimeError(f"Linear: {out['errors']}")
        return out["data"]

    def open_issue(self, title: str) -> dict | None:
        d = self.q("""query($team: ID!, $title: String!) {
            issues(first: 1, filter: {team: {id: {eq: $team}}, title: {eq: $title},
                   state: {type: {nin: ["completed", "canceled"]}}}) { nodes { id identifier } } }""",
                   team=TEAM_ID, title=title)
        nodes = d["issues"]["nodes"]
        return nodes[0] if nodes else None

    def fixed_recently(self, title: str) -> list[str]:
        """Identifiers of tickets with this exact title closed as done (not cancelled) in
        the last REPEAT_DAYS days, oldest first."""
        d = self.q("""query($team: ID!, $title: String!) {
            issues(first: 20, filter: {team: {id: {eq: $team}}, title: {eq: $title},
                   state: {type: {eq: "completed"}}, completedAt: {gte: "-P%dD"}}) { nodes { identifier completedAt } } }"""
                   % REPEAT_DAYS, team=TEAM_ID, title=title)
        return [n["identifier"] for n in sorted(d["issues"]["nodes"], key=lambda n: n.get("completedAt") or "")]

    def label_id(self, name: str) -> str | None:
        d = self.q("""query($name: String!) { issueLabels(first: 1, filter: {name: {eq: $name}}) { nodes { id } } }""", name=name)
        nodes = d["issueLabels"]["nodes"]
        return nodes[0]["id"] if nodes else None

    def file(self, t: dict) -> str:
        existing = self.open_issue(t["title"])
        if existing and not t.get("comment_again", True):
            return f"already open as {existing['identifier']}; nothing added"
        if existing:
            self.q("""mutation($issue: String!, $body: String!) { commentCreate(input: {issueId: $issue, body: $body}) { success } }""",
                   issue=existing["id"], body="Seen again.\n\n" + t["body"])
            return f"commented on {existing['identifier']}"
        fixed = []
        if t.get("stop_after_two_fixes"):
            try:
                fixed = self.fixed_recently(t["title"])
            except Exception as e:  # noqa: BLE001 - a ticket for an agent beats no ticket at all
                print(f"could not count earlier fixes ({e}); filing as an ordinary ticket", file=sys.stderr)
        if len(fixed) >= REPEAT_FIXES:
            t = after_two_fixes(t, fixed)
        fields = {"teamId": TEAM_ID, "title": t["title"], "description": t["body"], "priority": t["priority"]}
        label = t.get("label") or ("autopilot" if t["autopilot"] else None)
        if label and (lid := self.label_id(label)):
            fields["labelIds"] = [lid]
        if t["assignee"]:
            fields["assigneeId"] = t["assignee"]
        d = self.q("""mutation($input: IssueCreateInput!) { issueCreate(input: $input) { issue { identifier } } }""", input=fields)
        filed = f"filed {d['issueCreate']['issue']['identifier']}"
        if len(fixed) >= REPEAT_FIXES:
            filed += f" for Chandler's Monday summary, not for an agent: broke again after {', '.join(fixed)}"
        return filed


def _read(path: str | None) -> dict:
    """A robot report, or {} when it is missing or not JSON: no report must never mean no ticket."""
    try:
        return json.loads(Path(path).read_text()) if path else {}
    except (OSError, ValueError):
        return {}


def tickets(args) -> list[dict]:
    fails = failures(_read(args.report))
    if args.kind == "uptime":
        return [uptime_ticket(args)]
    if args.kind == "rollback-failed":
        after = _read(args.recheck_report)
        still = failures(after)
        # "Site down" only when nothing passed on the rolled-back site. Any doubt (no report,
        # no failing path named) stays on the urgent side.
        if still and anything_passed(after):
            return [robot_ticket("still-failing", f, args, fails) for f in still]
        return [rollback_failed_ticket(args, fails, still)]
    if args.kind == "rollback-not-done":
        return [rollback_not_done_ticket(args, fails)]
    if not fails:
        # The robot went red without a failing path in its report (it crashed, or never ran):
        # still a ticket, or the red run is the only trace.
        fails = [{"test": "the robot visitor itself", "projects": ["any"], "screenshots": [],
                  "error": f"No failing path in the report ({args.report}); the run log has the cause."}]
    return [robot_ticket(args.kind, f, args) for f in fails]


def main(argv=None, linear=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kind", required=True, choices=["deploy", "morning", "uptime", "rollback-failed", "rollback-not-done"])
    ap.add_argument("--report", help="the robot visitor's report.json")
    ap.add_argument("--recheck-report", help="rollback-failed: the robot visitor's report.json from the rolled-back site")
    ap.add_argument("--results-root", help="the folder the report's screenshot paths sit under")
    ap.add_argument("--evidence-base", help="public URL the results folder was copied to")
    ap.add_argument("--run-url")
    ap.add_argument("--change", help="the version that was live: short sha and subject")
    ap.add_argument("--rolled-back-to", help="the version a rollback put back")
    ap.add_argument("--detail", help="uptime: what the check saw")
    ap.add_argument("--rollback-problem", choices=sorted(ROLLBACK_PROBLEM), default="other",
                    help="rollback-not-done: why the rollback did not run")
    args = ap.parse_args(argv)

    todo = tickets(args)
    key = os.environ.get("LINEAR_API_KEY")
    if not key and linear is None:
        for t in todo:
            print(f"--- would file: {t['title']}\n{t['body']}\n")
        print("LINEAR_API_KEY is not set: no ticket filed.", file=sys.stderr)
        return 2
    linear = linear or Linear(key)
    for t in todo:
        print(f"{t['title']}: {linear.file(t)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
