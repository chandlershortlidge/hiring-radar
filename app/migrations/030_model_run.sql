-- 030: one row per model run, with what it actually cost (HIR-449).
--
-- Model costs were estimated by hand and the estimates were wrong (HIR-221: "about €3" was
-- about €10). extraction_log (016) already keeps each reading's token counts, but not which
-- run it belonged to, whether it was billed at the Batch API's half price, or what the run
-- as a whole spent. This table is that: written once by the CLI after every run that read
-- at least one posting (app/run_cost.py), read by the admin page, the morning caretaker's
-- over-cost alert and the Monday summary.
--
-- kind: 'poll' the daily collection's reading; 'launch' a city launch's first reading;
-- 're-read' a re-read after an extractor change (`python -m app extract`); 'bulk-read' a
-- held place's or track's one bulk read (`read-pending`); 'add' one posting added by hand.
-- Eval runs are not here: they run on a laptop and their own result files carry the
-- token counts (evals/results/<run>/predictions.jsonl).
--
-- cost_eur is priced from the provider's own token counts at app/reread_cost.py's prices,
-- at half rate when batch = 1. Readings that failed are attempted but not read, and carry
-- no token counts the run could price.
--
-- Append-only, like feed_run (021): a record of what was spent is never rewritten.
-- To undo: a migration that drops the table; nothing else reads or writes it.

CREATE TABLE model_run (
    id                 INTEGER PRIMARY KEY,
    kind               TEXT NOT NULL CHECK (kind IN ('poll', 'launch', 're-read', 'bulk-read', 'add')),
    model              TEXT NOT NULL,
    batch              INTEGER NOT NULL CHECK (batch IN (0, 1)),
    started_at         TEXT NOT NULL,          -- ISO 8601 UTC
    finished_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    attempted          INTEGER NOT NULL,       -- postings sent to the model
    readings           INTEGER NOT NULL,       -- postings read and stored
    input_tokens       INTEGER NOT NULL,
    output_tokens      INTEGER NOT NULL,
    cache_read_tokens  INTEGER NOT NULL,
    cache_write_tokens INTEGER NOT NULL,
    cost_eur           REAL NOT NULL
);
CREATE INDEX model_run_started ON model_run (started_at);

CREATE TRIGGER model_run_is_append_only_update BEFORE UPDATE ON model_run
BEGIN
    SELECT RAISE(ABORT, 'model_run is append-only: a recorded run may not be changed');
END;

CREATE TRIGGER model_run_is_append_only_delete BEFORE DELETE ON model_run
BEGIN
    SELECT RAISE(ABORT, 'model_run is append-only: a recorded run may not be deleted');
END;
