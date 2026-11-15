-- 024: which feed postings were dropped for reading blank twice (HIR-176).
--
-- Dropping a posting deletes its job and, by cascade, its job_source rows, so nothing was
-- left to say "this feed id was already tried". The feed lists the posting again the next
-- day, ingest stored it as a new job, and it was read twice and dropped again, every day.
-- One row here per (source, source_job_id) the dropped job was listed under; ingest passes
-- over a feed posting that has one (app/ingest.py, SKIPPED_UNREADABLE).
--
-- Not permanent: `extractor_version` is the version that read it blank, and the pipeline
-- deletes every row written under another version, so a change of prompt, model or skill
-- list gives the posting two fresh tries (DECISIONS 2026-11-14, HIR-176).
--
-- No foreign key to job on purpose: the job is gone by the time the row matters.
CREATE TABLE dropped_posting (
    source            TEXT NOT NULL,
    source_job_id     TEXT NOT NULL,
    extractor_version TEXT NOT NULL,
    dropped_at        TEXT NOT NULL,
    PRIMARY KEY (source, source_job_id)
);
