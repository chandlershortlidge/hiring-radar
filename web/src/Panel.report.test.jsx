// @vitest-environment jsdom
// HIR-259: an error a panel's "couldn't load" box catches never reaches the page-wide
// handler, so the box reports it itself. Rendered for real here, because React only calls
// a box's catch step when a child actually throws in a browser-like render.
import { describe, it, expect, vi } from "vitest";

vi.mock("@sentry/react", () => ({ init: vi.fn(), captureException: vi.fn() }));
import * as Sentry from "@sentry/react";
import { act } from "react";
import { createRoot } from "react-dom/client";
import Panel from "./Panel.jsx";
import { startErrorReports } from "./errorReports.js";

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

function Broken() {
  throw new Error("chart broke");
}

describe("a panel's safety box", () => {
  it("reports the error it catches, once, with the panel's name", () => {
    startErrorReports("https://k@o1.ingest.de.sentry.io/1");
    const quiet = vi.spyOn(console, "error").mockImplementation(() => {});
    const root = createRoot(document.createElement("div"));
    act(() => root.render(<Panel label="The chart"><Broken /></Panel>));
    quiet.mockRestore();

    expect(Sentry.captureException).toHaveBeenCalledTimes(1);
    const [err, ctx] = Sentry.captureException.mock.calls[0];
    expect(err.message).toBe("chart broke");
    expect(ctx.extra.panel).toBe("The chart");
    act(() => root.unmount());
  });
});
