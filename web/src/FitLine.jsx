import { pctInt } from "./format.js";

// "Gaps: [Agents 38%] [TypeScript 19%]  10 of 15 in your profile" (HIR-411): one small line
// inside the chart card on a city page, under the find box and above the bars, once the
// visitor has skills in their profile. It names the most-asked-for skills they do not have,
// which the chart otherwise makes them hunt for among the tinted bars.
//
// It replaced a headline band above the two columns ("You have 10 of the 15 skills Berlin
// asks for most", HIR-285), which restated the bars in the largest text on the page and had
// nothing to click.
//
// Counted in the browser from the rows the chart has already loaded, so it follows the
// chart's filters (job family, seniority, required or nice-to-have) and asks the server
// for nothing. "In your profile" is the same test the chart's bar colours use.
//
// Each gap is a button that does what a click on that skill's bar does: it is handed the
// chart's own click handler and selection, and keeps no state of its own.
//
// Does NOT judge single jobs (the fit badge in the job list does that), does NOT follow the
// chart's find box (the count is about the market, not about what was typed), and draws
// nothing without profile skills or before the chart's numbers are in.

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

// `selected` and `onSelect` are the chart's: the selected skill ids, and the handler a bar
// click calls with (skill id, whether shift or meta was held).
export default function FitLine({ profile, data, selected = [], onSelect }) {
  if (!profile?.skills?.length || !data?.total || !data.skills?.length) return null;
  const f = cityFit(profile, data.skills, data.total);
  return (
    <div className="gaps">
      {f.gaps.length > 0 && <span>Gaps:</span>}
      {f.gaps.map((g) => {
        const sel = selected.includes(g.id);
        return (
          <button key={g.id} type="button" className="gap-chip" aria-pressed={sel}
            aria-label={`${g.name}, ${g.pct}% of jobs, not in your profile. ${sel ? "Remove from" : "Filter"} job list`}
            onClick={(e) => onSelect?.(g.id, e.shiftKey || e.metaKey)}>
            {g.name} <span className="mono">{g.pct}%</span>
          </button>
        );
      })}
      <span className="gaps-count">{f.have} of {f.of} in your profile</span>
    </div>
  );
}
