import { COMPARE_MAX, FAMILIES, PLACES, familyLabel } from "./format.js";
import { X } from "./icons.jsx";
import CityPicker from "./CityPicker.jsx";

// The band at the top of the page that says which market you are looking at (HIR-188):
// "[AI Engineer ▾] in [Berlin ▾]". It replaced the row of city tabs, which only worked
// while there were four places and one kind of job.
//
// In compare mode the city picker becomes two or three removable tokens plus an "add"
// picker, and the whole bar gains a way back out.
//
// Both ways into compare are the same city list as the picker itself (HIR-191): "+ Compare
// with…" and compare mode's "+ add" are a CityPicker with nothing chosen, so entering a
// comparison is one click and one pick, not a mode switch followed by a pick.
//
// `landing` is the first screen, before any city is chosen: the bar centres itself and grows
// a size. The dashboard keeps its own alignment, where the bar is a control above a chart
// rather than the subject of the page.
//
// The family side is a plain <select>: a short, flat list of five needs no search box,
// and the browser's own control is the most accessible thing available. The city side is
// a custom listbox because it needs search, country groups and job counts.
export default function QueryBar({
  place, family, counts, recent, compare, compareCities, landing,
  onPlace, onFamily, onStartCompare, onAddCity, onRemoveCity, onExitCompare, onRequestCity, right,
}) {
  const left = PLACES.filter((p) => !compareCities.includes(p.name));

  return (
    <div className={`qbar${landing ? " landing" : ""}`}>
      <div className="qbar-in">
        <div className="qb">
          <label className="sr" htmlFor="qb-family">Job family</label>
          <select id="qb-family" className="qb-btn qb-sel" value={family || ""} onChange={(e) => onFamily(e.target.value || null)}>
            <option value="">All AI &amp; data roles</option>
            {FAMILIES.map((f) => <option key={f} value={f}>{familyLabel(f)}</option>)}
          </select>
          <span className="qb-in">in</span>

          {compare ? (
            <>
              {compareCities.map((c, i) => (
                <span key={c} className={`token col-${i}`}>
                  {c}
                  <button type="button" onClick={() => onRemoveCity(c)} aria-label={`Remove ${c} from the comparison`}><X size={12} /></button>
                </span>
              ))}
              {compareCities.length < COMPARE_MAX
                ? <CityPicker value={null} counts={counts} recent={recent} exclude={compareCities}
                    placeholder="+ add" variant="add" disabled={!left.length}
                    onPick={onAddCity} onRequestCity={onRequestCity} />
                : <button type="button" className="qb-add" disabled>+ add (max {COMPARE_MAX})</button>}
              <button type="button" className="btn ghost qb-exit" onClick={onExitCompare}>Exit compare</button>
            </>
          ) : (
            <>
              <CityPicker value={place} counts={counts} recent={recent} onPick={onPlace} onRequestCity={onRequestCity} />
              <CityPicker value={null} counts={counts} recent={recent} exclude={[place]}
                placeholder="+ Compare with…" variant="add" disabled={!place}
                onPick={onStartCompare} onRequestCity={onRequestCity} />
            </>
          )}
        </div>
        {right && <div className="qb-right">{right}</div>}
      </div>
    </div>
  );
}
