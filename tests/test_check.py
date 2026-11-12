import json
from pathlib import Path

import pytest

from app import check, db, geo
from app.check import (AtsRef, CheckResult, check_url, checked_coverage, containment, diagnose,
                       job_coverage, reach_breakdown, reach_of,
                       feed_had_it, log_check, parse_ats_url, posting_from_html, token_from_embed)
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


PAGES = Path(__file__).parent / "fixtures" / "pages"


def saved_page(name):
    """A saved copy of a real page (tests/fixtures/pages), as the checker would fetch it."""
    return (PAGES / name).read_text(encoding="utf-8")


def no_fetch(*a, **k):
    raise AssertionError("network fetch should not happen")


def embed_script(token, host="boards.greenhouse.io"):
    """What a company's careers page carries when it embeds its Greenhouse board."""
    return f'<script src="https://{host}/embed/job_board/js?for={token}"></script>'


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


# --- embed-script board token resolution (HIR-31) -----------------------------------------

def test_token_from_embed_reads_the_for_parameter():
    markup = page().replace("</body>", embed_script("acme") + "</body>")
    assert token_from_embed(markup) == "acme"


@pytest.mark.parametrize("host", ["boards.greenhouse.io", "boards.eu.greenhouse.io", "job-boards.greenhouse.io"])
def test_token_from_embed_any_greenhouse_embed_host(host):
    markup = page().replace("</body>", embed_script("acme", host) + "</body>")
    assert token_from_embed(markup) == "acme"


def test_token_from_embed_tolerates_other_query_params_either_side_of_for():
    before = page().replace("</body>", '<script src="https://boards.greenhouse.io/embed/job_board/js?gh_src=x&for=acme"></script></body>')
    after = page().replace("</body>", '<script src="https://boards.greenhouse.io/embed/job_board/js?for=acme&gh_src=x"></script></body>')
    assert token_from_embed(before) == token_from_embed(after) == "acme"


def test_token_from_embed_none_without_the_script():
    assert token_from_embed(page()) is None


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


def test_json_ld_address_given_as_a_list_is_read():
    # get-in-it.de writes a Place's address as a list, even when there is only one.
    place = {"@type": "Place", "address": [
        {"@type": "PostalAddress", "addressLocality": "Berlin", "addressCountry": "DE"},
        {"@type": "PostalAddress", "addressLocality": "Hamburg", "addressCountry": "DE"}, "", None]}
    ld = {"@type": "JobPosting", "title": "Data Scientist", "description": JD, "jobLocation": place}
    p, _ = posting_from_html("u", page(ld=ld))
    assert p.location_raw == "Berlin, DE; Hamburg, DE"
    ld["jobLocation"] = {"@type": "Place", "address": []}
    assert posting_from_html("u", page(ld=ld))[0].location_raw is None


def test_get_in_it_page_gives_a_berlin_location():
    """HIR-268: the saved page of the posting that was read as having no location."""
    url = "https://www.get-in-it.de/jobsuche/p314335-07f00735/07f00735"
    p, how = posting_from_html(url, saved_page("get_in_it.html"))
    assert how == "json-ld"
    assert (p.company, p.title) == ("smartclip", "Data Scientist (w/m/d) – Applied AI")
    assert p.location_raw == "Berlin, Berlin, DE"
    assert geo.active_place(p.location_raw, p.title, p.description_text) == "Berlin"


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


# --- location and title read off a page with no structured data (HIR-268) -------------------

def test_bayer_page_gives_a_berlin_location_and_a_clean_title():
    """The saved page of the posting that was read with no location and a title ending in
    "Stellendetails". The page has no JSON-LD; its posting text has a "Location:" line."""
    url = "https://jobs.bayer.com/job/Berlin-Agentic-AI-Internship-%28All-Genders%29-Berl/1447659333/"
    notes = []
    p, how = posting_from_html(url, saved_page("bayer.html"), notes=notes)
    assert how == "page-text"
    assert (p.company, p.title) == ("Bayer AG", "Agentic AI Internship (All Genders)")
    assert p.location_raw == "Deutschland : Berlin : Berlin"
    assert geo.active_place(p.location_raw, p.title, p.description_text) == "Berlin"
    assert "location read from the page's location line: 'Deutschland : Berlin : Berlin'" in notes


@pytest.mark.parametrize("line,expected", [
    ("Location: Berlin", "Berlin"),
    ("Standort:   Berlin,  Deutschland", "Berlin, Deutschland"),
    ("  einsatzort : München", "München"),
    ("Location:​ \xa0 Deutschland : Berlin : Berlin​", "Deutschland : Berlin : Berlin"),
])
def test_location_line_is_read_from_page_text(line, expected):
    assert check.location_from_text(f"AI Engineer\n{line}\nRequirements\n- Python") == expected


@pytest.mark.parametrize("text", [
    "We build agents in Berlin.",                         # a place, but not on a labelled line
    "Our location: Berlin",                               # the label must start the line
    "Location:\nBerlin",                                  # nothing on the line itself
    "Location: " + "we are a remote-first company with offices in many places " * 2,   # a sentence
])
def test_text_without_a_short_location_line_gives_no_location(text):
    assert check.location_from_text(text) is None


def test_first_usable_location_line_wins():
    text = "Location: " + "x" * 100 + "\nStandort: Berlin\nLocation: Munich"
    assert check.location_from_text(text) == "Berlin"


def test_location_flag_and_json_ld_are_not_overridden_by_a_location_line():
    markup = page().replace("<main>", "<main><p>Location: Munich</p>")
    assert posting_from_html("u", markup)[0].location_raw == "Munich"
    assert posting_from_html("u", markup, location="Berlin")[0].location_raw == "Berlin"
    ld = {"@type": "JobPosting", "title": "AI Engineer", "description": JD,
          "jobLocation": {"@type": "Place", "address": {"addressLocality": "Berlin"}}}
    assert posting_from_html("u", page(ld=ld).replace("<main>", "<main><p>Location: Munich</p>")
                             )[0].location_raw == "Berlin"


@pytest.mark.parametrize("title,expected", [
    ("AI Engineer Stellendetails | NewCo", "AI Engineer"),
    ("AI Engineer Job Details | NewCo", "AI Engineer"),
    ("AI Engineer Stellendetails", "AI Engineer"),
    ("Job Details Analyst | NewCo", "Job Details Analyst"),       # only a suffix is page furniture
])
def test_job_details_suffix_is_not_part_of_the_title(title, expected):
    assert posting_from_html("u", page(title=title), company="NewCo" if "|" not in title else None
                             )[0].title == expected


def test_job_details_suffix_goes_even_when_the_tail_stays_in_the_title():
    # --company given, so the title's tail is not used and stays; the suffix still goes.
    p, _ = posting_from_html("u", page(title="AI Engineer Stellendetails | NewCo"), company="Told Co")
    assert p.title == "AI Engineer | NewCo"


# --- company read off the page (HIR-198) ---------------------------------------------------

def tagged(tag, title="AI Engineer"):
    return page(title=title).replace("<head>", f"<head>{tag}")


def test_company_from_og_site_name_wins_over_the_title_tail():
    markup = tagged('<meta property="og:site_name" content="NewCo GmbH">', title="AI Engineer | Other Co")
    p, _ = posting_from_html("https://careers.newco.de/j/1", markup)
    assert p.company == "NewCo GmbH"
    assert p.title == "AI Engineer | Other Co"   # the title is only trimmed when its tail is used


def test_application_name_meta_counts_as_the_site_name():
    p, _ = posting_from_html("u", tagged('<meta name="application-name" content="NewCo">'))
    assert p.company == "NewCo"


def test_generic_site_name_is_skipped_for_the_next_rule():
    markup = tagged('<meta property="og:site_name" content="Personio">', title="AI Engineer | NewCo")
    p, _ = posting_from_html("u", markup)
    assert p.company == "NewCo"


@pytest.mark.parametrize("title", ["AI Engineer | NewCo", "AI Engineer – NewCo",
                                   "AI Engineer - NewCo", "AI Engineer at NewCo"])
def test_company_from_title_tail_each_separator_and_the_title_is_trimmed(title):
    p, _ = posting_from_html("u", page(title=title))
    assert p.company == "NewCo" and p.title == "AI Engineer"


def test_title_tail_takes_the_last_separator():
    p, _ = posting_from_html("u", page(title="AI Engineer - NLP | NewCo"))
    assert p.company == "NewCo" and p.title == "AI Engineer - NLP"


@pytest.mark.parametrize("tail", ["Jobs", "Careers", "Karriere", "Join us", "LinkedIn", "J…"])
def test_generic_or_truncated_title_tails_are_not_companies(tail):
    # No site name and the personio host is skipped by the domain rule, so a rejected tail
    # leaves the company unset.
    p, _ = posting_from_html("https://acto.jobs.personio.com/job/1", page(title=f"AI Engineer | {tail}"))
    assert p.company is None
    assert p.title == f"AI Engineer | {tail}"    # a tail not used as the company stays in the title


def test_company_from_the_hostname_as_a_last_resort():
    p, _ = posting_from_html("https://careers.newco.de/j/1", page(title="AI Engineer"))
    assert p.company == "Newco"


def test_hostname_rule_handles_two_part_tlds():
    p, _ = posting_from_html("https://jobs.newco.co.uk/j/1", page(title="AI Engineer"))
    assert p.company == "Newco"


def test_ats_hostname_is_never_the_company():
    p, _ = posting_from_html("https://boards.greenhouse.io/x", page(title="AI Engineer"))
    assert p.company is None


def test_caller_company_still_wins_over_every_fallback():
    p, _ = posting_from_html("https://careers.newco.de/j/1",
                             tagged('<meta property="og:site_name" content="NewCo">'), company="Told Co")
    assert p.company == "Told Co"


def test_the_note_names_the_rule_that_supplied_the_company():
    notes = []
    posting_from_html("https://careers.newco.de/j/1", page(title="AI Engineer"), notes=notes)
    assert notes == ["company read from the page's domain: 'Newco'"]


def personio_page(office="Berlin (Remote)", company="Acto", offices=True, ld=None):
    """A Personio tenant page as served: the posting JSON sits inside a JavaScript string,
    so every quote of the payload arrives backslash-escaped."""
    office_addresses = (r'\"office_addresses\":[{\"name\":\"%s\",\"city\":\"Remote\",'
                        r'\"state\":\"Berlin\",\"country\":\"DE\"}],' % office) if offices else ""
    payload = (r'\"id\":2735717,%s\"main_office\":\"%s\",\"schedule\":\"Full-time\",'
               r'\"careerSiteSettings\":{\"company_name\":\"%s\",\"logo_url\":null}'
               % (office_addresses, office, company))
    body = f'<script>self.__next_f.push([1,"{payload}"])</script>'
    return page(ld=ld).replace("</body>", f"{body}</body>")


def test_personio_without_json_ld_reads_company_and_city_from_the_payload():
    # acto.jobs.personio.com/job/2735717?language=de serves no JSON-LD; the page still shows Berlin.
    p, how = posting_from_html("https://acto.jobs.personio.com/job/2735717?language=de", personio_page())
    assert how == "page-text"                      # the description is still the page text
    assert p.company == "Acto" and p.location_raw == "Berlin (Remote)"
    assert city_of(p.location_raw) == "Berlin"     # so the posting is no longer dropped


def test_personio_de_host_is_read_the_same_way():
    p, _ = posting_from_html("https://adsquare.jobs.personio.de/job/2865259", personio_page(office="Berlin"))
    assert p.location_raw == "Berlin"


def test_personio_blank_company_name_falls_back_to_the_title_tail():
    # vanilla-steel-gmbh ships an empty company_name; HIR-198's fallbacks now read the
    # page title's tail instead of leaving the company unset (the host itself is skipped).
    p, _ = posting_from_html("https://vanilla-steel-gmbh.jobs.personio.com/job/2845809",
                             personio_page(office="Berlin", company=""))
    assert p.company == "Acme" and p.location_raw == "Berlin"   # page() titles "AI Engineer - Acme"
    assert p.title == "AI Engineer"                             # the tail used as company leaves the title


def test_personio_blank_company_and_tailless_title_still_needs_company():
    # Nothing to read: blank payload company, no site name, no title separator, and the
    # personio host never counts as the company.
    markup = personio_page(office="Berlin", company="").replace("AI Engineer - Acme", "AI Engineer")
    p, _ = posting_from_html("https://vanilla-steel-gmbh.jobs.personio.com/job/2845809", markup)
    assert p.company is None


def test_personio_falls_back_to_the_first_office_address():
    markup = personio_page().replace(r'\"main_office\":\"Berlin (Remote)\",', "")
    p, _ = posting_from_html("https://acto.jobs.personio.com/job/1", markup)
    assert p.location_raw == "Berlin (Remote)"     # the office's name, not its city ("Remote")


def test_personio_flags_still_override_the_payload():
    p, _ = posting_from_html("https://acto.jobs.personio.com/job/1", personio_page(),
                             company="Override Co", location="Munich")
    assert p.company == "Override Co" and p.location_raw == "Munich"


def test_personio_json_ld_tenant_is_unchanged():
    # juni.jobs.personio.com does serve JSON-LD; that path still wins and the payload is not read.
    ld = {"@type": "JobPosting", "title": "AI Engineer", "description": JD,
          "hiringOrganization": {"name": "Juni"},
          "jobLocation": {"@type": "Place", "address": {"addressLocality": "Berlin", "addressCountry": "DE"}}}
    p, how = posting_from_html("https://juni.jobs.personio.com/job/2872093", personio_page(ld=ld))
    assert how == "json-ld" and p.company == "Juni" and p.location_raw == "Berlin, DE"


def test_a_payload_on_another_host_is_ignored():
    # The Personio payload (company "Acto", office Berlin) is not read off a non-Personio
    # host; the company instead comes from HIR-198's title-tail fallback.
    p, _ = posting_from_html("https://acme.com/j/1", personio_page())
    assert p.company == "Acme" and p.location_raw is None


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
    board = [posting(source="greenhouse", sid="4012345", title="Account Executive, AI", location="Remote (US)", url=GH_URL)]
    r = check_url(conn, GH_URL, FEEDS, fetch_page=no_fetch, fetch_board=lambda s, t: board)
    assert r.verdict == "not_found"
    assert "is polled; ingest would drop it" in r.diagnosis
    assert "fails the title filter" in r.diagnosis and "is neither a tracked city nor EU-remote" in r.diagnosis


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


def test_plain_page_without_company_flag_matches_via_the_page_company(conn):
    # HIR-198: the title tail gives "Acme", company_key-equal to the stored "Acme GmbH",
    # so the text match works without --company and the check says where the name came from.
    ingest_one(conn, posting())
    r = check_url(conn, "https://acme.com/careers/ai", FEEDS, fetch_page=lambda u: page(), fetch_board=no_fetch)
    assert r.verdict == "found" and r.how == "text 1.00"
    assert any("company read from the page's title tail: 'Acme'" in n for n in r.notes)


def test_page_yielding_no_company_cannot_text_match_and_says_so(conn):
    ingest_one(conn, posting())
    r = check_url(conn, "https://acto.jobs.personio.com/job/1", FEEDS,
                  fetch_page=lambda u: page(title="AI Engineer"), fetch_board=no_fetch)
    assert r.verdict == "not_found"
    assert r.diagnosis.startswith("not a hosted ATS page")
    assert any("pass --company" in n for n in r.notes)


def test_greenhouse_embed_url_exact_hit_but_no_board_check(conn):
    url = "https://acme.com/careers?gh_jid=4012345"
    r = check_url(conn, url, FEEDS, fetch_page=lambda u: page(), fetch_board=no_fetch)
    assert r.verdict == "not_found" and "board token unknown" in r.diagnosis
    ingest_one(conn, posting(source="greenhouse", sid="4012345"))
    assert check_url(conn, url, FEEDS, fetch_page=no_fetch, fetch_board=no_fetch).verdict == "found"


def test_greenhouse_embed_url_resolves_token_from_embed_script_and_checks_the_board(conn):
    # HIR-31: the embed page itself carries the board token, so once it's fetched, an
    # embed URL diagnoses exactly like a plain boards.greenhouse.io URL would.
    url = "https://acme.com/careers?gh_jid=4012345"
    markup = page().replace("</body>", embed_script("acme") + "</body>")
    board = [posting(source="greenhouse", sid="4012345", url=GH_URL)]
    r = check_url(conn, url, FEEDS, fetch_page=lambda u: markup, fetch_board=lambda s, t: board)
    assert r.verdict == "not_found"
    assert "passes both filters" in r.diagnosis
    assert any("board token 'acme' read from the embed script" in n for n in r.notes)


def test_greenhouse_embed_url_resolved_token_not_polled_gives_add_hint(conn):
    url = "https://newco.com/careers?gh_jid=99"
    markup = page().replace("</body>", embed_script("newco") + "</body>")
    board = [Posting("greenhouse", "99", GH_URL, "NewCo", "AI Engineer", "Berlin", JD)]
    r = check_url(conn, url, FEEDS, fetch_page=lambda u: markup, fetch_board=lambda s, t: board)
    assert r.verdict == "not_found"
    assert r.diagnosis.startswith("board greenhouse:newco is not in config/feeds.json — add ")
    assert json.loads(r.diagnosis.split("add ", 1)[1]) == {"type": "greenhouse", "enabled": True,
                                                             "token": "newco", "company": "NewCo"}


def test_diagnose_is_pure_and_names_the_filter():
    p = Posting("url", "", "u", "Acme", "Call Center Agent", "Berlin", JD)
    assert "fails the title filter" in diagnose(p, None, FEEDS, None)
    assert "no feed can reach it" in diagnose(p, None, FEEDS, None)
    sf = Posting("url", "", "u", "Acme", "AI Engineer", "San Francisco, CA", JD)
    # SF is active since 2026-11-03 (HIR-12): no city reason is added any more.
    assert diagnose(sf, None, FEEDS, None) == ("not a hosted ATS page — no feed can reach it; "
                                               "--add stores it as source=url")


def test_diagnose_names_a_tracked_but_inactive_city(monkeypatch):
    """Still reachable for any city switched off: geo decides, check prints the list."""
    monkeypatch.setattr(geo, "ACTIVE_CITIES", ("Berlin", geo.REMOTE_EU))
    monkeypatch.setattr(check, "ACTIVE_CITIES", ("Berlin", geo.REMOTE_EU))
    sf = Posting("url", "", "u", "Acme", "AI Engineer", "San Francisco, CA", JD)
    assert ("maps to San Francisco, which is tracked but not active (active: Berlin, Remote (EU))"
            in diagnose(sf, None, FEEDS, None))


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
    assert legacy.is_new and new_shot.is_new
    assert job_coverage(conn) == (1, 3, 1)   # feed 1 of (feed, url, new screenshot); 1 legacy out
