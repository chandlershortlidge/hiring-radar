"""Record a newly added skill id so the taxonomy cannot quietly lose it (HIR-209).

Does: append every id in taxonomy/skills.json that is not yet in
tests/fixtures/skill_ids.json, which tests/test_taxonomy.py checks; and write today's date
into taxonomy/added.json for every id that has none there, the day each skill joined the
list (HIR-232: "what's rising" leaves a skill out until it has been read for long enough).
A date already written is never changed.

Does NOT: remove an id from the list. A skill id is never renamed or removed once rows
reference it (taxonomy/README.md): dropping one takes that skill off the chart for every
job that mentions it, with no error anywhere. So this script cannot silence the failure an
removed id causes — it exits non-zero and names it. If an id really must go, the list is
edited by hand, deliberately, in the same commit.

    uv run python scripts/record_skill_ids.py
"""

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "taxonomy" / "skills.json"
KNOWN_IDS = ROOT / "tests" / "fixtures" / "skill_ids.json"
ADDED = ROOT / "taxonomy" / "added.json"


def with_dates(current: set[str], dates: dict[str, str], today: str) -> dict[str, str]:
    """`dates` plus `today` for every current id it lacks. Never changes a date it has."""
    return dict(sorted({**{sid: today for sid in current}, **dates}.items()))


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

    dates = json.loads(ADDED.read_text()) if ADDED.exists() else {}
    dated = with_dates(current, dates, date.today().isoformat())
    if dated != dates:
        ADDED.write_text(json.dumps(dated, indent=1) + "\n")
        print(f"dated {len(dated) - len(dates)} new skill id(s) in taxonomy/added.json")

    for sid in removed:
        print(f"ERROR: skill id {sid!r} is recorded but no longer in taxonomy/skills.json; "
              f"every job that mentions it loses that skill from the chart", file=sys.stderr)
    return 1 if removed else 0


if __name__ == "__main__":
    raise SystemExit(main())
