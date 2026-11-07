"""The renderer: composes every slide from design tokens.

One code path serves both outputs:
    compose(part, t=None)  -> final still (the 1080x1920 PNG deliverable)
    compose(part, t=1.23)  -> the frame at that moment (used to build the MP4)

Animation timeline (locked to the spec):
    0.00-0.35  title slides up + fades, pill scales 0.8->1.0
    0.40-1.20  illustration pops (0.7->1.0 bounce) + yellow glow breathes
    1.20-2.00  yellow boxes pop (elastic) + typewriter 25ms/char
    2.00-2.80  metrics count up + underline draws left->right
    2.80-5.00  hold + subtle pulse
    +0.50      bottom bar slides up from the bottom
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Optional

from PIL import Image, ImageDraw, ImageFilter

from . import art as artlib
from . import style as S
from . import textutil as T

W, H = S.CANVAS
M = S.MARGIN
CONTENT_W = W - 2 * M


# ----------------------------------------------------------------- timelines
def prog(t: float, start: float, dur: float) -> float:
    if dur <= 0:
        return 1.0 if t >= start else 0.0
    return max(0.0, min(1.0, (t - start) / dur))


def out_cubic(x: float) -> float:
    return 1 - (1 - x) ** 3


def out_quint(x: float) -> float:
    return 1 - (1 - x) ** 5


def out_back(x: float, s: float = 1.9) -> float:
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def elastic(x: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    c = (2 * math.pi) / 3
    return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * c) + 1


def lerp(a: float, b: float, x: float) -> float:
    return a + (b - a) * x


@dataclass
class Part:
    """One slide of the 7-part series."""
    idx: int = 1
    total: int = 7
    badge: str = "HOOK"
    title: str = ""
    subtitle: str = ""
    layout: str = "hero"
    art: str = "brain_hero"
    art2: str | None = None
    episode: int = 42
    category: str = "BRAIN FACTS"
    channel: str = "FACTSHORTS"
    bottom: str = ""
    callouts: list[dict] = field(default_factory=list)     # boxes / labels
    metrics: list[dict] = field(default_factory=list)      # value + label (+icon)
    columns: list[dict] = field(default_factory=list)      # icon + head + sub
    ruler_labels: list[str] = field(default_factory=list)  # e.g. ["0 min", "10 min"]
    chart_label: str = "Frequency (%)"                     # y-axis caption
    bars: list[dict] = field(default_factory=list)
    footnote: str = ""
    headline: str = ""           # big statement under the art
    cta: str = ""
    diagram: str | None = None   # 'collision' | 'eye' | None
    accent: str = "yellow"
    duration: float = 5.0

    # -------------------------------------------------------------- helpers
    def pill_text(self) -> str:
        return f"{self.channel} • EP {self.episode} • {self.category} • LIVE"

    def bar_text(self) -> str:
        """PART 4/7: FACT 3 • 10-30 sec glitch — never repeats the badge twice."""
        tail = (self.bottom or "").strip()
        badge = (self.badge or "").strip()
        if tail.upper().startswith(badge.upper()):
            tail = tail[len(badge):].lstrip(" •:-|")
        if "-" in badge and badge.split("-")[0].strip() and \
                tail.upper().startswith(badge.split("-")[0].strip().upper()):
            tail = tail[len(badge.split("-")[0].strip()):].lstrip(" •:-|")
        return f"PART {self.idx}/{self.total}: {badge}" + (f" • {tail}" if tail else "")

    @classmethod
    def from_dict(cls, d: dict) -> "Part":
        keys = {f for f in cls.__dataclass_fields__}          # type: ignore[attr-defined]
        return cls(**{k: v for k, v in d.items() if k in keys})


# ------------------------------------------------------------------- canvas
@lru_cache(maxsize=2)
def _bg_rgba(_seed: int = 0) -> Image.Image:
    return _background(1).convert("RGBA")


@lru_cache(maxsize=4)
def _background(scale: int = 1) -> Image.Image:
    """White paper + light gray dot grid (cached: it never changes)."""
    w, h = W // scale, H // scale
    img = Image.new("RGB", (w, h), S.C["paper"])
    d = ImageDraw.Draw(img)
    step = max(6, S.DOT_GRID["spacing"] // scale)
    r = max(1, S.DOT_GRID["radius"] // max(1, scale // 2))
    col = tuple(int(255 - (255 - c) * S.DOT_GRID["opacity"]) for c in S.C["dot"])
    for y in range(step // 2, h, step):
        for x in range(step // 2, w, step):
            d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    return img


def new_canvas(scale: int = 1) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    layer = _bg_rgba().copy()
    return layer, ImageDraw.Draw(layer)


# ------------------------------------------------------------------- pieces
def _fg_layer() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def _paste_alpha(base: Image.Image, layer: Image.Image, alpha: int = 255, dy: int = 0):
    if alpha <= 0:
        return
    if alpha < 255:
        a = layer.getchannel("A").point(lambda v: int(v * alpha / 255))
        layer = layer.copy()
        layer.putalpha(a)
    base.alpha_composite(layer, (0, dy))


def paste_scaled(base: Image.Image, img: Image.Image, center: tuple[int, int], scale: float,
                 alpha: int = 255):
    if scale <= 0.001 or alpha <= 0:
        return
    w = max(1, int(img.width * scale))
    h = max(1, int(img.height * scale))
    im = img.resize((w, h), Image.LANCZOS if scale < 1 else Image.BICUBIC)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(im, (int(center[0] - w / 2), int(center[1] - h / 2)))
    _paste_alpha(base, layer, alpha)


def draw_pill(base: Image.Image, part: Part, scale_f: float = 1.0, alpha: int = 255):
    txt = part.pill_text()
    fnt = S.font("Bold", S.TYPE["pill"])
    pad_x, h_pill = 46, S.GEO["pill_h"]
    tw = T.text_size(txt, fnt)[0]
    w_pill = tw + pad_x * 2
    x0, y0 = (W - w_pill) / 2, S.GEO["pill_y"]
    layer, d = _fg_layer()
    d.rounded_rectangle((x0, y0, x0 + w_pill, y0 + h_pill), radius=S.GEO["pill_r"],
                        fill=S.rgba("ink"))
    x = x0 + pad_x
    y = y0 + (h_pill - fnt.size) / 2 - 4
    head, tail = txt.split("• LIVE")
    d.text((x, y), head + "• ", font=fnt, fill=(255, 255, 255, 255))
    x += d.textlength(head + "• ", font=fnt)
    d.text((x, y), "LIVE", font=fnt, fill=S.rgba("yellow"))
    # live dot
    dx = x + d.textlength("LIVE ", font=fnt) + 2
    d.ellipse((dx, y + fnt.size * 0.30, dx + 14, y + fnt.size * 0.30 + 14),
              fill=S.rgba("yellow"))
    if scale_f != 1.0:
        cx, cy = W / 2, y0 + h_pill / 2
        cw, ch = w_pill, h_pill
        tmp = Image.new("RGBA", (int(cw * 1.4) + 8, int(ch * 1.4) + 8), (0, 0, 0, 0))
        tmp.alpha_composite(layer.crop((int(x0), int(y0), int(x0 + w_pill), int(y0 + h_pill))),
                            (int(cw * 0.2), int(ch * 0.2)))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        s = scale_f
        tmp = tmp.resize((max(1, int(tmp.width * s)), max(1, int(tmp.height * s))), Image.LANCZOS)
        layer.alpha_composite(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)))
    _paste_alpha(base, layer, alpha)


def _soft_shadow(d: ImageDraw.ImageDraw, box, radius, blur=18, alpha=30, dy=10):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((box[0], box[1] + dy, box[2], box[3] + dy),
                                         radius=radius, fill=(0, 0, 0, alpha))
    return sh.filter(ImageFilter.GaussianBlur(blur))


def draw_yellow_box(base: Image.Image, box, lines: list[str], font_size: int,
                    fill="yellow", text_color="ink", radius=28, scale_f=1.0, alpha=255,
                    chars: float | None = None, pad=(34, 26), stroke=None):
    """The signature yellow annotation box with typewriter text."""
    x0, y0, x1, y1 = box
    layer, d = _fg_layer()
    sh = _soft_shadow(d, box, radius)
    layer.alpha_composite(sh)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, fill=S.rgba(fill),
                        outline=S.rgba(stroke) if stroke else None, width=3 if stroke else 0)
    fnt = S.font("Bold", font_size)
    tx, ty = x0 + pad[0], y0 + pad[1]
    T.draw_block(d, tx, ty, lines, fnt, S.rgba(text_color), line_h=1.06,
                 chars=chars)
    _composite_transformed(base, layer, box, scale_f, alpha, radius)


def _composite_transformed(base, layer, box, scale_f, alpha, radius=28):
    if scale_f != 1.0 and scale_f > 0.001:
        sub = layer.crop(tuple(int(v) for v in box))
        s = scale_f
        sub = sub.resize((max(1, int(sub.width * s)), max(1, int(sub.height * s))), Image.LANCZOS)
        cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
        holder = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        holder.alpha_composite(sub, (int(cx - sub.width / 2), int(cy - sub.height / 2)))
        layer = holder
    _paste_alpha(base, layer, alpha)


def draw_label(base: Image.Image, text: str, sub: str | None, anchor_xy, text_xy,
               color="yellow", alpha=255, size=None, leader=True, sub_size=None, side="left"):
    """Small caption with a leader line dot, e.g. 'TEMPORAL LOBE / memory encoding'."""
    size = size or S.TYPE["label"]
    layer, d = _fg_layer()
    fnt = S.font("Black", size)
    sub_f = S.font("Medium", sub_size or int(size * 0.78))
    tx, ty = text_xy
    # keep the caption inside the canvas no matter what the caller asked for
    tw = d.textlength(text, font=fnt)
    sw = d.textlength(sub, font=sub_f) if sub else 0
    tx = max(S.MARGIN, min(tx, W - S.MARGIN - max(tw, sw)))
    ty = max(S.GEO["title_y"] + 120, min(ty, S.GEO["bar_bottom"] - 150))
    if leader:
        d.line((anchor_xy[0], anchor_xy[1], tx - (14 if side == "left" else -14), ty + size * 0.35),
               fill=S.rgba(color, 210), width=3)
        d.ellipse((anchor_xy[0] - 8, anchor_xy[1] - 8, anchor_xy[0] + 8, anchor_xy[1] + 8),
                  fill=S.rgba(color))
    halo = (255, 255, 255, 225)
    d.text((tx, ty), text, font=fnt, fill=S.rgba(color), stroke_width=4, stroke_fill=halo)
    if sub:
        d.text((tx, ty + size * 1.22), sub, font=sub_f, fill=S.rgba("ink", 225),
               stroke_width=3, stroke_fill=halo)
    _paste_alpha(base, layer, alpha)


def draw_headline(base: Image.Image, xy, lines: list[str], font_size=52, align="center",
                  width=CONTENT_W, alpha=255, chars=None, color="ink", weight="Bold",
                  underline=False, underline_w=None):
    layer, d = _fg_layer()
    fnt = S.font(weight, font_size)
    T.draw_block(d, xy[0], xy[1], lines, fnt, S.rgba(color), line_h=1.04, align=align,
                 width=width, chars=chars)
    if underline:
        y = xy[1] + int(len(lines) * font_size * 1.04) + 6
        x0 = xy[0] if align == "left" else xy[0] + (width - (underline_w or width * 0.6)) / 2
        d.rectangle((x0, y, x0 + (underline_w or width * 0.6), y + 12), fill=S.rgba("yellow"))
    _paste_alpha(base, layer, alpha)


def draw_metric(base: Image.Image, center, value: str, label: str, size=None, alpha=255,
                color="ink", show_underline=True, underline_p=1.0, icon=None):
    size = size or S.TYPE["metric"]
    layer, d = _fg_layer()
    fnt = S.font("Black", size)
    lab_f = S.font("Medium", int(size * 0.46))
    vw = d.textlength(value, font=fnt)
    lw = d.textlength(label, font=lab_f)
    cx, cy = center
    d.text((cx - vw / 2, cy), value, font=fnt, fill=S.rgba(color))
    d.text((cx - lw / 2, cy + size * 1.02), label, font=lab_f, fill=S.rgba("gray"))
    if show_underline:
        uw = vw * underline_p
        d.rectangle((cx - uw / 2, cy + size * 0.98, cx + uw / 2, cy + size * 0.98 + 10),
                    fill=S.rgba("yellow"))
    if icon:
        draw_icon(d, icon, (cx, cy - size * 1.30), int(size * 0.58), color="ink")
    _paste_alpha(base, layer, alpha)


# --------------------------------------------------------------------- icons
def draw_icon(d: ImageDraw.ImageDraw, name: str, center, size: int, color="ink", width=3):
    """Outline 2-3px icons, no fill (spec: outline style only)."""
    cx, cy = center
    s = size / 2
    col = S.rgba(color)
    lw = max(2, int(width))
    box = (cx - s, cy - s, cx + s, cy + s)
    if name == "clock":
        d.ellipse(box, outline=col, width=lw)
        d.line((cx, cy, cx, cy - s * 0.55), fill=col, width=lw)
        d.line((cx, cy, cx + s * 0.45, cy + s * 0.2), fill=col, width=lw)
    elif name == "people":
        for i, dx in enumerate((-s * 0.5, 0, s * 0.5)):
            r = s * (0.30 if i == 1 else 0.26)
            hx = cx + dx
            hy = cy - s * 0.35 if i == 1 else cy - s * 0.22
            d.ellipse((hx - r, hy - r, hx + r, hy + r), outline=col, width=lw)
            bw = r * 1.7
            d.arc((hx - bw, hy + r * 0.4, hx + bw, hy + r * 0.4 + bw * 1.5), 200, 340,
                  fill=col, width=lw)
    elif name == "check":
        d.ellipse(box, outline=col, width=lw)
        d.line((cx - s * 0.45, cy + s * 0.02, cx - s * 0.08, cy + s * 0.4), fill=col, width=lw + 1)
        d.line((cx - s * 0.08, cy + s * 0.4, cx + s * 0.5, cy - s * 0.4), fill=col, width=lw + 1)
    elif name == "warning":
        d.polygon([(cx, cy - s), (cx + s, cy + s * 0.7), (cx - s, cy + s * 0.7)],
                  outline=col, width=lw)
        d.line((cx, cy - s * 0.25, cx, cy + s * 0.25), fill=col, width=lw)
        d.ellipse((cx - lw / 2, cy + s * 0.42, cx + lw / 2, cy + s * 0.42 + lw), fill=col)
    elif name == "brain":
        for a0, a1 in ((92, 292), (272, 452), (358, 214), (88, 268)):
            sub = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            sd = ImageDraw.Draw(sub)
            sd.arc((cx - s, cy - s * 0.86, cx + s * 0.22, cy + s * 0.44), a0, a1,
                   fill=col, width=lw)
            sd.arc((cx - s * 0.12, cy - s * 0.86, cx + s, cy + s * 0.44), a0, a1,
                   fill=col, width=lw)
            sd.arc((cx - s * 0.96, cy - s * 0.12, cx + s * 0.34, cy + s), a0, a1,
                   fill=col, width=lw)
            sd.arc((cx - s * 0.24, cy - s * 0.12, cx + s * 0.98, cy + s), a0, a1,
                   fill=col, width=lw)
            d._image.alpha_composite(sub)
        d.line((cx - s * 0.15, cy - s * 0.5, cx + s * 0.1, cy - s * 0.2, cx - s * 0.1, cy + s * 0.2),
               fill=col, width=lw, joint="curve")
    elif name == "shield":
        d.polygon([(cx, cy - s), (cx + s * 0.82, cy - s * 0.6), (cx + s * 0.82, cy + s * 0.15),
                   (cx, cy + s), (cx - s * 0.82, cy + s * 0.15), (cx - s * 0.82, cy - s * 0.6)],
                  outline=col, width=lw)
        d.line((cx - s * 0.3, cy, cx - s * 0.05, cy + s * 0.28), fill=col, width=lw)
        d.line((cx - s * 0.05, cy + s * 0.28, cx + s * 0.36, cy - s * 0.32), fill=col, width=lw)
    elif name == "moon":
        d.arc((cx - s, cy - s, cx + s, cy + s), 60, 300, fill=col, width=lw)
        d.arc((cx - s * 0.5, cy - s * 1.6, cx + s * 1.1, cy + s * 0.3), 120, 330, fill=col, width=lw)
    elif name == "chart":
        d.line((cx - s, cy + s, cx - s, cy - s), fill=col, width=lw)
        d.line((cx - s, cy + s, cx + s, cy + s), fill=col, width=lw)
        d.rectangle((cx - s * 0.55, cy - s * 0.1, cx - s * 0.05, cy + s), outline=col, width=lw)
        d.rectangle((cx + s * 0.15, cy - s * 0.75, cx + s * 0.65, cy + s), outline=col, width=lw)
    elif name == "eye":
        d.arc((cx - s, cy - s * 0.8, cx + s, cy + s * 0.8), 180, 360, fill=col, width=lw)
        d.arc((cx - s, cy - s * 0.8, cx + s, cy + s * 0.8), 0, 180, fill=col, width=lw)
        d.ellipse((cx - s * 0.28, cy - s * 0.28, cx + s * 0.28, cy + s * 0.28),
                  outline=col, width=lw)
    elif name == "pulse":
        pts = [(cx - s, cy), (cx - s * 0.45, cy), (cx - s * 0.2, cy - s * 0.75),
               (cx + s * 0.1, cy + s * 0.7), (cx + s * 0.35, cy), (cx + s, cy)]
        d.line(pts, fill=col, width=lw, joint="curve")
    elif name == "delta":
        d.polygon([(cx, cy - s), (cx + s, cy + s * 0.8), (cx - s, cy + s * 0.8)],
                  outline=col, width=lw)
    else:
        d.ellipse(box, outline=col, width=lw)


def draw_arrows(base: Image.Image, arrows: list[dict], alpha: int = 255, draw_p: float = 1.0):
    """blue/yellow circuit arrows with a glowing trail (draw_p animates the stroke)."""
    layer, d = _fg_layer()
    for a in arrows:
        col = S.rgba(a.get("color", "blue"), alpha)
        p0, p1 = a["p0"], a["p1"]
        ex = lerp(p0[0], p1[0], draw_p)
        ey = lerp(p0[1], p1[1], draw_p)
        d.line((p0[0], p0[1], ex, ey), fill=col, width=a.get("width", 6))
        head = a.get("head", 22)
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        if draw_p > 0.04:
            for s in (-1, 1):
                d.line((ex, ey, ex - head * math.cos(ang + s * 0.42),
                        ey - head * math.sin(ang + s * 0.42)), fill=col, width=a.get("width", 6))
        if a.get("glow"):
            gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(gl).line((p0[0], p0[1], ex, ey),
                                    fill=S.rgba(a.get("color", "blue"), 90), width=18)
            layer.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
    _paste_alpha(base, layer, alpha)


def draw_columns(base: Image.Image, columns: list[dict], y: int, alpha: int = 255,
                 reveal: float = 1.0):
    """3 icon + caption columns (spec: outline icons, no fill)."""
    if not columns:
        return
    n = len(columns)
    cell = CONTENT_W / n
    layer, d = _fg_layer()
    for i, col in enumerate(columns):
        if i >= math.ceil(reveal * n):
            continue
        cx = M + cell * (i + 0.5)
        r = 56
        d.ellipse((cx - r, y - r, cx + r, y + r), outline=S.rgba("gray_lt"), width=3)
        draw_icon(d, col.get("icon", "brain"), (cx, y), 58, color="ink")
        hf = S.font("Bold", S.TYPE["metric_sm"])
        sf = S.font("Medium", S.TYPE["body"])
        head = col.get("head", "")
        d.text((cx - d.textlength(head, font=hf) / 2, y + r + 22), head, font=hf,
               fill=S.rgba("ink"))
        sub = col.get("sub", "")
        d.text((cx - d.textlength(sub, font=sf) / 2, y + r + 22 + hf.size * 1.18), sub,
               font=sf, fill=S.rgba("gray"))
        if i:
            d.line((M + cell * i, y - 46, M + cell * i, y + 96), fill=(210, 210, 210, 255), width=2)
    _paste_alpha(base, layer, alpha)


def fallback_brain(base: Image.Image, center, size: int = 560, alpha: int = 255,
                   glow: bool = True):
    """Vector brain used when no illustration asset is available (never ship an empty slide)."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx, cy, s = center[0], center[1], size / 2
    col = (232, 232, 232, 255)
    edge = (120, 120, 120, 255)
    if glow:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse((cx - s * 1.15, cy - s * 0.95, cx + s * 1.15, cy + s * 1.05),
                                  fill=S.rgba("yellow", 46))
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(48)))
    d.ellipse((cx - s, cy - s * 0.82, cx + s * 0.95, cy + s * 0.72), fill=col, outline=edge, width=5)
    d.ellipse((cx - s * 1.02, cy - s * 0.1, cx + s * 0.4, cy + s * 0.95), fill=col, outline=edge, width=5)
    d.ellipse((cx - s * 0.15, cy - s * 0.2, cx + s * 0.95, cy + s * 0.95), fill=col, outline=edge, width=5)
    for i in range(7):
        x = cx - s * 0.55 + i * s * 0.22
        d.arc((x, cy - s * 0.6, x + s * 0.5, cy + s * 0.1), 200, 340, fill=edge, width=3)
    d.ellipse((cx + s * 0.25, cy + s * 0.25, cx + s * 0.85, cy + s * 0.8), fill=col,
              outline=edge, width=4)
    _paste_alpha(base, lay, alpha)


def draw_bars(base: Image.Image, bars: list[dict], area, alpha: int = 255, grow: float = 1.0):
    """Bar chart with count-up value labels."""
    if not bars:
        return
    x0, y0, x1, y1 = area
    layer, d = _fg_layer()
    n = len(bars)
    base_y = y1
    max_v = max(b["value"] for b in bars) or 1
    slot = (x1 - x0) / n
    d.line((x0, base_y, x1, base_y), fill=S.rgba("gray_lt"), width=3)
    for i, b in enumerate(bars):
        bw = slot * 0.52
        cx = x0 + slot * (i + 0.5)
        hgt = (base_y - y0) * (b["value"] / max_v) * grow
        col = b.get("color", "yellow")
        d.rounded_rectangle((cx - bw / 2, base_y - hgt, cx + bw / 2, base_y),
                            radius=14, fill=S.rgba(col))
        lab = b.get("display", "") or f"{int(b['value'])}"
        lf = S.font("Black", S.TYPE["metric"])
        # value label: dark text + colour underline (yellow on white is unreadable)
        lw_ = d.textlength(lab, font=lf)
        d.text((cx - lw_ / 2, base_y - hgt - lf.size * 1.20), lab, font=lf, fill=S.rgba("ink"))
        d.rectangle((cx - lw_ / 2, base_y - hgt - lf.size * 1.20 + lf.size * 0.98,
                     cx + lw_ / 2, base_y - hgt - lf.size * 1.20 + lf.size * 0.98 + 9),
                    fill=S.rgba(col if col != "gray" else "gray_lt"))
        nf = S.font("Bold", S.TYPE["metric_sm"])
        name = b["label"]
        d.text((cx - d.textlength(name, font=nf) / 2, base_y + 22), name, font=nf,
               fill=S.rgba("gray_lt" if col == "gray" else "ink"))
    _paste_alpha(base, layer, alpha)


def draw_ruler(base: Image.Image, area, label_left="0s", label_right="30s", fill_p=1.0,
               alpha: int = 255):
    """The 0s -> 30s timeline bar from PART 4/7."""
    x0, y0, x1, y1 = area
    layer, d = _fg_layer()
    d.rounded_rectangle((x0, y0, x1, y1), radius=(y1 - y0) // 2, outline=S.rgba("ink"), width=4)
    for i in range(31):
        tx = lerp(x0 + 16, x1 - 16, i / 30)
        th = 22 if i % 5 == 0 else 12
        d.line((tx, y0 - th, tx, y0 - 2), fill=S.rgba("gray_lt"), width=3)
    fw = (x1 - x0 - 10) * fill_p
    if fw > 6:
        d.rounded_rectangle((x0 + 5, y0 + 5, x0 + 5 + fw, y1 - 5), radius=(y1 - y0) // 2 - 4,
                            fill=S.rgba("yellow"))
    f_l = S.font("Bold", S.TYPE["label"])
    d.text((x0 - 8, y0 - 88), label_left, font=f_l, fill=S.rgba("ink"))
    d.text((x1 - d.textlength(label_right, font=f_l), y0 - 88), label_right, font=f_l,
           fill=S.rgba("ink"))
    _paste_alpha(base, layer, alpha)


def draw_rotated_text(base: Image.Image, xy, text: str, size=30, color="gray"):
    tmp = Image.new("RGBA", (600, 60), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((0, 0), text, font=S.font("Medium", size), fill=S.rgba(color))
    tmp = tmp.crop(tmp.getbbox() or (0, 0, 1, 1)).rotate(90, expand=True)
    base.alpha_composite(tmp, (int(xy[0]), int(xy[1])))


def draw_bottom_bar(base: Image.Image, part: Part, slide_p: float = 1.0, alpha: int = 255,
                    dots_p: float = 1.0):
    h_bar = S.GEO["bar_h"]
    y0 = S.GEO["bar_bottom"] + (1 - slide_p) * (h_bar + 60)
    box = (S.GEO["bar_inset"], y0, W - S.GEO["bar_inset"], y0 + h_bar)
    layer, d = _fg_layer()
    layer.alpha_composite(_soft_shadow(d, box, S.GEO["bar_r"], blur=22, alpha=34, dy=8))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=S.GEO["bar_r"], fill=S.rgba("ink"))
    fnt = S.font("Bold", S.TYPE["bottombar"])
    txt = part.bar_text()
    d.text((W / 2 - d.textlength(txt, font=fnt) / 2, y0 + (h_bar - fnt.size) / 2 - 6), txt,
           font=fnt, fill=(255, 255, 255, 255))
    # progress dots
    dots = part.total
    dw, gap = 12, 12
    total_w = dots * dw + (dots - 1) * gap
    dx = W / 2 - total_w / 2
    for i in range(dots):
        on = (i + 1) <= round(dots_p * dots)
        col = S.rgba("yellow") if on else (255, 255, 255, 70)
        d.rounded_rectangle((dx + i * (dw + gap), y0 + h_bar - 22, dx + i * (dw + gap) + dw,
                             y0 + h_bar - 14), radius=4, fill=col)
    # tick marks (visual texture on the left, per reference style)
    for i in range(6):
        tx = box[0] + 26 + i * 14
        d.line((tx, y0 + h_bar - 44, tx, y0 + h_bar - 30), fill=(255, 255, 255, 90), width=3)
    _paste_alpha(base, layer, alpha)


def draw_cta(base: Image.Image, text: str, y: int, alpha: int = 255, p: float = 1.0):
    fnt = S.font("Bold", S.TYPE["cta"])
    tw = T.text_size(text, fnt)[0]
    box = (W / 2 - (tw + 90) / 2, y, W / 2 + (tw + 90) / 2, y + 118)
    draw_yellow_box(base, box, [text], S.TYPE["cta"], radius=59, alpha=alpha,
                    scale_f=lerp(0.8, 1.0, p), pad=(45, 30))


def draw_spotlight(base: Image.Image, center, radius: int, alpha_p: float):
    if alpha_p <= 0.01:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((center[0] - radius, center[1] - radius,
                                 center[0] + radius, center[1] + radius),
                                fill=S.rgba("yellow", int(60 * alpha_p)))
    base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(radius * 0.45)))


# --------------------------------------------------------------- composition
@lru_cache(maxsize=24)
def _cached_hero_art(key: str, box: tuple[int, int], _mtime: float = 0.0):
    """Decode + fit + build the glow layer once per (art, box) instead of per frame."""
    img = artlib.fit(artlib.fetch_art(key), box)
    glow_layer, pad = artlib.glow(img, blur=40, alpha=155)
    return img, glow_layer


def _hero(base: Image.Image, part: Part, tl: dict):
    """Central illustration + glow + optional callouts/labels."""
    try:
        img = artlib.fetch_art(part.art)
    except Exception as e:                                     # noqa: BLE001
        print(f"  [warn] art '{part.art}' unavailable ({e}); using vector fallback")
        img = None
    box = tl.get("hero_box", (int(S.GEO["hero_max_w"] * 0.96), int(S.GEO["hero_max_h"])))
    center = tl.get("hero_center", S.GEO["hero_center"])
    if img is None:
        fallback_brain(base, center, int(box[1] * 1.05), alpha=tl["hero_alpha"])
        return (box[0], box[1], center)
    if img is not None:
        art_path = artlib.ART_DIR / f"{part.art}.png"
        mtime = art_path.stat().st_mtime if art_path.exists() else 0.0
        img, glow_layer = _cached_hero_art(part.art, (int(box[0]), int(box[1])), mtime)
        pulse = 1.0 + 0.012 * math.sin(tl.get("t", 0) * 2 * math.pi / 1.6)
        scale = tl["hero_scale"] * pulse
        paste_scaled(base, glow_layer, center, scale,
                     alpha=int(tl["hero_alpha"] * tl.get("glow_alpha_p", 1.0)))
        paste_scaled(base, img, center, scale, alpha=tl["hero_alpha"])
        return (img.width * scale, img.height * scale, center)
    return (0, 0, center)


def _callout_boxes(base: Image.Image, part: Part, tl: dict, default_area=None):
    """Yellow annotation boxes with typewriter text."""
    for i, c in enumerate(part.callouts):
        if c.get("kind") in ("label", "arrows"):
            continue
        st = tl["boxes"].get(i, {"alpha": 255, "scale": 1.0, "chars": None})
        if st["alpha"] <= 0:
            continue
        box = tuple(c["box"]) if "box" in c else default_area
        lines = c["lines"] if isinstance(c.get("lines"), list) else [c.get("lines", "")]
        size = c.get("size", S.TYPE["label"])
        draw_yellow_box(base, box, lines, size, fill=c.get("fill", "yellow"),
                        text_color=c.get("text_color", "ink"), radius=c.get("radius", 26),
                        scale_f=st["scale"], alpha=st["alpha"], chars=st["chars"],
                        stroke=c.get("stroke"))


def compose(part: Part, t: Optional[float] = None) -> Image.Image:
    """Render one slide. t=None -> final state (PNG); t=float -> animation frame."""
    final = t is None
    tt = 0.0 if final else float(t)
    ttl = {"t": tt}

    base, _ = new_canvas()
    ttl["hero_alpha"] = 255 if final else int(255 * out_cubic(prog(tt, 0.42, 0.45)))
    ttl["hero_scale"] = 1.0 if final else elastic(prog(tt, 0.42, 0.75))
    ttl["hero_center"] = S.GEO["hero_center"]

    # ---- title block ----------------------------------------------------
    draw_w, _ = _fg_layer()
    d = ImageDraw.Draw(draw_w)
    fnt, lines, size = T.autofit(d, part.title, "Black", S.TYPE["title"], S.TYPE["title_min"],
                                 CONTENT_W, max_lines=3)
    ty = S.GEO["title_y"]
    dy = 0 if final else int(40 * (1 - out_cubic(prog(tt, 0.0, 0.35))))
    a = 255 if final else int(255 * out_cubic(prog(tt, 0.0, 0.35)))
    T.draw_block(d, M, ty + dy, lines, fnt, S.rgba("ink"), line_h=0.98, align="center",
                 width=CONTENT_W)
    sub_y = ty + int(len(lines) * size * 0.98) + 22
    if part.subtitle:
        sf = S.font("SemiBold", S.TYPE["subtitle"])
        sa = 255 if final else int(255 * out_cubic(prog(tt, 0.15, 0.35)))
        sdy = 0 if final else int(24 * (1 - out_cubic(prog(tt, 0.15, 0.35))))
        T.draw_block(d, M, sub_y + sdy, [part.subtitle], sf, S.rgba("gray"), align="center",
                     width=CONTENT_W)
    _paste_alpha(base, draw_w, a)
    content_top = sub_y + 96

    # ---- layout body ----------------------------------------------------
    p_pill = 1.0 if final else lerp(0.8, 1.0, out_back(prog(tt, 0.0, 0.30)))
    draw_pill(base, part, scale_f=p_pill, alpha=255 if final else
              int(255 * out_cubic(prog(tt, 0.0, 0.25))))

    layout = part.layout
    ttl["boxes"] = {}
    for i, c in enumerate(part.callouts):
        if c.get("kind") in ("label", "arrows"):
            continue
        st = prog(tt, 1.2 + 0.16 * i, 0.45) if not final else 1.0
        ttl["boxes"][i] = {
            "alpha": 255 if final else int(255 * out_cubic(st)),
            "scale": 1.0 if final else lerp(0.6, 1.0, elastic(st)),
            "chars": None if final else max(0.0, (tt - (1.35 + 0.16 * i)) / 0.025),
        }

    # ------------------------------------------------------------------
    # Band layout engine: measure first, then place — nothing may cross
    # the bottom bar or leave the canvas (spec: "no text cutoff").
    # ------------------------------------------------------------------
    AVAIL_BOTTOM = S.GEO["bar_bottom"] - 64
    CH = max(320, AVAIL_BOTTOM - content_top)
    layout = part.layout
    hero_band = lambda f0, f1: (content_top + int(CH * f0), content_top + int(CH * f1))  # noqa: E731

    if layout in ("hook", "hero", "diagram", "payoff"):
        if layout == "payoff":
            hc = (int(W / 2), content_top + int(CH * 0.22))
            hbox = (int(W * 0.74), int(CH * 0.38))
        elif layout == "diagram":
            hc = (int(W * 0.68), content_top + int(CH * 0.30))
            hbox = (int(W * 0.42), int(CH * 0.44))
        else:
            hc = (int(W / 2), content_top + int(CH * 0.35))
            hbox = (int(W * 0.94), int(CH * 0.60))
        ttl["hero_center"] = hc
        ttl["hero_box"] = hbox
        if layout in ("hook", "hero") and part.callouts and any(c.get("kind") == "label"
                                                                for c in part.callouts):
            hc = (int(W * 0.55), content_top + int(CH * 0.33))       # leave room for the caption
            ttl["hero_center"] = hc
        hero_geo = _hero(base, part, ttl)
        if layout == "payoff":
            draw_spotlight(base, hc, int(hbox[1] * 0.72),
                           0.55 + 0.45 * math.sin(tt * 2) if not final else 0.7)

    if layout in ("hook", "hero"):
        mets = part.metrics or []
        row_y = content_top + int(CH * 0.80)
        for i, m in enumerate(mets):
            p = 1.0 if final else out_cubic(prog(tt, 2.0 + 0.12 * i, 0.6))
            val = str(m.get("value", ""))
            shown = val
            if not final and m.get("count") is not None:
                shown = f"{int(round(float(m['count']) * p))}{m.get('suffix','')}"
            cx = W / 2 + (i - (len(mets) - 1) / 2) * 380
            draw_metric(base, (cx, row_y), shown, m.get("label", ""), size=S.TYPE["metric"],
                        alpha=int(255 * p), icon=m.get("icon"), underline_p=p)

    if layout == "timeline":
        icon_c = (int(W / 2), content_top + int(CH * 0.17))
        if part.art:
            try:
                icon = artlib.fit(artlib.fetch_art(part.art), (int(CH * 0.30), int(CH * 0.28)))
                paste_scaled(base, icon, icon_c,
                             ttl["hero_scale"] if not final else 1.0,
                             ttl["hero_alpha"] if not final else 255)
            except Exception:                                  # noqa: BLE001
                fallback_brain(base, icon_c, int(CH * 0.22))
        ruler = (M + 50, content_top + int(CH * 0.50), W - M - 50, content_top + int(CH * 0.50) + 96)
        fp = 1.0 if final else out_cubic(prog(tt, 2.0, 0.9))
        rl = part.ruler_labels or []
        draw_ruler(base, ruler, fill_p=fp,
                   label_left=rl[0] if len(rl) > 0 else "0s",
                   label_right=rl[1] if len(rl) > 1 else "30s")
        draw_columns(base, part.columns, content_top + int(CH * 0.76),
                     reveal=1.0 if final else prog(tt, 2.4, 0.6))
        if part.footnote:
            ff = S.font("Medium", S.TYPE["caption"])
            T.draw_block(ImageDraw.Draw(base), M, AVAIL_BOTTOM - 78, [part.footnote], ff,
                         S.rgba("gray"), align="center", width=CONTENT_W)

    if layout == "chart":
        if part.headline:
            draw_headline(base, (M, content_top + 6), [part.headline], font_size=S.TYPE["h2"],
                          underline=True, chars=None if final else max(0.0, (tt - 1.2) / 0.025))
        grow = 1.0 if final else out_cubic(prog(tt, 2.0, 0.9))
        top_y = content_top + (215 if part.headline else 60)
        area = (M + 150, top_y, W - M - 50, AVAIL_BOTTOM - (150 if part.footnote else 80))
        draw_bars(base, part.bars, area, grow=grow)
        draw_rotated_text(base, (M + 12, top_y - 120), part.chart_label or "Frequency (%)",
                          size=27)
        if part.footnote:
            ff = S.font("Medium", S.TYPE["caption"])
            T.draw_block(ImageDraw.Draw(base), M, AVAIL_BOTTOM - 44, [part.footnote], ff,
                         S.rgba("gray"), align="center", width=CONTENT_W)

    if layout == "diagram":
        band_cy = content_top + int(CH * 0.30)
        eye_art = None
        try:
            eye_art = artlib.fit(artlib.fetch_art(part.art2 or "eye"),
                                 (int(W * 0.30), int(CH * 0.26)))
            paste_scaled(base, eye_art, (int(W * 0.235), band_cy),
                         ttl["hero_scale"] if not final else 1.0,
                         ttl["hero_alpha"] if not final else 255)
        except Exception:                                      # noqa: BLE001
            eye_art = None
        arrows = []
        for c in part.callouts:
            if isinstance(c, dict) and c.get("kind") == "arrows":
                arrows = c.get("arrows", [])
        if not arrows:
            arrows = [{"p0": (int(W * 0.385), band_cy), "p1": (int(W * 0.50), band_cy),
                       "color": "blue", "width": 7, "glow": True}]
        draw_arrows(base, arrows, draw_p=1.0 if final else out_cubic(prog(tt, 0.8, 0.8)))
        for i, m in enumerate(part.metrics):
            p_ = 1.0 if final else out_cubic(prog(tt, 2.0 + 0.12 * i, 0.6))
            draw_metric(base, (int(W * 0.235), content_top + int(CH * 0.62)), m.get("value", ""),
                        m.get("label", ""), size=S.TYPE["metric_sm"] + 6, alpha=int(255 * p_),
                        underline_p=p_, color=m.get("color", "ink"), icon=m.get("icon"))
            if m.get("note"):
                draw_headline(base, (M, content_top + int(CH * 0.74)),
                              [str(m["note"])], font_size=S.TYPE["body"], color="gray")
        if part.footnote:
            ff = S.font("Medium", S.TYPE["caption"])
            T.draw_block(ImageDraw.Draw(base), M, AVAIL_BOTTOM - 76, [part.footnote], ff,
                         S.rgba("gray"), align="center", width=CONTENT_W)

    if layout == "payoff":
        hl_y = content_top + int(CH * 0.50)
        if part.headline:
            fnt_h, lines_h, _ = T.autofit(ImageDraw.Draw(base), part.headline, "Bold",
                                          S.TYPE["h2"], 34, CONTENT_W, max_lines=2)
            draw_headline(base, (M, hl_y), lines_h, font_size=fnt_h.size, align="center",
                          alpha=255 if final else int(255 * out_cubic(prog(tt, 1.4, 0.5))),
                          chars=None if final else max(0.0, (tt - 1.5) / 0.025))
        cta_y = AVAIL_BOTTOM - 130
        draw_columns(base, part.columns, cta_y - 200,
                     reveal=1.0 if final else prog(tt, 2.4, 0.6))
        if part.cta:
            draw_cta(base, part.cta, cta_y,
                     alpha=255 if final else int(255 * out_cubic(prog(tt, 2.8, 0.4))),
                     p=1.0 if final else out_back(prog(tt, 2.8, 0.5)))

    # ---- labels & annotation boxes --------------------------------------
    _callout_boxes(base, part, ttl, default_area=(M, H - 560, W - M, H - 420))
    for i, c in enumerate(part.callouts):
        if c.get("kind") != "label":
            continue
        a = 255 if final else int(255 * out_cubic(prog(tt, 1.6 + 0.16 * i, 0.4)))
        side = c.get("side", "left")
        anchor = tuple(c.get("anchor", (540, content_top + int(CH * 0.4))))
        if layout in ("hook", "hero"):
            # caption band under the hero, above the metric row
            ty = content_top + int(CH * 0.63) + i * 96
            tx = M + 24 if side == "left" else int(W * 0.52)
        elif layout == "diagram":
            ty = content_top + int(CH * (0.50 + 0.14 * i))
            tx = M + 16 if side == "left" else int(W * 0.52)
        else:
            tx, ty = tuple(c.get("xy", (M + 20, content_top + int(CH * 0.6))))
        draw_label(base, c["text"], c.get("sub"), anchor, (tx, ty),
                   color=c.get("color", "yellow"), alpha=a, side=side)

    # ---- bottom bar ------------------------------------------------------
    sp = 1.0 if final else out_cubic(prog(tt, 0.5, 0.4))
    dp = 1.0 if final else prog(tt, 0.9, 0.7)
    draw_bottom_bar(base, part, slide_p=sp if not final else 1.0, dots_p=dp)

    return base.convert("RGB")


def compose_scaled(part: Part, t: Optional[float] = None, scale: int = 1) -> Image.Image:
    img = compose(part, t)
    if scale > 1:
        img = img.resize((W // scale, H // scale), Image.LANCZOS)
    return img
