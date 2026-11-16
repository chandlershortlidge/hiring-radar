"""Test-wide guarantees.

Two of them. No test ever logs in to the server: `check` ends by copying the check log
there (app/send_checks.py, HIR-294), and on a Mac with gcloud a CLI test of `check` would
do it for real, so the switch is off for every test.

And no test ever reaches LangSmith. scripts/run_eval.py calls
load_dotenv() at import, so a developer's real LANGSMITH_API_KEY is in the environment
while the suite runs, and app/langsmith_eval.enabled() would say yes — a mocked eval test
then uploads its fixture Goldens and opens an experiment in the real account. That
happened once while HIR-78 was being built. Unsetting the key for every test makes the
issue's "no test sends anything to LangSmith" an environment guarantee rather than
something each new test has to remember.
"""

import pytest

LANGSMITH_VARS = ("LANGSMITH_API_KEY", "LANGSMITH_TRACING", "LANGCHAIN_API_KEY",
                  "LANGCHAIN_TRACING_V2", "LANGSMITH_PROJECT", "LANGCHAIN_PROJECT")


@pytest.fixture(autouse=True)
def no_langsmith(monkeypatch):
    for var in LANGSMITH_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("LANGSMITH_TRACING", "false")


@pytest.fixture(autouse=True)
def no_sending_checks(monkeypatch):
    monkeypatch.setenv("HIRING_RADAR_SEND_CHECKS", "0")
