import asyncio, io
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw
from timemap_social import src
TS=[7.0,9.2,12.5,13.4]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        for page,W,H,tw,th,out in [('index_social.html',1920,1080,384,216,'qc/soc_h.jpg'),('index_social_v.html',1080,1920,162,288,'qc/soc_v.jpg')]:
            pg=await b.new_page(viewport={'width':W,'height':H}); pg.on('pageerror',lambda e: print('ERR',e))
            await pg.goto(f'file:///home/claude/build/{page}')
            await pg.evaluate("Promise.all([document.fonts.load('700 100px SG'),document.fonts.load('500 40px SG'),document.fonts.load('400 30px OF')])")
            await pg.evaluate("Promise.all([...document.images].map(i=>i.decode().catch(()=>0)))"); await pg.wait_for_timeout(500)
            ims=[]
            for T in TS:
                await pg.evaluate(f'render({min(19.999,src(T))},{int(T*30)},{T})')
                im=Image.open(io.BytesIO(await pg.screenshot(type='jpeg',quality=80))).resize((tw,th)); ImageDraw.Draw(im).text((4,4),f'{T}s',fill=(255,200,0)); ims.append(im)
            cols=4; s=Image.new('RGB',(cols*tw,2*th))
            for i,im in enumerate(ims): s.paste(im,((i%cols)*tw,(i//cols)*th))
            s.save(out); await pg.close()
        await b.close()
asyncio.run(main())
