-- 015: how many times the model has read this posting and returned nothing at all
-- (HIR-172). An all-empty tool call is a failed read, not a posting without skills, so the
-- job stays unstamped and is read again. Chandler's decision of 5 Nov: try twice, and if
-- the second attempt is also blank, drop the job. The count is what makes "twice" mean
-- twice across runs — the attempt itself leaves no other trace, since a failed extraction
-- writes no rows. It is never reset: a posting that reads blank is read at most twice
-- whatever the gap between polls.
ALTER TABLE job ADD COLUMN blank_extractions INTEGER NOT NULL DEFAULT 0;
