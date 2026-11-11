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
    """(all names to look for, the skill ids they belong to); None means a full re-read."""
    by_id = added_skills(old, new)
    if by_id is None:
        return None
    return [n for names in by_id.values() for n in names], list(by_id)


def added_skills(old: Snapshot, new: Snapshot) -> dict[str, list[str]] | None:
    """{skill id: names to look for} when `new` only *adds* to `old` — every id, display
    name and alias of a new skill, and each alias added to an existing one. None when
    anything else differs, which means a full re-read. Pure."""
    if old.core != new.core:
        return None
    out: dict[str, list[str]] = {}
    for sid, (display, aliases) in old.skills.items():
        if sid not in new.skills:
            return None                       # removed
        new_display, new_aliases = new.skills[sid]
        if new_display != display or not set(aliases) <= set(new_aliases):
            return None                       # renamed, or a spelling taken away
        extra = [a for a in new_aliases if a not in aliases]
        if extra:
            out[sid] = extra
    for sid in sorted(new.skills.keys() - old.skills.keys()):
        display, aliases = new.skills[sid]
        out[sid] = [sid, sid.replace("-", " "), display, *aliases]
    return out


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
    # Re-read only because the model had already suggested an added skill for the job,
    # in words the text match missed (HIR-224, Chandler 11 Nov).
    by_suggestion: list[int] = field(default_factory=list)
    # {added skill id: spellings from the suggestion queue that are not yet one of its
    # names} — offered as aliases in the PR, never added by themselves.
    offers: dict[str, list[str]] = field(default_factory=dict)

    @property
    def stale(self) -> int:
        return len(self.carry) + len(self.reread)


def plan(conn: sqlite3.Connection, tax: Taxonomy, model: str,
         snapshots: dict[str, Snapshot], now: str | None = None) -> Plan:
    """Sort the queue's stale-stamped open jobs into carry-over and re-read. Reads only.

    A job under a stamp the current list only adds to is re-read when its text names an
    added skill, or when the model had already suggested one of them for it (a pending
    row in the suggestion queue), whatever words the posting used."""
    from app.pipeline import _pending_clause  # the queue's one definition (HIR-221)
    current = snapshot(tax, model)
    out = Plan(current.version)
    where, params = _pending_clause(current.version, now)
    rows = conn.execute(
        f"SELECT id, extracted_version, title, description_text FROM job j"
        f" WHERE {where} AND j.extracted_version IS NOT NULL ORDER BY id", params).fetchall()
    suggestions = _suggestions_by_job(conn)
    # Per stamp: None = no targeted path (full re-read); else {added id: its pattern}.
    per_stamp: dict[str, dict[str, re.Pattern] | None] = {}
    added: dict[str, re.Pattern] = {}
    for r in rows:
        stamp = r["extracted_version"]
        if stamp not in per_stamp:
            old = snapshots.get(stamp)
            by_id = added_skills(old, current) if old else None
            per_stamp[stamp] = None if by_id is None else {
                sid: pat for sid, names in by_id.items() if (pat := names_pattern(names))}
            added.update(per_stamp[stamp] or {})
        pats = per_stamp[stamp]
        if pats is None:
            out.reread.append(r["id"])
            continue
        text = _norm(extraction_input(r["title"], r["description_text"]))
        if any(p.search(text) for p in pats.values()):
            out.reread.append(r["id"])
        elif any(_owner(label, tax, pats) for label, _ in suggestions.get(r["id"], [])):
            out.reread.append(r["id"])
            out.by_suggestion.append(r["id"])
        else:
            out.carry.append(r["id"])
    out.added_ids = sorted(added)
    out.offers = _offers(suggestions, tax, added)
    return out


# A quote longer than this is a sentence from the posting, not a spelling worth offering.
OFFER_MAX_CHARS = 40


def _suggestions_by_job(conn: sqlite3.Connection) -> dict[int, list[tuple[str, str]]]:
    """Every pending suggestion in the queue: {job id: [(label, quoted posting words)]}."""
    out: dict[int, list[tuple[str, str]]] = {}
    for r in conn.execute("SELECT job_id, label, raw_text FROM proposed_skill WHERE status = 'pending'"):
        out.setdefault(r[0], []).append((r[1] or "", r[2] or ""))
    return out


def _owner(label: str, tax: Taxonomy, patterns: dict[str, re.Pattern]) -> str | None:
    """Which added skill a suggested label is, if any: the new skill list resolves it to
    one, or it contains one of an added skill's names ("Ruby on Rails 7" for Ruby on Rails)."""
    sid = tax.resolve(label)
    if sid in patterns:
        return sid
    for sid, pat in patterns.items():
        if pat.search(_norm(label)):
            return sid
    return None


def _offers(suggestions: dict, tax: Taxonomy, added: dict[str, re.Pattern]) -> dict[str, list[str]]:
    """Spellings to offer as aliases: the model's own label and quote, across the whole
    queue, for every pending suggestion of an added skill — short ones only, and only those
    that contain none of the skill's names: "react oder angular" adds nothing an Angular
    entry does not already catch, "ng" would."""
    offers: dict[str, set[str]] = {}
    for items in suggestions.values():
        for label, raw in items:
            sid = _owner(label, tax, added)
            if sid is None:
                continue
            for word in (label, raw):
                w = _norm(word).lower()
                if w and len(w) <= OFFER_MAX_CHARS and tax.resolve(w) is None \
                        and not added[sid].search(w):
                    offers.setdefault(sid, set()).add(w)
    return {sid: sorted(ws) for sid, ws in sorted(offers.items())}


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
