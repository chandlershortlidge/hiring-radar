import { useState } from "react";
import Drawer from "./Drawer.jsx";
import { api } from "./api.js";
import { Check, Info, Warn } from "./icons.jsx";
import { PLACES, sourceCode, timeAgo } from "./format.js";

const FOUND = { linkedin: "LinkedIn", indeed: "Indeed", company_site: "Company site", referral: "Referral", other: "Other" };
const TABS = { url: "Paste a link", text: "Paste text", screenshot: "Upload screenshot" };

export default function AddJobDrawer({ onClose, onAdded, onViewJob }) {
  const [tab, setTab] = useState("url");
  const [f, setF] = useState({ url: "", text: "", company: "", title: "", location: PLACES[0], found_via: "linkedin", file: null });
  const [busy, setBusy] = useState(false);
  const [res, setRes] = useState(null);
  const set = (k) => (e) => setF((x) => ({ ...x, [k]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true); setRes(null);
    try {
      let r;
      const common = { company: f.company, title: f.title, location: f.location, found_via: f.found_via };
      if (tab === "url") r = await api.addUrl({ url: f.url.trim(), found_via: f.found_via, company: f.company || null, title: f.title || null, location: f.location || null });
      else if (tab === "text") r = await api.addText({ ...common, text: f.text, url: f.url || null });
      else r = await api.addScreenshot(f.file, { ...common, url: f.url || undefined });
      setRes(r);
      if (r.outcome === "added") onAdded?.(r.job_id);
    } catch (err) { setRes({ outcome: "error", message: err.message }); }
    setBusy(false);
  };

  const needsMeta = tab !== "url";
  const canSubmit = !busy && (tab === "url" ? /^https?:\/\//.test(f.url.trim()) : (f.company && f.title && (tab === "text" ? f.text.trim().length >= 40 : !!f.file)));

  return (
    <Drawer title="Add a job" onClose={onClose}>
      <div className="tabs" role="tablist" aria-label="How to add">
        {Object.entries(TABS).map(([k, v]) => <button key={k} type="button" role="tab" aria-selected={tab === k} onClick={() => { setTab(k); setRes(null); }}>{v}</button>)}
      </div>
      <form onSubmit={submit} style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        {tab === "url" && (
          <div className="field">
            <label htmlFor="url">Posting URL</label>
            <input id="url" type="url" className="mono" value={f.url} onChange={set("url")} placeholder="https://boards.greenhouse.io/acme/jobs/4012345" autoFocus />
            <span className="help">Greenhouse, Lever and Ashby links are read directly. Other career pages are read from the page text; LinkedIn and login-walled pages won't work — use Paste text.</span>
          </div>
        )}
        {tab === "text" && (
          <div className="field">
            <label htmlFor="text">Job description</label>
            <textarea id="text" value={f.text} onChange={set("text")} placeholder="Paste the whole posting, requirements included." autoFocus />
          </div>
        )}
        {tab === "screenshot" && (
          <div className="field">
            <label htmlFor="file">Screenshot</label>
            <input id="file" type="file" accept="image/png,image/jpeg,image/webp" onChange={(e) => setF((x) => ({ ...x, file: e.target.files?.[0] || null }))} style={{ padding: "8px 12px" }} />
            <span className="help">One image, up to 8 MB. The text is transcribed first, then skills are extracted.</span>
          </div>
        )}
        <div className="grid2">
          <div className="field"><label htmlFor="co">Company{needsMeta ? "" : " (optional)"}</label><input id="co" value={f.company} onChange={set("company")} /></div>
          <div className="field"><label htmlFor="ti">Title{needsMeta ? "" : " (optional)"}</label><input id="ti" value={f.title} onChange={set("title")} /></div>
          <div className="field"><label htmlFor="ci">City</label>
            <select id="ci" value={f.location} onChange={set("location")}>{PLACES.map((c) => <option key={c}>{c}</option>)}</select></div>
          <div className="field"><label htmlFor="fv">Found via</label>
            <select id="fv" value={f.found_via} onChange={set("found_via")}>{Object.entries(FOUND).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></div>
        </div>
        {tab !== "url" && <div className="field"><label htmlFor="u2">Link (optional)</label><input id="u2" type="url" className="mono" value={f.url} onChange={set("url")} /></div>}
        <div className="actions">
          <button type="submit" className="btn primary lg" disabled={!canSubmit}>{busy ? "Working…" : "Add job"}</button>
          <button type="button" className="btn lg" onClick={onClose}>Cancel</button>
        </div>
      </form>
      {res && <Result r={res} onViewJob={onViewJob} onText={() => setTab("text")} />}
    </Drawer>
  );
}

function Result({ r, onViewJob, onText }) {
  if (r.outcome === "added") return (
    <div className="note" role="status"><Check />
      <span><b>Added — {r.skills_found} skill{r.skills_found === 1 ? "" : "s"} found{r.proposed ? `, ${r.proposed} proposed for review` : ""}.</b>{" "}
        {r.failed?.length ? <span>Extraction failed: {r.failed[0][1]}. The job is stored and will be retried on the next extract run.</span> : <a href="#" onClick={(e) => { e.preventDefault(); onViewJob(r.job_id); }}>View row</a>}
      </span>
    </div>
  );
  if (r.outcome === "exists") {
    const src = r.job?.sources?.[0];
    return (
      <div className="note soft" role="status"><Info />
        <span><b>Already in the database</b>{src ? ` (seen via ${sourceCode(src.source)[1]} ${timeAgo(src.first_seen)})` : ""}. Nothing added.{" "}
          <a href="#" onClick={(e) => { e.preventDefault(); onViewJob(r.job_id); }}>Go to existing row</a></span>
      </div>
    );
  }
  if (r.outcome === "merged" || r.outcome === "repost") return (
    <div className="note soft" role="status"><Info /><span><b>Looks like a job we already have</b> (same company, near-identical text). Recorded as {r.outcome === "repost" ? "a repost" : "another source"}; nothing new extracted.</span></div>
  );
  if (r.outcome === "unreadable") return (
    <div className="note warn" role="alert"><Warn /><span><b>Couldn't read that page.</b> {r.verdict}. Try <a href="#" onClick={(e) => { e.preventDefault(); onText(); }}>Paste text</a> instead.</span></div>
  );
  if (r.outcome?.startsWith("dropped")) return (
    <div className="note warn" role="alert"><Warn /><span><b>Not stored.</b> {r.outcome.replace("dropped:", "").replace(/_/g, " ")} — the posting fell outside the title or city filter.</span></div>
  );
  return <div className="note warn" role="alert"><Warn /><span><b>Something went wrong.</b> {r.message || r.outcome}</span></div>;
}
