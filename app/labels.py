"""Load each labeller's own answer out of the labelling run folders into the database.

Does: read evals/labeling/<run>/raw/*.json — one file per labeller per posting — and append a
label_answer row for each, so the panel's disagreement survives as data and can be read back
as a soft label (HIR-170 step 2). Idempotent: re-running loads only what is not already there.

Does NOT: label anything, adjudicate, or touch the Goldens themselves. The agreed answer still
lives in evals/goldens/; this keeps the individual answers it was agreed from.

Invariants: append-only — an existing row is never updated or deleted, so a run folder that is
later edited cannot rewrite what was imported from it; a file that does not parse is reported
and skipped, never guessed at; (run, golden_id, labeler) identifies one answer.
"""

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = ROOT / "evals" / "labeling"


@dataclass
class ImportReport:
    runs: int = 0
    files: int = 0
    inserted: int = 0
    already: int = 0
    skipped: list[tuple[str, str]] = field(default_factory=list)

    def line(self) -> str:
        return (f"label answers: runs={self.runs} files={self.files} inserted={self.inserted} "
                f"already={self.already} skipped={len(self.skipped)}")


def _golden_id(path: Path, doc: dict) -> str:
    """The posting the answer is about. Later runs record it; the earliest ones only name the file."""
    gid = doc.get("golden_id")
    return str(gid) if gid else path.name.split(".")[0]


def _labeler(path: Path, doc: dict) -> str:
    """Which labeller in the panel. The filename is golden_049.A.json; the key is authoritative."""
    who = doc.get("labeler")
    if who:
        return str(who)
    parts = path.name.split(".")
    return parts[1] if len(parts) > 2 else ""


def answer_row(path: Path, run: str, doc: dict) -> dict:
    """Pure: one raw labeller file as the row it becomes.

    The two hash keys were renamed between runs (`prompt_sha` -> `prompt_sha256`), and the
    earliest run recorded no posting hash at all, so both spellings are accepted and a missing
    one stays NULL rather than being invented."""
    return {
        "run": run,
        "golden_id": _golden_id(path, doc),
        "labeler": _labeler(path, doc),
        "provider": doc.get("provider"),
        "model": doc.get("model"),
        # The parsed answer is the soft label's raw material; `raw` keeps the reply verbatim so a
        # future parser can do better than today's on the files that failed it.
        "answer": json.dumps(doc["parsed"], ensure_ascii=False, sort_keys=True, default=str)
                  if isinstance(doc.get("parsed"), dict) else None,
        "raw": doc.get("raw"),
        "error": doc.get("error"),
        "posting_sha256": doc.get("posting_sha256") or doc.get("posting_sha"),
        "prompt_sha256": doc.get("prompt_sha256") or doc.get("prompt_sha"),
    }


def run_dirs(runs_dir: Path = RUNS_DIR) -> list[Path]:
    """Labelling runs that kept their labellers' raw answers, oldest first."""
    if not runs_dir.is_dir():
        return []
    return sorted(d for d in runs_dir.iterdir() if (d / "raw").is_dir())


def import_answers(conn: sqlite3.Connection, runs_dir: Path = RUNS_DIR, log=print) -> ImportReport:
    report = ImportReport()
    for run_dir in run_dirs(runs_dir):
        report.runs += 1
        run = run_dir.name
        rows = []
        for path in sorted((run_dir / "raw").glob("*.json")):
            report.files += 1
            try:
                doc = json.loads(path.read_text())
                if not isinstance(doc, dict):
                    raise ValueError("not a JSON object")
                row = answer_row(path, run, doc)
                if not row["golden_id"] or not row["labeler"]:
                    raise ValueError("no golden_id or labeller in the file or its name")
            except Exception as e:
                report.skipped.append((f"{run}/{path.name}", f"{type(e).__name__}: {e}"))
                log(f"  {run}/{path.name}: SKIPPED {type(e).__name__}: {str(e)[:200]}")
                continue
            rows.append(row)
        if not rows:
            continue
        # One transaction per run. INSERT OR IGNORE against the UNIQUE key is what makes a second
        # import a no-op instead of a duplicate or an overwrite.
        before = conn.execute("SELECT count(*) FROM label_answer").fetchone()[0]
        with conn:
            conn.executemany(
                "INSERT OR IGNORE INTO label_answer"
                " (run, golden_id, labeler, provider, model, answer, raw, error, posting_sha256, prompt_sha256)"
                " VALUES (:run,:golden_id,:labeler,:provider,:model,:answer,:raw,:error,"
                ":posting_sha256,:prompt_sha256)", rows)
        added = conn.execute("SELECT count(*) FROM label_answer").fetchone()[0] - before
        report.inserted += added
        report.already += len(rows) - added
        log(f"  {run}: {added} new, {len(rows) - added} already there")
    return report
