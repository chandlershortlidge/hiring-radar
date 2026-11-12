import { gridPlaces, pctInt } from "./format.js";
import { pathFor } from "./routes.js";

// What a first-time visitor sees instead of a dashboard for a city they never chose
// (HIR-188): one card per market, each with its job count and the three skills its jobs ask
// for most, as mini bars.
//
// The cards sit in ONE grid, busiest market first, with the country as a small label on each
// card. They used to be split into a row per country, which left each row half empty while a
// country has only one or two cities (HIR-191). Grouping by country can come back once a
// group has four or more cities to fill a row with; `gridPlaces` is the only thing that
// would change. Not this ticket.
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
//
// With a job family chosen (HIR-197) the open count is not split by family, so the card
// shows that family's `city_totals` instead, and the grid sorts by it. `data.family` is the
// family the numbers were fetched for, so count, bars and order always describe the same jobs.
export const cardCounts = (counts, data) => (data?.family ? data.city_totals || {} : counts);

export default function HomeGrid({ data, counts, family, onRequestCity }) {
  const charted = data?.city_totals || {};
  const shown = cardCounts(counts, data);
  const places = gridPlaces(shown);
  const href = (place) => pathFor({ view: "city", place: place.slug, family });

  return (
    <section className="markets" aria-labelledby="markets-title">
      <div className="markets-head">
        <h2 id="markets-title">Or browse the markets</h2>
        <span className="dim">sorted by open jobs</span>
      </div>
      <div className="market-cards">
        {places.map((p) => {
          const total = shown[p.name] || 0;
          const top = topSkills(data?.skills, p.name, charted[p.name] || 0);
          const max = Math.max(1, ...top.map((s) => s.pct));
          return (
            <a key={p.slug} className="card market" href={href(p)}>
              <span className="market-tag">{p.group}</span>
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
      </div>
      {/* Out of the grid since HIR-191: a dashed card in a row of real markets reads as a market. */}
      <p className="market-ask dim">
        More cities as they’re added.{" "}
        <button type="button" className="btn ghost" onClick={onRequestCity}>Request a city →</button>
      </p>
    </section>
  );
}
