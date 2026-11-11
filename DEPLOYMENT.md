# Deployment — PETA SUARA MBG

## Current verified state

- Public HTTPS URL: **NONE — no Render service or URL has been verified by this agent**.
- GitHub repository: https://github.com/zandiirfan37/peta-suara-mbg
- Render service identifier: **NONE — requires authenticated Render access**.
- Intended service name: `peta-suara-mbg` (use a suffix only if unavailable).
- Deployment branch: `main`.
- Recovered application commit: `4337b82e91252634aad5b696ac486de12085f7b9`; confirmed on GitHub `main` during recovery.
- Runtime: Python 3.12.12.
- Plan: **Free only**.
- Build: `pip install -r requirements.txt`.
- Start: `gunicorn app:app`.
- Health check: `/healthz`.
- Auto deploy: configured as `commit` in `render.yaml`; **not yet verified in Render**.

## Human action needed: create service through connected GitHub

1. Open https://dashboard.render.com and check for an existing suitable PETA SUARA MBG service before creating one. Reuse it if present.
2. The Human Lead has already logged into Render through GitHub and is on **Create a new Service**. Select **Web Services → New Web Service → Git Provider → GitHub**, then connect `zandiirfan37/peta-suara-mbg`. If the repository is missing, configure the GitHub connection to grant Render access to this repository. Select it through the connected provider, rather than entering a public Git URL. No repeat Render login is needed.
3. Name `peta-suara-mbg`; branch `main`; language Python 3; region Singapore; root directory blank.
4. Build command `pip install -r requirements.txt`; start command `gunicorn app:app`; instance type **Free**.
5. Set health check path `/healthz`, environment variable `PYTHON_VERSION=3.12.12`, and Auto-Deploy **On Commit** in advanced settings or service Settings.
6. Click **Deploy Web Service**. Wait for the deployment to become Live and inspect logs for failures.
7. Copy the actual HTTPS URL shown by Render and share it with the agent for live verification. Record the actual service ID and URL here after verification. Never infer the URL from the name.

Alternatively use New → Blueprint with the connected GitHub repository to apply `render.yaml`; inspect that the proposed web service plan is Free before deploying.

## Recovery verification — 2026-11-11

Existing application preserved. Python syntax, Flask import, Gunicorn `app:app` import, homepage title, and HTTP 200 for all three routes passed locally; both API routes returned JSON. GitHub repository is public and remote `main` matched the recovered application commit. No browser automation tool or accessible authenticated Chrome session is available to the agent; no Render CLI, standard CLI configuration, or Render environment credentials were found. Render service existence, deployment status, actual hostname, and Auto-Deploy setting therefore remain unverified. The next action is the manual service connection/deployment above, followed by sharing Render's actual HTTPS URL for external verification.

## Overnight updates — preserve the same URL

Edit `content.json` for text and `templates/index.html` for the homepage. Change `app.py` only for route behavior. Do not add private datasets or credentials.

```sh
.venv/bin/python -m py_compile app.py
.venv/bin/python -c 'from app import app; c=app.test_client(); assert all(c.get(p).status_code == 200 for p in ["/", "/healthz", "/api/status"])'
git add app.py content.json templates/index.html requirements.txt render.yaml README.md DEPLOYMENT.md PROJECT_STATE.md .gitignore
git commit -m "Update public preview content"
git push origin main
```

Keep the existing Render service and its hostname. Deploy future commits to that service. Do not delete/recreate the service or change its assigned domain after submitting the PPT.

## Verify a successful deployment

In Render, confirm the latest deploy is **Live**, its commit matches GitHub `main`, and Settings → Auto-Deploy is **On Commit**. Inspect build and runtime logs.

Use the actual Render URL in place of ACTUAL_URL:

```sh
curl --fail --show-error --max-time 120 https://ACTUAL_URL/healthz
curl --fail --show-error --max-time 120 https://ACTUAL_URL/
curl --fail --show-error --max-time 120 https://ACTUAL_URL/api/status
```

Check HTTP 200, homepage text `PETA SUARA MBG`, and `/api/status` version matching the deployed commit. The health endpoint reports process health; analysis remains unavailable by design during preview.

## Free tier limitations

Render Free services sleep after 15 minutes without inbound traffic. A request starts the service again, usually taking about one minute. Open the submitted URL shortly before the presentation. Local filesystem changes are ephemeral; commit content updates to GitHub. Free instance hours, bandwidth, and build limits can suspend service or block builds. No paid resources are authorized.

Official references: https://render.com/docs/deploy-flask, https://render.com/docs/blueprint-spec, https://render.com/docs/free.
