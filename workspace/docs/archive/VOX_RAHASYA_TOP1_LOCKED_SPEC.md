# ⚠️ STATUS: LEGACY — ye Hindi-era CHRONIC template tha. 23-Oct reset ke baad Chronic pe apply NAHI hota (current = docs/CHRONIC_INDEX.md → Dossier Mode). Techniques (bloom/bezier/caption engine) reuse ke liye preserved.

# LOCKED SPEC — Vox / Johnny Harris / Fern Mystery ("Rahasya") Channel

- **Locked Gold Reference Video:** `/home/user/outputs/07-antarctica-mystery-vox.mp4` (`22.88s`, `1080x1920`, `30fps`)
- **Primary Skill Document:** `/home/user/skills/09-history-rahasya-doc/SKILL.md`
- **Scene & Shader Engine:** `/home/user/explainer-pipeline/tools/vox_antarctica_scenes.py`
- **Dynamic FX Library:** `/home/user/explainer-pipeline/tools/vox_dynamic_fx.py`
- **Master Renderer & Audio Mixer:** `/home/user/explainer-pipeline/tools/render_vox_history.py`

## Summary of Locked Rules for Every Future Topic (Short & Long Videos)
1. **85% Open Visual Cinema / Zero Box Clutter:** Max 1–2 frosted pointer pills (`draw_minimal_pointer_pill`, clamped inside `x=68..1012`). Never put bottom metric tables or multi-row text boxes above captions.
2. **Top 1% Editorial Font Pairing (`draw_top1_editorial_header`):**
   - `Inter-Black.ttf` (`52px` white) + `PlayfairDisplay-Italic.ttf` (`62px` colored accent) + `SpaceGrotesk-Bold.ttf` (`19px` kicker pill) over a soft top gradient vignette.
3. **True Shader Animations:**
   - 4x-downsampled dual-radius Gaussian optical bloom (`add_optical_bloom`).
   - Variable-width tapered Bezier curves & notched arrowheads (`draw_tapered_bezier_curve`).
   - Pressure-sensitive tapered brush circles (`draw_tapered_brush_circle`).
   - Photorealistic textured 3D cutaways & barrel-distorted (`cv2.remap`) glass magnifying loupes with specular reflection.
4. **Borderless Floating Captions:**
   - Mixed-case `Inter-Black.ttf` (`50px`), 3–4 words per chunk over a soft bottom vignette, rounded tactile active-word pill (`radius=14px`), and thin `3px` progress bar at `y=1805`.
5. **Mixkit Audio Pipeline:**
   - Real Mixkit stock background music (`bgm_188_30s.mp3`, `bgm_671_30s.mp3`) with sidechain ducking + real Mixkit foley SFX (`cinematic_boom`, `marker_swipe`, `paper_turn`, `ui_pop`).
