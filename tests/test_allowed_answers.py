"""The allowed answers are one list each, and the database agrees with it (HIR-311).

Seniority, degree level, required / nice-to-have and job family are each a short list of
allowed values. The model's form (app/extract.py) and the title rules (app/ingest.py) own
those lists; the database has its own copy in a CHECK on each column, because a migration
is SQL and cannot read Python. Nothing but a test can catch a value added to the list and
not to the CHECK, and without one the first job carrying the new value fails to store, in
production, and is retried (and billed) at every poll.

Same shape as the job-source test in tests/test_sources_registry.py.
"""

import importlib.util
import re
import sqlite3
from pathlib import Path

import pytest

from app import db, extract, ingest, queries

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("agent_label", ROOT / "scripts" / "agent_label.py")
agent_label = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agent_label)

# (table, column, the one list of answers allowed in it). Read at call time through
# `_columns()` so a test can show the check failing on a changed list.
def _columns():
    return [
        ("job", "seniority", extract.SENIORITY_LEVELS),
        ("job", "degree", extract.DEGREE_LEVELS),
        ("job", "degree_requirement", extract.REQUIREMENT_LEVELS),
        ("job", "german", extract.REQUIREMENT_LEVELS),
        ("job", "production", extract.REQUIREMENT_LEVELS),
        ("skill_mention", "requirement", extract.REQUIREMENT_LEVELS),
        ("job", "family", ingest.FAMILIES),
    ]


IDS = [f"{t}.{c}" for t, c, _ in _columns()]


@pytest.fixture
def conn(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    return c


def _check_values(conn, table: str, column: str) -> set[str]:
    """The values the database actually allows in a column, read from its own schema."""
    sql = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()[0]
    m = re.search(rf"CHECK\s*\(\s*{column}\s+IN\s*\((.*?)\)\s*\)", sql, re.S)
    assert m, f"no CHECK ({column} IN ...) found in the {table} schema:\n{sql}"
    return set(re.findall(r"'([^']*)'", m.group(1)))


def _mismatches(conn) -> list[str]:
    """One line per column whose database rule and Python list disagree."""
    out = []
    for table, column, allowed in _columns():
        stored = _check_values(conn, table, column)
        if stored != set(allowed):
            out.append(f"{table}.{column}: the database allows {sorted(stored)}, the code allows {sorted(allowed)}"
                       " (a new value needs a migration that rebuilds the column's CHECK)")
    return out


def test_every_list_matches_its_database_check(conn):
    """Add a value to a list and forget the migration, and this fails, naming the column."""
    assert _mismatches(conn) == []


@pytest.mark.parametrize("module, name, columns", [
    (extract, "SENIORITY_LEVELS", ["job.seniority"]),
    (extract, "DEGREE_LEVELS", ["job.degree"]),
    (extract, "REQUIREMENT_LEVELS",
     ["job.degree_requirement", "job.german", "job.production", "skill_mention.requirement"]),
    (ingest, "FAMILIES", ["job.family"]),
])
def test_one_extra_value_fails_and_names_the_column(conn, monkeypatch, module, name, columns):
    """The check above does fail when a list gains a value the database does not have."""
    monkeypatch.setattr(module, name, getattr(module, name) + ("intern",))
    found = _mismatches(conn)
    assert [line.split(":")[0] for line in found] == columns
    assert all("'intern'" in line for line in found)


def _insert(conn, table: str, column: str, value: str) -> None:
    if table == "job":
        conn.execute(f"INSERT INTO job (description_text, first_seen, last_seen, {column}) VALUES ('x','t','t',?)",
                     (value,))
    else:
        job_id = conn.execute("INSERT INTO job (description_text, first_seen, last_seen) "
                              "VALUES ('x','t','t')").lastrowid
        conn.execute("INSERT INTO skill_mention (job_id, skill_id, requirement, raw_text, taxonomy_version,"
                     " extractor_version) VALUES (?, 's', ?, 'r', 1, 'v')", (job_id, value))


@pytest.mark.parametrize("table, column, allowed", _columns(), ids=IDS)
def test_every_allowed_value_can_be_stored(conn, table, column, allowed):
    """The CHECK read above is the real constraint: each value inserts without error."""
    for value in allowed:
        _insert(conn, table, column, value)
    stored = {r[0] for r in conn.execute(f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL")}
    assert stored == set(allowed)


@pytest.mark.parametrize("table, column, allowed", _columns(), ids=IDS)
def test_a_value_outside_the_list_is_still_refused(conn, table, column, allowed):
    with pytest.raises(sqlite3.IntegrityError):
        _insert(conn, table, column, "not_an_answer")


def test_the_form_the_model_fills_in_offers_exactly_these_lists():
    """The form's own choices are written out in app/extract.py; this ties them to the
    lists, so the form cannot offer a value the lists (and so the database) do not have."""
    props = extract.TOOL["input_schema"]["properties"]

    def choices(schema) -> set[str]:
        found = set(schema.get("enum") or [])
        for option in schema.get("anyOf", []):
            found |= set(option.get("enum") or [])
        return {v for v in found if v is not None}

    assert choices(props["skills"]["items"]["properties"]["requirement"]) == set(extract.REQUIREMENT_LEVELS)
    assert choices(props["seniority"]) == set(extract.SENIORITY_LEVELS)
    assert choices(props["degree"]) == set(extract.DEGREE_LEVELS)
    for attr in ("german", "degree_requirement", "production"):
        assert choices(props[attr]) == set(extract.REQUIREMENT_LEVELS), attr


def test_filter_and_labelling_tool_read_the_one_list():
    """The server's filter list and the labelling tool hold the form's lists, not copies."""
    assert queries.SENIORITIES is extract.SENIORITY_LEVELS
    assert queries.FAMILIES is ingest.FAMILIES
    assert agent_label.SENIORITIES is extract.SENIORITY_LEVELS
    assert agent_label.DEGREES is extract.DEGREE_LEVELS
    assert agent_label.REQUIREMENTS is extract.REQUIREMENT_LEVELS
