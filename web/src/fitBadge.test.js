// What the row says about a fit, on the two pure text builders only: no DOM, no network.
// HIR-154: a job that lists fewer required skills than a posting normally does shows the
// count without a percentage and is never called a full match. HIR-161 put "fewer" at 3 or
// fewer, so the cases below are written in absolute counts as well as in SKILL_FLOOR: a
// test that only ever says SKILL_FLOOR - 1 passes at any threshold, including the 7 that
// was the bug.
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
  it("names the count plainly, without a percentage, at 3 asks or fewer", () => {
    expect(fitBadge(cov(2, 2))).toBe("2/2 · few skills listed");
    expect(fitBadge(cov(1, 3))).toBe("1/3 · few skills listed");
    expect(fitBadge(cov(3, 3))).toBe("3/3 · few skills listed");
    // The last thin width, whatever the threshold is set to.
    expect(fitBadge(cov(SKILL_FLOOR - 1, SKILL_FLOOR - 1)))
      .toBe(`${SKILL_FLOOR - 1}/${SKILL_FLOOR - 1} · few skills listed`);
  });

  it("shows the percentage from 4 asks upwards", () => {
    expect(fitBadge(cov(SKILL_FLOOR, SKILL_FLOOR))).toBe(`100% · ${SKILL_FLOOR}/${SKILL_FLOOR}`);
    expect(fitBadge(cov(5, 8))).toBe("63% · 5/8");
    expect(fitBadge(cov(10, 14))).toBe("71% · 10/14");
  });

  // HIR-161: the rows Chandler saw tagged "few skills listed" on 4 Nov, which are normal
  // lists. These are spelled out in full because they are the bug report.
  it("gives the rows from the bug report their percentage back", () => {
    expect(fitBadge(cov(2, 6))).toBe("33% · 2/6");   // Lieferando, ML Engineer, Berlin
    expect(fitBadge(cov(3, 4))).toBe("75% · 3/4");   // Anthropic
    expect(fitBadge(cov(3, 6))).toBe("50% · 3/6");   // Anthropic
    expect(fitBadge(cov(4, 4))).toBe("100% · 4/4");
  });
});

describe("fitTitle", () => {
  it("refuses 'a full match' to a job that listed too little, and says why", () => {
    expect(fitTitle(cov(2, 2), TAX)).toBe(
      "You cover 2 of 2 required skills — but few skills listed, so this is not a full match");
  });

  it("still calls a full list fully covered a full match", () => {
    expect(fitTitle(cov(SKILL_FLOOR, SKILL_FLOOR), TAX))
      .toBe(`You cover ${SKILL_FLOOR} of ${SKILL_FLOOR} required skills — a full match`);
    // HIR-161: at 4 asks this is now a full match rather than "few skills listed".
    expect(fitTitle(cov(4, 4), TAX)).toBe("You cover 4 of 4 required skills — a full match");
  });

  // HIR-161: 3 asks is still too few to call a match, 4 is not.
  it("draws the 'not a full match' line between 3 asks and 4", () => {
    expect(fitTitle(cov(3, 3), TAX)).toBe(
      "You cover 3 of 3 required skills — but few skills listed, so this is not a full match");
  });

  it("names the missing skills first whatever the list's length", () => {
    expect(fitTitle(cov(1, 3), TAX)).toBe(
      "You cover 1 of 3 required skills. Missing, most asked for first: Kubernetes, Go");
    expect(fitTitle(cov(8, 10), TAX)).toContain("Missing, most asked for first: Kubernetes, Go");
  });
});
