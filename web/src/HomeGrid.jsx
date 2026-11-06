import { gridGroups, pctInt } from "./format.js";

// What a first-time visitor sees instead of a dashboard for a city they never chose
// (HIR-188): one card per market, grouped by country, each with its job count and the
// three skills its jobs ask for most, as mini bars.
//
// Every number here comes from the one /api/skills request the page already makes with no
// city filter: each skill row carries its count per city, and the response carries the job
// total per city. Nothing is fetched per card. "New this week" is in the wireframe but has
// no data behind it yet, so it is left off (out of scope for HIR-188).
const TOP = 3;

export const topSkills = (skills, city, total, n = TOP) => (skills || [])
  .map((s) => ({ name: s.display, count: s.by_city?.[city] || 0 }))
  .filter((s) => s.count > 0)
  .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name))
  .slice(0, n)
  .map((s) => ({ ...s, pct: pctInt(s.count, total) }));

// `counts` is open jobs per city, the same number the city picker shows, so the two agree.
// The bars are a share of the jobs we have actually read in that city (`city_totals`),
// which is the slightly smaller set — a handful of postings are stored as a fragment too
// short to chart. Each number is right for what it says; the stats line explains the gap.
export default function HomeGrid({ data, counts, family, onRequestCity }) {
  const charted = data?.city_totals || {};
  const groups = gridGroups(counts);
  const href = (place) => (family ? `/${place.slug}/${family}` : `/${place.slug}`);

  return (
    <section className="markets" aria-labelledby="markets-title">
      <div className="markets-head">
        <h2 id="markets-title">Or browse the markets</h2>
        <span className="dim">sorted by open jobs</span>
      </div>
      {groups.map((g) => (
        <div key={g.name} className="market-group">
          <div className="market-head">{g.name}</div>
          <div className="market-cards">
            {g.places.map((p) => {
              const total = counts[p.name] || 0;
              const top = topSkills(data?.skills, p.name, charted[p.name] || 0);
              const max = Math.max(1, ...top.map((s) => s.pct));
              return (
                <a key={p.slug} className="card market" href={href(p)}>
                  <h3>{p.name}</h3>
                  <p className="mono dim">{total} open</p>
                  {top.length ? (
                    <ul>
                      {top.map((s) => (
                        <li key={s.name}>
                          <span className="nm">{s.name}</span>
                          <span className="tr"><i style={{ width: `${(s.pct / max) * 100}%` }} /></span>
                          <span className="pc mono">{s.pct}%</span>
                        </li>
                      ))}
                    </ul>
                  ) : <p className="dim none">No jobs here yet.</p>}
                </a>
              );
            })}
            {g.name === "Germany" && (
              <div className="card market ask">
                <p className="dim">More German cities as they’re added</p>
                <button type="button" className="btn ghost" onClick={onRequestCity}>Request a city →</button>
              </div>
            )}
          </div>
        </div>
      ))}
    </section>
  );
}
