# Video Pipeline Guide (`VIDEO-PIPELINE.md`)

1. **Stills & Contact Sheet Gate First (`--stills`):**
   - Render one representative still per shot and a phone-size contact sheet (`renders/<topic>-stills-sheet.png`).
   - Check anatomy/diagram readability, label placement, and caption safe zones (`y = 1420..1580`, `90px` horizontal margins) before encoding full video.
2. **VO & Word Alignment (`tools/align.py`):**
   - Synthesize Hindi VO via `kokoro-onnx` (`hf_beta`, `speed=1.1`) or load recorded human WAVs.
   - Run `faster-whisper` alignment against authoritative script words to generate word-level timings, `.srt` sidecar, and `@remotion/captions` JSON.
3. **2.5D Camera & Layered Overlays:**
   - Slow camera push/pan around `focus: [fx, fy]`, glowing signal rings/particles, flash cuts between shots, and word-synced callout labels.
4. **Post-Render QA:**
   - Verify with `ffprobe` (`1080x1920`, `30fps`, `h264` + `aac` audio stream, exact duration).
   - Keep final deliverables in `renders/` (persisted across workspace snapshots) in addition to `out/`.
