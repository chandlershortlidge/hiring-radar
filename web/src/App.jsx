import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "./api.js";
import { CITIES, PLACES, DEGREE_FILTERS, GERMAN_FILTERS, PRODUCTION_FILTERS, SENIORITIES, cap, dateTime, pctInt, timeAgo } from "./format.js";
import { useProfile } from "./profile.js";
import { Compare, Down, Person, Plus, Radar } from "./icons.jsx";
import SkillChart from "./SkillChart.jsx";
import CompareChart from "./CompareChart.jsx";
import JobList from "./JobList.jsx";
import RelatedSkills from "./RelatedSkills.jsx";
import SkillTree from "./SkillTree.jsx";
import AddJobDrawer from "./AddJobDrawer.jsx";
import ReviewDrawer from "./ReviewDrawer.jsx";
import ProfileDrawer from "./ProfileDrawer.jsx";
import JobPage from "./JobPage.jsx";

const WINDOWS = { open: "Currently open", "30d": "Last 30 days", "90d": "Last 90 days", all: "All" };
const DEFAULT = { cities: [], compare: false, seniorities: [], requirement: "required", window: "open", german: "any", degree: "any", production: "any", skillIds: [], query: "" };

// The only route besides "/": /jobs/{id} is a job's own page. The server returns index.html
// for every path, so the address bar is read here, on load and whenever the back/forward
// buttons change it. Returns the job id or null.
const jobFromPath = (path = window.location.pathname) => { const m = /^\/jobs\/(\d+)\/?$/.exec(path); return m ? Number(m[1]) : null; };

// The skill tree is the one card that stays shut until asked for: it is a big drawing and
// most visits want the chart and the list. Which way the reader left it is remembered per
// browser, like the profile and with the same care — storage throws in private modes, and
// a dashboard must not go blank over a preference.
const TREE_KEY = "hiring-radar.skilltree.v1";
const treeWasOpen = () => { try { return localStorage.getItem(TREE_KEY) === "1"; } catch { return false; } };
const rememberTree = (open) => { try { localStorage.setItem(TREE_KEY, open ? "1" : "0"); } catch {} };

export default function App() {
  const [filters, setFilters] = useState(DEFAULT);
  const [stats, setStats] = useState(null);
  const [skills, setSkills] = useState(null);
  const [tax, setTax] = useState({ version: 0, skills: [] });
  const [related, setRelated] = useState(null);
  const [tree, setTree] = useState(null);
  const [treeOpen, setTreeOpen] = useState(treeWasOpen);
  const [drawer, setDrawer] = useState(null); // 'add' | 'review' | 'profile'
  const [refresh, setRefresh] = useState(0);
  const [jumpTo, setJumpTo] = useState(null);
  const [profile, saveProfile] = useProfile();
  const [pageJob, setPageJob] = useState(jobFromPath);

  useEffect(() => { const onPop = () => setPageJob(jobFromPath()); window.addEventListener("popstate", onPop); return () => window.removeEventListener("popstate", onPop); }, []);
  const openPage = (id) => { window.history.pushState(null, "", `/jobs/${id}`); setPageJob(id); window.scrollTo(0, 0); };
  const closePage = () => { window.history.pushState(null, "", "/"); setPageJob(null); };

  const reload = useCallback(() => { api.stats().then(setStats); setRefresh((n) => n + 1); }, []);
  useEffect(() => { api.taxonomy().then(setTax); reload(); }, [reload]);
  useEffect(() => { let live = true; api.skills(filters).then((r) => { if (live) setSkills(r); }); return () => { live = false; }; }, [filters, refresh]);
  // Shut means unasked-for: no request until the reader opens it once. After that it
  // follows the filters like every other card.
  useEffect(() => {
    if (!treeOpen) return;
    let live = true;
    setTree(null);
    api.skillTree(filters).then((r) => { if (live) setTree(r); });
    return () => { live = false; };
  }, [filters, refresh, treeOpen]);
  const toggleTree = () => setTreeOpen((open) => { rememberTree(!open); return !open; });
  // The related-skills rows, fetched here and not in the panel: the panel draws them and the
  // chip row's add-skill popover suggests them, both from this one request and in its order.
  useEffect(() => {
    if (!filters.skillIds.length) { setRelated(null); return; }
    let live = true;
    api.relatedSkills(filters).then((r) => { if (live) setRelated(r); });
    return () => { live = false; };
  }, [filters, refresh]);

  const taxName = useMemo(() => Object.fromEntries(tax.skills.map((s) => [s.id, s.display])), [tax]);
  // For the chart's find box: it matches a skill's aliases as well as its display name.
  const taxAliases = useMemo(() => Object.fromEntries(tax.skills.map((s) => [s.id, s.aliases || []])), [tax]);
  // What the add-skill popover types over, and what it offers before anything is typed: the
  // related rows once a skill is selected, the chart's own rows (document frequency) before.
  const taxRows = useMemo(() => tax.skills.map((s) => ({ skill_id: s.id, display: s.display })), [tax]);
  const skillSuggestions = useMemo(() => (filters.skillIds.length
    ? (related?.skills || []).map((s) => ({ skill_id: s.skill_id, display: s.display, note: `${Math.round(s.pct)}% · vs ${Math.round(s.base_pct)}% of all jobs` }))
    : (skills?.skills || []).map((s) => ({ skill_id: s.skill_id, display: s.display, note: `${pctInt(s.count, skills.total)}% of jobs` }))),
  [filters.skillIds, related, skills]);
  const set = (patch) => setFilters((f) => ({ ...f, ...patch }));
  const setCity = (c) => set(c === "compare" ? { compare: true, cities: [] } : { compare: false, cities: c ? [c] : [] });
  const toggleSen = (s) => set({ seniorities: filters.seniorities.includes(s) ? filters.seniorities.filter((x) => x !== s) : [...filters.seniorities, s] });
  const viewJob = (id) => { setDrawer(null); if (pageJob) closePage(); set({ skillIds: [], query: "", window: "all" }); setJumpTo(id); };

  // The skill filter is a set, read as AND: the job list shows the jobs requiring every one
  // of them. A bar click replaces the selection — clicking the only selected skill clears it —
  // and a shift- or meta-click adds to it. A related-skills row always adds (that panel exists
  // to be drilled into). Nothing here touches the main chart, which ignores the selection.
  const selectSkill = (id, additive = false) => setFilters((f) => {
    const has = f.skillIds.includes(id);
    if (additive) return { ...f, skillIds: has ? f.skillIds.filter((x) => x !== id) : [...f.skillIds, id] };
    return { ...f, skillIds: has && f.skillIds.length === 1 ? [] : [id] };
  });
  const addSkill = (id) => setFilters((f) => (f.skillIds.includes(id) ? f : { ...f, skillIds: [...f.skillIds, id] }));
  const skillNames = filters.skillIds.map((id) => taxName[id] || id);

  const cityLabel = filters.compare ? `${CITIES.join(" + ")}` : filters.cities.length ? filters.cities.join(" + ") : PLACES.join(" + ");
  const winLabel = filters.window === "open" ? "currently open" : filters.window === "all" ? "" : `from the last ${filters.window.replace("d", " days")}`;
  const reqLabel = filters.requirement === "required" ? "as required" : "as required or nice-to-have";
  const senLabel = (filters.seniorities.length ? ` · ${filters.seniorities.map(cap).join("/")} roles` : "")
    + (filters.german !== "any" ? ` · German: ${GERMAN_FILTERS[filters.german].toLowerCase()}` : "")
    + (filters.production !== "any" ? ` · production experience: ${PRODUCTION_FILTERS[filters.production].toLowerCase()}` : "")
    + (filters.degree !== "any" ? ` · degree: ${DEGREE_FILTERS[filters.degree].toLowerCase()}` : "");

  return (
    <>
      <header className="hdr"><div className="hdr-in">
        <div className="brand"><a href="/" onClick={(e) => { e.preventDefault(); if (pageJob) closePage(); }} className="home" aria-label="hiring-radar home"><Radar /><b>hiring-radar</b></a><span className="sub">AI-engineering skills, {PLACES.join(" + ")}</span></div>
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

      {pageJob ? <JobPage id={pageJob} onBack={closePage} profile={profile} taxonomy={taxName} /> : <main className="main">
        {stats && (
          <p className="stats">
            <span>{stats.jobs} jobs</span><span>·</span>
            <span><abbr title={`A feed-sourced job counts as open while a feed still listed it in the last ${stats.open_rule.feed_days} days. A job added by hand is assumed open for ${stats.open_rule.manual_days} days.`}>{stats.open} currently open</abbr>
              {Object.keys(stats.open_by_city).length > 1 && ` (${Object.entries(stats.open_by_city).map(([c, n]) => `${c} ${n}`).join(" · ")})`}</span><span>·</span>
            <span>{stats.companies} companies</span><span>·</span>
            <span>{stats.skills_tracked} skills tracked</span><span>·</span>
            {stats.open > 0 && <><span><abbr title="Open jobs that ask for German outright or are written in German">{stats.open_german_required} need German</abbr></span><span>·</span>
            <span><abbr title="Open jobs that name a degree, don't mark it optional, and don't accept equivalent experience">{stats.open_degree_required} need a degree</abbr></span><span>·</span>
            <span><abbr title="Open jobs that ask the candidate for prior experience shipping or operating software real users depended on">{stats.open_production_required} need production experience</abbr></span><span>·</span></>}
            {stats.legacy > 0 && <><span><abbr title="Imported from the old project with the old extractor's skills; listed but not counted in the chart">{stats.legacy} legacy, not charted</abbr></span><span>·</span></>}
            {stats.too_short > 0 && <><span><abbr title="Only a fragment of the posting was stored; listed but not counted in the chart">{stats.too_short} too short, not charted</abbr></span><span>·</span></>}
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
                {PLACES.map((c) => <button key={c} type="button" aria-pressed={!filters.compare && filters.cities[0] === c} onClick={() => setCity(c)}>{c}</button>)}
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
            <div className="ctl"><label htmlFor="prod">Production experience</label>
              <select id="prod" className="sel" value={filters.production} onChange={(e) => set({ production: e.target.value })}>
                {Object.entries(PRODUCTION_FILTERS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
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
            ? <CompareChart data={skills} selected={filters.skillIds} onSelect={selectSkill}
                onSelectCity={(id, city) => set({ skillIds: [id], compare: false, cities: [city] })} />
            : <SkillChart data={skills} selected={filters.skillIds} onSelect={selectSkill} profile={profile}
                cityLabel={`${winLabel || "tracked"} jobs`} aliases={taxAliases} />}
        </section>

        <RelatedSkills filters={filters} skillNames={skillNames} onAdd={addSkill} data={related} />

        <JobList filters={filters} setFilters={setFilters}
          profile={profile} taxonomy={taxName} refreshKey={refresh} openJobId={jumpTo} onOpened={() => setJumpTo(null)} onOpenPage={openPage}
          taxonomyRows={taxRows} aliases={taxAliases} suggestions={skillSuggestions} onAddSkill={addSkill} />

        <section className="card chart" aria-labelledby="tree-title">
          <button type="button" className="fold" onClick={toggleTree}
            aria-expanded={treeOpen} aria-controls="tree-body">
            <h2 id="tree-title">The skill tree: what leads to what</h2>
            <span className="chev"><Down /></span>
          </button>
          <div id="tree-body" hidden={!treeOpen}>
            <p className="lede">
              The same {skills?.total ?? "…"} {winLabel} jobs, drawn as the market’s own
              specialization paths · {cityLabel}{senLabel}. The skills in most postings sit
              near the centre; an edge means the outer skill’s jobs nearly always ask for
              the inner one too. A node’s ring is how many jobs mention the skill and its
              solid core how many require it, because the gap between them is the point:
              mentioned often but required rarely is a résumé keyword, not a gate. Hover a
              skill, or tab to it, for both numbers. Required-only and the skill selection
              do not change this map.
            </p>
            {treeOpen && <SkillTree data={tree} selected={filters.skillIds} onSelect={selectSkill} />}
          </div>
        </section>
      </main>}

      {drawer === "add" && <AddJobDrawer onClose={() => setDrawer(null)} onAdded={reload} onViewJob={viewJob} />}
      {drawer === "review" && <ReviewDrawer onClose={() => setDrawer(null)} taxonomyList={tax.skills} skillsTracked={stats?.skills_tracked ?? tax.skills.length} onChanged={reload} onViewJob={viewJob} />}
      {drawer === "profile" && <ProfileDrawer onClose={() => setDrawer(null)} profile={profile} save={saveProfile} taxonomyList={tax.skills} />}
    </>
  );
}
