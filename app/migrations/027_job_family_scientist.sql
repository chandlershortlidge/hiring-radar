-- 027: titles with "scientist" in them are sorted by the kind of scientist (HIR-452).
--
-- 017 gave every job a family from its title, first match wins, with `ai-engineer` as the
-- remainder. No row of that rule named a scientist other than "data scien..." and "applied
-- scientist", so "Senior Machine Learning Scientist" and "AI Scientist" matched nothing and
-- fell through to `ai-engineer`. That inflated the AI-engineer count and hid ML-engineer
-- and research demand.
--
-- The rule now reads, in the same row order as before:
--   * a data scientist is `data-scientist` (unchanged);
--   * a machine-learning scientist ("machine learning scientist", "ml scientist", with a
--     space or a hyphen) is `ml-engineer`: the rule reads titles only, so it cannot tell a
--     shipping role from a publishing one, and Chandler chose ml-engineer for these;
--   * any other title with "scientist" in it is `research`. That row's old "applied
--     scientist" is covered by the plain "scientist" and is gone.
--
-- This is the whole CASE from 017 with those two rows extended, run over every row, so a
-- stored job carries what `family_of` in app/ingest.py would give its title today. The only
-- rows it changes are scientist titles that sat in `ai-engineer`: every title the old rule
-- matched is matched by the same row here. tests/test_ingest.py asserts both things.
--
-- To undo: revert the change to `family_of` and add a migration that runs 017's CASE
-- again. Titles are not touched, so every job goes back exactly where it was.

UPDATE job SET family = CASE
    WHEN lower(title) LIKE '%data scien%'
      OR lower(title) LIKE '%datenwissenschaft%'                     THEN 'data-scientist'
    WHEN lower(title) LIKE '%mlops%'
      OR lower(title) LIKE '%ml platform%'
      OR lower(title) LIKE '%ml-platform%'
      OR lower(title) LIKE '%ml infra%'
      OR lower(title) LIKE '%platform engineer%'                     THEN 'ml-platform'
    WHEN lower(title) LIKE '%machine learning engineer%'
      OR lower(title) LIKE '%machine-learning engineer%'
      OR lower(title) LIKE '%ml engineer%'
      OR lower(title) LIKE '%ml-engineer%'
      OR lower(title) LIKE '%machine learning scientist%'
      OR lower(title) LIKE '%machine-learning scientist%'
      OR lower(title) LIKE '%ml scientist%'
      OR lower(title) LIKE '%ml-scientist%'
      -- `mle` only as a whole word, exactly as in 017.
      OR ' ' || replace(replace(replace(replace(replace(replace(
             lower(title), '-', ' '), '/', ' '), '(', ' '), ')', ' '), ',', ' '), '.', ' ')
         || ' ' LIKE '% mle %'                                       THEN 'ml-engineer'
    WHEN lower(title) LIKE '%research%'
      OR lower(title) LIKE '%scientist%'                             THEN 'research'
    ELSE 'ai-engineer'
END;
