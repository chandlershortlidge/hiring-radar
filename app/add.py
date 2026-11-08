"""Adding one job by hand — from a link, from pasted text, or from a screenshot.

Does two things.

`decide` holds the rules for adding from a *link*: given the result of a link check
(app/check.py) it says what adding it should do — hand back the job it already is, give up
on a page nothing readable came off, refuse a posting with no company, refuse a page that
rendered almost no text, or store it — and whether ingest must insist on a known city.
It is pure: no database, no network, no printing, no model.

`add_by_hand` stores one hand-added posting, whichever of the three ways it arrived. It is
the only place that knows what "added by hand" means to storage, and it hands back
app/ingest.py's typed result.

Does NOT: check the link (app/check.py), read a screenshot (app/transcribe.py), extract
skills (app/pipeline.py), or format a message. Its callers do that: the CLI's `check --add`,
`add-text` and `add-screenshot` (app/__main__.py), the dashboard's three `POST /api/add/*`
endpoints (app/api.py), and the one-off legacy import (scripts/import_legacy.py). They
differ only in how they report an outcome, which is why the rules live here and the wording
does not.

Invariants: every entry point reaches every add-by-link rule through `decide`, and stores
through `add_by_hand`, and nowhere else. The rules drifted twice while they were written
out twice — the no-company rule of HIR-198 had to be added to both, and the minimum-text
rule was only ever in the CLI (HIR-204). A new rule added here reaches every caller at
once, and a new way of adding a job cannot forget one of the three storage settings
(HIR-210).
"""

import sqlite3
from dataclasses import dataclass

from app import dedup, ingest
from app.check import CheckResult
from app.sources import Posting, registry

MIN_ADD_TEXT = 200   # characters; shorter than any real JD

# What `decide` can ask its caller to do.
EXISTS = "exists"            # the check already found this posting stored; adding would duplicate it
UNREADABLE = "unreadable"    # no posting could be read off the page
NEEDS_COMPANY = "needs_company"   # the page named no company, and a blank company can never dedup
TOO_SHORT = "too_short"      # the page rendered too little text to be a posting
STORE = "store"              # go ahead: ingest it, then extract the one job


@dataclass(frozen=True)
class AddDecision:
    """What to do with a checked link. `action` is one of the five constants above."""

    action: str
    job_id: int | None = None     # EXISTS: the job it already is
    require_city: bool = False    # STORE: pass to ingest_one — a page posting needs a known city
    characters: int = 0           # TOO_SHORT: how much text did come off the page

    @property
    def stores(self) -> bool:
        return self.action == STORE


def decide(r: CheckResult, min_text: int = MIN_ADD_TEXT) -> AddDecision:
    """The whole rule set, in the order the rules apply. Pure.

    `min_text` is the shortest page text that may be stored; 0 accepts any readable page.
    """
    if r.verdict == "found":
        # Ingest's own dedup is symmetric Jaccard, which a full careers page can fail against
        # a shorter stored transcript; the check's containment match already said it is stored.
        return AddDecision(EXISTS, job_id=r.job_id)
    if r.posting is None:
        return AddDecision(UNREADABLE)
    if not dedup.company_key(r.posting.company):
        # A blank company can never be matched by dedup, so storing it plants a future
        # duplicate (DECISIONS 2026-11-06 "A job is never stored without a company").
        return AddDecision(NEEDS_COMPANY)
    n = len(r.posting.description_text)
    if n < min_text:
        # A page that rendered nothing readable would be stored as an empty job with no skills.
        return AddDecision(TOO_SHORT, characters=n)
    # Board postings keep their feed source and id, so a later poll sees them as still-listed;
    # page postings are source=url. Either way found_via records that a person found it.
    is_board = r.posting.source in registry.BOARD_SOURCES
    return AddDecision(STORE, require_city=not is_board)


def add_by_hand(conn: sqlite3.Connection, posting: Posting, found_via: str | None,
                when: str | None = None, require_city: bool = False,
                screenshot: ingest.Screenshot | None = None) -> ingest.Stored:
    """Store one posting a person added, and say what that did (app/ingest.py `Stored`).

    This is the one place the "added by hand" storage settings live, so a new way of adding
    a job cannot quietly store jobs under feed rules by forgetting one of them:

    * the title is taken as read — a person chose this posting, so the title filter that
      keeps feeds' unrelated postings out does not apply to it;
    * `found_via` records where the person found it, which is what the coverage line in
      `stats` counts;
    * the city is not insisted on. The one exception is a posting read off a company's own
      careers page, where `decide` asks for a known city — pass `require_city=True` for it.

    `screenshot` is the image the posting was read off, if any. It is written in the same
    transaction as the job, so the two can never come apart.
    """
    return ingest.ingest_one(conn, posting, when or ingest.now_iso(), require_city=require_city,
                             found_via=found_via, trust_title=True, screenshot=screenshot)
