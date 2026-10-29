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

// CITIES is the compare pair; PLACES is every filterable place, EU-remote included (DECISIONS 2026-10-26).
export const CITIES = ["Berlin", "San Francisco"];
export const PLACES = ["Berlin", "Remote (EU)", "San Francisco"];
export const SENIORITIES = ["junior", "mid", "senior"];
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
