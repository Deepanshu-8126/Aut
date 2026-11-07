# MODE 2B-CODE — PURE-CODE CUTAWAY ENGINE (LOCKED ✅ 2026-10-23)

**Status:** User-approved via test 58 (smoke detector). "Code wala test bhi aswm" — PASSED.
**Channel:** FUNCYOUS (English, USA/worldwide). No CHRONIC branding. No brand names/logos in visuals.

## What it is
100% code-drawn cinematic cutaway diagrams — zero AI video, zero GPU, CPU-only.
Benchmark feel: Branch Education / Zack-diagram hybrid. Vertical 1080×1920 @30fps.

## Pipeline (proven, 52s render for 342 frames)
1. **Scene** = single HTML canvas file, `window.renderAt(t)` + `window.READY=true`.
   - Canvas attr 1080×1920, CSS 540×960, `ctx.setTransform(2,0,0,2,0,0)`, design coords 540×960.
   - Deterministic particles: `R(i)=frac(sin(i*127.1+311.7)*43758.5453)` — stateless, pure f(t).
2. **Render** = playwright chromium headless, viewport 540×960, deviceScaleFactor=2, JPEG q92 frames.
   - Install per reset: `pip install playwright && python3 -m playwright install chromium --with-deps` (~30s).
3. **Post** = PIL pass per frame: word-pop captions + label chips (57/58 style — see below).
4. **Mux** = imageio ffmpeg: `eq=contrast=1.06:saturation=1.1,noise=alls=5:allf=t,unsharp=5:5:0.4`;
   VO atempo + adelay 150ms; synth audio beds via aevalsrc (**escape commas: `mod(t\,0.62)`, wrap expr in quotes**);
   `-crf 26 -ar 44100 -ac 2 +faststart`.

## Cinematic grammar (what made 58 work)
- **Camera = piecewise cut segments** [t0,t1,cx,cy,z0,z1] with smoothstep drift → feels like real cuts+push-ins. 4-6 cuts per 10-12s.
- **Materials:** multi-stop metallic gradients + brushed lines (alpha 0.07) + rivets (radial grad) + cut-edge stroke #79828f.
- **Emissives:** shadowBlur glows + globalCompositeOperation 'lighter' for particles/pellet/current.
- **Light:** volumetric top shaft, radial bg #1b2434→#04060b, vignette 0.55, drifting dust motes.
- **Story in physics:** state changes drive EVERYTHING (current dashes speed/color, meter bars, flicker, strobe, shake).
- **Alarm phase:** red strobe sin-pulse overlay + rim shadowBlur red + piezo expanding arcs + decaying shake (sub-pixel, smooth).
- **Audio from code:** 110Hz hum (tremolo 0.7Hz) @0.045 + alarm 3150Hz beep gate `lt(mod(t,0.62),0.33)` @0.16.

## Caption/chip spec (shared with 57 — Funcyous house style)
- Captions: 3-word chunks, char-weighted over [VOstart+0.30, VOend−0.15]; active word Montserrat-Black 58 amber (255,196,64); others Inter-SemiBold 56 white; y=1700; bottom gradient 1500→1920; measure each word WITH its actual font.
- Chips: JetBrainsMono-Bold 30, x48, y150, step 66, dark pill (10,12,16,190), colored dot, 0.18s fade.
- VO: voice-01 English, atempo 1.15-1.18.

## Reference implementation
`explainer-pipeline/assets/funcy58/` — scene.html + render.py + post.py + vo58.mp3 (reset-proof).
Output: `outputs/58-smoke-detector-codetest.mp4` (11.4s, 1.6MB).

## Lane strategy (Funcyous)
- LTX photoreal (57-style) = beauty shots / hooks.
- CODE cutaway (58-style) = X-ray explanation sections — instant, free, infinitely editable.
- HYBRID (C) = recommended: LTX real shots + code cutaway "X-ray view" — user decision pending.

## Rules inherited
Bespoke visuals per subject (no template copy-paste). Sub-pixel motion only. No brand names.
Common "How X Works" topics BANNED — only hidden/never-made mechanisms (8-topic bank in session notes).

---
# ⭐ FUNCYOUS HYBRID FORMULA — USER-APPROVED & LOCKED (2026-10-23)

**User verdict (video 60):** "beech me jo animation tha wo BEST laga — best tha wo Funcyous ke liye."
Videos 57 (LTX), 59 (LTX+hybrid fix), 60 (hybrid) ALL UPLOADED by user.

## THE FORMULA (per short, ~35-40s + 3.2s CTA):
1. **HOOK (0-10s):** 1-2 ultra-detail AI stills → LTX-2.5 animates (real-world beauty shots)
2. **X-RAY SECTION (12-17s): PURE-CODE cutaway animation** ← THE SIGNATURE. Canvas scene:
   piecewise camera cuts, metallic gradients, particle physics, state-driven story
   (gauge spikes, snaps, clicks), chips synced to mechanism beats
3. **PAYOFF/ENDER:** LTX zoom variants + ender shot
4. **CTA:** FUNCYOUS subscribe segment (assets/funcy58 recipe, 8s rebuild)

## WHY IT WINS:
- Only 2 LTX clips → Kaggle kernel 13 min (vs 30 for 6 clips)
- Code section = free, instant edits, infinitely detailed, NEVER hallucinates
  (59's f5 person-hallucination lesson: LTX for beauty only, code for mechanism)
- Total build ~25 min, ₹0, 5-6MB file

## SHIPPED FUNCYOUS LIBRARY:
- 57 smoke detector (LTX 8-cut) — UPLOADED
- 59 traffic loop (LTX + hybrid cabinet fix) — UPLOADED
- 60 gas pump (FULL HYBRID — formula video) — UPLOADED
- Scene recipes: assets/funcy58 (CTA+codetest), funcy59, funcy60 (scene60.html)

## TOPIC BANK (next up):
1. Shopping cart invisible wheel-lock fence (test-it-yourself viral)
2. Vending machine coin physics exam
3. Escalator handrail 2% speed trick
4. Piezo lighter crystal (800V squeeze)
5. Hotel key card offline rolling code
6. ATM bill counter | 7. Fridge ice maker | 8. Fire hydrant dry barrel

---
# 🔒 RETENTION LAYER — LOCKED (2026-10-23) — MANDATORY IN EVERY FUNCYOUS VIDEO
# Purpose: new-channel freeze fix. One place, same for all: tools/funcy_retention.py

## 1. HOOK CARD (the #1 anti-swipe weapon)
- `from funcy_retention import draw_hook_card` in EVERY assembler composite loop
- Frame 1 → 1.6s: two lines, Montserrat-Black 96/112, line2 AMBER, dark plate behind,
  0.22s pop-in, 0.3s fade-out. Frame 1 IS the feed thumbnail — it must carry the hook alone.
- Hook text = 4-6 words max, shock claim from script ("THE PUMP KNOWS. ZERO SENSORS.")

## 2. CTA POLICY (completion % protection)
- CTA ender OFF (CTA_ENABLED=False) until channel crosses 1,000 subs
- Ending must LOOP: last cut returns to opening shot (seamless rewatch = ranking fuel)

## 3. PACING RULES (already standard, now law)
- Visual change every <=4s (cut/zoom/state-change) - no shot overstays
- VO 1.15-1.18x, captions start 0.30s, word-pop always

## 4. UPLOAD CHECKLIST (same every time)
- Funcyous = ONLY formula videos (niche purity - no Tesla/facts/anything else)
- Post 5-8 PM IST (US morning) | title = curiosity line | 3 hashtags incl #shorts
- Altered content = YES | pin comment with a question | NEVER delete/re-upload
- Judge: video 72h, channel 21 days

## WHY (2026 shorts algorithm):
swipe-away (first 2s) ~50% > completion/rewatch ~30% > volume+consistency ~15% > engagement ~4% > timing/keywords ~1%

### SUBSCRIBE TAP (LOCKED 2026-10-23)
- `draw_subscribe_tap(im, tt, t0)` from funcy_retention.py — MANDATORY in every Funcyous video.
- Realistic YT interaction: slide-in → red SUBSCRIBE → finger-dot tap → SUBSCRIBED ✓ + gold bell shake → slide-out (2.6s).
- Placement: MID-VIDEO at a high-retention beat (~55-65%), y=1452. Max 1 per video.
- Ender stays CTA-free (seamless loop rule unchanged till 1K subs).

---------------------------------------------------------------
🔒 THUMBNAIL-FIRST ART PIPELINE — LOCKED 2026-10-25 (video 63)
---------------------------------------------------------------
USER LAW: "lock that type of thumbnail idea"
ORDER OF WORK (har Funcyous video me, NO EXCEPTIONS):
 1. THUMBNAIL PEHLE banao — bold graphic-novel poster style:
    - dark navy bg + glowing red accents + amber highlights, high contrast rim light
    - cutaway/X-ray split hero object + villain/curiosity element + red X
    - 2-4 WORD max text, condensed impact font, white + amber yellow
    - offer_options=true ALWAYS (user picks) + text ZOOM-VERIFY + no brand logos
 2. SELECTED THUMBNAIL = STYLE REFERENCE for saari image beats:
    - har image-beat (hook/story/payoff) generate_image me
      images=[thumbnail] pass karo + "match the exact bold cinematic
      graphic-novel illustration style, palette and lighting"
    - NO TEXT / NO LOGOS in beat images; top+bottom thirds khali (overlay space)
 3. RESULT: thumbnail click → frame 1 SAME visual family. Zero style-break.
 4. Agar image model 429/fail ho → offer_options=true se dusra model
    rotate hota hai (proven fix, video 63).
REFERENCE BUILD: assets/fun61/ (img_fob2/img_thief2/img_car2 + scene63.html)

---
# 67 TAP-TO-PAY BUILD LOG (2026-10-27) — VOICE VERDICT
- USER ORDER: "Voice old put" → voice-13 experiment REVERSED. **voice-01 = THE Funcyous voice, permanent.**
- VO law chain confirmed: silenceremove trim + internal-gap cap + atempo 1.18 + alimiter 0.89.
- X-ray signature delivered as PURE-CODE canvas (scene: /var/tmp volatile; recipe = solid card → scan sweep reveal → 4-loop copper coil draw-on (insets 24/34/44/54, draw from 0.17D step 0.05D) → live current dashes (22/46 dash, offset -t*230) → trace to chip + pulse rings; camera cuts wide → bottom-right corner (385,625,z1.8) → chip close (196,330,z2.0) → wide).
- Lesson: interior traces alpha 0.22 + 24 traces minimum, warna push-in EMPTY lagta hai.
- Grade chain (eq+noise+unsharp) + crf26 = 12MB/45s. crf22+noise = 58MB TRAP.
