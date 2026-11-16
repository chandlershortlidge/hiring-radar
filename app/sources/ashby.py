"""Ashby job boards: https://api.ashbyhq.com/posting-api/job-board/<name>

Public, no key. Provides `descriptionPlain` and `descriptionHtml`. Ids are UUIDs.

A posting has one primary office (`location`) and any number of others
(`secondaryLocations`). All of them are kept, "; "-joined as Greenhouse does, so a posting
whose first office is untracked still maps to a tracked city (HIR-268: Qonto lists Paris
first and Berlin second). Each office also contributes the city of its street address when
its name does not already say it (HIR-289: "Mercor HQ, 181 Fremont Street", "Czech
Republic").
"""

from app.html_text import html_to_text
from app.sources import Posting, fetch_json

SOURCE = "ashby"


def board_url(name: str) -> str:
    return f"https://api.ashbyhq.com/posting-api/job-board/{name}"


def _office(o: dict) -> list[str]:
    """One office → its name, then the city from its street address when the name does not
    already say it. Mercor names its office "Mercor HQ, 181 Fremont Street" and only the
    address says San Francisco (HIR-289). An address city that says "Remote" is left out:
    Plaid files remote roles under a "London Office" whose address city is "Remote", and
    that must not read as a remote posting."""
    name = o.get("location").strip() if isinstance(o.get("location"), str) else ""
    address = o.get("address") if isinstance(o.get("address"), dict) else {}
    postal = address.get("postalAddress") if isinstance(address.get("postalAddress"), dict) else {}
    city = postal.get("addressLocality").strip() if isinstance(postal.get("addressLocality"), str) else ""
    out = [name] if name else []
    if city and city.lower() not in name.lower() and "remote" not in city.lower():
        out.append(city)
    return out


def _locations(j: dict) -> str | None:
    """Every office the posting lists, primary first, "; "-joined, each once."""
    offices = [j] + [s for s in j.get("secondaryLocations") or [] if isinstance(s, dict)]
    return "; ".join(dict.fromkeys(p for o in offices for p in _office(o))) or None


def parse(payload: dict, company: str | None = None) -> list[Posting]:
    out = []
    for j in payload.get("jobs", []):
        text = j.get("descriptionPlain") or html_to_text(j.get("descriptionHtml") or "")
        if not text or not j.get("title"):
            continue
        out.append(Posting(
            source=SOURCE,
            source_job_id=str(j["id"]),
            url=j.get("jobUrl", ""),
            company=company,
            title=j["title"].strip(),
            location_raw=_locations(j),
            description_text=text.strip(),
            posted_at=j.get("publishedAt"),
        ))
    return out


def fetch(name: str, company: str | None = None) -> list[Posting]:
    return parse(fetch_json(board_url(name)), company)
