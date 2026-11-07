import sys, os
from playwright.sync_api import sync_playwright
OUT='/var/tmp/rtf3'; os.makedirs(OUT,exist_ok=True)
N=772; F=1.08
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':540,'height':960},device_scale_factor=2)
    pg.on('pageerror',lambda e:print('PAGEERROR',e))
    pg.goto('file:///home/user/outputs/roop-v2-test/test.html')
    pg.wait_for_function('window.READY===1',timeout=30000)
    for i in range(N):
        f=f'{OUT}/f{i:05d}.jpg'
        if os.path.exists(f): continue
        pg.evaluate(f'renderAt({((i+0.5)/30.0)*F})')
        pg.screenshot(path=f,type='jpeg',quality=90,clip={'x':0,'y':0,'width':540,'height':960})
        if i%200==0: print('frame',i,flush=True)
    b.close()
print('DONE')
