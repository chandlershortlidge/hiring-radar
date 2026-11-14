"""The app has to run on the packages the server gets, not the ones the tests get (HIR-234).

This test run installs the developer-only group; the server does not
(`uv sync --frozen --no-dev`). A package the app needs at run time can therefore sit in the
developer-only group with every other test green — the tracing package did, and the first
traced daily poll on the VM crashed (HIR-233).

So this builds the server's install set in a throwaway folder, exactly as the deploy does,
and runs scripts/server_install_check.py with that Python: every third-party module the
run-time code imports must import, and a small poll and the API must work. The packages
come from uv's cache, which the test run's own install has just filled, so this adds about
a second, no network and no model call.

tests/test_deploy_install_set.py asks a different question of the same set: does every
package in it arrive ready-built for the server's Python (HIR-235)?
"""

import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "server_install_check.py"

sys.path.insert(0, str(ROOT / "scripts"))
import server_install_check as check  # noqa: E402

# A package of the developer-only group that code could plausibly import: the stand-in for
# "a run-time package that slipped into the wrong group".
DEV_ONLY = "httpx"


def _clean_env(**extra):
    """The environment without this test run's own virtualenv in it, so neither uv nor the
    server's Python can pick up a developer-only package by accident."""
    env = {k: v for k, v in os.environ.items()
           if k not in ("VIRTUAL_ENV", "PYTHONPATH", "PYTHONHOME", "UV_PROJECT_ENVIRONMENT")}
    return {**env, **extra}


@pytest.fixture(scope="module")
def server_python(tmp_path_factory):
    """A Python with exactly what the deploy installs. Never a skip: a check that quietly
    does not run is the gap this ticket closes."""
    uv = os.environ.get("UV") or shutil.which("uv")
    assert uv, "uv is not on PATH, so the server's install set cannot be built; run the tests with `uv run pytest`"
    venv = tmp_path_factory.mktemp("server-install") / "venv"
    done = subprocess.run([uv, "sync", "--frozen", "--no-dev"], cwd=ROOT, capture_output=True, text=True,
                          env=_clean_env(UV_PROJECT_ENVIRONMENT=str(venv)))
    assert done.returncode == 0, f"`uv sync --frozen --no-dev` failed:\n{done.stdout}\n{done.stderr}"
    return venv / "bin" / "python"


def _run(python, *args, cwd=ROOT):
    return subprocess.run([str(python), *args], cwd=cwd, capture_output=True, text=True, env=_clean_env())


def test_the_app_runs_on_the_servers_install_set(server_python):
    """Imports, a poll of one made-up job, and the API, with only the server's packages."""
    done = _run(server_python, str(CHECK))
    assert done.returncode == 0, f"{done.stdout}\n{done.stderr}"
    assert "ok:" in done.stdout


def test_the_servers_install_set_really_is_the_smaller_one(server_python):
    """If the throwaway install had the developer-only group too, the test above would
    prove nothing. This is the developer-only group as pyproject.toml declares it."""
    groups = tomllib.loads((ROOT / "pyproject.toml").read_text())["dependency-groups"]
    assert any(d.startswith(DEV_ONLY) for d in groups["dev"]), (
        f"{DEV_ONLY} is no longer developer-only; pick another package of that group for DEV_ONLY")
    assert _run(server_python, "-c", "import pytest").returncode != 0
    assert _run(server_python, "-c", f"import {DEV_ONLY}").returncode != 0


def test_a_runtime_import_of_a_developer_only_package_fails_the_check(server_python, tmp_path):
    """Proof the check can fail, on the shape of HIR-233: the import sits inside a
    function, so nothing breaks until the code path runs — except this check."""
    (tmp_path / "app").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "app" / "traced.py").write_text(
        f"import json\n\ndef on_first_traced_poll():\n    import {DEV_ONLY}\n    return {DEV_ONLY}\n")
    code = ("import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]);"
            "import server_install_check as c;"
            "print(c.unimportable(c.third_party_imports(Path(sys.argv[2]))))")
    done = _run(server_python, "-c", code, str(CHECK.parent), str(tmp_path))
    assert done.returncode == 0, done.stderr
    assert f"'{DEV_ONLY}': \"ModuleNotFoundError" in done.stdout, done.stdout


def test_the_scan_sees_imports_made_late_and_by_name():
    """The three packages the app only imports when first used. An ordinary "does the app
    import?" check passes with any of them missing; that is why the files are read."""
    found = check.third_party_imports()
    assert found["anthropic"] == "app/extract.py"             # inside make_client()
    assert found["uvicorn"] == "app/__main__.py"              # inside the serve command
    assert {"langsmith", "langsmith.wrappers"} <= set(found)  # by name, in app/langsmith_live.py
    assert not {"app", "json", "rules_gate"} & {n.split(".")[0] for n in found}


def test_the_scan_reads_names_passed_to_an_import_function(tmp_path):
    (tmp_path / "app").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "app" / "late.py").write_text(
        "import importlib\nfrom . import sibling\n"
        "def a(): return importlib.import_module('somepkg.sub')\n"
        "def b(): return _module('otherpkg')\n"
        "def c(name): return importlib.import_module(name)\n")
    assert check.third_party_imports(tmp_path) == {"somepkg.sub": "app/late.py", "otherpkg": "app/late.py"}


def test_a_package_the_server_has_only_by_coincidence_is_reported():
    """`python-dotenv` moved to the developer-only group would still reach the server,
    because the web server's extras need it. The app importing it is then luck, not a
    dependency; the check says so instead of staying green."""
    providers = {"dotenv": ["python-dotenv"], "fastapi": ["fastapi"], "yaml": ["PyYAML"]}
    declared = {"fastapi", "pyyaml"}
    assert check.undeclared(["dotenv", "fastapi.responses", "yaml", "not_installed"], declared, providers) == {
        "dotenv": ["python-dotenv"]}


def test_every_third_party_import_comes_from_a_declared_dependency():
    """The same rule on the real tree, in this (larger) install: nothing the run-time code
    imports is there only because another package needs it."""
    assert check.undeclared(check.third_party_imports(), check.declared_dependencies()) == {}


def test_declared_dependencies_are_read_without_versions_or_extras():
    declared = check.declared_dependencies()
    assert {"uvicorn", "python-dotenv", "python-multipart", "anthropic"} <= declared
    assert "pytest" not in declared and DEV_ONLY not in declared


def test_unimportable_names_what_is_missing_and_why():
    failed = check.unimportable(["json", "no_such_package_hir234"])
    assert list(failed) == ["no_such_package_hir234"]
    assert failed["no_such_package_hir234"].startswith("ModuleNotFoundError")
