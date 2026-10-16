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
