-- 026: company boards the dashboard found we do not collect (HIR-324).
--
-- "Add a job" stores the one posting. When its link is on a company board that is not in
-- config/feeds.json, the company's next posting would be missed again. The board list is
-- a file in the repository, which the server cannot change, so the board is noted here and
-- app/boards_to_add.py files one Linear ticket for the boards waiting; an agent adds them
-- to the list in a pull request.
--
-- One row per board, however many postings led to it: `url` is the first link that did.
-- `ticket` and `filed_at` are set once, when the ticket naming the board has been filed.
-- A row is never deleted: a board that has reached feeds.json simply stops being waited on.

CREATE TABLE board_to_add (
    id          INTEGER PRIMARY KEY,
    source      TEXT NOT NULL,     -- greenhouse / lever / ashby / join
    token       TEXT NOT NULL,     -- the board's name on that system, as the link spelled it
    company     TEXT,
    url         TEXT NOT NULL,     -- the checked link that named the board
    recorded_at TEXT NOT NULL,
    ticket      TEXT,              -- the Linear ticket that asks for it, once filed
    filed_at    TEXT,
    CHECK ((ticket IS NULL) = (filed_at IS NULL))
);
CREATE UNIQUE INDEX board_to_add_board ON board_to_add (source, lower(token));
