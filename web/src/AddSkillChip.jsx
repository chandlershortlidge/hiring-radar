import { useEffect, useMemo, useRef, useState } from "react";
import { Plus } from "./icons.jsx";
import { filterSkills } from "./skillMatch.js";

const MAX = 12;

// "+ Add skill" at the end of the chip row, and the typeahead popover it opens. Before this
// the only ways into the AND filter were a ⇧/⌘-click on a chart bar and a related-skills
// row, neither of which says so until you already know.
//
// Two lists, one box. An empty query shows `suggestions`, which App sources and orders
// (the related-skills rows while a skill is selected, the chart's own rows before that);
// typing switches to the whole taxonomy through the shared matcher. Selected skills are
// dropped from both — the chip row already shows them. Adding keeps the popover open and
// clears the query, so the next suggestion list (recomputed from App's new request) is
// right there to add from.
//
// It owns no filter state: a pick calls `onAdd` and App's `skillIds` is the only thing that
// moves. No fetching here either.
export default function AddSkillChip({ selected, suggestions, taxonomy, aliases, onAdd }) {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const [cursor, setCursor] = useState(0);
  const box = useRef(null);
  const input = useRef(null);

  useEffect(() => { if (open) input.current?.focus(); }, [open]);
  useEffect(() => {
    if (!open) return;
    const away = (e) => { if (box.current && !box.current.contains(e.target)) setOpen(false); };
    document.addEventListener("mousedown", away);
    return () => document.removeEventListener("mousedown", away);
  }, [open]);

  const rows = useMemo(() => {
    const taken = new Set(selected);
    const base = q.trim() ? filterSkills(taxonomy, aliases, q) : suggestions;
    return base.filter((s) => !taken.has(s.skill_id)).slice(0, MAX);
  }, [q, suggestions, taxonomy, aliases, selected]);

  useEffect(() => { setCursor(0); }, [q, suggestions]);

  const close = () => { setOpen(false); setQ(""); setCursor(0); };
  const pick = (id) => { onAdd(id); setQ(""); setCursor(0); input.current?.focus(); };

  const onKeyDown = (e) => {
    if (e.key === "Escape") { e.preventDefault(); close(); return; }
    if (e.key === "ArrowDown") { e.preventDefault(); setCursor((n) => Math.min(n + 1, rows.length - 1)); return; }
    if (e.key === "ArrowUp") { e.preventDefault(); setCursor((n) => Math.max(n - 1, 0)); return; }
    if (e.key === "Enter") { e.preventDefault(); if (rows[cursor]) pick(rows[cursor].skill_id); }
  };

  return (
    <span className="add-skill" ref={box}>
      <button type="button" className="chip-add" aria-expanded={open} aria-haspopup="listbox"
        onClick={() => (open ? close() : setOpen(true))}>
        <Plus size={12} /> Add skill
      </button>
      {open && (
        <div className="skill-pop">
          <label htmlFor="add-skill-q" className="sr">Find a skill to add to the filter</label>
          <input id="add-skill-q" ref={input} type="search" className="inp" placeholder="Find a skill (name or alias)"
            value={q} onChange={(e) => setQ(e.target.value)} onKeyDown={onKeyDown}
            role="combobox" aria-expanded aria-controls="add-skill-list" aria-autocomplete="list" />
          <div className="pop-note">{q.trim() ? `${rows.length} match${rows.length === 1 ? "" : "es"}`
            : selected.length ? "Skills these jobs also require" : "Most asked for"}</div>
          <ul id="add-skill-list" className="pop-list" role="listbox">
            {rows.map((s, n) => (
              <li key={s.skill_id} role="option" aria-selected={n === cursor}>
                <button type="button" className={`pop-row${n === cursor ? " on" : ""}`}
                  onMouseEnter={() => setCursor(n)} onClick={() => pick(s.skill_id)}>
                  <span className="name">{s.display}</span>
                  {s.note && <span className="share">{s.note}</span>}
                </button>
              </li>
            ))}
          </ul>
          {!rows.length && <div className="pop-empty">{q.trim() ? `No skill matches “${q.trim()}”.` : "Nothing left to suggest."}</div>}
        </div>
      )}
    </span>
  );
}
