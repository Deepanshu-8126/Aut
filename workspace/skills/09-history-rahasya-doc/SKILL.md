# Skill 09 — LOCKED Top 1% Creator Documentary & Mystery ("Rahasya") Engine (v9 Viral Shorts Gold Master)

> **STATUS: LOCKED BY USER ("omgggg you boomeeddddddd itsss toooo bestt esa hi kuch mey expectt karra tha yarr finally mydrea")**
> **Gold Benchmark Deliverables:**
> - **#1 Viral Shorts Gold Master (`9:16`, Pure Visuals + Real Moving Stock Videos):** `/home/user/outputs/09-mansa-musa-desert-treasure.mp4` (`44.23s`, `1080x1920`, `30fps`, `7.7 MB`)
> - **#1 Widescreen Long-Form Documentary Gold Master (`16:9`, 11+ Minutes):** `/home/user/outputs/10-dwarka-submerged-city-documentary-16x9.mp4` (`11m 08s` / `668.18s`, `1920x1080`, `24fps`, `65.2 MB`, 6 Chapters, 24 Unique Scenes + `.srt` Sidecar)
> **Core Engine Files:**
> - `/home/user/explainer-pipeline/tools/vox_mansa_scenes.py` (v9 Pure-Visuals + Real Moving Mixkit Video + Zero-Tiny-Font `9:16` Viral Shorts Engine)
> - `/home/user/explainer-pipeline/tools/dwarka_16x9_scenes.py` & `/home/user/explainer-pipeline/tools/render_dwarka_16x9.py` (v10 Widescreen `16:9` `1920x1080` Long-Form Documentary Engine with 24 unique archaeological/forensic scenes & resumable per-scene segment encoding)
> - `/home/user/explainer-pipeline/tools/vox_earhart_scenes.py` & `/home/user/explainer-pipeline/tools/vox_antarctica_scenes.py` (Shader, Cutaway, Loupe, & Comparison Board Engines)
> - `/home/user/explainer-pipeline/tools/render_vox_history.py` (Master Frame, RMS-Normalized Mixkit BGM, & Caption Pipeline)

---

## PART 1: MISTAKES NEVER TO REPEAT (STRICT BAN LIST)

1. **NEVER Stuff the Screen with Text or Stacked Boxes ("pure screen mey text bhare hey"):**
   - **BANNED:** Putting 5–8 rectangular cards/boxes or 12–18 lines of text on screen at once.
   - **BANNED:** Adding a bottom horizontal metric table (`y=1150..1450`) above the captions when the narrator is already speaking the explanation.
   - **BANNED:** Long subheads, multi-row text tables, or corner telemetry boxes that compete with the main visual.
   - **RULE:** Keep **85%+ of the vertical frame pure visual cinema**. Allow **at most 1 or 2 compact 2-word frosted pointer pills** (`draw_minimal_pointer_pill`) on the entire canvas.

2. **NEVER Use Squished All-Caps Barcode Fonts (`BebasNeue` / `Oswald` Everywhere):**
   - **BANNED:** Using tall narrow condensed all-caps (`BebasNeue-Regular.ttf`, `Oswald-Bold.ttf`) for both headlines and captions, or putting solid yellow/black rectangular banners behind every title.
   - **RULE:** Always use **Editorial Mixed Typography** (`draw_top1_editorial_header`):
     - Line 1: Wide geometric sans **`Inter-Black.ttf` (`52px`, `#FFFFFF`)**
     - Line 2 (Accent): Luxury editorial serif **`PlayfairDisplay-Italic.ttf` (`62px`)** in scene-matched cinema accent (`#6EE6FF` Ice Cyan, `#F6C85F` Warm Gold, or `#FF4E6A` Signal Coral) with a subtle animated underline and soft top vignette (zero boxy header plates!).

3. **NEVER Draw Flat MS-Paint PIL Polygons, Uniform Neon Lines, or Flat Circles:**
   - **BANNED:** Flat solid-color PIL `d.polygon` diagrams (`fill=(140, 205, 242)`), uniform-width PIL `d.line` arrows, or flat yellow circles without optical bloom or lens refraction.
   - **RULE:** Every animated graphic must use **True Shader Glow & Photorealistic Textures**:
     - **Optical Bloom (`add_optical_bloom`):** 4x-downsampled dual-radius Gaussian bloom (`sigma1=16`, `sigma2=5`) screen-blended around a crisp white-hot core.
     - **Tapered Bezier Curves (`draw_tapered_bezier_curve`):** Variable stroke thickness (`sin(frac * pi)^0.7`) from a thin tail to a thick glowing body + geometric notched arrowhead.
     - **Organic Pressure Brush Circle (`draw_tapered_brush_circle`):** Hand-drawn tapered spotlight ring with pressure falloff + optical bloom.
     - **Photorealistic Textured Cutaways:** Map real photographic textures (`antarctica_glacier.jpg`, rock/brick strata) into 3D cross-sections with depth-attenuation shaders, 3D slope-shaded terrain ridges, and caustic water shaders.
     - **Barrel-Distorted Optical Glass Loupe:** Use `cv2.remap` barrel distortion (`1.0 - 0.22 * r^2`), upper-left curved glass specular reflection, deep drop shadow, and dark anodized bezel.

4. **NEVER Put a Giant Black Rectangular Box Behind Bottom Captions:**
   - **BANNED:** Full-width dark rectangular docks (`[54, 1485, 1026, 1695]`) at the bottom of the screen or all-caps condensed caption text.
   - **RULE:** Use **Borderless Floating Lower-Third Captions** over a soft bottom gradient vignette (`y=1500..1920`):
     - **3–4 words per chunk** in **Mixed-Case `Inter-Black.ttf` (`50px`)**.
     - Active spoken word pops (`pop_y = -6px`) inside a sleek **rounded tactile pill (`radius=14px`)** with scene-matched color (`#5FE4FF`, `#F6C85F`, or `#FF3E5F`) while other words float in crisp white with soft drop shadow.
     - Whisper-thin `3px` progress scrubber at `y=1805`.

5. **NEVER Let PIL Overwrite RGBA Alpha or Run Uncached Full-Frame Blur Loops:**
   - **BANNED:** Calling `ImageDraw.Draw(rgba_canvas, "RGBA").ellipse(..., fill=(R,G,B,A))` or `.polygon(..., fill=(R,G,B,A))` directly on `canvas` or on a real photograph layer (PIL replaces destination alpha with `A`, punching dark silhouette holes into real photos!). Always draw translucent overlays onto `ov = Image.new("RGBA", size, (0,0,0,0))` and call `canvas.alpha_composite(ov)`.
   - **BANNED:** Recomputing static 1080x1920 `np.mgrid` backgrounds per frame or running full-resolution `1080x1920` `cv2.GaussianBlur(sigma=18)` on every frame. Always cache static scene bases in `_STATIC_CACHE` and run optical bloom at `1/4` resolution (`270x480`) before bilinear upscaling.

6. **NEVER Put a Top Header Block (`Kicker Pill` + `Title` at `y=50..260`) or Tiny Fonts (`< 28px`) in Viral Shorts:**
   - **BANNED:** Putting a permanent 3-line top header block (`1324 AD • MALI EMPIRE` + `Title`) at the top of the frame in Shorts/Reels. It wastes the top 20% of the vertical screen, blurs at `0:00`, and distracts from the main visual.
   - **BANNED:** Any small font (`12px–20px` sub-labels, photo captions, or small chart axis text) inside images, cards, or pointer pills.
   - **RULE ("Pure Visuals + Bottom Captions Only"):** Let the **Main Visual start right at the top (`y=55..80`)** and fill the canvas down to `y=1410`. Every single on-screen number, card label, chart title, or pointer pill (`draw_bold_visual_pointer_pill`) must use **HUGE, PUNCHY `28px–54px` Bold/Black typography** with zero tiny sub-lines.

7. **NEVER Clone the Exact Same 6-Scene Earth-Map Skeleton Across Different Videos:**
   - **BANNED:** Reusing the same `Photo -> Zoom Earth Map -> Magnifying Glass -> Cutaway -> 2 Boxes -> Radar Globe` sequence with the same glass pointer pills for every script.
   - **RULE:** Design **topic-specific dynamic visual mechanics** for every script (e.g., for *Mansa Musa*: Live `$400B` Wealth Race Leaderboard, 3 Golden Caravan Loot Counters + Marching Camel Trail, Raining 24K Gold Coins + Plunging `-25%` Cairo Crash Chart, Sub-Surface Desert Dune Radar X-Ray, Clean Dual Museum Showcase, and Spinning 24K Golden Compass Rose).

8. **ALWAYS Include Official `CHRONIC OF HISTORIC` Branding & Animated Subscribe CTA:**
   - Place the official circular golden **`CHRONIC OF HISTORIC`** emblem (`chronic_of_historic_logo.png`) in the top-right (`x=936, y=48`) across all scenes.
   - In the final payoff scene, include the spoken + animated **`CHRONIC OF HISTORIC` Subscribe CTA Card** (`SUBSCRIBE` ──► `✓ SUBSCRIBED` with animated pointer cursor click, golden shockwave ring, and notification bell chime).

9. **ALWAYS Use Real Copyright-Free Moving HD Stock Videos (`Mixkit` `.mp4`) Across Scenes (Zero Repeated Static Images):**
   - **BANNED:** Reusing the same static photograph across multiple scenes (`Scene 2`, `Scene 4`, `Scene 6`).
   - **RULE:** Fetch topic-matched copyright-free Mixkit `.mp4` videos (`https://mixkit.co/free-stock-video/{topic}/` -> `https://assets.mixkit.co/videos/{id}/{id}-720.mp4`), pre-normalize them to `30fps` in `out/mixkit_vids/` (which is excluded from the `128 MB` workspace snapshot), and stream frames via `get_video_frame_rgba` with a single-decoder `cv2.VideoCapture` cache (releasing the previous decoder on scene switch so RAM stays `< 350 MB`).

---

## PART 2: DYNAMIC SCENE ROTATION FORMULA (SHORT & LONG VIDEOS)

For any new topic (30s Reel/Short or 5–15 min Long-Form Vox Documentary), dynamically rotate across these visual scene types every **3.5–5.5 seconds** so no two consecutive scenes share the same layout:
1. **3D Orbital / Polar / Satellite Globe & Shader Route Map** (`antarctica_polar_flight_radar` / `vox_map_pan_asia_routes`)
2. **Photorealistic Textured Geological / Architectural Cross-Section Cutaway** (`antarctica_4km_ice_cutaway` / `vox_xray_library_manuscript`)
3. **Full-Bleed Archival Cinema + Barrel-Distorted 2.5x Glass Magnifying Loupe** (`antarctica_blood_falls_investigation`)
4. **2.5D Floating Archival Evidence Desk + Golden Scanner Beam & Bezier Link Arcs** (`antarctica_treaty_declassified_board`)

---

## PART 3: AUDIO & MIXKIT SOUNDTRACK SPEC

- **Voiceover:** `en-US-AndrewMultilingualNeural` (or script-specified narrator) with exact `WordBoundary` / `faster-whisper` word timestamps and broadcast EQ (`highpass=f=70`, `130Hz` warmth, `3600Hz` presence).
- **Real Mixkit Background Music:** Fetch topic-matched atmospheric stock music from Mixkit (`assets/vox_antarctica/sfx/bgm_188_30s.mp3` *"Echoes"* + `bgm_671_30s.mp3` *"Piano Mystery"*) mixed with smooth sidechain voiceover ducking (`0.14` during speech, `0.30` in pauses).
- **Real Mixkit Foley SFX:** Layer `cinematic_boom.mp3`, `marker_swipe.mp3`, `paper_turn.mp3`, and `ui_pop.mp3` on scene cuts, pointer pops, and highlighter sweeps, loudness-normalized to `-14 LUFS`.

---

## PART 4: LOCKED PURE-CODE `THREE.JS` WEBGL 2.0 3D ENGINE (`11-Poompuhar v4` Style — ZERO IMAGES, ZERO BOXES, `30–40s`)

> **STATUS: LOCKED BY USER ("Ha yar yey tho kaafi dahi tha esme new new mast laga yar")**
> **Permanent Code Blueprint:** `/home/user/explainer-pipeline/tools/render_poompuhar_webgl.py` (Persists forever in workspace even if `.mp4` outputs are deleted to save disk space).
> **Gold Master Deliverable:** `/home/user/outputs/11-poompuhar-lost-city-short.mp4` (`37.43s`, `1080x1920`, `30fps`, `CRF 16`, `16.0 MB`).

Whenever the user asks for a **History / Mystery ("Rahasya") Short (`30–40s`)** in the **Pure-Code 3D Animation Style** (even if all `.mp4` reference videos have been deleted from `/home/user/outputs/`), clone the architecture of `/home/user/explainer-pipeline/tools/render_poompuhar_webgl.py` with these **7 Non-Negotiable Rules**:

1. **100% Pure-Code `Three.js` WebGL 2.0 3D World (`Zero External JPEG/PNG Photos`):**
   - Render via Headless Chromium (`PLAYWRIGHT_BROWSERS_PATH=/opt/playwright/browsers`, `--use-gl=angle --use-angle=swiftshader --enable-webgl`) at native `1080x1920` with `THREE.ACESFilmicToneMapping` (`exposure=1.22`) and `renderer.shadowMap.enabled = false` for fast CPU rendering.
   - Build every historical artifact, building, wave, ship, terrain, or megalith procedurally in `Three.js` (`LatheGeometry`, vertex-displaced `PlaneGeometry`, `QuadraticBezierCurve3` + `TubeGeometry`, `TorusGeometry`, `PolarGridHelper`, and a `650`-particle 3D `Points` marine-snow/dust system) paired with glowing wireframe X-ray overlays (`matGoldWire` / `matCyanWire` / `matEmeraldScan`).
2. **Zero Rectangular Boxes or Card Frames (`Frameless Open-Canvas HUD`):**
   - Never draw rectangular Polaroid frames, card containers, or boxed panels.
   - Keep **top-left frameless floating typography** (`#floating-hero-stat` at `top: 64px; left: 58px`):
     - Kicker telemetry: `JetBrainsMono-Bold.ttf` (`23px`, `#5FE4FF`, letter-spacing `2.5px`)
     - Main Hero Stat: `Inter-Black.ttf` (`62px`, `#FFFFFF`, heavy text-shadow)
     - Subtitle: `PlayfairDisplay-Italic.ttf` (`56px`, `#F6C85F` Gold, heavy text-shadow)
3. **Real-Time 3D-Projected (`camera.updateMatrixWorld(true)` + `vec3.project(camera)`) Curved SVG Pointers:**
   - Every scene has **2 floating capsule callouts** (`#pt-1` & `#pt-2`, `border-radius: 999px`) connected to exact 3D world coordinates via `<path d="M ... Q ...">` dashed SVG leader lines (`stroke-dasharray="10 6"`) and a double target ring (`r="10"` + `r="26"`).
   - **CRITICAL:** Always call `camera.updateMatrixWorld(true)` inside `projectTo2D(vec3)` right before `vec3.clone().project(camera)` so the 2D target dot lands **100% dead-center** on the moving 3D object.
4. **6 Distinct 3D Scenes Over `30–40 Seconds` (`~6s` per scene):**
   - Tighten voiceover WAVs (`atempo=1.28` if needed) so total runtime lands cleanly inside **`30–40 seconds`** (`~36–38s`).
   - Give every scene a completely different 3D camera path (`dive`, `globe orbit`, `tsunami sweep`, `sonar trench flythrough`, `holographic laser turntable`, `multi-gimbal astrolabe payoff`) and trigger an optical flash cut (`#flash-overlay`) + sub-bass whoosh on the first `0.14s` of every shot.
5. **Borderless Floating Lower-Third Captions (`#caption-container` at `bottom: 185px`):**
   - `3–4 words` per chunk (`1–2` lines) in mixed-case `Inter-Black.ttf` (`52px`), where the active spoken word pops (`translateY(-6px) scale(1.05)`) inside a glowing pill (`active-gold`, `active-cyan`, or `active-coral`).
   - Whisper-thin `5px` golden progress scrubber (`#scrubber-track`) at `top: 1810px`.
6. **Official `CHRONIC OF HISTORIC` Branding & Animated Subscribe CTA:**
   - Top-right `96×96` circular golden emblem (`#coh-watermark` at `top: 48px; right: 48px`).
   - Scene 6 includes `#cta-bar` (`bottom: 390px`) that animates at `u >= 0.54` from red `SUBSCRIBE` (`#EB2A48`) to gold `✓ SUBSCRIBED` (`#F6C85F`) synced to a `1568Hz + 2349Hz` golden bell chime.
7. **Mandatory Preview Contact Sheet Verification Before Full Render:**
   - Always run `--preview` first (`python3 tools/render_<topic>_webgl.py --preview`), inspect the 6-frame sheet via `read_file` to verify zero boxes, zero clipped 3D meshes, and dead-center 3D SVG pointers, and only then run the full `30fps` `CRF 16` encode + `.srt` export + `run_skill.py audit`.


---

## PART 5: 🔒 TEMPLATE 1A v2 — ENHANCED VISUAL SETUP (Map Engine + Real Images + Captions + Script Plan)

> **Diagnosis Date:** 2026-10-20 — Gold Masters `09-mansa-musa` & `10-dwarka` ke frames analyze
> karke yeh 8 galtiyan pakdi gayin. Har nayi Niche 1 video mein yeh v2 setup MANDATORY hai.

### 5.1 ❌ 8 MISTAKES FOUND IN OLD 1A VIDEOS (NEW BAN LIST)
1. **No real animated map** — location labels (`CAIRO`/`MALI` chips) photos par paste kiye
   gaye the. Vox ka signature animated route map hi missing tha. → AB `map_engine.py` USE KARO.
2. **Empty/late charts** — "EGYPT GOLD VALUE" chart screen par aaya aur 80% box khali tha
   (line end mein draw hui). → RULE: chart apne scene ke pehle **0.8s ke andar 60%+ fill** ho.
3. **Meaningless decoration particles** — Cairo photo par random gold confetti dots jo koi
   information nahi dete. → Har animated element ka narration se direct matlab hona chahiye.
4. **Repeated filler scenes** — 2 compass-dune scenes back-to-back (36s & 42s). → RULE: koi
   bhi visual type consecutive repeat NahI hoga (Scene Rotation PART 2 strictly enforce).
5. **Caption mid-phrase splits** — "one African / scorching Sahara" jaisi tooti lines + 3
   random highlight colors (yellow/blue/red pills). → Section 5.4 caption lock follow karo.
6. **Card-overload monotony** (doc 10) — har scene photo + stat-card same layout. → 8-beat
   visual variety plan (5.3) use karo.
7. **Static real images** — no Ken Burns, no parallax, no unified archival grade. → 5.5 spec.
8. **No pre-render visual beat plan** — visuals improvise hue, isliye random lage. → 5.3 ka
   script-plan table render se PEHLE likhna COMPULSORY hai.

### 5.2 🗺️ REUSABLE VOX MAP ANIMATION ENGINE (READY & VERIFIED)
- **Tool:** `explainer-pipeline/tools/map_engine.py`
  (demo verified: `/home/user/renders/map_engine_demo_mansa_route.mp4`, 10.5s, ~12 fps render)
- **Data:** REAL Natural Earth coastlines + country borders (`assets/world_110m.geojson` +
  `assets/world_borders_110m.geojson`) — Web-Mercator, koi external tile/API nahi.
- **Built-in:** camera pan + log-zoom keyframes, golden comet route line with glow, pin pops
  + pulse rings + label chips, title/era chips, live distance counter, compass rose,
  graticule, vignette + film grain — sab CHRONIC OF HISTORIC black-gold style mein.
- **Run:** `PYTHONPATH=/var/tmp/pydeps python3 map_engine.py --config route.json` → MP4 segment,
  jo master timeline mein concat/composite hota hai. Config schema file ke docstring mein hai.
- **RULE:** Har history/mystery video mein **kam se kam 1 map scene** (journey, empire extent,
  lost-city location, expedition route). Short = 1 map (6-9s), Doc 16:9 = 2-3 map scenes.

### 5.3 📝 8-BEAT SCRIPT → VISUAL PLAN (RENDER SE PEHLE YEH TABLE BHARO)
| Beat | Time (short) | Visual Type | Rule |
|---|---|---|---|
| 1 HOOK | 0-5s | ARCHIVE PORTRAIT (real image + Ken Burns + flash title) | Shock number/claim in first 2s |
| 2 CONTEXT | 5-11s | **MAP** (`map_engine.py` route/location reveal) | Era chip + distance counter |
| 3 EVIDENCE | 11-17s | REAL PHOTO + evidence card (1 card max) | Photo 70% frame, card 30% |
| 4 DATA | 17-23s | ANIMATED CHART/COMPARISON BAR | 60% fill within 0.8s |
| 5 MECHANISM | 23-29s | CUTAWAY/DIAGRAM (cross-section, how it worked) | Pure-code animation |
| 6 TWIST | 29-35s | MAP ZOOM-BACK ya 2nd archive + red string pin board | New info, not repeat |
| 7 PAYOFF | 35-41s | HERO WIDE (mystery unresolved visual) | 1 line punch |
| 8 CTA | 41-45s | Logo + SUBSCRIBED chip | CHRONIC OF HISTORIC branding |
- Visual types ki 8-beat sequence mein **koi bhi type 2 baar consecutive nahi**.
- Har beat likhte waqt: `NARRATION (words) | VISUAL TYPE | ON-SCREEN PROOF ELEMENT | MOTION`.
- 16:9 doc version: har beat ×4 duration, beat 3/4/5 rotate karke 3 chapters banao.

### 5.4 💬 CAPTION & SUBTITLE LOCK
1. Max 2 lines × max 4 words, split SIRF phrase boundary par (noun-phrase kabhi mat todo).
2. Ek hi accent system: WHITE text + **GOLD highlight pill sirf active word par**
   (`#F5C542` bg, black text); koi random blue/red pills nahi (red sirf danger words:
   "vanished", "cursed", "never found").
3. Captions y = 79% H, 68px Montserrat-Black/Inter-Black, 16px black stroke; safe margin 90px.
4. `.srt` sidecar HAMESHA export + `ffmpeg -i` + frame `read_file` verification se pehle
   kabhi "done" mat bolo (VIDEO_FACTS_EAR_SETUP.md discipline).

### 5.5 🖼️ REAL IMAGE SETUP (ARCHIVE LOOK)
1. **Source:** `image_search` tool → Wikimedia/public-domain preference → `uploads/` kabhi
   overwrite nahi; curated copies `explainer-pipeline/assets/images/<topic>/`.
2. **Unify grade (har image par same):** warm sepia-gold tone overlay (`#D4A843` @ 12%
   soft-light), contrast +8%, vignette 0.3, film grain 4-5%, gold 3px border + dark mat frame.
3. **Motion MANDATORY:** har real image par Ken Burns (scale 1.06→1.14 ya pan) + 2-layer
   parallax jahan subject alag ho sake; STATIC photo = BAN.
4. **Archival chips:** har real image ke saath source chip (`"TIMBUKTU MS • 1400s"`) — credibility.
5. Images legibly LARGE rakho (70%+ frame) — chhote thumbnails data-cards ke andar BAN.

### 5.6 ⚙️ PRODUCTION ORDER (HAR 1A VIDEO)
1. Script (words) → 2. **5.3 beat table** → 3. VO + word timestamps → 4. `image_search` +
   grade → 5. `map_engine.py` configs → 6. Scene renderers (PART 2 rotation) → 7. Mixkit SFX
   bed (PART 3) → 8. Mux + `.srt` → 9. PyAV frame sheets + `read_file` verify → 10. Deliver.

### 5.7 🗺️ MAP ENGINE v1.1 POLISH RULES (2nd Deep-Inspection Fixes — LOCKED)
1. **LAND-HUG RULE:** Zameeni routes (caravan/march/expedition) kabhi samundar cross nahi
   karenge — route config mein **unnamed via-waypoints** (`{"lon","lat"}` bina `"name"`) daalo
   jo coastline/desert road hug karein (demo: Taghaza→Murzuk→Siwa→Cairo→Suez→Hejaz→Mecca).
   Unnamed points par pin/label nahi banta, sirf route shape smooth hota hai.
2. **NO ORPHAN CHIPS:** Pin screen edge (30px) se bahar → pin + chip dono skip. Label chips
   90px safe-margin ke andar clamp hote hain, kabhi edge par cut nahi hote.
3. **Sparse waypoints = Catmull-Rom overshoot** — har 8-10° par ek via-point rakho warna curve
   bhatak kar sea/wrong region mein chali jati hai.
4. **Label collision:** per-point `"ldx"/"ldy"` offsets se chips ko route line se hata kar rakho.
5. **First-frame font race:** render loop se pehle warmup frame + `document.fonts.status ===
   'loaded'` wait (map_engine.py mein built-in).

---

## PART 6: 🔒 RAHASYA VISUAL VOCABULARY — 14 LOCKED VISUAL MODULES (Story-Beat → Visual Mapping)

> Niche 1 (CHRONIC OF HISTORIC) ki HAR video in 14 modules se banegi. Script ke har beat par
> table se module chuno — map ke alawa yeh POORA setup hai. Status: ✅ = pipeline mein ready,
> 🔨 = canvas-2D recipe (map_engine.py pattern par 1-file module banana hai).

### 6.1 STORY-BEAT → VISUAL MODULE MASTER TABLE
| Story Beat (script mein kya hai) | Module | Status |
|---|---|---|
| HOOK (shock fact / "gayab ho gaya") | M1 Archive Portrait Slam + M12 Headline | ✅ |
| History context (kab/kahan/kaun) | M2 Map Engine + M3 Timeline Ticker | ✅/🔨 |
| Journey/Route/Empire | M2 Map Engine (land-hug route) | ✅ |
| EVIDENCE (photo/artifact mila) | M4 Evidence Board (corkboard + red string) | 🔨 |
| FORENSIC analysis (zoom/scan/compare) | M5 Forensic Magnifier + M6 X-ray Scanner Wipe | 🔨/✅ |
| HIDDEN PLACE (gufa/vault/underwater) | M7 Satellite Zoom-In + M8 Underground Cutaway | 🔨 |
| Underwater khoj (Dwarka/Poompuhar) | M9 Sonar Ping Sweep | ✅ (Dwarka scenes) |
| Documents/manuscripts/letters | M10 Manuscript Quote Reveal | 🔨 |
| Numbers/data ("$400B", "27000 sainik") | M11 Data Counter + Scale Comparator | ✅ |
| News/announcement moment | M12 Torn Newspaper Spin-In | ✅ |
| Log/characters (raja, explorer, gawah) | M13 Character Dossier Card | 🔨 |
| TWIST/unsolved end | M14 Red-String Zoom-Out + "CASE OPEN" stamp | ✅ (stamp) |

### 6.2 MODULE SPECS (kya dikhega + motion rule)
- **M1 Archive Portrait Slam:** Real painting/photo full-frame, sepia-gold grade, scale
  1.18→1.06 slam-in + dust particles + title flash. Ken Burns MANDATORY (static BAN).
- **M2 Map Engine:** `tools/map_engine.py` (PART 5.2/5.7 rules — land-hug, via-points,
  comet route, pins, miles counter).
- **M3 Timeline Ticker:** Horizontal golden timeline, year chips (1324 ● 1325 ● 1337), camera
  slide + active year glow pop; era image thumbnails upar fade-in. Canvas-2D.
- **M4 Evidence Board:** Dark corkboard, polaroid-frame real photos pin hote hain ek-ek karke
  (rotation -4°..+4°), **red string** lines snap-connect with twang, chits ("LAST SEEN 1933").
  Rahasya ka SIGNATURE module — har mystery video mein 1 baar zaroor.
- **M5 Forensic Magnifier:** Real photo par golden magnifier circle (2.2x zoom lens region)
  path par ghoomta hai, ruk kar **"ENHANCE" ping** + detail chip ("NOTE THE SEAL — 1343 AD").
- **M6 X-ray Scanner Wipe:** `draw_split_xray_scanner_wipe` — photo par vertical scan line,
  peeche skeleton/blueprint/hidden layer reveal.
- **M7 Satellite Zoom-In:** Map Engine wide → pin pulse → white flash → real satellite/aerial
  photo crossfade → Ken Burns push-in → coordinates chip (`24.78°N 68.96°E`) typewriter.
  (Map + real image ka LOCKED combo — "hidden place" reveal ka standard.)
- **M8 Underground/Underwater Cutaway:** Side-view terrain cross-section (canvas layers:
  surface line, mitti/paani gradient bands), depth gauge -10m/-20m/-30m, hidden chamber/
  wreck golden glow + pulse rings. (Mansa gold-cache scene ka upgraded version.)
- **M9 Sonar Ping Sweep:** Radial sweep arm + expanding rings, blips light-up, depth telemetry
  (Dwarka engine mein ready — reuse).
- **M10 Manuscript Quote Reveal:** Aged parchment texture, quote typewriter/ink-fade in
  PlayfairDisplay Italic, source chip ("— IBN BATTUTA, 1352"), candle-light flicker vignette.
- **M11 Data Counter + Scale Comparator:** `draw_vox_scale_comparator` + big BebasNeue
  count-up numbers; comparison bars 0.8s ke andar 60%+ fill (PART 5.1 rule).
- **M12 Torn Newspaper Spin-In:** `draw_torn_newspaper_clipping` + spin/slam entrance,
  halftone photo + headline.
- **M13 Character Dossier Card:** File-folder khulti hai, portrait + naam plate + 3 stat
  lines (BORN/ROLE/FATE) stamp-in one-by-one; "CLASSIFIED" corner stamp.
- **M14 Red-String Zoom-Out + CASE OPEN:** Evidence board wide zoom-out, saare clues ek saath
  dikhte hain, `draw_stamp_slam` se red **"CASE STILL OPEN"** stamp + logo CTA.

### 6.3 HARD RULES
1. Ek video mein **min 5 alag modules**, koi module consecutive repeat nahi (PART 2 rotation).
2. Har real photo par motion (Ken Burns/parallax) + sepia-gold unify grade + source chip.
3. Har module CHRONIC OF HISTORIC palette mein: bg `#0B111E`, gold `#F5C542`/`#D4A843`,
   parchment `#F4E9D0`, danger red sirf mystery words par.
4. Har module entrance ≤ 0.5s (slam/pop/wipe), exit shutter-whip (`apply_shutter_whip_transition`).
5. SFX pairing: pin-slam = thud, red string = twang, magnifier ping = sonar chirp, stamp =
   heavy slam, map comet = soft whoosh (Mixkit bed PART 3).

---

## PART 7: 🔒 HINDI RAHASYA VIDEO SETUP (Voice + Captions + Script Formula)

### 7.1 🎙️ SMOOTH HINDI VOICE (VERIFIED 2026-10-20, USER-SELECTED)
- **🏆 LOCKED PRIMARY NARRATOR:** Agent platform voice **`voice-01`** (user ne audition
  mein side-by-side sun kar select kiya) — `generate_speech` tool se Devanagari text
  bol kar `.mp3` workspace mein save hota hai, phir pipeline mein mux.
  Demo: `renders/hindi_voice_test/narrator_locked_demo.mp3` (full hook→CTA).
  NOTE: `voice-01` sirf isi Agent session-flow se milta hai; naye session mein wahi
  pasand ki voice dubara `add_voice` audition se confirm karo.
- **Backup (scriptable pipeline):** `edge-tts --voice en-US-AndrewMultilingualNeural
  --rate=-5%` (Hindi bolta hai, warm-confident) — sample: `andrew_hindi_sample.mp3`.
- **❌ REJECTED by user:** `hi-IN-MadhurNeural` ("aawaj bekaar") — dubara use mat karna.
- **SMOOTHNESS KE 7 RULES (script likhte waqt):**
  1. **Pure Devanagari** likho — roman Hinglish TTS ko robotic banata hai.
  2. Chhote vaakya: **8-12 shabd max**, har vaakya ek saans.
  3. Pauses punctuation se: `,` chhota pause, `—` dramatic pause, `।` full stop,
     `...` suspense hang. SSML ki zaroorat nahi.
  4. **Numbers shabdon mein:** "चौदह सौ साल" (NOT "1400 साल"), "चार हज़ार मील"।
  5. English words Devanagari mein transliterate: "साइंटिस्ट", "कार्बन डेटिंग", "सोनार"।
  6. Har beat ke end par ek **sawaal ya hang** chhodo ("...तो वो गया कहाँ?").
  7. Hindi pace ≈ **2.1-2.4 shabd/sec** @ rate -6% → 45s short ≈ 100-110 shabd,
     word-budget pehle hi fix karo.
- **Word timestamps:** edge-tts timings nahi deta → syllable-weighted distribution
  (Devanagari maatra count se weight) ya `faster-whisper` (`language='hi'`) se transcribe.
- **HONESTY RULE (VIDEO_FACTS_EAR_SETUP.md):** Yeh synthetic TTS hai — kabhi real human
  voice mat bolna.

### 7.2 💬 HINDI CAPTIONS (VERIFIED)
- **Font:** `assets/fonts/NotoSansDevanagari-Black.ttf` — conjuncts (द्वा, क्या)
  chromium canvas + PIL (raqm ✓) dono mein sahi shape hote hain. Test frame verified.
- Caption spec same as PART 5.4 (2 lines × 4 shabd, gold pill active word, 14px stroke)
  — bas font `NotoDev` + size 60-64px (Devanagari taller hai, 68 → 62).
- Titles mix: English headers (BebasNeue/Cinzel) + Hindi captions (NotoDev) allowed —
  chips/labels English mein rakho (MAP labels, "CASE OPEN"), narration captions Hindi mein.
- `.srt` sidecar Hindi Devanagari mein hi export karo.

### 7.3 📝 HINDI 8-BEAT SCRIPT FORMULA (45s SHORT — HAR BEAT KE BOL + VISUAL)
| Beat | Time | Kya bolna hai (pattern) | Visual (PART 6) |
|---|---|---|---|
| 1 HOOK | 0-5s | Shock number + impossible claim: "चौदह सौ साल पहले, एक पूरा शहर रातों-रात समुद्र में डूब गया।" | M1 Portrait/City Slam |
| 2 CONTEXT | 5-11s | Kab/kahan/kaun: "ये है द्वारका — भगवान कृष्ण की नगरी..." | M2 Map + M3 Timeline |
| 3 EVIDENCE | 11-17s | "लेकिन उन्नीस सौ तिरासी में, समुद्र के नीचे मिला..." | M4 Evidence Board |
| 4 DATA | 17-23s | Number punch: "नौ हज़ार साल पुराना। पिरामिड से भी पुराना।" | M11 Counter/Compare |
| 5 MECHANISM | 23-29s | Kaise hua: "समुद्र का स्तर बढ़ा — और शहर... गायब।" | M8 Cutaway / M9 Sonar |
| 6 TWIST | 29-35s | Naya raaz: "पर असली रहस्य ये नहीं। असली रहस्य है..." | M5 Magnifier / M7 Satellite |
| 7 PAYOFF | 35-41s | Unsolved hang: "...तो सवाल ये है — इतिहास गलत है, या हम?" | M14 Red-String Zoom-Out |
| 8 CTA | 41-45s | Lock-in line (7.4 se) | Logo + SUBSCRIBED chip |

### 7.4 🪝 LOCKED HINDI HOOK & CTA TEMPLATES
**HOOKS (pehli line — 5 patterns):**
1. "____ साल पहले, ____ रातों-रात गायब हो गया। और आज तक कोई नहीं जानता क्यों।"
2. "ये तस्वीर देख रहे हो? इसमें एक ऐसा राज़ छुपा है जो ____ साल से दफ़न था।"
3. "साइंटिस्ट कहते हैं ये नामुमकिन है। फिर भी — ये मौजूद है।"
4. "दुनिया का सबसे अमीर आदमी... और उसका खज़ाना आज तक नहीं मिला।"
5. "इतिहास की किताबों में ये पन्ना क्यों फाड़ा गया?"

**CTAs (aakhri line — 3 patterns):**
1. "अगर ये राज़ यहीं तक पहुँचा है... तो अगला राज़ आपको ढूँढता हुआ आएगा। फ़ॉलो करना मत भूलना।"
2. "ऐसे ही दफ़न राज़ हर हफ़्ते — CHRONIC OF HISTORIC पर। सब्सक्राइब अभी।"
3. "कमेंट में बताओ — आपको क्या लगता है, सच क्या है?" (+ subscribe chip animation)
- CTA voice mein "फ़ॉलो/सब्सक्राइब" bolte waqt hi screen par M14 logo chip slam ho — audio-visual sync.

### 7.5 ⚙️ HINDI PRODUCTION ORDER
Script Devanagari (7.3 table + word budget) → edge-tts Madhur VO → syllable/whisper-hi
timestamps → PART 5.6 steps 4-10 (images, map configs, modules, SFX, mux, verify).

### 7.9 CTA LOGO SIZE RULE (USER-LOCKED, 2026-10-20)
- **End-scene channel logo MUST be BIG: `520px` diameter** (was 400px — user asked bigger: "last mey logo thoda bade karde").
- Applies to ALL future videos, every template/mode (1A, 1B, Hindi, English).
- Gold ring + glow shadow around circular-clipped logo stays as-is.
- Mode 1B architecture CONFIRMED LOVED by user (Wow Signal / Jupiter / Oumuamua trilogy):
  per-beat pure-code 3D scenes + frameless HUD callouts + borderless gold-word captions
  + circular CASE STILL OPEN seal + procedural SFX. Keep each topic's 3D world 100% fresh.

## 7.10 MODE 1D "ENGRAVED PLATE" (added 2026-10-20, TEST APPROVED-PENDING)
- Kit: drawn-by-code (illodev, MIT) Engrave engine integrated in our pipeline:
  `assets/dbc/{core.js,engrave.js,IMFellDWPicaSC-Regular.ttf}`.
- Look: charcoal on aged «Description de l'Égypte» plate; hand-cut stone mosaics,
  gold/live-blue second inks. Frame flags: charcoal:true, hatch:1, contour:1, course:0.012,
  ink #2e261d, paper #ebe1cb. Engrave scale 0.38 (SwiftShader budget ~5s/GL frame).
- Speed: output 24fps, GL "on twos" via layer key floor(t*12) — 2D furniture/captions smooth.
  27s video ≈ 25-30 min render (resumable frames). Plan long renders in 2+ calls.
- Furniture: plate double-rule border, running head DESCRIPTION DE L'ÉGYPTE / A.Vol.V / PL.IX
  (IM Fell), ink captions; OUR brand: emblem, 520px CTA logo, karaoke captions
  (ink #2e261d words, madder red #9E2B1E active — gold unreadable on paper).
- First test: outputs/22-great-pyramid-void-1d-short.mp4 (ScanPyramids Big Void).

### 7.11 MODE 1E "TABLETOP3D" (tested 2026-10-21, drawn-by-code kit)
- Kit: assets/dbc/tabletop3d.js + core.js (MIT). Raymarched GLSL miniature: PBR-lite,
  DOF (focus=cam distance, aperture 0.4), film grain, stop-motion on twos + nudge/flicker.
- Scene GLSL must define: map(p)->vec2(d,mat), albedo(m,p,n), material(m)=vec4(rough,metal,sss,relief?),
  relief(m,p). Prelude: sdBox/sdRoundBox/sdCapsule/sdRoundCone(p,a,b,r1,r2)/sdCylinder/sdTorus,
  rot, opU, noise, fbm, woodGrain, fibres, PF(i) params, uTex0 (canvas textures).
- SPEED RECIPE (2026-10-21): 8 unique drawings/s (floor(t*8)), render ONLY uniques,
  ffmpeg "-framerate 8 ... -r 24" duplicates to 24fps; scale 0.26, band 160.
  10s reel = 194s wall (was ~420s at 12/s+240 frames). Old: scale 0.30/band 96 ~2.4s/drawing.
  DBC_GPU not needed; works CPU (SwiftShader).
- Template recipe: desk wood + cutting mat + bg mug + sticky note (Patrick Hand canvas tex).
  Subject objects via PF params, hop(t0,t1,a,b,h) stop-motion arcs + settle wobble cos decay.
- Test master: outputs/25-tabletop3d-stonehenge-test.mp4 (10s). CHROME path now chromium-1248
  (playwright reinstall bumps version — update CHROME const when sandbox resets).

### 7.12 MODE 1C v3 "CINE-DOC" — THE UNIFIED DOCUMENTARY ENGINE (2026-10-21, USER DIRECTIVE)
USER RULE: Mode 1D and 1E are NO LONGER standalone modes. Everything folds into Mode 1C
as layers of ONE real-documentary engine. Reference master: outputs/26-colosseum-*.mp4,
script tools/render_colosseum_doc.py (single HTML page, 3 renderers coexist).
- L1 CINE: photoreal stills (real-type/AI gen, always "AI RECREATION" tag) + slams,
  hand circles, callouts, dataBars — the cinematic dark base.
- L4 PLATE INSERT (ex-Mode 1D): WHEN A BUILDING/STRUCTURE/MECHANISM APPEARS, cut to an
  engraved cross-section plate (Engrave kit, charcoal flags, scale 0.38, keys floor(t*12)).
  Page slides up into frame over dark bg (eob 0.55s + drop shadow) via offscreen plateCv
  (A2.apply resets transforms — never translate ctx directly). Plate furniture: double
  rules, latin running head per subject, IM Fell captions, inkCallout2, live-blue animated
  element (the machine moving). Captions switch to ink/red, shadowBlur 0.
  PORTRAIT GOTCHA: visible half-width = tan(fov/2)*camZ*(1080/1920); keep geometry inside.
- L5 TABLETOP INSERT (ex-Mode 1E role): "kahi kahi" — miniature desk model beats for
  reconstruction/scale/fun (tabletop3d kit, scale 0.26, keys floor(t*8), speed recipe 7.11).
  Subject model in GLSL SDF; stop-motion pops with nudge+flicker; sticky note gag.
- DYNAMIC CTA (every video, never the same twice): rotate variants —
  v1 dark still + gold logo (18-21,23) · v2 engraved plate CTA (22,24) · v3 tabletop desk
  CTA with red CASE STILL OPEN stamp over the model (26). Always: 520px logo, stamp/case
  element, SUBSCRIBE->SUBSCRIBED click. Invent new variants per subject.
- Cost: 39s = ~19 min render (cine fast, plate ~0.75fps, tabletop ~0.5fps segments).
