-- 017: which of five job families each posting belongs to (HIR-186), from the title alone.
--
-- Every row in `job` already passed the ingest title filter (an AI/ML domain term plus a
-- technical role term), so the title carries enough signal to sort the pool into five
-- buckets with no model call and no re-extraction: data scientist, ML platform, ML
-- engineer, research, and AI engineer as the remainder. A model-assigned family can
-- replace this rule later without touching the column, the filter or the dashboard.
--
-- First match wins, in the order below. `ml-platform` is deliberately tested before
-- `ml-engineer` so "ML Platform Engineer" lands in platform, and a title naming two
-- families takes the earlier row ("Senior Data Scientist / Machine Learning Engineer" is
-- data-scientist). Some misfiles are accepted for v1; see DECISIONS.md
-- "Job family is a title rule (v1)" for the known limits.
--
-- The CASE below must stay in step with `family_of` in app/ingest.py, which labels new
-- jobs at insert time. tests/test_ingest.py asserts the two agree on a fixture list of
-- titles, so a change to one that is not made in the other fails the suite.

ALTER TABLE job ADD COLUMN family TEXT CHECK (
    family IN ('ai-engineer', 'ml-engineer', 'data-scientist', 'ml-platform', 'research'));

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
      -- `mle` only as a whole word, so "Samle" and "MLE-adjacent" do not count. SQLite has
      -- no word boundary, so punctuation becomes spaces and the title is padded with them.
      OR ' ' || replace(replace(replace(replace(replace(replace(
             lower(title), '-', ' '), '/', ' '), '(', ' '), ')', ' '), ',', ' '), '.', ' ')
         || ' ' LIKE '% mle %'                                       THEN 'ml-engineer'
    WHEN lower(title) LIKE '%research%'
      OR lower(title) LIKE '%applied scientist%'                     THEN 'research'
    ELSE 'ai-engineer'
END;

-- The job clause filters on family the same way it filters on seniority (004).
CREATE INDEX job_family ON job (family);
