"""How an agent finds the MCP server from the site (HIR-480, app/discovery.py)."""

import asyncio
import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import discovery, mcp_server
from app.api import create_app
from tests.test_admin import asks_for_password
from tests.test_api import TAX

ROOT = Path(__file__).resolve().parent.parent
# The hiringradar.app site block alone: the old address forwards these pages to it.
CADDYFILE = (ROOT / "deploy" / "Caddyfile").read_text().split("www.hiringradar.app {")[0]
REGISTRY = json.loads((ROOT / "deploy" / "mcp-registry" / "server.json").read_text())


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(tmp_path / "t.db", TAX)) as c:
        yield c


def server(tmp_path):
    return mcp_server.build_server(tmp_path / "t.db", TAX, lambda: "2026-11-27T00:00:00Z", {})


def tool_names(tmp_path) -> list[str]:
    return [t.name for t in asyncio.run(server(tmp_path).list_tools())]


@pytest.mark.parametrize("path", discovery.CARD_PATHS)
def test_the_card_names_the_endpoint_and_every_tool_the_server_has(client, tmp_path, path):
    r = client.get(path)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/mcp-server-card+json")
    assert r.headers["access-control-allow-origin"] == "*"
    card = r.json()
    assert {"$schema", "name", "version", "description"} <= card.keys()     # the draft's required fields
    assert card["remotes"] == [{"type": "streamable-http", "url": "https://hiringradar.app/mcp",
                                "supportedProtocolVersions": card["remotes"][0]["supportedProtocolVersions"]}]
    meta = card["_meta"][discovery.META_KEY]
    assert [t["name"] for t in meta["tools"]] == tool_names(tmp_path)
    assert all(t["description"] for t in meta["tools"])
    assert "No sign-in" in meta["access"] and "Rate limited" in meta["access"]
    assert [r["uri"] for r in meta["resources"]] == [mcp_server.SKILLS_URI]


def test_a_tool_added_to_the_server_appears_in_the_card_and_in_llms_txt(tmp_path):
    """The files are built from the server's tool list, so a new tool needs no edit here."""
    s = server(tmp_path)

    @s.tool(annotations=mcp_server.READ_ONLY)
    def brand_new_tool() -> dict:
        """Count something new.

        Arguments go here."""
        return {}

    card = asyncio.run(discovery.server_card(s))
    assert {"name": "brand_new_tool", "description": "Count something new."} in card["_meta"][discovery.META_KEY]["tools"]
    assert "- brand_new_tool: Count something new." in asyncio.run(discovery.llms_txt(s))


def test_the_card_states_the_version_the_server_reports_when_a_client_connects(client):
    assert server(Path("/nonexistent"))._lowlevel_server.server_info.version == mcp_server.VERSION
    assert client.get(discovery.CARD_PATH).json()["version"] == mcp_server.VERSION


def test_llms_txt_names_the_endpoint_the_access_and_every_tool(client, tmp_path):
    r = client.get("/llms.txt")
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/plain")
    text = r.text
    assert text.startswith("# Hiring Radar\n")
    assert "MCP endpoint: https://hiringradar.app/mcp" in text
    assert "Streamable HTTP" in text and "No sign-in" in text
    listed = re.findall(r"^- (\w+): ", text.split("## Tools")[1].split("## Resources")[0], re.M)
    assert listed == tool_names(tmp_path)


def test_the_ai_catalog_points_to_the_card(client):
    r = client.get("/.well-known/ai-catalog.json")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/ai-catalog+json")
    [entry] = r.json()["entries"]
    assert entry["type"] == "application/mcp-server-card+json"
    assert entry["url"] == "https://hiringradar.app/mcp/server-card"


def test_the_discovery_pages_win_over_the_built_site(tmp_path, monkeypatch):
    """The live site answers any other address with the home page; these must not be."""
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<html>home</html>")
    monkeypatch.setattr("app.api.WEB_DIST", dist)
    with TestClient(create_app(tmp_path / "t.db", TAX)) as c:
        for path in discovery.OPEN_PATHS:
            assert c.get(path).text != "<html>home</html>", path
        assert c.get("/berlin").text == "<html>home</html>"


@pytest.mark.parametrize("path", discovery.OPEN_PATHS)
def test_the_web_server_answers_the_discovery_pages_without_the_password(path):
    assert not asks_for_password(CADDYFILE, path), (
        f"deploy/Caddyfile asks for the password at {path}: add it to the open `@mcp` paths")


@pytest.mark.parametrize("path", ["/", "/berlin", "/admin", "/api/stats", "/.well-known/other"])
def test_the_rest_of_the_site_still_asks_for_the_password(path):
    assert asks_for_password(CADDYFILE, path)


def test_every_answer_from_the_site_carries_a_link_to_the_card_and_llms_txt():
    [line] = [l.strip() for l in CADDYFILE.splitlines() if l.strip().startswith("header Link ")]
    assert "<https://hiringradar.app/mcp/server-card>" in line and "<https://hiringradar.app/llms.txt>" in line


def test_the_registry_entry_says_what_the_card_says(client):
    card = client.get(discovery.CARD_PATH).json()
    for key in ("name", "title", "description", "version", "websiteUrl"):
        assert REGISTRY[key] == card[key], key
    assert REGISTRY["remotes"] == [{"type": r["type"], "url": r["url"]} for r in card["remotes"]]
    assert len(REGISTRY["description"]) <= 100          # the Registry refuses a longer one
    assert re.fullmatch(r"[a-zA-Z0-9.-]+/[a-zA-Z0-9._-]+", REGISTRY["name"])
    assert REGISTRY["name"].split("/")[0] == "app.hiringradar"   # proved by the hiringradar.app domain
    assert REGISTRY["$schema"].startswith("https://static.modelcontextprotocol.io/schemas/")


def test_the_page_head_and_text_point_to_the_endpoint():
    page = (ROOT / "web" / "index.html").read_text()
    head, body = page.split("</head>")
    assert '<meta name="mcp-server" content="https://hiringradar.app/mcp" />' in head
    assert 'type="application/mcp-server-card+json" href="https://hiringradar.app/mcp/server-card"' in head
    assert 'href="https://hiringradar.app/llms.txt"' in head
    assert "For AI agents" in body and "https://hiringradar.app/mcp" in body
