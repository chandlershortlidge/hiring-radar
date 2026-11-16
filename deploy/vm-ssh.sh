#!/usr/bin/env bash
# Run one command on the VM from a GitHub workflow, trying again when the server refuses
# the login (HIR-317, DECISIONS 2026-11-16).
#
# Every workflow job makes a brand-new login key, registers it with Google's OS Login and
# connects seconds later. Now and then the server does not accept the key yet and answers
# "Permission denied (publickey)". On 15 Nov that stopped a rollback, so a version the
# robot visitor had failed stayed live. This is the one way a workflow logs in to the VM
# (tests/test_vm_ssh.py checks no workflow calls `gcloud compute ssh` itself).
#
# Does: up to VM_SSH_TRIES logins (default 3), VM_SSH_WAIT seconds apart (default 15),
# printing "server login: try N of M" each time so the log shows what happened.
# Does NOT: try again after anything but a refused login. A refused login is the one
# failure where nothing has run on the server. A command that started and failed, or a
# connection that dropped part-way, exits at once with the code it got: running a
# half-done deploy again in the hope that it passes is not this script's call.
#
# Exit: 0 the command ran and succeeded; 75 the login was refused on every try; anything
# else is the failed command's own code (255 when the connection broke for another reason).
#
# Usage: bash deploy/vm-ssh.sh '<command to run on the VM>' [file to send as its stdin]
set -uo pipefail

CMD=${1:?usage: vm-ssh.sh '<command>' [stdin-file]}
IN=${2:-/dev/null}
TRIES=${VM_SSH_TRIES:-3}
WAIT=${VM_SSH_WAIT:-15}
LOGIN_REFUSED=75

err=$(mktemp)
trap 'rm -f "$err"' EXIT

for i in $(seq 1 "$TRIES"); do
  echo "→ server login: try $i of $TRIES"
  # stderr goes to the log as it happens and to a file, so the refusal can be recognised.
  # (stdout passes straight through on descriptor 3; only stderr goes through the tee.)
  {
    gcloud compute ssh hiring-radar --zone=europe-west3-a --tunnel-through-iap --quiet \
      --strict-host-key-checking=no --ssh-key-expire-after=30m --command "$CMD" \
      < "$IN" 2>&1 >&3 | tee "$err" >&2
    rc=${PIPESTATUS[0]}
  } 3>&1
  [ "$rc" -eq 0 ] && exit 0
  # 255 is ssh's own code for "no session"; with this message, the login was refused.
  if [ "$rc" -ne 255 ] || ! grep -q "Permission denied (publickey" "$err"; then
    exit "$rc"
  fi
  if [ "$i" -lt "$TRIES" ]; then
    echo "→ the server refused the login; waiting ${WAIT}s before try $((i + 1)) of $TRIES"
    sleep "$WAIT"
  fi
done

echo "::error::The server refused the login $TRIES times in a row. Nothing was run on the server."
exit "$LOGIN_REFUSED"
