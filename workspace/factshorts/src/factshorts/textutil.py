"""Text measuring, wrapping, auto-fit and animated draw helpers."""
from __future__ import annotations

from typing import Iterable, Sequence

from PIL import Image, ImageDraw

from . import style as S


def measure(draw: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def text_size(text: str, fnt) -> tuple[int, int]:
    img = Image.new("L", (8, 8))
    return measure(ImageDraw.Draw(img), text, fnt)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if measure(draw, trial, fnt)[0] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def autofit(draw: ImageDraw.ImageDraw, text: str, weight: str, start: int, min_size: int,
            max_w: int, max_lines: int = 3) -> tuple[object, list[str], int]:
    """Shrink until the block fits max_w and max_lines. Guarantees 'no text cutoff'."""
    size = start
    while size > min_size:
        fnt = S.font(weight, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines and all(measure(draw, l, fnt)[0] <= max_w for l in lines):
            return fnt, lines, size
        size -= 2
    fnt = S.font(weight, min_size)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines], min_size


def tracking_kern(fnt, size: int, tracking: float) -> float:
    return size * tracking


def draw_tracked(draw: ImageDraw.ImageDraw, xy, text: str, fnt, fill, tracking: float = 0.0,
                 anchor_left: bool = True):
    """PIL has no letter-spacing; emulate it for the pill / all-caps kicker text."""
    if not tracking:
        draw.text(xy, text, font=fnt, fill=fill)
        return
    x, y = xy
    k = tracking_kern(fnt, fnt.size, tracking)
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + k


def draw_block(draw: ImageDraw.ImageDraw, x: int, y: int, lines: Sequence[str], fnt,
               fill, line_h: float = 0.96, align: str = "left", width: int = 0,
               spacing: float = 0.0, chars: float | None = None):
    """Draw multi-line text. `chars` = typewriter budget (None = full text)."""
    left = 0
    for line in lines:
        shown = line
        if chars is not None:
            if chars <= 0:
                shown = ""
            elif chars < len(line):
                shown = line[: int(chars)]
        if shown:
            lw = draw.textlength(shown, font=fnt)
            dx = x
            if align == "center":
                dx = x + (width - lw) / 2
            elif align == "right":
                dx = x + (width - lw)
            draw.text((dx, y), shown, font=fnt, fill=fill)
        if chars is not None:
            chars -= len(line) + 1
        y += int(fnt.size * line_h + spacing)
    return y


def block_height(lines: Iterable[str], fnt, line_h: float = 0.96, spacing: float = 0.0) -> int:
    lines = list(lines)
    if not lines:
        return 0
    return int(len(lines) * (fnt.size * line_h + spacing) - spacing)


def rrect_layer(size, box, radius, fill, shadow: bool = False, shadow_dy: int = 10,
                shadow_blur: int = 26, shadow_alpha: int = 28) -> Image.Image:
    """Rounded rect on a transparent layer, optional soft drop shadow."""
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    if shadow:
        from PIL import ImageFilter
        sh = Image.new("RGBA", size, (0, 0, 0, 0))
        d = ImageDraw.Draw(sh)
        d.rounded_rectangle((box[0], box[1] + shadow_dy, box[2], box[3] + shadow_dy),
                            radius=radius, fill=(0, 0, 0, shadow_alpha))
        sh = sh.filter(ImageFilter.GaussianBlur(shadow_blur * 0.5))
        layer.alpha_composite(sh)
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=fill)
    return layer
