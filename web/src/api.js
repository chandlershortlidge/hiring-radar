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
  city: f.compare ? [] : f.cities,
  seniority: f.seniorities,
  requirement: f.requirement,
  window: f.window,
  german: f.german,
  degree: f.degree,
});

export const api = {
  stats: () => call("/api/stats"),
  taxonomy: () => call("/api/taxonomy"),
  skills: (f) => call(`/api/skills${qs(filterParams(f))}`),
  relatedSkills: (f) => call(`/api/skills/related${qs({ ...filterParams(f), skill: f.skill })}`),
  jobs: (f, { sort, limit, offset }) =>
    call(`/api/jobs${qs({ ...filterParams(f), skill: f.skill, q: f.query, sort, limit, offset })}`),
  job: (id) => call(`/api/jobs/${id}`),
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
