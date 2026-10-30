"""Import the legacy job-skills-dashboard corpus (legacy/*.csv + screenshots) into the DB.

Usage:
    uv run python scripts/import_legacy.py --screenshots ~/path/to/screenshots [--dry-run]

Three groups, decided per job from legacy/job_rows.csv:
  A. Corpus jobs (job-N) whose text is in evals/goldens/ (matched by screenshot sha256)
     → inserted with that text, then extracted by the current stage 2 like any other job.
  B. Jobs with a screenshot file in --screenshots → stage 1 transcribes the image
     (one vision call each), then stage 2 extracts.
  C. Jobs with no text and no image → inserted with the legacy summary as description_text
     and their legacy skills mapped through the taxonomy; stamped extractor_version='legacy'
     so they count on the chart but are never re-extracted. Unmappable legacy labels are
     reported, not stored.

All rows: source='screenshot', found_via='linkedin', first_seen = legacy created_at. Title
filter is skipped (these were chosen by hand); city comes from the Golden text or stays
NULL for Berlin-less remote postings — pass --city Berlin to override for all.

Idempotent: a job already present (by screenshot hash, or by company+text dedup) is skipped.
Does NOT: touch the Goldens, the taxonomy, or the legacy CSVs.
"""

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from app import db  # noqa: E402
from app.extract import DEFAULT_MODEL, Extraction, Mention, extract, make_client  # noqa: E402
from app.ingest import ingest_one, job_id_for_screenshot, store_screenshot  # noqa: E402
from app.pipeline import extract_pending, store_extraction  # noqa: E402
from app.sources import Posting  # noqa: E402
from app.taxonomy import Taxonomy  # noqa: E402
from app.transcribe import DEFAULT_MODEL as VISION_MODEL, transcribe  # noqa: E402

LEGACY = ROOT / "legacy"
DB_PATH = Path(os.environ.get("HIRING_RADAR_DB", ROOT / "data" / "hiring-radar.db"))


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def goldens_by_sha() -> dict[str, dict]:
    out = {}
    for p in (ROOT / "evals/goldens").glob("golden_*.json"):
        g = json.loads(p.read_text())
        out[g["source_sha256"]] = g
    return out


def iso(ts: str) -> str:
    # "2026-06-11 13:19:29.952+00" -> "2026-06-11T13:19:29Z"
    return ts[:19].replace(" ", "T") + "Z"


def legacy_mentions(rows: list[dict], tax: Taxonomy) -> tuple[list[Mention], list[str]]:
    by_id: dict[str, Mention] = {}
    unmapped = []
    for r in rows:
        sid = tax.resolve(r["canonical"]) or tax.resolve(r["raw_text"])
        if sid is None:
            unmapped.append(r["canonical"])
            continue
        prev = by_id.get(sid)
        if prev is None or (prev.requirement == "nice_to_have" and r["requirement"] == "required"):
            by_id[sid] = Mention(sid, r["requirement"], r["raw_text"])
    return sorted(by_id.values(), key=lambda m: m.skill_id), unmapped


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--screenshots", type=Path, required=True, help="folder with job-N.png / live-*.png")
    ap.add_argument("--city", default=None, help="force this city on every imported job (e.g. Berlin)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-extract", action="store_true")
    args = ap.parse_args(argv)

    jobs = read_csv(LEGACY / "job_rows.csv")
    skills: dict[str, list[dict]] = {}
    for r in read_csv(LEGACY / "skill_rows.csv"):
        skills.setdefault(r["job_id"], []).append(r)
    goldens = goldens_by_sha()
    tax = Taxonomy.load()

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = db.connect(DB_PATH)
    db.migrate(conn)
    client = None
    counts = {"A": 0, "B": 0, "C": 0, "skipped": 0, "unmapped": 0}

    for j in jobs:
        legacy_id, when = j["id"], iso(j["created_at"])
        img = args.screenshots / f"{legacy_id}.png"
        data = img.read_bytes() if img.exists() else None
        sha = hashlib.sha256(data).hexdigest() if data else (j.get("screenshot_hash") or None)
        golden = goldens.get(sha) if sha else None

        if sha and job_id_for_screenshot(conn, sha):
            counts["skipped"] += 1
            print(f"{legacy_id}: already imported")
            continue

        if golden:
            group, text = "A", golden["job_description"]
        elif data:
            group = "B"
            if args.dry_run:
                text = "(would transcribe)"
            else:
                client = client or make_client()
                text = transcribe(data, client, VISION_MODEL).text
        else:
            group, text = "C", (j["summary"] or "").strip()
            if not text:
                print(f"{legacy_id}: no text, no image, no summary — skipped")
                counts["skipped"] += 1
                continue

        location = args.city or ("Berlin" if golden and "berlin" in text.lower() else None)
        print(f"{legacy_id}: group {group} — {j['company']} / {j['title']}")
        if args.dry_run:
            counts[group] += 1
            continue

        p = Posting(source="screenshot", source_job_id="", url="", company=j["company"], title=j["title"],
                    location_raw=location, description_text=text, posted_at=when)
        outcome = ingest_one(conn, p, when, require_city=False, found_via="linkedin", trust_title=True)
        if not outcome.startswith("new:"):
            counts["skipped"] += 1
            print(f"  {outcome} (dedup) — skipped")
            continue
        job_id = int(outcome[4:])
        counts[group] += 1
        if data:
            store_screenshot(conn, job_id, data, sha, "image/png")
        if group == "C":
            mentions, unmapped = legacy_mentions(skills.get(legacy_id, []), tax)
            counts["unmapped"] += len(unmapped)
            if unmapped:
                print(f"  unmapped legacy labels: {unmapped}")
            store_extraction(conn, job_id, Extraction(mentions=mentions, extractor_version="legacy",
                                                      taxonomy_version=tax.version))

    print(f"\nimported: A(golden text)={counts['A']} B(transcribed)={counts['B']} C(legacy skills)={counts['C']} "
          f"skipped={counts['skipped']} unmapped_labels={counts['unmapped']}")
    if not args.dry_run and not args.no_extract:
        client = client or make_client()
        report = extract_pending(conn, tax, lambda text, t, m: extract(text, t, client, m), DEFAULT_MODEL)
        print(report.line())


if __name__ == "__main__":
    main()
