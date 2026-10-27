-- 009: keep the extractor's validation rejects (HIR-32): items the model returned that failed
-- validation (raw_text not in the job text, unknown skill_id, bad requirement, malformed).
-- One current set per job, replaced on re-extraction like skill_mention.
CREATE TABLE extraction_reject (
    id                INTEGER PRIMARY KEY,
    job_id            INTEGER NOT NULL REFERENCES job (id) ON DELETE CASCADE,
    reason            TEXT NOT NULL,
    skill_id          TEXT,
    raw_text          TEXT,
    item              TEXT NOT NULL,   -- the model's item as JSON
    extractor_version TEXT NOT NULL
);
CREATE INDEX extraction_reject_job ON extraction_reject (job_id);
