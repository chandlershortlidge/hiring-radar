// HIR-226: a "doesn't belong here" flag must carry everything that was on screen, because
// the view is the only statement of what the job was supposed to be. The test that matters
// is the second one: whatever the job-list request sends to the server has to be in the
// flag too, so a filter added later cannot be in the address and missing from the flag.
import { describe, it, expect, vi, afterEach } from "vitest";
import { DEFAULT } from "./App.jsx";
import { api } from "./api.js";
import { flagView, jobPageView } from "./flagView.js";

// Every filter the dashboard keeps, each set to a value no other filter has.
const everyFilterSet = () => Object.fromEntries(Object.entries(DEFAULT).map(([k, v]) => [
  k, Array.isArray(v) ? [`${k}-a`, `${k}-b`] : typeof v === "boolean" ? true : `${k}-value`]));
const MARKET = { view: "city", place: "berlin", family: "ai-engineer", cities: [], jobId: null };

afterEach(() => vi.unstubAllGlobals());

describe("what a flag records about the screen", () => {
  it("holds every filter the dashboard keeps, with its value", () => {
    const filters = everyFilterSet();
    const view = flagView({ filters, sort: "newest", market: MARKET, url: "/berlin/ai-engineer" });
    expect(Object.keys(view.filters).sort()).toEqual(Object.keys(DEFAULT).sort());
    expect(view.filters).toEqual(filters);
  });

  it("holds everything the job-list request sends, so nothing is in the address and not in the flag", async () => {
    let asked = null;
    vi.stubGlobal("fetch", async (path) => { asked = path; return { ok: true, json: async () => ({}) }; });
    const filters = everyFilterSet();
    await api.jobs(filters, { sort: "reposts", limit: 20, offset: 40 });
    const sent = [...new URL(asked, "http://x").searchParams.entries()].filter(([k]) => !["limit", "offset"].includes(k));
    expect(sent.length).toBeGreaterThanOrEqual(12);   // the filters, the two searches, the sort

    const recorded = JSON.stringify(flagView({ filters, sort: "reposts", market: MARKET, url: "/berlin/ai-engineer" }));
    const missing = sent.filter(([, value]) => !recorded.includes(JSON.stringify(value)));
    expect(missing).toEqual([]);
  });

  it("holds the page address, the sort, the market and whether it was the saved list", () => {
    const view = flagView({ filters: DEFAULT, sort: "fit", saved: true, market: MARKET, url: "/compare/berlin+munich" });
    expect(view).toMatchObject({ page: "list", url: "/compare/berlin+munich", sort: "fit", saved: true, market: MARKET });
  });

  it("keeps a filter it has never heard of", () => {
    const view = flagView({ filters: { ...DEFAULT, visa: "sponsored" }, sort: "newest", url: "/berlin" });
    expect(view.filters.visa).toBe("sponsored");
  });

  it("copies the filters, so a later change on screen does not rewrite what was flagged", () => {
    const filters = { ...DEFAULT };
    const view = flagView({ filters, sort: "newest", url: "/berlin" });
    filters.german = "required";
    expect(view.filters.german).toBe("any");
  });

  it("records a job's own page as the page, with no filters", () => {
    expect(jobPageView("/jobs/42")).toEqual({ page: "job", url: "/jobs/42" });
  });
});
