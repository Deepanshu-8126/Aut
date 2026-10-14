"""Layout QA: har scene ka mid-frame still + contact sheet. Video render NAHI karta.

Usage: python3 pipeline/qa_stills.py remotion/props_<name>.json <outdir> [--frac 0.5]
Output: <outdir>/s01.png ... + <outdir>/sheet_1.png, sheet_2.png ...
"""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
REMO = ROOT / "remotion"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("props")
    ap.add_argument("outdir")
    ap.add_argument("--frac", type=float, default=0.5, help="scene ke kis hisse par still (0-1)")
    a = ap.parse_args()

    props_path = Path(a.props).resolve()
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    proj = json.loads(props_path.read_text(encoding="utf-8"))["project"]

    start = 0
    frames = []
    for i, sc in enumerate(proj["scenes"], 1):
        dur = int(sc.get("durationInFrames") or 90)
        f = start + int(dur * a.frac)
        rem_bin = ["npx.cmd" if sys.platform == "win32" else "npx", "remotion"]
        cmd = rem_bin + ["still", "src/index.ts", "Landscape", str(png.resolve()),
               f"--props={props_path}", f"--frame={f}", "--overwrite", "--log=warn"]
        res = subprocess.run(cmd, cwd=REMO, capture_output=True, text=True, shell=sys.platform == "win32")
        if res.returncode != 0 or not png.exists():
            print(f"scene {i}: still FAIL\n{res.stderr[-400:]}")
            continue
        frames.append((i, sc["type"], png))
        print(f"scene {i} ({sc['type']}): frame {f}", flush=True)
        start += dur

    per_sheet, cols = 6, 2
    tw, th = 640, 360
    for si in range(0, len(frames), per_sheet):
        chunk = frames[si:si + per_sheet]
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * (th + 26)), "white")
        d = ImageDraw.Draw(sheet)
        for k, (i, typ, png) in enumerate(chunk):
            im = Image.open(png).convert("RGB").resize((tw, th))
            x, y = (k % cols) * tw, (k // cols) * (th + 26)
            sheet.paste(im, (x, y + 26))
            d.text((x + 8, y + 6), f"scene {i}  {typ}", fill="black")
        path = out / f"sheet_{si // per_sheet + 1}.png"
        sheet.save(path)
        print("sheet:", path)


if __name__ == "__main__":
    main()
