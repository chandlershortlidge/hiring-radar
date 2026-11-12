-- 021: what each poll got from each feed, and what the caretaker decided about it (HIR-257).
--
-- `feed_run` is one row per feed per poll: did the fetch work, how many postings came
-- back, which optional fields they carried. Until now the poll printed this and forgot
-- it, so "this board has returned nothing for three days" or "this feed usually returns
-- 900" could not be asked of the database. Written by the poll (app/poll.py).
--
-- `caretaker_log` is every finding and every action of the morning caretaker
-- (app/caretaker_run.py): the weekly summary and any later "why was this board paused?"
-- read from the same rows. `mode` says whether it acted or only said what it would do;
-- `done` whether the action was carried out.
--
-- Both are append-only, enforced as 018 does for the extraction log: a record of what
-- happened is never rewritten.

CREATE TABLE feed_run (
    id      INTEGER PRIMARY KEY,
    day     TEXT NOT NULL,                 -- YYYY-MM-DD (UTC) of the poll
    ran_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    label   TEXT NOT NULL,                 -- the poll's label: greenhouse:doctolib, arbeitnow, ...
    kind    TEXT NOT NULL,                 -- board / feed / search (app/sources/registry.py)
    ok      INTEGER NOT NULL CHECK (ok IN (0, 1)),
    seen    INTEGER NOT NULL DEFAULT 0,
    error   TEXT,
    fields  TEXT NOT NULL DEFAULT '[]'     -- JSON list of optional Posting fields some posting filled
);
CREATE INDEX feed_run_label_day ON feed_run (label, day);
CREATE INDEX feed_run_day ON feed_run (day);

CREATE TABLE caretaker_log (
    id         INTEGER PRIMARY KEY,
    day        TEXT NOT NULL,              -- YYYY-MM-DD (UTC) the caretaker ran for
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    mode       TEXT NOT NULL CHECK (mode IN ('report', 'act')),
    subject    TEXT NOT NULL,              -- feed label, 'collection', 'city:<name>', 'caretaker'
    finding    TEXT NOT NULL,              -- board_dead, board_moved, feed_low, spend, weekly_summary, ...
    action     TEXT NOT NULL,              -- none / report / pause / unpause / switch / rerun_collection
    detail     TEXT NOT NULL,              -- one plain sentence, as the weekly summary shows it
    data       TEXT NOT NULL DEFAULT '{}', -- JSON
    done       INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
);
CREATE INDEX caretaker_log_day ON caretaker_log (day);

CREATE TRIGGER feed_run_is_append_only_update BEFORE UPDATE ON feed_run
BEGIN
    SELECT RAISE(ABORT, 'feed_run is append-only: a recorded poll may not be changed');
END;

CREATE TRIGGER feed_run_is_append_only_delete BEFORE DELETE ON feed_run
BEGIN
    SELECT RAISE(ABORT, 'feed_run is append-only: a recorded poll may not be deleted');
END;

CREATE TRIGGER caretaker_log_is_append_only_update BEFORE UPDATE ON caretaker_log
BEGIN
    SELECT RAISE(ABORT, 'caretaker_log is append-only: a logged finding may not be changed');
END;

CREATE TRIGGER caretaker_log_is_append_only_delete BEFORE DELETE ON caretaker_log
BEGIN
    SELECT RAISE(ABORT, 'caretaker_log is append-only: a logged finding may not be deleted');
END;
