"""Given a careers-page URL, say whether that posting is already in the database — and if
not, why the feeds could not have stored it. This is how feed coverage gets audited by hand.

Does:
  - recognize hosted ATS job URLs (Greenhouse, Lever, Ashby) and turn them into
    (source, board token, job id);
  - look the job up by exact (source, source_job_id), then by company + text containment
    against stored jobs (the page may have been stored via another source, e.g. arbeitnow);
  - for a page that is not a known ATS, read the posting out of JSON-LD `JobPosting` when
    the page has it, otherwise the stripped page text;
  - diagnose a miss: board not in config/feeds.json; board polled but the title or city
    filter would have dropped it; board polled and it would have passed (a feed bug, or
    posted since the last poll); not a feed-reachable page at all.

  - log each check (`log_check`) and report coverage over the logged checks
    (`checked_coverage`): of the URLs a person checked, how many a feed already had.

Does NOT: write anything but the url_check log (the CLI's --add hands the resolved Posting
to app.ingest), call a model, or fetch LinkedIn (its pages are not readable without a login
and the project does not scrape it).

Invariants: `parse_ats_url`, `posting_from_html`, `containment`, `diagnose` and
`feed_had_it` are pure; `check_url` reads the DB and never writes it, and does network I/O
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
from app.geo import city_of
from app.html_text import html_to_text
from app.ingest import in_scope_title
from app.sources import Posting, ashby, fetch_text, greenhouse, lever

CONTAINMENT_THRESHOLD = 0.7   # share of a stored JD's 3-word shingles that must appear on the page
MANUAL_SOURCES = ("url", "paste", "screenshot")   # job_source values a person added; the rest are feeds

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
)
_FETCHERS = {"greenhouse": greenhouse.fetch, "lever": lever.fetch, "ashby": ashby.fetch}


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


class _PageParser(HTMLParser):
    """Collect <title> and every <script type="application/ld+json"> body."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.ld_json: list[str] = []
        self._in: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in = "title"
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


def _location_of(jp: dict) -> str | None:
    loc = jp.get("jobLocation")
    if isinstance(loc, list):
        loc = loc[0] if loc else None
    if not isinstance(loc, dict):
        return None
    addr = loc.get("address")
    if isinstance(addr, str):
        return addr
    if isinstance(addr, dict):
        parts = [addr.get("addressLocality"), addr.get("addressRegion"), addr.get("addressCountry")]
        return ", ".join(p for p in parts if isinstance(p, str) and p) or None
    return loc.get("name")


def posting_from_html(url: str, markup: str, company: str | None = None,
                      title: str | None = None, location: str | None = None) -> tuple[Posting, str]:
    """Build a Posting from a careers page. Returns (posting, how), how ∈ {'json-ld', 'page-text'}.

    JSON-LD JobPosting wins when present: its description is the posting alone. Otherwise
    the whole page's text is the description and the caller's --company/--title fill in
    what the page cannot say for itself. Explicit flags override JSON-LD fields.
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
                company=company or org_name,
                title=title or (jp.get("title") or "").strip() or p.title.strip(),
                location_raw=location or _location_of(jp),
                description_text=text or html_to_text(markup),
                posted_at=jp.get("datePosted"),
            ), "json-ld"
    return Posting(
        source="url", source_job_id="", url=url, company=company,
        title=title or p.title.strip(), location_raw=location,
        description_text=html_to_text(markup),
    ), "page-text"


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
    if city_of(posting.location_raw) is None:
        reasons.append(f"location {posting.location_raw!r} maps to no tracked city")
    if ref is None:
        base = "not a hosted ATS page — no feed can reach it; --add stores it as source=url"
        return base + ("; it would also be dropped: " + "; ".join(reasons) if reasons else "")
    if ref.token is None:
        return (f"{ref.source} job {ref.job_id} via an embed URL — board token unknown; "
                f"re-run with the boards.greenhouse.io link to check the board")
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
    return _FETCHERS[source](token)


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
        posting, how = posting_from_html(url, fetch_page(url), company, title, location)
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
