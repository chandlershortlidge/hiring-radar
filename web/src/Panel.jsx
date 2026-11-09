import { Component } from "react";
import { Warn } from "./icons.jsx";

// A safety net around one part of the page (HIR-227). React unmounts the entire tree when
// a render throws and nothing catches it: that is how one wrong value in the add-a-job
// drawer turned the whole dashboard white, with no error text to go on. Each panel and
// each drawer sits inside one of these, so a failure costs that one box and the rest of
// the page stays up and usable.
//
// It has to be a class: getDerivedStateFromError / componentDidCatch have no hook form.
export default class Panel extends Component {
  constructor(props) {
    super(props);
    this.state = { failed: false };
  }

  static getDerivedStateFromError() {
    return { failed: true };
  }

  componentDidCatch(error, info) {
    // Nothing collects browser errors yet, so the console is where this is read from.
    console.error(`[hiring-radar] ${this.props.label || "a panel"} failed to render`, error, info);
  }

  render() {
    if (!this.state.failed) return this.props.children;
    return (
      <div className="note warn" role="alert">
        <Warn />
        <span>
          <b>{this.props.label || "This part of the page"} couldn't load.</b> The rest of the page still works.
          Reloading usually fixes it; if it doesn't, the browser console has the detail.
        </span>
      </div>
    );
  }
}
