// HIR-289: a job posted for several cities shows the first and a count; the tooltip names all.
import { describe, expect, it } from "vitest";
import { placeLabel } from "./JobList.jsx";

describe("placeLabel", () => {
  it("shows one city as it is", () => {
    expect(placeLabel({ city: "Berlin", places: ["Berlin"] })).toEqual({ text: "Berlin", title: "Berlin" });
  });
  it("shows the first city and how many more, all of them in the tooltip", () => {
    const j = { city: "Berlin", places: ["Berlin", "Hamburg", "Frankfurt", "Munich"] };
    expect(placeLabel(j)).toEqual({ text: "Berlin +3", title: "Berlin, Hamburg, Frankfurt, Munich" });
  });
  it("falls back to the city, then a dash", () => {
    expect(placeLabel({ city: "Munich" }).text).toBe("Munich");
    expect(placeLabel({ city: null, places: [] }).text).toBe("—");
  });
});
