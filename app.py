import os
from flask import Flask, jsonify, render_template
from data_source import load_source

app = Flask(__name__)
# Compact, offline-generated demo. Production performs no inference or training.
DASHBOARD = load_source('synthetic')
VERSION = os.environ.get('RENDER_GIT_COMMIT', 'local')


@app.get('/')
def index():
    return render_template('index.html', dashboard=DASHBOARD, version=VERSION)


@app.get('/api/dashboard')
def dashboard():
    response = jsonify(DASHBOARD)
    response.headers['X-Data-Provenance'] = 'synthetic'
    return response


@app.get('/healthz')
def healthz():
    return jsonify(status='ok'), 200


@app.get('/api/status')
def status():
    return jsonify(name='PETA SUARA MBG', status='Simulasi interaktif',
                   analysis_available=False, real_data_available=False,
                   mode='synthetic', synthetic_count=len(DASHBOARD['records']),
                   processed_count=None, schema_version=1,
                   source_seed=DASHBOARD['source']['seed'], version=VERSION)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', '5000')))
