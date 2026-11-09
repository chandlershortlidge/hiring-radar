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
import AddJobDrawer from "./AddJobDrawer.jsx";
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
