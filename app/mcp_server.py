"""The MCP server: hiring-radar's data as tools any Claude can call (HIR-103, HIR-338).

Does: build an MCP server (Streamable HTTP, stateless, JSON answers) whose tools read the
same queries the dashboard reads, and give the FastAPI app one endpoint, `/mcp`, that serves
it behind a rate limit per connection. Mounted by `app/api.py::create_app`.

Does NOT: write anything, call a model, or run a query of its own. Every tool is a thin
wrapper over a function in app/queries.py, given filters built by `queries.make_filters`,
the same check the dashboard's API uses, so a tool and the dashboard cannot disagree.

Invariants: tools only read and never call a model (AGENTS.md "The MCP server"); one
database connection per tool call; the route is open, with no password, because the data
is public job-market data (Chandler, 17 Nov, HIR-338), and the rate limit is the only gate.

Resources (reference data a client reads once, no arguments) sit under "--- resources ---";
the one today is the skill list (HIR-434).

Adding a tool: write a function under "--- tools ---" inside `build_server` (typed
arguments, a docstring written for a model that has never seen the dashboard, the query
call), decorated with `@server.tool(annotations=READ_ONLY)`. Copy `search_jobs` and its
tests in tests/test_mcp_server.py. Give it an example request in app/mcp_examples.json:
the robot visitor calls it on the live site after every deploy and every morning
(HIR-366), and tests/test_mcp_examples.py fails until it has one. Which tools come next, and which query each wraps:
the tool table in HIR-103.
"""

import difflib
import json
import math
import re
import time
from collections.abc import Callable
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
# The protocol versions that have sessions, from the module that routes requests on it.
from mcp.server.streamable_http_manager import HANDSHAKE_PROTOCOL_VERSIONS
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations

from app import db, fit, queries as q, scope
from app.geo import CITIES, REMOTE_EU
from app.taxonomy import Taxonomy, load_added

PATH = "/mcp"
# The version the server reports when a client connects, and the one its Server Card and its
# MCP Registry entry state (app/discovery.py, HIR-480). Raise it with a change to the tools,
# then publish the registry entry again (deploy/README.md).
VERSION = "1.1.0"

# Every tool is read-only and only reads our own database.
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)

# The accepted values, as types the tool's schema shows the model. Built from the same
# constants the API validates against; tests/test_mcp_server.py checks they stay equal.
# A place or career track that is still incubating (app/scope.py, HIR-395) is not offered:
# no tool names it, and app/queries.py returns none of its jobs.
Place = Literal[*(p for p in (*CITIES, REMOTE_EU) if p not in scope.incubating_places())]  # type: ignore[valid-type]
Seniority = Literal[*q.SENIORITIES]  # type: ignore[valid-type]
Family = Literal[*q.FAMILIES]  # type: ignore[valid-type]
Requirement = Literal[*q.REQUIREMENTS]  # type: ignore[valid-type]
Window = Literal[*q.WINDOWS]  # type: ignore[valid-type]
German = Literal[*q.GERMAN_FILTERS]  # type: ignore[valid-type]
Degree = Literal[*q.DEGREE_FILTERS]  # type: ignore[valid-type]
Production = Literal[*q.PRODUCTION_FILTERS]  # type: ignore[valid-type]
Sort = Literal[*q.SORTS]  # type: ignore[valid-type]

MAX_JOBS = 50  # per call; page with `offset` for more

# The degree a person holds, for match_profile: the dashboard profile's values, with "none"
# in place of its empty string. tests/test_mcp_server.py checks they stay equal.
ProfileDegree = Literal["none", "bachelor", "master", "phd"]
FIT_PAGE = 200  # match_profile reads the jobs to rank this many at a time, as the dashboard does

INSTRUCTIONS = """\
hiring-radar tracks AI and ML job postings (Berlin, Hamburg, Frankfurt, Munich, Remote (EU),
San Francisco, New York, Austin, Boston, Seattle, Los Angeles, Chicago, San Jose, London, Amsterdam) and reads each posting into a fixed list of skills, each marked
required or nice-to-have, plus seniority, German, degree and production-experience
requirements. All tools are read-only."""

# The skill list as an MCP resource (HIR-434): reference data a client loads once, in place
# of a tool. The dashboard's radial skill tree is not offered: its drawing coordinates are
# noise to a model, and the hierarchy it draws is the `parents` here.
SKILLS_URI = "hiring-radar://skills"
SKILLS_DESCRIPTION = """\
Every skill hiring-radar tracks, as JSON: {"version", "skills": [{"id", "display",
"aliases", "parents"}]}. Use it to turn a user's words into skill ids for search_jobs,
skill_demand and related_skills (match display or any alias, ignoring case; the tools also
accept names, but an id is exact), and to read the hierarchy: parents are the ids of the
broader skills a skill sits under (e.g. aws under cloud, autogen under agents). A skill not
listed here is not tracked, so no tool can count it; search_jobs' `text` filter can still
find it in posting text."""


def build_server(db_path: Path, tax: Taxonomy, now: Callable[[], str],
                 skill_added: dict[str, str] | None = None) -> MCPServer:
    """The MCP server with every tool registered. `now` is injected so tests can fix the
    clock, exactly as the API's routes do; `skill_added` (the day each skill joined the
    list, read only by rising_skills) likewise, defaulting to the recorded dates."""
    server = MCPServer("hiring-radar", instructions=INSTRUCTIONS, version=VERSION)
    added = load_added() if skill_added is None else skill_added

    @contextmanager
    def connect():
        c = db.connect(db_path, same_thread=False)
        try:
            yield c
        finally:
            c.close()

    # Every way a skill may be written, lowercased, to the id it means: the id, the display
    # name and each alias (HIR-442). A model usually sends the full name, so a typo in it
    # must find the skill as surely as a typo in the id.
    labels: dict[str, str] = {}
    for s in tax.skills.values():
        for label in (s.id, s.display, *s.aliases):
            labels.setdefault(label.strip().lower(), s.id)

    def suggestions(name: str) -> list[str]:
        """Up to three skill ids whose id, display name or alias is close to `name`."""
        close = difflib.get_close_matches(name.strip().lower(), list(labels), n=10, cutoff=0.6)
        return list(dict.fromkeys(labels[label] for label in close))[:3]

    def skill_ids(names: list[str]) -> list[str]:
        """Skill ids from ids or names ("RAG", "rag", "Retrieval Augmented Generation")."""
        out = []
        for n in names:
            sid = n if n in tax.skills else tax.resolve(n)
            if sid is None:
                close = suggestions(n)
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
        - family: ai-engineer, ml-engineer, data-scientist, ml-platform, research or
          forward-deployed-engineer, assigned from the job title.
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
          skill list (e.g. "on-call", "visa sponsorship"). For how many jobs mention
          them per city and career track, use search_postings.
        - sort: newest (default), oldest, reposts (most re-advertised first), company.
        - limit: jobs per call, 1 to 50 (default 20); offset: skip that many, to page.

        Returns total (all matching jobs), and per job: id, company, title, places, family,
        seniority, first_seen / last_seen (dates we saw it), status (open or closed),
        url (the posting), required_skills and nice_to_have_skills, german, degree and
        production requirements (null = not mentioned), and read.
        required_skills lists the job's requirements, one item each: a skill id, or a
        group of alternatives the posting accepts any one of ("AWS or Azure"), written as
        a list of ids, e.g. ["python", ["aws", "azure"]]. A job with no such group is a
        plain list of ids. Its length is match_profile's total for the job.
        nice_to_have_skills is a plain list of skill ids.
        read is false for a posting we stored but the model has not read yet, usually one
        first seen today: its skills, seniority, german, degree and production are then
        unknown, not absent, so never take it for a job that asks for nothing. Such a
        posting can match german, degree or production "none" / "not_required" / "open";
        ask again later for its reading.

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

    @server.tool(annotations=READ_ONLY)
    def search_postings(
        text: str,
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
        sort: Sort = "newest",
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Count the job postings whose text mentions some words, split by city and by
        career track, and list them. Answers "how many Berlin jobs mention Claude?" or "how
        many jobs ask for Kubernetes and German, per city?" in one call, for anything our
        skill list does not track: a product, a company, a tool, a phrase.

        - text (required): the words to find in the posting text, e.g. "Claude" or
          "visa sponsorship". Every word must appear somewhere in the posting, in any order
          and not necessarily together; case and accents do not matter. Words are matched
          whole, so "Claude" does not find "Claudette", and punctuation splits words, so
          "C++" searches for "C".
        - skills, city, seniority, family, requirement, window, german, degree, production,
          company_or_title, sort: the same filters as search_jobs, with the same values and
          defaults. Every count below is over the jobs these filters keep; by default, only
          open jobs.
        - limit: jobs listed, 0 to 50 (default 20); 0 returns only the counts. offset: skip
          that many, to page.

        Returns:
        - total: every matching job, not just those listed.
        - by_city: matching jobs per place, largest first. A job posted for several places
          counts in each, so these can add up to more than total. With a city filter, only
          the chosen places appear.
        - by_family: matching jobs per career track (ai-engineer, ml-engineer,
          data-scientist, ml-platform, research), largest first. A job with no track counts
          in total only. Places and tracks with no match are left out.
        - offset, and jobs: the matching jobs, in the same shape as search_jobs (id,
          company, title, places, family, seniority, first_seen, last_seen, status, url,
          required_skills, nice_to_have_skills, german, degree, production, read);
          required_skills writes a group of alternatives as a list of ids.
          read is false for a posting the model has not read yet: its skills and
          requirements are unknown, not absent. Use get_job for a job's full text.

        Example: how many open jobs mention Claude, per city and career track:
        search_postings(text="Claude", limit=0)
        """
        if not q.fts_query(text):
            raise ToolError("text must name at least one word to find, e.g. \"Claude\"")
        if not 0 <= limit <= MAX_JOBS:
            raise ToolError(f"limit must be between 0 and {MAX_JOBS}")
        if offset < 0:
            raise ToolError("offset must be 0 or more")
        try:
            f = q.make_filters(tax.skills, cities=city or (), seniorities=seniority or (),
                               families=family or (), requirement=requirement, window=window,
                               german=german, degree=degree, production=production,
                               skill_ids=skill_ids(skills or []), query=company_or_title, text=text)
        except ValueError as e:
            raise ToolError(str(e)) from None
        at = now()
        with connect() as conn:
            counts = q.text_counts(conn, f, at)
            jobs = q.list_jobs(conn, f, at, sort, limit, offset)["jobs"] if limit else []
        return {**counts, "offset": offset, "jobs": [_job(j) for j in jobs]}

    @server.tool(annotations=READ_ONLY)
    def get_job(job_id: int) -> dict[str, Any]:
        """Get one job posting in full, with the same details as the hiring-radar
        dashboard's job page. Use search_jobs first to find a job's id.

        - job_id: the id of the job, as search_jobs returns it. An id that does not
          exist is an error.

        Returns company, title, places, family, seniority, first_seen / last_seen (dates
        we saw it), status (open or closed), url (the posting), required_skills,
        nice_to_have_skills, german, degree and production requirements
        (null = not mentioned), description_text (the full posting text, which
        search_jobs leaves out), and read. read is false for a posting we stored but the
        model has not read yet, usually one first seen today: its skills, seniority,
        german, degree and production are then unknown, not absent; ask again later.

        required_skills lists the job's requirements, one item each, counted as
        match_profile counts them. An item is a skill id, or a group of alternatives
        written as a list of ids: the posting accepts any one of them ("AWS or Azure"),
        so the group is one requirement, met by any member. ["python", ["aws", "azure"]]
        is two requirements: Python, and AWS or Azure. A job with no group is a plain list
        of ids. nice_to_have_skills is a plain list of skill ids.

        Example: the details of job 42:
        get_job(job_id=42)
        """
        with connect() as conn:
            detail = q.job_detail(conn, job_id, now())
            if detail is None:
                raise ToolError(f"no job with id {job_id}")
        # The details hold one list of skill mentions; split it into the two lists the tool
        # returns. Required skills are counted as the match counts them: a group of
        # alternatives is one item (HIR-485).
        required_skills = fit.requirement_units(detail)
        nice_to_have_skills = [s["skill_id"] for s in detail["skills"] if s["requirement"] == "nice_to_have"]
        return {
            "company": detail["company"], "title": detail["title"], "places": detail["places"],
            "family": detail["family"], "seniority": detail["seniority"],
            "first_seen": detail["first_seen"][:10], "last_seen": detail["last_seen"][:10], "status": detail["status"],
            "url": next((s["url"] for s in detail["sources"] if s["url"]), None),
            "required_skills": required_skills, "nice_to_have_skills": nice_to_have_skills,
            "german": detail["german"], "production": detail["production"], "read": detail["read"],
            "degree": None if detail["degree"] is None else {
                "level": detail["degree"], "requirement": detail["degree_requirement"],
                "or_equivalent_experience": detail["degree_or_equivalent"]}, "description_text": detail["description_text"]
        }

    @server.tool(annotations=READ_ONLY)
    def skill_demand(
        city: list[Place] | None = None,
        seniority: list[Seniority] | None = None,
        family: list[Family] | None = None,
        requirement: Requirement = "required",
        window: Window = "open",
        german: German = "any",
        degree: Degree = "any",
        production: Production = "any"
        
    ) -> dict[str, Any]:
        """Find which skills job postings ask for most, with the same filters and numbers
        as the hiring-radar dashboard's skill list. Every filter is optional; filters
        combine with AND. Use search_jobs to see the jobs behind a skill.

        - city: any of these places; a job in several places matches each of them.
        - seniority: junior, mid or senior. Leaving it out includes jobs whose seniority
          is unknown; naming any level excludes them.
        - family: ai-engineer, ml-engineer, data-scientist, ml-platform, research or
          forward-deployed-engineer, assigned from the job title.
        - requirement: "required" (default) counts a skill only where the posting requires
          it; "all" also counts it where it is only nice-to-have.
        - window: "open" (default) = still being advertised; "30d" / "90d" = seen in the
          last 30 / 90 days, open or closed; "all" = every job ever collected.
        - german / production: "any" (default); "none" = the posting does not mention it;
          "not_required" = not mentioned or only nice-to-have; "required" = required.
          production means prior experience shipping to production.
        - degree: "any" (default); "none" = no degree mentioned; "open" = someone without
          a degree can apply (none named, optional, or equivalent experience accepted);
          "required" = a degree is required with no alternative.

        Returns total (all jobs matching the filters) and skills: the 50 most asked-for
        skills, most asked-for first. Per skill: skill_id, count (jobs asking for it) and
        pct (count as a percent of total). total counts every matching job, not just the
        jobs behind the 50 skills listed. For the split by city, call once per city.

        Example: what open Berlin AI engineer jobs ask for most:
        skill_demand(city=["Berlin"], family=["ai-engineer"])
        """
        try:
            f = q.make_filters(tax.skills, cities=city or (), seniorities=seniority or (),
                                        families=family or (), requirement=requirement, window=window,
                                        german=german, degree=degree, production=production)
        except ValueError as e:
            raise ToolError(str(e)) from None
        with connect() as conn:
            demand = q.skill_frequency(conn, f, now())
        for skill in demand["skills"]:
            skill.pop("by_city")
        return {"total": demand["total"], "skills": demand["skills"][:MAX_SKILLS_TO_RETURN]}

    @server.tool(annotations=READ_ONLY)
    def related_skills(
        skills: list[str],
        city: list[Place] | None = None,
        seniority: list[Seniority] | None = None,
        family: list[Family] | None = None,
        requirement: Requirement = "required",
        window: Window = "open",
        german: German = "any",
        degree: Degree = "any",
        production: Production = "any",
    ) -> dict[str, Any]:
        """Find what else the jobs asking for given skills ask for, with the same numbers as
        the hiring-radar dashboard's related-skills panel. Answers "I know RAG, what else do
        those jobs want?". Use skill_demand for the most asked-for skills overall.

        - skills (required): one or more skill ids or names, e.g. ["rag"]. With several,
          only jobs that list every one of them count (AND), so fewer jobs match and fewer
          skills come back. Names are matched to our skill list; an unknown name is an
          error that suggests ids.
        - city, seniority, family, requirement, window, german, degree, production: the
          same filters as skill_demand, with the same values and defaults. Every number
          below is over the jobs these filters keep.

        Returns total (all jobs matching the filters), selected_count (those of them that
        list every skill in `skills`) and skills: up to 10 other skills those jobs list,
        most common first. The given skills themselves are left out. Per skill:
        - skill_id, and count: how many of the selected_count jobs list it.
        - pct: count as a percent of selected_count, the share of these jobs that ask for it.
        - base_pct: the same skill as a percent of total, how common it is in all the
          filtered jobs.
        - lift: pct / base_pct. 2.5 means "2.5 times as common in these jobs as in jobs
          overall"; 1 means no more common than anywhere. The 10 skills are the ones with
          the highest lift, so the list shows what is specific to these jobs rather than
          what every job asks for (Python), and is then ordered by pct.
        A skill listed by fewer than 5 of the selected jobs is left out, as too few to
        trust. So skills can be an empty list even when selected_count is above zero: the
        sample is too small. Drop a filter or a skill to widen it.

        Example: what Berlin jobs that require RAG also ask for:
        related_skills(skills=["rag"], city=["Berlin"])
        """
        if not skills:
            raise ToolError("skills must name at least one skill, e.g. [\"rag\"]")
        try:
            f = q.make_filters(tax.skills, cities=city or (), seniorities=seniority or (),
                               families=family or (), requirement=requirement, window=window,
                               german=german, degree=degree, production=production,
                               skill_ids=skill_ids(skills))
        except ValueError as e:
            raise ToolError(str(e)) from None
        with connect() as conn:
            return q.related_skills(conn, f, now())

    @server.tool(annotations=READ_ONLY)
    def rising_skills(
        city: list[Place] | None = None,
        family: list[Family] | None = None,
        requirement: Requirement = "required",
    ) -> dict[str, Any]:
        """Find which skills are being asked for by a larger or smaller share of open jobs
        lately, with the same answer as the hiring-radar dashboard's "What's rising" panel.
        Answers "what's getting hotter in Berlin AI jobs?". skill_demand is one snapshot;
        this compares two periods.

        The two periods: "current" is the last 28 days, "previous" the 28 days before that.
        A job counts in every period it was open during.

        - city: any of these places; leave it out for every place we have collected long
          enough to compare (see places below).
        - family: ai-engineer, ml-engineer, data-scientist, ml-platform, research or
          forward-deployed-engineer, assigned from the job title.
        - requirement: "required" (default) counts a skill only where the posting requires
          it; "all" also counts it where it is only nice-to-have.
        Only these three filters apply, so both periods have as many jobs behind them as
        possible.

        Returns:
        - status: "ok", or "not_enough_data" when no comparison can be trusted yet.
        - reason (null when ok): "new_city" = we started collecting a chosen place too
          recently to cover both periods (its first day would make every skill look as if
          it rose); "few_jobs" = no skill had enough jobs behind it in both periods.
        - ready_from: with reason "new_city", the first day both periods are covered
          (null if that place is not collected at all). Say "not enough data yet, ready
          from <date>", not "nothing is rising". With no city chosen, a place too new to
          compare is left out instead of holding the answer back, and reason is "new_city"
          only when no place is ready yet (ready_from is then the day the first one is).
        - places: included (the places counted; empty when nothing was) and excluded
          (place and ready_from for each place left out, ready_from null if we do not
          collect it). With no city chosen, say which places the answer covers.
        - window_days (28); current and previous: start, end and open_jobs (jobs open in
          that period; null when not compared).
        - risers and fallers: up to 5 skills each, largest move first, and only moves
          of at least 1 point. Per skill: skill_id, current_count / previous_count (jobs asking
          for it in each period), current_share / previous_share (those counts as a
          percent of the period's open jobs) and change = current_share - previous_share,
          in percentage points of open jobs: 3.5 means 3.5 more of every 100 open jobs ask
          for it than in the previous period. Positive in risers, negative in fallers.
        A skill added to our skill list during the two periods is left out, as its early
        numbers would show a rise from zero.

        Example: what is rising and falling in Berlin AI engineer jobs:
        rising_skills(city=["Berlin"], family=["ai-engineer"])
        """
        try:
            f = q.make_filters(tax.skills, cities=city or (), families=family or (), requirement=requirement)
        except ValueError as e:
            raise ToolError(str(e)) from None
        with connect() as conn:
            return q.rising_skills(conn, f, now(), added)

    @server.tool(annotations=READ_ONLY)
    def match_profile(
        skills: list[str],
        seniority: Seniority | None = None,
        german: bool = False,
        production: bool = False,
        degree: ProfileDegree = "none",
        city: list[Place] | None = None,
        family: list[Family] | None = None,
        since: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Rank open jobs by how well they fit one person, best fit first, in the same order
        as the hiring-radar dashboard's "Best fit" sort. Answers "I know Python, RAG and
        LangChain, I'm mid-level, no German: which jobs fit me?", and with `since`, "what's
        new for me since yesterday?". Nothing about the person is stored; pass the profile
        on every call.

        The profile:
        - skills (required): the person's skills, as skill ids or names, e.g. ["python",
          "rag", "langchain"]. Matched to our skill list like search_jobs; an unknown name is
          an error that suggests ids.
        - seniority: junior, mid or senior, the level the person is applying at. Leave it
          out to never rule a job out on level.
        - german: true if the person works in professional German.
        - production: true if the person has shipped software to production.
        - degree: the highest degree the person holds: none (default), bachelor, master, phd.

        Which jobs are ranked:
        - only open jobs first seen in the last 30 days, as on the dashboard: an older
          posting is probably filled.
        - only postings the model has read. A posting we stored but have not read yet
          (usually one first seen today) has no known skills or hard asks, so it is left
          out rather than shown as a fit with nothing to fail; not_read_yet counts them.
        - city: any of these places; family: ai-engineer, ml-engineer, data-scientist,
          ml-platform, research or forward-deployed-engineer, assigned from the job title.
          Both optional.
        - since: an ISO date, e.g. "2026-11-22": only jobs we first saw on or after that
          day (UTC). For a morning digest pass yesterday's date. A date more than 30 days
          back changes nothing.
        - limit: jobs returned, 1 to 50 (default 20).

        The score: a job's required skills are its requirements, and a group of
        alternatives ("Python, Go or Java") is one requirement, met by any one of them.
        - covered / total: requirements the person meets, out of the job's requirements.
        - score: covered / total, from 0 to 1, what the dashboard's badge shows; null when
          the job lists no required skill (unknown, not a bad fit).
        - rank_score: what jobs are ordered by. The same ratio made cautious about thin
          evidence: a job listing fewer than 4 required skills is scored as if it listed 4,
          so 2 of 2 (0.15) ranks below 10 of 14 (0.45). few_skills_listed is true for such
          a job: its score says more about what we read than about the fit.
        - missing_required: the requirements not met, most asked-for across jobs first; a
          group of alternatives appears as a list of ids.
        - gated_by: the hard asks the person fails, in this order: "german" (German is
          required), "production" (production experience is required), "degree" (a higher
          degree is required, with no "or equivalent experience"), "seniority" (the job
          names a different level, from the posting or its title). A nice-to-have never
          gates, and a job that names no level never gates on seniority. A gate does not
          change the score, but every gated job ranks below every job that is not.
        Ties keep newest first; a covered nice-to-have skill only breaks ties.

        Returns ranked (how many jobs were ranked, before limit), not_read_yet (how many
        jobs the filters kept that were left out because the model has not read them yet;
        call again later to rank them) and per job, best fit first: id, company, title, places, url (the posting), first_seen, score,
        rank_score, covered, total, few_skills_listed, missing_required and gated_by.
        Use get_job for a job's full text.

        Example: the best-fitting Berlin jobs for a mid-level Python, RAG and LangChain
        engineer without German, new since 22 November:
        match_profile(skills=["python", "rag", "langchain"], seniority="mid",
                      city=["Berlin"], since="2026-11-22")
        """
        if not skills:
            raise ToolError("skills must name at least one skill, e.g. [\"python\", \"rag\"]")
        if not 1 <= limit <= MAX_JOBS:
            raise ToolError(f"limit must be between 1 and {MAX_JOBS}")
        try:
            day = None if since is None else date.fromisoformat(since).isoformat()
        except ValueError:
            raise ToolError(f"since must be an ISO date like \"2026-11-22\", not {since!r}") from None
        profile = {"skills": skill_ids(skills), "seniority": seniority or "", "german": german,
                   "production": production, "degree": "" if degree == "none" else degree}
        try:
            f = q.make_filters(tax.skills, cities=city or (), families=family or ())
        except ValueError as e:
            raise ToolError(str(e)) from None
        at = now()
        with connect() as conn:
            # Skill demand only orders missing_required, as the dashboard's skill counts do.
            demand = {s["skill_id"]: s["count"] for s in q.skill_frequency(conn, f, at)["skills"]}
            # Newest first, as the dashboard's Best fit asks for them, page by page until the
            # pages reach jobs older than 30 days. Unlike the dashboard it never stops at 200.
            jobs, offset = [], 0
            while True:
                page = q.list_jobs(conn, f, at, "newest", FIT_PAGE, offset)["jobs"]
                recent = fit.recent_jobs(page, at)
                jobs += recent
                if len(page) < FIT_PAGE or len(recent) < len(page):
                    break
                offset += FIT_PAGE
        if day is not None:
            jobs = [j for j in jobs if j["first_seen"][:10] >= day]
        # A posting not read yet has no skills or hard asks to score: ranked, it would look
        # like a fit with nothing to fail (HIR-484). Left out, and counted.
        not_read = sum(not j["read"] for j in jobs)
        ranked = fit.rank_jobs(profile, [j for j in jobs if j["read"]], demand)
        return {"ranked": len(ranked), "not_read_yet": not_read, "jobs": [_match(j, fit.fit(profile, j, demand), profile) for j in ranked[:limit]]}

    # --- resources ------------------------------------------------------------------

    @server.resource(SKILLS_URI, name="skills", title="The skill list", mime_type="application/json",
                     description=SKILLS_DESCRIPTION)
    def skills() -> str:
        # Every skill, as the dashboard's /api/taxonomy lists them. Skills belong to no
        # place or career track, so nothing here is incubating and nothing is left out.
        return json.dumps({"version": tax.version, "skills": [
            {"id": s.id, "display": s.display, "aliases": list(s.aliases), "parents": list(s.parents)}
            for s in sorted(tax.skills.values(), key=lambda s: s.id)]})

    return server


def _match(j: dict, f: dict, profile: dict) -> dict:
    """One job as match_profile returns it: who and where, then how the profile fits it."""
    return {
        "id": j["id"], "company": j["company"], "title": j["title"], "places": j["places"],
        "url": next((s["url"] for s in j["sources"] if s["url"]), None), "first_seen": j["first_seen"][:10],
        "score": f["score"], "rank_score": f["rank_score"], "covered": f["covered"], "total": f["total"],
        "few_skills_listed": f["thin"], "missing_required": f["missing"], "gated_by": fit.gates(profile, j),
    }


def _job(j: dict) -> dict:
    """One job as a tool returns it: what a reader needs, not the dashboard's bookkeeping."""
    return {
        "id": j["id"], "company": j["company"], "title": j["title"], "places": j["places"],
        "family": j["family"], "seniority": j["seniority"],
        "first_seen": j["first_seen"][:10], "last_seen": j["last_seen"][:10], "status": j["status"],
        "url": next((s["url"] for s in j["sources"] if s["url"]), None),
        "required_skills": fit.requirement_units(j), "nice_to_have_skills": j["nice_skills"],
        "german": j["german"], "production": j["production"],
        "degree": None if j["degree"] is None else {
            "level": j["degree"], "requirement": j["degree_requirement"],
            "or_equivalent_experience": j["degree_or_equivalent"]},
        "read": j["read"],
    }


# --- serving -------------------------------------------------------------------------

# The rate limit (HIR-444; numbers and reasons in
# decisions/2026-11-23-hir-444-mcp-rate-limit-per-connection.md). Each allowance is a token
# bucket: bursts of up to its BURST requests, refilled at its RATE a second.
BURST, RATE = 30, 1.0           # one connection (MCP session): 60 a minute sustained
IP_BURST, IP_RATE = 300, 5.0    # everything from one address: the ceiling against abuse
NEW_BURST, NEW_RATE = 60, 1.0   # new connections from one address
_MAX_VISITORS = 10_000  # forget idle visitors past this, so a table cannot grow forever
MAX_SKILLS_TO_RETURN = 50
_SESSION_ID = re.compile(r"[0-9a-f]{32}")  # the ids `RateLimit` hands out; nothing else is taken on


class Buckets:
    """Token buckets by name: `burst` requests at once, refilled at `rate` a second."""

    def __init__(self, burst: float, rate: float, clock: Callable[[], float]):
        self.burst, self.rate, self.clock = burst, rate, clock
        self.buckets: dict[str, tuple[float, float]] = {}  # name -> (tokens, last time)

    def __contains__(self, who: str) -> bool:
        return who in self.buckets

    def take(self, who: str) -> float:
        """0 if the request may go ahead (and is counted), else the seconds until it may."""
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


class RateLimit:
    """The rate limit in front of the MCP's ASGI app; 429 when an allowance is empty, with
    a message saying which allowance, its numbers and how long to wait (`_refuse`).

    Counts per connection, not per address: every user of one web assistant (claude.ai,
    ChatGPT, Gemini) arrives from that vendor's servers, so a per-address limit made them
    share one allowance (HIR-444). A connection is an MCP session. The server itself is
    stateless and issues no session id, so this class does: a request without one is a new
    connection and its answer carries a fresh `Mcp-Session-Id`, which the client sends
    back from then on. The id names a bucket and nothing else.

    Three allowances, checked in this order so that a connection that hammers is refused
    on its own bucket and cannot empty the address it shares with other people:
    - `sessions`: one bucket per connection (BURST, RATE).
    - `new_sessions`: new connections per address (NEW_BURST, NEW_RATE), so opening a
      fresh connection per request does not step around the first. An id this process
      does not know (after a deploy, or made up) is taken on as a new connection.
    - `addresses`: every request from one address (IP_BURST, IP_RATE), the ceiling.

    A request in the newest protocol version (2026-07-28) has no session by design: it is
    held to the address ceiling alone. GET, the listening stream a client with a session id
    may ask for, is answered 405 here and not counted: the server has nothing to push, and
    the stateless transport behind this would hold the stream open for nothing.

    The address is uvicorn's: the API listens on 127.0.0.1 behind Caddy, and uvicorn takes
    the visitor's address from Caddy's X-Forwarded-For header."""

    def __init__(self, app, burst: int = BURST, rate: float = RATE, clock: Callable[[], float] = time.monotonic,
                 ip_burst: int = IP_BURST, ip_rate: float = IP_RATE,
                 new_burst: int = NEW_BURST, new_rate: float = NEW_RATE):
        self.app = app
        self.sessions = Buckets(burst, rate, clock)
        self.new_sessions = Buckets(new_burst, new_rate, clock)
        self.addresses = Buckets(ip_burst, ip_rate, clock)

    def allow(self, address: str, session: str, version: str) -> tuple[float, str | None, str | None]:
        """(0 if the request may go ahead, else the seconds until it may; the session id to
        hand the client, if this request began a connection and brought no usable id; which
        allowance refused it, a key of `_REFUSED`, or None)."""
        def first(*checks: tuple[str, Buckets, str]) -> tuple[float, str | None]:
            for name, buckets, who in checks:
                if wait := buckets.take(who):
                    return wait, name
            return 0.0, None

        if version and version not in HANDSHAKE_PROTOCOL_VERSIONS:
            wait, which = first(("address", self.addresses, address))
            return wait, None, which
        if session in self.sessions:
            wait, which = first(("connection", self.sessions, session), ("address", self.addresses, address))
            return wait, None, which
        issued = None if _SESSION_ID.fullmatch(session) else uuid4().hex
        wait, which = first(("new_connections", self.new_sessions, address), ("address", self.addresses, address),
                            ("connection", self.sessions, issued or session))
        return wait, None if wait else issued, which

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        if scope.get("method") == "GET":  # before the count: a client's retries cost its user nothing
            return await _plain(send, 405, b"This server offers no listening stream: POST only.\n",
                                (b"allow", b"POST"))
        headers = {k: v.decode("latin-1") for k, v in scope.get("headers") or []}
        wait, issued, which = self.allow((scope.get("client") or ("unknown",))[0],
                                         headers.get(b"mcp-session-id", ""), headers.get(b"mcp-protocol-version", ""))
        if wait:
            return await self._refuse(send, wait, which, await _request_id(receive))

        async def send_with_id(message):
            if issued and message["type"] == "http.response.start":
                message = {**message, "headers": [*message.get("headers", []), (b"mcp-session-id", issued.encode())]}
            await send(message)

        await self.app(scope, receive, send_with_id)

    async def _refuse(self, send, wait: float, which: str, request_id: str | int | None) -> None:
        """429 with Retry-After, and a JSON-RPC error a client hands to its model (HIR-218).

        The MCP library's client passes a JSON-RPC error body at a non-2xx status on to the
        caller as that error; a plain-text body reaches the model as "Server returned an
        error response", which tells the person nothing."""
        seconds = max(1, math.ceil(wait))
        buckets = {"connection": self.sessions, "new_connections": self.new_sessions,
                   "address": self.addresses}[which]
        message = _REFUSED[which].format(burst=round(buckets.burst), per_minute=round(buckets.rate * 60),
                                         wait=f"{seconds} second{'s' if seconds != 1 else ''}")
        body = json.dumps({"jsonrpc": "2.0", "id": request_id, "error": {
            "code": RATE_LIMITED, "message": message, "data": {"retry_after": seconds, "limit": which}}})
        await send({"type": "http.response.start", "status": 429,
                    "headers": [(b"retry-after", str(seconds).encode()), (b"content-type", b"application/json")]})
        await send({"type": "http.response.body", "body": body.encode()})


# What a refused request is told, per allowance (HIR-218). Written for the person reading
# their assistant's answer: which limit, its numbers, how long to wait.
RATE_LIMITED = -32000  # JSON-RPC's range for errors a server defines
_REFUSED = {
    "connection": "hiring-radar's request limit for this connection is used up: up to {burst} requests "
                  "at once, then about {per_minute} a minute. Try again in {wait}.",
    "new_connections": "Too many new connections to hiring-radar from this network address: up to {burst} "
                       "at once, then about {per_minute} a minute. Keep using the connection already open "
                       "(send back its Mcp-Session-Id), or try again in {wait}.",
    "address": "hiring-radar's request limit for this network address is used up: up to {burst} requests "
               "at once, then about {per_minute} a minute, shared by everyone connecting from it (an "
               "assistant's servers count as one address). Try again in {wait}.",
}
_MAX_BODY_READ = 65_536  # a refused request's body is read only to find its id


async def _request_id(receive) -> str | int | None:
    """The JSON-RPC id of the refused request, so the client can match the error to it; None
    (sent as null, which JSON-RPC allows when the id cannot be read) for a batch, a body that
    is not JSON, or one too large to bother with."""
    body = b""
    while True:
        message = await receive()
        if message["type"] != "http.request":
            return None
        body += message.get("body", b"")
        if len(body) > _MAX_BODY_READ:
            return None
        if not message.get("more_body"):
            break
    try:
        rid = json.loads(body).get("id")
    except (ValueError, AttributeError):
        return None
    return rid if isinstance(rid, (str, int)) and not isinstance(rid, bool) else None


async def _plain(send, status: int, body: bytes, header: tuple[bytes, bytes]) -> None:
    await send({"type": "http.response.start", "status": status,
                "headers": [header, (b"content-type", b"text/plain")]})
    await send({"type": "http.response.body", "body": body})


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
