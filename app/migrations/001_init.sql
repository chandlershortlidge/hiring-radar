-- 001_init: core tables for jobs, where they came from, and the skills found in them.

-- One row per real-world posting. Reposts and multi-source sightings merge here.
CREATE TABLE job (
    id               INTEGER PRIMARY KEY,
    company          TEXT,
    title            TEXT,
    title_key        TEXT,          -- normalized title for dedup (lowercased, gender tags stripped)
    city             TEXT,          -- normalized, e.g. 'Berlin', 'San Francisco'
    location_raw     TEXT,          -- as the source stated it
    description_text TEXT NOT NULL, -- the text stage 2 reads (from a feed, paste, or stage-1 transcript)
    first_seen       TEXT NOT NULL, -- ISO 8601 UTC
    last_seen        TEXT NOT NULL,
    repost_count     INTEGER NOT NULL DEFAULT 0,
    created_at       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
CREATE INDEX job_company_title ON job (company, title_key);

-- Every sighting of a job from a given source. A job can have many.
CREATE TABLE job_source (
    id            INTEGER PRIMARY KEY,
    job_id        INTEGER NOT NULL REFERENCES job (id) ON DELETE CASCADE,
    source        TEXT NOT NULL CHECK (source IN
                    ('greenhouse', 'lever', 'ashby', 'startup_jobs', 'arbeitnow',
                     'url', 'paste', 'screenshot')),
    source_job_id TEXT,             -- the source's own stable id; NULL for paste/screenshot
    url           TEXT,
    found_via     TEXT,             -- manual adds only: 'linkedin', 'indeed', 'company_site', 'referral', 'other'
    first_seen    TEXT NOT NULL,
    last_seen     TEXT NOT NULL,
    UNIQUE (source, source_job_id)
);
CREATE INDEX job_source_job ON job_source (job_id);

-- Screenshot bytes for jobs that entered as images; kept so stage 1 can be re-run.
CREATE TABLE screenshot (
    job_id     INTEGER PRIMARY KEY REFERENCES job (id) ON DELETE CASCADE,
    sha256     TEXT NOT NULL UNIQUE,
    media_type TEXT NOT NULL CHECK (media_type IN ('image/png', 'image/jpeg', 'image/webp')),
    bytes      BLOB NOT NULL
);

-- Skills extracted from a job, as taxonomy ids. Versions let us re-normalize or re-extract later.
CREATE TABLE skill_mention (
    id                INTEGER PRIMARY KEY,
    job_id            INTEGER NOT NULL REFERENCES job (id) ON DELETE CASCADE,
    skill_id          TEXT NOT NULL,
    requirement       TEXT NOT NULL CHECK (requirement IN ('required', 'nice_to_have')),
    raw_text          TEXT NOT NULL,
    taxonomy_version  INTEGER NOT NULL,
    extractor_version TEXT NOT NULL,
    UNIQUE (job_id, skill_id)
);
CREATE INDEX skill_mention_skill ON skill_mention (skill_id);

-- Skills the model proposed that are not in the taxonomy yet. Never shown on the chart until accepted.
CREATE TABLE proposed_skill (
    id       INTEGER PRIMARY KEY,
    job_id   INTEGER NOT NULL REFERENCES job (id) ON DELETE CASCADE,
    label    TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    status   TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
    resolved_skill_id TEXT
);
