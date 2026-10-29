import { listAnd } from "./format.js";
import { Plus } from "./icons.jsx";

// What the jobs requiring every selected skill also require. The server does every bit of
// the arithmetic — share, the baseline it is held against, lift (which picks the ten rows
// but is never shown), the under-5-jobs cutoff, the order they arrive in — so this fetches
// those rows and draws them in that order. Clicking a row adds that skill to the selection.
//
// With several skills selected the list prunes fast, because a row now has to appear in at
// least MIN_CO_JOBS of the jobs requiring *all* of them. The two empty answers read
// differently and the server tells them apart with selected_count: 0 means no job requires
// all of these, above 0 means some do but nothing else recurs often enough to report.
// With a single skill an empty list stays silent, as it did before the panel took a set.
//
// The rows arrive as a prop: App makes the one request, because the add-skill popover in the
// chip row (HIR-79) suggests the same rows in the same order and must not ask for them again.
const MIN_CO_JOBS = 5;   // queries.MIN_CO_JOBS, stated in the description below

export default function RelatedSkills({ filters, skillNames, onAdd, data }) {
  const several = filters.skillIds.length > 1;
  if (!filters.skillIds.length || !data) return null;
  if (!data.skills.length && !several) return null;
  const names = listAnd(skillNames);

  return (
    <section className="card related" aria-labelledby="related-title">
      <div className="related-head">
        <h2 id="related-title">Jobs requiring {names} also require</h2>
        {data.skills.length > 0 ? (
          <p>
            {data.selected_count} of the {data.total} jobs in view require {names}. These
            skills show up more often in those jobs than across all jobs. Skills in fewer
            than {MIN_CO_JOBS} of them are left out. Click one to add it to the filter.
          </p>
        ) : (
          <p>
            {data.selected_count === 0
              ? `No job in view requires ${names} together, so there is nothing to compare.`
              : `Too few jobs require ${names} together to say what else they ask for:`
                + ` ${data.selected_count} do, and no other skill appears in at least ${MIN_CO_JOBS} of them.`}
          </p>
        )}
      </div>
      {data.skills.length > 0 && (
        <ul className="related-list">
          {data.skills.map((s) => (
            <li key={s.skill_id}>
              <button type="button" className="related-row" onClick={() => onAdd(s.skill_id)}
                aria-label={`Add ${s.display} to the skill filter`} title={`Also require ${s.display}`}>
                <span className="name">{s.display}</span>
                <span className="share">{Math.round(s.pct)}% <span className="dim">· vs {Math.round(s.base_pct)}% of all jobs</span>
                  <span className="plus" aria-hidden="true"><Plus size={12} /></span></span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
