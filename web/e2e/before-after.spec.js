// PR before/after screenshots (HIR-231), including the three drawers, open (HIR-230).
//
// Does: for each view, render main's build ("before") and the branch's build ("after")
// in the same browser, seconds apart, against the same live data; save both screenshots
// only when they differ, and write changed.json listing those views. A drawer view opens
// a city, clicks the drawer's button and captures the drawer with the page behind it.
// Fails when a drawer does not open on the branch's build: no drawer, a blank page, or the
// "couldn't load" box a part of the page shows when it crashed (Panel.jsx). Those views
// are saved whether or not they differ, and the failure message names the drawer and what
// went wrong. The workflow posts no comment on a failed run: the red check and its log are
// the report. HIR-227 (Add a job blanked the page) reached the live site because nothing
// before a merge ever opened that drawer.
// Does NOT: write anything to the live site — only GET /api requests are passed through,
// everything else is refused, and no drawer is ever submitted. Does not judge the plain
// page views or main's build: those are evidence for review. The one assertion is that the
// drawers open on the branch.
//
// How the two builds are served without a server: every request to http://radar.test is
// intercepted. /api GETs are fetched from SHOT_LIVE with the site login; any other path is
// answered from the build folder (a file if it exists, else index.html, as the real app's
// catch-all route does).
import { expect, test } from "@playwright/test";
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

// Returns the screenshot and, for a drawer view, why the drawer did not open (else null).
async function shot(page, path, button) {
  await page.goto(path);
  await page.waitForLoadState("networkidle", { timeout: 20_000 }).catch(() => {});
  // Text laid out before the web font arrives sits a pixel or two off; wait for the fonts.
  await page.evaluate(() => document.fonts.ready).catch(() => {});
  await page.waitForTimeout(800);
  if (!button) return { png: await page.screenshot({ fullPage: true, animations: "disabled" }), problem: null };

  let problem = null;
  try {
    await page.getByRole("button", { name: button }).click({ timeout: 10_000 });
    await page.getByRole("dialog").waitFor({ state: "visible", timeout: 10_000 });
    // What the drawer fetches for itself (proposed skills, skill counts) has arrived.
    await page.waitForLoadState("networkidle", { timeout: 20_000 }).catch(() => {});
    await page.waitForTimeout(800);
  } catch {
    problem = "the drawer did not open";
  }
  const crashed = await page.locator('[role="alert"]', { hasText: "couldn't load" }).allTextContents();
  if (crashed.length) problem = crashed[0].split(".")[0].trim();
  if (!(await page.locator("#root").innerText().catch(() => "")).trim()) problem = "blank page: nothing rendered";
  // The drawer is pinned to the window, so the window is the picture: drawer and page behind it.
  return { png: await page.screenshot({ animations: "disabled" }), problem };
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
    // The drawers, opened from a city by their button's name: the name is on the button at
    // both widths, also where a phone hides its words (HIR-263).
    ["add-job", "/berlin", "Add a job"],
    ["profile", "/berlin", "Your profile"],
    ["proposed-skills", "/berlin", /proposed skills to review/],
  ];

  const dir = `${OUT}/${info.project.name}`;
  mkdirSync(dir, { recursive: true });
  const changed = [];
  const broken = [];
  for (const [name, path, button] of views) {
    const png = {};
    let problem = null;
    for (const side of ["before", "after"]) {
      await serve(page, SIDES[side]);
      const got = await shot(page, path, button);
      png[side] = got.png;
      // Only the branch's build is judged: a PR that repairs a drawer broken on main must pass.
      if (side === "after") problem = got.problem;
    }
    if (problem) broken.push({ view: name, problem });
    if (problem || Buffer.compare(png.before, png.after) !== 0) {
      writeFileSync(`${dir}/${name}-before.png`, png.before);
      writeFileSync(`${dir}/${name}-after.png`, png.after);
      changed.push(name);
    }
  }
  writeFileSync(`${dir}/changed.json`, JSON.stringify(changed));
  expect(broken, broken.map((b) => `${b.view}: ${b.problem}`).join("\n")).toEqual([]);
});
