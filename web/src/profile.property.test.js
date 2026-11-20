// Rules the CV fit score and the ranking must keep for every profile and every job, not
// just the cases someone thought to write down (HIR-333). Each test states one rule and
// fast-check generates the profiles and jobs: both shapes the API returns (a list row and
// a job detail), groups of alternative skills, every hard ask, profiles with skills no job
// names.
//
// Every run tries the same 200 inputs per rule (a fixed seed), so a pull request never goes
// red on a bug it did not cause. HYPOTHESIS_PROFILE=sweep npm test is the by-hand search:
// 2000 random inputs per rule, different every run. It is the Python suite's variable, read
// here too so one setting drives both (AGENTS.md "Running and testing").
import { describe, expect, it } from "vitest";
import fc from "fast-check";
import { fitBadge } from "./JobList.jsx";
import { EMPTY, fit, rankJobs, skillSides, wilsonLower } from "./profile.js";

const SWEEP = process.env.HYPOTHESIS_PROFILE === "sweep";
const RUNS = SWEEP ? { numRuns: 2000 } : { numRuns: 200, seed: 333 };
const check = (property) => fc.assert(property, RUNS);

const SKILLS = ["python", "rag", "aws", "docker", "sql", "llm", "go", "rust"];
const skillSet = (max = SKILLS.length) => fc.uniqueArray(fc.constantFrom(...SKILLS), { maxLength: max });
const ask = fc.constantFrom(null, "required", "nice_to_have");

const hardAsks = {
  title: fc.constantFrom("AI Engineer", "Senior AI Engineer", "Junior Lead", "Werkstudent KI", ""),
  seniority: fc.constantFrom(null, "junior", "mid", "senior"),
  german: ask,
  production: ask,
  degree: fc.constantFrom(null, "bachelor", "master", "phd"),
  degree_requirement: ask,
  degree_or_equivalent: fc.boolean(),
};

// A job as the job list returns it. Groups of alternatives are cut from the required ids,
// two or more each and never overlapping, as the API builds them.
const listJob = fc.record({
  ...hardAsks,
  required_skills: skillSet(),
  nice_skills: skillSet(4),
  cuts: fc.array(fc.integer({ min: 2, max: 3 }), { maxLength: 2 }),
}).map(({ cuts, ...job }) => {
  const groups = [];
  let at = 0;
  for (const size of cuts) {
    if (at + size > job.required_skills.length) break;
    groups.push(job.required_skills.slice(at, at + size));
    at += size;
  }
  return { ...job, required_groups: groups };
});

// The same job as the detail view returns it: one `skills` list, each with its side and
// the group of alternatives it belongs to, if any.
const detailJob = fc.record({
  ...hardAsks,
  skills: fc.uniqueArray(
    fc.record({
      skill_id: fc.constantFrom(...SKILLS),
      requirement: fc.constantFrom("required", "required", "nice_to_have"),
      alternative_group: fc.constantFrom(null, null, 1, 2),
    }),
    { selector: (s) => s.skill_id, maxLength: SKILLS.length },
  ),
});

const job = fc.oneof(listJob, detailJob);

const profile = fc.record({
  skills: fc.uniqueArray(fc.constantFrom(...SKILLS, "cobol"), { maxLength: SKILLS.length + 1 }),
  seniority: fc.constantFrom("", "junior", "mid", "senior"),
  german: fc.boolean(),
  production: fc.boolean(),
  degree: fc.constantFrom("", "bachelor", "master", "phd"),
}).map((p) => ({ ...EMPTY, ...p }));

// How often the jobs ask for each skill; it only orders the missing list, so it must not
// move a score.
const demand = fc.option(fc.dictionary(fc.constantFrom(...SKILLS), fc.nat(500)), { nil: null });

describe("the fit score, for any profile and job", () => {
  it("is always between 0 and 100%", () => {
    check(fc.property(profile, job, demand, (me, j, d) => {
      const f = fit(me, j, d);
      expect(f.covered).toBeGreaterThanOrEqual(0);
      expect(f.covered).toBeLessThanOrEqual(f.total);
      expect(f.covered + f.missing.length).toBe(f.total);
      if (f.total === 0) {
        // No required skills: unknown, never 0% and never 100%.
        expect(f.score).toBeNull();
        expect(f.rank_score).toBeNull();
        return;
      }
      for (const score of [f.score, f.rank_score]) {
        expect(score).toBeGreaterThanOrEqual(0);
        expect(score).toBeLessThanOrEqual(1);
      }
      // What the row prints: a whole percentage from 0 to 100, when it prints one at all.
      const shown = /^(\d+)%/.exec(fitBadge(f));
      expect(f.thin || shown !== null).toBe(true);
      if (shown) expect(Number(shown[1])).toBeLessThanOrEqual(100);
    }));
  });

  it("the score jobs are ordered by stays between 0 and 1 for any count", () => {
    check(fc.property(fc.integer({ min: 1, max: 500 }), fc.nat(500), (total, n) => {
      const covered = n % (total + 1);
      const score = wilsonLower(covered, total);
      expect(score).toBeGreaterThanOrEqual(0);
      expect(score).toBeLessThanOrEqual(1);
      // ...and never above the plain ratio: it only ever pulls a score down.
      expect(score).toBeLessThanOrEqual(covered / total + 1e-12);
    }));
  });

  it("never falls when the profile gains a skill the job requires", () => {
    check(fc.property(profile, job, demand, fc.nat(), (me, j, d, pick) => {
      const required = skillSides(j).required;
      fc.pre(required.length > 0);
      const gained = required[pick % required.length];
      const before = fit(me, j, d);
      const after = fit({ ...me, skills: [...me.skills, gained] }, j, d);
      expect(after.total).toBe(before.total);
      expect(after.covered).toBeGreaterThanOrEqual(before.covered);
      expect(after.score).toBeGreaterThanOrEqual(before.score);
      expect(after.rank_score).toBeGreaterThanOrEqual(before.rank_score);
      // A skill does not change a hard ask.
      expect(after.gated_by).toBe(before.gated_by);
    }));
  });
});

describe("ranking, for any profile and list of jobs", () => {
  // A few distinct jobs, then a list that repeats them: identical jobs are the one case
  // where the scores are certain to be equal, whatever goes into a score.
  const jobList = fc.tuple(fc.array(job, { minLength: 1, maxLength: 5 }), fc.array(fc.nat(4), { maxLength: 25 }))
    .map(([kinds, picks]) => picks.map((p, i) => ({ ...kinds[p % kinds.length], id: i, kind: p % kinds.length })));

  it("never loses or duplicates a job", () => {
    check(fc.property(profile, jobList, demand, (me, jobs, d) => {
      const before = [...jobs];
      const ranked = rankJobs(me, jobs, d);
      expect(ranked).toHaveLength(jobs.length);
      expect(new Set(ranked).size).toBe(jobs.length);
      for (const j of jobs) expect(ranked).toContain(j);
      // The list it was given is left exactly as it was.
      expect(jobs).toEqual(before);
      jobs.forEach((j, i) => expect(j).toBe(before[i]));
    }));
  });

  it("keeps jobs with equal scores in the order they came in", () => {
    check(fc.property(profile, jobList, demand, (me, jobs, d) => {
      const ranked = rankJobs(me, jobs, d);
      const lastSeen = new Map();
      for (const j of ranked) {
        if (lastSeen.has(j.kind)) expect(j.id).toBeGreaterThan(lastSeen.get(j.kind));
        lastSeen.set(j.kind, j.id);
      }
    }));
  });

  it("returns the jobs untouched when there is no profile", () => {
    check(fc.property(jobList, (jobs) => {
      expect(rankJobs(null, jobs)).toBe(jobs);
    }));
  });
});
