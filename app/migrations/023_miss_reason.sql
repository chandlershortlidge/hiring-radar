-- 023: why each checked posting was missed (HIR-290).
--
-- Every `check` already logs one url_check row (005). It now also records which company,
-- city and careers system the posting belongs to, and one reason from a fixed list, chosen
-- by rule in app/check.py (`miss_reason`), with the detail a fix ticket needs: the board,
-- or the filter and the field that dropped the job. Rows logged before this migration keep
-- NULL here; app/misses.py recovers their reason from the stored `diagnosis` when it reads.

ALTER TABLE url_check ADD COLUMN company TEXT;
ALTER TABLE url_check ADD COLUMN city TEXT;            -- tracked city, 'Remote (EU)', or NULL
ALTER TABLE url_check ADD COLUMN careers_system TEXT;  -- greenhouse / personio / linkedin / own site / ...
ALTER TABLE url_check ADD COLUMN reason TEXT CHECK (reason IN (
    'not_in_sources', 'title_filter', 'location_filter', 'unreadable_system',
    'linkedin_only', 'already_had', 'other'));
ALTER TABLE url_check ADD COLUMN reason_detail TEXT;
