# Deployment — PETA SUARA MBG

## Current state

- Public production URL: **NOT VERIFIED / not supplied to agent**.
- GitHub: https://github.com/zandiirfan37/peta-suara-mbg
- Branch: `main`.
- Render service name and identifier: **not verified**. Human Lead reports hosting was configured manually; it may already be live.
- Auto-Deploy: **not verified**; blueprint requests On Commit.
- Deployment status: **DEPLOYMENT_UNVERIFIED** until actual URL and deployed version are checked.
- Before this dashboard release: `3edc70ebadac4b9761132da8569b64d03d3c023d`.
- Current source commit: use `git rev-parse HEAD`; final release SHA is reported in the release handoff. Deployed commit remains unknown until `/api/status` confirms it.

**Never delete/recreate the existing service, change hostname, provision another service, or switch to a paid plan.** The submitted URL must remain stable.

## Existing service configuration

| Field | Required configuration |
|---|---|
| Type / plan | Python Web Service / Free |
| GitHub repository | `zandiirfan37/peta-suara-mbg` |
| Branch | `main` |
| Root directory | Repository root (blank) |
| Build | `pip install -r requirements.txt` |
| Start | `gunicorn app:app` |
| Python | `PYTHON_VERSION=3.12.12` as in existing blueprint |
| Health path | `/healthz` |
| Auto-Deploy | On Commit |

No changes to dependencies or hosting configuration are needed for the dashboard. Flask imports only a compact public metadata JSON; no full dataset or model is loaded. CSS/JS are served from the same app. Source PPT, screenshots, private datasets, and credentials are excluded from publication.

## Verification and recovery

The agent has authenticated GitHub but no Render browser tool, Render CLI/API credentials, or access to the Human Lead's authenticated Chrome session. Public GitHub deployments, commit statuses, checks and homepage metadata did not reveal a production URL during this audit. No URL was guessed or new service created.

Human/student: open the **existing** Render service → Settings, verify the repository, branch and **Auto-Deploy: On Commit**. After the release push, inspect Events/Logs for the release commit. If Auto-Deploy is off, use **Manual Deploy → Deploy latest commit** in that same service, then enable On Commit if appropriate. Use Free only. Copy the actual HTTPS URL to the agent for external verification. Do not share credentials.

Live acceptance (substitute the actual service origin):

```sh
curl --fail --show-error --max-time 120 "$ACTUAL_URL/"
curl --fail --show-error --max-time 120 "$ACTUAL_URL/healthz"
curl --fail --show-error --max-time 120 "$ACTUAL_URL/api/status"
curl --fail --show-error --max-time 120 "$ACTUAL_URL/api/dashboard"
```

Expect 200, PETA SUARA MBG dashboard, health `status: ok`, preview metadata, and `/api/status.version` matching the release commit. Also check CSS/JS, group selection and hypothesis dialog in the public browser. A working older landing page or an issued hostname alone does not verify this release. A pending build is PENDING, not LIVE.

If build/runtime fails, inspect Render logs. Preserve the existing service and URL; use its prior successful deployment as rollback if needed. Fix the failure on a feature branch and retest before publishing again.

## Overnight updates

Use a feature branch. Edit only intended public files. Run backend and browser checks in README, inspect the diff and ensure raw data/secrets are absent. Merge a verified release into `main`, then `git push origin main`. Do not push unfinished work to production.

JSON metadata is read once when the app imports; deploy/restart through the existing service after changes. Do not edit the Render filesystem as a content store. Future analytical data needs a separate offline validation and UI integration before leaving preview mode.

## Free-tier operation

Free hosting can sleep when idle, producing a cold start. Open the submitted URL ahead of the presentation and wait for the dashboard to load. Local writes are not durable storage. Check the service dashboard for current free usage limits and build/runtime status. No paid resources are authorized. See [Render Free](https://render.com/docs/free).

## Known blockers

1. Actual production URL, service ID, deploy status and Auto-Deploy setting are unavailable to the agent.
2. No source comments, predictions, topic outputs, gold set or evaluation evidence; analytic results remain unavailable.

Presenter guide: [DEMO_SCRIPT.md](DEMO_SCRIPT.md). Evidence audit: [DATA_AUDIT.md](DATA_AUDIT.md).
