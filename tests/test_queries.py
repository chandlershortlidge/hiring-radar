import pytest

from app import db, queries as q
from app.extract import Extraction, Mention, Proposed, Seniority
from app.ingest import ingest_one
from app.pipeline import store_extraction
from app.sources import Posting

NOW = "2026-10-17T12:00:00Z"


def ts(days_ago: int) -> str:
    return q._days_ago(NOW, days_ago)


def add(conn, company, title, city, source, when, skills, seniority=None, sid=None, proposed=()):
    p = Posting(source, sid or (f"{source}-{company}-{title}" if source in q.FEED_SOURCES else ""), "", company, title, city,
                f"{company} {title} wants " + ", ".join(s for s, _ in skills)
                + f" {company} {title} posting body." * 20)  # past MIN_TEXT_CHARS: a full posting
    out = ingest_one(conn, p, when, require_city=False, trust_title=True)
    job_id = int(out[4:])
    ex = Extraction(seniority=Seniority(seniority, "stated", seniority) if seniority else Seniority(None, None, None),
                    mentions=[Mention(s, r, s) for s, r in skills],
                    proposed=[Proposed(l, "required", l) for l in proposed],
                    extractor_version="t", taxonomy_version=3)
    store_extraction(conn, job_id, ex)
    return job_id


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    # Berlin, feed, open: python+rag required, aws nice
    add(c, "Acme", "AI Engineer", "Berlin", "arbeitnow", ts(1), [("python", "required"), ("rag", "required"), ("aws", "nice_to_have")], "mid")
    # Berlin, feed, closed (last seen 10 days ago)
    add(c, "Beta", "ML Engineer", "Berlin", "arbeitnow", ts(10), [("python", "required"), ("docker", "required")], "senior")
    # SF, feed, open
    add(c, "Gamma", "AI Engineer", "San Francisco", "greenhouse", ts(0), [("python", "required"), ("aws", "required")], "junior")
    # Berlin, manual (screenshot) 40 days ago: still open under the 60-day rule
    add(c, "Delta", "Junior AI Engineer", "Berlin", "screenshot", ts(40), [("rag", "required")], "junior", proposed=["Rust", "DSPy"])
    # Berlin, manual 70 days ago: closed
    add(c, "Epsilon", "AI Engineer", "Berlin", "paste", ts(70), [("python", "required")], None, proposed=["rust"])
    return c


def test_open_rule_feed_vs_manual(conn):
    s = q.stats(conn, NOW, skills_tracked=143)
    assert s["jobs"] == 5 and s["open"] == 3  # Acme, Gamma, Delta
    assert s["open_by_city"] == {"Berlin": 2, "San Francisco": 1}
    assert s["companies"] == 5 and s["proposed_pending"] == 3


def test_search_sources_use_the_manual_rule_and_never_keep_a_closed_feed_job_open(conn):
    # JSearch-only, last seen 20 days ago: open (absence from a search sample proves nothing).
    add(conn, "Zeta", "AI Engineer", "Berlin", "jsearch", ts(20), [("python", "required")])
    # Arbeitsagentur-only, 70 days: closed under the 60-day rule.
    add(conn, "Eta", "AI Engineer", "Berlin", "arbeitsagentur", ts(70), [("python", "required")])
    # Beta's arbeitnow listing went stale 10 days ago; JSearch re-finding it today must not reopen it.
    beta = conn.execute("SELECT id FROM job WHERE company='Beta'").fetchone()[0]
    conn.execute("INSERT INTO job_source (job_id, source, source_job_id, first_seen, last_seen) VALUES (?,?,?,?,?)",
                 (beta, "jsearch", "js-beta", ts(0), ts(0)))
    conn.execute("UPDATE job SET last_seen=? WHERE id=?", (ts(0), beta))
    s = {j["company"]: j["status"] for j in q.list_jobs(conn, q.Filters(window="all"), NOW)["jobs"]}
    assert (s["Zeta"], s["Eta"], s["Beta"]) == ("open", "closed", "closed")
    assert q.stats(conn, NOW, 1)["open"] == 4  # Acme, Gamma, Delta, Zeta
    assert q.job_detail(conn, beta, NOW)["status"] == "closed"


def test_skill_frequency_required_only_over_open_jobs(conn):
    r = q.skill_frequency(conn, q.Filters(), NOW)
    assert r["total"] == 3
    by = {s["skill_id"]: s for s in r["skills"]}
    assert by["python"]["count"] == 2 and by["python"]["pct"] == pytest.approx(66.7)
    assert by["rag"]["count"] == 2 and by["rag"]["by_city"] == {"Berlin": 2}
    assert by["aws"]["count"] == 1  # Acme's aws is nice_to_have, excluded
    assert r["skills"][0]["skill_id"] in ("python", "rag")  # sorted by count desc, then id


def test_skill_frequency_with_nice_to_have_and_window_all(conn):
    r = q.skill_frequency(conn, q.Filters(requirement="all", window="all"), NOW)
    assert r["total"] == 5
    by = {s["skill_id"]: s for s in r["skills"]}
    assert by["aws"]["count"] == 2 and by["python"]["count"] == 4


def test_filters_city_and_seniority(conn):
    r = q.skill_frequency(conn, q.Filters(cities=("Berlin",), seniorities=("junior",), window="all"), NOW)
    assert r["total"] == 1 and [s["skill_id"] for s in r["skills"]] == ["rag"]
    assert q.city_totals(conn, q.Filters(window="all"), NOW) == {"Berlin": 4, "San Francisco": 1}


def test_list_jobs_filters_search_sort_and_status(conn):
    r = q.list_jobs(conn, q.Filters(window="all"), NOW)
    assert r["total"] == 5 and [j["company"] for j in r["jobs"]][:2] == ["Gamma", "Acme"]  # newest first
    statuses = {j["company"]: j["status"] for j in r["jobs"]}
    assert statuses == {"Acme": "open", "Beta": "closed", "Gamma": "open", "Delta": "open", "Epsilon": "closed"}
    r = q.list_jobs(conn, q.Filters(window="all", skill_id="rag"), NOW)
    assert {j["company"] for j in r["jobs"]} == {"Acme", "Delta"}
    r = q.list_jobs(conn, q.Filters(window="all", query="ml eng"), NOW)
    assert [j["company"] for j in r["jobs"]] == ["Beta"]
    r = q.list_jobs(conn, q.Filters(window="all"), NOW, sort="company", limit=2, offset=1)
    assert [j["company"] for j in r["jobs"]] == ["Beta", "Delta"] and r["total"] == 5
    assert r["jobs"][0]["skill_counts"] == {"required": 2, "nice_to_have": 0}
    assert r["jobs"][0]["required_skills"] == ["docker", "python"]


def test_job_detail(conn):
    jid = q.list_jobs(conn, q.Filters(window="all", query="acme"), NOW)["jobs"][0]["id"]
    d = q.job_detail(conn, jid, NOW)
    assert d["company"] == "Acme" and d["status"] == "open" and d["seniority"] == "mid"
    assert [(s["skill_id"], s["requirement"]) for s in d["skills"]] == [("python", "required"), ("rag", "required"), ("aws", "nice_to_have")]
    assert d["sources"][0]["source"] == "arbeitnow"
    assert q.job_detail(conn, 999, NOW) is None


def test_german_and_degree_filters(conn):
    # Acme: German required, master's or equivalent. Gamma: German nice, bachelor required. Beta: nothing.
    conn.execute("UPDATE job SET german='required', german_basis='stated', german_signal='German', degree='master',"
                 " degree_requirement='required', degree_or_equivalent=1, degree_signal='M.Sc. or equivalent' WHERE company='Acme'")
    conn.execute("UPDATE job SET german='nice_to_have', german_basis='stated', german_signal='German is a plus', degree='bachelor',"
                 " degree_requirement='required', degree_or_equivalent=0, degree_signal='B.Sc.' WHERE company='Gamma'")
    names = lambda f: {j["company"] for j in q.list_jobs(conn, f, NOW)["jobs"]}
    assert names(q.Filters(window="all", german="required")) == {"Acme"}
    assert names(q.Filters(window="all", german="not_required")) == {"Beta", "Gamma", "Delta", "Epsilon"}
    assert names(q.Filters(window="all", german="none")) == {"Beta", "Delta", "Epsilon"}
    assert names(q.Filters(window="all", degree="required")) == {"Gamma"}
    assert names(q.Filters(window="all", degree="open")) == {"Acme", "Beta", "Delta", "Epsilon"}
    assert names(q.Filters(window="all", degree="none")) == {"Beta", "Delta", "Epsilon"}
    assert q.skill_frequency(conn, q.Filters(window="all", german="required"), NOW)["total"] == 1
    s = q.stats(conn, NOW, 1)
    assert s["open_german_required"] == 1 and s["open_degree_required"] == 1
    d = q.job_detail(conn, q.list_jobs(conn, q.Filters(window="all", query="acme"), NOW)["jobs"][0]["id"], NOW)
    assert d["degree"] == "master" and d["degree_or_equivalent"] is True and d["german_signal"] == "German"


def test_legacy_jobs_stay_out_of_the_chart_but_in_the_list(conn):
    jid = add(conn, "Zeta", "AI Engineer", "Berlin", "paste", ts(1), [("python", "required"), ("docker", "required")])
    conn.execute("UPDATE job SET extracted_version='legacy' WHERE id=?", (jid,))
    f = q.Filters(window="all")
    assert q.skill_frequency(conn, f, NOW)["total"] == 5            # not 6
    assert {s["skill_id"]: s["count"] for s in q.skill_frequency(conn, f, NOW)["skills"]}["docker"] == 1
    assert q.city_totals(conn, f, NOW) == {"Berlin": 4, "San Francisco": 1}
    r = q.list_jobs(conn, f, NOW)
    assert r["total"] == 6 and {j["company"]: j["legacy"] for j in r["jobs"]}["Zeta"] is True
    assert q.job_detail(conn, jid, NOW)["legacy"] is True
    assert q.stats(conn, NOW, 1)["legacy"] == 1


def test_too_short_jobs_stay_out_of_the_chart_but_in_the_list(conn):
    p = Posting("screenshot", "", "", "Theta", "AI Engineer", "Berlin", "Theta AI Engineer. Python.")
    jid = int(ingest_one(conn, p, ts(1), require_city=False, trust_title=True)[4:])
    store_extraction(conn, jid, Extraction(mentions=[Mention("python", "required", "Python")],
                                           extractor_version="t", taxonomy_version=3))
    f = q.Filters(window="all")
    assert q.skill_frequency(conn, f, NOW)["total"] == 5  # not 6
    assert q.city_totals(conn, f, NOW) == {"Berlin": 4, "San Francisco": 1}
    r = q.list_jobs(conn, f, NOW)
    assert r["total"] == 6 and {j["company"]: j["too_short"] for j in r["jobs"]}["Theta"] is True
    assert not any(j["too_short"] for j in r["jobs"] if j["company"] != "Theta")
    assert q.job_detail(conn, jid, NOW)["too_short"] is True
    assert q.stats(conn, NOW, 1)["too_short"] == 1


def test_proposed_grouping_and_resolution(conn):
    groups = q.proposed_skills(conn)
    assert [(g["label"], g["count"]) for g in groups] == [("Rust", 2), ("DSPy", 1)]  # case-insensitive group
    rust = groups[0]
    n = q.resolve_proposed(conn, rust["ids"], "accepted", "rust-lang", taxonomy_version=3)
    assert n == 2
    assert conn.execute("SELECT count(*) FROM skill_mention WHERE skill_id='rust-lang'").fetchone()[0] == 2
    assert q.proposed_skills(conn) and q.proposed_skills(conn)[0]["label"] == "DSPy"
    n = q.resolve_proposed(conn, q.proposed_skills(conn)[0]["ids"], "rejected", None, 3)
    assert n == 1 and q.proposed_skills(conn) == []
    with pytest.raises(ValueError):
        q.resolve_proposed(conn, [1], "accepted", None, 3)
