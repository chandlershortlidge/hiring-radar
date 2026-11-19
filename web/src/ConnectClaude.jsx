// The two places the site points at connecting Claude to it (HIR-285): a coral-outlined
// pill in the header on every page, and a small plum strip, under the hero on the home
// page and on top of the jobs list on a city page. Chandler asked for it to be
// highlighted and rejected a full-width band as "very distracting".
//
// Neither is a button or a link yet. The Claude connection is not built, so there is
// nothing to open, and a control that does nothing is worse than a label that says so.
// The wording is a placeholder until the launch wording is settled. When the connection
// exists, the strip's "not available yet" becomes its button and the pill becomes a link.
export function ConnectPill() {
  return <span className="pill connect" title="Not available yet">Connect Claude <small>soon</small></span>;
}

export function ConnectStrip() {
  return (
    <aside className="mcp" aria-label="Connect Claude">
      <span><span className="mcp-tag">MCP</span>Connect your Claude to this job board.</span>
      <span className="mcp-soon">Not available yet</span>
    </aside>
  );
}
