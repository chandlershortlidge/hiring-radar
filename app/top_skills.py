MIN_SKILLS_LOST = 2
def find_skills_dropped_from_top_10_skills(expected:list[str], baseline: list[list[str]], new_run: list[list[str]]) -> list[str]: # result
    """Find which of the answer keys' top skills dropped out of the extractor model's top 10.

    The eval runs the model over the answer keys several times (repeats), and
    each repeat produces the model's top 10 skills. For each skill in the
    answer keys' top 10, this counts how many repeats of the baseline run and
    of the new run include it. The skill is lost when the new run's count is
    at least MIN_SKILLS_LOST lower. Example: a skill in 3 of 3 baseline repeats
    and 1 of 3 new repeats fell by 2, so it is lost. One that fell from 1 to 0
    is not: a drop of one repeat is usually a tie for 10th place.

    Only skills in the answer keys' top 10 are checked. If the model stops
    ranking a skill the answer keys never had there, that is an improvement.

    Args:
        expected: the answer keys' top 10 skills, one flat list.
        baseline: the model's top 10 skills from each repeat of the earlier
            run, one list per repeat.
        new_run: the same for the new run.

    Returns:
        The lost skills, in the order they appear in expected. An empty list
        when none were lost.
    """

    baseline_dict = {}
    new_run_dict = {}
    for skills in baseline:
        for skill in skills:
            if skill not in baseline_dict:
                baseline_dict[skill] = 0
            baseline_dict[skill] += 1

    for new_skills in new_run:
        for new_skill in new_skills:
            if new_skill not in new_run_dict:
                new_run_dict[new_skill] = 0
            new_run_dict[new_skill] += 1

    result = []
    for skill in expected:
        before = baseline_dict.get(skill, 0)
        after = new_run_dict.get(skill, 0)
        if before - after >= MIN_SKILLS_LOST:
            result.append(skill)
    return result
