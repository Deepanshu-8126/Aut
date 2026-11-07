import asyncio,os
from playwright.async_api import async_playwright
OUT='/var/tmp/fcyc_v4base'; os.makedirs(OUT,exist_ok=True)
N=647; FPS=30; DUR=21.55
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--force-color-profile=srgb','--disable-lcd-text'])
        pg=await b.new_page(viewport={'width':540,'height':960},device_scale_factor=2)
        await pg.goto('file:///home/user/outputs/fcy-chimera/test_v4_working.html')
        await pg.wait_for_function('window.READY===1',timeout=30000)
        for i in range(N):
            f=f'{OUT}/f_{i:04d}.png'
            if os.path.exists(f): continue
            t=min((i+0.5)/FPS, DUR-0.001)
            await pg.evaluate(f'window.renderAt({t})')
            await pg.screenshot(path=f,clip={'x':0,'y':0,'width':540,'height':960})
            if i%200==0: print('frame',i,flush=True)
        await b.close()
asyncio.run(main()); print('RENDER DONE')
