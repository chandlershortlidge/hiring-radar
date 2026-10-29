-- 013: a fourth per-job requirement attribute from stage 2, the German shape (006):
-- does the posting ask the candidate for prior experience shipping or operating software
-- that real users depended on? NULL = the posting does not ask for it.
-- production_basis only ever holds 'stated' — unlike German, nothing about the posting's
-- own form implies the demand — but the column keeps the shape the other three have.
-- Fourth and last attribute column group: the fifth demand moves all four into a
-- job_requirement table first (DECISIONS 2026-10-28, amending 2026-10-18).
ALTER TABLE job ADD COLUMN production TEXT CHECK (production IN ('required', 'nice_to_have'));
ALTER TABLE job ADD COLUMN production_basis TEXT CHECK (production_basis IN ('stated'));
ALTER TABLE job ADD COLUMN production_signal TEXT;
CREATE INDEX job_production ON job (production);
