-- 016: keep the extractor's whole answer for every reading of every posting (HIR-170).
-- skill_mention holds one current extraction per job: a re-extract deletes the previous one,
-- and the model's tool call is parsed and thrown away. That is enough to draw the chart and
-- not enough to train a smaller model later (HIR-93), which needs the evidence sentence the
-- model chose, the version of the prompt and taxonomy it ran under, and the model name.
-- Model versions retire, prompts change and postings expire, so none of it can be rebuilt
-- afterwards without paying to read every posting again.
--
-- Append-only: one row per extraction that stored something, never updated, never deleted on
-- re-extract. job_id is ON DELETE SET NULL, like url_check (005): a posting we drop or clean
-- up must not take the reading we paid for with it. The row still carries input_sha256, so a
-- reading can be matched back to the exact text that produced it.
CREATE TABLE extraction_log (
    id                INTEGER PRIMARY KEY,
    job_id            INTEGER REFERENCES job (id) ON DELETE SET NULL,
    extractor_version TEXT NOT NULL,
    taxonomy_version  INTEGER NOT NULL,
    model             TEXT NOT NULL,
    created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),  -- ISO 8601 UTC
    raw_output        TEXT NOT NULL,   -- the model's tool-call input as JSON, before validation
    usage             TEXT NOT NULL,   -- token counts as JSON; '{}' when the provider sent none
    input_sha256      TEXT NOT NULL    -- sha256 of the exact text sent to the model
);
CREATE INDEX extraction_log_job ON extraction_log (job_id, id);
CREATE INDEX extraction_log_version ON extraction_log (extractor_version);

-- One row per labeller per posting, so the panel's disagreement can be read back as a soft
-- label instead of only the agreed answer (HIR-170 step 2). Today these live in
-- evals/labeling/<run>/raw/*.json; `python -m app import-labels` loads them, so nothing
-- depends on those folders surviving. Keyed by golden_id, not job_id: a Golden is a file in
-- evals/goldens/, and the posting it came from may no longer be in the database.
-- UNIQUE (run, golden_id, labeler) makes the import idempotent — re-running it loads nothing
-- new and overwrites nothing.
CREATE TABLE label_answer (
    id             INTEGER PRIMARY KEY,
    run            TEXT NOT NULL,   -- the labelling run folder, e.g. 20261103T223629Z_label
    golden_id      TEXT NOT NULL,
    labeler        TEXT NOT NULL,   -- which labeller in the panel: 'A', 'B', 'C'
    provider       TEXT,
    model          TEXT,
    answer         TEXT,            -- the labeller's parsed answer as JSON; NULL if it did not parse
    raw            TEXT,            -- the labeller's reply verbatim, parsed or not
    error          TEXT,            -- the labeller's failure, when it failed
    posting_sha256 TEXT,            -- the posting text it was shown; older runs recorded no hash
    prompt_sha256  TEXT,            -- the labelling prompt it ran under
    imported_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    UNIQUE (run, golden_id, labeler)
);
CREATE INDEX label_answer_golden ON label_answer (golden_id);
