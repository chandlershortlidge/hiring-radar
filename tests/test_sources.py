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
