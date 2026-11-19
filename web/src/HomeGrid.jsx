import { gridPlaces, pctInt } from "./format.js";
import { pathFor } from "./routes.js";

// Every market on the home page, as one ranked table (HIR-285; it was a grid of cards,
// HIR-188): a row per market, busiest first, with its country, its open-job count and the
// three skills its jobs ask for most, as small bars. Each row is a link to that market.
//
// One table, not a group per country: `gridPlaces` orders the rows, and is the only thing
// that would change if grouping came back.
//
// Every number here comes from the one /api/skills request the page already makes with no
// city filter: each skill row carries its count per city, and the response carries the job
// total per city. Nothing is fetched per row. The hero above (HomeHero.jsx) reads the same
// answer through `topSkills` and `cardCounts`, so the two always agree. "New this week" is
// in the 5 Nov wireframe but has no data behind it, so it is left off.
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
// short to chart. Each number is right for what it says.
//
// With a job family chosen (HIR-197) the open count is not split by family, so the row
// shows that family's `city_totals` instead, and the table sorts by it. `data.family` is the
// family the numbers were fetched for, so count, bars and order always describe the same jobs.
export const cardCounts = (counts, data) => (data?.family ? data.city_totals || {} : counts);

// `loading` is true until the job counts and the skills answer have both arrived. Until
// then every city would count as zero, so the rows would sit in name order saying "0 open"
// under a heading that says "sorted by open jobs" (HIR-356: the robot visitor clicked the
// first row, a city with no jobs yet, and found no chart). No rows are drawn before the
// order they are drawn in is true.
export default function HomeGrid({ data, counts, family, onRequestCity, loading = false }) {
  const charted = data?.city_totals || {};
  const shown = cardCounts(counts, data);
  const places = gridPlaces(shown);
  const href = (place) => pathFor({ view: "city", place: place.slug, family });

  return (
    <section className="markets" aria-labelledby="markets-title">
      <div className="markets-head">
        <h2 id="markets-title">All {places.length} markets</h2>
        <span className="dim">sorted by open jobs · top three skills each</span>
      </div>
      <div className="card market-table">
        {loading ? <p className="dim market-loading" role="status">Loading markets…</p> : places.map((p) => {
          const total = shown[p.name] || 0;
          const top = topSkills(data?.skills, p.name, charted[p.name] || 0);
          return (
            <a key={p.slug} className="market-row" href={href(p)}>
              <div className="mk-city"><h3>{p.name}</h3><span className="market-tag">{p.group}</span></div>
              <span className="mk-open"><span>{total} open</span></span>
              {/* each bar is the share itself, so the rows can be read against each other */}
              {top.length ? top.map((s) => (
                <span key={s.name} className="mk-skill">
                  <span className="nm">{s.name}</span>
                  <span className="tr"><i style={{ width: `${Math.min(100, s.pct)}%` }} /></span>
                  <span className="pc">{s.pct}%</span>
                </span>
              )) : <span className="dim none">No jobs here yet.</span>}
              <span className="mk-go" aria-hidden="true">→</span>
            </a>
          );
        })}
      </div>
      <p className="market-ask dim">
        More cities as they’re added.{" "}
        <button type="button" className="btn ghost" onClick={onRequestCity}>Request a city →</button>
      </p>
    </section>
  );
}
