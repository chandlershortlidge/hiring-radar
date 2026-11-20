// HIR-285: the look Chandler chose (colours 14 Nov, layout 17 Nov), held to the pieces
// that carry it. The rules themselves are in docs/style.md.
//
// vitest has no layout engine, so nothing here measures a pixel. It holds the numbers the
// new parts print, the states they draw, and the one rule a stylesheet can be read for:
// colours come from the palette's variables.
import { describe, it, expect, vi } from "vitest";
import { readFileSync } from "node:fs";
import { renderToStaticMarkup } from "react-dom/server";
import App from "./App.jsx";
import FitLine, { cityFit } from "./FitLine.jsx";
import FilterPills, { germanLabel, seniorityLabel } from "./FilterPills.jsx";
import { Headline, HeroChart, heroFacts, heroPlace, heroRoles } from "./HomeHero.jsx";
import { ConnectPill, ConnectStrip } from "./ConnectClaude.jsx";
import { isBestFit } from "./JobList.jsx";
import { placeBySlug } from "./format.js";

const css = readFileSync(new URL("./styles.css", import.meta.url), "utf8");
const firstPaint = (pathname) => {
  vi.stubGlobal("window", { location: { pathname, search: "", hash: "" } });
  try { return renderToStaticMarkup(<App />); } finally { vi.unstubAllGlobals(); }
};

// Chart rows as /api/skills sends them: most asked for first.
const row = (id, count, by_city = {}) => ({ skill_id: id, display: id.toUpperCase(), count, by_city });
const ROWS = Array.from({ length: 20 }, (_, i) => row(`s${i + 1}`, 100 - i * 5));

describe("the palette", () => {
  it("is the one Chandler chose", () => {
    for (const [name, hex] of [["ground", "#F9F7F5"], ["stone", "#EEE8E1"], ["warm-grey", "#D0C3B7"], ["ink", "#1F1A1C"],
      ["ink-2", "#6B5F63"], ["plum", "#603C5F"], ["plum-tint", "#CFC4CF"], ["peach", "#FAB995"], ["coral", "#F38155"], ["butter", "#FCDEA6"]]) {
      expect(css).toContain(`--${name}: ${hex};`);
    }
  });

  it("is the only place a colour is written: the rest of the sheet uses the variables", () => {
    // Left out: the palette itself, and the skill tree's three branch hues, which are a
    // recorded decision of their own and are not on the page.
    const rest = css.slice(css.indexOf("* { box-sizing")).split("\n").filter((l) => !/tree|swatch|#3987e5/.test(l)).join("\n");
    const hexes = (rest.match(/#[0-9a-fA-F]{3,8}\b/g) || []).filter((h) => h.toLowerCase() !== "#fff");
    expect(hexes).toEqual([]);
  });

  it("never fills with coral, and draws a missing skill as a colour, not a pattern", () => {
    expect(css).not.toMatch(/background(-color)?:\s*var\(--coral\)/);
    expect(css).toMatch(/\.fill\.gap \{ background: var\(--plum-tint\); \}/);
    expect(css).not.toContain("repeating-linear-gradient(135deg");
  });

  it("uses the brand gradient once, for the rule under the header", () => {
    expect(css.match(/var\(--brand-gradient\)/g)).toHaveLength(1);
    expect(firstPaint("/")).toContain('class="brand-rule"');
  });
});

describe("the home page's headline and chart", () => {
  const data = { family: null, city_totals: { Berlin: 100, Munich: 10 }, skills: [
    row("python", 0, { Berlin: 67, Munich: 5 }), row("agents", 0, { Berlin: 29 }), row("llms", 0, { Berlin: 41 }),
  ] };

  it("leads with Berlin for a first visit, and with the market last looked at after that", () => {
    expect(heroPlace([]).name).toBe("Berlin");
    expect(heroPlace(["munich", "berlin"]).name).toBe("Munich");
  });

  it("skips All of Germany and places we no longer have: neither has numbers of its own", () => {
    expect(heroPlace(["all-germany", "hamburg"]).name).toBe("Hamburg");
    expect(heroPlace(["atlantis"]).name).toBe("Berlin");
  });

  it("names the two most-asked-for skills, in order, with that market's own shares", () => {
    const { top, open, roles } = heroFacts(data, { Berlin: 120 }, placeBySlug("berlin"));
    expect(open).toBe(120);
    expect(top.map((s) => [s.name, s.pct])).toEqual([["PYTHON", 67], ["LLMS", 41], ["AGENTS", 29]]);
    const html = renderToStaticMarkup(<Headline top={top} place="Berlin" roles={roles} />);
    expect(html).toBe("<h1><mark>67%</mark> of AI &amp; data jobs in Berlin ask for PYTHON. <mark>41%</mark> ask for LLMS.</h1>");
  });

  it("says which roles the numbers are for once a job family is chosen", () => {
    expect(heroRoles("ml-engineer")).toBe("ML Engineer jobs");
    const facts = heroFacts({ ...data, family: "ml-engineer" }, { Berlin: 120 }, placeBySlug("berlin"));
    expect(facts.roles).toBe("ML Engineer jobs");
    expect(facts.open).toBe(100); // the family's own count, not every role's
  });

  it("falls back to saying what the page is for when there are not two skills to name", () => {
    for (const top of [undefined, [], [{ name: "Python", pct: 50 }]]) {
      expect(renderToStaticMarkup(<Headline top={top} place="Hamburg" roles="AI & data jobs" />))
        .toBe("<h1>What are employers actually asking for?</h1>");
    }
    expect(firstPaint("/")).toContain("What are employers actually asking for?"); // before any numbers
  });

  it("links the chart to that market's full page, keeping the job family", () => {
    const top = [{ name: "Python", pct: 67 }, { name: "LLMs", pct: 41 }];
    const html = renderToStaticMarkup(<HeroChart place={placeBySlug("berlin")} family="ml-engineer" top={top} open={271} onOpen={() => {}} />);
    expect(html).toContain('href="/berlin/ml-engineer"');
    expect(html).toContain("Open the full Berlin chart and its 271 jobs");
    expect(html).toContain("width:83.75%"); // 67 on a scale that ends at 80
  });

  it("says the chart is loading, not that the market is empty, before the numbers arrive", () => {
    const at = (loading) => renderToStaticMarkup(<HeroChart place={placeBySlug("berlin")} top={[]} open={0} loading={loading} onOpen={() => {}} />);
    expect(at(true)).toContain("Loading the chart");
    expect(at(false)).toContain("No jobs here yet");
  });

  it("starts the pickers on the lead market, so compare is one pick away", () => {
    const html = firstPaint("/");
    expect(html).toMatch(/<button[^>]*class="qb-btn"[^>]*>Berlin</);
    expect(html).not.toContain("Pick a city");
  });
});

describe("the fit line on a city page", () => {
  const profile = { skills: ["s1", "s2", "s4", "s17"] };

  it("counts the profile against the 15 most-asked-for skills, not the whole chart", () => {
    const f = cityFit(profile, ROWS, 200);
    expect([f.have, f.of]).toEqual([3, 15]); // s17 is in the profile but outside the top 15
  });

  it("names the three biggest gaps, most asked for first, with their share of jobs", () => {
    expect(cityFit(profile, ROWS, 200).gaps).toEqual([
      { id: "s3", name: "S3", pct: 45 }, { id: "s5", name: "S5", pct: 40 }, { id: "s6", name: "S6", pct: 38 },
    ]);
  });

  it("says how many skills there are when the market has fewer than 15", () => {
    const f = cityFit(profile, ROWS.slice(0, 4), 200);
    expect([f.have, f.of]).toEqual([3, 4]);
    expect(f.gaps.map((g) => g.id)).toEqual(["s3"]);
  });

  it("names no gap when the profile has them all", () => {
    expect(cityFit({ skills: ["s1", "s2"] }, ROWS.slice(0, 2), 10)).toEqual({ have: 2, of: 2, gaps: [] });
  });

  it("reads as one sentence with the place in it", () => {
    const html = renderToStaticMarkup(<FitLine profile={profile} data={{ total: 200, skills: ROWS }} place="Berlin" />);
    expect(html).toContain("You have <mark>3 of the 15</mark> skills Berlin asks for most.");
    expect(html).toContain('<span class="gap-chip">S3 <span class="mono">45%</span></span>');
  });

  it("is not shown without profile skills, or before the chart's numbers are in", () => {
    const data = { total: 200, skills: ROWS };
    for (const [p, d] of [[null, data], [{ skills: [] }, data], [profile, null], [profile, { total: 0, skills: [] }]]) {
      expect(renderToStaticMarkup(<FitLine profile={p} data={d} place="Berlin" />)).toBe("");
    }
    expect(firstPaint("/berlin")).not.toContain("fitline");
  });
});

describe("the chart's filters as pills", () => {
  const base = { requirement: "required", seniorities: [], german: "any" };
  const render = (filters, extraOn = 0) => renderToStaticMarkup(
    <FilterPills filters={{ ...base, ...filters }} set={() => {}} toggleSeniority={() => {}} requiredLabel="Required only" extraOn={extraOn}>
      <span id="extra" />
    </FilterPills>);

  it("shows Required only as on by default and off when nice-to-have is included", () => {
    expect(render({})).toContain('aria-pressed="true">Required only<');
    expect(render({ requirement: "all" })).toContain('aria-pressed="false">Required only<');
  });

  it("says which seniority levels are on, in the pill itself", () => {
    expect(seniorityLabel([])).toBe("Any seniority");
    expect(seniorityLabel(["mid", "senior"])).toBe("Mid + Senior");
    expect(render({ seniorities: ["senior"] })).toMatch(/class="fpill on"[^>]*>Senior</);
  });

  it("words each German choice so it reads without a label beside it", () => {
    expect(germanLabel("any")).toBe("Any German");
    expect(germanLabel("not_required")).toBe("German: not required");
    const html = render({ german: "required" });
    expect(html).toContain('<label class="fpill pick on">');
    expect(html.match(/<option/g)).toHaveLength(4);
  });

  it("keeps the less-used filters closed until asked for, and open while one is set", () => {
    expect(render({})).not.toContain('id="extra"');
    const on = render({}, 2);
    expect(on).toContain('id="extra"');
    expect(on).toContain("More filters · 2");
  });
});

describe("Connect Claude", () => {
  it("is in the header of every page and on top of a city's jobs, but not on a comparison's", () => {
    for (const path of ["/", "/berlin", "/compare/berlin+munich"]) expect(firstPaint(path)).toContain('class="pill connect"');
    expect(firstPaint("/")).toContain('class="mcp-wrap"');
    expect(firstPaint("/berlin")).toMatch(/<section class="card jobs"[^>]*><aside class="mcp"/);
    expect(firstPaint("/compare/berlin+munich")).not.toContain('class="mcp"');
  });

  it("is a label, not a control, until there is something to connect to", () => {
    const html = renderToStaticMarkup(<><ConnectPill /><ConnectStrip /></>);
    expect(html).not.toMatch(/<(button|a)\b/);
    expect(html).toContain("Not available yet");
  });
});

describe("a city page's layout", () => {
  it("puts the chart and the jobs side by side for one city, and in one column for a comparison", () => {
    expect(firstPaint("/berlin")).toContain('<main class="main split">');
    expect(firstPaint("/compare/berlin+munich")).toContain('<main class="main">');
    expect(css).toMatch(/@media \(max-width: 1099px\) \{ \.main\.split \{ grid-template-columns: minmax\(0, 1fr\); \} \}/);
  });

  // HIR-345: the jobs list is far longer than the chart, so the chart has to follow it down.
  it("keeps the chart in view beside the jobs on a wide screen, never taller than the window", () => {
    const wide = css.slice(css.indexOf("@media (min-width: 1100px) {"));
    expect(wide).toMatch(/\.main\.split > \.lead \{ position: sticky; top: 16px; max-height: calc\(100vh - 32px\); overflow-y: auto; \}/);
    // the jobs get half the page, not the smaller share
    expect(css).toContain(".main.split { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); align-items: start; }");
  });

  it("moves What's rising out of the column that stays in view, to under the jobs", () => {
    const html = firstPaint("/berlin");
    const [lead, side, jobs, below] = ['<div class="stack lead">', '<div class="stack side">', '<section class="card jobs"', '<div class="below">'].map((t) => html.indexOf(t));
    expect(lead).toBeGreaterThan(-1);
    expect(side).toBeGreaterThan(lead);
    expect(jobs).toBeGreaterThan(side);
    expect(below).toBeGreaterThan(jobs);
    // a comparison has no single market to follow, so no such card and no empty box for it
    expect(firstPaint("/compare/berlin+munich")).not.toContain('class="below"');
  });

  it("stacks in the old order on a narrow screen: chart, what's rising, related skills, jobs", () => {
    const narrow = css.slice(css.lastIndexOf("@media (max-width: 1099px) {\n"));
    for (const rule of [".main.split > .stack { display: contents; }", ".main.split > .lead > * { order: 3; }", ".main.split > .lead > :first-child { order: 1; }",
      ".main.split > .side > .below { order: 2; }", ".main.split > .side > :first-child { order: 4; }"]) expect(narrow).toContain(rule);
  });
});

describe("the butter best-fit badge", () => {
  it("is for 90% and up", () => {
    expect(isBestFit({ score: 0.9, thin: false })).toBe(true);
    expect(isBestFit({ score: 1, thin: false })).toBe(true);
    expect(isBestFit({ score: 0.89, thin: false })).toBe(false);
  });

  it("is never given to a job that listed too few skills to score, or has no score", () => {
    expect(isBestFit({ score: 1, thin: true })).toBe(false);
    expect(isBestFit({ score: null, thin: false })).toBe(false);
  });
});
