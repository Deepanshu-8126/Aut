import asyncio,sys
from playwright.async_api import async_playwright
TIMES=[0.03,1.2,3.5,7.6,8.9,10.2,15.3,17.0,21.5,24.2,27.5,30.9,32.4,32.82]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--force-color-profile=srgb','--disable-lcd-text'])
        pg=await b.new_page(viewport={'width':540,'height':960},device_scale_factor=2)
        await pg.goto('file:///home/user/outputs/fcy-chimera/test.html')
        await pg.wait_for_function('window.READY===1',timeout=30000)
        for t in TIMES:
            await pg.evaluate(f'window.renderAt({t})')
            await pg.screenshot(path=f'/tmp/probe_{t:05.2f}.png',clip={'x':0,'y':0,'width':540,'height':960})
        await b.close()
asyncio.run(main())
print('done')
