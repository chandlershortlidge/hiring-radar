"""Send the dashboard server's errors to Sentry, with no visitor details (HIR-259).

Does: start the Sentry SDK when `SENTRY_DSN` is set, so an unhandled error in a request
becomes one grouped entry in Sentry (decisions/2026-11-25-hir-259-errors-go-to-sentry.md).

Does NOT: send anything when the key is absent; trace requests, profile, or keep logs;
collect who the visitor is (address, cookies, headers, request bodies, query strings,
local variables, MCP tool inputs and outputs). The browser side is web/src/errorReports.js.
"""

import os

# Every automatic collection category that could carry a visitor detail, switched off.
DATA_COLLECTION = {
    "user_info": False,
    "cookies": {"mode": "off"},
    "http_headers": {"request": {"mode": "off"}},  # X-Forwarded-For holds the visitor's address
    "http_bodies": [],
    "url_query_params": {"mode": "off"},
    "stack_frame_variables": False,
    "mcp": {"inputs": False, "outputs": False},
    "gen_ai": {"inputs": False, "outputs": False},
    "graphql": {"document": False, "variables": False},
    "database_query_data": False,
}


def scrub(event: dict, _hint: dict | None = None) -> dict:
    """The last filter before an event leaves: no user block, no query string, no
    headers, cookies, body or client address, whatever an integration added."""
    event.pop("user", None)
    req = event.get("request")
    if isinstance(req, dict):
        for k in ("query_string", "cookies", "headers", "data", "env"):
            req.pop(k, None)
        if isinstance(req.get("url"), str):
            req["url"] = req["url"].split("?", 1)[0]
    event.pop("server_name", None)
    return event


def options(dsn: str) -> dict:
    return {
        "dsn": dsn,
        "data_collection": DATA_COLLECTION,
        "before_send": scrub,
        "traces_sample_rate": None,
        "auto_session_tracking": False,
        "server_name": "",
        "max_request_body_size": "never",
    }


def start(env: dict | None = None) -> bool:
    """Start Sentry if the key is set. Returns whether it started."""
    dsn = (env if env is not None else os.environ).get("SENTRY_DSN", "").strip()
    if not dsn:
        return False
    import sentry_sdk

    sentry_sdk.init(**options(dsn))
    return True
