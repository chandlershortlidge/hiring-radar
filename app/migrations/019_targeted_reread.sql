-- 019: re-read only the postings a skill-list addition can change (HIR-224).
--
-- `job.extracted_version` keeps meaning "this job needs no reading at this version". A job
-- whose text names none of the skills a version added is moved to the new version without
-- a model call ("carried over"), so that column alone would claim a reading that never
-- happened. `read_version` is the version whose reading actually produced the job's skills:
-- equal to extracted_version after a real reading, older after a carry-over. Backfilled
-- from extracted_version, since every stamp before this migration came from a real reading
-- (or is 'legacy', which is copied as is).
--
-- `extractor_snapshot` remembers, per version stamp, what the stamp was made of: the skill
-- list the prompt carried and a hash of everything else. A stamp is itself a hash, so
-- without this the skill list behind an old stamp could not be compared with today's.
-- Rows are written by the app (app/targeted_reread.py), one per version it ran under.

ALTER TABLE job ADD COLUMN read_version TEXT;
UPDATE job SET read_version = extracted_version WHERE extracted_version IS NOT NULL;

CREATE TABLE extractor_snapshot (
    version TEXT PRIMARY KEY,
    core_hash TEXT NOT NULL,          -- the stamp of everything but the skill list
    skills TEXT NOT NULL,             -- JSON {id: [display, [aliases...]]}, as the prompt listed them
    taxonomy_version INTEGER NOT NULL,
    recorded_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
