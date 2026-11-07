import os, time
from playwright.sync_api import sync_playwright
FPS=30; N=504; OUT='/var/tmp/funcy61/code_frames'
os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--force-color-profile=srgb','--allow-file-access-from-files'])
    pg=b.new_page(viewport={'width':540,'height':960}, device_scale_factor=2)
    pg.goto('file:///var/tmp/funcy61/scene61.html')
    pg.wait_for_function('window.READY===true', timeout=15000)
    t0=time.time()
    for i in range(N):
        pg.evaluate(f'renderAt({i/FPS:.5f})')
        pg.screenshot(path=f'{OUT}/f{i:04d}.jpg', type='jpeg', quality=92)
    b.close()
print('SCENE61_DONE', round(time.time()-t0,1))
