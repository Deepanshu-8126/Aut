"""Shared helpers for all 3b1b-style Manim templates.

MANIM_BEATS (set by the pipeline) gives the seconds for each section, taken from narration audio.
section() plays the animations, then holds until that section's narration has finished.
"""
import json
import os

DEFAULT = [4.0, 4.0, 3.5, 3.5]

# Palette from the 3brown1blue rules (semantic colors) + vdo accents, tuned for white slides.
FONT = "DejaVu Sans"       # matches the lesson UI's sans-serif look
ACC = "#2563eb"           # primary: objects, ranges, main curve
HL = "#f59e0b"            # highlight: current focus, found item, slope
OK = "#16a34a"            # correct / gain
BAD = "#dc2626"           # wrong / loss



def beats(n=4):
    raw = os.environ.get("MANIM_BEATS")
    b = json.loads(raw) if raw else DEFAULT
    if len(b) >= n:
        return b[:n - 1] + [sum(b[n - 1:])]
    return b + DEFAULT[len(b):n]


def section(scene, dur, *groups):
    """groups: (animations, run_time) tuples; holds for the rest of `dur`."""
    used = 0.0
    for anims, rt in groups:
        rt = min(rt, max(dur - used, 0.3))
        scene.play(*anims, run_time=rt)
        used += rt
    rest = dur - used
    if rest > 0.05:  # Manim rejects wait(0)
        scene.wait(rest)
