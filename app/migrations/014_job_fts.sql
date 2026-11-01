-- 014_job_fts: full-text index over the stored posting text, for `?text=` on /api/jobs.
--
-- External-content FTS5 table: the text itself stays only in job.description_text, and
-- job_fts holds just the index, keyed by job.id. Triggers keep the two in step, so every
-- writer (ingest, the add endpoints, check) gets indexed without knowing this table exists.
--
-- remove_diacritics 2 so a search for "munchen" finds "München"; unicode61 (the default
-- tokenizer) otherwise, which splits on punctuation — "c++" indexes as the token "c".
CREATE VIRTUAL TABLE job_fts USING fts5(
    description_text,
    content='job',
    content_rowid='id',
    tokenize='unicode61 remove_diacritics 2'
);

INSERT INTO job_fts (rowid, description_text) SELECT id, description_text FROM job;

CREATE TRIGGER job_fts_insert AFTER INSERT ON job BEGIN
    INSERT INTO job_fts (rowid, description_text) VALUES (new.id, new.description_text);
END;

CREATE TRIGGER job_fts_delete AFTER DELETE ON job BEGIN
    INSERT INTO job_fts (job_fts, rowid, description_text) VALUES ('delete', old.id, old.description_text);
END;

-- Guarded on the text alone: every poll runs `UPDATE job SET last_seen=...` over every
-- live job, and reindexing each of those would cost more than the search saves.
CREATE TRIGGER job_fts_update AFTER UPDATE ON job
WHEN old.description_text IS NOT new.description_text BEGIN
    INSERT INTO job_fts (job_fts, rowid, description_text) VALUES ('delete', old.id, old.description_text);
    INSERT INTO job_fts (rowid, description_text) VALUES (new.id, new.description_text);
END;
