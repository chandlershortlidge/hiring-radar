// HIR-16: the per-city match count over the city comparison. The counting rule, the
// paging that feeds it and the line it prints, each on its pure part; no DOM, no network.
import { describe, expect, it } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import CityFit, { CityFitLine, cityFilters, cityFitRows, fetchCityJobs } from "./CityFit.jsx";
import { JOBS_MAX, allJobs } from "./api.js";
import { EMPTY, countMatches, isMatch } from "./profile.js";

const me = (skills) => ({ ...EMPTY, skills });
const job = (required, o = {}) => ({ id: 1, title: "AI Engineer", required_skills: required, nice_skills: [], ...o });
const TEN = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"];

describe("isMatch", () => {
  it("counts a job at exactly 70% of its required skills, and not one just under", () => {
    expect(isMatch(me(TEN.slice(0, 7)), job(TEN))).toBe(true);
    expect(isMatch(me(TEN.slice(0, 6)), job(TEN))).toBe(false);
    // 3 of 4 is 75%; 2 of 4 is 50%
    expect(isMatch(me(["a", "b", "c"]), job(["a", "b", "c", "d"]))).toBe(true);
    expect(isMatch(me(["a", "b"]), job(["a", "b", "c", "d"]))).toBe(false);
  });

  it("leaves out a job that lists three or fewer required skills, even fully covered", () => {
    expect(isMatch(me(["a", "b", "c"]), job(["a", "b", "c"]))).toBe(false);
    expect(isMatch(me(["a", "b", "c", "d"]), job(["a", "b", "c", "d"]))).toBe(true);
  });

  it("does not count a job with no required skills, or anything without a profile", () => {
    expect(isMatch(me(["a"]), job([]))).toBe(false);
    expect(isMatch(null, job(["a", "b", "c", "d"]))).toBe(false);
  });

  it("counts a list of alternatives as one requirement", () => {
    // python-or-go, plus b, c, d: four requirements, and python alone meets the first.
    const j = job(["python", "go", "b", "c", "d"], { required_groups: [["python", "go"]] });
    expect(isMatch(me(["python", "b", "c"]), j)).toBe(true);   // 3 of 4
    expect(isMatch(me(["python", "go", "b"]), j)).toBe(false); // 2 of 4
  });

  it("is about skills only: a hard ask the profile fails does not change the count", () => {
    expect(isMatch(me(["a", "b", "c", "d"]), job(["a", "b", "c", "d"], { german: "required" }))).toBe(true);
  });

  it("countMatches counts the matching jobs in a list", () => {
    const jobs = [job(["a", "b", "c", "d"]), job(["a", "x", "y", "z"]), job(["a", "b", "c", "z"])];
    expect(countMatches(me(["a", "b", "c", "d"]), jobs)).toBe(2);
    expect(countMatches(me(["a", "b", "c", "d"]), [])).toBe(0);
  });
});

describe("allJobs", () => {
  // A server holding `n` jobs that serves them as /api/jobs does.
  const server = (n, calls = []) => (filters, { sort, limit, offset }) => {
    calls.push({ sort, limit, offset });
    const jobs = Array.from({ length: Math.max(0, Math.min(limit, n - offset)) }, (_, i) => ({ id: offset + i }));
    return Promise.resolve({ total: n, jobs });
  };

  it("pages through every job, a full page at a time", async () => {
    const calls = [];
    const r = await allJobs({}, server(450, calls));
    expect(r.total).toBe(450);
    expect(r.jobs.map((j) => j.id)).toEqual(Array.from({ length: 450 }, (_, i) => i));
    expect(calls).toEqual([0, 200, 400].map((offset) => ({ sort: "newest", limit: JOBS_MAX, offset })));
  });

  it("asks once when everything fits on one page, and once when there is nothing", async () => {
    const one = [], none = [];
    expect((await allJobs({}, server(200, one))).jobs).toHaveLength(200);
    expect(one).toHaveLength(1);
    expect(await allJobs({}, server(0, none))).toEqual({ jobs: [], total: 0 });
    expect(none).toHaveLength(1);
  });

  it("stops on an empty page instead of asking forever when the total was too high", async () => {
    let n = 0;
    const get = (f, { offset }) => { n++; return Promise.resolve({ total: 500, jobs: offset ? [] : [{ id: 1 }] }); };
    expect((await allJobs({}, get)).jobs).toHaveLength(1);
    expect(n).toBe(2);
  });
});

describe("the per-city count", () => {
  const filters = { cities: [], compare: true, families: ["ml"], seniorities: ["senior"], window: "open", skillIds: ["python"], query: "acme", text: "rag" };

  it("asks for one city under the page's filters, without the job list's own narrowing", () => {
    expect(cityFilters(filters, "Berlin")).toEqual({ ...filters, cities: ["Berlin"], skillIds: [], query: "", text: "" });
  });

  it("fetches each compared city and counts its matches against its own total", async () => {
    const byCity = {
      Berlin: { total: 3, jobs: [job(["a", "b", "c", "d"]), job(["a", "b", "c", "z"]), job(["w", "x", "y", "z"])] },
      Munich: { total: 1, jobs: [job(["w", "x", "y", "z"])] },
    };
    const asked = [];
    const get = (f) => { asked.push(f.cities); return Promise.resolve(byCity[f.cities[0]]); };
    const fetched = await fetchCityJobs(filters, ["Berlin", "Munich"], get);
    expect(asked).toEqual([["Berlin"], ["Munich"]]);
    expect(cityFitRows(me(["a", "b", "c", "d"]), fetched)).toEqual([
      { city: "Berlin", matched: 2, total: 3 },
      { city: "Munich", matched: 0, total: 1 },
    ]);
  });

  it("fails as a whole when one city cannot be fetched", async () => {
    const get = (f) => (f.cities[0] === "Munich" ? Promise.reject(new Error("502")) : Promise.resolve({ total: 0, jobs: [] }));
    await expect(fetchCityJobs(filters, ["Berlin", "Munich"], get)).rejects.toThrow("502");
  });
});

describe("the line over the comparison", () => {
  const text = (el) => renderToStaticMarkup(el).replace(/<!-- -->/g, "").replace(/<[^>]+>/g, "");

  it("names every city with its matches and its jobs", () => {
    const t = text(<CityFitLine rows={[{ city: "Berlin", matched: 14, total: 212 }, { city: "Munich", matched: 9, total: 80 }]} />);
    expect(t).toBe("Jobs where you have at least 70% of the required skills: Berlin: 14 of 212 · Munich: 9 of 80");
  });

  it("says it is counting, and says when it could not", () => {
    expect(text(<CityFitLine rows={null} />)).toContain("Counting");
    expect(text(<CityFitLine rows={null} failed />)).toContain("Could not count");
  });

  it("draws nothing without a profile, or with a profile that has no skills", () => {
    const props = { filters: { cities: [] }, cities: ["Berlin", "Munich"], refreshKey: 0 };
    expect(renderToStaticMarkup(<CityFit profile={null} {...props} />)).toBe("");
    expect(renderToStaticMarkup(<CityFit profile={me([])} {...props} />)).toBe("");
    expect(renderToStaticMarkup(<CityFit profile={me(["python"])} {...props} />)).toContain("Counting");
  });
});
