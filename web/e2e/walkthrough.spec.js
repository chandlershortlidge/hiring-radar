// The PR walkthrough (HIR-214): the same short path through the dashboard on every run, so
// "before" (main) and "after" (the branch) screenshots line up one to one.
//
// Does: visit each main view by its address, wait for the data to load, save a named
// screenshot, and leave a pause between steps so the recording is watchable.
// Does NOT: assert on content or pixels. It is evidence, not a test that can fail a PR —
// it navigates by URL rather than clicking specific buttons so it still runs on `main`
// when a branch renames or moves a control. A step whose page fails to load is still
// captured (the screenshot shows the failure), and the walkthrough carries on.
//
// Runs against the fake demo database (scripts/seed_demo.py): Berlin + San Francisco.
import { test } from "@playwright/test";
import { mkdirSync } from "node:fs";

const OUT = process.env.DEMO_OUT || "demo-out";

const STEPS = [
  ["home", "/"],
  ["city", "/berlin"],
  ["city-family", "/berlin/ai-engineer"],
  ["compare", "/compare/berlin+san-francisco"],
  ["job", "/jobs/1"],
];

test("walkthrough", async ({ page }, info) => {
  const dir = `${OUT}/${info.project.name}`;
  mkdirSync(dir, { recursive: true });

  for (const [i, [name, path]] of STEPS.entries()) {
    await page.goto(path);
    // The dashboard fetches after first paint; networkidle is "the API calls finished".
    // Capped so a hung request costs seconds, not the job.
    await page.waitForLoadState("networkidle", { timeout: 15_000 }).catch(() => {});
    await page.waitForTimeout(600);
    const file = `${dir}/${String(i + 1).padStart(2, "0")}-${name}.png`;
    await page.screenshot({ path: file, fullPage: true });

    // Scroll through long pages so the recording shows below the fold too.
    const h = await page.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < Math.min(h, 3000); y += 400) {
      await page.mouse.wheel(0, 400);
      await page.waitForTimeout(150);
    }
    await page.waitForTimeout(400);
  }
});
