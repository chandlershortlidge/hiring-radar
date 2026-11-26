## 2026-11-26 — A usage-limit refusal stops one run, not the rest of the day (HIR-481)

Chandler decided on 26 Nov that a lead agent run refused by the Claude plan's usage limit
no longer stops every later run that day.

**What it is.** A refused run still starts nothing more, does not retry and writes
`Usage limit: reached` in its log. The next scheduled run, four hours later, picks as
normal.

**Why.** The limit resets within hours. On 26 Nov one refusal at 02:30 kept every run
idle until the next day, although the limit had reset at 09:00, so three finished,
approved fixes sat in Todo for a day.

**Supersedes** the rest-of-day stop recorded on 16 Nov
(decisions/2026-11-16-hir-305-one-file-per-decision.md, "anything, when … the usage limit
was hit"). That entry is left as written.

**Undo:** revert PR #292.
