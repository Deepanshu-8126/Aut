"""
C10 v2 RENDER — Point Nemo & The Bloop (Rebuilt)
Visual Investigation + ACTION-RECON + Dossier Mode upgrade
Run on Kaggle (playwright + chromium available there).

Usage:
  python3 render_v2.py          # full render → C10_BLOOP_V2_FINAL.mp4
  python3 render_v2.py probe    # key frames only (fast QC)
"""
from playwright.sync_api import sync_playwright
import os, sys, subprocess, shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FPS = 30
DUR = 31.5          # updated duration (closer + 31.5s)
N = int(DUR * FPS)
OUT = BASE_DIR / "frames_v2"
OUT.mkdir(exist_ok=True)

probe = len(sys.argv) > 1 and sys.argv[1] == 'probe'

if not probe and OUT.exists():
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(exist_ok=True)

# Probe frames cover every scene transition
probe_frames = [0, 15, 30, 36, 60,      # hook
                72, 100, 130, 150,       # scene1: map + clock
                180, 210, 240, 264,      # scene2: space + known/unknown
                300, 330, 380, 420,      # scene3: sync grid + sonar
                480, 510, 540, 585,      # scene4: bloop + spectrogram
                620, 660, 700, 735,      # scene5: 3000mi + sync lines
                780, 810, 840, 870,      # scene6: icequake + verdict
                900, 930, 945]           # closer

frames = probe_frames if probe else range(N)

html_url = (BASE_DIR / "c10_v2.html").as_uri()

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(
        viewport={'width': 540, 'height': 960},
        device_scale_factor=2
    )
    pg.goto(html_url)
    pg.wait_for_function('window.READY === 1', timeout=30000)
    print(f"Page ready. Rendering {'probe' if probe else f'all {N}'} frames...", flush=True)

    for i in frames:
        fp = OUT / f"f{i:05d}.jpg"
        if (not probe) and fp.exists():
            continue
        pg.evaluate(f"renderAt({(i + 0.5) / FPS})")
        pg.screenshot(
            path=str(fp), type='jpeg', quality=94,
            clip={'x': 0, 'y': 0, 'width': 540, 'height': 960}
        )
        if not probe and i % 100 == 0:
            print(f"  Frame {i}/{N} ({(i/N)*100:.1f}%)", flush=True)

    b.close()

print("Frame rendering complete.", flush=True)

if not probe:
    audio_file = BASE_DIR / "master_audio.wav"
    output_mp4 = BASE_DIR / "C10_BLOOP_V2_FINAL.mp4"
    print("Muxing video + audio...", flush=True)
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
    print(f"FINAL VIDEO READY: {output_mp4}", flush=True)
    shutil.rmtree(OUT, ignore_errors=True)
    print("Cleaned up frames.", flush=True)
