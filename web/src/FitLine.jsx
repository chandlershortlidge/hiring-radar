import { pctInt } from "./format.js";

// "You have 12 of the 15 skills Berlin asks for most" (HIR-285): the line a city page opens
// with once the visitor has skills in their profile, with the biggest gaps beside it. It is
// the one piece of layout B that Chandler carried over into the chosen layout A.
//
// Counted in the browser from the rows the chart has already loaded, so it follows the
// chart's filters (job family, seniority, required or nice-to-have) and asks the server
// for nothing. "In your profile" is the same test the chart's bar colours use.
//
// Does NOT judge single jobs (the fit badge in the job list does that), and draws nothing
// without profile skills or before the chart's numbers are in.

// How many of the most-asked-for skills the line is about, and how many gaps it names.
export const FIT_TOP = 15;
export const FIT_GAPS = 3;

// `skills` are the chart's rows, most asked for first; `total` is the job count behind them.
export function cityFit(profile, skills, total, n = FIT_TOP, gaps = FIT_GAPS) {
  const top = (skills || []).slice(0, n);
  const have = new Set(profile?.skills || []);
  const missing = top.filter((s) => !have.has(s.skill_id));
  return {
    have: top.length - missing.length,
    of: top.length,
    gaps: missing.slice(0, gaps).map((s) => ({ id: s.skill_id, name: s.display, pct: pctInt(s.count, total) })),
  };
}

export default function FitLine({ profile, data, place }) {
  if (!profile?.skills?.length || !data?.total || !data.skills?.length) return null;
  const f = cityFit(profile, data.skills, data.total);
  return (
    <section className="fitline" aria-labelledby="fit-title"><div className="fitline-in">
      <div>
        <p className="eyebrow">Your fit · {place}</p>
        <h2 id="fit-title">You have <mark>{f.have} of the {f.of}</mark> skills {place} asks for most.</h2>
      </div>
      {f.gaps.length > 0 && (
        <div className="gaps">
          <span>Gaps:</span>
          {f.gaps.map((g) => <span key={g.id} className="gap-chip">{g.name} <span className="mono">{g.pct}%</span></span>)}
        </div>
      )}
    </div></section>
  );
}
