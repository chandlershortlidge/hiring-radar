"""Fixes-only mode (HIR-341): is it on today, and what counts as a fix.

Chandler, 17 Nov 2026: the site is finished on 16 Dec, then he leaves it alone until the
public push in early January. Over that break agents keep repairing what breaks and ship
nothing new. The whole mode is one line in config/lead_agent.json:

    "fixes_only": {"from": "2026-12-16", "until": null},

`from` is the first day in the mode. `until` is the last day in it, or null for "until
Chandler turns it off". Turning it off is that one line: `"fixes_only": null`, or an
`until` that has passed.

Three readers ask the same question here, so they cannot disagree about the dates:

- scripts/lead_pick.py: which tickets the scheduled run may start;
- scripts/merge_reviewed.py: which reviewed pull requests GitHub merges;
- app/caretaker_run.py: the first line of the Monday summary.

    uv run python -m app.fixes_only                  # "on: <sentence>" or "off", for today in Berlin
    git show origin/main:config/lead_agent.json | uv run python -m app.fixes_only --config -

Does NOT: talk to Linear or GitHub, label anything, or decide whether a ticket deserves
the Bug label. It only reads the setting and the labels it is handed. Standard library
only, because the merger runs it on a bare GitHub runner.
"""

import argparse
import datetime
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

CONFIG = Path(__file__).resolve().parent.parent / "config" / "lead_agent.json"
KEY = "fixes_only"
# The Linear label that makes a ticket a fix. Compared without regard to case.
TICKET_LABEL = "bug"
# The GitHub label the reviewer puts on a pull request whose ticket carries that label.
# While the mode is on, the merger merges nothing without it.
PR_LABEL = "fix"


def load(path=CONFIG):
    """The setting as config/lead_agent.json holds it: a dict, or None when there is none."""
    return json.loads(Path(path).read_text()).get(KEY)


def today_berlin():
    """Today's date where Chandler is, as YYYY-MM-DD."""
    return datetime.datetime.now(ZoneInfo("Europe/Berlin")).date().isoformat()


def is_on(setting, today):
    """Is the mode on on `today` (YYYY-MM-DD)? No setting, or one with no `from`, is off.

    A date that cannot be read raises ValueError rather than being taken as off: a typo in
    the one line must not quietly end the break."""
    if not setting or not setting.get("from"):
        return False
    day = datetime.date.fromisoformat(today)
    if day < datetime.date.fromisoformat(setting["from"]):
        return False
    until = setting.get("until")
    return until is None or day <= datetime.date.fromisoformat(until)


def sentence(setting, today):
    """One plain sentence saying the mode is on, or None when it is off. The lead agent's
    log, Monday's pace and the Monday summary all print it unchanged."""
    if not is_on(setting, today):
        return None
    start = datetime.date.fromisoformat(setting["from"])
    until = setting.get("until")
    end = ("until Chandler turns it off" if until is None
           else f"up to and including {_plain(datetime.date.fromisoformat(until))}")
    return (f"The site is in fixes-only mode: since {_plain(start)} agents only repair what "
            f"breaks and ship nothing new, {end}.")


def _plain(day):
    return f"{day.day} {day.strftime('%B %Y')}"


def is_fix(labels, repair=False):
    """Is a ticket with these labels a fix: it carries the Bug label, or it is the repair
    for a check that is red right now."""
    return bool(repair) or TICKET_LABEL in {str(name).lower() for name in labels or []}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Is fixes-only mode on?")
    parser.add_argument("--config", default=str(CONFIG), help="the lead agent's config file (- = stdin)")
    parser.add_argument("--today", default=None, help="YYYY-MM-DD (default: today in Berlin)")
    args = parser.parse_args(argv)
    text = sys.stdin.read() if args.config == "-" else Path(args.config).read_text()
    said = sentence(json.loads(text).get(KEY), args.today or today_berlin())
    print(f"on: {said}" if said else "off")
    return 0


if __name__ == "__main__":
    sys.exit(main())
