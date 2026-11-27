// @vitest-environment jsdom
// HIR-479: on a city page the chart's column scrolls on its own beside the jobs (HIR-345),
// and the hover box, drawn inside that column, was cut off at its edge and gave the card a
// sideways scrollbar. The box now hangs on the page and is kept inside the window; on one
// city's page it no longer lists the other cities; long skill names wrap instead of being
// cut. jsdom has no layout, so the placement is checked through placeTip, and the rest
// through what is rendered and the stylesheet.
import { describe, it, expect, afterEach } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { act } from "react";
import { createRoot } from "react-dom/client";
import SkillChart, { placeTip } from "./SkillChart.jsx";

globalThis.IS_REACT_ACT_ENVIRONMENT = true;
// a path, not import.meta.url: under jsdom that URL is not a file:// one
const css = readFileSync(fileURLToPath(new URL("./styles.css", `file://${__filename}`)), "utf8");
const rule = (selector) => {
  const at = css.indexOf(`${selector} {`);
  return at < 0 ? null : css.slice(at, css.indexOf("}", at));
};

describe("where the hover box goes", () => {
  const box = { width: 260, height: 60 };
  const win = { vw: 1100, vh: 800 };

  it("opens to the right of the pointer when there is room", () => {
    expect(placeTip({ x: 300, top: 200 }, box, win)).toEqual({ left: 312, top: 188 });
  });

  it("opens to the left of the pointer near the right edge", () => {
    const { left } = placeTip({ x: 1000, top: 200 }, box, win);
    expect(left + box.width).toBeLessThanOrEqual(1000);
  });

  it("stays inside the window on a phone, at the top and at the bottom", () => {
    for (const x of [0, 50, 180, 300, 352]) {
      for (const top of [0, 400, 790]) {
        const p = placeTip({ x, top }, box, { vw: 360, vh: 640 });
        expect(p.left).toBeGreaterThanOrEqual(8);
        expect(p.left + box.width).toBeLessThanOrEqual(352);
        expect(p.top).toBeGreaterThanOrEqual(8);
        expect(p.top + box.height).toBeLessThanOrEqual(632);
      }
    }
  });
});

describe("the hover box on a city page", () => {
  let root;
  let host;
  afterEach(() => {
    act(() => root.unmount());
    host.remove();
  });

  const data = {
    total: 155,
    skills: [
      { skill_id: "evaluation", display: "Evaluation", count: 45, by_city: { "San Francisco": 45, London: 4, Munich: 3 } },
      { skill_id: "distributed-systems", display: "Distributed Systems", count: 30, by_city: { "San Francisco": 30 } },
    ],
  };

  function hoverFirstBar(props = {}) {
    host = document.createElement("div");
    document.body.appendChild(host);
    root = createRoot(host);
    act(() => root.render(<SkillChart data={data} selected={[]} onSelect={() => {}} jobsLabel="open AI Engineer jobs" {...props} />));
    const bar = host.querySelector(".bar-row");
    act(() => bar.dispatchEvent(new MouseEvent("mouseover", { bubbles: true, clientX: 400, clientY: 120 })));
    return document.querySelector(".tip");
  }

  it("is drawn on the page, outside the chart, so no scrolling box can cut it off", () => {
    const tip = hoverFirstBar();
    expect(tip).not.toBeNull();
    expect(host.contains(tip)).toBe(false);
    expect(tip.parentElement).toBe(document.body);
  });

  it("says the skill, its count and share of the filtered jobs, and that a click filters", () => {
    const text = hoverFirstBar().textContent;
    expect(text).toContain("Evaluation");
    expect(text).toContain("45 jobs · 29% of 155 open AI Engineer jobs");
    expect(text).toContain("Click to filter the jobs");
  });

  it("does not list the other cities", () => {
    const text = hoverFirstBar().textContent;
    expect(text).not.toContain("London");
    expect(text).not.toContain("Munich");
  });

  it("goes away when anything scrolls, since it would no longer sit by its bar", () => {
    hoverFirstBar();
    act(() => host.dispatchEvent(new Event("scroll")));
    expect(document.querySelector(".tip")).toBeNull();
  });
});

describe("the stylesheet", () => {
  it("fixes the hover box to the window", () => {
    expect(rule(".tip")).toMatch(/position:\s*fixed/);
  });

  it("wraps a long skill name onto two lines instead of cutting it", () => {
    const label = rule(".bar-row .name .label");
    expect(label).not.toBeNull();
    expect(label).toMatch(/-webkit-line-clamp:\s*2/);
    expect(label).not.toMatch(/nowrap|ellipsis/);
    expect(rule(".bar-row")).toMatch(/min-height:\s*32px/);
    expect(rule(".bar-row")).not.toMatch(/[^-]height:\s*32px/);
  });

  it("does not hide a sideways scroll on the chart's column instead of removing its cause", () => {
    const chartRules = css.split("\n").filter((l) => /\.(lead|chart|bars|bar-row|track)\b/.test(l));
    for (const l of chartRules) expect(l).not.toMatch(/overflow-x:\s*hidden/);
  });
});
