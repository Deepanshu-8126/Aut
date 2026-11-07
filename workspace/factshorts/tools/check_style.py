#!/usr/bin/env python3
"""Style guard: fails if the drawn tokens drift from config/style.json.

Run it in CI (or before a shoot) so a stray edit can never change the channel look.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from factshorts import style as S          # noqa: E402

cfg = json.loads((ROOT / "config" / "style.json").read_text())
problems = []
hexc = lambda n: "#%02X%02X%02X" % S.C[n]                        # noqa: E731
for name, key in (("yellow", "yellow"), ("blue", "blue")):
    want = cfg["accents"][key]
    if hexc(name) != want:
        problems.append(f"accent {name}: {hexc(name)} != {want}")
if (S.CANVAS) != (1080, 1920):
    problems.append(f"canvas {S.CANVAS} != (1080, 1920)")
if S.GEO["bar_h"] != cfg["bottom_bar"]["height"]:
    problems.append("bottom bar height drift")
for p in S.FONT_DIR.glob("*.ttf"):
    if "Inter" not in p.name:
        problems.append(f"non-Inter font present: {p.name}")
print("style OK" if not problems else "STYLE DRIFT:\n - " + "\n - ".join(problems))
sys.exit(1 if problems else 0)
