#!/usr/bin/env bash
# Nightly backup: consistent SQLite snapshot → integrity check → gzip → Cloud Storage.
set -euo pipefail

DB=/var/lib/hiring-radar/hiring-radar.db
BUCKET=gs://hiring-radar-512318-backups
STAMP=$(date -u +%Y-%m-%dT%H%M%SZ)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

sqlite3 "$DB" ".backup '$TMP/hiring-radar.db'"
[ "$(sqlite3 "$TMP/hiring-radar.db" 'PRAGMA integrity_check;')" = "ok" ] \
  || { echo "integrity check failed" >&2; exit 1; }
gzip "$TMP/hiring-radar.db"
gcloud storage cp "$TMP/hiring-radar.db.gz" "$BUCKET/db/hiring-radar-$STAMP.db.gz"
echo "backup ok: $BUCKET/db/hiring-radar-$STAMP.db.gz"
