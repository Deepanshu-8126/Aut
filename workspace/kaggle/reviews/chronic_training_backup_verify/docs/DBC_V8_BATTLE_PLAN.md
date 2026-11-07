# ⚔️ DBC v8 "RATHEE-SPEED CUT" — BATTLE PLAN (LOCKED)

## 🎯 TARGET
- **Duration: 12–14 min** English (voice-01). 8+ min = mid-roll ads = revenue. Uska 25 min presenter ke saath hai; hamara dossier-style 12-14 pe tightest rahega.
- **KPI #1 (naya LAW): ≥10 visual changes per minute.** Har sentence = ek visual event. Ye number render ke baad MEASURE hoga (cut-detection script ready hai) — pass nahi to ship nahi.
- **KPI #2: har number-reveal pe SFX hit. Har photo-entry pe slam sound. Total SFX events 150+** (v7 mein 37 the).
- **KPI #3: music curve** — opening −12dB region (gain ~0.32), story ~0.20, reveals swell, 3 silence-drops. Chapter change = music HARD CUT → riser → naya mood (crossfade band).

## 📜 SCRIPT (English, apni likhenge — uska sirf structure/beats, copy zero)
v7 ke 5 chapters + **6 naye story-engines** uske research map se:
1. **Nyrop quote** — "Full compliance with Cooper" (glow-quote treatment)
2. **"D.B." naam ki galti** — reporter James Long deadline story (sabse shareable nugget)
3. **Copycat hijackers** — 5 copycats, McCoy ki double-speed dive survive → "to Cooper bhi zinda ho sakta hai"
4. **Jump survival analysis** — −7°C, night, clouds at 5000ft, hypothermia math
5. **Titanium tie particles** — unalloyed titanium → Boeing/aerospace engineer theory + 2nd sketch
6. **Rackstraw #2 full case** — Colbert ki 40-member team, confession claim, barbaad zindagi, FBI rejection
Ending: hamara OPEN./STILL UNSOLVED (v7 ka, ye uske CTA se strong hai).

## 🛠️ ENGINE UPGRADES (dbclong.html mein naye primitives) — YE HI SKILL-FIX HAI
Root problem: hum "SCENES" banate the (16s canvas + drift). Ab "BEATS" banayenge (1-2s events). tl.json mein har sentence ko beat-type milega:
| Primitive | Kya karta hai | SFX |
|---|---|---|
| `slam` | photo/card scale 1.3→1.0 pop + 2° rot + flash, stack 1…2…3 | thud har slam pe |
| `numpop` | bada number screen pe SLAM (10,000 FT / $194,200 / $5,800) | impact + tick |
| `mapdraw` | dark map pe route line ANIMATE (4 maps: PDX→SEA, SEA circling, SEA→Reno, Tena Bar zoom) | radar ping |
| `halftone` | photo ko dot-treatment + RED highlight bar text pe | paper + bar-swipe |
| `quoteglow` | word-by-word glowing quote + speaker cutout + naam chip | shimmer |
| `redsil` | RED SILHOUETTE Cooper — recurring character har evidence ke saath | bass pulse |
| `silence` | 2-3s full music drop + bass boom (bomb note, 8:13 bump, ending) | sub-drop |
- Opening redo: pehle 30s mein 8-10 hard cuts (map draw → ticket halftone → counter slam → DAN COOPER typewriter → red-sil reveal).
- AI "REPRESENTATIONAL" stills: 6-8 naye hero stills (cabin interior, suitcase bomb inside, jump night, money dig) — Dhruv-validated approach, label ke saath.
- PD clips: wahi 5 + 2-3 naye Prelinger cuts (search parties, river) — ARCHIVE FILM frames.

## 🔊 ASSETS CHAHIYE (naye, free)
- SFX: cash rustle, coin drop, camera flash ×2, sub-drop, radar ping (Mixkit, ~6 files)
- Music: 5 chapter moods rakhenge + 1 high-energy opening track (Mixkit dark-suspense pool se)

## 🏭 PIPELINE (proven, same order)
Script → VO voice-01 (~10 chunks) → tl.json beats → engine patch → **local 10-SECOND TEST** (beat density visual check) → Kaggle render (12-14 min video ≈ 35-40 min kernel) → audio build (curve+150 SFX) → PD clip compose → **cut-detection QC: ≥10 changes/min verify** → SRT → ship.

## ⚠️ STORAGE WARNING
12-14 min @ ~800kbps ≈ **75-85 MB**. Workspace abhi 120M/128M. **v8 banane se pehle v7 master delete karna padega** (44MB free karne). USER: v7 download kar le pehle agar rakhna hai — phir GO bol.

## 📏 HONESTY LAWS (intact)
PD-only footage, REPRESENTATION labels, YT AI checkbox, .srt export, koi Nat Geo/HBO clip copy NAHI.

---

# 🔒🔒 LONG-FORM SYSTEM v8 — FINAL LOCK (2026-10-25)
**Ye section = AGLE HAR LONG VIDEO ka LAW. DBC v8 build me 2 din jo waste hue (5 defect, 3 re-splice, voice/story/QC issues) — unka har sabak yaha baked hai. Isse bahar kuch nahi karna. Next long video = ONE CLEAN PASS.**

## A. PIPELINE ORDER (isi sequence me, kabhi skip nahi)
1. **SCRIPT** pehle 100% final (tagdi story, dynamic ending, zero filler). Structure: COLD OPEN (≤0.5s, living-poster hook) → s1..s7 sections → VERDICT options (A/B/C pick-one) → OPEN./unsolved ending + CTA.
2. **VO generate (voice-01 English)** — FULL script ek baar me. Em-dash `—` TTS ko todta hai → pehle `-` se replace. VO start offset **1.6s** (music lead-in).
3. **SILENCE-DETECT SYNC (v5 LOCKED RECIPE)** — VO par silencedetect chala ke HAR sentence ka real t0/t1 nikalo. Beats VO ke measured time pe bante hai, estimate pe NAHI. **WORD-COMPLETE RULE: beat apna VO sentence khatam hone se pehle cut NAHI hota.**
4. **BEATS build** — real-asset-first: archive VIDEO (plane/search beats me REAL footage mandatory, code-drawn plane REJECTED), AI-image sirf jaha archive impossible (night jump), code = UI/maps/docs/typo. 3 silence-drops. Pacing **~15 events/min VO-measured (30 = too much, 10 = floor)**.
5. **SOUND MAP TABLE** assembly se pehle (SFX LAW). Har number/money beat = SFX hit. Music chapter-mood matched, NO DOUBLE LAYERS.
6. **RENDER** (playwright harness) → **ASSEMBLE** (overlays+audio) → **KPI MEASURE** (≥10 changes/min machine-verified, fail = no ship) → **QC GATES (Section C)** → ship.

## B. ENGINE GEOMETRY LAWS (code me hard-baked rakhna)
- **Caption:** JBM wrap@1420, 1-line y=992 / 2-line y=980, dark plate + red edge. Plate top kabhi y<940 content se na takraye.
- **🔴 OVERLAY-CAPTION LAW:** ffmpeg overlay footage ko caption ke UPAR paste karta hai. Fullscreen slot bottom y=940 → captions hamesha ≥y942 ya clip ko caption band ke NEECHE composite karo. (Is galti ne pura caption-overlap defect diya tha.)
- **🔴 TEXT-INSIDE-FRAME LAW:** har label/chip ka `x + measureText(txt).width ≤ 1880`. Lamba label = 2 lines me todo (McCoy ~500 KM/H label edge se kat gaya tha — judge audit me pakda).
- Fullscreen archive grade + windowed grade (340:150) — exact filters Key Results me locked. Zero clip repetition.
- Ending: living poster == thumbnail (§6.7) + **CTA BAKED: typed line `NEW CASE FILES EVERY WEEK` (typewriter SFX) + red `SUBSCRIBE` stampR (impact SFX) last ~3.2s me, duration extend kiye bina.** Intro logo = KABHI NAHI (retention killer; Dhruv/Lemmino cold-open standard). Upload pe YT end-screen Subscribe element bhi lagana.

## C. QC GATES (ship se pehle SAB pass — isi ne saari galtiya pakdi thi)
1. **Contact sheets:** fps=0.5, 5x6 tiles, pura video aankh se dekho (100-viewer judge mode). Suspect tile → FULL-RES frame grab karke hi verdict do (tiles dhokha dete hai: whip-pan blur, mid-slam animation, beat-flash sab defect jaise dikhte hai par design hote hai).
2. **Duplicate-beat grep** (theory-card dup repeat na ho) + **overlay-applied verify** (har planned overlay window ka frame grab — s0 jet/river kabhi apply hi nahi hue the).
3. **Caption overlap scan** (slot beats ke captions visible?), **label clipping scan** (edge-cut text).
4. **Machine:** packet count == expected frames, decode errors = 0, blackdetect = 0, KPI events/min pass.
5. **Audio:** full-file volumedetect (peak ≤ −0.1dB; AAC re-encode +0.2dB overshoot deta hai → mix me volume=0.966 headroom), start 1.6s lead-in, end fade tail, silence-drops sahi jagah. **freezedetect = false-positive factory** (grain-holds flag karta hai) — sirf visual confirm pe chase karo.
6. SRT: cue count, monotonic, duration ke andar. VO-visual sync spot-checks.

## D. FIX MACHINERY (galti mile to full re-render NAHI — surgical splice)
- **SPLICE (6x proven):** keyframes probe (`-skip_frame nokey`) → partA `-to` TUNE karke VERIFIED packet count (DTS trap!) → beat frames re-render → locked x264 (`-preset fast -crf 26 ref=2:bframes=2:rc-lookahead=20 -threads 2 -video_track_timescale 15360`) → concat demuxer → audio remux `-c copy`.
- **BAND-COMPOSITE:** caption-only fix = band y940 h140 crop → overlay on segment (footage re-source nahi karna padta).
- **RENDER HARNESS TRAPS:** (1) viewport 960x540 dsf=2; (2) fonts: `document.fonts.ready` + warmup seek + settle + RE-SEEK, warna pehle 1-2 frames serif-fallback me nikalte hai — render ke baad first-frames ka luma/visual check MANDATORY; (3) **IMGS wait: `Object.keys(IMGS).length>=5 && every(im.complete)`** — khali object pe `.every()` vacuous-true hota hai; (4) sandbox reset /var/tmp ka SAB kuch udata hai (ffmpeg static, pydeps, chromium) — rebuild: johnvansickle ffmpeg + `pip -t /var/tmp/pydeps playwright` + `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pwb playwright install chromium` + `sudo python3 -m playwright install-deps chromium` (libnspr4). Mixkit SFX re-download IDs SFX_LIBRARY/Key-Results me hai.

## E. VOICE/STORY LOCKS
- English long-form VO = **voice-01**; Hindi kabhi Chronic pe nahi. TTS ko human kabhi nahi bolna; AI disclosure = YT checkbox. `.srt` hamesha export.
- Story = SCENE-ACCORDING §6.8 (story FIRST, beat toolbox baad me). Quote cards draw-in, suspect cards big-stamp slam, doc cards typing — ye house style hai, QC me inke mid-animation frames ko defect mat samajhna.
- Research: script-verified facts hi (DBC fact-table pattern). Koi recent-tragedy/conspiracy angle nahi.

**BOTTOM LINE: Script final → VO measure → beats → SOUND MAP → render → KPI → 6 QC gates → ship. Beech me koi sawal nahi (ONE-SHOT), koi shortcut nahi, koi "baad me theek karenge" nahi.**

---
# 🔴 v8.1 ADDENDUM — USER AUDIT (DBC long, live hone ke baad) — LOCKED 2026-10-25
**User ne khud 3 defect pakde. Ye teeno ab HARD LAW hain — Earhart #2 se lagu. DBC live video ko kabhi re-upload nahi karna (originality law) — ye sirf aage ke liye hai.**

## LAW 1 — EVIDENCE REALISM (the "bomb problem")
VO jis cheez ka naam leta hai (bomb, tie, ticket, briefcase), screen pe wo cheez REAL jaisi dikhni chahiye — crude code-drawing BAND for hero evidence.
- Priority: (a) REAL archival photo (FBI ne tie/money ki photos release ki hui hain — pehle dhundo!)
  (b) photo exist nahi → PHOTOREAL AI still (DARK ATLAS/period grade) banao jo witness description se match kare
  (c) code = sirf us still ke UPAR animation (glow, wires spark, push-in, labels) — lemo-opuscar technique-mine se motion grammar lo
- Checklist line in SOUND MAP table: har evidence beat ke saamne likho REAL/AI-STILL/CODE — "CODE-only hero evidence" = auto-reject

## LAW 2 — MUSIC MIX (the "music bahut high" problem)
- **Duck law:** VO ke dauran music ≤0.14 vol (pehle 0.26 tha — BAHUT HIGH). Swell sirf VO-gaps/silence-drops me.
- **Chapter-mood table MANDATORY:** SOUND MAP me har chapter ke saamne track + mood likho (tension=dark drone, reveal=swell, verdict=heartbeat). Mood mismatch wale chapter me track BADLO — ek track pura video nahi ghaseetna.
- **Ear-QC gate (naya):** ship se pehle 3 random chapters ka 20s audio sun ke judge karo: "VO saaf hai? music mood sahi hai?" — volumedetect numbers kaafi nahi.

## LAW 3 — CUTOUT QUALITY (the "tie cut-out" problem)
Raw PNG-cutout floating on screen = BAND. Har object/evidence visual in me se EK format me aayega:
- EVIDENCE CARD (kraft frame + tape + stamp + shadow — dossier style)
- POLAROID (sepia + handwriting caption)
- FULL-BLEED graded photo (period grade + vignette)
Cutout use karna hi pade to: edge feather 2-3px + drop shadow + period color grade + texture overlay. Hard white/jagged edges = QC fail.

## NOTE — "video low quality" feeling ka asal source:
1080p sahi tha; "cheap" feel in 3 cheezon se aata hai: crude evidence drawings + loud flat music + raw cutouts. Teeno upar fix. + Earhart me: film grain consistent, archive footage REAL (v8 law), evidence REALISM law.

## LAW 2.5 — OPENING SOUND LAW (user: "shuru me strange bekar tune — yahan sound MATTER karta hai")
- **Cold open (0-30s) me MELODIC TUNE BAND.** Mystery ka opening = SOUND-DESIGN, music nahi:
  low drone (mk685-type) + atmosphere (wind/radio-static/engine jo story se ho) + VO. Bas.
- Melody/track pehli baar HOOK SLAM ke baad ya chapter-1 transition pe enter karegi — kabhi frame-1 pe nahi.
- **AUDITION GATE:** assembly se pehle 3 candidate tracks ko cold-open ke against sun ke choose karo (ear-test, meter nahi). "Ye tune is line ke mood se match karti hai?" NO → next track.
- Track kabhi "default" nahi uthana — har video ka opening sound uski story ka hona chahiye (DBC = airport ambience + 727 hum hona chahiye tha; Earhart = ocean wind + radio static + morse beeps).

## LAW 4 — MENTION-LOCK GRAMMAR (LOCKED 2026-10-25, proven in bomb-scene test v4)
Jab bhi VO kisi OBJECT/EVIDENCE ka naam le, TEENO ek hi beat pe fire honge:
1. CAMERA us cheez pe push/reframe karta hai (z 1.25-1.4, subject >= 1/3 frame)
2. ANNOTATION usi beat pe draw hoti hai — red ellipse (confirmed) / dashed box + "≈ inferred" (uncertain)
3. CALLOUT CARD + LEADER LINE card ko object se physically jodti hai + thud-tick SFX
Template: explainer-pipeline/assets/fun61/dbtest/bombtest2.html (BEATS[] array = copy-paste rig).
Base = photoreal still (LAW 1), kabhi crude drawing nahi. Camera pull-back finale + distressed
rubber-stamp (2600 ink-holes + roller streaks + double-strike ghost + settle wobble + 1-frame flash).

## LAW 4.5 — EVIDENCE-SCENE SOUND RECIPE (LOCKED, v4 mix = reference)
Har evidence/reveal scene ka mix (docs/SFX_LIBRARY.md me full recipe):
- BED: story-ambience (jet rumble/ocean wind = anoisesrc brown lowpass130 v0.5) + dark drone mk2745 lowpass2400 v0.42
- REVEAL: deep braam mk1287 v0.5 | MENTIONS: thud-tick mk2636 0.6s v0.34 synced to beat
- STAMP/IMPACT: mk1495 + mk1287 asetrate*0.78 bass g=5 (double-layer sub slam)
- MASTER: highpass28 -> acompressor -18dB 2.2:1 makeup4 -> alimiter -> peak <= -1dB, mean ~ -13/-14dB
- MELODY = ZERO in evidence scenes (Opening Sound Law extends here)

## LAW 4 TEMPLATES (LOCKED 2026-10-25) — jab bhi aisa scene aaye, YEHI use karna
- SCENE-OBJECT variant: assets/fun61/dbtest/bombtest2.html (photoreal scene + flashlight reveal + mention-lock + distressed stamp)
- EVIDENCE-CARD MASTER v3: assets/fun61/dbtest/tietest3.html — FBI-folder intro (flap opens) ->
  card slide-out + dust puff -> light sweep -> MACRO INSERT cuts (flashbulb + RACK FOCUS blur->snap +
  projector flicker + typewriter labels) -> UV FORENSIC moment (365nm beam + twinkling particles +
  Ti COUNT ticker) -> pull-back + rubber stamp. Gate weave + dust motes throughout.
- Sound: LAW 4.5 recipe, ambience = scene ka (jet/room/storm). Ye templates = REFERENCE QUALITY BAR.
