import math

# 1.96 is the conventional choice for about 95% confidence. The exact number
# matters less than using the same one everywhere jobs are ranked, so it is
# a named constant: change it here and every ranking changes together.

Z = 1.96
def confidence_adjusted_score(covered, total, z=Z):
    """Score how well a CV covers a job's required skills, allowing for how little evidence there is.

    The score is the lowest the true coverage ratio could plausibly be, given
    how many skills we actually counted. With few skills the score is pulled
    down: 2 of 2 covered scores well below 1, while 20 of 20 scores close to 1.
    This stops a job with only a couple of listed skills from looking like a
    perfect match.

    Args:
        covered: how many of the job's required skills the CV covers.
        total: how many required skills the job lists.
        z: how cautious to be. The default, 1.96, means we are about 95%
            sure the true ratio is at least the score. A larger z is more
            cautious.

    Returns:
        A number from 0 to 1, where higher means a better match. None when
        total is 0, because there is no evidence to score.
    """
    if total == 0:
        return None
    p = covered / total
    z2 = z * z
    centre = p + z2 / (2 * total)
    spread = z * math.sqrt((p * (1 - p)) / total + z2 / (4 * total * total))
    return (centre - spread) / (1 + z2 / total)


SKILLS_FLOOR = 4
def are_job_skills_thinly_listed(skill_count):
    """Say whether a job lists too few required skills to be ranked on its own numbers.

    Example: a job listing 3 skills is thinly listed, because the floor is 4.
    A job listing 4 skills is not.

    Args:
        skill_count: how many required skills the job lists.

    Returns:
        True when the job lists at least 1 skill and fewer than the skill floor, 4.
        False otherwise. A job listing 0 skills is False: that is "unknown",
        a different case from a short list.
    """
    if skill_count == 0:
        return False
    if skill_count < SKILLS_FLOOR:
        return True

    return False 


def skills_rank_scorer(covered, total):
    """Score a job for ranking, so a job with only a few listed skills cannot look perfect.

    A job listing fewer skills than the floor is scored as if it listed
    4 skills: 2 of 2 is scored as 2 of 4. A job at or above the floor is
    scored on its own numbers. The score itself comes from
    confidence_adjusted_score.

    Args:
        covered: how many of the job's required skills the CV covers.
        total: how many required skills the job lists.

    Returns:
        A number from 0 to 1, where higher means a better match. None when
        total is 0, because there is no evidence to score.
    """
    if total == 0:
        return None
    if total <= SKILLS_FLOOR:
        return confidence_adjusted_score(covered, SKILLS_FLOOR)
    return confidence_adjusted_score(covered, total)
    