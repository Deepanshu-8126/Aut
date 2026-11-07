# MotionMaxxing Skill (`03-motion-directing/motionmaxxing/SKILL.md`)

## Purpose
Directing, 2.5D camera choreography, visual hierarchy, and audio-visual pacing rules for science/history/facts videos.

## Core Directing Rules
1. **Single Causal Visual Path:**
   - Every shot (`Shot 1..N`) must visually advance along a connected physical pathway (e.g., `Sound Wave → Pinna → Canal → Eardrum → Ossicles → Cochlea → Hair Cells → Nerve → Brain`).
2. **2.5D Camera Moves (`zoom_in`, `pan_right`, `push_focus`):**
   - Anchor camera movement on each shot's `focus: [fx, fy]` coordinates.
   - Smooth cubic easing (`u_ease = 1 - (1 - u)^3`) from `from_scale` (`1.00–1.04`) to `to_scale` (`1.12–1.15`).
3. **Visual Proof + Sourced Metric Per Shot:**
   - Top-right high-contrast `#FFD60A` metric badge displays the verified number + unit (`343 m/s`, `2.5 cm`, `0.1 mm`, `3 mm`, `22×`, `15,000`, `30,000`, `0.05 sec`, `85 dB`).
4. **Audio-Visual Lock (`-14 LUFS`):**
   - Ambient pad (`D minor 9th`) ducks automatically under narration (`0.11 → 0.045` gain when VO RMS > threshold).
   - Transition whoosh at `shot_start` + crystalline tick (`1480 Hz`) at each `label.trigger_sec`.
