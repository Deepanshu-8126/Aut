# Chronic C09 — V5 test and fix record

## Deliverable tested
`CHRONIC_DODECAHEDRON_TESTED_V5_1080_UPSCALED.mp4`, 31.8 s, 30 fps, 1080×1920 encoded after upscaling a 540×960 render. SHA-256 `34eaa87be47c13cb9a2e634ef598d944581b28c8b5e23eaf1740feafeee39968`. Native 540×960 companion SHA-256 `ed8455d6248583488072ffb59be4af569dcbee4c5b07057ae648e89c15fcc658`. Both full decode cleanly.

## Fixes and tests
- Previous music mix dropped the background bed approximately 21–28 s. Rebuilt continuous bed separately, then mixed original voice and mapped SFX from sources. Two prominent effects were reduced. Measured half-second pre-master voice-to-background-plus-effects gaps: 13.0 dB at 6.3 s and 11.6 dB at 18.8 s; background was present at 22.5 s. These sample measurements do not replace listening.
- Encoded file loudness −16.52 LUFS, true peak −1.88 dBTP (FFmpeg loudnorm analysis). No claim of subjective clarity.
- Real museum stills and labeled AI illustrations are matched to narration; a museum image explicitly says it is not the 2023 find. Theory imagery is labeled as illustration or unproven theory. The measuring-theory section was changed to a different Tongeren example.
- V5 cover names the Roman dodecahedron, and the question scene also displays the name. Four contact sheets sample the actual encoded video every 0.5 seconds (`V5_FINAL_SHEET_1–4.jpg`); they were inspected, alongside the thumbnail feed-size simulation. This is sampled review, not a human full-speed watch.
- `PREFLIGHT_V5.txt` and `TEST_V5/report.json` are actual V5 local-tool outputs: 94/100 local preflight proxy; estimated 15 visual events, 4.72/10 s; longest detected frozen stretch 1 s; loop frame difference 11.4; estimated dead-air ratio .028. These are heuristic software measurements, not YouTube retention, impressions, views, CTR or a guarantee. The tool's 1080 pass identifies encoded dimensions, not genuine source detail.
- YouTube US autocomplete on 2026-10-31 returned the exact term and suggestions including mystery, purpose, and knitting. This is not verified search volume, saturation, channel analytics or performance.

## Remaining gates — do not treat the tool's SHIP label as publication approval
1. Master pipeline's stricter Chronic duration override is 15–20 s; this cut is 31.8 s (an older Chronic document allows 25–35 s). A compliant shorter edit requires a new script/voice and re-edit.
2. Stricter visual-event target is ≥5/10 s; measured 4.72. Opening detail/edge score 6.5 misses the preflight target >8.
3. Spoken name does not occur in the first 2 seconds or elsewhere: voice says 'Roman object'. The actual name appears onscreen and in title, which does not satisfy the spoken-keyword gate.
4. Still photos are animated; there is no real moving excavation footage. 1080p is an upscale, not native HD.
5. Full human watch/listen on phone and headphones, word-level caption timing, facts, applicable AI disclosure, and current asset/music/SFX license verification remain required. Automated alignment and proxy tests do not establish those outcomes.
6. The 3-second human viewer test, search demand/competition validation, and post-publication 72-hour and 21-day analytics remain unavailable. No actual YouTube performance is claimed.

See `UPLOAD_KIT_V5.txt` for title, description, credits, pinned comment and captions. The old pre-V5 upload ZIP and old FINAL file are superseded, not deleted.
