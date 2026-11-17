import { useEffect, useRef, useState } from "react";
import { GERMAN_FILTERS, SENIORITIES, cap } from "./format.js";

// The chart's filters as one row of pills (HIR-285, the chosen layout): "Required only",
// seniority, German, and "More filters" for the three used least (production experience,
// degree, time window). They were a row of labelled boxes that took two lines.
//
// Same filters, same values, same requests as before: this only changes how they are
// drawn. A pill that is on is plum; the seniority pill opens a small menu because
// several levels can be on at once; German is the browser's own dropdown drawn as a pill.
// `children` are the extra filters, shown under the row while "More filters" is open.

// What the seniority pill reads: the levels that are on, or that none is.
export const seniorityLabel = (on) => (on.length ? on.map(cap).join(" + ") : "Any seniority");
// What each German choice reads inside its pill, where no label sits beside it.
export const germanLabel = (key) => (key === "any" ? "Any German" : `German: ${GERMAN_FILTERS[key].toLowerCase()}`);

export default function FilterPills({ filters, set, toggleSeniority, requiredLabel, extraOn = 0, children }) {
  const [menu, setMenu] = useState(false);
  const [more, setMore] = useState(false);
  const box = useRef(null);
  // The menu closes on a click anywhere else and on Escape, as the city picker does.
  useEffect(() => {
    if (!menu) return undefined;
    const away = (e) => { if (box.current && !box.current.contains(e.target)) setMenu(false); };
    const esc = (e) => { if (e.key === "Escape") setMenu(false); };
    document.addEventListener("mousedown", away);
    document.addEventListener("keydown", esc);
    return () => { document.removeEventListener("mousedown", away); document.removeEventListener("keydown", esc); };
  }, [menu]);

  const required = filters.requirement === "required";
  const open = more || extraOn > 0;
  return (
    <>
      <div className="fpills" role="group" aria-label="Filters">
        <button type="button" className="fpill" aria-pressed={required}
          onClick={() => set({ requirement: required ? "all" : "required" })}>{requiredLabel}</button>

        <div className="fmenu" ref={box}>
          <button type="button" className={`fpill${filters.seniorities.length ? " on" : ""}`}
            aria-haspopup="true" aria-expanded={menu} onClick={() => setMenu((v) => !v)}>
            {seniorityLabel(filters.seniorities)}<span className="caret" aria-hidden="true">▾</span>
          </button>
          {menu && (
            <div className="fmenu-pop" role="group" aria-label="Seniority">
              <button type="button" className="fpill" aria-pressed={!filters.seniorities.length} onClick={() => set({ seniorities: [] })}>Any</button>
              {SENIORITIES.map((s) => (
                <button key={s} type="button" className="fpill" aria-pressed={filters.seniorities.includes(s)} onClick={() => toggleSeniority(s)}>{cap(s)}</button>
              ))}
            </div>
          )}
        </div>

        <label className={`fpill pick${filters.german !== "any" ? " on" : ""}`}>
          <span className="sr">German</span>
          <select id="de" value={filters.german} onChange={(e) => set({ german: e.target.value })}>
            {Object.keys(GERMAN_FILTERS).map((k) => <option key={k} value={k}>{germanLabel(k)}</option>)}
          </select>
          <span className="caret" aria-hidden="true">▾</span>
        </label>

        <button type="button" className={`fpill more${extraOn ? " on" : ""}`} aria-expanded={open}
          onClick={() => setMore((v) => !v)}>More filters{extraOn ? ` · ${extraOn}` : ""}</button>
      </div>
      {open && <div className="controls">{children}</div>}
    </>
  );
}
