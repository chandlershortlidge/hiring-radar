import json

import pytest

from app import db
from app.check import (AtsRef, CheckResult, check_url, checked_coverage, containment, diagnose,
                       job_coverage, reach_breakdown, reach_of,
                       feed_had_it, log_check, parse_ats_url, posting_from_html)
from app.geo import city_of
from app.ingest import ingest_one
from app.sources import Posting

JD = ("AI Engineer. Requirements: 3+ years Python, experience with LLM applications, RAG "
      "pipelines and vector databases. Nice to have: Kubernetes, AWS. We build agents in Berlin "
      "and ship to production every week with a small, senior team.")
GH_URL = "https://boards.greenhouse.io/acme/jobs/4012345"
FEEDS = [{"type": "arbeitnow", "enabled": True},
         {"type": "greenhouse", "enabled": True, "token": "acme", "company": "Acme GmbH"}]


def posting(source="arbeitnow", sid="a1", company="Acme GmbH", title="AI Engineer (m/w/d)",
            location="Berlin", text=JD, url="https://x/a1"):
    return Posting(source, sid, url, company, title, location, text)


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def page(text=JD, title="AI Engineer - Acme", ld=None):
    ld_tag = f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    return (f"<html><head><title>{title}</title>{ld_tag}</head><body><nav>Home Jobs About</nav>"
            f"<main><h1>{title}</h1><p>{text}</p></main><footer>© Acme 2026 · Imprint · Privacy</footer>"
            f"</body></html>")


def no_fetch(*a, **k):
    raise AssertionError("network fetch should not happen")


# --- URL parsing ------------------------------------------------------------------------

@pytest.mark.parametrize("url,expected", [
    (GH_URL, AtsRef("greenhouse", "acme", "4012345")),
    ("https://job-boards.eu.greenhouse.io/acme/jobs/4012345?gh_src=x", AtsRef("greenhouse", "acme", "4012345")),
    ("https://acme.com/careers?gh_jid=4012345", AtsRef("greenhouse", None, "4012345")),
    ("https://jobs.lever.co/acme/0a1b2c3d-1111-2222-3333-444455556666/apply",
     AtsRef("lever", "acme", "0a1b2c3d-1111-2222-3333-444455556666")),
    ("https://jobs.ashbyhq.com/acme/0a1b2c3d-1111-2222-3333-444455556666",
     AtsRef("ashby", "acme", "0a1b2c3d-1111-2222-3333-444455556666")),
    ("https://acme.com/careers/ai-engineer", None),
    ("https://www.linkedin.com/jobs/view/4012345", None),
    ("https://join.com/companies/xheroncom/16814436-ai-harness-engineer-m-f-x?widgetv2=true",
     AtsRef("join", "xheroncom", "16814436")),
    ("https://join.com/companies/dexter-health", None),
    ("https://boards.greenhouse.io/acme", None),
])
def test_parse_ats_url(url, expected):
    assert parse_ats_url(url) == expected


# --- page → posting ----------------------------------------------------------------------

def test_json_ld_job_posting_wins_over_page_text():
    ld = {"@context": "https://schema.org", "@type": "JobPosting", "title": "AI Engineer",
          "hiringOrganization": {"@type": "Organization", "name": "Acme GmbH"},
          "jobLocation": {"@type": "Place", "address": {"addressLocality": "Berlin", "addressCountry": "DE"}},
          "description": "<p>" + JD + "</p>", "datePosted": "2026-10-01"}
    p, how = posting_from_html("https://acme.com/j/1", page(ld=ld))
    assert how == "json-ld"
    assert (p.source, p.company, p.title, p.location_raw, p.posted_at) == ("url", "Acme GmbH", "AI Engineer", "Berlin, DE", "2026-10-01")
    assert p.description_text == JD          # not the nav/footer
    assert "Imprint" not in p.description_text


def test_json_ld_multi_office_keeps_every_location():
    # Phenom (careers.bcg.com) lists offices in jobLocation order; Berlin is not first.
    ld = {"@type": "JobPosting", "title": "AI Associate", "description": JD, "jobLocation": [
        {"@type": "Place", "address": {"addressLocality": "Cologne", "addressRegion": "", "addressCountry": "Germany"}},
        {"@type": "Place", "address": {"addressLocality": " Berlin", "addressRegion": "", "addressCountry": "Germany"}},
    ]}
    p, _ = posting_from_html("u", page(ld=ld))
    assert p.location_raw == "Cologne, Germany; Berlin, Germany"
    assert city_of(p.location_raw) == "Berlin"


def test_json_ld_in_graph_and_flag_overrides():
    ld = {"@graph": [{"@type": "WebSite"}, {"@type": ["JobPosting"], "title": "Engineer", "description": JD}]}
    p, how = posting_from_html("u", page(ld=ld), company="Override Co", title="ML Engineer")
    assert how == "json-ld" and p.company == "Override Co" and p.title == "ML Engineer"


def test_plain_page_falls_back_to_title_tag_and_page_text():
    p, how = posting_from_html("u", page(), company="Acme GmbH")
    assert how == "page-text"
    assert p.title == "AI Engineer - Acme" and p.company == "Acme GmbH" and p.location_raw is None
    assert "Imprint" in p.description_text    # whole page; that is why matching uses containment


def test_script_rendered_page_falls_back_to_meta_description():
    # jobs.gem.com: empty body until JavaScript runs; the JD sits in the meta description.
    markup = ('<html><head><title>Machine Learning Engineer</title>'
              f'<meta name="description" content="{JD}"><meta property="og:description" content="short">'
              '</head><body><div id="root"></div><script>app()</script></body></html>')
    p, how = posting_from_html("u", markup)
    assert how == "meta-description" and p.description_text == JD


def test_page_text_wins_over_a_shorter_meta_description():
    p, how = posting_from_html("u", page().replace("<head>", '<head><meta name="description" content="Jobs at Acme">'))
    assert how == "page-text"


def test_containment_is_one_directional():
    noisy = page()
    assert containment(JD, noisy) == 1.0
    assert containment(noisy, JD) < 0.7
    assert containment("", JD) == 0.0


# --- the check ----------------------------------------------------------------------------

def test_found_by_ats_id_without_any_fetch(conn):
    ingest_one(conn, posting(source="greenhouse", sid="4012345", url=GH_URL))
    r = check_url(conn, GH_URL, FEEDS, fetch_page=no_fetch, fetch_board=no_fetch)
    assert r.verdict == "found" and r.job_id == 1 and r.how == "ats id" and r.sources == ["greenhouse"]
    assert r.line().startswith("found: job 1 'AI Engineer (m/w/d)' (ats id; via greenhouse)")


def test_found_by_text_when_stored_via_another_source(conn):
    ingest_one(conn, posting())   # came in through arbeitnow
    board = [posting(source="greenhouse", sid="4012345", company="Acme", text=JD, url=GH_URL)]
    r = check_url(conn, GH_URL, FEEDS, fetch_page=no_fetch, fetch_board=lambda s, t: board)
    assert r.verdict == "found" and r.job_id == 1 and r.how == "text 1.00" and r.sources == ["arbeitnow"]
    assert r.posting is not None and r.posting.source == "greenhouse"   # --add would record the sighting


def test_plain_careers_page_matches_stored_jd_through_nav_noise(conn):
    ingest_one(conn, posting())
    r = check_url(conn, "https://acme.com/careers/ai", FEEDS, company="ACME GmbH",
                  fetch_page=lambda u: page(), fetch_board=no_fetch)
    assert r.verdict == "found" and r.how == "text 1.00"
    assert "read posting from page-text" in r.notes


def test_not_found_board_not_polled_says_what_to_add(conn):
    url = "https://jobs.lever.co/newco/0a1b2c3d-1111-2222-3333-444455556666"
    board = [Posting("lever", "0a1b2c3d-1111-2222-3333-444455556666", url, "NewCo", "AI Engineer", "Berlin", JD)]
    r = check_url(conn, url, FEEDS, fetch_page=no_fetch, fetch_board=lambda s, t: board)
    assert r.verdict == "not_found"
    assert r.diagnosis.startswith("board lever:newco is not in config/feeds.json — add ")
    assert json.loads(r.diagnosis.split("add ", 1)[1]) == {"type": "lever", "enabled": True, "token": "newco", "company": "NewCo"}


def test_not_found_board_polled_but_filter_drops_it(conn):
    board = [posting(source="greenhouse", sid="4012345", title="Account Executive, AI", location="Remote (Germany)", url=GH_URL)]
    r = check_url(conn, GH_URL, FEEDS, fetch_page=no_fetch, fetch_board=lambda s, t: board)
    assert r.verdict == "not_found"
    assert "is polled; ingest would drop it" in r.diagnosis
    assert "fails the title filter" in r.diagnosis and "maps to no tracked city" in r.diagnosis


def test_not_found_board_polled_and_posting_passes_is_a_feed_question(conn):
    board = [posting(source="greenhouse", sid="4012345", url=GH_URL)]
    r = check_url(conn, GH_URL, FEEDS, fetch_page=no_fetch, fetch_board=lambda s, t: board)
    assert r.verdict == "not_found" and "passes both filters" in r.diagnosis and "4012345" in r.diagnosis


def test_not_found_board_no_longer_lists_it_falls_back_to_page(conn):
    r = check_url(conn, GH_URL, FEEDS, fetch_page=lambda u: page(), fetch_board=lambda s, t: [])
    assert r.verdict == "not_found" and "no longer lists job 4012345" in r.diagnosis


def test_board_fetch_failure_falls_back_to_page_and_is_noted(conn):
    def boom(s, t):
        raise OSError("timed out")
    r = check_url(conn, GH_URL, FEEDS, company="Acme", fetch_page=lambda u: page(), fetch_board=boom)
    assert r.verdict == "not_found"
    assert any(n.startswith("board fetch failed: OSError") for n in r.notes)


def test_plain_page_without_company_cannot_text_match_and_says_so(conn):
    ingest_one(conn, posting())
    r = check_url(conn, "https://acme.com/careers/ai", FEEDS, fetch_page=lambda u: page(), fetch_board=no_fetch)
    assert r.verdict == "not_found"
    assert r.diagnosis.startswith("not a hosted ATS page")
    assert any("pass --company" in n for n in r.notes)


def test_greenhouse_embed_url_exact_hit_but_no_board_check(conn):
    url = "https://acme.com/careers?gh_jid=4012345"
    r = check_url(conn, url, FEEDS, fetch_page=lambda u: page(), fetch_board=no_fetch)
    assert r.verdict == "not_found" and "board token unknown" in r.diagnosis
    ingest_one(conn, posting(source="greenhouse", sid="4012345"))
    assert check_url(conn, url, FEEDS, fetch_page=no_fetch, fetch_board=no_fetch).verdict == "found"


def test_diagnose_is_pure_and_names_the_filter():
    p = Posting("url", "", "u", "Acme", "Call Center Agent", "Berlin", JD)
    assert "fails the title filter" in diagnose(p, None, FEEDS, None)
    assert "no feed can reach it" in diagnose(p, None, FEEDS, None)


def test_board_without_company_uses_board_token_for_the_match(conn):
    ingest_one(conn, posting(company="Almedia GmbH"))   # stored via arbeitnow
    url = "https://jobs.ashbyhq.com/almedia/0a1b2c3d-1111-2222-3333-444455556666"
    board = [Posting("ashby", "0a1b2c3d-1111-2222-3333-444455556666", url, None, "AI Engineer", "Berlin", JD)]
    r = check_url(conn, url, FEEDS, fetch_page=no_fetch, fetch_board=lambda s, t: board)
    assert r.verdict == "found" and r.job_id == 1 and r.sources == ["arbeitnow"]
    assert "company taken from board token: 'almedia'" in r.notes
    assert r.posting.company == "almedia"


def test_board_without_company_not_found_hint_names_the_token(conn):
    url = "https://jobs.ashbyhq.com/almedia/0a1b2c3d-1111-2222-3333-444455556666"
    board = [Posting("ashby", "0a1b2c3d-1111-2222-3333-444455556666", url, None, "AI Engineer", "Berlin", JD)]
    r = check_url(conn, url, FEEDS, fetch_page=no_fetch, fetch_board=lambda s, t: board)
    assert r.verdict == "not_found"
    assert json.loads(r.diagnosis.split("add ", 1)[1])["company"] == "almedia"
    assert not any("pass --company" in n for n in r.notes)


# --- check log and checked-URL coverage ---------------------------------------------------

T1, T2 = "2026-10-17T10:00:00Z", "2026-10-17T10:05:00Z"


def test_feed_had_it_needs_a_feed_source():
    assert feed_had_it(CheckResult("u", "found", "ats id", sources=["greenhouse"]))
    assert feed_had_it(CheckResult("u", "found", "text 0.9", sources=["screenshot", "arbeitnow"]))
    assert not feed_had_it(CheckResult("u", "found", "text 0.9", sources=["screenshot", "url"]))
    assert not feed_had_it(CheckResult("u", "not_found", "", sources=[]))


def test_logged_check_counts_a_feed_hit_and_a_miss(conn):
    ingest_one(conn, posting(source="greenhouse", sid="4012345", url=GH_URL))
    hit = check_url(conn, GH_URL, FEEDS, fetch_page=no_fetch, fetch_board=no_fetch)
    log_check(conn, hit, "linkedin", T1)
    url = "https://jobs.lever.co/newco/0a1b2c3d-1111-2222-3333-444455556666"
    board = [Posting("lever", "0a1b2c3d-1111-2222-3333-444455556666", url, "NewCo", "AI Engineer", "Berlin", JD)]
    miss = check_url(conn, url, FEEDS, fetch_page=no_fetch, fetch_board=lambda s, t: board)
    log_check(conn, miss, "linkedin", T1)
    assert checked_coverage(conn) == (1, 2)
    row = conn.execute("SELECT * FROM url_check WHERE verdict='not_found'").fetchone()
    assert row["job_id"] is None and row["found_via"] == "linkedin"
    assert row["diagnosis"].startswith("board lever:newco is not in config/feeds.json")


def test_recheck_after_poll_does_not_count_as_the_feed_having_had_it(conn):
    # The /check-url flow: miss → add board → poll → re-check finds it. Only the first check counts.
    url = "https://jobs.lever.co/newco/0a1b2c3d-1111-2222-3333-444455556666"
    board = [Posting("lever", "0a1b2c3d-1111-2222-3333-444455556666", url, "NewCo", "AI Engineer", "Berlin", JD)]
    log_check(conn, check_url(conn, url, FEEDS, fetch_page=no_fetch, fetch_board=lambda s, t: board), "linkedin", T1)
    ingest_one(conn, board[0])   # what the poll does once the board is in feeds.json
    again = check_url(conn, url, FEEDS, fetch_page=no_fetch, fetch_board=no_fetch)
    assert again.verdict == "found"
    log_check(conn, again, "linkedin", T2)
    assert checked_coverage(conn) == (0, 1)


def test_found_only_via_a_manual_add_is_not_feed_coverage(conn):
    ingest_one(conn, posting(source="url", sid="https://acme.com/careers/ai", url="https://acme.com/careers/ai"),
               require_city=False, found_via="company_site", trust_title=True)
    r = check_url(conn, "https://acme.com/careers/ai", FEEDS, company="Acme GmbH",
                  fetch_page=lambda u: page(), fetch_board=no_fetch)
    assert r.verdict == "found"
    log_check(conn, r, "linkedin", T1)
    assert checked_coverage(conn) == (0, 1)


def test_no_checks_logged_is_zero_of_zero(conn):
    assert checked_coverage(conn) == (0, 0)


# --- reach and job coverage (stats) ----------------------------------------------------

def test_reach_of_judges_a_checked_url_by_todays_feeds():
    lever = "https://jobs.lever.co/newco/0a1b2c3d-1111-2222-3333-444455556666"
    assert reach_of(GH_URL, True, FEEDS) == "feed had it"
    assert reach_of(GH_URL, False, FEEDS) == "board added since"            # acme is polled now
    assert reach_of(lever, False, FEEDS) == "board not added"
    assert reach_of("https://careers.tieto.com/job/x", False, FEEDS) == "no feed can reach it"
    assert reach_of("https://acme.com/careers?gh_jid=4012345", False, FEEDS) == "no feed can reach it"


def test_reach_breakdown_counts_first_checks_only(conn):
    for url, had, at in ((GH_URL, 0, T1), (GH_URL, 1, T2), ("https://acme.com/j/1", 0, T1)):
        conn.execute("INSERT INTO url_check (url, checked_at, verdict, feed_had_it) VALUES (?, ?, 'found', ?)",
                     (url, at, had))
    assert reach_breakdown(conn, FEEDS) == {"feed had it": 0, "board added since": 1,
                                            "board not added": 0, "no feed can reach it": 1}


def test_job_coverage_leaves_out_legacy_screenshot_imports(conn):
    ingest_one(conn, posting(sid="a1"))                                           # feed
    ingest_one(conn, posting(source="url", sid="", company="B Co", text="b " + JD), require_city=False)
    legacy = ingest_one(conn, posting(source="screenshot", sid="", company="C Co", text="c " + JD),
                        "2026-06-11T09:00:00Z", require_city=False)
    new_shot = ingest_one(conn, posting(source="screenshot", sid="", company="D Co", text="d " + JD),
                          "2026-10-18T09:00:00Z", require_city=False)
    assert legacy.startswith("new:") and new_shot.startswith("new:")
    assert job_coverage(conn) == (1, 3, 1)   # feed 1 of (feed, url, new screenshot); 1 legacy out
