import sys, os
from playwright.sync_api import sync_playwright
MODE=sys.argv[1] if len(sys.argv)>1 else 'probe'
OUT='/var/tmp/rl05fr'; os.makedirs(OUT,exist_ok=True)
DUR=25.0; N=750
ids=range(N) if MODE=='full' else [0,5,20,45,60,80,100,120,150,170,190,210,240,270,290,310,330,350,380,410,430,450,480,510,530,555,570,590,620,650,680,700,720,740,749]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':540,'height':960},device_scale_factor=2)
    pg.on('pageerror',lambda e:print('PAGEERROR',e))
    pg.goto('file:///home/user/outputs/rl05-build/rl05.html')
    pg.wait_for_function('window.READY===1',timeout=30000)
    for i in ids:
        f=f'{OUT}/f{i:05d}.jpg'
        if MODE=='full' and os.path.exists(f): continue
        t=(i+0.5)/30.0
        pg.evaluate(f'renderAt({t})')
        pg.screenshot(path=f,type='jpeg',quality=90,clip={'x':0,'y':0,'width':540,'height':960})
        if i%100==0: print('frame',i,flush=True)
    b.close()
print('DONE')
