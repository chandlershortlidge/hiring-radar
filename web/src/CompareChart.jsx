import { useMemo, useState } from "react";
import { axisMax, pctInt } from "./format.js";

const PAGE = 15;

// One column per place, each bar a share of that place's own job set, for two or three
// places at once (HIR-188; it was a fixed two sides with a diverging gap bar, HIR-138).
// Which places are in the comparison is the reader's choice and lives in the query bar
// above, so this component only draws what it is given.
//
// Rows are sorted by one column — the first place by default, the reader can click any
// column header — or by the widest spread between the places, or by name. The spread is
// also what the "largest gap" note marks. `selected` is the set of selected skill ids; a
// name click reports whether it was additive (shift or meta), exactly as SkillChart does.
export default function CompareChart({ data, selected, onSelect, onSelectCity, cities }) {
  const [shown, setShown] = useState(PAGE);
  // Sort key: a place name, "gap" or "alpha". Falls back to the first place whenever the
  // place it names has just been removed from the comparison.
  const [sort, setSort] = useState(null);
  const by = sort === "gap" || sort === "alpha" || cities.includes(sort) ? sort : cities[0];

  const totals = data?.city_totals || {};
  const counts = cities.map((c) => totals[c] || 0);
  const empty = cities.filter((c, i) => !counts[i]);

  const rows = useMemo(() => {
    const r = (data?.skills || []).map((s) => {
      const per = cities.map((c, i) => {
        const n = s.by_city?.[c] || 0;
        return { city: c, n, pct: pctInt(n, totals[c] || 0) };
      });
      const shares = per.map((p) => p.pct);
      return { id: s.skill_id, name: s.display, per, gap: Math.max(...shares) - Math.min(...shares) };
    });
    const key = by === "gap" ? (x) => x.gap : by === "alpha" ? null : (x) => x.per[cities.indexOf(by)]?.pct ?? 0;
    return key
      ? r.sort((x, y) => key(y) - key(x) || x.name.localeCompare(y.name))
      : r.sort((x, y) => x.name.localeCompare(y.name));
  }, [data, by, cities, totals]);

  // Every place needs jobs: an empty column is a column of nothing, and the way out is to
  // drop that place in the query bar above, so say which one it is.
  if (empty.length) {
    return (
      <div className="bars">
        <div className="empty">
          Compare needs jobs in every market. {cities.map((c, i) => `${c}: ${counts[i]}`).join(" · ")}.
          Remove {empty.join(" and ")} above, or pick another market.
        </div>
      </div>
    );
  }

  const max = axisMax(Math.max(...rows.flatMap((r) => r.per.map((p) => p.pct)), 0));
  const widest = Math.max(...rows.map((r) => r.gap), 0);
  const w = (p) => `${Math.min(100, (p / max) * 100)}%`;
  // How many columns, as a custom property rather than an inline grid-template: an inline
  // template would beat the phone media query, which needs a narrower name column.
  const cols = { "--cols": cities.length };

  return (
    <div className="bars">
      <div className="ctl cmp-sort"><span>Sort by</span>
        <div className="seg" role="group" aria-label="Sort skills">
          {cities.map((c) => (
            <button key={c} type="button" aria-pressed={by === c} onClick={() => setSort(c)}>{c}</button>
          ))}
          <button type="button" aria-pressed={by === "gap"} onClick={() => setSort("gap")}>Biggest difference</button>
          <button type="button" aria-pressed={by === "alpha"} onClick={() => setSort("alpha")}>Alphabetical</button>
        </div>
      </div>
      <div className="cmp-head" style={cols}>
        <span>Skill</span>
        {cities.map((c, i) => (
          <div key={c} className="cty">
            <button type="button" className="cty-h" aria-pressed={by === c} onClick={() => setSort(c)}
              aria-label={`Sort the skills by ${c}`}><b>{c}</b> · {counts[i]} jobs</button>
            <div className="axis"><span style={{ left: 0 }}>0%</span><span style={{ left: "50%" }}>{max / 2}%</span><span style={{ left: "100%" }}>{max}%</span></div>
          </div>
        ))}
      </div>
      {rows.slice(0, shown).map((r) => (
        <div key={r.id} className={`cmp-row${selected.includes(r.id) ? " sel" : ""}`} style={cols}>
          <button type="button" className="name" onClick={(e) => onSelect(r.id, e.shiftKey || e.metaKey)}
            aria-label={`${r.name}: ${r.per.map((p) => `${p.city} ${p.pct}%`).join(", ")}. Filter job list`}>
            {r.name}{widest > 0 && r.gap === widest && <small className="dim"> · largest gap</small>}
          </button>
          {r.per.map((p, i) => (
            <button key={p.city} type="button" className={`cb track col-${i}`} onClick={() => onSelectCity(r.id, p.city)}
              aria-label={`${r.name} in ${p.city}, ${p.pct}%`}>
              <span className="fill" style={{ width: w(p.pct) }} /><b>{p.pct}%</b><span>{p.n}</span>
            </button>
          ))}
        </div>
      ))}
      <div className="bars-foot">
        <div>
          {shown < rows.length && <button type="button" className="btn" onClick={() => setShown(shown + PAGE)}>Show {Math.min(PAGE, rows.length - shown)} more</button>}
          <span>{Math.min(shown, rows.length)} of {rows.length} skills</span>
        </div>
        <div><span>Click a city header to make it the sort column · click a skill to filter jobs · ⇧- or ⌘-click to add a skill</span></div>
      </div>
    </div>
  );
}
