-- 022: every place a job is posted for, not only the first (HIR-289).
--
-- `job.city` holds one place: the first tracked city its location names, in a fixed
-- order with Berlin first. A posting for Berlin and Munich therefore counted only under
-- Berlin, one for San Francisco and New York only under San Francisco, and a company's
-- per-city copies of one role, merged into one job, kept only the first copy's city.
--
-- `job_place` is one row per (job, place). `job.city` stays as it was — the job's first
-- place, shown on the job list — and is always one of its rows: the triggers below copy
-- it in whenever a job is written, so every writer of `job` (ingest, scripts, tests) keeps
-- that true without knowing about this table. Ingest adds the other places (app/ingest.py).
-- Rows are only ever added: a place a posting once named is not taken away.
--
-- The dashboard's city filter and per-city counts read this table (app/queries.py), so a
-- job posted for two cities counts once in each; totals over all places still count each
-- job once.

CREATE TABLE job_place (
    job_id INTEGER NOT NULL REFERENCES job(id) ON DELETE CASCADE,
    place  TEXT NOT NULL,                  -- a geo.CITIES name or 'Remote (EU)', as job.city
    PRIMARY KEY (job_id, place)
) WITHOUT ROWID;

CREATE INDEX job_place_place ON job_place (place, job_id);

INSERT INTO job_place (job_id, place) SELECT id, city FROM job WHERE city IS NOT NULL;

CREATE TRIGGER job_place_city_insert AFTER INSERT ON job WHEN NEW.city IS NOT NULL
BEGIN
    INSERT OR IGNORE INTO job_place (job_id, place) VALUES (NEW.id, NEW.city);
END;

CREATE TRIGGER job_place_city_update AFTER UPDATE OF city ON job
    WHEN NEW.city IS NOT NULL AND NEW.city IS NOT OLD.city
BEGIN
    INSERT OR IGNORE INTO job_place (job_id, place) VALUES (NEW.id, NEW.city);
END;
