# /// script
# dependencies = ["playwright==1.62.0"]
# ///
"""Local browser QA and independent arithmetic oracle. Run against a serving app."""
import argparse
from collections import Counter
import json
import math
import os
from pathlib import Path
from urllib.parse import urlparse

os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(Path.home()/'zandi/.runtime/browsers/playwright'))
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('--url',default='http://127.0.0.1:5067/')
parser.add_argument('--out',default='evidence/v2')
args=parser.parse_args()
if urlparse(args.url).hostname not in {'127.0.0.1','localhost'}:
    parser.error('Use an already running local test server.')
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
report={'errors':[],'checks':[],'viewports':[]}
with sync_playwright() as p:
    bins=sorted(Path(os.environ['PLAYWRIGHT_BROWSERS_PATH']).glob('chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell'))
    b=p.chromium.launch(**({'executable_path':str(bins[-1])} if bins else {}))
    ctx=b.new_context(viewport={'width':1440,'height':900},permissions=['clipboard-read','clipboard-write'])
    page=ctx.new_page()
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
    page.on('response',lambda r:report['errors'].append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
    assert page.goto(args.url).status==200
    page.wait_for_selector('.heat-cell')
    data=page.evaluate('MBG.data');rows=data['records']
    page.screenshot(path=str(out/'initial-1440.png'),full_page=True)
    assert page.locator('[data-group]').count()==6
    assert page.locator('[data-topic]').count()==8
    assert page.locator('.heat-cell').count()==48
    assert page.locator('.mode-switch button:disabled').count()==1
    assert page.locator('.provenance').is_visible()
    report['checks'].append('populated initial screen; synthetic disclosure; real mode locked')

    # Independent Python counts against browser arithmetic: 112 group/filter scopes.
    cases=[]
    for platform in ['all']+data['platforms']:
        for month in ['all']+[m['id'] for m in data['months']]:
            for gid in ['all']+[g['id'] for g in data['groups']]:
                cases.append(dict(platform=platform,month=month,group=gid))
    actual=page.evaluate('''cases=>cases.map(c=>{const s=MBGAnalytics.summarize(MBG.data,c.platform,c.month,c.group);return {total:s.total,selected:s.selected.length,groups:s.groups.map(g=>({id:g.id,count:g.count,share:g.share})),topics:s.topics.map(t=>({id:t.id,count:t.count,share:t.share}))};})''',cases)
    for c,s in zip(cases,actual):
        filtered=[r for r in rows if (c['platform']=='all' or r['specific_resource_type']==c['platform']) and (c['month']=='all' or r['date_created'].startswith(c['month']))]
        gname=next((g['name'] for g in data['groups'] if g['id']==c['group']),None)
        selected=[r for r in filtered if gname is None or r['taggenerasi']==gname]
        assert s['total']==len(filtered) and s['selected']==len(selected)
        for g in s['groups']:
            name=next(x['name'] for x in data['groups'] if x['id']==g['id'])
            count=sum(r['taggenerasi']==name for r in filtered)
            assert g['count']==count
            assert math.isclose(g['share'],100*count/len(filtered),abs_tol=1e-9)
        counts=Counter(r['topic_id'] for r in selected)
        assert sum(t['count'] for t in s['topics'])==len(selected)
        assert [t['count'] for t in s['topics']]==sorted((t['count'] for t in s['topics']),reverse=True)
        for t in s['topics']:
            assert t['count']==counts[t['id']]
            if selected:assert math.isclose(t['share'],100*counts[t['id']]/len(selected),abs_tol=1e-9)
            else:assert t['share'] is None
    # 576 comparisons, eight topics each, independently checked denominators.
    comparisons=[dict(platform=p,month=m,a=a['id'],b=b_['id']) for p in ['all']+data['platforms'] for m in ['all']+[m['id'] for m in data['months']] for a in data['groups'] for b_ in data['groups']]
    actual=page.evaluate('''cases=>cases.map(c=>MBGAnalytics.compare(MBG.data,MBGAnalytics.cohort(MBG.data,c.platform,c.month),c.a,c.b))''',comparisons)
    for c,result in zip(comparisons,actual):
        filtered=[r for r in rows if (c['platform']=='all' or r['specific_resource_type']==c['platform']) and (c['month']=='all' or r['date_created'].startswith(c['month']))]
        names={g['id']:g['name'] for g in data['groups']}
        a=[r for r in filtered if r['taggenerasi']==names[c['a']]]
        bb=[r for r in filtered if r['taggenerasi']==names[c['b']]]
        assert result['totalA']==len(a) and result['totalB']==len(bb)
        for t in result['topics']:
            na=sum(r['topic_id']==t['id'] for r in a);nb=sum(r['topic_id']==t['id'] for r in bb)
            assert t['countA']==na and t['countB']==nb
            expected=na/len(a)*100-nb/len(bb)*100 if a and bb else None
            assert t['delta'] is None if expected is None else math.isclose(t['delta'],expected,abs_tol=1e-9)
    assert page.evaluate('MBGAnalytics.share(0,0)') is None
    assert page.evaluate('MBGAnalytics.compare(MBG.data,[],"gen-z","non-individual").topics.every(t=>t.delta===null)')
    report['checks'].append('112 scopes and 576 comparisons checked against independent Python counts; zero denominator guarded')

    def evidence_matches():
        state=page.evaluate('MBG.state')
        catalog={r['id']:r for r in rows}
        ids=page.locator('#evidence-list [data-evidence-id]').evaluate_all('(els)=>els.map(e=>e.dataset.evidenceId)')
        for rid in ids:
            r=catalog[rid]
            assert state['group']=='all' or r['taggenerasi']==next(g['name'] for g in data['groups'] if g['id']==state['group'])
            assert r['topic_id']==state['topic']
            assert state['platform']=='all' or r['specific_resource_type']==state['platform']
            assert state['month']=='all' or r['date_created'].startswith(state['month'])
            assert state['query'].lower() in (r['id']+' '+r['content']).lower()
        return ids

    for g in data['groups']:
        page.locator(f'[data-group="{g["id"]}"]').click()
        assert page.locator('#selected-group').inner_text()==g['name']
        assert page.locator('#compare-a').input_value()==g['id']
        assert page.locator('[data-group][aria-pressed="true"]').count()==1
        evidence_matches()
    page.locator('[data-group="gen-z"]').click()
    for platform in ['Twitter/X','Instagram','YouTube','all']:
        page.locator('#platform-filter').select_option(platform)
        for month in ['2026-07','2026-08','2026-09','all']:
            page.locator('#month-filter').select_option(month)
            expected=sum((platform=='all' or r['specific_resource_type']==platform) and (month=='all' or r['date_created'].startswith(month)) for r in rows)
            assert int(page.locator('#kpi-total').inner_text().replace('.',''))==expected
            evidence_matches()
    for t in data['topics']:
        page.locator(f'[data-topic="{t["id"]}"]').click()
        assert page.locator('#evidence-topic').inner_text()==t['name']
        assert page.locator('#quick-evidence').evaluate('(el)=>el.open')
        assert page.locator('#quick-title').inner_text()==t['name']
        evidence_matches()
        page.keyboard.press('Escape')
    page.locator('#platform-filter').select_option('Instagram')
    page.locator('#month-filter').select_option('2026-08')
    page.locator('[data-cell-group="gen-z"][data-cell-topic="safety"]').click()
    assert page.evaluate('MBG.state.group')=='gen-z'
    assert page.evaluate('MBG.state.topic')=='safety'
    assert page.locator('.heat-cell[aria-pressed="true"]').count()==1
    evidence_matches()
    page.screenshot(path=str(out/'filtered-evidence.png'),full_page=True)
    report['checks'].append('all group/topic controls, platform/month combinations and matrix cell update matching source records')
    # A genuine zero-row topic context from the generated fixture, not a mocked UI count.
    empty=next((g,p,m,t) for g in data['groups'] for p in data['platforms'] for m in data['months'] for t in data['topics'] if not any(r['taggenerasi']==g['name'] and r['specific_resource_type']==p and r['date_created'].startswith(m['id']) and r['topic_id']==t['id'] for r in rows))
    g,platform,month,topic=empty
    page.locator('#platform-filter').select_option(platform)
    page.locator('#month-filter').select_option(month['id'])
    page.locator(f'[data-group="{g["id"]}"]').click()
    page.locator(f'[data-topic="{topic["id"]}"]').click()
    assert page.locator('#quick-comments .empty-state').is_visible()
    assert page.locator('#quick-comments [data-evidence-id]').count()==0
    page.keyboard.press('Escape')
    page.locator('#broaden').click()
    assert page.locator('#kpi-total').inner_text()=='1.080'
    # Heatmap text contrast is measured, including intermediate intensity colors.
    contrasts=page.locator('.heat-cell').evaluate_all(r"""els=>els.map(el=>{const rgb=s=>s.match(/[\d.]+/g).slice(0,3).map(Number);const lum=a=>a.map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);const s=getComputedStyle(el),a=lum(rgb(s.color)),b=lum(rgb(s.backgroundColor));return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)})""")
    assert min(contrasts)>=4.5,min(contrasts)
    report['checks'].append('genuine zero-result filter recovery and measured heatmap text contrast >=4.5')

    page.locator('#reset').click()
    page.locator('[data-group="gen-z"]').click()
    page.locator('[data-topic="menu"]').click()
    page.keyboard.press('Escape')
    first=evidence_matches()
    page.locator('#evidence-next').click();second=evidence_matches()
    assert set(first).isdisjoint(second)
    page.locator('#evidence-prev').click();assert evidence_matches()==first
    page.locator('#evidence-more').click();assert len(evidence_matches())==5
    page.locator('[data-copy]').first.click()
    page.wait_for_function("document.getElementById('copy-status').textContent.includes('disalin')")
    assert page.evaluate('navigator.clipboard.readText()')==first[0]
    page.locator('#evidence-search').fill('kata-yang-tidak-ada-98223')
    assert page.locator('.empty-state').is_visible()
    page.locator('#broaden').click();assert evidence_matches()
    page.locator('#evidence-search').fill(first[0]);assert evidence_matches()==[first[0]]
    page.locator('#reset').click()
    assert page.locator('#platform-filter').input_value()=='all'
    assert page.locator('#month-filter').input_value()=='all'
    assert page.evaluate('MBG.state.group')=='all'
    assert page.locator('#kpi-total').inner_text()=='1.080'
    page.locator('#compare-a').select_option('gen-z');page.locator('#compare-b').select_option('gen-z')
    assert 'Kelompok yang sama' in page.locator('#comparison-insight').inner_text()
    page.locator('#compare-nonindividual').click()
    assert page.locator('#compare-b').input_value()=='non-individual'
    assert 'SIMULASI' in page.locator('#comparison-insight').inner_text()
    report['checks'].append('evidence pagination, 3/5 examples, clipboard, search empty/recovery, reset, comparison selectors and shortcut')

    page.locator('[data-open-methods]').first.click()
    assert page.locator('#methods-dialog').evaluate('(el)=>el.open')
    page.keyboard.press('Escape');assert not page.locator('#methods-dialog').evaluate('(el)=>el.open')
    assert page.locator('[data-open-methods]').first.evaluate('(el)=>document.activeElement===el')
    page.locator('#start-demo').click()
    assert page.locator('#guide-back').is_disabled()
    page.locator('[data-group="gen-z"]').click()
    page.locator('#guide-next').click();assert '02' in page.locator('#guide-count').inner_text()
    page.locator('#guide-back').click();assert '01' in page.locator('#guide-count').inner_text()
    page.locator('#guide-next').click();page.locator('[data-topic="menu"]').click();page.keyboard.press('Escape')
    assert page.locator('#demo-guide').is_visible()
    page.locator('#guide-next').click();page.locator('#compare-nonindividual').click()
    page.locator('#guide-restart').click();assert page.evaluate('MBG.state.group')=='all'
    page.locator('#guide-next').click();page.locator('#guide-next').click();page.locator('#guide-next').click()
    assert page.locator('#demo-guide').is_hidden()
    page.locator('#start-demo').click();page.locator('#guide-exit').click()
    assert page.locator('#demo-guide').is_hidden()
    report['checks'].append('methods keyboard/focus; three-step guide next/back/restart/completion/exit')
    with page.expect_download() as dl: page.locator('#export-csv').click()
    dl.value.save_as(str(out/'synthetic-export.csv'))
    import csv
    with open(out/'synthetic-export.csv',encoding='utf-8-sig') as f: exported=list(csv.DictReader(f))
    assert len(exported)==48
    assert sum(int(r['count']) for r in exported)==1080
    assert all(r['provenance']=='SYNTHETIC_NOT_RESEARCH' for r in exported)
    report['checks'].append('export has provenance and 48 group/topic rows totaling 1080')

    for width,height in [(1440,900),(1366,768),(1920,1080),(375,812),(812,375),(768,1024)]:
        page.set_viewport_size({'width':width,'height':height});page.evaluate('MBG.reset();scrollTo(0,0)')
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),width
        page.screenshot(path=str(out/f'viewport-{width}.png'),full_page=True)
        page.locator('[data-open-methods]').first.click()
        r=page.locator('#close-methods').bounding_box()
        assert r['x']>=0 and r['y']>=0 and r['x']+r['width']<=width and r['y']+r['height']<=height
        page.keyboard.press('Escape')
        page.locator('#start-demo').click()
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
        page.screenshot(path=str(out/f'guide-{width}.png'))
        page.locator('#guide-exit').click()
        page.locator('[data-topic="menu"]').click()
        r=page.locator('#quick-close').bounding_box()
        assert r['x']>=0 and r['y']>=0 and r['x']+r['width']<=width and r['y']+r['height']<=height
        page.keyboard.press('Escape')
        report['viewports'].append({'width':width,'height':height,'overflow':False,'modal_close_visible':True})
    page.emulate_media(reduced_motion='reduce')
    page.locator('[data-group="gen-z"]').click();evidence_matches()
    fallback=b.new_context(java_script_enabled=False).new_page()
    assert fallback.goto(args.url).status==200
    assert fallback.locator('h1').is_visible()
    assert fallback.locator('noscript').is_visible()
    report['checks'].append('responsive overflow/modal/guide checks, reduced motion and no-JS fallback')
    assert report['errors']==[],report['errors']
    b.close()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
