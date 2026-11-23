// The chart's filters, as the jobs card names them (HIR-415). The chart and the job list
// share one set of filters, so picking "Junior" above the chart also narrows the list; the
// jobs card shows one removable chip per filter that is not at its default, so the list
// says what it is filtered by and can be un-filtered from where the person is looking.
//
// Does: turn the filters into chips, each with the words it shows and the change that
// puts its filter back to the default. Pure: the caller hands in the defaults and the
// time-window wording (both live in App.jsx), so nothing here is a second copy of either.
// Does NOT: make chips for city or job family (the sentence at the top of the page owns
// those), for the search box, or for the selected skills (the list draws those itself).
import { DEGREE_FILTERS, EXTRA_FILTER_NAMES, PRODUCTION_FILTERS, SENIORITIES, cap } from "./format.js";
import { germanLabel } from "./FilterPills.jsx";

// "Degree: open without one", but "Degree required" rather than "Degree: degree required".
const named = (name, option) => (option.toLowerCase().startsWith(name.toLowerCase()) ? option : `${name}: ${option.toLowerCase()}`);

// What a chip reads for each one-choice filter. The words come from the control that sets
// it above the chart: the same option text, with the control's label in front where the
// option alone ("Not required", "All") would not say which filter it belongs to.
const WORDS = {
  german: (value) => germanLabel(value),
  production: (value) => named(EXTRA_FILTER_NAMES.production, PRODUCTION_FILTERS[value] || value),
  degree: (value) => named(EXTRA_FILTER_NAMES.degree, DEGREE_FILTERS[value] || value),
  // "Last 30 days" stands alone; "All" does not.
  window: (value, windows) => (value === "all" ? named(EXTRA_FILTER_NAMES.window, windows.all || "All") : windows[value] || value),
};

// One chip per filter that differs from `defaults`: a chip per picked seniority level,
// then German, production experience, degree and the time window. A filter `defaults`
// does not name gets no chip, so a caller that passes no defaults gets no chips.
export function filterChips(filters, defaults = {}, windows = {}) {
  const chips = [];
  if (Array.isArray(defaults.seniorities)) {
    const picked = (filters.seniorities || []).filter((s) => !defaults.seniorities.includes(s));
    // The order of the buttons above the chart, not the order they were clicked in.
    for (const s of [...SENIORITIES.filter((x) => picked.includes(x)), ...picked.filter((x) => !SENIORITIES.includes(x))]) {
      chips.push({ key: `seniority-${s}`, label: cap(s), reset: (f) => ({ ...f, seniorities: f.seniorities.filter((x) => x !== s) }) });
    }
  }
  for (const key of ["german", "production", "degree", "window"]) {
    if (!(key in defaults) || filters[key] == null || filters[key] === defaults[key]) continue;
    chips.push({ key, label: WORDS[key](filters[key], windows), reset: (f) => ({ ...f, [key]: defaults[key] }) });
  }
  return chips;
}

// "Required only" decides how a selected skill is matched: listed as required, or listed
// at all. So it changes which jobs are listed only while a skill is selected, and that is
// the only time it gets a chip. Returns the chip, or null.
export function requirementChip(filters, defaults = {}, requirements = {}) {
  if (!("requirement" in defaults) || filters.requirement == null || filters.requirement === defaults.requirement) return null;
  if (!(filters.skillIds || []).length) return null;
  return { key: "requirement", label: requirements[filters.requirement] || filters.requirement,
    reset: (f) => ({ ...f, requirement: defaults.requirement }) };
}

// "Clear filters": every chip showing goes back to its default, and the selected skills
// with them. City, job family and the search box are left as they are.
export const clearChips = (chips) => (f) => ({ ...chips.reduce((g, chip) => chip.reset(g), f), skillIds: [] });
