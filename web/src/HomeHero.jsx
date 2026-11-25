import { ALL_GERMANY, axisMax, familyLabel, placeBySlug } from "./format.js";
import { pathFor } from "./routes.js";
import { cardCounts, topSkills } from "./HomeGrid.jsx";

// The top of the home page (HIR-285, the layout Chandler chose on 17 Nov; the left side as
// he redrew it on 25 Nov, HIR-474): the site's tagline on the left, with the search box
// under it, and one market's real top-skills chart on the right.
//
// Every number comes from the one /api/skills request the home page already makes with no
// city filter, the same one the markets table below is drawn from: each skill row carries
// its count per city and the answer carries the job total per city. Nothing new is fetched
// and nothing is counted that the table does not also show.
//
// Does NOT pick an "interesting" finding: the chart shows the most-asked-for skills, in order.

// The market the home page leads with when the visitor has not looked at one yet: the
// site's launch audience is Berlin.
export const HERO_DEFAULT = "berlin";
// How many bars the hero chart draws, as in the chosen picture.
export const HERO_SKILLS = 8;

// Which market the home page leads with: the one this visitor looked at last, else
// Berlin. "All of Germany" is several cities at once and has no numbers of its own in the
// answer, so it is skipped.
export function heroPlace(recent = []) {
  const seen = recent.map(placeBySlug).find((p) => p && p.slug !== ALL_GERMANY.slug);
  return seen || placeBySlug(HERO_DEFAULT);
}

// What the hero's numbers call the jobs: the chosen family, or every role we track.
export const heroRoles = (family) => (family ? `${familyLabel(family)} jobs` : "AI & data jobs");

// The hero's numbers for one market: its open-job count as the table shows it, and its
// most-asked-for skills as a share of the jobs read there. `data.family` is the family
// the numbers were fetched for, so the words and the numbers always describe the same jobs.
export function heroFacts(data, counts, place) {
  const open = cardCounts(counts, data)[place.name] || 0;
  const top = topSkills(data?.skills, place.name, data?.city_totals?.[place.name] || 0, HERO_SKILLS);
  return { open, top, roles: heroRoles(data?.family) };
}

// The headline: what the site is for, in Chandler's words (HIR-474). It replaced a sentence
// built from the lead market's two top shares, which the chart beside it already shows.
export function Tagline() {
  return <h1>See what skills employers <mark>actually</mark> want.</h1>;
}

// The chart beside the tagline: the same bars the city page opens with, cut to the top
// few, and the way in to the full page.
export function HeroChart({ place, family, top, open, loading, onOpen }) {
  const max = axisMax(top[0]?.pct || 0);
  const href = pathFor({ view: "city", place: place.slug, family });
  return (
    <section className="hero-chart" aria-labelledby="hero-chart-title">
      <div className="hero-chart-head">
        <h2 id="hero-chart-title">Most-asked skills in {place.name}</h2>
        <span>share of open jobs that require it</span>
      </div>
      {top.map((s) => (
        <div key={s.name} className="hero-row">
          <span className="nm">{s.name}</span>
          <span className="tr"><i style={{ width: `${Math.min(100, (s.pct / max) * 100)}%` }} /></span>
          <span className="pc">{s.pct}%</span>
        </div>
      ))}
      {!top.length && <div className="empty" role="status">{loading ? "Loading the chart…" : "No jobs here yet."}</div>}
      <a href={href} onClick={(e) => { e.preventDefault(); onOpen(place.slug); }}>
        Open the full {place.name} chart and its {open} jobs →
      </a>
    </section>
  );
}
