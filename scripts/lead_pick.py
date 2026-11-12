"""Which tickets the lead agent may start today (HIR-266).

The lead agent (.claude/skills/lead-agent) is a model following instructions. Its hard
limits are here instead, as code with tests, so a "never" cannot be skipped
(DECISIONS 2026-11-12, HIR-266). The agent gathers the Todo tickets and its own log from
Linear, hands them to this script, and starts exactly what it answers.

It answers no to:

- a ticket that is not in Todo, or is blocked by an open ticket;
- a ticket labelled `attended`, `hands-on` or `parked`;
- a ticket that has already failed twice (two failures go to Monday's summary, never a
  third try);
- a ticket whose spend is unknown, or would pass what is left of the day's cap;
- a fourth ticket in one day, or a third in one area;
- everything, when the daily cap is zero or already spent.

Order among the rest is the launch order's rule: milestone, then bugs a visitor would
notice, then priority, then oldest.

Input, one JSON object (a file path, or stdin):

    {"today": "2026-11-12",
     "log": [{"date": "2026-11-11", "body": "<a log comment's text>"}, ...],
     "tickets": [{"id": "HIR-197", "state": "Todo", "labels": ["autopilot", "Bug"],
                  "blocked": false, "milestone_rank": 0, "visitor_bug": true,
                  "priority": 2, "created": "2026-11-05", "area": "web",
                  "est_eur": 0}, ...]}

`milestone_rank` is the ticket's place in the launch-order document (0 = "always on", then
1, 2, ... by milestone). `priority` is Linear's (1 Urgent ... 4 Low, 0 none). `est_eur` is
the model-call spend starting the ticket would cause; null when it cannot be known.

The log lines it reads, one per ticket, written by the lead agent:

    - HIR-197 | picked: always on; a bug a visitor would notice | result: merged | spend: €0.00

Output: JSON with `stop` (null, or why nothing may start), `picked` and `skipped`, each
entry with the ticket id and a plain-words reason, plus `spent_eur` and `cap_eur`.

Does NOT: talk to Linear or GitHub, start anything, write anything, or call a model. It
does not judge what a ticket's area, milestone or spend is; the agent supplies those.
Standard library only.

    python scripts/lead_pick.py state.json            # cap from config/lead_agent.json
    python scripts/lead_pick.py state.json --cap 0    # the "cap set to zero" check
"""

import argparse
import json
import re
import sys
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "config" / "lead_agent.json"

# Labels that take a ticket away from the lead agent, whatever else is true of it.
NEVER_LABELS = ("attended", "hands-on", "parked")
# A ticket is tried at most this many times; after that it is Monday's, not a retry.
MAX_FAILURES = 2
FAILED = "failed"

LOG_LINE = re.compile(
    r"^\s*[-*]\s*(HIR-\d+)\s*\|.*?\|\s*result:\s*([a-z-]+)\s*\|\s*spend:\s*€\s*([0-9]+(?:\.[0-9]+)?)",
    re.MULTILINE,
)
PRIORITY_NAME = {1: "Urgent", 2: "High", 3: "Medium", 4: "Low"}


def read_log(log):
    """[(date, ticket id, result, spend)] for every ticket line in the log comments."""
    lines = []
    for entry in log:
        for ticket, result, spend in LOG_LINE.findall(entry.get("body") or ""):
            lines.append((entry.get("date"), ticket, result, float(spend)))
    return lines


def failures(log):
    """How many runs of each ticket ended `failed`, over the whole log."""
    counts = {}
    for _, ticket, result, _ in read_log(log):
        if result == FAILED:
            counts[ticket] = counts.get(ticket, 0) + 1
    return counts


def spent_on(log, today):
    """Model-call spend the log records for `today`."""
    return round(sum(spend for date, _, _, spend in read_log(log) if date == today), 2)


def _order(ticket):
    priority = ticket.get("priority") or 0
    return (
        ticket.get("milestone_rank", 99),
        0 if ticket.get("visitor_bug") else 1,
        priority if priority else 5,  # "no priority" sorts after Low
        ticket.get("created") or "9999",
        ticket["id"],
    )


def _why(ticket):
    rank = ticket.get("milestone_rank", 99)
    parts = ["always on" if rank == 0 else f"milestone {rank}"]
    if ticket.get("visitor_bug"):
        parts.append("a bug a visitor would notice")
    parts.append(f"priority {PRIORITY_NAME.get(ticket.get('priority') or 0, 'none')}")
    parts.append(f"filed {ticket.get('created') or 'date unknown'}")
    return "; ".join(parts)


def pick(tickets, log, today, cap_eur, max_tickets=3, max_per_area=2):
    """The day's answer: what may start, what may not and why."""
    spent = spent_on(log, today)
    result = {"stop": None, "picked": [], "skipped": [], "spent_eur": spent, "cap_eur": cap_eur}
    if cap_eur <= 0:
        result["stop"] = "the daily spending cap is set to zero, so nothing is started"
        return result
    if spent >= cap_eur:
        result["stop"] = f"today's spending cap of €{cap_eur:.2f} is reached (€{spent:.2f} spent)"
        return result

    failed = failures(log)
    left = cap_eur - spent
    per_area = {}

    def skip(ticket, why):
        result["skipped"].append({"id": ticket["id"], "why": why})

    for ticket in sorted(tickets, key=_order):
        labels = {str(name).lower() for name in ticket.get("labels") or []}
        barred = [name for name in NEVER_LABELS if name in labels]
        area = ticket.get("area") or ticket["id"]  # no area given: it shares one with nothing
        est = ticket.get("est_eur")
        if ticket.get("state") != "Todo":
            skip(ticket, f"not in Todo ({ticket.get('state')})")
        elif barred:
            skip(ticket, f"labelled {barred[0]}")
        elif ticket.get("blocked"):
            skip(ticket, "blocked by an open ticket")
        elif failed.get(ticket["id"], 0) >= MAX_FAILURES:
            skip(ticket, "failed twice already; it goes to Monday's summary, not a third try")
        elif est is None:
            skip(ticket, "its model-call spend cannot be known from here; a spend question for Chandler")
        elif est > left + 1e-9:
            skip(ticket, f"would spend €{est:.2f} with €{left:.2f} left under today's cap")
        elif len(result["picked"]) >= max_tickets:
            skip(ticket, f"{max_tickets} tickets already picked today")
        elif per_area.get(area, 0) >= max_per_area:
            skip(ticket, f"{max_per_area} tickets in the same area ({area}) already picked today")
        else:
            left -= est
            per_area[area] = per_area.get(area, 0) + 1
            result["picked"].append({"id": ticket["id"], "why": _why(ticket), "est_eur": est})
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Which tickets the lead agent may start today.")
    parser.add_argument("state", nargs="?", default="-", help="JSON file with today, log and tickets (- = stdin)")
    parser.add_argument("--cap", type=float, default=None, help="daily cap in euros (default: config/lead_agent.json)")
    args = parser.parse_args(argv)

    config = json.loads(CONFIG.read_text())
    cap = config["daily_cap_eur"] if args.cap is None else args.cap
    text = sys.stdin.read() if args.state == "-" else Path(args.state).read_text()
    state = json.loads(text)
    answer = pick(
        state.get("tickets", []),
        state.get("log", []),
        state["today"],
        cap,
        max_tickets=config["max_tickets"],
        max_per_area=config["max_per_area"],
    )
    print(json.dumps(answer, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
