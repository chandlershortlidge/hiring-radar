"""Record a newly added skill id so the taxonomy cannot quietly lose it (HIR-209).

Does: append every id in taxonomy/skills.json that is not yet in
tests/fixtures/skill_ids.json, which tests/test_taxonomy.py checks.

Does NOT: remove an id from the list. A skill id is never renamed or removed once rows
reference it (taxonomy/README.md): dropping one takes that skill off the chart for every
job that mentions it, with no error anywhere. So this script cannot silence the failure an
removed id causes — it exits non-zero and names it. If an id really must go, the list is
edited by hand, deliberately, in the same commit.

    uv run python scripts/record_skill_ids.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "taxonomy" / "skills.json"
KNOWN_IDS = ROOT / "tests" / "fixtures" / "skill_ids.json"


def main() -> int:
    current = {s["id"] for s in json.loads(SKILLS.read_text())["skills"]}
    known = set(json.loads(KNOWN_IDS.read_text())) if KNOWN_IDS.exists() else set()

    added = sorted(current - known)
    removed = sorted(known - current)

    if added:
        KNOWN_IDS.write_text(json.dumps(sorted(known | current), indent=2) + "\n")
        print(f"recorded {len(added)} new skill id(s): {', '.join(added)}")
    else:
        print("nothing new to record")

    for sid in removed:
        print(f"ERROR: skill id {sid!r} is recorded but no longer in taxonomy/skills.json; "
              f"every job that mentions it loses that skill from the chart", file=sys.stderr)
    return 1 if removed else 0


if __name__ == "__main__":
    raise SystemExit(main())
