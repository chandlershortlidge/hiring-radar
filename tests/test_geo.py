"""EU-remote recognition (DECISIONS 2026-10-26). Location strings are the shapes the feeds
and careers pages send; the Kake case is the posting /check-url rejected on 2026-10-26."""

import pytest

from app.check import posting_from_html
from app.geo import REMOTE_EU, active_place, is_remote_eu, place_of


@pytest.mark.parametrize("loc", [
    "Remote",
    "Remote (Germany)",
    "Remote - Europe",
    "Remote (EU)",
    "Remote, EMEA",
    "Europe (Remote)",
    "Fully remote / Anywhere",
    "Worldwide",
    "Hamburg, Germany (remote)",          # JOIN
    "Munich (remote, Germany)",           # arbeitnow, remote: true
    "Remote (CET ± 2 hours)",
    "Remote - US; Remote - Germany",      # Greenhouse multi-location
    "Remote (US or Europe)",
    "Deutschlandweit / Homeoffice",
])
def test_eu_remote_locations_count(loc):
    assert place_of(loc) == REMOTE_EU and active_place(loc) == REMOTE_EU


@pytest.mark.parametrize("loc", [
    "Remote - US",
    "Remote (United States)",
    "Remote, Spain",                      # one other country: residence/entity there
    "Remote - UK",
    "Remote (LATAM)",
    "Munich, Germany",                    # not remote
    "Hybrid",
    None,
    "",
])
def test_other_locations_do_not(loc):
    assert place_of(loc) is None and active_place(loc) is None


def test_a_city_wins_over_remote():
    assert place_of("Berlin or Remote (EU)") == "Berlin"
    assert active_place("San Francisco, CA (Remote)") is None   # tracked city, not active


def test_no_region_remote_is_dropped_when_the_description_restricts_it():
    assert not is_remote_eu("Remote", text="You must be located in the United States.")
    assert not is_remote_eu("Remote", text="Candidates must be authorized to work in the US.")
    assert not is_remote_eu("Remote", text="This role is US-only.")
    # Time-zone overlap is not a residence rule, and an EU region named in the location wins.
    assert is_remote_eu("Remote", text="US Timezone Overlap: 5h–6h daily PST")
    assert is_remote_eu("Remote (Europe)", text="US citizens and EU residents welcome")


def test_empty_location_falls_back_to_title_then_strong_description_phrases():
    assert place_of(None, title="Senior AI/LLM Engineer (Python) - Remote") == REMOTE_EU
    assert place_of(None, title="AI Engineer (Remote, US)") is None
    assert place_of(None, title="AI Engineer", text="We are a remote-first company.") == REMOTE_EU
    # Plain "remote" in a description is not enough: hybrid postings mention remote days.
    assert place_of(None, title="AI Engineer", text="Two remote days a week.") is None
    # A location that is present is not overridden by the description.
    assert place_of("Munich, Germany", text="We are a fully remote team.") is None


# Synthetic page built from the text of https://kake.co/jobs/senior-ai-llm-engineer-python-56a4536c4a20
# (no JSON-LD on that page, so --location is empty and the page text is all there is).
KAKE_PAGE = """<html><head><title>Senior AI/LLM Engineer (Python) | Kake</title></head><body>
<h1>Senior AI/LLM Engineer (Python) - Remote</h1>
<p>Kake is a remote-first company and a people-first global community of senior engineers.</p>
<ul><li>Strong Python and FastAPI</li><li>RAG, embeddings, vector databases</li>
<li>US Timezone Overlap: 5h–6h daily PST</li></ul>
<p>Fully Remote: Simply put, we trust you.</p></body></html>"""


def test_kake_page_without_json_ld_is_eu_remote():
    p, how = posting_from_html("https://kake.co/jobs/x", KAKE_PAGE, company="Kake")
    assert how == "page-text" and p.location_raw is None
    assert active_place(p.location_raw, p.title, p.description_text) == REMOTE_EU


def _ld(job: dict) -> str:
    import json
    return f'<html><script type="application/ld+json">{json.dumps(job)}</script></html>'


def test_json_ld_telecommute_becomes_a_remote_location():
    base = {"@type": "JobPosting", "title": "AI Engineer", "description": "<p>Python</p>"}
    p, _ = posting_from_html("u", _ld({**base, "jobLocationType": "TELECOMMUTE",
                                       "applicantLocationRequirements": [{"@type": "Country", "name": "Germany"},
                                                                         {"@type": "Country", "name": "France"}]}))
    assert p.location_raw == "Remote (Germany, France)" and place_of(p.location_raw) == REMOTE_EU
    p, _ = posting_from_html("u", _ld({**base, "jobLocationType": "TELECOMMUTE",
                                       "applicantLocationRequirements": {"@type": "Country", "name": "USA"}}))
    assert p.location_raw == "Remote (USA)" and place_of(p.location_raw) is None
