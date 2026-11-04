// What the row says about a fit, on the two pure text builders only: no DOM, no network.
// HIR-154: a job that lists fewer required skills than a posting normally does shows the
// count without a percentage and is never called a full match.
import { describe, expect, it } from "vitest";
import { fitBadge, fitTitle } from "./JobList.jsx";
import { fit, EMPTY, SKILL_FLOOR } from "./profile.js";

const me = (skills) => ({ ...EMPTY, skills });
const job = (required) => ({ id: 1, required_skills: required, nice_skills: [] });

// A job asking `total` required skills of which the profile covers `covered`.
const cov = (covered, total) => {
  const have = Array.from({ length: covered }, (_, i) => `have${i}`);
  const lack = Array.from({ length: total - covered }, (_, i) => `lack${i}`);
  return fit(me(have), job([...have, ...lack]));
};

const TAX = { lack0: "Kubernetes", lack1: "Go" };

describe("fitBadge", () => {
  it("names the count plainly, without a percentage, below the floor", () => {
    expect(fitBadge(cov(2, 2))).toBe("2/2 · few skills listed");
    expect(fitBadge(cov(1, 3))).toBe("1/3 · few skills listed");
    expect(fitBadge(cov(SKILL_FLOOR - 1, SKILL_FLOOR - 1))).toBe(`6/6 · few skills listed`);
  });

  it("shows the percentage from the floor upwards", () => {
    expect(fitBadge(cov(SKILL_FLOOR, SKILL_FLOOR))).toBe("100% · 7/7");
    expect(fitBadge(cov(5, 8))).toBe("63% · 5/8");
    expect(fitBadge(cov(10, 14))).toBe("71% · 10/14");
  });
});

describe("fitTitle", () => {
  it("refuses 'a full match' to a job that listed too little, and says why", () => {
    expect(fitTitle(cov(2, 2), TAX)).toBe(
      "You cover 2 of 2 required skills — but few skills listed, so this is not a full match");
  });

  it("still calls a full list fully covered a full match", () => {
    expect(fitTitle(cov(SKILL_FLOOR, SKILL_FLOOR), TAX)).toBe("You cover 7 of 7 required skills — a full match");
  });

  it("names the missing skills first whatever the list's length", () => {
    expect(fitTitle(cov(1, 3), TAX)).toBe(
      "You cover 1 of 3 required skills. Missing, most asked for first: Kubernetes, Go");
    expect(fitTitle(cov(8, 10), TAX)).toContain("Missing, most asked for first: Kubernetes, Go");
  });
});
