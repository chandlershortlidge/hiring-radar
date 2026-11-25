// The browser's fit logic gives the answers in tests/fixtures/fit_cases.json (HIR-435).
// tests/test_fit_cases.py checks app/fit.py against the same file, so a change to fit,
// gates or ranking here fails until the Python side (the match_profile MCP tool) agrees.
import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { fit, gates, isMatch, jobSeniority, metSkills, rankJobs, recentJobs, FIT_DAYS } from "./profile.js";

const CASES = JSON.parse(readFileSync(new URL("../../tests/fixtures/fit_cases.json", import.meta.url), "utf8"));
const byId = Object.fromEntries(CASES.jobs.map((j) => [String(j.id), j]));
const now = Date.parse(CASES.now);

// Scores to 1e-12; everything else exactly.
function same(got, want) {
  for (const k of Object.keys(want)) {
    if (typeof want[k] === "number" && !Number.isInteger(want[k])) expect(got[k]).toBeCloseTo(want[k], 12);
    else expect(got[k]).toEqual(want[k]);
  }
  expect(Object.keys(got).sort()).toEqual(Object.keys(want).sort());
}

describe("the shared fit cases", () => {
  it("are the ones the Python port is checked against", () => {
    expect(CASES.jobs.length).toBeGreaterThanOrEqual(20);
    expect(CASES.fit_days).toBe(FIT_DAYS);
  });

  it("give each job's level and which jobs are recent", () => {
    expect(Object.fromEntries(CASES.jobs.map((j) => [String(j.id), jobSeniority(j)]))).toEqual(CASES.job_seniority);
    expect(recentJobs(CASES.jobs, now).map((j) => j.id)).toEqual(CASES.recent);
  });

  for (const [name, want] of Object.entries(CASES.expected)) {
    const profile = CASES.profiles[name];
    describe(name, () => {
      it("scores every job the same", () => {
        for (const [id, f] of Object.entries(want.fit)) same(fit(profile, byId[id], CASES.demand), f);
        for (const [id, m] of Object.entries(want.fit_without_demand_missing)) expect(fit(profile, byId[id]).missing).toEqual(m);
      });

      it("gates and meets the same skills", () => {
        for (const id of Object.keys(byId)) {
          expect(gates(profile, byId[id])).toEqual(want.gates[id]);
          expect([...metSkills(profile, byId[id])].sort()).toEqual(want.met_skills[id]);
        }
      });

      it("ranks in the same order and counts the same matches", () => {
        expect(rankJobs(profile, CASES.jobs, CASES.demand).map((j) => j.id)).toEqual(want.order);
        expect(rankJobs(profile, recentJobs(CASES.jobs, now), CASES.demand).map((j) => j.id)).toEqual(want.order_recent);
        expect(CASES.jobs.filter((j) => isMatch(profile, j)).map((j) => j.id)).toEqual(want.matches);
      });
    });
  }
});
