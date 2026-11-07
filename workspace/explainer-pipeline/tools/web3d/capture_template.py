import sys, time
sys.path.insert(0,'/var/tmp/pydeps')
from playwright.sync_api import sync_playwright
FPS=30; N=300
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader"])
    pg=b.new_page(viewport={"width":540,"height":960}, device_scale_factor=2)
    pg.goto("file:///var/tmp/mg/index.html")
    pg.wait_for_function("window.READY===true", timeout=30000)
    t0=time.time()
    for f in range(N):
        pg.evaluate(f"window.renderAt({f/FPS})")
        pg.screenshot(path=f"/var/tmp/mg/fr/{f:04d}.jpg", type="jpeg", quality=88)
    b.close(); print(f"DONE {N} in {time.time()-t0:.0f}s")
