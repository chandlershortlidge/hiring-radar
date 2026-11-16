import { describe, expect, it } from "vitest";
import { HOME, parsePath, pathFor, withFamily } from "./routes.js";
import { ALL_GERMANY, PLACES, placeCities } from "./format.js";

describe("the address bar says which market you are looking at (HIR-188)", () => {
  it("reads the bare root as the home view", () => {
    expect(parsePath("/")).toEqual(HOME);
    expect(parsePath("")).toEqual(HOME);
  });

  it("reads a city on its own, and a city with a family", () => {
    expect(parsePath("/berlin")).toMatchObject({ view: "city", place: "berlin", family: null });
    expect(parsePath("/berlin/ai-engineer")).toMatchObject({ view: "city", place: "berlin", family: "ai-engineer" });
    expect(parsePath("/san-francisco/data-scientist")).toMatchObject({ view: "city", place: "san-francisco", family: "data-scientist" });
  });

  it("keeps the city when the family part is not one we know", () => {
    expect(parsePath("/berlin/quantum-engineer")).toMatchObject({ view: "city", place: "berlin", family: null });
  });

  it("reads 'all of Germany' as a place of its own", () => {
    expect(parsePath("/all-germany")).toMatchObject({ view: "city", place: "all-germany" });
    expect(placeCities(ALL_GERMANY.slug)).toEqual(PLACES.filter((p) => p.group === "Germany").map((p) => p.name));
  });

  it("reads two or three cities joined by + as compare mode", () => {
    expect(parsePath("/compare/berlin+san-francisco")).toMatchObject({ view: "compare", cities: ["Berlin", "San Francisco"] });
    expect(parsePath("/compare/berlin+san-francisco+new-york")).toMatchObject({ view: "compare", cities: ["Berlin", "San Francisco", "New York"] });
  });

  it("drops a repeated city and anything past the third", () => {
    expect(parsePath("/compare/berlin+berlin+san-francisco")).toMatchObject({ cities: ["Berlin", "San Francisco"] });
    expect(parsePath("/compare/berlin+san-francisco+new-york+remote-eu").cities).toHaveLength(3);
  });

  it("falls back to the home view when a comparison has fewer than two real cities", () => {
    expect(parsePath("/compare/berlin")).toEqual(HOME);
    expect(parsePath("/compare/atlantis+el-dorado")).toEqual(HOME);
    expect(parsePath("/compare")).toEqual(HOME);
  });

  it("does not compare a group against a city", () => {
    expect(parsePath("/compare/all-germany+berlin")).toEqual(HOME);
  });

  it("still reads a job's own page", () => {
    expect(parsePath("/jobs/42")).toMatchObject({ view: "job", jobId: 42 });
    expect(parsePath("/jobs/not-a-number")).toEqual(HOME);
  });

  it("sends an unknown path to the home view rather than erroring", () => {
    expect(parsePath("/atlantis")).toEqual(HOME);
    expect(parsePath("/berlin/ai-engineer/extra")).toEqual(HOME);
  });

  it("writes back the path it read, for every place and family", () => {
    for (const p of [...PLACES, ALL_GERMANY]) {
      expect(pathFor(parsePath(`/${p.slug}`))).toBe(`/${p.slug}`);
      expect(pathFor(parsePath(`/${p.slug}/ml-engineer`))).toBe(`/${p.slug}/ml-engineer`);
    }
    expect(pathFor(parsePath("/compare/berlin+new-york"))).toBe("/compare/berlin+new-york");
    expect(pathFor(parsePath("/jobs/7"))).toBe("/jobs/7");
    expect(pathFor(HOME)).toBe("/");
  });
});

describe("picking a job family (HIR-197)", () => {
  it("stays on the home view, at /, until a city is picked", () => {
    const next = withFamily(HOME, "ai-engineer");
    expect(next).toEqual({ ...HOME, family: "ai-engineer" });
    expect(pathFor(next)).toBe("/");
  });

  it("carries the family into the city picked next", () => {
    const home = withFamily(HOME, "ai-engineer");
    expect(pathFor({ ...HOME, view: "city", place: "berlin", family: home.family })).toBe("/berlin/ai-engineer");
  });

  it("goes back to every role on the home view without leaving it", () => {
    expect(withFamily(withFamily(HOME, "research"), null)).toEqual(HOME);
  });

  it("updates in place on a city and in a comparison, as before", () => {
    const city = { ...HOME, view: "city", place: "berlin", family: null };
    expect(withFamily(city, "ml-engineer")).toEqual({ ...city, family: "ml-engineer" });
    const compare = { ...HOME, view: "compare", cities: ["Berlin", "New York"] };
    expect(withFamily(compare, "research")).toEqual({ ...compare, family: "research" });
  });

  // The bug: a city view with no city drew the dashboard for every city at once.
  it("never makes a city view without a city", () => {
    const noPlace = { ...HOME, view: "city", place: null, family: "ai-engineer" };
    expect(pathFor(noPlace)).toBe("/");
    expect(parsePath(pathFor(noPlace))).toEqual(HOME);
    expect(withFamily(noPlace, "research").view).toBe("home");
  });
});
