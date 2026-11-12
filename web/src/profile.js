// The "what does this mean for me" profile. Lives only in this browser (localStorage);
// the server never sees it. Shape: { role, seniority, german (bool: professional German),
// degree ('' | bachelor | master | phd), production (bool: has shipped to production),
// skills: [skill_id] }.
//
// Also the one place that answers "how well does this job fit me?": `gates`, `fit` and
// `rankJobs` are pure functions over a profile and a job as the API returns it, so the
// row badge, the ranking, alerts (HIR-19) and the Advisor all get the same answer. They
// fetch nothing, store nothing and do not reach the network; ranking has to happen here
// because the server is never told the profile.
//
// What they do NOT do: weight rare skills above common ones, estimate what a missing
// skill costs to learn, or look at proficiency (HIR-59). A gate is a yes/no on what the
// posting insists on; the score a badge shows is a plain ratio, and the score jobs are
// *ordered* by is the Wilson lower bound of that ratio taken against a floor of
// SKILL_FLOOR required skills, so both thin evidence and a thin posting sort lower.
import { useCallback, useEffect, useState } from "react";
import { DEGREE_RANK } from "./format.js";

const KEY = "hiring-radar.profile.v1";
export const EMPTY = { role: "AI engineer", seniority: "", german: false, degree: "", production: false, skills: [] };

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    const p = JSON.parse(raw);
    return { ...EMPTY, ...p, skills: Array.isArray(p.skills) ? p.skills : [] };
  } catch { return null; }
}

export function useProfile() {
  const [profile, setProfile] = useState(() => load());
  const save = useCallback((p) => {
    setProfile(p);
    try { if (p) localStorage.setItem(KEY, JSON.stringify(p)); else localStorage.removeItem(KEY); } catch {}
  }, []);
  useEffect(() => {
    const onStorage = (e) => { if (e.key === KEY) setProfile(load()); };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);
  return [profile, save];
}

// --- fit --------------------------------------------------------------------------------

// The hard asks a profile can fail. A gate is only a gate when the posting *insists*:
// "nice to have" never gates, and a job that names no level — in the body or the title —
// never gates on seniority (plenty of postings simply don't say). Order matters: it is the
// order a row names the reason in, so the most concrete ask comes first.
export const GATES = ["german", "production", "degree", "seniority"];

// Level words a title can carry. Whole words only, so "Internal Tools" is not an
// internship and "Leading" is not a Lead. These are the words HIR-113 lists and nothing
// more: the list is deliberately short, because a wrong guess here hides a job.
const SENIOR_TITLE = /\b(senior|staff|principal|lead|head)\b/i;
const JUNIOR_TITLE = /\b(junior|werkstudent|working student|intern)\b/i;

// The level a job names: the extractor's stored level when it found one, otherwise the
// title's own word. Returns null when nothing names a level, and also when the title names
// both ("Junior Lead") — ambiguous is as good as silent, and a null level never gates.
//
// The stored level wins on purpose. It was read from the whole posting, where the title is
// one line; when the two disagree the body is the better evidence (HIR-113).
export function jobSeniority(job) {
  if (job.seniority) return job.seniority;
  const title = job.title || "";
  const senior = SENIOR_TITLE.test(title);
  const junior = JUNIOR_TITLE.test(title);
  if (senior === junior) return null;
  return senior ? "senior" : "junior";
}

// Does this one hard ask rule the profile out? Pure; false whenever the ask is absent.
export function fails(profile, job, gate) {
  if (!profile) return false;
  if (gate === "german") return job.german === "required" && !profile.german;
  if (gate === "production") return job.production === "required" && !profile.production;
  if (gate === "degree") {
    const hard = job.degree_requirement === "required" && !job.degree_or_equivalent;
    return hard && DEGREE_RANK[profile.degree || ""] < DEGREE_RANK[job.degree];
  }
  if (gate === "seniority") {
    const level = jobSeniority(job);
    return Boolean(profile.seniority && level && level !== profile.seniority);
  }
  return false;
}

// Every hard ask this job makes that the profile fails, in GATES order.
export const gates = (profile, job) => GATES.filter((g) => fails(profile, job, g));

// A job's required and nice-to-have skill ids, from either shape the API returns: a list
// row (`required_skills` / `nice_skills` / `required_groups`) or a job detail (`skills`
// with `requirement` and `alternative_group`). `groups` lists the required skills that are
// alternatives to each other — "Python, Go or Java" — as arrays of two or more ids; every
// id in them is also in `required` (HIR-251).
export function skillSides(job) {
  if (job.skills) {
    const required = job.skills.filter((s) => s.requirement === "required");
    const byGroup = new Map();
    for (const s of required) {
      if (s.alternative_group == null) continue;
      if (!byGroup.has(s.alternative_group)) byGroup.set(s.alternative_group, []);
      byGroup.get(s.alternative_group).push(s.skill_id);
    }
    return {
      required: required.map((s) => s.skill_id),
      nice: job.skills.filter((s) => s.requirement !== "required").map((s) => s.skill_id),
      groups: [...byGroup.entries()].sort((a, b) => a[0] - b[0]).map(([, ids]) => ids).filter((ids) => ids.length > 1),
    };
  }
  return { required: job.required_skills || [], nice: job.nice_skills || [], groups: job.required_groups || [] };
}

// What the match counts as one requirement each: a skill asked for on its own (an id), or a
// group of alternatives (an array of ids), met by any one member. A posting asking for
// "Python, Rust, Go or Java" and Docker has two requirements, not five (DECISIONS 2026-11-11).
export function requirementUnits(job) {
  const { required, groups } = skillSides(job);
  const grouped = new Set(groups.flat());
  return [...required.filter((id) => !grouped.has(id)), ...groups];
}

const unitMet = (unit, have) => (Array.isArray(unit) ? unit.some((id) => have.has(id)) : have.has(unit));
// A group is as asked-for as its most asked-for member; ties break on its first id.
const unitDemand = (unit, demand) => (Array.isArray(unit) ? Math.max(...unit.map((id) => demand[id] || 0)) : demand[unit] || 0);
const unitKey = (unit) => (Array.isArray(unit) ? unit[0] : unit);

// The required skill ids that need no learning: the ones the profile has, plus every member
// of a group the profile meets through another member. The detail view marks the rest missing.
export function metSkills(profile, job) {
  const have = new Set(profile?.skills || []);
  const { required, groups } = skillSides(job);
  const met = new Set(required.filter((id) => have.has(id)));
  for (const g of groups) if (unitMet(g, have)) g.forEach((id) => met.add(id));
  return met;
}

// z for a 95% one-sided-ish normal interval. The number only has to be the same everywhere
// the ranking is computed; 1.96 is the conventional choice and the one PatternAI's eval
// rates already use, so the two read the same way.
const Z = 1.96;

// Where "too little was listed to read as a percentage" ends. A job listing fewer than
// this is scored as though it had listed this many and failed the rest, so "2/2" is judged
// as 2 out of 4: two required skills is usually what the extractor found, not what the
// posting asks. It is one number on purpose — the same threshold decides what the badge
// shows and what the ranking divides by, so a row never reads 100% while being held back
// with nothing on screen to say why (HIR-154).
//
// 4, meaning "few skills" is 3 or fewer (HIR-161, Chandler's call). It was 7, the measured
// median required-skill count, until a job listing 6 skills reading "6/6 · few skills
// listed" turned out to be the bug rather than an accepted side effect: six is a normal
// list. A constant, not a median recomputed per request — that would score the same job
// differently on page 1 and page 2. See DECISIONS.md: 4 is below the 5-to-8 band HIR-154
// measured, and the undo is restoring this to 7.
export const SKILL_FLOOR = 4;

// Is this job's required list too thin to read as a percentage — 3 or fewer asks? False
// for a job with no required skills at all: that is "unknown", and `score` is already null
// there.
export const thinlyListed = (total) => total > 0 && total < SKILL_FLOOR;

// The Wilson score interval's lower bound for `covered` successes out of `total`. Shrinks
// a ratio towards 0 by however little evidence stands behind it: 2/2 lands at 0.34 and
// 10/14 at 0.45, so the better-evidenced job sorts first. Returns null for total = 0,
// which is "unknown", not "no fit". Pure arithmetic — no clamping needed, the bound is in
// [0, 1] for any 0 <= covered <= total.
export function wilsonLower(covered, total, z = Z) {
  if (!total) return null;
  const p = covered / total;
  const z2 = z * z;
  const centre = p + z2 / (2 * total);
  const spread = z * Math.sqrt((p * (1 - p)) / total + z2 / (4 * total * total));
  return (centre - spread) / (1 + z2 / total);
}

// How well a job fits a profile. Returns null without a profile, otherwise
//   { score, rank_score, covered, total, thin, missing, gated_by }
// where `total` is the job's required-skill count, `covered` how many of them the profile
// has, `score` their ratio (null when the job has no required skills at all — a fragment
// or a legacy import — because 0/0 is "unknown", not "no fit"), `missing` the required
// skill ids the profile lacks, most-asked-for first — a group of alternatives counts as one
// requirement and appears in `missing` as an array of its ids (HIR-251) — and `gated_by` the first hard ask the
// profile fails, or null. A gate does not change the score: it says the score is moot.
//
// `rank_score` is what *orders* jobs: the Wilson lower bound of covered over
// max(total, SKILL_FLOOR) (null alongside a null `score`). `score` is what a badge
// *shows*. They differ on purpose — a 2/2 job has covered every skill it names, so its
// ratio really is 1, but it is scored as 2 out of 7 and sorts below a 5/8 one, because a
// posting that names two required skills has not told us enough to call it a match
// (HIR-113, tightened by HIR-154). Anything that ranks jobs — the list, alerts (HIR-19),
// the Advisor — sorts on `rank_score` so they all agree.
//
// `thin` says the job named fewer required skills than a posting normally does. It is why
// the row shows the count without a percentage and never says "full match": at this end
// of the scale the ratio is a fact about the extraction, not about the fit.
//
// `demand` maps a skill id to how many jobs ask for it, and only orders `missing`. Without
// it the ids keep the order they arrived in, so the result stays deterministic either way.
export function fit(profile, job, demand = null) {
  if (!profile) return null;
  const required = requirementUnits(job);
  const have = new Set(profile.skills);
  const missing = required.filter((unit) => !unitMet(unit, have));
  if (demand) {
    missing.sort((a, b) => {
      const ka = unitKey(a), kb = unitKey(b);
      return unitDemand(b, demand) - unitDemand(a, demand) || (ka < kb ? -1 : ka > kb ? 1 : 0);
    });
  }
  const covered = required.length - missing.length;
  return {
    score: required.length ? covered / required.length : null,
    rank_score: required.length ? wilsonLower(covered, Math.max(required.length, SKILL_FLOOR)) : null,
    covered,
    total: required.length,
    thin: thinlyListed(required.length),
    missing,
    gated_by: gates(profile, job)[0] || null,
  };
}

// A covered nice-to-have is worth a quarter of a covered required one.
const NICE_WEIGHT = 0.25;

// Sortable fit, lower sorts earlier: gated-out jobs last, then jobs with no required
// skills to judge, then the confidence-bounded score, and only then nice-to-have coverage.
//
// Nice-to-haves are a *separate, lower* term rather than part of the score, because the
// issue asks them to break ties and nothing more. Folded into one number they do more
// than that: a job asking two required skills you half cover, plus two nice-to-haves you
// have, would read 0.75 and outrank a job you cover 3 of 5 of — a worse fit shown first.
// So the ratio decides, and this only separates jobs the ratio leaves equal.
function sortKey(profile, job, f) {
  const { nice } = skillSides(job);
  const have = new Set(profile.skills);
  const coveredNice = nice.filter((id) => have.has(id)).length;
  const bonus = f.total ? (NICE_WEIGHT * coveredNice) / f.total : 0;
  return [f.gated_by ? 1 : 0, f.total ? 0 : 1, -(f.rank_score || 0), -bonus];
}

// Best fit first, over jobs already fetched and filtered. Stable: jobs that tie keep the
// order they came in (the server's newest-first), so the ranking is reproducible. Returns
// a new array and never mutates its input; without a profile it returns the jobs unchanged.
export function rankJobs(profile, jobs, demand = null) {
  if (!profile) return jobs;
  const keyed = jobs.map((job, i) => ({ job, i, key: sortKey(profile, job, fit(profile, job, demand)) }));
  keyed.sort((a, b) => {
    for (let k = 0; k < a.key.length; k++) if (a.key[k] !== b.key[k]) return a.key[k] - b.key[k];
    return a.i - b.i;
  });
  return keyed.map((x) => x.job);
}
