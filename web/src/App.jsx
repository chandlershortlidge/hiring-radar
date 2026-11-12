import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "./api.js";
import { COMPARE_DEFAULT, DEGREE_FILTERS, GERMAN_FILTERS, PLACE_NAMES, PRODUCTION_FILTERS, SENIORITIES, cap, compareAdd, compareRemove, dateTime, familyLabel, listFilters as deriveListFilters, placeByName, placeBySlug, placeCities, pctInt, timeAgo } from "./format.js";
import { HOME, parsePath, pathFor, withFamily } from "./routes.js";
import { pushRecent, readLast, readRecent, writeLast } from "./lastPlace.js";
import { useProfile } from "./profile.js";
import { Person, Plus, Radar } from "./icons.jsx";
import QueryBar from "./QueryBar.jsx";
import HomeGrid from "./HomeGrid.jsx";
import SkillChart from "./SkillChart.jsx";
import CompareChart from "./CompareChart.jsx";
import JobList from "./JobList.jsx";
import RelatedSkills from "./RelatedSkills.jsx";
import AddJobDrawer from "./AddJobDrawer.jsx";
import ReviewDrawer from "./ReviewDrawer.jsx";
import ProfileDrawer from "./ProfileDrawer.jsx";
import JobPage from "./JobPage.jsx";
import Panel from "./Panel.jsx";

// The time windows the server accepts, with the wording a person reads. Keys here and on
// the server have to match; tests/test_frontend_lists.py fails if they drift (HIR-203).
const WINDOWS = { open: "Currently open", "30d": "Last 30 days", "90d": "Last 90 days", all: "All" };
const DEFAULT = { cities: [], compare: false, seniorities: [], families: [], requirement: "required", window: "open", german: "any", degree: "any", production: "any", skillIds: [], query: "", text: "" };

// Where a request to add a city goes. There is no form for it, so it opens the repo's
// issue tracker, which is where every other request already lands.
const REQUEST_CITY_URL = "https://github.com/chandlershortlidge/hiring-radar/issues/new?title=City%20request";

// The market a returning visitor lands on: what the browser remembered, as long as that
// place is still one we collect.
function rememberedMarket() {
  const last = readLast();
  return last && placeBySlug(last.place) ? { ...HOME, view: "city", place: last.place, family: last.family } : HOME;
}

export default function App() {
  const [filters, setFilters] = useState(DEFAULT);
  const [stats, setStats] = useState(null);
  const [skills, setSkills] = useState(null);
  const [tax, setTax] = useState({ version: 0, skills: [] });
  const [related, setRelated] = useState(null);
  const [drawer, setDrawer] = useState(null); // 'add' | 'review' | 'profile'
  const [refresh, setRefresh] = useState(0);
  const [jumpTo, setJumpTo] = useState(null);
  const [profile, saveProfile] = useProfile();
  const [recent, setRecent] = useState(readRecent);

  // Two pieces of address-bar state (HIR-188). `route` is what the URL says right now;
  // `market` is the last city, comparison or home view it showed — so closing a job's own
  // page returns to the market you came from rather than to the home grid.
  const [route, setRoute] = useState(() => {
    const r = parsePath();
    if (r.view !== "home") return r;
    // A returning visitor goes straight to their last market. replaceState, not push: the
    // back button should leave the site, not bounce between "/" and the city.
    const m = rememberedMarket();
    if (m.view !== "home") window.history.replaceState(null, "", pathFor(m));
    return m;
  });
  const [market, setMarket] = useState(() => (route.view === "job" ? rememberedMarket() : route));
  const pageJob = route.view === "job" ? route.jobId : null;

  useEffect(() => {
    const onPop = () => { const r = parsePath(); setRoute(r); if (r.view !== "job") setMarket(r); };
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);

  // Going to a market is the one place the remembered city and the recent list are written.
  const goMarket = (r) => {
    window.history.pushState(null, "", pathFor(r));
    setRoute(r); setMarket(r);
    if (r.view === "city") { writeLast(r.place, r.family); setRecent(pushRecent(r.place)); }
    window.scrollTo(0, 0);
  };
  const openPage = (id) => { const r = { ...HOME, view: "job", jobId: id }; window.history.pushState(null, "", pathFor(r)); setRoute(r); window.scrollTo(0, 0); };
  const closePage = () => { window.history.pushState(null, "", pathFor(market)); setRoute(market); };

  // The address bar owns city, family and compare mode; the rest of the filters are the
  // controls' own state. Keeping it one-way — route in, filters out — means the back
  // button, a shared link and a picker click all land in exactly the same place.
  useEffect(() => {
    if (market.view === "job") return;
    setFilters((f) => ({
      ...f,
      cities: market.view === "city" ? placeCities(market.place) : [],
      compare: market.view === "compare",
      families: market.family ? [market.family] : [],
    }));
  }, [market]);
  const compareCities = market.view === "compare" ? market.cities : COMPARE_DEFAULT;
  // What the job-scoped consumers (the job list, the related-skills panel) filter by: in
  // compare mode the compared cities, otherwise `filters` untouched. `filters` itself keeps
  // cities empty in compare so the chart still covers every city in one request (HIR-196).
  const listFilters = useMemo(() => deriveListFilters(filters, compareCities), [filters, compareCities]);
  // Open jobs per city, for the picker's counts and the market cards. From /api/stats, so
  // it stays the whole picture even while the page is filtered down to one city.
  const cityCounts = stats?.open_by_city || {};

  const reload = useCallback(() => { api.stats().then(setStats); setRefresh((n) => n + 1); }, []);
  useEffect(() => { api.taxonomy().then(setTax); reload(); }, [reload]);
  // The answer is tagged with the family it was asked for, so the market cards never show a
  // new family's order over the previous family's numbers while a request is in flight.
  useEffect(() => { let live = true; api.skills(filters).then((r) => { if (live) setSkills({ ...r, family: filters.families[0] || null }); }); return () => { live = false; }; }, [filters, refresh]);
  // The related-skills rows, fetched here and not in the panel: the panel draws them and the
  // chip row's add-skill popover suggests them, both from this one request and in its order.
  useEffect(() => {
    if (!listFilters.skillIds.length) { setRelated(null); return; }
    let live = true;
    api.relatedSkills(listFilters).then((r) => { if (live) setRelated(r); });
    return () => { live = false; };
  }, [listFilters, refresh]);

  const taxName = useMemo(() => Object.fromEntries(tax.skills.map((s) => [s.id, s.display])), [tax]);
  // How many jobs ask for each skill, straight off the chart's own rows. It only orders the
  // missing-skill list in a job's fit badge — most asked for first — so the first name there
  // is the one worth learning next. Null until the chart's numbers arrive; the order is
  // deterministic either way (HIR-51).
  const demand = useMemo(() => (skills ? Object.fromEntries(skills.skills.map((s) => [s.skill_id, s.count])) : null), [skills]);
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
  const toggleSen = (s) => set({ seniorities: filters.seniorities.includes(s) ? filters.seniorities.filter((x) => x !== s) : [...filters.seniorities, s] });
  const viewJob = (id) => { setDrawer(null); if (pageJob) closePage(); set({ skillIds: [], query: "", text: "", window: "all" }); setJumpTo(id); };

  // Everything the query bar can do, as moves between addresses.
  const goPlace = (slug) => goMarket({ ...HOME, view: "city", place: slug, family: market.family });
  // On the home view a family pick is not a move: the address stays "/", nothing is pushed
  // to the history, and only the market cards follow it (HIR-197).
  const goFamily = (f) => {
    const next = withFamily(market, f);
    if (next.view === "home") { setRoute(next); setMarket(next); } else goMarket(next);
  };
  // Compare opens on the city you are looking at plus the one picked in the compare
  // dropdown, so it takes one pick to see two markets (HIR-191). The dropdown hides the
  // city you are already on, but "All of Germany" resolves to the busiest German city,
  // which today is the only one — so if the pick lands back on the city we are already
  // comparing, fall back to the busiest other market rather than comparing it with itself.
  const startCompare = (slug) => {
    const here = placeCities(market.place)[0];
    const picked = placeCities(slug)[0];
    const other = picked && picked !== here
      ? picked
      : PLACE_NAMES.filter((n) => n !== here).sort((a, b) => (cityCounts[b] || 0) - (cityCounts[a] || 0))[0];
    goMarket({ ...HOME, view: "compare", cities: [here, other].filter(Boolean), family: market.family });
  };
  const addCompare = (slug) => goMarket({ ...market, cities: compareAdd(market.cities, placeCities(slug)[0]) });
  // Down to one city there is nothing left to compare, so removing the second-to-last one
  // leaves compare mode with whichever city is still standing.
  const removeCompare = (name) => {
    const left = compareRemove(market.cities, name);
    goMarket(left.length >= 2
      ? { ...market, cities: left }
      : { ...HOME, view: "city", place: placeByName(left[0])?.slug || null, family: market.family });
  };
  const exitCompare = () => goMarket({ ...HOME, view: "city", place: placeByName(market.cities[0])?.slug || null, family: market.family });
  const requestCity = () => window.open(REQUEST_CITY_URL, "_blank", "noopener");

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

  const placeName = market.view === "city" ? (placeBySlug(market.place)?.name || "") : "";
  const cityLabel = filters.compare ? compareCities.join(" + ") : placeName || PLACE_NAMES.join(" + ");
  // What the chart's heading calls the roles: the chosen family, or every role we track.
  const roleLabel = market.family ? `${familyLabel(market.family)} jobs` : "AI-engineering jobs";
  const winLabel = filters.window === "open" ? "currently open" : filters.window === "all" ? "" : `from the last ${filters.window.replace("d", " days")}`;
  const reqLabel = filters.requirement === "required" ? "as required" : "as required or nice-to-have";
  // Family reads next to seniority in every subtitle: both describe the role, where the
  // rest of senLabel describes what the posting demands.
  const famLabel = filters.families.length ? ` · ${filters.families.map(familyLabel).join(" + ")}` : "";
  const senLabel = (filters.seniorities.length ? ` · ${filters.seniorities.map(cap).join("/")} roles` : "")
    + (filters.german !== "any" ? ` · German: ${GERMAN_FILTERS[filters.german].toLowerCase()}` : "")
    + (filters.production !== "any" ? ` · production experience: ${PRODUCTION_FILTERS[filters.production].toLowerCase()}` : "")
    + (filters.degree !== "any" ? ` · degree: ${DEGREE_FILTERS[filters.degree].toLowerCase()}` : "");

  return (
    <>
      <header className="hdr"><div className="hdr-in">
        <div className="brand"><a href="/" onClick={(e) => { e.preventDefault(); goMarket(HOME); }} className="home" aria-label="hiring-radar home"><Radar /><b>hiring-radar</b></a><span className="sub" title={PLACE_NAMES.join(" · ")}>Skills employers ask for, across {PLACE_NAMES.length} markets</span></div>
        <div className="hdr-actions">
          {market.view !== "home" && <a className="pill" href="/" onClick={(e) => { e.preventDefault(); goMarket(HOME); }}>All markets</a>}
          <button type="button" className={`pill${profile ? " on" : ""}`} onClick={() => setDrawer("profile")} aria-label="Your profile">
            <Person /><span className="lbl">{profile ? `${profile.skills.length} skills in your profile` : "Set up your profile"}</span>
          </button>
          <button type="button" className="pill" onClick={() => setDrawer("review")} aria-label={`${stats?.proposed_pending ?? 0} proposed skills to review`}>
            <span className="count">{stats?.proposed_pending ?? 0}</span><span className="lbl">proposed skills</span>
          </button>
          <button type="button" className="btn outline" onClick={() => setDrawer("add")} aria-label="Add a job"><Plus /><span className="lbl">Add a job</span></button>
        </div>
      </div></header>

      {pageJob ? <Panel label="This job's page"><JobPage id={pageJob} onBack={closePage} profile={profile} taxonomy={taxName} demand={demand} /></Panel> : <>

      {market.view === "home" && (
        <section className="hero landing"><div className="hero-in">
          <h1>What are employers actually asking for?</h1>
          <p className="lede">Live skill demand from every open AI &amp; data job we can find, per city.</p>
        </div></section>
      )}

      <QueryBar
        place={market.view === "city" ? market.place : null}
        family={market.family}
        counts={cityCounts}
        recent={recent}
        compare={market.view === "compare"}
        compareCities={market.view === "compare" ? market.cities : []}
        landing={market.view === "home"}
        onPlace={goPlace} onFamily={goFamily}
        onStartCompare={startCompare} onAddCity={addCompare} onRemoveCity={removeCompare} onExitCompare={exitCompare}
        onRequestCity={requestCity}
        right={stats && market.view !== "home"
          ? <span className="mono dim">{stats.open} open jobs · updated {timeAgo(stats.last_updated)}</span>
          : null} />

      {market.view === "home" ? <main className="main landing">
        {recent.length > 0 && (
          <p className="recents"><span className="dim">Recent:</span>
            {recent.map(placeBySlug).filter(Boolean).map((p) => (
              <a key={p.slug} className="pill" href={market.family ? `/${p.slug}/${market.family}` : `/${p.slug}`}
                onClick={(e) => { e.preventDefault(); goPlace(p.slug); }}>{p.name}</a>
            ))}
          </p>
        )}
        <Panel label="The market grid"><HomeGrid data={skills} counts={cityCounts} family={market.family} onRequestCity={requestCity} /></Panel>
      </main> : <main className="main">
        {stats && (
          <p className="stats">
            <span>{stats.jobs} jobs</span><span>·</span>
            <span><abbr title={`A feed-sourced job counts as open while a feed still listed it in the last ${stats.open_rule.feed_days} days. A job added by hand is assumed open for ${stats.open_rule.manual_days} days.`}>{stats.open} currently open</abbr>
              {Object.keys(stats.open_by_city).length > 1 && ` (${Object.entries(stats.open_by_city).map(([c, n]) => `${c} ${n}`).join(" · ")})`}</span><span>·</span>
            <span>{stats.companies} companies</span><span>·</span>
            <span>{stats.skills_tracked} skills tracked</span><span>·</span>
            {stats.open > 0 && <><span>of those open now:</span><span>·</span>
            <span><abbr title="Open jobs that ask for German outright or are written in German">{stats.open_german_required} need German</abbr></span><span>·</span>
            <span><abbr title="Open jobs that name a degree, don't mark it optional, and don't accept equivalent experience">{stats.open_degree_required} need a degree</abbr></span><span>·</span>
            <span><abbr title="Open jobs that ask the candidate for prior experience shipping or operating software real users depended on">{stats.open_production_required} need production experience</abbr></span><span>·</span></>}
            {stats.legacy > 0 && <><span><abbr title="Imported from the old project with the old extractor's skills; listed but not counted in the chart">{stats.legacy} legacy, not charted</abbr></span><span>·</span></>}
            {stats.too_short > 0 && <><span><abbr title="Only a fragment of the posting was stored; listed but not counted in the chart">{stats.too_short} too short, not charted</abbr></span><span>·</span></>}
            <span>{stats.last_updated ? `last updated ${timeAgo(stats.last_updated)} (${dateTime(stats.last_updated)})` : "no jobs yet"}</span>
          </p>
        )}

        <Panel label="The chart"><section className="card chart" aria-labelledby="chart-title">
          <div>
            <h1 id="chart-title">{filters.compare
              ? `${compareCities.join(" vs ")} · ${market.family ? familyLabel(market.family) : "AI & data roles"}`
              : `What skills are ${roleLabel}${placeName ? ` in ${placeName}` : ""} asking for?`}</h1>
            <p className="lede">
              {filters.compare ? `Share of each city's ${winLabel || "tracked"} jobs listing the skill ${reqLabel}. Rows sorted by the column you pick`
                : `Share of the ${skills?.total ?? "…"} ${winLabel} jobs that list each skill ${reqLabel} · ${cityLabel}`}{famLabel}{senLabel}.
              {profile && " Solid bars are skills in your profile."}
            </p>
          </div>
          <div className="controls">
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
            ? <CompareChart data={skills} selected={filters.skillIds} onSelect={selectSkill} cities={compareCities}
                onSelectCity={(id, city) => { set({ skillIds: [id] }); goMarket({ ...HOME, view: "city", place: placeByName(city)?.slug || null, family: market.family }); }} />
            : <SkillChart data={skills} selected={filters.skillIds} onSelect={selectSkill} profile={profile}
                cityLabel={`${winLabel || "tracked"} jobs`} aliases={taxAliases} />}
        </section></Panel>

        <Panel label="Related skills"><RelatedSkills filters={listFilters} skillNames={skillNames} onAdd={addSkill} data={related} /></Panel>

        <Panel label="The job list"><JobList filters={listFilters} setFilters={setFilters}
          profile={profile} taxonomy={taxName} demand={demand} refreshKey={refresh} openJobId={jumpTo} onOpened={() => setJumpTo(null)} onOpenPage={openPage}
          taxonomyRows={taxRows} aliases={taxAliases} suggestions={skillSuggestions} onAddSkill={addSkill} /></Panel>

        {/* The skill tree card stood here. Off the MVP page by HIR-187; SkillTree.jsx, api.skillTree
            and /api/skills/tree all still work, and HIR-81 / HIR-89 bring it back per career track. */}
      </main>}</>}

      {drawer === "add" && <Panel label="The add-a-job drawer"><AddJobDrawer onClose={() => setDrawer(null)} onAdded={reload} onViewJob={viewJob} /></Panel>}
      {drawer === "review" && <Panel label="The proposed-skills drawer"><ReviewDrawer onClose={() => setDrawer(null)} taxonomyList={tax.skills} skillsTracked={stats?.skills_tracked ?? tax.skills.length} onChanged={reload} onViewJob={viewJob} /></Panel>}
      {drawer === "profile" && <Panel label="The profile drawer"><ProfileDrawer onClose={() => setDrawer(null)} profile={profile} save={saveProfile} taxonomyList={tax.skills} /></Panel>}
    </>
  );
}
