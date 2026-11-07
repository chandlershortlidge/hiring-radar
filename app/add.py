"""The rules for adding one job from a link, in one place.

Does: given the result of a link check (app/check.py), decide what adding it should do —
hand back the job it already is, give up on a page nothing readable came off, refuse a
posting with no company, refuse a page that rendered almost no text, or store it — and say
whether ingest must insist on a known city. `decide` is pure: no database, no network, no
printing, no model.

Does NOT: check the link (app/check.py), store anything (app/ingest.py), extract skills
(app/pipeline.py), or format a message. Its two callers do that: the CLI's `check --add`
(app/__main__.py) and the dashboard's `POST /api/add/url` (app/api.py). They differ only in
how they report an outcome, which is why the decision lives here and the wording does not.

Invariant: both entry points reach every add-by-link rule through `decide` and nowhere
else. The rules drifted twice while they were written out twice — the no-company rule of
HIR-198 had to be added to both, and the minimum-text rule was only ever in the CLI
(HIR-204). A new rule added here reaches both callers at once.
"""

from dataclasses import dataclass

from app import dedup
from app.check import CheckResult
from app.sources import registry

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
