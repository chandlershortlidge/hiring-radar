// HIR-190: at phone width the skill chart's scale (0% … "80% of jobs") had five markers in
// a strip about 220px wide, and the fourth ran into the last. The fix is CSS: under the
// phone breakpoint every second marker is hidden, leaving the start, the middle and the end.
//
// vitest has no layout engine, so this cannot measure the overlap itself. What it holds on
// to is the two halves the fix depends on: the chart still writes all five markers (so the
// desktop scale is what it was), and the rule that hides two of them exists only inside the
// phone block and only for the skill chart's scale — the compare chart has its own
// three-marker scale and must not lose its middle one.
import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { renderToStaticMarkup } from "react-dom/server";
import SkillChart from "./SkillChart.jsx";

const css = readFileSync(new URL("./styles.css", import.meta.url), "utf8");

// The body of the `@media (max-width: 720px)` block, found by matching braces.
function phoneBlock(sheet) {
  const start = sheet.indexOf("@media (max-width: 720px)");
  if (start < 0) return null;
  const open = sheet.indexOf("{", start);
  let depth = 0;
  for (let i = open; i < sheet.length; i++) {
    if (sheet[i] === "{") depth++;
    else if (sheet[i] === "}" && --depth === 0) return { body: sheet.slice(open + 1, i), start, end: i + 1 };
  }
  return null;
}

const HIDE = /\.bars-head \.axis span:nth-child\(even\)\s*\{\s*display:\s*none;?\s*\}/;

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

  it("hides no marker outside the phone block, and none of the compare chart's", () => {
    const phone = phoneBlock(css);
    const rest = css.slice(0, phone.start) + css.slice(phone.end);
    expect(rest).not.toMatch(/\.axis span[^{]*\{[^}]*display:\s*none/);
    // every rule in the sheet that hides a scale marker names the skill chart's head row
    const hiders = css.match(/[^{}]*\.axis span[^{]*\{[^}]*display:\s*none[^}]*\}/g) || [];
    expect(hiders).toHaveLength(1);
    expect(hiders[0]).toMatch(HIDE);
  });
});
