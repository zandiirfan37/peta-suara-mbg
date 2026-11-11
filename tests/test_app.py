import copy
import json
import unittest
from collections import Counter
from pathlib import Path

from app import app, DASHBOARD
from data_source import validate_source, load_source
from gunicorn.util import import_app
from scripts.generate_demo_data import generate


class DashboardTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_routes_and_provenance(self):
        for path in ['/', '/healthz', '/api/status', '/api/dashboard', '/static/css/dashboard.css', '/static/js/dashboard.js', '/static/js/analytics.js']:
            with self.subTest(path=path), self.client.get(path) as r:
                self.assertEqual(r.status_code, 200)
        page = self.client.get('/').get_data(as_text=True)
        self.assertIn('MODE SIMULASI — DATA SINTETIS', page)
        self.assertIn('Bukan hasil analisis resmi dataset lomba', page)
        self.assertEqual(self.client.get('/healthz').json, {'status': 'ok'})
        self.assertIs(import_app('app:app'), app)
        self.assertEqual(self.client.get('/unknown').status_code, 404)
        self.assertEqual(self.client.get('/api/dashboard').headers['X-Data-Provenance'], 'synthetic')
        self.assertEqual(self.client.get('/api/dashboard').json, DASHBOARD)
        s = self.client.get('/api/status').json
        self.assertEqual(s['mode'], 'synthetic')
        self.assertFalse(s['analysis_available'])
        self.assertFalse(s['real_data_available'])
        self.assertIsNone(s['processed_count'])
        self.assertEqual(s['synthetic_count'], 1080)

    def test_deterministic_unique_valid_records(self):
        self.assertEqual(generate(), DASHBOARD)
        rows = DASHBOARD['records']
        self.assertEqual(len(rows), 1080)
        self.assertEqual(len({r['id'] for r in rows}), 1080)
        self.assertEqual(len({r['content'] for r in rows}), 1080)
        self.assertTrue(all(r['id'].startswith('SIM-') for r in rows))
        self.assertEqual(len(DASHBOARD['topics']), 8)
        self.assertEqual(len(DASHBOARD['groups']), 6)
        self.assertEqual(validate_source(DASHBOARD, 'synthetic'), DASHBOARD)
        groups = Counter(r['taggenerasi'] for r in rows)
        self.assertEqual(sum(groups.values()), len(rows))
        self.assertEqual(sorted(groups.values()), [100,130,152,194,218,286])
        for p in ['all'] + DASHBOARD['platforms']:
            for m in ['all'] + [m['id'] for m in DASHBOARD['months']]:
                filtered = [r for r in rows if (p=='all' or r['specific_resource_type']==p) and (m=='all' or r['date_created'].startswith(m))]
                by_group = Counter(r['taggenerasi'] for r in filtered)
                by_topic = Counter(r['topic_id'] for r in filtered)
                self.assertEqual(sum(by_group.values()), len(filtered))
                self.assertEqual(sum(by_topic.values()), len(filtered))
                self.assertGreater(len(filtered), 0)

    def test_invalid_sources_fail_closed(self):
        with self.assertRaises(FileNotFoundError): load_source('real')
        with self.assertRaises(ValueError): load_source('mixed')
        with self.assertRaises(ValueError): validate_source(DASHBOARD, 'real')
        for field, value in [('id',DASHBOARD['records'][0]['id']),('topic_id','unknown'),('taggenerasi','unknown'),('specific_resource_type','unknown'),('date_created','2026-10-01')]:
            broken = copy.deepcopy(DASHBOARD)
            broken['records'][1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_source(broken, 'synthetic')


if __name__ == '__main__':
    unittest.main()
