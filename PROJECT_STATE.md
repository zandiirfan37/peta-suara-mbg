# Project state

Mission: jury-facing PETA SUARA MBG interactive companion for GEMASTIK 19. Dashboard implementation is separate from completing the scientific analysis.

Authority/scope: Human Lead authorized build, local QA and public-safe push to existing GitHub main. Preserve PPT and existing Render hostname; no service creation or paid infrastructure.

Baseline: main `3edc70ebadac4b9761132da8569b64d03d3c023d`. Implemented on feature branch `feat/jury-demo` before verified merge/publication.

Completed: all 15 PPT slides and notes extracted; key embedded diagrams inspected. DATA_AUDIT.md records method proposals and inconsistencies. New editorial responsive dashboard includes six-group selection, four source-attributed PPT hypothesis drawers, comparison selectors with unavailable/same-group guards, denominator definition, evidence/method panel, four-step presentation guide and no-JS fallback. Existing health/status routes and Gunicorn entrypoint preserved; compact `/api/dashboard` added. No production dependency added.

Scientific status: PREVIEW. Brief describes 434,463 comments, but no original CSV, predictions, topic assignments, model, label set or evaluation report exists in this project. Counts are null, no fabricated distributions/quotes/IDs. Hypotheses are not findings. See DATA_AUDIT.md for availability matrix and DEMO_SCRIPT.md for exact grounded script.

Local verification: syntax, Flask/Gunicorn import/config, public routes/assets, preview-state integrity, all six selections/four drawers, comparison guards, demo completion/exit, no-JS fallback and browser console passed. Responsive QA: 1366×768, 1920×1080, 768×1024, 375×812, no horizontal overflow, modal close visible. Screenshots inspected for laptop, mobile and evidence drawer; untracked screenshots/report in evidence/browser. Tests reproducible from README.

External state: GitHub public repository https://github.com/zandiirfan37/peta-suara-mbg. Render configured manually per Human Lead, possibly live. No authenticated Render tooling or accessible Chrome session. GitHub deployment/status metadata did not expose a public URL. Exact URL requested asynchronously. Production deployment, commit and Auto-Deploy remain UNVERIFIED; never assume service absence or create duplicates.

Next: obtain actual existing Render URL and verify dashboard, HTTP routes, release commit and On Commit setting. Highest scientific improvement: validate authorized source CSVs and real classification/topic outputs offline, then integrate compact verified aggregates. Do not infer demographics as identity.
