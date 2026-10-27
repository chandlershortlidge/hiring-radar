"""Put the job title on top of held-out Goldens that came from feed text (HIR-57).

Matches each Golden to its job by `source_sha256` (hash of the stored description) and sets
`job_description` to `extraction_input(title, description)`, the same input production now
sends. Goldens whose text already opens with the title are left alone. Labels are not touched:
check each changed file's seniority against its new title afterwards.

    uv run python scripts/golden_titles.py            # dry run: list what would change
    uv run python scripts/golden_titles.py --write
"""

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.extract import extraction_input  # noqa: E402

GOLDENS = ROOT / "evals" / "goldens"
DB = Path(os.environ.get("HIRING_RADAR_DB", ROOT / "data" / "hiring-radar.db"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    conn = sqlite3.connect(DB)
    by_sha = {hashlib.sha256(d.encode()).hexdigest(): (jid, t, d)
              for jid, t, d in conn.execute("SELECT id, title, description_text FROM job")}
    for f in sorted(GOLDENS.glob("golden_*.json")):
        g = json.loads(f.read_text())
        hit = by_sha.get(g.get("source_sha256"))
        if not hit:
            continue
        jid, title, desc = hit
        new = extraction_input(title, desc)
        if new == g["job_description"]:
            continue
        print(f"{g['id']}  job {jid}  title: {title!r}  seniority now: {g.get('seniority')}/{g.get('seniority_basis')}")
        if args.write:
            g["job_description"] = new
            f.write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
