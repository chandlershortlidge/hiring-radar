import math
import re
from datetime import datetime, timedelta

# 1.96 is the conventional choice for about 95% confidence. The exact number
# matters less than using the same one everywhere jobs are ranked, so it is
# a named constant: change it here and every ranking changes together.

Z = 1.96
def confidence_adjusted_score(covered, total, z=Z):
    """Score how well a CV covers a job's required skills, allowing for how little evidence there is.

    The score is the lowest the true coverage ratio could plausibly be, given
    how many skills we actually counted. With few skills the score is pulled
    down: 2 of 2 covered scores well below 1, while 20 of 20 scores close to 1.
    This stops a job with only a couple of listed skills from looking like a
    perfect match.

    Args:
        covered: how many of the job's required skills the CV covers.
        total: how many required skills the job lists.
        z: how cautious to be. The default, 1.96, means we are about 95%
            sure the true ratio is at least the score. A larger z is more
            cautious.

    Returns:
        A number from 0 to 1, where higher means a better match. None when
        total is 0, because there is no evidence to score.
    """
    if total == 0:
        return None
    p = covered / total
    z2 = z * z
    centre = p + z2 / (2 * total)
    spread = z * math.sqrt((p * (1 - p)) / total + z2 / (4 * total * total))
    return (centre - spread) / (1 + z2 / total)


SKILLS_FLOOR = 4
def are_job_skills_thinly_listed(skill_count):
    """Say whether a job lists too few required skills to be ranked on its own numbers.

    Example: a job listing 3 skills is thinly listed, because the floor is 4.
    A job listing 4 skills is not.

    Args:
        skill_count: how many required skills the job lists.

    Returns:
        True when the job lists at least 1 skill and fewer than the skill floor, 4.
        False otherwise. A job listing 0 skills is False: that is "unknown",
        a different case from a short list.
    """
    if skill_count == 0:
        return False
    if skill_count < SKILLS_FLOOR:
        return True

    return False 


def skills_rank_scorer(covered, total):
    """Score a job for ranking, so a job with only a few listed skills cannot look perfect.

    A job listing fewer skills than the floor is scored as if it listed
    4 skills: 2 of 2 is scored as 2 of 4. A job at or above the floor is
    scored on its own numbers. The score itself comes from
    confidence_adjusted_score.

    Args:
        covered: how many of the job's required skills the CV covers.
        total: how many required skills the job lists.

    Returns:
        A number from 0 to 1, where higher means a better match. None when
        total is 0, because there is no evidence to score.
    """
    if total == 0:
        return None
    if total <= SKILLS_FLOOR:
        return confidence_adjusted_score(covered, SKILLS_FLOOR)
    return confidence_adjusted_score(covered, total)


# --- the rest of the browser's fit logic (HIR-435) -------------------------------------
#
# A line-for-line port of web/src/profile.js, so the match_profile MCP tool ranks jobs
# exactly as the dashboard's "Best fit" sort does. tests/fixtures/fit_cases.json holds
# profiles, jobs and the answers both sides must give; web/src/fitCases.test.js and
# tests/test_fit_cases.py both read it, so a change on one side fails the other's tests.
#
# A profile is a dict shaped like the browser's: {"skills": [skill ids], "seniority":
# "" | junior | mid | senior, "german": bool, "production": bool, "degree": "" | bachelor
# | master | phd}. A job is a dict as app/queries.py's list_jobs returns it (or a job
# detail, with "skills"). Nothing here reads the database, the clock or the network.

# The hard asks a profile can fail, in the order a job names the reason in.
GATES = ("german", "production", "degree", "seniority")

# The same ranks as web/src/format.js's DEGREE_RANK.
DEGREE_RANK = {"": 0, "bachelor": 1, "master": 2, "phd": 3}

# Level words a title can carry, whole words only (HIR-113): the browser's two lists.
SENIOR_TITLE = re.compile(r"\b(senior|staff|principal|lead|head)\b", re.IGNORECASE)
JUNIOR_TITLE = re.compile(r"\b(junior|werkstudent|working student|intern)\b", re.IGNORECASE)

# A covered nice-to-have is worth a quarter of a covered required one, and only breaks ties.
NICE_WEIGHT = 0.25

# Best fit only ranks jobs first seen in the last FIT_DAYS days (HIR-391).
FIT_DAYS = 30

# The share of required skills a profile must cover for a job to count as a match (HIR-16).
MATCH_PCT = 70


def job_seniority(job):
    """The level a job names: its stored level, else the title's own word, else None.

    A title naming both a senior and a junior word ("Junior Lead") is None, like silence.
    """
    if job.get("seniority"):
        return job["seniority"]
    title = job.get("title") or ""
    senior = bool(SENIOR_TITLE.search(title))
    junior = bool(JUNIOR_TITLE.search(title))
    if senior == junior:
        return None
    return "senior" if senior else "junior"


def fails(profile, job, gate):
    """Whether this one hard ask rules the profile out. False whenever the ask is absent."""
    if not profile:
        return False
    if gate == "german":
        return job.get("german") == "required" and not profile.get("german")
    if gate == "production":
        return job.get("production") == "required" and not profile.get("production")
    if gate == "degree":
        hard = job.get("degree_requirement") == "required" and not job.get("degree_or_equivalent")
        asked = DEGREE_RANK.get(job.get("degree"))
        has = DEGREE_RANK.get(profile.get("degree") or "")
        return bool(hard and asked is not None and has is not None and has < asked)
    if gate == "seniority":
        level = job_seniority(job)
        return bool(profile.get("seniority") and level and level != profile["seniority"])
    return False


def gates(profile, job):
    """Every hard ask this job makes that the profile fails, in GATES order."""
    return [g for g in GATES if fails(profile, job, g)]


def skill_sides(job):
    """A job's required ids, nice-to-have ids and groups of alternative required ids.

    Reads a list row (required_skills / nice_skills / required_groups) or a job detail
    (skills, each with requirement and alternative_group). Every id in a group is also in
    required; a group has two or more ids (HIR-251).
    """
    if job.get("skills") is not None:  # as in JS, an empty list is still the detail shape
        required = [s for s in job["skills"] if s["requirement"] == "required"]
        by_group = {}
        for s in required:
            if s.get("alternative_group") is not None:
                by_group.setdefault(s["alternative_group"], []).append(s["skill_id"])
        return {
            "required": [s["skill_id"] for s in required],
            "nice": [s["skill_id"] for s in job["skills"] if s["requirement"] != "required"],
            "groups": [ids for _, ids in sorted(by_group.items()) if len(ids) > 1],
        }
    return {"required": job.get("required_skills") or [], "nice": job.get("nice_skills") or [],
            "groups": job.get("required_groups") or []}


def requirement_units(job):
    """What the match counts as one requirement each: a lone skill id, or a group (a list
    of ids) met by any one member. "Python, Go or Java" and Docker are two requirements."""
    sides = skill_sides(job)
    grouped = {sid for g in sides["groups"] for sid in g}
    return [sid for sid in sides["required"] if sid not in grouped] + [list(g) for g in sides["groups"]]


def _unit_met(unit, have):
    return any(sid in have for sid in unit) if isinstance(unit, list) else unit in have


def _unit_demand(unit, demand):
    if isinstance(unit, list):
        return max(demand.get(sid) or 0 for sid in unit)
    return demand.get(unit) or 0


def _unit_key(unit):
    return unit[0] if isinstance(unit, list) else unit


def met_skills(profile, job):
    """The required ids that need no learning: those the profile has, plus every member of
    a group the profile meets through another member."""
    have = set((profile or {}).get("skills") or [])
    sides = skill_sides(job)
    met = {sid for sid in sides["required"] if sid in have}
    for g in sides["groups"]:
        if _unit_met(g, have):
            met.update(g)
    return met


def fit(profile, job, demand=None):
    """How well a job fits a profile, as the dashboard's badge and ranking read it.

    None without a profile, else {score, rank_score, covered, total, thin, missing,
    gated_by}: score is covered / total (None when the job lists no required skill),
    rank_score is what orders jobs (skills_rank_scorer: thin evidence and thin postings
    sort lower), missing the unmet requirements, most asked-for first when demand (skill
    id -> how many jobs ask for it) is given, and gated_by the first hard ask the profile
    fails, or None. A gate does not change the score.
    """
    if not profile:
        return None
    required = requirement_units(job)
    have = set(profile.get("skills") or [])
    missing = [u for u in required if not _unit_met(u, have)]
    if demand:
        missing.sort(key=lambda u: (-_unit_demand(u, demand), _unit_key(u)))
    covered = len(required) - len(missing)
    total = len(required)
    # Nothing covered is exactly 0, as in the browser (HIR-333): the formula gives 0 there
    # only up to floating-point noise, which would order the jobs the profile covers none of.
    rank_score = None if not total else 0.0 if covered == 0 else skills_rank_scorer(covered, total)
    failed = gates(profile, job)
    return {
        "score": covered / total if total else None,
        "rank_score": rank_score,
        "covered": covered,
        "total": total,
        "thin": are_job_skills_thinly_listed(total),
        "missing": missing,
        "gated_by": failed[0] if failed else None,
    }


def _sort_key(profile, job, f):
    # Lower sorts earlier: gated jobs last, then jobs with no required skill to judge, then
    # rank_score, and nice-to-have coverage only to break what rank_score leaves equal.
    have = set(profile.get("skills") or [])
    covered_nice = sum(1 for sid in skill_sides(job)["nice"] if sid in have)
    bonus = NICE_WEIGHT * covered_nice / f["total"] if f["total"] else 0
    return (1 if f["gated_by"] else 0, 0 if f["total"] else 1, -(f["rank_score"] or 0), -bonus)


def rank_jobs(profile, jobs, demand=None):
    """Best fit first. Stable, so ties keep the order given (newest first from list_jobs).
    Returns a new list; without a profile, the jobs unchanged."""
    if not profile:
        return jobs
    return sorted(jobs, key=lambda j: _sort_key(profile, j, fit(profile, j, demand)))


def _instant(iso):
    try:
        t = datetime.fromisoformat(iso)
    except (TypeError, ValueError):
        return None
    return t if t.tzinfo else None  # the browser would read a zoneless time as local: refuse it


def recent_jobs(jobs, now, days=FIT_DAYS):
    """The jobs first seen in the last `days` days before `now` (an ISO time), in order.
    A job first seen exactly `days` days ago is in; one with no readable date is out."""
    at = _instant(now)
    if at is None:
        return []
    out = []
    for job in jobs:
        seen = _instant(job.get("first_seen"))
        if seen is not None and at - seen <= timedelta(days=days):
            out.append(job)
    return out


def is_match(profile, job):
    """Whether the profile covers at least MATCH_PCT% of the job's required skills. False
    for a job with no required skill or a thinly listed one; gates do not change it."""
    f = fit(profile, job)
    return bool(f and f["total"] and not f["thin"] and f["covered"] * 100 >= f["total"] * MATCH_PCT)
