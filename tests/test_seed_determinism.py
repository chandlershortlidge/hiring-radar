"""The seed script was a one-off whose output has since been hand-edited (taxonomy v2,
Golden realignment), so its output no longer matches the committed files and must never
overwrite them. This guards only that the script is still deterministic, in a temp copy.

Skipped when the legacy repo is not checked out next to this one.
"""

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LEGACY = Path(os.environ.get("LEGACY_REPO", ROOT.parent / "job-skills-dashboard"))


def _real_digest() -> str:
    h = hashlib.sha256()
    for p in [ROOT / "taxonomy/skills.json", *sorted((ROOT / "evals/goldens").glob("golden_*.json"))]:
        h.update(p.read_bytes())
    return h.hexdigest()


def _run_in(tmp: Path) -> str:
    scripts = tmp / "scripts"
    scripts.mkdir(parents=True)
    shutil.copy(ROOT / "scripts/seed_from_legacy.py", scripts / "seed_from_legacy.py")
    subprocess.run([sys.executable, str(scripts / "seed_from_legacy.py"), str(LEGACY)],
                   check=True, capture_output=True, env={**os.environ, "PYTHONHASHSEED": "random"})
    h = hashlib.sha256()
    for p in [tmp / "taxonomy/skills.json", *sorted((tmp / "evals/goldens").glob("golden_*.json"))]:
        h.update(p.read_bytes())
    return h.hexdigest()


@pytest.mark.skipif(not (LEGACY / "evals").exists(), reason="legacy repo not available")
def test_seed_script_is_deterministic(tmp_path):
    before = _real_digest()
    a = _run_in(tmp_path / "a")
    b = _run_in(tmp_path / "b")
    assert a == b
    assert _real_digest() == before  # it never touched the real files
