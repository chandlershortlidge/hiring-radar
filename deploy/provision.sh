#!/usr/bin/env bash
# Build the VM's software side: packages, swap, app user, checkout, systemd units, Caddy.
# This is steps 3-7 of deploy/README.md "Building the VM from nothing". Steps 1, 2 and 8
# create GCP resources (IP, firewall, instance, bucket, workload identity) and are run from
# the Mac by hand -- this script needs no GCP credentials beyond the VM's own.
#
# Safe to re-run: every step checks for its own result first, so a second run is a no-op
# apart from `apt-get`, `uv sync` and `systemctl`, which are idempotent anyway. It never
# overwrites /etc/hiring-radar.env (the secrets) and never touches the database.
#
# What it does NOT do: deploy code (that is GitHub Actions -> remote-deploy.sh), build
# web/dist (the e2-micro cannot), restore a backup, or change any GCP resource.
#
# Usage, as root on the VM:
#   sudo bash deploy/provision.sh                       # no Caddyfile change
#   sudo DASHBOARD_PASSWORD='...' bash deploy/provision.sh   # ...and set the basic-auth password
set -euo pipefail

# ---- settings ----------------------------------------------------------------
APP_USER=hiring-radar
APP_DIR=/opt/hiring-radar/app
DB_DIR=/var/lib/hiring-radar
DB_PATH=$DB_DIR/hiring-radar.db
ENV_FILE=/etc/hiring-radar.env
REPO_URL=https://github.com/chandlershortlidge/hiring-radar.git
SITE_HOST=34-159-223-190.sslip.io   # the static IP with dots as dashes; see README step 1
BASICAUTH_USER=chandler
SWAP_FILE=/swapfile
SWAP_SIZE=1G
# Password for the dashboard's basic-auth gate. Leave empty to leave /etc/caddy/Caddyfile
# alone (the usual case when re-running); set DASHBOARD_PASSWORD in the environment to
# write a fresh Caddyfile with that password hashed.
DASHBOARD_PASSWORD=${DASHBOARD_PASSWORD:-}
# -----------------------------------------------------------------------------

[ "$(id -u)" -eq 0 ] || { echo "run as root (sudo bash $0)" >&2; exit 1; }
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
step() { echo; echo "== $*"; }
skip() { echo "   already done: $*"; }

step "3a. packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq git sqlite3 caddy curl
if command -v uv >/dev/null; then
  skip "uv $(uv --version | awk '{print $2}')"
else
  curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
fi

step "3b. swap ($SWAP_SIZE)"
# An e2-micro has under 1 GB of RAM; `uv sync` alongside the running app needs the swap.
if swapon --show=NAME --noheadings | grep -qx "$SWAP_FILE"; then
  skip "$SWAP_FILE active"
else
  if [ ! -f "$SWAP_FILE" ]; then
    fallocate -l "$SWAP_SIZE" "$SWAP_FILE"
    chmod 600 "$SWAP_FILE"
    mkswap "$SWAP_FILE" >/dev/null
  fi
  swapon "$SWAP_FILE"
  grep -qF "$SWAP_FILE" /etc/fstab || echo "$SWAP_FILE none swap sw 0 0" >> /etc/fstab
fi

step "3c. app user and directories"
if id "$APP_USER" >/dev/null 2>&1; then
  skip "user $APP_USER"
else
  useradd --system --home "$(dirname "$APP_DIR")" --create-home \
    --shell /usr/sbin/nologin "$APP_USER"
fi
# 750: only the app user and root can read the database.
install -d -o "$APP_USER" -g "$APP_USER" -m 750 "$DB_DIR"
install -d -o "$APP_USER" -g "$APP_USER" -m 755 "$(dirname "$APP_DIR")"

step "4. code and virtualenv at $APP_DIR"
if [ -d "$APP_DIR/.git" ]; then
  skip "checkout exists"
  sudo -u "$APP_USER" -H git -C "$APP_DIR" fetch --quiet origin main
else
  sudo -u "$APP_USER" -H git clone --quiet "$REPO_URL" "$APP_DIR"
fi
sudo -u "$APP_USER" -H uv --directory "$APP_DIR" sync --frozen --no-dev
# web/dist is not in git. The first deploy puts it there; until then the dashboard 404s
# and only the JSON endpoints answer.
[ -d "$APP_DIR/web/dist" ] || echo "   note: no web/dist yet -- merge to main, or build it on the Mac and copy it up"

step "5. secrets at $ENV_FILE"
if [ -s "$ENV_FILE" ]; then
  skip "$ENV_FILE (left untouched)"
else
  install -m 600 /dev/null "$ENV_FILE"
  cat > "$ENV_FILE" <<ENV
# Root-only, never in git. Loaded by the systemd units; a login shell does not see it.
ANTHROPIC_API_KEY=
BRAVE_API_KEY=
# Optional. With a key, every poll and re-read is one LangSmith trace with a child per
# job (HIR-160). Left blank, tracing is off and the poll runs exactly as before.
LANGSMITH_API_KEY=
HIRING_RADAR_DB=$DB_PATH
ENV
  echo "   WROTE A TEMPLATE -- put the real keys in $ENV_FILE before the app is any use"
fi
grep -q '^HIRING_RADAR_DB=' "$ENV_FILE" || echo "HIRING_RADAR_DB=$DB_PATH" >> "$ENV_FILE"
# Appended blank rather than skipped, so an env file written before HIR-160 shows the
# variable exists. Blank means off; nothing breaks until a real key is pasted in.
grep -q '^LANGSMITH_API_KEY=' "$ENV_FILE" || echo "LANGSMITH_API_KEY=" >> "$ENV_FILE"

step "6. systemd units"
# Copied from this repo, so /etc matches what is committed. `diff` the two to spot drift.
changed=0
for unit in "$HERE"/hiring-radar*.service "$HERE"/hiring-radar*.timer; do
  dest=/etc/systemd/system/$(basename "$unit")
  if cmp -s "$unit" "$dest"; then
    skip "$(basename "$unit")"
  else
    install -m 644 "$unit" "$dest"
    changed=1
  fi
done
if [ "$changed" -eq 1 ]; then systemctl daemon-reload; fi
systemctl enable --now hiring-radar hiring-radar-poll.timer hiring-radar-backup.timer
if [ "$changed" -eq 1 ]; then systemctl restart hiring-radar; fi
# The first request creates the database and applies every migration, so this is setup,
# not only a check.
for i in $(seq 1 60); do
  curl -fsS -o /dev/null http://127.0.0.1:8000/api/stats && break
  [ "$i" -eq 60 ] && { echo "api did not answer /api/stats in 60s" >&2
                       journalctl -u hiring-radar -n 30 --no-pager >&2; exit 1; }
  sleep 1
done
echo "   api up on 127.0.0.1:8000"

step "7. Caddy (HTTPS + basic auth for $SITE_HOST)"
if [ -n "$DASHBOARD_PASSWORD" ]; then
  # The committed Caddyfile carries a placeholder hash; this is the only step that sees
  # the password, and the hash never enters the repo.
  hash=$(caddy hash-password --plaintext "$DASHBOARD_PASSWORD")
  tmp=$(mktemp)
  sed -e "s|REPLACE_WITH_BCRYPT_HASH|$hash|" \
      -e "s|^34-159-223-190\.sslip\.io|$SITE_HOST|" \
      -e "s|^\([[:space:]]*\)chandler |\1$BASICAUTH_USER |" "$HERE/Caddyfile" > "$tmp"
  if grep -q REPLACE_WITH_BCRYPT_HASH "$tmp"; then
    echo "the placeholder hash was not substituted -- refusing to install" >&2
    rm -f "$tmp"; exit 1
  fi
  install -m 644 -o root -g root "$tmp" /etc/caddy/Caddyfile
  rm -f "$tmp"
  caddy validate --config /etc/caddy/Caddyfile >/dev/null
  systemctl enable caddy
  systemctl reload-or-restart caddy
  echo "   wrote /etc/caddy/Caddyfile; watch the certificate: journalctl -u caddy -n 20"
elif [ -s /etc/caddy/Caddyfile ] && ! grep -q REPLACE_WITH_BCRYPT_HASH /etc/caddy/Caddyfile; then
  systemctl enable --now caddy
  skip "/etc/caddy/Caddyfile (set DASHBOARD_PASSWORD to rewrite it)"
else
  echo "   NO CADDYFILE YET -- re-run with DASHBOARD_PASSWORD='...' to write one" >&2
fi

echo
echo "provisioned. Still by hand, from the Mac: README steps 1, 2 and 8 (static IP,"
echo "firewall, instance, backups bucket, workload-identity deployer for CI/CD)."
