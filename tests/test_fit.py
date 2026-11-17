from app.fit import confidence_adjusted_score, are_job_skills_thinly_listed, skills_rank_scorer
import pytest


def test_confidence_adjusted_score_is_none_when_total_is_zero():
    assert confidence_adjusted_score(0, 0) is None


def test_confidence_adjusted_score_is_zero_when_covered_is_zero():
    assert confidence_adjusted_score(0, 5) == pytest.approx(0, abs=1e-9)


def test_confidence_adjusted_score_matches_the_browser_version():
    assert confidence_adjusted_score(10, 14) == pytest.approx(0.4535, abs=0.0001)


def test_confidence_adjusted_score_more_evidence_ranks_above_a_perfect_ratio():
    assert confidence_adjusted_score(2, 2) < confidence_adjusted_score(10, 15)


def test_are_job_skills_thinly_listed_is_false_when_no_skills_are_listed():
    assert are_job_skills_thinly_listed(0) is False


def test_are_job_skills_thinly_listed_is_true_for_one_skill():
    assert are_job_skills_thinly_listed(1) is True


def test_are_job_skills_thinly_listed_is_true_one_below_the_floor():
    assert are_job_skills_thinly_listed(3) is True


def test_are_job_skills_thinly_listed_is_false_at_exactly_the_floor():
    assert are_job_skills_thinly_listed(4) is False


def test_are_job_skills_thinly_listed_is_false_well_above_the_floor():
    assert are_job_skills_thinly_listed(14) is False


def test_skills_rank_scorer_ranks_two_of_two_as_two_of_four():
    assert skills_rank_scorer(2, 2) == pytest.approx(0.1500, abs=0.0001)


def test_skills_rank_scorer_ranks_three_of_three_as_three_of_four():
    assert skills_rank_scorer(3, 3) == pytest.approx(0.3006, abs=0.0001)


def test_skills_rank_scorer_ranks_four_of_four_as_it_is_at_the_floor():
    assert skills_rank_scorer(4, 4) == pytest.approx(0.5101, abs=0.0001)


def test_skills_rank_scorer_ranks_a_job_above_the_floor_on_its_own_numbers():
    assert skills_rank_scorer(5, 8) == pytest.approx(0.3057, abs=0.0001)


def test_skills_rank_scorer_matches_the_confidence_adjusted_score_above_the_floor():
    assert skills_rank_scorer(10, 14) == pytest.approx(0.4535, abs=0.0001)


def test_skills_rank_scorer_is_none_when_total_is_zero():
    assert skills_rank_scorer(0, 0) is None


def test_skills_rank_scorer_sorts_the_jobs_highest_first():
    jobs = [(2, 2), (3, 3), (4, 4), (5, 8), (10, 14)]
    assert sorted(jobs, key=lambda job: skills_rank_scorer(*job), reverse=True) == [
        (4, 4),
        (10, 14),
        (5, 8),
        (3, 3),
        (2, 2),
    ]
