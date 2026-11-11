import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template

app = Flask(__name__)
CONTENT_PATH = Path(__file__).with_name('content.json')


def load_content():
    return json.loads(CONTENT_PATH.read_text(encoding='utf-8'))


@app.get('/')
def index():
    return render_template('index.html', content=load_content())


@app.get('/healthz')
def healthz():
    return jsonify(status='ok'), 200


@app.get('/api/status')
def status():
    content = load_content()
    return jsonify(name=content['title'], status=content['status'],
                   analysis_available=False,
                   version=os.environ.get('RENDER_GIT_COMMIT', 'local'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')))
