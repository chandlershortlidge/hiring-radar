import { describe, expect, it } from "vitest";
import { COMPARE_DEFAULT, FAMILIES, FAMILY_LABELS, PLACES, comparePick, familyLabel } from "./format.js";

describe("compare mode's two sides (HIR-138)", () => {
  it("opens on Berlin vs San Francisco, the pair it had before it was pickable", () => {
    expect(COMPARE_DEFAULT).toEqual(["Berlin", "San Francisco"]);
  });

  it("offers every collected place, New York included", () => {
    for (const p of COMPARE_DEFAULT) expect(PLACES).toContain(p);
    expect(PLACES).toContain("New York");
  });

  it("replaces the place on the side that was picked", () => {
    expect(comparePick(["Berlin", "San Francisco"], 0, "New York")).toEqual(["New York", "San Francisco"]);
    expect(comparePick(["Berlin", "San Francisco"], 1, "New York")).toEqual(["Berlin", "New York"]);
  });

  it("swaps rather than showing a place against itself", () => {
    expect(comparePick(["Berlin", "San Francisco"], 0, "San Francisco")).toEqual(["San Francisco", "Berlin"]);
    expect(comparePick(["Berlin", "San Francisco"], 1, "Berlin")).toEqual(["San Francisco", "Berlin"]);
  });

  it("changes nothing when a side is set to what it already shows", () => {
    expect(comparePick(["Berlin", "New York"], 0, "Berlin")).toEqual(["Berlin", "New York"]);
    expect(comparePick(["Berlin", "New York"], 1, "New York")).toEqual(["Berlin", "New York"]);
  });

  it("keeps the two sides different for every pair of places", () => {
    for (const a of PLACES) for (const b of PLACES) {
      if (a === b) continue;
      for (const side of [0, 1]) for (const pick of PLACES) {
        const [x, y] = comparePick([a, b], side, pick);
        expect(x).not.toBe(y);
      }
    }
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
