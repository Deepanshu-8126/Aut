# 🔒 NYT-STYLE STORYTIME ENGINE — LOCKED (2026-10-26)
**Status: LOCKED by user order ("aab set hai, is situation ko lock").**
Lane: Hindi animated storytime comedy (NOT YOUR TYPE reference-class).
Channel: TBD by user (Dadi Toons lane-match ya naya) — engine channel-agnostic.
Proof artifacts: `outputs/nyt-jaan-test.mp4` (6s, lip-sync v3) + `outputs/nyt-style-story-test.mp4` (21.8s director cut v2).
Assets: `explainer-pipeline/assets/nyt-test/` (18 frames: scenes + flap/acting pairs).

---

## 1. 🎨 STYLE DNA (visual — NEVER CHANGE)
- **Character:** HUGE round head + tiny body, simple dot eyes, thick clean black outlines.
- **Hero:** messy dark-brown hair, YELLOW t-shirt (recognition anchor — har episode same).
- **Backgrounds:** flat pastel, minimal shapes, NO gradients/texture. Budget expressions me jata hai, background me nahi.
- **COLOR-CODED SCENES:** har location ka apna pastel (ghar=orange-pink, raat=navy, dukaan=teal, anger=red burst). Scene badla = palette badla.
- **Format:** 16:9 landscape 1920x1080 @30fps (NYT-class long). Shorts version banau to 9:16 re-crop, captions y≈1330 law.
- Image gen size 1376x768 → cover-crop w/ OZ=1.05 overscan (rotation ke liye).

## 2. 🎙️ VOICE (locked)
- **voice-18 = Hindi storytime narrator.** Script DEVANAGARI me. atempo **1.15** → ~4 words/sec (NYT pace).
- First-person narration + quoted dialogue ("मम्मी ने बोला — ..."). Zero dead air.
- ⚠️ Voice IDs sessions me mar sakte hain — nayi session me pehle test, fail ho to re-audition karke is doc me update.

## 3. 👄 LIP-SYNC LAW (v3 — VO-DRIVEN, automatic)
1. VO decode @ timeline speed (atempo baked): `ffmpeg -af atempo=1.15 -ar 8000 -ac 1 → wav`
2. Per-video-frame RMS (33ms) → fast-attack envelope (release ×0.55/frame)
3. States: u>0.52 → KHULA(2) | u>0.20 → AADHA(1) | else BAND(0); min 2-frame hold
4. KHULA runs >5 frames → 6Hz syllable dips (frames %5∈{3,4} → AADHA)
5. **Speaker windows:** sirf on-screen bolne wala character flap kare; narration gap me sab BAND
6. Pause windows (>0.4s) = **BLINK slot**
- Per speaking character chahiye sirf 3 mouth frames: BAND / AADHA / KHULA (edit-mode gen: "change ONLY mouth, everything pixel-identical").
- Reference code: jaan-test build (fxj3 block) — envelope → `mouth_states.json` → frame picker.

## 4. 🎭 ACTING GRAMMAR (jaan ka formula)
**ANTICIPATION → ACTION → REACTION. Har dialogue 3 emotions se guzre.**
- Anticipation: shout se pehle brow-raise/saans frame (~0.15-0.2s)
- Reaction shots: sunne wale ka eye-roll / dead-eyes / smug — har beat pe ek
- Blink har 2-4s (pause slots me)
- Talking head-bob: KHULA/AADHA frames pe cy −2px
- Squash-stretch: pose-SNAP pe sy=0.965 (1-2 frames), shout pe sy=1.045
- **LINE BOIL (muft jaan):** global ±1px offset + ±0.14° rot, reseed @6fps (har 5 frames)
- Pose SNAP cuts — morph/tween KABHI nahi, limited-animation snap hi style hai

## 5. 📷 DIRECTOR CAMERA GRAMMAR
- Har move **eased** (easeInOutCubic), linear push BAN
- Handheld float har shot: x=2.2sin(0.6t·2π), y=1.6sin(1.05t·2π)
- Micro-rotation ±0.4-0.5° wide shots pe
- Crash-zoom se pehle **anticipation pullback** (0.12s)
- **Whip-smear** location change pe; white-flash pop chhote cuts pe
- Shot ≤2-3s — 5s se lamba hold BAN (NYT storyboard match)
- Angle menu har scene: WIDE establish → LOW-ANGLE power → INSERT closeup → REACTION extreme-CU
- Zoom-crop targets image-coords me; reaction close-ups DEDICATED image (zoom-pixelation nahi)

## 6. 🔊 SOUND LAW (NYT-analyzed)
- Cartoon foley HAR action pe: pop (cut), whoosh (snap), boing, plinks, dhol-hit (desi punchline), heartbeat (tension, accelerating), DUN-DUN-DUNNN stinger (drama), record scratch (twist), sad violin (ro-dhona)
- **SILENCE-DROP:** twist se ~0.8s pehle music duck 20-25% — signature move
- Bed: mixkit #595 v0.17 (comedy sneak). Synth SFX recipes: jaan/v2 build blocks (sfx2.wav gen)
- Peak ≤ −1dB, alimiter 0.82. NO DOUBLE AUDIO LAYERS.

## 7. 📖 STORY FORMULA (NYT 20M-view structure)
- **Cold-open shock/claim word #1** — intro BAN
- CLAIM → 2-3 escalating gags → punchline (har chapter)
- Long-form (8-9 min): themed chapters → 2-min CENTERPIECE (peak absurd) → **FLIP at ~77%** (roast → pyaar) → specific-number comment CTA → brand end-card
- Short (20-35s): setup → escalation → twist → punchline-freeze (jaan-test pattern)
- Self-deprecating affectionate roast. HATE kabhi nahi. Recurring side-characters banao (mummy, dukaan-wala).
- Har VO word ka **visual echo** — bola to dikhao.

## 8. 🎬 DIRECTOR SIR KE UNIQUE TOUCHES (hamare signature — NYT ke paas bhi nahi)
**RECOMMENDED-LOCKED (top 5):**
1. **🦎 HIDDEN CHHIPKALI:** har episode me kahin ek chhipkali chhipi hai (wall/poster/shelf). Pin comment: "chhipkali dhundo" → comment engine + rewatch engine. (NYT ke 25k-CTA ka hamara jawab.)
2. **🎵 CHARACTER LEITMOTIF SFX:** mummy entry = dhol-hit, hero ka fail = slide-whistle-down, dukaan-wala = ghanti. Awaaz se hi character pehchana jaye.
3. **👁️ 4TH-WALL LOOK:** har episode ME EK BAAR — punchline pe character seedha camera me dekhe (dead stare, 0.8s hold, music drop). Comedy nuclear weapon.
4. **🎥 TRIPLE BOLLYWOOD ZOOM:** bade twist pe ek hi face pe 3 crash-zooms DUN-DUN-DUNNN ke saath (zoom1-dun, zoom2-dun, zoom3-DUNNN). Desi DNA.
5. **📦 OBJECT-POV SHOT:** har episode me 1 shot kisi cheez ki nazar se (doodh packet ki POV se boy ka rota muh). Trademark angle.
**OPTIONAL (jab fit ho):**
6. Background poster-gags — deewar ke posters me chhipe jokes, scene-relevant, rewatch bait
7. Chekhov ki CHAPPAL — scene 1 me dikhi cheez climax me wapas aaye
8. Match-cuts (clock → bulb → chanda same shape)
**REJECTED:** freeze-frame "yep that's me" (cliché, overused globally).

## 9. ⚙️ PIPELINE (order of operations)
1. Script (Devanagari, beats marked) → 2. VO voice-18 → 3. envelope + word-boundary table → 4. shot-list (angle menu + acting beats envelope ke hisaab) → 5. image gen: scene masters pehle, phir EDIT-mode variants (mouth×3, blink, poses) "keep EVERYTHING pixel-identical, change ONLY..." → 6. frame render (boil+float+ease+squash code) → 7. SOUND MAP TABLE → synth SFX wav → 8. mux (VO atempo 1.15 + #595 duck-automation + sfx; alimiter 0.82) → 9. QC: dense frame sweep ≤3s + sync-table verify (pause=BAND, peak=KHULA) + volumedetect.
- Cost yardstick: ~1 scene master + 3-5 variants per dialogue beat; poses heavily REUSE (NYT bhi karta hai). 20s short ≈ 15-20 images; 8-min long ≈ 80-120 + Kaggle render.
- 10-img/turn cap → multi-turn gen plan. THUMBNAIL-FIRST law lagu. NOT-for-kids. AI disclosure YT checkbox.

## 10. ❌ BANNED
Flat-vector static holds | linear zooms | random-cycle flaps (VO-driven ONLY) | morph tweens | hate-roast | intro sections | shot >5s | music over twist-silence | emoji in PIL frames.
