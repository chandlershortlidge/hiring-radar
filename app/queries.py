"""Read queries behind the dashboard: stats, skill frequencies, related skills, job list, job detail.

Does: turn a Filters object into SQL, compute document frequency over the filtered job
set (count of jobs mentioning each skill ÷ jobs in the set), the skills that co-occur with
the selected ones (share against the same set's baseline), and the open/closed status of a job.
`rising_skills` counts the jobs open during each of two back-to-back periods and hands the
counts to app.rising, which owns the comparison and its thresholds.
The job list also searches two ways that do not blur: `query` over company and title,
`text` over the posting text itself (the FTS5 index migration 014 keeps in step with it).

Does NOT: write anything, know about HTTP, or call a model. Frontend-only concerns
(profile match, chip ordering) are computed from these results elsewhere.

Open rule (the one the UI states in a tooltip): a job with at least one feed sighting is
open while a feed listed it within FEED_OPEN_DAYS of now; a job known only from manual
adds is assumed open for MANUAL_OPEN_DAYS after it was last seen.

Public rule (HIR-395): every read here answers for the public, so it leaves out what is
still incubating (app/scope.py): a job on an incubating career track, and a job posted
only for incubating places. A job posted for a live place as well is shown, as a job in
its live places only. `public_clause` is that rule; the reads that take
`include_incubating` exist for the tools that work behind the site (labelling, the add
paths, evals), and no public route or MCP tool passes it.

Invariants: pure functions of (connection, filters, now, and the states in app/scope.py);
every count is a count of distinct jobs; percentages are over the filtered set, never the
whole table; with `include_incubating` left off, nothing returned names an incubating
place or belongs to an incubating track.
"""

import sqlite3
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone

from app import scope
from app.extract import SENIORITY_LEVELS
from app.geo import CITIES, COLLECTING_SINCE, REMOTE_EU
from app.ingest import SALES_TITLE_PHRASES
from app.rising import skill_change_calculation
from app.sources import registry

# Complete feeds list every live posting on every poll, so not seeing a job for
# FEED_OPEN_DAYS means it closed. Search sources return a sample (JSearch: ~10 ranked
# results; Arbeitsagentur: only postings published in the last 30 days), so absence there
# proves nothing: a job known only from them, or added by hand, is assumed open for
# MANUAL_OPEN_DAYS. When a complete feed has the job, only that feed's last sighting counts.
# Which source is which kind is declared once, in the source registry (HIR-202).
FEED_SOURCES = registry.COMPLETE_SOURCES
SEARCH_SOURCES = registry.SEARCH_SOURCES
MANUAL_SOURCES = registry.MANUAL_SOURCES
FEED_OPEN_DAYS = 3
MANUAL_OPEN_DAYS = 60
WINDOWS = ("open", "30d", "90d", "all")
REQUIREMENTS = ("required", "all")
# The seniority levels are the ones the model's form allows (HIR-311): one list, so a new
# level cannot reach the model and be refused by the filter.
SENIORITIES = SENIORITY_LEVELS
# The job families a visitor may filter by (HIR-186): the live career tracks of
# app/scope.py, as they stood when the process started. Ingest assigns one to every new job
# from its title. `make_filters` asks scope again on every request, so a track that is
# incubating is refused as a filter value exactly like a name nobody ever defined (HIR-395).
FAMILIES = scope.live_tracks()
# Single-choice filters over the German / degree / production attributes. "open" on degree
# means a person without one can still apply: no degree named, marked optional, or
# equivalent experience accepted.
GERMAN_FILTERS = {
    "any": None,
    "none": "j.german IS NULL",
    "not_required": "(j.german IS NULL OR j.german = 'nice_to_have')",
    "required": "j.german = 'required'",
}
# Production experience (HIR-69): German's four keys exactly, so "not_required" means the
# same thing for both — not asked for, or asked for but marked optional.
PRODUCTION_FILTERS = {
    "any": None,
    "none": "j.production IS NULL",
    "not_required": "(j.production IS NULL OR j.production = 'nice_to_have')",
    "required": "j.production = 'required'",
}
DEGREE_FILTERS = {
    "any": None,
    "none": "j.degree IS NULL",
    "open": "(j.degree IS NULL OR j.degree_or_equivalent = 1 OR j.degree_requirement = 'nice_to_have')",
    "required": "(j.degree IS NOT NULL AND j.degree_or_equivalent = 0 AND j.degree_requirement = 'required')",
}
LEGACY_VERSION = "legacy"   # jobs imported with the hackathon extractor's skills and no real JD text
_NOT_LEGACY = "(j.extracted_version IS NULL OR j.extracted_version != 'legacy')"
# Below this many characters the stored text is a fragment (a cut-off screenshot
# transcript, a teaser), not a posting: extraction finds little or nothing, and counting
# the job would only shrink every share on the chart. DECISIONS 2026-10-21.
MIN_TEXT_CHARS = 400
_LONG_ENOUGH = f"length(j.description_text) >= {MIN_TEXT_CHARS}"
# Stored postings whose title names a sales role are out of the chart, like the two kinds
# above; ingest no longer stores them, and nothing is deleted (DECISIONS 2026-11-16,
# HIR-246). Built from ingest's own tuple so the two cannot drift; tests/test_queries.py
# checks this SQL and ingest.sales_title agree title by title.
_NOT_SALES = "(" + " AND ".join(
    f"lower(coalesce(j.title, '')) NOT LIKE '%{p}%'" for p in SALES_TITLE_PHRASES) + ")"
# related_skills: how many of the selected skill's jobs a skill must share before it is
# worth showing (below that, one odd stack of skills reads as a 4x lift), and how many of
# the ranked rows the panel gets. DECISIONS 2026-10-28.
MIN_CO_JOBS = 5
RELATED_LIMIT = 10
# rising_skills (HIR-232): the length of each of the two periods compared, how many risers
# and how many fallers the panel gets, and the smallest move, in percentage points, worth
# calling a rise or a fall (below 1 point the two shares can print as the same whole
# percent). Whether a move can be trusted at all is app.rising's call, not one of these.
RISING_DAYS = 28
RISING_LIMIT = 5
RISING_MIN_CHANGE = 1.0


def _days_ago(now: str, days: int) -> str:
    t = datetime.strptime(now, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (t - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True)
class Filters:
    cities: tuple[str, ...] = ()          # () = all
    seniorities: tuple[str, ...] = ()     # () = all, including unknown
    families: tuple[str, ...] = ()        # () = all; every job has one (HIR-186)
    german: str = "any"                   # key of GERMAN_FILTERS
    degree: str = "any"                   # key of DEGREE_FILTERS
    production: str = "any"               # key of PRODUCTION_FILTERS
    requirement: str = "required"         # 'required' | 'all'
    window: str = "open"                  # 'open' | '30d' | '90d' | 'all'
    # Job list and related panel only, never the chart. Several ids mean AND: the jobs
    # that list every one of them. () = no skill filter.
    skill_ids: tuple[str, ...] = ()
    query: str = ""                       # job list only: company/title substring
    text: str = ""                        # job list only: words that must appear in the posting text


# --- the job set ----------------------------------------------------------------------

def make_filters(known_skills, *, cities=(), seniorities=(), families=(), requirement="required",
                 window="open", german="any", degree="any", production="any", skill_ids=(), query="",
                 text="") -> Filters:
    """Filters from request values, or ValueError naming the first bad one. The one check
    shared by the dashboard API and the MCP tools, so both accept exactly the same values.
    Cities are not checked: a place we don't collect matches no jobs. Several skill ids
    mean AND; deduplicated, order kept, so a skill sent twice adds no redundant clause."""
    for s in seniorities:
        if s not in SENIORITIES:
            raise ValueError(f"bad seniority {s!r}")
    for s in families:
        if s not in scope.live_tracks():
            raise ValueError(f"bad family {s!r}")
    if requirement not in REQUIREMENTS:
        raise ValueError(f"bad requirement {requirement!r}")
    if window not in WINDOWS:
        raise ValueError(f"bad window {window!r}")
    if german not in GERMAN_FILTERS:
        raise ValueError(f"bad german {german!r}")
    if degree not in DEGREE_FILTERS:
        raise ValueError(f"bad degree {degree!r}")
    if production not in PRODUCTION_FILTERS:
        raise ValueError(f"bad production {production!r}")
    for s in skill_ids:
        if s not in known_skills:
            raise ValueError(f"unknown skill {s!r}")
    return Filters(cities=tuple(cities), seniorities=tuple(seniorities), families=tuple(families),
                   requirement=requirement, window=window, german=german, degree=degree,
                   production=production, skill_ids=tuple(dict.fromkeys(skill_ids)), query=query, text=text)


_HAS_FEED =f"EXISTS (SELECT 1 FROM job_source s WHERE s.job_id = j.id AND s.source IN {FEED_SOURCES})"


_FEED_SEEN = (f"EXISTS (SELECT 1 FROM job_source s WHERE s.job_id = j.id AND s.source IN {FEED_SOURCES}"
              f" AND s.last_seen >= ?)")


def open_clause(now: str) -> tuple[str, list]:
    """SQL (over alias j) that is true when the job counts as open (rule above FEED_SOURCES)."""
    return (f"({_FEED_SEEN} OR (NOT {_HAS_FEED} AND j.last_seen >= ?))",
            [_days_ago(now, FEED_OPEN_DAYS), _days_ago(now, MANUAL_OPEN_DAYS)])


def _marks(values) -> str:
    return ",".join("?" * len(values))


def public_clause() -> tuple[str, list]:
    """SQL (over alias j) true for the jobs the public may see (HIR-395): not on an
    incubating track, and not posted only for incubating places. A job with no place at
    all (some hand-added ones) is shown as before. "1=1" while nothing is incubating, so
    the queries then run exactly as they did."""
    parts, params = [], []
    tracks, places = list(scope.incubating_tracks()), list(scope.incubating_places())
    if tracks:
        parts.append(f"(j.family IS NULL OR j.family NOT IN ({_marks(tracks)}))")
        params += tracks
    if places:
        parts.append(f"(NOT EXISTS (SELECT 1 FROM job_place ipl WHERE ipl.job_id = j.id"
                     f" AND ipl.place IN ({_marks(places)}))"
                     f" OR EXISTS (SELECT 1 FROM job_place lpl WHERE lpl.job_id = j.id"
                     f" AND lpl.place NOT IN ({_marks(places)})))")
        params += places + places
    return (" AND ".join(parts) or "1=1"), params


def _public_place(column: str) -> tuple[str, list]:
    """SQL true when `column` holds a place the public may see: per-place counts never
    carry an incubating place, even for a job that is shown under its live place."""
    places = list(scope.incubating_places())
    return (f"{column} NOT IN ({_marks(places)})", places) if places else ("1=1", [])


def is_public(conn: sqlite3.Connection, job_id: int) -> bool:
    """Does this job exist and may the public see it?"""
    pc, pp = public_clause()
    return conn.execute(f"SELECT 1 FROM job j WHERE j.id = ? AND {pc}", [job_id] + pp).fetchone() is not None


def job_set_clause(f: Filters, now: str, include_legacy: bool = False,
                   include_incubating: bool = False) -> tuple[str, list]:
    """WHERE fragment (over alias j) selecting the jobs the filters describe.

    Unless include_incubating, only jobs the public may see (`public_clause`), and a city
    filter never matches through an incubating place.

    Unless include_legacy, three kinds of job are out of the chart (the job list shows them):
    legacy imports, whose skills never came from the evaluated extractor, jobs whose
    text is shorter than MIN_TEXT_CHARS, a fragment rather than a posting, and jobs whose
    title names a sales role, which are outside the market the chart measures (HIR-246)."""
    parts, params = ([] if include_legacy else [_NOT_LEGACY, _LONG_ENOUGH, _NOT_SALES]), []
    cities = f.cities
    if not include_incubating:
        pc, pp = public_clause()
        if pp:
            parts.append(pc); params += pp
        cities = tuple(c for c in f.cities if c not in scope.incubating_places())
    if f.cities and not cities:
        parts.append("0=1")      # only incubating places were asked for: no job, as for a place we do not collect
    elif cities:
        # Any of the job's places, not only its first: a Berlin + Munich job is in both (HIR-289).
        parts.append(f"EXISTS (SELECT 1 FROM job_place jpl WHERE jpl.job_id = j.id"
                     f" AND jpl.place IN ({_marks(cities)}))")
        params += list(cities)
    if f.seniorities:
        parts.append(f"j.seniority IN ({','.join('?' * len(f.seniorities))})")
        params += list(f.seniorities)
    if f.families:
        parts.append(f"j.family IN ({','.join('?' * len(f.families))})")
        params += list(f.families)
    if GERMAN_FILTERS.get(f.german):
        parts.append(GERMAN_FILTERS[f.german])
    if DEGREE_FILTERS.get(f.degree):
        parts.append(DEGREE_FILTERS[f.degree])
    if PRODUCTION_FILTERS.get(f.production):
        parts.append(PRODUCTION_FILTERS[f.production])
    if f.window == "open":
        c, p = open_clause(now)
        parts.append(c); params += p
    elif f.window in ("30d", "90d"):
        parts.append("j.last_seen >= ?")
        params.append(_days_ago(now, 30 if f.window == "30d" else 90))
    return (" AND ".join(parts) or "1=1"), params


def _mention_clause(f: Filters, alias: str = "m") -> tuple[str, list]:
    if f.requirement == "required":
        return f"{alias}.requirement = 'required'", []
    return "1=1", []


def _skills_clause(f: Filters, prefix: str = "sm") -> tuple[str, list]:
    """SQL (over alias j) true for the jobs that list *every* skill in f.skill_ids.

    One EXISTS per selected skill, ANDed: a skill set of two is read as "and", not "or".
    Each subquery gets its own alias, so the requirement filter applies per skill and the
    clause can sit beside an aggregate's own mention row. No skills selected: "1=1".
    """
    parts, params = [], []
    for i, sid in enumerate(f.skill_ids):
        a = f"{prefix}{i}"
        mc, mp = _mention_clause(f, a)
        parts.append(f"EXISTS (SELECT 1 FROM skill_mention {a}"
                     f" WHERE {a}.job_id = j.id AND {a}.skill_id = ? AND {mc})")
        params += [sid] + mp
    return (" AND ".join(parts) or "1=1"), params


# --- posting-text search ----------------------------------------------------------------

def fts_query(text: str) -> str:
    """Turn what a person typed into an FTS5 MATCH expression: every word must appear.

    FTS5 reads bare input as a query language (AND/OR/NOT, NEAR, column filters, "*"), so
    typing `AND` or an unbalanced quote would either change the meaning or raise a syntax
    error. Each whitespace-separated word is therefore wrapped in double quotes, which
    makes it a literal string token, and the quoted words are ANDed. Returns "" when
    nothing is left to search for, which the caller reads as "no text filter".
    """
    words = [w.replace('"', "") for w in text.split()]
    return " AND ".join(f'"{w}"' for w in words if w)


_FTS_CLAUSE = "j.id IN (SELECT rowid FROM job_fts WHERE job_fts MATCH ?)"


# --- stats ------------------------------------------------------------------------------

def stats(conn: sqlite3.Connection, now: str, skills_tracked: int) -> dict:
    """The header's counts. Every one is over the jobs the public may see (HIR-395): an
    incubating place or track adds to none of them, and is no key of the two breakdowns."""
    # The public rule rides inside the open clause and stands alone for the all-time counts.
    pc, pp = public_clause()
    oc, op = open_clause(now)
    oc, op = f"{pc} AND {oc}", pp + op
    plc, plp = _public_place("jpl.place")
    total = conn.execute(f"SELECT count(*) FROM job j WHERE {pc}", pp).fetchone()[0]
    open_total = conn.execute(f"SELECT count(*) FROM job j WHERE {oc}", op).fetchone()[0]
    by_city = {r["place"]: r["n"] for r in conn.execute(
        f"SELECT jpl.place, count(*) n FROM job j JOIN job_place jpl ON jpl.job_id = j.id WHERE {oc} AND {plc}"
        f" GROUP BY jpl.place", op + plp)}
    by_family = {r["family"]: r["n"] for r in conn.execute(
        f"SELECT j.family, count(*) n FROM job j WHERE {oc} AND j.family IS NOT NULL GROUP BY j.family", op)}
    companies = conn.execute(
        f"SELECT count(DISTINCT lower(j.company)) FROM job j WHERE j.company IS NOT NULL AND {pc}", pp).fetchone()[0]
    last = conn.execute(f"SELECT max(j.last_seen) FROM job j WHERE {pc}", pp).fetchone()[0]
    pending = conn.execute(
        f"SELECT count(*) FROM proposed_skill p JOIN job j ON j.id = p.job_id WHERE p.status='pending' AND {pc}",
        pp).fetchone()[0]
    legacy = conn.execute(f"SELECT count(*) FROM job j WHERE j.extracted_version = ? AND {pc}",
                          [LEGACY_VERSION] + pp).fetchone()[0]
    too_short = conn.execute(f"SELECT count(*) FROM job j WHERE {_NOT_LEGACY} AND NOT {_LONG_ENOUGH} AND {pc}",
                             pp).fetchone()[0]
    open_german = conn.execute(f"SELECT count(*) FROM job j WHERE {oc} AND {GERMAN_FILTERS['required']}", op).fetchone()[0]
    open_degree = conn.execute(f"SELECT count(*) FROM job j WHERE {oc} AND {DEGREE_FILTERS['required']}", op).fetchone()[0]
    open_production = conn.execute(f"SELECT count(*) FROM job j WHERE {oc} AND {PRODUCTION_FILTERS['required']}", op).fetchone()[0]
    return {"jobs": total, "open": open_total, "open_by_city": by_city, "open_by_family": by_family,
            "companies": companies,
            "skills_tracked": skills_tracked, "last_updated": last, "proposed_pending": pending, "legacy": legacy, "too_short": too_short,
            "open_german_required": open_german, "open_degree_required": open_degree,
            "open_production_required": open_production,
            "open_rule": {"feed_days": FEED_OPEN_DAYS, "manual_days": MANUAL_OPEN_DAYS}}


# --- skill frequencies -----------------------------------------------------------------

def _skill_rows(rows, total: int, with_cities: bool = True) -> list[dict]:
    """One row per skill from (skill_id, city, n) rows: count, pct over `total`, by_city.

    The shared tail of skill_frequency and related_skills — group, sort by count desc then
    id, divide by the denominator the caller chose. with_cities=False skips the per-city
    breakdown (and the rows then need no city column).
    """
    agg: dict[str, dict] = {}
    for r in rows:
        s = agg.setdefault(r["skill_id"], {"skill_id": r["skill_id"], "count": 0}
                           | ({"by_city": {}} if with_cities else {}))
        s["count"] += r["n"]
        if with_cities and r["city"]:
            s["by_city"][r["city"]] = s["by_city"].get(r["city"], 0) + r["n"]
    skills = sorted(agg.values(), key=lambda s: (-s["count"], s["skill_id"]))
    for s in skills:
        s["pct"] = round(100 * s["count"] / total, 1) if total else 0.0
    return skills


def skill_frequency(conn: sqlite3.Connection, f: Filters, now: str) -> dict:
    """{'total': n_jobs, 'skills': [{skill_id, count, pct, by_city: {city: count}}...]} sorted by count desc."""
    jc, jp = job_set_clause(f, now)
    mc, mp = _mention_clause(f)
    total = conn.execute(f"SELECT count(*) FROM job j WHERE {jc}", jp).fetchone()[0]
    # The jobs are picked first, once, and only their mentions are read (HIR-372). Joined
    # the other way round, SQLite walked every stored mention and re-checked the whole job
    # filter for each one, posting text included: many times the work, on the request
    # every page makes. CROSS JOIN is SQLite's way of fixing the join order as written.
    js = f"WITH js AS MATERIALIZED (SELECT j.id FROM job j WHERE {jc})"
    rows = conn.execute(
        f"{js} SELECT m.skill_id, count(DISTINCT m.job_id) n FROM js"
        f" CROSS JOIN skill_mention m ON m.job_id = js.id"
        f" WHERE {mc} GROUP BY m.skill_id", jp + mp).fetchall()
    # Per place on a query of its own: a job in two places counts once in `count` and once
    # in each place's `by_city` (HIR-289), so the two cannot come from one grouping.
    by_place: dict[str, dict] = {}
    plc, plp = _public_place("jpl.place")
    for r in conn.execute(
            f"{js} SELECT m.skill_id, jpl.place, count(DISTINCT m.job_id) n FROM js"
            f" CROSS JOIN skill_mention m ON m.job_id = js.id"
            f" CROSS JOIN job_place jpl ON jpl.job_id = js.id"
            f" WHERE {mc} AND {plc} GROUP BY m.skill_id, jpl.place", jp + mp + plp):
        by_place.setdefault(r["skill_id"], {})[r["place"]] = r["n"]
    skills = _skill_rows(rows, total, with_cities=False)
    for s in skills:
        s["by_city"] = by_place.get(s["skill_id"], {})
    return {"total": total, "skills": skills}


def related_skills(conn: sqlite3.Connection, f: Filters, now: str) -> dict:
    """What the jobs listing every skill in f.skill_ids also list.

    Returns {'selected_count', 'total', 'skills': [...]}; with one skill selected the
    answer is identical to the single-skill version this grew out of.

    Every number is over the current filter set (city, seniority, German, degree, window),
    never over all jobs: `total` is that whole set, `selected_count` the jobs in it that
    list the selected skill, and each row's

      pct      = count / selected_count          — the share people read
      base_pct = base count / total              — the same skill across the whole set
      lift     = (count/selected_count) / (base/total)

    Lift is what *selects* the list (Python tops every raw share list; lift surfaces the
    skills that are specific to these jobs), and it comes from the counts, never from the
    rounded percentages. The RELATED_LIMIT rows it picks are then returned by pct desc,
    count desc, so the panel reads top-down by the number it shows. Rows seen in fewer than
    MIN_CO_JOBS of the selected jobs are dropped — one odd stack otherwise reads as a 4x lift.
    Every selected skill is excluded from the rows. No skill selected, or no job in the
    filter set listing all of them: no rows. Several skills are ANDed (`_skills_clause`),
    so `selected_count` shrinks as skills are added and MIN_CO_JOBS prunes the rows
    faster; `selected_count > 0` with no rows is that pruning, and the UI says so.
    """
    base = skill_frequency(conn, f, now)      # the baseline, by construction the same filter set
    total = base["total"]
    base_count = {s["skill_id"]: s for s in base["skills"]}
    empty = {"selected_count": 0, "total": total, "skills": []}
    if not f.skill_ids or not total:
        return empty
    jc, jp = job_set_clause(f, now)
    mc, mp = _mention_clause(f)
    # The same clause list_jobs uses to narrow to the jobs listing every selected skill.
    sel, sel_params = _skills_clause(f)
    selected_count = conn.execute(f"SELECT count(*) FROM job j WHERE {jc} AND {sel}", jp + sel_params).fetchone()[0]
    if not selected_count:
        return empty
    excl = f"m.skill_id NOT IN ({','.join('?' * len(f.skill_ids))})"
    rows = conn.execute(
        f"SELECT m.skill_id, count(DISTINCT j.id) n FROM skill_mention m JOIN job j ON j.id = m.job_id"
        f" WHERE {jc} AND {mc} AND {sel} AND {excl} GROUP BY m.skill_id",
        jp + mp + sel_params + list(f.skill_ids)).fetchall()
    skills = []
    for s in _skill_rows(rows, selected_count, with_cities=False):
        if s["count"] < MIN_CO_JOBS:
            continue
        b = base_count[s["skill_id"]]["count"]   # a subset's skill is always in the baseline
        s["base_pct"] = base_count[s["skill_id"]]["pct"]
        s["lift"] = round((s["count"] / selected_count) / (b / total), 3)
        skills.append(s)
    skills.sort(key=lambda s: (-s["lift"], -s["count"], s["skill_id"]))
    top = skills[:RELATED_LIMIT]
    # Lift picks the ten; the panel then reads top-down by the number it shows. (Every row
    # here shares the denominator selected_count, so pct ranks exactly as count does.)
    top.sort(key=lambda s: (-s["pct"], -s["count"], s["skill_id"]))
    return {"selected_count": selected_count, "total": total, "skills": top}


def city_totals(conn: sqlite3.Connection, f: Filters, now: str) -> dict[str, int]:
    """Jobs per city in the filtered set — the denominators for compare mode."""
    jc, jp = job_set_clause(f, now)
    plc, plp = _public_place("jpl.place")
    return {r["place"]: r["n"] for r in conn.execute(
        f"SELECT jpl.place, count(*) n FROM job j JOIN job_place jpl ON jpl.job_id = j.id WHERE {jc} AND {plc}"
        f" GROUP BY jpl.place", jp + plp)}


# --- what's rising ----------------------------------------------------------------------

def _open_during(conn: sqlite3.Connection, f: Filters, start: str, end: str) -> tuple[int, dict[str, int]]:
    """(jobs open at any moment between start and end, {skill_id: how many of them list it}).

    Open during a period = first seen by its end, and still open at its start by the
    dashboard's own open rule (`open_clause`, asked as of `start`): so a job counts in every
    period it was open in, and a job that stays open counts in both periods compared."""
    base, bp = job_set_clause(replace(f, window="all"), end)
    oc, op = open_clause(start)
    where, params = f"{base} AND j.first_seen <= ? AND {oc}", bp + [end] + op
    mc, mp = _mention_clause(f)
    total = conn.execute(f"SELECT count(*) FROM job j WHERE {where}", params).fetchone()[0]
    rows = conn.execute(
        f"SELECT m.skill_id, count(DISTINCT j.id) n FROM skill_mention m JOIN job j ON j.id = m.job_id"
        f" WHERE {where} AND {mc} GROUP BY m.skill_id", params + mp)
    return total, {r["skill_id"]: r["n"] for r in rows}


def rising_skills(conn: sqlite3.Connection, f: Filters, now: str, skill_added: dict[str, str],
                  collecting_since: dict[str, str] = COLLECTING_SINCE) -> dict:
    """Skills asked for by a larger or smaller share of open jobs in the last RISING_DAYS
    days than in the RISING_DAYS before (HIR-232), for f's cities and families.

    Reads only `cities` (none = every live place), `families` and `requirement` from f.
    An incubating place is no part of the answer (HIR-395): it is not among "every live
    place", so its recent start date cannot hold the whole comparison back, and asked for
    by name it answers like a place we do not collect.
    The shares, the change and whether a change can be trusted are app.rising's
    `skill_change_calculation`, with its own thresholds; nothing here repeats them.

    Two things are held back, because their early numbers would be an artefact:
    - a place whose collection began after the earlier period started (`collecting_since`,
      or a place with no date there): everything open on its first day was "first seen"
      that day, so every skill would look as if it rose. Then status is 'not_enough_data',
      reason 'new_city', and `ready_from` is the first day both periods are covered.
    - a skill added to the list after the earlier period started (`skill_added`, or a skill
      with no date there): postings that closed before it existed were never read with it.

    Otherwise status is 'ok' when at least one skill had enough jobs behind it to compare,
    else 'not_enough_data' with reason 'few_jobs'. `risers` and `fallers` each hold at most
    RISING_LIMIT rows, largest move first, and only moves of RISING_MIN_CHANGE points or
    more; each row carries both counts and both shares.
    """
    cur_start, prev_start = _days_ago(now, RISING_DAYS), _days_ago(now, 2 * RISING_DAYS)
    out = {"status": "not_enough_data", "reason": "new_city", "ready_from": None, "window_days": RISING_DAYS,
           "current": {"start": cur_start, "end": now, "open_jobs": None},
           "previous": {"start": prev_start, "end": cur_start, "open_jobs": None},
           "risers": [], "fallers": []}
    hidden = scope.incubating_places()
    since = [None if c in hidden else collecting_since.get(c) for c in (f.cities or scope.live_places())]
    if None in since:
        return out
    if max(since) > prev_start[:10]:
        newest = datetime.strptime(max(since), "%Y-%m-%d") + timedelta(days=2 * RISING_DAYS)
        return {**out, "ready_from": newest.strftime("%Y-%m-%d")}

    cur_total, cur = _open_during(conn, f, cur_start, now)
    prev_total, prev = _open_during(conn, f, prev_start, cur_start)
    out["current"]["open_jobs"], out["previous"]["open_jobs"] = cur_total, prev_total
    rows, comparable = [], False
    for sid in sorted(set(cur) | set(prev)):
        if skill_added.get(sid, "9999-12-31") > prev_start[:10]:
            continue
        r = skill_change_calculation(cur.get(sid, 0), cur_total, prev.get(sid, 0), prev_total)
        if r is None:
            continue
        comparable = True
        if abs(r["total_change"]) >= RISING_MIN_CHANGE:
            rows.append({"skill_id": sid, "current_count": cur.get(sid, 0), "previous_count": prev.get(sid, 0),
                         "current_share": round(r["current_share"], 1),
                         "previous_share": round(r["previous_share"], 1),
                         "change": round(r["total_change"], 1)})
    if not comparable:
        return {**out, "reason": "few_jobs"}
    rows.sort(key=lambda s: (-abs(s["change"]), s["skill_id"]))
    return {**out, "status": "ok", "reason": None,
            "risers": [s for s in rows if s["change"] > 0][:RISING_LIMIT],
            "fallers": [s for s in rows if s["change"] < 0][:RISING_LIMIT]}


# --- jobs -------------------------------------------------------------------------------

_PLACE_ORDER = {p: i for i, p in enumerate([*CITIES, REMOTE_EU])}


def _places(conn: sqlite3.Connection, ids: list[int], include_incubating: bool = False) -> dict[int, list[str]]:
    """{job id: every place it is posted for}, in geo's order, so the job's own city (the
    first place) leads (HIR-289). Incubating places are left out unless asked for."""
    out: dict[int, list[str]] = {i: [] for i in ids}
    plc, plp = ("1=1", []) if include_incubating else _public_place("place")
    if ids:
        for r in conn.execute(f"SELECT job_id, place FROM job_place WHERE job_id IN ({_marks(ids)}) AND {plc}",
                              ids + plp):
            out[r["job_id"]].append(r["place"])
    for v in out.values():
        v.sort(key=lambda p: (_PLACE_ORDER.get(p, len(_PLACE_ORDER)), p))
    return out


def _shown_city(city: str | None, places: list[str], include_incubating: bool) -> str | None:
    """The job's own city, unless that city is incubating: then the first place the public
    may see, so a job shown for its live place never names its incubating one."""
    if include_incubating or city not in scope.incubating_places():
        return city
    return places[0] if places else None


SORTS = {
    "newest": "j.first_seen DESC, j.id DESC",
    "oldest": "j.first_seen ASC, j.id ASC",
    "reposts": "j.repost_count DESC, j.first_seen DESC",
    "company": "lower(j.company) ASC, j.first_seen DESC",
}


def _status(row, now: str, sources: list[dict]) -> str:
    """Python twin of open_clause, over a job row and its job_source rows (need last_seen)."""
    feed_seen = [s["last_seen"] for s in sources if s["source"] in FEED_SOURCES]
    if feed_seen:
        return "open" if max(feed_seen) >= _days_ago(now, FEED_OPEN_DAYS) else "closed"
    return "open" if row["last_seen"] >= _days_ago(now, MANUAL_OPEN_DAYS) else "closed"


def list_jobs(conn: sqlite3.Connection, f: Filters, now: str, sort: str = "newest",
              limit: int = 20, offset: int = 0, include_incubating: bool = False) -> dict:
    """Find the jobs that match a set of filters, one page at a time.

    This is the dashboard's job list and the search_jobs tool's search: both call it,
    so they always agree. Every filter must match (they combine with AND).

    Example: open Berlin jobs that require RAG, newest first, the first 20:
    list_jobs(conn, filters, now) with filters built from skill "rag" and city "Berlin".

    Args:
        conn: an open database connection.
        f: the filters: which window of jobs, which skills, city, seniority and so
            on, and any words to find in the company, title or posting text.
        now: the current time, as an ISO string. A job is open or closed relative to it.
        sort: "newest" (default), "oldest", "reposts" (most re-advertised first) or
            "company". An unknown value falls back to "newest".
        limit: how many jobs to return.
        offset: how many matching jobs to skip, to reach the next page.
        include_incubating: also return jobs from incubating places and tracks. Off for
            everything public; only tools behind the site turn it on (HIR-395).

    Returns:
        A dict with:
            total: how many jobs match in all, not just on this page.
            jobs: this page's jobs, in the chosen order. Each has its id, company,
                title, places, family, seniority, first_seen, last_seen, status
                (open or closed), sources (where it was posted, with links),
                required_skills and nice_skills (skill ids), skill_counts, and its
                german, degree and production requirements.
            limit, offset: as passed in.
        When nothing matches, total is 0 and jobs is an empty list.
    """
    jc, jp = job_set_clause(f, now, include_legacy=True, include_incubating=include_incubating)
    params = list(jp)
    where = [jc]
    if f.skill_ids:
        sc, sp = _skills_clause(f, "m")      # every selected skill, ANDed
        where.append(sc)
        params += sp
    if f.query.strip():
        q = f"%{f.query.strip().lower()}%"
        where.append("(lower(j.company) LIKE ? OR lower(j.title) LIKE ?)")
        params += [q, q]
    match = fts_query(f.text)
    if match:
        where.append(_FTS_CLAUSE)
        params.append(match)
    w = " AND ".join(where)
    total = conn.execute(f"SELECT count(*) FROM job j WHERE {w}", params).fetchone()[0]
    order = SORTS.get(sort, SORTS["newest"])
    rows = conn.execute(
        f"SELECT j.id, j.company, j.title, j.city, j.family, j.seniority, j.seniority_basis, j.first_seen, j.last_seen,"
        f" j.repost_count, j.extracted_version, length(j.description_text) AS text_len, j.german, j.degree, j.degree_requirement, j.degree_or_equivalent, j.production"
        f" FROM job j WHERE {w} ORDER BY {order} LIMIT ? OFFSET ?",
        params + [limit, offset]).fetchall()
    ids = [r["id"] for r in rows]
    srcs: dict[int, list] = {i: [] for i in ids}
    if ids:
        for s in conn.execute(
                f"SELECT job_id, source, url, first_seen, last_seen, found_via FROM job_source"
                f" WHERE job_id IN ({','.join('?' * len(ids))}) ORDER BY first_seen", ids):
            srcs[s["job_id"]].append({"source": s["source"], "url": s["url"], "first_seen": s["first_seen"],
                                      "last_seen": s["last_seen"], "found_via": s["found_via"]})
    skill_counts: dict[int, dict] = {i: {"required": 0, "nice_to_have": 0} for i in ids}
    required: dict[int, list] = {i: [] for i in ids}
    nice: dict[int, list] = {i: [] for i in ids}
    groups: dict[int, dict] = {i: {} for i in ids}
    if ids:
        for s in conn.execute(
                f"SELECT job_id, skill_id, requirement, alternative_group FROM skill_mention"
                f" WHERE job_id IN ({','.join('?' * len(ids))}) ORDER BY skill_id", ids):
            skill_counts[s["job_id"]][s["requirement"]] += 1
            (required if s["requirement"] == "required" else nice)[s["job_id"]].append(s["skill_id"])
            if s["requirement"] == "required" and s["alternative_group"] is not None:
                groups[s["job_id"]].setdefault(s["alternative_group"], []).append(s["skill_id"])
    places = _places(conn, ids, include_incubating)
    jobs = []
    for r in rows:
        d = dict(r)
        d["places"] = places[r["id"]]
        d["city"] = _shown_city(d["city"], d["places"], include_incubating)
        d["legacy"] = d.pop("extracted_version") == LEGACY_VERSION
        d["too_short"] = not d["legacy"] and d.pop("text_len") < MIN_TEXT_CHARS
        d["degree_or_equivalent"] = bool(d["degree_or_equivalent"])
        d["sources"] = srcs[r["id"]]
        d["status"] = _status(r, now, d["sources"])
        d["skill_counts"] = skill_counts[r["id"]]
        # Ids only, both lists. The browser-side profile match scores a job on the required
        # ones and breaks ties on the nice-to-have ones (HIR-51); the profile itself never
        # reaches this process, so the ranking cannot happen here.
        d["required_skills"] = required[r["id"]]
        d["nice_skills"] = nice[r["id"]]
        # Required skills that are alternatives to each other ("Python, Go or Java"): the
        # match counts each list as one requirement, met by any member (HIR-251). Lists of
        # two or more ids, in group-number order; every id is also in required_skills.
        d["required_groups"] = [g for _, g in sorted(groups[r["id"]].items()) if len(g) > 1]
        jobs.append(d)
    return {"total": total, "jobs": jobs, "limit": limit, "offset": offset}


def job_detail(conn: sqlite3.Connection, job_id: int, now: str, include_incubating: bool = False) -> dict | None:
    """One job in full, or None when there is no such job. A job the public may not see
    yet (`public_clause`) is "no such job" too, unless include_incubating (HIR-395)."""
    if not include_incubating and not is_public(conn, job_id):
        return None
    r = conn.execute(
        "SELECT id, company, title, city, location_raw, family, seniority, seniority_basis, seniority_signal,"
        " german, german_basis, german_signal, degree, degree_requirement, degree_or_equivalent, degree_signal,"
        " production, production_basis, production_signal,"
        " first_seen, last_seen, repost_count, extracted_version, description_text, length(description_text) AS text_len"
        " FROM job WHERE id = ?", (job_id,)).fetchone()
    if not r:
        return None
    d = dict(r)
    d["places"] = _places(conn, [job_id], include_incubating)[job_id]
    d["city"] = _shown_city(d["city"], d["places"], include_incubating)
    d["sources"] = [dict(s) for s in conn.execute(
        "SELECT source, source_job_id, url, found_via, first_seen, last_seen, posted_at FROM job_source"
        " WHERE job_id = ? ORDER BY first_seen", (job_id,))]
    d["status"] = _status(r, now, d["sources"])
    d["legacy"] = d["extracted_version"] == LEGACY_VERSION
    d["too_short"] = not d["legacy"] and (d.pop("text_len") or 0) < MIN_TEXT_CHARS
    d["degree_or_equivalent"] = bool(d["degree_or_equivalent"])
    d["skills"] = [dict(m) for m in conn.execute(
        "SELECT skill_id, requirement, raw_text, alternative_group FROM skill_mention WHERE job_id = ?"
        " ORDER BY requirement = 'required' DESC, skill_id", (job_id,))]
    d["proposed"] = [dict(p) for p in conn.execute(
        "SELECT id, label, raw_text, status FROM proposed_skill WHERE job_id = ? ORDER BY id", (job_id,))]
    d["has_screenshot"] = conn.execute("SELECT 1 FROM screenshot WHERE job_id = ?", (job_id,)).fetchone() is not None
    return d


# --- proposed skills ------------------------------------------------------------------

def proposed_skills(conn: sqlite3.Connection, status: str = "pending", include_incubating: bool = False) -> list[dict]:
    """Grouped by label (case-insensitive): one row per label with every job that proposed it.
    Jobs the public may not see yet, and what only they proposed, are left out unless
    include_incubating (HIR-395): the review queue names each job's company and title."""
    pc, pp = ("1=1", []) if include_incubating else public_clause()
    rows = conn.execute(
        "SELECT p.id, p.label, p.raw_text, p.status, p.resolved_skill_id, j.id job_id, j.company, j.title, j.city, j.first_seen"
        f" FROM proposed_skill p JOIN job j ON j.id = p.job_id WHERE p.status = ? AND {pc} ORDER BY p.id",
        [status] + pp).fetchall()
    groups: dict[str, dict] = {}
    for r in rows:
        key = r["label"].strip().lower()
        g = groups.setdefault(key, {"label": r["label"], "status": r["status"], "ids": [], "jobs": [],
                                    "resolved_skill_id": r["resolved_skill_id"]})
        g["ids"].append(r["id"])
        g["jobs"].append({"job_id": r["job_id"], "company": r["company"], "title": r["title"], "city": r["city"],
                          "raw_text": r["raw_text"], "first_seen": r["first_seen"]})
    out = list(groups.values())
    out.sort(key=lambda g: (-len(g["jobs"]), g["label"].lower()))
    for g in out:
        g["count"] = len(g["jobs"])
    return out


def resolve_proposed(conn: sqlite3.Connection, ids: list[int], status: str, resolved_skill_id: str | None,
                     taxonomy_version: int, extractor_version: str = "review") -> int:
    """Reject, or accept as an alias of an existing taxonomy skill (adds the mention to each job).

    Accepting as a *new* skill is a taxonomy edit (taxonomy/skills.json) followed by
    re-extraction; it is deliberately not done from here.
    """
    if status not in ("accepted", "rejected"):
        raise ValueError("status must be accepted or rejected")
    if status == "accepted" and not resolved_skill_id:
        raise ValueError("accepting needs resolved_skill_id (an existing taxonomy id)")
    if not ids:
        return 0
    q = ",".join("?" * len(ids))
    with conn:
        if status == "accepted":
            rows = conn.execute(
                f"SELECT p.job_id, p.raw_text, m.requirement req FROM proposed_skill p"
                f" LEFT JOIN skill_mention m ON m.job_id = p.job_id AND m.skill_id = ?"
                f" WHERE p.id IN ({q}) AND p.status = 'pending'", [resolved_skill_id] + ids).fetchall()
            for r in rows:
                if r["req"] is None:  # not already on the job
                    conn.execute(
                        "INSERT OR IGNORE INTO skill_mention (job_id, skill_id, requirement, raw_text, taxonomy_version, extractor_version)"
                        " VALUES (?,?,?,?,?,?)",
                        (r["job_id"], resolved_skill_id, "required", r["raw_text"], taxonomy_version, extractor_version))
        cur = conn.execute(
            f"UPDATE proposed_skill SET status = ?, resolved_skill_id = ? WHERE id IN ({q}) AND status = 'pending'",
            [status, resolved_skill_id] + ids)
        return cur.rowcount
