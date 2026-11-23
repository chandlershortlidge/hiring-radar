// The robot visitor for the MCP (HIR-366): connects to the LIVE site's /mcp the way a
// user's Claude does (over the public address, JSON-RPC over HTTP), lists the tools, and
// calls each one with its example request from app/mcp_examples.json.
//
// Does: one test per tool, named after its example ("MCP tool search_jobs: search for open
// AI engineer jobs in Berlin"), so a failure names the tool and the ticket filed by
// scripts/site_watch_ticket.py is titled after it; the error holds what the tool answered.
// One more test checks the live tool list against the examples, both ways: a tool missing
// from the site fails, and so does a live tool with no example, so none goes unchecked.
// Does NOT: write anything (every tool is read-only), call a model, or sign in. Sends the
// site's login (WATCH_AUTH) when given, because the server's front door may still ask for
// it on /mcp; once /mcp is open the header is simply ignored.
//
// Env: WATCH_URL (the site's origin), WATCH_AUTH ("user:password", optional). Without
// WATCH_URL every test is skipped. Runs as the "mcp" project in playwright.watch.config.js.
import { test, request as pwRequest } from "@playwright/test";
import { readFileSync } from "node:fs";

const EXAMPLES_FILE = new URL("../../app/mcp_examples.json", import.meta.url);
const { _about, ...EXAMPLES } = JSON.parse(readFileSync(EXAMPLES_FILE, "utf8"));
const PROTOCOL = "2025-06-18";
const SHOW = 1500; // characters of a tool's answer quoted in a failure

test.skip(!process.env.WATCH_URL, "WATCH_URL not set");

// One MCP session, as a client opens it: initialize, then say so, then requests.
async function connect() {
  const [username, ...rest] = (process.env.WATCH_AUTH || "").split(":");
  const http = await pwRequest.newContext({
    baseURL: process.env.WATCH_URL,
    httpCredentials: username ? { username, password: rest.join(":"), send: "always" } : undefined,
  });
  let id = 0;
  async function rpc(method, params, notify = false) {
    const res = await http.post("/mcp", {
      headers: { accept: "application/json, text/event-stream", "content-type": "application/json",
                 "mcp-protocol-version": PROTOCOL },
      data: notify ? { jsonrpc: "2.0", method, params } : { jsonrpc: "2.0", id: ++id, method, params },
    });
    const body = await res.text();
    if (!res.ok()) throw new Error(`${method}: HTTP ${res.status()} from /mcp: ${body.slice(0, SHOW) || "(empty)"}`);
    if (notify) return null;
    let msg;
    try { msg = JSON.parse(body); } catch { throw new Error(`${method}: /mcp did not answer JSON: ${body.slice(0, SHOW)}`); }
    if (msg.error) throw new Error(`${method}: /mcp answered an error: ${JSON.stringify(msg.error).slice(0, SHOW)}`);
    return msg.result;
  }
  const init = await rpc("initialize", { protocolVersion: PROTOCOL, capabilities: {},
                                         clientInfo: { name: "hiring-radar robot visitor", version: "1" } });
  if (init?.serverInfo?.name !== "hiring-radar") throw new Error(`initialize: the server did not say it is hiring-radar: ${JSON.stringify(init).slice(0, SHOW)}`);
  await rpc("notifications/initialized", {}, true);
  return { rpc, close: () => http.dispose() };
}

// A tool's answer, or a failure that says what it returned instead.
async function callTool(mcp, name, args) {
  const r = await mcp.rpc("tools/call", { name, arguments: args });
  const text = (r?.content || []).map((c) => c.text || "").join("\n");
  if (r?.isError) throw new Error(`${name} answered with an error: ${text.slice(0, SHOW)}`);
  if (!r?.structuredContent) throw new Error(`${name} answered with no data: ${text.slice(0, SHOW) || "(nothing)"}`);
  return r.structuredContent;
}

// Arguments with every {from, path} filled in from that tool's own example answer.
async function resolveArgs(mcp, args, seen = []) {
  const out = {};
  for (const [k, v] of Object.entries(args)) {
    if (v && typeof v === "object" && !Array.isArray(v) && "from" in v) {
      if (seen.includes(v.from)) throw new Error(`examples refer to each other in a loop: ${[...seen, v.from].join(" → ")}`);
      const ex = EXAMPLES[v.from];
      if (!ex) throw new Error(`argument ${k} is taken from ${v.from}, which has no example`);
      const answer = await callTool(mcp, v.from, await resolveArgs(mcp, ex.arguments, [...seen, v.from]));
      const value = v.path.split(".").reduce((o, p) => (o == null ? undefined : o[p]), answer);
      if (value == null) throw new Error(`argument ${k}: ${v.from} answered without ${v.path}: ${JSON.stringify(answer).slice(0, SHOW)}`);
      out[k] = value;
    } else out[k] = v;
  }
  return out;
}

const empty = (v) => v == null || v === "" || v === 0 || (Array.isArray(v) && !v.length)
  || (typeof v === "object" && !Array.isArray(v) && !Object.keys(v).length);

// The paths of `expect` that the answer does not hold. Same rules as tests/test_mcp_examples.py.
function missing(answer, path) {
  const [head, ...rest] = path.split(".");
  const list = head.endsWith("[]");
  const v = answer?.[list ? head.slice(0, -2) : head];
  if (empty(v)) return [path];
  if (!rest.length) return [];
  if (!list) return missing(v, rest.join("."));
  return v.flatMap((item, i) => missing(item, rest.join(".")).map((m) => `${head.slice(0, -2)}[${i}].${m}`));
}

test("MCP lists every tool, and each has an example request", async () => {
  const mcp = await connect();
  try {
    const live = ((await mcp.rpc("tools/list", {}))?.tools || []).map((t) => t.name);
    const gone = Object.keys(EXAMPLES).filter((n) => !live.includes(n));
    const unchecked = live.filter((n) => !(n in EXAMPLES));
    if (gone.length) throw new Error(`tools missing from the live MCP: ${gone.join(", ")} (it lists: ${live.join(", ") || "nothing"})`);
    if (unchecked.length) throw new Error(`live tools with no example request in app/mcp_examples.json, so nothing checks them: ${unchecked.join(", ")}`);
  } finally {
    await mcp.close();
  }
});

for (const [name, ex] of Object.entries(EXAMPLES)) {
  test(`MCP tool ${name}: ${ex.ask}`, async () => {
    const mcp = await connect();
    try {
      const args = await resolveArgs(mcp, ex.arguments, [name]);
      const answer = await callTool(mcp, name, args);
      const gaps = ex.expect.flatMap((p) => missing(answer, p));
      if (gaps.length) {
        throw new Error(`${name}(${JSON.stringify(args)}) answered, but this was empty or missing: ` +
                        `${gaps.slice(0, 5).join(", ")}. It returned: ${JSON.stringify(answer).slice(0, SHOW)}`);
      }
    } finally {
      await mcp.close();
    }
  });
}
