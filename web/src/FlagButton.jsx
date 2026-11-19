// "This job doesn't belong here" (HIR-226): one click flags a job, a second click takes
// the flag off. No reason to pick and no form — the click sends the whole view (flagView.js)
// and the server keeps it next to the job as it was stored, so `python -m app flags` can
// work out which filter the job should not have passed.
//
// Three pieces, because the job list needs them in different places: `useFlag` holds the
// state, `FlagToggle` is the button (and, once flagged, the mark), and `FlagNote` is the
// optional one-line note offered right after the click.
//
// Does NOT hide the job, change any count, or keep anything in the browser: whether a job
// is flagged comes from the server with the job (`flagged`).
import { useEffect, useState } from "react";
import { api } from "./api.js";
import { Flag } from "./icons.jsx";

export const NOTE_MAX = 200;   // app/flags.py NOTE_MAX

export function useFlag(jobId, flagged, getView) {
  const [on, setOn] = useState(Boolean(flagged));
  const [flagId, setFlagId] = useState(null);   // set by the click that flagged: the note is on offer
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => { setOn(Boolean(flagged)); }, [flagged]);
  useEffect(() => { setFlagId(null); }, [jobId]);   // a note on offer belongs to the job it was for

  const toggle = () => {
    if (busy) return;
    setBusy(true);
    const done = on
      ? api.unflag(jobId).then(() => { setOn(false); setFlagId(null); })
      : api.flag(jobId, getView()).then((r) => { setOn(true); setFlagId(r.flag_id); setNote(""); });
    done.catch(() => {}).finally(() => setBusy(false));
  };
  // The flag is already stored; the note only adds to it, so closing without one is fine.
  const closeNote = () => setFlagId(null);
  const saveNote = () => {
    if (flagId && note.trim()) api.flagNote(flagId, note).catch(() => {});
    closeNote();
  };
  return { on, busy, toggle, noteOpen: flagId !== null, note, setNote, saveNote, closeNote };
}

// `withText` spells the button out (the job's own page has room). The list row shows the
// icon alone and puts its own "flagged" mark beside the title.
export function FlagToggle({ flag, name, withText = false }) {
  const stop = (e) => e.stopPropagation();
  return (
    <button type="button" className={`flag${flag.on ? " on" : ""}`} aria-pressed={flag.on} disabled={flag.busy}
      aria-label={flag.on ? `Flagged: ${name} doesn't belong here. Click to remove the flag` : `Flag ${name}: doesn't belong here`}
      title={flag.on ? "Flagged as not belonging here — click to remove the flag" : "This job doesn't belong here"}
      onClick={(e) => { stop(e); flag.toggle(); }} onKeyDown={stop}>
      <Flag />{withText && <span>{flag.on ? "Flagged" : "Doesn't belong here"}</span>}
    </button>
  );
}

export function FlagNote({ flag, id }) {
  if (!flag.noteOpen) return null;
  return (
    <form className="flag-note" onSubmit={(e) => { e.preventDefault(); flag.saveNote(); }} onClick={(e) => e.stopPropagation()}>
      <b>Flagged.</b>
      <label htmlFor={id}>Why doesn't it belong? <span className="dim">(optional)</span></label>
      <input id={id} className="inp" maxLength={NOTE_MAX} autoFocus placeholder="e.g. it's a platform role" value={flag.note}
        onChange={(e) => flag.setNote(e.target.value)} onKeyDown={(e) => { if (e.key === "Escape") flag.closeNote(); }} />
      <button type="submit" className="btn">{flag.note.trim() ? "Save note" : "Done"}</button>
    </form>
  );
}
