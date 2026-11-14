"""Which tickets the lead agent may start in this run (HIR-266, HIR-280), and which of
the decisions waiting for Chandler go into Monday's comment (HIR-277).

The lead agent (.claude/skills/lead-agent) is a model following instructions. Its hard
limits are here instead, as code with tests, so a "never" cannot be skipped
(DECISIONS 2026-11-12, HIR-266). The agent gathers the tickets and its own log from
Linear, hands them to this script, and starts exactly what it answers.

There is no fixed number of tickets per run or per day (Chandler, 2026-11-12, HIR-280):
every ticket that can run without him is started, unless one of these says no.

It answers no to:

- a ticket that is not in Todo, or is blocked by an open ticket;
- a ticket labelled `attended`, `hands-on` or `parked`;
- a ticket that has already failed twice (two failures go to Monday's summary, never a
  third try);
- a ticket whose spend is unknown, or would pass what is left of the day's cap;
- a ticket in an area where another ticket is already under way (In Progress or In
  Review) or was picked earlier in this run: two changes to the same part of the code
  run one after the other, never together;
- a ticket likely to add a decision for Chandler, while the decisions already waiting for
  him, plus the likely ones picked in this run, are at the limit (10);
- a second ticket in one day that makes the model re-read the stored jobs;
- every ticket that is not a repair, while the main branch's checks or the robot visitor
  are red;
- everything, when the daily cap is zero or already spent, or when a run earlier today
  hit the Claude plan's usage limit.

Order among the rest is the launch order's rule: milestone, then bugs a visitor would
notice, then priority, then oldest.

Input, one JSON object (a file path, or stdin):

    {"today": "2026-11-12",
     "decisions_waiting": 4,
     "red": ["the robot visitor"],
     "decisions": [{"id": "HIR-131", "kind": "question", "labels": ["attended"],
                    "answered": false, "blocks_milestone": true, "blocks_todo": false,
                    "since": "2026-11-03"}, ...],
     "log": [{"date": "2026-11-11", "body": "<a log comment's text>"}, ...],
     "tickets": [{"id": "HIR-197", "state": "Todo", "labels": ["autopilot", "Bug"],
                  "blocked": false, "milestone_rank": 0, "visitor_bug": true,
                  "priority": 2, "created": "2026-11-05", "area": "web-chart",
                  "est_eur": 0, "may_add_decision": false, "rereads": false,
                  "repair": false}, ...]}

`decisions_waiting` is how many real decisions are waiting for Chandler now; the agent
counts them (its skill says how). `red` names each check that is failing (the main
branch's checks, the robot visitor); empty when all are green. Both are required: a run
that did not look must not be read as "nothing waiting, nothing red".

`tickets` holds every ticket in Todo and every ticket under way (In Progress, In Review):
the ones under way are never picked, but each holds its area. `milestone_rank` is the
ticket's place in the launch-order document (0 = "always on", then 1, 2, ... by
milestone). `priority` is Linear's (1 Urgent ... 4 Low, 0 none). `est_eur` is the
model-call spend starting the ticket would cause; null when it cannot be known.
`may_add_decision` is whether the work is likely to end on a decision for Chandler; left
out, it counts as true. `rereads` is whether merging it makes the model re-read the
stored jobs. `repair` marks the ticket that fixes what `red` names.

`decisions` is optional: the open `attended` tickets, handed over by the run that writes
Monday's "Decisions waiting for you" comment (HIR-277). `kind` is `question` (a decision
he has to make) or `yours` (work he does with an agent: an eval session, a cost session);
left out, it is a question. `answered` is true once he has answered and the lead agent has
recorded it on the ticket. `blocks_milestone`: the ticket is in the launch order's current
milestone, or blocks a ticket that is. `blocks_todo`: it blocks a ticket in Todo. `since`
is the day the ticket was filed. Left out altogether, the answer has no
`monday_decisions`: a run that did not look must not be read as "No decisions waiting".

`answers` is optional too: one entry per open `attended` ticket that carries a question
an agent put to Chandler, as `{"id", "question_at", "comments": [{"at", "body"}, ...]}`.
`question_at` is when the newest such question was posted (the comment that @mentions
him, or the Monday comment that listed the ticket), `at` when each comment was; both as
Linear gives them. The answer then has `answer_candidates`: per ticket, the comments
that are newer than the question and are not an agent's own. None means he has not
answered; one or more means the agent reads them and judges.

The log lines it reads, one per ticket, written by the lead agent:

    - HIR-197 | picked: always on; a bug a visitor would notice | result: merged | spend: €0.00

and, anywhere in a log comment, a line starting `Usage limit: reached`.

Output: JSON with `stop` (null, or why nothing may start), `picked` and `skipped`, each
entry with the ticket id and a plain-words reason, plus `spent_eur`, `cap_eur`,
`decisions_waiting`, `queue` (how many tickets that can run alone are in Todo, how many
of those are still there after this pick, and how many more to pull into Todo to keep 5
waiting) and, when `today` is a Monday, `monday`: the three numbers for the weekly
summary as plain sentences. When the state has `decisions`, also `monday_decisions`:
`ask` (the ticket ids to put as questions, in order, at most 10), `more` (how many
questions did not fit), `yours` (the ids for "Yours this week", at most 3) and `text`
(the line that follows the questions: how many more are waiting, or "No decisions
waiting").

Does NOT: talk to Linear or GitHub, start anything, write anything, or call a model. It
does not judge what a ticket's area, milestone or spend is, whether it may add a
decision, or how many decisions are waiting; the agent supplies those. It does not write
the questions either: it only says which tickets, in what order, and how many. Standard
library only.

    python scripts/lead_pick.py state.json            # limits from config/lead_agent.json
    python scripts/lead_pick.py state.json --cap 0    # the "cap set to zero" check
"""

import argparse
import datetime
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
# A ticket in one of these states is being worked: it is never picked, and it holds its
# area until it merges.
UNDER_WAY = ("In Progress", "In Review")
# A log line with this result was held back before any work began; the ticket did not run.
NOT_STARTED = "not-started"
# What a pick reason says when merging the ticket re-reads the stored jobs. The day's log
# is searched for it, so the wording is fixed.
REREAD = "sets off a re-read of the stored jobs"

LOG_LINE = re.compile(
    r"^\s*[-*]\s*(HIR-\d+)\s*\|(.*?)\|\s*result:\s*([a-z-]+)\s*\|\s*spend:\s*€\s*([0-9]+(?:\.[0-9]+)?)",
    re.MULTILINE,
)
# Written by the lead agent when the run, or one of its workers, was refused for usage.
USAGE_LINE = re.compile(r"^\s*Usage limit:\s*reached", re.MULTILINE | re.IGNORECASE)
PRIORITY_NAME = {1: "Urgent", 2: "High", 3: "Medium", 4: "Low"}


def _lines(log):
    """[(date, ticket id, pick reason, result, spend)] for every ticket line in the log."""
    lines = []
    for entry in log:
        for ticket, why, result, spend in LOG_LINE.findall(entry.get("body") or ""):
            lines.append((entry.get("date"), ticket, why.strip(), result, float(spend)))
    return lines


def read_log(log):
    """[(date, ticket id, result, spend)] for every ticket line in the log comments."""
    return [(date, ticket, result, spend) for date, ticket, _, result, spend in _lines(log)]


def failures(log):
    """How many runs of each ticket ended `failed`, over the whole log."""
    counts = {}
    for _, ticket, result, _ in read_log(log):
        if result == FAILED:
            counts[ticket] = counts.get(ticket, 0) + 1
    return counts


def spent_on(log, today):
    """Model-call spend the log records for `today`, over every run of that day."""
    return round(sum(spend for date, _, _, spend in read_log(log) if date == today), 2)


def reread_started_on(log, today):
    """Did a run today already start a ticket that re-reads the stored jobs?"""
    return any(date == today and REREAD in why and result != NOT_STARTED
               for date, _, why, result, _ in _lines(log))


def usage_limit_hit_on(log, today):
    """Did a run today say the Claude plan's usage limit was reached?"""
    return any(entry.get("date") == today and USAGE_LINE.search(entry.get("body") or "")
               for entry in log)


def ran_between(log, start, end):
    """How many different tickets were started from `start` to `end` (days, inclusive)."""
    return len({ticket for date, ticket, result, _ in read_log(log)
                if date and start <= date <= end and result != NOT_STARTED})


def runs_alone(ticket, failed):
    """Could an agent take this ticket with nobody asked: no label that bars it, nothing
    open blocking it, not failed twice. Says nothing about whether its turn has come."""
    labels = {str(name).lower() for name in ticket.get("labels") or []}
    return (not any(name in labels for name in NEVER_LABELS)
            and not ticket.get("blocked")
            and failed.get(ticket["id"], 0) < MAX_FAILURES)


def monday_text(log, today, tickets, decisions_waiting, queue_min=5):
    """The weekly summary's three numbers as plain sentences, for the seven days up to
    yesterday: tickets run, tickets left that can run alone (in Todo or Backlog), decisions
    waiting. Says so plainly when fewer than `queue_min` are left."""
    day = datetime.date.fromisoformat(today)
    start = (day - datetime.timedelta(days=7)).isoformat()
    end = (day - datetime.timedelta(days=1)).isoformat()
    ran = ran_between(log, start, end)
    failed = failures(log)
    left = sum(1 for t in tickets if t.get("state") in ("Todo", "Backlog") and runs_alone(t, failed))

    def n(count, noun):
        return f"{count} {noun}{'' if count == 1 else 's'}"

    text = (f"Agents ran {n(ran, 'ticket')} last week ({start} to {end}). "
            f"{n(left, 'ticket')} left can run without you. "
            f"{n(decisions_waiting, 'decision')} {'is' if decisions_waiting == 1 else 'are'} waiting for you.")
    if left < queue_min:
        text += (" The queue of tickets that can run without you is nearly empty: the project is"
                 " now waiting on your decisions, not on agents.")
    return text


# How an agent's own comment on a ticket starts (the brief, a small call, a review, the
# lead agent's notes and Monday comments, the mark that an answer was recorded). Linear
# shows every agent's comment under Chandler's name, so the first line is what tells them
# apart. A comment an agent session wrote down for him, "Decision (Chandler, <date>)", is
# not in this list on purpose: it is his answer.
AGENT_HEADING = re.compile(
    r"^(brief|doing:|decided for you|review:|lead agent|hands-on brief|answered|pace|"
    r"decisions waiting for you|needs chandler|follow-ups)(?![a-z])", re.IGNORECASE)
# The comment a worker leaves when its pull request is open.
PR_LINK = re.compile(r"github\.com/[^\s/]+/[^\s/]+/pull/\d+")


def answer_candidates(question_at, comments):
    """The comments on a ticket that may be Chandler's answer to the question an agent put
    to him at `question_at` (HIR-277): newer than the question and not an agent's own.

    A ticket nobody asked him about (`question_at` empty) has none, whatever its comments
    say: its `attended` label is his own and no agent lifts it. This only rules comments
    out; whether a candidate really settles the question is the lead agent's reading."""
    if not question_at:
        return []
    found = []
    for comment in comments or []:
        body = (comment.get("body") or "").strip()
        if not body or (comment.get("at") or "") <= question_at:
            continue
        first_line = body.splitlines()[0].lstrip("*#`>_ ")
        if AGENT_HEADING.match(first_line) or PR_LINK.search(body):
            continue
        found.append(comment)
    return found


# Labels that mean a ticket is not a question for Chandler, whatever else it carries.
NOT_A_QUESTION = ("hands-on", "parked")


def monday_decisions(decisions, max_questions=10, max_yours=3):
    """Which waiting decisions Monday's comment asks, in what order (HIR-277).

    At most `max_questions`, so the list can be answered in one sitting: first what blocks
    the current launch milestone, then what blocks a ticket in Todo, then the oldest. A
    ticket he has already answered is never asked again; `hands-on` and `parked` tickets
    are not questions. Work he does with an agent is not a question either: up to
    `max_yours` of those go under "Yours this week", in the same order."""
    def order(item):
        return (0 if item.get("blocks_milestone") else 1,
                0 if item.get("blocks_todo") else 1,
                item.get("since") or "9999",
                item["id"])

    waiting = []
    for item in decisions:
        labels = {str(name).lower() for name in item.get("labels") or []}
        if item.get("answered") or any(name in labels for name in NOT_A_QUESTION):
            continue
        waiting.append(item)
    waiting.sort(key=order)
    questions = [item["id"] for item in waiting if item.get("kind", "question") != "yours"]
    yours = [item["id"] for item in waiting if item.get("kind") == "yours"]
    ask, more = questions[:max_questions], len(questions[max_questions:])
    if not ask:
        text = "No decisions waiting"
    elif more:
        text = f"{more} more {'is' if more == 1 else 'are'} waiting for you."
    else:
        text = "That is every decision waiting for you."
    return {"ask": ask, "more": more, "yours": yours[:max_yours], "text": text}


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
    if ticket.get("rereads"):
        parts.append(REREAD)
    return "; ".join(parts)


def pick(tickets, log, today, cap_eur, decisions_waiting=0, red=(), max_decisions=10, queue_min=5,
         decisions=None, max_questions=10, max_yours=3, answers=None):
    """The run's answer: what may start, what may not and why."""
    spent = spent_on(log, today)
    failed = failures(log)
    alone = [t for t in tickets if t.get("state") == "Todo" and runs_alone(t, failed)]
    result = {
        "stop": None, "picked": [], "skipped": [], "spent_eur": spent, "cap_eur": cap_eur,
        "decisions_waiting": decisions_waiting,
        "queue": {"run_alone_in_todo": len(alone), "left_after_pick": len(alone),
                  "pull": max(0, queue_min - len(alone))},
    }
    if datetime.date.fromisoformat(today).weekday() == 0:
        result["monday"] = monday_text(log, today, tickets, decisions_waiting, queue_min)
    if decisions is not None:
        result["monday_decisions"] = monday_decisions(decisions, max_questions, max_yours)
    if answers is not None:
        result["answer_candidates"] = [
            {"id": item["id"],
             "candidates": answer_candidates(item.get("question_at"), item.get("comments"))}
            for item in answers]
    if cap_eur <= 0:
        result["stop"] = "the daily spending cap is set to zero, so nothing is started"
        return result
    if spent >= cap_eur:
        result["stop"] = f"today's spending cap of €{cap_eur:.2f} is reached (€{spent:.2f} spent)"
        return result
    if usage_limit_hit_on(log, today):
        result["stop"] = ("a run earlier today hit the Claude plan's usage limit, so nothing more "
                          "is started today")
        return result

    red = [str(name) for name in red or []]
    left = cap_eur - spent
    reread_today = reread_started_on(log, today)
    # Each area holds one ticket at a time: the one under way, or the first picked here.
    busy = {}
    for ticket in tickets:
        if ticket.get("state") in UNDER_WAY and ticket.get("area"):
            busy.setdefault(ticket["area"], ticket["id"])
    likely = 0  # picked in this run and likely to add a decision for Chandler

    def skip(ticket, why):
        result["skipped"].append({"id": ticket["id"], "why": why})

    for ticket in sorted(tickets, key=_order):
        labels = {str(name).lower() for name in ticket.get("labels") or []}
        barred = [name for name in NEVER_LABELS if name in labels]
        area = ticket.get("area") or ticket["id"]  # no area given: it shares one with nothing
        est = ticket.get("est_eur")
        may_decide = ticket.get("may_add_decision", True)  # in doubt, it may
        if ticket.get("state") != "Todo":
            skip(ticket, f"not in Todo ({ticket.get('state')})")
        elif barred:
            skip(ticket, f"labelled {barred[0]}")
        elif ticket.get("blocked"):
            skip(ticket, "blocked by an open ticket")
        elif failed.get(ticket["id"], 0) >= MAX_FAILURES:
            skip(ticket, "failed twice already; it goes to Monday's summary, not a third try")
        elif red and not ticket.get("repair"):
            skip(ticket, f"{' and '.join(red)} must be green first; only the repair is started")
        elif est is None:
            skip(ticket, "its model-call spend cannot be known from here; a spend question for Chandler")
        elif est > left + 1e-9:
            skip(ticket, f"would spend €{est:.2f} with €{left:.2f} left under today's cap")
        elif area in busy:
            skip(ticket, f"{busy[area]} is changing the same area ({area}); this one waits for it to merge")
        elif may_decide and decisions_waiting + likely >= max_decisions:
            skip(ticket, f"likely to add a decision for Chandler, and {decisions_waiting + likely} "
                         f"are already waiting or under way (the limit is {max_decisions})")
        elif ticket.get("rereads") and reread_today:
            skip(ticket, "a re-read of the stored jobs was already started today; one a day")
        else:
            left -= est
            busy[area] = ticket["id"]
            likely += 1 if may_decide else 0
            reread_today = reread_today or bool(ticket.get("rereads"))
            result["picked"].append({"id": ticket["id"], "why": _why(ticket), "est_eur": est})

    picked = {entry["id"] for entry in result["picked"]}
    still = sum(1 for t in alone if t["id"] not in picked)
    result["queue"]["left_after_pick"] = still
    result["queue"]["pull"] = max(0, queue_min - still)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Which tickets the lead agent may start in this run.")
    parser.add_argument("state", nargs="?", default="-",
                        help="JSON file with today, decisions_waiting, red, log and tickets (- = stdin)")
    parser.add_argument("--cap", type=float, default=None, help="daily cap in euros (default: config/lead_agent.json)")
    args = parser.parse_args(argv)

    config = json.loads(CONFIG.read_text())
    cap = config["daily_cap_eur"] if args.cap is None else args.cap
    text = sys.stdin.read() if args.state == "-" else Path(args.state).read_text()
    state = json.loads(text)
    missing = [key for key in ("today", "decisions_waiting", "red") if key not in state]
    if missing:
        parser.error(f"the state has no {' or '.join(missing)}; a run that did not look must not "
                     "be read as nothing waiting and nothing red")
    answer = pick(
        state.get("tickets", []),
        state.get("log", []),
        state["today"],
        cap,
        decisions_waiting=state["decisions_waiting"],
        red=state["red"],
        max_decisions=config["max_decisions_waiting"],
        queue_min=config["queue_min"],
        decisions=state.get("decisions"),
        answers=state.get("answers"),
        max_questions=config["monday_questions_max"],
        max_yours=config["monday_yours_max"],
    )
    print(json.dumps(answer, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
