import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "./api.js";
import { CITIES, DEGREE_FILTERS, GERMAN_FILTERS, SENIORITIES, cap, dateTime, timeAgo } from "./format.js";
import { useProfile } from "./profile.js";
import { Compare, Person, Plus, Radar } from "./icons.jsx";
import SkillChart from "./SkillChart.jsx";
import CompareChart from "./CompareChart.jsx";
import JobList from "./JobList.jsx";
import AddJobDrawer from "./AddJobDrawer.jsx";
import ReviewDrawer from "./ReviewDrawer.jsx";
import ProfileDrawer from "./ProfileDrawer.jsx";

const WINDOWS = { open: "Currently open", "30d": "Last 30 days", "90d": "Last 90 days", all: "All" };
const DEFAULT = { cities: [], compare: false, seniorities: [], requirement: "required", window: "open", german: "any", degree: "any", skill: null, query: "" };

export default function App() {
  const [filters, setFilters] = useState(DEFAULT);
  const [stats, setStats] = useState(null);
  const [skills, setSkills] = useState(null);
  const [tax, setTax] = useState({ version: 0, skills: [] });
  const [drawer, setDrawer] = useState(null); // 'add' | 'review' | 'profile'
  const [refresh, setRefresh] = useState(0);
  const [jumpTo, setJumpTo] = useState(null);
  const [profile, saveProfile] = useProfile();

  const reload = useCallback(() => { api.stats().then(setStats); setRefresh((n) => n + 1); }, []);
  useEffect(() => { api.taxonomy().then(setTax); reload(); }, [reload]);
  useEffect(() => { let live = true; api.skills(filters).then((r) => { if (live) setSkills(r); }); return () => { live = false; }; }, [filters, refresh]);

  const taxName = useMemo(() => Object.fromEntries(tax.skills.map((s) => [s.id, s.display])), [tax]);
  const set = (patch) => setFilters((f) => ({ ...f, ...patch }));
  const setCity = (c) => set(c === "compare" ? { compare: true, cities: [] } : { compare: false, cities: c ? [c] : [] });
  const toggleSen = (s) => set({ seniorities: filters.seniorities.includes(s) ? filters.seniorities.filter((x) => x !== s) : [...filters.seniorities, s] });
  const viewJob = (id) => { setDrawer(null); set({ skill: null, query: "", window: "all" }); setJumpTo(id); };

  const cityLabel = filters.compare ? `${CITIES.join(" + ")}` : filters.cities.length ? filters.cities.join(" + ") : CITIES.join(" + ");
  const winLabel = filters.window === "open" ? "currently open" : filters.window === "all" ? "" : `from the last ${filters.window.replace("d", " days")}`;
  const reqLabel = filters.requirement === "required" ? "as required" : "as required or nice-to-have";
  const senLabel = (filters.seniorities.length ? ` · ${filters.seniorities.map(cap).join("/")} roles` : "")
    + (filters.german !== "any" ? ` · German: ${GERMAN_FILTERS[filters.german].toLowerCase()}` : "")
    + (filters.degree !== "any" ? ` · degree: ${DEGREE_FILTERS[filters.degree].toLowerCase()}` : "");

  return (
    <>
      <header className="hdr"><div className="hdr-in">
        <div className="brand"><Radar /><b>hiring-radar</b><span className="sub">AI-engineering skills, {CITIES.join(" + ")}</span></div>
        <div className="hdr-actions">
          <button type="button" className={`pill${profile ? " on" : ""}`} onClick={() => setDrawer("profile")} aria-label="Your profile">
            <Person /><span className="lbl">{profile ? `${profile.skills.length} skills in your profile` : "Set up your profile"}</span>
          </button>
          <button type="button" className="pill" onClick={() => setDrawer("review")} aria-label={`${stats?.proposed_pending ?? 0} proposed skills to review`}>
            <span className="count">{stats?.proposed_pending ?? 0}</span><span className="lbl">proposed skills</span>
          </button>
          <button type="button" className="btn outline" onClick={() => setDrawer("add")}><Plus /><span className="lbl">Add a job</span></button>
        </div>
      </div></header>

      <main className="main">
        {stats && (
          <p className="stats">
            <span>{stats.jobs} jobs</span><span>·</span>
            <span><abbr title={`A feed-sourced job counts as open while a feed still listed it in the last ${stats.open_rule.feed_days} days. A job added by hand is assumed open for ${stats.open_rule.manual_days} days.`}>{stats.open} currently open</abbr>
              {Object.keys(stats.open_by_city).length > 1 && ` (${Object.entries(stats.open_by_city).map(([c, n]) => `${c} ${n}`).join(" · ")})`}</span><span>·</span>
            <span>{stats.companies} companies</span><span>·</span>
            <span>{stats.skills_tracked} skills tracked</span><span>·</span>
            {stats.open > 0 && <><span><abbr title="Open jobs that ask for German outright or are written in German">{stats.open_german_required} need German</abbr></span><span>·</span>
            <span><abbr title="Open jobs that name a degree, don't mark it optional, and don't accept equivalent experience">{stats.open_degree_required} need a degree</abbr></span><span>·</span></>}
            {stats.legacy > 0 && <><span><abbr title="Imported from the old project with the old extractor's skills; listed but not counted in the chart">{stats.legacy} legacy, not charted</abbr></span><span>·</span></>}
            <span>{stats.last_updated ? `last updated ${timeAgo(stats.last_updated)} (${dateTime(stats.last_updated)})` : "no jobs yet"}</span>
          </p>
        )}

        <section className="card chart" aria-labelledby="chart-title">
          <div>
            <h1 id="chart-title">{filters.compare ? `${CITIES[0]} vs ${CITIES[1]}: which skills does each market ask for?` : "What skills are AI-engineering jobs asking for?"}</h1>
            <p className="lede">
              {filters.compare ? `Share of each city's ${winLabel || "tracked"} jobs listing the skill ${reqLabel}`
                : `Share of the ${skills?.total ?? "…"} ${winLabel} jobs that list each skill ${reqLabel} · ${cityLabel}`}{senLabel}.
              {profile && " Solid bars are skills in your profile."}
            </p>
          </div>
          <div className="controls">
            <div className="ctl"><span>City</span>
              <div className="seg" role="group" aria-label="City">
                <button type="button" aria-pressed={!filters.compare && !filters.cities.length} onClick={() => setCity(null)}>All</button>
                {CITIES.map((c) => <button key={c} type="button" aria-pressed={!filters.compare && filters.cities[0] === c} onClick={() => setCity(c)}>{c}</button>)}
                <button type="button" aria-pressed={filters.compare} onClick={() => setCity("compare")}><Compare />Compare</button>
              </div>
            </div>
            <div className="ctl"><span>Requirement</span>
              <div className="seg" role="group" aria-label="Requirement">
                <button type="button" aria-pressed={filters.requirement === "required"} onClick={() => set({ requirement: "required" })}>Required only</button>
                <button type="button" aria-pressed={filters.requirement === "all"} onClick={() => set({ requirement: "all" })}>Required + nice-to-have</button>
              </div>
            </div>
            <div className="ctl"><span>Seniority</span>
              <div className="seg" role="group" aria-label="Seniority">
                <button type="button" aria-pressed={!filters.seniorities.length} onClick={() => set({ seniorities: [] })}>Any</button>
                {SENIORITIES.map((s) => <button key={s} type="button" aria-pressed={filters.seniorities.includes(s)} onClick={() => toggleSen(s)}>{cap(s)}</button>)}
              </div>
            </div>
            <div className="ctl"><label htmlFor="de">German</label>
              <select id="de" className="sel" value={filters.german} onChange={(e) => set({ german: e.target.value })}>
                {Object.entries(GERMAN_FILTERS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
            <div className="ctl"><label htmlFor="deg">Degree</label>
              <select id="deg" className="sel" value={filters.degree} onChange={(e) => set({ degree: e.target.value })}>
                {Object.entries(DEGREE_FILTERS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
            <div className="ctl"><label htmlFor="win">Time window</label>
              <select id="win" className="sel" value={filters.window} onChange={(e) => set({ window: e.target.value })}>
                {Object.entries(WINDOWS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
          </div>
          {filters.compare
            ? <CompareChart data={skills} selected={filters.skill} onSelect={(id) => set({ skill: id })}
                onSelectCity={(id, city) => set({ skill: id, compare: false, cities: [city] })} />
            : <SkillChart data={skills} selected={filters.skill} onSelect={(id) => set({ skill: id })} profile={profile}
                cityLabel={`${winLabel || "tracked"} jobs`} />}
        </section>

        <JobList filters={filters} setFilters={setFilters} skillName={filters.skill ? taxName[filters.skill] || filters.skill : ""}
          profile={profile} taxonomy={taxName} refreshKey={refresh} openJobId={jumpTo} onOpened={() => setJumpTo(null)} />
      </main>

      {drawer === "add" && <AddJobDrawer onClose={() => setDrawer(null)} onAdded={reload} onViewJob={viewJob} />}
      {drawer === "review" && <ReviewDrawer onClose={() => setDrawer(null)} taxonomyList={tax.skills} skillsTracked={stats?.skills_tracked ?? tax.skills.length} onChanged={reload} onViewJob={viewJob} />}
      {drawer === "profile" && <ProfileDrawer onClose={() => setDrawer(null)} profile={profile} save={saveProfile} taxonomyList={tax.skills} />}
    </>
  );
}
