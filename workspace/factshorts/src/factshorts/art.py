"""Illustration library: fetch -> knockout white -> trim -> cache as RGBA PNG.

Free-by-default: if no API key exists we use the public Pollinations endpoint
(no key, no signup).  You can also drop your own PNGs (already background-free)
into assets/illustrations/<key>.png and the pipeline will use them instead.
"""
from __future__ import annotations

import hashlib
import io
import os
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
ART_DIR = ROOT / "assets" / "illustrations"
ART_DIR.mkdir(parents=True, exist_ok=True)

STYLE_SUFFIX = ("Vox documentary explainer illustration, matte white and light gray "
                "anatomically accurate, soft studio lighting, isolated on pure white "
                "background, no text, no labels, no watermark, centered, ultra clean, 4k")

ILLUSTRATIONS: dict[str, str] = {
    "brain_hero":   f"3D render of a human brain, side profile, warm yellow rim light glowing on the temporal lobe, {STYLE_SUFFIX}",
    "brain_glow":   f"3D render of a human brain glowing from the inside with golden yellow light, particles and sparks, {STYLE_SUFFIX}",
    "brain_flat":   f"3D render of a human brain, plain matte gray, neutral pose, {STYLE_SUFFIX}",
    "brain_dark":   f"3D render of a human brain, dark gray graphite material, dramatic side light, {STYLE_SUFFIX}",
    "brain_cut":    f"medical cross-section x-ray style diagram of a human brain showing hippocampus highlighted in bright yellow, clean line art, {STYLE_SUFFIX}",
    "eye":          f"3D render of a single human eye, highly detailed iris, dramatic macro, {STYLE_SUFFIX}",
    "clock_brain":  f"minimal icon illustration: half brain half clock face merged, black outline with yellow accent, {STYLE_SUFFIX}",
    "chip":         f"3D render of a small silicon chip with glowing yellow circuit traces, {STYLE_SUFFIX}",
    "sleep":        f"3D render of a crescent moon with soft yellow glow and floating z letters, {STYLE_SUFFIX}",
    "shield_brain": f"minimal icon illustration of a shield containing a brain, green and white, {STYLE_SUFFIX}",
    "world_map":    f"flat vector world map, thin dark gray strokes, minimal, {STYLE_SUFFIX}",
    "suez":         f"clean technical illustration of a container ship passing through a desert canal, blueprint style, {STYLE_SUFFIX}",
}


def _cache_path(key: str, src: str) -> Path:
    h = hashlib.md5(src.encode()).hexdigest()[:8]
    return ART_DIR / f"{key}.png"


def _knockout_white(img: Image.Image, hi: int = 246, lo: int = 226) -> Image.Image:
    """Turn the white studio background into transparency (with edge de-haloing)."""
    img = img.convert("RGB")
    a = np.asarray(img).astype(np.float32)
    whiteness = a.min(axis=2)                       # pure white -> 255
    alpha = np.clip((hi - whiteness) / (hi - lo), 0.0, 1.0)
    # keep already-dark pixels fully opaque even if the source is light gray art
    alpha = np.where(whiteness < lo, 1.0, alpha)
    # decontaminate: remove white bleed from semi transparent edge pixels
    with np.errstate(divide="ignore", invalid="ignore"):
        a2 = (a - (1.0 - alpha)[..., None] * 255.0) / np.maximum(alpha, 1e-3)[..., None]
    a2 = np.clip(a2, 0, 255)
    out = np.dstack([a2, alpha * 255.0]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def _trim(img: Image.Image, pad: int = 6) -> Image.Image:
    bbox = img.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    if not bbox:
        return img
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(img.width, x1 + pad), min(img.height, y1 + pad)
    return img.crop((x0, y0, x1, y1))


@lru_cache(maxsize=32)
def _load_cached(path_str: str):
    return Image.open(path_str).convert("RGBA")


def art_mode() -> str:
    """auto (default) -> AI only when a token exists, else the offline vector engine."""
    mode = (os.environ.get("FACTSHORTS_ART") or "auto").lower()
    if mode == "auto":
        has_token = bool(os.environ.get("POLLINATIONS_TOKEN") or os.environ.get("HF_TOKEN")
                         or os.environ.get("OPENAI_API_KEY"))
        return "ai" if has_token else "vector"
    return mode


def fetch_art(key: str, width: int = 1024, height: int = 1024, force: bool = False,
              model: str = "flux") -> Image.Image:
    """Load (or create) one transparent illustration.

    Order: local file in assets/illustrations -> AI provider (if a token is set)
    -> offline vector engine.  Always returns a usable RGBA image.
    """
    path = ART_DIR / f"{key}.png"
    if path.exists() and not force:
        return _load_cached(str(path))

    if art_mode() == "ai":
        try:
            prompt = ILLUSTRATIONS.get(key, f"{key}. {STYLE_SUFFIX}")
            from .providers import generate_image_bytes      # late import: avoids cycle
            raw = generate_image_bytes(prompt, width=width, height=height, model=model)
            img = raw if isinstance(raw, Image.Image) else Image.open(io.BytesIO(raw))
            art = _trim(_knockout_white(img.convert("RGB")))
            art.save(path)
            return art
        except Exception as e:                               # noqa: BLE001
            print(f"  [warn] AI art for '{key}' failed ({e}); falling back to vector engine")

    from . import vectorart                               # late import: heavy module
    return vectorart.build(key, force=force)


def import_art(src: str | Path, key: str, bbox: tuple[int, int, int, int] | None = None,
               knockout: bool = True) -> Path:
    """Use your own generated art (e.g. cropped out of a reference frame) as a library key."""
    img = Image.open(src).convert("RGB")
    if bbox:
        img = img.crop(bbox)
    if knockout:
        img = _trim(_knockout_white(img))
    out = ART_DIR / f"{key}.png"
    img.save(out)
    return out


def fit(img: Image.Image, box: tuple[int, int], contain: bool = True) -> Image.Image:
    bw, bh = box
    r = min(bw / img.width, bh / img.height) if contain else max(bw / img.width, bh / img.height)
    return img.resize((max(1, int(img.width * r)), max(1, int(img.height * r))), Image.LANCZOS)


def glow(img: Image.Image, blur: int = 34, alpha: int = 132, color: tuple = (255, 214, 10),
         spread: int = 1.0) -> Image.Image:
    """Yellow outer glow layer sized for the given art (returns a same-size RGBA pad)."""
    pad = int(blur * 2.2 * spread)
    canvas = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    silhouette = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    silhouette.paste(img, (pad, pad), img)
    alpha_ch = silhouette.getchannel("A").filter(ImageFilter.GaussianBlur(blur))
    alpha_ch = alpha_ch.point(lambda v: min(255, int(v * (alpha / 255.0) * 1.8)))
    layer = Image.new("RGBA", canvas.size, color + (0,))
    layer.putalpha(alpha_ch)
    return layer, pad
