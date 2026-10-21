"""Draft new held-out Goldens from jobs in the database, for a person to label.

Does: pick jobs (by default German-language postings, Arbeitsagentur first, skipping
legacy imports and jobs already used as Goldens), and write one draft file per job to
evals/goldens/ with the posting text and every label empty: `expected: []`, attributes
null, `split: "heldout"`, `draft: true`.

Does NOT: call a model or pre-fill labels from the extractor. Held-out labels must come
from the posting, not from the thing being measured; a pre-filled draft anchors the
labeler on the model's answer. run_eval.py skips drafts until `draft` is removed.

    uv run python scripts/new_goldens.py --german 3            # 3 German postings
    uv run python scripts/new_goldens.py --ids 41 57           # specific job ids
    uv run python scripts/new_goldens.py --german 3 --dry-run  # just list the picks
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.extract import extraction_input  # noqa: E402
GOLDENS = ROOT / "evals" / "goldens"
DB = Path(os.environ.get("HIRING_RADAR_DB", ROOT / "data" / "hiring-radar.db"))

_DE = re.compile(r"\b(und|der|die|das|wir|mit|für|oder|sie|ihre|eine|bei|von|zu|auf|deine?|ist)\b", re.I)
_EN = re.compile(r"\b(and|the|we|with|for|or|you|your|our|a|at|of|to|on|is)\b", re.I)


def is_german(text: str) -> bool:
    """True when German function words clearly outnumber English ones."""
    de, en = len(_DE.findall(text)), len(_EN.findall(text))
    return de >= 20 and de > 2 * en


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def existing() -> tuple[set[str], int]:
    hashes, top = set(), 0
    for f in GOLDENS.glob("golden_*.json"):
        g = json.loads(f.read_text())
        hashes.add(g.get("source_sha256") or sha(g["job_description"]))
        top = max(top, int(g["id"].split("_")[1]))
    return hashes, top


def draft(gid: str, text: str, title: str | None = None) -> dict:
    """source_sha256 hashes the stored description (the dedup key); job_description is what
    the extractor is sent, title on top, so the eval sees the same input as production."""
    return {
        "id": gid, "split": "heldout", "draft": True,
        "seniority": None, "seniority_basis": None, "seniority_signal": None,
        "german": None, "german_basis": None, "german_signal": None,
        "degree": None, "degree_requirement": None, "degree_or_equivalent": False, "degree_signal": None,
        "source_sha256": sha(text),
        "job_description": extraction_input(title, text),
        "expected": [],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--german", type=int, default=0, help="pick N German-language postings")
    ap.add_argument("--ids", type=int, nargs="*", default=[], help="specific job ids")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    if not args.german and not args.ids:
        ap.error("give --german N or --ids ...")

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    used, top = existing()
    rows = conn.execute(
        "SELECT j.id, j.company, j.title, j.description_text,"
        " EXISTS (SELECT 1 FROM job_source s WHERE s.job_id = j.id AND s.source = 'arbeitsagentur') AS ba"
        " FROM job j WHERE (j.extracted_version IS NULL OR j.extracted_version != 'legacy')"
        " ORDER BY ba DESC, j.first_seen DESC").fetchall()
    rows = [r for r in rows if sha(r["description_text"]) not in used]
    picks = [r for r in rows if r["id"] in set(args.ids)]
    if args.german:
        picks += [r for r in rows if r["id"] not in set(args.ids) and is_german(r["description_text"])][:args.german]
    if not picks:
        sys.exit("no matching jobs (already Goldens, legacy, or none German)")

    for i, r in enumerate(picks, start=top + 1):
        gid = f"golden_{i:03d}"
        print(f"{gid}  job {r['id']}  {r['company']} · {r['title']}")
        if not args.dry_run:
            path = GOLDENS / f"{gid}.json"
            path.write_text(json.dumps(draft(gid, r["description_text"], r["title"]), indent=2, ensure_ascii=False) + "\n")
    if not args.dry_run:
        print("Label each file per evals/LABELING.md, then delete the \"draft\" key.")


if __name__ == "__main__":
    main()
