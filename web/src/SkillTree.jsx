import { useMemo, useState } from "react";

// The skill tree: one radial map of how the market's skills sit above and below each other.
// Every coordinate — ring radius, angle, each edge's two endpoints, the viewBox — arrives
// from app/skill_tree.py, so this file does no layout arithmetic. What it decides is purely
// how a node looks:
//
//   * distance from the centre = how specialized the skill is (the trunk is prevalent);
//   * the outer ring's area = the share of jobs *mentioning* the skill;
//   * the filled core's area = the share *requiring* it.
//
// Both numbers are also printed beside every node, never hidden in a tooltip: the gap
// between them (Snowflake, mentioned by 17% and required by 3%) is the thing worth seeing,
// and it is what tells a résumé keyword apart from a skill that gates the interview.
//
// Labels sit beside their node, on the side of the picture the node is on. At MAX_NODES
// they mostly clear each other; what still touches is a branch whose child sits at nearly
// its own angle one ring further out (Machine Learning and PyTorch, Azure and GCP).
// Pulling branch labels back along their own spoke was tried and is not the fix — it
// slides them across the node they name. The real fix is a de-collision pass with leader
// lines, which v1 does not need.
//
// Hovering a node lights the path back to the centre — the route through the market that
// leads to that specialization. Clicking one filters the job list, exactly as a chart bar
// does, additive on shift- or meta-click.
// Sizes below are in the user units of a 1000-unit viewBox and get scaled by `k` to
// whatever viewBox the server actually sent — a deeper tree needs more rings and so a
// larger box, and without this a node and its label would shrink as the tree grew. Strokes
// are left to CSS, which keeps them at a constant screen width (vector-effect).
const MIN_R = 7;
const MAX_R = 20;
const LABEL_GAP = 7;
const NAME_SIZE = 13;
const NUMS_SIZE = 11;
const HUB_R = 23;
// Area, not radius, carries the share, so a node twice as common draws twice the ink.
const radius = (pct, max) => MIN_R + (MAX_R - MIN_R) * Math.sqrt(Math.max(0, pct) / (max || 1));

export default function SkillTree({ data, selected = [], onSelect }) {
  const [hover, setHover] = useState(null);
  const nodes = data?.nodes || [];
  const by = useMemo(() => Object.fromEntries(nodes.map((n) => [n.skill_id, n])), [nodes]);
  const maxPct = useMemo(() => nodes.reduce((m, n) => Math.max(m, n.mentioned_pct), 0), [nodes]);
  // The hovered node and every ancestor up to the centre: the branch to light up.
  const lit = useMemo(() => {
    const path = new Set();
    for (let at = hover; at && by[at] && !path.has(at); at = by[at].parent) path.add(at);
    return path;
  }, [hover, by]);

  if (!data) return <div className="empty">Loading the tree…</div>;
  if (!data.total) return <div className="empty">No jobs match these filters yet.</div>;
  if (!nodes.length) return <div className="empty">Too few jobs match these filters to map a tree.</div>;

  const { size } = data;
  const cx = data.centre.x;
  const cy = data.centre.y;
  const k = size / 1000;

  return (
    <div className="tree">
      <svg viewBox={`0 0 ${size} ${size}`} className="tree-svg" role="group"
        aria-label={`Skill tree: ${nodes.length} skills over ${data.total} jobs`}>
        {data.edges.map((e) => (
          <path key={e.child} className={`tree-edge${lit.has(e.child) ? " lit" : ""}`} d={e.path} />
        ))}
        <circle className="tree-hub" cx={cx} cy={cy} r={HUB_R * k} />
        <text className="tree-hub-n" x={cx} y={cy - 2 * k} textAnchor="middle" style={{ fontSize: NAME_SIZE * k }}>{data.total}</text>
        <text className="tree-hub-l" x={cx} y={cy + 12 * k} textAnchor="middle" style={{ fontSize: NUMS_SIZE * k }}>jobs</text>
        {nodes.map((n) => {
          const r = radius(n.mentioned_pct, maxPct) * k;
          // The core's area is the required share of the ring's area, so the visible gap
          // between the two circles *is* the mentioned-but-not-required margin.
          const core = r * Math.sqrt(n.mentioned ? n.required / n.mentioned : 0);
          const right = n.angle < 180;
          const lx = n.x + (right ? 1 : -1) * (r + LABEL_GAP * k);
          const sel = selected.includes(n.skill_id);
          const dim = selected.length > 0 && !sel;
          return (
            <g key={n.skill_id} role="button" tabIndex={0}
              className={`tree-node${sel ? " on" : ""}${dim ? " dimmed" : ""}${lit.has(n.skill_id) ? " lit" : ""}`}
              aria-pressed={sel}
              aria-label={`${n.display}: mentioned by ${n.mentioned_pct}% of jobs, required by ${n.required_pct}%.`
                + `${n.parent ? ` A specialization of ${by[n.parent]?.display || n.parent}.` : " A branch of its own."}`
                + ` ${sel ? "Remove from" : "Filter"} job list`}
              onClick={(e) => onSelect(n.skill_id, e.shiftKey || e.metaKey)}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onSelect(n.skill_id, e.shiftKey || e.metaKey); } }}
              onMouseEnter={() => setHover(n.skill_id)} onMouseLeave={() => setHover(null)}
              onFocus={() => setHover(n.skill_id)} onBlur={() => setHover(null)}>
              <circle className="ring" cx={n.x} cy={n.y} r={r} />
              {core > 0.5 && <circle className="core" cx={n.x} cy={n.y} r={core} />}
              <text className="label" x={lx} y={n.y - 1 * k} textAnchor={right ? "start" : "end"} style={{ fontSize: NAME_SIZE * k }}>{n.display}</text>
              <text className="nums" x={lx} y={n.y + 12 * k} textAnchor={right ? "start" : "end"} style={{ fontSize: NUMS_SIZE * k }}>
                {Math.round(n.mentioned_pct)}% · {Math.round(n.required_pct)}% req
              </text>
            </g>
          );
        })}
      </svg>
      <div className="bars-foot">
        <div>
          <span className="legend"><svg width="30" height="16" aria-hidden="true"><circle className="lg-ring" cx="15" cy="8" r="7" /><circle className="lg-core" cx="15" cy="8" r="3.5" /></svg>
            ring = mentioned, core = required</span>
          <span>farther out = more specialized · an edge means the outer skill’s jobs nearly always ask for the inner one too</span>
        </div>
        <div><span>Click a skill to filter the jobs below · ⇧- or ⌘-click to add one · hover to light its path</span></div>
      </div>
    </div>
  );
}
