// HIR-99 on the pure parts: the toggle, what a reload reads back, the Saved view's sorts
// (including that a closed job is never dropped), and the clipboard format. No DOM, no
// network — localStorage is a plain in-memory stub, which is all load/save touch.
import { beforeEach, describe, expect, it } from "vitest";
import { copyLines, jobUrl, loadSaved, saveSaved, sortJobs, toggleId } from "./saved.js";
import { EMPTY } from "./profile.js";

// What localStorage looks like to saved.js: getItem/setItem over a map.
const store = new Map();
globalThis.localStorage = {
  getItem: (k) => (store.has(k) ? store.get(k) : null),
  setItem: (k, v) => store.set(k, String(v)),
};
beforeEach(() => store.clear());

const job = (o = {}) => ({
  id: 1, company: "Acme", title: "AI Engineer", first_seen: "2026-10-01T00:00:00Z",
  repost_count: 0, status: "open", sources: [], required_skills: [], nice_skills: [],
  german: null, production: null, degree: null, degree_requirement: null,
  degree_or_equivalent: false, seniority: null, ...o,
});

describe("toggle", () => {
  it("adds an id that is not saved and removes one that is", () => {
    expect(toggleId([], 7)).toEqual([7]);
    expect(toggleId([3, 7], 7)).toEqual([3]);
    expect(toggleId([3], 7)).toEqual([3, 7]);
  });

  it("never mutates its input", () => {
    const ids = [3];
    toggleId(ids, 7);
    expect(ids).toEqual([3]);
  });
});

describe("persistence across reload", () => {
  it("reads back after a save exactly what was saved", () => {
    saveSaved([3, 7, 12]);
    expect(loadSaved()).toEqual([3, 7, 12]);   // a fresh load() is what a reload runs
  });

  it("reads an empty, unreadable or wrong-shaped store as nothing saved", () => {
    expect(loadSaved()).toEqual([]);
    store.set("hiring-radar.saved.v1", "not json");
    expect(loadSaved()).toEqual([]);
    store.set("hiring-radar.saved.v1", '{"ids": [3]}');
    expect(loadSaved()).toEqual([]);
    store.set("hiring-radar.saved.v1", '[3, "x", 7]');
    expect(loadSaved()).toEqual([3, 7]);       // keeps the ids it can trust
  });
});

describe("the Saved view respects the current sort", () => {
  const a = job({ id: 1, company: "Zeta", first_seen: "2026-10-01T00:00:00Z", repost_count: 2 });
  const b = job({ id: 2, company: "acme", first_seen: "2026-10-20T00:00:00Z", repost_count: 0 });
  const c = job({ id: 3, company: "Mid", first_seen: "2026-10-10T00:00:00Z", repost_count: 5 });

  it("orders newest, oldest, most-reposted and company A–Z like the server", () => {
    expect(sortJobs([a, b, c], "newest").map((j) => j.id)).toEqual([2, 3, 1]);
    expect(sortJobs([a, b, c], "oldest").map((j) => j.id)).toEqual([1, 3, 2]);
    expect(sortJobs([a, b, c], "reposts").map((j) => j.id)).toEqual([3, 1, 2]);
    expect(sortJobs([a, b, c], "company").map((j) => j.id)).toEqual([2, 3, 1]);
  });

  it("breaks a first_seen tie by id, newest id first, like the server", () => {
    const x = job({ id: 5, first_seen: "2026-10-01T00:00:00Z" });
    expect(sortJobs([a, x], "newest").map((j) => j.id)).toEqual([5, 1]);
  });

  it("ranks Best fit with the profile over a newest-first base, like the main list", () => {
    const me = { ...EMPTY, skills: ["python"] };
    const good = job({ id: 4, first_seen: "2026-09-01T00:00:00Z", required_skills: ["python"] });
    const bad = job({ id: 5, first_seen: "2026-10-30T00:00:00Z", required_skills: ["rust"] });
    expect(sortJobs([bad, good], "fit", me).map((j) => j.id)).toEqual([4, 5]);
    // Without a profile there is no fit to rank by; newest-first is the honest fallback.
    expect(sortJobs([bad, good], "fit").map((j) => j.id)).toEqual([5, 4]);
  });

  it("never drops a closed job: status plays no part in sorting or export", () => {
    const closed = job({ id: 9, status: "closed", first_seen: "2026-10-25T00:00:00Z" });
    expect(sortJobs([a, closed], "newest").map((j) => j.id)).toEqual([9, 1]);
    expect(copyLines([closed])).toContain("Acme");
  });
});

describe("copy format", () => {
  it("writes one `company — title — url` line per job, in the order given", () => {
    const jobs = [
      job({ id: 1, company: "Acme", title: "AI Engineer", sources: [{ source: "greenhouse", url: "https://boards.greenhouse.io/acme/jobs/1" }] }),
      job({ id: 2, company: "Beta", title: "ML Engineer", sources: [{ source: "lever", url: "https://jobs.lever.co/beta/2" }] }),
    ];
    expect(copyLines(jobs)).toBe(
      "Acme — AI Engineer — https://boards.greenhouse.io/acme/jobs/1\n"
      + "Beta — ML Engineer — https://jobs.lever.co/beta/2",
    );
  });

  it("keeps the line, without a third part, for a job with no stored URL", () => {
    expect(copyLines([job({ sources: [{ source: "screenshot", url: null }] })])).toBe("Acme — AI Engineer");
    expect(jobUrl(job({ sources: [{ url: null }, { url: "https://x.example/1" }] }))).toBe("https://x.example/1");
  });
});
