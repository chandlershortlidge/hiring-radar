"""How an AI agent finds the MCP server from the site (HIR-480).

Does: build, from the running MCP server's own tool list, the documents an agent reads to
learn where the server lives and what it offers:
- the AI Catalog at /.well-known/ai-catalog.json: the site-wide list of agent endpoints,
  which points to the Server Card (the MCP draft's discovery flow);
- the Server Card at /mcp/server-card (the address the draft reserves: the MCP URL plus
  "/server-card"), also at /.well-known/mcp/server-card.json and /.well-known/mcp.json,
  the addresses earlier drafts proposed and some tools still try;
- /llms.txt: the same facts in plain words for an agent that reads text.
Format and addresses: decisions/2026-11-27-hir-480-agent-discovery.md.

Does NOT: list the server in the public MCP Registry (that entry is a static file,
deploy/mcp-registry/server.json, published by hand), or open these addresses past the
password: deploy/Caddyfile does that, and tests/test_discovery.py checks it.

Invariants: every tool the server registers is named in the card and in llms.txt, because
both are built from `server.list_tools()` at request time, never typed out by hand.
"""

from typing import Any

from mcp.server.mcpserver import MCPServer
# The protocol versions the server answers, from the modules that route requests on them
# (as app/mcp_server.py does): the ones with a handshake, and the newest, without one.
from mcp.server.lowlevel.server import MODERN_PROTOCOL_VERSIONS
from mcp.server.streamable_http_manager import HANDSHAKE_PROTOCOL_VERSIONS

from app import mcp_server

SITE = "https://hiringradar.app"
MCP_URL = SITE + mcp_server.PATH
CARD_PATH = mcp_server.PATH + "/server-card"
CARD_PATHS = (CARD_PATH, "/.well-known/mcp/server-card.json", "/.well-known/mcp.json")
CATALOG_PATH = "/.well-known/ai-catalog.json"
LLMS_PATH = "/llms.txt"
OPEN_PATHS = (*CARD_PATHS, CATALOG_PATH, LLMS_PATH)  # answered without the dashboard password

# The registry-style name (reverse DNS of the domain), the same in the card and in
# deploy/mcp-registry/server.json.
NAME = "app.hiringradar/hiring-radar"
TITLE = "Hiring Radar"
# At most 100 characters: the MCP Registry refuses a longer description.
DESCRIPTION = "Read-only AI/ML job-market data: which skills job postings ask for, by city, seniority and role."
ACCESS = "No sign-in. Read-only. Rate limited per connection."

CARD_SCHEMA = "https://static.modelcontextprotocol.io/schemas/v1/server-card.schema.json"
CARD_TYPE = "application/mcp-server-card+json"
CATALOG_TYPE = "application/ai-catalog+json"
META_KEY = "app.hiringradar/discovery"

# What the draft asks of a hosted card: anyone may read it, and it may be cached for an hour.
CARD_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type, If-None-Match",
    "Cache-Control": "public, max-age=3600",
}


def _summary(description: str | None) -> str:
    """A tool's first paragraph on one line: what it does, without its argument notes."""
    first = (description or "").strip().split("\n\n")[0]
    return " ".join(first.split())


async def tools(server: MCPServer) -> list[dict[str, str]]:
    return [{"name": t.name, "description": _summary(t.description)} for t in await server.list_tools()]


async def resources(server: MCPServer) -> list[dict[str, str]]:
    return [{"uri": str(r.uri), "name": r.name, "description": _summary(r.description)}
            for r in await server.list_resources()]


async def server_card(server: MCPServer) -> dict[str, Any]:
    return {
        "$schema": CARD_SCHEMA,
        "name": NAME,
        "title": TITLE,
        "version": mcp_server.VERSION,
        "description": DESCRIPTION,
        "websiteUrl": SITE,
        "remotes": [{"type": "streamable-http", "url": MCP_URL,
                     "supportedProtocolVersions": [*HANDSHAKE_PROTOCOL_VERSIONS, *MODERN_PROTOCOL_VERSIONS]}],
        # The draft leaves tools out of the card (a client lists them once connected); they
        # are here under our own namespace because the card is also what a person or an
        # agent reads before deciding to connect.
        "_meta": {META_KEY: {"access": ACCESS, "tools": await tools(server),
                             "resources": await resources(server), "llmsTxt": SITE + LLMS_PATH}},
    }


def catalog() -> dict[str, Any]:
    return {"specVersion": "1.0",
            "entries": [{"identifier": "urn:air:hiringradar.app:mcp:hiring-radar",
                         "type": CARD_TYPE, "url": SITE + CARD_PATH}]}


async def llms_txt(server: MCPServer) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "> Hiring Radar tracks AI and machine-learning job postings in Europe and the US and reads "
        "each one into a fixed list of skills, each marked required or nice-to-have, plus seniority, "
        "German, degree and production-experience requirements.",
        "",
        "Its data is open to AI agents through an MCP server (Model Context Protocol):",
        "",
        f"- MCP endpoint: {MCP_URL}",
        "- Transport: Streamable HTTP",
        f"- Access: {ACCESS}",
        f"- Server card: {SITE + CARD_PATH}",
        "",
        "## Tools",
        "",
        *(f"- {t['name']}: {t['description']}" for t in await tools(server)),
        "",
        "## Resources",
        "",
        *(f"- {r['uri']}: {r['description']}" for r in await resources(server)),
        "",
    ]
    return "\n".join(lines)
