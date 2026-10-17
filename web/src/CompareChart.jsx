import { useMemo, useState } from "react";
import { CITIES, axisMax, pctInt } from "./format.js";

const PAGE = 15;
const SORTS = { combined: "Combined share", a: `${CITIES[0]} share`, b: `${CITIES[1]} share`, gap: "Largest gap" };

// Two bars per skill (one per city, each as % of that city's job set) plus a diverging
// gap bar. Needs both cities to have jobs; otherwise says so instead of drawing one side empty.
export default function CompareChart({ data, selected, onSelect, onSelectCity }) {
  const [shown, setShown] = useState(PAGE);
  const [sort, setSort] = useState("combined");
  const [A, B] = CITIES;
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

  if (!nA || !nB) {
    return <div className="empty">Compare needs jobs in both cities. {A}: {nA} · {B}: {nB}. {!nB && `${B} feeds come after ${A} is solid.`}</div>;
  }
  const max = axisMax(Math.max(...rows.map((r) => Math.max(r.ap, r.bp)), 0));
  const gapMax = Math.max(5, ...rows.map((r) => Math.abs(r.gap)));
  const w = (p) => `${Math.min(100, (p / max) * 100)}%`;

  return (
    <div className="bars" style={{ "--tick": "50%" }}>
      <div className="controls" style={{ marginBottom: 4 }}>
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
        <div className="cty"><span><b>Gap</b> <span className="dim">pts</span></span><div className="axis"><span style={{ left: 0 }}>◂ {A}</span><span style={{ left: "100%" }}>SF ▸</span></div></div>
      </div>
      {rows.slice(0, shown).map((r, i) => (
        <div key={r.id} className={`cmp-row${selected === r.id ? " sel" : ""}`}>
          <button type="button" className="name" onClick={() => onSelect(selected === r.id ? null : r.id)} aria-label={`${r.name}: ${A} ${r.ap}%, ${B} ${r.bp}%. Filter job list`}>
            <span className="rank">{i + 1}</span>{r.name}
          </button>
          <button type="button" className="cb track" onClick={() => onSelectCity(r.id, A)} aria-label={`${r.name} in ${A}, ${r.ap}%`}>
            <span className="fill" style={{ width: w(r.ap) }} /><b>{r.ap}%</b><span>{r.a}</span>
          </button>
          <button type="button" className="cb sf track" onClick={() => onSelectCity(r.id, B)} aria-label={`${r.name} in ${B}, ${r.bp}%`}>
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
        <div><span>Click a skill to filter jobs · click one city's bar for skill + city</span></div>
      </div>
    </div>
  );
}
