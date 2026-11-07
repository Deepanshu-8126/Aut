# 🧪 MASTER TEST PIPELINE — ONE SYSTEM, ALL CHANNELS (LOCKED Oct 28)
> Consolidates EVERY test from: VIRAL_CHECKLIST_MASTER, VIRAL_GRADER_RESEARCH, SOUND_PLAYBOOK,
> CHRONIC_DOSSIER_MODE_LOCKED, MODE_2B_CODE_LOCKED, NYT_STORYTIME_ENGINE_LOCKED, HUMAN_EDIT_LAYER,
> GROWTH_TRICKS_PLAYBOOK, THUMBNAIL 5-STYLE DNA, GRADER_LOG lessons.
> RULE: no video uploads unless ALL 10 gates pass. User sees only the 5-line kit + scores.
> c05 (Oct 28) = first video that ran the full chain end-to-end. This doc IS the law now.

## THE 10 GATES (run in this exact order)

### GATE 0 — TREND GATE (before ANY build)
- Live US autocomplete: `suggestqueries-clients6.youtube.com/complete/search?client=youtube&ds=yt&gl=US&hl=en&q=`
- PASS = ≥3 live phrase variants for topic + channel-DNA fit + unique angle. FAIL = don't build.

### GATE 1 — SCRIPT TEST (before render)
- [ ] Linear "ear test": narration alone must tell complete story (read SRT with eyes closed)
- [ ] 7-beat max for ≤20s; 13-beat skeleton for Funcyous
- [ ] Hook line = question/promise in first 1s; payoff beat identified by timestamp
- [ ] Ends on NEW question (retention), loops into opening line
- [ ] Honesty law: legend-as-story, never hoax-as-fact; curiosity gap ≠ false promise
- [ ] Word-sync: every on-screen text matches narration beat it appears on

### GATE 2 — SOUND MAP (before build, SFX LAW)
- [ ] Cue sheet written BEFORE build (library-first: SFX_LIBRARY/MUSIC_LIBRARY)
- [ ] No double audio layers; KM beds = CC-BY credit in desc
- [ ] VOICE LAW chain: silenceremove → atempo (Funcyous 1.18 / Chronic 1.15) → alimiter .89 → gap-cap

### GATE 3 — RENDER QC (canvas engine law)
- [ ] fonts: explicit `document.fonts.load()` per family + `fonts.check()` gate + warmup draw
  (fonts.ready ALONE IS NOT A GATE — frame-0 serif bug, c05)
- [ ] 1080x1920 out; verify via frames not logs; ?v=N cache-bump on every HTML edit
- [ ] assert-replace patches only; grep anchor uniqueness before splice

### GATE 4 — EYE-QC (from FINAL ENCODE, not render frames)
- [ ] 2fps contact sheets across FULL duration
- [ ] FULL-RES crop on every text element (downscale garbles text — c05 LAKF WATFR bug)
- [ ] Check: overlaps, frame-edge clipping, seams in source stills, fallback fonts, grade consistency
- [ ] Loop check: frame-0 vs last-frame side-by-side

### GATE 5 — MACHINE PREFLIGHT (tools/preflight.py)
- [ ] SHIP verdict required. Ceiling = 96 on real footage — don't iterate past it
- [ ] Audio: max vol ≤ -1.5dB (no clip), mean -14 to -17dB

### GATE 6 — VIRAL EVIDENCE (tools/viral_agent.py)
- [ ] hook_motion_0_1s ≥ 20 | cut_rate ≥ 5/10s | static_holds = 0
- [ ] 🆕 SWIPE_GATE (first-2s law, Oct 28): viral_agent SWIPE_GATE must = PASS
      (peak ≥20 in 0-1s AND no half-sec below 6 in 0-2s). 50-60% of all drop-off
      happens in first 3s; <2s hooks = +30% AVD; algorithm's FIRST filter = 2s swipe rate.
- [ ] EYE CHECK first 2s: frame-1 shows STAKES (character/threat/conflict visible, never empty setup);
      text hook ≤0.3s (muted autoplay = text is the only hook); sound hit ON frame 1;
      by 2.0s viewer must have a QUESTION ("phir kya hua?"). Static/slow warm-up opening = auto-FAIL.
- [ ] dead_air ≤ 5% | loop_seam_diff ≤ 15

### GATE 7 — THUMBNAIL TEST (90+ required) — scoring rubric /100:
- Feed legibility @124px sim (25): ONE big word readable, no micro-text
- Single story flow (20): eye path = subject → device
- Contrast/pop (15): luma stddev ≥ 45; pop-color device present
- Curiosity device (15): red circle / ??? / hidden subject
- THUMB-TITLE JODI (15): ZERO word overlap with title (different layers law)
- Clutter (10): ≤1 word + 1 symbol ideal
- Method: PIL metrics + 124px feed-sim eye check. Fix fails via image-edit, retest.

### GATE 8 — METADATA TEST
- [ ] Title: keyword in first 3 words, 40-70ch, curiosity gap, 1 emoji (Chronic)
- [ ] Desc: keyword in line 1, honest caveat, PD/credit line, exactly 3 hashtags incl #shorts
- [ ] Tags: live-autocomplete-tested only, ≤500ch, tier order: exact-niche → question → broad
- [ ] Pinned comment ready; category + NOT-for-kids + AI-disclosure checklist

### GATE 9 — POST-UPLOAD PROTOCOL
- [ ] Pinned comment within 10 min; replies 2h window
- [ ] Judge @72h: views/AVD%/likes/subs → verdict + lesson → GRADER_LOG
- [ ] Judge @21d second look. NEVER delete/re-upload judged content.
- [ ] TEST clips / rejected builds NEVER uploaded (Oct 28 lesson — tests leaked to channels)

## PER-CHANNEL OVERRIDES
| Gate | Chronic | Funcyous | Dadi Toons | ROop_Loop |
|---|---|---|---|---|
| Length | 15-20s Dossier | ≤4s/beat, 13-beat | NYT storytime | hero battles |
| Upload slot | 7-9PM IST | 5-8PM IST | eve | eve |
| Voice | voice-30 @1.15 | EN @1.18 | 22/18 Devanagari | — |
| Captions | baked chips | amber + JBM chips | NO burn, .srt only | — |
| Music | Mixkit dark, intro-loop | #595/#464 only | KM storytime | — |
| Extra | REAL footage + PD labels | code X-ray, tap @55-65%, crf26 | locked lip-sync | hero NAME in title |
| Category | Education | Education | Film & Animation | Film & Animation |

## STANDING LESSONS (auto-apply)
- Machine 96 ≠ user pass (fog reject). User eye = final gate before upload, always.
- Old "ready" builds re-judged against CURRENT bar before upload.
- /var/tmp volatile: re-install chromium + ffstatic after any reset.
- Every new skill = 10-SECOND TEST first. HUMAN-FEEL: ≥2 new visual devices/video.

---
# 🎙️ GATE 2 EXPANSION — VOICE EMOTION MAP + VIRAL SFX MAP (researched Oct 28, 2026)

## A) VOICE EMOTION MAP — per channel (delivery direction for every VO generation)
| Channel | Emotion/Style | Delivery rules | Why |
|---|---|---|---|
| **Chronic** (mystery) | Curious + suspenseful, LOW controlled intensity | Deliberate pace; micro-pause 200-350ms BEFORE each reveal; slight intensity on sentence ENDINGS; first line = "middle of a story" feel, never an intro | Suspense voice gives viewer "reason to wait"; flat delivery = 10-25% early-retention loss |
| **Funcyous** (mechanisms) | Fast, punchy, confident — "bold claim" energy | Compact energy, NO shouting; sharp emphasis on 1 keyword/sentence; zero breathing gap in hook; rising energy through beats | Fast+focused style = match for quick-cut edits; Shorts punish slow intros |
| **Dadi Toons** (Hindi storytime) | Warm storyteller + deadpan contrast on comedy beats | Emotionally controlled, paced; comedy = dry/deadpan against funny visual (contrast > acting); native Hindi = +31% engagement vs EN | Storytime = warm keeps viewer INSIDE narrative; deadpan drives rewatch |
| **ROop_Loop** (battles) | High-energy hype, rising per sentence | Bold-claim delivery; hard emphasis on hero NAMES; sentence endings punch UP | Entertainment pacing = fastest of all four |

## B) VOICE NUMBERS (locked targets)
- TTS rate: 150-170 wpm clear; our atempo chain (1.15/1.18) stays — verify consonant clarity per video
- Word budget: 40-80 words for 15-25s; 120-150 for 60s. ONE fact per beat.
- Emphasize exactly 1 word per sentence (not more)
- VOICE→VISUAL SYNC RULE: voice introduces → visual proves → caption reinforces → cut resets → next beat
- DUAL-VOICE transition tactic ([M]+[F], already Wow law) = valid retention device, use for beat-shifts
- Narration-led > caption-only: 1.9x shares/saves — every video keeps VO, never caption-only
- Judge voice by: 3s retention, rewatch rate, drop-off points (not by "sounds nice")

## C) VIRAL SFX MAP — placement grammar (all channels)
| Moment | SFX | Length | Level vs voice |
|---|---|---|---|
| Hook visual (≤1s) | impact/bass hit (Chronic: low thump; Funcyous: clean hit) | 100-250ms | -8 to -12dB |
| EVERY cut | whoosh/swoosh | 0.3-0.8s | **-20 to -24dB (subliminal)** |
| Text/chip reveal | pop/tick/click | 40-100ms | subliminal |
| Pre-reveal build | riser/tension | 1-2s, peak AT reveal frame | **MAX 1-2 risers per video** (else trailer-feel) |
| Payoff/reveal | bass hit or dun-dun-dun (Chronic) | 100-300ms | -8dB |
| Zoom punch-in | short impact + click layer | 100-250ms | -12dB |
| Scene change | whoosh INTO low impact | 300-600ms | -15dB |
| Comedy beat (Dadi) | vine boom / boing / record-scratch hard-stop | 200-500ms | -10dB |
| Ending/CTA | short riser → final hit (canonical close) | 1s | -10dB |

## D) SFX LAWS (additions to SOUND MAP gate)
- Music bed ≥ 20dB UNDER voice, always
- SILENCE = weapon: drop music + tiny tension tick right before reveal → ear leans in (pairs with our heartbeat cue)
- LOOP LAW: cut on BEAT not sentence-end; ending riser must resolve into opening frame's sound
- Density caps: bass hits 1-2/video; ~1 SFX per 2-3s on VO videos; NEVER SFX on top of hook's key word
- Shorts decide fast: hook hit ≤1s, payoff sound lands BEFORE 7s
- Whoosh direction: rises INTO cut = arrival; decays PAST cut = same-idea continuation
- Existing SFX LAW stack (library-first, no double layers, mk-IDs, synth recipes) UNCHANGED — this maps WHERE, that maps WHAT

---
# 🔬 SELF-AUDIT Oct 28 (system validation on own videos)
## C05 vs new standards: 177wpm (target ≤170, borderline — 1.15x chain); ZERO micro-pauses (gap-cap crushed them — VOICE LAW AMENDMENT below); silence-before-reveal PASS by instinct (RMS dip -24dB @10.7-11.2 → payoff spike -12.5 @11.7 = textbook); dead air 0 ✓; loop tail fade ✓.
## FOG autopsy (user "bekar" = machine-confirmed): 182wpm 9 lines CRAMPED (no breathing); 2 DEAD-AIR HOLES (-40dB @10.2s, -55dB @16.1s mid/end = retention killers); no silence→spike reveal architecture (peak @5.9s then flat drift). User eye saw what old preflight missed — new Gates 2+6 would have REJECTED fog pre-upload.
## ⚖️ VOICE LAW AMENDMENT: silenceremove/gap-cap must PROTECT (not crush) 200-350ms pauses before reveal lines — mark reveal lines in script FIRST, exempt their preceding gaps. WPM target ≤170 post-atempo; if over, cut words not clarity.
## 📈 RMS-CURVE TEST added to Gate 6: audio curve must show ≥1 dip→spike (reveal architecture); NO window below -35dB mid-video (dead-air hole).


## 🧱 STANDING LESSONS — Oct 29 additions (humans + c06 builds)
1. **JS FALSY-FADE TRAP:** `(window.X||1)` fails jab X=0 (0||1=1) — fade/multiplier globals ke liye HAMESHA `(X===undefined)?1:X`. (c06 tail text fade silently dead tha, seam 13.3.)
2. **STOCK-CLIP ANACHRONISM QC:** har extracted segment frame EYEBALL karo render se PEHLE — "ancient" context mein telescope/tent/camping chair aa gaye the (humans f7 slot, 3 attempts). Clip ka ek frame theek hona kaafi nahi — slot ke START/MID/END frames dekho.
3. **CANVAS CSS SIZE TRAP:** canvas attr 1080×1920 + viewport 540×960 = CSS pe canvas ko `width:540px;height:960px` dena MANDATORY, warna screenshots sirf LEFT HALF capture karte hain (c06 first probe).
4. **STILL-HOOK SWIPE RECIPE:** agar hook shot still hai → SWIPE FAIL pakka. Fix jo PASS hua: 0.55s pe HARD PUNCH-CUT (wide→tight 2.05x) + shake (frame-0 clean, ramp-in 0.1s) + fog/particle screen-blend overlay + flash. Peak needed ≥20 first 1s.
5. **SEAM = TEXT SYMMETRY:** loop tail ka text/stamps VO khatam hote hi fade (TXF global), kyunki frame-0 pe text nahi hota. Tail-end zoom/pan values frame-0 se EXACT match karo (eo() curve 1.0 nahi hota — 0.19 vs 0.20 delta tak matter karta hai).
6. **VO LENGTH GATE (pre-build):** script likhte waqt word-count × channel wpm se duration estimate karo — c06 pehla VO 43.4s nikla (lock 25-35s), script cut + regen ka cycle laga. ~88 words ≈ 35s @ voice-30 chain.
