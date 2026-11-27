-- 029: software engineer becomes a seventh job family, incubating (HIR-397,
-- decisions/2026-11-27-hir-397-software-engineer-incubating.md).
--
-- The column's list of allowed values gains 'software-engineer' (HIR-311: the database and
-- app/scope.py hold the same list). SQLite cannot change a CHECK, so a new column with the
-- longer list takes a copy of every row's family, the old column goes (its index first),
-- and the new one takes its name. No row's family changes: every stored job passed the old
-- title filter, which no software engineer title passes unless another track holds it, so
-- unlike 028 there is nothing to re-label. tests/test_ingest.py asserts that.
--
-- To undo: revert the change to app/scope.py and add a migration that narrows the list the
-- same way, after the track's jobs are deleted or moved (a narrower CHECK refuses them).

ALTER TABLE job ADD COLUMN family_029 TEXT CHECK (
    family_029 IN ('ai-engineer', 'ml-engineer', 'data-scientist', 'ml-platform', 'research',
                   'forward-deployed-engineer', 'software-engineer'));
UPDATE job SET family_029 = family;
DROP INDEX job_family;
ALTER TABLE job DROP COLUMN family;
ALTER TABLE job RENAME COLUMN family_029 TO family;
CREATE INDEX job_family ON job (family);
