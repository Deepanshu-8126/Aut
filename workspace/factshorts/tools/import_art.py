#!/usr/bin/env python3
"""Import your own art (or crops from reference frames) as library assets.

    # crop a hero object out of a reference frame and knock out its white background
    python tools/import_art.py --src ~/uploads/IMG-20261006-WA8240.jpg --key brain_hero \
        --crop 60,470,940,1300

Then the renderer picks it up automatically on the next run.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from factshorts import art as artlib      # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--crop", help="x0,y0,x1,y1 in source pixels")
    ap.add_argument("--no-knockout", action="store_true")
    a = ap.parse_args()
    bbox = tuple(int(v) for v in a.crop.split(",")) if a.crop else None
    out = artlib.import_art(a.src, a.key, bbox=bbox, knockout=not a.no_knockout)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
