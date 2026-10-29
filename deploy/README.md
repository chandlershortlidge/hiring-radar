# Operating the VM

Where hiring-radar runs: one GCP Compute Engine VM, project `hiring-radar-512318`, zone
`europe-west3-a`, instance `hiring-radar`. Port 22 is closed; SSH goes through IAP.
The dashboard is behind Caddy (HTTPS + basic auth) on an `sslip.io` hostname.

Decided in HIR-29; design in [DECISIONS.md](../DECISIONS.md) (2026-10-21).

## SSH in

From the Mac, with `gcloud` logged in to the project:

```
gcloud compute ssh hiring-radar --zone europe-west3-a --tunnel-through-iap
```

`--tunnel-through-iap` is required because the firewall allows only 80/443. `exit` to leave.
Everything below runs on the VM unless it says otherwise.

## Where things are on the VM

| What | Where |
|---|---|
| Code (project root) | `/opt/hiring-radar/app` — not a git checkout; files were copied up |
| Database | `/var/lib/hiring-radar/hiring-radar.db` |
| Secrets (`ANTHROPIC_API_KEY` etc.) | `/etc/hiring-radar.env`, root-only, never in git |
| API process | a systemd service on `127.0.0.1:8000`, Caddy in front |
| Daily poll | `hiring-radar-poll.timer` → `hiring-radar-poll.service`, 07:00 Europe/Berlin |
| Nightly backup | `hiring-radar-backup.timer` → `backup.sh`, 02:30 UTC, to `gs://hiring-radar-512318-backups/db/` |

`systemctl list-units | grep hiring` shows the exact unit names.

## Is it healthy?

```
curl -s localhost:8000/api/stats | grep -o '"last_updated":"[^"]*"'   # moves on every ingest
systemctl list-timers --all | grep hiring                           # LAST / NEXT for poll + backup
journalctl -u hiring-radar-poll --since today --no-pager            # today's poll log
```

`last_updated` is `max(last_seen)` across jobs: it advances whenever the poll ingests anything,
even with no new jobs. A healthy morning shows it at ~06:00Z. The poll log ends with a `TOTAL`
line and an `extracted=` line; a feed line with `FAILED` or `WARNING seen=0` needs a look
(the warning means a company board that used to return postings returned none — usually
the board changed its page format, as JOIN did in October 2026).

## Run the poll by hand

```
cd /opt/hiring-radar/app
sudo -u hiring-radar env HIRING_RADAR_DB=/var/lib/hiring-radar/hiring-radar.db \
  uv run python -m app poll --only join:motor-ai   # one feed; drop --only for all feeds
```

`HIRING_RADAR_DB` must be set: the real path lives in `/etc/hiring-radar.env`, which systemd
loads and a shell does not. Without it the poll creates an empty `data/hiring-radar.db` next
to the code and reports `applied migrations: [1, …]` — that is the tell. Run as the app user
so the DB file keeps its owner. `--no-extract` skips the LLM step.

## Service control

```
sudo systemctl restart <api service>      # after a manual code change
sudo systemctl status hiring-radar-poll.timer
journalctl -u <api service> -n 100 --no-pager
```

## Deploying code

There is no automatic deploy yet (HIR-73). Merging to `main` changes GitHub only. To get a
change onto the VM today, download the changed files from `main` over the old ones, then
restart the API service if `app/` changed:

```
sudo curl -sSo /opt/hiring-radar/app/app/poll.py \
  https://raw.githubusercontent.com/chandlershortlidge/hiring-radar/main/app/poll.py
```

(One line per changed file. Frontend changes need a `web/dist` rebuild, which the e2-micro
can't do; build on the Mac and copy `web/dist` up.)

## Get the database onto the Mac

The DB never travels with a deploy and nothing syncs it back. The local dashboard shows
whatever copy is in `data/`. To refresh it (from the Mac, overwrites the local file):

```
gcloud compute scp hiring-radar:/var/lib/hiring-radar/hiring-radar.db ./data/hiring-radar.db \
  --zone europe-west3-a --tunnel-through-iap
```

Or pull last night's backup from the bucket:

```
gsutil ls gs://hiring-radar-512318-backups/db/      # pick the newest
gsutil cp gs://hiring-radar-512318-backups/db/<file>.gz . && gunzip <file>.gz
```

## Backups

`backup.sh` runs nightly via `hiring-radar-backup.timer`: SQLite `.backup`, integrity check,
gzip, copy to the bucket. `gcs-lifecycle.json` deletes copies older than 30 days.
`journalctl -u hiring-radar-backup --since yesterday --no-pager` shows the last run.
