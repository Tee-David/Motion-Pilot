import asyncio, sys, io, subprocess, time
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright
import os
if os.environ.get('TM')=='social':
    from timemap_social import src, DUR as _D
else:
    from timemap import src; _D=30.0
FPS=30; DUR=_D; SUB=1 if __import__('os').path.exists('/home/claude/build/force_sub1') else int(__import__('os').environ.get('SUB','2')); SHUTTER=0.5
orient,f0,f1,outp=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]; LOOP=len(sys.argv)>5
W,H,page={'SL':(1920,1080,'index_social_light.html'),'TL':(1080,1920,'index_social_v_light.html'),'HL':(1920,1080,'index_hero_light.html'),'VL':(1080,1920,'index_hero_v_light.html'),'S':(1920,1080,'index_social.html'),'T':(1080,1920,'index_social_v.html'),'h':(1920,1080,'index.html'),'v':(1080,1920,'index_v.html'),'H':(1920,1080,'index_hero.html'),'V':(1080,1920,'index_hero_v.html')}[orient]
async def main():
    ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p',outp],stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg=await b.new_page(viewport={'width':W,'height':H})
        await pg.goto(f'file:///home/claude/build/{page}')
        await pg.evaluate("Promise.all([document.fonts.load('700 100px SG'),document.fonts.load('500 40px SG'),document.fonts.load('400 30px OF'),document.fonts.load('500 30px OF')])")
        await pg.evaluate("Promise.all([...document.images].map(i=>i.decode().catch(()=>0)))")
        await pg.wait_for_timeout(1000)
        if LOOP: await pg.evaluate('window.LOOP=true')
        st=time.time()
        for f in range(f0,f1):
            acc=None
            for s in range(SUB):
                T=(f+(s/SUB-0.5*(1-1/SUB))*SHUTTER)/FPS
                T=max(0,min(DUR-0.001,T)); t=min(19.999,src(T))
                await pg.evaluate(f'render({t},{f},{T})')
                a=np.asarray(Image.open(io.BytesIO(await pg.screenshot(type='png'))).convert('RGB'),dtype=np.float32)
                acc=a if acc is None else acc+a
            ff.stdin.write((acc/SUB+0.5).astype(np.uint8).tobytes())
            if f%30==0: print(f,round(time.time()-st,1),flush=True)
        await b.close()
    ff.stdin.close(); ff.wait()
asyncio.run(main())
