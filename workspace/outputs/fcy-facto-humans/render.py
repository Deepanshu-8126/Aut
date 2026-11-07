from playwright.sync_api import sync_playwright
import os, sys
FPS=30; DUR=43.9; N=int(DUR*FPS)
OUT='/var/tmp/fhfr'; os.makedirs(OUT,exist_ok=True)
probe = len(sys.argv)>1 and sys.argv[1]=='probe'
frames = [0, 200, 700, 920, 960, 1250, 1320] if probe else range(N)
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':540,'height':960},device_scale_factor=2)
    pg.goto('file:///home/user/outputs/fcy-facto-humans/humans.html')
    pg.wait_for_function('window.READY===1',timeout=15000)
    for i in frames:
        fp=f'{OUT}/f{i:05d}.jpg'
        if (not probe) and os.path.exists(fp): continue
        pg.evaluate(f'renderAt({(i+0.5)/FPS})')
        pg.screenshot(path=fp,type='jpeg',quality=92,clip={'x':0,'y':0,'width':540,'height':960})
        if not probe and i%200==0: print('frame',i,flush=True)
    b.close()
print('DONE')
