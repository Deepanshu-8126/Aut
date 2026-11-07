# MODE 1C — "CINE-REAL" (Vox-Style Cinematic Real-Mix) — PLAN v1
> User brief (2026-10-20): "Mode 1B ka mixup + photoreal thumbnail look — kitna real mix-up type"
> Reference: user's AI 'Oumuamua thumbnail (uploads/image-1.png) — photoreal render + bold condensed
> type + yellow highlights + hand-drawn circle/arrow callouts + "?!" stickers.

## 1. CORE IDEA — 3-LAYER VISUAL DNA
Har video 3 layers ka sandwich hai, beat-by-beat mix hota hai:

| Layer | Kya | Kab | Source |
|---|---|---|---|
| **L1 — CINE STILLS** | Photoreal AI hero images (thumbnail-grade), 2.5D parallax + Ken Burns + push-in | HOOK, REVEAL, TWIST, PAYOFF | `generate_image` (free platform tool), 4-6 per video |
| **L2 — PURE-CODE 3D** | Mode 1B WebGL scenes (trajectories, cutaways, data, mechanisms) | EVIDENCE, DATA, MECHANISM beats | three.js (existing engine) |
| **L3 — VOX GRAPHICS** | Kinetic bold type + yellow HIGHLIGHTER bars + hand-drawn circles/arrows (draw-on anim) + mono data tags + paper "?!" stickers | HAR scene ke upar | 2D canvas overlay |

**"Thumbnail-to-video continuity":** Video ka frame #1 = thumbnail hi zinda ho jata hai
(same still, parallax push + same title slam). Viewer click karte hi seamless feel — top 1% creator trick.

## 2. MODE 1C vs 1B — KYA BADLA
| | Mode 1B | Mode 1C |
|---|---|---|
| Visuals | 100% pure-code 3D | Photoreal stills (50%) + 3D (35%) + graphics (15%) |
| Boxes | ZERO boxes | **Yellow highlighter bars ALLOWED** (thumbnail DNA) |
| Type | Inter-Black 52px captions | **Anton/Montserrat-Black SLAM words** + highlight strips + Inter captions |
| Annotations | Gold leader-line callouts | **Hand-drawn jittery circles + arrows** (marker style, draw-on animated) |
| Mood | Deep-space minimal | Cinematic docu-poster, high contrast, film grain heavy |
| Honesty | — | Photoreal AI stills par **"AI RECREATION" mono tag** (MANDATORY) |

## 3. 8-BEAT FORMULA (1C mapping)
1. **HOOK** — L1 living thumbnail: parallax push + title slam (Anton + yellow highlight) + hand-drawn circle on subject
2. **CONTEXT** — L1 second still (different angle/scene) + typewriter mono facts + arrow annotations
3. **EVIDENCE** — L2 3D scene (data/trajectory/discovery) + L3 tags
4. **DATA** — L2 3D + big counter/graph (1B style)
5. **MECHANISM** — L2 3D cutaway/physics scene
6. **TWIST** — L1 dramatic still + hand-drawn circle + "?!" sticker slam + whip-zoom
7. **PAYOFF** — L1 wide cinematic still + circular CASE STILL OPEN seal (1B se)
8. **CTA** — logo **520px** (LOCKED §7.9) + subscribe click

## 4. L1 STILL SPEC (generate_image prompts ka formula)
- "photorealistic cinematic space/history photography, dramatic rim light, volumetric glow,
  shot on 70mm, deep blacks, teal-orange or gold-black grade, 9:16 vertical, no text"
- Har video: 1 HERO (thumbnail-grade) + 3-5 SUPPORT stills (angles/moments)
- Parallax: 2 layers minimum (subject sharp + bg blur-shift) — PIL mask ya simple dual-scale drift
- Grade in-canvas: vignette 0.45 + grain 0.06 + slight teal shadows/warm highlights

## 5. L3 GRAPHICS KIT (canvas, reusable functions)
- `slamWord(text)` — Anton 140-200px, white/yellow, 3-frame scale punch + grain texture fill
- `highlight(word)` — yellow bar (#FFE400) behind word, skewed -2°, wipe-in 0.2s
- `handCircle(x,y,rx,ry)` — jittery 2.5-turn ellipse draw-on (marker red/white/black per bg)
- `handArrow(x1,y1,x2,y2)` — curved jitter arrow + head, draw-on
- `sticker(text)` — "?!" / "WHAT?" paper sticker, drop-shadow, rotate -8°, eob pop
- `monoTag(text)` — JetBrainsMono gold tag (AI RECREATION / dates / coords)
- Captions: 1B wale hi (gold active word + underline) — PROVEN, change nahi
- SFX adds: marker squeak (filtered noise sweep), paper slap, camera shutter, whip-zoom whoosh

## 6. PIPELINE (same skeleton as 1B)
1. `--vo` edge-tts Andrew 8 beats (ya voice-01 Hindi version)
2. `generate_image` x4-6 stills -> /var/tmp/<topic>/stills/ (b64 into HTML)
3. HTML: three.js (L2 scenes) + 2D canvas compositor (L1 parallax + L3 kit)
4. `--preview` 8-beat contact sheet -> user-style frame verify
5. `--render` 30fps screenshots -> CRF 27 + master SFX wav -> outputs/NN + .srt
6. Thumbnail bhi saath generate karo (hero still + title comp PNG) — FREE bonus per video

## 7. FIRST 1C CANDIDATE TOPICS
- "The Bermuda Triangle — 100 Years of Vanishing" (stills: storm sea, old planes, sonar 3D)
- "Area 51 — What's Actually Inside?" (desert gate still + 3D satellite zoom)
- "The Titanic's Last 160 Minutes" (cinematic wreck stills + 3D sinking physics)
- "Göbekli Tepe — Older Than Everything" (golden-hour megalith stills + 3D site map)
- 'Oumuamua 1C REMAKE (user ka thumbnail hi hero hai — direct continuity)

## 8. RULES CARRIED OVER (LOCKED)
- CTA logo 520px (§7.9) • CHRONIC OF HISTORIC emblem top-right • .srt sidecar
- Frame-verify before claiming success • AI stills = "AI RECREATION" tag (honesty)
- Har topic ka fresh world — scene templates copy-paste BAN (standing rule)
