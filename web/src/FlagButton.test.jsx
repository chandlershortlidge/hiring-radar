// HIR-226: the flag button's two states and the note offered after the click. Rendered to
// markup, as the other component tests here are (no browser): the state comes in as the
// object `useFlag` returns, so what is checked is what each state looks like and says.
import { describe, it, expect } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { FlagNote, FlagToggle, NOTE_MAX } from "./FlagButton.jsx";

const state = (over = {}) => ({ on: false, busy: false, toggle() {}, noteOpen: false, note: "", setNote() {}, saveNote() {}, closeNote() {}, ...over });
const NAME = "Acme — Senior Staff Software Engineer";

describe("the doesn't-belong-here button", () => {
  it("is an unpressed button that names the job, with no words in a list row", () => {
    const html = renderToStaticMarkup(<FlagToggle flag={state()} name={NAME} />);
    expect(html).toContain('aria-pressed="false"');
    expect(html).toContain(`aria-label="Flag ${NAME}: doesn&#x27;t belong here"`);
    expect(html).not.toContain("<span>");
  });

  it("is pressed once flagged and says a second click removes the flag", () => {
    const html = renderToStaticMarkup(<FlagToggle flag={state({ on: true })} name={NAME} />);
    expect(html).toContain('aria-pressed="true"');
    expect(html).toContain('class="flag on"');
    expect(html).toContain("Click to remove the flag");
  });

  it("spells itself out on the job's own page, and confirms with Flagged", () => {
    expect(renderToStaticMarkup(<FlagToggle flag={state()} name={NAME} withText />)).toContain("<span>Doesn&#x27;t belong here</span>");
    expect(renderToStaticMarkup(<FlagToggle flag={state({ on: true })} name={NAME} withText />)).toContain("<span>Flagged</span>");
  });

  it("cannot be clicked twice while the first click is being stored", () => {
    expect(renderToStaticMarkup(<FlagToggle flag={state({ busy: true })} name={NAME} />)).toContain("disabled");
  });
});

describe("the optional note", () => {
  it("is not there until a job has just been flagged", () => {
    expect(renderToStaticMarkup(<FlagNote flag={state()} id="n" />)).toBe("");
  });

  it("confirms the flag and offers one optional line", () => {
    const html = renderToStaticMarkup(<FlagNote flag={state({ on: true, noteOpen: true })} id="n" />);
    expect(html).toContain("<b>Flagged.</b>");
    expect(html).toContain("(optional)");
    expect(html).toContain(`maxLength="${NOTE_MAX}"`);
    expect(html).toContain(">Done</button>");   // nothing typed: closing is all there is to do
  });

  it("offers to save once something is typed", () => {
    const html = renderToStaticMarkup(<FlagNote flag={state({ on: true, noteOpen: true, note: "it's a platform role" })} id="n" />);
    expect(html).toContain(">Save note</button>");
  });
});
