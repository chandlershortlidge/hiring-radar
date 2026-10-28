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


def test_production_filters_stats_and_detail(conn):
    # Acme: production required. Gamma: nice_to_have. Everything else: not asked for.
    conn.execute("UPDATE job SET production='required', production_basis='stated',"
                 " production_signal='You have shipped production systems' WHERE company='Acme'")
    conn.execute("UPDATE job SET production='nice_to_have', production_basis='stated',"
                 " production_signal='production ML is a plus' WHERE company='Gamma'")
    names = lambda f: {j["company"] for j in q.list_jobs(conn, f, NOW)["jobs"]}
    assert names(q.Filters(window="all", production="required")) == {"Acme"}
    # not_required means the same for production as for German: not asked for, or optional.
    assert names(q.Filters(window="all", production="not_required")) == {"Beta", "Gamma", "Delta", "Epsilon"}
    assert names(q.Filters(window="all", production="none")) == {"Beta", "Delta", "Epsilon"}
    assert names(q.Filters(window="all", production="any")) == names(q.Filters(window="all"))
    assert q.skill_frequency(conn, q.Filters(window="all", production="required"), NOW)["total"] == 1
    assert q.stats(conn, NOW, 1)["open_production_required"] == 1
    jid = q.list_jobs(conn, q.Filters(window="all", query="acme"), NOW)["jobs"][0]["id"]
    d = q.job_detail(conn, jid, NOW)
    assert d["production"] == "required" and d["production_basis"] == "stated"
    assert d["production_signal"] == "You have shipped production systems"
    # the list carries the value (the row's "!" flag needs it) but not the quote
    row = next(j for j in q.list_jobs(conn, q.Filters(window="all", query="acme"), NOW)["jobs"])
    assert row["production"] == "required" and "production_signal" not in row


def test_production_and_german_filters_are_independent(conn):
    conn.execute("UPDATE job SET german='required', german_basis='stated', german_signal='German' WHERE company='Acme'")
    conn.execute("UPDATE job SET production='required', production_basis='stated',"
                 " production_signal='shipped production systems' WHERE company='Gamma'")
    names = lambda f: {j["company"] for j in q.list_jobs(conn, f, NOW)["jobs"]}
    # the headline set: no German asked for and no production experience asked for
    assert names(q.Filters(window="all", german="not_required", production="not_required")) \
        == {"Beta", "Delta", "Epsilon"}
    assert names(q.Filters(window="all", german="required", production="required")) == set()


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


# --- related skills (HIR-66) -------------------------------------------------------------

# skill_frequency's output on the fixture above, captured before related_skills factored
# the group/sort/pct block out into _skill_rows. The panel must not move the chart.
FREQ_SNAPSHOT = {
    "default": {"total": 3, "skills": [
        {"skill_id": "python", "count": 2, "by_city": {"Berlin": 1, "San Francisco": 1}, "pct": 66.7},
        {"skill_id": "rag", "count": 2, "by_city": {"Berlin": 2}, "pct": 66.7},
        {"skill_id": "aws", "count": 1, "by_city": {"San Francisco": 1}, "pct": 33.3}]},
    "all_all": {"total": 5, "skills": [
        {"skill_id": "python", "count": 4, "by_city": {"Berlin": 3, "San Francisco": 1}, "pct": 80.0},
        {"skill_id": "aws", "count": 2, "by_city": {"Berlin": 1, "San Francisco": 1}, "pct": 40.0},
        {"skill_id": "rag", "count": 2, "by_city": {"Berlin": 2}, "pct": 40.0},
        {"skill_id": "docker", "count": 1, "by_city": {"Berlin": 1}, "pct": 20.0}]},
    "berlin_all": {"total": 4, "skills": [
        {"skill_id": "python", "count": 3, "by_city": {"Berlin": 3}, "pct": 75.0},
        {"skill_id": "rag", "count": 2, "by_city": {"Berlin": 2}, "pct": 50.0},
        {"skill_id": "docker", "count": 1, "by_city": {"Berlin": 1}, "pct": 25.0}]},
}
FREQ_CASES = {
    "default": q.Filters(),
    "all_all": q.Filters(requirement="all", window="all"),
    "berlin_all": q.Filters(cities=("Berlin",), window="all"),
}


def test_skill_frequency_output_unchanged_by_the_related_skills_refactor(conn):
    for name, f in FREQ_CASES.items():
        assert q.skill_frequency(conn, f, NOW) == FREQ_SNAPSHOT[name], name


# Twenty jobs, chosen so the numbers for the selected skill "python" are exact. Over the
# whole set (window="all"): 20 jobs, 10 of them require python. Among those 10 — docker 6,
# pytorch 5, aws 5, rag 5, kubernetes 4 (below MIN_CO_JOBS) — against baselines over all
# 20: docker 6, pytorch 5, aws 10, rag 15. So lift = 2*count/base: docker and pytorch 2.0
# (the sort's count tiebreak), aws 1.0, rag 0.667. Fifteen jobs are Berlin, five SF.
RELATED_JOBS = [
    ("Co01", "Berlin", ["python", "docker", "pytorch", "aws", "rag", "kubernetes"]),
    ("Co02", "Berlin", ["python", "docker", "pytorch", "aws", "rag", "kubernetes"]),
    ("Co03", "Berlin", ["python", "docker", "pytorch", "aws", "kubernetes"]),
    ("Co04", "Berlin", ["python", "docker", "pytorch", "aws", "kubernetes"]),
    ("Co05", "Berlin", ["python", "docker", "rag"]),
    ("Co06", "Berlin", ["python", "pytorch", "rag"]),
    ("Co07", "Berlin", ["rag", "aws"]),
    ("Co08", "Berlin", ["rag", "aws"]),
    ("Co09", "Berlin", ["rag", "aws"]),
    ("Co10", "Berlin", ["rag", "aws"]),
    ("Co11", "Berlin", ["rag", "aws"]),
    ("Co12", "San Francisco", ["rag"]),
    ("Co13", "San Francisco", ["rag"]),
    ("Co14", "San Francisco", ["rag"]),
    ("Co15", "San Francisco", ["rag"]),
]


@pytest.fixture
def wide(conn):
    for company, city, skills in RELATED_JOBS:
        add(conn, company, "AI Engineer", city, "arbeitnow", ts(1), [(s, "required") for s in skills])
    return conn


ALL = q.Filters(window="all", skill_id="python")


def test_related_skills_counts_shares_and_lift(wide):
    r = q.related_skills(wide, ALL, NOW)
    assert (r["selected_count"], r["total"]) == (10, 20)
    by = {s["skill_id"]: s for s in r["skills"]}
    assert "python" not in by                                    # the selected skill is excluded
    assert "kubernetes" not in by                                # 4 co-occurring jobs, under MIN_CO_JOBS
    assert set(by) == {"docker", "pytorch", "aws", "rag"}
    assert (by["docker"]["count"], by["docker"]["pct"], by["docker"]["base_pct"]) == (6, 60.0, 30.0)
    assert (by["pytorch"]["count"], by["pytorch"]["pct"], by["pytorch"]["base_pct"]) == (5, 50.0, 25.0)
    assert (by["aws"]["count"], by["aws"]["pct"], by["aws"]["base_pct"]) == (5, 50.0, 50.0)
    assert (by["rag"]["count"], by["rag"]["pct"], by["rag"]["base_pct"]) == (5, 50.0, 75.0)
    # Returned by pct desc, then count desc: docker (60%) first, then the three at 50% by id.
    assert [s["skill_id"] for s in r["skills"]] == ["docker", "aws", "pytorch", "rag"]
    assert [s["pct"] for s in r["skills"]] == [60.0, 50.0, 50.0, 50.0]
    # lift from the counts, (count/10) / (base/20): it selects the rows, it does not order them.
    assert [s["lift"] for s in r["skills"]] == [2.0, 1.0, 2.0, 0.667]


def test_related_skills_baseline_follows_the_filters(wide):
    f = q.Filters(window="all", skill_id="python", cities=("Berlin",))
    r = q.related_skills(wide, f, NOW)
    assert (r["selected_count"], r["total"]) == (9, 15)     # Berlin only
    docker = next(s for s in r["skills"] if s["skill_id"] == "docker")
    freq = {s["skill_id"]: s for s in q.skill_frequency(wide, f, NOW)["skills"]}
    assert docker["base_pct"] == freq["docker"]["pct"] == 40.0   # the same filter set, not all 20 jobs
    unfiltered = next(s for s in q.related_skills(wide, ALL, NOW)["skills"] if s["skill_id"] == "docker")
    assert unfiltered["base_pct"] == 30.0 and docker["base_pct"] != unfiltered["base_pct"]
    # aws is in 5 of python's jobs overall but only 4 of Berlin's: the threshold follows the filter too.
    assert "aws" not in {s["skill_id"] for s in r["skills"]}


def test_related_skills_caps_the_list_at_ten(wide):
    # Eight more skills, each in five of python's jobs and nowhere else: lift 2.0, count 5.
    # Plus "zz-six", in six of them: the same lift, a higher count, the last id of the lot.
    ids = [r[0] for r in wide.execute(
        "SELECT job_id FROM skill_mention WHERE skill_id='python' ORDER BY job_id LIMIT 6")]
    for skill, n_jobs in [(f"extra{n:02d}", 5) for n in range(8)] + [("zz-six", 6)]:
        for job_id in ids[:n_jobs]:
            wide.execute("INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text,"
                         " taxonomy_version, extractor_version) VALUES (?,?,?,?,?,?)",
                         (job_id, skill, "required", "x", 3, "t"))
    r = q.related_skills(wide, ALL, NOW)
    # Thirteen rows qualify. Eleven tie on lift at 2.0, so the selection's count tiebreak
    # decides the last slot: zz-six (6 jobs) is in and pytorch (5, but an earlier id) is out,
    # and aws (lift 1.0) and rag (0.667) never get close.
    assert len(r["skills"]) == 10
    assert [s["skill_id"] for s in r["skills"]] == ["docker", "zz-six"] + [f"extra{n:02d}" for n in range(8)]
    assert [s["pct"] for s in r["skills"]] == [60.0, 60.0] + [50.0] * 8


def test_related_skills_needs_a_selected_skill_that_jobs_require(wide):
    assert q.related_skills(wide, q.Filters(window="all"), NOW) == {"selected_count": 0, "total": 20, "skills": []}
    r = q.related_skills(wide, q.Filters(window="all", skill_id="nothing-asks-for-this"), NOW)
    assert r == {"selected_count": 0, "total": 20, "skills": []}
