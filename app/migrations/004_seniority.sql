-- 004: seniority the posting targets, from stage 2. NULL = no usable signal in the text.
ALTER TABLE job ADD COLUMN seniority TEXT CHECK (seniority IN ('junior', 'mid', 'senior'));
ALTER TABLE job ADD COLUMN seniority_basis TEXT CHECK (seniority_basis IN ('stated', 'inferred'));
ALTER TABLE job ADD COLUMN seniority_signal TEXT;
CREATE INDEX job_seniority ON job (seniority);
