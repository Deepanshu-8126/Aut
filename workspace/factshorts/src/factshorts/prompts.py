"""Prompt factory — turns the locked style tokens into agent prompts.

Use it to drive Antigravity / Veo / Sora / any external agent in the SAME style,
and keep the prompts in sync with what the Python renderer actually draws.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import style as S
from .renderer import Part


def master_agent_prompt(pack: dict | None = None) -> str:
    """The full system prompt + task prompt for an external video agent."""
    topic = (pack or {}).get("topic", "Why You Feel Deja Vu")
    ep = (pack or {}).get("episode", 42)
    cat = (pack or {}).get("category", "BRAIN FACTS")
    c = lambda name: "#%02X%02X%02X" % S.C[name]                       # noqa: E731
    return f"""You are FACTSHORTS ENGINE — a Vox + Johnny Harris + Kurzgesagt documentary generator.
It is the SAME visual system that the local Python renderer draws, so never invent a new look.

=== STYLE LOCK (do not change) ===
Background     : pure white {c('paper')} + light-gray dot grid {S.DOT_GRID['spacing']}px, ~20% opacity. No gradients.
Top pill       : black {c('ink')} rounded pill r={S.GEO['pill_h']//2}px h={S.GEO['pill_h']}px, white Inter Bold {S.TYPE['pill']}px
                 text: "FACTSHORTS • EP {ep} • {cat} • LIVE"  (LIVE word + dot in yellow)
Title          : Inter Black {S.TYPE['title']}px, line-height 0.98, {c('ink')}, tight tracking, centred
Subtitle       : Inter SemiBold {S.TYPE['subtitle']}px, gray {c('gray')}
Bottom bar     : black rounded bar (inset {S.GEO['bar_inset']}px, h={S.GEO['bar_h']}px) with progress dots,
                 Inter Bold {S.TYPE['bottombar']}px: "PART X/7: BADGE • metric"
Palette        : yellow {c('yellow')} highlights/glow | blue {c('blue')} trails/arrows | red {c('red')} fail only
                 green {c('green')} healthy only | gray {c('gray')} secondary
Illustration   : 3D/vector hybrid object centred, soft shadow, yellow outer glow ~36px blur 45% opacity
Icons          : outline only, 2.5px stroke, rounded, black or yellow. Never filled emoji icons.
Canvas         : 1080x1920, margin {S.MARGIN}px, safe area {S.SAFE}px, Inter only. No text cutoff ever.

=== ANIMATION LOCK (identical to renderer timing) ===
0.00-0.35s  pill pop  scale 0.8->1.0 (out-back) | title slide up 40px + fade (easeOutCubic)
0.15-0.50s  subtitle fade + 24px rise
0.42-1.20s  hero pops scale 0.7->1.0 elastic, yellow glow breathes (blur 36 -> 56 -> 36)
0.42-1.20s  blue/better trails draw with stroke-dasharray 1.2s + glow moving along path
1.20-2.00s  yellow boxes pop 0.6->1.0 elastic; inner text types 25ms/char (typewriter tick SFX)
2.00-2.80s  metrics count up 0->target 0.8s easeOut; yellow underline draws left->right
0.50s+      bottom bar slides up 0.4s; progress dots fill; PART counter ticks
2.80-5.00s  hold with 1.02 breathing pulse on the hero
Duration    : 4-6s per part, 28-32s total, 24-30 fps, 1080x1920, CRF 19

=== SOUND DESIGN ===
whoosh in on title • exponential pop per yellow box • digital glitch when circuits draw •
typewriter ticks on annotation text • soft 110Hz/165Hz ambient pad • ding on final CTA.
Lo-fi electronic bed ~85 BPM, no vocals, no lyrics.

=== 7-PART FORMULA ===
1 HOOK     big mystery + "97%"-style stat + glowing hero
2 FACT 1   first mechanism diagram (signal path, blue trail)
3 FACT 2   second mechanism (collision / misfire inside the brain)
4 FACT 3   duration timeline, ruler bar 0s -> 30s filling yellow
5 FACT 4   trigger comparison, bar chart (normal vs triggered = 2x)
6 FACT 5   twist/benefit, green check, reassurance
7 PAYOFF   3 icon takeaways + yellow CTA pill + newest-line statement

=== TASK ===
TOPIC: "{topic}"   EPISODE: {ep}   CATEGORY: {cat}
Generate 7 images 1080x1920 in the locked style (no cutoff, no watermark, 4K clean),
then animate them with the timeline above and export one 28-32s vertical Short.
"""


def image_prompt(part: Part, pack: dict | None = None) -> str:
    cat = (part.category or "FACTS").upper()
    return (f"Vertical 9:16 social explainer slide, 1080x1920, pure white background with a light "
            f"gray dot grid, top black rounded pill label reading \"FACTSHORTS • EP {part.episode} • "
            f"{cat} • LIVE\", huge black Inter headline \"{part.title}\", gray subtitle "
            f"\"{part.subtitle}\", centered {part.art.replace('_', ' ')} illustration with a soft "
            f"yellow glow, yellow highlight box, thin black bottom bar with progress dots, "
            f"minimal editorial Vox documentary design, crisp typography, no clipping, no watermark")


def animation_spec() -> dict:
    return {
        "entrance": "pill scale 0.8->1.0 out-back 0.30s; title slide-up 40px + fade 0.35s easeOutCubic",
        "subtitle": "fade + 24px rise, 0.15s delay",
        "hero_pop": "scale 0.7->1.0 elastic 0.75s at 0.42s; glow breathe blur 36->56->36",
        "trail": "stroke-dasharray draw 1.2s + glowing head 0.8s",
        "box_pop": "scale 0.6->1.0 elastic 0.45s + typewriter 25ms/char",
        "metrics": "count-up 0.8s easeOut + underline draw left->right 0.4s",
        "bottom_bar": "slide up 0.4s at 0.5s; dots fill; part counter tick",
        "hold": "1.02 breathing pulse every 1.6s",
        "per_part_seconds": 4.5,
        "series_seconds": "28-32",
        "fps": 24,
        "resolution": "1080x1920",
        "sfx": ["whoosh@0.02", "expop@0.55", "glitch@1.25", "typewriter ticks", "ding@CTA"],
    }


def ui_spec() -> dict:
    hexc = lambda n: "#%02X%02X%02X" % S.C[n]                          # noqa: E731
    return {
        "style_name": "White Minimal Box v1 (renderer-locked)",
        "canvas": {"w": S.CANVAS[0], "h": S.CANVAS[1], "margin": S.MARGIN, "safe": S.SAFE},
        "background": f"{hexc('paper')} + dot grid {S.DOT_GRID['spacing']}px "
                      f"{int(S.DOT_GRID['opacity']*100)}%",
        "top_pill": {"fill": hexc("ink"), "radius": S.GEO["pill_r"], "height": S.GEO["pill_h"],
                     "font": f"Inter Bold {S.TYPE['pill']}px"},
        "title": {"font": f"Inter Black {S.TYPE['title']}px", "color": hexc("ink"), "lh": 0.98},
        "subtitle": {"font": f"Inter SemiBold {S.TYPE['subtitle']}px", "color": hexc("gray")},
        "bottom_bar": {"fill": hexc("ink"), "height": S.GEO["bar_h"], "radius": S.GEO["bar_r"],
                       "font": f"Inter Bold {S.TYPE['bottombar']}px"},
        "colors": {k: hexc(k) for k in ("yellow", "blue", "red", "green", "gray", "ink")},
        "fonts": list(S.FONT_FILES),
    }


def write_style_files(out_dir: Path, pack: dict | None = None) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "MASTER_AGENT_PROMPT.md": master_agent_prompt(pack),
        "ui_spec.json": json.dumps(ui_spec(), indent=2),
        "animation_spec.json": json.dumps(animation_spec(), indent=2),
    }
    written = []
    for name, body in files.items():
        p = out_dir / name
        p.write_text(body)
        written.append(p)
    if pack:
        shots = out_dir / "image_prompts.md"
        parts = pack.get("parts", [])
        txt = "# Image prompts (one per part)\n\n"
        for i, p in enumerate(parts, 1):
            dummy = Part(idx=i, total=len(parts), title=p["title"], subtitle=p.get("subtitle", ""),
                         episode=pack.get("episode", 43), category=pack.get("category", "FACTS"),
                         art=p.get("art", "brain_hero"))
            txt += f"## PART {i}/7 — {p['badge']}\n\n{image_prompt(dummy)}\n\n"
        shots.write_text(txt)
        written.append(shots)
    return written
