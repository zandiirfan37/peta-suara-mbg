"""Common, explicit source boundary; synthetic and real records never merge."""
import json
from datetime import date
from pathlib import Path

DEMO_PATH = Path(__file__).parent / 'static/data/demo.json'


def validate_source(data, expected_kind):
    if data.get('schema_version') != 1 or data['source']['kind'] != expected_kind:
        raise ValueError('Unexpected schema or source provenance')
    if expected_kind == 'real' and not data['source'].get('validated_real'):
        raise ValueError('Real outputs require independent validation and evidence')
    group_names = {g['name'] for g in data['groups']}
    group_ids = {g['id'] for g in data['groups']}
    topics = {t['id']: t['name'] for t in data['topics']}
    months = {m['id'] for m in data['months']}
    if len(group_names) != 6 or len(group_ids) != 6 or len(topics) != len(data['topics']):
        raise ValueError('Invalid or duplicate catalog definitions')
    ids = set()
    for row in data['records']:
        if not row['id'] or row['id'] in ids:
            raise ValueError('Missing or duplicate record ID')
        ids.add(row['id'])
        if expected_kind == 'synthetic' and not row['id'].startswith('SIM-'):
            raise ValueError('Synthetic IDs must be unmistakable')
        if row['taggenerasi'] not in group_names or topics.get(row['topic_id']) != row['topic_name']:
            raise ValueError('Invalid group or topic reference')
        if row['specific_resource_type'] not in data['platforms']:
            raise ValueError('Invalid platform')
        date.fromisoformat(row['date_created'])
        if row['date_created'][:7] not in months or not row['content'].strip():
            raise ValueError('Invalid month or empty comment')
    return data


def load_source(mode='synthetic', *, real_path=None):
    if mode not in {'synthetic', 'real'}:
        raise ValueError('Unknown source mode')
    if mode == 'real' and real_path is None:
        raise FileNotFoundError('Validated real output has not been registered')
    path = DEMO_PATH if mode == 'synthetic' else Path(real_path)
    return validate_source(json.loads(path.read_text(encoding='utf-8')), mode)
