"""Every MCP tool has an example request, and every example works (HIR-366).

The robot visitor for the MCP (web/e2e/mcp-watch.spec.js) calls each tool on the live site
with its example from app/mcp_examples.json, after each deploy and every morning. A tool
without an example would go unchecked, and an example that is wrong (a misspelt argument,
an `expect` path the tool never returns) would fail on the live site and roll back a good
deploy. Both are caught here instead, before the merge: the first test fails until a new
tool has its example, the second runs every example against test data the way the robot
visitor does on the live site.

`missing` is the same rule as the spec's `missing`; the tests at the bottom pin it.
"""

import asyncio
import json
from pathlib import Path

import pytest

from app import db, mcp_server
from tests.test_api import TAX
from tests.test_mcp_server import JOBS
from tests.test_queries import NOW, add, ts

EXAMPLES_FILE = Path(mcp_server.__file__).with_name("mcp_examples.json")
EXAMPLES = {k: v for k, v in json.loads(EXAMPLES_FILE.read_text()).items() if not k.startswith("_")}

# The test data of tests/test_mcp_server.py, plus a job in every place the examples name,
# so each example has something to find, as it does on the live site. Five Munich jobs with
# python and docker give the related_skills example a skill seen in enough Python jobs to
# be listed (queries.MIN_CO_JOBS).
EXTRA = [(f"Muc{n}", "AI Engineer", "Munich", ts(1), [("python", "required"), ("docker", "required")], "mid")
         for n in range(5)]


@pytest.fixture
def server(tmp_path):
    c = db.connect(tmp_path / "t.db")
    db.migrate(c)
    for company, title, city, when, skills, seniority in JOBS + EXTRA:
        add(c, company, title, city, "greenhouse", when, skills, seniority)
    c.close()
    return mcp_server.build_server(tmp_path / "t.db", TAX, lambda: NOW)


def _empty(v) -> bool:
    return v is None or v == "" or v == 0 or v == [] or v == {}


def missing(answer, path: str) -> list[str]:
    """The parts of `path` the answer does not hold. "jobs[].title": jobs is a non-empty
    list and every item has a title. Null, zero, "" and empty lists count as missing."""
    head, _, rest = path.partition(".")
    is_list = head.endswith("[]")
    key = head[:-2] if is_list else head
    v = answer.get(key) if isinstance(answer, dict) else None
    if _empty(v):
        return [path]
    if not rest:
        return []
    if not is_list:
        return missing(v, rest)
    return [f"{key}[{i}].{m}" for i, item in enumerate(v) for m in missing(item, rest)]


def run_example(server, name: str, seen=()) -> dict:
    """Call a tool with its example's arguments, filling each {from, path} the way the spec does."""
    args = {}
    for k, v in EXAMPLES[name]["arguments"].items():
        if isinstance(v, dict) and "from" in v:
            assert v["from"] not in seen + (name,), f"{name}: examples refer to each other in a loop"
            value = run_example(server, v["from"], seen + (name,))
            for p in v["path"].split("."):
                value = value[int(p)] if isinstance(value, list) else value[p]
            args[k] = value
        else:
            args[k] = v
    result = asyncio.run(server.call_tool(name, args))
    assert result.structured_content is not None, f"{name} answered with no data"
    return result.structured_content


def test_every_tool_has_an_example_and_every_example_a_tool(server):
    tools = {t.name for t in asyncio.run(server.list_tools())}
    assert tools - EXAMPLES.keys() == set(), "add an example for each new tool to app/mcp_examples.json"
    assert EXAMPLES.keys() - tools == set(), "an example in app/mcp_examples.json names a tool the server does not have"


@pytest.mark.parametrize("name", sorted(EXAMPLES))
def test_each_example_answers_with_what_it_expects(server, name):
    ex = EXAMPLES[name]
    assert ex["ask"].strip() and ex["expect"], f"{name}: an example needs an `ask` and at least one `expect` path"
    answer = run_example(server, name)
    assert [m for p in ex["expect"] for m in missing(answer, p)] == []


# --- the `expect` rule ---------------------------------------------------------------

def test_missing_reads_plain_and_list_paths():
    answer = {"total": 2, "jobs": [{"title": "A", "places": ["Berlin"]}, {"title": "", "places": []}]}
    assert missing(answer, "total") == []
    assert missing(answer, "jobs[].title") == ["jobs[1].title"]
    assert missing(answer, "jobs[].places") == ["jobs[1].places"]
    assert missing(answer, "nope") == ["nope"]


def test_missing_counts_null_zero_and_empty_as_missing():
    assert missing({"total": 0, "jobs": []}, "total") == ["total"]
    assert missing({"total": 0, "jobs": []}, "jobs[].title") == ["jobs[].title"]
    assert missing({"degree": None}, "degree") == ["degree"]
    assert missing({"degree": {"level": "bachelor"}}, "degree.level") == []
