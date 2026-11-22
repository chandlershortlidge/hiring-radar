// HIR-227: clicking "Add a job" blanked the whole dashboard. The city list in format.js
// became a list of records ({ name, slug, group }) when the city picker was rebuilt
// (HIR-188), and this drawer still rendered each entry straight into an <option>. React
// throws on an object used as a child, and an uncaught throw during render unmounts the
// whole tree — a white page, no error text.
//
// The test renders the drawer the way the browser's first paint does (no jsdom needed:
// the drawer only touches the document from an effect, which does not run here). If
// anything in the drawer throws on render again, this fails.
import { describe, it, expect } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import AddJobDrawer, { Result } from "./AddJobDrawer.jsx";
import { PLACE_NAMES } from "./format.js";

const render = () =>
  renderToStaticMarkup(<AddJobDrawer onClose={() => {}} onAdded={() => {}} onViewJob={() => {}} />);

describe("the add-a-job drawer", () => {
  it("renders without throwing", () => {
    expect(() => render()).not.toThrow();
  });

  it("offers every place by name in the city dropdown", () => {
    const html = render();
    for (const name of PLACE_NAMES) {
      expect(html).toContain(`>${name}</option>`);
    }
    // The bug's signature: a record printed instead of a name.
    expect(html).not.toContain("[object Object]");
    expect(html).not.toContain("slug");
  });

  it("starts on a real place, not a record", () => {
    expect(render()).toContain('<option selected="">Berlin</option>');
  });
});

// HIR-213: a posting turned away on purpose (no company, or a city we don't collect) was
// reported as "Something went wrong" plus the server's code word. Nothing went wrong, and
// the message named neither the rule nor what to do. The outcome strings are the ones
// /api/add/* really sends: app/ingest.py's skipped kinds.
describe("what the drawer says when a posting was turned away", () => {
  const say = (r) => renderToStaticMarkup(<Result r={r} onViewJob={() => {}} onText={() => {}} />);

  it("names the missing company and says to type it in", () => {
    const html = say({ outcome: "skipped_company", job_id: null });
    expect(html).toContain("we need a company name");
    expect(html).toContain("Type the company in and try again");
    expect(html).not.toContain("Something went wrong");
    expect(html).not.toContain("skipped_company");
  });

  it("names the untracked city", () => {
    const html = say({ outcome: "skipped_city", job_id: null });
    expect(html).toContain("a city we don&#x27;t track");
    expect(html).not.toContain("Something went wrong");
    expect(html).not.toContain("skipped_city");
  });

  it("still calls a real failure a failure", () => {
    const html = say({ outcome: "error", message: "500 Internal Server Error" });
    expect(html).toContain("Something went wrong");
    expect(html).toContain("500 Internal Server Error");
  });
});

// HIR-324: adding a job stored the one posting and said nothing about the company's other
// jobs. The reply now carries where the company's job board stands, and the drawer says in
// one line whether those jobs will arrive on their own.
describe("what the drawer says about the company's other jobs after an add", () => {
  const say = (board) => renderToStaticMarkup(
    <Result r={{ outcome: "added", job_id: 7, skills_found: 3, proposed: 0, failed: [], board }} onViewJob={() => {}} onText={() => {}} />);
  const WILL = "We&#x27;ll also collect this company&#x27;s other jobs from tomorrow.";
  const CANNOT = "This company&#x27;s jobs can&#x27;t be collected automatically yet.";

  it("says the other jobs will be collected when the board was just queued", () => {
    const html = say("queued");
    expect(html).toContain(WILL);
    expect(html).not.toContain(CANNOT);
    expect(html).toContain("3 skills found");   // the line it joins is still there
    expect(html).toContain("View row");
  });

  it("says they cannot be collected when there is no board we can read", () => {
    const html = say("none");
    expect(html).toContain(CANNOT);
    expect(html).not.toContain(WILL);
  });

  it("says we already collect them when the board is in the list", () => {
    const html = say("collected");
    expect(html).toContain("We already collect this company&#x27;s other jobs.");
    expect(html).not.toContain("from tomorrow");
  });

  it("says nothing either way when the add came with no link", () => {
    for (const board of [null, undefined]) {
      const html = say(board);
      expect(html).not.toContain("other jobs");
      expect(html).not.toContain("collected automatically");
    }
  });
});
