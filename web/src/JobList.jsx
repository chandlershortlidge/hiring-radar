import { useEffect, useState } from "react";
import { api } from "./api.js";
import { Down, Ext, Repost, Search, Up, X } from "./icons.jsx";
import { DEGREE_RANK, cap, dateShort, degreeLine, germanLine, productionLine, sourceCode, timeAgo } from "./format.js";
import { coverage } from "./profile.js";
import AddSkillChip from "./AddSkillChip.jsx";

const SORTS = { newest: "Newest first", oldest: "Oldest first", reposts: "Most reposted", company: "Company A–Z" };
const PAGE = 20;

export default function JobList({ filters, setFilters, profile, taxonomy, refreshKey, openJobId, onOpened, onOpenPage,
  taxonomyRows = [], aliases = {}, suggestions = [], onAddSkill }) {
  const [sort, setSort] = useState("newest");
  const [page, setPage] = useState({ jobs: [], total: 0 });
  const [open, setOpen] = useState(null);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState(filters.query);

  useEffect(() => { const t = setTimeout(() => setFilters((f) => ({ ...f, query: q })), 250); return () => clearTimeout(t); }, [q, setFilters]);

  useEffect(() => {
    let live = true;
    setLoading(true);
    api.jobs(filters, { sort, limit: PAGE, offset: 0 }).then((r) => { if (live) { setPage(r); setLoading(false); } });
    return () => { live = false; };
  }, [filters, sort, refreshKey]);

  useEffect(() => { if (openJobId) { setOpen(openJobId); onOpened?.(); } }, [openJobId, onOpened]);

  const more = () => api.jobs(filters, { sort, limit: PAGE, offset: page.jobs.length })
    .then((r) => setPage((p) => ({ ...r, jobs: [...p.jobs, ...r.jobs] })));

  const scope = filters.compare ? "both cities" : filters.cities.length ? filters.cities.join(" + ") : "all cities";
  return (
    <section className="card jobs" aria-labelledby="jobs-title">
      <div className="jobs-head">
        <div className="l">
          <h2 id="jobs-title">Jobs</h2>
          {filters.skillIds.length > 0 && <span className="muted" style={{ fontSize: 12.5 }}>Requires</span>}
          {filters.skillIds.map((id) => (
            <span key={id} className="chip-filter">{taxonomy[id] || id}
              <button type="button" aria-label={`Remove ${taxonomy[id] || id} from the skill filter`}
                onClick={() => setFilters((f) => ({ ...f, skillIds: f.skillIds.filter((x) => x !== id) }))}><X size={12} /></button>
            </span>
          ))}
          <AddSkillChip selected={filters.skillIds} suggestions={suggestions} taxonomy={taxonomyRows}
            aliases={aliases} onAdd={onAddSkill} />
          <span className="muted" style={{ fontSize: 13 }}>{page.total} {filters.window === "open" ? "open" : ""} jobs · {scope}</span>
        </div>
        <div className="r">
          <label htmlFor="q" className="sr">Search company or title</label>
          <div className="search"><Search stroke="#6B6B6B" /><input id="q" type="search" className="inp" placeholder="Search company or title" value={q} onChange={(e) => setQ(e.target.value)} /></div>
          <label htmlFor="sort" className="muted" style={{ fontSize: 12.5 }}>Sort</label>
          <select id="sort" className="sel" value={sort} onChange={(e) => setSort(e.target.value)}>
            {Object.entries(SORTS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </div>
      </div>
      <div className="tbl"><div className="tbl-in">
        <div className="row-head"><span>Company</span><span>Title</span><span>City</span><span>First seen</span><span>Status</span><span>Sources</span><span /></div>
        {page.jobs.map((j) => (
          <Row key={j.id} job={j} open={open === j.id} onToggle={() => setOpen(open === j.id ? null : j.id)}
            profile={profile} taxonomy={taxonomy} onOpenPage={onOpenPage} />
        ))}
        {!loading && !page.jobs.length && <div className="empty">No jobs match. Widen the time window or clear the skill filter.</div>}
      </div></div>
      <div className="jobs-foot">
        {page.jobs.length < page.total && <button type="button" className="btn" onClick={more}>Load {Math.min(PAGE, page.total - page.jobs.length)} more</button>}
        <span>Showing {page.jobs.length} of {page.total}</span>
      </div>
    </section>
  );
}

function Row({ job: j, open, onToggle, profile, taxonomy, onOpenPage }) {
  const [detail, setDetail] = useState(null);
  useEffect(() => { if (open && !detail) api.job(j.id).then(setDetail); }, [open, detail, j.id]);
  const cov = profile ? coverage(profile, (j.required_skills || []).map((id) => ({ skill_id: id, requirement: "required" }))) : null;
  const miss = misses(profile, j);
  return (
    <>
      <div className={`row${open ? " open-row" : ""}${j.legacy || j.too_short ? " legacy" : ""}`} onClick={onToggle} role="button" tabIndex={0} aria-expanded={open}
        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onToggle(); } }}>
        <span className="co">{j.company}{j.legacy && <span className="src" style={{ marginLeft: 6 }} title="Imported from the old project with its skills; not in the chart">legacy</span>}{j.too_short && <span className="src" style={{ marginLeft: 6 }} title="Only a fragment of the posting was stored; not in the chart">short</span>}</span>
        <span className="ti">{miss.length > 0 && <span className="fit miss" title={miss.map((w) => MISS_LABELS[w]).join(" · ")}>!</span>}{cov && <span className={`fit${cov.covered === cov.total ? " full" : ""}`} title={`You cover ${cov.covered} of ${cov.total} required skills`}>{cov.covered}/{cov.total}</span>}{j.title}{j.seniority && <span className="dim" style={{ marginLeft: 8, fontSize: 12 }}>{cap(j.seniority)}</span>}</span>
        <span className="ci muted">{j.city || "—"}</span>
        <span className="fs muted" style={{ fontSize: 13 }}>{timeAgo(j.first_seen)}</span>
        <span className="st">
          <span className={`status ${j.status}`}><i />{cap(j.status)}</span>
          {j.repost_count > 0 && <span className="repost" title={`Reposted ${j.repost_count}×`}><Repost />×{j.repost_count}</span>}
        </span>
        <span className="srcs">{j.sources.map((s, i) => { const [code, full] = sourceCode(s.source); return <span key={i} className="src" title={full} aria-label={full}>{code}</span>; })}</span>
        <span className="meta-m muted">{j.city || "—"} · {timeAgo(j.first_seen)} · {cap(j.status)}{j.repost_count > 0 ? ` · reposted ×${j.repost_count}` : ""} · {j.sources.map((s) => sourceCode(s.source)[0]).join(" ")}</span>
        <button type="button" className="exp" aria-label={`${open ? "Hide" : "Show"} skills for ${j.company}`} onClick={(e) => { e.stopPropagation(); onToggle(); }}>{open ? <Up /> : <Down />}</button>
      </div>
      {open && <Detail job={j} d={detail} profile={profile} taxonomy={taxonomy} cov={cov} onOpenPage={onOpenPage} />}
    </>
  );
}

// "miss" when the profile says the person does not meet a hard ask; "" otherwise.
function flag(profile, what, j) {
  if (!profile) return "";
  if (what === "german") return j.german === "required" && !profile.german ? "miss" : "ok";
  if (what === "production") return j.production === "required" && !profile.production ? "miss" : "ok";
  const hard = j.degree_requirement === "required" && !j.degree_or_equivalent;
  return hard && DEGREE_RANK[profile.degree || ""] < DEGREE_RANK[j.degree] ? "miss" : "ok";
}

// The hard asks a profile can fail, and how the row's "!" tooltip names each one.
const MISS_LABELS = {
  german: "needs German",
  production: "needs production experience you don't claim",
  degree: "needs a degree you don't list",
};
const misses = (profile, j) => Object.keys(MISS_LABELS).filter((w) => flag(profile, w, j) === "miss");

// Also rendered by JobPage, which passes no onOpenPage: it is already the page, and its header
// carries the original-posting link, so neither link is repeated here.
export function Detail({ job, d, profile, taxonomy, cov, onOpenPage }) {
  const [quote, setQuote] = useState(null);
  if (!d) return <div className="detail"><span className="dim">Loading…</span></div>;
  const req = d.skills.filter((s) => s.requirement === "required");
  const nice = d.skills.filter((s) => s.requirement !== "required");
  const have = new Set(profile?.skills || []);
  const url = d.sources.find((s) => s.url)?.url;
  const chip = (s) => {
    const on = quote?.skill_id === s.skill_id;
    const miss = profile && s.requirement === "required" && !have.has(s.skill_id);
    return (
      <button key={s.skill_id} type="button" className={`chip${s.requirement !== "required" ? " nice" : ""}${on ? " on" : ""}${miss ? " missing" : ""}`}
        title={profile ? (have.has(s.skill_id) ? "In your profile" : "Not in your profile") : "Show the quote"}
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
      {cov && (
        <div className="cover">You cover <b>{cov.covered} of {cov.total}</b> required skills{cov.missing.length ? ` · missing: ${cov.missing.map((id) => taxonomy[id] || id).join(", ")}` : " · full match"}.</div>
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
          {onOpenPage && <a href={`/jobs/${d.id}`} onClick={(e) => { e.preventDefault(); onOpenPage(d.id); }} title="Our stored copy of the posting; keeps working after the original is taken down">Permanent page</a>}
          {url && onOpenPage && <a href={url} target="_blank" rel="noopener">Open original posting<Ext /></a>}
        </span>
      </div>
    </div>
  );
}
