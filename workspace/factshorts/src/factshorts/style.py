"""Design tokens for the FACTSHORTS "White Minimal Box" style.

Single source of truth: every renderer / animator / prompt-builder reads from here,
so the style can never drift between parts (that is the whole point of the lock).
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[2]          # /home/user/factshorts
FONT_DIR = Path(os.environ.get("FACTSHORTS_FONT_DIR", ROOT / "assets" / "fonts"))
CONFIG_DIR = ROOT / "config"

CANVAS = (1080, 1920)          # 9:16 vertical
SAFE = 90                      # safe area for text
MARGIN = 56                    # visual margin

# ---------------------------------------------------------------- colours
C = {
    "white":   (255, 255, 255),
    "paper":   (255, 255, 255),
    "dot":     (222, 222, 222),
    "ink":     (10, 10, 10),
    "ink_soft":(0, 0, 0),
    "gray":    (85, 85, 85),
    "gray_lt": (150, 150, 150),
    "yellow":  (255, 214, 10),
    "yellow_d":(240, 190, 0),
    "blue":    (58, 134, 255),
    "red":     (255, 59, 48),
    "green":   (0, 200, 83),
    "purple":  (120, 80, 220),
    "shadow":  (0, 0, 0, 26),
}

FONT_FILES = {
    "Regular":  "Inter-Regular.ttf",
    "Medium":   "Inter-Medium.ttf",
    "SemiBold": "Inter-SemiBold.ttf",
    "Bold":     "Inter-Bold.ttf",
    "Black":    "Inter-Black.ttf",
}

# ---------------------------------------------------------------- type scale
TYPE = {
    "pill":     34,
    "title":    112,
    "title_min": 62,
    "subtitle": 46,
    "h2":       52,
    "body":     30,
    "label":    34,
    "metric":   72,
    "metric_sm":44,
    "bottombar":44,
    "caption":  27,
    "cta":      44,
}

# ---------------------------------------------------------------- geometry
GEO = {
    "pill_y": 66,
    "pill_h": 76,
    "pill_r": 38,
    "title_y": 196,
    "bar_h": 104,
    "bar_bottom": 1782,
    "bar_inset": 34,
    "bar_r": 40,
    "hero_center": (540, 1060),
    "hero_max_w": 900,
    "hero_max_h": 760,
}

DOT_GRID = {"spacing": 24, "radius": 2, "opacity": 0.42}   # 12px @1x == 24px @2x


def load_config(name: str, default: dict | None = None) -> dict:
    p = CONFIG_DIR / name
    if p.exists():
        return json.loads(p.read_text())
    return default or {}


@lru_cache(maxsize=64)
def font(weight: str = "Medium", size: int = 40) -> ImageFont.FreeTypeFont:
    """Inter only. Falls back to DejaVu (with a warning) if assets are missing."""
    fname = FONT_FILES.get(weight, FONT_FILES["Medium"])
    path = FONT_DIR / fname
    if not path.exists():
        for alt in ("Inter-Regular.ttf", "DejaVuSans.ttf"):
            alt_p = FONT_DIR / alt
            if alt_p.exists():
                path = alt_p
                break
        else:
            path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(str(path), size)


def rgba(name: str, alpha: int = 255) -> tuple:
    r, g, b = C[name]
    return (r, g, b, alpha)


def mix(a: str, b: str, t: float) -> tuple:
    ca, cb = C[a], C[b]
    return tuple(int(ca[i] + (cb[i] - ca[i]) * t) for i in range(3))
