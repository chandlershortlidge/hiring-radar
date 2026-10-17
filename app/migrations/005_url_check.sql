-- 005: one row per `check` run, so feed coverage can be measured from the postings a person
-- actually found by hand — including the ones a feed already had, which leave no job_source row.
CREATE TABLE url_check (
    id          INTEGER PRIMARY KEY,
    url         TEXT NOT NULL,
    checked_at  TEXT NOT NULL,      -- ISO 8601 UTC
    found_via   TEXT,               -- where the person found the posting: 'linkedin', 'company_site', ...
    verdict     TEXT NOT NULL CHECK (verdict IN ('found', 'not_found')),
    job_id      INTEGER REFERENCES job (id) ON DELETE SET NULL,  -- the matched job; NULL when not found
    feed_had_it INTEGER NOT NULL CHECK (feed_had_it IN (0, 1)),  -- found AND a feed had stored it, as of checked_at
    diagnosis   TEXT                -- the not-found reason, verbatim
);
CREATE INDEX url_check_url ON url_check (url, id);
