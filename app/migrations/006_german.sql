-- 006: whether the posting asks for German, from stage 2. NULL = not mentioned.
ALTER TABLE job ADD COLUMN german TEXT CHECK (german IN ('required', 'nice_to_have'));
ALTER TABLE job ADD COLUMN german_basis TEXT CHECK (german_basis IN ('stated', 'inferred'));
ALTER TABLE job ADD COLUMN german_signal TEXT;
CREATE INDEX job_german ON job (german);
