"""Tests for deploy/vm-ssh.sh (HIR-317): a refused server login is tried again, anything
else is not. A fake `gcloud` on PATH stands in for the real one; nothing leaves the machine.

The fake reads its script from FAKE_PLAN: one line per call, "<exit code> <stderr text>".
It appends what it was sent on stdin to FAKE_STDIN and its arguments to FAKE_ARGS.
"""

import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "deploy" / "vm-ssh.sh"
WORKFLOWS = ROOT / ".github" / "workflows"
REFUSED = "255 sa_1@compute.2: Permission denied (publickey)."

FAKE_GCLOUD = r"""#!/usr/bin/env bash
n=$(cat "$FAKE_COUNT" 2>/dev/null || echo 0); n=$((n + 1)); echo "$n" > "$FAKE_COUNT"
line=$(sed -n "${n}p" "$FAKE_PLAN")
code=${line%% *}; msg=${line#* }
echo "call $n: $*" >> "$FAKE_ARGS"
cat >> "$FAKE_STDIN"
[ "$msg" != "$code" ] && echo "$msg" >&2
[ "$code" = 0 ] && echo "ran on the server"
exit "$code"
"""


def run(tmp_path, plan, stdin_text="tarball-bytes"):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake = bin_dir / "gcloud"
    fake.write_text(FAKE_GCLOUD)
    fake.chmod(0o755)
    (tmp_path / "plan").write_text("\n".join(plan) + "\n")
    payload = tmp_path / "payload"
    payload.write_text(stdin_text)
    env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}", "VM_SSH_WAIT": "0",
           "FAKE_PLAN": str(tmp_path / "plan"), "FAKE_COUNT": str(tmp_path / "count"),
           "FAKE_STDIN": str(tmp_path / "stdin"), "FAKE_ARGS": str(tmp_path / "args")}
    p = subprocess.run(["bash", str(SCRIPT), "echo hello", str(payload)], env=env,
                       capture_output=True, text=True, timeout=30)
    calls = int((tmp_path / "count").read_text())
    sent = (tmp_path / "stdin").read_text()
    return p, calls, sent


def test_a_login_that_works_first_time_is_one_call(tmp_path):
    p, calls, sent = run(tmp_path, ["0"])
    assert p.returncode == 0 and calls == 1
    assert "server login: try 1 of 3" in p.stdout and "ran on the server" in p.stdout
    assert sent == "tarball-bytes"
    args = (tmp_path / "args").read_text()
    assert "compute ssh hiring-radar" in args and "--tunnel-through-iap" in args and "--command echo hello" in args


def test_a_refused_login_is_tried_again_and_the_log_shows_it(tmp_path):
    p, calls, sent = run(tmp_path, [REFUSED, REFUSED, "0"])
    assert p.returncode == 0 and calls == 3
    assert "try 2 of 3" in p.stdout and "try 3 of 3" in p.stdout
    assert "the server refused the login; waiting 0s" in p.stdout
    # The refusal itself stays in the log, and every try is sent the whole file again.
    assert "Permission denied (publickey)" in p.stderr
    assert sent == "tarball-bytes" * 3


def test_three_refusals_fail_with_their_own_code_and_say_so(tmp_path):
    p, calls, _ = run(tmp_path, [REFUSED, REFUSED, REFUSED])
    assert p.returncode == 75 and calls == 3
    assert "refused the login 3 times in a row. Nothing was run on the server." in p.stdout


def test_a_command_that_fails_on_the_server_is_not_run_again(tmp_path):
    p, calls, _ = run(tmp_path, ["1 app did not answer /api/stats within 60s", "0"])
    assert p.returncode == 1 and calls == 1


def test_a_connection_that_drops_part_way_is_not_run_again(tmp_path):
    # ssh's 255 without a refused login: the deploy may be half done on the server.
    p, calls, _ = run(tmp_path, ["255 client_loop: send disconnect: Broken pipe", "0"])
    assert p.returncode == 255 and calls == 1


def test_the_refusal_words_from_a_command_that_ran_do_not_count(tmp_path):
    # e.g. a git fetch on the server that was itself refused: exit code 1, not ssh's 255.
    p, calls, _ = run(tmp_path, ["1 git@github.com: Permission denied (publickey).", "0"])
    assert p.returncode == 1 and calls == 1


def test_no_workflow_logs_in_to_the_server_any_other_way():
    for wf in sorted(WORKFLOWS.glob("*.yml")):
        code = "\n".join(line for line in wf.read_text().splitlines() if not line.lstrip().startswith("#"))
        assert not re.search(r"gcloud\s+compute\s+(ssh|scp)", code), f"{wf.name} logs in without deploy/vm-ssh.sh"
    assert "vm-ssh.sh" in (WORKFLOWS / "deploy.yml").read_text()
