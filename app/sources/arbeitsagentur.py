"""Bundesagentur für Arbeit Jobsuche: https://rest.arbeitsagentur.de/jobboerse/jobsuche-service

Germany's federal job board. Free, no account: every request carries the public header
`X-API-Key: jobboerse-jobsuche`. Not an official public API — it is the access the
agency's own site uses (documented by the community at github.com/bundesAPI/jobsuche-api),
so it can change without notice.

Two calls per posting:
- search `GET /pc/v6/jobs?was=..&wo=..&umkreis=..&veroeffentlichtseit=..&page=..&size=..`
  → `{"stellenangebote": [...], "maxErgebnisse": int, "page": int, "size": int}`. A listing
  has `referenznummer` (`refnr` in the older v4 search; both are read), `titel`, `arbeitgeber`, `arbeitsort` (`ort`, `plz`, `region`, `land`),
  `aktuelleVeroeffentlichungsdatum`, and `externeUrl` when the posting lives elsewhere.
  No description.
- details `GET /pc/v4/jobdetails/{base64(refnr)}` → `stellenangebotsTitel`, `firma`,
  `stellenangebotsBeschreibung` (plain text, sometimes HTML-ish), `stellenlokationen`
  (`[{"adresse": {"ort": ..}}]`), `datumErsteVeroeffentlichung`, `allianzpartnerUrl`.

Field names come from the bundesAPI docs and the `jobsuche` Rust crate's response types,
not from a recorded call: tests/fixtures/feeds/arbeitsagentur_*.json are hand-built to
that shape. Replace them with a recorded response when one is available.

Postings from partner boards often have no description in the details response; those
are skipped (a Posting needs description text), the same as other adapters skip empties.

The v4 search path answers `403 No match found for request` (seen on a live poll,
2026-10-18): it is gone, so search uses v6. Details stay on v4, the documented choice.

Pagination: page numbers start at 1; stop on an empty page or once page*size covers
maxErgebnisse.

Does NOT filter by title or city (ingest does), even though every listing costs one
details call — keep `max_pages` × `size` modest and the `was` query narrow.
"""

import base64
import urllib.parse

from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "arbeitsagentur"
BASE = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service"
HEADERS = {"X-API-Key": "jobboerse-jobsuche"}
JOB_PAGE = "https://www.arbeitsagentur.de/jobsuche/jobdetail/"


def listings(payload: dict) -> list[dict]:
    """The listings in a search page that carry a reference number, each with `refnr` set
    (v6 calls it `referenznummer`)."""
    out = []
    for l in (payload or {}).get("stellenangebote") or []:
        ref = l.get("refnr") or l.get("referenznummer")
        if ref:
            out.append({**l, "refnr": ref})
    return out


def has_next(payload: dict) -> bool:
    if not listings(payload):
        return False
    try:
        page, size, total = int(payload["page"]), int(payload["size"]), int(payload["maxErgebnisse"])
    except (KeyError, TypeError, ValueError):
        return False
    return page * size < total


def parse(listing: dict, details: dict) -> Posting | None:
    """One listing plus its details → a Posting, or None when there is no description."""
    text = html_to_text(details.get("stellenangebotsBeschreibung") or "")
    title = details.get("stellenangebotsTitel") or listing.get("titel")
    if not text or not title:
        return None
    location = None
    for loc in details.get("stellenlokationen") or []:
        location = ((loc or {}).get("adresse") or {}).get("ort")
        if location:
            break
    location = location or (listing.get("arbeitsort") or {}).get("ort")
    refnr = listing["refnr"]
    return Posting(
        source=SOURCE,
        source_job_id=refnr,
        url=JOB_PAGE + refnr,
        company=details.get("firma") or listing.get("arbeitgeber"),
        title=str(title).strip(),
        location_raw=location,
        description_text=text,
        posted_at=details.get("datumErsteVeroeffentlichung") or listing.get("aktuelleVeroeffentlichungsdatum"),
    )


def search_url(search: str, where: str | None, radius_km: int | None, days: int | None,
               page: int, size: int) -> str:
    params = {"was": search, "angebotsart": 1, "page": page, "size": size}
    if where:
        params["wo"] = where
    if radius_km is not None:
        params["umkreis"] = radius_km
    if days is not None:
        params["veroeffentlichtseit"] = days
    return f"{BASE}/pc/v6/jobs?{urllib.parse.urlencode(params)}"


def details_url(refnr: str) -> str:
    return f"{BASE}/pc/v4/jobdetails/{base64.b64encode(refnr.encode()).decode()}"


def fetch(search: str, where: str | None = "Berlin", radius_km: int | None = 25,
          days: int | None = 30, max_pages: int = 2, size: int = 50) -> list[Posting]:
    out, page = [], 1
    while page <= max_pages:
        payload = fetch_json(search_url(search, where, radius_km, days, page, size), headers=HEADERS)
        for l in listings(payload):
            p = parse(l, fetch_json(details_url(l["refnr"]), headers=HEADERS))
            if p:
                out.append(p)
        if not has_next(payload):
            break
        page += 1
    return out
