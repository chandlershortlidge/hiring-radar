// HIR-227: the safety net around each panel and drawer. The white page happened because a
// render error had nothing to stop it, so the test that matters here is that a failure
// turns into one small message naming the part that broke, and that a healthy panel is
// passed straight through untouched.
//
// Panel is a class component, so its two halves can be checked without a browser: the
// state React puts it in when a child throws, and what it renders in that state.
import { describe, it, expect, vi } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import Panel from "./Panel.jsx";

const failed = (label) => {
  const p = new Panel({ label, children: null });
  p.state = Panel.getDerivedStateFromError(new Error("boom"));
  return renderToStaticMarkup(p.render());
};

describe("the panel safety net", () => {
  it("passes a healthy panel through unchanged", () => {
    expect(renderToStaticMarkup(<Panel label="The chart"><p>all fine</p></Panel>)).toBe("<p>all fine</p>");
  });

  it("replaces a broken panel with a message that names it", () => {
    const html = failed("The chart");
    expect(html).toContain("The chart couldn&#x27;t load");
    expect(html).toContain("The rest of the page still works");
    expect(html).toContain('role="alert"');
  });

  it("still says something useful with no label", () => {
    expect(failed(undefined)).toContain("This part of the page couldn&#x27;t load");
  });

  it("writes the failure to the browser console, which is all that collects them today", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    const p = new Panel({ label: "The job list", children: null });
    const err = new Error("boom");
    p.componentDidCatch(err, { componentStack: "" });
    expect(spy).toHaveBeenCalledWith(expect.stringContaining("The job list failed to render"), err, expect.anything());
    spy.mockRestore();
  });
});
