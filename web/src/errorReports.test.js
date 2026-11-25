// HIR-259: browser errors go to Sentry only when the build has a key, and leave with no
// visitor details. The send itself is Sentry's; what is checked here is what we hand it.
import { describe, it, expect, vi, beforeEach } from "vitest";

vi.mock("@sentry/react", () => ({ init: vi.fn(), captureException: vi.fn() }));
import * as Sentry from "@sentry/react";
import { keepBreadcrumb, options, reportError, scrub, startErrorReports } from "./errorReports.js";

beforeEach(() => vi.clearAllMocks());

describe("browser error reports", () => {
  it("start nothing without a key", () => {
    expect(startErrorReports("")).toBe(false);
    expect(startErrorReports("   ")).toBe(false);
    expect(startErrorReports(undefined)).toBe(false);
    reportError(new Error("x"));
    expect(Sentry.init).not.toHaveBeenCalled();
    expect(Sentry.captureException).not.toHaveBeenCalled();
  });

  it("switch off every visitor detail and load no tracing, replay or session pings", () => {
    const o = options("https://k@o1.ingest.de.sentry.io/1");
    expect(o.sendDefaultPii).toBe(false);
    expect(o.dataCollection).toEqual({ userInfo: false, cookies: false, httpHeaders: false, httpBodies: [], urlQueryParams: false });
    expect(o.tracesSampleRate).toBeUndefined();
    expect(o.replaysSessionSampleRate).toBeUndefined();
    const kept = o.integrations([{ name: "GlobalHandlers" }, { name: "BrowserSession" }, { name: "Breadcrumbs" }]);
    expect(kept.map((i) => i.name)).toEqual(["GlobalHandlers", "Breadcrumbs"]);
  });

  it("strip what an integration added before the event leaves", () => {
    const e = scrub({
      user: { ip_address: "{{auto}}" },
      request: { url: "https://hiringradar.app/berlin?q=me#x", headers: { "User-Agent": "u" }, cookies: "a=b", query_string: "q=me" },
      breadcrumbs: [{ category: "console", message: "cv text" }, { category: "ui.click" }, { category: "fetch", data: { url: "/api/skills" } }],
    });
    expect(e).toEqual({ request: { url: "https://hiringradar.app/berlin" }, breadcrumbs: [{ category: "fetch", data: { url: "/api/skills" } }] });
  });

  it("drop console, click and typing breadcrumbs, and query strings from the rest", () => {
    expect(keepBreadcrumb({ category: "console", message: "x" })).toBeNull();
    expect(keepBreadcrumb({ category: "ui.input" })).toBeNull();
    expect(keepBreadcrumb({ category: "fetch", data: { url: "/api/jobs?text=my+search" } })).toEqual({ category: "fetch", data: { url: "/api/jobs" } });
    expect(keepBreadcrumb({ category: "navigation", data: { from: "/a?x=1", to: "/b#y" } })).toEqual({ category: "navigation", data: { from: "/a", to: "/b" } });
  });

  it("report a caught error once started", () => {
    expect(startErrorReports("https://k@o1.ingest.de.sentry.io/1")).toBe(true);
    expect(Sentry.init).toHaveBeenCalledTimes(1);
    const err = new Error("panel broke");
    reportError(err, { panel: "The chart" });
    expect(Sentry.captureException).toHaveBeenCalledWith(err, { extra: { panel: "The chart" } });
  });
});
