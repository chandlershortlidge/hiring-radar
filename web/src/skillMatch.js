// The one skill matcher. Used by the find box over the chart (HIR-67A) and by the add-skill
// popover in the chip row (HIR-79), so both answer "does this skill match what I typed?"
// the same way: case-insensitive substring over the display name or any taxonomy alias.
//
// Pure. It does not order, rank, cut or fetch anything — a caller keeps whatever order its
// rows already arrived in, and an empty query means "everything", unfiltered.

export function matchSkill(display, aliases, query) {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  return (display || "").toLowerCase().includes(q)
    || (aliases || []).some((a) => a.toLowerCase().includes(q));
}

// `rows` carry `skill_id` and `display`; `aliases` maps a skill id to its aliases.
export function filterSkills(rows, aliases, query) {
  if (!query.trim()) return rows;
  return rows.filter((s) => matchSkill(s.display, (aliases || {})[s.skill_id], query));
}
