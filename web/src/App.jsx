import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api, fetchSkills } from "./api.js";
import { COMPARE_DEFAULT, DEGREE_FILTERS, EXTRA_FILTER_NAMES, GERMAN_FILTERS, PLACE_NAMES, PRODUCTION_FILTERS, cap, compareAdd, compareRemove, familyLabel, listFilters as deriveListFilters, placeByName, placeBySlug, placeCities, pctInt, timeAgo } from "./format.js";
import { HOME, parsePath, pathFor, withFamily } from "./routes.js";
import { pushRecent, readLast, readRecent, writeLast } from "./lastPlace.js";
import { useProfile } from "./profile.js";
import { Person, Radar } from "./icons.jsx";
import QueryBar from "./QueryBar.jsx";
import HomeGrid from "./HomeGrid.jsx";
import { HeroChart, Tagline, heroFacts, heroPlace } from "./HomeHero.jsx";
import { ConnectPill, ConnectStrip } from "./ConnectClaude.jsx";
import FilterPills from "./FilterPills.jsx";
import SkillChart, { ChartStatus } from "./SkillChart.jsx";
import CompareChart from "./CompareChart.jsx";
import CityFit from "./CityFit.jsx";
import JobList from "./JobList.jsx";
import RelatedSkills from "./RelatedSkills.jsx";
import RisingSkills from "./RisingSkills.jsx";
import ProfileDrawer from "./ProfileDrawer.jsx";
import JobPage from "./JobPage.jsx";
import Panel from "./Panel.jsx";

// The time windows the server accepts, with the wording a person reads. Keys here and on
// the server have to match; tests/test_frontend_lists.py fails if they drift (HIR-203).
const WINDOWS = { open: "Currently open", "30d": "Last 30 days", "90d": "Last 90 days", all: "All" };
const REQUIREMENTS = { required: "Required only", all: "Required + nice-to-have" };
// Every key here is recorded by a "doesn't belong here" flag and must be known to its
// diagnosis (app/flags.py VIEW_FILTERS); tests/test_flags.py fails when one is not (HIR-226).
export const DEFAULT = { cities: [], compare: false, seniorities: [], families: [], requirement: "required", window: "open", german: "any", degree: "any", production: "any", skillIds: [], query: "", text: "" };

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
  const [skillsFailed, setSkillsFailed] = useState(false);
  const [tax, setTax] = useState({ version: 0, skills: [] });
  const [related, setRelated] = useState(null);
  const [drawer, setDrawer] = useState(null); // 'profile'
  const [refresh, setRefresh] = useState(0);
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
  // The home page leads with one market: its chart and the city its pickers start on
  // (HomeHero.jsx). Fixed while the page is open, so visiting a city and coming back does
  // not change the chart under the reader.
  const [lead] = useState(() => heroPlace(recent));
  const hero = useMemo(() => heroFacts(skills, cityCounts, lead), [skills, cityCounts, lead]);
  // The city picked in the home page's search box (HIR-474): a choice, not a move, until
  // "View jobs" is pressed. Until then the box shows the market the page leads with.
  const [heroPick, setHeroPick] = useState(null);
  const heroSlug = heroPick || lead.slug;
  // Set by "View jobs", read once the city page has drawn: the visitor asked for the jobs,
  // so the page opens on the job list rather than at its top. Where the columns stack (a
  // phone) the chart above the list is still loading and pushes it down, so the list is
  // held in place while the page settles, until the visitor scrolls or touches it.
  const toJobs = useRef(false);
  useEffect(() => {
    if (!toJobs.current || market.view !== "city") return;
    toJobs.current = false;
    const jobs = document.querySelector(".card.jobs");
    const main = document.querySelector("main.main");
    if (!jobs || !main) return;
    const pin = () => jobs.scrollIntoView({ block: "start" });
    pin();
    const ro = typeof ResizeObserver === "function" ? new ResizeObserver(pin) : null;
    ro?.observe(main);
    const stop = () => { ro?.disconnect(); clearTimeout(t); for (const e of ["wheel", "touchstart", "keydown"]) window.removeEventListener(e, stop); };
    const t = setTimeout(stop, 4000);
    for (const e of ["wheel", "touchstart", "keydown"]) window.addEventListener(e, stop, { passive: true });
    return stop;
  }, [market]);
  // The filters "More filters" holds, and how many of them are set to something.
  const extraOn = [filters.production, filters.degree].filter((v) => v !== "any").length + (filters.window !== "open" ? 1 : 0);

  const reload = useCallback(() => { api.stats().then(setStats); setRefresh((n) => n + 1); }, []);
  useEffect(() => { api.taxonomy().then(setTax); reload(); }, [reload]);
  // The answer is tagged with the family it was asked for, so the market cards never show a
  // new family's order over the previous family's numbers while a request is in flight.
  // A request that fails clears the old numbers and is remembered (HIR-318), so the chart
  // says it could not load; before, a failure left "No jobs match" on screen for good.
  useEffect(() => {
    let live = true;
    setSkillsFailed(false);
    fetchSkills(filters).then((r) => { if (live) { setSkills(r.data); setSkillsFailed(r.failed); } });
    return () => { live = false; };
  }, [filters, refresh]);
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

  // Everything the query bar can do, as moves between addresses.
  const goPlace = (slug) => goMarket({ ...HOME, view: "city", place: slug, family: market.family });
  const viewJobs = () => { toJobs.current = true; goPlace(heroSlug); };
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
    // On the home page no city is opened yet; the one picked in the search box stands in.
    const here = placeCities(market.place || heroSlug)[0];
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

  // The "[job family] in [city]" pickers. On the home page they sit under the headline in a
  // search box, start on the market the page leads with, and open nothing until "View jobs".
  const queryBar = (
    <QueryBar
      place={market.view === "city" ? market.place : market.view === "home" ? heroSlug : null}
      family={market.family}
      counts={cityCounts}
      recent={recent}
      compare={market.view === "compare"}
      compareCities={market.view === "compare" ? market.cities : []}
      landing={market.view === "home"}
      onPlace={market.view === "home" ? setHeroPick : goPlace} onFamily={goFamily} onViewJobs={viewJobs}
      onStartCompare={startCompare} onAddCity={addCompare} onRemoveCity={removeCompare} onExitCompare={exitCompare}
      onRequestCity={requestCity}
      right={stats && market.view !== "home"
        ? <span className="mono dim">updated {timeAgo(stats.last_updated)}</span>
        : null} />
  );

  return (
    <>
      <header className="hdr"><div className="hdr-in">
        <div className="brand"><a href="/" onClick={(e) => { e.preventDefault(); goMarket(HOME); }} className="home" aria-label="hiring-radar home"><Radar /><b>hiring-radar</b></a><span className="sub" title={PLACE_NAMES.join(" · ")}>Skills employers ask for, across {PLACE_NAMES.length} markets</span></div>
        <div className="hdr-actions">
          {market.view !== "home" && <a className="pill" href="/" onClick={(e) => { e.preventDefault(); goMarket(HOME); }}>All markets</a>}
          <button type="button" className={`pill${profile ? " on" : ""}`} onClick={() => setDrawer("profile")} aria-label="Your profile">
            <Person /><span className="lbl">{profile ? `${profile.skills.length} skills in your profile` : "Set up your profile"}</span>
          </button>
          {/* Not a button: there is nothing to connect to yet (ConnectClaude.jsx). */}
          <ConnectPill />
        </div>
      </div><div className="brand-rule" aria-hidden="true" /></header>

      {pageJob ? <Panel label="This job's page"><JobPage id={pageJob} onBack={closePage} profile={profile} taxonomy={taxName} demand={demand} /></Panel> : <>

      {/* Home (HIR-285, HIR-474): the tagline and the search box on the left, the lead
          market's chart on the right. On a city page the same pickers are a band of their own. */}
      {market.view === "home" ? (
        <>
          <section className="hero"><div className="hero-in">
            <div className="hero-l">
              <Tagline />
              {queryBar}
            </div>
            <Panel label="The top-skills chart">
              <HeroChart place={lead} family={market.family} top={hero.top} open={hero.open} loading={!skills && !skillsFailed} onOpen={goPlace} />
            </Panel>
          </div></section>
          <div className="mcp-wrap"><ConnectStrip /></div>
        </>
      ) : queryBar}

      {market.view === "home" ? <main className="main landing">
        {recent.length > 0 && (
          <p className="recents"><span className="dim">Recent:</span>
            {recent.map(placeBySlug).filter(Boolean).map((p) => (
              <a key={p.slug} className="pill" href={market.family ? `/${p.slug}/${market.family}` : `/${p.slug}`}
                onClick={(e) => { e.preventDefault(); goPlace(p.slug); }}>{p.name}</a>
            ))}
          </p>
        )}
        <Panel label="The market grid"><HomeGrid data={skills} counts={cityCounts} family={market.family} onRequestCity={requestCity} loading={!stats || (!skills && !skillsFailed)} /></Panel>
      </main> : <main className={`main${market.view === "city" ? " split" : ""}`}>
        {/* A city page is two columns (HIR-285): the chart, and what hangs off it, on the
            left; the jobs on the right, so a click on a bar filters a list already in
            view. The left column stays in view while the jobs scroll (HIR-345); the
            stylesheet does that, and puts "What's rising" back under the chart where the
            columns stack, below 1100px. A comparison keeps one column: its chart needs
            the width for a column per city. */}
        <div className="stack lead">
        <Panel label="The chart"><section className="card chart" aria-labelledby="chart-title">
          <div>
            <h1 id="chart-title">{filters.compare
              ? `${compareCities.join(" vs ")} · ${market.family ? familyLabel(market.family) : "AI & data roles"}`
              : `What skills are ${roleLabel}${placeName ? ` in ${placeName}` : ""} asking for?`}</h1>
            <p className="lede">
              {filters.compare ? `Share of each city's ${winLabel || "tracked"} jobs listing the skill ${reqLabel}. Rows sorted by the column you pick`
                : `Share of the ${skills?.total ?? "…"} ${winLabel} jobs that list each skill ${reqLabel} · ${cityLabel}`}{famLabel}{senLabel}.
              {profile && " Dark bars are skills in your profile."}
            </p>
          </div>
          <FilterPills filters={filters} set={set} toggleSeniority={toggleSen} requiredLabel={REQUIREMENTS.required} extraOn={extraOn}>
            <div className="ctl"><label htmlFor="prod">{EXTRA_FILTER_NAMES.production}</label>
              <select id="prod" className="sel" value={filters.production} onChange={(e) => set({ production: e.target.value })}>
                {Object.entries(PRODUCTION_FILTERS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
            <div className="ctl"><label htmlFor="deg">{EXTRA_FILTER_NAMES.degree}</label>
              <select id="deg" className="sel" value={filters.degree} onChange={(e) => set({ degree: e.target.value })}>
                {Object.entries(DEGREE_FILTERS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
            <div className="ctl"><label htmlFor="win">{EXTRA_FILTER_NAMES.window}</label>
              <select id="win" className="sel" value={filters.window} onChange={(e) => set({ window: e.target.value })}>
                {Object.entries(WINDOWS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
          </FilterPills>
          {/* No numbers yet is not "no jobs": both charts read missing numbers as zero jobs,
              so neither is drawn until the answer is in (HIR-318). */}
          {/* Where the visitor's skills are wanted, city by city (HIR-16). Draws nothing
              without skills in the profile. */}
          {filters.compare && <CityFit profile={profile} filters={filters} cities={compareCities} refreshKey={refresh} />}
          {!skills ? <ChartStatus failed={skillsFailed} onRetry={reload} />
            : filters.compare
            ? <CompareChart data={skills} selected={filters.skillIds} onSelect={selectSkill} cities={compareCities}
                onSelectCity={(id, city) => { set({ skillIds: [id] }); goMarket({ ...HOME, view: "city", place: placeByName(city)?.slug || null, family: market.family }); }} />
            : <SkillChart data={skills} selected={filters.skillIds} onSelect={selectSkill} profile={profile}
                cityLabel={`${winLabel || "tracked"} jobs`} aliases={taxAliases}
                gaps={market.view === "city" && !!placeName} />}
        </section></Panel>

        <Panel label="Related skills"><RelatedSkills filters={listFilters} skillNames={skillNames} onAdd={addSkill} data={related} /></Panel>
        </div>

        <div className="stack side">
        <Panel label="The job list"><JobList filters={listFilters} setFilters={setFilters} connect={market.view === "city"}
          defaults={DEFAULT} windows={WINDOWS} requirements={REQUIREMENTS}
          profile={profile} taxonomy={taxName} demand={demand} refreshKey={refresh} onOpenPage={openPage}
          taxonomyRows={taxRows} aliases={taxAliases} suggestions={skillSuggestions} onAddSkill={addSkill} market={market} /></Panel>

        {/* One place at a time: a comparison of cities has no single market to follow.
            Under the jobs, in their column: in the left column it made the part that
            stays in view taller than a laptop screen (HIR-345). */}
        {market.view === "city" && (
          <div className="below"><Panel label="What's rising"><RisingSkills cities={placeCities(market.place)} family={market.family}
            place={placeName || "this market"} role={roleLabel} refreshKey={refresh} /></Panel></div>
        )}
        </div>

        {/* The skill tree card stood here. Off the MVP page by HIR-187; SkillTree.jsx, api.skillTree
            and /api/skills/tree all still work, and HIR-81 / HIR-89 bring it back per career track. */}
      </main>}</>}

      {drawer === "profile" && <Panel label="The profile drawer"><ProfileDrawer onClose={() => setDrawer(null)} profile={profile} save={saveProfile} taxonomyList={tax.skills} /></Panel>}
    </>
  );
}
