-- 020: alternative groups (HIR-251, DECISIONS 2026-11-11). A posting that accepts any one
-- of several tools ("Python, Rust, Go or Java") stores them with the same group number.
-- Numbers are scoped to one job; NULL means the skill stands alone, which is every row
-- written before this migration. The chart ignores the column (each member still counts
-- for its own bar); the browser's skill match counts a required group as one requirement.

ALTER TABLE skill_mention ADD COLUMN alternative_group INTEGER
    CHECK (alternative_group IS NULL OR alternative_group >= 1);
