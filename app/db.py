"""SQLite connection and schema migrations.

Does: open the database with foreign keys on, and apply any numbered SQL files in
app/migrations/ that have not been applied yet, in order, each in its own transaction.

Does NOT: define queries for jobs or skills (those live with the code that needs them),
roll migrations back, or support any database other than SQLite.

Invariants: a migration file is applied at most once; applied versions are recorded
in schema_migrations; migration files are never edited after they are committed —
changes go in a new numbered file.
"""

import re
import sqlite3
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent / "migrations"
_NAME = re.compile(r"^(\d{3})_[a-z0-9_]+\.sql$")


def connect(path: str | Path, same_thread: bool = True) -> sqlite3.Connection:
    """same_thread=False is for the HTTP layer, where a request's connection is opened and
    closed on different threadpool threads but never used concurrently."""
    conn = sqlite3.connect(path, check_same_thread=same_thread)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def pending_migrations(applied: set[int], migrations_dir: Path = MIGRATIONS_DIR) -> list[tuple[int, Path]]:
    """Pure: which migration files still need applying, in order."""
    found = []
    for p in sorted(migrations_dir.glob("*.sql")):
        m = _NAME.match(p.name)
        if not m:
            raise ValueError(f"bad migration filename: {p.name}")
        version = int(m.group(1))
        if version not in applied:
            found.append((version, p))
    versions = [v for v, _ in found]
    if len(versions) != len(set(versions)):
        raise ValueError("duplicate migration version")
    return found


def migrate(conn: sqlite3.Connection, migrations_dir: Path = MIGRATIONS_DIR) -> list[int]:
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY)")
    applied = {r[0] for r in conn.execute("SELECT version FROM schema_migrations")}
    done = []
    for version, path in pending_migrations(applied, migrations_dir):
        # One script so the schema change and its bookkeeping row commit together or not at all.
        script = f"BEGIN;\n{path.read_text()}\nINSERT INTO schema_migrations (version) VALUES ({version});\nCOMMIT;"
        try:
            conn.executescript(script)
        except Exception:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        done.append(version)
    return done
