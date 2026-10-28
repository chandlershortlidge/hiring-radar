#!/usr/bin/env bash
# Deploy the code already checked out in /opt/hiring-radar/app:
# backup → Python deps → frontend → restart → smoke check.
# Run as root on the VM by the GitHub deploy workflow, after it has reset
# the checkout to the commit being deployed.
# Usage: sudo bash deploy/remote-deploy.sh /tmp/web-dist.tgz
set -euo pipefail

APP=/opt/hiring-radar/app
DIST_TARBALL=${1:?usage: remote-deploy.sh <web-dist.tgz>}
as_app() { sudo -u hiring-radar -H "$@"; }

echo "→ backup before deploy"
systemctl start hiring-radar-backup.service

echo "→ python deps"
as_app uv --directory "$APP" sync --frozen --no-dev

echo "→ frontend"
as_app rm -rf "$APP/web/dist"
as_app tar -xzf "$DIST_TARBALL" -C "$APP/web"
rm -f "$DIST_TARBALL"

echo "→ restart"
systemctl restart hiring-radar

echo "→ smoke check"
for i in $(seq 1 60); do
  if curl -fsS -o /dev/null http://127.0.0.1:8000/api/stats; then
    echo "✓ deployed $(as_app git -C "$APP" rev-parse --short HEAD)"
    exit 0
  fi
  sleep 1
done
echo "✗ app did not answer /api/stats within 60s" >&2
journalctl -u hiring-radar -n 30 --no-pager >&2
exit 1
