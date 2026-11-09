"""Put postings into the database: still-listed, repost, new-source sighting, or new job.

Does: for each posting decide, in order —
  1. same (source, source_job_id) already stored → still listed: bump last_seen, nothing else;
  2. same company + near-identical text as an existing job → merge: add a job_source row;
     it's a repost (repost_count+1) only when that source had a *different* id for this job
     and none of those ids is in the current fetch — the earlier listing went away. Only
     board feeds (REPOST_SOURCES) can say that; a second id listed at the same time is a
     concurrent duplicate and just merges;
  3. otherwise insert a new job.
Also applies the title/city filters so feeds' unrelated postings never become rows:
a title needs both an AI/ML domain term and a technical role term. A posting with no
company is dropped here too (HIR-207): dedup matches on company first, so a blank-company
row can never be recognised as a duplicate and every repost of it from another source
becomes a second row. A posting whose company name reads as a recruitment agency or a job
portal is dropped as well, but only when it came from a country-wide source (HIR-220):
board sources are screened before the board is ever added, and a posting a person added by
hand was chosen deliberately. A new job is labelled with its job family (family_of, from the title
alone) as it is inserted.

Does NOT: call the model (see app/pipeline.py), fetch anything, or delete rows. It does
not know where a posting came from either: the settings a hand-added posting is stored
with live in app/add.py, which is the one entry point for those (HIR-210).

`in_scope_title` and `agency_name_word` are the two pure screens that decide what may be
stored, and both live here so there is one copy of each: app/discover.py imports
`agency_name_word` for its board screen rather than keeping its own word list (HIR-220).

Invariants: one DB transaction per posting, and a screenshot passed in shares it — the
image and the job it belongs to are both stored or neither is, because the "have I added
this screenshot already?" check reads the image, so a job left without its image would be
added again from the same file (HIR-210); `job.first_seen` never moves later (a
backdated sighting may move it earlier); `job.last_seen` never moves earlier; a posting that fails the filters is counted, not stored (the agency screen runs last, so
the title, city and company counts mean what they always did); no row in `job` is ever written with a blank company; every timestamp written is of the form 2026-11-07T15:42:00Z (check_timestamp).
"""

import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app import dedup
from app.geo import active_place, place_of
from app.sources import Posting, registry

# A title is in scope only when it names an AI/ML domain AND a technical role. Either half
# alone is noise: feeds carry "Industrial AI" in sales titles and "Agent" in call-centre and
# retail ones, and plain "Software Engineer" is not what this project measures. Still broad
# within that rule; the taxonomy decides what the skills are later. German domain words
# (KI, Künstliche Intelligenz) are in because the Arbeitsagentur feed carries German titles;
# "Artificial Intelligence" because titles spell AI out too.
DOMAIN_PATTERN = re.compile(
    r"\b(ai|ki|künstliche intelligenz|artificial intelligence|ml|mlops|llmops|llm|genai|generative ai|nlp|deep learning|"
    r"agentic|agent|prompt|machine learning|data scien\w*|applied scientist|research engineer)\b", re.I)

# `applied scientist` and `research engineer` sit in DOMAIN_PATTERN as well: they carry the
# domain in the role name, so they satisfy both halves on their own, as they did before.
ROLE_PATTERN = re.compile(
    r"\b(engineer\w*|developer|scientist|researcher|architect|mlops)\b", re.I)


# Board feeds return a company's whole board on every fetch, so an id missing from the
# fetch was taken down. Everything else returns a sample (search sources, capped or
# windowed aggregators) or isn't a feed (manual adds), so absence there proves nothing
# and never makes a repost. DECISIONS 2026-10-19 "Reposts".
REPOST_SOURCES = registry.BOARD_SOURCES


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# Every timestamp this project stores has exactly this shape: UTC, to the second, ending in
# Z — 2026-11-07T15:42:00Z. SQLite has no date type, so first_seen and last_seen are plain
# text and everything that reads them compares them as text: the open/closed rule in
# app/queries.py (open_clause) and the min()/max() below that move a job's seen window. A
# value in any other format sorts wrong, and silently — an offset ("+00:00") sorts after
# "Z", milliseconds make a longer string that compares as later, and a bare date is shorter
# than every full timestamp, so it looks older than everything. Callers may pass their own
# `when` (scripts/import_legacy.py, scripts/seed_demo.py), so the check sits here, where
# every stored timestamp goes through. HIR-209.
#
# Not applied to job_source.posted_at: that is kept as the feed gave it, in whatever format
# that is (app/sources/__init__.py), and nothing compares it as text.
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def check_timestamp(when: str) -> str:
    """Returns `when` unchanged, or raises ValueError naming what is wrong with it."""
    if not isinstance(when, str) or not _TIMESTAMP.match(when):
        raise ValueError(
            f"timestamp {when!r} is not of the form 2026-11-07T15:42:00Z (UTC, to the second,"
            f" ending in Z). Stored timestamps are compared as text, so another format sorts"
            f" wrong without any error.")
    try:
        datetime.strptime(when, TIMESTAMP_FORMAT)
    except ValueError as e:
        raise ValueError(f"timestamp {when!r} is not a real date or time: {e}") from None
    return when


def in_scope_title(title: str) -> bool:
    return bool(DOMAIN_PATTERN.search(title) and ROLE_PATTERN.search(title))


# A conservative screen for "recruitment agency or job aggregator": its postings are not
# written by the hiring company, so they distort skill counts the way the aggregator
# headline rows did (DECISIONS 2026-11-03, HIR-123; HIR-104). Substring match on a
# lowercased name with every separator removed, so "talent-partners" and "talentpartners"
# read alike. Conservative on purpose: a missed agency is one noisy feed that can be
# disabled, while a false positive silently drops a real employer — which is why every
# verdict is counted and reported (`skipped_agency` below, and discover's own report).
#
# Lives here, beside in_scope_title, because both are screens on what may be stored and
# there must be exactly one of each: app/discover.py applies this same list to a board's
# token before the board is added, and imports it from here (HIR-220). The dependency
# cannot run the other way — app/discover.py already imports in_scope_title from this
# module.
AGENCY_WORDS = (
    "recruit", "staffing", "headhunt", "jobboard", "jobportal", "jobsite", "aggregator",
    "personalberatung", "personalvermittlung", "zeitarbeit", "workforce", "placement",
    "resourcing", "talentpartner", "talentsolutions", "talentacquisition", "talentgroup",
    "manpower", "randstad", "adecco", "hays", "michaelpage", "roberthalf", "kellyservices",
    "experis", "robertwalters", "pagegroup", "huntscanlon", "jobrapido", "jobleads",
    "learn4good", "ziprecruiter", "indeed", "glassdoor", "monsterjobs",
)


def squashed_name(*parts: str | None) -> str:
    """The parts lowercased and stripped to letters and digits, joined. Pure."""
    return "".join(ch for p in parts if p for ch in p.lower() if ch.isalnum())


def agency_name_word(*parts: str | None) -> str | None:
    """The agency/aggregator word these name parts match, or None. Pure."""
    text = squashed_name(*parts)
    return next((w for w in AGENCY_WORDS if w in text), None)


# The sources the agency screen applies to at ingest: the country-wide ones — the
# Bundesagentur für Arbeit, arbeitnow, JSearch, Startup Jobs — which hand us whoever
# published the posting (DECISIONS 2026-11-09, HIR-220). Derived from the registry's kinds,
# so a country-wide source added later is screened by being registered. Deliberately not
# the board sources: a board is screened before it is ever added, so screening its postings
# again would let a board we chose store nothing at all. Nor the manual sources: a person
# who adds a posting by hand has chosen it, the same reason `trust_title` exists.
SCREENED_SOURCES = registry.of_kind("feed", "search")


# Which of five job families a posting belongs to, from the title alone (HIR-186). Every
# stored job already passed in_scope_title, so the title is enough to bucket the pool at no
# model cost; a model-assigned family can replace this later without the column changing.
# First match wins, in list order: `ml-platform` before `ml-engineer` so "ML Platform
# Engineer" is platform, and a title naming two families takes the earlier entry. The same
# rule, in the same order, backfills existing rows in app/migrations/017_job_family.sql;
# tests/test_ingest.py asserts the two agree. See DECISIONS.md "Job family is a title rule
# (v1)" for the accepted misfiles.
FAMILIES = ("ai-engineer", "ml-engineer", "data-scientist", "ml-platform", "research")

# Punctuation becomes a space before the whole-word `mle` test, so "(MLE)" and "MLE, Berlin"
# count. The SQL backfill normalises exactly this set of characters.
_FAMILY_PUNCT = "-/(),."

_FAMILY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("data-scientist", ("data scien", "datenwissenschaft")),
    ("ml-platform", ("mlops", "ml platform", "ml-platform", "ml infra", "platform engineer")),
    ("ml-engineer", ("machine learning engineer", "machine-learning engineer", "ml engineer", "ml-engineer")),
    ("research", ("research", "applied scientist")),
)


def family_of(title: str) -> str:
    low = (title or "").lower()
    padded = low
    for ch in _FAMILY_PUNCT:
        padded = padded.replace(ch, " ")
    padded = f" {padded} "
    for family, needles in _FAMILY_RULES:
        if any(n in low for n in needles):
            return family
        if family == "ml-engineer" and " mle " in padded:
            return family
    return "ai-engineer"


# What storing one posting did. `ingest_one` returns one of these as `Stored.kind`.
STILL_LISTED = "still_listed"       # this source already had this id: only last_seen moved
MERGED = "merged"                   # same job, another source row added
REPOST = "repost"                   # a merge where the earlier listing had gone away
NEW = "new"                         # a new job row
SKIPPED_TITLE = "skipped_title"
SKIPPED_CITY = "skipped_city"
SKIPPED_COMPANY = "skipped_company"
SKIPPED_AGENCY = "skipped_agency"    # a country-wide source published an agency's posting


@dataclass(frozen=True)
class Screenshot:
    """The image a screenshot posting was read off, stored with the job it creates."""

    data: bytes
    sha256: str
    media_type: str


@dataclass(frozen=True)
class Stored:
    """What storing one posting did, so no caller has to read it out of a string.

    `kind` is one of the eight constants above. `job_id` is the job the posting ended up
    on, and is None only for the four skipped kinds, where no job was touched.
    """

    kind: str
    job_id: int | None = None

    @property
    def is_new(self) -> bool:
        return self.kind == NEW

    def line(self) -> str:
        """One word for the CLI, with the id when a job was created."""
        return f"{NEW}:{self.job_id}" if self.is_new else self.kind


@dataclass
class Report:
    seen: int = 0
    still_listed: int = 0
    merged: int = 0
    reposts: int = 0
    new: int = 0
    skipped_title: int = 0
    skipped_city: int = 0
    skipped_company: int = 0
    skipped_agency: int = 0
    new_job_ids: list[int] = field(default_factory=list)

    def line(self) -> str:
        return (f"seen={self.seen} new={self.new} still_listed={self.still_listed} merged={self.merged} "
                f"reposts={self.reposts} skipped_title={self.skipped_title} skipped_city={self.skipped_city} "
                f"skipped_company={self.skipped_company} skipped_agency={self.skipped_agency}")


def _candidates(conn: sqlite3.Connection, company: str | None) -> list[dedup.Candidate]:
    # Pull same-company rows only; company_key is applied again in dedup for safety.
    rows = conn.execute(
        "SELECT id, company, title, description_text FROM job WHERE company IS NOT NULL").fetchall()
    ck = dedup.company_key(company)
    return [dedup.Candidate(r["id"], r["company"], r["title"], r["description_text"])
            for r in rows if dedup.company_key(r["company"]) == ck]


def ingest_one(conn: sqlite3.Connection, p: Posting, when: str | None = None,
               require_city: bool = True, found_via: str | None = None,
               trust_title: bool = False, fetched_ids: frozenset[str] | None = None,
               screenshot: Screenshot | None = None) -> Stored:
    """Store one posting; see `Stored` for what comes back.

    trust_title skips the title filter — for postings a person chose by hand. It does not
    reach the agency screen, which no manual source goes through in the first place.
    fetched_ids is every source_job_id in the fetch this posting came from; without it
    (a single posting added by hand) nothing counts as a repost.
    screenshot is the image the posting was read off; it is written in the same
    transaction as the new job, and only when a new job is created (a posting that merges
    into a job already stored leaves that job's image alone, as it always has).

    Raises ValueError if `when` is not of the form 2026-11-07T15:42:00Z — a caller's bug,
    not a posting this function can report on (check_timestamp).
    """
    when = check_timestamp(when or now_iso())
    if not trust_title and not in_scope_title(p.title):
        return Stored(SKIPPED_TITLE)
    city = place_of(p.location_raw, p.title, p.description_text)
    if require_city and active_place(p.location_raw, p.title, p.description_text) is None:
        return Stored(SKIPPED_CITY)
    # Last, so the title and city counts keep meaning what they did. No trust_title-style
    # escape: this is the invariant of DECISIONS 2026-11-06 "A job is never stored without
    # a company". Blank means blank *to dedup* — the same company_key that would have to
    # match it — so punctuation alone ("-", "—") and a bare legal suffix ("GmbH") are
    # refused too: they key to the empty string and so could never match anything either.
    if not dedup.company_key(p.company):
        return Stored(SKIPPED_COMPANY)
    # Last of all, so every count above keeps meaning what it did and this one holds only
    # postings that would otherwise have been stored. Country-wide sources only; see
    # SCREENED_SOURCES for why boards and hand-added postings are left out. HIR-220.
    if p.source in SCREENED_SOURCES and agency_name_word(p.company):
        return Stored(SKIPPED_AGENCY)

    with conn:
        if p.source_job_id:
            row = conn.execute("SELECT id, job_id FROM job_source WHERE source=? AND source_job_id=?",
                               (p.source, p.source_job_id)).fetchone()
            if row:
                conn.execute("UPDATE job_source SET last_seen=? WHERE id=?", (when, row["id"]))
                conn.execute("UPDATE job SET last_seen=max(last_seen, ?) WHERE id=?", (when, row["job_id"]))
                return Stored(STILL_LISTED, row["job_id"])

        match = dedup.find_match(p.company, p.title, p.description_text, _candidates(conn, p.company))
        if match:
            job_id = match.job_id
            other_ids = {r[0] for r in conn.execute(
                "SELECT source_job_id FROM job_source WHERE job_id=? AND source=? AND source_job_id IS NOT ?",
                (job_id, p.source, p.source_job_id))}
            is_repost = (p.source in REPOST_SOURCES and fetched_ids is not None
                         and bool(other_ids) and not other_ids & fetched_ids)
            conn.execute(
                "INSERT INTO job_source (job_id, source, source_job_id, url, found_via, first_seen, last_seen, posted_at)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (job_id, p.source, p.source_job_id or None, p.url or None, found_via, when, when, p.posted_at))
            conn.execute("UPDATE job SET last_seen=max(last_seen, ?), first_seen=min(first_seen, ?) WHERE id=?",
                         (when, when, job_id))
            if is_repost:
                conn.execute("UPDATE job SET repost_count = repost_count + 1 WHERE id=?", (job_id,))
                return Stored(REPOST, job_id)
            return Stored(MERGED, job_id)

        cur = conn.execute(
            "INSERT INTO job (company, title, title_key, city, location_raw, description_text, family, first_seen, last_seen)"
            " VALUES (?,?,?,?,?,?,?,?,?)",
            (p.company, p.title, dedup.title_key(p.title), city, p.location_raw, p.description_text,
             family_of(p.title), when, when))
        job_id = cur.lastrowid
        conn.execute(
            "INSERT INTO job_source (job_id, source, source_job_id, url, found_via, first_seen, last_seen, posted_at)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (job_id, p.source, p.source_job_id or None, p.url or None, found_via, when, when, p.posted_at))
        if screenshot is not None:
            _insert_screenshot(conn, job_id, screenshot)
        return Stored(NEW, job_id)


def ingest(conn: sqlite3.Connection, postings: list[Posting], when: str | None = None,
           require_city: bool = True) -> Report:
    """Ingest one feed's fetch. `postings` must be the whole fetch: repost detection reads
    which ids it contains, in any order."""
    r = Report()
    fetched_ids = frozenset(p.source_job_id for p in postings if p.source_job_id)
    for p in postings:
        r.seen += 1
        res = ingest_one(conn, p, when, require_city, fetched_ids=fetched_ids)
        if res.is_new:
            r.new += 1
            r.new_job_ids.append(res.job_id)
        elif res.kind == REPOST:
            r.reposts += 1
            r.merged += 1
        else:
            setattr(r, res.kind, getattr(r, res.kind) + 1)
    return r


def _insert_screenshot(conn: sqlite3.Connection, job_id: int, s: Screenshot) -> None:
    """The write itself, with no transaction of its own, so it can join one."""
    conn.execute("INSERT OR REPLACE INTO screenshot (job_id, sha256, media_type, bytes) VALUES (?,?,?,?)",
                 (job_id, s.sha256, s.media_type, s.data))


def store_screenshot(conn: sqlite3.Connection, job_id: int, data: bytes, sha256: str, media_type: str) -> None:
    """Keep the image so stage 1 can be re-run; one per job, replaced if re-added.

    For a job that already exists. A job being created stores its image in the same
    transaction — pass `screenshot=` to `ingest_one` instead.
    """
    with conn:
        _insert_screenshot(conn, job_id, Screenshot(data, sha256, media_type))


def job_id_for_screenshot(conn: sqlite3.Connection, sha256: str) -> int | None:
    row = conn.execute("SELECT job_id FROM screenshot WHERE sha256=?", (sha256,)).fetchone()
    return row["job_id"] if row else None
