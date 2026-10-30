"""Draft new held-out Goldens from jobs in the database, for a person to label.

Does: pick jobs (by default German-language postings, Arbeitsagentur first, skipping
legacy imports and jobs already used as Goldens), and write one draft file per job to
evals/goldens/ with the posting text and every label empty: `expected: []`, attributes
null, `split: "heldout"`, `draft: true`.

Does NOT: call a model, or pre-fill labels from the *extractor*. A draft pre-filled by the
thing being measured anchors the labeler on its own answer. Labels drafted by independent
models are a different thing and are allowed: `scripts/agent_label.py` (HIR-70) runs two
blind labelers over the same picks, which is where held-out Goldens now come from. This
script stays the hand-labeling path, and shares its candidate query with that one.
run_eval.py skips drafts until `draft` is removed.

Postings listed in evals/goldens/excluded.json (ruled out of scope by a person during
adjudication) are never picked again, by either script.

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


def excluded_path() -> Path:
    """Where the out-of-scope list lives. Derived from GOLDENS when it is asked for,
    not bound at import, so redirecting GOLDENS redirects this with it."""
    return GOLDENS / "excluded.json"


def excluded() -> list[dict]:
    """Postings a person ruled out of scope at adjudication (evals/goldens/excluded.json).

    Kept as a record rather than a deletion: a posting dropped silently gets re-picked by
    the next run, and nobody can see why it is not a Golden."""
    if not excluded_path().exists():
        return []
    return json.loads(excluded_path().read_text())["excluded"]


def existing() -> tuple[set[str], int]:
    """Hashes not to pick again, and the highest golden_NNN number in use.

    "Not again" covers both Goldens and the excluded list, so a posting ruled out of scope
    stays out. `top` counts Goldens only — an excluded id is never reused, so numbering
    keeps climbing past it."""
    hashes, top = set(), 0
    for f in GOLDENS.glob("golden_*.json"):
        g = json.loads(f.read_text())
        hashes.add(g.get("source_sha256") or sha(g["job_description"]))
        top = max(top, int(g["id"].split("_")[1]))
    for e in excluded():
        hashes.add(e["source_sha256"])
        top = max(top, int(e["golden_id"].split("_")[1]))
    return hashes, top


CANDIDATE_SQL = (
    "SELECT j.id, j.company, j.title, j.city, j.seniority, j.description_text,"
    " EXISTS (SELECT 1 FROM job_source s WHERE s.job_id = j.id AND s.source = 'arbeitsagentur') AS ba,"
    " (SELECT GROUP_CONCAT(s.source) FROM job_source s WHERE s.job_id = j.id) AS sources"
    " FROM job j WHERE (j.extracted_version IS NULL OR j.extracted_version != 'legacy')"
    " ORDER BY ba DESC, j.first_seen DESC")


def candidates(conn, used: set[str]) -> list:
    """Jobs eligible to become a Golden: not a legacy import, not already a Golden.

    Arbeitsagentur first, then newest. Shared with scripts/agent_label.py, which needs the
    same exclusions and re-sorts the rows itself."""
    rows = conn.execute(CANDIDATE_SQL).fetchall()
    return [r for r in rows if sha(r["description_text"]) not in used]


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
    rows = candidates(conn, used)
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
