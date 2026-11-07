# Chronic C09 V6 — review and testing

Tested file `CHRONIC_ROMAN_V6_1080_UPSCALED.mp4`, SHA-256 `f542e88794b7c8d9530781e56a796a51d22648e95460b4fc0c0ea61e134af23b`; 16.8 s, 30 fps, 1080×1920 upscale from a 540×960 render. Native companion and upscaled video both full-decode passed.

## Changes from V5
- Rescripted, regenerated voice-30 and re-edited the video to 16.8 seconds. Approximate automatic word alignment places the complete spoken phrase 'Roman dodecahedron' at 0.70–1.92 seconds including the voice delay; human confirmation remains necessary.
- Rebuilt all scene timing and caption draft for the new voice. Alternate museum image at 0.5s improves first-two-second visual change; theories are shown as unproven and the 2023 scene labels the museum example as not the actual find.
- New music bed and SFX mix built from original sources, not stacked over V5. Reduced two cues after quantitative voice/background inspection. In 0.24s pre-master samples, voice-to-combined-background gaps at 6.95 and 15s improved from 11.0 and 9.6 dB to 13.5 and 15.7 dB respectively. Not a substitute for listening.
- 34 images sampled at 0.5s intervals from final encoded output, inspected. Natural Earth map and museum photos reused with credits; AI knitting illustration is labeled.

## Actual local test results
- `PREFLIGHT_V6.txt`: **96/100**, not 100. First-frame contrast std 55, edge 4.6 versus requested >8; scored 6/10 on first-frame punch. Upscale affects the detail available, and the score is resolution-dependent; it is a heuristic, not a real audience result.
- `TEST_V6/report.json`: 8.33 estimated visual changes/10s, zero detected static holds, first-two-second motion proxy pass, loop difference 1.2, dead-air ratio 0.015. The tool counts change events, not verified editorial cuts or YouTube swipes.
- Final encode FFmpeg loudnorm: −16.43 LUFS integrated, −1.89 dBTP. No claims about subjective clarity without human listening.
- No verified real YouTube impressions, CTR, retention, search volume or 72h outcomes. Autocomplete suggests possible phrases, not demand.

## Remaining checks
Not all gates pass: opening edge proxy remains below target. Human full-speed watch/listen, caption spelling/timing and pronunciation, 3-second audience test, fact/rights/license verification and applicable AI disclosure remain outstanding. 1080p is an upscale, and the pictures are animated stills, not moving excavation footage. Do not interpret a local score or tool's SHIP label as publication approval.
