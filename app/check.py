"""Given a careers-page URL, say whether that posting is already in the database — and if
not, why the feeds could not have stored it. This is how feed coverage gets audited by hand.

Does:
  - recognize hosted ATS job URLs (Greenhouse, Lever, Ashby, JOIN) and turn them into
    (source, board token, job id); a Greenhouse embed URL (`?gh_jid=`) names the job but
    not the board, so the board token is instead read off the embed widget script on the
    fetched page, when the page has one;
  - look the job up by exact (source, source_job_id), then by company + text containment
    against stored jobs (the page may have been stored via another source, e.g. arbeitnow);
  - for a page that is not a known ATS, read the posting out of JSON-LD `JobPosting` when
    the page has it, otherwise the stripped page text; a Personio tenant serving no
    JSON-LD still gives up its company and city, out of the payload it embeds; a page
    with neither gives a location when its text has a "Location:" / "Standort:" line;
  - read a Workable job link (apply.workable.com) through Workable's public job API,
    because its page is built in the browser and holds no posting text (HIR-268);
  - diagnose a miss: board not in config/feeds.json; board polled but the title or city
    filter would have dropped it; board polled and it would have passed (a feed bug, or
    posted since the last poll); not a feed-reachable page at all.

  - log each check (`log_check`) and report coverage over the logged checks
    (`checked_coverage`): of the URLs a person checked, how many a feed already had;
    `reach_breakdown` sorts the misses by whether a feed can reach them *now*;
  - count jobs a feed has seen (`job_coverage`), leaving out the legacy screenshot imports.

Does NOT: write anything but the url_check log (the CLI's --add hands the resolved Posting
to app.ingest), call a model, or fetch LinkedIn (its pages are not readable without a login
and the project does not scrape it).

Invariants: `parse_ats_url`, `token_from_embed`, `posting_from_html`, `containment`,
`diagnose` and `feed_had_it` are pure; `check_url` reads the DB and never writes it, and does network I/O
only through the injected fetchers, so tests never touch the network. Coverage counts only
the first check of each URL: the /check-url skill re-checks after adding a board and
polling, and that re-check must not count as the feed having had the posting.
Text matching here is one-directional containment (how much of the *stored* JD appears on
the page), not ingest's symmetric Jaccard: a careers page carries nav, footer and other
listings, which would sink a symmetric score for the same posting.
"""

import json
import re
import sqlite3
import urllib.parse
from dataclasses import dataclass, field
from html.parser import HTMLParser

from app import dedup
from app.geo import ACTIVE_CITIES, active_place, city_of
from app.html_text import html_to_text
from app.ingest import in_scope_title
from app.sources import Posting, fetch_text, registry

CONTAINMENT_THRESHOLD = 0.7   # share of a stored JD's 3-word shingles that must appear on the page
MANUAL_SOURCES = registry.MANUAL_SOURCES   # job_source values a person added; the rest are feeds
# The legacy importer keeps the old project's dates as first_seen, all before the rebuild
# began; a screenshot first seen before this is from the old (hackathon) collection method.
REBUILD_START = "2026-10-16"

_ATS_PATTERNS = (
    # https://boards.greenhouse.io/acme/jobs/4012345  (also job-boards.greenhouse.io, job-boards.eu.greenhouse.io)
    ("greenhouse", re.compile(r"^(?:boards|job-boards)(?:\.eu)?\.greenhouse\.io$", re.I),
     re.compile(r"^/(?P<token>[^/]+)/jobs/(?P<id>\d+)")),
    # https://jobs.lever.co/acme/0a1b2c3d-...  (optional /apply)
    ("lever", re.compile(r"^jobs\.lever\.co$", re.I),
     re.compile(r"^/(?P<token>[^/]+)/(?P<id>[0-9a-f-]{36})")),
    # https://jobs.ashbyhq.com/acme/0a1b2c3d-...
    ("ashby", re.compile(r"^jobs\.ashbyhq\.com$", re.I),
     re.compile(r"^/(?P<token>[^/]+)/(?P<id>[0-9a-f-]{36})")),
    # https://join.com/companies/acme/16814436-ai-engineer-m-f-x  (the id is the leading number)
    ("join", re.compile(r"^(?:www\.)?join\.com$", re.I),
     re.compile(r"^/companies/(?P<token>[^/]+)/(?P<id>\d+)")),
)
# A company embedding its Greenhouse board loads this script; its `for=` value is the board
# token (Greenhouse's own embed-code snippet names it exactly this way), independent of which
# greenhouse.io host happens to be serving it (boards. or job-boards., plain or .eu).
_EMBED_TOKEN_RE = re.compile(r"greenhouse\.io/embed/job_board(?:/js)?\?(?:[^\"'\s>]*&)?for=(?P<token>[\w-]+)", re.I)

# One Personio tenant per subdomain, on either of the two hosts Personio serves them from
# (`acto.jobs.personio.com`, `adsquare.jobs.personio.de`). Not an ATS pattern: a Personio
# job URL is read as a page, not resolved to a board — see `_personio_fields`.
_PERSONIO_HOST_RE = re.compile(r"(?:^|\.)jobs\.personio\.(?:com|de)$", re.I)

# Workable job links: https://apply.workable.com/<account>/j/<shortcode>/ (optional /apply).
# Not an ATS pattern either: there is no Workable source, the posting is stored as a page
# (source=url) — but read through Workable's public job API, see `posting_from_workable`.
_WORKABLE_HOST = "apply.workable.com"
_WORKABLE_PATH_RE = re.compile(r"^/(?P<account>[^/]+)/j/(?P<code>[0-9A-Za-z]+)")

# Platform names that can sit in a page's site name, title tail or hostname without naming
# the employer: the job boards and ATS vendors this project meets. A page declaring one of
# these declares where it is hosted, not who is hiring (HIR-198).
_GENERIC_SITE_NAMES = frozenset({
    "linkedin", "indeed", "stepstone", "glassdoor", "xing", "personio", "workday",
    "myworkdayjobs", "greenhouse", "lever", "ashby", "ashbyhq", "join",
    # Every source this project polls (app/sources/registry.py), by its site name and by
    # the hostname label its posting links carry. A feed job stored blank whose page has
    # gone must stay blank, not become a job at "Arbeitsagentur" (HIR-211).
    # tests/test_check.py fails when a polled source has no address covered here.
    "arbeitsagentur", "bundesagentur für arbeit", "arbeitnow",
    "startup", "startup jobs", "startup.jobs",
    "jsearch", "rapidapi", "openwebninja",
    # JSearch is a search over other job sites and links to whichever one carried the
    # posting. These are the ones its stored links have named so far that are job sites,
    # not employers.
    "learn4good", "trabajo", "jobleads", "jooble", "speedyapply", "freelance", "devjobs",
    "absolventa", "efinancialcareers", "nortjobs",
})
# Title tails that name a careers section rather than a company ("AI Engineer | Careers").
_GENERIC_TITLE_TAILS = frozenset({"jobs", "job", "careers", "career", "karriere", "join us", "jobs & careers"})
# A page title's last "|", "–"/"—", spaced "-", or " at " splits it into role and company.
# The hyphen needs space on both sides so "Machine-Learning Engineer" never splits.
_TITLE_TAIL_RE = re.compile(r"\s*\|\s*|\s+[–—-]\s+|\s+at\s+")
# acme.co.uk → acme: hostname labels that are a public-suffix part, not the company.
_SECOND_LEVEL_TLDS = frozenset({"co", "com", "org", "net", "ac", "gov"})
# SAP SuccessFactors career sites (jobs.bayer.com) title every posting page
# "<job title> Stellendetails | <company>" ("Job Details" in English): page furniture that
# is not part of the job title (HIR-268). Matched at the end, or just before the "|".
_JOB_DETAILS_SUFFIX_RE = re.compile(r"\s+(?:Stellendetails|Job Details)(?=\s*(?:\||$))", re.I)
# A posting with no structured data that still states its place on a line of its own:
# "Location: Deutschland : Berlin : Berlin" (jobs.bayer.com), "Standort: Berlin".
_LOCATION_LINE_RE = re.compile(
    r"^[ \t]*(?:Location|Standort|Arbeitsort|Einsatzort)[ \t]*:[ \t]*(?P<v>\S[^\n]*)$", re.I | re.M)
# Zero-width and non-breaking characters a rich-text editor leaves around such a line.
_INVISIBLE_RE = re.compile("[" + "".join(map(chr, (0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF, 0xA0))) + "]")
_MAX_LOCATION_LINE = 80   # characters; a longer "Location: …" line is a sentence, not a place


def location_from_text(text: str) -> str | None:
    """The value of the first "Location:" / "Standort:" line in a page's text, or None.

    Only a short line counts, so a sentence that happens to start with the label is not
    stored as a place. What the line says is returned as written; whether it names a
    tracked city is `app.geo`'s call, as for every other location."""
    for m in _LOCATION_LINE_RE.finditer(_INVISIBLE_RE.sub(" ", text)):
        value = " ".join(m["v"].split())
        if value and len(value) <= _MAX_LOCATION_LINE:
            return value
    return None


def split_title_tail(title: str) -> tuple[str, str | None]:
    """"Senior AI Engineer | Acme" → ("Senior AI Engineer", "Acme"), on the LAST separator
    so "AI Engineer - NLP | Acme" keeps its subtitle. (title, None) when there is none."""
    last = None
    for m in _TITLE_TAIL_RE.finditer(title):
        last = m
    if last is None:
        return title.strip(), None
    return title[:last.start()].strip(), title[last.end():].strip()


def _usable_company(name: str | None) -> bool:
    """A candidate company name is usable unless it is blank, a single character, truncated
    (an ellipsis means the page or store cut it off mid-name), or a generic platform or
    careers-section name."""
    if not name:
        return False
    low = name.strip().lower()
    return (len(low) > 1 and "…" not in name and "..." not in name
            and low not in _GENERIC_SITE_NAMES and low not in _GENERIC_TITLE_TAILS)


def company_from_page(url: str, parser: "_PageParser") -> tuple[str | None, str | None]:
    """(company, rule) read off a page that has no structured job data; (None, None) when
    nothing usable. Rules in order (HIR-198): the site name the page declares, the page
    title's tail, the hostname's registrable label. `rule` names which one answered, for
    the check's notes; "title tail" also tells the caller to strip the tail off the title.
    """
    site = (parser.site_name or parser.application_name).strip()
    if _usable_company(site):
        return site, "site name"
    _, tail = split_title_tail(parser.title.strip())
    if _usable_company(tail):
        return tail, "title tail"
    labels = (urllib.parse.urlsplit(url).hostname or "").lower().split(".")
    labels = [l for l in labels if l and l != "www"]
    if len(labels) >= 2:
        name = labels[-3] if len(labels) >= 3 and labels[-2] in _SECOND_LEVEL_TLDS else labels[-2]
        if _usable_company(name):
            return name.capitalize(), "domain"
    return None, None


@dataclass(frozen=True)
class AtsRef:
    source: str
    token: str | None      # board token; None when the URL names the job but not the board
    job_id: str


def parse_ats_url(url: str) -> AtsRef | None:
    """Hosted ATS job URL → AtsRef. Anything else → None.

    Greenhouse embeds (`https://acme.com/careers?gh_jid=4012345`) give the job id but not the
    board token, so the ref has token=None: exact lookup works, board fetch does not.
    """
    u = urllib.parse.urlsplit(url.strip())
    for source, host_pat, path_pat in _ATS_PATTERNS:
        if host_pat.match(u.hostname or ""):
            m = path_pat.match(u.path)
            if m:
                return AtsRef(source, m["token"], m["id"])
    q = dict(urllib.parse.parse_qsl(u.query))
    if q.get("gh_jid", "").isdigit():
        return AtsRef("greenhouse", None, q["gh_jid"])
    return None


def token_from_embed(markup: str) -> str | None:
    """A `gh_jid` URL's page, when Greenhouse's own job board is embedded on it, carries a
    script tag loading `.../embed/job_board(/js)?for=<token>` — that `for=` value is the
    board token the URL itself doesn't carry. None when no such script is on the page
    (a custom-built careers page, or the embed removed since)."""
    m = _EMBED_TOKEN_RE.search(markup)
    return m["token"] if m else None


class _PageParser(HTMLParser):
    """Collect <title>, the longest meta/og description, the declared site name
    (og:site_name / application-name), and every <script type="application/ld+json"> body."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta_description = ""
        self.site_name = ""
        self.application_name = ""
        self.ld_json: list[str] = []
        self._in: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in = "title"
        elif tag == "meta" and (a.get("name") or a.get("property") or "").lower() in ("description", "og:description"):
            content = (a.get("content") or "").strip()
            if len(content) > len(self.meta_description):
                self.meta_description = content
        elif tag == "meta" and (a.get("property") or "").lower() == "og:site_name":
            self.site_name = (a.get("content") or "").strip()
        elif tag == "meta" and (a.get("name") or "").lower() == "application-name":
            self.application_name = (a.get("content") or "").strip()
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._in = "ld"
            self.ld_json.append("")

    def handle_endtag(self, tag):
        self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "ld":
            self.ld_json[-1] += data


def _job_postings(obj) -> list[dict]:
    """Walk a JSON-LD value and return every JobPosting node (top level, @graph, or arrays)."""
    if isinstance(obj, list):
        return [p for o in obj for p in _job_postings(o)]
    if not isinstance(obj, dict):
        return []
    t = obj.get("@type")
    if t == "JobPosting" or (isinstance(t, list) and "JobPosting" in t):
        return [obj]
    return _job_postings(obj.get("@graph", []))


def _address_text(addr) -> str | None:
    if isinstance(addr, str):
        return addr.strip() or None
    if isinstance(addr, dict):
        parts = [addr.get("addressLocality"), addr.get("addressRegion"), addr.get("addressCountry")]
        return ", ".join(p.strip() for p in parts if isinstance(p, str) and p.strip()) or None
    return None


def _place_of(loc) -> str | None:
    """One jobLocation → its address as text. schema.org allows a Place several addresses,
    and get-in-it.de writes even a single one as a list (HIR-268); each is kept."""
    if not isinstance(loc, dict):
        return None
    addr = loc.get("address")
    if isinstance(addr, list):
        return "; ".join(t for t in map(_address_text, addr) if t) or None
    if isinstance(addr, (str, dict)):
        return _address_text(addr)
    return loc.get("name")


def _remote_of(jp: dict) -> str | None:
    """schema.org remote: jobLocationType TELECOMMUTE, with applicantLocationRequirements
    naming where applicants may live → "Remote (Germany, France)" or plain "Remote"."""
    if str(jp.get("jobLocationType") or "").upper() != "TELECOMMUTE":
        return None
    reqs = jp.get("applicantLocationRequirements")
    names = [r.get("name") if isinstance(r, dict) else r
             for r in (reqs if isinstance(reqs, list) else [reqs])]
    names = [n.strip() for n in names if isinstance(n, str) and n.strip()]
    return f"Remote ({', '.join(names)})" if names else "Remote"


def _location_of(jp: dict) -> str | None:
    """Every place the posting lists, "; "-joined — as Greenhouse does — so a multi-office
    posting whose first office is untracked still maps to a tracked city. A remote posting
    adds its remote segment."""
    loc = jp.get("jobLocation")
    places = [_place_of(l) for l in (loc if isinstance(loc, list) else [loc])] + [_remote_of(jp)]
    return "; ".join(p for p in places if p) or None


def _personio_field(flat: str, pattern: str) -> str | None:
    """One string value out of Personio's payload, JSON escapes decoded. None when absent or blank."""
    m = re.search(pattern, flat)
    if not m:
        return None
    try:
        value = json.loads(f'"{m["v"]}"')
    except ValueError:
        value = m["v"]
    return value.strip() or None


def _personio_fields(markup: str) -> tuple[str | None, str | None]:
    """(company, location) out of the Next.js payload a Personio tenant embeds in its page.

    The tenants that serve no JSON-LD still carry the posting as JSON inside a JavaScript
    string, so its quotes arrive backslash-escaped (`\\"main_office\\":\\"Berlin\\"`);
    dropping that escaping first lets one plain pattern read either form. The payload is
    preferred over the visible location label because the label's CSS class carries a
    build hash that changes between Personio releases.

    `main_office` ("Berlin", "Berlin (Remote)") is the city as the page shows it next to
    the title, and `city_of` reads a tracked city out of either; the first office address
    is the fallback, by its `name` and not its `city`, because a remote posting puts
    "Remote" in `city` and the city in `state`. Company is blank on some tenants — those
    still need `--company`.

    `additional_offices` (a list of office names) follows the main office, "; "-joined as
    every other reader does, so a posting whose main office is untracked still maps to a
    tracked city (HIR-289: Cloover lists Wien first and Berlin second).
    """
    flat = markup.replace('\\"', '"')
    company = _personio_field(flat, r'"company_name"\s*:\s*"(?P<v>[^"]*)"')
    main = (_personio_field(flat, r'"main_office"\s*:\s*"(?P<v>[^"]*)"')
            or _personio_field(flat, r'"office_addresses"\s*:\s*\[\s*\{\s*"name"\s*:\s*"(?P<v>[^"]*)"'))
    places = [main] + _personio_list(flat, "additional_offices")
    location = "; ".join(dict.fromkeys(p for p in places if p)) or None
    return company, location


def _personio_list(flat: str, key: str) -> list[str]:
    """A list of strings out of Personio's payload (`"additional_offices":["Berlin"]`).
    Empty when absent, unreadable or not a list of strings."""
    m = re.search(r'"' + key + r'"\s*:\s*(?P<v>\[[^\]]*\])', flat)
    if not m:
        return []
    try:
        values = json.loads(m["v"])
    except ValueError:
        return []
    return [v.strip() for v in values if isinstance(v, str) and v.strip()] if isinstance(values, list) else []


def posting_from_html(url: str, markup: str, company: str | None = None,
                      title: str | None = None, location: str | None = None,
                      notes: list[str] | None = None) -> tuple[Posting, str]:
    """Build a Posting from a careers page. Returns (posting, how), how ∈ {'json-ld', 'page-text', 'meta-description'}.

    JSON-LD JobPosting wins when present: its description is the posting alone. Otherwise
    the whole page's text is the description and the caller's --company/--title fill in
    what the page cannot say for itself. A JavaScript-rendered page (jobs.gem.com) has
    almost no body text; when its meta description is longer, that is the description.
    Explicit flags override JSON-LD fields.

    A Personio tenant that serves no JSON-LD can still give its company and location, out
    of the payload Personio embeds (`_personio_fields`); `--company`/`--location` override
    that too. `how` keeps naming where the *description* came from, which on those pages
    is still the page text.

    Any other page without JSON-LD gives a location only when its text states one on a
    labelled line (`location_from_text`), and its title loses a "Stellendetails" /
    "Job Details" suffix (HIR-268, jobs.bayer.com).
    """
    p = _PageParser()
    p.feed(markup)
    p.close()
    for raw in p.ld_json:
        try:
            nodes = _job_postings(json.loads(raw))
        except ValueError:
            continue
        if nodes:
            jp = nodes[0]
            org = jp.get("hiringOrganization")
            org_name = org.get("name") if isinstance(org, dict) else (org if isinstance(org, str) else None)
            text = html_to_text(jp.get("description") or "")
            return Posting(
                source="url", source_job_id="", url=url,
                company=company or (org_name or "").strip() or None,
                title=title or (jp.get("title") or "").strip() or p.title.strip(),
                location_raw=location or _location_of(jp),
                description_text=text or html_to_text(markup),
                posted_at=jp.get("datePosted"),
            ), "json-ld"
    body_text = html_to_text(markup)
    text, how = body_text, "page-text"
    if len(p.meta_description) > len(text):
        text, how = p.meta_description, "meta-description"
    page_company = page_location = None
    if _PERSONIO_HOST_RE.search(urllib.parse.urlparse(url).hostname or ""):
        page_company, page_location = _personio_fields(markup)
    if not (location or page_location):
        page_location = location_from_text(body_text)
        if page_location and notes is not None:
            notes.append(f"location read from the page's location line: {page_location!r}")
    page_title = _JOB_DETAILS_SUFFIX_RE.sub("", p.title.strip())
    if not (company or page_company):
        page_company, rule = company_from_page(url, p)
        if page_company:
            if rule == "title tail":
                page_title, _ = split_title_tail(page_title)
            if notes is not None:
                notes.append(f"company read from the page's {rule}: {page_company!r}")
    return Posting(
        source="url", source_job_id="", url=url, company=company or page_company,
        title=title or page_title, location_raw=location or page_location,
        description_text=text,
    ), how


def workable_api_url(url: str) -> str | None:
    """A Workable job link (`apply.workable.com/<account>/j/<shortcode>`) → the public API
    address that returns that posting as JSON. Anything else → None."""
    u = urllib.parse.urlsplit(url.strip())
    if (u.hostname or "").lower() != _WORKABLE_HOST:
        return None
    m = _WORKABLE_PATH_RE.match(u.path)
    return f"https://{_WORKABLE_HOST}/api/v2/accounts/{m['account']}/jobs/{m['code']}" if m else None


def _workable_place(loc) -> str | None:
    """{"city": "Berlin", "region": "Berlin", "country": "Germany"} → "Berlin, Germany"."""
    if not isinstance(loc, dict):
        return None
    parts = [p.strip() for p in (loc.get("city"), loc.get("region"), loc.get("country"))
             if isinstance(p, str) and p.strip()]
    return ", ".join(dict.fromkeys(parts)) or None


def posting_from_workable(url: str, payload: dict, company: str | None = None,
                          title: str | None = None, location: str | None = None) -> Posting:
    """Build a Posting from Workable's public job API (HIR-268). Pure.

    Workable builds its job page in the browser, so the fetched page holds only a
    truncated meta description. The API holds the whole posting: the title, every
    location ("; "-joined, plus "Remote" for a remote posting), and the text in the three
    sections the page shows under these same headings. It does not name the company, so
    that is passed in — the caller reads it off the page. `title`/`location` override.

    Raises ValueError when the payload has no title or no text, so the caller can fall
    back to the page.
    """
    sections = [payload.get("description") or ""]
    sections += [f"<h3>{heading}</h3>{payload[key]}"
                 for heading, key in (("Requirements", "requirements"), ("Benefits", "benefits"))
                 if payload.get(key)]
    text = html_to_text("".join(sections))
    api_title = (payload.get("title") or "").strip()
    if not text or not (title or api_title):
        raise ValueError("Workable API returned no title or no text")
    places = [_workable_place(loc) for loc in payload.get("locations") or [payload.get("location")]]
    places.append("Remote" if payload.get("remote") is True else None)
    return Posting(
        source="url", source_job_id="", url=url, company=company,
        title=title or api_title,
        location_raw=location or "; ".join(dict.fromkeys(p for p in places if p)) or None,
        description_text=text,
        posted_at=payload.get("published"),
    )


def containment(stored: str, page: str) -> float:
    """Share of `stored`'s shingles present in `page`. 1.0 = the whole stored JD is on the page."""
    a = dedup.shingles(stored)
    if not a:
        return 0.0
    return len(a & dedup.shingles(page)) / len(a)


@dataclass(frozen=True)
class TextMatch:
    job_id: int
    title: str
    score: float


def best_text_match(conn: sqlite3.Connection, company: str | None, page_text: str,
                    threshold: float = CONTAINMENT_THRESHOLD) -> TextMatch | None:
    ck = dedup.company_key(company)
    if not ck:
        return None
    best = None
    for r in conn.execute("SELECT id, company, title, description_text FROM job WHERE company IS NOT NULL"):
        if dedup.company_key(r["company"]) != ck:
            continue
        s = containment(r["description_text"], page_text)
        if s >= threshold and (best is None or s > best.score):
            best = TextMatch(r["id"], r["title"], s)
    return best


def sources_of(conn: sqlite3.Connection, job_id: int) -> list[str]:
    return [r["source"] for r in conn.execute(
        "SELECT source FROM job_source WHERE job_id=? ORDER BY first_seen", (job_id,))]


def polled_boards(feeds: list[dict]) -> set[tuple[str, str]]:
    return {(f["type"], f["token"]) for f in feeds if f.get("token")}


def diagnose(posting: Posting, ref: AtsRef | None, feeds: list[dict], board_had_it: bool | None) -> str:
    """Why no feed stored this posting. Pure; one sentence, phrased as what to do about it."""
    reasons = []
    if not in_scope_title(posting.title):
        reasons.append(f"title {posting.title!r} fails the title filter (needs an AI/ML term and a role term)")
    if active_place(posting.location_raw, posting.title, posting.description_text) is None:
        city = city_of(posting.location_raw)
        reasons.append(f"location {posting.location_raw!r} maps to {city}, which is tracked but not active "
                       f"(active: {', '.join(ACTIVE_CITIES)})" if city else
                       f"location {posting.location_raw!r} is neither a tracked city nor EU-remote "
                       f"(remote tied to a non-EU country, or no remote signal)")
    if ref is None:
        base = "not a hosted ATS page — no feed can reach it; --add stores it as source=url"
        return base + ("; it would also be dropped: " + "; ".join(reasons) if reasons else "")
    if ref.token is None:
        return (f"{ref.source} job {ref.job_id} via an embed URL — board token unknown "
                f"(the page carries no Greenhouse embed script); re-run with the "
                f"boards.greenhouse.io link to check the board")
    if (ref.source, ref.token) not in polled_boards(feeds):
        hint = json.dumps({"type": ref.source, "enabled": True, "token": ref.token,
                           "company": posting.company or ""})
        return f"board {ref.source}:{ref.token} is not in config/feeds.json — add {hint}"
    if board_had_it is False:
        return f"board {ref.source}:{ref.token} is polled but no longer lists job {ref.job_id} (closed or re-posted under a new id)"
    if reasons:
        return f"board {ref.source}:{ref.token} is polled; ingest would drop it: " + "; ".join(reasons)
    return (f"board {ref.source}:{ref.token} is polled and the posting passes both filters — "
            f"either posted since the last poll (run `poll`) or a feed bug; job id {ref.job_id}")


@dataclass
class CheckResult:
    url: str
    verdict: str                      # 'found' | 'not_found'
    how: str                          # 'ats id' | 'text 0.93' | ''
    job_id: int | None = None
    job_title: str | None = None
    sources: list[str] = field(default_factory=list)
    diagnosis: str = ""
    posting: Posting | None = None    # resolved posting, for --add
    notes: list[str] = field(default_factory=list)

    def line(self) -> str:
        if self.verdict == "found":
            via = ", ".join(self.sources) or "?"
            return f"found: job {self.job_id} {self.job_title!r} ({self.how}; via {via})"
        return f"not found: {self.diagnosis}"


def _fetch_board_posting(ref: AtsRef, fetch_board) -> Posting | None:
    for p in fetch_board(ref.source, ref.token):
        if p.source_job_id == ref.job_id:
            return p
    return None


def default_fetch_board(source: str, token: str) -> list[Posting]:
    """Fetch a company board by its token, through the source registry. Only a board can be
    reached from a token alone, so anything else is a KeyError, as it always was."""
    if source not in registry.BOARD_SOURCES:
        raise KeyError(source)
    return registry.fetch({"type": source, "token": token})


def check_url(conn: sqlite3.Connection, url: str, feeds: list[dict], company: str | None = None,
              title: str | None = None, location: str | None = None,
              fetch_page=fetch_text, fetch_board=default_fetch_board) -> CheckResult:
    """The whole check. Reads the DB, never writes it."""
    ref = parse_ats_url(url)
    result = CheckResult(url=url, verdict="not_found", how="")

    # 1. Exact: the feed's own id for this job.
    if ref is not None:
        row = conn.execute("SELECT job_id FROM job_source WHERE source=? AND source_job_id=?",
                           (ref.source, ref.job_id)).fetchone()
        if row:
            return _found(conn, result, row["job_id"], "ats id")

    # 1b. An embed URL names the job but not the board; the page it points at may carry
    # Greenhouse's own embed script, which does. Fetch it once and reuse it below either way.
    markup: str | None = None
    if ref is not None and ref.token is None:
        markup = fetch_page(url)
        resolved = token_from_embed(markup)
        if resolved:
            ref = AtsRef(ref.source, resolved, ref.job_id)
            result.notes.append(f"board token {resolved!r} read from the embed script")
        else:
            result.notes.append("page carries no Greenhouse embed script — board token still unknown")

    # 2. Resolve the posting text: from the board API when we know the board, else the page.
    posting: Posting | None = None
    board_had_it: bool | None = None
    if ref is not None and ref.token is not None:
        try:
            posting = _fetch_board_posting(ref, fetch_board)
            board_had_it = posting is not None
        except Exception as e:  # board unreachable → fall back to the page itself
            result.notes.append(f"board fetch failed: {type(e).__name__}: {str(e)[:120]}")
    if posting is None:
        posting, how = posting_from_html(url, markup if markup is not None else fetch_page(url),
                                         company, title, location, notes=result.notes)
        # A Workable page is built in the browser, so the page gave the company (its title
        # tail) and little else; the title, location and text come from Workable's API.
        api_url = workable_api_url(url)
        if api_url:
            try:
                posting = posting_from_workable(url, json.loads(fetch_page(api_url)),
                                                posting.company, title, location)
                how = "the Workable API"
            except Exception as e:  # API unreachable or empty → keep what the page gave
                result.notes.append(f"Workable API read failed: {type(e).__name__}: {str(e)[:120]}")
        result.notes.append(f"read posting from {how}")
    else:
        # Lever and Ashby boards don't name the company; the board token is its slug
        # ("almedia" ↔ "Almedia GmbH" under company_key), so use it unless told otherwise.
        fallback = company or posting.company or ref.token
        if fallback != posting.company or title or location:
            posting = Posting(posting.source, posting.source_job_id, posting.url, fallback,
                              title or posting.title, location or posting.location_raw,
                              posting.description_text, posting.posted_at)
            if not company and fallback == ref.token:
                result.notes.append(f"company taken from board token: {ref.token!r}")
    result.posting = posting

    # 3. Same company, stored under another source?
    m = best_text_match(conn, posting.company, posting.description_text)
    if m:
        return _found(conn, result, m.job_id, f"text {m.score:.2f}")
    if not dedup.company_key(posting.company):
        result.notes.append("company unknown — pass --company to enable the text match")

    result.diagnosis = diagnose(posting, ref, feeds, board_had_it)
    return result


def _found(conn, result: CheckResult, job_id: int, how: str) -> CheckResult:
    result.verdict, result.how, result.job_id = "found", how, job_id
    result.job_title = conn.execute("SELECT title FROM job WHERE id=?", (job_id,)).fetchone()["title"]
    result.sources = sources_of(conn, job_id)
    return result


def feed_had_it(result: CheckResult) -> bool:
    """Pure: the check found the posting and at least one feed had stored it."""
    return result.verdict == "found" and any(s not in MANUAL_SOURCES for s in result.sources)


def log_check(conn: sqlite3.Connection, result: CheckResult, found_via: str | None, now: str) -> None:
    conn.execute(
        "INSERT INTO url_check (url, checked_at, found_via, verdict, job_id, feed_had_it, diagnosis)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (result.url, now, found_via, result.verdict, result.job_id, int(feed_had_it(result)),
         result.diagnosis or None))
    conn.commit()


def checked_coverage(conn: sqlite3.Connection) -> tuple[int, int]:
    """(URLs whose first check found the posting already in a feed, distinct URLs checked)."""
    row = conn.execute("""
        SELECT count(*) total, coalesce(sum(c.feed_had_it), 0) covered
        FROM url_check c
        WHERE c.id = (SELECT min(id) FROM url_check WHERE url = c.url)
    """).fetchone()
    return row["covered"], row["total"]


FEED_HAD_IT, BOARD_ADDED, BOARD_NOT_ADDED, NO_FEED = (
    "feed had it", "board added since", "board not added", "no feed can reach it")


def reach_of(url: str, had_it: bool, feeds: list[dict]) -> str:
    """Pure: one checked URL's coverage, judged by today's parser and feeds. A miss on a
    board that has since been added is now covered; a page no adapter recognizes (careers
    sites, recruiters, Gem) can only ever be added by hand."""
    if had_it:
        return FEED_HAD_IT
    ref = parse_ats_url(url)
    if ref is None or ref.token is None:
        return NO_FEED
    return BOARD_ADDED if (ref.source, ref.token) in polled_boards(feeds) else BOARD_NOT_ADDED


def reach_breakdown(conn: sqlite3.Connection, feeds: list[dict]) -> dict[str, int]:
    """{reach_of kind: count} over the first check of each URL, in a fixed order."""
    rows = conn.execute("""
        SELECT c.url, c.feed_had_it FROM url_check c
        WHERE c.id = (SELECT min(id) FROM url_check WHERE url = c.url)
    """).fetchall()
    out = dict.fromkeys((FEED_HAD_IT, BOARD_ADDED, BOARD_NOT_ADDED, NO_FEED), 0)
    for r in rows:
        out[reach_of(r["url"], bool(r["feed_had_it"]), feeds)] += 1
    return out


def job_coverage(conn: sqlite3.Connection) -> tuple[int, int, int]:
    """(jobs a feed has seen, jobs counted, legacy imports left out). A legacy import is a job
    with a screenshot first seen before REBUILD_START: collected by the old method, so it
    says nothing about what today's feeds miss."""
    legacy = ("EXISTS (SELECT 1 FROM job_source s WHERE s.job_id = j.id"
              " AND s.source = 'screenshot' AND s.first_seen < :start)")
    feed = f"EXISTS (SELECT 1 FROM job_source s WHERE s.job_id = j.id AND s.source NOT IN {MANUAL_SOURCES})"
    row = conn.execute(f"""
        SELECT coalesce(sum(CASE WHEN {legacy} THEN 0 ELSE 1 END), 0) counted,
               coalesce(sum(CASE WHEN {legacy} THEN 0 WHEN {feed} THEN 1 ELSE 0 END), 0) seen,
               coalesce(sum(CASE WHEN {legacy} THEN 1 ELSE 0 END), 0) legacy
        FROM job j
    """, {"start": REBUILD_START}).fetchone()
    return row["seen"], row["counted"], row["legacy"]
