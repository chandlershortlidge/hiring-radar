"""Tests for deploy/install-units.sh (HIR-310): every deploy makes the server's systemd
units match the ones in the repo, and says in its log what it found.

Before this, a merged change to a schedule (the daily poll, the backup, the caretaker)
deployed green and changed nothing on the server, because only provision.sh, run by hand,
ever copied a unit file to /etc.

A temporary folder stands in for /etc/systemd/system and a fake `systemctl` on PATH
records what it was asked to do; nothing touches this machine's systemd.
"""

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEPLOY = ROOT / "deploy"
SCRIPT = DEPLOY / "install-units.sh"
UNITS = sorted(p.name for p in DEPLOY.glob("hiring-radar*.service")) + sorted(
    p.name for p in DEPLOY.glob("hiring-radar*.timer"))
TIMERS = [u for u in UNITS if u.endswith(".timer")]

FAKE_SYSTEMCTL = """#!/usr/bin/env bash
echo "$*" >> "$FAKE_CALLS"
exit "${FAKE_EXIT:-0}"
"""


def server_folder(tmp_path):
    """A stand-in for the server's /etc/systemd/system, holding the repo's units as they are."""
    dest = tmp_path / "etc-systemd-system"
    dest.mkdir()
    for name in UNITS:
        shutil.copy(DEPLOY / name, dest / name)
    return dest


def run(tmp_path, dest, src=DEPLOY, fake_exit="0"):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    fake = bin_dir / "systemctl"
    fake.write_text(FAKE_SYSTEMCTL)
    fake.chmod(0o755)
    calls = tmp_path / "calls"
    calls.write_text("")
    env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}",
           "FAKE_CALLS": str(calls), "FAKE_EXIT": fake_exit}
    p = subprocess.run(["bash", str(SCRIPT), str(src), str(dest)], env=env,
                       capture_output=True, text=True, timeout=30)
    return p, calls.read_text().splitlines()


def test_the_repo_has_the_units_this_file_expects():
    assert "hiring-radar.service" in UNITS
    assert {"hiring-radar-poll.timer", "hiring-radar-backup.timer",
            "hiring-radar-caretaker.timer"} <= set(TIMERS)


def test_identical_folders_install_nothing_and_stay_green(tmp_path):
    dest = server_folder(tmp_path)
    before = {n: (dest / n).stat().st_mtime_ns for n in UNITS}
    p, calls = run(tmp_path, dest)
    assert p.returncode == 0, p.stderr
    for name in UNITS:
        assert f"same       {name}" in p.stdout
    assert "installed" not in p.stdout.replace("0 installed", "")
    assert f"units: {len(UNITS)} compared, 0 installed" in p.stdout
    assert {n: (dest / n).stat().st_mtime_ns for n in UNITS} == before
    # No reload and no restart; `enable --now` on timers already enabled changes nothing.
    assert calls == ["enable --now " + " ".join(TIMERS)]


def test_a_changed_file_and_a_missing_file_are_both_installed_and_named(tmp_path):
    dest = server_folder(tmp_path)
    (dest / "hiring-radar-poll.timer").write_text("[Timer]\nOnCalendar=*-*-* 06:00:00\n")
    (dest / "hiring-radar-caretaker.service").unlink()
    p, calls = run(tmp_path, dest)
    assert p.returncode == 0, p.stderr
    assert "installed  hiring-radar-poll.timer (differed from the server's copy)" in p.stdout
    assert "installed  hiring-radar-caretaker.service (was not on the server)" in p.stdout
    assert "same       hiring-radar-backup.timer" in p.stdout
    assert f"units: {len(UNITS)} compared, 2 installed" in p.stdout
    # The server's folder now holds exactly what the repo holds.
    for name in UNITS:
        assert (dest / name).read_bytes() == (DEPLOY / name).read_bytes(), name
    assert (dest / "hiring-radar-poll.timer").stat().st_mode & 0o777 == 0o644


def test_every_unit_gets_a_line_in_the_log(tmp_path):
    """The first deploy with this change is the first real check of the server, so the
    log has to answer for every file, not only the ones that differed."""
    dest = server_folder(tmp_path)
    (dest / "hiring-radar-backup.service").unlink()
    p, _ = run(tmp_path, dest)
    lines = [l for l in p.stdout.splitlines() if l.startswith(("same ", "installed "))]
    assert sorted(l.split()[1] for l in lines) == sorted(UNITS)


def test_a_change_reloads_systemd_and_a_changed_timer_is_restarted(tmp_path):
    dest = server_folder(tmp_path)
    (dest / "hiring-radar-poll.timer").write_text("old\n")
    p, calls = run(tmp_path, dest)
    assert p.returncode == 0, p.stderr
    assert calls == ["daemon-reload", "enable --now " + " ".join(TIMERS),
                     "restart hiring-radar-poll.timer"]


def test_a_changed_service_is_never_started_or_restarted(tmp_path):
    """Restarting the poll's or the backup's service would run the job. The API's restart
    belongs to the deploy script, which does it right after this step."""
    dest = server_folder(tmp_path)
    for name in UNITS:
        if name.endswith(".service"):
            (dest / name).write_text("old\n")
    p, calls = run(tmp_path, dest)
    assert p.returncode == 0, p.stderr
    assert calls == ["daemon-reload", "enable --now " + " ".join(TIMERS)]


def test_a_timer_new_to_the_repo_is_installed_and_enabled_without_a_list_to_update(tmp_path):
    src = tmp_path / "repo-deploy"
    src.mkdir()
    for name in UNITS:
        shutil.copy(DEPLOY / name, src / name)
    (src / "hiring-radar-weekly.timer").write_text("[Timer]\nOnCalendar=Mon 09:00\n")
    (src / "hiring-radar-weekly.service").write_text("[Service]\nExecStart=/bin/true\n")
    (src / "Caddyfile").write_text("not a unit\n")
    dest = server_folder(tmp_path)
    p, calls = run(tmp_path, dest, src=src)
    assert p.returncode == 0, p.stderr
    assert "installed  hiring-radar-weekly.timer (was not on the server)" in p.stdout
    assert (dest / "hiring-radar-weekly.service").exists()
    assert "hiring-radar-weekly.timer" in calls[1] and calls[1].startswith("enable --now ")
    assert not (dest / "Caddyfile").exists()


def test_a_systemctl_failure_fails_the_step(tmp_path):
    dest = server_folder(tmp_path)
    (dest / "hiring-radar-poll.timer").write_text("old\n")
    p, _ = run(tmp_path, dest, fake_exit="1")
    assert p.returncode != 0


def test_a_missing_destination_folder_fails_loudly(tmp_path):
    p, calls = run(tmp_path, tmp_path / "nowhere")
    assert p.returncode != 0 and "no such folder" in p.stderr and calls == []


def test_the_deploy_runs_the_step_before_it_restarts_the_api():
    text = (DEPLOY / "remote-deploy.sh").read_text()
    step = text.index('bash "$APP/deploy/install-units.sh"')
    assert step < text.index("systemctl restart hiring-radar")
    assert "set -euo pipefail" in text  # so a failed step stops the deploy


def test_provisioning_uses_the_same_step_and_keeps_no_list_of_timers():
    text = (DEPLOY / "provision.sh").read_text()
    assert 'bash "$HERE/install-units.sh"' in text
    assert ".timer" not in text.split('step "6. systemd units"')[1].split('step "7.')[0]


def test_the_deploy_guide_no_longer_says_a_deploy_leaves_the_units_alone():
    text = (DEPLOY / "README.md").read_text()
    assert "A deploy never touches the database or `/etc`" not in text
    assert "They are *not* applied by a deploy" not in text
    assert "install-units.sh" in text
