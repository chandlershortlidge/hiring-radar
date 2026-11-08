// Playwright config for the PR walkthrough (HIR-214).
//
// Does: drive a real browser through the dashboard and save screenshots plus a screen
// recording, so a PR carries evidence of what it changes on screen.
// Does NOT: start the server, seed data, assert on pixels, or run in `npm test` (vitest
// ignores e2e/). The server is started by the caller — the "PR demo" workflow, or by
// hand: seed a scratch DB with scripts/seed_demo.py, `python -m app serve`, then
// `DEMO_URL=http://127.0.0.1:8000 npx playwright test`.
//
// Evidence lands in DEMO_OUT (default demo-out/): <project>/NN-name.png and the video
// Playwright records per test under <project>/video/.
import { defineConfig, devices } from "@playwright/test";

const out = process.env.DEMO_OUT || "demo-out";

export default defineConfig({
  testDir: "e2e",
  outputDir: `${out}/_playwright`,
  // One walkthrough, run in order: parallel workers would interleave two recordings.
  workers: 1,
  retries: 0,
  reporter: [["list"]],
  use: {
    baseURL: process.env.DEMO_URL || "http://127.0.0.1:8000",
    video: "on",
    screenshot: "off", // the walkthrough takes its own, named ones
    // Use an installed Chrome instead of Playwright's download, where that is blocked.
    launchOptions: process.env.DEMO_CHROME ? { executablePath: process.env.DEMO_CHROME } : {},
  },
  projects: [
    { name: "desktop", use: { viewport: { width: 1440, height: 900 }, video: { mode: "on", size: { width: 1440, height: 900 } } } },
    { name: "phone", use: { ...devices["Pixel 7"] } },
  ],
});
