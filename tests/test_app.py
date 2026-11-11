import json
import unittest
from pathlib import Path

from app import app
from gunicorn.util import import_app


class DashboardTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_public_routes_and_assets(self):
        for path in ['/', '/healthz', '/api/status', '/api/dashboard', '/static/css/dashboard.css', '/static/js/dashboard.js']:
            with self.subTest(path=path):
                with self.client.get(path) as response:
                    self.assertEqual(response.status_code, 200)
        self.assertIn(b'PETA SUARA MBG', self.client.get('/').data)
        self.assertEqual(self.client.get('/healthz').json, {'status': 'ok'})
        self.assertIs(import_app('app:app'), app)
        self.assertEqual(self.client.get('/unknown').status_code, 404)

    def test_preview_cannot_masquerade_as_analysis(self):
        status = self.client.get('/api/status').json
        data = self.client.get('/api/dashboard').json
        self.assertFalse(status['analysis_available'])
        self.assertEqual(status['mode'], 'preview')
        self.assertIsNone(status['processed_count'])
        self.assertEqual(data['dataset']['brief_count'], 434463)
        self.assertIsNone(data['dataset']['processed_count'])
        self.assertEqual(len(data['groups']), 6)
        self.assertEqual(len({g['id'] for g in data['groups']}), 6)
        for group in data['groups']:
            self.assertIsNone(group['count'])
        for q in data['questions']:
            self.assertEqual(q['examples'], [])
            for field in ['rank', 'count', 'keywords']:
                self.assertIsNone(q[field])
            self.assertIn('contoh hipotesis', q['source'])
        self.assertEqual(data, json.loads(Path('static/data/dashboard.json').read_text()))


if __name__ == '__main__':
    unittest.main()
