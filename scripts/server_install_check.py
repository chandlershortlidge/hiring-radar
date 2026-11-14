"""Can the app run on the packages the server gets, and only those? (HIR-234)

The server installs the smaller set (`uv sync --frozen --no-dev`); the automated tests
install the developer-only group as well. So a package the app needs at run time can sit
in the developer-only group and every test stays green, while the server does not have
it. That is how HIR-233 happened: the tracing package was developer-only, and the first
traced daily poll on the VM crashed.

This script is meant to be run by a Python that has ONLY the server's install set.
tests/test_server_install_set.py builds that install in a throwaway folder and runs this
file with it, so the check is part of the ordinary test run:

    UV_PROJECT_ENVIRONMENT=/tmp/server-venv uv sync --frozen --no-dev
    /tmp/server-venv/bin/python scripts/server_install_check.py

Does, in order:
  1. Reads every Python file under app/ and scripts/ and collects each third-party module
     it imports, including the ones imported inside a function and the ones imported by
     name (`importlib.import_module("langsmith")`). Those late imports are the point: the
     model client, the tracing package and the web server are all imported only when
     first used, so merely importing the app would never notice one missing.
  2. Imports each of those modules. One that cannot be imported is a failure. So is one
     that imports but whose package is not in the project's own dependency list: it is on
     the server only because some other package happens to need it today.
  3. Imports every module of the app.
  4. Runs the real `poll` command on a throwaway database: one made-up job from a made-up
     feed, read through a stand-in for the model client.
  5. Builds the API on that database and asks it for the job.

Does NOT: call a model, reach the network, send anything to LangSmith, or touch the real
database. It needs nothing but the standard library until step 2, and uses no test
library at all, because the server's install set has none.

Exit 0 when everything works, 1 with one line per failure otherwise.
"""

import ast
import importlib
import os
import pkgutil
import re
import sys
import tempfile
import tomllib
import traceback
from importlib import metadata
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent

# Where run-time code lives. scripts/ counts: several are run against the live database.
SCANNED_DIRS = ("app", "scripts")

# Functions whose first argument is a module name to import.
IMPORT_BY_NAME = {"import_module", "_module", "__import__"}

# Set before the app is imported, and never overridden by a developer's .env (python-dotenv
# leaves a variable alone when it is already set, even to nothing): no test run of this
# check may trace to the real LangSmith account or log in to the server.
QUIET_ENV = {
    "LANGSMITH_API_KEY": "", "LANGCHAIN_API_KEY": "", "LANGSMITH_TRACING": "false",
    "LANGCHAIN_TRACING_V2": "false", "HIRING_RADAR_SEND_CHECKS": "0",
    "ANTHROPIC_API_KEY": "not-a-real-key",
}


def _is_ours(top: str, root: Path) -> bool:
    """A module of this repository rather than an installed package."""
    return ((root / top).is_dir() or (root / f"{top}.py").exists()
            or any((root / d / f"{top}.py").exists() for d in SCANNED_DIRS))


def _imported_names(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.module
        elif isinstance(node, ast.Call) and node.args:
            fn = node.func
            name = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", None)
            arg = node.args[0]
            if name in IMPORT_BY_NAME and isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                yield arg.value


def third_party_imports(root: Path = ROOT) -> dict[str, str]:
    """Pure apart from reading files: every installed-package module the run-time code
    imports, mapped to the first file that imports it. Standard-library modules and this
    repository's own are left out."""
    found: dict[str, str] = {}
    for d in SCANNED_DIRS:
        for path in sorted((root / d).rglob("*.py")):
            tree = ast.parse(path.read_text(), filename=str(path))
            for name in _imported_names(tree):
                top = name.split(".")[0]
                if top in sys.stdlib_module_names or _is_ours(top, root):
                    continue
                found.setdefault(name, str(path.relative_to(root)))
    return found


def unimportable(names) -> dict[str, str]:
    """The modules among `names` this Python cannot import, each with the reason."""
    failed = {}
    for name in sorted(names):
        try:
            importlib.import_module(name)
        except Exception as e:  # noqa: BLE001 - a package that breaks on import is as absent as a missing one
            failed[name] = f"{type(e).__name__}: {e}"
    return failed


def _normal(dist: str) -> str:
    """A package name as the index compares them: `Python_Dotenv` is `python-dotenv`."""
    return re.sub(r"[-_.]+", "-", dist).lower()


def declared_dependencies(root: Path = ROOT) -> set[str]:
    """The packages pyproject.toml lists as the project's own run-time dependencies."""
    deps = tomllib.loads((root / "pyproject.toml").read_text())["project"]["dependencies"]
    return {_normal(re.match(r"[A-Za-z0-9._-]+", d).group(0)) for d in deps}


def undeclared(names, declared: set[str], providers: dict[str, list[str]] | None = None) -> dict[str, list[str]]:
    """The modules among `names` that are installed but come from no declared dependency,
    each with the packages that do provide it. `providers` maps a top-level module to the
    installed packages that ship it; the default asks this Python.

    Moving `python-dotenv` to the developer-only group leaves it on the server, because
    the web server's extras need it too. The app would keep working by coincidence, until
    that other package drops it. A module nobody provides is `unimportable`'s to report.
    """
    providers = providers if providers is not None else metadata.packages_distributions()
    found = {}
    for name in sorted(names):
        dists = sorted({_normal(d) for d in providers.get(name.split(".")[0], [])})
        if dists and not declared & set(dists):
            found[name] = dists
    return found


def _attempt(what: str, fn, *args) -> list[str]:
    """Run one step; a crash is a failure line, with the traceback above it."""
    try:
        return fn(*args)
    except (Exception, SystemExit) as e:  # noqa: BLE001 - whatever stops the app is what this reports
        traceback.print_exc()
        return [f"{what} crashed: {type(e).__name__}: {str(e)[:300]}"]


def import_the_app() -> dict[str, str]:
    import app
    return unimportable(m.name for m in pkgutil.walk_packages(app.__path__, "app."))


class FakeAnthropic:
    """Stands in for `anthropic.Anthropic`: answers the one Batch API submission the poll
    makes with a canned reading, and counts the submissions. No network."""

    submissions = 0

    def __init__(self, *a, **kw):
        self.messages = SimpleNamespace(batches=self)
        self._requests = []

    def create(self, requests):
        type(self).submissions += 1
        self._requests = requests
        return SimpleNamespace(id="batch_1", processing_status="ended")

    def retrieve(self, batch_id):
        return SimpleNamespace(id=batch_id, processing_status="ended")

    def results(self, batch_id):
        block = SimpleNamespace(type="tool_use", name="record_skills", input={"skills": [
            {"skill_id": "python", "requirement": "required", "raw_text": "Python"}]})
        message = SimpleNamespace(stop_reason="tool_use", content=[block], usage=SimpleNamespace(
            input_tokens=10, output_tokens=5, cache_read_input_tokens=0, cache_creation_input_tokens=0))
        return [SimpleNamespace(custom_id=r["custom_id"], result=SimpleNamespace(type="succeeded", message=message))
                for r in self._requests]


def tiny_poll(db_path: Path) -> list[str]:
    """The real `python -m app poll`, with the feed list, the fetch and the model client
    replaced. Returns what went wrong, as plain lines."""
    import anthropic
    import app.__main__ as cli
    from app import db
    from app.sources import Posting, registry

    posting = Posting("arbeitnow", "check-1", "https://example.com/check-1", "Check GmbH",
                      "AI Engineer", "Berlin", "We need an AI Engineer who writes Python every day.")
    real = (cli.load_feeds, cli.DB_PATH, registry.fetch, anthropic.Anthropic)
    cli.load_feeds = lambda: [{"type": "arbeitnow"}]
    cli.DB_PATH = db_path
    registry.fetch = lambda feed: [posting]
    anthropic.Anthropic = FakeAnthropic
    try:
        cli.main(["poll"])
    finally:
        cli.load_feeds, cli.DB_PATH, registry.fetch, anthropic.Anthropic = real

    problems = []
    conn = db.connect(db_path)
    jobs = conn.execute("SELECT count(*) FROM job WHERE extracted_version IS NOT NULL").fetchone()[0]
    mentions = conn.execute("SELECT count(*) FROM skill_mention").fetchone()[0]
    conn.close()
    if jobs != 1:
        problems.append(f"the poll stored and read {jobs} jobs, expected 1")
    if mentions != 1:
        problems.append(f"the poll stored {mentions} skills, expected 1")
    if FakeAnthropic.submissions != 1:
        problems.append(f"the poll submitted {FakeAnthropic.submissions} batches to the stand-in client, expected 1")
    return problems


def _get(app, path: str) -> tuple[int, bytes]:
    """One GET against the ASGI app, by hand: the test client needs httpx, which the
    server's install set does not have."""
    import asyncio

    sent = []
    scope = {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1", "method": "GET",
             "path": path, "raw_path": path.encode(), "query_string": b"", "headers": [],
             "scheme": "http", "server": ("check", 80), "client": ("127.0.0.1", 1), "root_path": ""}

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    asyncio.run(app(scope, receive, send))
    status = next(m["status"] for m in sent if m["type"] == "http.response.start")
    return status, b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")


def start_the_api(db_path: Path) -> list[str]:
    from app.api import create_app

    app = create_app(db_path)
    problems = []
    for path in ("/api/stats", "/api/skills", "/api/jobs"):
        status, body = _get(app, path)
        if status != 200:
            problems.append(f"GET {path} answered {status}: {body[:200]!r}")
        elif path == "/api/jobs" and b"Check GmbH" not in body:
            problems.append("GET /api/jobs does not list the job the poll just stored")
    return problems


def main() -> int:
    os.environ.update(QUIET_ENV)
    sys.path.insert(0, str(ROOT))
    wanted = third_party_imports()
    problems = [f"{where} imports {name}, which this install cannot import ({why})"
                for name, why in unimportable(wanted).items() for where in [wanted[name]]]
    problems += [f"{wanted[name]} imports {name} from the package {' / '.join(dists)}, which is not in "
                 f"pyproject.toml's dependencies; it is installed only because another package needs it"
                 for name, dists in undeclared(wanted, declared_dependencies()).items()]
    problems += [f"{name} cannot be imported ({why})" for name, why in import_the_app().items()]
    if not problems:  # a poll on a broken install would only repeat the lines above
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "check.db"
            problems += _attempt("the poll", tiny_poll, db_path)
            problems += _attempt("starting the API", start_the_api, db_path)
    if problems:
        print("This install set cannot be relied on to run the app:")
        for p in problems:
            print(f"  - {p}")
        print("If this is the server's set (`uv sync --frozen --no-dev`), a package the app "
              "needs is probably in the developer-only group in pyproject.toml.")
        return 1
    print(f"ok: {len(wanted)} third-party modules import, the app imports, a poll stored and "
          f"read one job, and the API listed it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
