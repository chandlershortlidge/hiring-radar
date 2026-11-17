-- 025: "this job doesn't belong here" flags (HIR-226).
--
-- One row per click on a job's flag button. The row carries everything needed to work out
-- later why the job showed, with nobody having to remember: `view` is the whole dashboard
-- state at that moment (every filter, the sort, the search, the page address), and `job`
-- is the job as it was stored at that moment (title, company, places, sources, family,
-- seniority and the quote it rests on, German, degree, production, skills, extractor
-- version). Both are JSON, written once. A later re-read of the job changes the job row
-- and leaves this copy alone, which is the point: the flag is about what was on screen.
--
-- Append-only in the sense of 018: what was recorded is never changed and a row is never
-- deleted. Three things may still move, and nothing else:
--   * job_id: ON DELETE SET NULL, so removing a job does not take its flags with it, and
--     folding a duplicate job into the row it duplicates re-points the flag at the kept row
--     (app/repair.py merge_jobs finds this table by its foreign key);
--   * note: the optional one line typed after the click, while the flag is open;
--   * closed_at + closed_reason: set once. 'unflagged' is a second click on the button,
--     'fixed' is `python -m app flags --fixed`. A closed flag is frozen entirely.
--
-- No personal data: no address, no browser, no account. The site has one user today.

CREATE TABLE job_flag (
    id            INTEGER PRIMARY KEY,
    job_id        INTEGER REFERENCES job (id) ON DELETE SET NULL,
    created_at    TEXT NOT NULL,
    view          TEXT NOT NULL,    -- JSON: the dashboard state the job was flagged from
    job           TEXT NOT NULL,    -- JSON: the job as stored at that moment
    note          TEXT,
    closed_at     TEXT,
    closed_reason TEXT CHECK (closed_reason IN ('unflagged', 'fixed')),
    CHECK ((closed_at IS NULL) = (closed_reason IS NULL))
);
CREATE INDEX job_flag_job ON job_flag (job_id);

CREATE TRIGGER job_flag_is_append_only_update
BEFORE UPDATE ON job_flag
WHEN NOT (new.id = old.id
          AND new.created_at = old.created_at
          AND new.view = old.view
          AND new.job = old.job
          AND (old.closed_at IS NULL
               OR (new.closed_at IS old.closed_at
                   AND new.closed_reason IS old.closed_reason
                   AND new.note IS old.note)))
BEGIN
    SELECT RAISE(ABORT, 'job_flag is append-only: what a flag recorded may not be changed');
END;

CREATE TRIGGER job_flag_is_append_only_delete
BEFORE DELETE ON job_flag
BEGIN
    SELECT RAISE(ABORT, 'job_flag is append-only: a flag may not be deleted');
END;
