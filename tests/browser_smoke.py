# /// script
# dependencies = ["playwright==1.62.0"]
# ///
import argparse
import json
from urllib.parse import urlparse
import os
from pathlib import Path
browser_root = Path(os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(Path.home() / 'zandi/.runtime/browsers/playwright')))
parser = argparse.ArgumentParser()
parser.add_argument('--url', default='http://127.0.0.1:5067/')
parser.add_argument('--out', default='evidence/browser')
args = parser.parse_args()
if urlparse(args.url).hostname not in {'127.0.0.1', 'localhost'}:
    parser.error('This QA script accepts a local test server only.')
from playwright.sync_api import sync_playwright
out=Path(args.out);out.mkdir(parents=True, exist_ok=True)
report={'viewports':[], 'checks':[], 'errors':[]}
with sync_playwright() as p:
 executables = sorted(browser_root.glob('chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell'))
 b=p.chromium.launch(**({'executable_path': str(executables[-1])} if executables else {}))
 page=b.new_page(viewport={'width':1366,'height':768})
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
 page.on('response',lambda r:report['errors'].append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
 assert page.goto(args.url).status==200
 assert page.locator('[data-group][aria-pressed="true"]').count()==0
 assert page.locator('#compare-b').input_value()==''
 page.screenshot(path=str(out/'desktop.png'),full_page=True)
 data=page.locator('#dashboard-data').text_content();data=json.loads(data)
 for g in data['groups']:
  page.locator(f'[data-group="{g["id"]}"]').click()
  assert page.locator('#selected-group').inner_text()==g['name']
  assert page.locator('[data-group][aria-pressed="true"]').count()==1
  assert page.locator('#compare-a').input_value()==g['id']
  assert g['name'] in page.locator('#topic-state').inner_text()
 report['checks'].append('all six group selections update context and comparison A')
 page.locator('[data-group="gen-z"]').click()
 assert 'pilih pembanding' in page.locator('#comparison-title').inner_text()
 for q in data['questions']:
  button=page.locator(f'[data-question="{q["id"]}"]');button.click()
  assert page.locator('#evidence').evaluate('(el)=>el.open')
  assert page.locator('#evidence-title').inner_text()==q['title']
  assert q['verify']==page.locator('#evidence-verify').inner_text()
  assert 'Gen Z' in page.locator('#evidence-group').inner_text()
  page.keyboard.press('Escape')
  assert not page.locator('#evidence').evaluate('(el)=>el.open')
  assert button.evaluate('(el)=>document.activeElement===el')
 report['checks'].append('all four hypothesis panels, exact source text, Escape close, focus restored')
 page.locator('[data-question="food-safety"]').click();page.locator('#close-evidence').click()
 page.locator('#compare-b').select_option('gen-z')
 assert 'dua kelompok berbeda' in page.locator('#comparison-copy').inner_text()
 page.locator('#compare-b').select_option('non-individual')
 assert page.locator('.disabled-action').is_disabled()
 assert 'Gen Z ↔ Non-individual'==page.locator('#comparison-title').inner_text()
 page.locator('.denominator summary').click()
 assert 'termasuk yang belum mendapat topik' in page.locator('.denominator').inner_text()
 report['checks'].append('same-group guard; comparison disabled without evidence; denominator disclosed')
 page.locator('#start-demo').click()
 for i in range(4):
  assert page.locator('.demo-focus').count()==1
  page.locator('#guide-next').click()
 assert page.locator('#guide').is_hidden()
 page.locator('#start-demo').click();page.locator('#guide-exit').click()
 assert page.locator('#guide').is_hidden()
 page.locator('#audit-open').click()
 assert page.locator('#methods').evaluate('(el)=>el.open')
 report['checks'].append('four guided steps, completion, early exit and audit shortcut')
 page.locator('#methods').evaluate('(el)=>el.open=false')
 page.locator('.denominator').evaluate('(el)=>el.open=false')
 for w,h in [(1366,768),(1920,1080),(768,1024),(375,812)]:
  page.set_viewport_size({'width':w,'height':h});page.evaluate('scrollTo(0,0)')
  overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth')
  assert not overflow,(w,'horizontal overflow')
  page.screenshot(path=str(out/f'viewport-{w}.png'),full_page=True)
  page.locator('[data-question="food-safety"]').click()
  rect=page.locator('#close-evidence').bounding_box()
  assert rect['x']>=0 and rect['y']>=0 and rect['x']+rect['width']<=w and rect['y']+rect['height']<=h
  page.screenshot(path=str(out/f'evidence-{w}.png'))
  page.locator('#close-evidence').click()
  report['viewports'].append({'width':w,'height':h,'overflow':overflow,'modal_close_visible':True})
 nojs=b.new_page(java_script_enabled=False,viewport={'width':1366,'height':768})
 assert nojs.goto(args.url).status==200
 assert nojs.locator('h1').is_visible()
 assert nojs.locator('#start-demo').is_hidden()
 assert nojs.locator('noscript').is_visible()
 nojs.locator('#methods summary').click()
 assert nojs.locator('table').is_visible()
 report['checks'].append('no-JavaScript fallback retains context and expandable methods')
 assert report['errors']==[],report['errors']
 b.close()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
