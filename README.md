# PETA SUARA MBG

Interactive companion to GEMASTIK 19 PPT v5, Universitas Airlangga. Lightweight Flask + Gunicorn + local CSS/JavaScript; no CDN, model API, training, or external assets at runtime.

**Current release: evidence-aware preview.** The repository contains the presentation but no source CSVs, predictions, topic outputs, or evaluation reports. Dataset size 434,463 is attributed to the brief. All analytical counts are unavailable, not zero. See [DATA_AUDIT.md](DATA_AUDIT.md).

## Present in one minute

1. Open the existing submitted production URL and allow Render's cold start.
2. Click **Gen Z**: selected group updates topic context and comparison A.
3. Click **Keamanan pangan**: inspect the PPT hypothesis and verification plan, then Escape.
4. Choose **Non-individual** as comparison B: the dashboard explains why numerical comparison requires evidence.
5. Optional **Lihat kesiapan bukti** reveals methods and missing artifacts. **Mulai demo 60 detik** provides a manual guide.

Exact dialogue, timing, grounded jury answers, and fallback: [DEMO_SCRIPT.md](DEMO_SCRIPT.md). Do not present this as completed analytics.

## Feature states

| Working now | Scientific state |
|---|---|
| Six-category selector, contextual topic panel | PREVIEW: no group distributions |
| Four PPT hypothesis / verification drawers | PREVIEW: no measured ranks, keywords or source comments |
| Two comparison selectors and same-group guard | UNAVAILABLE: numeric comparison disabled |
| Methods, denominator definition, evidence matrix | REAL: source-attributed documentation |
| Four-step demo guide, Escape / close / focus return | REAL: interface behavior |
| Platform / month filters, trend, export | UNAVAILABLE: intentionally omitted without data |

The hypotheses are identical for all groups; selection is context, not evidence of group interest. True age cannot be verified from comment text alone.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/gunicorn --bind 127.0.0.1:5067 app:app
```

Open `http://127.0.0.1:5067/`. Production entrypoint remains `gunicorn app:app`. No paid resource or model initialization is required.

Routes: `/`, `/healthz`, `/api/status`, `/api/dashboard`. Status includes `analysis_available: false`, `mode: preview`, `processed_count: null`, and Render commit when supplied. `/api/dashboard` exposes only small public metadata, never datasets or credentials.

## Verification

```sh
.venv/bin/python -m py_compile app.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/gunicorn --check-config app:app
# Against the already running local server; requires uv and installed Chromium:
uv run tests/browser_smoke.py --url http://127.0.0.1:5067/ --out evidence/browser
```

Browser checks cover all six groups, all four hypothesis drawers, modal close / Escape / focus, comparison guards, guided tour, no-JS fallback, console errors and overflow at 1366×768, 1920×1080, 768×1024, 375×812. Set `PLAYWRIGHT_BROWSERS_PATH` if Chromium is stored elsewhere. QA results and screenshots stay untracked under `evidence/`.

## Content and release

- `static/data/dashboard.json`: public brief metadata, category definitions and PPT hypothesis plans. Missing scientific values must remain `null`; changing them requires an independently verified data integration.
- `templates/index.html`, `static/css/dashboard.css`, `static/js/dashboard.js`: interface.
- `content.json`: legacy preview metadata consumed by `/api/status` for compatibility.
- Original PPT is local reference only and excluded from Git; do not overwrite it.

No analytics-data ingestion is implemented. Audit and preprocess real outputs offline before adding aggregates or redacted evidence; the preview UI will need a verified integration, not just a status toggle.

[DEPLOYMENT.md](DEPLOYMENT.md) explains release to the **existing** Render service. Preserve its hostname. Live URL and Auto-Deploy remain unverified until observed.
