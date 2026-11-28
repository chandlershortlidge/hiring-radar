// HIR-232: the "What's rising" panel. The server decides what is shown; what is checked
// here is that each of its answers is worded for a person: a rise and a fall with the job
// counts behind them, and "not enough data yet" with the reason and the date it fills in.
import { describe, it, expect } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { RisingView, dayMonth, leftOut, waiting } from "./RisingSkills.jsx";

const periods = { current: { open_jobs: 80 }, previous: { open_jobs: 82 } };
const agents = { skill_id: "agents", display: "Agents", current_count: 33, previous_count: 24, current_share: 41.3, previous_share: 29.3, change: 12 };
const docker = { skill_id: "docker", display: "Docker", current_count: 8, previous_count: 16, current_share: 10, previous_share: 19.5, change: -9.5 };
const html = (data) => renderToStaticMarkup(<RisingView data={data} place="Berlin" role="AI Engineer jobs" />)
  .replace(/<!-- -->/g, "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");

describe("what's rising", () => {
  it("shows a rise and a fall with the counts behind each", () => {
    const text = html({ status: "ok", ...periods, risers: [agents], fallers: [docker] });
    expect(text).toContain("What’s rising in Berlin");
    expect(text).toContain("Agents 41% · up from 29% 33 of 80 jobs, was 24 of 82");
    expect(text).toContain("Docker 10% · down from 20% 8 of 80 jobs, was 16 of 82");
    expect(text).not.toContain("Not enough data yet");
  });

  it("says so when nothing fell", () => {
    const text = html({ status: "ok", ...periods, risers: [agents], fallers: [] });
    expect(text).toContain("Falling None by a point or more.");
  });

  it("tells a new city's visitor when the panel fills in", () => {
    const text = html({ status: "not_enough_data", reason: "new_city", ready_from: "2027-01-03", risers: [], fallers: [] });
    expect(text).toContain("Not enough data yet.");
    expect(text).toContain("This fills in from about 3 January.");
    expect(text).not.toContain("Rising");
  });

  it("says there are too few jobs when that is the reason", () => {
    const data = { status: "not_enough_data", reason: "few_jobs", ready_from: null };
    expect(waiting(data, "Berlin", "AI Engineer jobs")).toBe("Too few open AI Engineer jobs in Berlin over the last 8 weeks to compare.");
  });

  it("gives no date it does not have", () => {
    expect(waiting({ reason: "new_city", ready_from: null }, "Paris", "jobs")).toBe("");
  });

  it("names the places too new to count, grouped by the day they join", () => {
    const places = { included: ["Berlin", "Munich"], excluded: [
      { place: "Seattle", ready_from: "2027-01-14" }, { place: "Austin", ready_from: "2027-01-14" },
      { place: "Hamburg", ready_from: "2027-01-03" }] };
    const text = html({ status: "ok", ...periods, risers: [agents], fallers: [], places });
    expect(text).toContain("Not yet counted, collected too recently to compare: Hamburg (from 3 January); Seattle, Austin (from 14 January).");
  });

  it("says nothing about left-out places when every place is counted", () => {
    expect(leftOut({ places: { included: ["Berlin"], excluded: [] } })).toBe("");
    expect(leftOut({ places: { included: [], excluded: [{ place: "Paris", ready_from: null }] } })).toBe("");
    expect(leftOut({})).toBe("");
  });

  it("draws nothing until the answer arrives", () => {
    expect(renderToStaticMarkup(<RisingView data={null} place="Berlin" role="jobs" />)).toBe("");
  });

  it("reads the date as a calendar day", () => {
    expect(dayMonth("2026-12-13")).toBe("13 December");
  });
});
