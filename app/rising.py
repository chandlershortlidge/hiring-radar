def skill_change_calculation(skill_current_28, open_current_28, skill_previous_28, open_previous_28, min_jobs=20, min_skill_jobs=5):
    """Compare how often one skill is asked for in the last 28 days with the 28 days before.

    Example: 41 of 100 open jobs asked for the skill in the last 28 days,
    and 29 of 100 in the 28 days before. The share went from 29% to 41%,
    a rise of 12 percentage points.

    Args:
        skill_current_28: jobs asking for the skill in the last 28 days.
        open_current_28: all open jobs in the last 28 days.
        skill_previous_28: jobs asking for the skill in the 28 days before.
        open_previous_28: all open jobs in the 28 days before.
        min_jobs: fewest open jobs a period needs for its share to be trusted.
        min_skill_jobs: fewest jobs that must ask for the skill in at least
            one of the two periods.

    Returns:
        A dict with three numbers:
            current_share: percent of open jobs asking for the skill in the
                last 28 days (0 to 100).
            previous_share: the same for the 28 days before.
            total_change: current_share minus previous_share, in percentage
                points. Positive means the skill is rising.
        None when there is too little data to trust a change: a period has
        too few open jobs, or the skill appears in fewer than min_skill_jobs
        jobs in both periods.
    """

    if open_current_28 < min_jobs or open_previous_28 < min_jobs:
        return None

    if skill_current_28 < min_skill_jobs and skill_previous_28 < min_skill_jobs:
        return None

    else:
        current_share = (skill_current_28 / open_current_28 * 100)
        previous_share = (skill_previous_28 / open_previous_28 * 100)

        change = current_share - previous_share
        skill_change_totals = {
            "total_change": change,
            "current_share": current_share,
            "previous_share": previous_share
        }

    return skill_change_totals