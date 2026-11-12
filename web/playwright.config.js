// Playwright config for PR before/after screenshots (HIR-231, replacing HIR-214's demo).
//
// Does: open two builds of the dashboard — main's and the branch's — against the LIVE
// site's data, screenshot the same views of each, and keep only the pairs that differ.
// Does NOT: start a server, use a demo database, record video, or run in `npm test`
// (vitest ignores e2e/). See e2e/before-after.spec.js for how the two builds are served.
//
// Env: SHOT_BEFORE / SHOT_AFTER (the two web/dist folders), SHOT_LIVE (live site origin),
// SHOT_AUTH ("user:password" for the site's login), SHOT_OUT (default shots-out/).
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "e2e",
  testMatch: "before-after.spec.js",
  outputDir: `${process.env.SHOT_OUT || "shots-out"}/_playwright`,
  workers: 1,
  retries: 0,
  reporter: [["list"]],
  use: {
    // A made-up host: every request is answered by the spec itself, never by DNS.
    baseURL: "http://radar.test",
    video: "off",
    screenshot: "off",
    // Use an installed Chrome instead of Playwright's download, where that is blocked.
    launchOptions: process.env.SHOT_CHROME ? { executablePath: process.env.SHOT_CHROME } : {},
  },
  projects: [
    { name: "desktop", use: { viewport: { width: 1440, height: 900 } } },
    // Phone-sized, at pixel ratio 1 and not in Chrome's mobile mode. Both mobile mode
    // (text autosizing) and a pixel ratio above 1 make text land a pixel or two
    // differently on each load, so two identical builds would always "differ".
    { name: "phone", use: { viewport: { width: 412, height: 915 }, deviceScaleFactor: 1 } },
  ],
});
