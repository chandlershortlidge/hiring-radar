#!/usr/bin/env bash
# Make the server's systemd units match the ones committed in this folder (HIR-310).
#
# Compares every hiring-radar*.service and hiring-radar*.timer in <source> with the file
# of the same name in <destination>, installs the ones that differ or are missing, and
# prints one line per file, so the deploy log says what the server had:
#
#   same       hiring-radar-poll.timer
#   installed  hiring-radar-backup.timer (differed from the server's copy)
#   installed  hiring-radar-caretaker.timer (was not on the server)
#
# Then: `daemon-reload` if anything was installed, `enable --now` for every timer (so a
# timer new to the repo starts ticking), and a restart of each timer that was installed
# (so a changed time takes effect now, not at the next boot). Restarting a timer does not
# run its job. A .service is never started or restarted here: for poll, backup and
# caretaker that would run the job, and the API is restarted by whoever called this.
#
# Called by remote-deploy.sh on every deploy and by provision.sh. Not the Caddyfile: the
# server's copy holds a password hash the repo's does not.
#
# Usage, as root: bash deploy/install-units.sh [<source>] [<destination>]
#   <source>       default: the folder this script is in
#   <destination>  default: /etc/systemd/system
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SRC=${1:-$HERE}
DEST=${2:-/etc/systemd/system}

shopt -s nullglob
units=("$SRC"/hiring-radar*.service "$SRC"/hiring-radar*.timer)
[ "${#units[@]}" -gt 0 ] || { echo "no hiring-radar unit files in $SRC" >&2; exit 1; }
[ -d "$DEST" ] || { echo "no such folder: $DEST" >&2; exit 1; }

installed=()
for unit in "${units[@]}"; do
  name=$(basename "$unit")
  if [ ! -e "$DEST/$name" ]; then
    why="was not on the server"
  elif cmp -s "$unit" "$DEST/$name"; then
    echo "same       $name"
    continue
  else
    why="differed from the server's copy"
  fi
  install -m 644 "$unit" "$DEST/$name"
  installed+=("$name")
  echo "installed  $name ($why)"
done

if [ "${#installed[@]}" -gt 0 ]; then systemctl daemon-reload; fi

timers=()
for unit in "$SRC"/hiring-radar*.timer; do timers+=("$(basename "$unit")"); done
if [ "${#timers[@]}" -gt 0 ]; then systemctl enable --now "${timers[@]}"; fi

for name in ${installed[@]+"${installed[@]}"}; do
  case "$name" in *.timer) systemctl restart "$name" ;; esac
done

echo "units: ${#units[@]} compared, ${#installed[@]} installed"
