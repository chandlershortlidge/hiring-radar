// HIR-391: two rules of the job list.
//   1. It opens sorted newest first for everyone, with or without a profile. Best fit is
//      a choice in the menu, not the starting sort.
//   2. Best fit only ranks jobs first seen in the last FIT_DAYS days. Older jobs are left
//      out of that view (they are still there under Newest first).
//
// Rule 2 lives in two pure functions in profile.js (recentJobs, then rankJobs), so it is
// tested on those, with "today" pinned to the ticket's 20 Nov. Rule 1 and the menu label
// are read off the list's first paint, rendered the way App.test.jsx does (no jsdom:
// effects do not run, so nothing is fetched and the list has no rows).
//
// Does NOT cover: the Saved view's ranking, which has no age rule and is tested in
// saved.test.js; or the line under the list in a browser, which the PR screenshots show.
import { describe, it, expect } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import JobList, { Detail, Row, bestFitList, waitingLine } from "./JobList.jsx";
import { sortJobs } from "./saved.js";
import { EMPTY, FIT_DAYS, fit, rankJobs, recentJobs } from "./profile.js";

const NOW = Date.parse("2026-11-20T12:00:00+00:00");
const me = { ...EMPTY, seniority: "mid", skills: ["python", "rag"] };
const job = (id, first_seen, o = {}) => ({
  id, title: "AI Engineer", first_seen, required_skills: [], nice_skills: [], german: null, production: null,
  degree: null, degree_requirement: null, degree_or_equivalent: false, seniority: null, ...o,
});
const ids = (jobs) => jobs.map((j) => j.id);
// What the list does when Best fit is chosen: drop the old jobs, then rank the rest.
const bestFit = (profile, jobs) => rankJobs(profile, recentJobs(jobs, NOW));

describe("Best fit only ranks recent jobs", () => {
  it("the limit is 30 days", () => {
    expect(FIT_DAYS).toBe(30);
  });

  // The ticket's table, today = 20 Nov.
  it.each([
    ["19 Nov (yesterday)", "2026-11-19T07:03:12+00:00", true],
    ["22 Oct (29 days ago)", "2026-10-22T07:03:12+00:00", true],
    ["20 Oct (31 days ago)", "2026-10-20T07:03:12+00:00", false],
    ["1 Sep", "2026-09-01T07:03:12+00:00", false],
  ])("a job first seen %s: in Best fit = %s", (_label, firstSeen, kept) => {
    expect(ids(bestFit(me, [job(1, firstSeen)]))).toEqual(kept ? [1] : []);
  });

  it("gives an empty list, not an error, when none of the jobs are recent", () => {
    expect(bestFit(me, [job(1, "2026-09-01T07:03:12+00:00"), job(2, "2026-10-01T07:03:12+00:00")])).toEqual([]);
    expect(bestFit(me, [])).toEqual([]);
  });

  it("keeps a job first seen exactly 30 days ago and drops it a moment later", () => {
    const edge = job(1, "2026-10-21T12:00:00+00:00");
    expect(ids(recentJobs([edge], NOW))).toEqual([1]);
    expect(ids(recentJobs([edge], NOW + 1))).toEqual([]);
  });

  it("leaves out a job whose date is missing or unreadable", () => {
    expect(recentJobs([job(1, null), job(2, "not a date"), job(3, undefined)], NOW)).toEqual([]);
  });

  it("an old perfect match no longer tops the list; the recent jobs keep their ranking", () => {
    const oldPerfect = job(1, "2026-10-01T00:00:00+00:00", { required_skills: ["python", "rag", "sql", "docker"] });
    const recentWeak = job(2, "2026-11-18T00:00:00+00:00", { required_skills: ["rust", "go", "java", "scala"] });
    const recentGood = job(3, "2026-11-10T00:00:00+00:00", { required_skills: ["python", "rag", "rust", "go"] });
    const all = [recentWeak, recentGood, oldPerfect];
    const full = { ...me, skills: ["python", "rag", "sql", "docker"] };
    expect(ids(rankJobs(full, all))[0]).toBe(1);          // without the age rule it wins
    expect(ids(bestFit(full, all))).toEqual([3, 2]);      // with it, it is gone
    // Same order the ranking alone gives the two recent jobs: the ranking did not change.
    expect(ids(bestFit(full, all))).toEqual(ids(rankJobs(full, [recentWeak, recentGood])));
  });

  it("returns a new list and leaves the one it was given untouched", () => {
    const jobs = [job(1, "2026-11-19T00:00:00+00:00"), job(2, "2026-09-01T00:00:00+00:00")];
    const before = [...jobs];
    const out = recentJobs(jobs, NOW);
    expect(out).not.toBe(jobs);
    expect(jobs).toEqual(before);
  });

  it("counts back from the present when no day is given", () => {
    const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
    const longAgo = new Date(Date.now() - 45 * 24 * 60 * 60 * 1000).toISOString();
    expect(ids(recentJobs([job(1, yesterday), job(2, longAgo)]))).toEqual([1]);
  });

  it("takes another number of days when asked, so the rule is not baked into the function", () => {
    const jobs = [job(1, "2026-11-19T00:00:00+00:00"), job(2, "2026-10-22T00:00:00+00:00")];
    expect(ids(recentJobs(jobs, NOW, 14))).toEqual([1]);
  });
});

describe("the job list's starting sort", () => {
  const filters = { query: "", cities: [], skillIds: [], window: "open" };
  const paint = (profile) => renderToStaticMarkup(<JobList filters={filters} setFilters={() => {}} profile={profile} taxonomy={{}} />);
  const sortMenu = (html) => html.match(/<select id="sort"[^>]*>(.*?)<\/select>/s)[1];
  const selected = (menu) => menu.match(/<option[^>]*\bselected=""[^>]*>(.*?)<\/option>/s)[1];

  it("is Newest first for someone with a profile", () => {
    expect(selected(sortMenu(paint(me)))).toBe("Newest first");
  });

  it("offers Best fit in the menu, named with its 30-day limit, without choosing it", () => {
    const menu = sortMenu(paint(me));
    expect(menu).toContain(`<option value="fit">Best fit (last ${FIT_DAYS} days)</option>`);
  });

  it("no profile: nothing changes — Newest first, and no Best fit in the menu", () => {
    const menu = sortMenu(paint(null));
    expect(selected(menu)).toBe("Newest first");
    expect(menu).not.toContain("Best fit");
    expect(menu.match(/<option/g)).toHaveLength(4);
  });

  it("no profile: the list is handed back as it came, never ranked or trimmed", () => {
    const old = [job(1, "2026-09-01T00:00:00+00:00")];
    expect(rankJobs(null, old)).toBe(old);
  });
});

// HIR-486: a posting stored but not read by the model yet (`read: false` from the API).
// Its skills and hard asks are unknown, not absent: the row and the job page say "not read
// yet" instead of an empty skill list, and Best fit leaves it out rather than ranking it
// among the jobs nothing rules out.
describe("a posting the model has not read yet", () => {
  const unread = job(7, "2026-11-20T08:00:00+00:00", { company: "Acme", status: "open", repost_count: 0, read: false,
    last_seen: "2026-11-20T08:00:00+00:00", sources: [{ source: "greenhouse", url: "https://example.com/7", first_seen: "2026-11-20T08:00:00+00:00" }],
    skills: [], proposed: [] });
  const readGood = job(8, "2026-11-19T08:00:00+00:00", { required_skills: ["python", "rag", "sql", "docker"], read: true });
  const readWeak = job(9, "2026-11-18T08:00:00+00:00", { required_skills: ["rust", "go", "java", "scala"], read: true });
  const row = (j) => renderToStaticMarkup(<Row job={j} open={false} onToggle={() => {}} profile={me} taxonomy={{}}
    saved={false} onSave={() => {}} getView={() => ({})} />);

  it("is marked in the job list; a read job is not", () => {
    expect(row(unread)).toContain(">not read yet</span>");
    expect(row({ ...unread, read: true })).not.toContain("not read yet");
    expect(row({ ...unread, read: undefined })).not.toContain("not read yet");   // older response: read
  });

  it("the job page and the opened row say it is not read, not that it asks for nothing", () => {
    const page = renderToStaticMarkup(<Detail job={unread} d={unread} profile={me} taxonomy={{}} cov={fit(me, unread)} />);
    expect(page).toContain("<b>Not read yet.</b>");
    expect(page).toContain("unknown, not missing");
    expect(page).not.toContain("none extracted");
    expect(page).not.toContain("Required · 0");
  });

  it("Best fit leaves it out of the ranking, and the foot says how many wait", () => {
    const out = bestFitList(me, [unread, readGood, readWeak], null, NOW);
    expect(ids(out.ranked)).toEqual([8, 9]);
    expect(out.waiting).toBe(1);
    expect(out.recent).toBe(3);
    // Same order the ranking gives the read jobs alone: the shared ranking is unchanged.
    expect(ids(out.ranked)).toEqual(ids(rankJobs(me, [readGood, readWeak])));
    expect(waitingLine(out.waiting)).toBe(" 1 new job is not read yet and left out until it is.");
    expect(waitingLine(3)).toBe(" 3 new jobs are not read yet and left out until they are.");
    expect(waitingLine(0)).toBe("");
  });

  it("without the rule it would sit above a read job that asks for German", () => {
    const german = job(10, "2026-11-19T08:00:00+00:00", { required_skills: ["python"], german: "required", read: true });
    expect(ids(rankJobs(me, [german, unread]))).toEqual([7, 10]);   // the bug
    expect(ids(bestFitList(me, [german, unread], null, NOW).ranked)).toEqual([10]);
  });

  it("in the Saved view it stays, below every read job", () => {
    expect(sortJobs([unread, readWeak, readGood], "fit", me).map((j) => j.id)).toEqual([8, 9, 7]);
  });
});
