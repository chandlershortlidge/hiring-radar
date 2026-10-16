"""One-off: seed taxonomy/skills.json and evals/goldens/ from the legacy job-skills-dashboard repo.

Usage:
    uv run python scripts/seed_from_legacy.py /path/to/job-skills-dashboard

What it does:
  - Builds skills.json from three legacy sources: the generated alias map
    (dashboard/public/canonical_map.json), every canonical named in the 20 Golden
    fixtures, and the directional implications in dashboard/src/skillImplications.js
    (which become `parents`).
  - Converts each Golden into the slim contract: JD text + expected
    {raw_text, skill_id, requirement}. Non-skill mentions and alternative groups
    are dropped (DECISIONS 2026-10-16).

What it does NOT do: call any model, judge which seed entries are real technical
skills (every entry is written with reviewed=false for a human pass), or read
anything outside the legacy repo path it is given.

Invariant: deterministic — same legacy input, byte-identical output.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Display names that differ only by case but are different skills. Without this,
# case-insensitive merging would fold the ReAct agent pattern into the React framework.
CASE_SENSITIVE_DISPLAYS = {"ReAct", "React"}
ID_OVERRIDES = {"ReAct": "react-agent-pattern", "React": "react", "C#": "csharp", "C++": "cpp"}


def slug(display: str) -> str:
    if display in ID_OVERRIDES:
        return ID_OVERRIDES[display]
    s = display.lower().replace("&", " and ").replace("+", " plus ").replace("#", " sharp ")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def load_implications(path: Path) -> dict[str, list[str]]:
    """Parse `Key: Object.freeze(['A', 'B'])` lines from the legacy JS module."""
    out = {}
    pat = re.compile(r"^\s*(?:'([^']+)'|([A-Za-z0-9_]+)):\s*Object\.freeze\(\[([^\]]*)\]\)")
    for line in path.read_text().splitlines():
        m = pat.match(line)
        if m:
            key = m.group(1) or m.group(2)
            out[key] = re.findall(r"'([^']+)'", m.group(3))
    return out


def load_goldens(legacy: Path) -> list[dict]:
    rows = []
    for p in sorted((legacy / "evals").glob("golden_*.jsonl")):
        rows.append(json.loads(p.read_text().splitlines()[0]))
    return rows


def build_taxonomy(legacy: Path, goldens: list[dict]):
    cmap = json.loads((legacy / "dashboard/public/canonical_map.json").read_text())
    alias_to_display = dict(cmap["map"])
    implications = load_implications(legacy / "dashboard/src/skillImplications.js")

    # Golden spellings win display ties, since they are the most-reviewed labels.
    golden_displays = []
    for g in goldens:
        for s in g["expected_extraction"]["technical_skills"]:
            golden_displays.append(s["canonical"])

    displays = list(dict.fromkeys(
        golden_displays
        + sorted(set(alias_to_display.values()))
        + sorted(set(implications) | {p for ps in implications.values() for p in ps})
    ))

    # Merge case-only variants (e.g. "Prompt Engineering" vs "Prompt engineering").
    by_fold: dict[str, str] = {}
    merged_into: dict[str, str] = {}
    for d in displays:
        key = d if d in CASE_SENSITIVE_DISPLAYS else d.lower()
        if key in by_fold:
            merged_into[d] = by_fold[key]
        else:
            by_fold[key] = d
    canon = lambda d: merged_into.get(d, d)

    entries: dict[str, dict] = {}
    for d in by_fold.values():
        sid = slug(d)
        if sid in entries:
            raise SystemExit(f"id collision: {d!r} and {entries[sid]['display']!r} -> {sid}")
        entries[sid] = {"id": sid, "display": d, "aliases": [], "parents": [], "reviewed": False}
    display_to_id = {e["display"]: e["id"] for e in entries.values()}

    for alias, d in alias_to_display.items():
        e = entries[display_to_id[canon(d)]]
        if alias != e["display"].lower() and alias not in e["aliases"]:
            e["aliases"].append(alias)
    for d, target in merged_into.items():
        e = entries[display_to_id[target]]
        if d.lower() not in e["aliases"] and d.lower() != e["display"].lower():
            e["aliases"].append(d.lower())
    for child, parents in implications.items():
        e = entries[display_to_id[canon(child)]]
        for p in parents:
            pid = display_to_id[canon(p)]
            if pid not in e["parents"]:
                e["parents"].append(pid)

    for e in entries.values():
        e["aliases"].sort()
        e["parents"].sort()
    skills = sorted(entries.values(), key=lambda e: e["id"])
    return {"version": 1, "skills": skills}, display_to_id, canon


def convert_goldens(goldens, display_to_id, canon):
    out = []
    for g in goldens:
        seen = {}
        for s in g["expected_extraction"]["technical_skills"]:
            sid = display_to_id[canon(s["canonical"])]
            # One criterion per skill per JD; any required mention wins (DECISIONS legacy 2026-08-29).
            prev = seen.get(sid)
            if prev is None or (prev["requirement"] != "required" and s["requirement"] == "required"):
                seen[sid] = {"skill_id": sid, "requirement": s["requirement"], "raw_text": s["raw_text"]}
        out.append({
            "id": g["id"],
            "split": "dev",
            "source_sha256": g["source_sha256"],
            "job_description": g["job_description"],
            "expected": sorted(seen.values(), key=lambda x: x["skill_id"]),
        })
    return out


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 1
    legacy = Path(argv[1]).resolve()
    goldens = load_goldens(legacy)
    taxonomy, display_to_id, canon = build_taxonomy(legacy, goldens)

    tax_path = ROOT / "taxonomy/skills.json"
    tax_path.parent.mkdir(parents=True, exist_ok=True)
    tax_path.write_text(json.dumps(taxonomy, indent=2, ensure_ascii=False) + "\n")

    gdir = ROOT / "evals/goldens"
    gdir.mkdir(parents=True, exist_ok=True)
    converted = convert_goldens(goldens, display_to_id, canon)
    for g in converted:
        (gdir / f"{g['id']}.json").write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n")

    n_expected = sum(len(g["expected"]) for g in converted)
    print(f"skills.json: {len(taxonomy['skills'])} skills")
    print(f"goldens: {len(converted)} files, {n_expected} expected skill criteria")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
