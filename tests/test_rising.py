from app.rising import skill_change_calculation

def test_skill_change_calculation():
    assert skill_change_calculation(20, 100, 15, 100) == {'total_change': 5.0, 'current_share': 20.0, 'previous_share': 15.0}
    assert skill_change_calculation(15, 100, 20, 100) == {'total_change': -5.0, 'current_share': 15.0, 'previous_share': 20.0}
    assert skill_change_calculation(20, 19, 15, 100) is None
    assert skill_change_calculation(4, 100, 3, 100) is None
    assert skill_change_calculation(30, 100, 30, 100) == {'total_change': 0.0, 'current_share': 30.0, 'previous_share': 30.0}
    assert skill_change_calculation(5, 100, 5, 10) is None
