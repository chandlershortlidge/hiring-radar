"""The server installs ready-made packages only — no compiler, so no building from source.

The deploy runs `uv sync --frozen --no-dev` on a VM with no C compiler, so every package
in that smaller install set has to arrive as a wheel (a package already built for this
Python and this machine). Nothing checked that before HIR-233's deploy: the project said
only "Python 3.12 or newer", the VM's installer helpfully picked 3.15 the week it came
out, two of the tracing package's dependencies had no 3.15 wheel yet, and the install died
on a missing `cc` after the backup and before the restart.

So this reads the lockfile and the Python pin as text and answers one question: if the VM
installs the server's set on the pinned Python for linux x86_64, is anything missing a
wheel? A package that would have to be compiled fails here, in a second, instead of on
the VM halfway through a deploy.

Markers are honoured only where they exclude this platform (a Windows-only dependency is
not the VM's problem). Everything else counts, which is the safe direction: at worst this
asks for a wheel the VM would not have needed.
"""

import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "hiring-radar"

# What the VM is. The deploy's install step runs here and nowhere else.
PLATFORM_TAGS = ("manylinux", "musllinux", "linux_x86_64", "any")
NOT_THIS_PLATFORM = re.compile(r"sys_platform\s*==\s*'(win32|darwin)'|platform_system\s*==\s*'(Windows|Darwin)'")


@pytest.fixture(scope="module")
def lock():
    return tomllib.loads((ROOT / "uv.lock").read_text())


@pytest.fixture(scope="module")
def pinned_python():
    """The one Python version this project runs on, everywhere: `.python-version`."""
    raw = (ROOT / ".python-version").read_text().strip()
    major, minor = raw.split(".")[:2]
    return int(major), int(minor)


def test_the_project_pins_one_python_and_forbids_the_untested_ones(pinned_python):
    """An open-ended "3.12 or newer" is what let the VM choose 3.15. The upper bound is
    the actual fix: a Python nobody has run this on cannot be picked by accident."""
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    requires = pyproject["project"]["requires-python"]
    assert "<" in requires, f"requires-python has no upper bound: {requires!r}"
    major, minor = pinned_python
    assert f">={major}.{minor}" in requires or f">={major}.12" in requires
    assert f"<{major}.{minor + 2}" in requires or f"<{major}.{minor + 1}" in requires


def _runtime_closure(lock):
    """Every package `uv sync --no-dev` would install, by name."""
    by_name = {p["name"]: p for p in lock["package"]}
    root = by_name[PROJECT]
    wanted, seen = [d["name"] for d in root.get("dependencies", [])], set()
    while wanted:
        name = wanted.pop()
        if name in seen:
            continue
        seen.add(name)
        pkg = by_name[name]
        for dep in pkg.get("dependencies", []):
            if NOT_THIS_PLATFORM.search(dep.get("marker", "")):
                continue
            wanted.append(dep["name"])
        # An extra ("uvicorn[standard]") brings its own dependencies.
        for deps in pkg.get("optional-dependencies", {}).values():
            for dep in deps:
                if NOT_THIS_PLATFORM.search(dep.get("marker", "")):
                    continue
                wanted.append(dep["name"])
    return [by_name[n] for n in sorted(seen)]


def _has_a_wheel_for(pkg, major, minor):
    """Is one of this package's wheels installable on the pinned Python, on linux?

    Three kinds count: pure Python (`py3-none-any`), a build for exactly this Python
    (`cp313-...-manylinux...`), and a stable-ABI build for this Python or older
    (`cp312-abi3-manylinux...`), which newer Pythons can use.
    """
    for wheel in pkg.get("wheels", []):
        name = wheel["url"].rsplit("/", 1)[-1]
        if not any(t in name for t in PLATFORM_TAGS):
            continue
        if re.search(r"-(py2\.)?py3-none-any\.whl$", name):
            return True
        if f"-cp{major}{minor}-cp{major}{minor}" in name:
            return True
        m = re.search(rf"-cp{major}(\d+)-abi3-", name)
        if m and int(m.group(1)) <= minor:
            return True
    return False


def test_every_package_the_server_installs_has_a_wheel_for_the_pinned_python(
        lock, pinned_python):
    """The check that would have caught HIR-235 before the deploy, not during it."""
    major, minor = pinned_python
    missing = [p["name"] for p in _runtime_closure(lock)
               if not _has_a_wheel_for(p, major, minor)]
    assert not missing, (
        f"these packages have no ready-made build for Python {major}.{minor} on linux, so "
        f"the deploy would try to compile them on a VM with no compiler: {missing}")


def test_the_check_notices_a_package_that_would_have_to_be_compiled(lock, pinned_python):
    """Proof the check can fail: zstandard's own wheels stop at 3.14, which is exactly how
    the VM's 3.15 broke the deploy."""
    major, minor = pinned_python
    zstandard = next(p for p in lock["package"] if p["name"] == "zstandard")
    assert _has_a_wheel_for(zstandard, major, minor)
    assert not _has_a_wheel_for(zstandard, 3, 15)
