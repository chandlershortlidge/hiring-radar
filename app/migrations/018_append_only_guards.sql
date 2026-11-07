-- 018: make the append-only rule of extraction_log and label_answer (016) something the
-- database enforces, not something a comment asks for (HIR-209).
--
-- Both tables hold readings that cannot be rebuilt: an extraction_log row is the model's
-- own answer for one paid reading of one posting, and a label_answer row is one labeller's
-- verdict in a panel whose run folder may be gone. 016 says "never updated, never deleted"
-- and nothing stopped either. A script or an agent that did not know the rule would lose
-- the row silently, with no error and no way back.
--
-- What is append-only here is the *reading*, not which posting it hangs off. Two recorded
-- behaviours move that link and must keep working: extraction_log.job_id is ON DELETE SET
-- NULL by design, so dropping a posting does not take the reading we paid for with it
-- (016); and folding a duplicate posting into the row it duplicates re-points the
-- duplicate's readings at the kept row rather than deleting them (HIR-208, app/repair.py
-- merge_jobs). So the UPDATE trigger lets job_id change and freezes every other column —
-- the model, the versions, the timestamp, the raw answer, the token counts and the hash of
-- the text that was read. (With recursive_triggers off, as it is here, a foreign-key action
-- fires no trigger at all; the exception is written out anyway so the guard does not depend
-- on that pragma.) label_answer has no job link, so it refuses every UPDATE.
--
-- Loudly: RAISE(ABORT) rolls the statement back with the message below, so a wrong write
-- fails where it happens instead of leaving a gap to find later.

CREATE TRIGGER extraction_log_is_append_only_update
BEFORE UPDATE ON extraction_log
WHEN NOT (new.id = old.id
          AND new.extractor_version = old.extractor_version
          AND new.taxonomy_version = old.taxonomy_version
          AND new.model = old.model
          AND new.created_at = old.created_at
          AND new.raw_output = old.raw_output
          AND new."usage" = old."usage"
          AND new.input_sha256 = old.input_sha256)
BEGIN
    SELECT RAISE(ABORT, 'extraction_log is append-only: a stored reading may not be changed');
END;

CREATE TRIGGER extraction_log_is_append_only_delete
BEFORE DELETE ON extraction_log
BEGIN
    SELECT RAISE(ABORT, 'extraction_log is append-only: a stored reading may not be deleted');
END;

CREATE TRIGGER label_answer_is_append_only_update
BEFORE UPDATE ON label_answer
BEGIN
    SELECT RAISE(ABORT, 'label_answer is append-only: a stored label may not be changed');
END;

CREATE TRIGGER label_answer_is_append_only_delete
BEFORE DELETE ON label_answer
BEGIN
    SELECT RAISE(ABORT, 'label_answer is append-only: a stored label may not be deleted');
END;
