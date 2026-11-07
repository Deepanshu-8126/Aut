#!/usr/bin/env python3
"""Slice the Inter variable font into the 5 static weights the renderer uses.

  python tools/make_fonts.py            # download + slice into assets/fonts/
  python tools/make_fonts.py --check    # only verify what is already there

Inter is licensed under the SIL Open Font License 1.1 — the OFL text ships next to
the TTFs in assets/fonts/OFL.txt and must stay with them when redistributed.
"""
from __future__ import annotations

import argparse
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts"
VAR_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/inter/"
           "Inter%5Bopsz,wght%5D.ttf")
OFL_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/OFL.txt"
WEIGHTS = {"Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700, "Black": 900}


def check() -> bool:
    missing = [f"Inter-{w}.ttf" for w in WEIGHTS if not (FONT_DIR / f"Inter-{w}.ttf").exists()]
    for w in WEIGHTS:
        p = FONT_DIR / f"Inter-{w}.ttf"
        print(f"  {'OK  ' if p.exists() else 'MISS'} {p.name}")
    return not missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    if a.check:
        return 0 if check() else 1
    if not a.force and all((FONT_DIR / f"Inter-{w}.ttf").exists() for w in WEIGHTS):
        print("static weights already present (use --force to rebuild)")
        return 0

    try:
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont
    except ImportError:
        print("pip install fonttools", file=sys.stderr)
        return 2

    tmp = FONT_DIR / "_InterVar.ttf"
    print("downloading Inter variable font…")
    urllib.request.urlretrieve(VAR_URL, tmp)
    for name, wght in WEIGHTS.items():
        f = TTFont(tmp)
        inst = instantiateVariableFont(f, {"wght": wght, "opsz": 14}, updateFontNames=False)
        out = FONT_DIR / f"Inter-{name}.ttf"
        inst.save(out)
        print(f"  wrote {out.name} ({out.stat().st_size // 1024} KB)")
    tmp.unlink(missing_ok=True)
    try:
        urllib.request.urlretrieve(OFL_URL, FONT_DIR / "OFL.txt")
        print("  wrote OFL.txt")
    except Exception as e:                                     # noqa: BLE001
        print(f"  (could not fetch OFL.txt: {e})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
