// Thin fetch layer over the FastAPI routes. Every function returns parsed JSON or throws
// an Error whose message is the server's `detail` when there is one.

async function call(path, init) {
  const r = await fetch(path, init);
  const body = await r.json().catch(() => null);
  if (!r.ok) throw new Error((body && body.detail) || `${r.status} ${r.statusText}`);
  return body;
}

function qs(params) {
  const u = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v == null || v === "") continue;
    if (Array.isArray(v)) v.forEach((x) => u.append(k, x));
    else u.set(k, v);
  }
  const s = u.toString();
  return s ? `?${s}` : "";
}

export const filterParams = (f) => ({
  // `cities` is sent as given: the chart's filters hold [] in compare mode (every city in
  // one request), while the job list and related panel pass the compared cities (HIR-196).
  city: f.cities,
  seniority: f.seniorities,
  family: f.families,
  requirement: f.requirement,
  window: f.window,
  german: f.german,
  production: f.production,
  degree: f.degree,
});

export const api = {
  stats: () => call("/api/stats"),
  taxonomy: () => call("/api/taxonomy"),
  skills: (f) => call(`/api/skills${qs(filterParams(f))}`),
  // The tree reports both the required and the mentioned share of every skill and always
  // maps the whole market, so `requirement` and the skill selection are left off the
  // request rather than sent and ignored (app/skill_tree.py says the same).
  skillTree: (f) => call(`/api/skills/tree${qs({ ...filterParams(f), requirement: null })}`),
  relatedSkills: (f) => call(`/api/skills/related${qs({ ...filterParams(f), skill: f.skillIds })}`),
  // What's rising reads place and family only, so nothing else is sent (HIR-232).
  risingSkills: (f) => call(`/api/skills/rising${qs({ city: f.cities, family: f.families })}`),
  jobs: (f, { sort, limit, offset }) =>
    call(`/api/jobs${qs({ ...filterParams(f), skill: f.skillIds, q: f.query, text: f.text, sort, limit, offset })}`),
  job: (id) => call(`/api/jobs/${id}`),
  // "Doesn't belong here" (HIR-226). `view` is the whole screen state (flagView.js), stored
  // as sent; un-flagging closes the flag on the server, it does not delete it.
  flag: (id, view) => call(`/api/jobs/${id}/flag`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ view }) }),
  unflag: (id) => call(`/api/jobs/${id}/flag`, { method: "DELETE" }),
  flagNote: (flagId, note) => call(`/api/flags/${flagId}/note`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ note }) }),
  proposed: () => call("/api/proposed"),
  resolve: (ids, status, resolved_skill_id) =>
    call("/api/proposed/resolve", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ ids, status, resolved_skill_id }),
    }),
  addUrl: (body) => call("/api/add/url", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) }),
  addText: (body) => call("/api/add/text", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) }),
  addScreenshot: (file, fields) => {
    const fd = new FormData();
    fd.append("file", file);
    return call(`/api/add/screenshot${qs(fields)}`, { method: "POST", body: fd });
  },
};

// The chart's numbers for these filters, or the fact that they could not be fetched
// (HIR-318). Never rejects: the page has to tell "still waiting" from "failed" from "zero
// jobs", and an unhandled failure used to look like the first of those for good.
// The answer is tagged with the family it was asked for, so the market cards never show a
// new family's order over the previous family's numbers while a request is in flight.
export const fetchSkills = (filters, get = api.skills) => get(filters).then(
  (r) => ({ data: { ...r, family: filters.families[0] || null }, failed: false }),
  () => ({ data: null, failed: true }),
);
