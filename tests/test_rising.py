from app.rising import skill_change_calculation


def test_a_rising_skill_reports_a_positive_change():
    assert skill_change_calculation(20, 100, 15, 100) == {
        "total_change": 5.0,
        "current_share": 20.0,
        "previous_share": 15.0,
    }


def test_a_falling_skill_reports_a_negative_change():
    assert skill_change_calculation(15, 100, 20, 100) == {
        "total_change": -5.0,
        "current_share": 15.0,
        "previous_share": 20.0,
    }


def test_too_few_open_jobs_in_the_current_period_returns_none():
    assert skill_change_calculation(20, 19, 15, 100) is None


def test_skill_seen_in_too_few_jobs_in_both_periods_returns_none():
    assert skill_change_calculation(4, 100, 3, 100) is None


def test_an_unchanged_skill_reports_zero_change():
    assert skill_change_calculation(30, 100, 30, 100) == {
        "total_change": 0.0,
        "current_share": 30.0,
        "previous_share": 30.0,
    }


def test_too_few_open_jobs_in_the_previous_period_returns_none():
    assert skill_change_calculation(5, 100, 5, 10) is None


def test_no_open_jobs_in_the_current_period_returns_none():
    assert skill_change_calculation(0, 0, 29, 100) is None
