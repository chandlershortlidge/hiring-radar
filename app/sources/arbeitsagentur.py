"""Bundesagentur für Arbeit Jobsuche: https://rest.arbeitsagentur.de/jobboerse/jobsuche-service

Germany's federal job board. Free, no account: every request carries the public header
`X-API-Key: jobboerse-jobsuche`. Not an official public API — it is the access the
agency's own site uses (documented by the community at github.com/bundesAPI/jobsuche-api),
so it can change without notice.

Two calls per posting (shapes recorded from a live call, 2026-10-18):
- search `GET /pc/v6/jobs?was=..&wo=..&umkreis=..&veroeffentlichtseit=..&page=..&size=..`
  → `{"ergebnisliste": [...], "maxErgebnisse": int, "page": int, "size": int, "woOutput",
  "facetten"}`. A result carries `referenznummer`, `stellenangebotsTitel`, `firma`,
  `stellenlokationen` (`[{"adresse": {"ort": ..}}]`), `datumErsteVeroeffentlichung`,
  `externeURL`, `hauptberuf`, but no description. (The v4 search, `stellenangebote` with
  `refnr`, now answers `403 No match found for request`.)
- details `GET /pc/v4/jobdetails/{base64(refnr)}` → the same fields plus
  `stellenangebotsBeschreibung` (the description, Markdown-ish text).

tests/fixtures/feeds/arbeitsagentur_*.json are trimmed from that live call.

Postings from partner boards often have no description in the details response; those
are skipped (a Posting needs description text), the same as other adapters skip empties.

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
    """The results in a search page that carry a reference number, each with `refnr` set.
    v6 returns them under `ergebnisliste` with `referenznummer`; v4 used `stellenangebote`
    and `refnr`. Both are read."""
    payload = payload or {}
    out = []
    for l in payload.get("ergebnisliste") or payload.get("stellenangebote") or []:
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


def _first_city(locations) -> str | None:
    for loc in locations or []:
        city = ((loc or {}).get("adresse") or {}).get("ort")
        if city:
            return city
    return None


def parse(listing: dict, details: dict) -> Posting | None:
    """One search result plus its details → a Posting, or None when there is no description.

    Location comes from the search result first: a posting listed in several cities is
    returned by a Berlin search with Berlin first, while its details may list another
    city first (seen live: Berlin in search, Leipzig first in details)."""
    text = html_to_text(details.get("stellenangebotsBeschreibung") or "")
    title = (listing.get("stellenangebotsTitel") or details.get("stellenangebotsTitel")
             or listing.get("titel"))
    if not text or not title:
        return None
    location = (_first_city(listing.get("stellenlokationen"))
                or (listing.get("arbeitsort") or {}).get("ort")
                or _first_city(details.get("stellenlokationen")))
    refnr = listing["refnr"]
    return Posting(
        source=SOURCE,
        source_job_id=refnr,
        url=JOB_PAGE + refnr,
        company=listing.get("firma") or details.get("firma") or listing.get("arbeitgeber"),
        title=str(title).strip(),
        location_raw=location,
        description_text=text,
        posted_at=(listing.get("datumErsteVeroeffentlichung") or details.get("datumErsteVeroeffentlichung")
                   or listing.get("aktuelleVeroeffentlichungsdatum")),
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
