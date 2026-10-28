import { useEffect, useState } from "react";
import { api } from "./api.js";

// What the jobs requiring the selected skill also require. The server does every bit of
// the arithmetic — share, the baseline it is held against, lift (which picks the ten rows
// but is never shown), the under-5-jobs cutoff, the order they arrive in — so this fetches
// those rows and draws them in that order. Renders nothing until a skill is selected.
const MIN_CO_JOBS = 5;   // queries.MIN_CO_JOBS, stated in the description below

export default function RelatedSkills({ filters, skillName, refreshKey }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!filters.skill) { setData(null); return; }
    let live = true;
    api.relatedSkills(filters).then((r) => { if (live) setData(r); });
    return () => { live = false; };
  }, [filters, refreshKey]);

  if (!filters.skill || !data?.skills.length) return null;

  return (
    <section className="card related" aria-labelledby="related-title">
      <div className="related-head">
        <h2 id="related-title">Jobs requiring {skillName} also require</h2>
        <p>
          {data.selected_count} of the {data.total} jobs in view require {skillName}. These
          skills show up more often in those jobs than across all jobs. Skills in fewer
          than {MIN_CO_JOBS} of them are left out.
        </p>
      </div>
      <ul className="related-list">
        {/* TODO(HIR-66): a row should be clickable to drill in (jobs requiring both skills).
            That needs `skill` to become a list on the filters, with AND semantics. */}
        {data.skills.map((s) => (
          <li key={s.skill_id} className="related-row">
            <span className="name">{s.display}</span>
            <span className="share">{Math.round(s.pct)}% <span className="dim">· vs {Math.round(s.base_pct)}% of all jobs</span></span>
          </li>
        ))}
      </ul>
    </section>
  );
}
