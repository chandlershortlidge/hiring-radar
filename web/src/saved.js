// Saved jobs (HIR-99). The ids live only in this browser (localStorage, a key alongside
// the profile's); the server never learns which jobs are saved and stores nothing — the
// Saved view fetches each saved job by its public id, the same request any visitor makes.
//
// Also the pure logic the Saved view runs on: `sortJobs` reorders an already-fetched set
// the way the server would (so the Saved view honours the current sort without sending
// the ids anywhere), and `copyLines` is the clipboard export. Neither fetches, stores,
// nor filters: a saved job that has closed, or dropped out of every server filter, still
// sorts and exports like any other — the saved list never silently shrinks.
//
// What this file does NOT do: application status (applied / interviewing — Dossier's job,
// HIR-11/HIR-15), notes, or server-side saving (HIR-19 part C).
import { useCallback, useEffect, useState } from "react";
import { rankJobs } from "./profile.js";

const KEY = "hiring-radar.saved.v1";

// The stored shape is a plain array of job ids. Anything else — garbage, an old shape,
// storage that throws in private modes — reads as "nothing saved", never as a crash.
export function loadSaved() {
  try {
    const ids = JSON.parse(localStorage.getItem(KEY) || "[]");
    return Array.isArray(ids) ? ids.filter((n) => Number.isInteger(n)) : [];
  } catch { return []; }
}

export function saveSaved(ids) {
  try { localStorage.setItem(KEY, JSON.stringify(ids)); } catch {}
}

// One star click: saved becomes unsaved and back. Pure; returns a new array, newest save last.
export const toggleId = (ids, id) => (ids.includes(id) ? ids.filter((x) => x !== id) : [...ids, id]);

export function useSaved() {
  const [ids, setIds] = useState(loadSaved);
  const toggle = useCallback((id) => {
    setIds((cur) => { const next = toggleId(cur, id); saveSaved(next); return next; });
  }, []);
  // Another tab starring a job updates this one, same as the profile.
  useEffect(() => {
    const onStorage = (e) => { if (e.key === KEY) setIds(loadSaved()); };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);
  return [ids, toggle];
}

// --- the Saved view's pure logic ---------------------------------------------------------

// The server's SORTS (app/queries.py), re-spoken in the browser: the Saved view has the
// whole (small) set in hand, so it sorts locally instead of telling the server which jobs
// to order. "Best fit" reuses rankJobs over a newest-first base, exactly what the main
// list does, so both views rank identically.
const COMPARE = {
  newest: (a, b) => b.first_seen.localeCompare(a.first_seen) || b.id - a.id,
  oldest: (a, b) => a.first_seen.localeCompare(b.first_seen) || a.id - b.id,
  reposts: (a, b) => b.repost_count - a.repost_count || b.first_seen.localeCompare(a.first_seen),
  company: (a, b) => a.company.toLowerCase().localeCompare(b.company.toLowerCase()) || b.first_seen.localeCompare(a.first_seen),
};

export function sortJobs(jobs, sort, profile = null, demand = null) {
  const newest = [...jobs].sort(COMPARE.newest);
  if (sort === "fit") return profile ? rankJobs(profile, newest, demand) : newest;
  return COMPARE[sort] ? [...jobs].sort(COMPARE[sort]) : newest;
}

// The handoff to Dossier or a spreadsheet until HIR-15: one line per job,
// `company — title — url`, in the order given. A job with no stored URL (a screenshot or
// pasted posting) keeps its line, just without the third part.
export const jobUrl = (job) => (job.sources || []).find((s) => s.url)?.url || "";
export const copyLines = (jobs) => jobs.map((j) => [j.company, j.title, jobUrl(j)].filter(Boolean).join(" — ")).join("\n");
