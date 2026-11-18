"""The MCP server: hiring-radar's data as tools any Claude can call (HIR-103, HIR-338).

Does: build an MCP server (Streamable HTTP, stateless, JSON answers) whose tools read the
same queries the dashboard reads, and give the FastAPI app one endpoint, `/mcp`, that serves
it behind a per-visitor rate limit. Mounted by `app/api.py::create_app`.

Does NOT: write anything, call a model, or run a query of its own. Every tool is a thin
wrapper over a function in app/queries.py, given filters built by `queries.make_filters`,
the same check the dashboard's API uses, so a tool and the dashboard cannot disagree.

Invariants: tools only read and never call a model (AGENTS.md "The MCP server"); one
database connection per tool call; the route is open, with no password, because the data
is public job-market data (Chandler, 17 Nov, HIR-338), and the rate limit is the only gate.

Adding a tool: write a function under "--- tools ---" inside `build_server` (typed
arguments, a docstring written for a model that has never seen the dashboard, the query
call), decorated with `@server.tool(annotations=READ_ONLY)`. Copy `search_jobs` and its
tests in tests/test_mcp_server.py. Which tools come next, and which query each wraps:
the tool table in HIR-103.
"""

import difflib
import math
import time
from collections.abc import Callable
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Literal

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations

from app import db, queries as q
from app.geo import CITIES, REMOTE_EU
from app.taxonomy import Taxonomy

PATH = "/mcp"

# Every tool is read-only and only reads our own database.
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)

# The accepted values, as types the tool's schema shows the model. Built from the same
# constants the API validates against; tests/test_mcp_server.py checks they stay equal.
Place = Literal[*CITIES, REMOTE_EU]  # type: ignore[valid-type]
Seniority = Literal[*q.SENIORITIES]  # type: ignore[valid-type]
Family = Literal[*q.FAMILIES]  # type: ignore[valid-type]
Requirement = Literal[*q.REQUIREMENTS]  # type: ignore[valid-type]
Window = Literal[*q.WINDOWS]  # type: ignore[valid-type]
German = Literal[*q.GERMAN_FILTERS]  # type: ignore[valid-type]
Degree = Literal[*q.DEGREE_FILTERS]  # type: ignore[valid-type]
Production = Literal[*q.PRODUCTION_FILTERS]  # type: ignore[valid-type]
Sort = Literal[*q.SORTS]  # type: ignore[valid-type]

MAX_JOBS = 50  # per call; page with `offset` for more

INSTRUCTIONS = """\
hiring-radar tracks AI and ML job postings (Berlin, Hamburg, Frankfurt, Munich, Remote (EU),
San Francisco, New York) and reads each posting into a fixed list of skills, each marked
required or nice-to-have, plus seniority, German, degree and production-experience
requirements. All tools are read-only."""


def build_server(db_path: Path, tax: Taxonomy, now: Callable[[], str]) -> MCPServer:
    """The MCP server with every tool registered. `now` is injected so tests can fix the
    clock, exactly as the API's routes do."""
    server = MCPServer("hiring-radar", instructions=INSTRUCTIONS)

    @contextmanager
    def connect():
        c = db.connect(db_path, same_thread=False)
        try:
            yield c
        finally:
            c.close()

    def skill_ids(names: list[str]) -> list[str]:
        """Skill ids from ids or names ("RAG", "rag", "Retrieval Augmented Generation")."""
        out = []
        for n in names:
            sid = n if n in tax.skills else tax.resolve(n)
            if sid is None:
                close = difflib.get_close_matches(n.lower(), list(tax.skills), n=3, cutoff=0.6)
                hint = f"; did you mean {', '.join(close)}?" if close else ""
                raise ToolError(f"unknown skill {n!r}{hint}")
            out.append(sid)
        return out

    # --- tools ----------------------------------------------------------------------

    @server.tool(annotations=READ_ONLY)
    def search_jobs(
        skills: list[str] | None = None,
        city: list[Place] | None = None,
        seniority: list[Seniority] | None = None,
        family: list[Family] | None = None,
        requirement: Requirement = "required",
        window: Window = "open",
        german: German = "any",
        degree: Degree = "any",
        production: Production = "any",
        company_or_title: str = "",
        text: str = "",
        sort: Sort = "newest",
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Find job postings, with the same filters and results as the hiring-radar
        dashboard's job list. Every filter is optional; filters combine with AND.

        - skills: skill ids or names, e.g. ["rag", "python"]. A job must list every one.
          Names are matched to our skill list ("RAG", "Retrieval Augmented Generation"
          and "rag" are the same skill); an unknown name is an error that suggests ids.
        - requirement: "required" (default) counts a skill only where the posting requires
          it; "all" also counts it where it is only nice-to-have.
        - city: any of these places; a job in several places matches each of them.
        - seniority: junior, mid or senior. Leaving it out includes jobs whose seniority
          is unknown; naming any level excludes them.
        - family: ai-engineer, ml-engineer, data-scientist, ml-platform or research,
          assigned from the job title.
        - window: "open" (default) = still being advertised; "30d" / "90d" = seen in the
          last 30 / 90 days, open or closed; "all" = every job ever collected.
        - german / production: "any" (default); "none" = the posting does not mention it;
          "not_required" = not mentioned or only nice-to-have; "required" = required.
          production means prior experience shipping to production.
        - degree: "any" (default); "none" = no degree mentioned; "open" = someone without
          a degree can apply (none named, optional, or equivalent experience accepted);
          "required" = a degree is required with no alternative.
        - company_or_title: words that must appear in the company name or job title.
        - text: words that must appear in the posting text, for anything not on the
          skill list (e.g. "on-call", "visa sponsorship").
        - sort: newest (default), oldest, reposts (most re-advertised first), company.
        - limit: jobs per call, 1 to 50 (default 20); offset: skip that many, to page.

        Returns total (all matching jobs), and per job: id, company, title, places, family,
        seniority, first_seen / last_seen (dates we saw it), status (open or closed),
        url (the posting), required_skills and nice_to_have_skills (skill ids),
        and german, degree and production requirements (null = not mentioned).

        Example: open Berlin AI engineer jobs that require RAG:
        search_jobs(skills=["rag"], city=["Berlin"], family=["ai-engineer"])
        """
        if not 1 <= limit <= MAX_JOBS:
            raise ToolError(f"limit must be between 1 and {MAX_JOBS}")
        if offset < 0:
            raise ToolError("offset must be 0 or more")
        try:
            f = q.make_filters(tax.skills, cities=city or (), seniorities=seniority or (),
                               families=family or (), requirement=requirement, window=window,
                               german=german, degree=degree, production=production,
                               skill_ids=skill_ids(skills or []), query=company_or_title, text=text)
        except ValueError as e:
            raise ToolError(str(e)) from None
        with connect() as conn:
            r = q.list_jobs(conn, f, now(), sort, limit, offset)
        return {"total": r["total"], "offset": offset, "jobs": [_job(j) for j in r["jobs"]]}

    # The next tool goes here (HIR-103's table): a function like search_jobs above.

    return server


def _job(j: dict) -> dict:
    """One job as a tool returns it: what a reader needs, not the dashboard's bookkeeping."""
    return {
        "id": j["id"], "company": j["company"], "title": j["title"], "places": j["places"],
        "family": j["family"], "seniority": j["seniority"],
        "first_seen": j["first_seen"][:10], "last_seen": j["last_seen"][:10], "status": j["status"],
        "url": next((s["url"] for s in j["sources"] if s["url"]), None),
        "required_skills": j["required_skills"], "nice_to_have_skills": j["nice_skills"],
        "german": j["german"], "production": j["production"],
        "degree": None if j["degree"] is None else {
            "level": j["degree"], "requirement": j["degree_requirement"],
            "or_equivalent_experience": j["degree_or_equivalent"]},
    }


# --- serving -------------------------------------------------------------------------

# Per visitor (IP address): bursts of up to BURST requests, refilled at RATE a second,
# so 60 a minute sustained. One MCP tool call is one or two requests. Numbers recorded in
# decisions/2026-11-17-hir-338-mcp-open-read-only-rate-limit.md.
BURST = 30
RATE = 1.0
_MAX_VISITORS = 10_000  # forget idle visitors past this, so the table cannot grow forever


class RateLimit:
    """A token bucket per client address in front of an ASGI app; 429 when empty.

    The client address is uvicorn's: the API listens on 127.0.0.1 behind Caddy, and
    uvicorn takes the visitor's address from Caddy's X-Forwarded-For header."""

    def __init__(self, app, burst: int = BURST, rate: float = RATE, clock: Callable[[], float] = time.monotonic):
        self.app, self.burst, self.rate, self.clock = app, burst, rate, clock
        self.buckets: dict[str, tuple[float, float]] = {}  # address -> (tokens, last time)

    def allow(self, who: str) -> float:
        """0 if the request may go ahead, else the seconds until it may."""
        now = self.clock()
        tokens, last = self.buckets.get(who, (self.burst, now))
        tokens = min(self.burst, tokens + (now - last) * self.rate)
        if tokens < 1:
            self.buckets[who] = (tokens, now)
            return (1 - tokens) / self.rate
        if len(self.buckets) >= _MAX_VISITORS and who not in self.buckets:
            full = [k for k, (t, at) in self.buckets.items() if t + (now - at) * self.rate >= self.burst]
            for k in full or list(self.buckets):
                del self.buckets[k]
        self.buckets[who] = (tokens - 1, now)
        return 0.0

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            wait = self.allow((scope.get("client") or ("unknown",))[0])
            if wait:
                await send({"type": "http.response.start", "status": 429,
                            "headers": [(b"retry-after", str(math.ceil(wait)).encode()),
                                        (b"content-type", b"text/plain")]})
                await send({"type": "http.response.body", "body": b"Too many requests: slow down.\n"})
                return
        await self.app(scope, receive, send)


def endpoint(server: MCPServer) -> RateLimit:
    """The ASGI app the FastAPI app serves at PATH, rate limited. The app's lifespan must
    run `server.session_manager.run()`."""
    inner = server.streamable_http_app(
        streamable_http_path=PATH, stateless_http=True, json_response=True,
        # The SDK's DNS-rebinding guard defends a server on a visitor's own machine; this one
        # is public, holds no credentials and only reads public data, and Caddy fixes the host.
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))
    (route,) = [r for r in inner.routes if getattr(r, "path", None) == PATH]
    return RateLimit(route.app)
