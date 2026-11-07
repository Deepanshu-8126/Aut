# LEMO-OPUSCAR → HAMARI PIPELINE (integration map)
*Source: github.com/lemomo-ai/lemo-opuscar (MIT, free) — 59 film styles, 100% code, no video model.*
*Saved locally: `docs/lemo-styles/` (15 style prompts + TECHNIQUE.md + DIRECTOR.md). Full repo volatile at /var/tmp/lemo (re-clone anytime).*

## ⚖️ RULE OF USE (so our locks stay intact)
- 🔒 **Chronic = DOSSIER MODE remains law.** Lemo styles REPLACE nothing — they are a **technique mine**: we steal grammar/craft and inject into Dossier Mode.
- 🔒 SFX LAW, LIVING POSTER, VIRAL LAW, style locks (factshorts etc.) — all unchanged.
- Lemo style prompts may be used AS-IS only for **new experimental lanes** (user approval first).

## 🎯 WHAT WE ACTUALLY NEED (the user's question)

### A) CHRONIC (Dossier Mode) — inject from `chronic_visual-investigation.md` ⭐ TOP PICK
The demo is literally a Hindenburg disaster investigation = our genre. Steal:
1. **One clock, read in the picture** — timestamps ON evidence cards, `T+xx.x` stopwatch over decisive seconds, frozen "32 s". No permanent timeline band (eats frame).
2. **Sources meet at one moment** — payoff = 2+ independent sources pointing at same second/place; cut points = sync points.
3. **Uncertainty is drawn, not apologised** — `≈`, *inferred*, dashed boxes; known vs unknown as separate columns. (Perfect for unsolved mysteries — the UNKNOWN column IS the hook.)
4. **One accent color only** (#FF4A2E red in VI; ours = dossier red) — it only ever POINTS: circles, sync lines, highlights, the convergence zone.
5. **Archival footage pipeline (ffmpeg):** pre-1950 film max 2.5×: `bwdif=0` deinterlace → crop borders → `hqdn3d=2:2:3:3` → lanczos upscale → `unsharp=5:5:0.5` → greyscale, one shared grain (α 0.22 footage / 0.10 paper). Modern ≤1.5×. Never colourised copies.
6. **Restraint law:** no slo-mo of the catastrophe, casualties = counted dots + numbers, fire only inside evidence frames. (Matches our auto-reject rules.)
Also mine: `chronic_archive-lighttable.md` (paper-on-glass evidence desk), `chronic_satellite-briefing.md` + `chronic_lidar-survey.md` (earth mysteries / lost cities!), `chronic_newsreel.md` (pre-1950 era stories), `chronic_halftone-dossier.md` (print-texture tricks: halftone shading, stamp rendering, misregistration shadows), `chronic_spy-titles.md` (title sequences), `chronic_kino-montage.md` (pace).

### B) FUNCYOUS (mechanisms) — inject from `funcyous_teardown.md` ⭐ TOP PICK
Exploded-view product teardown in code = hamare "hidden mechanism" pillar ka exact tool. Also: `funcyous_briefing-board.md` (engineering board), `funcyous_blueprint.md`, `funcyous_iso-infographic.md` (process flows), `funcyous_white-model.md` (projection on white model — city/structure stories), `funcyous_dataviz.md`, `funcyous_microscope.md`.

### C) CRAFT UPGRADES (both channels) — from DIRECTOR.md + TECHNIQUE.md
- **Music grid FIRST:** write cue map before animating; picture locks to grid. (= our SOUND MAP TABLE, now with: vary pace, one acceleration, one breath/long take. "A film at one even speed has failed.")
- **Readability law:** subtitle hold ≥1.8s and ≥ spoken+0.6s; after text animates in, hold (letters÷15 + 1.5)s English; title cards ≥4s.
- **Camera law:** ≥4 different camera moves per film; ONE signature shot people remember; transitions designed inside the medium (no default fades).
- **Subject size:** key moments = subject ≥ 1/3 frame height.
- **Failure checklist (avoid):** subject too small/edge-pushed; colour-on-same-colour; subs covering subject; blank transition frames; effects that don't track after camera moves.
- TECHNIQUE.md §2: picture = pure function of time (we already do renderAt(t) ✅); §3 one timeline drives everything; §6 SFX mix; §9 3D notes; §10 code-rig characters.

## 🚀 ACTION PLAN (agreed path)
1. **c03 (next Chronic)** = Dossier Mode + VI injections: one-clock grammar, known/unknown columns, sync-point cuts, archival ffmpeg pipeline, restraint law. LIVING POSTER hook stays.
2. **Funcyous next mechanism video** = teardown-style exploded view segment (code), briefing-board labels.
3. Both: music-grid-first + camera law + readability law added to QC.
