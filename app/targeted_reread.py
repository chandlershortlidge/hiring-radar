"""Re-read only the postings a skill-list addition can change (HIR-224).

Does: remember, per extractor version stamp, the skill list the prompt carried and a hash
of everything else (`extractor_snapshot`); compare an open job's stale stamp with the
current one; when the only difference is skills or spellings *added* to the list, move the
jobs whose text names none of them to the current stamp without a model call ("carry
over"), leaving `job.read_version` on the version whose reading they really have. Every
job it does not carry over stays in the queue and is read in full, as before.

Does NOT: call the model, or touch skill rows, proposed rows or the reading log. A
carried-over job's skills are exactly the ones its last reading produced.

Why: any skill-list edit changes the stamp, and a new stamp re-read every open job — 722
of them, about €5, on 11 Nov. A batch of accepted suggestions can only change the reading
of postings that mention one of the new skills.

Invariants: anything other than a pure addition re-reads in full; so does a stamp with no
recorded snapshot. Matching is generous (case-insensitive, word-bounded, any id, display
name or alias), because an extra re-read costs under a cent and a missed one leaves a
skill off a posting. The "everything else" hash is the stamp of the same code with a fixed
one-skill list, so a new ingredient added to `extractor_version` later is covered here
without anyone remembering to add it. See DECISIONS 2026-11-11.
"""

import json
import re
import sqlite3
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from app.extract import extraction_input, extractor_version
from app.taxonomy import Taxonomy

# A fixed stand-in skill list: the stamp of the current code with this list is the
# fingerprint of everything *but* the skill list — prompt rules, tool schema, model, input
# format, and how the list is laid out in the prompt (one skill with an alias exercises
# the per-line format too).
_CORE_PROBE = {"version": 0, "skills": [{"id": "probe", "display": "Probe", "aliases": ["probe alias"]}]}

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Snapshot:
    version: str
    core: str
    skills: dict  # id -> (display, tuple of aliases), as the prompt listed them
    taxonomy_version: int


def snapshot(tax: Taxonomy, model: str) -> Snapshot:
    return Snapshot(
        version=extractor_version(tax, model),
        core=extractor_version(Taxonomy(_CORE_PROBE), model),
        skills={s.id: (s.display, tuple(s.aliases)) for s in tax.skills.values()},
        taxonomy_version=tax.version)


def record_snapshot(conn: sqlite3.Connection, tax: Taxonomy, model: str) -> Snapshot:
    """Remember what the current stamp is made of. Idempotent; cheap enough for every run."""
    snap = snapshot(tax, model)
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO extractor_snapshot (version, core_hash, skills, taxonomy_version)"
            " VALUES (?,?,?,?)",
            (snap.version, snap.core,
             json.dumps({k: [d, list(a)] for k, (d, a) in snap.skills.items()}, ensure_ascii=False,
                        sort_keys=True),
             snap.taxonomy_version))
    return snap


def load_snapshots(conn: sqlite3.Connection) -> dict[str, Snapshot]:
    out = {}
    for r in conn.execute("SELECT version, core_hash, skills, taxonomy_version FROM extractor_snapshot"):
        skills = {k: (d, tuple(a)) for k, (d, a) in json.loads(r[2]).items()}
        out[r[0]] = Snapshot(r[0], r[1], skills, r[3])
    return out


def snapshot_from_git(model: str, ref: str = "origin/main") -> Snapshot | None:
    """The snapshot `ref`'s skill list would have under *this* code — what `reread-cost`
    compares a branch against when the database has not recorded the old stamp. Only ever
    matches a stored stamp when the branch changed nothing but the skill list, which is
    exactly the case it is for. None when git or the file is unavailable."""
    try:
        text = subprocess.run(["git", "show", f"{ref}:taxonomy/skills.json"], cwd=REPO_ROOT,
                              capture_output=True, text=True, timeout=10, check=True).stdout
        return snapshot(Taxonomy(json.loads(text)), model)
    except Exception:
        return None


def added_names(old: Snapshot, new: Snapshot) -> tuple[list[str], list[str]] | None:
    """(names to look for, skill ids they belong to) when `new` only *adds* to `old`;
    None when anything else differs, which means a full re-read. Pure."""
    if old.core != new.core:
        return None
    names: list[str] = []
    ids: list[str] = []
    for sid, (display, aliases) in old.skills.items():
        if sid not in new.skills:
            return None                       # removed
        new_display, new_aliases = new.skills[sid]
        if new_display != display or not set(aliases) <= set(new_aliases):
            return None                       # renamed, or a spelling taken away
        extra = [a for a in new_aliases if a not in aliases]
        if extra:
            names += extra
            ids.append(sid)
    for sid in sorted(new.skills.keys() - old.skills.keys()):
        display, aliases = new.skills[sid]
        names += [sid, sid.replace("-", " "), display, *aliases]
        ids.append(sid)
    return names, ids


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def names_pattern(names: list[str]) -> re.Pattern | None:
    """Case-insensitive, word-bounded alternation of `names`. None for an empty list."""
    alts = sorted({re.escape(_norm(n)).replace(r"\ ", r"\s+") for n in names if _norm(n)},
                  key=len, reverse=True)
    if not alts:
        return None
    return re.compile(r"(?<!\w)(?:" + "|".join(alts) + r")(?!\w)", re.IGNORECASE)


@dataclass
class Plan:
    """What the next run would do with the open jobs carrying a stale stamp."""
    version: str
    carry: list[int] = field(default_factory=list)    # carried over, no model call
    reread: list[int] = field(default_factory=list)   # read again in full
    added_ids: list[str] = field(default_factory=list)  # skills behind a targeted re-read

    @property
    def stale(self) -> int:
        return len(self.carry) + len(self.reread)


def plan(conn: sqlite3.Connection, tax: Taxonomy, model: str,
         snapshots: dict[str, Snapshot], now: str | None = None) -> Plan:
    """Sort the queue's stale-stamped open jobs into carry-over and re-read. Reads only."""
    from app.pipeline import _pending_clause  # the queue's one definition (HIR-221)
    current = snapshot(tax, model)
    out = Plan(current.version)
    where, params = _pending_clause(current.version, now)
    rows = conn.execute(
        f"SELECT id, extracted_version, title, description_text FROM job j"
        f" WHERE {where} AND j.extracted_version IS NOT NULL ORDER BY id", params).fetchall()
    patterns: dict[str, re.Pattern | None | bool] = {}
    added: set[str] = set()
    for r in rows:
        stamp = r["extracted_version"]
        if stamp not in patterns:
            old = snapshots.get(stamp)
            diff = added_names(old, current) if old else None
            # False = no targeted path for this stamp: re-read in full.
            patterns[stamp] = False if diff is None else names_pattern(diff[0])
            if diff is not None:
                added.update(diff[1])
        pat = patterns[stamp]
        if pat is False:
            out.reread.append(r["id"])
        elif pat is not None and pat.search(_norm(extraction_input(r["title"], r["description_text"]))):
            out.reread.append(r["id"])
        else:
            out.carry.append(r["id"])
    out.added_ids = sorted(added)
    return out


def carry_over(conn: sqlite3.Connection, tax: Taxonomy, model: str, now: str | None = None) -> Plan:
    """Record the current snapshot, then move every job the plan carries to the current
    stamp in one transaction. `read_version` is left alone: it still names the reading."""
    record_snapshot(conn, tax, model)
    p = plan(conn, tax, model, load_snapshots(conn), now)
    if p.carry:
        with conn:
            conn.executemany("UPDATE job SET extracted_version = ? WHERE id = ?",
                             [(p.version, job_id) for job_id in p.carry])
    return p
