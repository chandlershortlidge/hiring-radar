// HIR-263: at phone width the header's "Add a job" button shows only a plus sign. Its
// words are hidden with display:none, which removes them for screen readers too, and the
// button had no other name — so it was announced as just "button", and the robot visitor
// (e2e/site-watch.spec.js) had to find it by its place in the header.
//
// The words being hidden is CSS, so the thing to hold on to is a name that does not
// depend on them: an aria-label on the button itself, as its two neighbours already have.
//
// Renders the page the way the browser's first paint does (no jsdom: the page only
// touches the document from effects, which do not run here). The one thing it reads
// while rendering is the address bar, so that is all the stand-in window provides.
import { describe, it, expect, beforeAll, afterAll, vi } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import App from "./App.jsx";

let buttons;

beforeAll(() => {
  vi.stubGlobal("window", { location: { pathname: "/", search: "", hash: "" } });
  const html = renderToStaticMarkup(<App />);
  const actions = html.match(/<div class="hdr-actions">(.*?)<\/div>/s);
  buttons = actions ? actions[1].match(/<button\b[^>]*>/g) : null;
});

afterAll(() => vi.unstubAllGlobals());

describe("the header's buttons", () => {
  it("are the three the page has always had", () => {
    expect(buttons).toHaveLength(3);
  });

  it('names the add-a-job button "Add a job" without relying on its visible words', () => {
    const add = buttons.filter((b) => b.includes('class="btn outline"'));
    expect(add).toHaveLength(1);
    expect(add[0]).toContain('aria-label="Add a job"');
  });

  it("leaves no header button whose only name is words a phone hides", () => {
    for (const b of buttons) expect(b).toMatch(/aria-label="[^"]+"/);
  });
});
