# Operating the VM

Where hiring-radar runs: one GCP Compute Engine VM, project `hiring-radar-512318`, zone
`europe-west3-a`, instance `hiring-radar` (e2-micro, Debian 12, 20 GB disk). Port 22 is
reachable only from Google's IAP range, so SSH goes through IAP. The dashboard is behind
Caddy (HTTPS + basic auth) on an `sslip.io` hostname. Merging to `main` deploys.

Decided in HIR-29; design in [DECISIONS.md](../DECISIONS.md) (2026-10-21), final shape of
the setup in the 2026-11-01 entry.

## What is in this folder

| File | What it is |
|---|---|
| `provision.sh` | Builds the VM's software side from nothing. Safe to re-run. |
| `hiring-radar.service` | The API process (systemd unit, copied from the VM). |
| `hiring-radar-poll.service` / `.timer` | The 07:00 Europe/Berlin poll. |
| `hiring-radar-backup.service` / `.timer` | The 03:30 Europe/Berlin backup. |
| `Caddyfile` | HTTPS + basic auth in front of the API. The bcrypt hash is a placeholder. |
| `backup.sh` | What the backup unit runs: snapshot → integrity check → gzip → bucket. |
| `remote-deploy.sh` | What the GitHub deploy job runs on the VM. |
| `gcs-lifecycle.json` | Bucket rule: delete backups older than 30 days. |

The unit files and the Caddyfile are verbatim copies of what is in `/etc` on the VM (the
one exception is the Caddyfile's password hash), so `diff` against `/etc` says whether the
VM has drifted from the repo. They are *not* applied by a deploy — `provision.sh` installs
them, and a change to one has to be provisioned or copied up by hand.

## SSH in

From the Mac, with `gcloud` logged in to the project:

```
gcloud compute ssh hiring-radar --zone europe-west3-a --tunnel-through-iap
```

`--tunnel-through-iap` is required because the firewall allows 22 only from
`35.235.240.0/20` (IAP) and 80/443 from anywhere. `exit` to leave. Everything below runs
on the VM unless it says otherwise.

## Where things are on the VM

| What | Where |
|---|---|
| Code (project root) | `/opt/hiring-radar/app` — a git checkout of `main`, owned by `hiring-radar` |
| Virtualenv | `/opt/hiring-radar/app/.venv`, built by `uv sync --frozen --no-dev` |
| Database | `/var/lib/hiring-radar/hiring-radar.db` |
| Secrets (`ANTHROPIC_API_KEY`, `LANGSMITH_API_KEY`, `HIRING_RADAR_DB`, …) | `/etc/hiring-radar.env`, root-only, never in git |
| API process | `hiring-radar.service` on `127.0.0.1:8000`, Caddy in front |
| Daily poll | `hiring-radar-poll.timer` → `hiring-radar-poll.service`, 07:00 Europe/Berlin |
| Nightly backup | `hiring-radar-backup.timer` → `backup.sh`, 03:30 Europe/Berlin, to `gs://hiring-radar-512318-backups/db/` |

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
the board changed its page format, as JOIN did in October 2026). A `grounding:` line means
the model quoted evidence that is not in the posting — see [Tracing the poll](#tracing-the-poll).

## Tracing the poll

With `LANGSMITH_API_KEY` set in `/etc/hiring-radar.env`, every extraction run is one trace
in the LangSmith project `hiring-radar-live`, with a child span per job (HIR-160):

| Level | What is on it |
|---|---|
| the run | `poll`, `re-read`, `add` or `backfill`; jobs queued, how many were first reads and how many re-reads, jobs attempted/succeeded/failed/dropped, skills found, and the run's grounding totals |
| a job | the posting that was sent, the skills found, token usage, and its grounding — how many snippets the model quoted as evidence were really in the ad |
| the model call | tokens, latency and cost, measured by LangSmith from the wrapped Anthropic client |

One trace per run, not per job, so the free plan's 5,000 traces a month (shared with the
eval) covers a few dozen a month however many cities are added.

Turning it off is removing the key — there is no other switch, and a LangSmith outage can
only ever print a `[langsmith] … continuing without it` line on stderr. Override the
project name with `LANGSMITH_LIVE_PROJECT` if you ever want a run kept apart.

The `langsmith` package is a project dependency, so the deploy's `uv sync --frozen
--no-dev` installs it on the VM. It was dev-only until HIR-233, and the first traced poll
died on the missing import; a failed import is now tracing off with one warning, like any
other LangSmith failure.

**Tags worth filtering on.** `grounding-failure` on a run or a job means the model offered
a quote that is not in the posting it came from — it invented its evidence. The poll log
says so too, in a `grounding:` line printed only when it happens. `extraction-failure` and
`dropped` are jobs the model could not read; `reread` is a run whose queue held jobs being
read a second time after a version bump.

**The monitoring dashboard is four clicks in the LangSmith UI**, not something this repo
can create: the LangSmith SDK (0.14) has no dashboard API, so there is nothing to script.
Once, in `hiring-radar-live` → Dashboards → New:

1. **Cost per day** — metric `Total cost`, grouped by run name, filtered to root runs only.
2. **Jobs read per day** — metric `Run count`, filtered to `name = job`-prefixed spans (or
   sum the runs' `succeeded` output).
3. **Extraction errors per day** — metric `Run count`, filtered to tag `extraction-failure`.
4. **Grounding failures per day** — metric `Run count`, filtered to tag `grounding-failure`.

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
sudo systemctl restart hiring-radar          # after a manual code change
sudo systemctl status hiring-radar-poll.timer
journalctl -u hiring-radar -n 100 --no-pager
```

## How deploys work

Merging to `main` deploys. `.github/workflows/ci.yml` runs the Python tests and the
frontend build on every push and PR; on a push to `main` that passes both, the `deploy` job
runs. It is serialized (`concurrency: deploy`, no cancel-in-progress), so two merges deploy
one after the other rather than racing.

The job:

1. Builds `web/dist` on the runner and tars it — the e2-micro cannot run a Vite build in
   969 MB of RAM.
2. Gets a GCP credential with no stored key, through **workload identity federation**:
   GitHub mints an OIDC token for the run, GCP's provider `hiring-radar-repo` in pool
   `github` accepts it only when `assertion.repository == 'chandlershortlidge/hiring-radar'`
   **and** `assertion.ref == 'refs/heads/main'`, and swaps it for a token for the
   `github-deployer` service account. A fork, a branch or a PR gets nothing. There is no
   service-account key anywhere, and no GitHub secret to rotate.
3. Opens **one** `gcloud compute ssh` connection over IAP and does everything in it: the
   tarball goes in on that connection's stdin (`cat > /tmp/web-dist.tgz`), then `main` is
   fetched and `git reset --hard` to the merged commit, then
   `sudo bash deploy/remote-deploy.sh /tmp/web-dist.tgz`. `remote-deploy.sh` takes a
   backup first, then `uv sync --frozen --no-dev`, unpacks `web/dist`, restarts the API, and
   polls `/api/stats` for up to 60 s. If the app does not answer it exits non-zero and
   prints the last 30 journal lines, so the workflow goes red. A tarball that arrives
   truncated fails `tar -xzf` in the same script, so that is loud too.

`github-deployer` holds exactly three roles: `roles/compute.viewer` and
`roles/iap.tunnelResourceAccessor` on the project, and `roles/compute.osAdminLogin` on the
instance only. **OS Login** (`enable-oslogin=TRUE` on the instance) is what turns that role
into a Linux account: no SSH keys live in instance metadata, and each run gets a throwaway
key (`--ssh-key-expire-after=30m`). `osAdminLogin` rather than `osLogin` because
`remote-deploy.sh` needs `sudo`.

Most of a deploy's wall clock is the IAP/OS Login connection, which provisions a fresh
throwaway key. Until HIR-106 there were two of them (an `scp`, then the `ssh`) and a deploy
took ~5 minutes; there is now one.

Migrations need no step here: the API opens the database per request and applies any
pending migration first (`app/api.py` → `db.migrate`), so step 3's smoke check against
`/api/stats` is what migrates.

**A deploy never touches the database or `/etc`.** Changing a unit file, the Caddyfile or
`/etc/hiring-radar.env` means provisioning or copying it up by hand.

## Deploying by hand

If Actions is unavailable, the same three lines from the Mac:

```
cd web && npm ci && npm run build && tar -czf ../web-dist.tgz dist && cd ..
gcloud compute scp web-dist.tgz hiring-radar:/tmp/web-dist.tgz --zone europe-west3-a --tunnel-through-iap
gcloud compute ssh hiring-radar --zone europe-west3-a --tunnel-through-iap --command \
  'sudo -u hiring-radar -H git -C /opt/hiring-radar/app pull --ff-only &&
   sudo bash /opt/hiring-radar/app/deploy/remote-deploy.sh /tmp/web-dist.tgz'
```

## Get the database onto the Mac

The DB never travels with a deploy and nothing syncs it back. The local dashboard shows
whatever copy is in `data/`. To refresh it (from the Mac, overwrites the local file):

```
gcloud compute scp hiring-radar:/var/lib/hiring-radar/hiring-radar.db ./data/hiring-radar.db \
  --zone europe-west3-a --tunnel-through-iap
```

Or pull last night's backup from the bucket:

```
gcloud storage ls "gs://hiring-radar-512318-backups/db/hiring-radar-$(date -u +%Y-%m-%d)*"
gcloud storage cp gs://hiring-radar-512318-backups/db/<file>.gz . && gunzip <file>.gz
```

One day at a time, not the whole `db/` prefix — see [Backups](#backups) for why the full
listing misleads.

## Backups

`backup.sh` runs nightly via `hiring-radar-backup.timer`: SQLite `.backup`, integrity check,
gzip, copy to `gs://hiring-radar-512318-backups/db/`. `gcs-lifecycle.json` deletes copies
older than 30 days. The VM writes to the bucket as its own (default Compute Engine) service
account, which has project `roles/editor` — no extra grant.
`journalctl -u hiring-radar-backup --since yesterday --no-pager` shows the last run.
`systemctl start hiring-radar-backup.service` takes one on demand (a deploy does this).

**To check that a backup landed, ask for one day, not for the whole bucket:**

```
gcloud storage ls "gs://hiring-radar-512318-backups/db/hiring-radar-$(date -u +%Y-%m-%d)*"
```

A nightly plus every deploy means the bucket holds 50+ objects, and a plain
`gcloud storage ls` of `db/` returns all of them oldest-first. Any wrapper or terminal that
clips long output then leaves you reading a *prefix* of the listing whose last line looks
like the newest backup — and `| sort | tail` does not save you if the clipping happens
before the pipe. The listing above is a few lines however the bucket grows, so there is
nothing to clip. HIR-112 was a two-day backup outage reported entirely from a clipped
listing; see DECISIONS.md (2026-11-03).

## Restore a backup

On the VM. The `-wal` and `-shm` files must go: SQLite will otherwise replay the old
write-ahead log over the file you just restored and you get a mix of both databases.

```
BK=hiring-radar-2026-11-01T023000Z.db.gz          # pick one from the bucket listing
gcloud storage cp "gs://hiring-radar-512318-backups/db/$BK" /tmp/
gunzip -f "/tmp/$BK"
sqlite3 "/tmp/${BK%.gz}" 'PRAGMA integrity_check;'          # expect: ok

sudo systemctl stop hiring-radar-poll.timer hiring-radar
sudo mv /var/lib/hiring-radar/hiring-radar.db /var/lib/hiring-radar/hiring-radar.db.before-restore
sudo rm -f /var/lib/hiring-radar/hiring-radar.db-wal /var/lib/hiring-radar/hiring-radar.db-shm
sudo install -o hiring-radar -g hiring-radar -m 644 "/tmp/${BK%.gz}" \
  /var/lib/hiring-radar/hiring-radar.db
sudo systemctl start hiring-radar hiring-radar-poll.timer

curl -s localhost:8000/api/stats | head -c 200
```

`install` rather than `mv` so the owner and mode are right in one step — the app runs as
`hiring-radar` and cannot write a root-owned file. Keep `.before-restore` until the
dashboard looks right, then delete it. Anything ingested since the backup was taken is
gone; the next poll re-ingests whatever is still listed.

## Building the VM from nothing

`provision.sh` does steps 3–7 below — everything inside the VM. Steps 1, 2 and 8 create GCP
resources and need admin credentials, so they are run from the Mac, by hand, once.

Set these first (from the Mac):

```
PROJECT=hiring-radar-512318
ZONE=europe-west3-a
REGION=europe-west3
REPO=chandlershortlidge/hiring-radar
gcloud config set project "$PROJECT"
```

### 1. Project, APIs, static IP, firewall

```
gcloud services enable compute.googleapis.com iap.googleapis.com \
  iamcredentials.googleapis.com storage.googleapis.com

gcloud compute addresses create hiring-radar-ip --region "$REGION"
gcloud compute addresses describe hiring-radar-ip --region "$REGION" --format='value(address)'

gcloud compute firewall-rules create allow-web \
  --allow tcp:80,tcp:443 --source-ranges 0.0.0.0/0 --target-tags web
gcloud compute firewall-rules create allow-ssh-iap \
  --allow tcp:22 --source-ranges 35.235.240.0/20
```

Port 22 is open only to IAP's range; there is no `default-allow-ssh`. The hostname is the
static IP with dots turned into dashes plus `.sslip.io` — `34.159.223.190` →
`34-159-223-190.sslip.io`. sslip.io resolves it, which is enough for Caddy to get a Let's
Encrypt certificate without owning a domain. **The hostname is baked into the Caddyfile: a
new IP means a new hostname.**

### 2. The VM

```
gcloud compute instances create hiring-radar \
  --zone "$ZONE" --machine-type e2-micro \
  --image-family debian-12 --image-project debian-cloud --boot-disk-size 20GB \
  --tags web --address hiring-radar-ip \
  --metadata enable-oslogin=TRUE \
  --scopes https://www.googleapis.com/auth/cloud-platform
```

`enable-oslogin=TRUE` is what lets IAM decide who may log in (step 8 relies on it).
Then `gcloud compute ssh hiring-radar --zone "$ZONE" --tunnel-through-iap` and either run
`provision.sh` or steps 3–7 by hand.

### 3. Packages, swap, app user, directories

```
sudo apt-get update
sudo apt-get install -y git sqlite3 caddy        # caddy 2.6.2 is in bookworm
curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR=/usr/local/bin sh

sudo fallocate -l 1G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

sudo useradd --system --home /opt/hiring-radar --create-home --shell /usr/sbin/nologin hiring-radar
sudo install -d -o hiring-radar -g hiring-radar -m 750 /var/lib/hiring-radar
```

1 GB of swap: an e2-micro has 969 MB of RAM, and `uv sync` plus the running app fit only
with it. The DB directory is `750` so only the app user and root can read the database.

### 4. The code

```
sudo -u hiring-radar -H git clone https://github.com/$REPO.git /opt/hiring-radar/app
sudo -u hiring-radar -H uv --directory /opt/hiring-radar/app sync --frozen --no-dev
```

`web/dist` is **not** in git; the first deploy (or a hand-built tarball) puts it there.
Until then the API serves the JSON endpoints and returns 404 for the dashboard.

### 5. Secrets

```
sudo install -m 600 /dev/null /etc/hiring-radar.env
sudo tee /etc/hiring-radar.env >/dev/null <<'ENV'
ANTHROPIC_API_KEY=sk-ant-...
BRAVE_API_KEY=...
LANGSMITH_API_KEY=lsv2_...
HIRING_RADAR_DB=/var/lib/hiring-radar/hiring-radar.db
ENV
```

Root-only, loaded by the systemd units, never in git. `HIRING_RADAR_DB` belongs here and
not in the unit files so that a unit file can be committed as it stands.

`LANGSMITH_API_KEY` is optional and is the only switch for tracing — see
[Tracing the poll](#tracing-the-poll). Blank or absent, the poll runs exactly as it did
before HIR-160 and nothing is sent anywhere.

### 6. systemd

```
sudo install -m 644 /opt/hiring-radar/app/deploy/hiring-radar*.service \
  /opt/hiring-radar/app/deploy/hiring-radar*.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now hiring-radar hiring-radar-poll.timer hiring-radar-backup.timer
curl -fsS localhost:8000/api/stats >/dev/null && echo "api up"
```

The `curl` is not just a check: the first request creates the database file and applies
every migration.

### 7. Caddy

```
HASH=$(caddy hash-password --plaintext 'the-dashboard-password')
sudo sed "s|REPLACE_WITH_BCRYPT_HASH|$HASH|" \
  /opt/hiring-radar/app/deploy/Caddyfile > /etc/caddy/Caddyfile
sudo systemctl reload caddy
journalctl -u caddy -n 20 --no-pager        # watch the certificate get issued
```

The committed Caddyfile carries the placeholder, so this substitution is the only step that
knows the password. `basicauth` (one word) is Caddy 2.6 syntax; 2.8 and later renamed it
`basic_auth`.

### 8. Backups bucket and the CD deployer

```
gcloud storage buckets create "gs://$PROJECT-backups" --location "$REGION" \
  --uniform-bucket-level-access
gcloud storage buckets update "gs://$PROJECT-backups" \
  --lifecycle-file /opt/hiring-radar/app/deploy/gcs-lifecycle.json

gcloud iam service-accounts create github-deployer

NUM=$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')
gcloud iam workload-identity-pools create github --location=global \
  --display-name="GitHub Actions"
gcloud iam workload-identity-pools providers create-oidc hiring-radar-repo \
  --location=global --workload-identity-pool=github \
  --issuer-uri=https://token.actions.githubusercontent.com \
  --attribute-mapping='google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.ref=assertion.ref' \
  --attribute-condition="assertion.repository=='$REPO' && assertion.ref=='refs/heads/main'"

SA=github-deployer@$PROJECT.iam.gserviceaccount.com
gcloud iam service-accounts add-iam-policy-binding "$SA" \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$NUM/locations/global/workloadIdentityPools/github/attribute.repository/$REPO"
gcloud projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:$SA" \
  --role=roles/compute.viewer
gcloud projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:$SA" \
  --role=roles/iap.tunnelResourceAccessor
gcloud compute instances add-iam-policy-binding hiring-radar --zone "$ZONE" \
  --member="serviceAccount:$SA" --role=roles/compute.osAdminLogin
```

`workload_identity_provider` and `service_account` in `.github/workflows/ci.yml` must match
what this creates — the provider is named by project **number**, not id. The attribute
condition is the security boundary: only `main` of this repo can assume the account.
