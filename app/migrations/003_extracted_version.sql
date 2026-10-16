-- 003: record which extractor version last processed a job, so zero-skill jobs are not
-- re-extracted on every poll and a version bump re-queues everything exactly once.
ALTER TABLE job ADD COLUMN extracted_version TEXT;
CREATE INDEX job_extracted_version ON job (extracted_version);
