// "Where are my skills wanted?" — one line over the city comparison: per compared city,
// how many of its jobs the visitor's profile matches (HIR-16).
//
// The count happens here, in the browser: this asks for each city's jobs and counts them
// against the profile, because the server is never told the profile. What a match is
// lives in profile.js (`isMatch`), next to the fit score it reuses.
//
// It follows the chart's filters (family, seniority, German, degree, production, window)
// and deliberately not the skill selection or the search box, which narrow the job list
// only. It does NOT rank, list or link the jobs, and draws nothing for a visitor with no
// skills in their profile.
import { useEffect, useMemo, useState } from "react";
import { allJobs } from "./api.js";
import { MATCH_PCT, SKILL_FLOOR, countMatches } from "./profile.js";

// The chart's filters narrowed to one city, with the job list's own narrowing taken off.
export const cityFilters = (filters, city) => ({ ...filters, cities: [city], skillIds: [], query: "", text: "" });

// Each city's jobs, in the order the cities were given. Rejects if any request fails: a
// line with one city missing would read as a comparison and not be one.
export const fetchCityJobs = (filters, cities, get = allJobs) =>
  Promise.all(cities.map((city) => get(cityFilters(filters, city)).then((r) => ({ city, jobs: r.jobs, total: r.total }))));

// What the line prints: per city, the jobs matched and the jobs there are.
export const cityFitRows = (profile, fetched) =>
  fetched.map(({ city, jobs, total }) => ({ city, matched: countMatches(profile, jobs), total }));

const NOTE = `Counted on required skills only. Jobs that list fewer than ${SKILL_FLOOR} required skills are left out: too little to read as a percentage.`;

// The line itself. `rows` is null while the jobs are on their way.
export function CityFitLine({ rows, failed = false }) {
  if (failed) return <p className="cmp-fit">Could not count the jobs that match your profile.</p>;
  if (!rows) return <p className="cmp-fit">Counting the jobs that match your profile…</p>;
  return (
    <p className="cmp-fit" title={NOTE}>
      Jobs where you have at least {MATCH_PCT}% of the required skills:{" "}
      {rows.map((r, i) => (
        <span key={r.city}>{i > 0 && " · "}{r.city}: <b>{r.matched}</b> of {r.total}</span>
      ))}
    </p>
  );
}

export default function CityFit({ profile, filters, cities, refreshKey }) {
  const on = Boolean(profile?.skills.length);
  const [state, setState] = useState({ fetched: null, failed: false });
  // What the requests depend on, as text: selecting a skill or typing in the search box
  // makes a new `filters` object, and neither should count every job again.
  const asked = JSON.stringify([cityFilters(filters, null), cities]);
  useEffect(() => {
    if (!on) return undefined;
    let live = true;
    setState({ fetched: null, failed: false });
    const [f, cs] = JSON.parse(asked);
    fetchCityJobs(f, cs).then(
      (fetched) => { if (live) setState({ fetched, failed: false }); },
      () => { if (live) setState({ fetched: null, failed: true }); },
    );
    return () => { live = false; };
  }, [on, asked, refreshKey]);
  // Editing the profile recounts the jobs already here; it does not fetch them again.
  const rows = useMemo(() => (on && state.fetched ? cityFitRows(profile, state.fetched) : null), [on, profile, state.fetched]);
  if (!on) return null;
  return <CityFitLine rows={rows} failed={state.failed} />;
}
