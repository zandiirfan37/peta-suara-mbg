# PETA SUARA MBG

Platform Analitik Percakapan Publik — GEMASTIK 19.

Flask preview, without datasets or analytical claims. Edit `content.json` for text and `templates/index.html` for layout.

## Local

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/flask --app app run
```

Routes: `/`, `/healthz`, `/api/status`.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md). `render.yaml` specifies a Free Python web service. Connect the repository through the authenticated GitHub provider to enable deployment on commits to `main`.
