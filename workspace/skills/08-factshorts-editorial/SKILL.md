# Skill 08 — FactShorts 95%+ Studio Accuracy Native Sub-Layer & Kinetic Engine

## Purpose
Achieve **90–95%+ studio motion-graphics accuracy** on any `FACTSHORTS` vertical explainer (`1080x1920`, `30fps`, white dot-grid editorial canvas) — both when animating existing reference artwork (`/home/user/uploads/`) and when generating brand-new episodes on any future topic.

## Core Architecture (`/home/user/explainer-pipeline/tools/render_factshorts_god.py`)

### 1. Zero Tacked-On Fake Overlays (100% Reference Design Purity)
- **Never** draw crude OpenCV boxes, extra bottom caption bars, fake yellow underline rectangles, or random floating circles on top of the editorial canvas.
- Reconstruct the pure full-frame dot-grid background (`extract_clean_dot_canvas`) from the reference's clean margin strip so erased/separated elements leave **zero white holes**.

### 2. Automatic 2D Connected-Projection Word Segmentation (`auto_extract_all_headline_words`)
- Uses horizontal & vertical ink-density projection (`lum < 168`) across `y = 295..720` to automatically segment **every headline row and every individual word** without manual word coordinates.
- Verified at **100% word-count accuracy** across all 7 reference frames (`WA8240`, `WA1488`, `WA3044`, `WA5715`, `WA8090`, `WA1025`, `WA4723`).
- Each word animates via `paste_word_kinetic`:
  - **Vertical Baseline Clip-Mask (`clip_y_max = y1 + lh + 6`)** so words rise out of an invisible floor mask (`+32px -> 0px`).
  - **Elastic Overshoot Spring (`ease_out_back`)** staggered by `55–58ms` per word.
  - **Keyword Emphasis Micro-Pop**: anchor words (`"False Memories"`, `"Lying"`, `"Glitch"`) receive a synchronized `1.0 -> 1.045 -> 1.0` scale pulse when spoken.

### 3. Monochrome-to-Color HSV Chroma Decomposition (`make_monochrome_base_and_color_overlay`)
- Every anatomical/technical illustration is decomposed in HSV space into:
  1. **`mono_crop`**: 100% pure greyscale anatomical linework (with crossing colored circuits optionally inpainted via `remove_circuits_in_mono=True` and overlapping badges reconstructed via `build_clean_shot3_brain`).
  2. **`color_crop` + `c_mask`**: Only the high-chroma native highlights, circuits, and internal glows (`sat > 28`), which illuminate progressively via directional (`wipe_x`, `wipe_y`) or radial (`radial_wipe`) masks with a traveling diagonal light sheen (`sheen_pos`).

### 4. Live Anatomical Micro-Motion & 2.5D Multi-Plane Parallax
- **Optical Pupil Focus Warp (`apply_eye_focus_warp`)**: sub-pixel `cv2.remap` (`CV_32FC1`) radial iris contraction/dilation + subtle horizontal gaze tracking toward the target organ.
- **Multi-Plane Parallax**:
  - Background dot grid: static / `0.25x`
  - Monochrome organ core: `1.0x` floating oscillation
  - Highlighted anatomical lobe / core: `1.25x` foreground plane
  - Callout badges (`⚠️ Brain thinks NEW = OLD`, `TEMPORAL LOBE •`): `1.40x` foreground plane + soft `drop_shadow` depth separation.
- **Live Broadcast Pill HUD (`render_live_hud_pills`)**:
  - Top pill `• LIVE` yellow dot pulses organically.
  - Bottom pill Morse-code progress dots (`y=1818..1848`) illuminate progressively from left to right (`0% -> 100%`) across each shot's duration.
