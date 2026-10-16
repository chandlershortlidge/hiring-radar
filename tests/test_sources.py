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


def test_startup_jobs_parse_handles_nested_company():
    payload = load("startup_jobs.json")
    [p] = startup_jobs.parse(payload)
    assert p.company == "Clera" and p.source_job_id == "98765" and p.location_raw == "Berlin, Germany"
    assert "- Experience with LLMs and agents" in p.description_text
    assert startup_jobs.next_url(payload) is None


def test_startup_jobs_fetch_requires_key(monkeypatch):
    monkeypatch.delenv("STARTUP_JOBS_API_KEY", raising=False)
    import pytest
    with pytest.raises(RuntimeError, match="STARTUP_JOBS_API_KEY"):
        startup_jobs.fetch("ai")
