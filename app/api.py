"""HTTP API for the dashboard, plus static serving of the built frontend.

Does: expose read endpoints over app/queries.py, the MCP server at /mcp (app/mcp_server.py),
and the "doesn't belong here" flag on a job (app/flags.py: flag, note, un-flag), which is
the only thing a visitor can write. Serves web/dist/ at / when it exists.

Does NOT: add a job or settle a proposed skill (HIR-346 removed both from the site: jobs
are added from the command line through app/add.py, proposed skills are settled in
skill-list pull requests), call a model, compute the profile match (the profile lives in
the browser; the frontend computes coverage from /api/skills and job detail), edit the
taxonomy, or poll feeds.

Every read route answers for the public: app/queries.py leaves out the places and career
tracks that are still incubating (app/scope.py, HIR-395), and no route here asks it not to.

Invariants: every filter is validated against the allowed values and rejected with 422
otherwise; DB connections are per request; the API boots without model credentials.
"""

import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import db, flags, mcp_server, queries as q
from app.extract import DEFAULT_MODEL as EXTRACT_MODEL
from app.ingest import now_iso
from app.skill_tree import skill_tree
from app.taxonomy import Taxonomy, load_added
from app.targeted_reread import record_snapshot

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("HIRING_RADAR_DB", ROOT / "data" / "hiring-radar.db"))
WEB_DIST = ROOT / "web" / "dist"

FoundVia = Literal["linkedin", "indeed", "company_site", "referral", "other"]


def _record_snapshot(db_path: Path, tax: Taxonomy) -> None:
    """Remember the skill list this version runs under (HIR-224). Every deploy restarts this
    process, so the version that was live before a skill-list merge is always on record and
    the next poll can re-read only the postings the added skills could change. Never stops
    the dashboard from starting: without a record the next change simply re-reads in full."""
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        c = db.connect(db_path)
        try:
            db.migrate(c)
            record_snapshot(c, tax, EXTRACT_MODEL)
        finally:
            c.close()
    except Exception as e:  # noqa: BLE001 — a missing record only costs a full re-read
        print(f"warning: could not record the extractor snapshot: {type(e).__name__}: {e}")


def create_app(db_path: Path = DB_PATH, taxonomy: Taxonomy | None = None,
               skill_added: dict[str, str] | None = None) -> FastAPI:
    tax = taxonomy or Taxonomy.load()
    # The MCP server (app/mcp_server.py): the same reads as tools for anyone's Claude, at /mcp.
    mcp = mcp_server.build_server(db_path, tax, lambda: now_iso())

    @asynccontextmanager
    async def lifespan(_app):
        async with mcp.session_manager.run():
            yield

    app = FastAPI(title="hiring-radar", version="0.1.0", lifespan=lifespan)
    app.add_route(mcp_server.PATH, mcp_server.endpoint(mcp), include_in_schema=False)
    # The day each skill joined the list; only "what's rising" reads it.
    added = load_added() if skill_added is None else skill_added
    _record_snapshot(db_path, tax)

    def conn_dep():
        db_path.parent.mkdir(parents=True, exist_ok=True)
        c = db.connect(db_path, same_thread=False)
        db.migrate(c)
        try:
            yield c
        finally:
            c.close()

    def filters(city: list[str] = Query(default=[]), seniority: list[str] = Query(default=[]),
                family: list[str] = Query(default=[]),
                requirement: str = "required", window: str = "open", german: str = "any", degree: str = "any",
                production: str = "any",
                skill: list[str] = Query(default=[]), q_: str = Query(default="", alias="q"),
                text: str = Query(default="")) -> q.Filters:
        # The same check the MCP tools use (app/mcp_server.py), so both reject the same values.
        try:
            return q.make_filters(tax.skills, cities=city, seniorities=seniority, families=family,
                                  requirement=requirement, window=window, german=german, degree=degree,
                                  production=production, skill_ids=skill, query=q_, text=text)
        except ValueError as e:
            raise HTTPException(422, str(e)) from None

    def with_display(skills: list[dict]) -> list[dict]:
        for s in skills:
            t = tax.skills.get(s["skill_id"])
            s["display"] = t.display if t else s["skill_id"]
        return skills

    # --- reads ----------------------------------------------------------------------

    @app.get("/api/stats")
    def get_stats(conn=Depends(conn_dep)):
        return q.stats(conn, now_iso(), skills_tracked=len(tax.skills))

    @app.get("/api/skills")
    def get_skills(f: q.Filters = Depends(filters), conn=Depends(conn_dep)):
        r = q.skill_frequency(conn, f, now_iso())
        r["skills"] = with_display(r["skills"])
        r["city_totals"] = q.city_totals(conn, f, now_iso())
        return r

    @app.get("/api/skills/related")
    def get_related_skills(f: q.Filters = Depends(filters), conn=Depends(conn_dep)):
        """What the jobs listing every `skill` also list. Same filters as /api/skills;
        at least one `skill` is required, and several mean AND."""
        if not f.skill_ids:
            raise HTTPException(422, "skill is required")
        r = q.related_skills(conn, f, now_iso())
        r["skills"] = with_display(r["skills"])
        return r

    @app.get("/api/skills/rising")
    def get_rising_skills(f: q.Filters = Depends(filters), conn=Depends(conn_dep)):
        """What's rising (HIR-232): skills whose share of open jobs moved between the last
        4 weeks and the 4 before. Reads `city`, `family` and `requirement` only; the other
        filters are ignored, so the two periods always have the most jobs behind them."""
        r = q.rising_skills(conn, q.Filters(cities=f.cities, families=f.families, requirement=f.requirement),
                            now_iso(), added)
        r["risers"], r["fallers"] = with_display(r["risers"]), with_display(r["fallers"])
        return r

    @app.get("/api/skills/tree")
    def get_skill_tree(f: q.Filters = Depends(filters), conn=Depends(conn_dep)):
        """The radial skill tree over the filtered job set. Same filters as /api/skills,
        except that `requirement` and `skill` are ignored: every node carries both the
        required and the mentioned share, and the tree always maps the whole market."""
        # The display names go in, not on: a label's width decides the layout, so the
        # tree cannot place anything without knowing what will be written.
        return skill_tree(conn, f, now_iso(), {k: v.display for k, v in tax.skills.items()})

    @app.get("/api/jobs")
    def get_jobs(f: q.Filters = Depends(filters), sort: str = "newest",
                 limit: int = Query(20, ge=1, le=200), offset: int = Query(0, ge=0), conn=Depends(conn_dep)):
        if sort not in q.SORTS:
            raise HTTPException(422, f"bad sort {sort!r}")
        r = q.list_jobs(conn, f, now_iso(), sort, limit, offset)
        flagged = flags.flagged_job_ids(conn, [j["id"] for j in r["jobs"]])
        for j in r["jobs"]:
            j["flagged"] = j["id"] in flagged
        return r

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: int, conn=Depends(conn_dep)):
        d = q.job_detail(conn, job_id, now_iso())
        if d is None:
            raise HTTPException(404, "no such job")
        d["skills"] = with_display(d["skills"])
        d["flagged"] = bool(flags.flagged_job_ids(conn, [job_id]))
        return d

    # --- "this job doesn't belong here" (HIR-226) --------------------------------------

    class Flag(BaseModel):
        # The dashboard's state when the button was clicked, stored as sent: no list of
        # accepted keys here, so a filter the dashboard gains later is recorded untouched.
        view: dict
        note: str | None = None

    @app.post("/api/jobs/{job_id}/flag")
    def post_flag(job_id: int, body: Flag, conn=Depends(conn_dep)):
        if len(json.dumps(body.view)) > flags.VIEW_MAX_BYTES:
            raise HTTPException(422, "view is too large")
        flag_id = flags.add_flag(conn, job_id, body.view, body.note, now_iso(),
                                 skill_names={k: v.display for k, v in tax.skills.items()})
        if flag_id is None:
            raise HTTPException(404, "no such job")
        return {"flag_id": flag_id, "flagged": True}

    @app.delete("/api/jobs/{job_id}/flag")
    def delete_flag(job_id: int, conn=Depends(conn_dep)):
        """A second click on the button. The flag is closed, never deleted."""
        return {"closed": flags.unflag(conn, job_id, now_iso()), "flagged": False}

    class FlagNote(BaseModel):
        note: str

    @app.post("/api/flags/{flag_id}/note")
    def post_flag_note(flag_id: int, body: FlagNote, conn=Depends(conn_dep)):
        if not flags.set_note(conn, flag_id, body.note):
            raise HTTPException(404, "no such open flag")
        return {"flag_id": flag_id, "note": flags.clean_note(body.note)}

    @app.get("/api/taxonomy")
    def get_taxonomy():
        return {"version": tax.version, "skills": [
            {"id": s.id, "display": s.display, "aliases": list(s.aliases), "parents": list(s.parents)}
            for s in sorted(tax.skills.values(), key=lambda s: s.id)]}

    @app.get("/api/proposed")
    def get_proposed(status: str = "pending", conn=Depends(conn_dep)):
        if status not in ("pending", "accepted", "rejected"):
            raise HTTPException(422, "bad status")
        return {"groups": q.proposed_skills(conn, status)}

    # Nothing else lives under /api: an unknown path there is 404 for every method, so it
    # never falls through to the pages below (which would answer a POST with 405 and a GET
    # with the home page). Registered after every real /api route, so it shadows none.
    @app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], include_in_schema=False)
    def no_such_api_route(path: str):
        raise HTTPException(404, "no such route")

    # --- frontend -------------------------------------------------------------------

    if WEB_DIST.exists():
        app.mount("/assets", StaticFiles(directory=WEB_DIST / "assets"), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        def spa(path: str):
            target = WEB_DIST / path
            if path and target.is_file():
                return FileResponse(target)
            return FileResponse(WEB_DIST / "index.html")

    return app


app = None  # created lazily by `python -m app serve` or uvicorn factory


def factory() -> FastAPI:
    return create_app()
