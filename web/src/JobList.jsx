import { useEffect, useMemo, useState } from "react";
import { api } from "./api.js";
import { Down, Ext, Repost, Search, Star, Up, X } from "./icons.jsx";
import { cap, dateShort, degreeLine, familyLabel, germanLine, productionLine, sourceCode, timeAgo } from "./format.js";
import { fails, fit, gates, jobSeniority, metSkills, rankJobs, skillSides } from "./profile.js";
import { copyLines, sortJobs, useSaved } from "./saved.js";
import AddSkillChip from "./AddSkillChip.jsx";

const SORTS = { newest: "Newest first", oldest: "Oldest first", reposts: "Most reposted", company: "Company A–Z" };
const FIT = "fit";                   // best fit first; only offered once a profile exists
const PAGE = 20;
// "Best fit" is the one sort the server cannot do: it never learns the profile (HIR-51).
// So that sort asks for the whole filtered set in one request, ranks it here, and pages
// through the result locally. FIT_MAX is the largest page /api/jobs will serve, and the
// honest limit of the trick: past it the ranking only covers the newest FIT_MAX jobs, so
// the foot says so rather than quietly ranking a slice.
const FIT_MAX = 200;

export default function JobList({ filters, setFilters, profile, taxonomy, demand = null, refreshKey, openJobId, onOpened, onOpenPage,
  taxonomyRows = [], aliases = {}, suggestions = [], onAddSkill }) {
  // Best fit is the default for someone who has a profile: it is why they made one. The
  // profile loads synchronously, so this is right on the first render, not after a flash.
  const [sort, setSort] = useState(() => (profile ? FIT : "newest"));
  const [page, setPage] = useState({ jobs: [], total: 0 });
  const [shown, setShown] = useState(PAGE);   // only "Best fit" pages locally; see FIT_MAX
  const [open, setOpen] = useState(null);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState(filters.query);
  // The posting-text search (HIR-67) had a second box here, next to this one. It is off the
  // MVP page (HIR-187): two unexplained search boxes side by side, and the pair is what made
  // the toolbar wrap to two rows. `filters.text` still exists and `/api/jobs` still accepts
  // it — it is simply always "" from the UI until an advanced-filters drawer offers it again.
  // Saved jobs (HIR-99): ids live only in this browser. The Saved view fetches each saved
  // job by its id — the one request no filter touches — so a job that has since closed, or
  // left the current window, still shows with its status instead of silently vanishing.
  const [savedIds, toggleSaved] = useSaved();
  const [savedOn, setSavedOn] = useState(false);
  const [savedJobs, setSavedJobs] = useState(null);   // null until the first fetch answers
  const [copied, setCopied] = useState(false);

  useEffect(() => { const t = setTimeout(() => setFilters((f) => ({ ...f, query: q })), 250); return () => clearTimeout(t); }, [q, setFilters]);

  // Clearing the profile has to take its sort with it, or the list would sit on an
  // ordering there is nothing left to compute.
  const byFit = sort === FIT && Boolean(profile);
  useEffect(() => { if (sort === FIT && !profile) setSort("newest"); }, [sort, profile]);

  useEffect(() => {
    let live = true;
    setLoading(true);
    setShown(PAGE);
    api.jobs(filters, { sort: byFit ? "newest" : sort, limit: byFit ? FIT_MAX : PAGE, offset: 0 })
      .then((r) => { if (live) { setPage(r); setLoading(false); } });
    return () => { live = false; };
  }, [filters, sort, byFit, refreshKey]);

  useEffect(() => { if (openJobId) { setOpen(openJobId); onOpened?.(); } }, [openJobId, onOpened]);

  // A saved id whose job the server no longer has (deleted by hand) is dropped from the
  // view rather than crashing it; un-starring filters below without waiting for a refetch.
  useEffect(() => {
    if (!savedOn) return;
    let live = true;
    Promise.all(savedIds.map((id) => api.job(id).catch(() => null)))
      .then((js) => { if (live) setSavedJobs(js.filter(Boolean)); });
    return () => { live = false; };
  }, [savedOn, savedIds, refreshKey]);

  // Ranked once per fetch, not once per row: every row's badge reads its own fit, but the
  // order is one pass over the set. Ties keep the server's newest-first order.
  const ordered = useMemo(() => (byFit ? rankJobs(profile, page.jobs, demand) : page.jobs), [byFit, profile, page.jobs, demand]);
  // The Saved view sorts locally (saved.js mirrors the server's sorts) because the ids
  // never leave the browser; the whole set is in hand, so there is nothing to page.
  const savedRows = useMemo(
    () => sortJobs((savedJobs || []).filter((j) => savedIds.includes(j.id)), byFit ? "fit" : sort, profile, demand),
    [savedJobs, savedIds, sort, byFit, profile, demand],
  );
  const rows = savedOn ? savedRows : byFit ? ordered.slice(0, shown) : ordered;
  const more = byFit
    ? () => setShown((n) => n + PAGE)
    : () => api.jobs(filters, { sort, limit: PAGE, offset: page.jobs.length })
      .then((r) => setPage((p) => ({ ...r, jobs: [...p.jobs, ...r.jobs] })));
  const left = byFit ? Math.min(ordered.length, page.total) - rows.length : page.total - rows.length;

  // The cities in the filter name the list's scope in every mode — compare mode passes the
  // compared cities in (HIR-196), so there is no compare special case here.
  const scope = filters.cities.length ? filters.cities.join(" + ") : "all cities";
  return (
    <section className="card jobs" aria-labelledby="jobs-title">
      <div className="jobs-head">
        <div className="l">
          <h2 id="jobs-title">Jobs</h2>
          <button type="button" className={`pill saved-toggle${savedOn ? " on" : ""}`} aria-pressed={savedOn}
            onClick={() => setSavedOn((v) => !v)} title="Only the jobs you starred. Saved jobs live in this browser; the server never sees them.">
            <Star />Saved · {savedIds.length}
          </button>
          {!savedOn && filters.skillIds.length > 0 && <span className="muted" style={{ fontSize: 12.5 }}>Requires</span>}
          {savedOn && <span className="muted" style={{ fontSize: 13 }}>in the current sort · a saved job that closed stays listed</span>}
          {!savedOn && <>
            {filters.skillIds.map((id) => (
              <span key={id} className="chip-filter">{taxonomy[id] || id}
                <button type="button" aria-label={`Remove ${taxonomy[id] || id} from the skill filter`}
                  onClick={() => setFilters((f) => ({ ...f, skillIds: f.skillIds.filter((x) => x !== id) }))}><X size={12} /></button>
              </span>
            ))}
            <AddSkillChip selected={filters.skillIds} suggestions={suggestions} taxonomy={taxonomyRows}
              aliases={aliases} onAdd={onAddSkill} />
            <span className="muted jobs-count">{page.total} {filters.window === "open" ? "open" : ""} jobs · {scope}</span>
          </>}
        </div>
        <div className="r">
          {savedOn ? (
            <button type="button" className="btn" disabled={!rows.length}
              title="Puts one “company — title — link” line per saved job on the clipboard"
              onClick={() => navigator.clipboard.writeText(copyLines(rows)).then(() => { setCopied(true); setTimeout(() => setCopied(false), 1500); }).catch(() => {})}>
              {copied ? "Copied" : "Copy as list"}
            </button>
          ) : (<>
            <label htmlFor="q" className="sr">Search company or title</label>
            <div className="search"><Search stroke="#6B6B6B" /><input id="q" type="search" className="inp" placeholder="Search company or title" value={q} onChange={(e) => setQ(e.target.value)} /></div>
          </>)}
          <label htmlFor="sort" className="muted" style={{ fontSize: 12.5 }}>Sort</label>
          <select id="sort" className="sel" value={sort} onChange={(e) => setSort(e.target.value)}>
            {profile && <option value={FIT}>Best fit</option>}
            {Object.entries(SORTS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </div>
      </div>
      <div className="tbl"><div className="tbl-in">
        <div className="row-head"><span>Company</span><span>Title</span><span>City</span><span>First seen</span><span>Status</span><span>Sources</span><span /></div>
        {rows.map((j) => (
          <Row key={j.id} job={j} open={open === j.id} onToggle={() => setOpen(open === j.id ? null : j.id)}
            profile={profile} taxonomy={taxonomy} demand={demand} onOpenPage={onOpenPage}
            saved={savedIds.includes(j.id)} onSave={() => toggleSaved(j.id)} />
        ))}
        {savedOn && !savedJobs && savedIds.length > 0 && <div className="empty">Loading your saved jobs…</div>}
        {savedOn && !rows.length && (savedJobs || !savedIds.length) && <div className="empty">Nothing saved yet. Star a job to keep it here.</div>}
        {/* The "no posting contains those words" variant of this message went with the
            posting-text box (HIR-187): nothing in the UI can set `filters.text` any more. */}
        {!savedOn && !loading && !page.jobs.length && <div className="empty">No jobs match. Widen the time window or clear the skill filter.</div>}
      </div></div>
      <div className="jobs-foot">
        {!savedOn && left > 0 && <button type="button" className="btn" onClick={more}>Load {Math.min(PAGE, left)} more</button>}
        <span>{savedOn ? `Showing all ${rows.length} saved` : `Showing ${rows.length} of ${page.total}`}</span>
        {!savedOn && byFit && page.total > FIT_MAX && <span className="dim">Best fit ranks the {FIT_MAX} newest of them.</span>}
      </div>
    </section>
  );
}

function Row({ job: j, open, onToggle, profile, taxonomy, demand, onOpenPage, saved, onSave }) {
  const [detail, setDetail] = useState(null);
  useEffect(() => { if (open && !detail) api.job(j.id).then(setDetail); }, [open, detail, j.id]);
  const cov = profile ? fit(profile, j, demand) : null;
  const miss = gates(profile, j);
  return (
    <>
      <div className={`row${open ? " open-row" : ""}${j.legacy || j.too_short ? " legacy" : ""}${cov?.gated_by ? " gated" : ""}`} onClick={onToggle} role="button" tabIndex={0} aria-expanded={open}
        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onToggle(); } }}>
        <span className="co">
          <button type="button" className={`star${saved ? " on" : ""}`} aria-pressed={saved}
            aria-label={saved ? `Remove ${j.company} — ${j.title} from saved` : `Save ${j.company} — ${j.title}`}
            title={saved ? "Saved — click to remove" : "Save this job (stays in this browser)"}
            onClick={(e) => { e.stopPropagation(); onSave(); }} onKeyDown={(e) => e.stopPropagation()}>
            <Star />
          </button>
          {j.company}{j.legacy && <span className="src" style={{ marginLeft: 6 }} title="Imported from the old project with its skills; not in the chart">legacy</span>}{j.too_short && <span className="src" style={{ marginLeft: 6 }} title="Only a fragment of the posting was stored; not in the chart">short</span>}</span>
        <span className="ti">
          {miss.length > 0 && <span className="fit miss" title={miss.map((w) => MISS_LABELS[w]).join(" · ")}>!</span>}
          {cov?.gated_by && <span className="fit gate" title={MISS_LABELS[cov.gated_by]}>{gateWord(cov.gated_by, j)}</span>}
          {cov && cov.score !== null && <span className={`fit${cov.score === 1 && !cov.thin ? " full" : ""}`} title={fitTitle(cov, taxonomy)}>{fitBadge(cov)}</span>}
          {j.title}{j.seniority && <span className="dim" style={{ marginLeft: 8, fontSize: 12 }}>{cap(j.seniority)}</span>}{j.family && <span className="dim" style={{ marginLeft: 8, fontSize: 12 }} title="Job family, from the title">{familyLabel(j.family)}</span>}
        </span>
        <span className="ci muted" title={placeLabel(j).title}>{placeLabel(j).text}</span>
        <span className="fs muted" style={{ fontSize: 13 }}>{timeAgo(j.first_seen)}</span>
        <span className="st">
          <span className={`status ${j.status}`}><i />{cap(j.status)}</span>
          {j.repost_count > 0 && <span className="repost" title={`Reposted ${j.repost_count}×`}><Repost />×{j.repost_count}</span>}
        </span>
        <span className="srcs">{j.sources.map((s, i) => { const [code, full] = sourceCode(s.source); return <span key={i} className="src" title={full} aria-label={full}>{code}</span>; })}</span>
        <span className="meta-m muted">{placeLabel(j).text} ·{timeAgo(j.first_seen)} · {cap(j.status)}{j.repost_count > 0 ? ` · reposted ×${j.repost_count}` : ""} · {j.sources.map((s) => sourceCode(s.source)[0]).join(" ")}</span>
        <button type="button" className="exp" aria-label={`${open ? "Hide" : "Show"} skills for ${j.company}`} onClick={(e) => { e.stopPropagation(); onToggle(); }}>{open ? <Up /> : <Down />}</button>
      </div>
      {open && <Detail job={j} d={detail} profile={profile} taxonomy={taxonomy} cov={cov} onOpenPage={onOpenPage} />}
    </>
  );
}

// "miss" when the profile says the person does not meet a hard ask; "ok" otherwise. The
// judgment itself lives in profile.js, so the row, the ranking and the attribute lines in
// the detail below all read the same rule.
const flag = (profile, what, j) => (!profile ? "" : fails(profile, j, what) ? "miss" : "ok");

// How the row's "!" tooltip names each hard ask the profile fails.
const MISS_LABELS = {
  german: "needs German",
  production: "needs production experience you don't claim",
  degree: "needs a degree you don't list",
  seniority: "wants a level you are not targeting",
};

// The one word the badge uses for a gated-out row. Seniority says which level, because
// "senior" is the useful word there and "seniority" is not — and it asks profile.js for
// that level rather than reading the row, so a job gated on its title alone still names
// one instead of showing a blank (HIR-113).
const GATE_WORDS = { german: "German", production: "production", degree: "degree" };
const gateWord = (gate, j) => (gate === "seniority" ? jobSeniority(j) : GATE_WORDS[gate]);

const pct = (score) => Math.round(score * 100);

// What a job below the floor says instead of a percentage, in the badge and in the two
// sentences below. A posting naming two required skills has told us too little for a
// percentage to mean anything, so the row shows the count and says why (HIR-154).
const FEW_SKILLS = "few skills listed";

// The badge: a percentage and the count, except on a thinly listed job, where the
// percentage is exactly the misleading part and the count stands alone.
// A job posted for several cities (HIR-289) shows its first one and how many more; the
// tooltip names them all. Older API responses carry only `city`.
export function placeLabel(j) {
  const places = j.places && j.places.length ? j.places : (j.city ? [j.city] : []);
  if (!places.length) return { text: "—", title: undefined };
  return { text: places.length > 1 ? `${places[0]} +${places.length - 1}` : places[0], title: places.join(", ") };
}

export function fitBadge(cov) {
  if (cov.thin) return `${cov.covered}/${cov.total} · ${FEW_SKILLS}`;
  return `${pct(cov.score)}% · ${cov.covered}/${cov.total}`;
}

// The missing requirements as words. A group of alternatives is one requirement, so it is
// named as one: "Python, Rust, Go or Java" (HIR-251). Requirements stay comma-separated, so
// a group is set off in parentheses when more than one requirement is listed.
export function missingNames(missing, taxonomy) {
  const name = (id) => taxonomy[id] || id;
  const unit = (u) => {
    if (!Array.isArray(u)) return name(u);
    const names = u.map(name);
    const words = `${names.slice(0, -1).join(", ")} or ${names[names.length - 1]}`;
    return missing.length > 1 ? `(${words})` : words;
  };
  return missing.map(unit).join(", ");
}

// The gap, in the badge's tooltip: the required skills the profile lacks, most-asked-for
// first, so the first name in the list is the one worth learning next. "A full match" is
// only ever said of a job that listed a normal number of asks; covering both asks of a
// two-ask posting is not a match, it is a posting we know little about.
export function fitTitle(cov, taxonomy) {
  const head = `You cover ${cov.covered} of ${cov.total} required skills`;
  if (cov.missing.length) return `${head}. Missing, most asked for first: ${missingNames(cov.missing, taxonomy)}`;
  if (cov.thin) return `${head} — but ${FEW_SKILLS}, so this is not a full match`;
  return `${head} — a full match`;
}

// Also rendered by JobPage, which passes no onOpenPage: it is already the page, and its header
// carries the original-posting link, so neither link is repeated here.
export function Detail({ job, d, profile, taxonomy, cov, onOpenPage }) {
  const [quote, setQuote] = useState(null);
  if (!d) return <div className="detail"><span className="dim">Loading…</span></div>;
  const req = d.skills.filter((s) => s.requirement === "required");
  const nice = d.skills.filter((s) => s.requirement !== "required");
  const have = new Set(profile?.skills || []);
  const met = metSkills(profile, d);
  const url = d.sources.find((s) => s.url)?.url;
  // A required group's members say so on hover: any one of them meets the ask (HIR-251).
  const { groups } = skillSides(d);
  const others = (id) => groups.find((g) => g.includes(id))?.filter((x) => x !== id).map((x) => taxonomy[x] || x);
  const chip = (s) => {
    const on = quote?.skill_id === s.skill_id;
    const miss = profile && s.requirement === "required" && !met.has(s.skill_id);
    const alt = s.requirement === "required" && others(s.skill_id);
    const status = profile ? (have.has(s.skill_id) ? "In your profile" : met.has(s.skill_id) ? "Not in your profile, but you have an alternative" : "Not in your profile") : "Show the quote";
    return (
      <button key={s.skill_id} type="button" className={`chip${s.requirement !== "required" ? " nice" : ""}${on ? " on" : ""}${miss ? " missing" : ""}`}
        title={alt ? `${status}. Any one of these meets the ask: also ${alt.join(", ")}` : status}
        onClick={() => setQuote(on ? null : s)}>
        {profile && have.has(s.skill_id) && <span className="tick">✓</span>}{s.display}
      </button>
    );
  };
  return (
    <div className="detail">
      <div className="cols">
        <div className="col wide"><h4>Required · {req.length}</h4><div className="chips">{req.map(chip)}{!req.length && <span className="dim">none extracted</span>}</div></div>
        <div className="col"><h4>Nice-to-have · {nice.length}</h4><div className="chips">{nice.map(chip)}{!nice.length && <span className="dim">none</span>}</div></div>
      </div>
      {quote && (
        <div className="quote" role="note">
          <span className="k">{quote.display} · {quote.requirement === "required" ? "required" : "nice-to-have"} · quote from posting</span>
          <span>“{quote.raw_text}”</span>
        </div>
      )}
      {cov && cov.total > 0 && (
        <div className="cover">You cover <b>{cov.covered} of {cov.total}</b> required skills{cov.thin ? "" : ` (${pct(cov.score)}%)`}{cov.missing.length ? ` · missing, most asked for first: ${missingNames(cov.missing, taxonomy)}` : cov.thin ? ` · ${FEW_SKILLS}, so Best fit does not treat this as a full match` : " · full match"}.</div>
      )}
      {cov?.gated_by && (
        <div className="cover">Out of reach as the posting is written: it {MISS_LABELS[cov.gated_by]}. Best fit sorts it to the bottom.</div>
      )}
      {(d.german || d.degree || d.production) && (
        <div className="cover attrs">
          {d.german && <span className={flag(profile, "german", d)}>{germanLine(d)}{d.german_signal && <span className="dim"> · “{d.german_signal}”</span>}</span>}
          {d.degree && <span className={flag(profile, "degree", d)}>{degreeLine(d)}{d.degree_signal && <span className="dim"> · “{d.degree_signal}”</span>}</span>}
          {d.production && <span className={flag(profile, "production", d)}>{productionLine(d)}{d.production_signal && <span className="dim"> · “{d.production_signal}”</span>}</span>}
        </div>
      )}
      {d.too_short && (
        <div className="cover">Only a fragment of this posting was stored (a cut-off screenshot or a teaser), so it is <b>left out of the chart</b>. Add the full posting via a link or pasted text to replace it.</div>
      )}
      {d.legacy && (
        <div className="cover">Imported from the old project with the old extractor's skills and no posting text, so it is <b>left out of the chart</b> and never re-extracted. Add the posting via a link or screenshot to replace it.</div>
      )}
      {d.proposed.filter((p) => p.status === "pending").length > 0 && (
        <div className="cover">Also mentions {d.proposed.filter((p) => p.status === "pending").map((p) => p.label).join(", ")} — not in the taxonomy yet, waiting for review.</div>
      )}
      <div className="meta">
        <div className="m">
          <span>First seen {dateShort(d.first_seen)}</span><span>·</span><span>Last seen {timeAgo(d.last_seen)}</span><span>·</span><span>Reposts {d.repost_count}</span>
          {d.seniority && <><span>·</span><span>Seniority {d.seniority} ({d.seniority_basis}{d.seniority_signal ? `: “${d.seniority_signal}”` : ""})</span></>}
          <span>·</span><span>Sources: {d.sources.map((s) => `${sourceCode(s.source)[1]} (${dateShort(s.first_seen)})`).join(", ")}</span>
        </div>
        <span className="links">
          {onOpenPage && <a href={`/jobs/${d.id}`} target="_blank" rel="noopener" title="Our stored copy of the posting; keeps working after the original is taken down">Permanent page<Ext /></a>}
          {url && onOpenPage && <a href={url} target="_blank" rel="noopener">Open original posting<Ext /></a>}
        </span>
      </div>
    </div>
  );
}
