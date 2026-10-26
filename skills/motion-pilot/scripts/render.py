#!/usr/bin/env python3
"""Deterministic HTML -> MP4 renderer. Resumable, single-instance (flock), optional motion blur + time map.
  render.py PROJECT --w 1920 --h 1080 --fps 30 --dur 10 --theme dark --out out.mp4 [--timemap map.json] [--sub 2] [--audio mix.wav]
  render.py PROJECT ... --sheet 0.5,2,4 --sheet-out sheet.jpg        quick contact sheet (no video)
Parts are cached in PROJECT/.parts/<tag>; re-running resumes. Run long renders DETACHED (setsid nohup) and poll."""
import argparse, asyncio, fcntl, glob, io, json, os, subprocess, sys, time
import numpy as np
from PIL import Image
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
class TimeMap:
    def __init__(s,path=None):
        s.out = None
        if path:
            k = json.load(open(path)); k = k['knots'] if isinstance(k,dict) else k
            s.out = np.array([a for a,b in k],float); s.src = np.array([b for a,b in k],float)
            assert np.all(np.diff(s.out)>0) and np.all(np.diff(s.src)>0), 'time map knots must strictly increase'
    def __call__(s,T): return float(T) if s.out is None else float(np.interp(T,s.out,s.src))
def nframes(f):
    r = subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',f],capture_output=True,text=True)
    try: return int(r.stdout.strip())
    except: return -1
async def open_page(p,a):
    b = await p.chromium.launch(executable_path=chrome())
    pg = await b.new_page(viewport={'width':a.w,'height':a.h})
    pg.on('pageerror',lambda e: print('PAGE ERROR:',e,file=sys.stderr))
    await pg.goto(f'file://{os.path.abspath(a.project)}/index.html?w={a.w}&h={a.h}&theme={a.theme}')
    await pg.evaluate('M.ready()')
    json.dump(await pg.evaluate('M.exportCues()'),open(os.path.join(a.project,'cues.json'),'w'),indent=1)   # source-time sound cues
    return b,pg
async def sheet(a):
    tm = TimeMap(a.timemap); ts = [float(x) for x in a.sheet.split(',')]
    async with async_playwright() as p:
        b,pg = await open_page(p,a); ims = []
        for T in ts:
            await pg.evaluate('([t,f,rt])=>M.render(t,f,rt)',[tm(T),int(T*a.fps),T])
            ims.append(Image.open(io.BytesIO(await pg.screenshot(type='png'))).convert('RGB'))
        await b.close()
    cw = a.sheet_width; ch = int(cw*a.h/a.w); cols = min(a.sheet_cols,len(ims)); rows = (len(ims)+cols-1)//cols
    sh = Image.new('RGB',(cols*cw,rows*ch),(30,30,40))
    for i,im in enumerate(ims): sh.paste(im.resize((cw,ch)),((i%cols)*cw,(i//cols)*ch))
    sh.save(a.sheet_out,quality=88); print('sheet ->',a.sheet_out)
async def render(a):
    proj = os.path.abspath(a.project); lock = open(proj+'/.render.lock','w')
    try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError: sys.exit('Another render holds this project lock. Never run two pipelines on one project (they corrupt shared outputs).')
    tm = TimeMap(a.timemap); fps = a.fps; total = int(round(a.dur*fps)); sub = a.sub
    tag = f'{a.w}x{a.h}_{a.theme}_{fps}_{sub}'; pdir = f'{proj}/.parts/{tag}'; os.makedirs(pdir,exist_ok=True)
    chunks = [(s,min(s+a.chunk,total)) for s in range(0,total,a.chunk)]
    async with async_playwright() as p:
        b,pg = await open_page(p,a); t0 = time.time()
        for s,e in chunks:
            part = f'{pdir}/p_{s:06d}_{e:06d}.mp4'
            if os.path.exists(part) and nframes(part)==e-s: print('skip',part); continue
            ff = subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{a.w}x{a.h}','-r',str(fps),'-i','-','-c:v','libx264','-preset','medium','-crf',str(a.crf),'-pix_fmt','yuv420p',part+'.tmp.mp4'],stdin=subprocess.PIPE)
            for f in range(s,e):
                acc = None
                for k in range(sub):
                    T = min(max((f+(k/sub-0.5*(1-1/sub))*a.shutter)/fps,0),a.dur-1e-3)
                    await pg.evaluate('([t,f,rt])=>M.render(t,f,rt)',[tm(T),f,T])
                    im = np.asarray(Image.open(io.BytesIO(await pg.screenshot(type='png'))).convert('RGB'),dtype=np.float32)
                    acc = im if acc is None else acc+im
                ff.stdin.write((acc/sub+0.5).astype(np.uint8).tobytes())
                if f%30==0: print(f'frame {f}/{total}  {time.time()-t0:.0f}s',flush=True)
            ff.stdin.close(); ff.wait(); os.replace(part+'.tmp.mp4',part)
        await b.close()
    lst = f'{pdir}/list.txt'; open(lst,'w').write(''.join(f"file '{x}'\n" for x in sorted(glob.glob(pdir+'/p_*.mp4') if False else [f'{pdir}/p_{s:06d}_{e:06d}.mp4' for s,e in chunks])))
    cmd = ['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',lst]
    if a.audio: cmd += ['-i',a.audio,'-map','0:v','-map','1:a','-c:a','aac','-b:a','256k','-shortest']
    cmd += ['-c:v','libx264','-crf',str(a.final_crf),'-preset','medium','-pix_fmt','yuv420p','-r',str(fps),'-movflags','+faststart',a.out]
    subprocess.run(cmd,check=True); print('done ->',a.out)
if __name__=='__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('project'); ap.add_argument('--w',type=int,default=1920); ap.add_argument('--h',type=int,default=1080)
    ap.add_argument('--fps',type=int,default=30); ap.add_argument('--dur',type=float,required=True); ap.add_argument('--theme',default='dark')
    ap.add_argument('--out',default='out.mp4'); ap.add_argument('--timemap'); ap.add_argument('--sub',type=int,default=2,help='motion-blur subframes (1 = off)')
    ap.add_argument('--shutter',type=float,default=0.5); ap.add_argument('--crf',type=int,default=14); ap.add_argument('--final-crf',type=int,default=18)
    ap.add_argument('--chunk',type=int,default=150); ap.add_argument('--audio'); ap.add_argument('--sheet'); ap.add_argument('--sheet-out',default='sheet.jpg')
    ap.add_argument('--sheet-cols',type=int,default=5); ap.add_argument('--sheet-width',type=int,default=384)
    a = ap.parse_args(); asyncio.run(sheet(a) if a.sheet else render(a))
