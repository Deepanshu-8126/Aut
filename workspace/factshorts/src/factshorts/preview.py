#!/usr/bin/env python3
"""Build a self-contained preview.html for one rendered run (images embedded as data URIs).

    python tools/make_preview.py --run out/why-you-feel-deja-vu-your-brain-s-glitch-explain
"""
from __future__ import annotations

import base64
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
from . import style as S

CSS = """
  :root { --ink:#0A0A0A; --gray:#555; --yellow:#FFD60A; --blue:#3A86FF; }
  * { box-sizing:border-box }
  body { margin:0; background:#fff; color:var(--ink);
         font:16px/1.5 Inter,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
         background-image:radial-gradient(#DEDEDE 1.2px, transparent 1.2px);
         background-size:24px 24px; }
  header { max-width:1180px; margin:0 auto; padding:44px 24px 12px; }
  .pill { display:inline-block; background:var(--ink); color:#fff; font-weight:700;
          font-size:13px; letter-spacing:.04em; padding:10px 20px; border-radius:999px; }
  .pill b { color:var(--yellow) }
  h1 { font-size:46px; line-height:1.02; letter-spacing:-.02em; margin:20px 0 6px; }
  .lede { color:var(--gray); font-size:19px; margin:0 0 8px; max-width:72ch; }
  .meta { display:flex; gap:10px; flex-wrap:wrap; margin-top:18px; }
  .meta span { background:#fff; border:1px solid #E6E6E6; border-radius:999px;
               padding:7px 14px; font-size:13px; font-weight:600; }
  main { max-width:1180px; margin:0 auto; padding:8px 24px 60px; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
          gap:26px; margin-top:26px; }
  .card { margin:0; background:#fff; border:1px solid #ECECEC; border-radius:18px;
          overflow:hidden; box-shadow:0 8px 26px rgba(0,0,0,.07); }
  .card img { width:100%; display:block; background:#fff; }
  figcaption { padding:14px 16px 18px; }
  .badge { font-size:11px; font-weight:800; letter-spacing:.06em; color:#8A8A8A;
           text-transform:uppercase; }
  .title { font-weight:800; font-size:17px; letter-spacing:-.01em; margin:6px 0 2px; }
  .sub { color:var(--gray); font-size:13px; margin-bottom:10px; }
  .chips { display:flex; flex-wrap:wrap; gap:6px; }
  .chip { background:#F6F6F6; border-radius:999px; padding:4px 10px; font-size:11px; color:#444; }
  .clip { margin-top:9px; font-size:12px; font-weight:700; color:var(--blue); }
  h2 { font-size:24px; letter-spacing:-.01em; margin:52px 0 12px; }
  .rows { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:18px; }
  .panel { background:#fff; border:1px solid #ECECEC; border-radius:16px; padding:18px 20px; }
  .panel h3 { margin:0 0 10px; font-size:15px; letter-spacing:.02em; text-transform:uppercase;
              color:#8A8A8A; }
  .sw { display:flex; align-items:center; gap:9px; font-size:13px; margin:6px 0; }
  .sw i { width:16px; height:16px; border-radius:5px; display:inline-block;
          box-shadow:inset 0 0 0 1px rgba(0,0,0,.08); }
  table { width:100%; border-collapse:collapse; font-size:13.5px; }
  td { padding:6px 0; border-bottom:1px dashed #EDEDED; vertical-align:top; }
  td:first-child { color:#8A8A8A; white-space:nowrap; padding-right:14px; font-weight:600; }
  code, pre { font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
  pre { background:var(--ink); color:#F3F3F3; padding:16px 18px; border-radius:14px;
        overflow:auto; font-size:12.5px; line-height:1.7; }
  pre b { color:var(--yellow); font-weight:700; }
  ul { margin:8px 0 0 18px; padding:0; font-size:13.5px; color:#444; }
  li { margin:4px 0; }
"""

TIMELINE_ROWS = """
        <tr><td>0.00&ndash;0.35s</td><td>pill pops 0.8&rarr;1.0, title slide-up 40px + fade</td></tr>
        <tr><td>0.42&ndash;1.20s</td><td>hero elastic pop + glow breathe, blue trail draws</td></tr>
        <tr><td>1.20&ndash;2.00s</td><td>yellow boxes pop, typewriter 25 ms/char</td></tr>
        <tr><td>2.00&ndash;2.80s</td><td>metrics count up, underline draws left&rarr;right</td></tr>
        <tr><td>0.50s+</td><td>black PART bar slides up, progress dots fill</td></tr>
        <tr><td>audio</td><td>whoosh &middot; pop &middot; glitch &middot; ticks &middot; 110Hz pad &middot; CTA ding</td></tr>
"""

RUN_SNIPPET = """python run.py doctor
python run.py demo --full
python run.py video --topic "Why We Forget Dreams" \\
        --episode 44 --category "BRAIN FACTS"
"""


def data_uri(p: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def card_html(i: int, p: dict, img: Path, clip: Path | None) -> str:
    chips = "".join(
        f'<span class="chip">{html.escape(k)}: {html.escape(str(v))}</span>'
        for k, v in [("Art", p.get("art", "-")), ("Layout", p.get("layout", "-")),
                     ("Bar", p.get("bottom") or "-"), ("SRC", p.get("_src", "-"))])
    clip_line = f'<div class="clip">&#127916; {html.escape(clip.name)}</div>' if clip else ""
    return f"""
      <figure class="card">
        <img src="{data_uri(img)}" alt="PART {i}">
        <figcaption>
          <div class="badge">PART {i}/7 &nbsp;&middot;&nbsp; {html.escape(p['badge'])}</div>
          <div class="title">{html.escape(p['title'])}</div>
          <div class="sub">{html.escape(p.get('subtitle', ''))}</div>
          <div class="chips">{chips}</div>
          {clip_line}
        </figcaption>
      </figure>"""


def build(run: Path) -> Path:
    script = json.loads((run / "script.json").read_text())
    parts = script["parts"]
    stills = sorted(p for p in run.glob("part-*.png"))
    clips = sorted(run.glob("part-*.mp4"))
    full = run / "FULL-short.mp4"
    hexc = lambda n: "#%02X%02X%02X" % S.C[n]                       # noqa: E731

    cards = []
    for i, (p, img) in enumerate(zip(parts, stills), 1):
        clip = next((c for c in clips if c.name.startswith(f"part-{i}-")), None)
        cards.append(card_html(i, p, img, clip))

    tokens = "".join(
        f'<div class="sw"><i style="background:{hexc(k)}"></i>{k} <code>{hexc(k)}</code></div>'
        for k in ("yellow", "blue", "red", "green", "ink", "gray"))

    meta = "".join(f"<span>{m}</span>" for m in [
        f"{len(stills)} stills", f"{len(clips)} animated parts",
        "FULL-short.mp4 &#9989;" if full.exists() else "no full cut",
        f"EP {script.get('episode', '?')}", "Inter Black / Bold",
        "dot grid 24px", "SFX bed synthesised"])

    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FACTSHORTS &mdash; {html.escape(script['topic'])}</title>
<style>{CSS}</style></head>
<body>
<header>
  <div class="pill">FACTSHORTS &bull; EP {script.get('episode','?')} &bull;
    {html.escape(script.get('category',''))} &bull; <b>LIVE</b></div>
  <h1>{html.escape(script['topic'])}</h1>
  <p class="lede">Locked &ldquo;White Minimal Box&rdquo; style &mdash; 7 parts, 1080&times;1920,
  rendered by the Python pipeline. Every frame below is generated output, not a mockup.</p>
  <div class="meta">{meta}</div>
</header>
<main>
  <div class="grid">{''.join(cards)}
  </div>
  <h2>Style lock (drives the renderer and the agent prompt)</h2>
  <div class="rows">
    <div class="panel"><h3>Palette</h3>{tokens}</div>
    <div class="panel"><h3>Timeline</h3><table>{TIMELINE_ROWS}</table></div>
    <div class="panel"><h3>Run it</h3>
      <pre>{html.escape(RUN_SNIPPET)}</pre>
      <ul>
        <li>Prompts for Antigravity / Veo live in <code>prompts/</code> of this run &mdash;
            same tokens, so both outputs match.</li>
        <li>Re-render after editing <code>script.json</code>:
            <code>python run.py stills --script {run.name}/script.json</code></li>
        <li>Art default is the offline vector engine; add a token for AI art.</li>
      </ul>
    </div>
  </div>
</main></body></html>"""
    out = run / "preview.html"
    out.write_text(doc)
    return out



