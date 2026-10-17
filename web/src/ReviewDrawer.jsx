import { useEffect, useState } from "react";
import Drawer from "./Drawer.jsx";
import { api } from "./api.js";
import { timeAgo } from "./format.js";

// Proposed skills: labels the extractor saw that aren't in the taxonomy. Reject, or accept
// as an alias of an existing taxonomy entry. A brand-new skill is a taxonomy edit
// (taxonomy/skills.json + a re-extract), which this drawer deliberately does not do.
export default function ReviewDrawer({ onClose, taxonomyList, skillsTracked, onChanged, onViewJob }) {
  const [groups, setGroups] = useState(null);
  const [pick, setPick] = useState({});
  const [busy, setBusy] = useState(null);
  const load = () => api.proposed().then((r) => setGroups(r.groups));
  useEffect(() => { load(); }, []);

  const act = async (g, status) => {
    setBusy(g.label);
    try { await api.resolve(g.ids, status, status === "accepted" ? pick[g.label] : null); await load(); onChanged?.(); }
    catch (e) { alert(e.message); }
    setBusy(null);
  };

  return (
    <Drawer title="Proposed skills" onClose={onClose}
      sub={groups ? `${groups.length} label${groups.length === 1 ? "" : "s"} the model found that aren't in the taxonomy (${skillsTracked} entries)` : "Loading…"}
      foot="Accepting as an alias adds a required mention of that skill to every job that quoted it. New skills are added in taxonomy/skills.json.">
      {groups && !groups.length && <div className="empty">Queue is empty.</div>}
      <ul className="rq">
        {(groups || []).map((g) => (
          <li key={g.label}>
            <div className="t"><b>{g.label}</b><span>in {g.jobs.length} job{g.jobs.length === 1 ? "" : "s"} · {timeAgo(g.jobs[0]?.first_seen)}</span></div>
            {g.jobs.slice(0, 2).map((j, i) => (
              <div key={i}>
                <blockquote>“{j.raw_text}”</blockquote>
                <a href="#" className="jl" onClick={(e) => { e.preventDefault(); onViewJob(j.job_id); }}>{j.company} · {j.title}{j.city ? ` · ${j.city}` : ""}</a>
              </div>
            ))}
            {g.jobs.length > 2 && <span className="dim" style={{ fontSize: 12 }}>+{g.jobs.length - 2} more</span>}
            <div className="act">
              <select className="sel" value={pick[g.label] || ""} onChange={(e) => setPick({ ...pick, [g.label]: e.target.value })} aria-label={`Taxonomy skill for ${g.label}`}>
                <option value="">Alias of…</option>
                {taxonomyList.map((s) => <option key={s.id} value={s.id}>{s.display}</option>)}
              </select>
              <button type="button" className="btn outline" disabled={!pick[g.label] || busy === g.label} onClick={() => act(g, "accepted")}>Accept</button>
              <button type="button" className="btn" disabled={busy === g.label} onClick={() => act(g, "rejected")}>Reject</button>
            </div>
          </li>
        ))}
      </ul>
    </Drawer>
  );
}
