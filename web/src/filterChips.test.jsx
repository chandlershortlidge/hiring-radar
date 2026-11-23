// HIR-415: the jobs card names the chart's filters that are switched on, as removable chips.
//
// Covers: which filters get a chip and what it reads (filterChips.js); that removing a
// chip puts exactly that filter back to its default; "Clear filters"; and what the jobs
// card's header draws, read off its first paint the way JobList.test.jsx does (no jsdom,
// so nothing is fetched and no click is simulated: the clicks are tested on the pure
// functions the buttons call).
//
// Does NOT cover: the chart's control changing when a chip is removed. Both read the same
// filters object, so there is nothing to keep in step; the PR screenshots show it. Nor the
// wrapping at phone width, which is CSS.
import { describe, it, expect } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import JobList from "./JobList.jsx";
import { DEFAULT } from "./App.jsx";
import { clearChips, filterChips, requirementChip } from "./filterChips.js";
import { germanLabel } from "./FilterPills.jsx";
import { DEGREE_FILTERS, GERMAN_FILTERS, PRODUCTION_FILTERS } from "./format.js";

const WINDOWS = { open: "Currently open", "30d": "Last 30 days", "90d": "Last 90 days", all: "All" };
const REQUIREMENTS = { required: "Required only", all: "Required + nice-to-have" };
const labels = (filters) => filterChips(filters, DEFAULT, WINDOWS).map((c) => c.label);
const berlin = { ...DEFAULT, cities: ["Berlin"] };

describe("which filters get a chip", () => {
  it("none when every filter is at its default", () => {
    expect(labels(berlin)).toEqual([]);
  });

  it("city, job family, the search box and the selected skills never do", () => {
    expect(labels({ ...berlin, families: ["ai_engineering"], query: "acme", text: "rag", skillIds: ["python"] })).toEqual([]);
  });

  it("one per picked seniority level, in the order of the buttons above the chart", () => {
    expect(labels({ ...berlin, seniorities: ["senior", "junior"] })).toEqual(["Junior", "Senior"]);
  });

  it.each([
    ["german", "not_required", "German: not required"],
    ["german", "required", "German: required"],
    ["production", "not_required", "Production experience: not required"],
    ["production", "required", "Production experience: required"],
    ["degree", "open", "Degree: open without one"],
    ["degree", "required", "Degree required"],
    ["window", "30d", "Last 30 days"],
    ["window", "90d", "Last 90 days"],
    ["window", "all", "Time window: all"],
  ])("%s = %s reads “%s”", (key, value, label) => {
    expect(labels({ ...berlin, [key]: value })).toEqual([label]);
  });

  it("every option of every filter gets words, never a blank or a raw key", () => {
    const options = { german: GERMAN_FILTERS, production: PRODUCTION_FILTERS, degree: DEGREE_FILTERS, window: WINDOWS };
    for (const [key, choices] of Object.entries(options)) {
      for (const value of Object.keys(choices).filter((v) => v !== DEFAULT[key])) {
        const [label] = labels({ ...berlin, [key]: value });
        expect(label, `${key}=${value}`).toBeTruthy();
        expect(label, `${key}=${value}`).not.toBe(value);
      }
    }
  });

  it("the German chip reads what the German control above the chart reads", () => {
    expect(labels({ ...berlin, german: "none" })).toEqual([germanLabel("none")]);
  });

  it("the order is seniority, German, production experience, degree, time window", () => {
    expect(labels({ ...berlin, window: "30d", degree: "required", production: "required", german: "required", seniorities: ["mid"] }))
      .toEqual(["Mid", "German: required", "Production experience: required", "Degree required", "Last 30 days"]);
  });

  it("no defaults handed in: no chips, rather than a chip for everything", () => {
    expect(filterChips({ ...berlin, seniorities: ["junior"], german: "required" })).toEqual([]);
  });
});

describe("removing a chip", () => {
  const on = { ...berlin, seniorities: ["junior", "senior"], german: "required", window: "30d", skillIds: ["python"] };
  const remove = (label) => filterChips(on, DEFAULT, WINDOWS).find((c) => c.label === label).reset(on);

  it("a seniority chip takes off that level and leaves the other", () => {
    expect(remove("Junior")).toEqual({ ...on, seniorities: ["senior"] });
  });

  it("a one-choice chip puts that filter back to its default and touches nothing else", () => {
    expect(remove("German: required")).toEqual({ ...on, german: DEFAULT.german });
    expect(remove("Last 30 days")).toEqual({ ...on, window: DEFAULT.window });
  });

  it("Clear filters resets every chip and the selected skills, not city, family or search", () => {
    const all = { ...on, families: ["ai_engineering"], query: "acme", requirement: "all" };
    const chips = [...filterChips(all, DEFAULT, WINDOWS), requirementChip(all, DEFAULT, REQUIREMENTS)];
    expect(clearChips(chips)(all)).toEqual({ ...berlin, families: ["ai_engineering"], query: "acme" });
  });
});

describe("“Required only”", () => {
  it("gets no chip while no skill is selected: it does not change which jobs are listed", () => {
    expect(requirementChip({ ...berlin, requirement: "all" }, DEFAULT, REQUIREMENTS)).toBeNull();
  });

  it("gets no chip at its default", () => {
    expect(requirementChip({ ...berlin, skillIds: ["python"] }, DEFAULT, REQUIREMENTS)).toBeNull();
  });

  it("switched off with a skill selected, the list is wider, so it gets a chip that switches it back on", () => {
    const f = { ...berlin, requirement: "all", skillIds: ["python"] };
    const chip = requirementChip(f, DEFAULT, REQUIREMENTS);
    expect(chip.label).toBe("Required + nice-to-have");
    expect(chip.reset(f)).toEqual({ ...f, requirement: "required" });
  });
});

describe("the jobs card's header", () => {
  const head = (filters, props = { defaults: DEFAULT, windows: WINDOWS, requirements: REQUIREMENTS }) => {
    const html = renderToStaticMarkup(<JobList filters={filters} setFilters={() => {}} profile={null} taxonomy={{ python: "Python" }} {...props} />);
    return html.match(/<div class="jobs-head"><div class="l">(.*?)<\/div><div class="r">/s)[1];
  };
  const chipWords = (html) => [...html.matchAll(/<span class="chip-filter">([^<]*)</g)].map((m) => m[1]);

  it("with every filter at its default it is exactly what it is with no chips at all", () => {
    expect(head(berlin)).toBe(head(berlin, {}));
    expect(head(berlin)).not.toContain("chip-filter");
    expect(head(berlin)).not.toContain("Clear filters");
  });

  it("Junior picked above the chart: a Junior chip with a remove button, and no Clear filters for one chip", () => {
    const html = head({ ...berlin, seniorities: ["junior"] });
    expect(chipWords(html)).toEqual(["Junior"]);
    expect(html).toContain('aria-label="Remove the Junior filter"');
    expect(html).not.toContain("Clear filters");
  });

  it("two chips: Clear filters appears, after the chips", () => {
    const html = head({ ...berlin, seniorities: ["junior"], window: "30d" });
    expect(chipWords(html)).toEqual(["Junior", "Last 30 days"]);
    expect(html.indexOf("Clear filters")).toBeGreaterThan(html.indexOf("Last 30 days"));
  });

  it("a filter chip and a skill chip count as two", () => {
    const html = head({ ...berlin, german: "not_required", skillIds: ["python"] });
    expect(chipWords(html)).toEqual(["German: not required", "Python"]);
    expect(html).toContain("Clear filters");
  });

  it("one skill chip alone is as it was: no Clear filters", () => {
    expect(head({ ...berlin, skillIds: ["python"] })).not.toContain("Clear filters");
  });
});
