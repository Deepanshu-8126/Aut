"""Offline vector illustration engine.

Renders every illustration the white-box style needs with pure PIL maths, so the
pipeline works with zero API keys, zero cost and zero latency.  Outputs are cached
RGBA PNGs with real transparency (the AI path gets the same treatment via art.py).
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from . import style as S

SIZE = 1200                    # working canvas for every illustration
ART_DIR = Path(__file__).resolve().parents[2] / "assets" / "illustrations"
ART_DIR.mkdir(parents=True, exist_ok=True)

C = S.C


# ------------------------------------------------------------------ helpers
def _catmull(points: list[tuple[float, float]], samples: int = 26, closed: bool = True):
    """Catmull-Rom spline through control points -> smooth polyline."""
    pts = list(points)
    n = len(pts)
    if closed:
        pts = [pts[-1]] + pts + [pts[0], pts[1]]
    else:
        pts = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(len(pts) - 3):
        p0, p1, p2, p3 = pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    return out


def _mask(draw_fn, size: int = SIZE) -> Image.Image:
    m = Image.new("L", (size, size), 0)
    draw_fn(ImageDraw.Draw(m))
    return m


def _grad(size: tuple[int, int], c0, c1, angle: float = 90.0) -> Image.Image:
    """Linear gradient image (RGB) at any angle."""
    w, h = size
    small = Image.new("L", (64, 64))
    px = small.load()
    rad = math.radians(angle)
    dx, dy = math.cos(rad), math.sin(rad)
    for y in range(64):
        for x in range(64):
            v = (x / 63 * dx + y / 63 * dy)
            v = max(0.0, min(1.0, (v + 1) / 2 if (dx < 0 or dy < 0) else v))
            px[x, y] = int(v * 255)
    grad = small.resize(size, Image.BICUBIC)
    r = Image.new("RGB", size, c0)
    return Image.composite(Image.new("RGB", size, c1), r, grad)


def _shade(base: Image.Image, mask: Image.Image, color, alpha: int, blur: int, offset=(0, 0)):
    """Soft shadow/highlight clipped to a mask."""
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    m = ImageChops.offset(mask, offset[0], offset[1]).filter(ImageFilter.GaussianBlur(blur))
    solid = Image.new("RGBA", base.size, tuple(color) + (alpha,))
    lay.paste(solid, (0, 0), m)
    base.alpha_composite(lay)


def _ring_masks(mask: Image.Image, rings: int = 11, step: int = 13):
    """Concentric offset contours of a silhouette — the basis of the cortex folds."""
    out, cur = [], mask
    for _ in range(rings):
        nxt = cur.filter(ImageFilter.MinFilter(step))
        out.append(ImageChops.subtract(cur, nxt))
        cur = nxt
        if not cur.getbbox():
            break
    return out


def _finish(img: Image.Image, key: str, glow_color=(255, 214, 10), glow_alpha: int = 0) -> Image.Image:
    out = img.crop(img.getbbox() or (0, 0, img.width, img.height))
    if glow_alpha:
        g = Image.new("RGBA", out.size, (0, 0, 0, 0))
        am = out.getchannel("A").filter(ImageFilter.GaussianBlur(26))
        am = am.point(lambda v: int(v * glow_alpha / 255))
        g.putalpha(am)
        g = Image.composite(Image.new("RGBA", out.size, tuple(glow_color) + (255,)), g, am)
        g.putalpha(am)
        canvas = Image.new("RGBA", (out.width + 120, out.height + 120), (0, 0, 0, 0))
        canvas.alpha_composite(g, (60, 60))
        canvas.alpha_composite(out, (60, 60))
        out = canvas
    return out


# -------------------------------------------------------------------- brain
# Anatomical profile of a human brain, facing left (normalised 0..1).
OUTLINE = [
    (0.045, 0.470), (0.070, 0.330), (0.140, 0.215), (0.260, 0.130), (0.420, 0.078),
    (0.580, 0.070), (0.720, 0.112), (0.840, 0.195), (0.925, 0.310), (0.972, 0.440),
    (0.962, 0.560), (0.900, 0.640), (0.800, 0.672),
    (0.690, 0.660), (0.610, 0.588), (0.545, 0.582), (0.480, 0.640),
    (0.410, 0.740), (0.290, 0.782), (0.170, 0.752), (0.085, 0.680), (0.042, 0.580),
]
TEMPORAL = [
    (0.480, 0.640), (0.410, 0.740), (0.290, 0.782), (0.170, 0.752), (0.085, 0.680),
    (0.042, 0.580), (0.062, 0.470), (0.150, 0.400), (0.300, 0.430), (0.420, 0.520),
]


def _scale_path(pts, size: int):
    return [(x * size, y * size) for x, y in pts]


def _brain_outline(size: int = SIZE):
    return _catmull(_scale_path(OUTLINE, size), 20, closed=True)


def lerp_pt(path, t):
    t = max(0.0, min(1.0, t))
    i = max(0, min(len(path) - 2, int(t * (len(path) - 1))))
    f = t * (len(path) - 1) - i
    return (path[i][0] + (path[i + 1][0] - path[i][0]) * f,
            path[i][1] + (path[i + 1][1] - path[i][1]) * f)


def _boundaries(size: int):
    """Top and bottom edge of the silhouette sampled across x."""
    sil = _brain_outline(size)
    xs = [p[0] for p in sil]
    top, bot = [], []
    for x in range(int(min(xs)) + 14, int(max(xs)) - 14, 22):
        col = [p[1] for p in sil if abs(p[0] - x) < 12]
        if len(col) < 2:
            continue
        top.append((x, min(col)))
        bot.append((x, max(col)))
    return top, bot


def _fold_layer(mask: Image.Image, size: int, fold_color, hi_color, rnd: random.Random,
                count: int = 15, width: int = 11) -> Image.Image:
    """Gyri: a fan of smooth, non-crossing S-curves joining the top and bottom edges."""
    top, bot = _boundaries(size)
    folds = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    fd = ImageDraw.Draw(folds)
    for i in range(count):
        fa = 0.03 + i / (count - 1) * 0.94
        fb = min(0.995, fa + 0.055 + i / (count - 1) * 0.075)
        p0, p1 = lerp_pt(top, fa), lerp_pt(bot, fb)
        sway = rnd.uniform(-1, 1) * size * 0.028
        path = _catmull([p0,
                         (p0[0] + (p1[0] - p0[0]) * 0.32 + sway, p0[1] + (p1[1] - p0[1]) * 0.32),
                         (p0[0] + (p1[0] - p0[0]) * 0.68 - sway, p0[1] + (p1[1] - p0[1]) * 0.68),
                         p1], 18, closed=False)
        w = width + rnd.randint(-2, 2)
        fd.line(path, fill=fold_color + (250,), width=w, joint="curve")
        fd.line([(x, y + w * 0.75) for x, y in path], fill=hi_color + (150,),
                width=max(2, w // 3), joint="curve")
        fd.line([(x, y - w * 0.75) for x, y in path], fill=(0, 0, 0, 45),
                width=max(2, w // 4), joint="curve")
        if i % 2 == 0:                                   # branch sulcus
            k = rnd.randint(8, max(9, len(path) - 9))
            bx, by = path[k]
            dx, dy = path[k + 1][0] - path[k - 1][0], path[k + 1][1] - path[k - 1][1]
            n = math.hypot(dx, dy) or 1
            nx, ny = -dy / n, dx / n
            if ny > 0:
                nx, ny = -nx, -ny
            L = rnd.uniform(size * 0.05, size * 0.11)
            fd.line((bx, by, bx + nx * L, by + ny * L), fill=fold_color + (215,),
                    width=max(4, w - 4), joint="curve")
    return folds.filter(ImageFilter.GaussianBlur(2.2))


def brain(accent: str | None = "yellow", glow: bool = True, dark: bool = False,
          cross_section: bool = False) -> Image.Image:
    size = SIZE
    sil = _brain_outline(size)
    mask = _mask(lambda d: d.polygon(sil, fill=255))

    if dark:
        top_c, bot_c, fold, ridge = (120, 122, 128), (46, 48, 54), (30, 32, 38), (180, 182, 188)
    else:
        top_c, bot_c, fold, ridge = (252, 252, 253), (188, 190, 196), (108, 110, 118), (255, 255, 255)

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # --- cerebellum (right-lower, outside the cerebrum silhouette)
    cm = _mask(lambda d: d.ellipse((size * 0.655, size * 0.520, size * 0.975, size * 0.755), fill=255))
    cm = ImageChops.subtract(cm, mask.filter(ImageFilter.GaussianBlur(3)))
    cer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cer.paste(_grad((size, size), (226, 227, 232), (152, 154, 161), 110).convert("RGBA"), (0, 0), cm)
    cd = ImageDraw.Draw(cer)
    for i in range(11):
        y = size * 0.528 + i * (size * 0.235 / 11)
        cd.arc((size * 0.655, y - 2, size * 0.975, y + 34), 185, 355, fill=(114, 116, 124, 235),
               width=6)
    cd.arc((size * 0.655, size * 0.520, size * 0.975, size * 0.755), 0, 360,
           fill=(104, 106, 114, 215), width=5)
    cer.putalpha(ImageChops.multiply(cer.getchannel("A"), cm.point(lambda v: 255 if v > 40 else 0)))
    img.alpha_composite(cer)

    # --- brainstem (angled down, tucked behind the temporal lobe)
    stem = _catmull([(size * 0.520, size * 0.650), (size * 0.520, size * 0.760),
                     (size * 0.522, size * 0.860), (size * 0.575, size * 0.925),
                     (size * 0.628, size * 0.870), (size * 0.620, size * 0.762),
                     (size * 0.590, size * 0.672)], 18, closed=True)
    sm = _mask(lambda d: d.polygon(stem, fill=255))
    st = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    st.paste(_grad((size, size), (216, 217, 222), (156, 158, 165), 90).convert("RGBA"), (0, 0), sm)
    st.putalpha(ImageChops.multiply(st.getchannel("A"), sm.point(lambda v: 255 if v > 40 else 0)))
    img.alpha_composite(st)

    # --- cerebrum body
    body = Image.new("RGB", (size, size), (236, 236, 236))
    body.paste(_grad((size, size), top_c, bot_c, angle=112), (0, 0), mask)
    body_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    body_layer.paste(body, (0, 0), mask)
    img.alpha_composite(body_layer)

    # --- accent region under the gyri
    if accent:
        blobs = None
        if accent == "yellow":
            blobs = _mask(lambda d: d.polygon(_scale_path(TEMPORAL, size), fill=255))
        elif accent == "all":
            blobs = mask.copy()
        if blobs is not None:
            soft = blobs.filter(ImageFilter.GaussianBlur(10))
            lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            lay.paste(Image.new("RGBA", (size, size), tuple(C["yellow"]) + (208,)), (0, 0),
                      ImageChops.multiply(soft, mask))
            img.alpha_composite(lay)

    # --- cortex folds
    rnd = random.Random(11)
    folds = _fold_layer(mask, size, fold, ridge, rnd, count=15, width=12)
    folds.putalpha(ImageChops.multiply(folds.getchannel("A"), mask))
    img.alpha_composite(folds)

    # --- volume + line work
    _shade(img, ImageChops.offset(mask, -52, -58), (255, 255, 255), 145, 56)
    _shade(img, ImageChops.offset(mask, 56, 62), (22, 24, 30), 78, 60)
    inner_line = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(27)))
    lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    lay.paste(Image.new("RGBA", (size, size), tuple(fold) + (105,)), (0, 0), inner_line)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)))
    rim = ImageChops.subtract(mask, ImageChops.offset(mask, -20, -20))
    lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    lay.paste(Image.new("RGBA", (size, size), (255, 255, 255, 170)), (0, 0),
              ImageChops.multiply(rim, mask))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
    outline = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(3)),
                                  mask.filter(ImageFilter.MinFilter(5)))
    lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    lay.paste(Image.new("RGBA", (size, size), (74, 76, 84, 165)), (0, 0), outline)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.2)))

    if cross_section:
        dd = ImageDraw.Draw(img)
        for i in range(6):
            y = size * (0.24 + i * 0.075)
            dd.line((size * 0.07, y, size * 0.96, y), fill=(88, 90, 98, 55), width=3)

    return _finish(img, "brain", glow_alpha=55 if glow else 0)


# ---------------------------------------------------------------------- eye
def eye(accent="yellow") -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    w, h = SIZE, SIZE
    upper = _catmull([(w * 0.06, h * 0.52), (w * 0.22, h * 0.28), (w * 0.5, h * 0.24),
                      (w * 0.78, h * 0.28), (w * 0.94, h * 0.52)], 22, closed=False)
    lower = _catmull([(w * 0.06, h * 0.52), (w * 0.24, h * 0.74), (w * 0.5, h * 0.78),
                      (w * 0.76, h * 0.74), (w * 0.94, h * 0.52)], 22, closed=False)
    d = ImageDraw.Draw(img)
    d.polygon(upper + lower[::-1], fill=(252, 252, 252, 255))
    d.line(upper, fill=(60, 62, 70, 255), width=9, joint="curve")
    d.line(lower, fill=(60, 62, 70, 255), width=7, joint="curve")
    # sclera shading
    sc = _mask(lambda dd: dd.polygon(upper + lower[::-1], fill=255))
    _shade(img, ImageChops.offset(sc, 0, -26), (120, 130, 150), 70, 30)
    # iris
    cx, cy, r = w * 0.52, h * 0.50, w * 0.17
    iris = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    idm = _mask(lambda dd: dd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255))
    iris.paste(_grad((w, h), (96, 132, 176), (24, 40, 66), 110).convert("RGBA"), (0, 0), idm)
    idr = ImageDraw.Draw(iris)
    rnd = random.Random(3)
    for i in range(72):                                   # iris fibres
        a = i / 72 * 2 * math.pi
        l = r * rnd.uniform(0.45, 0.95)
        idr.line((cx + math.cos(a) * r * 0.38, cy + math.sin(a) * r * 0.38,
                  cx + math.cos(a) * l, cy + math.sin(a) * l),
                 fill=(190, 214, 240, rnd.randint(50, 120)), width=3)
    idr.ellipse((cx - r * 0.42, cy - r * 0.42, cx + r * 0.42, cy + r * 0.42),
                fill=(12, 14, 18, 255))
    idr.ellipse((cx - r * 0.72, cy - r * 0.78, cx - r * 0.18, cy - r * 0.30),
                fill=(255, 255, 255, 210))
    iris.alpha_composite(iris.filter(ImageFilter.GaussianBlur(16)))
    iris.putalpha(ImageChops.multiply(iris.getchannel("A"), idm.point(lambda v: 255)))
    img.alpha_composite(iris)
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(50, 54, 64, 255), width=6)
    # lashes + brow
    for i in range(16):
        t = 0.10 + i * 0.05
        x = lerp_pt(upper, t)
        ang = -1.9 + i * 0.06
        L = 26 + 16 * math.sin(i / 15 * math.pi)
        d.line((x[0], x[1], x[0] + L * math.cos(ang), x[1] + L * math.sin(ang)),
               fill=(40, 42, 50, 255), width=5)
    brow = _catmull([(w * 0.10, h * 0.20), (w * 0.30, h * 0.09), (w * 0.55, h * 0.07),
                     (w * 0.80, h * 0.12), (w * 0.93, h * 0.22)], 22, closed=False)
    d.line(brow, fill=(70, 72, 80, 255), width=17, joint="curve")
    return _finish(img, "eye", glow_alpha=70)


# --------------------------------------------------------------- small icons
def clock_brain():
    """Brain + clock identity mark (used by the timeline part)."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    r = SIZE * 0.30
    cx, cy = SIZE * 0.62, SIZE * 0.52
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255),
              outline=(24, 24, 26, 255), width=13)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        l0, l1 = r * 0.80, r * 0.92
        d.line((cx + math.cos(a) * l0, cy + math.sin(a) * l0,
                cx + math.cos(a) * l1, cy + math.sin(a) * l1), fill=(24, 24, 26, 255), width=7)
    d.line((cx, cy, cx, cy - r * 0.52), fill=(24, 24, 26, 255), width=12)
    d.line((cx, cy, cx + r * 0.40, cy + r * 0.24), fill=(232, 180, 0, 255), width=12)
    b = brain(accent="yellow", glow=False)
    bw = int(SIZE * 0.62)
    b = b.resize((bw, int(b.height * (bw / b.width))))
    holder = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    holder.alpha_composite(b, (int(SIZE * 0.045), int(cy - b.height / 2 + SIZE * 0.02)))
    img.alpha_composite(holder)
    return _finish(img, "clock_brain", glow_alpha=45)


def chip():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = SIZE * 0.30
    c = SIZE / 2
    d.rounded_rectangle((c - s, c - s, c + s, c + s), radius=28, fill=(52, 54, 60, 255),
                        outline=(20, 20, 22, 255), width=8)
    d.rounded_rectangle((c - s * 0.55, c - s * 0.55, c + s * 0.55, c + s * 0.55), radius=18,
                        fill=(28, 29, 34, 255))
    for i in range(8):
        off = -s * 0.78 + i * (s * 1.56 / 7)
        for sx in (-1, 1):
            d.rounded_rectangle((c + off - 9, c + sx * s - 34, c + off + 9, c + sx * s + 34),
                                radius=6, fill=(214, 216, 222, 255))
            d.rounded_rectangle((c + sx * s - 34, c + off - 9, c + sx * s + 34, c + off + 9),
                                radius=6, fill=(214, 216, 222, 255))
    for i in range(5):                                    # glowing traces
        y = c - s * 0.42 + i * s * 0.21
        d.line((c - s * 0.9, y, c + s * 0.9, y), fill=(255, 214, 10, 90), width=4)
    img.alpha_composite(img.filter(ImageFilter.GaussianBlur(14)))
    return _finish(img, "chip", glow_alpha=70)


def sleep():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    lay = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(lay).ellipse((SIZE * 0.18, SIZE * 0.16, SIZE * 0.82, SIZE * 0.84), fill=255)
    ImageDraw.Draw(lay).ellipse((SIZE * 0.34, SIZE * 0.02, SIZE * 0.98, SIZE * 0.70), fill=0)
    img.paste(_grad((SIZE, SIZE), (255, 232, 130), (238, 180, 0), 110).convert("RGBA"), (0, 0), lay)
    d = ImageDraw.Draw(img)
    for i, (x, y, s) in enumerate(((0.62, 0.24, 0.10), (0.74, 0.12, 0.13), (0.86, 0.02, 0.16))):
        w = SIZE * s
        d.line((x * SIZE, y * SIZE, x * SIZE + w, y * SIZE), fill=(30, 30, 34, 255), width=14)
        d.line((x * SIZE + w, y * SIZE, x * SIZE, y * SIZE + w), fill=(30, 30, 34, 255), width=14)
        d.line((x * SIZE, y * SIZE + w, x * SIZE + w, y * SIZE + w), fill=(30, 30, 34, 255), width=14)
    return _finish(img, "sleep", glow_alpha=110)


def shield_brain():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    pts = _catmull([(SIZE * 0.5, SIZE * 0.10), (SIZE * 0.86, SIZE * 0.24), (SIZE * 0.86, SIZE * 0.55),
                    (SIZE * 0.5, SIZE * 0.90), (SIZE * 0.14, SIZE * 0.55), (SIZE * 0.14, SIZE * 0.24)],
                   20, closed=True)
    d = ImageDraw.Draw(img)
    d.polygon(pts, fill=(232, 250, 240, 255), outline=(0, 200, 83, 255))
    d.line(pts + [pts[0]], fill=(0, 200, 83, 255), width=16, joint="curve")
    b = brain(accent="yellow", glow=False)
    b = b.resize((int(b.width * 0.62), int(b.height * 0.62)))
    holder = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    holder.alpha_composite(b, (int(SIZE * 0.5 - b.width / 2), int(SIZE * 0.46 - b.height / 2)))
    img.alpha_composite(holder)
    return _finish(img, "shield_brain", glow_color=(0, 200, 83), glow_alpha=40)


def world_map():
    """Dotted-grid world map (approximate land mask from coarse blobs)."""
    img = Image.new("RGBA", (SIZE * 2, SIZE), (0, 0, 0, 0))
    land = Image.new("L", (SIZE * 2, SIZE), 0)
    d = ImageDraw.Draw(land)
    blobs = [
        (0.10, 0.20, 0.30, 0.42), (0.14, 0.40, 0.24, 0.66), (0.22, 0.62, 0.32, 0.86),
        (0.40, 0.16, 0.55, 0.34), (0.42, 0.30, 0.52, 0.66), (0.44, 0.62, 0.54, 0.84),
        (0.52, 0.12, 0.74, 0.40), (0.60, 0.34, 0.74, 0.62), (0.70, 0.60, 0.80, 0.80),
        (0.80, 0.62, 0.94, 0.84), (0.30, 0.10, 0.40, 0.20),
    ]
    for x0, y0, x1, y1 in blobs:
        d.ellipse((x0 * SIZE * 2, y0 * SIZE, x1 * SIZE * 2, y1 * SIZE), fill=255)
    land = land.filter(ImageFilter.GaussianBlur(18))
    px = land.load()
    dd = ImageDraw.Draw(img)
    step = 18
    for y in range(0, SIZE, step):
        for x in range(0, SIZE * 2, step):
            if px[x, y] > 120:
                dd.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(10, 10, 10, 230))
    return _finish(img, "world_map")


# Coarse continent outlines (normalised 0..1, equirectangular-ish).
# Simplified on purpose: at 9:16 phone size a dotted map only needs recognisable silhouettes.
CONTINENTS = [
    # North America
    [(0.06, 0.20), (0.15, 0.12), (0.26, 0.10), (0.30, 0.16), (0.26, 0.24), (0.29, 0.31),
     (0.24, 0.38), (0.20, 0.34), (0.15, 0.36), (0.11, 0.30), (0.08, 0.26)],
    # Central America + Caribbean bridge
    [(0.20, 0.38), (0.24, 0.42), (0.26, 0.46), (0.23, 0.47), (0.19, 0.43)],
    # South America
    [(0.26, 0.50), (0.33, 0.48), (0.37, 0.54), (0.35, 0.62), (0.31, 0.72), (0.27, 0.78),
     (0.24, 0.72), (0.23, 0.62), (0.24, 0.54)],
    # Europe
    [(0.46, 0.16), (0.54, 0.13), (0.58, 0.18), (0.56, 0.24), (0.50, 0.26), (0.47, 0.22)],
    # Africa
    [(0.47, 0.30), (0.55, 0.28), (0.60, 0.34), (0.59, 0.44), (0.55, 0.56), (0.50, 0.64),
     (0.46, 0.58), (0.45, 0.46), (0.44, 0.36)],
    # Asia (bulk)
    [(0.58, 0.14), (0.70, 0.10), (0.82, 0.14), (0.88, 0.22), (0.84, 0.30), (0.76, 0.34),
     (0.68, 0.32), (0.61, 0.26), (0.57, 0.20)],
    # India
    [(0.70, 0.34), (0.76, 0.34), (0.77, 0.42), (0.73, 0.47), (0.69, 0.41)],
    # South-east Asia
    [(0.80, 0.36), (0.86, 0.38), (0.88, 0.44), (0.83, 0.46), (0.79, 0.41)],
    # Australia
    [(0.80, 0.56), (0.89, 0.54), (0.92, 0.62), (0.88, 0.70), (0.81, 0.68), (0.78, 0.61)],
    # Greenland
    [(0.32, 0.05), (0.42, 0.04), (0.44, 0.12), (0.36, 0.14), (0.31, 0.10)],
]


def world_map(highlight: tuple[float, float] | None = None) -> Image.Image:
    """Dotted world map with an optional yellow highlight pin (e.g. the Suez isthmus)."""
    W2, H2 = SIZE * 2, SIZE
    land = Image.new("L", (W2, H2), 0)
    d = ImageDraw.Draw(land)
    for poly in CONTINENTS:
        pts = [(x * W2, y * H2) for x, y in poly]
        d.polygon(_catmull(pts, 12, closed=True), fill=255)
    land = land.filter(ImageFilter.GaussianBlur(14))

    img = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    dd = ImageDraw.Draw(img)
    step = 20
    px = land.load()
    for y in range(0, H2, step):
        for x in range(0, W2, step):
            if px[x, y] > 120:
                dd.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(14, 14, 16, 235))
    if highlight:
        hx, hy = highlight[0] * W2, highlight[1] * H2
        gl = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
        ImageDraw.Draw(gl).ellipse((hx - 74, hy - 74, hx + 74, hy + 74),
                                   fill=S.rgba("yellow", 150))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26)))
        dd.ellipse((hx - 15, hy - 15, hx + 15, hy + 15), outline=S.rgba("yellow"), width=8)
        dd.ellipse((hx - 7, hy - 7, hx + 7, hy + 7), fill=S.rgba("yellow"))
    out = img.crop(img.getbbox() or (0, 0, W2, H2))
    return out


def suez_ship():
    """Documentary canal illustration: desert banks, water, laden container ship."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    W_, H_ = SIZE, SIZE

    # desert banks (soft warm sand, low contrast so the style stays white-box friendly)
    d.polygon([(0, H_ * 0.44), (W_, H_ * 0.40), (W_, H_ * 0.60), (0, H_ * 0.64)],
              fill=(232, 224, 205, 255))
    d.polygon([(0, H_ * 0.50), (W_, H_ * 0.455), (W_, H_ * 0.60), (0, H_ * 0.64)],
              fill=(222, 212, 190, 255))

    # water band
    water_top, water_bot = H_ * 0.60, H_ * 0.80
    d.rectangle((0, water_top, W_, water_bot), fill=(206, 226, 244, 255))
    water = img.crop((0, int(water_top), W_, int(water_bot)))
    img.paste(water, (0, int(water_top)))
    for i in range(9):                                    # ripples
        y = water_top + 10 + i * (water_bot - water_top - 20) / 9
        x0 = 20 + (i % 3) * 90
        d.line((x0, y, x0 + 150 + i * 12, y), fill=(150, 186, 220, 190), width=5)

    # ship hull
    hull_top, hull_bot = H_ * 0.34, water_top + 6
    d.polygon([(W_ * 0.10, hull_top), (W_ * 0.82, hull_top), (W_ * 0.90, hull_bot - H_ * 0.03),
               (W_ * 0.84, hull_bot), (W_ * 0.14, hull_bot), (W_ * 0.07, hull_bot - H_ * 0.03)],
              fill=(48, 52, 60, 255))
    d.rectangle((W_ * 0.10, hull_top + H_ * 0.055, W_ * 0.84, hull_top + H_ * 0.075),
                fill=(196, 60, 52, 255))                   # waterline stripe
    # containers
    for i in range(3):
        for j in range(6):
            x0 = W_ * (0.14 + j * 0.115)
            y0 = H_ * (0.20 + i * 0.048)
            col = ((250, 200, 60, 255) if (i + j) % 4 == 0 else
                   (236, 238, 242, 255) if (i + j) % 2 == 0 else (206, 210, 218, 255))
            d.rounded_rectangle((x0, y0, x0 + W_ * 0.10, y0 + H_ * 0.042), radius=5, fill=col)
    # bridge house + funnel
    d.rounded_rectangle((W_ * 0.72, H_ * 0.145, W_ * 0.86, H_ * 0.205), radius=7,
                        fill=(238, 240, 244, 255))
    d.rounded_rectangle((W_ * 0.80, H_ * 0.10, W_ * 0.845, H_ * 0.15), radius=5,
                        fill=(196, 60, 52, 255))
    # tiny dust/sun accents
    d.ellipse((W_ * 0.86, H_ * 0.06, W_ * 0.96, H_ * 0.16), fill=S.rgba("yellow", 210))
    return _finish(img, "suez")


BUILDERS = {
    "brain_hero":  lambda: brain(accent="yellow", cross_section=False),
    "brain_glow":  lambda: brain(accent="all", glow=True),
    "brain_flat":  lambda: brain(accent=None, glow=False),
    "brain_dark":  lambda: brain(accent="yellow", dark=True, glow=False),
    "brain_cut":   lambda: brain(accent="yellow", cross_section=True),
    "eye":         lambda: eye(),
    "clock_brain": clock_brain,
    "chip":        chip,
    "sleep":       sleep,
    "shield_brain": shield_brain,
    "world_map":   lambda: world_map(highlight=(0.575, 0.335)),
    "world_map_plain": world_map,
    "suez":        suez_ship,
}


def build(key: str, force: bool = False) -> Image.Image:
    path = ART_DIR / f"{key}.png"
    if path.exists() and not force:
        return Image.open(path).convert("RGBA")
    fn = BUILDERS.get(key, BUILDERS["brain_flat"])
    img = fn()
    img.save(path)
    return img


def build_all(force: bool = False) -> list[Path]:
    out = []
    for k in BUILDERS:
        build(k, force=force)
        out.append(ART_DIR / f"{k}.png")
    return out
