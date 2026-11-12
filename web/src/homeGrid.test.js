import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import HomeGrid, { cardCounts, topSkills } from "./HomeGrid.jsx";
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
    const places = gridPlaces({ Berlin: 100, Hamburg: 70, Frankfurt: 55, Munich: 80, "San Francisco": 292, "New York": 300, "Remote (EU)": 40 });
    expect(places.map((p) => p.name)).toEqual(["New York", "San Francisco", "Berlin", "Munich", "Hamburg", "Frankfurt", "Remote (EU)"]);
  });

  it("carries each market's country, since there is no row heading to say it any more", () => {
    for (const p of gridPlaces({})) expect(PLACE_GROUPS).toContain(p.group);
  });

  it("breaks a tie by name, so the grid does not reshuffle between visits", () => {
    const places = gridPlaces({ Berlin: 7, Hamburg: 7, Frankfurt: 7, Munich: 7, "San Francisco": 7, "New York": 7, "Remote (EU)": 7 });
    expect(places.map((p) => p.name)).toEqual(["Berlin", "Frankfurt", "Hamburg", "Munich", "New York", "Remote (EU)", "San Francisco"]);
  });

  it("still lists a market with no jobs — that is where a new city starts", () => {
    expect(gridPlaces({}).map((p) => p.name)).toContain("New York");
  });

  // PLACES is the one list the picker, the grid, compare and the URLs all read, so sorting
  // it in place would quietly reorder the city picker as well.
  it("sorts a copy, leaving the shared place list in its own declared order", () => {
    gridPlaces({ "New York": 999 });
    expect(PLACES.map((p) => p.name)).toEqual(["Berlin", "Hamburg", "Frankfurt", "Munich", "Remote (EU)", "San Francisco", "New York"]);
  });
});

describe("the market cards follow the job family picked on the home view (HIR-197)", () => {
  // Open jobs per city for every role, from /api/stats: New York is the busiest.
  const OPEN = { Berlin: 120, "San Francisco": 292, "New York": 300 };
  // /api/skills asked for one family and no city: Berlin has the most AI Engineer jobs.
  const AI = {
    family: "ai-engineer",
    city_totals: { Berlin: 40, "San Francisco": 25, "New York": 10 },
    skills: [
      { skill_id: "llms", display: "LLMs", by_city: { Berlin: 30, "San Francisco": 20 } },
      { skill_id: "python", display: "Python", by_city: { Berlin: 20, "San Francisco": 5 } },
    ],
  };
  const ALL = { family: null, city_totals: { Berlin: 110, "San Francisco": 280, "New York": 290 }, skills: SKILLS };
  const render = (data, family) => renderToStaticMarkup(createElement(HomeGrid, { data, counts: OPEN, family, onRequestCity: () => {} }));
  const cardOrder = (html) => [...html.matchAll(/<h3>([^<]+)<\/h3>/g)].map((m) => m[1]).slice(0, 3);

  it("counts every role's open jobs while no family is chosen", () => {
    expect(cardCounts(OPEN, ALL)).toBe(OPEN);
    expect(cardCounts(OPEN, null)).toBe(OPEN);
    const html = render(ALL, null);
    expect(html).toContain("300 open");
    expect(cardOrder(html)).toEqual(["New York", "San Francisco", "Berlin"]);
    expect(html).toContain('href="/berlin"');
  });

  it("shows the chosen family's job count on each card and sorts by it", () => {
    expect(cardCounts(OPEN, AI)).toEqual(AI.city_totals);
    const html = render(AI, "ai-engineer");
    expect(html).toContain("40 open");
    expect(html).not.toContain("120 open");
    expect(cardOrder(html)).toEqual(["Berlin", "San Francisco", "New York"]);
  });

  it("shows the family's top skills as a share of that family's jobs in the city", () => {
    const html = render(AI, "ai-engineer");
    expect(html).toContain("75%"); // LLMs: 30 of Berlin's 40 AI Engineer jobs
    expect(html).toContain("50%"); // Python: 20 of 40
  });

  it("opens the city with the family when a card is clicked", () => {
    const html = render(AI, "ai-engineer");
    expect(html).toContain('href="/berlin/ai-engineer"');
    expect(html).toContain('href="/new-york/ai-engineer"');
  });

  it("shows zero, not the all-roles count, for a city with none of that family", () => {
    const html = render({ ...AI, city_totals: { Berlin: 40 } }, "ai-engineer");
    expect(html).toContain(">0 open<");
    expect(html).not.toContain("300 open");
  });

  // Between the pick and the server's answer the numbers on screen are still the old ones;
  // they must stay one consistent set, not the new family's order over the old counts.
  it("keeps the previous numbers whole until the new family's answer arrives", () => {
    const html = render(ALL, "ai-engineer");
    expect(html).toContain("300 open");
    expect(cardOrder(html)).toEqual(["New York", "San Francisco", "Berlin"]);
  });
});
