from app.fit import confidence_adjusted_score
import pytest


def test_confidence_adjusted_score_is_none_when_total_is_zero():
    assert confidence_adjusted_score(0, 0) is None


def test_confidence_adjusted_score_is_zero_when_covered_is_zero():
    assert confidence_adjusted_score(0, 5) == pytest.approx(0, abs=1e-9)


def test_confidence_adjusted_score_matches_the_browser_version():
    assert confidence_adjusted_score(10, 14) == pytest.approx(0.4535, abs=0.0001)
    
def test_confidence_adjusted_score_more_evidence_ranks_above_a_perfect_ratio():
    assert confidence_adjusted_score(2, 2) < confidence_adjusted_score(10, 15)