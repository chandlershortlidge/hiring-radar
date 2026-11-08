import { describe, expect, it } from "vitest";
import {
  ALL_GERMANY, COMPARE_DEFAULT, COMPARE_MAX, FAMILIES, FAMILY_LABELS, PLACES, PLACE_GROUPS, PLACE_NAMES,
  compareAdd, compareListCities, compareRemove, familyLabel, listFilters, placeBySlug, placeCities, placeMatches,
} from "./format.js";

describe("every place carries a slug and a group (HIR-188)", () => {
  it("still lists every collected place, EU-remote and New York included", () => {
    expect(PLACE_NAMES).toEqual(["Berlin", "Hamburg", "Remote (EU)", "San Francisco", "New York"]);
  });

  it("gives each place a unique slug and a group the picker knows", () => {
    const slugs = PLACES.map((p) => p.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
    for (const p of PLACES) {
      expect(p.slug).toMatch(/^[a-z0-9-]+$/);
      expect(PLACE_GROUPS).toContain(p.group);
    }
  });

  it("finds a place by its slug, and nothing for a slug we do not have", () => {
    expect(placeBySlug("berlin").name).toBe("Berlin");
    expect(placeBySlug("atlantis")).toBeNull();
  });

  it("turns 'all of Germany' into every German place, and a city into just itself", () => {
    expect(placeCities(ALL_GERMANY.slug)).toEqual(["Berlin", "Hamburg"]);
    expect(placeCities("san-francisco")).toEqual(["San Francisco"]);
    expect(placeCities("atlantis")).toEqual([]);
  });

  it("searches a place by name, country and alias", () => {
    const sf = placeBySlug("san-francisco");
    expect(placeMatches(sf, "")).toBe(true);
    expect(placeMatches(sf, "fran")).toBe(true);
    expect(placeMatches(sf, "sf")).toBe(true);
    expect(placeMatches(sf, "united")).toBe(true);
    expect(placeMatches(sf, "berlin")).toBe(false);
    expect(placeMatches(placeBySlug("berlin"), "germany")).toBe(true);
  });
});

describe("compare mode holds two or three places (HIR-188, was HIR-138's two sides)", () => {
  it("opens on Berlin vs San Francisco, the pair it had before", () => {
    expect(COMPARE_DEFAULT).toEqual(["Berlin", "San Francisco"]);
    for (const p of COMPARE_DEFAULT) expect(PLACE_NAMES).toContain(p);
  });

  it("adds a third place but not a fourth", () => {
    expect(compareAdd(["Berlin"], "New York")).toEqual(["Berlin", "New York"]);
    expect(compareAdd(["Berlin", "San Francisco"], "New York")).toEqual(["Berlin", "San Francisco", "New York"]);
    expect(compareAdd(["Berlin", "San Francisco", "New York"], "Remote (EU)")).toEqual(["Berlin", "San Francisco", "New York"]);
    expect(COMPARE_MAX).toBe(3);
  });

  it("never shows the same place twice", () => {
    expect(compareAdd(["Berlin", "San Francisco"], "Berlin")).toEqual(["Berlin", "San Francisco"]);
  });

  it("removes the place asked for, first one included", () => {
    expect(compareRemove(["Berlin", "San Francisco", "New York"], "Berlin")).toEqual(["San Francisco", "New York"]);
    expect(compareRemove(["Berlin", "San Francisco"], "San Francisco")).toEqual(["Berlin"]);
    expect(compareRemove(["Berlin", "San Francisco"], "New York")).toEqual(["Berlin", "San Francisco"]);
  });
});

describe("compare mode filters the job list to the compared cities (HIR-196)", () => {
  const base = { cities: [], compare: true, skillIds: ["langchain"], families: ["ai-engineer"], seniorities: ["senior"], window: "open" };

  it("puts the compared cities into the list's filters, two or three of them", () => {
    expect(listFilters(base, ["Berlin", "San Francisco"]).cities).toEqual(["Berlin", "San Francisco"]);
    expect(listFilters(base, ["Berlin", "San Francisco", "New York"]).cities).toEqual(["Berlin", "San Francisco", "New York"]);
  });

  it("keeps every other filter — skills, family, seniority — as it was", () => {
    const lf = listFilters(base, ["Berlin", "San Francisco"]);
    expect(lf.skillIds).toEqual(["langchain"]);
    expect(lf.families).toEqual(["ai-engineer"]);
    expect(lf.seniorities).toEqual(["senior"]);
    expect(lf.window).toBe("open");
    expect(lf.compare).toBe(true);
  });

  it("passes the single-city view through unchanged, the very same object", () => {
    const single = { ...base, compare: false, cities: ["Berlin"] };
    expect(listFilters(single, ["Berlin", "San Francisco"])).toBe(single);
  });

  it("expands a compared place that stands for several cities", () => {
    expect(compareListCities([ALL_GERMANY.name, "San Francisco"])).toEqual(["Berlin", "Hamburg", "San Francisco"]);
    expect(compareListCities(["Berlin", "New York"])).toEqual(["Berlin", "New York"]);
  });
});

describe("the job family filter (HIR-186)", () => {
  it("offers the five families the server accepts, in button order", () => {
    expect(FAMILIES).toEqual(["ai-engineer", "ml-engineer", "data-scientist", "ml-platform", "research"]);
  });

  it("has a readable label for every family", () => {
    for (const f of FAMILIES) expect(FAMILY_LABELS[f]).toBeTruthy();
    expect(familyLabel("data-scientist")).toBe("Data Scientist");
  });

  it("falls back to the stored value for a family it does not know", () => {
    expect(familyLabel("quantum-engineer")).toBe("quantum-engineer");
  });
});
