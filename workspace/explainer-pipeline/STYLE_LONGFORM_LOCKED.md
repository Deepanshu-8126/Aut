# 🔒 LONG-FORM FORMAT — LOCKED (User approved, 2026-10-21)
**Reference master:** `outputs/31-patal-bhuvaneshwar-rahasya-long.mp4` (Patal Bhuvaneshwar v2)
**Reference engine code:** `tools/render_patalbhuv_long.py` + `tools/render_wordsync_test.py`
User verdict: "yey cheej bhut best tha" — SAVE THIS FORMAT. Har future long video isi formula pe.
RE-CONFIRMED by user 2026-10-21 (evening): "video 31 formula lock karde... bahut mehnat se
bani hai... sab perfect hai, abhi to best hai." PERMANENT.

## 0. MODE 3D CAMERA LAYER (added 2026-10-21, user-approved)
- MODE 3D (Three.js real-camera shots — spec MODE_3D_LOCKED.md) is now an OFFICIAL
  layer of this formula: "kahin-kahin pe" — 1-3 hero shots per video, NOT every scene.
- Best spots: gufa/structure ke andar camera utarna, underwater dive, terrain fly-over,
  engraving-plate diorama push-in. Ek shot = ek continuous camera, no cuts inside.
- Baaki video 2D engine (papercut + stock + diagrams) hi rahega — 3D sirf masala hai.

## 0b. SHORTS ADAPTATION (user-approved 2026-10-21)
- Yahi formula shorts (9:16 1080x1920) ke liye bhi USE HO SAKTA HAI:
  word-sync papercut + karaoke captions + real photo/AI engraving tags + cold-open hook,
  compressed into 45-60s (hook 5s, 3-4 beats, subscribe end).
- Jab rahasya-style short banana ho to ye "LONGFORM-SHORT" use karo; purana FACTSHORTS
  mode (white bg, PART X/7) apni jagah alag LOCKED hai — dono alag cheez hain.


## 1. STRUCTURE (~4-7 min, 10 chapters)
USER EMPHASIS (2026-10-21): har video ki script TAGDI ho — hook se ending tak koi dheela
beat nahi; ending hamesha DYNAMIC (subscribe anim + energy), kabhi flat fade-only nahi.
Real-footage mixup (Mixkit/Pexels + real human scenes) starting se CTA tak — SET, locked.
1. **COLD-OPEN HOOK (30s)** — seedha action/mystery se shuru, koi intro nahi.
   Big number slam (e.g. "90 FT"), shocking visual prop pop, phir title slam + English sub-line.
2. Concept/context chapter (chhota)
3-4. Granth/history/legend chapters (timeline anims, diagram anims)
5-8. **DEEP DETAIL chapters** — jagah ke ANDAR ki har cheez, har formation + uski katha
9. Science/vigyan chapter (aastha + vigyan dono ko izzat)
10. Visit info + dynamic SUBSCRIBE ending. **NEVER "case abhi bhi khula hai" ending.**
Ending line: "Milte hain… agli yatra mein" type + fade to black.

## 2. WORD-SYNC PAPER-CUT ENGINE (core USP)
- `word_times()`: char-weighted (len+1) proportional timing across measured VO duration, LEAD=0.5
- `kt(chapter, word, occurrence)` → KT dict injected into JS; har prop EXACTLY us word pe girta hai
- `papercut()`: torn-edge chit (seeded tornPath polygon), tape, drop-in + overshoot, wobble,
  shadow, left label (JetBrainsMono) + right source tag
- `kword()`: spoken word ka kinetic pop (60px Deva, stroke outline, 2.2s life)
- Har pop pe `paper()+thud()` SFX

## 3. REAL vs AI VISUALS (critical — user directive)
- **Jo cheez asli jagah pe dikhti hai → web image_search se REAL PHOTO** (crop text overlays),
  green `REAL PHOTO` tag. Real tho real lagta hai.
- **AI engravings sirf mythology moments ke liye** (jo photo ho hi nahi sakti —
  e.g. kata sir, Kalbhairav chehra), sepia antique-etching style, `AI ART` tag.
- Real photo aur AI card saath-saath dono bhi chalega (real left, AI right).

## 4. BACKGROUNDS
- Real Mixkit stock clips (720p → 960x540 crf25 **all-intra `-g 1`** trim), data-URI base64 in page
- Shot cut every ~5-10s, documentary edit; ANIM chapters pure-code cave bg (dust + light blobs)
- Zoom punch-in at each cut (`1+0.06*exp(-since*5)`), slow drift zoom, dim layer per shot
- Film grain noise canvas + vignette + bottom progress bar (orange)

## 5. DIAGRAM ANIMS (per subject, bespoke — never template-copy)
Patal v2 examples: 14-lok stacked bars, 3-yug timeline w/ pulse dots, 4 gates w/ red X "BAND",
depth meter + swinging chains + rib waves, falling droplet + ripple loop, ceiling star sparkles,
4 yug stones (Kalyug red, growing, dashed line to chhat), stalactite/stalagmite growth diagram.

## 6. TEXT SYSTEM
- figbar: top rule + Mono left/right labels | kickerD: Mono small + 72px Deva big
- typew() typewriter Mono lines | stampD() rubber-stamp verdict (ink border rect, slam-in)
- chip() pills for lists | karaoke captions bottom (38px Deva, spoken word ORG highlight, rest white 30%→100%)

## 7. AUDIO
- voice-06, Devanagari VO text, 10 segments, LEAD 0.5 / GAP 1.0
- Generative BGM: drone root + pad, per-chapter intensity envelope, risers before each beat,
  final chord at TOTAL-8; **VO ducking** (box-filter env, -55%)
- SFX: subboom, thud, paper, pop, ping, bell, drip, tickk, whoosh (cut whooshes every shot cut)

## 8. DELIVERY SPECS
1920x1080 @30fps, JPEG frames via headless Chromium (batch 10, resumable), mux crf32 veryfast,
`-movflags +faststart`, srt export, 520px CTA logo + pulsing SUBSCRIBE, frame-verify from FINAL MP4
before claiming success. Palette: bg #07050a, CYAN #4dd8ff, ORG #ff8c3b, GOLD #e8b24a,
PAPER #eef2f8, RED #e8503a, paper #f3eee0. Stamp slam at ~(960,310) if centered.

## B-ROLL RULES v2 (LOCKED 2026-10-21, video 36 se) — USER ORDER
1. **REAL-PLACE FOOTAGE FIRST:** Jis jagah ki baat VO me ho, pehle usi jagah ki REAL video dhundo
   (Pexels place-name search via headless Chrome scrape → Wikimedia Commons → Mixkit generic fallback).
   Source quality: best available (QHD 2560 common on Pexels; "4K" tabhi bolo jab sach ho).
2. **ZERO-REPEAT:** Ek stock clip poore video me SIRF EK BAAR. Render se pehle code-assert:
   Counter(SHOTS keys) me koi dupe nahi.
3. **REAL-FOOTAGE TAG:** Confirmed-location clips par chhota mono tag top-right
   ("SIGIRIYA · REAL DRONE"); unverified location → sirf "REAL FOOTAGE". Kabhi galat jagah ka naam mat likho.
4. **CLIP-LENGTH ASSERT:** shot_dur*0.9 <= clip_eff_dur warna mid-shot loop dikhta hai. Short clips ko chhota shot do.
5. **CTA LOGO = PAPERCUT:** channel logo end-scene me torn-paper chit + tape + label style me (520px lock barkarar).
6. Split-render (HALF=A/B) 20+ clips walे pages ke liye — OOM se bachav; audio hamesha alag step.
7. **CONTINUOUS MUSIC BED (LOCKED 2026-10-21):** Har video me ek REAL music track poore video
   chalti rahe (Mixkit free music, e.g. #188 dark-cinematic; assets me copy rakho).
   Loop 2s-crossfade se TOTAL tak, end me 7s fade-out. Gain ~1.15, VO-sidechain duck ~0.38x
   under speech. Synth drone bed 0.45x par neeche layer. Gap-RMS target 0.03-0.08.
