"""Record the fingerprint of a newly added migration file (HIR-209).

Does: append a sha256 for every migration file that has none recorded yet, to
tests/fixtures/migration_sha256.json, which tests/test_migration_immutability.py checks.

Does NOT: rewrite or drop a fingerprint that is already recorded. A migration file is
never edited after it is committed (app/db.py), so a recorded fingerprint that no longer
matches is a mistake to undo, not a line to refresh — this script cannot silence that
failure, and it exits non-zero when it sees one.

    uv run python scripts/record_migration_hashes.py
"""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIGRATIONS = ROOT / "app" / "migrations"
FINGERPRINTS = ROOT / "tests" / "fixtures" / "migration_sha256.json"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    recorded: dict[str, str] = json.loads(FINGERPRINTS.read_text()) if FINGERPRINTS.exists() else {}
    on_disk = {p.name: sha256_of(p) for p in sorted(MIGRATIONS.glob("*.sql"))}

    changed = sorted(n for n, h in recorded.items() if n in on_disk and on_disk[n] != h)
    gone = sorted(n for n in recorded if n not in on_disk)
    added = sorted(n for n in on_disk if n not in recorded)

    for name in added:
        recorded[name] = on_disk[name]
    if added:
        FINGERPRINTS.write_text(json.dumps(dict(sorted(recorded.items())), indent=2) + "\n")
        print(f"recorded {len(added)} new migration(s): {', '.join(added)}")
    else:
        print("nothing new to record")

    for name in changed:
        print(f"ERROR: {name} has been edited since it was committed; restore it and put the "
              f"change in a new numbered file", file=sys.stderr)
    for name in gone:
        print(f"ERROR: {name} was recorded but is no longer in app/migrations/", file=sys.stderr)
    return 1 if (changed or gone) else 0


if __name__ == "__main__":
    raise SystemExit(main())
