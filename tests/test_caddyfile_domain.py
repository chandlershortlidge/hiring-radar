"""deploy/Caddyfile after the move to hiringradar.app (HIR-458).

The site lives at hiringradar.app; www and the old sslip.io address forward to it with
the path kept. On the old address /mcp is still served, not redirected, until that
address is removed: a client that follows a 301 resends the POST as a GET, which /mcp
refuses, so a redirect would cut off every Claude already connected there.
"""

import re
from pathlib import Path

CADDYFILE = (Path(__file__).resolve().parent.parent / "deploy" / "Caddyfile").read_text()


def sites() -> dict[str, str]:
    """Each top-level site block, by its address line, with its body."""
    out, depth, name, body = {}, 0, None, []
    for raw in CADDYFILE.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if depth == 0 and line.endswith("{"):
            name, body = line.rstrip("{").strip(), []
        elif depth == 1 and line == "}":
            out[name] = "\n".join(body)
        else:
            body.append(line)
        depth += line.endswith("{") - (line == "}")
    return out


def test_the_site_is_served_at_the_domain_first():
    # First, because tests/test_admin.py reads the first plain `handle` as the dashboard's.
    assert list(sites())[0] == "hiringradar.app"
    assert "reverse_proxy 127.0.0.1:8000" in sites()["hiringradar.app"]


def test_www_and_the_old_address_forward_to_the_domain_with_the_path_kept():
    for old in ("www.hiringradar.app", "34-159-223-190.sslip.io"):
        assert "redir https://hiringradar.app{uri} 301" in sites()[old], old


def test_the_old_address_still_serves_the_mcp_rather_than_redirecting_it():
    old = sites()["34-159-223-190.sslip.io"]
    assert re.search(r"@mcp path /mcp\s+handle @mcp \{\s+reverse_proxy 127\.0\.0\.1:8000", old)


def test_the_old_address_appears_nowhere_but_its_own_block():
    assert [s for s in sites() if "sslip" in s] == ["34-159-223-190.sslip.io"]
    assert "sslip" not in "\n".join(v for k, v in sites().items())
