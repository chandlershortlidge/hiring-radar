// PR before/after screenshots (HIR-231).
//
// Does: for each view, render main's build ("before") and the branch's build ("after")
// in the same browser, seconds apart, against the same live data; save both screenshots
// only when they differ, and write changed.json listing those views.
// Does NOT: write anything to the live site — only GET /api requests are passed through,
// everything else is refused. Does not assert: it is evidence for review, never a gate.
//
// How the two builds are served without a server: every request to http://radar.test is
// intercepted. /api GETs are fetched from SHOT_LIVE with the site login; any other path is
// answered from the build folder (a file if it exists, else index.html, as the real app's
// catch-all route does).
import { test } from "@playwright/test";
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { extname, join, normalize, resolve } from "node:path";

const OUT = process.env.SHOT_OUT || "shots-out";
const LIVE = (process.env.SHOT_LIVE || "").replace(/\/$/, "");
const AUTH = process.env.SHOT_AUTH;
const SIDES = { before: process.env.SHOT_BEFORE, after: process.env.SHOT_AFTER };
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml",
  ".png": "image/png", ".ico": "image/x-icon", ".json": "application/json", ".woff2": "font/woff2" };
const authHeader = () => ({ authorization: "Basic " + Buffer.from(AUTH).toString("base64") });

async function serve(page, dist) {
  const root = resolve(dist);
  await page.unroute("**/*");
  await page.route("**/*", async (route) => {
    const req = route.request();
    const url = new URL(req.url());
    // The real page's web fonts load as on the live site; anything else off-site is refused.
    if (url.host === "fonts.googleapis.com" || url.host === "fonts.gstatic.com") return route.continue();
    if (url.host !== "radar.test") return route.abort();
    if (url.pathname.startsWith("/api/")) {
      if (req.method() !== "GET") return route.abort(); // never write to the live site
      const res = await route.fetch({ url: LIVE + url.pathname + url.search, headers: authHeader() });
      return route.fulfill({ response: res });
    }
    let file = join(root, normalize(url.pathname));
    if (!file.startsWith(root) || !existsSync(file) || statSync(file).isDirectory()) file = join(root, "index.html");
    return route.fulfill({ body: readFileSync(file), contentType: TYPES[extname(file)] || "application/octet-stream" });
  });
}

async function shot(page, path) {
  await page.goto(path);
  await page.waitForLoadState("networkidle", { timeout: 20_000 }).catch(() => {});
  // Text laid out before the web font arrives sits a pixel or two off; wait for the fonts.
  await page.evaluate(() => document.fonts.ready).catch(() => {});
  await page.waitForTimeout(800);
  return page.screenshot({ fullPage: true, animations: "disabled" });
}

test("before and after", async ({ page, request }, info) => {
  test.skip(!LIVE || !AUTH, "SHOT_LIVE / SHOT_AUTH not set");
  test.setTimeout(180_000);

  // One real job for the job page: the newest one on the live site.
  const res = await request.get(`${LIVE}/api/jobs?limit=1`, { headers: authHeader() });
  const jobId = res.ok() ? (await res.json()).jobs?.[0]?.id : undefined;

  const views = [
    ["home", "/"],
    ["city", "/berlin"],
    ["city-family", "/berlin/ai-engineer"],
    ["compare", "/compare/berlin+san-francisco"],
    ...(jobId ? [["job", `/jobs/${jobId}`]] : []),
  ];

  const dir = `${OUT}/${info.project.name}`;
  mkdirSync(dir, { recursive: true });
  const changed = [];
  for (const [name, path] of views) {
    const png = {};
    for (const side of ["before", "after"]) {
      await serve(page, SIDES[side]);
      png[side] = await shot(page, path);
    }
    if (Buffer.compare(png.before, png.after) !== 0) {
      writeFileSync(`${dir}/${name}-before.png`, png.before);
      writeFileSync(`${dir}/${name}-after.png`, png.after);
      changed.push(name);
    }
  }
  writeFileSync(`${dir}/changed.json`, JSON.stringify(changed));
});
