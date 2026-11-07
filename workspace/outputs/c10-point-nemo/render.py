from playwright.sync_api import sync_playwright
import os, sys, subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FPS = 30
DUR = 30.0
N = int(DUR * FPS)
OUT = BASE_DIR / "frames"
OUT.mkdir(exist_ok=True)

probe = len(sys.argv) > 1 and sys.argv[1] == 'probe'
if not probe and OUT.exists():
    import shutil
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(exist_ok=True)
frames = [0, 15, 30, 60, 114, 150, 200, 285, 350, 420, 480, 550, 620, 705, 780, 855] if probe else range(N)

html_url = (BASE_DIR / "c10.html").as_uri()

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2)
    pg.goto(html_url)
    pg.wait_for_function('window.READY === 1', timeout=25000)
    print(f"Page ready. Rendering {'probe' if probe else f'all {N}'} frames...", flush=True)
    
    for i in frames:
        fp = OUT / f"f{i:05d}.jpg"
        if (not probe) and fp.exists():
            continue
        pg.evaluate(f"renderAt({(i + 0.5) / FPS})")
        pg.screenshot(path=str(fp), type='jpeg', quality=94, clip={'x': 0, 'y': 0, 'width': 540, 'height': 960})
        if not probe and i % 100 == 0:
            print(f"Rendered frame {i}/{N} ({(i/N)*100:.1f}%)", flush=True)
            
    b.close()

print("Frame rendering complete.")

if not probe:
    audio_file = BASE_DIR / "master_audio.wav"
    output_mp4 = BASE_DIR / "C10_BLOOP_FINAL.mp4"
    print("Muxing video with audio via ffmpeg...", flush=True)
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-framerate", str(FPS),
        "-i", str(OUT / "f%05d.jpg"),
        "-i", str(audio_file),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ]
    subprocess.run(cmd, check=True)
    print(f"FINAL VIDEO READY: {output_mp4}")
    import shutil
    shutil.rmtree(OUT, ignore_errors=True)
    print("Cleaned up intermediate frames.")
