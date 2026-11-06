import { useEffect, useMemo, useRef, useState } from "react";
import { ALL_GERMANY, PLACES, PLACE_GROUPS, placeBySlug, placeMatches } from "./format.js";
import { Search } from "./icons.jsx";

// The city half of the query bar: a button that opens a searchable list of every place
// (HIR-188). The list is grouped — the places you looked at recently first, then Germany,
// Remote and the United States — with each place's job count on the right, "All of
// Germany" at the end of the Germany group and a way to ask for a city we don't have.
//
// Places inside a group are ordered by job count, biggest first, so the busiest market in
// a country is the first one offered however long the list grows.
//
// Keyboard: the button opens the list and focus goes to the search box; up and down move
// the highlight, Enter picks it, Escape closes. Clicking outside closes it too.
export default function CityPicker({ value, counts, recent, onPick, onRequestCity }) {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const [at, setAt] = useState(0);
  const box = useRef(null);
  const input = useRef(null);

  const chosen = placeBySlug(value);
  const count = (p) => (p.slug === ALL_GERMANY.slug
    ? PLACES.filter((x) => x.group === "Germany").reduce((n, x) => n + (counts[x.name] || 0), 0)
    : counts[p.name] || 0);

  // The groups, as drawn: Recent (only when there is something to recall and nothing
  // typed), then every country group with its places sorted by job count.
  const groups = useMemo(() => {
    const match = (p) => placeMatches(p, q);
    const out = [];
    const recentPlaces = recent.map(placeBySlug).filter(Boolean).filter(match);
    if (!q.trim() && recentPlaces.length) out.push({ name: "Recent", places: recentPlaces });
    for (const g of PLACE_GROUPS) {
      const places = PLACES.filter((p) => p.group === g && match(p)).sort((a, b) => count(b) - count(a));
      if (g === "Germany" && (places.length || match(ALL_GERMANY))) places.push(ALL_GERMANY);
      if (places.length) out.push({ name: g, places });
    }
    return out;
  }, [q, recent, counts]);

  // One flat list in drawn order, so the arrow keys walk the list the eye sees.
  const flat = useMemo(() => groups.flatMap((g) => g.places.map((p) => ({ group: g.name, place: p }))), [groups]);
  useEffect(() => { setAt(0); }, [q]);
  useEffect(() => { if (open) input.current?.focus(); }, [open]);
  useEffect(() => {
    if (!open) return;
    const away = (e) => { if (box.current && !box.current.contains(e.target)) setOpen(false); };
    document.addEventListener("mousedown", away);
    return () => document.removeEventListener("mousedown", away);
  }, [open]);

  const close = () => { setOpen(false); setQ(""); };
  const pick = (p) => { close(); onPick(p.slug); };

  const onKey = (e) => {
    if (e.key === "Escape") { e.preventDefault(); close(); return; }
    if (e.key === "ArrowDown") { e.preventDefault(); setAt((i) => Math.min(flat.length - 1, i + 1)); return; }
    if (e.key === "ArrowUp") { e.preventDefault(); setAt((i) => Math.max(0, i - 1)); return; }
    if (e.key === "Enter" && flat[at]) { e.preventDefault(); pick(flat[at].place); }
  };

  return (
    <div className="picker" ref={box}>
      <button type="button" className="qb-btn" aria-haspopup="listbox" aria-expanded={open}
        onClick={() => (open ? close() : setOpen(true))}>
        {chosen ? chosen.name : "Pick a city"}<span className="caret" aria-hidden="true">▾</span>
      </button>
      {open && (
        <div className="pop" role="dialog" aria-label="Choose a city">
          <div className="pop-search">
            <Search />
            <input ref={input} className="inp" type="text" value={q} placeholder="Search city or country…"
              onChange={(e) => setQ(e.target.value)} onKeyDown={onKey} aria-label="Search city or country"
              aria-controls="city-listbox" aria-activedescendant={flat[at] ? `city-opt-${flat[at].group}-${flat[at].place.slug}` : undefined} />
            <button type="button" className="btn ghost esc" onClick={close}>esc</button>
          </div>
          <div className="pop-list" id="city-listbox" role="listbox" aria-label="Cities" tabIndex={-1}>
            <div className="pop-cols"><span>jobs</span></div>
            {flat.length === 0 && <p className="empty">No city matches “{q}”.</p>}
            {groups.map((g) => (
              <div key={g.name} className="pop-group">
                <div className="pop-head">{g.name}</div>
                {g.places.map((p) => {
                  const i = flat.findIndex((f) => f.group === g.name && f.place.slug === p.slug);
                  return (
                    <div key={p.slug} id={`city-opt-${g.name}-${p.slug}`} role="option"
                      aria-selected={p.slug === value}
                      className={`pop-opt${i === at ? " at" : ""}${p.slug === value ? " on" : ""}`}
                      onMouseEnter={() => setAt(i)} onClick={() => pick(p)}>
                      <span className="nm">{p.name}{p.slug === value && <b aria-hidden="true"> ✓</b>}</span>
                      <span className="n">{count(p)}</span>
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
          <div className="pop-foot">
            <span className="dim">↑↓ to move · ↵ to select</span>
            <button type="button" className="btn ghost" onClick={() => { close(); onRequestCity(); }}>Don’t see your city? Request it</button>
          </div>
        </div>
      )}
    </div>
  );
}
