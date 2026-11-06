export const SOURCE_CODES = {
  arbeitnow: ["AB", "arbeitnow"],
  startup_jobs: ["SJ", "startup.jobs"],
  greenhouse: ["GH", "Greenhouse"],
  lever: ["LV", "Lever"],
  ashby: ["AS", "Ashby"],
  join: ["JN", "JOIN"],
  arbeitsagentur: ["BA", "Bundesagentur für Arbeit"],
  jsearch: ["JS", "JSearch (Google for Jobs)"],
  url: ["URL", "Pasted link"],
  paste: ["TXT", "Pasted text"],
  screenshot: ["IMG", "Screenshot"],
};
export const sourceCode = (s) => (SOURCE_CODES[s] || [s.toUpperCase().slice(0, 3), s]);

// PLACES is every filterable place, EU-remote included (DECISIONS 2026-10-26). It is the
// option list for the city picker, the market grid and compare mode's tokens, so a newly
// launched city appears in all three by being added here and nowhere else (HIR-188).
// Each entry carries:
//   name    what the server stores in job.city and what a person reads
//   slug    the URL segment — /berlin/ai-engineer
//   group   which heading it sits under, one of PLACE_GROUPS
//   aliases extra words the picker's search box matches, beyond name and group
export const PLACES = [
  { name: "Berlin", slug: "berlin", group: "Germany", aliases: ["deutschland", "de"] },
  { name: "Remote (EU)", slug: "remote-eu", group: "Remote", aliases: ["remote", "eu", "europe", "anywhere"] },
  { name: "San Francisco", slug: "san-francisco", group: "United States", aliases: ["sf", "bay area", "usa", "us", "california"] },
  { name: "New York", slug: "new-york", group: "United States", aliases: ["nyc", "usa", "us", "manhattan", "brooklyn"] },
];
// The group headings, in the order the picker and the grid show them.
export const PLACE_GROUPS = ["Germany", "Remote", "United States"];
// Names only, for the callers that just need the list of places.
export const PLACE_NAMES = PLACES.map((p) => p.name);
// "All of Germany" is not a place the server stores: it is every German place at once,
// sent as a repeated city param. It sits at the end of the Germany group.
export const ALL_GERMANY = { name: "All of Germany", slug: "all-germany", group: "Germany", aliases: ["germany", "deutschland", "de"] };
export const placeBySlug = (slug) => (slug === ALL_GERMANY.slug ? ALL_GERMANY : PLACES.find((p) => p.slug === slug) || null);
export const placeByName = (name) => (name === ALL_GERMANY.name ? ALL_GERMANY : PLACES.find((p) => p.name === name) || null);
// The city names a chosen place asks the server for: one name, or every German one.
export const placeCities = (slug) => (slug === ALL_GERMANY.slug
  ? PLACES.filter((p) => p.group === "Germany").map((p) => p.name)
  : (placeBySlug(slug) ? [placeBySlug(slug).name] : []));
// Does this place match what someone typed into the picker's search box? Name, group and
// aliases all count, so "germany" finds Berlin and "sf" finds San Francisco.
// The market grid: every place in one list, busiest first, each card carrying its country
// as a label. It used to be one row per country, but with one or two cities in a group each
// row filled only half the page (HIR-191) — grouping can come back once a group has four or
// more cities to put in a row. Ties break by name, so the grid does not reshuffle between
// visits. Places with no jobs still appear — an empty market is information, and it is where
// a newly launched city starts.
export const gridPlaces = (counts) => [...PLACES]
  .sort((a, b) => (counts[b.name] || 0) - (counts[a.name] || 0) || a.name.localeCompare(b.name));

export function placeMatches(place, q) {
  const t = q.trim().toLowerCase();
  if (!t) return true;
  return [place.name, place.group, ...(place.aliases || [])].some((s) => s.toLowerCase().includes(t));
}

export const COMPARE_DEFAULT = ["Berlin", "San Francisco"];
export const SENIORITIES = ["junior", "mid", "senior"];

// The five job families every posting is sorted into from its title (HIR-186). The order is
// the order of the buttons; the server validates against the same five. FAMILY_LABELS is
// what a person reads — the stored value is the hyphenated id.
export const FAMILIES = ["ai-engineer", "ml-engineer", "data-scientist", "ml-platform", "research"];
export const FAMILY_LABELS = {
  "ai-engineer": "AI Engineer",
  "ml-engineer": "ML Engineer",
  "data-scientist": "Data Scientist",
  "ml-platform": "ML Platform",
  research: "Research",
};
export const familyLabel = (f) => FAMILY_LABELS[f] || f;

// Compare mode holds two or three places as removable tokens (HIR-188). The same place is
// never added twice — a place against itself is an empty column — and the third is the last:
// four columns do not fit the row, and reading three markets at once is already the limit.
// Removing is allowed down to one; the caller then leaves compare mode with what is left.
export const COMPARE_MAX = 3;
export const compareAdd = (cities, place) => (cities.includes(place) || cities.length >= COMPARE_MAX ? cities : [...cities, place]);
export const compareRemove = (cities, place) => cities.filter((c) => c !== place);
// "A", "A and B", "A, B and C" — for the sentences that name the selected skills.
export const listAnd = (xs) => (xs.length < 2 ? xs[0] || "" : `${xs.slice(0, -1).join(", ")} and ${xs[xs.length - 1]}`);

export const cap = (s) => (s ? s[0].toUpperCase() + s.slice(1) : s);

export function timeAgo(iso, now = Date.now()) {
  if (!iso) return "—";
  const t = Date.parse(iso);
  const s = Math.max(0, (now - t) / 1000);
  if (s < 90) return "just now";
  const m = s / 60; if (m < 60) return `${Math.round(m)} min ago`;
  const h = m / 60; if (h < 36) return `${Math.round(h)} h ago`;
  const d = h / 24; if (d < 45) return `${Math.round(d)} days ago`;
  return dateShort(iso);
}

export function dateShort(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

export function dateTime(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleString("en-GB", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
}

export const pct = (n, d) => (d ? Math.round((n / d) * 1000) / 10 : 0);
export const pctInt = (n, d) => (d ? Math.round((n / d) * 100) : 0);

// Axis max: next multiple of 20 at or above the largest share, at least 20, at most 100.
export const axisMax = (maxPct) => Math.min(100, Math.max(20, Math.ceil((maxPct || 0) / 20) * 20));

export const GERMAN_FILTERS = { any: "Any", not_required: "Not required", none: "Not mentioned", required: "Required" };
export const PRODUCTION_FILTERS = { any: "Any", not_required: "Not required", none: "Not asked for", required: "Required" };
export const DEGREE_FILTERS = { any: "Any", open: "Open without one", none: "Not mentioned", required: "Degree required" };
export const DEGREE_NAMES = { bachelor: "Bachelor's", master: "Master's", phd: "PhD" };
export const DEGREE_RANK = { "": 0, bachelor: 1, master: 2, phd: 3 };

// One line describing a job's degree ask, e.g. "Master's or equivalent experience".
export function degreeLine(j) {
  if (!j.degree) return null;
  const name = DEGREE_NAMES[j.degree] || j.degree;
  if (j.degree_requirement === "nice_to_have") return `${name} preferred`;
  return j.degree_or_equivalent ? `${name} or equivalent experience` : `${name} required`;
}
export function germanLine(j) {
  if (!j.german) return null;
  return j.german === "required" ? (j.german_basis === "inferred" ? "German (posting written in German)" : "German required") : "German a plus";
}
// One line describing a job's production-experience ask. Unlike German there is no
// inferred basis, so the value alone decides the wording.
export function productionLine(j) {
  if (!j.production) return null;
  return j.production === "required" ? "Production experience required" : "Production experience a plus";
}
