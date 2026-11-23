// HIR-190: at phone width the skill chart's scale (0% … "80% of jobs") had five markers in
// a strip about 220px wide, and the fourth ran into the last. The fix is CSS: under the
// phone breakpoint every second marker is hidden, leaving the start, the middle and the end.
//
// vitest has no layout engine, so this cannot measure the overlap itself. What it holds on
// to is the two halves the fix depends on: the chart still writes all five markers (so the
// desktop scale is what it was), and the rule that hides two of them exists only inside the
// phone block and only for the skill chart's scale — the compare chart has its own
// three-marker scale and must not lose its middle one.
//
// HIR-393: since the chart sits beside the jobs list at desktop width (HIR-345) it has half
// the page, and the same two markers touched there ("60%80% of jobs"). Same fix, in the
// desktop block and only for a city page's two columns. So the rule now exists in exactly
// two places, and between the two widths, where the chart has the full page, all five show.
import { describe, it, expect, vi } from "vitest";
import { readFileSync } from "node:fs";
import { renderToStaticMarkup } from "react-dom/server";
import SkillChart, { ChartStatus } from "./SkillChart.jsx";
import App from "./App.jsx";
import { fetchSkills } from "./api.js";

const css = readFileSync(new URL("./styles.css", import.meta.url), "utf8");

// The body of the first `@media (<query>)` block, found by matching braces.
function mediaBlock(sheet, query) {
  const start = sheet.indexOf(`@media (${query})`);
  if (start < 0) return null;
  const open = sheet.indexOf("{", start);
  let depth = 0;
  for (let i = open; i < sheet.length; i++) {
    if (sheet[i] === "{") depth++;
    else if (sheet[i] === "}" && --depth === 0) return { body: sheet.slice(open + 1, i), start, end: i + 1 };
  }
  return null;
}
const phoneBlock = (sheet) => mediaBlock(sheet, "max-width: 720px");
// the block that also keeps the chart in view beside the jobs: the two-column widths
const besideJobsBlock = (sheet) => mediaBlock(sheet, "min-width: 1100px");

const HIDE = /\.bars-head \.axis span:nth-child\(even\)\s*\{\s*display:\s*none;?\s*\}/;
const HIDE_BESIDE_JOBS = /\.main\.split \.bars-head \.axis span:nth-child\(even\)\s*\{\s*display:\s*none;?\s*\}/;

describe("the skill chart's scale", () => {
  it("still writes five markers, the last one saying what the scale measures", () => {
    const data = { total: 10, skills: [{ skill_id: "python", display: "Python", count: 8, by_city: {} }] };
    const html = renderToStaticMarkup(<SkillChart data={data} selected={[]} onSelect={() => {}} />);
    const axis = html.match(/<div class="axis">(.*?)<\/div>/s)[1];
    const markers = axis.match(/<span\b[^>]*>.*?<\/span>/gs);
    expect(markers).toHaveLength(5);
    expect(markers[0]).toContain(">0%<");
    expect(markers[4]).toContain("% of jobs");
  });

  it("hides every second marker at phone width, so three are left", () => {
    const phone = phoneBlock(css);
    expect(phone).not.toBeNull();
    expect(phone.body).toMatch(HIDE);
  });

  it("hides every second marker beside the jobs list too, where the chart has half the page", () => {
    const beside = besideJobsBlock(css);
    expect(beside).not.toBeNull();
    expect(beside.body).toMatch(HIDE_BESIDE_JOBS);
    // the rule sits with the two columns: below that width the page is one column again
    expect(beside.body).toMatch(/\.main\.split > \.lead\s*\{[^}]*position:\s*sticky/);
    expect(css).toMatch(/@media \(max-width: 1099px\)\s*\{\s*\.main\.split\s*\{\s*grid-template-columns:\s*minmax\(0, 1fr\);\s*\}\s*\}/);
  });

  it("hides markers at those two widths only, and none of the compare chart's", () => {
    const [first, second] = [phoneBlock(css), besideJobsBlock(css)].sort((x, y) => x.start - y.start);
    const rest = css.slice(0, first.start) + css.slice(first.end, second.start) + css.slice(second.end);
    expect(rest).not.toMatch(/\.axis span[^{]*\{[^}]*display:\s*none/);
    // every rule in the sheet that hides a scale marker names the skill chart's head row
    const hiders = css.match(/[^{}]*\.axis span[^{]*\{[^}]*display:\s*none[^}]*\}/g) || [];
    expect(hiders).toHaveLength(2);
    for (const h of hiders) expect(h).toMatch(HIDE);
  });
});

// HIR-318: on 15 Nov the chart's numbers took over 15 seconds, and for all that time the
// chart box said "No jobs match these filters yet." beside a list of 274 open jobs. A
// request that failed outright left the same line there for good.
describe("the chart box before its numbers are in", () => {
  const NO_JOBS = "No jobs match these filters";
  const filters = { families: ["ml-engineer"] };

  // The page as first painted at this address: nothing has been fetched yet (effects do
  // not run here), which is exactly the state a slow answer leaves the page in.
  const firstPaint = (pathname) => {
    vi.stubGlobal("window", { location: { pathname, search: "", hash: "" } });
    try { return renderToStaticMarkup(<App />); } finally { vi.unstubAllGlobals(); }
  };

  it("says it is loading, not that no jobs match, while the page waits", () => {
    const html = firstPaint("/berlin");
    expect(html).toContain('id="chart-title"'); // the chart's page, not the home grid
    expect(html).toContain("Loading the chart");
    expect(html).not.toContain(NO_JOBS);
  });

  it("says the same in compare mode, instead of counting every city as empty", () => {
    const html = firstPaint("/compare/berlin+munich");
    expect(html).toContain('id="chart-title"');
    expect(html).toContain("Loading the chart");
    expect(html).not.toContain("Compare needs jobs in every market");
  });

  it("shows an error with a way to try again when the request failed", () => {
    const html = renderToStaticMarkup(<ChartStatus failed onRetry={() => {}} />);
    expect(html).toContain('role="alert"');
    expect(html).toContain("The chart could not be loaded");
    expect(html).toMatch(/<button\b[^>]*>Try again<\/button>/);
    expect(html).not.toContain(NO_JOBS);
    expect(html).not.toContain("Loading");
  });

  it("reports a failed request as failed, with no numbers, instead of throwing", async () => {
    const r = await fetchSkills(filters, () => Promise.reject(new Error("502 Bad Gateway")));
    expect(r).toEqual({ data: null, failed: true });
  });

  it("passes a good answer through, tagged with the job type it was asked for", async () => {
    const r = await fetchSkills(filters, () => Promise.resolve({ total: 0, skills: [] }));
    expect(r).toEqual({ data: { total: 0, skills: [], family: "ml-engineer" }, failed: false });
  });

  it("still says no jobs match when the answer really is zero jobs", () => {
    const html = renderToStaticMarkup(<SkillChart data={{ total: 0, skills: [] }} selected={[]} onSelect={() => {}} />);
    expect(html).toContain(NO_JOBS);
  });
});
