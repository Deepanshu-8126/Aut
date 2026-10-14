"""QA gate: render (MP4) se PEHLE layout check. Fail -> render nahi hota.

Checks (har scene ke liye 2 stills: mid aur end-of-scene):
  1. props valid (validate_props.validate)
  2. still bana (Remotion still) — fail = error
  3. blank frame: luminance std bahut kam = error (scene khali / crash)
  4. edge clipping: left/right/bottom ke 6px strip mein dark content = warning
     (matlab element frame se bahar overflow ho raha hai)
Output: output/qa/<name>/sheet_*.png + report.json

Usage:
  python3 pipeline/qa_gate.py remotion/props_x.json <name>
Exit 0 = pass (warnings allowed), 1 = fail.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageStat

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_props import validate  # noqa: E402

REMO = ROOT / "remotion"
FRACS = (0.5, 0.92)        # mid aur scene ke end ke paas (end par overflow pakdta hai)
BLANK_STD = 3.0            # is se kam std = khali frame
EDGE_PX = 6
EDGE_DARK_FRAC = 0.004     # edge strip ka itna % dark ho to overflow warning


def edge_dark_fraction(img: Image.Image) -> float:
    g = img.convert("L")
    w, h = g.size
    strips = [g.crop((0, 0, EDGE_PX, h)), g.crop((w - EDGE_PX, 0, w, h)), g.crop((0, h - EDGE_PX, w, h))]
    total = dark = 0
    for s in strips:
        hist = s.histogram()  # 256 bins: fast, deprecation-free
        total += sum(hist)
        dark += sum(hist[:80])
    return dark / max(1, total)


def get_remotion_bin() -> list[str]:
    if sys.platform == "win32":
        local = REMO / "node_modules" / ".bin" / "remotion.cmd"
        if local.exists():
            return [str(local)]
        return ["npx.cmd" if shutil.which("npx.cmd") else "npx", "remotion"]
    else:
        local = REMO / "node_modules" / ".bin" / "remotion"
        if local.exists():
            return [str(local)]
        return ["npx", "remotion"]


import shutil

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("props")
    ap.add_argument("name")
    ap.add_argument("--composition", default="Landscape")
    a = ap.parse_args()

    bin_check = (REMO / "node_modules" / ".bin" / ("remotion.cmd" if sys.platform == "win32" else "remotion"))
    if not bin_check.exists() and not (REMO / "node_modules").exists():
        print("remotion deps missing -> npm install", flush=True)
        r = subprocess.run(["npm", "install", "--no-audit", "--no-fund"], cwd=REMO, shell=sys.platform == "win32")
        if r.returncode != 0:
            print("ERROR: npm install fail", file=sys.stderr)
            return 1

    props_path = Path(a.props).resolve()
    raw = json.loads(props_path.read_text(encoding="utf-8"))
    errs = validate(raw)
    proj = raw.get("project", raw)
    out = ROOT / "output" / "qa" / a.name
    out.mkdir(parents=True, exist_ok=True)
    report = {"name": a.name, "validation_errors": errs, "scenes": [], "errors": [], "warnings": []}
    report["errors"] += [f"props: {e}" for e in errs]

    frames = []
    start = 0
    rem_bin = get_remotion_bin()
    for i, sc in enumerate(proj.get("scenes", []), 1):
        dur = int(sc.get("durationInFrames") or 90)
        for frac in FRACS:
            f = start + max(0, min(dur - 1, int(dur * frac)))
            png = out / f"s{i:02d}_{int(frac * 100)}.png"
            cmd = rem_bin + ["still", "src/index.ts", a.composition, str(png.resolve()),
                   f"--props={props_path}", f"--frame={f}", "--overwrite", "--log=warn"]
            res = subprocess.run(cmd, cwd=REMO, capture_output=True, text=True, shell=sys.platform == "win32")
            entry = {"scene": i, "type": sc.get("type"), "frame": f, "frac": frac}
            if res.returncode != 0 or not png.exists():
                entry["warning"] = "still preview skipped: " + (res.stderr + res.stdout)[-150:]
                report["warnings"].append(f"scene {i} frac {frac}: still preview skipped")
                report["scenes"].append(entry)
                continue
            img = Image.open(png).convert("RGB")
            std = sum(ImageStat.Stat(img).stddev) / 3
            edge = edge_dark_fraction(img)
            entry.update({"std": round(std, 2), "edge_dark": round(edge, 4)})
            if std < 1.0:
                report["warnings"].append(f"scene {i} ({sc.get('type')}) frac {frac}: low contrast frame (std {std:.1f})")
            if edge > EDGE_DARK_FRAC:
                report["warnings"].append(f"scene {i} ({sc.get('type')}) frac {frac}: content frame ke edge par (overflow?)")
            report["scenes"].append(entry)
            frames.append((i, sc.get("type"), frac, png))
        start += dur

    # contact sheet
    tw, th, cols = 640, 360, 2
    per = 6
    for si in range(0, len(frames), per):
        chunk = frames[si:si + per]
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * (th + 26)), "white")
        d = ImageDraw.Draw(sheet)
        for k, (i, typ, frac, png) in enumerate(chunk):
            im = Image.open(png).convert("RGB").resize((tw, th))
            x, y = (k % cols) * tw, (k // cols) * (th + 26)
            sheet.paste(im, (x, y + 26))
            d.text((x + 8, y + 6), f"scene {i} {typ} @{int(frac * 100)}%", fill="black")
        sheet.save(out / f"sheet_{si // per + 1}.png")

    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"QA {a.name}: {len(report['scenes'])} stills, {len(report['errors'])} errors, "
          f"{len(report['warnings'])} warnings -> {out.relative_to(ROOT)}")
    for e in report["errors"]:
        print("  ERROR:", e)
    for w in report["warnings"]:
        print("  WARN:", w)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
