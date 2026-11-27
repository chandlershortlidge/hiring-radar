// The header's buttons. HIR-346 took "Add a job" and the proposed-skills counter off the
// site for good (jobs are added from the command line, proposed skills are settled in
// skill-list pull requests), so the one button left is the profile; "Connect Claude" is
// not a button.
//
// HIR-263 still holds for whatever is there: at phone width a header button's words are
// hidden with display:none, which removes them for screen readers too, so every button
// needs a name that does not depend on them: an aria-label on the button itself.
//
// Renders the page the way the browser's first paint does (no jsdom: the page only
// touches the document from effects, which do not run here). The one thing it reads
// while rendering is the address bar, so that is all the stand-in window provides.
import { describe, it, expect, beforeAll, afterAll, vi } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { readFileSync } from "node:fs";
import App from "./App.jsx";

let buttons;
let header;

beforeAll(() => {
  vi.stubGlobal("window", { location: { pathname: "/berlin", search: "", hash: "" } });
  const html = renderToStaticMarkup(<App />);
  const actions = html.match(/<div class="hdr-actions">(.*?)<\/div>/s);
  header = actions ? actions[1] : null;
  buttons = header ? header.match(/<button\b[^>]*>/g) : null;
});

afterAll(() => vi.unstubAllGlobals());

describe("the header's buttons", () => {
  it("is the profile button and nothing else", () => {
    expect(buttons).toHaveLength(1);
    expect(buttons[0]).toContain('aria-label="Your profile"');
  });

  // HIR-477 took the "All markets" pill out: the logo already goes home.
  it("offers the profile and Connect Claude on a city page, and no more", () => {
    const words = header.replace(/<svg.*?<\/svg>/gs, "").replace(/<[^>]+>/g, "|").split("|").filter(Boolean);
    expect(words[0]).toBe("Set up your profile");
    expect(words[1].trim()).toBe("Connect Claude");
    // Two pills and no main button: whatever else Connect Claude says sits inside its own pill.
    expect(header.match(/class="pill\b/g)).toHaveLength(2);
    expect(header).not.toContain('class="btn');
  });

  it("has no add-a-job button and no proposed-skills counter (HIR-346)", () => {
    const source = readFileSync(new URL("./App.jsx", import.meta.url), "utf8");
    for (const gone of ["Add a job", "proposed skills", "proposed_pending", "AddJobDrawer", "ReviewDrawer"]) {
      expect(source).not.toContain(gone);
    }
  });

  it("leaves no header button whose only name is words a phone hides", () => {
    for (const b of buttons) expect(b).toMatch(/aria-label="[^"]+"/);
  });
});

// HIR-284: the run-on line of statistics above the chart ("944 jobs · 739 currently open
// (Berlin 256 · …) · 397 companies · 244 skills tracked · … · last updated 14 h ago") was
// removed on Chandler's call: nobody reads it. Open jobs per city live on the home page's
// market cards instead. The block only rendered once /api/stats had answered, which the
// static render above never reaches, so this holds the line on the source: none of the
// wording that existed only in that block may come back.
describe("the statistics line above the chart", () => {
  const source = readFileSync(new URL("./App.jsx", import.meta.url), "utf8");

  it.each(["skills tracked", "too short, not charted", "legacy, not charted", "of those open now", "last updated", "need German", 'className="stats"'])(
    'is gone: the page no longer says "%s"', (words) => {
      expect(source).not.toContain(words);
    });
});

// HIR-412: on a city or compare page the bar with the job-family and city pickers said
// "1289 open jobs · updated 18 h ago" on its right edge. That number was every open job on
// the site, while the jobs card below says "78 open jobs · Berlin" for the search the
// visitor is looking at: two "open jobs" numbers that disagree. The bar now says only how
// fresh the data is. Like the block above, that text only renders once /api/stats has
// answered, so this holds the line on the source.
describe("the right edge of the pickers' bar", () => {
  const source = readFileSync(new URL("./App.jsx", import.meta.url), "utf8");

  it("no longer counts open jobs: the jobs card is the only place that does", () => {
    expect(source).not.toContain("open jobs");
  });

  it("still says how fresh the data is", () => {
    expect(source).toContain(">updated {timeAgo(stats.last_updated)}</span>");
  });
});

// HIR-477, Chandler 25 Nov with screenshots: "we need to remove these." The header's
// tagline, the "All markets" pill, and the chart's heading with its explanation line went.
// What the percentages are moved under the chart, in place of the click/hover hint.
describe("the text Chandler had removed", () => {
  const page = (pathname) => {
    vi.stubGlobal("window", { location: { pathname, search: "", hash: "" } });
    try { return renderToStaticMarkup(<App />); } finally { vi.unstubAllGlobals(); }
  };

  it.each(["/", "/berlin", "/compare/berlin+munich"])("is gone from %s", (path) => {
    const html = page(path);
    expect(html).not.toContain("Skills employers ask for");
    expect(html).not.toContain("All markets");
    expect(html).not.toContain("asking for?");
    expect(html).not.toContain('class="lede"');
    expect(html).not.toContain("Click a bar to filter");
    expect(html).not.toContain("Click a city header");
  });

  it.each(["/", "/berlin", "/compare/berlin+munich"])("leaves the logo going home on %s", (path) => {
    expect(page(path)).toMatch(/<a href="\/"[^>]*aria-label="hiring-radar home"/);
  });

  it("names the city chart for screen readers, and keeps one <h1> on the page", () => {
    const html = page("/berlin");
    expect(html).toContain('<section class="card chart" aria-label="Skills asked for in Berlin">');
    expect(html.match(/<h1\b/g)).toHaveLength(1);
    expect(html).toMatch(/<h1 id="chart-title" class="sr">Skills asked for in Berlin<\/h1>/);
  });

  // The cities only reach the compare chart's filters after first paint (an effect), as they
  // did for the old heading, so this checks the section has a name, not which one.
  it("names the compare chart for screen readers, and keeps one <h1> on the page", () => {
    const html = page("/compare/berlin+munich");
    expect(html).toMatch(/<section class="card chart" aria-label="Skills asked for in [^"]+">/);
    expect(html.match(/<h1\b/g)).toHaveLength(1);
  });
});
