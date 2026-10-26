#!/usr/bin/env python3
"""Read a brand's website like a designer would. Captures desktop+mobile screenshots, real colours (by usage), fonts, logo candidates,
headlines, meta description, social links, and downloads logo/og assets. Use BEFORE proposing concepts.
  brand_probe.py https://example.com --out probe [--pages /about,/services]
Writes probe/{home_d.png,home_m.png,probe.json,assets/*}. Colours are weighted by on-screen area, so brand colours rise above defaults."""
import argparse, asyncio, colorsys, json, os, re, urllib.request, urllib.parse, glob
from collections import Counter
from playwright.async_api import async_playwright
def chrome():
    """Chromium for Playwright: $CHROME_PATH, else a Playwright-managed build, else None (Playwright's own default)."""
    if os.environ.get('CHROME_PATH'): return os.environ['CHROME_PATH']
    roots = ['/opt/pw-browsers', os.path.expanduser('~/.cache/ms-playwright'), os.path.expanduser('~/Library/Caches/ms-playwright'), os.path.join(os.environ.get('LOCALAPPDATA',''),'ms-playwright')]
    tails = ['chrome-linux64/chrome','chrome-linux/chrome','chrome-mac*/Chromium.app/Contents/MacOS/Chromium','chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing','chrome-win*/chrome.exe']
    for r in roots:
        for t in tails:
            hits = sorted(glob.glob(os.path.join(r,'chromium-*',t)))
            if hits: return hits[-1]
    return None
JS = """() => {
 const parse = c => { const m = c.match(/rgba?\\(([^)]+)\\)/); if(!m) return null; const p = m[1].split(',').map(Number); if (p.length>3 && p[3] < .2) return null; return p.slice(0,3).map(Math.round); };
 const hex = a => '#' + a.map(x => x.toString(16).padStart(2,'0')).join('');
 const area = {}, fonts = {}, texts = [];
 for (const e of document.querySelectorAll('body *')) {
   const r = e.getBoundingClientRect(); if (r.width < 4 || r.height < 4) continue; const cs = getComputedStyle(e);
   const a = Math.min(r.width, innerWidth) * Math.min(r.height, innerHeight*2);
   const bg = parse(cs.backgroundColor); if (bg) area[hex(bg)] = (area[hex(bg)]||0) + a;
   if (e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) {
     const fg = parse(cs.color); if (fg) area[hex(fg)] = (area[hex(fg)]||0) + a*.15;
     const f = cs.fontFamily.split(',')[0].replace(/["']/g,'').trim(); fonts[f] = (fonts[f]||0) + e.textContent.length; }
 }
 const bodyBg = parse(getComputedStyle(document.body).backgroundColor) || parse(getComputedStyle(document.documentElement).backgroundColor);
 const heads = [...document.querySelectorAll('h1,h2,h3')].slice(0,14).map(h => ({tag: h.tagName, text: h.innerText.trim().slice(0,140), font: getComputedStyle(h).fontFamily.split(',')[0].replace(/["']/g,''), weight: getComputedStyle(h).fontWeight, size: getComputedStyle(h).fontSize}));
 const logos = [...document.querySelectorAll('img,svg,link[rel*=icon],meta[property="og:image"]')].map(e => e.tagName === 'IMG' ? e.currentSrc || e.src : e.tagName === 'LINK' ? e.href : e.tagName === 'META' ? e.content : '').filter(s => /logo|brand|icon|mark|favicon|og/i.test(s)).slice(0,12);
 const css = {}; const rs = getComputedStyle(document.documentElement); for (const n of [...document.styleSheets].flatMap(s => { try { return [...s.cssRules] } catch(e) { return [] } }).flatMap(r => r.style ? [...r.style].filter(k => k.startsWith('--')) : [])) css[n] = rs.getPropertyValue(n).trim();
 const faces = [...document.fonts].map(f => f.family.replace(/["']/g,'')).filter((v,i,a)=>a.indexOf(v)===i);
 return {title: document.title, desc: (document.querySelector('meta[name=description]')||{}).content||'', bodyBg: bodyBg && hex(bodyBg), area, fonts, heads, logos, cssVars: Object.fromEntries(Object.entries(css).filter(([k,v]) => /^#|rgb|hsl/.test(v)).slice(0,40)), faces,
   links: [...document.querySelectorAll('a[href]')].map(a => a.href).filter(h => /instagram|linkedin|twitter|x\\.com|facebook|tiktok|youtube/i.test(h)).slice(0,8),
   nav: [...document.querySelectorAll('nav a')].map(a => a.innerText.trim()).filter(Boolean).slice(0,12)}; }"""
def tidy(area, n=8):
    out = []
    for h, v in sorted(area.items(), key=lambda kv: -kv[1]):
        r, g, b = (int(h[i:i+2], 16)/255 for i in (1, 3, 5)); hh, l, s = colorsys.rgb_to_hls(r, g, b)
        if any(sum(abs(int(h[i:i+2], 16)-int(o['hex'][i:i+2], 16)) for i in (1, 3, 5)) < 40 for o in out): continue
        out.append({'hex': h, 'weight': int(v), 'sat': round(s, 2), 'light': round(l, 2)})
        if len(out) >= n: break
    return out
async def main():
    ap = argparse.ArgumentParser(); ap.add_argument('url'); ap.add_argument('--out', default='probe'); ap.add_argument('--pages', default=''); a = ap.parse_args()
    os.makedirs(a.out+'/assets', exist_ok=True); res = {'url': a.url, 'pages': {}}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=chrome())
        for path in ['']+[x for x in a.pages.split(',') if x]:
            u = urllib.parse.urljoin(a.url, path); tag = (path.strip('/') or 'home').replace('/', '_')
            for name, vp, dpr in (('d', {'width': 1440, 'height': 900}, 1), ('m', {'width': 390, 'height': 844}, 2)):
                pg = await b.new_page(viewport=vp, device_scale_factor=dpr)
                try:
                    await pg.goto(u, wait_until='networkidle', timeout=45000); await pg.wait_for_timeout(2500)
                    for _ in range(6): await pg.mouse.wheel(0, 700); await pg.wait_for_timeout(200)
                    await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(500)
                    await pg.screenshot(path=f'{a.out}/{tag}_{name}.png')
                    if name == 'd':
                        d = await pg.evaluate(JS); d['palette'] = tidy(d.pop('area')); res['pages'][tag] = d
                        await pg.screenshot(path=f'{a.out}/{tag}_full.png', full_page=True)
                except Exception as e: print('ERR', u, str(e)[:100])
                await pg.close()
        await b.close()
    seen = set()
    for pg in res['pages'].values():
        for l in pg['logos']:
            if l in seen or not l.startswith('http'): continue
            seen.add(l)
            try:
                fn = re.sub(r'[^a-zA-Z0-9._-]', '_', os.path.basename(urllib.parse.urlparse(l).path) or 'asset')[:60]
                urllib.request.urlretrieve(l, f'{a.out}/assets/{fn}'); pg.setdefault('downloaded', []).append(fn)
            except Exception as e: pass
    json.dump(res, open(a.out+'/probe.json', 'w'), indent=1)
    for t, d in res['pages'].items():
        print(f"[{t}] {d['title']!r}\n  desc: {d['desc'][:160]}\n  bodyBg {d['bodyBg']}  palette: {' '.join(c['hex'] for c in d['palette'])}\n  fonts: {dict(Counter(d['fonts']).most_common(4))}  faces: {d['faces'][:6]}")
        for h in d['heads'][:5]: print(f"  {h['tag']} {h['size']} w{h['weight']} {h['font']}: {h['text'][:90]}")
        print('  nav:', d['nav'], '\n  socials:', d['links'][:4], '\n  assets:', d.get('downloaded', []))
asyncio.run(main())
