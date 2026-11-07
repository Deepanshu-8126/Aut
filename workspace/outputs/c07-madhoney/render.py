import asyncio,os,sys
from playwright.async_api import async_playwright
DUR=36.4; FPS=30; OUT='/var/tmp/c07fr'
os.makedirs(OUT,exist_ok=True)
N=int(DUR*FPS)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(args=['--allow-file-access-from-files','--disable-web-security'])
        pg=await b.new_page(viewport={'width':540,'height':960},device_scale_factor=2)
        await pg.goto('file:///home/user/outputs/c07-madhoney/c07.html')
        await pg.wait_for_function('window.READY===1',timeout=60000)
        for i in range(N):
            fp=f'{OUT}/f{i:05d}.jpg'
            if os.path.exists(fp): continue
            t=(i+0.5)/FPS
            await pg.evaluate(f'window.renderAt({t})')
            await pg.screenshot(path=fp,type='jpeg',quality=90)
        await b.close()
    print('DONE')
asyncio.run(main())
