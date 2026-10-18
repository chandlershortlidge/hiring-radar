-- 006: two more per-job requirement attributes from stage 2, same shape as seniority (004).
-- NULL = the posting does not mention it. Third attribute column set on job; a fourth goes
-- into a job_requirement table instead (DECISIONS 2026-10-18).
ALTER TABLE job ADD COLUMN german TEXT CHECK (german IN ('required', 'nice_to_have'));
ALTER TABLE job ADD COLUMN german_basis TEXT CHECK (german_basis IN ('stated', 'inferred'));
ALTER TABLE job ADD COLUMN german_signal TEXT;
ALTER TABLE job ADD COLUMN degree TEXT CHECK (degree IN ('bachelor', 'master', 'phd'));
ALTER TABLE job ADD COLUMN degree_requirement TEXT CHECK (degree_requirement IN ('required', 'nice_to_have'));
ALTER TABLE job ADD COLUMN degree_or_equivalent INTEGER NOT NULL DEFAULT 0 CHECK (degree_or_equivalent IN (0, 1));
ALTER TABLE job ADD COLUMN degree_signal TEXT;
CREATE INDEX job_german ON job (german);
CREATE INDEX job_degree ON job (degree);
