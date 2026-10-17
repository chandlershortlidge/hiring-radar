"""HTTP API for the dashboard, plus static serving of the built frontend.

Does: expose read endpoints over app/queries.py, the review-queue actions, and the three
add-a-job paths (url / text / screenshot) which run intake + extraction synchronously.
Serves web/dist/ at / when it exists.

Does NOT: compute the profile match (the profile lives in the browser; the frontend
computes coverage from /api/skills and job detail), edit the taxonomy, or poll feeds.

Invariants: every filter is validated against the allowed values and rejected with 422
otherwise; DB connections are per request; model clients are created lazily so the API
boots without credentials and only the add endpoints need them.
"""

import hashlib
import os
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import db, queries as q
from app.check import check_url, log_check
from app.extract import DEFAULT_MODEL, extract, make_client
from app.ingest import ingest_one, job_id_for_screenshot, now_iso, store_screenshot
from app.pipeline import extract_pending
from app.poll import load_feeds
from app.sources import Posting
from app.taxonomy import Taxonomy
from app.transcribe import DEFAULT_MODEL as VISION_MODEL, TranscriptionError, transcribe

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("HIRING_RADAR_DB", ROOT / "data" / "hiring-radar.db"))
WEB_DIST = ROOT / "web" / "dist"

FoundVia = Literal["linkedin", "indeed", "company_site", "referral", "other"]


def create_app(db_path: Path = DB_PATH, taxonomy: Taxonomy | None = None, client_factory=make_client) -> FastAPI:
    app = FastAPI(title="hiring-radar", version="0.1.0")
    tax = taxonomy or Taxonomy.load()
    state = {"client": None}

    def client():
        if state["client"] is None:
            state["client"] = client_factory()
        return state["client"]

    def conn_dep():
        db_path.parent.mkdir(parents=True, exist_ok=True)
        c = db.connect(db_path, same_thread=False)
        db.migrate(c)
        try:
            yield c
        finally:
            c.close()

    def filters(city: list[str] = Query(default=[]), seniority: list[str] = Query(default=[]),
                requirement: str = "required", window: str = "open",
                skill: str | None = None, q_: str = Query(default="", alias="q")) -> q.Filters:
        for s in seniority:
            if s not in q.SENIORITIES:
                raise HTTPException(422, f"bad seniority {s!r}")
        if requirement not in q.REQUIREMENTS:
            raise HTTPException(422, f"bad requirement {requirement!r}")
        if window not in q.WINDOWS:
            raise HTTPException(422, f"bad window {window!r}")
        if skill is not None and skill not in tax.skills:
            raise HTTPException(422, f"unknown skill {skill!r}")
        return q.Filters(cities=tuple(city), seniorities=tuple(seniority), requirement=requirement,
                         window=window, skill_id=skill, query=q_)

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

    @app.get("/api/jobs")
    def get_jobs(f: q.Filters = Depends(filters), sort: str = "newest",
                 limit: int = Query(20, ge=1, le=200), offset: int = Query(0, ge=0), conn=Depends(conn_dep)):
        if sort not in q.SORTS:
            raise HTTPException(422, f"bad sort {sort!r}")
        return q.list_jobs(conn, f, now_iso(), sort, limit, offset)

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: int, conn=Depends(conn_dep)):
        d = q.job_detail(conn, job_id, now_iso())
        if d is None:
            raise HTTPException(404, "no such job")
        d["skills"] = with_display(d["skills"])
        return d

    @app.get("/api/taxonomy")
    def get_taxonomy():
        return {"version": tax.version, "skills": [
            {"id": s.id, "display": s.display, "parents": list(s.parents)} for s in sorted(tax.skills.values(), key=lambda s: s.id)]}

    @app.get("/api/proposed")
    def get_proposed(status: str = "pending", conn=Depends(conn_dep)):
        if status not in ("pending", "accepted", "rejected"):
            raise HTTPException(422, "bad status")
        return {"groups": q.proposed_skills(conn, status)}

    class Resolve(BaseModel):
        ids: list[int] = Field(min_length=1)
        status: Literal["accepted", "rejected"]
        resolved_skill_id: str | None = None

    @app.post("/api/proposed/resolve")
    def post_resolve(body: Resolve, conn=Depends(conn_dep)):
        if body.status == "accepted":
            if not body.resolved_skill_id or body.resolved_skill_id not in tax.skills:
                raise HTTPException(422, "accepting needs resolved_skill_id, an existing taxonomy id")
        n = q.resolve_proposed(conn, body.ids, body.status, body.resolved_skill_id, tax.version)
        return {"resolved": n}

    # --- adds -----------------------------------------------------------------------

    def finish_add(conn, outcome: str) -> dict:
        if outcome.startswith("new:"):
            job_id = int(outcome[4:])
            report = extract_pending(conn, tax, lambda text, t, m: extract(text, t, client(), m), DEFAULT_MODEL,
                                     log=lambda *_: None, job_ids=[job_id])
            d = q.job_detail(conn, job_id, now_iso())
            return {"outcome": "added", "job_id": job_id, "skills_found": len(d["skills"]),
                    "proposed": len(d["proposed"]), "failed": [f for f in report.failed if f[0] == job_id]}
        return {"outcome": outcome, "job_id": None}

    class AddUrl(BaseModel):
        url: str
        found_via: FoundVia = "linkedin"
        company: str | None = None
        title: str | None = None
        location: str | None = None

    @app.post("/api/add/url")
    def add_url(body: AddUrl, conn=Depends(conn_dep)):
        r = check_url(conn, body.url, load_feeds(), body.company, body.title, body.location)
        log_check(conn, r, body.found_via, now_iso())
        if r.job_id:
            d = q.job_detail(conn, r.job_id, now_iso())
            return {"outcome": "exists", "job_id": r.job_id, "job": d, "verdict": r.line()}
        if r.posting is None:
            return {"outcome": "unreadable", "job_id": None, "verdict": r.line(), "notes": r.notes}
        is_board = r.posting.source in ("greenhouse", "lever", "ashby")
        outcome = ingest_one(conn, r.posting, now_iso(), require_city=not is_board,
                             found_via=body.found_via, trust_title=True)
        res = finish_add(conn, outcome)
        res["verdict"] = r.line()
        return res

    class AddText(BaseModel):
        text: str = Field(min_length=40)
        company: str
        title: str
        location: str | None = None
        url: str | None = None
        found_via: FoundVia = "linkedin"

    @app.post("/api/add/text")
    def add_text(body: AddText, conn=Depends(conn_dep)):
        p = Posting(source="paste", source_job_id="", url=body.url or "", company=body.company, title=body.title,
                    location_raw=body.location, description_text=body.text.strip())
        outcome = ingest_one(conn, p, now_iso(), require_city=False, found_via=body.found_via, trust_title=True)
        return finish_add(conn, outcome)

    @app.post("/api/add/screenshot")
    def add_screenshot(file: UploadFile, company: str, title: str, location: str | None = None,
                             url: str | None = None, found_via: FoundVia = "linkedin", conn=Depends(conn_dep)):
        data = file.file.read()
        if len(data) > 8 * 1024 * 1024:
            raise HTTPException(413, "image over 8 MB")
        existing = job_id_for_screenshot(conn, hashlib.sha256(data).hexdigest())
        if existing:
            return {"outcome": "exists", "job_id": existing, "job": q.job_detail(conn, existing, now_iso())}
        try:
            t = transcribe(data, client(), VISION_MODEL)
        except TranscriptionError as e:
            raise HTTPException(422, f"could not read the screenshot: {e}")
        p = Posting(source="screenshot", source_job_id="", url=url or "", company=company, title=title,
                    location_raw=location, description_text=t.text)
        outcome = ingest_one(conn, p, now_iso(), require_city=False, found_via=found_via, trust_title=True)
        if outcome.startswith("new:"):
            store_screenshot(conn, int(outcome[4:]), data, t.sha256, t.media_type)
        return finish_add(conn, outcome)

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
