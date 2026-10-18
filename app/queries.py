"""Read queries behind the dashboard: stats, skill frequencies, job list, job detail.

Does: turn a Filters object into SQL, compute document frequency over the filtered job
set (count of jobs mentioning each skill ÷ jobs in the set), and the open/closed status
of a job.

Does NOT: write anything, know about HTTP, or call a model. Frontend-only concerns
(profile match, chip ordering) are computed from these results elsewhere.

Open rule (the one the UI states in a tooltip): a job with at least one feed sighting is
open while a feed listed it within FEED_OPEN_DAYS of now; a job known only from manual
adds is assumed open for MANUAL_OPEN_DAYS after it was last seen.

Invariants: pure functions of (connection, filters, now); every count is a count of
distinct jobs; percentages are over the filtered set, never the whole table.
"""

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

# Complete feeds list every live posting on every poll, so not seeing a job for
# FEED_OPEN_DAYS means it closed. Search sources return a sample (JSearch: ~10 ranked
# results; Arbeitsagentur: only postings published in the last 30 days), so absence there
# proves nothing: a job known only from them, or added by hand, is assumed open for
# MANUAL_OPEN_DAYS. When a complete feed has the job, only that feed's last sighting counts.
FEED_SOURCES = ("greenhouse", "lever", "ashby", "startup_jobs", "arbeitnow")
SEARCH_SOURCES = ("jsearch", "arbeitsagentur")
MANUAL_SOURCES = ("url", "paste", "screenshot")
FEED_OPEN_DAYS = 3
MANUAL_OPEN_DAYS = 60
WINDOWS = ("open", "30d", "90d", "all")
REQUIREMENTS = ("required", "all")
SENIORITIES = ("junior", "mid", "senior")
# Single-choice filters over the German / degree attributes. "open" on degree means a person
# without one can still apply: no degree named, marked optional, or equivalent experience accepted.
GERMAN_FILTERS = {
    "any": None,
    "none": "j.german IS NULL",
    "not_required": "(j.german IS NULL OR j.german = 'nice_to_have')",
    "required": "j.german = 'required'",
}
DEGREE_FILTERS = {
    "any": None,
    "none": "j.degree IS NULL",
    "open": "(j.degree IS NULL OR j.degree_or_equivalent = 1 OR j.degree_requirement = 'nice_to_have')",
    "required": "(j.degree IS NOT NULL AND j.degree_or_equivalent = 0 AND j.degree_requirement = 'required')",
}
LEGACY_VERSION = "legacy"   # jobs imported with the hackathon extractor's skills and no real JD text
_NOT_LEGACY = "(j.extracted_version IS NULL OR j.extracted_version != 'legacy')"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _days_ago(now: str, days: int) -> str:
    t = datetime.strptime(now, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (t - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True)
class Filters:
    cities: tuple[str, ...] = ()          # () = all
    seniorities: tuple[str, ...] = ()     # () = all, including unknown
    german: str = "any"                   # key of GERMAN_FILTERS
    degree: str = "any"                   # key of DEGREE_FILTERS
    requirement: str = "required"         # 'required' | 'all'
    window: str = "open"                  # 'open' | '30d' | '90d' | 'all'
    skill_id: str | None = None           # job list only
    query: str = ""                       # job list only: company/title substring


# --- the job set ----------------------------------------------------------------------

_HAS_FEED = f"EXISTS (SELECT 1 FROM job_source s WHERE s.job_id = j.id AND s.source IN {FEED_SOURCES})"


_FEED_SEEN = (f"EXISTS (SELECT 1 FROM job_source s WHERE s.job_id = j.id AND s.source IN {FEED_SOURCES}"
              f" AND s.last_seen >= ?)")


def open_clause(now: str) -> tuple[str, list]:
    """SQL (over alias j) that is true when the job counts as open (rule above FEED_SOURCES)."""
    return (f"({_FEED_SEEN} OR (NOT {_HAS_FEED} AND j.last_seen >= ?))",
            [_days_ago(now, FEED_OPEN_DAYS), _days_ago(now, MANUAL_OPEN_DAYS)])


def job_set_clause(f: Filters, now: str, include_legacy: bool = False) -> tuple[str, list]:
    """WHERE fragment (over alias j) selecting the jobs the filters describe.

    Legacy-imported jobs are out unless include_legacy: their skills were never produced by
    the evaluated extractor, so they must not reach the chart. The job list shows them."""
    parts, params = ([] if include_legacy else [_NOT_LEGACY]), []
    if f.cities:
        parts.append(f"j.city IN ({','.join('?' * len(f.cities))})")
        params += list(f.cities)
    if f.seniorities:
        parts.append(f"j.seniority IN ({','.join('?' * len(f.seniorities))})")
        params += list(f.seniorities)
    if GERMAN_FILTERS.get(f.german):
        parts.append(GERMAN_FILTERS[f.german])
    if DEGREE_FILTERS.get(f.degree):
        parts.append(DEGREE_FILTERS[f.degree])
    if f.window == "open":
        c, p = open_clause(now)
        parts.append(c); params += p
    elif f.window in ("30d", "90d"):
        parts.append("j.last_seen >= ?")
        params.append(_days_ago(now, 30 if f.window == "30d" else 90))
    return (" AND ".join(parts) or "1=1"), params


def _mention_clause(f: Filters) -> tuple[str, list]:
    if f.requirement == "required":
        return "m.requirement = 'required'", []
    return "1=1", []


# --- stats ------------------------------------------------------------------------------

def stats(conn: sqlite3.Connection, now: str, skills_tracked: int) -> dict:
    oc, op = open_clause(now)
    total = conn.execute("SELECT count(*) FROM job").fetchone()[0]
    open_total = conn.execute(f"SELECT count(*) FROM job j WHERE {oc}", op).fetchone()[0]
    by_city = {r["city"]: r["n"] for r in conn.execute(
        f"SELECT j.city, count(*) n FROM job j WHERE {oc} AND j.city IS NOT NULL GROUP BY j.city", op)}
    companies = conn.execute("SELECT count(DISTINCT lower(company)) FROM job WHERE company IS NOT NULL").fetchone()[0]
    last = conn.execute("SELECT max(last_seen) FROM job").fetchone()[0]
    pending = conn.execute("SELECT count(*) FROM proposed_skill WHERE status='pending'").fetchone()[0]
    legacy = conn.execute("SELECT count(*) FROM job WHERE extracted_version = ?", (LEGACY_VERSION,)).fetchone()[0]
    open_german = conn.execute(f"SELECT count(*) FROM job j WHERE {oc} AND {GERMAN_FILTERS['required']}", op).fetchone()[0]
    open_degree = conn.execute(f"SELECT count(*) FROM job j WHERE {oc} AND {DEGREE_FILTERS['required']}", op).fetchone()[0]
    return {"jobs": total, "open": open_total, "open_by_city": by_city, "companies": companies,
            "skills_tracked": skills_tracked, "last_updated": last, "proposed_pending": pending, "legacy": legacy,
            "open_german_required": open_german, "open_degree_required": open_degree,
            "open_rule": {"feed_days": FEED_OPEN_DAYS, "manual_days": MANUAL_OPEN_DAYS}}


# --- skill frequencies -----------------------------------------------------------------

def skill_frequency(conn: sqlite3.Connection, f: Filters, now: str) -> dict:
    """{'total': n_jobs, 'skills': [{skill_id, count, pct, by_city: {city: count}}...]} sorted by count desc."""
    jc, jp = job_set_clause(f, now)
    mc, mp = _mention_clause(f)
    total = conn.execute(f"SELECT count(*) FROM job j WHERE {jc}", jp).fetchone()[0]
    rows = conn.execute(
        f"SELECT m.skill_id, j.city, count(DISTINCT j.id) n FROM skill_mention m JOIN job j ON j.id = m.job_id"
        f" WHERE {jc} AND {mc} GROUP BY m.skill_id, j.city", jp + mp).fetchall()
    agg: dict[str, dict] = {}
    for r in rows:
        s = agg.setdefault(r["skill_id"], {"skill_id": r["skill_id"], "count": 0, "by_city": {}})
        s["count"] += r["n"]
        if r["city"]:
            s["by_city"][r["city"]] = s["by_city"].get(r["city"], 0) + r["n"]
    skills = sorted(agg.values(), key=lambda s: (-s["count"], s["skill_id"]))
    for s in skills:
        s["pct"] = round(100 * s["count"] / total, 1) if total else 0.0
    return {"total": total, "skills": skills}


def city_totals(conn: sqlite3.Connection, f: Filters, now: str) -> dict[str, int]:
    """Jobs per city in the filtered set — the denominators for compare mode."""
    jc, jp = job_set_clause(f, now)
    return {r["city"]: r["n"] for r in conn.execute(
        f"SELECT j.city, count(*) n FROM job j WHERE {jc} AND j.city IS NOT NULL GROUP BY j.city", jp)}


# --- jobs -------------------------------------------------------------------------------

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
              limit: int = 20, offset: int = 0) -> dict:
    jc, jp = job_set_clause(f, now, include_legacy=True)
    params = list(jp)
    where = [jc]
    if f.skill_id:
        mc, mp = _mention_clause(f)
        where.append(f"EXISTS (SELECT 1 FROM skill_mention m WHERE m.job_id = j.id AND m.skill_id = ? AND {mc})")
        params += [f.skill_id] + mp
    if f.query.strip():
        q = f"%{f.query.strip().lower()}%"
        where.append("(lower(j.company) LIKE ? OR lower(j.title) LIKE ?)")
        params += [q, q]
    w = " AND ".join(where)
    total = conn.execute(f"SELECT count(*) FROM job j WHERE {w}", params).fetchone()[0]
    order = SORTS.get(sort, SORTS["newest"])
    rows = conn.execute(
        f"SELECT j.id, j.company, j.title, j.city, j.seniority, j.seniority_basis, j.first_seen, j.last_seen,"
        f" j.repost_count, j.extracted_version, j.german, j.degree, j.degree_requirement, j.degree_or_equivalent"
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
    if ids:
        for s in conn.execute(
                f"SELECT job_id, skill_id, requirement FROM skill_mention"
                f" WHERE job_id IN ({','.join('?' * len(ids))}) ORDER BY skill_id", ids):
            skill_counts[s["job_id"]][s["requirement"]] += 1
            if s["requirement"] == "required":
                required[s["job_id"]].append(s["skill_id"])
    jobs = []
    for r in rows:
        d = dict(r)
        d["legacy"] = d.pop("extracted_version") == LEGACY_VERSION
        d["degree_or_equivalent"] = bool(d["degree_or_equivalent"])
        d["sources"] = srcs[r["id"]]
        d["status"] = _status(r, now, d["sources"])
        d["skill_counts"] = skill_counts[r["id"]]
        d["required_skills"] = required[r["id"]]  # ids only; the browser-side profile match uses them
        jobs.append(d)
    return {"total": total, "jobs": jobs, "limit": limit, "offset": offset}


def job_detail(conn: sqlite3.Connection, job_id: int, now: str) -> dict | None:
    r = conn.execute(
        "SELECT id, company, title, city, location_raw, seniority, seniority_basis, seniority_signal,"
        " german, german_basis, german_signal, degree, degree_requirement, degree_or_equivalent, degree_signal,"
        " first_seen, last_seen, repost_count, extracted_version FROM job WHERE id = ?", (job_id,)).fetchone()
    if not r:
        return None
    d = dict(r)
    d["sources"] = [dict(s) for s in conn.execute(
        "SELECT source, source_job_id, url, found_via, first_seen, last_seen, posted_at FROM job_source"
        " WHERE job_id = ? ORDER BY first_seen", (job_id,))]
    d["status"] = _status(r, now, d["sources"])
    d["legacy"] = d["extracted_version"] == LEGACY_VERSION
    d["degree_or_equivalent"] = bool(d["degree_or_equivalent"])
    d["skills"] = [dict(m) for m in conn.execute(
        "SELECT skill_id, requirement, raw_text FROM skill_mention WHERE job_id = ?"
        " ORDER BY requirement = 'required' DESC, skill_id", (job_id,))]
    d["proposed"] = [dict(p) for p in conn.execute(
        "SELECT id, label, raw_text, status FROM proposed_skill WHERE job_id = ? ORDER BY id", (job_id,))]
    d["has_screenshot"] = conn.execute("SELECT 1 FROM screenshot WHERE job_id = ?", (job_id,)).fetchone() is not None
    return d


# --- proposed skills ------------------------------------------------------------------

def proposed_skills(conn: sqlite3.Connection, status: str = "pending") -> list[dict]:
    """Grouped by label (case-insensitive): one row per label with every job that proposed it."""
    rows = conn.execute(
        "SELECT p.id, p.label, p.raw_text, p.status, p.resolved_skill_id, j.id job_id, j.company, j.title, j.city, j.first_seen"
        " FROM proposed_skill p JOIN job j ON j.id = p.job_id WHERE p.status = ? ORDER BY p.id", (status,)).fetchall()
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
