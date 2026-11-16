// Playwright config for the robot visitor (HIR-258): e2e/site-watch.spec.js against the
// LIVE site, run after every deploy, every morning, and by hand (.github/workflows/site-watch.yml).
//
// Env: WATCH_URL (site origin, required), WATCH_AUTH ("user:password" for the site's
// login, optional), WATCH_OUT (default watch-out/: report.json, and a screenshot of every
// failing test under results/), WATCH_CHROME (an installed Chrome, where Playwright's own
// download is blocked).
import { defineConfig } from "@playwright/test";

const OUT = process.env.WATCH_OUT || "watch-out";
const [username, ...rest] = (process.env.WATCH_AUTH || "").split(":");

export default defineConfig({
  testDir: "e2e",
  testMatch: "site-watch.spec.js",
  outputDir: `${OUT}/results`,
  workers: 1,
  // One retry: a single slow response from the live site is not a break worth a ticket.
  retries: 1,
  timeout: 60_000,
  expect: { timeout: 15_000 },
  reporter: [["list"], ["json", { outputFile: `${OUT}/report.json` }]],
  use: {
    baseURL: process.env.WATCH_URL || "http://localhost:8000",
    httpCredentials: username ? { username, password: rest.join(":") } : undefined,
    screenshot: "only-on-failure",
    video: "off",
    trace: "off",
    launchOptions: process.env.WATCH_CHROME ? { executablePath: process.env.WATCH_CHROME } : {},
  },
  projects: [
    { name: "desktop", use: { viewport: { width: 1440, height: 900 } } },
    { name: "phone", use: { viewport: { width: 412, height: 915 }, isMobile: true, hasTouch: true } },
  ],
});
