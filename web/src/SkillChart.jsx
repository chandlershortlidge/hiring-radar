import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { axisMax, pct, pctInt } from "./format.js";
import FitLine from "./FitLine.jsx";
import { Search } from "./icons.jsx";
import { filterSkills } from "./skillMatch.js";

const PAGE = 15;

// What the chart box says while it has no numbers (HIR-318): that they are on their way,
// or that the request for them failed. "No jobs match these filters" is kept for an answer
// that really is zero jobs; it used to be shown for a missing answer too, next to a job
// list of hundreds. Both lines keep the `empty` class, so they look like the chart's other
// one-line messages.
export function ChartStatus({ failed, onRetry }) {
  if (failed) {
    return (
      <div className="empty" role="alert">
        The chart could not be loaded. <button type="button" className="btn" onClick={onRetry}>Try again</button>
      </div>
    );
  }
  return <div className="empty" role="status">Loading the chart…</div>;
}

// The hover box (HIR-479). It is drawn on the page itself, not inside the chart: beside the
// jobs the chart's column scrolls on its own, and anything drawn inside a scrolling box is
// cut off at its edge — the box ran past the card and gave it a sideways scrollbar. It
// hangs from the pointer (from the keyboard, from the bar's count), opens to the right,
// flips to the left when it would leave the window, and is kept inside the window.
const EDGE = 8;
const GAP = 12;
export function placeTip({ x, top }, { width, height }, { vw, vh }) {
  let left = x + GAP;
  if (left + width > vw - EDGE) left = x - GAP - width;
  left = Math.max(EDGE, Math.min(left, vw - EDGE - width));
  const y = Math.max(EDGE, Math.min(top - GAP, vh - EDGE - height));
  return { left, top: y };
}

function Tip({ anchor, children }) {
  const ref = useRef(null);
  const [pos, setPos] = useState(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    const root = document.documentElement;
    setPos(placeTip(anchor, { width: el.offsetWidth, height: el.offsetHeight },
      { vw: root.clientWidth || window.innerWidth, vh: root.clientHeight || window.innerHeight }));
  }, [anchor.x, anchor.top]);
  // hidden until measured, so it never flashes at the wrong place
  return createPortal(
    <div ref={ref} className="tip" role="tooltip"
      style={pos ? { left: pos.left, top: pos.top } : { left: 0, top: 0, visibility: "hidden" }}>
      {children}
    </div>,
    document.body,
  );
}

// One bar per skill: share of the filtered job set listing it. With a profile, the bar
// is plum for skills the person has and plum tint for the ones they don't (docs/style.md).
//
// `selected` is the set of selected skill ids (AND, several at a time). A click reports
// whether it was additive — shift or meta held — and App decides replace vs add; this
// component only draws the selection it is given.
//
// The find box (HIR-67A) narrows the rows by display name or any taxonomy alias (the match
// itself lives in skillMatch.js, shared with the chip row's add-skill popover), before
// the "show 15 / show more" cut, so a skill that would sit past the cut becomes visible by
// typing its name. It is pure display: it never changes the selection and never asks the
// server for anything. Ranks and the axis keep the values they have in the whole chart, so
// a filtered row still says where it sits overall and bar widths do not jump while typing.
//
// The hover box names the skill, its count and share of the filtered jobs (`jobsLabel` says
// which jobs, e.g. "open AI Engineer jobs"), and that a click filters. It used to list the
// other cities too; on one city's page that was noise (HIR-479). A comparison of cities
// has its own chart, where each city is a column.
//
// `gaps` (HIR-411) puts the line naming the visitor's biggest gaps between the find box and
// the bars. App turns it on for a single city's page; FitLine.jsx says when it draws.
export default function SkillChart({ data, selected, onSelect, profile, note, jobsLabel = "jobs", aliases = {}, gaps = false }) {
  const [shown, setShown] = useState(PAGE);
  // { id, x, top }: which bar, and the screen point the box hangs from
  const [hover, setHover] = useState(null);
  // The box is fixed to the window, so it would stay put while the bars scroll away under
  // it: any scroll (the page, or the chart's own column) or resize hides it.
  const hovering = !!hover;
  useEffect(() => {
    if (!hovering) return undefined;
    const hide = () => setHover(null);
    window.addEventListener("scroll", hide, true);
    window.addEventListener("resize", hide);
    return () => { window.removeEventListener("scroll", hide, true); window.removeEventListener("resize", hide); };
  }, [hovering]);
  const [find, setFind] = useState("");
  const total = data?.total || 0;
  const skills = data?.skills || [];
  const max = useMemo(() => axisMax(skills.length ? pct(skills[0].count, total) : 0), [skills, total]);
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((t) => Math.round(max * t));
  const have = new Set(profile?.skills || []);
  const rank = useMemo(() => Object.fromEntries(skills.map((s, i) => [s.skill_id, i + 1])), [skills]);
  const rows = useMemo(() => filterSkills(skills, aliases, find), [skills, aliases, find]);

  if (!total) return <div className="empty">No jobs match these filters yet.</div>;

  return (
    <div className="bars" style={{ "--tick": "25%" }}>
      <div className="chart-find">
        <label htmlFor="skill-find" className="sr">Find a skill in the chart</label>
        <div className="search"><Search />
          <input id="skill-find" type="search" className="inp" placeholder="Find a skill (name or alias)"
            value={find} onChange={(e) => setFind(e.target.value)} />
        </div>
        {find.trim() && <span className="muted">{rows.length} of {skills.length} skills match “{find.trim()}”</span>}
      </div>
      {gaps && <FitLine profile={profile} data={data} selected={selected} onSelect={onSelect} />}
      <div className="bars-head">
        <span>Skill</span>
        <div className="axis">
          {ticks.map((t, i) => <span key={i} style={{ left: `${i * 25}%` }}>{t}%{i === 4 ? " of jobs" : ""}</span>)}
        </div>
      </div>
      {rows.slice(0, shown).map((s) => {
        const p = pct(s.count, total);
        const w = `${Math.min(100, (p / max) * 100)}%`;
        const sel = selected.includes(s.skill_id);
        const dim = selected.length > 0 && !sel;
        const cls = profile ? (have.has(s.skill_id) ? "have" : "gap") : "";
        const rowTop = (e) => e.currentTarget.getBoundingClientRect().top;
        const atPointer = (e) => setHover({ id: s.skill_id, x: e.clientX, top: rowTop(e) });
        // from the keyboard there is no pointer: hang the box off the bar's count
        const atBar = (e) => {
          const n = e.currentTarget.querySelector(".n");
          const x = (n || e.currentTarget).getBoundingClientRect().right;
          setHover({ id: s.skill_id, x, top: rowTop(e) });
        };
        return (
          <button key={s.skill_id} type="button" className={`bar-row${dim ? " dimmed" : ""}`} aria-pressed={sel}
            aria-label={`${s.display}, ${s.count} jobs, ${pctInt(s.count, total)}%. ${sel ? "Remove from" : "Filter"} job list`}
            onClick={(e) => onSelect(s.skill_id, e.shiftKey || e.metaKey)}
            onMouseEnter={atPointer} onMouseMove={atPointer} onMouseLeave={() => setHover(null)}
            onFocus={atBar} onBlur={() => setHover(null)}>
            <span className="name"><span className="rank">{rank[s.skill_id]}</span><span className="label">{s.display}</span></span>
            <span className="track">
              <span className={`fill ${dim && !profile ? "dimmed" : cls}`} style={{ width: w }} />
              <span className="n">{s.count} <span className="pct">{pctInt(s.count, total)}%</span></span>
            </span>
            {hover?.id === s.skill_id && (
              <Tip anchor={hover}>
                <b>{s.display}{profile && (have.has(s.skill_id) ? " · you have this" : " · not in your profile")}</b>
                <span>{s.count} jobs · {pctInt(s.count, total)}% of {total} {jobsLabel}</span>
                <span className="c">{sel ? "Click to remove this filter" : "Click to filter the jobs"}</span>
              </Tip>
            )}
          </button>
        );
      })}
      {!rows.length && <div className="empty">No skill in the chart matches “{find.trim()}”.</div>}
      <div className="bars-foot">
        <div>
          {shown < rows.length && <button type="button" className="btn" onClick={() => setShown(shown + PAGE)}>Show {Math.min(PAGE, rows.length - shown)} more</button>}
          <span>{Math.min(shown, rows.length)} of {rows.length} skills{find.trim() ? " matching" : " with at least one mention"}</span>
        </div>
        <div>
          {profile && (
            <>
              <span className="legend"><i className="fill have" /> in your profile</span>
              <span className="legend"><i className="fill gap" /> not yet</span>
            </>
          )}
          {/* What the percentages are (HIR-477): it was the line above the chart. It replaces
              the click/hover hint; each bar's hover box still says "Click to filter the jobs". */}
          {note && <span className="chart-note">{note}</span>}
        </div>
      </div>
    </div>
  );
}
