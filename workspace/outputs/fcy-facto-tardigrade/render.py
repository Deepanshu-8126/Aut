from playwright.sync_api import sync_playwright
import os, sys
FPS=30; DUR=45.9; N=int(DUR*FPS)
OUT='/var/tmp/tdfr'; os.makedirs(OUT,exist_ok=True)
probe = len(sys.argv)>1 and sys.argv[1]=='probe'
frames = [0,10,35,100,150,210,228,260,310,350,420,480,500,560,620,700,760,850,900,960,1010,1060,1130,1180,1240,1310,1360,1376] if probe else range(N)
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':540,'height':960},device_scale_factor=2)
    pg.goto('file:///home/user/outputs/fcy-facto-tardigrade/tardigrade.html')
    pg.wait_for_function('window.READY===1',timeout=20000)
    for i in frames:
        fp=f'{OUT}/f{i:05d}.jpg'
        if (not probe) and os.path.exists(fp): continue
        pg.evaluate(f'renderAt({(i+0.5)/FPS})')
        pg.screenshot(path=fp,type='jpeg',quality=92,clip={'x':0,'y':0,'width':540,'height':960})
        if not probe and i%200==0: print('frame',i,flush=True)
    b.close()
print('DONE')
