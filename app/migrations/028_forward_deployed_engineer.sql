-- 028: Forward Deployed Engineer becomes a sixth job family (HIR-408,
-- decisions/2026-11-25-hir-408-forward-deployed-engineer-track.md).
--
-- Two things. The column's list of allowed values gains 'forward-deployed-engineer'
-- (HIR-311: the database and app/scope.py hold the same list). SQLite cannot change a
-- CHECK, so the column is dropped and added again with the longer list; its index goes
-- first and comes back after, and nothing else in the schema names the column. Dropping
-- it empties it, so every row is labelled again below.
--
-- The CASE is 027's, unchanged, with one row in front of it: a title with the FDE words
-- is Forward Deployed Engineer whatever else it names. It means exactly what
-- `FDE_PATTERN` in app/scope.py means: the title lowercased, each of `- / ( ) , .` a
-- space, padded with a space at each end, then
--   * "forward deployed" / "forward deployment" as words, and "engineer" anywhere;
--   * "fde" as a word;
--   * "deployed engineer".
-- So the only stored rows whose family changes are titles with those words; every other
-- row gets back exactly the family 027 gave it. tests/test_ingest.py asserts both.
--
-- To undo: revert the change to app/scope.py and add a migration that runs 027's CASE
-- over every row (and narrows the list again the same way). Titles are not touched.

DROP INDEX job_family;
ALTER TABLE job DROP COLUMN family;
ALTER TABLE job ADD COLUMN family TEXT CHECK (
    family IN ('ai-engineer', 'ml-engineer', 'data-scientist', 'ml-platform', 'research',
               'forward-deployed-engineer'));

UPDATE job SET family = CASE
    WHEN (' ' || replace(replace(replace(replace(replace(replace(
             lower(title), '-', ' '), '/', ' '), '(', ' '), ')', ' '), ',', ' '), '.', ' ')
          || ' ' LIKE '% forward deployed %'
       OR ' ' || replace(replace(replace(replace(replace(replace(
             lower(title), '-', ' '), '/', ' '), '(', ' '), ')', ' '), ',', ' '), '.', ' ')
          || ' ' LIKE '% forward deployment %')
      AND lower(title) LIKE '%engineer%'                             THEN 'forward-deployed-engineer'
    WHEN ' ' || replace(replace(replace(replace(replace(replace(
             lower(title), '-', ' '), '/', ' '), '(', ' '), ')', ' '), ',', ' '), '.', ' ')
         || ' ' LIKE '% fde %'
      OR ' ' || replace(replace(replace(replace(replace(replace(
             lower(title), '-', ' '), '/', ' '), '(', ' '), ')', ' '), ',', ' '), '.', ' ')
         || ' ' LIKE '% deployed engineer%'                          THEN 'forward-deployed-engineer'
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

CREATE INDEX job_family ON job (family);
