import { useMemo, useState } from "react";

// The skill tree: one radial map of how the market's skills sit above and below each other.
// Every coordinate — ring position, node and core radius, each edge's path, where a name
// goes so it overlaps nothing, the tooltip's own box — arrives from app/skill_tree.py.
// This file does no arithmetic. What it decides is only what things are made of:
//
//   * distance from the centre = how specialized the skill is (the trunk is prevalent);
//   * the outer circle's area = the share of jobs *mentioning* the skill, drawn as a tint;
//   * the solid core's area = the share *requiring* it, so the band between the two is
//     the mentioned-but-not-required margin — a résumé keyword rather than a gate;
//   * hue = which branch of the market the skill belongs to. Only the three largest
//     branches are coloured (a tree shows every branch at once, and the dataviz palette
//     validates three hues for that case); the trunk and the small branches are ink.
//
// The two percentages are not written on the drawing — thirty two-line labels do not fit.
// They live in the tooltip, which opens on hover *and* on keyboard focus, and they are in
// every node's aria-label besides, so a screen reader never depends on the tip at all.
//
// Hovering a node also lights the path back to the centre — the route through the market
// that leads to that specialization. Clicking filters the job list exactly as a chart bar
// does, additive on shift- or meta-click.
export default function SkillTree({ data, selected = [], onSelect }) {
  const [hover, setHover] = useState(null);
  const nodes = data?.nodes || [];
  const by = useMemo(() => Object.fromEntries(nodes.map((n) => [n.skill_id, n])), [nodes]);
  // The hovered node and every ancestor up to the centre: the branch to light up.
  const lit = useMemo(() => {
    const path = new Set();
    for (let at = hover; at && by[at] && !path.has(at); at = by[at].parent) path.add(at);
    return path;
  }, [hover, by]);
  // The coloured branches, in hue order — the legend, and the proof that identity is
  // never carried by colour alone.
  const legend = useMemo(() => nodes
    .filter((n) => n.branch_index != null && n.branch === n.skill_id)
    .sort((a, b) => a.branch_index - b.branch_index), [nodes]);

  if (!data) return <div className="empty">Loading the tree…</div>;
  if (!data.total) return <div className="empty">No jobs match these filters yet.</div>;
  if (!nodes.length) return <div className="empty">Too few jobs match these filters to map a tree.</div>;

  const { size, font } = data;
  const tip = hover ? by[hover] : null;

  return (
    <div className="tree">
      <svg viewBox={`0 0 ${size} ${size}`} className="tree-svg" role="group"
        aria-label={`Skill tree: ${nodes.length} skills over ${data.total} jobs`}>
        {data.edges.map((e) => (
          <path key={e.child} className={`tree-edge${lit.has(e.child) ? " lit" : ""}`} d={e.path} />
        ))}
        <circle className="tree-hub" cx={data.centre.x} cy={data.centre.y} r={data.hub_r} />
        <text className="tree-hub-n" x={data.centre.x} y={data.centre.y} textAnchor="middle"
          style={{ fontSize: font * 0.62 }}>{data.total} jobs</text>
        {nodes.map((n) => {
          const sel = selected.includes(n.skill_id);
          const dim = selected.length > 0 && !sel;
          // A branch with no hue is drawn in ink: hue is an extra, never the only cue.
          const hue = n.branch_index == null ? "" : ` b${n.branch_index}`;
          return (
            <g key={n.skill_id} role="button" tabIndex={0}
              className={`tree-node${hue}${sel ? " on" : ""}${dim ? " dimmed" : ""}${lit.has(n.skill_id) ? " lit" : ""}`}
              aria-pressed={sel}
              aria-label={`${n.display}: mentioned by ${n.mentioned_pct}% of jobs, required by ${n.required_pct}%.`
                + `${n.parent ? ` A specialization of ${by[n.parent]?.display || n.parent}.` : " A branch of its own."}`
                + ` ${sel ? "Remove from" : "Filter"} job list`}
              onClick={(e) => onSelect(n.skill_id, e.shiftKey || e.metaKey)}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onSelect(n.skill_id, e.shiftKey || e.metaKey); } }}
              onMouseEnter={() => setHover(n.skill_id)} onMouseLeave={() => setHover(null)}
              onFocus={() => setHover(n.skill_id)} onBlur={() => setHover(null)}>
              {n.leader && <path className="leader" d={n.leader} />}
              <circle className="ring" cx={n.x} cy={n.y} r={n.r} />
              {n.core_r > 0.5 && <circle className="core" cx={n.x} cy={n.y} r={n.core_r} />}
              <text className="label" x={n.label_x} y={n.label_y} textAnchor={n.label_anchor}
                style={{ fontSize: font }}>{n.display}</text>
            </g>
          );
        })}
        {/* Last, so it is over everything. Pointer events off: the tip must never steal the
            hover that is keeping it open. */}
        {tip && (
          <g className="tree-tip" aria-hidden="true">
            <rect x={tip.tip.x} y={tip.tip.y} width={tip.tip.w} height={tip.tip.h} rx={5 * (size / 1000)} />
            {tip.tip.lines.map((line, i) => (
              <text key={i} x={tip.tip.x + 8 * (size / 1000)}
                y={tip.tip.y + data.tip_font * (1.35 * i + 1.25)} style={{ fontSize: data.tip_font }}>{line}</text>
            ))}
          </g>
        )}
      </svg>
      <div className="bars-foot">
        <div>
          {legend.map((n) => (
            <span key={n.skill_id} className="legend">
              <i className={`swatch b${n.branch_index}`} />{n.display}
            </span>
          ))}
          <span className="legend"><i className="swatch" />everything else</span>
        </div>
        <div><span>Ring = mentioned, solid core = required · farther out = more specialized · click to filter, ⇧/⌘ to add · hover or tab for the numbers</span></div>
      </div>
    </div>
  );
}
