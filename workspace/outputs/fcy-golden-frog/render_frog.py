"""
Golden Poison Frog Render Script (Funcyous Mode 2B Hybrid)
Generates frames from scene_frog.html via playwright and muxes with audio.
"""
from playwright.sync_api import sync_playwright
import os, sys, subprocess, shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FPS = 30
DUR = 32.0  # 32 seconds short
N = int(DUR * FPS)
OUT = BASE_DIR / "frames_frog"
OUT.mkdir(exist_ok=True)

html_url = (BASE_DIR / "scene_frog.html").as_uri()

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(
        viewport={'width': 540, 'height': 960},
        device_scale_factor=2
    )
    pg.goto(html_url)
    pg.wait_for_function('window.READY === 1', timeout=25000)
    print(f"Page ready. Rendering all {N} frames...", flush=True)

    for i in range(N):
        fp = OUT / f"f{i:05d}.jpg"
        if fp.exists():
            continue
        pg.evaluate(f"renderAt({(i + 0.5) / FPS})")
        pg.screenshot(
            path=str(fp), type='jpeg', quality=94,
            clip={'x': 0, 'y': 0, 'width': 540, 'height': 960}
        )
        if i % 100 == 0:
            print(f"  Frame {i}/{N} ({(i/N)*100:.1f}%)", flush=True)

    b.close()

print("Frame rendering complete.", flush=True)

output_mp4 = BASE_DIR / "FCY_GOLDEN_FROG_FINAL.mp4"
print("Muxing video via ffmpeg...", flush=True)
cmd = [
    "ffmpeg", "-v", "error", "-y",
    "-framerate", str(FPS),
    "-i", str(OUT / "f%05d.jpg"),
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "22",
    "-pix_fmt", "yuv420p",
    str(output_mp4)
]
subprocess.run(cmd, check=True)
print(f"FINAL VIDEO READY: {output_mp4}", flush=True)
shutil.rmtree(OUT, ignore_errors=True)
print("Cleaned up frames.", flush=True)
