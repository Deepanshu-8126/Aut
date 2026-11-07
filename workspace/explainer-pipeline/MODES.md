# 📋 MASTER MODE LIST — Documentary/Rahasya Pipeline (updated 2026-10-22)
Ek hi jagah, sab modes. Yahi file source of truth hai.

## ⚡ TL;DR — CONFUSED? SIRF YE PADHO
**Video types sirf PAANCH hain. Bas ye poocho: "kya banana hai?"**

| Kya banana hai? | Mode | Spec file | Reference |
|---|---|---|---|
| Lamba documentary (8-15min, 16:9, rahasya/jagah) | **MODE 1C** | STYLE_LONGFORM_LOCKED.md | video 31 |
| Mythology/philosophy reel (45-60s, 9:16, vivid art) | **MODE SHUNYA v2** | MODE_SHUNYA_V2_LOCKED.md | reel 42 |
| Facts short (white bg, PART X/7) | **FACTSHORTS** | factshorts/ | video 21 |
| Machine/engineering "How X Works" (pure 3D code, NO CHRONIC logo) | **MODE 2 (2A stunt / 2B lab)** | docs/MASTER_TEMPLATES_GUIDE.md Niche 2 | videos 12/13/14 (purged, spec zinda) |
| Body/science 3D anatomy (Zack D. style) | **MODE ZACK** | skills/07-blender-3d SKILL §6 (11 Laws) | video 15 (purged, spec zinda) |

**Baaki sab modes NAHI hain:**
- MODE 3D = 1C ke andar ka TOOL (1-3 hero shots) — khud se video type nahi
- Paper-cut engine / DBC kits / engravings / stock beds = MASALE (add-on layers), kisi bhi mode pe lagte hain
- 1B, 1D, 1E, flat-vector = RETIRED — naam bhool jao
- 1A Cinema History = practically retired, 1C ne takeover kar liya

---

## ✅ ACTIVE MODES — video types 3 (1C, SHUNYA v2, FACTSHORTS) + 1 tool (3D)

### MODE 1C — "RAHASYA DOCUMENTARY" (MAIN MODE — LOCKED)
- Hamara mukhya long-form mode. Reference: video 31 Patal Bhuvaneshwar.
- Full spec: STYLE_LONGFORM_LOCKED.md (10-chapter structure, cold-open hook,
  word-sync paper-cut engine, karaoke captions, real Mixkit stock bg + 5-10s cuts).
- REAL photos (green REAL PHOTO tag) jagah ke liye; AI engravings (AI ART tag)
  sirf mythology moments ke liye. Photoreal AI stills = "AI RECREATION" tag.
- ANDAR MERGED (ab alag modes nahi):
  - (ex-1D) PLATE-INSERT layer — buildings/structures dikhane pe 3D plate inserts
  - (ex-1E) TABLETOP 3D — kabhi-kabhi, occasional shot ke liye
- Dynamic SUBSCRIBE ending har video; CTA logo 520px; "case abhi bhi khula hai"
  ending BANNED.
- MODE 3D shots ab is formula ka OFFICIAL hissa hain — "kahin-kahin pe", 1-3 hero
  shots per video (user-approved 2026-10-21).
- SHORTS ADAPTATION approved: yahi formula 9:16 45-60s shorts mein bhi chalega
  ("LONGFORM-SHORT") — FACTSHORTS se alag cheez.

### MODE 3D — "REAL CAMERA" (NEW — LOCKED, standalone)
- Three.js r128 asli 3D camera shots: cave/mandir ke andar dolly, fly-through,
  underwater dive, terrain, water, fire, rain, snow, caustics, stars, 2.5D plates.
- Spec: MODE_3D_LOCKED.md (+ skills/10-3d-scene-spec). Proof: outputs/34 + 35.
- Use: MODE 1C video ke andar special shots ke liye, ya standalone 3D sequences.

### MODE 1A — "CINEMA HISTORY" (practically RETIRED)
- 1C ne long-form takeover kar liya. Sirf tab use karo agar user khaas bole
  "1A wala cinema typography look chahiye". Warna ignore.

### FACTSHORTS — shorts mode (LOCKED "NEVER CHANGE")
- 9:16 1080x1920, white bg + dot grid, black top pill, Inter, PART X/7 bottom bar
  + Morse dots, 7-part formula, 90px safe margin.

## 🔧 ADD-ON LAYERS (modes nahi — kisi bhi mode ke upar lagte hain)
- WORD-SYNC PAPER-CUT engine — APPROVED, har video ka standard (1C core USP)
- DBC STYLE KITS (12 kits, assets/dbc/): COMIC, RISO, CLAY, LINE-ART, 70s POSTER,
  LIQUID, KALEIDO... (demo: outputs/33).
  - ✅ LINE-ART: USER-APPROVED (2026-10-21) — par SIRF jab scene usse related ho:
    naksha/route banna, yatra ka rasta, structure ka layout, "kaise banta hai" diagram,
    purani khoj ka sketch feel. Scene-driven use only — decoration ke liye kabhi nahi.
  - Baaki kits (COMIC, RISO, CLAY, 70s...) ke picks abhi PENDING.
- AI ENGRAVING plates (sepia etching, AI ART tag) — mythology moments
- REAL STOCK footage beds (Mixkit/Pexels) + B-roll cutting har 5-10s

## 📦 RETIRED / MERGED (ab alag use NAHI hote)
- MODE 1B — Poompuhar pure-code (100% code, zero images) — tech 1C mein zinda hai,
  par alag mode ke roop mein retire
- MODE 1D — plate-insert → 1C mein merge (upar dekho)
- MODE 1E — tabletop 3D → 1C mein merge, standalone kabhi nahi
- Flat-vector slide-deck look (video 27) — REJECTED, kabhi wapas nahi

## 🔒 SAB MODES PE LAGU (universal locks)
- voice-06 Hindi (Devanagari script) / voice-01 — voice LOCKED, upgrade visuals not voice
- CTA logo 520px + dynamic subscribe ending
- NO static image holds — full animation bar
- Free-only (zero paid APIs), frame-verify before claiming success, srt export
- Bespoke visuals per subject — template copy-paste BANNED

---

## MODE SHUNYA v2 — LOCKED (2026-10-22, user approved via reel 42)
**FULL SPEC (ek-ek cheez, code+math+banned list): `MODE_SHUNYA_V2_LOCKED.md` — wahi kanoon hai.**
**Category: HISTORY niche ke andar alag sub-category (mythology/philosophy vivid reels, 45-60s)**
Reference master: `outputs/42-sudarshan-reel-50s.mp4` | Renderer: `explainer-pipeline/tools/render_reel50.py`

### Pipeline (is order mein, kabhi mat badlo):
1. **Art:** vivid comic/graphic-novel stills (ek hi style poore reel mein), 768x1376, "AI ART" tag. Naya art generate karna allowed sirf NAYE topic pe — approved reel ke andar kabhi replace nahi, sirf EDIT/refine.
2. **Motion — HYBRID RULE (CHAAR engine; full spec MODE_SHUNYA_V2_LOCKED.md):**
   - **FLAP-WARP (Engine D)** = pankh/kapda CODE se jab LTX na mile (proof: output 43) — traveling wave + asymmetric stroke + body bob.
   - **LTX img2vid** = soft/living cheezein (pankh, kapda, dhuaan, paani). Anon quota ~2min/day; hero shots pe kharch karo.
   - **Code sprite rotation** = rigid/round objects (chakra, wheel). Sprite ko bg se MATH-BIND karo: `u=(fx+(zc-1)/2)/zc` art-fraction nikaal ke har frame pe `(u*w0-left)*S` — zoom ke saath track, ghost impossible.
   - **Differential swirl (flow-map)** = vortex/galaxy/toofan. Rigid rotpatch BANNED non-symmetric content pe. Swirl: falloff `(1-r^2)^2` (kinara zero = seam impossible), 2-layer flow crossfade (endless, bounded warp). Params: storm A=85 T=2.6, galaxy A=60 T=3.8.
3. **Camera — SUB-PIXEL AFFINE ONLY:** integer crop BANNED. `art.transform(AFFINE,(1/S,0,left,0,1/S,top),BILINEAR)` — float zoom (smoothstep eased) + organic drift (±7px sin). Uniformity target: consecutive-diff std/mean < 0.08.
4. **Life layers:** god-rays (alpha-pulsing polygon blur), embers/jugnu particles, glow pulses, diya flicker (smooth sines only), lightning = continuous ramp (threshold max(0,...)), global smoke + gold particles + vignette + grain ±3.
5. **Typography:** Teko word-pop 3-tier (Tiro small white / Teko-Bold big yellow / Teko-Med) char-weighted timing; s8 CTA pe caption y=0.775H (card se neeche, overlap BANNED).
6. **CTA:** papercut card slide (ease-out cubic) + CHRONIC logo + SUBSCRIBE pill pulse + mandala pe orbiting light-glints (mandala rotation BANNED — petals smear hote hain).
7. **Audio:** voice-06 Devanagari whisper VO + music bed (locked recipe: duck 1-0.38*min(env*3,1), flat-gain 0.105/rms, tanh x1.1, norm 0.97) + .srt export.
8. **Grade (mux pe):** `eq=contrast=1.05:saturation=1.14,unsharp=5:5:0.35:3:3:0`, crf 26, 30fps, faststart.

### QC gates (bina pass kiye present nahi):
probe-sheet all scenes → position bugs fix → full render → POST-MUX frame QC (motion/scene ≥ ~7, dead-air zero, user-flagged timestamps full-res check).
