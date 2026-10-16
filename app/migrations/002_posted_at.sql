-- 002: keep the source's own publish date on each sighting.
ALTER TABLE job_source ADD COLUMN posted_at TEXT;
