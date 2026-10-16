"""The skill taxonomy: load taxonomy/skills.json, validate it, and resolve labels to skill ids.

Does: validate the file's structure (unique ids, unique aliases across skills, parents
that exist, no parent cycles), resolve a free-text label to a skill id via display name
or alias, and expand a skill to its ancestors.

Does NOT: call a model, decide what counts as a skill, write to the file, or touch the
database. New skills arrive through the proposed_skill review queue and a human edit.

Invariants: resolution is exact after case-folding and whitespace trimming, except for
display names listed in CASE_SENSITIVE (where case carries meaning, e.g. ReAct vs React);
an unknown label resolves to None, never to a guess.
"""

import json
from dataclasses import dataclass
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "taxonomy" / "skills.json"
CASE_SENSITIVE = {"ReAct", "React"}


@dataclass(frozen=True)
class Skill:
    id: str
    display: str
    aliases: tuple[str, ...]
    parents: tuple[str, ...]
    reviewed: bool


class TaxonomyError(ValueError):
    pass


class Taxonomy:
    def __init__(self, data: dict):
        self.version: int = data["version"]
        self.skills: dict[str, Skill] = {}
        for raw in data["skills"]:
            s = Skill(raw["id"], raw["display"], tuple(raw.get("aliases", [])),
                      tuple(raw.get("parents", [])), bool(raw.get("reviewed", False)))
            if s.id in self.skills:
                raise TaxonomyError(f"duplicate id: {s.id}")
            self.skills[s.id] = s

        self._exact: dict[str, str] = {}
        self._folded: dict[str, str] = {}
        for s in self.skills.values():
            if s.display in CASE_SENSITIVE:
                self._add(self._exact, s.display, s.id)
            else:
                self._add(self._folded, s.display.strip().lower(), s.id)
            for a in s.aliases:
                self._add(self._folded, a.strip().lower(), s.id)
            for p in s.parents:
                if p not in self.skills:
                    raise TaxonomyError(f"{s.id}: unknown parent {p}")
        for sid in self.skills:
            self.ancestors(sid)  # raises on cycles

    @staticmethod
    def _add(index: dict, key: str, sid: str):
        if key in index and index[key] != sid:
            raise TaxonomyError(f"label {key!r} maps to both {index[key]} and {sid}")
        index[key] = sid

    @classmethod
    def load(cls, path: Path = DEFAULT_PATH) -> "Taxonomy":
        return cls(json.loads(Path(path).read_text()))

    def resolve(self, label: str) -> str | None:
        label = label.strip()
        if label in self._exact:
            return self._exact[label]
        return self._folded.get(label.lower())

    def ancestors(self, sid: str) -> set[str]:
        out: set[str] = set()
        stack = [(sid, (sid,))]
        while stack:
            cur, path = stack.pop()
            for p in self.skills[cur].parents:
                if p in path:
                    raise TaxonomyError(f"parent cycle: {' -> '.join(path + (p,))}")
                if p not in out:
                    out.add(p)
                    stack.append((p, path + (p,)))
        return out
