MIN_SKILLS_LOST = 2
def find_skills_dropped_from_top_10_skills(expected:list[str], baseline: list[list[str]], new_run: list[list[str]]) -> list[str]: # result
    """Find which of the top 10 skills were picked up in fewer postings after a change.

    Counts, for each skill, how many postings list it in the baseline run and
    in the new run. A skill is dropped from the top 10 list when its count fell by at least
    MIN_SKILLS_LOST postings. Example: a skill in 9 baseline postings and 6
    new-ru n postings fell by 3, so it is dropped. One that fell from 9 to 8
    is not—this could be noise.

    Args:
        expected: the answer keys' top 10 skills
        baseline: the skills found in each posting by the earlier run, one
            list per posting.
        new_run: the skills found in each posting by the new run, one list
            per posting, in the same postings.

    Returns:
        The skills from expected that were dropped, in the order they appear
        in expected. An empty list when none were dropped. A skill that
        gained postings, or is in neither run, is never dropped.
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
