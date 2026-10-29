import { useMemo, useState } from "react";
import { axisMax, pct, pctInt } from "./format.js";

const PAGE = 15;

// One bar per skill: share of the filtered job set listing it. With a profile, the bar
// is drawn solid for skills the person has and hatched for the ones they don't.
//
// `selected` is the set of selected skill ids (AND, several at a time). A click reports
// whether it was additive — shift or meta held — and App decides replace vs add; this
// component only draws the selection it is given.
export default function SkillChart({ data, selected, onSelect, profile, cityLabel }) {
  const [shown, setShown] = useState(PAGE);
  const [hover, setHover] = useState(null);
  const total = data?.total || 0;
  const skills = data?.skills || [];
  const max = useMemo(() => axisMax(skills.length ? pct(skills[0].count, total) : 0), [skills, total]);
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((t) => Math.round(max * t));
  const have = new Set(profile?.skills || []);

  if (!total) return <div className="empty">No jobs match these filters yet.</div>;

  return (
    <div className="bars" style={{ "--tick": "25%" }}>
      <div className="bars-head">
        <span>Skill</span>
        <div className="axis">
          {ticks.map((t, i) => <span key={i} style={{ left: `${i * 25}%` }}>{t}%{i === 4 ? " of jobs" : ""}</span>)}
        </div>
      </div>
      {skills.slice(0, shown).map((s, i) => {
        const p = pct(s.count, total);
        const w = `${Math.min(100, (p / max) * 100)}%`;
        const sel = selected.includes(s.skill_id);
        const dim = selected.length > 0 && !sel;
        const cities = Object.entries(s.by_city || {});
        const cls = profile ? (have.has(s.skill_id) ? "have" : "gap") : "";
        return (
          <button key={s.skill_id} type="button" className={`bar-row${dim ? " dimmed" : ""}`} aria-pressed={sel}
            aria-label={`${s.display}, ${s.count} jobs, ${pctInt(s.count, total)}%. ${sel ? "Remove from" : "Filter"} job list`}
            onClick={(e) => onSelect(s.skill_id, e.shiftKey || e.metaKey)}
            onMouseEnter={() => setHover(s.skill_id)} onMouseLeave={() => setHover(null)}
            onFocus={() => setHover(s.skill_id)} onBlur={() => setHover(null)}>
            <span className="name"><span className="rank">{i + 1}</span><span>{s.display}</span></span>
            <span className="track">
              <span className={`fill ${dim && !profile ? "dimmed" : cls}`} style={{ width: w }} />
              <span className="n">{s.count} <span className="pct">{pctInt(s.count, total)}%</span></span>
              {hover === s.skill_id && (
                <span className="tip" style={{ "--x": `calc(${w} + 72px)` }}>
                  <b>{s.display}{profile && (have.has(s.skill_id) ? " · you have this" : " · not in your profile")}</b>
                  <span>{s.count} jobs · {p}% of {total} {cityLabel}</span>
                  {cities.length > 1 && <span className="c">{cities.map(([c, n]) => `${c} ${n}`).join(" · ")}</span>}
                </span>
              )}
            </span>
          </button>
        );
      })}
      <div className="bars-foot">
        <div>
          {shown < skills.length && <button type="button" className="btn" onClick={() => setShown(shown + PAGE)}>Show {Math.min(PAGE, skills.length - shown)} more</button>}
          <span>{Math.min(shown, skills.length)} of {skills.length} skills with at least one mention</span>
        </div>
        <div>
          {profile && (
            <>
              <span className="legend"><i style={{ background: "var(--ink)" }} /> in your profile</span>
              <span className="legend"><i className="fill gap" style={{ height: 10 }} /> not yet</span>
            </>
          )}
          {/* How to select stays visible with a profile set too: the legend used to take the
              whole footer, which hid the one place that says a second skill can be added. */}
          <span>Click a bar to filter the jobs below · ⇧- or ⌘-click to add a skill{profile ? "" : " · hover for % and cities"}</span>
        </div>
      </div>
    </div>
  );
}
