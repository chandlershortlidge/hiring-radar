// A job's own page at /jobs/{id}: the stored posting text, served by us, so the link keeps
// working after the employer takes the original down. Shows the same skills/attributes
// detail as the expanded list row, then the text as captured.
//
// Does NOT re-fetch the original, edit the text, or check whether the original is still up.

import { useEffect, useState } from "react";
import { api } from "./api.js";
import { Ext } from "./icons.jsx";
import { cap, dateShort, sourceCode } from "./format.js";
import { coverage } from "./profile.js";
import { Detail } from "./JobList.jsx";

export default function JobPage({ id, onBack, profile, taxonomy }) {
  const [d, setD] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let live = true;
    setD(null); setError(null);
    api.job(id).then((r) => { if (live) setD(r); }).catch((e) => { if (live) setError(e.message); });
    return () => { live = false; };
  }, [id]);

  useEffect(() => {
    const before = document.title;
    if (d) document.title = `${d.company} · ${d.title} · hiring-radar`;
    return () => { document.title = before; };
  }, [d]);

  const back = (e) => { e.preventDefault(); onBack(); };

  if (error) {
    return (
      <main className="main page">
        <a href="/" onClick={back}>← All jobs</a>
        <section className="card"><div className="empty">{error === "no such job" ? `There is no job #${id}.` : error}</div></section>
      </main>
    );
  }
  if (!d) return <main className="main page"><a href="/" onClick={back}>← All jobs</a><section className="card"><div className="empty dim">Loading…</div></section></main>;

  const url = d.sources.find((s) => s.url)?.url;
  const captured = d.sources.map((s) => `${sourceCode(s.source)[1]} (${dateShort(s.first_seen)})`).join(", ");
  const cov = profile ? coverage(profile, d.skills) : null;

  return (
    <main className="main page">
      <a href="/" onClick={back}>← All jobs</a>
      <section className="card" aria-labelledby="job-title">
        <div className="page-head">
          <div>
            <h1 id="job-title">{d.title}</h1>
            <p className="lede">{d.company}{d.location_raw || d.city ? ` · ${d.location_raw || d.city}` : ""}{d.seniority ? ` · ${cap(d.seniority)}` : ""}</p>
          </div>
          <div className="page-links">
            <span className="dim">Stored copy from {dateShort(d.first_seen)} · {captured}</span>
            {url && <a href={url} target="_blank" rel="noopener">Open original posting<Ext /></a>}
          </div>
        </div>
        <Detail job={d} d={d} profile={profile} taxonomy={taxonomy} cov={cov} />
        <div className="posting-wrap">
          <h4>Posting as captured</h4>
          <pre className="posting">{d.description_text}</pre>
        </div>
      </section>
    </main>
  );
}
