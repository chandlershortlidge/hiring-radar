"""A committed migration file is never edited afterwards (HIR-209).

app/db.py states this as an invariant and nothing checked it. An edited migration does not
re-run on a database that already applied it, so the production database and a database
built from scratch quietly stop matching: one has the old statement's effect, the other the
new one, and no error is raised anywhere. A change goes in a new numbered file instead.

tests/fixtures/migration_sha256.json holds a sha256 per migration file. These tests fail if
a recorded fingerprint no longer matches its file, if a recorded file has disappeared, or
if a file has no fingerprint at all. The last case is what makes the first two meaningful:
without it, an edit could be hidden by deleting the file's line from the fixture.

Adding a migration means running `uv run python scripts/record_migration_hashes.py`, which
only ever appends. It cannot refresh a fingerprint that stopped matching, so there is no
one-command way to make an edited migration pass.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIGRATIONS = ROOT / "app" / "migrations"
FINGERPRINTS = ROOT / "tests" / "fixtures" / "migration_sha256.json"


def differences(recorded: dict[str, str], on_disk: dict[str, str]) -> dict[str, list[str]]:
    """Pure: which files were edited, which disappeared, which are unrecorded."""
    return {
        "edited": sorted(n for n, h in recorded.items() if n in on_disk and on_disk[n] != h),
        "gone": sorted(n for n in recorded if n not in on_disk),
        "unrecorded": sorted(n for n in on_disk if n not in recorded),
    }


def _on_disk() -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(MIGRATIONS.glob("*.sql"))}


def test_no_committed_migration_was_edited_disappeared_or_went_unrecorded():
    """The guard itself, against the real files. Every migration in app/migrations/ matches
    the fingerprint committed with it, and every one has a fingerprint."""
    d = differences(json.loads(FINGERPRINTS.read_text()), _on_disk())
    assert not d["edited"], (
        "a migration file changed after it was committed: " + ", ".join(d["edited"])
        + ". An edited migration does not re-run on a database that already applied it, so"
          " production and a fresh database drift apart silently. Restore the file and put"
          " the change in a new numbered file.")
    assert not d["gone"], (
        "a migration file that was committed is gone: " + ", ".join(d["gone"])
        + ". A database built from scratch would no longer get what it did.")
    assert not d["unrecorded"], (
        "migration file(s) with no recorded fingerprint: " + ", ".join(d["unrecorded"])
        + ". Run `uv run python scripts/record_migration_hashes.py` and commit"
          " tests/fixtures/migration_sha256.json with them.")


def test_an_edited_file_is_reported_as_edited():
    assert differences({"001_init.sql": "aaa"}, {"001_init.sql": "bbb"})["edited"] == ["001_init.sql"]


def test_a_deleted_file_is_reported_as_gone():
    assert differences({"001_init.sql": "aaa"}, {})["gone"] == ["001_init.sql"]


def test_a_new_file_must_be_recorded():
    """So an edit cannot be hidden by deleting the file's line from the fixture."""
    assert differences({}, {"019_new.sql": "aaa"})["unrecorded"] == ["019_new.sql"]


def test_an_unchanged_set_of_files_reports_nothing():
    same = {"001_init.sql": "aaa", "018_append_only_guards.sql": "bbb"}
    assert differences(same, dict(same)) == {"edited": [], "gone": [], "unrecorded": []}
