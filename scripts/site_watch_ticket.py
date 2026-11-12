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
    rollback-failed  a deploy broke the site AND putting the previous version back did not
                     fix it. The one kind that goes straight to Chandler: Urgent, assigned
                     to him, and not labelled autopilot.

Every other ticket is labelled `autopilot`, so an agent picks it up without him.

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

WHAT_HAPPENED = {
    "deploy": "The robot visitor failed right after a deploy. **The deploy was rolled back** to the "
              "last version that passed, so the site is working; this fix is not urgent.",
    "morning": "The robot visitor failed on its morning run, after the day's collection. Nothing was "
               "rolled back: the code did not change, so the cause is likely in the data "
               "(an odd posting, an empty city).",
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


def shot_url(path: str, results_root: str | None, base: str | None) -> str | None:
    if not (results_root and base):
        return None
    try:
        rel = Path(path).resolve().relative_to(Path(results_root).resolve())
    except ValueError:
        return None
    return f"{base.rstrip('/')}/{rel.as_posix()}"


def robot_ticket(kind: str, f: dict, args) -> dict:
    widths = " and ".join(f["projects"])
    lines = [WHAT_HAPPENED[kind], "",
             f"**Failing path:** {f['test']} — at {widths} width.",
             f"**Live version:** {args.change or 'unknown'}."]
    if kind == "deploy" and args.rolled_back_to:
        lines.append(f"**Rolled back to:** {args.rolled_back_to}.")
    lines += ["", "**Error:**", "```", f["error"][:ERROR_CHARS] or "(no message)", "```"]
    for p in f["screenshots"][:2]:
        url = shot_url(p, args.results_root, args.evidence_base)
        if url:
            lines += ["", f"![screenshot]({url})"]
    lines += ["", f"Run: {args.run_url or 'unknown'}", "",
              "Fix through a normal pull request with a test; the robot visitor confirms the fix "
              "on the live site on its next run (or run the site-watch workflow by hand)."]
    return {"title": f"Site watch: \"{f['test']}\" fails", "body": "\n".join(lines),
            "autopilot": True, "priority": 2, "assignee": None}


def uptime_ticket(args) -> dict:
    body = (f"The outside check could not reach the site twice in a row.\n\n"
            f"**What it saw:** {args.detail or 'no answer'}\n\nRun: {args.run_url or 'unknown'}\n\n"
            "If the site is already back, find what stopped it (the VM, the app service, Caddy) "
            "and close this with the cause.")
    return {"title": "Site watch: the site does not answer", "body": body,
            "autopilot": True, "priority": 1, "assignee": None}


def rollback_failed_ticket(args, fails: list[dict]) -> dict:
    paths = "\n".join(f"- {f['test']} ({' and '.join(f['projects'])}): {f['error'][:300]}" for f in fails) or "- (no report)"
    body = ("@Chandler Shortlidge the site is broken and the automatic rollback did not fix it.\n\n"
            f"**Deploy that broke it:** {args.change or 'unknown'}\n"
            f"**Rolled back to:** {args.rolled_back_to or 'unknown'}, and the robot visitor still fails:\n\n"
            f"{paths}\n\nRun: {args.run_url or 'unknown'}")
    return {"title": "Site down and rollback failed", "body": body,
            "autopilot": False, "priority": 1, "assignee": CHANDLER_ID}


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

    def label_id(self, name: str) -> str | None:
        d = self.q("""query($name: String!) { issueLabels(first: 1, filter: {name: {eq: $name}}) { nodes { id } } }""", name=name)
        nodes = d["issueLabels"]["nodes"]
        return nodes[0]["id"] if nodes else None

    def file(self, t: dict) -> str:
        existing = self.open_issue(t["title"])
        if existing:
            self.q("""mutation($issue: String!, $body: String!) { commentCreate(input: {issueId: $issue, body: $body}) { success } }""",
                   issue=existing["id"], body="Seen again.\n\n" + t["body"])
            return f"commented on {existing['identifier']}"
        fields = {"teamId": TEAM_ID, "title": t["title"], "description": t["body"], "priority": t["priority"]}
        if t["autopilot"] and (lid := self.label_id("autopilot")):
            fields["labelIds"] = [lid]
        if t["assignee"]:
            fields["assigneeId"] = t["assignee"]
        d = self.q("""mutation($input: IssueCreateInput!) { issueCreate(input: $input) { issue { identifier } } }""", input=fields)
        return f"filed {d['issueCreate']['issue']['identifier']}"


def tickets(args) -> list[dict]:
    report = json.loads(Path(args.report).read_text()) if args.report and Path(args.report).exists() else {}
    fails = failures(report)
    if args.kind == "uptime":
        return [uptime_ticket(args)]
    if args.kind == "rollback-failed":
        return [rollback_failed_ticket(args, fails)]
    if not fails:
        # The robot went red without a failing path in its report (it crashed, or never ran):
        # still a ticket, or the red run is the only trace.
        fails = [{"test": "the robot visitor itself", "projects": ["any"], "screenshots": [],
                  "error": f"No failing path in the report ({args.report}); the run log has the cause."}]
    return [robot_ticket(args.kind, f, args) for f in fails]


def main(argv=None, linear=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kind", required=True, choices=["deploy", "morning", "uptime", "rollback-failed"])
    ap.add_argument("--report", help="the robot visitor's report.json")
    ap.add_argument("--results-root", help="the folder the report's screenshot paths sit under")
    ap.add_argument("--evidence-base", help="public URL the results folder was copied to")
    ap.add_argument("--run-url")
    ap.add_argument("--change", help="the version that was live: short sha and subject")
    ap.add_argument("--rolled-back-to", help="the version a rollback put back")
    ap.add_argument("--detail", help="uptime: what the check saw")
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
