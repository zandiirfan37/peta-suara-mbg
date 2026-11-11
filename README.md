# PETA SUARA MBG 2.0

Interactive GEMASTIK 19 jury demo: **Kenali suara. Pahami prioritas.**

Production: https://peta-suara-mbg.onrender.com/ — existing service and hostname preserved. GitHub: https://github.com/zandiirfan37/peta-suara-mbg, branch `main`.

## Scientific disclosure

**MODE SIMULASI — DATA SINTETIS.** All 1,080 comments, dates, platform assignments, category assignments and scenario differences are generated fixtures, not scraped data or competition results. Taxonomy is illustrative; labels are not inferred ages. No trained classifier, Macro-F1, confidence, causal or policy-performance claim is made. The 434,463 total is separately identified in the methodology dialog as a competition-brief figure, never as records processed.

The real-analysis mode is disabled: no validated source outputs exist. [DATA_AUDIT.md](DATA_AUDIT.md) records the PPT and original evidence audit. [DATA_SCHEMA.md](DATA_SCHEMA.md) documents source separation and future integration.

## Three analytical clicks

1. **Gen Z** in Peta kelompok: all eight topic ranks update; comparison A follows.
2. **Mutu & variasi menu**: a dialog shows matching synthetic comments with SIM-ID, platform, date, group and topic. Close with × or Escape.
3. **Bandingkan dengan Non-individual**: compare within-group topic proportions, with calculated A − B percentage-point differences and the largest contrast.

Use **Mulai Demo 60 Detik** for presentation mode: header controls/metrics collapse, an in-flow guided toolbar supports Next/Back/Restart/Exit. It does not autoplay or scroll on its own; “Lihat area” is an explicit navigation action. Full script and jury Q&A: [DEMO_SCRIPT.md](DEMO_SCRIPT.md).

## Working features

- Six-group distribution chart; selected states and All control.
- Eight ranked topic bars with exact counts and within-group percentages.
- Two-group diverging comparison, zero-denominator and same-group guards.
- Six × eight intensity matrix; click a cell to select both group and topic.
- Platform and July/August/September filters update KPIs, charts, denominators and evidence together. Topic/search selection affects evidence without changing comparison denominators.
- Evidence dialog and explorer: 3/5 samples, previous/next, search, copy ID and useful empty states.
- Reset, three-step presenter guide, responsive views, keyboard dialogs and reduced-motion support.
- CSV aggregate export with synthetic provenance, seed, filter and denominators on every row. No private raw data.
- Persistent simulation disclosure, separate disabled real mode, transparent methodology and a topic-dependent illustrative policy question.

## Run and verify

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
python3 scripts/generate_demo_data.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/gunicorn --check-config app:app
.venv/bin/gunicorn --bind 127.0.0.1:5067 --workers 1 app:app
```

Open http://127.0.0.1:5067/. Production entrypoint remains `gunicorn app:app`. Runtime dependencies remain Flask and Gunicorn; no CDN, model initialization, external API, database, training or paid resource.

Against the already serving local app:

```sh
uv run tests/browser_smoke.py --out evidence/v2
```

Requires the QA-only Playwright package (resolved by uv) and installed Chromium; set `PLAYWRIGHT_BROWSERS_PATH` if needed. No browser download or package is required by the production app. Screenshots/report remain ignored under `evidence/`.

QA includes three backend/data tests, 112 filter/group scopes and 576 comparisons against independent Python counts; source ID checks, actual filter interactions, heatmap, evidence pagination/search/copy, reset, dialogs, guide and CSV. Viewports: 1440×900, 1366×768, 1920×1080, 375×812, 812×375 and 768×1024.

## Source layout

- `scripts/generate_demo_data.py`: deterministic seed `190726`, 1,080 unique synthetic records.
- `static/data/demo.json`: compact committed demo fixture, ~310 KB.
- `data_source.py`: common-schema validation and explicit source loader; no mixed source kinds.
- `static/js/analytics.js`: source-neutral, pure count/share/ranking/comparison/evidence functions.
- `static/js/dashboard.js`: UI state and interactions; all numeric analytics derive from actual fixture rows.
- `templates/index.html`, `static/css/dashboard.css`: responsive UI with local assets and web-safe typography.

Routes: `/`, `/healthz`, `/api/status`, `/api/dashboard`. Status reports `mode: synthetic`, `synthetic_count: 1080`, real outputs unavailable and Render Git commit when supplied. Dashboard endpoint has `X-Data-Provenance: synthetic`.

Do not modify or publish the reference PPT. Do not enter plausible “real” numbers into demo files. Regeneration changes only the fixture when the generator changes; rerun QA before release. Production JSON loads once at import, so source updates require a deployment of the **same** Render service. See [DEPLOYMENT.md](DEPLOYMENT.md).
