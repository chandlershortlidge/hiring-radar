import { useMemo, useState } from "react";
import { PLACES, axisMax, comparePick, pctInt } from "./format.js";

const PAGE = 15;

// Two bars per skill (one per side, each as % of that place's job set) plus a diverging
// gap bar. Which two places are on the sides is the reader's choice (`pair`, picked from
// PLACES — HIR-138); the layout stays two-sided whatever is collected. Needs both sides to
// have jobs; otherwise says so instead of drawing one side empty. `selected` is the set of
// selected skill ids; a name click reports whether it was additive (shift or meta), exactly
// as SkillChart does.
export default function CompareChart({ data, selected, onSelect, onSelectCity, pair, onPair }) {
  const [shown, setShown] = useState(PAGE);
  const [sort, setSort] = useState("combined");
  const [A, B] = pair;
  const SORTS = { combined: "Combined share", a: `${A} share`, b: `${B} share`, gap: "Largest gap" };
  const totals = data?.city_totals || {};
  const nA = totals[A] || 0, nB = totals[B] || 0;

  const rows = useMemo(() => {
    const r = (data?.skills || []).map((s) => {
      const a = s.by_city?.[A] || 0, b = s.by_city?.[B] || 0;
      const ap = pctInt(a, nA), bp = pctInt(b, nB);
      return { id: s.skill_id, name: s.display, a, b, ap, bp, gap: bp - ap, combined: ap + bp };
    });
    const key = { combined: (x) => x.combined, a: (x) => x.ap, b: (x) => x.bp, gap: (x) => Math.abs(x.gap) }[sort];
    return r.sort((x, y) => key(y) - key(x) || x.name.localeCompare(y.name));
  }, [data, sort, nA, nB]);

  const pickers = (
    <>
      <div className="ctl"><label htmlFor="cityA">Left side</label>
        <select id="cityA" className="sel" value={A} onChange={(e) => onPair(comparePick(pair, 0, e.target.value))}>
          {PLACES.map((p) => <option key={p} value={p}>{p}</option>)}
        </select>
      </div>
      <div className="ctl"><label htmlFor="cityB">Right side</label>
        <select id="cityB" className="sel" value={B} onChange={(e) => onPair(comparePick(pair, 1, e.target.value))}>
          {PLACES.map((p) => <option key={p} value={p}>{p}</option>)}
        </select>
      </div>
    </>
  );

  // Both sides stay pickable when one has no jobs — otherwise the only way out of an empty
  // comparison would be to leave compare mode and come back.
  if (!nA || !nB) {
    return (
      <div className="bars">
        <div className="controls" style={{ marginBottom: 4 }}>{pickers}</div>
        <div className="empty">Compare needs jobs on both sides. {A}: {nA} · {B}: {nB}. Pick another place for the empty side.</div>
      </div>
    );
  }
  const max = axisMax(Math.max(...rows.map((r) => Math.max(r.ap, r.bp)), 0));
  const gapMax = Math.max(5, ...rows.map((r) => Math.abs(r.gap)));
  const w = (p) => `${Math.min(100, (p / max) * 100)}%`;

  return (
    <div className="bars" style={{ "--tick": "50%" }}>
      <div className="controls" style={{ marginBottom: 4 }}>
        {pickers}
        <div className="ctl"><label htmlFor="csort">Sort skills</label>
          <select id="csort" className="sel" value={sort} onChange={(e) => setSort(e.target.value)}>
            {Object.entries(SORTS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </div>
      </div>
      <div className="cmp-head">
        <span>Skill</span>
        <div className="cty"><span><b>{A}</b> · {nA} jobs</span><div className="axis"><span style={{ left: 0 }}>0%</span><span style={{ left: "50%" }}>{max / 2}%</span><span style={{ left: "100%" }}>{max}%</span></div></div>
        <div className="cty"><span><b>{B}</b> · {nB} jobs</span><div className="axis"><span style={{ left: 0 }}>0%</span><span style={{ left: "50%" }}>{max / 2}%</span><span style={{ left: "100%" }}>{max}%</span></div></div>
        <div className="cty"><span><b>Gap</b> <span className="dim">pts</span></span><div className="axis"><span style={{ left: 0 }}>◂ {A}</span><span style={{ left: "100%" }}>{B} ▸</span></div></div>
      </div>
      {rows.slice(0, shown).map((r, i) => (
        <div key={r.id} className={`cmp-row${selected.includes(r.id) ? " sel" : ""}`}>
          <button type="button" className="name" onClick={(e) => onSelect(r.id, e.shiftKey || e.metaKey)} aria-label={`${r.name}: ${A} ${r.ap}%, ${B} ${r.bp}%. Filter job list`}>
            <span className="rank">{i + 1}</span>{r.name}
          </button>
          <button type="button" className="cb track" onClick={() => onSelectCity(r.id, A)} aria-label={`${r.name} in ${A}, ${r.ap}%`}>
            <span className="fill" style={{ width: w(r.ap) }} /><b>{r.ap}%</b><span>{r.a}</span>
          </button>
          <button type="button" className="cb side-b track" onClick={() => onSelectCity(r.id, B)} aria-label={`${r.name} in ${B}, ${r.bp}%`}>
            <span className="fill" style={{ width: w(r.bp) }} /><b>{r.bp}%</b><span>{r.b}</span>
          </button>
          <div className="gap">
            <div>{r.gap < 0 && <i style={{ width: `${(Math.abs(r.gap) / gapMax) * 100}%` }} />}</div>
            <div>{r.gap > 0 && <i style={{ width: `${(r.gap / gapMax) * 100}%` }} />}</div>
            <em>{r.gap > 0 ? "+" : r.gap < 0 ? "−" : "±"}{Math.abs(r.gap)}</em>
          </div>
        </div>
      ))}
      <div className="bars-foot">
        <div>
          {shown < rows.length && <button type="button" className="btn" onClick={() => setShown(shown + PAGE)}>Show {Math.min(PAGE, rows.length - shown)} more</button>}
          <span>{Math.min(shown, rows.length)} of {rows.length} skills</span>
        </div>
        <div><span>Click a skill to filter jobs · ⇧- or ⌘-click to add a skill · click one city's bar for skill + city</span></div>
      </div>
    </div>
  );
}
