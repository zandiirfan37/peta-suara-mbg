# Deployment — PETA SUARA MBG

## Stable production target

- URL: https://peta-suara-mbg.onrender.com/
- Health: https://peta-suara-mbg.onrender.com/healthz
- GitHub: https://github.com/zandiirfan37/peta-suara-mbg
- Branch: `main`
- Existing service hostname: `peta-suara-mbg.onrender.com`; internal Render service ID unavailable to agent.
- Baseline verified before 2.0: `/api/status` returned HTTP 200 and commit `b477ad4be719d81cd473114919a44bc3a3ab6867`.
- 2.0 source release: final commit SHA is in the release handoff and `git rev-parse HEAD`. Live deployed commit is exposed by `/api/status.version`.
- Auto-Deploy setting: blueprint requests On Commit; dashboard setting cannot be directly inspected without authenticated Render access. An observed automatic version change after push supports trigger behavior, but does not independently verify the dashboard setting.

**Reuse this service. Never delete/recreate it, alter the hostname or enable a paid instance.**

## Configuration retained

| Field | Value |
|---|---|
| Runtime / plan | Python 3 / Free |
| Repository | `zandiirfan37/peta-suara-mbg` |
| Branch / root | `main` / repository root (blank) |
| Build | `pip install -r requirements.txt` |
| Start | `gunicorn app:app` |
| Python variable | `PYTHON_VERSION=3.12.12` |
| Health path | `/healthz` |
| Auto-Deploy intended | On Commit |

No runtime dependency added. One compact synthetic fixture loads at import; count/share calculations use 1,080 rows in the browser. Assets are local, no CDN or online model required. App imports its explicit synthetic source, does no training or inference, and cannot enable real mode from a query parameter.

## Release and overnight updates

1. Work on a feature branch; preserve existing `main` until checks pass.
2. If changing scenarios, run `python3 scripts/generate_demo_data.py`.
3. Run unittest, Gunicorn config check, browser QA and inspect screenshots as in README.
4. Inspect staged files: only public application code, synthetic fixtures and documentation. PPT, private datasets, `.env`, keys and QA artifacts stay excluded.
5. Commit, fast-forward main, push once to `origin/main`.
6. Check the existing public service and version after Render finishes building.

Keep the same URL overnight. Do not edit files on Render as a persistence strategy; commit changes to GitHub. To roll back a bad deployment, use the existing service's previous successful deployment; do not replace the service.

## Public acceptance

Check `/`, `/healthz`, `/api/status`, `/api/dashboard`, CSS and both JS files for HTTP 200. Expect `mode: synthetic`, `synthetic_count: 1080`, `analysis_available: false`, `real_data_available: false`, `processed_count: null`, and the release commit. Homepage must show MODE SIMULASI — DATA SINTETIS. Check Gen Z → menu → Non-individual, filter propagation and real-mode lock in a browser.

If current version remains older, the 2.0 release is PENDING/UNVERIFIED, not LIVE UPDATED. Human/student: in the existing Render service inspect Events/Logs and Settings → Auto-Deploy. If needed, select **Manual Deploy → Deploy latest commit** in the same service. No credentials in chat.

## Free operation and limits

Free instances can sleep while idle and need a cold start. Open the submitted URL before presenting; wait for complete load. Filesystem writes are not durable storage. Check Render dashboard for current free usage and build limits. No paid resource is authorized. Reference: https://render.com/docs/free.

## Scientific boundary

All data in 2.0 is synthetic with persistent provenance. No competition processing total, Macro-F1 or real analytical result is implied. Real source registration, validation, privacy review and source-aware mode activation are separate future work; see DATA_SCHEMA.md. Presenter dialogue: DEMO_SCRIPT.md.
