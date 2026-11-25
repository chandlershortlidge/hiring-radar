""""This job doesn't belong here": store a flag, and work out why the job showed (HIR-226).

Does two things, kept apart.

Storage (thin, over the `job_flag` table of migration 025): `add_flag` writes one row per
click, holding the dashboard state the job was flagged from (`view`, stored exactly as the
browser sent it, so a filter added to the dashboard later is recorded with no change here)
and the job as it was stored at that moment (`job_snapshot`). `unflag` and `mark_fixed`
close flags; `flagged_job_ids` is what puts the "flagged" mark on a job.

Diagnosis (pure): `diagnose(view, job, text)` compares every filter that was on screen with
the job's stored value and with the posting's own title, location and text, and returns one
`Check` per filter plus the two checks that hang off no filter (was the job in scope at
all; is the company a recruiter). A check that finds the stored reading contradicted names
a cause. `report_lines` groups open flags by cause, because the fix is per cause.

Does NOT: call a model, fix anything, hide or delete a job, or change what a flag recorded
(the database refuses that). It does not guess either: a flag no rule explains is listed
under "not explained" with its evidence, for an agent or a person to read.

Invariants: `view` and the job snapshot are written once and never rewritten, so a flag
survives a re-read of its job; every filter key the dashboard has is in VIEW_FILTERS
(tests/test_flags.py fails when the dashboard gains one that is missing here); the rules
that judge a title are the ones ingest stores by (`family_of`, `in_scope_title`,
`agency_name_word`, `geo.places_of`), imported, never copied.
"""

import hashlib
import json
import re
import sqlite3
from dataclasses import dataclass

from app import geo, queries
from app.ingest import DOMAIN_PATTERN, agency_name_word, family_of, in_scope_title
from app.sources import registry

NOTE_MAX = 200          # "an optional one-line note"
VIEW_MAX_BYTES = 20_000  # a dashboard state is a few hundred bytes; this only stops junk

UNFLAGGED, FIXED = "unflagged", "fixed"


# --- storage ----------------------------------------------------------------------------

def job_snapshot(conn: sqlite3.Connection, job_id: int, now: str) -> dict | None:
    """The job as it is stored right now, minus the posting text (kept as a length and a
    fingerprint: the text is on the job row, and a re-read never changes it)."""
    d = queries.job_detail(conn, job_id, now)
    if d is None:
        return None
    text = d.pop("description_text") or ""
    d["text_chars"] = len(text)
    d["text_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    d["extractor_version"] = d.pop("extracted_version")
    return d


def clean_note(note: str | None) -> str | None:
    """One line, trimmed, at most NOTE_MAX characters; None when nothing is left."""
    line = " ".join((note or "").split())[:NOTE_MAX]
    return line or None


def add_flag(conn: sqlite3.Connection, job_id: int, view: dict, note: str | None, now: str,
             skill_names: dict[str, str] | None = None) -> int | None:
    """Record one flag; returns its id, or None when there is no such job. `skill_names`
    ({skill id: name}) puts each skill's readable name in the stored copy."""
    snap = job_snapshot(conn, job_id, now)
    if snap is None:
        return None
    for s in snap["skills"]:
        s["display"] = (skill_names or {}).get(s["skill_id"], s["skill_id"])
    with conn:
        cur = conn.execute(
            "INSERT INTO job_flag (job_id, created_at, view, job, note) VALUES (?, ?, ?, ?, ?)",
            (job_id, now, json.dumps(view, sort_keys=True), json.dumps(snap, sort_keys=True), clean_note(note)))
    return cur.lastrowid


def set_note(conn: sqlite3.Connection, flag_id: int, note: str | None) -> bool:
    """Put the note on an open flag. False when the flag is closed or does not exist."""
    with conn:
        cur = conn.execute("UPDATE job_flag SET note = ? WHERE id = ? AND closed_at IS NULL",
                           (clean_note(note), flag_id))
    return cur.rowcount == 1


def unflag(conn: sqlite3.Connection, job_id: int, now: str) -> int:
    """A second click: close every open flag on the job. Returns how many were closed."""
    with conn:
        cur = conn.execute(
            "UPDATE job_flag SET closed_at = ?, closed_reason = ? WHERE job_id = ? AND closed_at IS NULL",
            (now, UNFLAGGED, job_id))
    return cur.rowcount


def mark_fixed(conn: sqlite3.Connection, flag_ids: list[int], now: str) -> int:
    """The cause was fixed: close these flags, which takes the mark off their jobs."""
    if not flag_ids:
        return 0
    with conn:
        cur = conn.execute(
            f"UPDATE job_flag SET closed_at = ?, closed_reason = ? WHERE closed_at IS NULL"
            f" AND id IN ({','.join('?' * len(flag_ids))})", [now, FIXED, *flag_ids])
    return cur.rowcount


def flagged_job_ids(conn: sqlite3.Connection, job_ids: list[int]) -> set[int]:
    """Which of these jobs carry an open flag."""
    if not job_ids:
        return set()
    return {r[0] for r in conn.execute(
        f"SELECT DISTINCT job_id FROM job_flag WHERE closed_at IS NULL"
        f" AND job_id IN ({','.join('?' * len(job_ids))})", job_ids)}


def open_flags(conn: sqlite3.Connection) -> list[dict]:
    """Every open flag, oldest first, with the posting text as it is stored today (None
    when the job has since been removed)."""
    out = []
    for r in conn.execute(
            "SELECT f.id, f.job_id, f.created_at, f.view, f.job, f.note, j.description_text AS text"
            " FROM job_flag f LEFT JOIN job j ON j.id = f.job_id WHERE f.closed_at IS NULL ORDER BY f.id"):
        out.append({"id": r["id"], "job_id": r["job_id"], "created_at": r["created_at"], "note": r["note"],
                    "view": json.loads(r["view"]), "job": json.loads(r["job"]), "text": r["text"]})
    return out


# --- diagnosis --------------------------------------------------------------------------

# The causes, in the order the report prints them. The wording is what a person reads.
FAMILY, SENIORITY, CITY = "job family", "seniority", "city"
GERMAN, DEGREE, PRODUCTION, SKILL = "German", "degree", "production experience", "skill"
FILTER, RELEVANCE, AGENCY, UNEXPLAINED = "filter", "feed relevance", "agency", "not explained"
CAUSES = {
    FAMILY: "job family reading is wrong",
    SENIORITY: "seniority reading is wrong",
    CITY: "city reading is wrong",
    GERMAN: "German reading is wrong",
    DEGREE: "degree reading is wrong",
    PRODUCTION: "production experience reading is wrong",
    SKILL: "skill reading is wrong",
    FILTER: "the filter did not hold (the stored value does not match it)",
    RELEVANCE: "feed relevance (the job should not have been collected)",
    AGENCY: "agency (posted by a recruiter or a job board)",
    UNEXPLAINED: "not explained by any rule (read the evidence)",
}

FAMILY_LABELS = {"ai-engineer": "AI Engineer", "ml-engineer": "ML Engineer", "data-scientist": "Data Scientist",
                 "ml-platform": "ML Platform", "research": "Research",
                 "forward-deployed-engineer": "Forward Deployed Engineer"}

# The title's own level word. The same two lists the dashboard's fit badge reads
# (web/src/profile.js SENIOR_TITLE / JUNIOR_TITLE, HIR-113): short on purpose.
_SENIOR_TITLE = re.compile(r"\b(senior|staff|principal|lead|head)\b", re.I)
_JUNIOR_TITLE = re.compile(r"\b(junior|werkstudent|working student|intern)\b", re.I)

# What the posting text talks about, for the one family that is a remainder: a title lands
# in AI Engineer when it names no other family, so the text is the only other evidence.
_AI_TEXT = re.compile(
    r"\b(ai|ki|ml|llms?|genai|nlp|rag|mlops|llmops|machine learning|deep learning|generative ai|"
    r"artificial intelligence|künstliche intelligenz|agentic)\b", re.I)
_INFRA_TEXT = re.compile(
    r"\b(platform|infrastructure|kubernetes|k8s|terraform|devops|sre|site reliability|ci/cd|"
    r"observability|distributed systems|backend|cloud)\b", re.I)
AI_FEW = 2        # at most this many AI/ML words in the whole posting ...
INFRA_MANY = 3    # ... against at least this many platform/infrastructure words

_WS = re.compile(r"\s+")


@dataclass(frozen=True)
class Check:
    """One comparison: what the view asked for, what was stored, and what the posting says."""
    view: str               # "AI Engineer"
    stored: str             # "job family: AI Engineer"
    evidence: str           # "Title and text describe ..."
    cause: str | None = None   # a key of CAUSES when the comparison found something wrong

    def line(self) -> str:
        verdict = CAUSES[self.cause] if self.cause else "nothing found against it"
        return f"View: {self.view}. Stored {self.stored}. {self.evidence} → {verdict}."


def _quoted(text: str | None, quote: str | None) -> bool | None:
    """Is the quote in the posting? None when either is missing (nothing to judge).
    Whitespace- and case-insensitive, as app/grounding.py compares."""
    if not text or not quote:
        return None
    return _WS.sub(" ", quote).strip().lower() in _WS.sub(" ", text).strip().lower()


def title_level(title: str | None) -> tuple[str | None, str]:
    """('senior' | 'junior' | None, the level words found). None when the title names no
    level, or both."""
    senior = [m.group(0) for m in _SENIOR_TITLE.finditer(title or "")]
    junior = [m.group(0) for m in _JUNIOR_TITLE.finditer(title or "")]
    words = " ".join(senior + junior)
    if bool(senior) == bool(junior):
        return None, words
    return ("senior" if senior else "junior"), words


def _fam(key: str | None) -> str:
    return FAMILY_LABELS.get(key, key or "none")


def _check_families(value, job, text, filters) -> Check:
    stored, title = job.get("family"), job.get("title") or ""
    view, kept = " or ".join(_fam(f) for f in value), f"job family: {_fam(stored)}"
    if stored not in value:
        return Check(view, kept, "The stored family is not one the view asked for", FILTER)
    if family_of(title) != stored:
        return Check(view, kept, f"Today's title rule reads “{title}” as {_fam(family_of(title))}", FAMILY)
    if stored == "ai-engineer":
        # The remainder family: nothing in the title named another one.
        found = []
        if not DOMAIN_PATTERN.search(title):
            found.append(f"The title “{title}” names no AI or ML work; AI Engineer is only where a title"
                         f" lands when it names no other family")
        if text:
            ai, infra = len(_AI_TEXT.findall(text)), len(_INFRA_TEXT.findall(text))
            if ai <= AI_FEW and infra >= INFRA_MANY:
                found.append(f"Title and text describe platform/infrastructure engineering ({infra} such words)"
                             f" with AI or ML mentioned {ai} time{'' if ai == 1 else 's'}")
        if found:
            return Check(view, kept, ". ".join(found), FAMILY)
    return Check(view, kept, f"The title “{title}” fits it")


def _check_seniorities(value, job, text, filters) -> Check:
    stored, title = job.get("seniority"), job.get("title") or ""
    basis, signal = job.get("seniority_basis"), job.get("seniority_signal")
    kept = f"seniority: {stored or 'none'}" + (f" ({basis}{f': “{signal}”' if signal else ''})" if basis else "")
    view = " or ".join(s.capitalize() for s in value)
    if stored not in value:
        return Check(view, kept, "The stored level is not one the view asked for", FILTER)
    level, words = title_level(title)
    if level and level != stored:
        return Check(view, kept, f"Title says “{words}”", SENIORITY)
    if _quoted(text, signal) is False:
        return Check(view, kept, "The quote it rests on is not in the posting", SENIORITY)
    return Check(view, kept, f"The title “{title}” does not contradict it")


def _check_cities(value, job, text, filters) -> Check:
    places = job.get("places") or ([job["city"]] if job.get("city") else [])
    raw = job.get("location_raw")
    view, kept = " or ".join(value), f"city: {', '.join(places) or 'none'}"
    if not set(places) & set(value):
        return Check(view, kept, "None of the stored places is one the view asked for", FILTER)
    today = geo.places_of(raw, job.get("title"), text)
    if not set(today) & set(value):
        return Check(view, kept, f"The location line reads “{raw or ''}”, which today's rule places in"
                                 f" {', '.join(today) or 'no tracked city'}", CITY)
    return Check(view, kept, f"The location line reads “{raw or ''}”")


def _attribute(name: str, cause: str, passes) -> callable:
    """A check for German / degree / production: the filter key against the stored value,
    then whether the quote the reading rests on is in the posting at all."""
    def check(value, job, text, filters) -> Check:
        stored, signal = job.get(name), job.get(f"{name}_signal")
        kept = f"{cause}: {stored or 'not asked for'}" + (f" (“{signal}”)" if signal else "")
        view = f"{cause} {value.replace('_', ' ')}"
        if not passes(value, job):
            return Check(view, kept, "The stored value does not satisfy the filter", FILTER)
        if _quoted(text, signal) is False:
            return Check(view, kept, "The quote it rests on is not in the posting", cause)
        return Check(view, kept, "No rule can judge this one from the text; the quote is the evidence")
    return check


def _two_level(name: str):
    """German and production share their four keys (queries.GERMAN_FILTERS)."""
    return lambda value, job: {"none": job.get(name) is None,
                               "not_required": job.get(name) in (None, "nice_to_have"),
                               "required": job.get(name) == "required"}.get(value, True)


def _degree_passes(value, job) -> bool:
    has, equiv, req = job.get("degree") is not None, bool(job.get("degree_or_equivalent")), job.get("degree_requirement")
    return {"none": not has, "open": not has or equiv or req == "nice_to_have",
            "required": has and not equiv and req == "required"}.get(value, True)


def _check_skills(value, job, text, filters) -> list[Check]:
    required_only = filters.get("requirement", "required") == "required"
    out = []
    for skill_id in value:
        m = next((s for s in job.get("skills") or [] if s.get("skill_id") == skill_id), None)
        name = (m or {}).get("display") or skill_id
        view = f"{'requires' if required_only else 'mentions'} {name}"
        if m is None or (required_only and m.get("requirement") != "required"):
            kept = f"skill: {name} {'as nice-to-have' if m else 'not stored'}"
            out.append(Check(view, kept, "The job does not carry the skill the view asked for", FILTER))
            continue
        kept = f"skill: {name}, {m.get('requirement', '').replace('_', ' ')} (“{m.get('raw_text') or ''}”)"
        if _quoted(text, m.get("raw_text")) is False:
            out.append(Check(view, kept, "The quote it rests on is not in the posting", SKILL))
        else:
            out.append(Check(view, kept, "No rule can judge this one from the text; the quote is the evidence"))
    return out


def _check_window(value, job, text, filters) -> Check:
    status = job.get("status") or "unknown"
    if status != "open":
        return Check("currently open", f"status: {status}", "The job was not open when it was flagged", FILTER)
    return Check("currently open", f"status: {status}", f"Last seen {job.get('last_seen') or 'unknown'}")


# Every filter key the dashboard keeps (web/src/App.jsx DEFAULT), with when it is on and
# how it is judged. None = the key says nothing about one job, and why. A key the dashboard
# gains must be added here, in one of the two ways: tests/test_flags.py fails until it is.
VIEW_FILTERS = {
    "families": (lambda v: bool(v), _check_families),
    "seniorities": (lambda v: bool(v), _check_seniorities),
    "cities": (lambda v: bool(v), _check_cities),
    "german": (lambda v: v not in (None, "any"), _attribute("german", GERMAN, _two_level("german"))),
    "degree": (lambda v: v not in (None, "any"), _attribute("degree", DEGREE, _degree_passes)),
    "production": (lambda v: v not in (None, "any"),
                   _attribute("production", PRODUCTION, _two_level("production"))),
    "skillIds": (lambda v: bool(v), _check_skills),
    "window": (lambda v: v == "open", _check_window),
    "compare": None,       # which chart is drawn; the compared cities arrive in `cities`
    "requirement": None,   # how the skill filter reads; judged with `skillIds`
    "query": None,         # literal match on company or title: not a reading of the job
    "text": None,          # literal match on the posting's words: not a reading of the job
}


def diagnose(view: dict, job: dict, text: str | None) -> list[Check]:
    """Every comparison for one flag. Pure."""
    checks: list[Check] = []
    filters = view.get("filters") or {}
    # On a job's own page, and in the saved list, no filter decided that the job showed.
    filtered = view.get("page", "list") == "list" and not view.get("saved")
    if filtered:
        for key, value in filters.items():
            rule = VIEW_FILTERS.get(key)
            if rule is None:
                if key not in VIEW_FILTERS and value not in (None, "", [], False, "any"):
                    checks.append(Check(f"{key} = {value!r}", "value: unknown",
                                        "This filter is newer than the diagnosis and was not judged", UNEXPLAINED))
                continue
            active, check = rule
            if active(value):
                found = check(value, job, text, filters)
                checks += found if isinstance(found, list) else [found]

    title, company = job.get("title") or "", job.get("company") or ""
    by_hand = any(s.get("source") in registry.MANUAL_SOURCES for s in job.get("sources") or [])
    if not by_hand and not in_scope_title(title):
        checks.append(Check("any job we collect", f"title: “{title}”",
                            "Today's title rule (an AI/ML word and a technical role) would not collect it",
                            RELEVANCE))
    if (word := agency_name_word(company)):
        checks.append(Check("jobs posted by the employer", f"company: “{company}”",
                            f"The company name contains “{word}”", AGENCY))
    return checks


def causes_of(checks: list[Check]) -> list[str]:
    """The causes a flag is filed under, in CAUSES order; UNEXPLAINED when no rule fired."""
    found = {c.cause for c in checks if c.cause}
    return [c for c in CAUSES if c in found] or [UNEXPLAINED]


def _where(view: dict) -> str:
    if view.get("page") == "job":
        return f"the job's own page ({view.get('url') or '?'}); no filter decided that it showed"
    saved = "; the saved list, which no filter narrows" if view.get("saved") else ""
    return f"{view.get('url') or '?'}{saved}"


def report_lines(flags: list[dict]) -> list[str]:
    """The `flags` command's output: open flags grouped by cause. Pure."""
    if not flags:
        return ["No open flags."]
    groups: dict[str, list[list[str]]] = {c: [] for c in CAUSES}
    for f in flags:
        job, view = f["job"], f["view"]
        checks = diagnose(view, job, f.get("text"))
        sources = ", ".join(sorted({s.get("source", "?") for s in job.get("sources") or []})) or "no source"
        block = [f"  flag {f['id']} · job {f['job_id'] if f['job_id'] is not None else 'removed'} ·"
                 f" {job.get('company') or '?'} — {job.get('title') or '?'} · {sources} ·"
                 f" flagged {f['created_at'][:10]}"
                 + (f" · note: “{f['note']}”" if f.get("note") else ""),
                 f"    seen on: {_where(view)}",
                 f"    read by extractor version: {job.get('extractor_version') or 'not read yet'}"]
        if f.get("text") is None:
            block.append("    the posting is no longer stored, so nothing was compared with its text")
        block += [f"    {c.line()}" for c in checks]
        if not checks:
            block.append("    No filter was on and neither general rule found a cause: nothing to compare.")
        for cause in causes_of(checks):
            groups[cause].append(block)
    used = [(c, blocks) for c, blocks in groups.items() if blocks]
    lines = [f"{len(flags)} open flag{'' if len(flags) == 1 else 's'}, {len(used)} cause{'' if len(used) == 1 else 's'}."]
    for cause, blocks in used:
        lines += ["", f"{CAUSES[cause]} ({len(blocks)})"]
        for block in blocks:
            lines += block
    return lines
