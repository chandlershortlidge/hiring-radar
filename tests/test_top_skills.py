from app.top_skills import find_skills_dropped_from_top_10_skills


def test_find_skills_dropped_from_top_10_skills_ignores_a_drop_of_one_repeat():
    expected = ["apis"]
    baseline = [["apis"], [], []]
    new_run = [[], [], []]
    assert find_skills_dropped_from_top_10_skills(expected, baseline, new_run) == []


def test_find_skills_dropped_from_top_10_skills_reports_a_skill_that_fell_by_two_repeat():
    expected = ["agents"]
    baseline = [["agents"], ["agents"], ["agents"]]
    new_run = [["agents"], [], []]
    assert find_skills_dropped_from_top_10_skills(expected, baseline, new_run) == ["agents"]


def test_find_skills_dropped_from_top_10_skills_ignores_skills_that_were_kept_or_gained():
    expected = ["python", "llms"]
    baseline = [["python", "llms"]] * 3
    new_run = [["python", "llms", "rag", "agents"]] * 3
    assert find_skills_dropped_from_top_10_skills(expected, baseline, new_run) == []


def test_find_skills_dropped_from_top_10_skills_ignores_a_skill_that_is_not_in_the_expected_list():
    expected = ["python"]
    baseline = [["python", "excel"]] * 3
    new_run = [["python"]] * 3
    assert find_skills_dropped_from_top_10_skills(expected, baseline, new_run) == []


def test_find_skills_dropped_from_top_10_skills_reports_two_skills_lost_at_once():
    expected = ["agents", "rag", "python"]
    baseline = [["agents", "rag", "python"]] * 3
    new_run = [["python"]] * 3
    assert find_skills_dropped_from_top_10_skills(expected, baseline, new_run) == ["agents", "rag"]
