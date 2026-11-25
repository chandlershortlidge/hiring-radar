"""The server's error reports to Sentry (HIR-259): off without a key, and an error from a
real request leaves with no visitor details (decisions/2026-11-25-hir-259-errors-go-to-sentry.md)."""

import pytest
import sentry_sdk
from fastapi.testclient import TestClient
from sentry_sdk.transport import Transport

from app import db, error_reports
from app.api import create_app
from tests.test_api import TAX

DSN = "https://public@o1.ingest.de.sentry.io/1"


class Capture(Transport):
    events: list = []

    def capture_envelope(self, envelope):
        for item in envelope.items:
            if item.type == "event":
                Capture.events.append(item.payload.json)


@pytest.fixture
def sentry():
    Capture.events = []
    sentry_sdk.init(**error_reports.options(DSN), transport=Capture)
    yield Capture.events
    sentry_sdk.get_client().close()
    sentry_sdk.init()  # back to a client that sends nothing


def test_no_key_starts_nothing():
    assert error_reports.start({}) is False
    assert error_reports.start({"SENTRY_DSN": "  "}) is False


def test_options_switch_off_every_visitor_detail():
    o = error_reports.options(DSN)
    dc = o["data_collection"]
    assert dc["user_info"] is False and dc["http_bodies"] == [] and dc["stack_frame_variables"] is False
    assert dc["cookies"]["mode"] == dc["url_query_params"]["mode"] == dc["http_headers"]["request"]["mode"] == "off"
    assert dc["mcp"] == {"inputs": False, "outputs": False}
    assert o["traces_sample_rate"] is None and o["auto_session_tracking"] is False


def test_scrub_drops_what_an_integration_added():
    e = error_reports.scrub({"user": {"ip_address": "1.2.3.4"}, "server_name": "vm",
                             "request": {"url": "https://x/api/jobs?q=me", "query_string": "q=me",
                                         "headers": {"X-Forwarded-For": "1.2.3.4"}, "cookies": {"a": "b"},
                                         "data": "note", "env": {"REMOTE_ADDR": "1.2.3.4"}}})
    assert e == {"request": {"url": "https://x/api/jobs"}}


def test_a_failing_request_is_reported_without_visitor_details(tmp_path, sentry):
    path = tmp_path / "t.db"
    c = db.connect(path)
    db.migrate(c)
    c.close()
    app = create_app(path, TAX)

    @app.post("/boom")
    def boom():
        raise RuntimeError("deliberate test error")

    client = TestClient(app, raise_server_exceptions=False, cookies={"c": "v"})
    r = client.post("/boom?q=my+search", content=b"my private note",
                    headers={"X-Forwarded-For": "203.0.113.7", "User-Agent": "test"})
    assert r.status_code == 500
    sentry_sdk.flush()

    assert len(sentry) == 1
    ev = sentry[0]
    assert ev["exception"]["values"][-1]["type"] == "RuntimeError"
    assert "user" not in ev and "server_name" not in ev
    req = ev.get("request", {})
    assert req.get("url", "").endswith("/boom")
    assert not {"query_string", "headers", "cookies", "data", "env"} & set(req)
    # Outside the code listing around each line (which quotes this test's own source).
    text = repr({k: v for k, v in ev.items() if k != "exception"})
    for detail in ("203.0.113.7", "my private note", "my+search", "my search"):
        assert detail not in text
    for frame in ev["exception"]["values"][-1]["stacktrace"]["frames"]:
        assert "vars" not in frame
