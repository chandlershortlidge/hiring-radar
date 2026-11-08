import { describe, expect, it } from "vitest";
import { topSkills } from "./HomeGrid.jsx";
import { PLACES, PLACE_GROUPS, gridPlaces } from "./format.js";

// One /api/skills response shape: every skill row carries its count per city, and the
// response carries the job total per city. The market cards are drawn from that one
// answer, never from a request per city.
const SKILLS = [
  { skill_id: "python", display: "Python", by_city: { Berlin: 58, "San Francisco": 170 } },
  { skill_id: "llms", display: "LLMs", by_city: { Berlin: 35, "San Francisco": 102 } },
  { skill_id: "sql", display: "SQL", by_city: { Berlin: 18 } },
  { skill_id: "agents", display: "Agents", by_city: { Berlin: 17, "San Francisco": 50 } },
  { skill_id: "rust", display: "Rust", by_city: {} },
];

describe("the market cards on the home view (HIR-188)", () => {
  it("shows a city's three most-asked-for skills, as a share of that city's own jobs", () => {
    expect(topSkills(SKILLS, "Berlin", 100)).toEqual([
      { name: "Python", count: 58, pct: 58 },
      { name: "LLMs", count: 35, pct: 35 },
      { name: "SQL", count: 18, pct: 18 },
    ]);
  });

  it("counts each city against its own total, not the whole market", () => {
    const sf = topSkills(SKILLS, "San Francisco", 292);
    expect(sf.map((s) => s.name)).toEqual(["Python", "LLMs", "Agents"]);
    expect(sf[0].pct).toBe(58);
  });

  it("leaves out skills no job in that city asks for", () => {
    expect(topSkills(SKILLS, "Berlin", 100).map((s) => s.name)).not.toContain("Rust");
  });

  it("says nothing rather than guessing when a city has no jobs", () => {
    expect(topSkills(SKILLS, "Hamburg", 0)).toEqual([]);
    expect(topSkills(undefined, "Berlin", 100)).toEqual([]);
  });

  it("breaks a tie by name, so the card is the same on every render", () => {
    const tied = [
      { skill_id: "b", display: "Bravo", by_city: { Berlin: 5 } },
      { skill_id: "a", display: "Alpha", by_city: { Berlin: 5 } },
    ];
    expect(topSkills(tied, "Berlin", 10).map((s) => s.name)).toEqual(["Alpha", "Bravo"]);
  });

  it("puts every market in one grid, busiest first, whatever country it is in (HIR-191)", () => {
    const places = gridPlaces({ Berlin: 100, Hamburg: 70, "San Francisco": 292, "New York": 300, "Remote (EU)": 40 });
    expect(places.map((p) => p.name)).toEqual(["New York", "San Francisco", "Berlin", "Hamburg", "Remote (EU)"]);
  });

  it("carries each market's country, since there is no row heading to say it any more", () => {
    for (const p of gridPlaces({})) expect(PLACE_GROUPS).toContain(p.group);
  });

  it("breaks a tie by name, so the grid does not reshuffle between visits", () => {
    const places = gridPlaces({ Berlin: 7, Hamburg: 7, "San Francisco": 7, "New York": 7, "Remote (EU)": 7 });
    expect(places.map((p) => p.name)).toEqual(["Berlin", "Hamburg", "New York", "Remote (EU)", "San Francisco"]);
  });

  it("still lists a market with no jobs — that is where a new city starts", () => {
    expect(gridPlaces({}).map((p) => p.name)).toContain("New York");
  });

  // PLACES is the one list the picker, the grid, compare and the URLs all read, so sorting
  // it in place would quietly reorder the city picker as well.
  it("sorts a copy, leaving the shared place list in its own declared order", () => {
    gridPlaces({ "New York": 999 });
    expect(PLACES.map((p) => p.name)).toEqual(["Berlin", "Hamburg", "Remote (EU)", "San Francisco", "New York"]);
  });
});
