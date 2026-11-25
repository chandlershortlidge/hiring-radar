# Operating the VM

Where hiring-radar runs: one GCP Compute Engine VM, project `hiring-radar-512318`, zone
`europe-west3-a`, instance `hiring-radar` (e2-micro, Debian 12, 20 GB disk). Port 22 is
reachable only from Google's IAP range, so SSH goes through IAP. The dashboard is behind
Caddy (HTTPS + basic auth) at `hiringradar.app`. Merging to `main` deploys.

Decided in HIR-29; design in [DECISIONS.md](../DECISIONS.md) (2026-10-21), final shape of
the setup in the 2026-11-01 entry.

## What is in this folder

| File | What it is |
|---|---|
| `provision.sh` | Builds the VM's software side from nothing. Safe to re-run. |
| `hiring-radar.service` | The API process (systemd unit, copied from the VM). |
| `hiring-radar-poll.service` / `.timer` | The Europe poll, 07:00 Europe/Berlin (`poll --region europe`). |
| `hiring-radar-poll-us.service` / `.timer` | The US poll, 07:00 America/New_York (`poll --region us`, HIR-369). |
| `hiring-radar-backup.service` / `.timer` | The 03:30 Europe/Berlin backup. |
| `hiring-radar-caretaker.service` / `.timer` | The 10:00 Europe/Berlin caretaker. |
| `install-units.sh` | Makes the unit files in `/etc/systemd/system` match the ones here. Run by every deploy and by `provision.sh`. |
| `Caddyfile` | HTTPS + basic auth in front of the API, except `/mcp`, which is open. The bcrypt hash is a placeholder. |
| `backup.sh` | What the backup unit runs: snapshot → integrity check → gzip → bucket. |
| `remote-deploy.sh` | What the GitHub deploy job runs on the VM. |
| `gcs-lifecycle.json` | Bucket rule: delete backups older than 30 days. |

The unit files and the Caddyfile are verbatim copies of what is in `/etc` on the VM (the
one exception is the Caddyfile's password hash), so `diff` against `/etc` says whether the
VM has drifted from the repo.

**Every deploy applies the unit files** (HIR-310): `remote-deploy.sh` runs
`install-units.sh`, which compares each `hiring-radar*.service` and `hiring-radar*.timer`
here with the one in `/etc/systemd/system`, installs those that differ or are missing, and
prints one line per file in the deploy log (`same` or `installed`, with why). So a merged
change to a schedule, or a new timer, is live after the deploy of that commit, with nothing
to do by hand. The Caddyfile is the exception: no deploy touches it, because the VM's copy
holds the real password hash; `provision.sh` writes it.

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
| Daily polls | Europe: `hiring-radar-poll.timer` → `hiring-radar-poll.service`, 07:00 Europe/Berlin. US: `hiring-radar-poll-us.timer` → `hiring-radar-poll-us.service`, 07:00 America/New_York (13:00 Berlin). Each fetches only its region's feeds; company boards are in both (HIR-369, DECISIONS 2026-11-19) |
| Nightly backup | `hiring-radar-backup.timer` → `backup.sh`, 03:30 Europe/Berlin, to `gs://hiring-radar-512318-backups/db/` |
| Caretaker | `hiring-radar-caretaker.timer` → `python -m app caretaker`, 10:00 Europe/Berlin: checks every job source, logs to `caretaker_log`, posts the Monday summary to Linear when `LINEAR_API_KEY` is set (HIR-257). The same post starts with the week's pull requests (needs you, merged, sent back and fixed), read from GitHub's public API and the checkout's git history, with no token (HIR-264). Then the robot visitor's week (what broke on the live site, what was rolled back, what was fixed), read from its Linear tickets with the same `LINEAR_API_KEY`, one read-only request a week; a break that came back after two fixes is listed above everything else (HIR-260). It never edits `config/feeds.json` on the server and has no GitHub credential: each morning's fixes (pause a dead board, switch a moved one, switch a recovered one back on) are filed as one Linear ticket, "Caretaker: job-source fixes for <day>", which the agents turn into a reviewed pull request with `python -m app caretaker apply-fixes`. A collection that did not run or failed everywhere is re-run once that day, by the caretaker itself, as the same user with the same command as the 07:00 poll (HIR-261) |

`systemctl list-units | grep hiring` shows the exact unit names.

**Checks run on the Mac arrive over this SSH login** (HIR-294). The caretaker's miss count
reads this database, so `python -m app check` on the Mac ends by piping its check log to
`python -m app receive-checks` here, run as `hiring-radar` (`app/send_checks.py` holds the
exact command). It stores only the checks this database does not have, so a repeat is
harmless. `HIRING_RADAR_SEND_CHECKS=0` on the Mac switches it off.

## Is it healthy?

```
curl -s localhost:8000/api/stats | grep -o '"last_updated":"[^"]*"'   # moves on every ingest
systemctl list-timers --all | grep hiring                           # LAST / NEXT for poll + backup
journalctl -u hiring-radar-poll --since today --no-pager            # today's Europe poll log
journalctl -u hiring-radar-poll-us --since today --no-pager         # today's US poll log
```

`last_updated` is `max(last_seen)` across jobs: it advances whenever the poll ingests anything,
even with no new jobs. A healthy day shows it at ~06:00Z after the Europe poll and again around
11:00–12:00Z after the US one. Each poll log starts with a `region` line naming the cities it
covers, and ends with a `TOTAL`
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

The LangSmith SDK has its own tracing switch, `LANGSMITH_TRACING=true`, which `run()` now
turns on by itself whenever the key is set (HIR-238) — the 10 Nov VM needed both, with the
key alone silently tracing nothing. If `LANGSMITH_TRACING=true` is already in
`/etc/hiring-radar.env` from that workaround, it is harmless to leave; it just no longer
does anything.

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
frontend build on every push and PR; on a push to `main` that passes both, the `release`
job runs `.github/workflows/site-watch.yml`: deploy the commit (`deploy.yml`), then the
robot visitor clicks through the live site (HIR-258). If the robot fails, the site is
rolled back to the last commit it passed (the `site-good` git tag) by deploying that
commit the same way, and a Linear ticket is filed. If the rolled-back site fails too, the
robot's second report picks the ticket (HIR-359): when no path passed on it, the ticket is
"Site down and rollback failed", Urgent and assigned to Chandler; when some path passed,
the site is up and the deploy is probably not the cause, so each path that still fails
gets an ordinary autopilot ticket that says so. The whole release is serialized
(`concurrency: release`, no cancel-in-progress), so a second merge waits until the first
is deployed and watched.

A rollback puts the old code back but not the old database: a migration the broken
commit applied stays applied. Most migrations only add, and old code runs on the newer
schema; a migration that rebuilds, drops or renames something (007, 008, 015 and 016 did)
can leave the old code unable to read it. Then the robot fails on the rolled-back site
too; when it fails every path there, that is the "rollback failed" ticket that goes
straight to Chandler.

The deploy job (`.github/workflows/deploy.yml`):

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
   fetched (and the commit itself, when it is a rollback target or a drill commit not on
   `main`) and `git reset --hard` to it, then
   `sudo bash deploy/remote-deploy.sh /tmp/web-dist.tgz`. `remote-deploy.sh` takes a
   backup first, then `uv sync --frozen --no-dev`, unpacks `web/dist`, installs any unit file
   that differs from the VM's (`install-units.sh`, below), restarts the API, and
   polls `/api/stats` for up to 60 s. If the app does not answer it exits non-zero and
   prints the last 30 journal lines, so the workflow goes red. A tarball that arrives
   truncated fails `tar -xzf` in the same script, so that is loud too.

   The connection is made by `deploy/vm-ssh.sh` (HIR-317), the one way a workflow logs in
   to the VM. Each job registers a new throwaway key with OS Login and connects seconds
   later, and now and then the VM refuses it ("Permission denied (publickey)"). The script
   tries a refused login again, 3 tries 15 seconds apart, and the log shows
   `server login: try N of 3`. It tries nothing else again: a deploy that started and
   failed stays failed. Three refusals exit with code 75. The job fetches the script from
   the workflow's own commit into `.deploy-tools/`, because a rollback deploys an older
   commit that may not have it.

When the robot fails after a deploy and the rollback job itself fails, the ticket is
"Deploy failed the robot visitor and the rollback did not run": the site is still on the
new version, and the ticket says whether the rollback could not log in or failed later.

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

**A deploy installs the unit files and touches nothing else in `/etc`, and never the
database.** Just before the restart, `install-units.sh` makes the units in
`/etc/systemd/system` match the commit being deployed and logs one line per file:

```
→ systemd units
same       hiring-radar.service
installed  hiring-radar-poll.timer (differed from the server's copy)
installed  hiring-radar-caretaker.timer (was not on the server)
units: 7 compared, 2 installed
```

When something was installed it reloads systemd, enables every timer (so a new one starts
ticking) and restarts each changed timer so the new time applies at once; restarting a
timer does not run its job. It never starts a job's service, and the API's restart is the
deploy's own next step. If it fails, the deploy stops there, red, with the old API still
running. Three limits: a unit deleted from the repo is not removed from the VM
(`systemctl disable --now` it and delete the file by hand); a rollback to a commit from
before HIR-310 leaves the units as the newer commit set them; and the Caddyfile and
`/etc/hiring-radar.env` are still changed only by hand or by `provision.sh`.

**The VM installs wheels only — it has no compiler.** `.python-version` pins the Python
every environment uses (3.13, the same one CI runs), and `requires-python` in
`pyproject.toml` caps the range, because a package without a wheel for the running Python
is built from source and `cc` does not exist on the instance. Until HIR-235 there was no
pin, so `uv` on the VM picked the newest Python it could find — 3.15, days old — and the
first dependency without a 3.15 wheel failed the deploy after the backup and before the
restart. `tests/test_deploy_install_set.py` now reads `uv.lock` and fails if anything in
the `--no-dev` set has no wheel for the pinned Python on linux. Raising the pin means
checking that test still passes; bumping it past the cap means raising the cap too.

## Deploying by hand

If Actions is unavailable, the same three lines from the Mac:

```
cd web && npm ci && npm run build && tar -czf ../web-dist.tgz dist && cd ..
gcloud compute scp web-dist.tgz hiring-radar:/tmp/web-dist.tgz --zone europe-west3-a --tunnel-through-iap
gcloud compute ssh hiring-radar --zone europe-west3-a --tunnel-through-iap --command \
  'sudo -u hiring-radar -H git -C /opt/hiring-radar/app pull --ff-only &&
   sudo bash /opt/hiring-radar/app/deploy/remote-deploy.sh /tmp/web-dist.tgz'
```

## Caddy: apply `deploy/Caddyfile` by hand

No deploy touches the web server's config (the server's copy holds the password hash; the
repo's does not), so a change to `deploy/Caddyfile` is applied by hand, after the deploy
of the merge that needs it. This keeps the VM's current password hash and takes the rest
from `deploy/Caddyfile`. Back up first, under a name that says what the change was.

```
gcloud compute ssh hiring-radar --zone europe-west3-a --tunnel-through-iap
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.before-<change>
HASH=$(sudo awk '$1 == "chandler" {print $2}' /etc/caddy/Caddyfile)
sudo sed "s|REPLACE_WITH_BCRYPT_HASH|$HASH|" /opt/hiring-radar/app/deploy/Caddyfile > /tmp/Caddyfile
sudo caddy validate --config /tmp/Caddyfile --adapter caddyfile \
  && sudo install -m 644 -o root -g root /tmp/Caddyfile /etc/caddy/Caddyfile \
  && sudo systemctl reload caddy
rm /tmp/Caddyfile
```

Check from the Mac: the dashboard still asks for the password, and `/mcp` answers without it.

```
curl -s -o /dev/null -w '%{http_code}\n' https://hiringradar.app/          # 401
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://hiringradar.app/mcp \
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -H 'mcp-protocol-version: 2025-06-18' -d '{"jsonrpc":"2.0","id":1,"method":"ping","params":{}}'   # 200
```

Undo: `sudo cp /etc/caddy/Caddyfile.before-<change> /etc/caddy/Caddyfile && sudo systemctl reload caddy`.

Add it to Claude: `claude mcp add --transport http hiring-radar https://hiringradar.app/mcp`,
or in claude.ai, Settings → Connectors → Add custom connector, with that URL.

## The move to hiringradar.app (HIR-458): two stages around the merge

The uptime check and the robot visitor read one address: the old one before the merge, the
new one after it. So the server answers at both names across the merge.

1. **Before the merge**, the new name is added next to the old one, nothing redirected:
   ```
   sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.before-domain
   umask 077
   { sudo sed '1s|^34-159-223-190\.sslip\.io {|hiringradar.app, 34-159-223-190.sslip.io {|' /etc/caddy/Caddyfile
     printf '\nwww.hiringradar.app {\n\tredir https://hiringradar.app{uri} 301\n}\n'; } > /tmp/Caddyfile
   grep -q '^hiringradar.app, 34-159-223-190.sslip.io {' /tmp/Caddyfile \
     && sudo caddy validate --config /tmp/Caddyfile --adapter caddyfile \
     && sudo install -m 644 -o root -g root /tmp/Caddyfile /etc/caddy/Caddyfile \
     && sudo systemctl reload caddy
   rm /tmp/Caddyfile
   ```
2. **After the merge's "Deploy and watch" run is green**, apply `deploy/Caddyfile` with the
   recipe above (`<change>` = `redirect`). The old address then forwards everything to
   `https://hiringradar.app` with the path kept, except `/mcp`, which it still serves so a
   Claude connected there keeps working.

The old address stays until 31 Jan 2027 (decisions/2026-11-25-hir-458-hiringradar-app.md).

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

sudo systemctl stop hiring-radar-poll.timer hiring-radar-poll-us.timer hiring-radar
sudo mv /var/lib/hiring-radar/hiring-radar.db /var/lib/hiring-radar/hiring-radar.db.before-restore
sudo rm -f /var/lib/hiring-radar/hiring-radar.db-wal /var/lib/hiring-radar/hiring-radar.db-shm
sudo install -o hiring-radar -g hiring-radar -m 644 "/tmp/${BK%.gz}" \
  /var/lib/hiring-radar/hiring-radar.db
sudo systemctl start hiring-radar hiring-radar-poll.timer hiring-radar-poll-us.timer

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

Port 22 is open only to IAP's range; there is no `default-allow-ssh`. The site's name is
`hiringradar.app` (Cloudflare Registrar; HIR-458): an `A` record for `@` pointing at the
static IP and a `CNAME` for `www`, both **DNS only** (grey cloud) so Caddy gets its own
Let's Encrypt certificate. A new IP means changing the `A` record. Before HIR-458 the
name was the IP with dots as dashes on sslip.io, which now only forwards.

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
sudo bash /opt/hiring-radar/app/deploy/install-units.sh   # copies the units, enables every timer
sudo systemctl enable --now hiring-radar
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

`workload_identity_provider` and `service_account` in `.github/workflows/deploy.yml` must match
what this creates — the provider is named by project **number**, not id. The attribute
condition is the security boundary: only `main` of this repo can assume the account.
