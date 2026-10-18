import { useEffect, useMemo, useState } from "react";
import Drawer from "./Drawer.jsx";
import { api } from "./api.js";
import { DEGREE_NAMES, SENIORITIES, cap } from "./format.js";
import { EMPTY } from "./profile.js";

const ROLES = ["AI engineer", "ML engineer", "Data scientist", "LLM / applied scientist", "Other"];

// Role → seniority → skill chips ordered by how often the market asks for them. No résumé,
// no score: the profile is a set of taxonomy ids, and matching is set overlap.
export default function ProfileDrawer({ onClose, profile, save, taxonomyList }) {
  const [p, setP] = useState(profile || EMPTY);
  const [freq, setFreq] = useState([]);
  const [q, setQ] = useState("");
  useEffect(() => { api.skills({ cities: [], seniorities: [], requirement: "all", window: "all" }).then((r) => setFreq(r.skills)); }, []);

  const ordered = useMemo(() => {
    const seen = new Set(freq.map((s) => s.skill_id));
    const rest = taxonomyList.filter((s) => !seen.has(s.id)).map((s) => ({ skill_id: s.id, display: s.display, count: 0 }));
    const all = [...freq, ...rest];
    const needle = q.trim().toLowerCase();
    return needle ? all.filter((s) => s.display.toLowerCase().includes(needle) || s.skill_id.includes(needle)) : all;
  }, [freq, taxonomyList, q]);
  const have = new Set(p.skills);
  const toggle = (id) => setP((x) => ({ ...x, skills: have.has(id) ? x.skills.filter((s) => s !== id) : [...x.skills, id] }));
  const shown = q ? ordered : ordered.slice(0, 40);

  return (
    <Drawer title="Your profile" onClose={onClose}
      sub="Stays in this browser. Used to show which required skills you cover; nothing is scored or uploaded."
      foot={<div className="actions"><button type="button" className="btn primary" onClick={() => { save(p); onClose(); }}>Save</button>
        {profile && <button type="button" className="btn" onClick={() => { save(null); onClose(); }}>Clear profile</button>}
        <span className="dim" style={{ marginLeft: "auto" }}>{p.skills.length} skills</span></div>}>
      <div className="grid2">
        <div className="field"><label htmlFor="role">Role family</label>
          <select id="role" value={p.role} onChange={(e) => setP({ ...p, role: e.target.value })}>{ROLES.map((r) => <option key={r}>{r}</option>)}</select></div>
        <div className="field"><label htmlFor="sen">Seniority you're targeting</label>
          <select id="sen" value={p.seniority} onChange={(e) => setP({ ...p, seniority: e.target.value })}>
            <option value="">Any</option>{SENIORITIES.map((s) => <option key={s} value={s}>{cap(s)}</option>)}</select></div>
        <div className="field"><label htmlFor="deg">Highest degree</label>
          <select id="deg" value={p.degree || ""} onChange={(e) => setP({ ...p, degree: e.target.value })}>
            <option value="">None / bootcamp</option>{Object.entries(DEGREE_NAMES).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></div>
        <div className="field"><label htmlFor="ger">Professional German</label>
          <select id="ger" value={p.german ? "yes" : "no"} onChange={(e) => setP({ ...p, german: e.target.value === "yes" })}>
            <option value="no">No / not yet</option><option value="yes">Yes (B2 or better)</option></select></div>
      </div>
      <div className="field">
        <label htmlFor="sq">Skills you have</label>
        <span className="help">Ordered by how often postings ask for them. Pick what you could defend in an interview — 10 to 15 is plenty.</span>
        <input id="sq" type="search" placeholder="Search the taxonomy" value={q} onChange={(e) => setQ(e.target.value)} />
      </div>
      <div className="pchips">
        {shown.map((s) => (
          <button key={s.skill_id} type="button" className="pchip" aria-pressed={have.has(s.skill_id)} onClick={() => toggle(s.skill_id)}>
            {s.display}{s.count > 0 && <small>{s.count}</small>}
          </button>
        ))}
        {!shown.length && <span className="dim">No skill matches “{q}”.</span>}
      </div>
      {!q && ordered.length > 40 && <span className="dim" style={{ fontSize: 12.5 }}>Showing the 40 most-asked-for. Search to find the rest.</span>}
    </Drawer>
  );
}
