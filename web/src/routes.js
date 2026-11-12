// The address bar is the app's state for "which market am I looking at" (HIR-188), so a
// city has a link to share and the back button works. There is no router: the server
// returns index.html for every path and these two pure functions are the whole mapping.
//
//   /                                  the home view — pick a market
//   /berlin                            Berlin, every family
//   /berlin/ai-engineer                Berlin, AI Engineer only
//   /all-germany/data-scientist        every German place at once
//   /compare/berlin+san-francisco      compare mode, two or three places
//   /jobs/42                           one job's own page (unchanged)
//
// Anything else reads as the home view rather than erroring: a stale or hand-typed link
// should land somewhere usable, not on a blank page.
import { ALL_GERMANY, COMPARE_MAX, FAMILIES, placeByName, placeBySlug } from "./format.js";

export const HOME = { view: "home", place: null, family: null, cities: [], jobId: null };

export function parsePath(path = window.location.pathname) {
  const parts = path.split("/").filter(Boolean).map((s) => decodeURIComponent(s));
  if (!parts.length) return HOME;

  if (parts[0] === "jobs" && parts.length === 2 && /^\d+$/.test(parts[1])) {
    return { ...HOME, view: "job", jobId: Number(parts[1]) };
  }

  if (parts[0] === "compare") {
    // The places are joined by "+" so one path segment holds the whole comparison.
    // "All of Germany" is not one of them: a group has no column of its own.
    const slugs = (parts[1] || "").split("+").filter(Boolean);
    const names = slugs.map(placeBySlug).filter((p) => p && p.slug !== ALL_GERMANY.slug).map((p) => p.name);
    const cities = [...new Set(names)].slice(0, COMPARE_MAX);
    // Fewer than two real places is not a comparison; fall back to the home view.
    return cities.length >= 2 ? { ...HOME, view: "compare", cities } : HOME;
  }

  const place = placeBySlug(parts[0]);
  if (!place || parts.length > 2) return HOME;
  // /berlin/not-a-family is Berlin, not the home view: the city is the part worth keeping.
  const family = parts[1] && FAMILIES.includes(parts[1]) ? parts[1] : null;
  return { ...HOME, view: "city", place: place.slug, family };
}

export function pathFor(route) {
  if (route.view === "job") return `/jobs/${route.jobId}`;
  if (route.view === "compare") {
    const slugs = (route.cities || []).map((n) => placeByName(n)?.slug).filter(Boolean);
    return slugs.length >= 2 ? `/compare/${slugs.join("+")}` : "/";
  }
  if (route.view === "city" && route.place) return route.family ? `/${route.place}/${route.family}` : `/${route.place}`;
  return "/";
}

// Where changing the job family leads from the market you are on (HIR-197). On the home
// view it stays the home view: the bar reads "[family] in [city]", so nothing opens until
// the city is picked too. A city view with no city is not a place either — it used to open
// a dashboard for every city at once — so it is treated as the home view.
export function withFamily(market, family) {
  if (market.view === "compare") return { ...market, family };
  if (market.view === "city" && market.place) return { ...HOME, view: "city", place: market.place, family };
  return { ...HOME, family };
}
