// HIR-251: "Expertise in Python, Rust, Go or Java" is one requirement, met by any one of
// the four. The match counts it once; the chart is untouched (tested on the server side).
import { describe, expect, it } from "vitest";
import { fitTitle, missingNames } from "./JobList.jsx";
import { EMPTY, fit, metSkills, requirementUnits } from "./profile.js";

const me = (skills) => ({ ...EMPTY, skills });
const LANGS = ["go", "java", "python", "rust"];
// A list row as /api/jobs returns it: four grouped languages plus Docker.
const row = { id: 1, required_skills: ["docker", ...LANGS], nice_skills: [], required_groups: [LANGS] };
// The same job as /api/jobs/<id> returns it.
const detail = {
  id: 1,
  skills: [
    { skill_id: "docker", requirement: "required", alternative_group: null },
    ...LANGS.map((id) => ({ skill_id: id, requirement: "required", alternative_group: 1 })),
    { skill_id: "aws", requirement: "nice_to_have", alternative_group: null },
  ],
};
const TAX = { go: "Go", java: "Java", python: "Python", rust: "Rust", docker: "Docker" };

describe("a group of alternatives", () => {
  it("counts as one requirement, so the job has two, not five", () => {
    expect(requirementUnits(row)).toEqual(["docker", LANGS]);
    expect(requirementUnits(detail)).toEqual(["docker", LANGS]);
  });

  it("is met by any one member", () => {
    for (const shape of [row, detail]) {
      const f = fit(me(["python", "docker"]), shape);
      expect([f.covered, f.total, f.score]).toEqual([2, 2, 1]);
      expect(f.missing).toEqual([]);
    }
  });

  it("is one missing requirement when no member is in the profile", () => {
    const f = fit(me(["docker"]), row);
    expect([f.covered, f.total]).toEqual([1, 2]);
    expect(f.missing).toEqual([LANGS]);
  });

  it("is named as one requirement in the tooltip", () => {
    expect(fitTitle(fit(me(["docker"]), row), TAX)).toBe(
      "You cover 1 of 2 required skills. Missing, most asked for first: Go, Java, Python or Rust");
    expect(missingNames(["docker", LANGS], TAX)).toBe("Docker, (Go, Java, Python or Rust)");
  });

  it("sorts by its most asked-for member", () => {
    const f = fit(me([]), row, { docker: 50, python: 90, go: 1 });
    expect(f.missing).toEqual([LANGS, "docker"]);
  });

  it("marks every member met once one is in the profile, so none shows as missing", () => {
    expect([...metSkills(me(["rust"]), detail)].sort()).toEqual(LANGS);
    expect([...metSkills(me(["docker"]), detail)]).toEqual(["docker"]);
  });

  it("leaves a job without groups scored exactly as before", () => {
    const plain = { id: 2, required_skills: ["docker", "python"], nice_skills: [] };
    const f = fit(me(["python"]), plain);
    expect([f.covered, f.total, f.missing]).toEqual([1, 2, ["docker"]]);
  });
});
