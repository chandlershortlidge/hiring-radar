// Errors that visitors' browsers hit go to Sentry, with no visitor details (HIR-259,
// decisions/2026-11-25-hir-259-errors-go-to-sentry.md). The server side is
// app/error_reports.py.
//
// Off unless the build was given VITE_SENTRY_DSN. No tracing, no session replay, no
// session pings (those count visits), no cookies, no user info, no query strings, and no
// breadcrumbs from the console or from clicks and typing: a CV's text is read in this
// browser and must never leave it.
import * as Sentry from "@sentry/react";

const DROPPED_INTEGRATIONS = new Set(["BrowserSession", "CultureContext"]);
const DROPPED_BREADCRUMBS =new Set(["console", "ui.click", "ui.input", "ui.keypress"]);

const stripQuery = (url) => (typeof url === "string" ? url.split(/[?#]/)[0] : url);

// The last filter before an event leaves: no user block, no query string, no headers or
// cookies, whatever an integration added.
export function scrub(event) {
  delete event.user;
  if (event.request) {
    delete event.request.headers;
    delete event.request.cookies;
    delete event.request.query_string;
    delete event.request.data;
    event.request.url = stripQuery(event.request.url);
  }
  if (Array.isArray(event.breadcrumbs)) {
    event.breadcrumbs = event.breadcrumbs.filter((b) => !DROPPED_BREADCRUMBS.has(b.category));
  }
  return event;
}

export function keepBreadcrumb(crumb) {
  if (DROPPED_BREADCRUMBS.has(crumb.category)) return null;
  if (crumb.data) {
    if (crumb.data.url) crumb.data.url = stripQuery(crumb.data.url);
    if (crumb.data.from) crumb.data.from = stripQuery(crumb.data.from);
    if (crumb.data.to) crumb.data.to = stripQuery(crumb.data.to);
  }
  return crumb;
}

export function options(dsn) {
  return {
    dsn,
    sendDefaultPii: false,
    dataCollection: {
      userInfo: false,
      cookies: false,
      httpHeaders: false,
      httpBodies: [],
      urlQueryParams: false,
    },
    // Session pings are one per page load: a visitor count, which is out of scope. The
    // visitor's language and time zone are no help with a bug, so they stay home too.
    integrations: (defaults) => defaults.filter((i) => !DROPPED_INTEGRATIONS.has(i.name)),
    beforeSend: scrub,
    beforeBreadcrumb: keepBreadcrumb,
  };
}

let started = false;

export function startErrorReports(dsn = import.meta.env.VITE_SENTRY_DSN) {
  const key = (dsn || "").trim();
  if (!key) return false;
  Sentry.init(options(key));
  started = true;
  return true;
}

// For errors something on the page already caught (a panel's safety box), which would
// otherwise never reach the global handler.
export function reportError(error, extra) {
  if (!started) return;
  Sentry.captureException(error, extra ? { extra } : undefined);
}
