import json
from pathlib import Path

from app.html_text import html_to_text
from app.sources import arbeitnow, ashby, greenhouse, lever, startup_jobs

FIX = Path(__file__).parent / "fixtures" / "feeds"


def load(name):
    return json.loads((FIX / name).read_text())


# --- html_to_text ---------------------------------------------------------------

def test_html_to_text_keeps_structure_and_drops_scripts():
    s = "<h3>Req</h3><ul><li>Python</li><li>RAG &amp; LLMs</li></ul><script>x()</script><p>Done</p>"
    assert html_to_text(s) == "Req\n\n- Python\n\n- RAG & LLMs\n\nDone"


def test_html_to_text_passes_plain_text_through():
    assert html_to_text("a  b\n\n\n\nc &amp; d") == "a b\n\nc & d"


# --- adapters -------------------------------------------------------------------

def test_greenhouse_parse_unescapes_content_and_skips_empty():
    ps = greenhouse.parse(load("greenhouse.json"))
    assert [p.source_job_id for p in ps] == ["5390795008", "1", "2"]  # id 3 has no content
    p = ps[0]
    assert p.source == "greenhouse" and p.company == "Acme" and p.location_raw == "Berlin, Germany"
    assert "agent architectures" in p.description_text and "<" not in p.description_text
    assert p.posted_at == "2026-08-01T10:00:00-04:00"
    assert greenhouse.parse(load("greenhouse.json"), company="Override")[0].company == "Override"


def test_lever_parse_joins_description_and_lists():
    [p] = lever.parse(load("lever.json"), company="Acme")
    assert p.source == "lever" and p.title == "AI Engineer (m/w/d)" and p.location_raw == "Berlin"
    for s in ("We build agents.", "Requirements", "- Python", "- LangGraph or similar", "Nice to have", "- Kubernetes"):
        assert s in p.description_text
    assert p.posted_at == "2025-10-09T08:53:20Z"


def test_ashby_parse_prefers_plain_description():
    [p] = ashby.parse(load("ashby.json"), company="Acme")
    assert p.source == "ashby" and p.location_raw == "San Francisco"
    assert p.description_text == "Requirements:\n- Python\n- RAG"


def test_arbeitnow_parse_and_pagination():
    payload = load("arbeitnow.json")
    ps = arbeitnow.parse(payload)
    assert [p.company for p in ps] == ["logen.ai", "We Love X GmbH"]
    assert ps[0].source_job_id == "ai-agent-architect-berlin-123"
    assert "- Experience with APIs and backend systems" in ps[0].description_text
    assert ps[0].posted_at == "2025-10-09T08:53:20Z"
    assert arbeitnow.next_url(payload) == "https://www.arbeitnow.com/api/job-board-api?page=2"


def test_startup_jobs_parse_reads_nested_company_and_location():
    payload = load("startup_jobs.json")
    first, second = startup_jobs.parse(payload)
    assert first.source_job_id == "10479227"
    assert first.company == "bei Buddybrand"
    assert first.location_raw == "Berlin"
    # The API appends its own attribution params to every job url; we keep them as served.
    assert first.url == (
        "https://startup.jobs/junior-influencer-creator-marketing-manager-m-w-d-bei-buddybrand-10479227"
        "?utm_source=startup-jobs-key1&utm_medium=api"
    )
    assert first.posted_at == "2026-10-15T10:51:25Z"
    assert "WAS DU BEI UNS MACHST" in first.description_text
    assert "<li>" not in first.description_text
    assert second.company == "Databricks" and second.location_raw == "Munich"


def test_startup_jobs_next_url_advances_on_the_last_id():
    payload = load("startup_jobs.json")
    url = "https://api.startup.jobs/v1/jobs?search=AI+engineer&country=DE"
    # next_cursor repeats the id of the last job in the page.
    assert payload["next_cursor"] == 10483131
    nxt = startup_jobs.next_url(payload, url)
    assert nxt == url + "&starting_after=10483131"
    # A second page replaces the cursor rather than appending another one.
    assert startup_jobs.next_url(payload, nxt) == nxt


def test_startup_jobs_next_url_stops_when_has_more_is_false():
    payload = load("startup_jobs.json")
    assert startup_jobs.next_url({**payload, "has_more": False}, "https://x/?a=1") is None
    assert startup_jobs.next_url({**payload, "next_cursor": None}, "https://x/?a=1") is None


def test_startup_jobs_fetch_requires_key(monkeypatch):
    monkeypatch.delenv("STARTUP_JOBS_API_KEY", raising=False)
    import pytest
    with pytest.raises(RuntimeError, match="STARTUP_JOBS_API_KEY"):
        startup_jobs.fetch("ai")


# --- arbeitsagentur (fixtures trimmed from a live call, plus one hand-made empty) --

def test_arbeitsagentur_listings_keep_only_rows_with_a_reference_number():
    from app.sources import arbeitsagentur
    ls = arbeitsagentur.listings(load("arbeitsagentur_search.json"))
    assert [l["refnr"] for l in ls] == ["12336-a26f1192j0456062-S", "12265-PARTNER99-S"]
    assert arbeitsagentur.listings({}) == [] and arbeitsagentur.listings({"ergebnisliste": None}) == []
    # The older v4 shape still reads.
    assert arbeitsagentur.listings({"stellenangebote": [{"refnr": "R-1"}]})[0]["refnr"] == "R-1"


def test_arbeitsagentur_parse_takes_location_from_the_search_result():
    from app.sources import arbeitsagentur
    listing = arbeitsagentur.listings(load("arbeitsagentur_search.json"))[0]
    p = arbeitsagentur.parse(listing, load("arbeitsagentur_details.json")[listing["refnr"]])
    assert p.source == "arbeitsagentur" and p.source_job_id == "12336-a26f1192j0456062-S"
    assert p.url == "https://www.arbeitsagentur.de/jobsuche/jobdetail/12336-a26f1192j0456062-S"
    assert p.title == "AI Engineer (m/d/w)" and p.company == "EXXETA AG"
    assert p.location_raw == "Berlin"          # details list Leipzig first; the Berlin search matched Berlin
    assert p.posted_at == "2026-10-14"
    assert p.description_text.startswith("**AI Engineer**")


def test_arbeitsagentur_parse_falls_back_to_details_and_v4_fields():
    from app.sources import arbeitsagentur
    d = {"stellenangebotsBeschreibung": "Python", "stellenangebotsTitel": "AI Engineer",
         "firma": "D GmbH", "stellenlokationen": [{"adresse": {"ort": "Munich"}}],
         "datumErsteVeroeffentlichung": "2026-10-01"}
    p = arbeitsagentur.parse({"refnr": "R"}, d)
    assert (p.title, p.company, p.location_raw, p.posted_at) == ("AI Engineer", "D GmbH", "Munich", "2026-10-01")
    v4 = {"refnr": "R", "titel": "ML Engineer", "arbeitgeber": "V4 AG", "arbeitsort": {"ort": "Berlin"},
          "aktuelleVeroeffentlichungsdatum": "2026-09-30"}
    p = arbeitsagentur.parse(v4, {"stellenangebotsBeschreibung": "x"})
    assert (p.title, p.company, p.location_raw, p.posted_at) == ("ML Engineer", "V4 AG", "Berlin", "2026-09-30")


def test_arbeitsagentur_parse_skips_postings_without_description():
    from app.sources import arbeitsagentur
    listing = arbeitsagentur.listings(load("arbeitsagentur_search.json"))[1]
    assert arbeitsagentur.parse(listing, load("arbeitsagentur_details.json")[listing["refnr"]]) is None


def test_arbeitsagentur_has_next_stops_at_total_or_empty_page():
    from app.sources import arbeitsagentur
    payload = load("arbeitsagentur_search.json")
    assert arbeitsagentur.has_next(payload)                                  # 1*2 < 3
    assert not arbeitsagentur.has_next({**payload, "page": 2})               # 2*2 >= 3
    assert not arbeitsagentur.has_next({**payload, "ergebnisliste": []})     # empty page
    assert not arbeitsagentur.has_next({"ergebnisliste": payload["ergebnisliste"]})  # no counts


def test_arbeitsagentur_urls():
    from app.sources import arbeitsagentur
    assert arbeitsagentur.details_url("10001-1001234567-S").endswith(
        "/pc/v4/jobdetails/MTAwMDEtMTAwMTIzNDU2Ny1T")
    u = arbeitsagentur.search_url("AI Engineer", "Berlin", 25, 30, page=2, size=50)
    assert "/pc/v6/jobs?" in u
    assert "was=AI+Engineer" in u and "wo=Berlin" in u and "umkreis=25" in u
    assert "veroeffentlichtseit=30" in u and "page=2" in u and "angebotsart=1" in u


def test_arbeitsagentur_fetch_pages_and_calls_details(monkeypatch):
    from app.sources import arbeitsagentur
    search, details = load("arbeitsagentur_search.json"), load("arbeitsagentur_details.json")
    calls = []

    def fake_fetch_json(url, headers=None, timeout=30):
        calls.append(url)
        assert headers == {"X-API-Key": "jobboerse-jobsuche"}
        if "/jobdetails/" in url:
            for refnr, d in details.items():
                if url == arbeitsagentur.details_url(refnr):
                    return d
            raise AssertionError(url)
        return search if "page=1" in url else {**search, "page": 2, "ergebnisliste": []}

    monkeypatch.setattr(arbeitsagentur, "fetch_json", fake_fetch_json)
    ps = arbeitsagentur.fetch("AI Engineer", max_pages=5)
    assert [p.source_job_id for p in ps] == ["12336-a26f1192j0456062-S"]
    assert sum("/pc/v6/jobs?" in c for c in calls) == 2 and sum("/jobdetails/" in c for c in calls) == 2


# --- jsearch (fixture is hand-built to the documented shape) ---------------------

def test_jsearch_parse_maps_fields_and_skips_empty():
    from app.sources import jsearch
    first, second = jsearch.parse(load("jsearch.json"))   # third has no description
    assert first.source == "jsearch" and first.source_job_id == "abc123=="
    assert first.title == "AI Engineer (m/w/d)" and first.company == "Beispiel GmbH"
    assert first.url == "https://www.linkedin.com/jobs/view/123" and first.location_raw == "Berlin"
    assert first.posted_at == "2026-10-16T09:00:00.000Z" and "- RAG" in first.description_text
    # No apply link → Google link; no city → location string.
    assert second.url.startswith("https://www.google.com/") and second.location_raw == "Germany"
    assert second.posted_at is None
    assert jsearch.parse({"status": "ERROR"}) == [] and jsearch.parse([]) == []


def test_jsearch_request_per_host():
    from app.sources import jsearch
    url, headers = jsearch.request("AI engineer in Berlin", "de", "week", 1, 1, "openwebninja", "k")
    assert url.startswith("https://api.openwebninja.com/jsearch/search?") and headers == {"x-api-key": "k"}
    for part in ("query=AI+engineer+in+Berlin", "country=de", "date_posted=week", "page=1", "num_pages=1"):
        assert part in url
    url, headers = jsearch.request("x", None, None, 1, 1, "rapidapi", "k")
    assert url.startswith("https://jsearch.p.rapidapi.com/search?") and "country" not in url
    assert headers == {"X-RapidAPI-Key": "k", "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}


def test_jsearch_request_rejects_unknown_host():
    import pytest
    from app.sources import jsearch
    with pytest.raises(ValueError):
        jsearch.request("x", None, None, 1, 1, "openai", "k")


def test_jsearch_fetch_needs_a_key_and_makes_one_call(monkeypatch):
    import pytest
    from app.sources import jsearch
    monkeypatch.delenv("JSEARCH_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        jsearch.fetch("AI engineer in Berlin")
    calls = []
    monkeypatch.setattr(jsearch, "fetch_json", lambda url, headers=None, timeout=30: calls.append(url) or load("jsearch.json"))
    monkeypatch.setenv("JSEARCH_API_KEY", "k")
    assert len(jsearch.fetch("AI engineer in Berlin")) == 2 and len(calls) == 1


# Two ids JSearch returned for the same StepStone posting on two calls (live, 2026-10-18).
JSEARCH_IDS_SAME_POSTING = (
    "OXF1enQyQ2NBc3JrX1hWS0FBQUFBQT09OkVzd0JDb3dCUVVwcFZEUjBTV1o1YldwR2JEZExaekI2ZFRCdGFqRm1NMlV6T1VsMWQxTXRjRVZQV1Vzd1FsVlRlRU5ETlhCNFkwWlJZamcwY1VkT2FHZFlhM0pMWjJsblIwcFhkV3MwYUU1RVJISlVRMnhUU1RKclExRkhPVUo0WldaSGVtbDVjM3AzU25Zd1JrNXZOazlEUWxBeFIwWkRaa1EzWmtwbVJsWjJSRTlHTjA1a2IxUnlaMmhQT1hkYWNHb1NGMGxSVUZaaGNTMXZTSEpwWlRWT2IxQnJjV2xWYlVGbkdpSkJSSE55T1daU1JtYzBaMlpsTkZsbWRrNXJORjlGWm10bFVqWnhZM3BFTkZCUg",
    "OXF1enQyQ2NBc3JrX1hWS0FBQUFBQT09OkVzd0JDb3dCUVVwcFZEUjBTVzlNT1VReVRrWldjMk5aU25Ga016WnFlVEEwUjJGdVdrcEJja3BMYUdSc01VaHpOakkwWkZkS05XaHBaSE14TUdsTGIyWnZXVWxqY1ZWRlVYWmFTVEZLTWxRM1gycFJZMnh0YzFGdmR6UlpZMGx4VUZOM0xXRnZkR05wVkZWaFNFcHpkbmswUm1aSVREZHhSMkl0UlRWeldYVmZaSEpITFRSWWJEVXhZMVpwTFVwaVZGTVNGelZSU0ZaaGRIbHdTelZ1WlRWT2IxQnVUQzFRYzBFd0dpSkJSSE55T1daUlppMVVNRmR4V25oWUxWQkhWVGh5TmpSd0xWb3hObk5oV0daUg",
)


def test_jsearch_stable_id_drops_the_per_request_token():
    from app.sources import jsearch
    a, b = (jsearch.stable_id(i) for i in JSEARCH_IDS_SAME_POSTING)
    assert a == b == "9quzt2CcAsrk_XVKAAAAAA=="
    for odd in ("abc123==", "not base64!", "", "bm9jb2xvbg=="):   # last decodes to "nocolon"
        assert jsearch.stable_id(odd) == odd


def test_jsearch_parse_uses_the_stable_id():
    from app.sources import jsearch
    payload = {"data": [{"job_id": i, "job_title": "AI Engineer", "job_description": "x"}
                        for i in JSEARCH_IDS_SAME_POSTING]}
    assert {p.source_job_id for p in jsearch.parse(payload)} == {"9quzt2CcAsrk_XVKAAAAAA=="}


# --- join (fixtures: trimmed initialState from live pages, 2026-10-19) -----------------
from app.sources import join  # noqa: E402


def test_join_page_state_reads_next_data_and_tolerates_pages_without_it():
    markup = ('<html><script id="__NEXT_DATA__" type="application/json">'
              '{"props": {"pageProps": {"initialState": {"job": {"title": "x"}}}}}</script></html>')
    assert join.page_state(markup) == {"job": {"title": "x"}}
    assert join.page_state("<html>no data</html>") == {}
    assert join.page_state('<script id="__NEXT_DATA__">{broken</script>') == {}


def test_join_page_state_reads_page_data_on_company_pages():
    # Company pages switched from `initialState` to `pageData` in October 2026; the old key is
    # still present on job pages. An empty old key must not shadow a populated new one.
    markup = ('<script id="__NEXT_DATA__" type="application/json">{"props": {"pageProps": '
              '{"initialState": {}, "pageData": {"jobs": {"items": [{"idParam": "1-x"}], '
              '"pagination": {"pageCount": 1}}}}}}</script>')
    assert join.listing(join.page_state(markup)) == (["1-x"], 1)
    assert join.page_state('<script id="__NEXT_DATA__">{"props": {"pageProps": {"locale": "en"}}}</script>') == {}


def test_join_listing_gives_id_params_and_page_count():
    ids, pages = join.listing(load("join_company.json"))
    assert ids[0] == "16792067-ai-developer-llm-products-remote" and len(ids) == 3
    assert pages == 2
    assert join.listing({}) == ([], 0)


def test_join_parse_uses_the_url_number_as_id():
    p = join.parse(load("join_job.json"), "xheroncom")
    assert p.source == "join"
    assert p.source_job_id == "16814436"          # from idParam, not the internal `id`
    assert p.url == "https://join.com/companies/xheroncom/16814436-ai-harness-engineer-agentic-and-autonomous-operations-m-f-x"
    assert (p.company, p.location_raw) == ("xHeron Solutions", "Berlin, Germany")
    assert p.title.startswith("AI Harness Engineer") and "<p>" not in p.description_text
    assert p.posted_at.startswith("2026-09-14")


def test_join_parse_marks_remote_and_skips_empty():
    state = load("join_job.json")
    state["job"]["workplaceType"] = "REMOTE"
    assert join.parse(state, "xheroncom", company="xHeron").location_raw == "Berlin, Germany (remote)"
    state["job"]["description"] = ""
    assert join.parse(state, "xheroncom") is None


def test_join_fetch_dedups_overlapping_pages(monkeypatch):
    company = load("join_company.json")
    page2 = {"jobs": {"items": [company["jobs"]["items"][0]], "pagination": {"pageCount": 2}}}
    job = load("join_job.json")
    fetched = []

    def fake(url):
        fetched.append(url)
        state = company if url.endswith("?page=1") else page2 if url.endswith("?page=2") else job
        return '<script id="__NEXT_DATA__">' + json.dumps({"props": {"pageProps": {"initialState": state}}}) + "</script>"

    monkeypatch.setattr(join, "fetch_text", fake)
    out = join.fetch("dexter-health")
    job_pages = [u for u in fetched if "?page=" not in u]
    assert len(job_pages) == 3 == len(out)        # page 2's job was already on page 1


def test_remote_flags_become_part_of_the_location():
    """arbeitnow `remote`, startup.jobs `workplace_type`, JSearch `job_is_remote` → geo sees them."""
    from app.geo import place_of
    from app.sources import jsearch
    item = {"slug": "s", "company_name": "Acme", "title": "AI Engineer", "description": "<p>x</p>",
            "url": "u", "location": "Munich", "remote": True, "created_at": 1760000000}
    assert arbeitnow.parse({"data": [item]})[0].location_raw == "Munich (remote, Germany)"
    assert place_of("Munich (remote, Germany)") == "Remote (EU)"
    sj = {"id": 1, "title": "AI Engineer", "description": "x", "company_name": "Acme", "url": "u",
          "workplace_type": "remote", "location": {"city": "Hamburg", "country": "Germany"}}
    assert startup_jobs.parse({"data": [sj]})[0].location_raw == "Hamburg (remote, Germany)"
    js = {"job_id": "abc", "job_title": "AI Engineer", "job_description": "x", "employer_name": "Acme",
          "job_city": None, "job_location": None, "job_country": "DE", "job_is_remote": True}
    assert jsearch.parse({"data": [js]})[0].location_raw == "Remote (Germany)"
    assert jsearch.parse({"data": [{**js, "job_country": "US"}]})[0].location_raw == "Remote (US)"
    assert place_of("Remote (US)") is None
