// The fit rules of HIR-51, on the pure functions only: a gate beats any score, the
// nice-to-have tie-break, and a job with no required skills to judge. No DOM, no network,
// no localStorage — these are the functions alerts and the Advisor will reuse.
import { describe, expect, it } from "vitest";
import { EMPTY, SKILL_FLOOR, fails, fit, gates, jobSeniority, rankJobs, skillSides, thinlyListed, wilsonLower } from "./profile.js";

const me = (p = {}) => ({ ...EMPTY, seniority: "mid", skills: ["python", "rag"], ...p });

// A list row as /api/jobs returns it, with only the fields fit() reads.
const job = (o = {}) => ({
  id: 1, title: "AI Engineer", required_skills: [], nice_skills: [], german: null, production: null,
  degree: null, degree_requirement: null, degree_or_equivalent: false, seniority: null, ...o,
});

describe("fit", () => {
  it("is null without a profile, so a visitor who set none sees no badge", () => {
    expect(fit(null, job({ required_skills: ["python"] }))).toBe(null);
  });

  it("scores covered required skills as a ratio and lists what is missing", () => {
    const f = fit(me(), job({ required_skills: ["python", "rag", "aws", "docker"] }));
    expect(f.covered).toBe(2);
    expect(f.total).toBe(4);
    expect(f.score).toBe(0.5);
    expect(f.missing).toEqual(["aws", "docker"]);
    expect(f.gated_by).toBe(null);
  });

  it("orders the missing skills most-asked-for first, and ties by id", () => {
    const j = job({ required_skills: ["aws", "docker", "kafka"] });
    expect(fit(me(), j, { docker: 90, aws: 12, kafka: 12 }).missing).toEqual(["docker", "aws", "kafka"]);
    // Without demand counts the ids keep the order the server sent them in.
    expect(fit(me(), j).missing).toEqual(["aws", "docker", "kafka"]);
  });

  it("ties missing skills alphabetically by id, not by the order they arrived in", () => {
    // Deliberately not alphabetical, and not the order the test above happens to use, so a
    // tie-break that silently fell back to input order instead of comparing ids could not
    // slip past by coincidence.
    const j = job({ required_skills: ["kafka", "aws"] });
    expect(fit(me(), j, { kafka: 12, aws: 12 }).missing).toEqual(["aws", "kafka"]);
  });

  it("calls a job with no required skills unknown, not a zero fit", () => {
    const f = fit(me(), job({ nice_skills: ["python"] }));
    expect(f.score).toBe(null);
    expect(f.total).toBe(0);
    expect(f.covered).toBe(0);
    expect(f.missing).toEqual([]);
  });

  it("ignores nice-to-have skills in the score", () => {
    const f = fit(me(), job({ required_skills: ["python"], nice_skills: ["aws"] }));
    expect(f.score).toBe(1);
    expect(f.total).toBe(1);
  });

  it("reads a job detail's skills list as well as a list row's ids", () => {
    const detail = { skills: [
      { skill_id: "python", requirement: "required" },
      { skill_id: "aws", requirement: "nice_to_have" },
    ] };
    expect(skillSides(detail)).toEqual({ required: ["python"], nice: ["aws"] });
    expect(fit(me(), detail).score).toBe(1);
  });
});

describe("gates", () => {
  it("gates on German, production and a degree only when the posting insists", () => {
    expect(gates(me(), job({ german: "required" }))).toEqual(["german"]);
    expect(gates(me(), job({ german: "nice_to_have" }))).toEqual([]);
    expect(gates(me({ german: true }), job({ german: "required" }))).toEqual([]);

    expect(gates(me(), job({ production: "required" }))).toEqual(["production"]);
    expect(gates(me(), job({ production: "nice_to_have" }))).toEqual([]);
    expect(gates(me({ production: true }), job({ production: "required" }))).toEqual([]);

    const phd = { degree: "phd", degree_requirement: "required" };
    expect(gates(me(), job(phd))).toEqual(["degree"]);
    expect(gates(me({ degree: "phd" }), job(phd))).toEqual([]);
    expect(gates(me(), job({ ...phd, degree_or_equivalent: true }))).toEqual([]);
    expect(gates(me(), job({ ...phd, degree_requirement: "nice_to_have" }))).toEqual([]);
    // A master's clears a bachelor's ask; a bachelor's does not clear a master's.
    expect(gates(me({ degree: "master" }), job({ degree: "bachelor", degree_requirement: "required" }))).toEqual([]);
    expect(gates(me({ degree: "bachelor" }), job({ degree: "master", degree_requirement: "required" }))).toEqual(["degree"]);
  });

  it("gates on a level only when both sides name one", () => {
    expect(gates(me(), job({ seniority: "senior" }))).toEqual(["seniority"]);
    expect(gates(me(), job({ seniority: "mid" }))).toEqual([]);
    expect(gates(me(), job({ seniority: null }))).toEqual([]);          // the job names no level
    expect(gates(me({ seniority: "" }), job({ seniority: "senior" }))).toEqual([]);  // nor does the profile
  });

  // HIR-113: the extractor leaves plenty of senior postings at null, and HIR-51's "a job
  // that names no level never gates" let them sit at the top of a Mid profile's list.
  it("falls back to the title when the posting stores no level", () => {
    const titled = (t) => job({ seniority: null, title: t });
    for (const t of [
      "(Senior) AI Web & GTM Engineer (f/m/d)",
      "Senior Consultant AI Engineer",
      "Staff Engineer, Künstliche Intelligenz Ingenieur",
      "Principal Software Engineer - Machine Learning",
      "AI Engineer Team Lead (all genders)",
      "Head of AI Engineering",
    ]) {
      expect(gates(me(), titled(t))).toEqual(["seniority"]);
      expect(jobSeniority(titled(t))).toBe("senior");
    }
  });

  it("reads a junior title the same way, so a Mid profile is not shown internships", () => {
    for (const t of ["Junior AI Engineer", "Werkstudent Machine Learning", "Working Student AI", "Intern, AI Engineering"]) {
      expect(jobSeniority(job({ title: t }))).toBe("junior");
      expect(gates(me(), job({ title: t }))).toEqual(["seniority"]);
    }
    // A junior title does gate a junior profile out of nothing.
    expect(gates(me({ seniority: "junior" }), job({ title: "Junior AI Engineer" }))).toEqual([]);
  });

  it("matches level words only as whole words, so ordinary titles still name no level", () => {
    for (const t of ["AI Engineer", "Machine Learning Engineer (m/w/d)", "Internal Tools Engineer", "Leading Edge AI Developer"]) {
      expect(jobSeniority(job({ title: t }))).toBe(null);
      expect(gates(me(), job({ title: t }))).toEqual([]);
    }
  });

  it("lets a stored level win over the title, because the body is the better evidence", () => {
    const j = job({ seniority: "mid", title: "(Senior) AI Web & GTM Engineer" });
    expect(jobSeniority(j)).toBe("mid");
    expect(gates(me(), j)).toEqual([]);
    expect(gates(me({ seniority: "senior" }), j)).toEqual(["seniority"]);
  });

  it("treats a title naming two levels as naming none", () => {
    expect(jobSeniority(job({ title: "Junior to Lead AI Engineer" }))).toBe(null);
    expect(gates(me(), job({ title: "Junior to Lead AI Engineer" }))).toEqual([]);
  });

  it("never gates on a title when the profile targets no level", () => {
    expect(gates(me({ seniority: "" }), job({ title: "Senior AI Engineer" }))).toEqual([]);
    expect(gates(me({ seniority: "" }), job({ title: "Werkstudent AI" }))).toEqual([]);
  });

  it("survives a job with no title at all", () => {
    const j = job({ title: undefined });
    expect(jobSeniority(j)).toBe(null);
    expect(gates(me(), j)).toEqual([]);
  });

  it("names every failed ask in order, and fit reports the first", () => {
    const hard = job({ german: "required", production: "required", seniority: "senior", required_skills: ["python"] });
    expect(gates(me(), hard)).toEqual(["german", "production", "seniority"]);
    expect(fit(me(), hard).gated_by).toBe("german");
  });

  it("gates nothing without a profile", () => {
    expect(fails(null, job({ german: "required" }), "german")).toBe(false);
    expect(gates(null, job({ german: "required" }))).toEqual([]);
  });

  it("fires no gate for an unrecognized gate name, even when every real check would fail", () => {
    // Pins that each branch above is its own `gate === "..."` guard, not a catch-all that
    // could be forced on -- the seniority check only ever applies to the seniority gate.
    const demanding = job({ seniority: "senior", german: "required", production: "required" });
    expect(fails(me(), demanding, "not-a-real-gate")).toBe(false);
  });
});

// HIR-113: the order is the Wilson lower bound of covered/total, not the raw ratio, so a
// perfect score off two skills stops beating a near-perfect one off fourteen.
describe("wilsonLower", () => {
  it("shrinks a ratio by how little evidence stands behind it", () => {
    expect(wilsonLower(10, 14)).toBeCloseTo(0.4535, 3);
    expect(wilsonLower(6, 8)).toBeCloseTo(0.4091, 3);
    expect(wilsonLower(2, 2)).toBeCloseTo(0.3424, 3);
    // ...which is the whole point: the raw ratios run the other way.
    expect(wilsonLower(10, 14)).toBeGreaterThan(wilsonLower(6, 8));
    expect(wilsonLower(6, 8)).toBeGreaterThan(wilsonLower(2, 2));
  });

  it("is unknown with nothing to judge, and bottoms out when nothing is covered", () => {
    expect(wilsonLower(0, 0)).toBe(null);
    expect(wilsonLower(0, 3)).toBeCloseTo(0, 10);
    expect(wilsonLower(0, 14)).toBeCloseTo(0, 10);
  });

  it("stays inside [0, 1], and rises with evidence at an unchanged ratio", () => {
    expect(wilsonLower(1, 1)).toBeGreaterThan(0);
    expect(wilsonLower(1, 1)).toBeLessThan(1);
    expect(wilsonLower(20, 20)).toBeGreaterThan(wilsonLower(2, 2));
    expect(wilsonLower(50, 100)).toBeGreaterThan(wilsonLower(5, 10));
  });
});

// HIR-154: a job is scored against max(total, SKILL_FLOOR), so a posting that lists two
// required skills is judged as though it had listed SKILL_FLOOR and failed the rest.
// HIR-161 moved SKILL_FLOOR from 7 to 4, so "thin" is 3 asks or fewer. The threshold is
// asserted in absolute counts as well as in SKILL_FLOOR, because an assertion written only
// as SKILL_FLOOR - 1 holds at every threshold, including the 7 that was the bug.
describe("the skill floor", () => {
  const fitJob = (id, covered, total) => job({
    id,
    required_skills: [
      ...Array.from({ length: covered }, (_, i) => `have${i}`),
      ...Array.from({ length: total - covered }, (_, i) => `lack${i}`),
    ],
  });
  const haveAll = me({ skills: Array.from({ length: 40 }, (_, i) => `have${i}`) });
  const rank = (covered, total) => fit(haveAll, fitJob(1, covered, total)).rank_score;
  const ids = (jobs) => jobs.map((j) => j.id);

  it("marks a job below the floor thin, and leaves a full list alone", () => {
    expect(thinlyListed(2)).toBe(true);
    expect(thinlyListed(SKILL_FLOOR - 1)).toBe(true);
    expect(thinlyListed(SKILL_FLOOR)).toBe(false);
    expect(thinlyListed(20)).toBe(false);
    // HIR-161, in the numbers the decision is written in: the line sits between 3 and 4.
    expect(thinlyListed(3)).toBe(true);
    expect(thinlyListed(4)).toBe(false);
    expect(thinlyListed(6)).toBe(false);
    // Nothing listed at all is "unknown", not thin: score and rank_score are already null.
    expect(thinlyListed(0)).toBe(false);
    const nothing = fit(haveAll, job({ id: 1 }));
    expect(nothing.thin).toBe(false);
    expect(nothing.score).toBe(null);
    expect(nothing.rank_score).toBe(null);
  });

  it("scores a thin job against the floor, and a full one against its own list", () => {
    expect(rank(2, 2)).toBeCloseTo(wilsonLower(2, SKILL_FLOOR), 10);
    expect(rank(3, 3)).toBeCloseTo(wilsonLower(3, SKILL_FLOOR), 10);
    // From the floor up the denominator is the job's own count: the floor only ever
    // lowers a score, never raises one.
    expect(rank(7, 7)).toBeCloseTo(wilsonLower(7, 7), 10);
    expect(rank(10, 14)).toBeCloseTo(wilsonLower(10, 14), 10);
    expect(rank(2, 2)).toBeLessThan(wilsonLower(2, 2));
  });

  it("puts a partly covered fuller posting above a thin one it covers completely", () => {
    // The San Francisco complaint: "100% · 2/2" rows sitting above real matches.
    expect(ids(rankJobs(haveAll, [fitJob(1, 2, 2), fitJob(2, 5, 8)]))).toEqual([2, 1]);
    expect(ids(rankJobs(haveAll, [fitJob(1, 3, 3), fitJob(2, 5, 7)]))).toEqual([2, 1]);
    expect(ids(rankJobs(haveAll, [fitJob(1, 3, 3), fitJob(2, 6, 10)]))).toEqual([2, 1]);
  });

  // HIR-161, and the price of it, pinned so it is a decision rather than a surprise: at
  // the old floor of 7 a 4/4 posting was thin and sorted below 6/10. Four asks is a normal
  // list now, so it ranks on its own ratio and wins. This is the intended consequence of
  // "jobs with 4 or more rank by Best fit like any other job"; it is also the residue of
  // the HIR-154 complaint, which was about 2/2 and 3/3 rows, and those still sort below.
  it("lets a 4-ask posting you cover in full rank on its own ratio", () => {
    expect(ids(rankJobs(haveAll, [fitJob(1, 4, 4), fitJob(2, 6, 10)]))).toEqual([1, 2]);
    expect(rank(4, 4)).toBeCloseTo(wilsonLower(4, 4), 10);
    expect(rank(5, 5)).toBeCloseTo(wilsonLower(5, 5), 10);
    // ...while 3 asks and fewer stay floored, so they cannot read as perfect matches.
    expect(rank(3, 3)).toBeCloseTo(wilsonLower(3, SKILL_FLOOR), 10);
    expect(rank(3, 3)).toBeLessThan(wilsonLower(3, 3));
  });

  it("never ranks a thin job above a full match of the floor or more — the issue's bar", () => {
    // Over every pair the data can produce, not a hand-picked few: any thin job, against
    // any job that lists at least the floor and covers all of it.
    for (let total = 1; total < SKILL_FLOOR; total++) {
      for (let covered = 0; covered <= total; covered++) {
        for (let full = SKILL_FLOOR; full <= 30; full++) {
          expect(rank(covered, total)).toBeLessThan(rank(full, full));
        }
      }
    }
  });

  it("still separates two thin jobs by how much of each you cover", () => {
    expect(rank(3, 3)).toBeGreaterThan(rank(2, 2));
    expect(rank(2, 4)).toBeGreaterThan(rank(1, 4));
    expect(ids(rankJobs(haveAll, [fitJob(1, 1, 2), fitJob(2, 3, 3)]))).toEqual([2, 1]);
  });
});

describe("rankJobs", () => {
  const ids = (jobs) => jobs.map((j) => j.id);

  // A job asking `total` required skills of which the profile below covers `covered`.
  const fitJob = (id, covered, total, o = {}) => job({
    id,
    required_skills: [
      ...Array.from({ length: covered }, (_, i) => `have${i}`),
      ...Array.from({ length: total - covered }, (_, i) => `lack${i}`),
    ],
    ...o,
  });
  const haveAll = me({ skills: Array.from({ length: 12 }, (_, i) => `have${i}`) });

  it("ranks better-evidenced coverage first, so 2/2 no longer tops the list (HIR-113)", () => {
    // The live screenshot's three rows: Pentadoc 2/2, PharmaHera 6/8, Deloitte 10/14.
    expect(ids(rankJobs(haveAll, [fitJob(1, 2, 2), fitJob(2, 6, 8), fitJob(3, 10, 14)]))).toEqual([3, 2, 1]);
    // The ratio a badge shows is untouched: the 2/2 job really does cover both its asks.
    const f = fit(haveAll, fitJob(1, 2, 2));
    expect(f.score).toBe(1);
    expect(f.covered).toBe(2);
    expect(f.total).toBe(2);
    // ...but it is scored as 2 out of SKILL_FLOOR, not 2 out of 2 (HIR-154). Before the
    // floor this was 0.3424, the bound of a true 2/2, which beat every partly covered job.
    // 0.1500 is the bound of 2 out of 4; it was 0.0822 at the floor of 7 (HIR-161).
    expect(f.rank_score).toBeCloseTo(wilsonLower(2, SKILL_FLOOR), 10);
    expect(f.rank_score).toBeCloseTo(0.1500, 3);
    expect(f.thin).toBe(true);
  });

  it("still puts a gated-out job last, however well evidenced its coverage", () => {
    const jobs = [fitJob(1, 10, 14), fitJob(2, 10, 10, { german: "required" })];
    expect(ids(rankJobs(haveAll, jobs))).toEqual([1, 2]);
  });

  it("sorts a job covering none of its required skills below any job covering some", () => {
    const jobs = [fitJob(1, 0, 5), fitJob(2, 1, 20), job({ id: 3, nice_skills: ["have0"] })];
    expect(ids(rankJobs(haveAll, jobs))).toEqual([2, 1, 3]);
  });

  it("keeps the order it was given when two jobs share a bound", () => {
    const jobs = [fitJob(7, 3, 4), fitJob(4, 3, 4), fitJob(9, 3, 4)];
    expect(ids(rankJobs(haveAll, jobs))).toEqual([7, 4, 9]);
  });

  it("puts a gated-out job below every job still in reach, however well it scores", () => {
    const perfect_but_german = job({ id: 1, required_skills: ["python", "rag"], german: "required" });
    const poor_but_open = job({ id: 2, required_skills: ["python", "aws", "docker", "kafka"] });
    expect(ids(rankJobs(me(), [perfect_but_german, poor_but_open]))).toEqual([2, 1]);
  });

  it("sorts by score, highest first", () => {
    const jobs = [
      job({ id: 1, required_skills: ["python", "aws", "docker", "kafka"] }), // 1/4
      job({ id: 2, required_skills: ["python", "rag"] }),                    // 2/2
      job({ id: 3, required_skills: ["python", "rag", "aws"] }),             // 2/3
    ];
    expect(ids(rankJobs(me(), jobs))).toEqual([2, 3, 1]);
  });

  it("breaks a tie on covered nice-to-have skills, at a quarter of a required one", () => {
    const bare = job({ id: 1, required_skills: ["python", "aws"] });
    const sweetened = job({ id: 2, required_skills: ["python", "aws"], nice_skills: ["rag"] });
    expect(ids(rankJobs(me(), [bare, sweetened]))).toEqual([2, 1]);
    // A quarter of one required skill cannot outweigh a whole one: 1/2 + nice stays under 2/2.
    const better = job({ id: 3, required_skills: ["python", "rag"] });
    expect(ids(rankJobs(me(), [sweetened, better]))).toEqual([3, 2]);
  });

  it("earns no nice-to-have bonus for a nice-to-have skill the profile does not have", () => {
    const bare = job({ id: 1, required_skills: ["python", "aws"] });
    const uncoveredNice = job({ id: 2, required_skills: ["python", "aws"], nice_skills: ["kafka"] });
    // "kafka" is not among the profile's skills, so it must earn no bonus: these two tie
    // and keep the order they were given in, same as two jobs with no nice_skills at all.
    expect(ids(rankJobs(me(), [bare, uncoveredNice]))).toEqual([1, 2]);
  });

  it("divides the nice-to-have bonus by the job's own required count, not multiplies by it", () => {
    const profile = me({ skills: ["python", "kafka"] });
    const smaller = job({ id: 1, required_skills: ["python", "aws"], nice_skills: ["kafka"] });
    const bigger = job({ id: 2, required_skills: ["python", "aws", "docker"], nice_skills: ["kafka"] });
    // Both list fewer required skills than SKILL_FLOOR and cover the same count (1), so
    // they tie on rank_score before the nice-to-have bonus is applied.
    expect(fit(profile, smaller).rank_score).toBeCloseTo(fit(profile, bigger).rank_score, 10);
    // The bonus must then favor the job with FEWER required skills (a bigger fraction of a
    // smaller list), not the job with more of them.
    expect(ids(rankJobs(profile, [bigger, smaller]))).toEqual([1, 2]);
  });

  it("keeps relative order among tied jobs even with other jobs ranked around them", () => {
    const jobs = [fitJob(1, 0, 5), fitJob(10, 3, 4), fitJob(11, 3, 4), fitJob(2, 5, 5)];
    expect(ids(rankJobs(haveAll, jobs))).toEqual([2, 10, 11, 1]);
  });

  it("never lets nice-to-have coverage beat a better score, however much of it there is", () => {
    // 1/2 required, but every nice-to-have covered, against a plain 3/5. Scored as one
    // number the first would read 0.75 and come first; it is the worse fit, and sorts second.
    const shallow = job({ id: 1, required_skills: ["python", "aws"], nice_skills: ["rag", "sql", "docker"] });
    const deeper = job({ id: 2, required_skills: ["python", "rag", "sql", "aws", "docker"] });
    expect(fit(me({ skills: ["python", "rag", "sql"] }), deeper).score).toBe(0.6);
    expect(ids(rankJobs(me({ skills: ["python", "rag", "sql"] }), [shallow, deeper]))).toEqual([2, 1]);
  });

  it("sorts a job with no required skills last among those still in reach", () => {
    const jobs = [
      job({ id: 1, nice_skills: ["python"] }),                              // a fragment: nothing to judge
      job({ id: 2, required_skills: ["aws", "docker", "kafka"] }),          // 0/3
      job({ id: 3, required_skills: ["python"], german: "required" }),      // gated out
    ];
    expect(ids(rankJobs(me(), jobs))).toEqual([2, 1, 3]);
  });

  it("keeps the order it was given for jobs that tie, and never mutates the input", () => {
    const jobs = [job({ id: 7 }), job({ id: 4 }), job({ id: 9 })];
    const ranked = rankJobs(me(), jobs);
    expect(ids(ranked)).toEqual([7, 4, 9]);
    expect(ids(jobs)).toEqual([7, 4, 9]);
    expect(ranked).not.toBe(jobs);
  });

  it("leaves the jobs alone without a profile", () => {
    const jobs = [job({ id: 1, german: "required" }), job({ id: 2 })];
    expect(rankJobs(null, jobs)).toBe(jobs);
  });
});
