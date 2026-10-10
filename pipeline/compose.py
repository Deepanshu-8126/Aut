"""Build a HyperFrames composition in a clean WHITE "daily code lesson" style.

Scene elements (all optional except heading/narration):
- code:      white code window, Shiki-highlighted, typed char-by-char in sync with narration
- terminal:  black terminal card with "$ command" + output lines
- tip:       yellow "Teacher Tip" callout
- compare:   two cards (bad vs good) + green badge like "RAM saved 99.9%"
- formula:   KaTeX-rendered math
Every scene starts with its narration and lasts exactly as long as its audio.
"""
import html
import json

SIZES = {"long": (1920, 1080), "short": (1080, 1920)}
TRANSITION = 0.4


def _esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def build_html(script: dict, durations: list[float], audio_files: list[str],
               fmt: str, language: str, series_label: str, rendered: dict[int, dict],
               day_label: str = "") -> str:
    w, h = SIZES[fmt]
    total = sum(durations)
    is_short = fmt == "short"
    font = ("'Noto Sans Devanagari', 'Inter', sans-serif" if language == "hi"
            else "'Inter', 'Helvetica Neue', Arial, sans-serif")
    pad = int(w * 0.06)
    head = 84 if is_short else 66
    body = 46 if is_short else 32
    code = 36 if is_short else 25

    scene_blocks, audio_tags, scene_js, clip_tags = [], [], [], []
    start = 0.0
    n = len(script["scenes"])
    for i, (scene, dur, afile) in enumerate(zip(script["scenes"], durations, audio_files)):
        sid = f"s{i}"
        r = rendered.get(scene["id"], {})
        parts = []

        parts.append(f'<h1 class="heading">{_esc(scene.get("heading"))}</h1>')
        clip_src = scene.get("_clip")
        if clip_src:
            clip_tags.append(f'<video class="vidclip" id="{sid}-clip" src="{clip_src}" muted playsinline '
                             f'data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="2"></video>')
        bullets = scene.get("bullets") or []
        if bullets:
            parts.append('<ul class="bullets">' + "".join(f"<li>{_esc(b)}</li>" for b in bullets) + "</ul>")

        has_code = bool(r.get("code_html"))
        if has_code:
            chars = r.get("code_chars", 0)
            parts.append(
                '<div class="win">'
                '<div class="win-bar"><span class="dot r"></span><span class="dot y"></span>'
                f'<span class="dot g"></span><span class="fname">{_esc(scene.get("code_title") or "")}</span></div>'
                f'<pre class="code" id="{sid}-code" data-chars="{chars}">{r["code_html"]}</pre></div>'
            )

        term = scene.get("terminal")
        has_term = bool(term)
        if has_term:
            out = "".join(f'<div class="t-out">{_esc(x)}</div>' for x in (term.get("lines") or []))
            parts.append(
                f'<div class="term" id="{sid}-term">'
                f'<div class="t-label">Terminal</div>'
                f'<div class="t-cmd">$ {_esc(term.get("command", ""))}</div>{out}</div>'
            )

        formula = r.get("formula_html")
        has_formula = bool(formula)
        if has_formula:
            parts.append(f'<div class="formula" id="{sid}-formula">{formula}</div>')

        cmp_ = scene.get("compare")
        has_cmp = bool(cmp_)
        if has_cmp:
            cards = []
            for side in ("left", "right"):
                c = cmp_.get(side, {})
                ok = bool(c.get("ok"))
                cards.append(
                    f'<div class="card {"good" if ok else "bad"}" id="{sid}-{side}">'
                    f'<div class="card-title">{"&#10004;" if ok else "&#10006;"} {_esc(c.get("title"))}</div>'
                    f'<div class="card-code">{_esc(c.get("code"))}</div></div>'
                )
            parts.append('<div class="cmp">' + "".join(cards) + "</div>")
            if cmp_.get("badge"):
                parts.append(f'<div class="badge-ok" id="{sid}-badge">&#10004; {_esc(cmp_["badge"])}</div>')

        tip = scene.get("tip")
        has_tip = bool(tip)
        if has_tip:
            parts.append(
                f'<div class="tip" id="{sid}-tip"><div class="tip-t">Teacher Tip</div>'
                f'<div class="tip-b">{_esc(tip)}</div></div>'
            )

        scene_blocks.append(
            f'<section class="scene clip" id="{sid}" data-start="{start:.3f}" data-duration="{dur:.3f}" '
            f'data-track-index="0">' + "".join(parts) + "</section>"
        )
        audio_tags.append(
            f'<audio id="a{i}" src="{afile}" data-start="{start:.3f}" data-duration="{dur:.3f}" '
            f'data-track-index="1" data-volume="1"></audio>'
        )
        scene_js.append(_scene_timeline(sid, start, dur, has_code, r.get("code_chars", 0),
                                        has_term, has_formula, has_cmp, has_tip, bool(clip_src)))
        start += dur

    badge = _esc(day_label or series_label)
    return f"""<!doctype html>
<html lang="{language}" data-resolution="{fmt}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={w}, height={h}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800&family=Noto+Sans+Devanagari:wght@500;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.19.0/dist/katex.min.css" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {w}px; height: {h}px; overflow: hidden; background: #ffffff; }}
  #root {{ position: relative; width: {w}px; height: {h}px; font-family: {font}; color: #0a0a0a;
          background-color: #ffffff;
          background-image: linear-gradient(#eef0f3 1px, transparent 1px), linear-gradient(90deg, #eef0f3 1px, transparent 1px);
          background-size: 48px 48px; }}
  .pill {{ position: absolute; top: {int(pad*0.7)}px; left: {pad}px; background: #0a0a0a; color: #fff;
          font-weight: 700; font-size: {26 if not is_short else 30}px; letter-spacing: 0.04em; text-transform: uppercase;
          padding: 12px 26px; border-radius: 999px; }}
  .series {{ position: absolute; top: {int(pad*0.7)}px; right: {pad}px; font-size: 24px; color: #6b7280; }}
  .scene {{ position: absolute; left: {pad}px; right: {pad}px; top: {int(pad*2.2)}px; bottom: {int(pad*1.4)}px;
           display: flex; flex-direction: column; gap: 22px; opacity: 0; }}
  .heading {{ font-size: {head}px; font-weight: 800; line-height: 1.1; letter-spacing: -0.02em; color: #0a0a0a; }}
  .bullets {{ list-style: none; font-size: {body}px; line-height: 1.35; color: #374151; }}
  .bullets li {{ margin: 6px 0; padding-left: 34px; position: relative; }}
  .bullets li::before {{ content: "\\25CF"; position: absolute; left: 0; color: #0a0a0a; font-size: 0.6em; top: 0.25em; }}

  .win {{ background: #ffffff; border-radius: 18px; overflow: hidden; border: 1px solid #e5e7eb;
          box-shadow: 0 18px 50px rgba(15,23,42,0.12); }}
  .win-bar {{ background: #f3f4f6; padding: 16px 22px; display: flex; align-items: center; gap: 10px; }}
  .dot {{ width: 14px; height: 14px; border-radius: 50%; display: inline-block; }}
  .dot.r {{ background: #ff5f57; }} .dot.y {{ background: #febc2e; }} .dot.g {{ background: #28c840; }}
  .fname {{ margin-left: 14px; font-family: 'DejaVu Sans Mono', monospace; font-size: 22px; color: #4b5563; }}
  .code {{ padding: 22px 0; font-family: 'DejaVu Sans Mono', monospace; font-size: {code}px; line-height: 1.55;
           white-space: pre; background: #ffffff; }}
  .code .line {{ padding: 0 28px; min-height: 1.55em; }}
  .code .gutter {{ display: inline-block; width: 34px; color: #9ca3af; user-select: none; }}
  .code .line.add {{ background: #e6ffed; }} .code .line.del {{ background: #ffeef0; }}
  .code .line.add .gutter {{ color: #22863a; }} .code .line.del .gutter {{ color: #cb2431; }}

  .term {{ background: #0f1115; color: #e5e7eb; border-radius: 18px; padding: 22px 28px;
          font-family: 'DejaVu Sans Mono', monospace; font-size: {int(code*0.95)}px; box-shadow: 0 18px 50px rgba(15,23,42,0.18); }}
  .t-label {{ color: #9ca3af; font-size: {int(code*0.8)}px; margin-bottom: 8px; font-family: {font}; }}
  .t-cmd {{ font-weight: 700; color: #ffffff; margin-bottom: 6px; }}
  .t-out {{ color: #86efac; }}

  .vidclip {{ position: absolute; left: 50%; transform: translateX(-50%);
             mix-blend-mode: multiply; opacity: 0;
             {'top: 470px; width: ' + str(w - 2*pad) + 'px; height: auto;' if is_short else 'top: 370px; height: 520px; width: auto;'} }}
  .formula {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 16px 24px;
             text-align: center; font-size: {int(code*1.5)}px; }}

  .cmp {{ display: flex; gap: 24px; }}
  .card {{ flex: 1; background: #fff; border-radius: 18px; padding: 22px 24px; border: 1px solid #e5e7eb;
          box-shadow: 0 12px 34px rgba(15,23,42,0.1); border-left: 8px solid #e5e7eb; }}
  .card.bad {{ border-left-color: #ef4444; }} .card.good {{ border-left-color: #22c55e; }}
  .card-title {{ font-size: {int(body*1.05)}px; font-weight: 700; margin-bottom: 14px; }}
  .card-code {{ background: #f3f4f6; border-radius: 12px; padding: 16px; font-family: 'DejaVu Sans Mono', monospace;
               font-size: {int(code*0.9)}px; white-space: pre-wrap; }}
  .badge-ok {{ align-self: stretch; background: #f3f4f6; border-radius: 16px; padding: 22px 26px;
              font-size: {int(body*1.2)}px; font-weight: 700; color: #111827; }}
  .badge-ok, .tip {{ box-shadow: 0 10px 28px rgba(15,23,42,0.06); }}

  .tip {{ background: #fff6cc; border: 1px solid #f5e08a; border-radius: 18px; padding: 20px 26px; }}
  .tip-t {{ font-weight: 800; font-size: {int(body*0.95)}px; color: #78350f; margin-bottom: 6px; }}
  .tip-b {{ font-size: {int(body*0.85)}px; line-height: 1.4; color: #451a03; }}

  .footer {{ position: absolute; left: 0; right: 0; bottom: {int(pad*0.6)}px; text-align: center; font-size: 24px; color: #6b7280; }}
  .progress {{ position: absolute; left: 0; bottom: 0; height: {int(h*0.008)}px; background: #0a0a0a; width: 0; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}"
     data-width="{w}" data-height="{h}">
  <div class="pill">{badge}</div>
  <div class="series">{_esc(series_label)}</div>
  {''.join(scene_blocks)}
  <div class="footer">Progress &#8226; {_esc(day_label)} &#8226; {n} scenes</div>
  <div class="progress" id="progress"></div>
  {''.join(clip_tags)}
  {''.join(audio_tags)}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  tl.fromTo("#progress", {{ width: "0%" }}, {{ width: "100%", duration: {total:.3f}, ease: "none" }}, 0);
  {chr(10).join(' ' + j for j in scene_js)}
  window.__timelines["main"] = tl;
  tl.seek(0);
</script>
</body>
</html>
"""


def _scene_timeline(sid, start, dur, has_code, code_chars, has_term, has_formula, has_cmp, has_tip, has_clip=False) -> str:
    fade = min(TRANSITION, dur / 4)
    js = [
        f'tl.fromTo("#{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: {fade:.3f}, ease: "power2.inOut" }}, {start:.3f});',
        f'tl.to("#{sid}", {{ opacity: 0, duration: {fade:.3f}, ease: "power2.inOut" }}, {start + dur - fade:.3f});',
        f'tl.fromTo("#{sid} .heading", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }}, {start:.3f});',
        f'tl.fromTo("#{sid} .bullets li", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, stagger: 0.22, ease: "back.out(1.4)" }}, {start + 0.4:.3f});',
    ]
    if has_clip:
        js.append(f'tl.fromTo("#{sid}-clip", {{ opacity: 0 }}, {{ opacity: 1, duration: {fade:.3f} }}, {start:.3f});')
        js.append(f'tl.to("#{sid}-clip", {{ opacity: 0, duration: {fade:.3f} }}, {start + dur - fade:.3f});')
    if has_code and code_chars > 0:
        type_start = start + dur * 0.25
        type_len = max(dur * 0.45, 1.0)
        step = type_len / code_chars
        js.append(
            f'tl.fromTo("#{sid}-code .ch", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01, '
            f'stagger: {{ each: {step:.5f} }} }}, {type_start:.3f});'
        )
    if has_term:
        js.append(f'tl.fromTo("#{sid}-term", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power2.out" }}, {start + dur * 0.7:.3f});')
    if has_formula:
        js.append(f'tl.fromTo("#{sid}-formula", {{ scale: 0.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.3)" }}, {start + dur * 0.5:.3f});')
    if has_cmp:
        js.append(f'tl.fromTo("#{sid} .card", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, stagger: 0.2, ease: "back.out(1.2)" }}, {start + dur * 0.4:.3f});')
        js.append(f'tl.fromTo("#{sid}-badge", {{ scale: 0.95, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4 }}, {start + dur * 0.75:.3f});')
    if has_tip:
        js.append(f'tl.fromTo("#{sid}-tip", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power2.out" }}, {start + dur * 0.6:.3f});')
    return "\n  ".join(js)
