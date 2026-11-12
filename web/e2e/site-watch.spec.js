// The robot visitor (HIR-258): walks the paths a person uses on the LIVE site and fails on
// a blank page, a browser error, a failed request, a part of the page that couldn't load, or
// a missing element.
//
// Does: read the site exactly as a visitor would, at desktop and phone width (the two
// projects in playwright.watch.config.js). Each test is one visitor path, so a failure names
// the path that broke; the ticket filed by scripts/site_watch_ticket.py is titled after it.
// Does NOT: write anything. Every request to /api that is not a GET is refused before it
// leaves the browser and fails the test — so the add-a-job drawer is opened, never
// submitted, and no click here can start a model call. The profile it sets up lives in this
// test browser's own storage, which is thrown away after each test.
//
// Real data, so "a filter changes the results" is checked as "the filter reaches the server
// in the request and the page redraws without error": a filter can rightly leave a count
// unchanged (no junior roles in a city this week), and that is not a break.
//
// Env: WATCH_URL (the site's origin), WATCH_AUTH ("user:password", optional) — read by the
// config. Without WATCH_URL every test is skipped.
import { test as base, expect } from "@playwright/test";

const URL_SET = !!process.env.WATCH_URL;

// Collects every sign of a break while a test runs and fails the test on any of them.
const test = base.extend({
  problems: async ({ page, baseURL }, use) => {
    const origin = new URL(baseURL).origin;
    const problems = [];
    const ours = (u) => { try { return new URL(u).origin === origin; } catch { return false; } };

    await page.route("**/api/**", (route) => {
      const req = route.request();
      if (req.method() === "GET") return route.continue();
      problems.push(`refused a ${req.method()} to ${new URL(req.url()).pathname}: the robot visitor never writes`);
      return route.abort();
    });
    page.on("pageerror", (e) => problems.push(`page error: ${e.message}`));
    page.on("console", (m) => { if (m.type() === "error") problems.push(`console error: ${m.text()}`); });
    page.on("requestfailed", (r) => {
      // Our own refusal above is already counted; a request cut off by navigating away isn't a break.
      const why = r.failure()?.errorText || "";
      if (ours(r.url()) && !/ERR_ABORTED|cancelled/i.test(why)) problems.push(`request failed: ${new URL(r.url()).pathname} (${why})`);
    });
    page.on("response", (r) => {
      if (ours(r.url()) && r.status() >= 400) problems.push(`HTTP ${r.status()} from ${new URL(r.url()).pathname}`);
    });

    await use(problems);

    // A part of the page that caught its own crash shows a "couldn't load" box (the Panel
    // safety net); the page looks alive but that part is gone.
    const broken = await page.locator('[role="alert"]', { hasText: "couldn't load" }).allTextContents();
    for (const b of broken) problems.push(`part of the page failed: ${b.split(".")[0]}`);
    // A blank page: the app mounted nothing.
    const text = (await page.locator("#root").innerText().catch(() => "")).trim();
    if (!text) problems.push("blank page: nothing rendered");
    expect(problems, problems.join("\n")).toEqual([]);
  },
});

test.skip(!URL_SET, "WATCH_URL not set");
test.describe.configure({ mode: "serial" });

// The busiest market, by clicking its card on the home page: that is the first one.
async function openBusiestCity(page) {
  await page.goto("/");
  const card = page.locator("a.card.market").first();
  await expect(card).toBeVisible();
  await card.click();
  await expect(page).not.toHaveURL(/\/$/);
  await expectChartAndJobs(page);
}

async function expectChartAndJobs(page) {
  await expect(page.locator("#chart-title")).toBeVisible();
  await expect(page.locator(".chart .bars")).toBeVisible();
  await expect(page.locator(".chart .bars-head")).toBeVisible(); // drawn only when there are jobs
  await expect(page.locator(".jobs .row").first()).toBeVisible();
}

test("home loads; pick a city and a job type; chart and job list have data", async ({ page, problems }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "What are employers actually asking for?" })).toBeVisible();
  const cards = page.locator("a.card.market");
  await expect(cards.first()).toBeVisible();
  await expect(cards.first().locator("li").first()).toBeVisible(); // its top skills drew

  await page.getByRole("button", { name: /Pick a city/ }).click();
  await page.getByRole("listbox", { name: "Cities" }).getByRole("option").first().click();
  await expect(page).not.toHaveURL(/\/$/);
  await expectChartAndJobs(page);

  const family = page.locator("#qb-family");
  const first = await family.locator("option").nth(1).getAttribute("value");
  const wait = page.waitForResponse((r) => r.url().includes("/api/skills") && r.url().includes(`family=${first}`));
  await family.selectOption(first);
  expect((await wait).status()).toBe(200);
  await expect(page).toHaveURL(new RegExp(`/${first}$`));
  await expect(page.locator(".chart .bars")).toBeVisible();
});

test("each filter reaches the server and the page redraws", async ({ page, problems }) => {
  await openBusiestCity(page);
  const filters = [
    ["Requirement", () => page.getByRole("button", { name: "Required + nice-to-have" }).click(), "requirement=all"],
    ["Seniority", () => page.getByRole("group", { name: "Seniority" }).getByRole("button").nth(1).click(), "seniority="],
    ["German", () => page.locator("#de").selectOption({ index: 1 }), "german="],
    ["Production experience", () => page.locator("#prod").selectOption({ index: 1 }), "production="],
    ["Degree", () => page.locator("#deg").selectOption({ index: 1 }), "degree="],
    ["Time window", () => page.locator("#win").selectOption("all"), "window=all"],
  ];
  for (const [name, act, param] of filters) {
    await test.step(name, async () => {
      const wait = page.waitForResponse((r) => r.url().includes("/api/skills?") && r.url().includes(param));
      await act();
      expect((await wait).status(), `${name}: /api/skills`).toBe(200);
      // Either bars or the chart's own "no jobs match" line: both are a drawn chart.
      await expect(page.locator(".chart .bars, .chart .empty").first()).toBeVisible();
    });
  }
});

test("compare mode with a second city", async ({ page, problems }) => {
  await openBusiestCity(page);
  await page.getByRole("button", { name: /Compare with/ }).click();
  await page.getByRole("listbox", { name: "Cities" }).getByRole("option").first().click();
  await expect(page).toHaveURL(/\/compare\/[^/]+\+[^/]+/);
  await expect(page.locator(".qbar .token")).toHaveCount(2);
  await expect(page.locator(".chart .bars").first()).toBeVisible();
  await expect(page.locator(".jobs .row").first()).toBeVisible();
});

test("a job card, its permanent page, and the original posting link", async ({ page, problems }) => {
  await openBusiestCity(page);
  const row = page.locator(".jobs .row").first();
  await row.click();
  const permanent = page.getByRole("link", { name: /Permanent page/ }).first();
  await expect(permanent).toBeVisible();
  const href = await permanent.getAttribute("href");
  expect(href).toMatch(/^\/jobs\/\d+$/);

  await page.goto(href);
  await expect(page.locator("#job-title")).toBeVisible();
  await expect(page.locator("pre.posting")).not.toBeEmpty();
  // A posting the site has a link for must link somewhere real. Whether the employer has
  // since taken it down is their side, not a break of ours, so the link is checked for
  // shape, not fetched.
  const original = page.getByRole("link", { name: /Open original posting/ });
  if (await original.count()) {
    expect(await original.getAttribute("href")).toMatch(/^https?:\/\/[^/\s]+\.[^/\s]+/);
  }
});

test("the add-a-job drawer opens (never submitted)", async ({ page, problems }) => {
  await openBusiestCity(page);
  // By place, not by name: at phone width the button's words are hidden and it has no
  // other name, so "Add a job" finds nothing there.
  await page.locator(".hdr-actions button.btn.outline").click();
  const drawer = page.getByRole("dialog");
  await expect(drawer).toBeVisible();
  await expect(drawer.locator("#url")).toBeVisible();
  await drawer.getByRole("button", { name: "Close" }).click();
  await expect(drawer).toBeHidden();
});

test("the profile drawer opens, a skill can be added, fit numbers show", async ({ page, problems }) => {
  await openBusiestCity(page);
  await page.getByRole("button", { name: "Your profile" }).click();
  const drawer = page.getByRole("dialog");
  await expect(drawer).toBeVisible();
  // The most-asked-for skill is first; with it, most jobs in the busiest city get a score.
  const skill = drawer.locator(".pchips .pchip").first();
  await skill.click();
  await expect(skill).toHaveAttribute("aria-pressed", "true");
  await drawer.getByRole("button", { name: "Save" }).click();
  await expect(drawer).toBeHidden();
  await expect(page.getByRole("button", { name: "Your profile" })).toContainText("1 skills in your profile");
  await expect(page.locator(".jobs .row .fit").first()).toBeVisible();
});
