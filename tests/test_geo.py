"""EU-remote recognition (DECISIONS 2026-10-26). Location strings are the shapes the feeds
and careers pages send; the Kake case is the posting /check-url rejected on 2026-10-26."""

import pytest

from app.check import posting_from_html
from app import geo
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
    assert active_place("San Francisco, CA (Remote)") == "San Francisco"   # active since HIR-12


def test_san_francisco_is_active_but_the_gate_still_drops_an_inactive_city(monkeypatch):
    """The tracked-vs-active gate is unchanged; only SF's side of it moved."""
    assert "San Francisco" in geo.ACTIVE_CITIES
    monkeypatch.setattr(geo, "ACTIVE_CITIES", ("Berlin", REMOTE_EU))
    assert place_of("San Francisco, CA") == "San Francisco"   # still tracked
    assert active_place("San Francisco, CA") is None          # but not collected


def test_no_region_remote_is_dropped_when_the_description_restricts_it():
    assert not is_remote_eu("Remote", text="You must be located in the United States.")
    assert not is_remote_eu("Remote", text="Candidates must be authorized to work in the US.")
    assert not is_remote_eu("Remote", text="This role is US-only.")
    # Time-zone overlap is not a residence rule, and an EU region named in the location wins.
    assert is_remote_eu("Remote", text="US Timezone Overlap: 5h–6h daily PST")
    assert is_remote_eu("Remote (Europe)", text="US citizens and EU residents welcome")


# --- HIR-109: the declarative residence sentence counts too ----------------------

# The tails of the two real Clera postings, which share one LOCATION template and differ
# only in the region named. One must drop out, the other must stay in.
CLERA_US_TAIL = ("COMPENSATION & BENEFITS\n\nAnnual base salary is $180,000 to $260,000 USD, "
                 "depending on skills, experience,\nand role scope. Visa sponsorship is not "
                 "available.\n\nLOCATION\n\nRemote within the United States.")
CLERA_EU_TAIL = ("COMPENSATION & BENEFITS\n\nSalary range: €75,000 to €100,000 annually."
                 "\n\nLOCATION\n\nFully remote within the EU.")


def test_declarative_us_location_sentence_drops_a_no_region_remote_posting():
    assert not is_remote_eu("remote", text=CLERA_US_TAIL)
    assert is_remote_eu("remote", text=CLERA_EU_TAIL)


@pytest.mark.parametrize("sentence", [
    "Remote within the United States.",
    "Fully remote within the US.",
    "Remote in the United States",
    "Remote from the US.",
    "Remote within Canada.",
    "Remote within India.",
    "LOCATION\n\nBased in the United States.",
    "This role is based in the United States.",
    "Candidates are located in the UK.",
    "You must be located in the U.S.",          # the abbreviation, now reachable
])
def test_declarative_and_imperative_residence_sentences_both_restrict(sentence):
    assert not is_remote_eu("remote", text=sentence)


@pytest.mark.parametrize("sentence", [
    # The documented accepted risk: no residence sentence at all still gets in.
    "We are a fully remote team building agents. Python and RAG required.",
    # An EU region in the same template is not on the non-EU country list.
    "Fully remote within the EU.",
    "Remote within Europe.",
    # Explicitly rejected as residence evidence (HIR-109): each has a counter-example.
    "Annual base salary is $180,000 to $260,000 USD, depending on skills.",
    "Visa sponsorship is not available.",
    "We are a US-based company with a distributed team.",
    "Clera is a company based in the United States, with a remote team across the EU.",
    # Anchored on a named country, so no country means no restriction.
    "Remote within your timezone.",
    "Remote within the CET timezone.",
    # A country named for some other reason than where you live.
    "You will support customers in the United States.",
    "We serve clients in India and the UK.",
])
def test_phrases_that_do_not_restrict_where_you_live(sentence):
    assert is_remote_eu("remote", text=sentence)


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
