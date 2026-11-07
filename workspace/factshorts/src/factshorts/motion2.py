"""MOTION2 — skills/03-motion-directing integration (hypermotion + motionmaxxing).

STYLE CONTRACT: zero visual-token changes. White bg, dot grid, pill, Inter,
yellow boxes, PART bar — all untouched. This module only upgrades MOTION:
  * micro camera life (slow push-in / pull-out, alternating per part) — no static holds
  * flash-punch scale at each part head (hypermotion flash_cut_duration)
  * punchier SFX recipe (motionmaxxing whoosh sweep 160->65 Hz, 1480 Hz label ticks)
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image

_PRESETS = {}
for _p in (Path("/home/user/skills/03-motion-directing/motion_presets.json"),
           Path(__file__).resolve().parents[3] / "skills/03-motion-directing/motion_presets.json"):
    if _p.exists():
        _PRESETS = json.loads(_p.read_text())
        break

HYPER = _PRESETS.get("hypermotion", {})
MAXX = _PRESETS.get("motionmaxxing", {})

FLASH_DUR = float(HYPER.get("flash_cut_duration_sec", 0.12))
PUSH_MAX = 0.013          # 1.3% slow push (subtle; bottom bar stays visually fixed enough)
PUNCH = 0.035             # extra scale at frame 0, decays over FLASH_DUR
FPS = int(_PRESETS.get("remotion_motion_graphics", {}).get("fps", 30))


def _ease_io(x: float) -> float:
    return x * x * (3 - 2 * x)


def apply_camera(img: Image.Image, t: float, dur: float, idx: int = 1) -> Image.Image:
    """Micro camera move on the finished frame. Push-in on odd parts, pull-out on even."""
    W, H = img.size
    p = max(0.0, min(1.0, t / max(dur, 0.01)))
    drift = PUSH_MAX * _ease_io(p)
    z = 1.004 + drift if idx % 2 == 1 else 1.004 + PUSH_MAX - drift
    if t < FLASH_DUR:                       # flash-punch: tiny scale kick that settles
        z += PUNCH * (1.0 - t / FLASH_DUR) ** 2
    zw, zh = int(W * z) // 2 * 2, int(H * z) // 2 * 2
    big = img.resize((zw, zh), Image.LANCZOS)
    x0, y0 = (zw - W) // 2, (zh - H) // 2
    return big.crop((x0, y0, x0 + W, y0 + H))


def whoosh_sweep(sr: int = 44100, dur: float = 0.55, gain: float = 0.17):
    """motionmaxxing whoosh: noise-flavored sine sweep 160 -> 65 Hz."""
    f0 = float(MAXX.get("whoosh_freq_start_hz", 160.0))
    f1 = float(MAXX.get("whoosh_freq_end_hz", 65.0))
    n = int(dur * sr)
    out, ph = [], 0.0
    for i in range(n):
        x = i / n
        f = f0 + (f1 - f0) * x
        ph += 2 * math.pi * f / sr
        env = math.sin(math.pi * min(1.0, x * 1.15)) ** 1.5
        s = math.sin(ph) + 0.35 * math.sin(2.13 * ph + 0.7)
        out.append(gain * env * s)
    return out


def label_tick(sr: int = 44100, gain: float = 0.09):
    """1480 Hz UI tick (motionmaxxing label_tick_freq_hz)."""
    f = float(MAXX.get("label_tick_freq_hz", 1480.0))
    n = int(0.028 * sr)
    return [gain * math.exp(-6.0 * i / n) * math.sin(2 * math.pi * f * i / sr)
            for i in range(n)]
