// The fit rules of HIR-51, on the pure functions only: a gate beats any score, the
// nice-to-have tie-break, and a job with no required skills to judge. No DOM, no network,
// no localStorage — these are the functions alerts and the Advisor will reuse.
import { describe, expect, it } from "vitest";
import { EMPTY, fails, fit, gates, jobSeniority, rankJobs, skillSides } from "./profile.js";

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
});

describe("rankJobs", () => {
  const ids = (jobs) => jobs.map((j) => j.id);

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
