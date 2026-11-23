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
import time
from collections.abc import Callable
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Any, Literal

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations

from app import db, fit, queries as q, scope
from app.geo import CITIES, REMOTE_EU
from app.taxonomy import Taxonomy, load_added

PATH = "/mcp"

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
    server = MCPServer("hiring-radar", instructions=INSTRUCTIONS)
    added = load_added() if skill_added is None else skill_added

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
          skill list (e.g. "on-call", "visa sponsorship"). For how many jobs mention
          them per city and career track, use search_postings.
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
          required_skills, nice_to_have_skills, german, degree, production). Use get_job
          for a job's full text.

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
        we saw it), status (open or closed), url (the posting), required_skills and
        nice_to_have_skills (skill ids), german, degree and production requirements
        (null = not mentioned), and description_text (the full posting text, which
        search_jobs leaves out).

        Example: the details of job 42:
        get_job(job_id=42)
        """
        with connect() as conn:
            detail = q.job_detail(conn, job_id, now())
            if detail is None:
                raise ToolError(f"no job with id {job_id}")
        # The details hold one list of skill mentions; split it into the two lists the tool returns.
        required_skills = [s["skill_id"] for s in detail["skills"] if s["requirement"] == "required"]
        nice_to_have_skills = [s["skill_id"] for s in detail["skills"] if s["requirement"] == "nice_to_have"]
        return {
            "company": detail["company"], "title": detail["title"], "places": detail["places"],
            "family": detail["family"], "seniority": detail["seniority"],
            "first_seen": detail["first_seen"][:10], "last_seen": detail["last_seen"][:10], "status": detail["status"],
            "url": next((s["url"] for s in detail["sources"] if s["url"]), None),
            "required_skills": required_skills, "nice_to_have_skills": nice_to_have_skills,
            "german": detail["german"], "production": detail["production"],
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
        - family: ai-engineer, ml-engineer, data-scientist, ml-platform or research,
          assigned from the job title.
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

        - city: any of these places; leave it out for every place we collect.
        - family: ai-engineer, ml-engineer, data-scientist, ml-platform or research,
          assigned from the job title.
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
          from <date>", not "nothing is rising".
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
        - city: any of these places; family: ai-engineer, ml-engineer, data-scientist,
          ml-platform or research, assigned from the job title. Both optional.
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

        Returns ranked (how many jobs were ranked, before limit) and per job, best fit
        first: id, company, title, places, url (the posting), first_seen, score,
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
        ranked = fit.rank_jobs(profile, jobs, demand)
        return {"ranked": len(ranked), "jobs": [_match(j, fit.fit(profile, j, demand), profile) for j in ranked[:limit]]}

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
MAX_SKILLS_TO_RETURN = 50

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
