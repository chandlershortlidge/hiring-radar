"""The seed script is a one-off, but its output is committed; guard that it is reproducible.

Skipped when the legacy repo is not checked out next to this one.
"""

import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LEGACY = Path(os.environ.get("LEGACY_REPO", ROOT.parent / "job-skills-dashboard"))


def _digest():
    h = hashlib.sha256()
    for p in [ROOT / "taxonomy/skills.json", *sorted((ROOT / "evals/goldens").glob("*.json"))]:
        h.update(p.read_bytes())
    return h.hexdigest()


@pytest.mark.skipif(not (LEGACY / "evals").exists(), reason="legacy repo not available")
def test_seed_output_matches_committed_files():
    before = _digest()
    subprocess.run([sys.executable, str(ROOT / "scripts/seed_from_legacy.py"), str(LEGACY)],
                   check=True, capture_output=True, env={**os.environ, "PYTHONHASHSEED": "random"})
    assert _digest() == before
