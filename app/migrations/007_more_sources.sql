-- 007: allow the arbeitsagentur and jsearch feeds in job_source.source.
-- SQLite cannot alter a CHECK constraint, so the table is rebuilt with the same columns,
-- data, unique key and index. Nothing references job_source by foreign key.
CREATE TABLE job_source_new (
    id            INTEGER PRIMARY KEY,
    job_id        INTEGER NOT NULL REFERENCES job (id) ON DELETE CASCADE,
    source        TEXT NOT NULL CHECK (source IN
                    ('greenhouse', 'lever', 'ashby', 'startup_jobs', 'arbeitnow',
                     'arbeitsagentur', 'jsearch',
                     'url', 'paste', 'screenshot')),
    source_job_id TEXT,
    url           TEXT,
    found_via     TEXT,
    first_seen    TEXT NOT NULL,
    last_seen     TEXT NOT NULL,
    posted_at     TEXT,
    UNIQUE (source, source_job_id)
);
INSERT INTO job_source_new (id, job_id, source, source_job_id, url, found_via, first_seen, last_seen, posted_at)
    SELECT id, job_id, source, source_job_id, url, found_via, first_seen, last_seen, posted_at FROM job_source;
DROP TABLE job_source;
ALTER TABLE job_source_new RENAME TO job_source;
CREATE INDEX job_source_job ON job_source (job_id);
