import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template

app = Flask(__name__)
CONTENT_PATH = Path(__file__).with_name('content.json')
DASHBOARD_PATH = Path(__file__).parent / 'static' / 'data' / 'dashboard.json'
# Small public metadata only; no model or source dataset is loaded at startup.
DASHBOARD = json.loads(DASHBOARD_PATH.read_text(encoding='utf-8'))


def load_content():
    return json.loads(CONTENT_PATH.read_text(encoding='utf-8'))


@app.get('/')
def index():
    return render_template('index.html', dashboard=DASHBOARD)


@app.get('/api/dashboard')
def dashboard():
    return jsonify(DASHBOARD)


@app.get('/healthz')
def healthz():
    return jsonify(status='ok'), 200


@app.get('/api/status')
def status():
    content = load_content()
    return jsonify(name=content['title'], status=content['status'],
                   analysis_available=False,
                   mode=DASHBOARD['mode'],
                   processed_count=DASHBOARD['dataset']['processed_count'],
                   version=os.environ.get('RENDER_GIT_COMMIT', 'local'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')))
