import { useEffect, useState } from "react";
import { api } from "./api.js";

// "What's rising" (HIR-232): the skills required by a larger or smaller share of open jobs
// in the last 4 weeks than in the 4 weeks before, for one place and job family.
//
// A standalone panel on purpose: it makes its own request and takes only the place and the
// family, so the homepage rework can put it anywhere. The server does all the arithmetic
// and all the holding back (too few jobs, a city or a skill too new to compare); this draws
// the rows in the order they arrive and words the "not enough data yet" answers.
//
// It reads place and family only. The page's other controls (seniority, German, degree,
// time window) do not narrow it: each period needs as many jobs behind it as it can get.

const pct = (n) => `${Math.round(n)}%`;

// "2027-01-03" → "3 January". The server sends a calendar day, so it is read as UTC and
// never shifts by the reader's time zone.
export const dayMonth = (iso) => new Date(`${iso}T00:00:00Z`)
  .toLocaleDateString("en-GB", { day: "numeric", month: "long", timeZone: "UTC" });

// Why there is nothing to show, in a sentence. `place` is the name a person reads.
export function waiting(data, place, role) {
  if (data.reason === "new_city" && data.ready_from) {
    return `Jobs in ${place} have not been collected for long enough to compare two 4-week periods. `
      + `This fills in from about ${dayMonth(data.ready_from)}.`;
  }
  if (data.reason === "few_jobs") return `Too few open ${role} in ${place} over the last 8 weeks to compare.`;
  return "";
}

function Rows({ title, rows, word, total, before }) {
  return (
    <div>
      <h3>{title}</h3>
      {rows.length ? (
        <ul className="related-list">
          {rows.map((s) => (
            <li key={s.skill_id} className="rising-row">
              <span className="name">{s.display}</span>
              <span className="share">
                {pct(s.current_share)} <span className="dim">· {word} from {pct(s.previous_share)}</span>
                <span className="counts dim">{s.current_count} of {total} jobs, was {s.previous_count} of {before}</span>
              </span>
            </li>
          ))}
        </ul>
      ) : <p className="dim none">None by a point or more.</p>}
    </div>
  );
}

// The drawing, apart from the request, so it can be tested without a server.
export function RisingView({ data, place, role }) {
  if (!data) return null;
  const ok = data.status === "ok";
  return (
    <section className="card related rising" aria-labelledby="rising-title">
      <div className="related-head">
        <h2 id="rising-title">What’s rising in {place}</h2>
        {ok ? (
          <p>
            Share of open {role} requiring each skill, last 4 weeks against the 4 weeks before.
            Skills in too few jobs to trust are left out.
          </p>
        ) : <p><b>Not enough data yet.</b> {waiting(data, place, role)}</p>}
      </div>
      {ok && (
        <div className="rising-cols">
          <Rows title="Rising" rows={data.risers} word="up" total={data.current.open_jobs} before={data.previous.open_jobs} />
          <Rows title="Falling" rows={data.fallers} word="down" total={data.current.open_jobs} before={data.previous.open_jobs} />
        </div>
      )}
    </section>
  );
}

export default function RisingSkills({ cities, family, place, role, refreshKey }) {
  const [data, setData] = useState(null);
  const key = cities.join("|");
  useEffect(() => {
    let live = true;
    setData(null);
    api.risingSkills({ cities, families: family ? [family] : [] }).then((r) => { if (live) setData(r); });
    return () => { live = false; };
    // `key` stands in for `cities`: the array is rebuilt on every render of the page.
  }, [key, family, refreshKey]);
  return <RisingView data={data} place={place} role={role} />;
}
