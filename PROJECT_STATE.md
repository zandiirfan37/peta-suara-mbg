# Project state

Mission: PETA SUARA MBG 2.0 — visually redesigned, populated interactive jury demo. Human Lead explicitly authorized realistic synthetic data with persistent provenance and release to existing Render service.

Baseline: `b477ad4be719d81cd473114919a44bc3a3ab6867`, verified HTTP 200 on production `/api/status` before modification. Work on `feat/simulation-v2` before merge into `main`. URL fixed: https://peta-suara-mbg.onrender.com/. Never create another service or change hostname; Free only.

Completed: deterministic offline generation of 1,080 unique synthetic comments (seed 190726), six groups, eight illustrative topics, three platforms and July–September 2026. No actual source dataset/model/evaluation became available. Full PPT review retained in DATA_AUDIT.md; key claims rechecked against unchanged PPT hash.

UI: full editorial redesign with dark forest distribution panel, ranked topic bars, diverging normalized comparison, largest-gap summary, interactive 6×8 heatmap, immediate topic evidence dialog, contextual example explorer, platform/month filters, reset, search, 3/5 examples, pagination, copy SIM-ID, aggregate CSV and three-stage presenter mode with back/restart/exit. Policy question changes with topic and remains illustrative. Real mode disabled; synthetic provenance persistent.

Architecture: Flask/Gunicorn preserved, no production dependency added. Common source loader in data_source.py, pure source-neutral browser calculations in analytics.js; compact pre-generated demo.json. No model or large dataset startup. Missing real-source registration fails closed. DATA_SCHEMA.md records denominators and future validation requirements.

QA: backend routes/import/config, deterministic/unique records, catalog references and rejected invalid sources pass. Browser verifies 112 scopes and 576 group comparisons against independent Python arithmetic, actual UI filters, group/topic/cell selection, matching evidence IDs, pagination/search/copy, reset, native dialogs, guided mode and export. Responsive screenshots inspected at 1440×900, 1366×768, 1920×1080, mobile 375×812; additional overflow/close tests at 812×375 and 768×1024. Visual review led to wider mobile filters, guide in layout rather than covering charts, immediate evidence dialog and improved heatmap contrast. Screenshots/report under ignored evidence/v2.

Scientific state: SIMULATION ONLY. All numeric UI values derive from synthetic rows; taxonomy and labels are illustrative, no Macro-F1 or true ages. Brief size 434,463 is separately attributed in methodology. Source data, models, gold labels, topic outputs and evaluation evidence remain missing. Original PPT excluded and unchanged.

Release: commit/push only after final verification. Live commit must match `/api/status.version` before claiming updated production. Render CLI/authenticated browser unavailable; use public HTTP/browser verification. Internal service ID and dashboard Auto-Deploy setting not directly inspectable.

Next boundary: verify 2.0 at the stable public URL, then rehearse DEMO_SCRIPT.md. Future scientific improvement is independently validated source outputs; never treat synthetic differences as MBG findings.
