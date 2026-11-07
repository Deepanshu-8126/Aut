# 🔒 CHRONIC DOSSIER MODE — LOCKED (2026-10-24)
**User order: "is mode ko lock kar de — aisi stories ke liye yehi style + yehi thumbnail style."**
Applies to: CHRONIC channel, unsolved-mystery / cold-case / disappearance stories.
Reference master: `outputs/c02-dbcooper-chronic.mp4` (D.B. Cooper #02 v4) — THE template.
Engine: `explainer-pipeline/assets/dbc02/dbc02.html` + `tools/assemble_dbc02.py` — clone & re-skin per story. 100% CODE, NO LTX.

---

## 1. CORE LAW — IMAGES IN VIDEOS (non-negotiable)
**Priority order (user locked 2026-10-24):**
1. **REAL archival first** — jahan real photos exist (modern cases: planes, FBI evidence, documents, sketches) → fetch & use real
2. **DARK ATLAS generated cinematics** — jahan real photo EXIST hi nahi karti (ancient ruins, lost cities, ghost ships, pre-camera era, atmosphere/mood shots) → generate in locked DARK ATLAS style (dark charcoal-teal, fog, antique map tones, gold candle-light, film grain, 8k) and treat them like archival cards in the collage (polaroid/kraft frames, sepia grade, stamps on top)
3. Dono cases mein altered-content = YES on upload.
Har story mein minimum 3-5 aisi hero images (real ya DARK ATLAS):
- **Map scene** → real vintage chart/map of the actual region (aeronautical/USGS/period map)
- **Evidence scene** → real evidence photos (FBI/police/archive, Wikimedia PD)
- **Subject scene** → real sketch/photo of the person/object (wanted poster, composite, bulletin)
- **Vehicle/object** → real photo cutout, sky/bg keyed out (flood-fill hole fix), night/period graded in PIL
- Prep recipe: hi-res original → PIL crop/enhance (Color 0.85-0.92, Contrast 1.05-1.08) → kraft/sepia blend 15% for map cards; brightness 0.55 + blue blend 38% for night cutouts
- HTML: load via `new Image()` relative paths, **gate `window.READY` on ALL image loads**

## 2. VISUAL FORMULA (defencesquad doc-collage)
Scene chain (~60s): HOOK year-card → MAP card → BLUEPRINT → EVIDENCE/MONEY → ACTION night scene → POLAROID reveal → A/B/C verdict → LOOP end.
- Kraft paper BG + film-strip edges + continuous slow camera motion (push-in 1.03+L*0.024 + sin drift 0.006)
- Map card: real chart + aged tape corners + evidence pins (cream ring + red core + shine dot) + dashed red route WITH shadow + tiny plane/marker — **pins/route INSIDE zoom transform (pin-drift bug fix)**
- Blueprint: cyanotype #0d2545 + grid, CAD-grade line drawing (real proportions, real registration/serial numbers, dimension lines), draw-on segments
- Polaroid: real photo cover-fit + sepia cast + IM Fell handwriting caption
- Sketch card: real composite on #f0ead8 card, rotated ~0.05, JBM caption, paperclip, shadow
- GENUINE STAMPS (locked fn in dbc02.html): offscreen canvas + double-strike ghost + 520 erosion speckles (destination-out) + dry-ink streaks. Red #8a1f14/#b3261a/#e05246
- Fonts: Inter-Black (headlines/stamps/captions) + JetBrains Mono (data/chips) + IM Fell (handwriting). NO other fonts.
- A/B/C scene: headline + subject sketch card + 3 option chips + hot-cycle + COMMENT A,B OR C bar

## 3. SOUND FORMULA — LIBRARY-FIRST (upgraded 2026-10-24)
**NEW LAW: SFX = real library files from `assets/sfx/` (20 Mixkit pro sounds). Synth = fallback only.**
**Har video se pehle SOUND MAP TABLE banta hai (kab kya bajega) — full law: `docs/SFX_LIBRARY.md`**
- Music: Mixkit dark pool (538/565/605/658/678/871) — **LOOP THE INTRO**: pick consistent 20-25s opening block, 3× acrossfade d=2 tri → no mid-track mood shift. Vol 0.26, fade in 0.8 / out 1.5
- Braam on hook slam (stacked detuned 52/78/104/156 Hz, exp decay)
- 1.1s noise riser INTO every stamp; thud ON stamp
- Heartbeat lub-dub under A/B/C verdict section
- Whooshes on scene cuts (-0.15s)
- VO voice-01, atempo 1.15, adelay 250; SFX 0.9; target mean ≈ −19 dB, peak ≤ −0.5 dB

## 4. CAPTION LAW
Sentence-anchored timing via silencedetect (NEVER linear char-weighted). T = nat/1.15 + 0.25. 3-word karaoke chunks, active word gold.

## 5. QC LAW (before delivery)
Frame-strips from FINAL mp4 (not just raw frames): hook / each real-image scene / stamps / captions. Check: pin-drift, chip collisions, text overflow, caption sync. volumedetect. Typography audit pass.

## 6. 🖼️ THUMBNAIL STYLE — LOCKED
**"WANTED-POSTER SKETCH" formula** (reference: outputs/c02-thumbnail.jpg):
- Vertical 9:16, extreme close-up
- Subject as 1970s FBI pencil-sketch / crosshatch ink on aged cream paper (wanted-poster look)
- ONE mystery element reflected/embedded (sunglasses reflection, missing detail)
- BIG torn/painted red element (question mark / X / stamp) over part of face
- 2-3 word distressed stamp text question: "WHO WAS HE?" / "WHERE IS SHE?" / "WHAT HAPPENED?"
- Paper texture + coffee stains + file markings. Minimal, ONE focal point, high contrast
- Generate via offer_options, user picks

## 6.5 🎨 CHRONIC IMAGE STYLE — LOCKED (user: "crazy vibe, isi type ki")
Har Chronic branding/channel image (logo, banner, posters, community posts, end-cards) = **"DARK ATLAS" style**:
dark charcoal-teal cinematic montage + antique world map with dotted RED routes + fog/storm + era-mix subjects (ruins, old ship, vintage plane, signal tower) + big distressed CREAM serif title with COMPASS worked into lettering + gold candle-light highlights + film grain + 8k detail + center-weighted composition.
Reference masters: `outputs/chronic-logo-800.png` + `outputs/chronic-banner-2560x1440.png`. Generate via offer_options, user picks.

## 6.7 🎬 LIVING POSTER SCENE — LOCKED (2026-10-24, user: "lock karo aage video generation mein aisa hi")
Every Chronic video's HOOK (and optionally closer) = the thumbnail coming alive, element by element. Last frame of the scene == the thumbnail, near pixel-perfect (thumbnail→video continuity = retention hack).

**Recipe (proven on DBC#02, `assets/thumbtest/test4.html` = reference engine):**
1. Generate thumbnail (WANTED-POSTER SKETCH formula, §6) at full quality.
2. **CLEAN PLATE:** generate_image edit of the thumbnail → remove QM/text/stamps, keep art+paper identical → `plate.jpg`.
3. **EXTRACT real elements** from the original via color/diff mask (e.g. red QM: R-G>45 & R-B>45 & R>110, MaxFilter(3)+blur+threshold, putalpha → transparent PNG). NEVER redraw complex textures in code — flat code shapes look fake (user rejected); always extract the real pixels and reveal them.
4. **Code elements** (test4.html pattern, canvas 1080×1920 + `canvas{width:540px;height:960px}` CSS):
   - full-bleed plate + Ken Burns (z=1.03+t·0.012) + micro-drift
   - title SLAM ~0.35s (grunge double-strike, scale 1.8→1.0, ≤134px for full-width)
   - header/box fade ~0.7s; agency block typewriter ~0.95s (0.03s/char)
   - extracted hero element (QM etc.) brush-path paint-on 1.8–3.2s (circles r≈175 along hook→stem→dot path, destination-in mask; full draw at p≥0.97; soft drop shadow)
   - subject/footer line typewriter ~3.5s
   - always-on: flicker, dust (240 specks), grain, vignette pulse
5. **SOUND MAP (library-first, assets/sfx/):** mk788 slam@title · mk1125 typewriter@text · mk790 riser@paint-on start · mk685 bass hit@element lands · mk494 heartbeat bed 0.42 · mk2393 rain 0.22 · afade out.
6. QC: side-by-side last-frame vs thumbnail before mux.

Reference render harness: playwright 540×960 dsf2, window.READY, renderAt((i+0.5)/30), 30fps.

## 6.8 🎬 SCENE TOOLBOX + SCENE-ACCORDING RULE — LOCKED (2026-10-24)
**User law: "ye cheez actual mein SCENE ACCORDING aani chahiye — na ki pehle se decide kab kya scene aayega."**
→ Story/script FIRST. Har beat khud decide karta hai treatment. Koi fixed scene order nahi. Styles = toolbox, story = boss.

**Approved scene treatments (tested on DBC assets, both user-approved):**
1. **LIVING POSTER** (§6.7) — hook/closer; thumbnail comes alive.
2. **EVIDENCE SYNC desk** (Visual Investigation; test: `assets/thumbtest/vi_test.html`) — dark ground #0B0C0E, timestamps ON evidence, T+ stopwatch, red #FF4A2E sync-lines converge, KNOWN/UNKNOWN columns, frozen decisive second. Use when: beat = timeline/multiple-sources/the-moment-it-happened.
3. **ARCHIVE LIGHT TABLE** (test: `assets/thumbtest/lt_test.html`) — backlit table flicker-on, real objects, loupe lands + 2.5× magnify, orange #FF5A1F anchors/readings/count-ups, verdict plate. Use when: beat = look-closer at ONE object/detail/number.
4. **Dossier paper cards** (dbc02 engine) — default narration fabric between the above.

Pick per beat, never force all into one video. Full style prompts: `docs/lemo-styles/` + craft laws in `docs/LEMO_OPUSCAR_MAP.md`.

## 7. METADATA FORMULA — LOCKED
- Title: curiosity 3-beat "He [did X], [took Y], and [vanished/was never Z]" + 1 emoji
- Desc: date-led story para + evidence hook para + "Comment A, B or C 👇" + "New unsolved mystery every day at 7 PM" + exactly 5 hashtags (#shorts first)
- ~20 tags; 7-9 PM IST (Fri/Sat best); NOT-kids; Altered-content YES; pinned comment = own stance + "A, B or C 👇"

## 8. STORY PICK RULES (unchanged Chronic lock)
Pillars V3/F2/H2/L2/S1. Auto-reject: true crime w/ victims glorified, paranormal-as-fact, recent tragedies, conspiracies. USA high-RPM topics first. English only.

## 🔒 ACTION-RECONSTRUCTION TEMPLATE (LOCKED 2026-10-25) — CHRONIC HOUSE STYLE
Jab bhi story me MOTION/ACTION moment aaye (jump, crash, chase, takeoff, sinking, last signal):
**Template: explainer-pipeline/assets/fun61/dbtest/jumptest.html** (THE JUMP test = reference bar)

RIG CHECKLIST (sab reusable code blocks):
1. PHOTOREAL AI-STILL base (LAW 1) + code LIVING layer: bob/sway, nav/beacon blink lights, light-spill flicker
2. ATMOSPHERE: 2-layer seeded rain/wind streaks (angle+speed story ke saath badle), parallax cloud wisps, mist band (image seams feather), depth fog
3. ⚡ LIGHTNING RIG: distant soft + ONE big flash (subject white-rim silhouette) + delayed thunder (mk1287 lowpass) + crack — flash 0.13s, physics delay realistic
4. PHYSICS FIGURE: tiny silhouette (hamesha SMALL = honest night/distance), accel gravity, tumble, 3-ghost motion trail, moon-halo glow (dark-on-dark BAND — halo+rim mandatory)
5. CAMERA FOLLOW: z 1.38->1.62 push during action, turbulence jitter grows with speed, world-coord follow
6. STORY PROPS: detail objects peel off (bills/debris) + colored chip w/ leader line mid-action
7. LENS DROPLETS after exposure to elements (sliding drop = handheld feel)
8. DATA TICKER: live ALT/time/speed counter in corner — one clock law
9. FREEZE FRAME finale: world freezes (ts=min(t,TF)), flash+grain, circle+"LAST ..." card, then distressed rubber stamp
10. SOUND = LAW 4.5 + story automation: engine fade DOWN as wind rises, heartbeat into freeze, SILENCE dip at freeze, double-layer slam. Melody ZERO.
QC: dark-subject visibility tiles MANDATORY (JUMP me figure 2 baar invisible mila tha).

## 🔒 WOW! SIGNAL = ACTIVE LONG-FORM #2 (2026-10-25)
Production doc: docs/WOW_SIGNAL_SCRIPT_v1.md (script+chapters+VO delivery law+sound map locked).
DUAL-VOICE LAW: [M] narrator storyteller + [F] "THE RECORD" (data/documents only, flat cold).
[F] never emotes, [M] never reads tables. Per-chapter atempo pacing table = law.
