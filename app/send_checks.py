"""Copy this machine's check log to the server, so its checks are counted there (HIR-294).

The caretaker counts misses in the server's database (app/misses.py), and /check-url runs
on a laptop against a copy. `check` therefore ends by sending its log up.

Does:
  - `outgoing`: every url_check row of this database, oldest first, each with its reason,
    company, city and careers system worked out here (app.misses.recover) — the server
    has no copy of this machine's jobs to recover them from;
  - `send`: hand those records to `python -m app receive-checks` on the server, over the
    SSH login `make ssh` uses (gcloud, through IAP), and read back what it stored;
  - `receive`: on the server, store each record it does not already hold — same URL, same
    time of check — in the order given, in one transaction;
  - `after_check`: what `check` calls. Sends, prints one line, and never raises: a check
    that could not be sent is still in this database and goes with the next one.

Does NOT: run a check, change what a check decides, send jobs or anything but the check
log, or delete or rewrite a row on either side. A record's job id stays behind: it is this
database's, and means nothing in the server's.

Invariants: `receive` is idempotent, so the whole log is sent every time and nothing keeps
track of what went. The first check of a URL is the one counted, by row order, so records
are sent and stored oldest first. HIRING_RADAR_SEND_CHECKS=0 switches sending off; the
test suite sets it (tests/conftest.py).
"""

import json
import os
import shutil
import sqlite3
import subprocess

from app import misses

SERVER_DB = "/var/lib/hiring-radar/hiring-radar.db"
# Where the server is and how `make ssh` reaches it: deploy/README.md.
SSH = ("gcloud", "compute", "ssh", "hiring-radar", "--zone", "europe-west3-a",
       "--project", "hiring-radar-512318", "--tunnel-through-iap")
# Run as the app's user from the checkout, as the units in deploy/ do.
REMOTE = ("sudo -n -u hiring-radar sh -c 'cd /opt/hiring-radar/app && "
          f"HIRING_RADAR_DB={SERVER_DB} .venv/bin/python -m app receive-checks'")
TIMEOUT_S = 120
SWITCH = "HIRING_RADAR_SEND_CHECKS"

FIELDS = ("url", "checked_at", "found_via", "verdict", "feed_had_it", "diagnosis",
          "company", "city", "careers_system", "reason", "reason_detail")
REQUIRED = ("url", "checked_at", "verdict", "feed_had_it")


class SendError(Exception):
    """The records did not reach the server, or it did not say what it stored."""


def outgoing(conn: sqlite3.Connection) -> list[dict]:
    """Every check in this database as a record the server can store as it is."""
    # The same job lookup as misses.records: a miss names no job, but a later check of the
    # same URL often found one, and that job's company and city are the posting's.
    rows = conn.execute("""
        SELECT c.*, j.company AS job_company, j.city AS job_city
        FROM url_check c LEFT JOIN job j ON j.id = coalesce(c.job_id, (
            SELECT c2.job_id FROM url_check c2
            WHERE c2.url = c.url AND c2.job_id IS NOT NULL ORDER BY c2.id LIMIT 1))
        ORDER BY c.id
    """).fetchall()
    out = []
    for r in rows:
        m = misses.recover(dict(r))
        out.append({"url": r["url"], "checked_at": r["checked_at"], "found_via": r["found_via"],
                    "verdict": r["verdict"], "feed_had_it": r["feed_had_it"],
                    "diagnosis": r["diagnosis"], "company": m.company, "city": m.city,
                    "careers_system": m.careers_system, "reason": m.reason,
                    "reason_detail": m.detail or None})
    return out


def receive(conn: sqlite3.Connection, records: list[dict]) -> tuple[int, int]:
    """Store the records this database does not hold yet. (added, already held).
    All or nothing: a malformed record raises ValueError and nothing is stored."""
    for rec in records:
        if not isinstance(rec, dict) or any(rec.get(k) is None for k in REQUIRED):
            raise ValueError(f"not a check record: {str(rec)[:120]}")
    added = 0
    try:
        for rec in records:
            if conn.execute("SELECT 1 FROM url_check WHERE url=? AND checked_at=?",
                            (rec["url"], rec["checked_at"])).fetchone():
                continue
            conn.execute(
                f"INSERT INTO url_check ({', '.join(FIELDS)}) VALUES ({', '.join('?' * len(FIELDS))})",
                [rec.get(k) for k in FIELDS])
            added += 1
    except Exception:
        conn.rollback()
        raise
    conn.commit()
    return added, len(records) - added


def send(records: list[dict], run=subprocess.run) -> tuple[int, int]:
    """Hand the records to the server. (added there, already held there)."""
    try:
        done = run([*SSH, "--command", REMOTE], input=json.dumps({"checks": records}),
                   capture_output=True, text=True, timeout=TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise SendError(f"{type(e).__name__}: {str(e)[:120]}") from e
    # The answer is the last line that is JSON: gcloud and a first-run migration print too.
    for line in reversed(done.stdout.splitlines()):
        if line.startswith("{"):
            try:
                answer = json.loads(line)
                return int(answer["added"]), int(answer["already_held"])
            except (ValueError, KeyError, TypeError):
                break
    last = (done.stderr.strip().splitlines() or ["no answer"])[-1]
    raise SendError(f"exit {done.returncode}: {last[:160]}")


def enabled(db_path) -> bool:
    """Send from here? Not when switched off, not from the server's own database, and not
    from a machine that has no gcloud to log in with."""
    return (os.environ.get(SWITCH, "1") != "0" and str(db_path) != SERVER_DB
            and shutil.which(SSH[0]) is not None)


def after_check(conn: sqlite3.Connection, db_path, log=print, send=send) -> None:
    if not enabled(db_path):
        return
    try:
        records = outgoing(conn)
        if not records:
            return
        added, held = send(records)
    except Exception as e:  # sending is never a reason for a check to fail
        log(f"checks not sent to the server ({str(e)[:200]}); they go with the next check")
        return
    log(f"checks sent to the server: {added} new there, {held} it already had")
