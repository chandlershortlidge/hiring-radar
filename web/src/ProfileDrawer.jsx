import { useEffect, useMemo, useRef, useState } from "react";
import Drawer from "./Drawer.jsx";
import { api } from "./api.js";
import { matchCvSkills } from "./cvSkills.js";
import { CvReadError, readCvFile } from "./cvText.js";
import { DEGREE_NAMES, SENIORITIES, cap } from "./format.js";
import { EMPTY } from "./profile.js";

const ROLES = ["AI engineer", "ML engineer", "Data scientist", "LLM / applied scientist", "Other"];

// Role → seniority → skill chips ordered by how often the market asks for them. No score:
// the profile is a set of taxonomy ids, and matching is set overlap.
//
// A CV can pre-tick those chips (HIR-14). It is read in this browser and thrown away when
// the drawer closes — no endpoint, no model call, nothing stored (DECISIONS 2026-11-01), so
// the drawer's "nothing is uploaded" promise stays true.
export default function ProfileDrawer({ onClose, profile, save, taxonomyList }) {
  const [p, setP] = useState(profile || EMPTY);
  const [freq, setFreq] = useState([]);
  const [q, setQ] = useState("");
  const [cv, setCv] = useState(null);   // { reading } | { found, added } | { error }
  const fileRef = useRef(null);
  useEffect(() => { api.skills({ cities: [], seniorities: [], requirement: "all", window: "all" }).then((r) => setFreq(r.skills)); }, []);

  const have = new Set(p.skills);
  const ordered = useMemo(() => {
    const seen = new Set(freq.map((s) => s.skill_id));
    const rest = taxonomyList.filter((s) => !seen.has(s.id)).map((s) => ({ skill_id: s.id, display: s.display, count: 0 }));
    const all = [...freq, ...rest];
    const needle = q.trim().toLowerCase();
    const rows = needle ? all.filter((s) => s.display.toLowerCase().includes(needle) || s.skill_id.includes(needle)) : all;
    // Selected first, each group keeping its frequency order: a skill the CV ticked must be
    // visible without searching for it, even when the market rarely asks for it.
    const picked = new Set(p.skills);
    return [...rows.filter((s) => picked.has(s.skill_id)), ...rows.filter((s) => !picked.has(s.skill_id))];
  }, [freq, taxonomyList, q, p.skills]);

  async function onCvPick(e) {
    const file = e.target.files && e.target.files[0];
    if (fileRef.current) fileRef.current.value = "";   // so the same file can be re-picked
    if (!file) return;
    setCv({ reading: true });
    try {
      const text = await readCvFile(file);
      const { ids } = matchCvSkills(text, taxonomyList);
      const already = new Set(p.skills);
      const added = ids.filter((id) => !already.has(id));
      setP((x) => ({ ...x, skills: [...x.skills, ...added] }));
      setCv({ found: ids.length, added: added.length });
    } catch (err) {
      setCv({ error: err instanceof CvReadError ? err.message : "That file could not be read." });
    }
  }
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
        <div className="field"><label htmlFor="prod">Shipped software to production</label>
          <select id="prod" value={p.production ? "yes" : "no"} onChange={(e) => setP({ ...p, production: e.target.value === "yes" })}>
            <option value="no">No / not yet</option><option value="yes">Yes, real users depended on it</option></select></div>
      </div>
      <div className="field">
        <label htmlFor="sq">Skills you have</label>
        <span className="help">Ordered by how often postings ask for them. Pick what you could defend in an interview — 10 to 15 is plenty.</span>
        <input id="sq" type="search" placeholder="Search the taxonomy" value={q} onChange={(e) => setQ(e.target.value)} />
      </div>
      <div className="field">
        <div className="actions">
          <button type="button" className="btn" disabled={cv?.reading}
            onClick={() => fileRef.current && fileRef.current.click()}>
            {cv?.reading ? "Reading…" : "Fill from your CV"}
          </button>
          <input ref={fileRef} type="file" accept=".pdf,.docx,.txt,.md" onChange={onCvPick}
            style={{ display: "none" }} aria-hidden="true" tabIndex={-1} />
        </div>
        <span className="help">
          Ticks the skills your CV names, for you to correct. Read in this browser only — the
          file is not uploaded, not sent to a model, and not kept. PDF, .docx or plain text.
        </span>
        {cv?.error && <span className="help" role="alert">{cv.error}</span>}
        {cv?.found !== undefined && (
          <span className="help" role="status">
            {cv.found === 0
              ? "No skill in the taxonomy was named in that CV. Pick them by hand below."
              : `Found ${cv.found} skill${cv.found === 1 ? "" : "s"}${cv.added ? `, ${cv.added} newly ticked` : ", all already ticked"}. Check them below — a CV only matches skills it spells out.`}
          </span>
        )}
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
